"""Keep shared validation errors consistent with the documented JSON API."""

import json

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from .responses import validation_response


class ValidationResponseTests(SimpleTestCase):
    def assert_error_response(self, error, *, status, code, message):
        response = validation_response(error)

        self.assertEqual(response.status_code, status)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(
            json.loads(response.content),
            {"error": {"code": code, "message": message}},
        )

    def test_missing_record_returns_404_with_code_and_message(self):
        self.assert_error_response(
            ValidationError(
                "Record %(id)s was not found.", code="NOT_FOUND", params={"id": 41}
            ),
            status=404,
            code="NOT_FOUND",
            message="Record 41 was not found.",
        )

    def test_all_conflict_errors_return_409(self):
        for code in (
            "BED_OCCUPIED",
            "ALREADY_ALLOCATED",
            "ALREADY_RELEASED",
            "HAS_ACTIVE_ALLOCATION",
        ):
            with self.subTest(code=code):
                self.assert_error_response(
                    ValidationError(
                        "The allocation conflicts with current records.", code=code
                    ),
                    status=409,
                    code=code,
                    message="The allocation conflicts with current records.",
                )

    def test_all_domain_validation_errors_return_422(self):
        for code in (
            "GENDER_MISMATCH",
            "IMMUTABLE_FIELD",
            "INACTIVE_STUDENT",
            "INACTIVE_HOSTEL",
        ):
            with self.subTest(code=code):
                self.assert_error_response(
                    ValidationError("This change is not allowed.", code=code),
                    status=422,
                    code=code,
                    message="This change is not allowed.",
                )

    def test_unknown_and_uncoded_errors_return_400_and_preserve_messages(self):
        cases = (
            (
                ValidationError("An unfamiliar validation failed.", code="NEW_ERROR"),
                "NEW_ERROR",
                "An unfamiliar validation failed.",
            ),
            (
                ValidationError(["First issue.", "Second issue."]),
                "VALIDATION_ERROR",
                "First issue.; Second issue.",
            ),
        )
        for error, code, message in cases:
            with self.subTest(code=code):
                self.assert_error_response(
                    error, status=400, code=code, message=message
                )
