"""Database-free tests for security and business-rule boundaries."""

import json
from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock, patch
from urllib.parse import parse_qs, urlsplit

from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from django.test import RequestFactory, SimpleTestCase

from accounts.decorators import roles_required
from accounts.models import User
from accounts.validators import LetterAndDigitPasswordValidator
from hms.decorators import staff_required
from hms.security_headers import ContentSecurityPolicyMiddleware
from payments.models import Payment
from payments.services import status_row
from reports.views import csv_cell


class IsolatedBusinessRuleTests(SimpleTestCase):
    @patch("payments.models.timezone.localdate", return_value=date(2026, 11, 13))
    def test_payment_clean_rejects_future_dates_and_invalid_amounts(self, today):
        cases = (
            (date(2026, 11, 13) + timedelta(days=1), Decimal("1"), "date"),
            (date(2026, 11, 13), Decimal("0"), "amount"),
            (date(2026, 11, 13), Decimal("-1"), "amount"),
        )
        for payment_date, amount, field in cases:
            with self.subTest(field=field, amount=amount):
                payment = Payment(date=payment_date, amount=amount)
                with self.assertRaises(ValidationError) as error:
                    payment.clean()
                self.assertIn(field, error.exception.message_dict)
        today.assert_called()

    @patch("payments.models.timezone.localdate", return_value=date(2026, 11, 13))
    def test_payment_correction_requires_original_and_nonblank_reason(self, today):
        cases = ((1, ""), (None, "reason"), (1, "   "))
        for original, reason in cases:
            with self.subTest(original=original, reason=reason):
                payment = Payment(
                    date=date(2026, 11, 13),
                    amount=Decimal("1"),
                    adjustment_of_id=original,
                    adjustment_reason=reason,
                )
                with self.assertRaises(ValidationError) as error:
                    payment.clean()
                self.assertIn("adjustment_reason", error.exception.message_dict)
        correction = Payment(
            date=date(2026, 11, 13),
            amount=Decimal("-1"),
            adjustment_of_id=1,
            adjustment_reason="  correction  ",
        )
        correction.clean()
        self.assertEqual(correction.adjustment_reason, "correction")
        today.assert_called()

    def test_payment_status_boundaries_and_due(self):
        cases = (
            ("0", "0", "Pending", "0.00", False),
            ("100", "0", "Pending", "100.00", True),
            ("100", "25", "Partial", "75.00", True),
            ("100", "100", "Paid", "0.00", True),
            ("100", "101", "Paid", "0.00", True),
        )
        for fee, paid, status, due, configured in cases:
            with self.subTest(fee=fee, paid=paid):
                student = SimpleNamespace(
                    student_id="S1",
                    name="Test",
                    fee_amount=Decimal(fee),
                    amount_paid=Decimal(paid),
                    billing_hostel_id=1,
                    billing_hostel=None,
                    billing_room=None,
                    billing_bed=None,
                )
                row = status_row(student)
                self.assertEqual((row["status"], row["due"]), (status, due))
                self.assertEqual(row["fee_configured"], configured)
                self.assertEqual((row["hostel"], row["room"], row["bed"]), ("", "", ""))

    def test_unassigned_student_has_no_configured_fee(self):
        student = SimpleNamespace(
            student_id="S1",
            name="Test",
            fee_amount=Decimal("100"),
            amount_paid=Decimal("20"),
            billing_hostel_id=None,
            billing_hostel=None,
            billing_room=None,
            billing_bed=None,
        )
        self.assertFalse(status_row(student)["fee_configured"])

    def test_csv_formula_prefixes_are_escaped_but_numbers_are_preserved(self):
        for value in (
            "=1+1",
            " +SUM(A1)",
            "-1",
            "@name",
            "\tplain",
            "\rplain",
            "\nplain",
        ):
            with self.subTest(value=value):
                self.assertEqual(csv_cell(value), "'" + value)
        for value in ("normal", "  plain", 42, Decimal("-2"), None):
            with self.subTest(value=value):
                self.assertEqual(csv_cell(value), value)

    def test_password_validator_requires_both_letters_and_digits(self):
        validator = LetterAndDigitPasswordValidator()
        for password in ("letters", "12345", "!@#", ""):
            with (
                self.subTest(password=password),
                self.assertRaises(ValidationError) as error,
            ):
                validator.validate(password)
            self.assertEqual(error.exception.code, "letter_and_digit")
        self.assertIsNone(validator.validate("abc123"))
        self.assertIn("letter and one digit", str(validator.get_help_text()))

    def test_security_header_is_added_and_existing_policy_preserved(self):
        response = HttpResponse("ok")
        middleware = ContentSecurityPolicyMiddleware(Mock(return_value=response))
        self.assertEqual(middleware(None)["Content-Security-Policy"], middleware.POLICY)
        response["Content-Security-Policy"] = "default-src 'none'"
        self.assertEqual(
            middleware(None)["Content-Security-Policy"], "default-src 'none'"
        )


class IsolatedAuthorizationTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = Mock(return_value=HttpResponse("allowed"))
        self.view.__name__ = "private_view"

    def test_anonymous_json_request_returns_401_without_calling_view(self):
        request = self.factory.get("/private/", HTTP_ACCEPT="application/json")
        request.user = SimpleNamespace(is_authenticated=False)
        response = roles_required(User.Role.ADMIN)(self.view)(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content)["error"]["code"], "AUTH_REQUIRED")
        self.view.assert_not_called()

    def test_anonymous_html_request_redirects_to_login_with_original_path(self):
        request = self.factory.get("/private/?page=2")
        request.user = SimpleNamespace(is_authenticated=False)
        response = roles_required(User.Role.ADMIN)(self.view)(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            parse_qs(urlsplit(response.url).query)["next"], ["/private/?page=2"]
        )
        self.view.assert_not_called()

    @patch("accounts.decorators.record_event")
    def test_wrong_role_is_denied_and_audited_for_json(self, record_event):
        request = self.factory.get("/private/", HTTP_ACCEPT="application/json")
        request.user = SimpleNamespace(is_authenticated=True, role=User.Role.STUDENT)
        response = roles_required(User.Role.ADMIN)(self.view)(request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)["error"]["code"], "ACCESS_DENIED")
        record_event.assert_called_once()
        self.view.assert_not_called()

    def test_authorized_role_reaches_view_with_arguments(self):
        request = self.factory.get("/private/")
        request.user = SimpleNamespace(is_authenticated=True, role=User.Role.WARDEN)
        response = roles_required(User.Role.WARDEN)(self.view)(request, pk=5)
        self.assertEqual(response.content, b"allowed")
        self.view.assert_called_once_with(request, pk=5)

    def test_staff_missing_record_is_json_404_or_html_exception(self):
        def missing(request):
            raise Http404

        for accepts_json in (True, False):
            with self.subTest(accepts_json=accepts_json):
                request = self.factory.get(
                    "/private/",
                    HTTP_ACCEPT="application/json" if accepts_json else "text/html",
                )
                request.user = SimpleNamespace(
                    is_authenticated=True, role=User.Role.ADMIN
                )
                if accepts_json:
                    response = staff_required(missing)(request)
                    self.assertEqual(response.status_code, 404)
                    self.assertEqual(
                        json.loads(response.content)["error"]["code"], "NOT_FOUND"
                    )
                else:
                    with self.assertRaises(Http404):
                        staff_required(missing)(request)
