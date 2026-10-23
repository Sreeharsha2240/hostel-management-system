
from datetime import date
from time import perf_counter

from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User
from allocations.models import Allocation
from hostels.models import Bed, Hostel, Room
from students.models import Student

from students.forms import StudentForm


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

    def test_duplicate_student_id_form_shows_exact_error_message(self):
        Student.objects.create(**self.student_data())

        form = StudentForm(
            data=self.student_data(name="Another Student")
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["student_id"],
            ["Student ID already registered"],
        )

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

    def student_payload(self, **overrides):
        payload = {
            "student_id": "PES1234567890",
            "name": "Test Student",
            "date_of_birth": "2005-05-15",
            "gender": Student.Gender.MALE,
            "course": "Computer Science",
            "year": "2",
            "mobile": "9876543210",
            "email": "student@example.com",
            "guardian_name": "Test Guardian",
            "guardian_mobile": "9876543211",
            "address": "Bengaluru",
            "status": Student.Status.ACTIVE,
        }
        payload.update(overrides)
        return payload

    def test_admin_can_register_student(self):
        response = self.client.post(
            reverse("student-create"),
            self.student_payload(student_id="PES0000000001"),
        )

        self.assertRedirects(response, reverse("student-list"))
        self.assertTrue(
            Student.objects.filter(student_id="PES0000000001").exists()
        )

    def test_warden_can_register_student(self):
        warden = User.objects.create_user(
            username="student_warden",
            password="TestPassword123!",
            role=User.Role.WARDEN,
        )
        self.client.force_login(warden)

        response = self.client.post(
            reverse("student-create"), self.student_payload(student_id="PES0000000002")
        )

        self.assertRedirects(response, reverse("student-list"))
        self.assertTrue(
            Student.objects.filter(student_id="PES0000000002").exists()
        )

    def test_student_role_cannot_register_update_or_deactivate(self):
        student_user = User.objects.create_user(
            username="student_role",
            password="TestPassword123!",
            role=User.Role.STUDENT,
        )
        self.client.force_login(student_user)

        for url, method in (
            (reverse("student-list"), "get"),
            (reverse("student-create"), "get"),
            (reverse("student-update", args=[self.student.pk]), "get"),
            (reverse("student-deactivate", args=[self.student.pk]), "post"),
        ):
            response = getattr(self.client, method)(url)
            self.assertEqual(response.status_code, 403)

    def test_admin_can_update_contact_course_and_year_but_not_student_id(self):
        response = self.client.post(
            reverse("student-update", args=[self.student.pk]),
            self.student_payload(
                student_id="PES0000000001",
                mobile="9000000000",
                course="Engineering",
                year="3",
            ),
        )

        self.assertRedirects(response, reverse("student-list"))
        self.student.refresh_from_db()
        self.assertEqual(self.student.student_id, "PES1234567890")
        self.assertEqual(self.student.mobile, "9000000000")
        self.assertEqual(self.student.course, "Engineering")
        self.assertEqual(self.student.year, 3)

    def test_duplicate_registration_shows_required_message(self):
        response = self.client.post(
            reverse("student-create"),
            self.student_payload(student_id=self.student.student_id),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student ID already registered")
        self.assertEqual(Student.objects.count(), 1)

    def test_search_matches_student_id_partial_name_and_hostel(self):
        response = self.client.get(reverse("student-list"), {"q": "PES1234567890"})
        self.assertContains(response, self.student.student_id)

        response = self.client.get(reverse("student-list"), {"q": "Test Stud"})
        self.assertContains(response, self.student.student_id)

        Allocation.objects.create(student=self.student, bed=self.bed)
        response = self.client.get(
            reverse("student-list"), {"q": "Deactivation Test Hostel"}
        )
        self.assertContains(response, self.student.student_id)

    def test_student_search_handles_5000_records_within_two_seconds(self):
        Student.objects.bulk_create(
            [
                Student(
                    student_id=f"PES{index:010d}",
                    name=f"Synthetic Student {index:05d}",
                    date_of_birth=date(2005, 5, 15),
                    gender=Student.Gender.MALE,
                    course="Computer Science",
                    year=2,
                    mobile="9876543210",
                    email=f"student{index}@example.test",
                    guardian_name="Synthetic Guardian",
                    guardian_mobile="9876543211",
                )
                for index in range(5000)
            ]
        )

        started = perf_counter()
        response = self.client.get(
            reverse("student-list"), {"q": "PES0000004999"}
        )
        elapsed = perf_counter() - started

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PES0000004999")
        self.assertLess(elapsed, 2.0, f"5000-record search took {elapsed:.3f}s")

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
