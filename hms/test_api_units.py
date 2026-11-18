"""Database-free checks for the shared documented API boundaries."""

import json
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse, JsonResponse
from django.test import RequestFactory, SimpleTestCase

from accounts.models import User
from audit.models import AuditEvent

from .api import (
    ErrorResponseMiddleware,
    api_payload,
    api_roles_required,
    validate_api_types,
)


class ApiBoundaryUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def request(self, *, user=None, name="api-example", **headers):
        request = self.factory.get("/api/example/", **headers)
        request.user = user if user is not None else User(pk=8, role=User.Role.ADMIN)
        request.resolver_match = SimpleNamespace(url_name=name)
        return request

    def assert_error(self, response, status, code, message):
        self.assertEqual(response.status_code, status)
        self.assertEqual(
            json.loads(response.content),
            {"error": {"code": code, "message": message}},
        )

    @patch("hms.api.record_event")
    def test_anonymous_and_inactive_users_never_enter_view_or_create_denial_audit(
        self, audit
    ):
        entered = []

        @api_roles_required(User.Role.ADMIN)
        def restricted(request):
            entered.append(request)
            return HttpResponse()

        for user in (
            AnonymousUser(),
            User(pk=9, is_active=False, role=User.Role.ADMIN),
        ):
            with self.subTest(user=user):
                request = self.request(user=user)
                self.assert_error(
                    restricted(request), 401, "AUTH_REQUIRED", "Sign in to continue."
                )
                self.assertFalse(hasattr(request, "_access_denied_audited"))
        self.assertEqual(entered, [])
        audit.assert_not_called()

    @patch("hms.api.record_event")
    def test_wrong_role_is_denied_and_audited_with_view_identity(self, audit):
        entered = []

        @api_roles_required(User.Role.ADMIN, User.Role.WARDEN)
        def staff_only(request):
            entered.append(request)
            return HttpResponse()

        for role in (User.Role.STUDENT, "unexpected-role"):
            with self.subTest(role=role):
                request = self.request(user=User(pk=9, role=role))
                self.assert_error(
                    staff_only(request), 403, "ACCESS_DENIED", "Access denied."
                )
                audit.assert_called_with(
                    user=request.user,
                    action=AuditEvent.Action.ACCESS_DENIED,
                    record_type="view",
                    record_id="staff_only",
                )
                self.assertTrue(request._access_denied_audited)
        self.assertEqual(entered, [])
        self.assertEqual(audit.call_count, 2)

    @patch("hms.api.record_event")
    def test_allowed_roles_forward_positional_and_keyword_arguments(self, audit):
        received = []
        original = JsonResponse({"record": 7})

        @api_roles_required(User.Role.ADMIN, User.Role.WARDEN)
        def detail(request, pk, *, verbose):
            received.append((request.user.role, pk, verbose))
            return original

        for role in (User.Role.ADMIN, User.Role.WARDEN):
            request = self.request(user=User(pk=1, role=role))
            self.assertIs(detail(request, 7, verbose=True), original)
        self.assertEqual(
            received, [(User.Role.ADMIN, 7, True), (User.Role.WARDEN, 7, True)]
        )
        self.assertEqual(detail.__name__, "detail")
        audit.assert_not_called()

    def test_authorized_not_found_becomes_public_json_error(self):
        @api_roles_required(User.Role.ADMIN)
        def missing(request):
            raise Http404("private model lookup")

        self.assert_error(
            missing(self.request()), 404, "NOT_FOUND", "Record not found."
        )

    def test_unexpected_view_exception_is_not_hidden(self):
        @api_roles_required(User.Role.ADMIN)
        def broken(request):
            raise RuntimeError("must reach error handling")

        with self.assertRaisesMessage(RuntimeError, "must reach error handling"):
            broken(self.request())

    def test_payload_accepts_declared_json_scalar_fields_without_coercion(self):
        request = self.factory.post(
            "/api/example/",
            data='{"name":"Asha","year":2,"active":false,"note":null}',
            content_type="application/json",
        )
        self.assertEqual(
            api_payload(request, {"name", "year", "active", "note"}),
            {"name": "Asha", "year": 2, "active": False, "note": None},
        )

    def test_payload_accepts_form_data_and_preserves_multiple_values(self):
        request = self.factory.post("/api/example/", {"tag": ["one", "two"]})
        result = api_payload(request, {"tag"})
        self.assertIs(result, request.POST)
        self.assertEqual(result.getlist("tag"), ["one", "two"])

    def test_payload_rejects_unknown_fields_even_with_false_or_null_values(self):
        for body in (
            '{"is_superuser":false}',
            '{"role":null}',
            '{"safe":1,"extra":""}',
        ):
            with self.subTest(body=body):
                request = self.factory.post(
                    "/api/example/", data=body, content_type="application/json"
                )
                with self.assertRaisesMessage(ValidationError, "unsupported fields"):
                    api_payload(request, {"safe"})

    def test_payload_does_not_turn_malformed_or_nested_json_into_empty_data(self):
        for body in ("{", "[]", '{"safe":{}}'):
            with self.subTest(body=body):
                request = self.factory.post(
                    "/api/example/", data=body, content_type="application/json"
                )
                with self.assertRaisesMessage(
                    ValidationError, "Enter a valid JSON object."
                ):
                    api_payload(request, {"safe"})
        empty = self.factory.post(
            "/api/example/", data="{}", content_type="application/json"
        )
        self.assertEqual(api_payload(empty, set()), {})

    def test_scalar_type_validation_accepts_exact_types_and_absent_optional_fields(
        self,
    ):
        self.assertIsNone(
            validate_api_types(
                {"name": "", "year": 0, "active": False},
                text_fields={"name", "optional"},
                integer_fields={"year"},
                boolean_fields={"active"},
            )
        )
        self.assertIsNone(validate_api_types({}))

    def test_scalar_type_validation_reports_all_fields_and_rejects_python_coercions(
        self,
    ):
        with self.assertRaises(ValidationError) as caught:
            validate_api_types(
                {"name": 12, "year": True, "active": 1},
                text_fields={"name"},
                integer_fields={"year"},
                boolean_fields={"active"},
            )
        self.assertEqual(
            caught.exception.message_dict,
            {
                "name": ["Enter a text value."],
                "year": ["Enter a whole number."],
                "active": ["Enter true or false."],
            },
        )
        for value in (None, "2", 2.0):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                validate_api_types({"year": value}, integer_fields={"year"})


