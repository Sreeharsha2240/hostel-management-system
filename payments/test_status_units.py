from decimal import Decimal
from types import SimpleNamespace

from django.test import SimpleTestCase

from .services import status_row


class PaymentStatusRowTests(SimpleTestCase):
    def test_configured_fee_overpayment_is_paid_without_negative_due(self):
        student = SimpleNamespace(
            student_id="ST001",
            name="Test Student",
            fee_amount=Decimal("1000.00"),
            amount_paid=Decimal("1000.01"),
            billing_hostel_id=1,
            billing_hostel="Test Hostel",
            billing_room="101",
            billing_bed="B1",
        )

        row = status_row(student)

        self.assertEqual(row["status"], "Paid")
        self.assertEqual(row["due"], "0.00")
        self.assertEqual(row["paid"], "1000.01")
        self.assertTrue(row["fee_configured"])
