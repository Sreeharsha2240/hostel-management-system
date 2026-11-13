"""Receipt rendering from in-memory payment data."""

from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from django.test import SimpleTestCase
from pypdf import PdfReader

from .receipts import receipt_pdf


class ReceiptPDFUnitTests(SimpleTestCase):
    def payment(self, **overrides):
        values = {
            "receipt_no": "R00000000001",
            "student": SimpleNamespace(student_id="S123", name="A & B"),
            "date": date(2026, 11, 13),
            "amount": Decimal("125.50"),
            "mode": "UPI",
            "reference": "",
            "adjustment_of_id": None,
            "adjustment_reason": "",
        }
        return SimpleNamespace(**(values | overrides))

    def text(self, payment):
        result = receipt_pdf(payment)
        self.assertEqual(result.tell(), 0)
        return "\n".join(page.extract_text() for page in PdfReader(result).pages)

    def test_payment_receipt_contains_identifiers_amount_and_safe_text(self):
        text = self.text(self.payment())
        for value in (
            "Payment receipt",
            "R00000000001",
            "S123",
            "A & B",
            "13-11-2026",
            "125.50",
            "UPI",
            "None",
        ):
            with self.subTest(value=value):
                self.assertIn(value, text)

    def test_adjustment_receipt_names_original_and_reason(self):
        original = SimpleNamespace(receipt_no="R00000000001")
        payment = self.payment(
            receipt_no="R00000000002",
            amount=Decimal("-25"),
            adjustment_of_id=1,
            adjustment_of=original,
            adjustment_reason="Correction & refund",
        )
        text = self.text(payment)
        for value in (
            "Payment adjustment receipt",
            "R00000000002",
            "R00000000001",
            "-25.00",
            "Correction & refund",
        ):
            with self.subTest(value=value):
                self.assertIn(value, text)

    def test_markup_in_student_name_is_rendered_as_literal_text(self):
        payment = self.payment(
            student=SimpleNamespace(student_id="S123", name="<b>Student</b>")
        )
        self.assertIn("<b>Student</b>", self.text(payment))
