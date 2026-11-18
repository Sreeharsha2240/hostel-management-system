"""JSON text values must not become coerced transaction references."""

from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from .views import payment_form


class PaymentJsonScalarTests(SimpleTestCase):
    def test_nontext_references_are_rejected_before_student_lookup(self):
        for reference in (True, False, 123, 1.25):
            with (
                self.subTest(reference=reference),
                patch("payments.views.Student.objects.filter") as lookup,
            ):
                request = RequestFactory().post(
                    "/payments/",
                    {
                        "student_id": "PES1UG24CS001",
                        "amount": "100.00",
                        "mode": "UPI",
                        "date": "2026-11-01",
                        "reference": reference,
                    },
                    content_type="application/json",
                )
                request.user = SimpleNamespace(role="warden")
                response = payment_form(request)
                self.assertEqual(response.status_code, 400)
                self.assertIn(b"text value", response.content)
                lookup.assert_not_called()
