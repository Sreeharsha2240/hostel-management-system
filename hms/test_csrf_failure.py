"""CSRF failures retain enforcement, audit and the correct response format."""

from types import SimpleNamespace
from unittest.mock import patch

from django.http import HttpResponseForbidden
from django.test import RequestFactory, SimpleTestCase

from audit.models import AuditEvent

from .csrf import csrf_failure


class CsrfFailureTests(SimpleTestCase):
    @patch("hms.csrf.record_event")
    def test_json_failure_is_generic_and_audits_route_only(self, audit):
        request = RequestFactory().post(
            "/auth/login/", {}, content_type="application/json"
        )
        request.resolver_match = SimpleNamespace(url_name="api-login")
        response = csrf_failure(request, reason="private token detail")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertNotIn(b"private token detail", response.content)
        audit.assert_called_once_with(
            user=None,
            action=AuditEvent.Action.ACCESS_DENIED,
            record_type="csrf",
            record_id="api-login",
        )

    @patch("hms.csrf.record_event")
    @patch(
        "hms.csrf.html_csrf_failure", return_value=HttpResponseForbidden("HTML failure")
    )
    def test_html_failure_preserves_django_page_and_is_also_audited(self, html, audit):
        request = RequestFactory().post("/login/", {"password": "private password"})
        request.resolver_match = SimpleNamespace(url_name="login")
        response = csrf_failure(request, reason="missing cookie")
        self.assertEqual(response.content, b"HTML failure")
        html.assert_called_once_with(request, reason="missing cookie")
        self.assertEqual(audit.call_args.kwargs["record_id"], "login")
