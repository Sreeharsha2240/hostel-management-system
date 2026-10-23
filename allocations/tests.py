
from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from allocations.models import Allocation
from hostels.models import Bed, Hostel, Room
from students.models import Student


class AllocationModelTests(TestCase):
    def setUp(self):
        self.student1 = Student.objects.create(
            student_id="PES1234567890",
            name="Student One",
            date_of_birth=date(2005, 5, 15),
            gender=Student.Gender.MALE,
            course="Computer Science",
            year=2,
            mobile="9876543210",
            email="student1@example.com",
            guardian_name="Guardian One",
            guardian_mobile="9876543211",
        )

        self.student2 = Student.objects.create(
            student_id="PES1234567891",
            name="Student Two",
            date_of_birth=date(2005, 6, 15),
            gender=Student.Gender.MALE,
            course="Computer Science",
            year=2,
            mobile="9876543212",
            email="student2@example.com",
            guardian_name="Guardian Two",
            guardian_mobile="9876543213",
        )

        self.hostel = Hostel.objects.create(
            name="Test Boys Hostel",
            hostel_type=Hostel.HostelType.BOYS,
        )

        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number="101",
            floor=1,
            room_type=Room.RoomType.DOUBLE,
            capacity=2,
        )

        self.bed1 = self.room.beds.get(label="101-A")
        self.bed2 = self.room.beds.get(label="101-B")

    def test_active_allocation_occupies_bed(self):
        allocation = Allocation(
            student=self.student1,
            bed=self.bed1,
        )
        allocation.save()

        self.bed1.refresh_from_db()
        self.assertEqual(self.bed1.status, Bed.BedStatus.OCCUPIED)
        self.assertEqual(
            allocation.active_student_id,
            self.student1.pk,
        )
        self.assertEqual(allocation.active_bed_id, self.bed1.pk)

    def test_student_cannot_have_two_active_allocations(self):
        Allocation.objects.create(
            student=self.student1,
            bed=self.bed1,
        )

        with self.assertRaises(ValidationError):
            Allocation.objects.create(
                student=self.student1,
                bed=self.bed2,
            )

    def test_bed_cannot_have_two_active_allocations(self):
        Allocation.objects.create(
            student=self.student1,
            bed=self.bed1,
        )

        with self.assertRaises(ValidationError):
            Allocation.objects.create(
                student=self.student2,
                bed=self.bed1,
            )

    def test_maintenance_bed_cannot_be_allocated(self):
        self.bed1.status = Bed.BedStatus.MAINTENANCE
        self.bed1.save(update_fields=["status"])

        with self.assertRaises(ValidationError):
            Allocation.objects.create(
                student=self.student1,
                bed=self.bed1,
            )

    def test_completing_allocation_releases_bed(self):
        allocation = Allocation.objects.create(
            student=self.student1,
            bed=self.bed1,
        )

        allocation.status = Allocation.AllocationStatus.COMPLETED
        allocation.vacated_on = date.today()
        allocation.save()

        self.bed1.refresh_from_db()
        self.assertEqual(self.bed1.status, Bed.BedStatus.AVAILABLE)
        self.assertIsNone(allocation.active_student_id)
        self.assertIsNone(allocation.active_bed_id)

    def test_completing_allocation_preserves_maintenance_status(self):
        allocation = Allocation.objects.create(
            student=self.student1,
            bed=self.bed1,
        )

        self.bed1.status = Bed.BedStatus.MAINTENANCE
        self.bed1.save(update_fields=["status"])

        allocation.status = Allocation.AllocationStatus.COMPLETED
        allocation.vacated_on = date.today()
        allocation.save()

        self.bed1.refresh_from_db()
        self.assertEqual(self.bed1.status, Bed.BedStatus.MAINTENANCE)
