"""Framework API errors preserve headers/cookies and denial audit semantics."""

import json
from types import SimpleNamespace
from unittest.mock import patch

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.test import RequestFactory, SimpleTestCase

from .api import ErrorResponseMiddleware


class ApiErrorResponseTests(SimpleTestCase):
    def request(self, name="api-login"):
        request = RequestFactory().get("/auth/login/")
        request.resolver_match = SimpleNamespace(url_name=name)
        return request

    def test_method_error_is_json_and_keeps_security_and_session_headers(self):
        response = HttpResponseNotAllowed(["POST"])
        response.headers["Cache-Control"] = "private, no-store"
        response.headers["Vary"] = "Cookie"
        response.set_cookie("synthetic", "retained")
        result = ErrorResponseMiddleware(lambda request: response)(self.request())
        self.assertEqual(result.status_code, 405)
        self.assertEqual(
            json.loads(result.content)["error"]["code"], "METHOD_NOT_ALLOWED"
        )
        self.assertEqual(result.headers["Allow"], "POST")
        self.assertEqual(result.headers["Cache-Control"], "private, no-store")
        self.assertEqual(result.headers["Vary"], "Cookie")
        self.assertEqual(result.cookies["synthetic"].value, "retained")

    @patch("hms.api.record_event")
    def test_served_unaudited_denial_gets_one_route_only_event(self, audit):
        request = self.request("student-list")
        response = ErrorResponseMiddleware(
            lambda request: HttpResponseForbidden("HTML denial")
        )(request)
        self.assertEqual(response.content, b"HTML denial")
        self.assertEqual(audit.call_args.kwargs["record_id"], "student-list")
        self.assertTrue(request._access_denied_audited)
        audit.assert_called_once()

    @patch("hms.api.record_event")
    def test_decorator_audited_denial_is_not_duplicated(self, audit):
        request = self.request()
        request._access_denied_audited = True
        response = ErrorResponseMiddleware(
            lambda request: HttpResponseForbidden("private reason")
        )(request)
        self.assertEqual(response.status_code, 403)
        self.assertNotIn(b"private reason", response.content)
        audit.assert_not_called()

    def test_regular_html_errors_and_successes_keep_their_original_response(self):
        for status in (200, 302, 404, 405):
            original = HttpResponse("HTML", status=status)
            self.assertIs(
                ErrorResponseMiddleware(lambda request, original=original: original)(
                    self.request("login")
                ),
                original,
            )
