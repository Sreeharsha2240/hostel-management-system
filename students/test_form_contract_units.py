"""Student form account selection and identifier checks without database access."""

from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.test import SimpleTestCase

from accounts.models import User

from .forms import StudentForm
from .models import Student


class StudentAccountPickerUnitTests(SimpleTestCase):
    @patch("students.forms.User.objects.filter")
    def test_new_and_unlinked_profiles_only_offer_unlinked_student_accounts(
        self, accounts
    ):
        for instance in (Student(), Student(pk=7), Student(user_id=91)):
            with self.subTest(pk=instance.pk, user_id=instance.user_id):
                accounts.reset_mock()

                form = StudentForm(instance=instance)

                accounts.assert_called_once_with(role=User.Role.STUDENT)
                accounts.return_value.filter.assert_called_once_with(
                    student_profile__isnull=True
                )
                choices = accounts.return_value.filter.return_value
                choices.order_by.assert_called_once_with("username")
                self.assertIs(
                    form.fields["user"].queryset,
                    choices.order_by.return_value.all.return_value,
                )

    @patch("students.forms.User.objects.filter")
    def test_editing_linked_profile_keeps_its_account_available(self, accounts):
        form = StudentForm(instance=Student(pk=7, user_id=91))

        accounts.assert_called_once_with(role=User.Role.STUDENT)
        accounts.return_value.filter.assert_called_once_with(
            Q(student_profile__isnull=True) | Q(pk=91)
        )
        choices = accounts.return_value.filter.return_value
        choices.order_by.assert_called_once_with("username")
        self.assertIs(
            form.fields["user"].queryset,
            choices.order_by.return_value.all.return_value,
        )

    @patch("students.forms.User.objects.filter")
    def test_linked_login_is_optional_and_explains_access_to_student_records(
        self, accounts
    ):
        field = StudentForm().fields["user"]

        self.assertFalse(field.required)
        self.assertIsNone(field.clean(""))
        self.assertEqual(field.label, "Linked student login")
        self.assertIn("allocation and payment details", field.help_text)


class StudentIdentifierFormUnitTests(SimpleTestCase):
    def setUp(self):
        accounts = patch("students.forms.User.objects.filter")
        accounts.start()
        self.addCleanup(accounts.stop)

    @patch("students.forms.Student.objects.filter")
    def test_new_identifier_is_uppercased_and_checked_case_insensitively(
        self, students
    ):
        students.return_value.exists.return_value = False
        form = StudentForm()
        form.cleaned_data = {"student_id": "pes1234567890"}

        self.assertEqual(form.clean_student_id(), "PES1234567890")

        students.assert_called_once_with(student_id__iexact="PES1234567890")
        students.return_value.exclude.assert_not_called()
        students.return_value.exists.assert_called_once_with()

    @patch("students.forms.Student.objects.filter")
    def test_editing_identifier_excludes_own_profile_from_duplicate_lookup(
        self, students
    ):
        students.return_value.exclude.return_value.exists.return_value = False
        form = StudentForm(instance=Student(pk=7))
        form.cleaned_data = {"student_id": "pes1234567890"}

        self.assertEqual(form.clean_student_id(), "PES1234567890")

        students.assert_called_once_with(student_id__iexact="PES1234567890")
        students.return_value.exclude.assert_called_once_with(pk=7)
        students.return_value.exclude.return_value.exists.assert_called_once_with()

    @patch("students.forms.Student.objects.filter")
    def test_new_and_edited_profiles_reject_another_students_identifier(self, students):
        for instance in (Student(), Student(pk=7)):
            with self.subTest(pk=instance.pk):
                students.reset_mock()
                students.return_value.exists.return_value = True
                students.return_value.exclude.return_value.exists.return_value = True
                form = StudentForm(instance=instance)
                form.cleaned_data = {"student_id": "pes1234567890"}

                with self.assertRaisesMessage(
                    ValidationError, "Student ID already registered"
                ):
                    form.clean_student_id()

                students.assert_called_once_with(student_id__iexact="PES1234567890")
                if instance.pk:
                    students.return_value.exclude.assert_called_once_with(pk=7)
                    students.return_value.exists.assert_not_called()
                else:
                    students.return_value.exclude.assert_not_called()