class ApiMiddlewareUnitTests(SimpleTestCase):
    def request(self, name="api-example", **headers):
        request = RequestFactory().get("/api/example/", **headers)
        request.resolver_match = SimpleNamespace(url_name=name)
        return request

    @patch("hms.api.record_event")
    def test_error_status_mapping_hides_internal_html_and_keeps_status(self, audit):
        contracts = {
            400: ("VALIDATION_ERROR", "Enter a valid request."),
            401: ("AUTH_REQUIRED", "Sign in to continue."),
            403: ("ACCESS_DENIED", "Access denied."),
            404: ("NOT_FOUND", "Record not found."),
            405: ("METHOD_NOT_ALLOWED", "This request method is not allowed."),
            500: ("SERVER_ERROR", "The request could not be completed."),
            502: ("SERVER_ERROR", "The request could not be completed."),
        }
        for status, (code, message) in contracts.items():
            with self.subTest(status=status):
                response = HttpResponse("private internal detail", status=status)
                result = ErrorResponseMiddleware(
                    lambda request, response=response: response
                )(self.request())
                self.assertEqual(result.status_code, status)
                self.assertEqual(
                    json.loads(result.content),
                    {"error": {"code": code, "message": message}},
                )
        audit.assert_called_once_with(
            user=None,
            action=AuditEvent.Action.ACCESS_DENIED,
            record_type="view",
            record_id="api-example",
        )

    def test_json_accept_header_converts_error_without_api_route_name(self):
        original = HttpResponse("not found", status=404)
        request = self.request(
            "student-list", HTTP_ACCEPT="text/html, application/json"
        )
        result = ErrorResponseMiddleware(lambda request: original)(request)
        self.assertEqual(json.loads(result.content)["error"]["code"], "NOT_FOUND")

    def test_json_content_type_converts_error_without_api_route_name(self):
        original = HttpResponse("not found", status=404)
        request = RequestFactory().post(
            "/students/", data="{}", content_type="application/json"
        )
        result = ErrorResponseMiddleware(lambda request: original)(request)
        self.assertEqual(json.loads(result.content)["error"]["code"], "NOT_FOUND")

    @patch("hms.api.record_event")
    def test_existing_json_denial_is_preserved_and_audited_only_once(self, audit):
        original = JsonResponse({"error": {"code": "BUSINESS_DENIAL"}}, status=403)
        request = self.request()
        request.user = User(pk=3, role=User.Role.STUDENT)
        middleware = ErrorResponseMiddleware(lambda request: original)
        self.assertIs(middleware(request), original)
        self.assertIs(middleware(request), original)
        audit.assert_called_once_with(
            user=request.user,
            action=AuditEvent.Action.ACCESS_DENIED,
            record_type="view",
            record_id="api-example",
        )
        self.assertTrue(request._access_denied_audited)

    @patch("hms.api.record_event")
    def test_missing_empty_and_overlong_route_names_have_bounded_audit_identity(
        self, audit
    ):
        for name, expected in (
            (None, "unresolved"),
            ("", "unresolved"),
            ("x" * 90, "x" * 64),
        ):
            with self.subTest(name=name):
                request = self.request(name)
                ErrorResponseMiddleware(lambda request: HttpResponse(status=403))(
                    request
                )
                self.assertEqual(audit.call_args.kwargs["record_id"], expected)
        request = RequestFactory().get("/unknown/")
        ErrorResponseMiddleware(lambda request: HttpResponse(status=403))(request)
        self.assertEqual(audit.call_args.kwargs["record_id"], "unresolved")

    @patch("hms.api.record_event")
    def test_decorator_denial_is_not_audited_again_by_middleware(self, audit):
        @api_roles_required(User.Role.ADMIN)
        def restricted(request):
            self.fail("A student must not enter the protected view")

        request = self.request()
        request.user = User(pk=3, role=User.Role.STUDENT)
        result = ErrorResponseMiddleware(restricted)(request)
        self.assertEqual(result.status_code, 403)
        self.assertEqual(audit.call_count, 1)
        self.assertEqual(audit.call_args.kwargs["record_id"], "restricted")

    def test_replacement_preserves_response_metadata_but_recomputes_body_headers(self):
        original = HttpResponse(
            "private details", status=405, content_type="text/plain"
        )
        original.headers["Content-Length"] = "15"
        original.headers["Allow"] = "PATCH"
        original.headers["Cache-Control"] = "private, no-store"
        original.headers["Vary"] = "Cookie"
        original.set_cookie("sessionid", "changed", httponly=True, samesite="Lax")
        result = ErrorResponseMiddleware(lambda request: original)(self.request())
        self.assertEqual(result.headers["Content-Type"], "application/json")
        self.assertNotIn("Content-Length", result.headers)
        for header in ("Allow", "Cache-Control", "Vary"):
            self.assertEqual(result.headers[header], original.headers[header])
        self.assertEqual(result.cookies.output(), original.cookies.output())

    def test_success_redirect_json_and_regular_html_errors_keep_response_identity(self):
        for status, name, content_type in (
            (200, "api-example", "text/html"),
            (302, "api-example", "text/html"),
            (404, "api-example", "application/json; charset=utf-8"),
            (404, "student-list", "text/html"),
        ):
            with self.subTest(status=status, name=name, content_type=content_type):
                original = HttpResponse(
                    "existing response", status=status, content_type=content_type
                )
                result = ErrorResponseMiddleware(
                    lambda request, original=original: original
                )(self.request(name))
                self.assertIs(result, original)
