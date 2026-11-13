"""Payment-view serialization and presentation decisions with data access mocked."""

import json
from datetime import date
from decimal import Decimal
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from accounts.models import User

from .views import (
    payment_adjust,
    payment_list,
    payment_receipt,
    payment_receipt_pdf,
    serialize,
    student_payment_status,
)


class PaymentViewUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = SimpleNamespace(is_authenticated=True, role=User.Role.WARDEN)

    def get(self, data=None, json_output=False):
        request = self.factory.get(
            "/payments/",
            data or {},
            HTTP_ACCEPT="application/json" if json_output else "text/html",
        )
        request.user = self.user
        return request

    def payment(self, **overrides):
        values = {
            "receipt_no": "R1",
            "student": SimpleNamespace(student_id="S1"),
            "amount": Decimal("25.50"),
            "date": date(2026, 11, 13),
            "mode": "Cash",
            "reference": "ABC",
            "adjustment_of_id": None,
            "adjustment_reason": "",
        }
        return SimpleNamespace(**(values | overrides))

    def test_serialization_formats_amount_date_and_optional_adjustment(self):
        normal = serialize(self.payment())
        self.assertEqual(
            (normal["student_id"], normal["amount"], normal["date"]),
            ("S1", "25.50", "2026-11-13"),
        )
        self.assertIsNone(normal["adjustment_of"])
        adjustment = serialize(
            self.payment(
                adjustment_of_id=2,
                adjustment_of=SimpleNamespace(receipt_no="R0"),
                adjustment_reason="refund",
            )
        )
        self.assertEqual(
            (adjustment["adjustment_of"], adjustment["adjustment_reason"]),
            ("R0", "refund"),
        )

    @patch("payments.views.serialize", side_effect=lambda item: {"id": item})
    @patch("payments.views.Paginator")
    @patch("payments.views.Payment.objects.select_related")
    def test_payment_search_returns_paginated_json(
        self, payments, paginator, serializer
    ):
        page = MagicMock(number=2)
        page.paginator = SimpleNamespace(count=1)
        page.__iter__.return_value = iter(["payment"])
        paginator.return_value.get_page.return_value = page
        response = payment_list(
            self.get({"q": " Alice ", "page": "2"}, json_output=True)
        )
        self.assertEqual(
            json.loads(response.content),
            {"results": [{"id": "payment"}], "total": 1, "page": 2},
        )
        payments.return_value.filter.assert_called_once()
        paginator.return_value.get_page.assert_called_once_with("2")

    @patch("payments.views.render", return_value=HttpResponse("list"))
    @patch("payments.views.Paginator")
    @patch("payments.views.Payment.objects.select_related")
    def test_payment_list_renders_trimmed_search_term(
        self, payments, paginator, render
    ):
        response = payment_list(self.get({"q": "  Alice  "}))
        self.assertEqual(response.content, b"list")
        self.assertEqual(render.call_args.args[1], "payments/payment_list.html")
        self.assertEqual(render.call_args.args[2]["query"], "Alice")

    @patch("payments.views.render", return_value=HttpResponse("receipt"))
    @patch("payments.views.get_receipt")
    def test_html_receipt_includes_adjustments(self, receipt, render):
        payment = Mock()
        receipt.return_value = payment
        self.assertEqual(payment_receipt(self.get(), "R1").content, b"receipt")
        self.assertIs(render.call_args.args[2]["payment"], payment)
        payment.adjustments.all.assert_called_once()

    @patch("payments.views.receipt_pdf", return_value=BytesIO(b"%PDF-test"))
    @patch("payments.views.get_receipt")
    def test_receipt_pdf_is_a_named_attachment(self, receipt, pdf):
        receipt.return_value = SimpleNamespace(receipt_no="R1")
        response = payment_receipt_pdf(self.get(), "R1")
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn('filename="R1.pdf"', response["Content-Disposition"])
        self.assertEqual(b"".join(response.streaming_content), b"%PDF-test")

    @patch("payments.views.render", return_value=HttpResponse("status"))
    @patch("payments.views.status_row", return_value={"status": "Paid"})
    @patch("payments.views.get_object_or_404")
    @patch("payments.views.payment_status_queryset")
    def test_html_payment_status_includes_selected_student(
        self, query, lookup, status, render
    ):
        self.assertEqual(student_payment_status(self.get(), 12).content, b"status")
        self.assertIs(render.call_args.args[2]["student"], lookup.return_value)
        self.assertEqual(render.call_args.args[2]["row"], {"status": "Paid"})

    @patch("payments.views.payment_form", return_value=HttpResponse("adjustment"))
    @patch("payments.views.get_object_or_404")
    @patch("payments.views.Payment.objects.select_related")
    def test_adjustment_looks_up_only_original_payment(self, query, lookup, form):
        request = self.get()
        self.assertEqual(payment_adjust(request, "R1").content, b"adjustment")
        self.assertEqual(
            lookup.call_args.kwargs, {"receipt_no": "R1", "adjustment_of__isnull": True}
        )
        form.assert_called_once_with(request, lookup.return_value)
