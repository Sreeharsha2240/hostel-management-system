from datetime import date, timedelta
from time import perf_counter
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection, models, transaction
from django.test import Client, TestCase, TransactionTestCase
from django.test.utils import isolate_apps
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from audit.models import AuditEvent
from hostels.models import Hostel, Room, Bed

from .models import Student


def student_fields(**overrides):
    return {
        'student_id': 'PES1UG24CS145', 'name': 'Sample Student', 'dob': date(2006, 1, 2),
        'gender': 'Male', 'course': 'B.Tech CSE', 'year': 2, 'mobile': '9000000000',
        'email': 'sample@example.test', 'guardian_name': 'Sample Guardian',
        'guardian_mobile': '9000000001', 'address': '', **overrides,
    }


class StudentModelTests(TestCase):
    def test_student_id_is_unique_canonical_and_immutable(self):
        student = Student.objects.create(**student_fields(student_id='pes1ug24cs145'))
        self.assertEqual(student.student_id, 'PES1UG24CS145')
        with self.assertRaisesMessage(ValidationError, 'Student ID already registered'):
            Student.objects.create(**student_fields())
        student.student_id = 'PES1UG24CS146'
        with self.assertRaises(ValidationError):
            student.save()
        student.refresh_from_db()
        self.assertEqual(student.student_id, 'PES1UG24CS145')
        with self.assertRaises(ValidationError):
            Student.objects.filter(pk=student.pk).update(student_id='PES1UG24CS147')

    def test_students_cannot_be_deleted_or_bulk_deactivated(self):
        student = Student.objects.create(**student_fields())
        with self.assertRaises(ValidationError):
            student.delete()
        with self.assertRaises(ValidationError):
            Student.objects.all().delete()
        with self.assertRaises(ValidationError):
            Student.objects.filter(pk=student.pk).update(status='Inactive')
        self.assertEqual(Student.objects.count(), 1)

    def test_model_validates_srs_fields_and_database_year_constraint(self):
        for fields in (
            {'student_id': 'short'}, {'dob': timezone.localdate() + timedelta(days=1)},
            {'gender': 'Other'}, {'year': 0}, {'year': 6}, {'mobile': 'abc'},
            {'guardian_mobile': '123'}, {'email': 'bad'}, {'name': ' '},
        ):
            with self.subTest(fields=fields), self.assertRaises(ValidationError):
                Student.objects.create(**student_fields(**fields))
        student = Student.objects.create(**student_fields())
        with self.assertRaises(IntegrityError), transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute('UPDATE students_student SET year = %s WHERE id = %s', [6, student.pk])

    def test_only_student_user_accounts_can_be_linked_to_profile(self):
        account = User.objects.create_user(username='profile-warden', role=User.Role.WARDEN)
        with self.assertRaises(ValidationError):
            Student.objects.create(**student_fields(user=account))


class StudentViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(username='students-admin', role=User.Role.ADMIN)
        cls.warden = User.objects.create_user(username='students-warden', role=User.Role.WARDEN)
        cls.student_user = User.objects.create_user(username='students-student', role=User.Role.STUDENT)
        cls.student = Student.objects.create(**student_fields())

    def test_admin_and_warden_can_register_valid_students_using_srs_dates(self):
        for index, account in enumerate((self.admin, self.warden)):
            self.client.force_login(account)
            response = self.client.post(reverse('student-list'), student_fields(
                student_id=f'PES1UG24CS15{index}', dob='02-01-2006',
            ), content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()['dob'], '02-01-2006')
            self.assertTrue(AuditEvent.objects.filter(
                user=account, action='create', record_type='students.student',
                record_id=str(response.json()['id']),
            ).exists())

    def test_duplicate_id_has_required_message_and_no_second_record(self):
        self.client.force_login(self.warden)
        response = self.client.post(reverse('student-list'), student_fields(dob='2006-01-02'), content_type='application/json')
        self.assertEqual(response.status_code, 409)
        self.assertIn('Student ID already registered', response.content.decode())
        self.assertEqual(Student.objects.count(), 1)

    def test_each_mandatory_field_is_validated_without_saving(self):
        self.client.force_login(self.warden)
        for field in ('student_id', 'name', 'dob', 'gender', 'course', 'year', 'mobile', 'email', 'guardian_name', 'guardian_mobile'):
            with self.subTest(field=field):
                data = student_fields(student_id='PES1UG24CS146', dob='2006-01-02')
                data[field] = ''
                response = self.client.post(reverse('student-list'), data, content_type='application/json')
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.json()['error']['fields'])
        self.assertEqual(Student.objects.count(), 1)

    def test_invalid_formats_choices_lengths_and_future_birth_date_are_rejected(self):
        self.client.force_login(self.warden)
        for field, value in (
            ('student_id', '123'), ('dob', '31-02-2006'), ('dob', '2999-01-01'),
            ('gender', 'Other'), ('year', 6), ('mobile', '123456789a'),
            ('guardian_mobile', '123'), ('email', 'bad'), ('name', 'A' * 61),
            ('course', 'C' * 31), ('address', 'A' * 201),
        ):
            with self.subTest(field=field, value=value):
                response = self.client.post(reverse('student-list'), student_fields(
                    **{'student_id': 'PES1UG24CS146', 'dob': '2006-01-02', field: value},
                ), content_type='application/json')
                self.assertEqual(response.status_code, 400)
        self.assertEqual(Student.objects.count(), 1)

    def test_student_role_cannot_read_or_modify_any_staff_student_route(self):
        self.client.force_login(self.student_user)
        for name, args in (
            ('student-list', []), ('student-create', []), ('student-detail', [self.student.pk]),
            ('student-update', [self.student.pk]), ('student-deactivate', [self.student.pk]),
        ):
            url = reverse(name, args=args)
            self.assertEqual(self.client.get(url).status_code, 403)
            self.assertEqual(self.client.post(url, {}).status_code, 403)
        self.assertEqual(self.client.patch(
            reverse('student-detail', args=[self.student.pk]), {'mobile': '9999999999'},
            content_type='application/json',
        ).status_code, 403)

    def test_anonymous_access_and_missing_record_are_handled(self):
        self.assertEqual(self.client.get(reverse('student-list')).status_code, 302)
        self.assertEqual(self.client.get(reverse('student-list'), HTTP_ACCEPT='application/json').status_code, 401)
        self.client.force_login(self.warden)
        self.assertEqual(self.client.get(reverse('student-detail', args=[999999])).status_code, 404)

    def test_search_id_partial_name_no_match_and_sql_injection_input(self):
        Student.objects.create(**student_fields(student_id='PES1UG24CS146', name='Another Person'))
        self.client.force_login(self.warden)
        for query, count in (('PES1UG24CS145', 1), ('sample', 1), ('no match', 0), ("' OR '1'='1", 0)):
            response = self.client.get(reverse('student-list'), {'q': query}, HTTP_ACCEPT='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['total'], count)

    def test_hostel_filter_without_allocations_returns_no_matches(self):
        hostel = Hostel.objects.create(name='Empty hostel', type='Boys')
        self.client.force_login(self.warden)
        response = self.client.get(reverse('student-list'), {'hostel': hostel.pk}, HTTP_ACCEPT='application/json')
        self.assertEqual(response.json()['total'], 0)

    def test_partial_patch_updates_allowed_fields_but_rejects_changed_student_id(self):
        self.client.force_login(self.warden)
        url = reverse('student-detail', args=[self.student.pk])
        response = self.client.patch(url, {'mobile': '9999999999'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.student.refresh_from_db()
        self.assertEqual(self.student.mobile, '9999999999')
        response = self.client.patch(url, {
            'student_id': 'PES1UG24CS199', 'mobile': '9888888888',
        }, content_type='application/json')
        self.assertEqual(response.status_code, 422)
        self.student.refresh_from_db()
        self.assertEqual(self.student.student_id, 'PES1UG24CS145')
        self.assertEqual(self.student.mobile, '9999999999')

    def test_updates_ignore_fields_outside_the_allowed_contact_and_course_fields(self):
        self.client.force_login(self.admin)
        response = self.client.patch(reverse('student-detail', args=[self.student.pk]), {
            'name': 'Tampered', 'status': 'Inactive', 'year': 3,
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'Sample Student')
        self.assertEqual(self.student.status, 'Active')
        self.assertEqual(self.student.year, 3)

    def test_deactivation_retains_record_and_is_idempotent(self):
        self.client.force_login(self.warden)
        url = reverse('student-deactivate', args=[self.student.pk])
        for _ in range(2):
            response = self.client.post(url, {}, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['status'], 'Inactive')
        self.student.refresh_from_db()
        self.assertEqual(self.student.status, Student.Status.INACTIVE)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(AuditEvent.objects.filter(action='deactivate', record_type='students.student').count(), 1)

    def test_audit_failure_rolls_back_registration(self):
        self.client.force_login(self.warden)
        with patch('students.services.record_event', side_effect=RuntimeError('audit failed')):
            with self.assertRaises(RuntimeError):
                self.client.post(reverse('student-list'), student_fields(
                    student_id='PES1UG24CS146', dob='2006-01-02',
                ))
        self.assertEqual(Student.objects.count(), 1)

    def test_html_forms_escape_script_input_and_require_csrf(self):
        self.client.force_login(self.warden)
        for name, args in (('student-list', []), ('student-create', []), ('student-detail', [self.student.pk]), ('student-update', [self.student.pk])):
            self.assertEqual(self.client.get(reverse(name, args=args)).status_code, 200)
        Student.objects.create(**student_fields(student_id='PES1UG24CS146', name='<script>alert(1)</script>'))
        response = self.client.get(reverse('student-list'))
        self.assertContains(response, '&lt;script&gt;alert(1)&lt;/script&gt;')
        self.assertNotContains(response, '<script>alert(1)</script>')
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.warden)
        self.assertEqual(client.post(reverse('student-list'), student_fields(dob='2006-01-02')).status_code, 403)

    def test_malformed_json_and_bad_search_parameters_are_rejected(self):
        self.client.force_login(self.warden)
        for body in ('[', '[]', 'null'):
            self.assertEqual(self.client.post(reverse('student-list'), body, content_type='application/json').status_code, 400)
        self.assertEqual(self.client.get(reverse('student-list'), {'hostel': 'bad'}, HTTP_ACCEPT='application/json').status_code, 400)


class StudentSearchVolumeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.warden = User.objects.create_user(username='volume-warden', role=User.Role.WARDEN)
        Student.objects.bulk_create([
            Student(**student_fields(
                student_id=f'TEST{index:09d}', name=f'Volume Student {index:04d}',
                email=f'student{index}@example.test',
            )) for index in range(5000)
        ], batch_size=500)

    def test_searches_over_five_thousand_records_are_paginated_and_under_two_seconds(self):
        self.client.force_login(self.warden)
        for query, expected in (('TEST000004999', 1), ('Volume Student 19', 100), ('absent', 0)):
            with self.subTest(query=query):
                start = perf_counter()
                response = self.client.get(reverse('student-list'), {'q': query}, HTTP_ACCEPT='application/json')
                elapsed = perf_counter() - start
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()['total'], expected)
                self.assertLessEqual(len(response.json()['results']), 25)
                self.assertLess(elapsed, 2.0, f'Search took {elapsed:.3f}s')


class AllocationReadContractTests(TransactionTestCase):
    def test_current_hostel_search_and_deactivation_guard_use_real_database_queries(self):
        # This fixture exercises the read contract only. No Sprint 2 allocation
        # operation, transaction, or business-rule implementation is supplied.
        with isolate_apps():
            class AllocationReadFixture(models.Model):
                student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='+')
                bed = models.ForeignKey(Bed, on_delete=models.PROTECT, related_name='+')
                vacated_on = models.DateField(null=True)

                class Meta:
                    app_label = 'allocation_contract'
                    db_table = 'test_allocation_read_contract'

            with connection.schema_editor() as editor:
                editor.create_model(AllocationReadFixture)
            try:
                warden = User.objects.create_user(username='contract-warden', role=User.Role.WARDEN)
                hostel = Hostel.objects.create(name='Contract hostel', type='Boys')
                room = Room.objects.create(hostel=hostel, room_number='101', floor=0, room_type='Double', capacity=2, fee_amount=100)
                student = Student.objects.create(**student_fields())
                former = Student.objects.create(**student_fields(student_id='PES1UG24CS146'))
                allocation = AllocationReadFixture.objects.create(student=student, bed=room.beds.first())
                AllocationReadFixture.objects.create(student=former, bed=room.beds.last(), vacated_on=date(2026, 1, 1))
                self.client.force_login(warden)
                with patch('students.allocation_access.get_allocation_model', return_value=AllocationReadFixture):
                    response = self.client.get(reverse('student-list'), {'hostel': hostel.pk}, HTTP_ACCEPT='application/json')
                    self.assertEqual([row['id'] for row in response.json()['results']], [student.pk])
                    response = self.client.post(reverse('student-deactivate', args=[student.pk]), {}, content_type='application/json')
                    self.assertEqual(response.status_code, 409)
                    self.assertIn('101-A', response.json()['error']['message'])
                    student.refresh_from_db()
                    self.assertEqual(student.status, 'Active')
                    allocation.vacated_on = date(2026, 1, 2)
                    allocation.save()
                    response = self.client.post(reverse('student-deactivate', args=[student.pk]), {}, content_type='application/json')
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(AllocationReadFixture.objects.count(), 2)
            finally:
                with connection.schema_editor() as editor:
                    editor.delete_model(AllocationReadFixture)
