
from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User
from allocations.models import Allocation
from hostels.models import Bed, Hostel, Room
from students.models import Student


class StudentModelTests(TestCase):
    def student_data(self, **overrides):
        data = {
            "student_id": "PES1234567890",
            "name": "Test Student",
            "date_of_birth": date(2005, 5, 15),
            "gender": Student.Gender.MALE,
            "course": "Computer Science",
            "year": 2,
            "mobile": "9876543210",
            "email": "student@example.com",
            "guardian_name": "Test Guardian",
            "guardian_mobile": "9876543211",
            "address": "Bengaluru",
        }
        data.update(overrides)
        return data

    def test_create_student(self):
        student = Student.objects.create(**self.student_data())
        self.assertEqual(student.status, Student.Status.ACTIVE)
        self.assertEqual(student.student_id, "PES1234567890")

    def test_duplicate_student_id_is_rejected(self):
        Student.objects.create(**self.student_data())
        with self.assertRaises(Exception):
            Student.objects.create(**self.student_data(name="Another Student"))

    def test_student_can_be_deactivated_without_deleting_record(self):
        student = Student.objects.create(**self.student_data())
        student.status = Student.Status.INACTIVE
        student.save()

        student.refresh_from_db()
        self.assertEqual(student.status, Student.Status.INACTIVE)
        self.assertTrue(Student.objects.filter(pk=student.pk).exists())

    def test_student_year_must_be_between_one_and_five(self):
        student = Student(**self.student_data(year=6))
        with self.assertRaises(ValidationError):
            student.full_clean()

    def test_mobile_must_have_ten_digits(self):
        student = Student(**self.student_data(mobile="12345"))
        with self.assertRaises(ValidationError):
            student.full_clean()


class StudentDeactivationViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create an administrator allowed to manage student records.
        self.admin = User.objects.create_user(
            username="student_admin",
            password="TestPassword123!",
            role=User.Role.ADMIN,
        )
        self.client.force_login(self.admin)

        self.student = Student.objects.create(
            student_id="PES1234567890",
            name="Test Student",
            date_of_birth=date(2005, 5, 15),
            gender=Student.Gender.MALE,
            course="Computer Science",
            year=2,
            mobile="9876543210",
            email="student@example.com",
            guardian_name="Test Guardian",
            guardian_mobile="9876543211",
        )

        self.hostel = Hostel.objects.create(
            name="Deactivation Test Hostel",
            hostel_type=Hostel.HostelType.BOYS,
        )
        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number="101",
            floor=1,
            room_type=Room.RoomType.DOUBLE,
            capacity=2,
        )
        self.bed = self.room.beds.get(label="101-A")

    def test_unallocated_student_can_be_deactivated(self):
        response = self.client.post(
            reverse("student-deactivate", args=[self.student.pk])
        )

        self.assertRedirects(response, reverse("student-list"))
        self.student.refresh_from_db()
        self.assertEqual(self.student.status, Student.Status.INACTIVE)
        self.assertTrue(Student.objects.filter(pk=self.student.pk).exists())

    def test_student_with_active_allocation_cannot_be_deactivated(self):
        Allocation.objects.create(
            student=self.student,
            bed=self.bed,
        )

        response = self.client.post(
            reverse("student-deactivate", args=[self.student.pk]),
            follow=True,
        )

        self.student.refresh_from_db()
        self.assertEqual(self.student.status, Student.Status.ACTIVE)
        self.assertContains(response, self.bed.label)
        self.assertTrue(Student.objects.filter(pk=self.student.pk).exists())

    def test_student_deactivation_requires_post(self):
        response = self.client.get(
            reverse("student-deactivate", args=[self.student.pk])
        )

        self.assertEqual(response.status_code, 405)
        self.student.refresh_from_db()
        self.assertEqual(self.student.status, Student.Status.ACTIVE)
