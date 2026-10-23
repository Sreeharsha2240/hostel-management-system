
from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from allocations.models import Allocation
from students.models import Student
from .models import Bed, Hostel, Room


class HostelModelTests(TestCase):
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
