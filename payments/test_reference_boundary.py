"""Model validation must reject non-alphanumeric receipt references."""

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from .models import Payment


class PaymentReferenceBoundaryTests(SimpleTestCase):
    def test_reference_rejects_trailing_line_breaks(self):
        field = Payment._meta.get_field("reference")
        for value in ("PAY123\n", "\n", "PAY123\r\n"):
            with self.subTest(value=repr(value)), self.assertRaises(ValidationError):
                field.clean(value, Payment())

    def test_reference_accepts_empty_or_thirty_alphanumeric_characters(self):
        field = Payment._meta.get_field("reference")
        for value in ("", "PAY123", "A9" * 15):
            with self.subTest(value=value):
                self.assertEqual(field.clean(value, Payment()), value)
