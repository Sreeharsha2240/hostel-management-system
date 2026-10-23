
from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import User

from allocations.models import Allocation
from students.models import Student
from .models import Bed, Hostel, Room



class HostelModelTests(TestCase):
    def setUp(self):
        self.hostel = Hostel.objects.create(
            name="Test Hostel",
            hostel_type=Hostel.HostelType.BOYS,
        )


class HostelManagementViewTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="hostel_admin", password="TestPassword123!", role=User.Role.ADMIN
        )
        self.warden = User.objects.create_user(
            username="hostel_warden", password="TestPassword123!", role=User.Role.WARDEN
        )
        self.client = Client()
        self.client.force_login(self.admin)
        self.hostel = Hostel.objects.create(
            name="Filtered Boys Hostel", hostel_type=Hostel.HostelType.BOYS
        )
        self.other_hostel = Hostel.objects.create(
            name="Filtered Girls Hostel", hostel_type=Hostel.HostelType.GIRLS
        )
        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number="701",
            floor=7,
            room_type=Room.RoomType.DOUBLE,
            capacity=3,
        )
        self.other_room = Room.objects.create(
            hostel=self.other_hostel,
            room_number="801",
            floor=8,
            room_type=Room.RoomType.SINGLE,
            capacity=1,
        )

    def test_admin_can_create_hostel_and_room(self):
        hostel_response = self.client.post(
            reverse("hostel-list"),
            {"name": "Admin Created Hostel", "hostel_type": Hostel.HostelType.BOYS},
        )
        self.assertRedirects(hostel_response, reverse("hostel-list"))
        created_hostel = Hostel.objects.get(name="Admin Created Hostel")

        room_response = self.client.post(
            reverse("room-create"),
            {
                "hostel": created_hostel.pk,
                "room_number": "901",
                "floor": 9,
                "room_type": Room.RoomType.SINGLE,
                "capacity": 1,
            },
        )
        self.assertRedirects(room_response, reverse("bed-list"))
        self.assertTrue(Room.objects.filter(hostel=created_hostel, room_number="901").exists())

    def test_only_admin_can_create_or_edit_hostels_and_rooms(self):
        self.client.force_login(self.warden)
        forbidden_requests = (
            ("get", reverse("hostel-list")),
            ("post", reverse("hostel-list"), {"name": "Forbidden", "hostel_type": "Boys"}),
            ("get", reverse("hostel-update", args=[self.hostel.pk])),
            ("get", reverse("room-create")),
            ("post", reverse("room-create"), {
                "hostel": self.hostel.pk,
                "room_number": "702",
                "floor": 7,
                "room_type": "Single",
                "capacity": 1,
            }),
            ("get", reverse("room-update", args=[self.room.pk])),
        )

        for request in forbidden_requests:
            method, url, *data = request
            response = getattr(self.client, method)(url, *(data or [{}]))
            self.assertEqual(response.status_code, 403, f"{method.upper()} {url}")

        self.assertFalse(Hostel.objects.filter(name="Forbidden").exists())
        self.assertFalse(Room.objects.filter(room_number="702").exists())

    def test_available_bed_filter_combines_hostel_floor_and_room_type(self):
        available = self.room.beds.get(label="701-A")
        occupied = self.room.beds.get(label="701-B")
        maintenance = self.room.beds.get(label="701-C")
        occupied.status = Bed.BedStatus.OCCUPIED
        occupied.save(update_fields=["status"])
        maintenance.status = Bed.BedStatus.MAINTENANCE
        maintenance.save(update_fields=["status"])

        response = self.client.get(
            reverse("bed-list"),
            {
                "hostel": self.hostel.pk,
                "floor": 7,
                "room_type": Room.RoomType.DOUBLE,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["beds"]), [available])
        self.assertNotIn(self.other_room.beds.get(), response.context["beds"])

    def test_available_bed_results_exclude_occupied_and_maintenance_beds(self):
        occupied = self.room.beds.get(label="701-A")
        maintenance = self.room.beds.get(label="701-B")
        occupied.status = Bed.BedStatus.OCCUPIED
        occupied.save(update_fields=["status"])
        maintenance.status = Bed.BedStatus.MAINTENANCE
        maintenance.save(update_fields=["status"])

        response = self.client.get(reverse("bed-list"))

        self.assertEqual(response.status_code, 200)
        bed_ids = set(response.context["beds"].values_list("pk", flat=True))
        self.assertNotIn(occupied.pk, bed_ids)
        self.assertNotIn(maintenance.pk, bed_ids)


