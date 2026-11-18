"""Student edit and admin safeguards without a database."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.contrib.admin import AdminSite
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse

from accounts.models import User
from allocations.models import Allocation
from allocations.services import allocate
from hostels.models import Bed, Hostel
from tests.factories import make_room, make_student

from .admin import StudentAdmin
from .forms import StudentForm
from .models import Student
from .views import student_update


class StudentAdminEditUnitTests(SimpleTestCase):
    @patch("django.db.models.Model.save")
    @patch("students.models.Student.objects.select_for_update")
    def test_student_save_preserves_iterable_update_fields(self, locked, save):
        student = Student(pk=7)
        locked.return_value.get.return_value = student

        Student.save.__wrapped__(student, update_fields=iter(["mobile"]))

        self.assertEqual(set(save.call_args.kwargs["update_fields"]), {"mobile"})

    @patch("django.contrib.admin.options.ModelAdmin.get_object")
    @patch("students.admin.Student.objects.select_for_update")
    def test_admin_post_locks_and_refreshes_student_before_form_validation(
        self, locked, lookup
    ):
        lookup.return_value = Student(pk=7)
        current = Student(pk=7, status=Student.Status.INACTIVE)
        locked.return_value.get.return_value = current
        model_admin = StudentAdmin(Student, AdminSite())

        result = model_admin.get_object(SimpleNamespace(method="POST"), "7")

        self.assertIs(result, current)
        locked.return_value.get.assert_called_once_with(pk=7)

    @patch("students.views.render", return_value=HttpResponse("form errors"))
    @patch("students.views.record_event")
    @patch("students.views.transaction.atomic")
    @patch("students.views.StudentForm")
    @patch("students.views.get_object_or_404")
    def test_update_displays_rule_conflict_that_appears_after_validation(
        self, lookup, form_type, atomic, audit, render
    ):
        form = form_type.return_value
        form.fields = {"student_id": Mock(), "status": Mock()}
        form.is_valid.return_value = True
        error = ValidationError("Release active allocation before changing gender.")
        form.save.side_effect = error
        request = RequestFactory().post("/students/7/update/", {})
        request.user = SimpleNamespace(is_authenticated=True, role=User.Role.WARDEN)

        response = student_update(request, 7)

        self.assertEqual(response.status_code, 200)
        form.add_error.assert_called_once_with(None, error)
        audit.assert_not_called()

    def test_bulk_identity_or_gender_changes_cannot_bypass_model_checks(self):
        for field, value in (("student_id", "PES0000000999"), ("gender", "Female")):
            with self.subTest(field=field), self.assertRaises(ValidationError):
                Student.objects.all().update(**{field: value})

    def test_admin_uses_the_restricted_student_account_picker(self):
        self.assertIs(StudentAdmin.form, StudentForm)

    def test_admin_identity_is_read_only_after_registration(self):
        model_admin = StudentAdmin(Student, AdminSite())
        self.assertIn(
            "student_id", model_admin.get_readonly_fields(None, Student(pk=7))
        )
        self.assertNotIn("student_id", model_admin.get_readonly_fields(None, None))

    @patch("django.forms.models.BaseModelForm.save")
    def test_profile_update_does_not_restore_removed_status_field(self, parent):
        student = Mock()
        student._state.adding = False
        parent.return_value = student
        form = StudentForm(instance=Student(pk=7))
        form.cleaned_data = {}
        form.fields.pop("status")

        self.assertIs(form.save(), student)

        parent.assert_called_once_with(commit=False)
        student.save.assert_called_once()
        fields = student.save.call_args.kwargs["update_fields"]
        self.assertNotIn("status", fields)
        self.assertIn("mobile", fields)
        self.assertIn("updated_at", fields)

    @patch("allocations.models.Allocation.objects.select_related")
    def test_form_deactivation_explains_active_bed_before_save(self, allocations):
        allocation = Mock()
        allocation.bed.label = "101-A"
        allocations.return_value.filter.return_value.first.return_value = allocation
        form = StudentForm(instance=Student(pk=7))
        form.cleaned_data = {"status": Student.Status.INACTIVE}

        with self.assertRaisesMessage(ValidationError, "101-A"):
            form.clean_status()


class StudentEditIntegrityTests(TestCase):
    def setUp(self):
        self.student = make_student(981)

    def edit_form(self, **overrides):
        from django.forms.models import model_to_dict

        data = model_to_dict(self.student)
        data.update(overrides)
        return StudentForm(data, instance=self.student)

    def test_update_cannot_reactivate_a_concurrently_deactivated_student(self):
        form = self.edit_form(mobile="9000000000")
        form.fields.pop("status")
        self.assertTrue(form.is_valid(), form.errors)
        current = Student.objects.get(pk=self.student.pk)
        current.status = Student.Status.INACTIVE
        current.save(update_fields=["status"])

        form.save()

        self.student.refresh_from_db()
        self.assertEqual(self.student.status, Student.Status.INACTIVE)
        self.assertEqual(self.student.mobile, "9000000000")

    def test_existing_student_id_cannot_be_changed_with_model_save(self):
        original = self.student.student_id
        self.student.student_id = "PES0000000999"

        with self.assertRaises(ValidationError):
            self.student.save(update_fields=["student_id"])

        self.student.refresh_from_db()
        self.assertEqual(self.student.student_id, original)

    def allocate_student(self):
        hostel = Hostel.objects.create(
            name="Student integrity hostel", hostel_type="Boys"
        )
        room = make_room(hostel=hostel)
        return allocate(student=self.student, bed=room.beds.first(), actor=None)

    def test_conflict_upsert_cannot_change_allocated_student_eligibility_or_identity(
        self,
    ):
        from django.forms.models import model_to_dict

        allocation = self.allocate_student()
        original = model_to_dict(self.student)
        for field, value in (
            ("status", Student.Status.INACTIVE),
            ("gender", Student.Gender.FEMALE),
            ("student_id", "PES0000000999"),
        ):
            with self.subTest(field=field):
                replacement = Student(**original)
                replacement.pk = self.student.pk
                setattr(replacement, field, value)

                with self.assertRaises(ValidationError):
                    Student.objects.bulk_create(
                        [replacement], update_conflicts=True, update_fields=[field]
                    )

                self.student.refresh_from_db()
                self.assertEqual(model_to_dict(self.student), original)
                allocation.refresh_from_db()
                allocation.bed.refresh_from_db()
                self.assertEqual(allocation.status, Allocation.AllocationStatus.ACTIVE)
                self.assertEqual(allocation.bed.status, Bed.BedStatus.OCCUPIED)

    def test_normal_bulk_creation_still_accepts_new_students(self):
        from django.forms.models import model_to_dict

        data = model_to_dict(self.student)
        data.pop("id", None)
        data["student_id"] = "BULK000000001"
        student = Student(**data)

        Student.objects.bulk_create([student])

        self.assertTrue(Student.objects.filter(student_id="BULK000000001").exists())

    def test_gender_cannot_change_to_conflict_with_active_hostel(self):
        self.allocate_student()
        self.student.gender = Student.Gender.FEMALE

        with self.assertRaises(ValidationError):
            self.student.save(update_fields=["gender"])

        self.student.refresh_from_db()
        self.assertEqual(self.student.gender, Student.Gender.MALE)

    def test_admin_form_shows_active_bed_when_deactivation_is_refused(self):
        allocation = self.allocate_student()
        form = self.edit_form(status=Student.Status.INACTIVE)

        self.assertFalse(form.is_valid())
        self.assertIn(allocation.bed.label, str(form.errors["status"]))

    def test_admin_form_rejects_gender_change_before_save(self):
        self.allocate_student()
        form = self.edit_form(gender=Student.Gender.FEMALE)

        self.assertFalse(form.is_valid())
        self.assertIn("gender", form.errors)

    def test_admin_change_preserves_identity_and_restricts_account_link(self):
        from django.forms.models import model_to_dict

        administrator = User.objects.create_superuser(
            username="student-admin-integrity", password="Validpass123"
        )
        self.client.force_login(administrator)
        payload = model_to_dict(self.student)
        payload.update(student_id="PES0000000999", mobile="9000000000", user="")
        original_id = self.student.student_id

        response = self.client.post(
            reverse("admin:students_student_change", args=[self.student.pk]), payload
        )

        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.student_id, original_id)
        self.assertEqual(self.student.mobile, "9000000000")
