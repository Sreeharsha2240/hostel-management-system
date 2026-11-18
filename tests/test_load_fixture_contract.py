"""Load setup must remain compatible with the actual inventory model guards."""

from django.test import TestCase

from hostels.models import Bed, Hostel, Room
from scripts.part3 import test_issue40_load as load_harness
from students.models import Student


class LoadFixtureContractTests(TestCase):
    def test_fixture_grows_without_bulk_bypasses_or_duplicate_beds(self):
        hostel = Hostel.objects.create(name="Load fixture contract", hostel_type="Boys")
        seed = load_harness.Issue40LoadExecution.seed_fixture
        seed(hostel, student_count=6, bed_count=4)
        self.assertEqual(
            (Student.objects.count(), Room.objects.count(), Bed.objects.count()),
            (6, 2, 4),
        )
        seed(hostel, student_count=10, bed_count=8)
        seed(hostel, student_count=10, bed_count=8)
        self.assertEqual(
            (Student.objects.count(), Room.objects.count(), Bed.objects.count()),
            (10, 4, 8),
        )
        for room in Room.objects.all():
            self.assertEqual(
                set(room.beds.values_list("label", flat=True)),
                {f"{room.room_number}-A", f"{room.room_number}-B"},
            )
