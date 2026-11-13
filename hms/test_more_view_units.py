"""Allocation and payment view contracts with data services mocked."""

import json
from datetime import date
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from accounts.models import User
from allocations.views import (
    allocation_create,
    allocation_history,
    allocation_list,
    allocation_release,
    allocation_transfer,
)
from payments.views import payment_form, payment_receipt, student_payment_status


class ViewContractUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = SimpleNamespace(is_authenticated=True, role=User.Role.WARDEN)

    def get(self, path="/test/", data=None, json_output=False):
        request = self.factory.get(
            path,
            data or {},
            HTTP_ACCEPT="application/json" if json_output else "text/html",
        )
        request.user = self.user
        return request

    def post(self, data, json_input=False, url_name="allocation-release"):
        request = (
            self.factory.post(
                "/test/", data=json.dumps(data), content_type="application/json"
            )
            if json_input
            else self.factory.post("/test/", data)
        )
        request.user = self.user
        request.resolver_match = SimpleNamespace(url_name=url_name)
        return request

    @patch("allocations.views.render", return_value=HttpResponse("form"))
    @patch("allocations.views.available_beds", return_value="beds")
    @patch("allocations.views.Student.objects.filter")
    @patch("allocations.views.AllocationForm")
    def test_create_form_limits_students_and_available_beds(
        self, form, students, beds, render
    ):
        student_field, bed_field = Mock(), Mock()
        form.return_value.fields = {"student": student_field, "bed": bed_field}
        self.assertEqual(allocation_create(self.get()).content, b"form")
        self.assertEqual(bed_field.queryset, "beds")
        students.return_value.exclude.assert_called_once()
        self.assertEqual(
            render.call_args.args[2]["heading"], "Create Hostel Allocation"
        )

    @patch("allocations.views.redirect", return_value=HttpResponse("redirect"))
    @patch("allocations.views.messages.success")
    @patch("allocations.views.allocate")
    @patch("allocations.views.AllocationForm")
    def test_successful_html_allocation_calls_service_and_redirects(
        self, form, service, message, redirect
    ):
        allocation = SimpleNamespace(
            bed=SimpleNamespace(label="A"), student=SimpleNamespace(name="N")
        )
        form.return_value.is_valid.return_value = True
        form.return_value.cleaned_data = {"student": "student", "bed": "bed"}
        service.return_value = allocation
        self.assertEqual(
            allocation_create(self.post({"student": "1", "bed": "2"})).content,
            b"redirect",
        )
        service.assert_called_once_with(actor=self.user, student="student", bed="bed")
        redirect.assert_called_once_with("allocation-list")
        message.assert_called_once()

    @patch(
        "allocations.views.form_error", return_value=HttpResponse("invalid", status=400)
    )
    @patch("allocations.views.allocate")
    @patch("allocations.views.Student.objects.filter")
    @patch("allocations.views.AllocationForm")
    def test_invalid_allocation_form_does_not_call_service(
        self, form, students, service, error
    ):
        students.return_value.first.return_value = SimpleNamespace(pk=1)
        form.return_value.is_valid.return_value = False
        response = allocation_create(
            self.post({"student_id": "S1", "bed_id": 2}, json_input=True)
        )
        self.assertEqual(response.status_code, 400)
        service.assert_not_called()
        error.assert_called_once()

    @patch("allocations.views.render", return_value=HttpResponse("form"))
    @patch("allocations.views.available_beds")
    @patch("allocations.views.TransferForm")
    @patch("allocations.views.get_object_or_404")
    @patch("allocations.views.Allocation.objects.select_related")
    def test_transfer_form_excludes_current_bed(
        self, query, lookup, form, available, render
    ):
        lookup.return_value = SimpleNamespace(bed_id=5)
        field = Mock()
        form.return_value.fields = {"new_bed": field}
        self.assertEqual(allocation_transfer(self.get(), 8).content, b"form")
        available.return_value.exclude.assert_called_once_with(pk=5)
        self.assertEqual(
            render.call_args.args[2]["confirmation_message"],
            "Transfer this allocation?",
        )

    @patch("allocations.views.timezone.localdate", return_value=date(2026, 11, 13))
    @patch("allocations.views.serialize", return_value={"status": "Completed"})
    @patch("allocations.views.release")
    @patch("allocations.views.ReleaseForm")
    @patch("allocations.views.get_object_or_404")
    @patch("allocations.views.Allocation.objects.select_related")
    def test_complete_without_body_uses_today(
        self, query, lookup, form, service, serialize, today
    ):
        lookup.return_value = SimpleNamespace(pk=8)
        form.return_value.is_valid.return_value = True
        form.return_value.cleaned_data = {"vacate_date": date(2026, 11, 13)}
        response = allocation_release(
            self.post({}, json_input=True, url_name="allocation-complete"), 8
        )
        self.assertEqual(json.loads(response.content)["status"], "Released")
        form.assert_any_call({"vacate_date": date(2026, 11, 13)})
        service.assert_called_once_with(
            allocation_id=8, actor=self.user, vacate_date=date(2026, 11, 13)
        )

    @patch("allocations.views.serialize", side_effect=lambda item: {"id": item})
    @patch("allocations.views.get_object_or_404")
    def test_allocation_history_json_contains_only_selected_students_records(
        self, lookup, serialize
    ):
        student = Mock(student_id="S1")
        student.allocations.select_related.return_value = [1, 2]
        lookup.return_value = student
        response = allocation_history(self.get(json_output=True), 8)
        self.assertEqual(
            json.loads(response.content),
            {"student_id": "S1", "allocations": [{"id": 1}, {"id": 2}]},
        )

    @patch("allocations.views.serialize", side_effect=lambda item: {"id": item})
    @patch("allocations.views.Paginator")
    @patch("allocations.views.Allocation.objects.select_related")
    def test_allocation_search_returns_paginated_json(
        self, allocations, paginator, serialize
    ):
        page = Mock(number=2, paginator=SimpleNamespace(count=1))
        page.__iter__ = Mock(return_value=iter([7]))
        paginator.return_value.get_page.return_value = page
        response = allocation_list(
            self.get(data={"q": " Alice ", "page": "2"}, json_output=True)
        )
        self.assertEqual(
            json.loads(response.content),
            {"results": [{"id": 7}], "page": 2, "total": 1},
        )
        allocations.return_value.filter.assert_called_once()
        paginator.return_value.get_page.assert_called_once_with("2")

    @patch("payments.views.serialize", return_value={"receipt_no": "R2"})
    @patch("payments.views.record_payment")
    @patch("payments.views.AdjustmentForm")
    def test_adjustment_uses_original_student_and_payment(
        self, form, service, serialize
    ):
        original = SimpleNamespace(student="student")
        form.return_value.is_valid.return_value = True
        form.return_value.cleaned_data = {
            "amount": "-5",
            "adjustment_reason": "correction",
        }
        response = payment_form(
            self.post(
                {"amount": "-5", "adjustment_reason": "correction"}, json_input=True
            ),
            original,
        )
        self.assertEqual(response.status_code, 201)
        service.assert_called_once_with(
            actor=self.user,
            student="student",
            adjustment_of=original,
            amount="-5",
            adjustment_reason="correction",
        )

    @patch("payments.views.render", return_value=HttpResponse("payment form"))
    @patch("payments.views.PaymentForm")
    def test_payment_get_renders_form(self, form, render):
        self.assertEqual(payment_form(self.get()).content, b"payment form")
        self.assertIsNone(render.call_args.args[2]["original"])

    @patch("payments.views.serialize", return_value={"receipt_no": "R1"})
    @patch("payments.views.get_receipt")
    def test_receipt_json_uses_requested_receipt(self, receipt, serialize):
        response = payment_receipt(self.get(json_output=True), "R1")
        self.assertEqual(json.loads(response.content), {"receipt_no": "R1"})
        receipt.assert_called_once_with("R1")
        serialize.assert_called_once_with(receipt.return_value)

    @patch("payments.views.status_row", return_value={"status": "Paid"})
    @patch("payments.views.get_object_or_404")
    @patch("payments.views.payment_status_queryset")
    def test_student_payment_status_json_uses_selected_student(
        self, query, lookup, status
    ):
        response = student_payment_status(self.get(json_output=True), 12)
        self.assertEqual(json.loads(response.content), {"status": "Paid"})
        lookup.assert_called_once_with(query.return_value, pk=12)
        status.assert_called_once_with(lookup.return_value)
