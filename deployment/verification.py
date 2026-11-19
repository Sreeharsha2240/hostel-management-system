"""Production checks with no listener, credentials, or database access.

Run using Django's test runner with --settings=deployment.settings and explicit
dummy credential environment values. SimpleTestCase forbids database queries.
"""

import gzip
import json
import os
import runpy
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.handlers.wsgi import WSGIHandler
from django.core.management import call_command
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.test import Client, RequestFactory, SimpleTestCase, override_settings
from django.urls import path
from waitress.proxy_headers import proxy_headers_middleware


def _probe(request):
    get_token(request)
    return JsonResponse({"secure": request.is_secure(), "host": request.get_host()})


urlpatterns = [path("deployment-probe/", _probe)]

_DUMMY_ENV = {
    "DJANGO_SECRET_KEY": "production-test-only-0123456789-ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "DB_NAME": "unused_production_test_database",
    "DB_USER": "unused_production_test_user",
    "DB_PASSWORD": "unused_production_test_password",
    "DB_HOST": "127.0.0.1",
    "DB_PORT": "3306",
}


def _load_production(environment):
    # Reimport the inherited settings too, so tests exercise stale development
    # environment flags rather than reuse whichever module the runner loaded.
    with patch.dict(os.environ, environment, clear=True), patch.dict(sys.modules):
        sys.modules.pop("hms.settings", None)
        # Disabled dotenv must return before constructing/reading a .env file.
        with patch("dotenv.main.DotEnv", side_effect=AssertionError("Read .env")):
            return runpy.run_path(str(Path(__file__).with_name("settings.py")))


class ProductionConfigurationTests(SimpleTestCase):
    def test_development_environment_cannot_weaken_production(self):
        configured = _load_production(
            {
                **_DUMMY_ENV,
                "DJANGO_DEBUG": "True",
                "DJANGO_ALLOWED_HOSTS": "*,localhost,evil.example",
                "DJANGO_SESSION_COOKIE_SECURE": "False",
                "DJANGO_CSRF_COOKIE_SECURE": "False",
                "DJANGO_SECURE_SSL_REDIRECT": "False",
                "DJANGO_SECURE_HSTS_SECONDS": "0",
                "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS": "False",
                "DJANGO_SECURE_HSTS_PRELOAD": "False",
            }
        )
        self.assertFalse(configured["DEBUG"])
        self.assertEqual(configured["ALLOWED_HOSTS"], ["se.d3va.dev"])
        self.assertEqual(configured["CSRF_TRUSTED_ORIGINS"], [])
        for name in (
            "SESSION_COOKIE_SECURE",
            "SESSION_COOKIE_HTTPONLY",
            "CSRF_COOKIE_SECURE",
            "CSRF_COOKIE_HTTPONLY",
            "SECURE_SSL_REDIRECT",
            "SECURE_HSTS_INCLUDE_SUBDOMAINS",
            "SECURE_HSTS_PRELOAD",
            "SECURE_CONTENT_TYPE_NOSNIFF",
        ):
            self.assertIs(configured[name], True, name)
        self.assertEqual(configured["SECURE_HSTS_SECONDS"], 31536000)
        self.assertIsNone(configured["SECURE_PROXY_SSL_HEADER"])
        self.assertFalse(configured["USE_X_FORWARDED_HOST"])
        self.assertFalse(configured["USE_X_FORWARDED_PORT"])

    def test_every_credential_must_be_explicit_and_nonempty(self):
        for name in _DUMMY_ENV:
            for value in (None, "", "   "):
                with self.subTest(name=name, value=value):
                    environment = dict(_DUMMY_ENV)
                    if value is None:
                        environment.pop(name)
                    else:
                        environment[name] = value
                    with self.assertRaisesMessage(ImproperlyConfigured, name):
                        _load_production(environment)

    def test_weak_or_development_secret_is_rejected(self):
        for secret in ("short", "a" * 64, "django-insecure-" + "abcd1234" * 8):
            with self.subTest(secret_kind=secret[:6]):
                with self.assertRaisesMessage(ImproperlyConfigured, "strong"):
                    _load_production({**_DUMMY_ENV, "DJANGO_SECRET_KEY": secret})