class HostelModelBehaviorTests(TestCase):
    def setUp(self):
        self.hostel = Hostel.objects.create(
            name="Test Hostel",
            hostel_type=Hostel.HostelType.BOYS,
        )

    def test_create_hostel(self):
        self.assertEqual(self.hostel.name, "Test Hostel")
        self.assertTrue(self.hostel.is_active)

    def test_duplicate_hostel_name_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Hostel.objects.create(
                    name="Test Hostel",
                    hostel_type=Hostel.HostelType.GIRLS,
                )

    def test_room_creation_automatically_creates_beds(self):
        room = Room.objects.create(
            hostel=self.hostel,
            room_number="101",
            floor=1,
            room_type=Room.RoomType.TRIPLE,
            capacity=3,
        )

        self.assertEqual(room.beds.count(), 3)
        self.assertSetEqual(
            set(room.beds.values_list("label", flat=True)),
            {"101-A", "101-B", "101-C"},
        )
        self.assertEqual(
            room.beds.filter(status=Bed.BedStatus.AVAILABLE).count(),
            3,
        )

    def test_room_capacity_cannot_exceed_four(self):
        room = Room(
            hostel=self.hostel,
            room_number="102",
            floor=1,
            room_type=Room.RoomType.TRIPLE,
            capacity=5,
        )

        with self.assertRaises(ValidationError):
            room.full_clean()

    def test_room_numbers_must_be_unique_within_hostel(self):
        Room.objects.create(
            hostel=self.hostel,
            room_number="103",
            floor=1,
            room_type=Room.RoomType.SINGLE,
            capacity=1,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Room.objects.create(
                    hostel=self.hostel,
                    room_number="103",
                    floor=2,
                    room_type=Room.RoomType.DOUBLE,
                    capacity=2,
                )

    def test_bed_status_can_be_changed(self):
        room = Room.objects.create(
            hostel=self.hostel,
            room_number="104",
            floor=1,
            room_type=Room.RoomType.SINGLE,
            capacity=1,
        )

        bed = room.beds.get()
        bed.status = Bed.BedStatus.MAINTENANCE
        bed.save()

        bed.refresh_from_db()
        self.assertEqual(bed.status, Bed.BedStatus.MAINTENANCE)

    def test_renaming_room_updates_existing_bed_labels(self):
        room = Room.objects.create(
            hostel=self.hostel,
            room_number="201",
            floor=2,
            room_type=Room.RoomType.TRIPLE,
            capacity=3,
        )

        room.room_number = "202"
        room.save()

        self.assertEqual(room.beds.count(), 3)
        self.assertSetEqual(
            set(room.beds.values_list("label", flat=True)),
            {"202-A", "202-B", "202-C"},
        )

    def test_reducing_capacity_removes_unallocated_beds(self):
        room = Room.objects.create(
            hostel=self.hostel,
            room_number="301",
            floor=3,
            room_type=Room.RoomType.TRIPLE,
            capacity=3,
        )

        room.capacity = 2
        room.save()

        self.assertEqual(room.beds.count(), 2)
        self.assertSetEqual(
            set(room.beds.values_list("label", flat=True)),
            {"301-A", "301-B"},
        )

    def test_capacity_cannot_be_reduced_below_active_allocations(self):
        room = Room.objects.create(
            hostel=self.hostel,
            room_number="401",
            floor=4,
            room_type=Room.RoomType.TRIPLE,
            capacity=3,
        )

        student1 = Student.objects.create(
            student_id="PES9876543210",
            name="Test Student One",
            date_of_birth=date(2005, 1, 15),
            gender=Student.Gender.MALE,
            course="Engineering",
            year=2,
            mobile="9876543210",
            email="student1@example.com",
            guardian_name="Guardian One",
            guardian_mobile="9876543211",
        )

        student2 = Student.objects.create(
            student_id="PES9876543211",
            name="Test Student Two",
            date_of_birth=date(2005, 2, 15),
            gender=Student.Gender.FEMALE,
            course="Engineering",
            year=2,
            mobile="9876543212",
            email="student2@example.com",
            guardian_name="Guardian Two",
            guardian_mobile="9876543213",
        )

        Allocation.objects.create(
            student=student1,
            bed=room.beds.get(label="401-A"),
            allocated_on=date.today(),
        )

        Allocation.objects.create(
            student=student2,
            bed=room.beds.get(label="401-B"),
            allocated_on=date.today(),
        )

        room.capacity = 1

        with self.assertRaises(ValidationError):
            room.full_clean()

        room.refresh_from_db()
        self.assertEqual(room.capacity, 3)
        self.assertEqual(room.beds.count(), 3)

    
    def test_queryset_update_rejects_capacity_and_room_number(self):
        room = Room.objects.create(
            hostel=self.hostel,
            room_number="501",
            floor=5,
            room_type=Room.RoomType.TRIPLE,
            capacity=3,
        )

        room.beds.get(label="501-B").status = Bed.BedStatus.MAINTENANCE
        room.beds.get(label="501-B").save()

        before = list(
            room.beds.order_by("label").values_list("label", "status")
        )

        with self.assertRaises(ValueError):
            Room.objects.filter(pk=room.pk).update(capacity=2)

        with self.assertRaises(ValueError):
            Room.objects.filter(pk=room.pk).update(room_number="502")

        room.refresh_from_db()
        after = list(
            room.beds.order_by("label").values_list("label", "status")
        )

        self.assertEqual(room.capacity, 3)
        self.assertEqual(room.room_number, "501")
        self.assertEqual(len(after), 3)
        self.assertEqual(after, before)

    def test_bulk_update_rejects_capacity_and_room_number(self):
        room = Room.objects.create(
            hostel=self.hostel,
            room_number="601",
            floor=6,
            room_type=Room.RoomType.TRIPLE,
            capacity=3,
        )

        room.beds.get(label="601-B").status = Bed.BedStatus.MAINTENANCE
        room.beds.get(label="601-B").save()

        before = list(
            room.beds.order_by("label").values_list("label", "status")
        )

        room.capacity = 2
        with self.assertRaises(ValueError):
            Room.objects.bulk_update([room], ["capacity"])

        room.refresh_from_db()
        room.room_number = "602"
        with self.assertRaises(ValueError):
            Room.objects.bulk_update([room], ["room_number"])

        room.refresh_from_db()
        after = list(
            room.beds.order_by("label").values_list("label", "status")
        )

        self.assertEqual(room.capacity, 3)
        self.assertEqual(room.room_number, "601")
        self.assertEqual(len(after), 3)
        self.assertEqual(after, before)

