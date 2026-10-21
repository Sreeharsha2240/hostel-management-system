from decimal import Decimal
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection, transaction
from django.db.models.deletion import ProtectedError
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import User
from audit.models import AuditEvent

from .models import Bed, Hostel, Room


class HostelModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hostel = Hostel.objects.create(name='Boys A', type=Hostel.Type.BOYS)
        cls.other = Hostel.objects.create(name='Girls A', type=Hostel.Type.GIRLS)

    def room(self, number='101', capacity=3, **kwargs):
        return Room.objects.create(
            hostel=kwargs.pop('hostel', self.hostel),
            room_number=number,
            capacity=capacity,
            floor=0,
            room_type=Room.Type.TRIPLE,
            fee_amount='5000.00',
            **kwargs,
        )

    def test_each_allowed_capacity_creates_exactly_that_many_available_beds(self):
        for capacity in range(1, 5):
            with self.subTest(capacity=capacity):
                room = self.room(number=str(capacity), capacity=capacity)
                self.assertEqual(
                    list(room.beds.values_list('bed_number', flat=True)),
                    [f'{capacity}-{chr(65 + index)}' for index in range(capacity)],
                )
                self.assertEqual(
                    set(room.beds.values_list('status', flat=True)), {'Available'}
                )

    def test_hostel_and_room_uniqueness_and_invalid_capacity(self):
        self.room()
        with self.assertRaises(ValidationError):
            self.room()
        self.room(hostel=self.other)
        with self.assertRaises(ValidationError):
            Hostel.objects.create(name='boys a', type='Boys')
        for capacity in (0, 5):
            with self.subTest(capacity=capacity), self.assertRaises(ValidationError):
                self.room(number=f'bad{capacity}', capacity=capacity)
        self.assertEqual(Room.objects.count(), 2)

    def test_database_rejects_capacity_outside_one_to_four(self):
        room = self.room()
        with self.assertRaises(IntegrityError), transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(
                    'UPDATE hostels_room SET capacity = %s WHERE id = %s', [5, room.pk]
                )
        room.refresh_from_db()
        self.assertEqual(room.capacity, 3)

    def test_capacity_updates_preserve_existing_beds_and_do_not_duplicate(self):
        room = self.room(capacity=2)
        original = list(room.beds.values_list('pk', flat=True))
        Bed.objects.filter(pk=original[0]).update(status=Bed.Status.MAINTENANCE)
        room.save()
        self.assertEqual(room.beds.count(), 2)
        room.capacity = 4
        room.save()
        self.assertEqual(room.beds.count(), 4)
        self.assertEqual(list(room.beds.values_list('pk', flat=True))[:2], original)
        self.assertEqual(room.beds.get(pk=original[0]).status, Bed.Status.MAINTENANCE)

    def test_shrinking_capacity_removes_only_available_excess_beds(self):
        room = self.room()
        retained = list(room.beds.values_list('pk', flat=True))[:2]
        room.capacity = 2
        room.save()
        self.assertEqual(list(room.beds.values_list('pk', flat=True)), retained)
        self.assertEqual(room.beds.count(), 2)

    def test_shrinking_with_occupied_or_maintenance_excess_bed_rolls_back(self):
        room = self.room()
        extra = room.beds.get(position=3)
        for status in (Bed.Status.OCCUPIED, Bed.Status.MAINTENANCE):
            extra.status = status
            extra.save()
            room.capacity = 2
            with self.assertRaises(ValidationError):
                room.save()
            room.refresh_from_db()
            self.assertEqual(room.capacity, 3)
            self.assertEqual(room.beds.count(), 3)

    def test_bed_with_protected_history_cannot_be_removed(self):
        room = self.room()
        room.capacity = 2
        with patch.object(Bed, 'delete', side_effect=ProtectedError('history', [])):
            with self.assertRaises(ValidationError):
                room.save()
        room.refresh_from_db()
        self.assertEqual(room.capacity, 3)
        self.assertEqual(room.beds.count(), 3)

    def test_room_rename_updates_bed_labels_without_replacing_records(self):
        room = self.room()
        ids = list(room.beds.values_list('pk', flat=True))
        room.room_number = '202'
        room.save()
        self.assertEqual(list(room.beds.values_list('pk', flat=True)), ids)
        self.assertEqual(
            list(room.beds.values_list('bed_number', flat=True)),
            ['202-A', '202-B', '202-C'],
        )

    def test_bed_creation_failure_rolls_back_room_and_preceding_beds(self):
        save = Bed.save

        def fail_second_bed(bed, *args, **kwargs):
            if bed.position == 2:
                raise RuntimeError('simulated storage failure')
            return save(bed, *args, **kwargs)

        with (
            patch.object(Bed, 'save', new=fail_second_bed),
            self.assertRaises(RuntimeError),
        ):
            self.room()
        self.assertEqual(Room.objects.count(), 0)
        self.assertEqual(Bed.objects.count(), 0)

    def test_partial_room_save_does_not_sync_unsaved_capacity(self):
        room = self.room(capacity=2)
        room.capacity = 4
        room.fee_amount = '6000.00'
        room.save(update_fields=['fee_amount'])
        room.refresh_from_db()
        self.assertEqual(room.capacity, 2)
        self.assertEqual(room.beds.count(), 2)

    def test_bulk_room_changes_that_bypass_bed_generation_are_rejected(self):
        room = self.room()
        original_beds = list(room.beds.values_list('pk', 'bed_number', 'status'))
        with self.assertRaises(ValidationError):
            Room.objects.filter(pk=room.pk).update(capacity=1)
        with self.assertRaises(ValidationError):
            Room.objects.bulk_create([Room()])
        for field, value in (
            ('capacity', 1),
            ('room_number', '202'),
            ('hostel', self.other),
            ('hostel_id', self.other.pk),
        ):
            with self.subTest(field=field):
                setattr(room, field, value)
                with self.assertRaises(ValidationError):
                    Room.objects.filter(pk=room.pk).bulk_update([room], [field])
                room.refresh_from_db()
                self.assertEqual(room.room_number, '101')
                self.assertEqual(room.capacity, 3)
                self.assertEqual(room.hostel_id, self.hostel.pk)
                self.assertEqual(
                    list(room.beds.values_list('pk', 'bed_number', 'status')),
                    original_beds,
                )

    def test_bulk_room_fee_and_floor_updates_preserve_generated_beds(self):
        room = self.room()
        original_beds = list(room.beds.values_list('pk', 'bed_number', 'status'))
        room.floor = 1
        room.fee_amount = Decimal('6000.00')
        updated = Room.objects.filter(pk=room.pk).bulk_update(
            [room],
            ['floor', 'fee_amount'],
        )
        self.assertEqual(updated, 1)
        room.refresh_from_db()
        self.assertEqual(room.floor, 1)
        self.assertEqual(room.fee_amount, Decimal('6000.00'))
        self.assertEqual(
            list(room.beds.values_list('pk', 'bed_number', 'status')),
            original_beds,
        )

    def test_bed_validation_and_hostel_type_change_protect_occupied_beds(self):
        room = self.room()
        with self.assertRaises(ValidationError):
            Bed.objects.create(room=room, position=4)
        bed = room.beds.first()
        bed.status = Bed.Status.OCCUPIED
        bed.save()
        self.hostel.type = Hostel.Type.GIRLS
        with self.assertRaises(ValidationError):
            self.hostel.save()
        bed.status = 'invalid'
        with self.assertRaises(ValidationError):
            bed.save()


class HostelViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            username='hostel-admin', role=User.Role.ADMIN
        )
        cls.warden = User.objects.create_user(
            username='hostel-warden', role=User.Role.WARDEN
        )
        cls.student = User.objects.create_user(
            username='hostel-student', role=User.Role.STUDENT
        )
        cls.hostel = Hostel.objects.create(name='Boys B', type=Hostel.Type.BOYS)
        cls.room = Room.objects.create(
            hostel=cls.hostel,
            room_number='101',
            capacity=3,
            floor=0,
            room_type=Room.Type.TRIPLE,
            fee_amount='5000.00',
        )

    def test_only_admin_can_write_even_with_direct_post_or_patch(self):
        for account in (self.warden, self.student):
            self.client.force_login(account)
            for url, data in (
                (reverse('hostel-list'), {'name': 'Forbidden', 'type': 'Boys'}),
                (
                    reverse('hostel-update', args=[self.hostel.pk]),
                    {'name': 'Forbidden', 'type': 'Boys'},
                ),
                (
                    reverse('room-create', args=[self.hostel.pk]),
                    {
                        'room_number': '102',
                        'capacity': 2,
                        'floor': 0,
                        'room_type': 'Double',
                        'fee_amount': 100,
                    },
                ),
                (
                    reverse('bed-update', args=[self.room.beds.first().pk]),
                    {'status': 'Maintenance'},
                ),
            ):
                with self.subTest(role=account.role, url=url):
                    self.assertEqual(self.client.post(url, data).status_code, 403)
                    if url != reverse('hostel-list'):
                        self.assertEqual(
                            self.client.patch(
                                url, data, content_type='application/json'
                            ).status_code,
                            403,
                        )
        self.assertEqual(Hostel.objects.count(), 1)
        self.assertEqual(Room.objects.count(), 1)
        self.assertEqual(self.room.beds.filter(status='Available').count(), 3)

    def test_warden_can_read_but_student_cannot_read_staff_records(self):
        for account, expected in ((self.warden, 200), (self.student, 403)):
            self.client.force_login(account)
            for name, args in (
                ('hostel-list', []),
                ('hostel-detail', [self.hostel.pk]),
                ('available-beds', []),
            ):
                with self.subTest(role=account.role, name=name):
                    response = self.client.get(reverse(name, args=args))
                    self.assertEqual(response.status_code, expected)
                    if expected == 200:
                        self.assertNotContains(response, reverse('hostel-create'))

    def test_admin_json_creation_and_automatic_beds_are_audited(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse('hostel-list'),
            {
                'name': 'Girls B',
                'type': 'Girls',
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        hostel_id = response.json()['id']
        response = self.client.post(
            reverse('room-create', args=[hostel_id]),
            {
                'room_number': '202',
                'capacity': 2,
                'floor': 1,
                'room_type': 'Double',
                'fee_amount': '4000.00',
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            [bed['bed_number'] for bed in response.json()['beds']], ['202-A', '202-B']
        )
        self.assertEqual(
            AuditEvent.objects.filter(
                user=self.admin,
                action='create',
                record_type='hostels.bed',
            ).count(),
            2,
        )

    def test_duplicate_hostel_and_room_return_conflict_without_saving(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse('hostel-list'),
            {
                'name': self.hostel.name,
                'type': 'Boys',
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 409)
        response = self.client.post(
            reverse('room-create', args=[self.hostel.pk]),
            {
                'room_number': '101',
                'capacity': 2,
                'floor': 0,
                'room_type': 'Double',
                'fee_amount': '4000.00',
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(Room.objects.count(), 1)

    def test_invalid_room_fields_and_malformed_json_are_rejected(self):
        self.client.force_login(self.admin)
        url = reverse('room-create', args=[self.hostel.pk])
        valid = {
            'room_number': '102',
            'capacity': 2,
            'floor': 0,
            'room_type': 'Double',
            'fee_amount': '4000.00',
        }
        for field, value in (
            ('capacity', 5),
            ('floor', -1),
            ('fee_amount', '-1'),
            ('room_type', 'other'),
            ('room_number', "' OR 1=1"),
        ):
            with self.subTest(field=field):
                response = self.client.post(
                    url, {**valid, field: value}, content_type='application/json'
                )
                self.assertEqual(response.status_code, 400)
        self.assertEqual(
            self.client.post(url, '[', content_type='application/json').status_code, 400
        )
        self.assertEqual(Room.objects.count(), 1)

    def test_available_beds_filter_floor_zero_type_and_hostel_and_exclude_nonavailable(
        self,
    ):
        first, second, third = self.room.beds.all()
        Bed.objects.filter(pk=second.pk).update(status=Bed.Status.OCCUPIED)
        Bed.objects.filter(pk=third.pk).update(status=Bed.Status.MAINTENANCE)
        other = Hostel.objects.create(name='Other', type='Girls')
        Room.objects.create(
            hostel=other,
            room_number='101',
            capacity=1,
            floor=1,
            room_type='Single',
            fee_amount=0,
        )
        self.client.force_login(self.warden)
        url = reverse('available-beds')
        response = self.client.get(
            url,
            {
                'hostel': self.hostel.pk,
                'floor': 0,
                'room_type': 'Triple',
            },
            HTTP_ACCEPT='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual([bed['id'] for bed in response.json()['beds']], [first.pk])
        self.assertEqual(
            self.client.get(
                url, {'floor': 'bad'}, HTTP_ACCEPT='application/json'
            ).status_code,
            400,
        )

    def test_room_and_bed_can_be_updated_through_html_and_json(self):
        self.client.force_login(self.admin)
        response = self.client.patch(
            reverse('room-update', args=[self.room.pk]),
            {
                'room_number': '103',
                'capacity': 4,
                'floor': 1,
                'room_type': 'Triple',
                'fee_amount': '6000.00',
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.room.beds.count(), 4)
        bed = self.room.beds.first()
        response = self.client.post(
            reverse('bed-update', args=[bed.pk]), {'status': 'Maintenance'}
        )
        self.assertEqual(response.status_code, 302)
        bed.refresh_from_db()
        self.assertEqual(bed.status, 'Maintenance')

    def test_audit_failure_rolls_back_room_and_automatic_beds(self):
        self.client.force_login(self.admin)
        with patch(
            'hostels.services.record_event', side_effect=RuntimeError('audit failed')
        ):
            with self.assertRaises(RuntimeError):
                self.client.post(
                    reverse('room-create', args=[self.hostel.pk]),
                    {
                        'room_number': '105',
                        'capacity': 2,
                        'floor': 0,
                        'room_type': 'Double',
                        'fee_amount': 100,
                    },
                )
        self.assertFalse(Room.objects.filter(room_number='105').exists())
        self.assertEqual(Bed.objects.count(), 3)

    def test_html_forms_csrf_and_missing_records(self):
        self.client.force_login(self.admin)
        for name, args in (
            ('hostel-create', []),
            ('hostel-update', [self.hostel.pk]),
            ('room-create', [self.hostel.pk]),
            ('room-update', [self.room.pk]),
            ('bed-update', [self.room.beds.first().pk]),
        ):
            self.assertEqual(self.client.get(reverse(name, args=args)).status_code, 200)
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.admin)
        self.assertEqual(
            csrf_client.post(
                reverse('hostel-list'),
                {
                    'name': 'No CSRF',
                    'type': 'Boys',
                },
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.get(reverse('hostel-detail', args=[999999])).status_code, 404
        )

    def test_hostel_names_are_escaped_when_displayed(self):
        Hostel.objects.create(name='<script>alert(1)</script>', type='Boys')
        self.client.force_login(self.warden)
        response = self.client.get(reverse('hostel-list'))
        self.assertContains(response, '&lt;script&gt;alert(1)&lt;/script&gt;')
        self.assertNotContains(response, '<script>alert(1)</script>')
