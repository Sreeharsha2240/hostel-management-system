"""Payment form failure and dispatch decisions with services and queries isolated."""

import json
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from accounts.models import User

from .forms import PaymentForm
from .views import get_receipt, payment_create, payment_form, payment_list


class RemainingPaymentViewUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.actor = SimpleNamespace(is_authenticated=True, role=User.Role.WARDEN)

    def post(self, data=None, json_output=False):
        request = self.factory.post(
            "/payments/",
            data or {},
            HTTP_ACCEPT="application/json" if json_output else "text/html",
        )
        request.user = self.actor
        return request

    def test_list_post_reaches_payment_form_once_and_preserves_response(self):
        request = self.post({"amount": "bad"})
        response = HttpResponse("payment form errors", status=422)
        with (
            patch("payments.views.payment_form", return_value=response) as form,
            patch("payments.views.Payment.objects.select_related") as query,
        ):
            self.assertIs(payment_list(request), response)
        form.assert_called_once_with(request)
        query.assert_not_called()

    def test_create_rejects_unsupported_method_before_form_handling(self):
        request = self.factory.delete("/payments/new/")
        request.user = self.actor
        with patch("payments.views.payment_form") as form:
            response = payment_create(request)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response["Allow"], "GET, POST")
        form.assert_not_called()

    def test_html_success_records_receipt_message_and_redirects_to_that_receipt(self):
        request = self.post({"student": "3", "amount": "25.00"})
        student = SimpleNamespace(pk=3)
        values = {"student": student, "amount": "25.00"}
        payment = SimpleNamespace(receipt_no="HMS-2026-0042")
        with (
            patch("payments.views.PaymentForm") as form_type,
            patch("payments.views.record_payment", return_value=payment) as service,
            patch("payments.views.messages.success") as message,
            patch(
                "payments.views.redirect", return_value=HttpResponse("receipt")
            ) as redirect,
        ):
            form_type.return_value.is_valid.return_value = True
            form_type.return_value.cleaned_data = values.copy()
            self.assertEqual(payment_form(request).content, b"receipt")
        service.assert_called_once_with(actor=self.actor, **values)
        message.assert_called_once_with(request, "Receipt HMS-2026-0042 recorded.")
        redirect.assert_called_once_with("payment-receipt", receipt_no="HMS-2026-0042")
        self.assertEqual(form_type.return_value.cleaned_data, values)

    def test_invalid_json_form_returns_real_field_errors_without_recording_payment(
        self,
    ):
        request = self.post(
            {"amount": "", "student": "not-an-integer"}, json_output=True
        )
        form = PaymentForm(request.POST)
        self.assertFalse(form.is_valid())
        with (
            patch("payments.views.PaymentForm", return_value=form) as form_type,
            patch("payments.views.record_payment") as service,
        ):
            response = payment_form(request)
        self.assertEqual(response.status_code, 404)
        payload = json.loads(response.content)
        self.assertEqual(payload["error"]["code"], "NOT_FOUND")
        self.assertIn("amount", payload["error"]["fields"])
        self.assertIn("student", payload["error"]["fields"])
        self.assertEqual(
            payload["error"]["fields"]["student"][0]["code"], "invalid_choice"
        )
        self.assertEqual(payload["error"]["fields"]["amount"][0]["code"], "required")
        self.assertEqual(form_type.call_args.args, (request.POST,))
        service.assert_not_called()

    def test_html_invalid_form_and_domain_error_keep_bound_form_and_original(self):
        original = SimpleNamespace(student=SimpleNamespace(pk=3))
        for domain_error in (False, True):
            with (
                self.subTest(domain_error=domain_error),
                patch("payments.views.AdjustmentForm") as form_type,
                patch("payments.views.record_payment") as service,
                patch(
                    "payments.views.render", return_value=HttpResponse("errors")
                ) as render,
                patch("payments.views.messages.success") as message,
                patch("payments.views.redirect") as redirect,
            ):
                request = self.post({"amount": "-25", "adjustment_reason": "refund"})
                form = form_type.return_value
                form.is_valid.return_value = domain_error
                form.cleaned_data = {"amount": "-25", "adjustment_reason": "refund"}
                service.side_effect = ValidationError(
                    ["Receipt is closed.", "Cannot adjust."]
                )
                self.assertEqual(payment_form(request, original).content, b"errors")
                form_type.assert_called_with(request.POST)
                render.assert_called_once_with(
                    request,
                    "payments/payment_form.html",
                    {"form": form, "original": original},
                )
                if domain_error:
                    service.assert_called_once_with(
                        actor=self.actor,
                        student=original.student,
                        adjustment_of=original,
                        amount="-25",
                        adjustment_reason="refund",
                    )
                    form.add_error.assert_called_once_with(
                        None, "Receipt is closed.; Cannot adjust."
                    )
                else:
                    service.assert_not_called()
                    form.add_error.assert_not_called()
                message.assert_not_called()
                redirect.assert_not_called()

    def test_receipt_lookup_preserves_receipt_identifier_and_loads_adjustment(self):
        receipt = Mock()
        with (
            patch("payments.views.Payment.objects.select_related") as related,
            patch("payments.views.get_object_or_404", return_value=receipt) as lookup,
        ):
            self.assertIs(get_receipt("HMS-2026-0042"), receipt)
        related.assert_called_once_with("student", "adjustment_of")
        lookup.assert_called_once_with(related.return_value, receipt_no="HMS-2026-0042")
