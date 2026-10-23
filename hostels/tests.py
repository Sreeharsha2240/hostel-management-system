
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

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
        self.assertTrue(
            room.beds.filter(status=Bed.BedStatus.AVAILABLE).count() == 3
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
