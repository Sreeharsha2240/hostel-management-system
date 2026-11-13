"""Student field and deactivation decisions with persistence mocked."""

from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from allocations.models import Allocation

from .models import Student


class StudentModelUnitTests(SimpleTestCase):
    def test_student_id_requires_thirteen_alphanumeric_characters(self):
        field = Student._meta.get_field("student_id")
        field.run_validators("ABC123DEF456G")
        for value in ("short", "ABC123DEF456!", "ABC123DEF45678"):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                field.run_validators(value)

    def test_year_boundaries_are_one_to_five(self):
        field = Student._meta.get_field("year")
        for value in (1, 5):
            field.run_validators(value)
        for value in (0, 6):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                field.run_validators(value)

    def test_mobile_fields_require_ten_digits(self):
        for name in ("mobile", "guardian_mobile"):
            field = Student._meta.get_field(name)
            field.run_validators("9000000000")
            for value in ("123", "90000abcde", "90000000000"):
                with (
                    self.subTest(name=name, value=value),
                    self.assertRaises(ValidationError),
                ):
                    field.run_validators(value)

    def test_bulk_status_change_is_rejected(self):
        with self.assertRaisesMessage(ValidationError, "individually"):
            Student.objects.all().update(status=Student.Status.INACTIVE)

    @patch("django.db.models.Model.save", return_value=None)
    @patch("allocations.models.Allocation.objects.filter")
    @patch("students.models.Student.objects.select_for_update")
    def test_deactivation_with_active_allocation_is_rejected(
        self, locked, allocation, save
    ):
        student = Student(pk=7, status=Student.Status.INACTIVE)
        allocation.return_value.exists.return_value = True
        with self.assertRaises(ValidationError) as error:
            Student.save.__wrapped__(student)
        self.assertEqual(error.exception.code, "HAS_ACTIVE_ALLOCATION")
        allocation.assert_called_once_with(
            student_id=7, status=Allocation.AllocationStatus.ACTIVE
        )
        save.assert_not_called()

    @patch("django.db.models.Model.save", return_value=None)
    @patch("allocations.models.Allocation.objects.filter")
    @patch("students.models.Student.objects.select_for_update")
    def test_deactivation_without_allocation_saves(self, locked, allocation, save):
        student = Student(pk=7, status=Student.Status.INACTIVE)
        allocation.return_value.exists.return_value = False
        Student.save.__wrapped__(student, update_fields=["status"])
        locked.return_value.get.assert_called_once_with(pk=7)
        save.assert_called_once_with(update_fields=["status"])

    @patch("django.db.models.Model.save", return_value=None)
    @patch("students.models.Student.objects.select_for_update")
    def test_new_student_does_not_require_a_persisted_row_lock(self, locked, save):
        Student.save.__wrapped__(Student(status=Student.Status.ACTIVE))
        locked.assert_not_called()
        save.assert_called_once()
