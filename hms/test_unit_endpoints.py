"""Isolated response and service-boundary checks for allocation and payment views."""

import json
from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import RequestFactory, SimpleTestCase

from accounts.models import User
from allocations.views import allocation_create, allocation_release, allocation_transfer
from payments.views import payment_form


class EndpointUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = SimpleNamespace(is_authenticated=True, role=User.Role.WARDEN)

    def request(self, payload, url_name="allocation-release"):
        request = self.factory.post(
            "/test/", data=json.dumps(payload), content_type="application/json"
        )
        request.user = self.user
        request.resolver_match = SimpleNamespace(url_name=url_name)
        return request

    @patch("allocations.views.AllocationForm")
    @patch("allocations.views.Student.objects.filter")
    @patch("allocations.views.allocate")
    def test_allocation_rejects_unknown_student_before_service(
        self, service, students, form
    ):
        students.return_value.first.return_value = None
        response = allocation_create(
            self.request({"student_id": "missing", "bed_id": 3})
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content)["error"]["code"], "NOT_FOUND")
        service.assert_not_called()

    @patch("allocations.views.serialize", return_value={"allocation_id": 8})
    @patch("allocations.views.allocate")
    @patch("allocations.views.Student.objects.filter")
    @patch("allocations.views.AllocationForm")
    def test_allocation_resolves_student_and_returns_created_record(
        self, form, students, service, serialize
    ):
        students.return_value.first.return_value = SimpleNamespace(pk=12)
        form.return_value.is_valid.return_value = True
        form.return_value.cleaned_data = {"student": "student", "bed": "bed"}
        response = allocation_create(self.request({"student_id": "S1", "bed_id": 3}))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content), {"allocation_id": 8})
        form.assert_any_call({"student": 12, "bed": 3})
        service.assert_called_once_with(actor=self.user, student="student", bed="bed")
        serialize.assert_called_once_with(service.return_value)

    @patch(
        "allocations.views.allocate",
        side_effect=ValidationError("occupied", code="BED_OCCUPIED"),
    )
    @patch("allocations.views.Student.objects.filter")
    @patch("allocations.views.AllocationForm")
    def test_allocation_maps_bed_conflict_to_409(self, form, students, service):
        students.return_value.first.return_value = SimpleNamespace(pk=12)
        form.return_value.is_valid.return_value = True
        form.return_value.cleaned_data = {}
        response = allocation_create(self.request({"student_id": "S1", "bed_id": 3}))
        self.assertEqual(response.status_code, 409)
        self.assertEqual(json.loads(response.content)["error"]["code"], "BED_OCCUPIED")
        service.assert_called_once()

    @patch("allocations.views.serialize", return_value={"allocation_id": 9})
    @patch("allocations.views.transfer")
    @patch("allocations.views.TransferForm")
    @patch("allocations.views.get_object_or_404")
    @patch("allocations.views.Allocation.objects.select_related")
    def test_transfer_maps_new_bed_and_calls_service(
        self, query, lookup, form, service, serialize
    ):
        lookup.return_value = SimpleNamespace(pk=8)
        form.return_value.is_valid.return_value = True
        form.return_value.cleaned_data = {"new_bed": "bed"}
        response = allocation_transfer(self.request({"new_bed_id": 3}), 8)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"allocation_id": 9})
        form.assert_any_call({"new_bed": 3})
        service.assert_called_once_with(allocation_id=8, actor=self.user, new_bed="bed")

    @patch(
        "allocations.views.serialize",
        return_value={"allocation_id": 8, "status": "Completed"},
    )
    @patch("allocations.views.release")
    @patch("allocations.views.ReleaseForm")
    @patch("allocations.views.get_object_or_404")
    @patch("allocations.views.Allocation.objects.select_related")
    def test_release_returns_public_released_status(
        self, query, lookup, form, service, serialize
    ):
        lookup.return_value = SimpleNamespace(pk=8)
        form.return_value.is_valid.return_value = True
        form.return_value.cleaned_data = {"vacate_date": date(2026, 11, 13)}
        response = allocation_release(self.request({"vacate_date": "2026-11-13"}), 8)
        self.assertEqual(
            json.loads(response.content), {"allocation_id": 8, "status": "Released"}
        )
        service.assert_called_once_with(
            allocation_id=8, actor=self.user, vacate_date=date(2026, 11, 13)
        )

    @patch("payments.views.PaymentForm")
    @patch("payments.views.Student.objects.filter")
    @patch("payments.views.record_payment")
    def test_payment_rejects_unknown_student_before_service(
        self, service, students, form
    ):
        students.return_value.first.return_value = None
        response = payment_form(self.request({"student_id": "missing"}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content)["error"]["code"], "NOT_FOUND")
        service.assert_not_called()

    @patch("payments.views.serialize", return_value={"receipt_no": "R1"})
    @patch("payments.views.record_payment")
    @patch("payments.views.Student.objects.filter")
    @patch("payments.views.PaymentForm")
    def test_payment_resolves_student_and_returns_receipt(
        self, form, students, service, serialize
    ):
        students.return_value.first.return_value = SimpleNamespace(pk=12)
        form.return_value.is_valid.return_value = True
        form.return_value.cleaned_data = {"student": "student", "amount": 25}
        response = payment_form(self.request({"student_id": "S1", "amount": "25"}))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content), {"receipt_no": "R1"})
        form.assert_any_call({"student": 12, "amount": "25"})
        service.assert_called_once_with(actor=self.user, student="student", amount=25)

    @patch(
        "payments.views.record_payment",
        side_effect=ValidationError("invalid", code="IMMUTABLE_FIELD"),
    )
    @patch("payments.views.Student.objects.filter")
    @patch("payments.views.PaymentForm")
    def test_payment_maps_domain_validation_to_422(self, form, students, service):
        students.return_value.first.return_value = SimpleNamespace(pk=12)
        form.return_value.is_valid.return_value = True
        form.return_value.cleaned_data = {}
        response = payment_form(self.request({"student_id": "S1"}))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.content)["error"]["code"], "IMMUTABLE_FIELD"
        )
        service.assert_called_once()
