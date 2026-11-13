"""Private response caching contracts, including login and logout transitions."""

from types import SimpleNamespace
from unittest.mock import Mock

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase
from django.utils.cache import get_max_age

from .middleware import PrivatePageMiddleware


class PrivatePageMiddlewareUnitTests(SimpleTestCase):
    def request(self, authenticated):
        request = RequestFactory().get("/private/")
        request.user = SimpleNamespace(is_authenticated=authenticated)
        return request

    def assert_private(self, response):
        directives = {
            directive.strip() for directive in response["Cache-Control"].split(",")
        }
        self.assertTrue(
            {"no-cache", "no-store", "must-revalidate", "private"} <= directives
        )
        self.assertNotIn("public", directives)
        self.assertEqual(get_max_age(response), 0)
        self.assertIn("Expires", response)

    def test_anonymous_public_response_keeps_existing_cache_headers(self):
        request = self.request(False)
        response = HttpResponse("public")
        response["Cache-Control"] = "public, max-age=3600"
        response["Expires"] = "Wed, 21 Oct 2037 07:28:00 GMT"
        headers = dict(response.headers)
        get_response = Mock(return_value=response)

        result = PrivatePageMiddleware(get_response)(request)

        self.assertIs(result, response)
        self.assertEqual(dict(result.headers), headers)
        get_response.assert_called_once_with(request)

    def test_anonymous_response_without_cache_headers_remains_unchanged(self):
        response = HttpResponse("public")

        result = PrivatePageMiddleware(Mock(return_value=response))(self.request(False))

        self.assertIs(result, response)
        self.assertNotIn("Cache-Control", result)
        self.assertNotIn("Expires", result)

    def test_authenticated_response_disables_caching_and_keeps_body_and_status(self):
        request = self.request(True)
        response = HttpResponse("private details", status=403)
        get_response = Mock(return_value=response)

        result = PrivatePageMiddleware(get_response)(request)

        self.assertIs(result, response)
        self.assert_private(result)
        self.assertEqual(result.content, b"private details")
        self.assertEqual(result.status_code, 403)
        get_response.assert_called_once_with(request)

    def test_login_response_becomes_private_when_view_authenticates_user(self):
        request = self.request(False)
        response = HttpResponse(status=302)
        response["Location"] = "/dashboard/"

        def login(received):
            self.assertIs(received, request)
            received.user = SimpleNamespace(is_authenticated=True)
            return response

        result = PrivatePageMiddleware(login)(request)

        self.assert_private(result)
        self.assertEqual(result["Location"], "/dashboard/")

    def test_logout_response_remains_private_after_view_clears_user(self):
        request = self.request(True)
        response = HttpResponse(status=302)
        response["Location"] = "/login/"

        def logout(received):
            self.assertIs(received, request)
            received.user = SimpleNamespace(is_authenticated=False)
            return response

        result = PrivatePageMiddleware(logout)(request)

        self.assert_private(result)
        self.assertEqual(result["Location"], "/login/")

    def test_private_response_overrides_public_cache_policy_and_preserves_vary(self):
        response = HttpResponse("private")
        response["Cache-Control"] = "public, max-age=3600, stale-while-revalidate=60"
        response["Vary"] = "Accept-Language, Cookie"

        result = PrivatePageMiddleware(Mock(return_value=response))(self.request(True))

        self.assert_private(result)
        self.assertIn("stale-while-revalidate=60", result["Cache-Control"])
        self.assertEqual(result["Vary"], "Accept-Language, Cookie")
