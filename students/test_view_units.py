"""Unit checks for student-view permissions and form/audit decisions."""

from contextlib import nullcontext
from inspect import unwrap
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from accounts.models import User
from audit.models import AuditEvent

from .views import (
    can_manage_students,
    my_records,
    student_create,
    student_deactivate,
    student_list,
    student_update,
)


class StudentViewUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.warden = SimpleNamespace(is_authenticated=True, role=User.Role.WARDEN)

    def test_manage_permission_accepts_only_authenticated_staff(self):
        for authenticated, role, expected in (
            (False, User.Role.ADMIN, False),
            (True, User.Role.ADMIN, True),
            (True, User.Role.WARDEN, True),
            (True, User.Role.STUDENT, False),
        ):
            with self.subTest(authenticated=authenticated, role=role):
                self.assertEqual(
                    can_manage_students(
                        SimpleNamespace(is_authenticated=authenticated, role=role)
                    ),
                    expected,
                )

    @patch("students.views.StudentForm")
    def test_student_role_cannot_open_registration(self, form):
        request = self.factory.get("/students/new/")
        request.user = SimpleNamespace(is_authenticated=True, role=User.Role.STUDENT)
        self.assertEqual(student_create(request).status_code, 403)
        form.assert_not_called()

    @patch("students.views.redirect", return_value=HttpResponse("redirected"))
    @patch("students.views.messages.success")
    @patch("students.views.record_event")
    @patch("students.views.transaction.atomic", return_value=nullcontext())
    @patch("students.views.StudentForm")
    def test_registration_saves_and_audits_valid_student(
        self, form, atomic, audit, message, redirect
    ):
        student = SimpleNamespace(student_id="STUDENT000001")
        form.return_value.is_valid.return_value = True
        form.return_value.save.return_value = student
        request = self.factory.post("/students/new/", {"name": "Student"})
        request.user = self.warden
        self.assertEqual(student_create(request).content, b"redirected")
        audit.assert_called_once_with(
            user=self.warden, action=AuditEvent.Action.CREATE, record=student
        )
        redirect.assert_called_once_with("student-list")
        message.assert_called_once()
        atomic.assert_called_once()

    @patch("students.views.render", return_value=HttpResponse("form"))
    @patch("students.views.record_event")
    @patch("students.views.StudentForm")
    def test_invalid_registration_is_rendered_without_audit(self, form, audit, render):
        form.return_value.is_valid.return_value = False
        request = self.factory.post("/students/new/", {"name": ""})
        request.user = self.warden
        self.assertEqual(student_create(request).content, b"form")
        self.assertEqual(render.call_args.args[2]["heading"], "Register Student")
        form.return_value.save.assert_not_called()
        audit.assert_not_called()

    @patch("students.views.redirect", return_value=HttpResponse("redirected"))
    @patch("students.views.messages.success")
    @patch("students.views.record_event")
    @patch("students.views.transaction.atomic", return_value=nullcontext())
    @patch("students.views.StudentForm")
    @patch("students.views.get_object_or_404")
    def test_update_disables_student_id_and_does_not_expose_status(
        self, lookup, form, atomic, audit, message, redirect
    ):
        student = SimpleNamespace(student_id="STUDENT000001")
        lookup.return_value = student
        id_field = Mock()
        form.return_value.fields = {"student_id": id_field, "status": Mock()}
        form.return_value.is_valid.return_value = True
        form.return_value.save.return_value = student
        request = self.factory.post("/students/1/", {"name": "Updated"})
        request.user = self.warden
        self.assertEqual(student_update(request, 1).content, b"redirected")
        self.assertTrue(id_field.disabled)
        self.assertNotIn("status", form.return_value.fields)
        audit.assert_called_once_with(
            user=self.warden, action=AuditEvent.Action.UPDATE, record=student
        )
        redirect.assert_called_once_with("student-list")

    @patch("students.views.render", return_value=HttpResponse("list"))
    @patch("students.views.Paginator")
    @patch("students.views.Student.objects.all")
    def test_search_trims_query_and_renders_distinct_page(
        self, students, paginator, render
    ):
        request = self.factory.get("/students/", {"q": "  Alice  ", "page": "2"})
        request.user = self.warden
        self.assertEqual(student_list(request).content, b"list")
        students.return_value.filter.assert_called_once()
        students.return_value.filter.return_value.distinct.assert_called_once()
        paginator.return_value.get_page.assert_called_once_with("2")
        self.assertEqual(render.call_args.args[2]["query"], "Alice")

    @patch("students.views.render", return_value=HttpResponse("no profile"))
    @patch("students.views.payment_status_queryset")
    @patch("students.views.Student.objects.filter")
    def test_unlinked_student_gets_empty_records_page(self, students, balances, render):
        balances.return_value.first.return_value = None
        request = self.factory.get("/my-records/")
        request.user = SimpleNamespace(
            is_authenticated=True, role=User.Role.STUDENT, pk=12
        )
        self.assertEqual(my_records(request).content, b"no profile")
        students.assert_called_once_with(user_id=12)
        self.assertEqual(render.call_args.args[2], {"student": None})

    @patch("students.views.render", return_value=HttpResponse("records"))
    @patch("students.views.status_row", return_value={"status": "Partial"})
    @patch("students.views.Payment.objects.filter")
    @patch("students.views.payment_status_queryset")
    @patch("students.views.Student.objects.filter")
    def test_records_select_current_allocation_and_own_payments(
        self, students, balances, payments, status, render
    ):
        active = SimpleNamespace(status="Active")
        completed = SimpleNamespace(status="Completed")
        student = Mock(pk=12)
        student.allocations.exclude.return_value.select_related.return_value.order_by.return_value = [
            completed,
            active,
        ]
        balances.return_value.first.return_value = student
        request = self.factory.get("/my-records/")
        request.user = SimpleNamespace(
            is_authenticated=True, role=User.Role.STUDENT, pk=7
        )
        self.assertEqual(my_records(request).content, b"records")
        students.assert_called_once_with(user_id=7)
        payments.assert_called_once_with(student_id=12)
        context = render.call_args.args[2]
        self.assertIs(context["current_allocation"], active)
        self.assertEqual(context["payment_summary"], {"status": "Partial"})
        status.assert_called_once_with(student)

    @patch("students.views.redirect", return_value=HttpResponse("redirected"))
    @patch("students.views.messages.error")
    @patch("students.views.record_event")
    @patch("students.views.Allocation.objects.select_related")
    @patch("students.views.get_object_or_404")
    @patch("students.views.Student.objects.select_for_update")
    def test_deactivation_with_active_allocation_is_rejected(
        self, locked, lookup, allocations, audit, message, redirect
    ):
        student = Mock(student_id="STUDENT000001")
        lookup.return_value = student
        allocation = SimpleNamespace(
            bed=SimpleNamespace(
                label="A", room=SimpleNamespace(hostel=SimpleNamespace(name="H"))
            )
        )
        allocations.return_value.filter.return_value.first.return_value = allocation
        request = self.factory.post("/students/1/deactivate/")
        request.user = self.warden
        # The core decision is isolated; real transaction and role decorators are tested separately.
        self.assertEqual(unwrap(student_deactivate)(request, 1).content, b"redirected")
        student.save.assert_not_called()
        audit.assert_not_called()
        message.assert_called_once()

    @patch("students.views.redirect", return_value=HttpResponse("redirected"))
    @patch("students.views.messages.success")
    @patch("students.views.record_event")
    @patch("students.views.Allocation.objects.select_related")
    @patch("students.views.get_object_or_404")
    @patch("students.views.Student.objects.select_for_update")
    def test_deactivation_without_allocation_saves_and_audits(
        self, locked, lookup, allocations, audit, message, redirect
    ):
        student = Mock(student_id="STUDENT000001", status="Active")
        lookup.return_value = student
        allocations.return_value.filter.return_value.first.return_value = None
        request = self.factory.post("/students/1/deactivate/")
        request.user = self.warden
        self.assertEqual(unwrap(student_deactivate)(request, 1).content, b"redirected")
        self.assertEqual(student.status, "Inactive")
        student.save.assert_called_once_with(update_fields=["status", "updated_at"])
        audit.assert_called_once_with(
            user=self.warden, action=AuditEvent.Action.DEACTIVATE, record=student
        )
