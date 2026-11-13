"""Remaining student management permissions, invalid update and idempotence units."""

from inspect import unwrap
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from accounts.models import User
from allocations.models import Allocation

from .models import Student
from .views import student_deactivate, student_list, student_update


class RemainingStudentViewUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.warden = SimpleNamespace(is_authenticated=True, role=User.Role.WARDEN)

    def test_student_role_cannot_list_update_or_deactivate_other_students(self):
        for view, args in (
            (student_list, ()),
            (student_update, (8,)),
            (student_deactivate, (8,)),
        ):
            with (
                self.subTest(view=view.__name__),
                patch("students.views.Student.objects.all") as query,
                patch("students.views.Student.objects.select_for_update") as locked,
                patch("students.views.get_object_or_404") as lookup,
                patch("students.views.StudentForm") as form,
                patch("students.views.record_event") as audit,
            ):
                request = self.factory.post("/students/8/", {"name": "changed"})
                request.user = SimpleNamespace(
                    is_authenticated=True, role=User.Role.STUDENT
                )
                # The deactivation transaction has separate integration coverage.
                core = unwrap(view) if view is student_deactivate else view
                response = core(request, *args)
                self.assertEqual(response.status_code, 403)
                query.assert_not_called()
                locked.assert_not_called()
                lookup.assert_not_called()
                form.assert_not_called()
                audit.assert_not_called()

    def test_update_get_and_invalid_post_keep_identity_read_only_and_hide_status(self):
        student = SimpleNamespace(pk=8, student_id="STUDENT000008")
        for method in ("get", "post"):
            with (
                self.subTest(method=method),
                patch(
                    "students.views.get_object_or_404", return_value=student
                ) as lookup,
                patch("students.views.StudentForm") as form_type,
                patch("students.views.record_event") as audit,
                patch(
                    "students.views.render", return_value=HttpResponse("errors")
                ) as render,
            ):
                request = getattr(self.factory, method)("/students/8/", {"name": ""})
                request.user = self.warden
                form = form_type.return_value
                id_field = SimpleNamespace(disabled=False)
                form.fields = {"student_id": id_field, "status": Mock(), "name": Mock()}
                form.is_valid.return_value = False
                self.assertEqual(student_update(request, 8).content, b"errors")
                lookup.assert_called_once_with(Student, pk=8)
                form_type.assert_called_once_with(
                    request.POST if method == "post" else None, instance=student
                )
                self.assertTrue(id_field.disabled)
                self.assertNotIn("status", form.fields)
                render.assert_called_once_with(
                    request,
                    "students/student_form.html",
                    {"form": form, "heading": "Update Student", "student": student},
                )
                form.save.assert_not_called()
                audit.assert_not_called()

    def test_already_inactive_student_is_not_saved_or_audited_again(self):
        student = Mock(pk=8, student_id="STUDENT000008", status=Student.Status.INACTIVE)
        request = self.factory.post("/students/8/deactivate/")
        request.user = self.warden
        with (
            patch("students.views.Student.objects.select_for_update") as locked,
            patch("students.views.get_object_or_404", return_value=student) as lookup,
            patch("students.views.Allocation.objects.select_related") as allocations,
            patch("students.views.messages.info") as info,
            patch("students.views.messages.success") as success,
            patch("students.views.record_event") as audit,
            patch(
                "students.views.redirect", return_value=HttpResponse("students")
            ) as redirect,
        ):
            allocations.return_value.filter.return_value.first.return_value = None
            self.assertEqual(
                unwrap(student_deactivate)(request, 8).content, b"students"
            )
        lookup.assert_called_once_with(locked.return_value, pk=8)
        allocations.assert_called_once_with("bed__room__hostel")
        allocations.return_value.filter.assert_called_once_with(
            student=student, status=Allocation.AllocationStatus.ACTIVE
        )
        allocations.return_value.filter.return_value.first.assert_called_once_with()
        info.assert_called_once_with(request, "This student is already inactive.")
        redirect.assert_called_once_with("student-list")
        student.save.assert_not_called()
        audit.assert_not_called()
        success.assert_not_called()