@override_settings(ROOT_URLCONF=__name__)
class ProductionRequestTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._static_directory = TemporaryDirectory(prefix="hms-production-static-")
        cls.addClassCleanup(cls._static_directory.cleanup)
        cls._static_settings = override_settings(STATIC_ROOT=cls._static_directory.name)
        cls._static_settings.enable()
        cls.addClassCleanup(cls._static_settings.disable)
        call_command("collectstatic", interactive=False, verbosity=0)

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True, HTTP_HOST="se.d3va.dev")
        # Keep the real failure view and middleware while stubbing only the
        # audit persistence sink. SimpleTestCase forbids every database query.
        self.enterContext(patch("hms.csrf.record_event"))

    def test_suite_runs_against_production_middleware(self):
        # Django's runner appends its own "testserver" host to this setting.
        self.assertIn("se.d3va.dev", settings.ALLOWED_HOSTS)
        self.assertNotIn("*", settings.ALLOWED_HOSTS)
        self.assertFalse(settings.DEBUG)
        self.assertEqual(
            settings.MIDDLEWARE[:2],
            [
                "django.middleware.security.SecurityMiddleware",
                "whitenoise.middleware.WhiteNoiseMiddleware",
            ],
        )
        self.assertIn("django.middleware.csrf.CsrfViewMiddleware", settings.MIDDLEWARE)

    def test_raw_forwarded_proto_cannot_bypass_http_redirect(self):
        response = self.client.get(
            "/deployment-probe/?from=http", HTTP_X_FORWARDED_PROTO="https"
        )
        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response["Location"], "https://se.d3va.dev/deployment-probe/?from=http"
        )

    def test_exact_public_host_and_forwarded_host_boundary(self):
        response = self.client.get(
            "/deployment-probe/", secure=True, HTTP_X_FORWARDED_HOST="evil.example"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["host"], "se.d3va.dev")
        for host in ("evil.example", "sub.se.d3va.dev", "localhost", "127.0.0.1"):
            with self.subTest(host=host):
                response = self.client.get(
                    "/deployment-probe/", secure=True, HTTP_HOST=host
                )
                self.assertEqual(response.status_code, 400)

    def test_https_response_has_security_headers_and_secure_csrf_cookie(self):
        response = self.client.get("/deployment-probe/", secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Strict-Transport-Security"],
            "max-age=31536000; includeSubDomains; preload",
        )
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response["X-Frame-Options"], "DENY")
        self.assertEqual(response["Referrer-Policy"], "same-origin")
        self.assertEqual(response["Cross-Origin-Opener-Policy"], "same-origin")
        self.assertIn("form-action 'self'", response["Content-Security-Policy"])
        cookie = response.cookies[settings.CSRF_COOKIE_NAME]
        self.assertTrue(cookie["secure"])
        self.assertTrue(cookie["httponly"])
        self.assertEqual(cookie["samesite"], "Lax")
        self.assertEqual(cookie["domain"], "")

    def test_csrf_requires_token_and_same_https_origin(self):
        response = self.client.post(
            "/deployment-probe/", secure=True, HTTP_ORIGIN="https://se.d3va.dev"
        )
        self.assertEqual(response.status_code, 403)
        self.client.get("/deployment-probe/", secure=True)
        token = self.client.cookies[settings.CSRF_COOKIE_NAME].value
        for origin in (
            "https://evil.example",
            "https://sub.se.d3va.dev",
            "http://se.d3va.dev",
        ):
            with self.subTest(origin=origin):
                response = self.client.post(
                    "/deployment-probe/",
                    {"csrfmiddlewaretoken": token},
                    secure=True,
                    HTTP_ORIGIN=origin,
                )
                self.assertEqual(response.status_code, 403)
        response = self.client.post(
            "/deployment-probe/",
            {"csrfmiddlewaretoken": token},
            secure=True,
            HTTP_ORIGIN="https://se.d3va.dev",
        )
        self.assertEqual(response.status_code, 200)

    def test_collected_assets_are_hashed_gzipped_and_secure(self):
        static_root = Path(settings.STATIC_ROOT)
        manifest = json.loads((static_root / "staticfiles.json").read_text())
        hashed_name = manifest["paths"]["hms/styles.css"]
        self.assertNotEqual(hashed_name, "hms/styles.css")
        self.assertTrue((static_root / (hashed_name + ".gz")).is_file())
        response = self.client.get(
            "/static/" + hashed_name,
            secure=True,
            HTTP_ACCEPT_ENCODING="gzip",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Encoding"], "gzip")
        self.assertIn("immutable", response["Cache-Control"])
        self.assertIn("Accept-Encoding", response["Vary"])
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")
        self.assertIn("max-age=31536000", response["Strict-Transport-Security"])
        self.assertNotIn("Access-Control-Allow-Origin", response)
        try:
            content = b"".join(response.streaming_content)
        finally:
            response.close()
        self.assertEqual(
            gzip.decompress(content), (static_root / hashed_name).read_bytes()
        )
        redirect = self.client.get("/static/" + hashed_name)
        self.assertEqual(redirect.status_code, 301)
        self.assertEqual(
            redirect["Location"], "https://se.d3va.dev/static/" + hashed_name
        )

    def _through_waitress(self, peer, **headers):
        application = proxy_headers_middleware(
            WSGIHandler(),
            trusted_proxy="127.0.0.1",
            trusted_proxy_count=1,
            trusted_proxy_headers={"x-forwarded-proto"},
            clear_untrusted=True,
        )
        request = RequestFactory().get(
            "/deployment-probe/", HTTP_HOST="se.d3va.dev", **headers
        )
        environ = request.environ
        environ["REMOTE_ADDR"] = peer
        captured = {}

        def start_response(status, response_headers, exc_info=None):
            captured.update(
                status=int(status.split()[0]), headers=dict(response_headers)
            )

        result = application(environ, start_response)
        try:
            captured["body"] = b"".join(result)
        finally:
            if hasattr(result, "close"):
                result.close()
        captured["environ"] = environ
        return captured

    def test_only_trusted_loopback_proxy_normalizes_https_scheme(self):
        response = self._through_waitress(
            "127.0.0.1",
            HTTP_X_FORWARDED_PROTO="https",
            HTTP_X_FORWARDED_HOST="evil.example",
            HTTP_X_FORWARDED_FOR="198.51.100.7",
            HTTP_FORWARDED='host="evil.example";proto=http',
        )
        self.assertEqual(response["status"], 200)
        self.assertEqual(
            json.loads(response["body"]), {"secure": True, "host": "se.d3va.dev"}
        )
        self.assertIn("Strict-Transport-Security", response["headers"])
        for name in ("HTTP_X_FORWARDED_HOST", "HTTP_X_FORWARDED_FOR", "HTTP_FORWARDED"):
            self.assertNotIn(name, response["environ"])

    def test_untrusted_proxy_spoof_is_stripped_and_redirected(self):
        response = self._through_waitress(
            "198.51.100.7", HTTP_X_FORWARDED_PROTO="https"
        )
        self.assertEqual(response["status"], 301)
        self.assertEqual(response["environ"]["wsgi.url_scheme"], "http")
        self.assertNotIn("HTTP_X_FORWARDED_PROTO", response["environ"])
        self.assertEqual(
            response["headers"]["Location"], "https://se.d3va.dev/deployment-probe/"
        )

    def test_ambiguous_proxy_scheme_is_rejected(self):
        response = self._through_waitress(
            "127.0.0.1", HTTP_X_FORWARDED_PROTO="https, http"
        )
        self.assertEqual(response["status"], 400)
