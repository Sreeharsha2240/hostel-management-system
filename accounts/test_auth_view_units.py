"""Unit checks for sign-in and role-dashboard decisions."""

from types import SimpleNamespace
from unittest.mock import patch

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from .models import User
from .views import dashboard, sign_in


class SignInViewUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch("accounts.views.redirect", return_value=HttpResponse("dashboard"))
    @patch("accounts.views.authenticate")
    def test_signed_in_user_is_redirected_without_authentication(
        self, authenticate, redirect
    ):
        request = self.factory.get("/login/")
        request.user = SimpleNamespace(is_authenticated=True)
        self.assertEqual(sign_in(request).content, b"dashboard")
        redirect.assert_called_once_with("dashboard")
        authenticate.assert_not_called()

    @patch("accounts.views.render", return_value=HttpResponse("login page"))
    @patch("accounts.views.authenticate", return_value=None)
    def test_invalid_login_uses_generic_error_and_strips_username(
        self, authenticate, render
    ):
        request = self.factory.post(
            "/login/", {"username": "  warden  ", "password": "bad"}
        )
        request.user = SimpleNamespace(is_authenticated=False)
        self.assertEqual(sign_in(request).content, b"login page")
        authenticate.assert_called_once_with(request, username="warden", password="bad")
        self.assertEqual(
            render.call_args.args[2], {"error": "Invalid username or password"}
        )

    @patch("accounts.views.redirect", return_value=HttpResponse("dashboard"))
    @patch("accounts.views.login")
    @patch("accounts.views.authenticate")
    def test_successful_login_starts_session_and_redirects(
        self, authenticate, login, redirect
    ):
        user = SimpleNamespace(username="warden")
        authenticate.return_value = user
        request = self.factory.post(
            "/login/", {"username": "warden", "password": "valid"}
        )
        request.user = SimpleNamespace(is_authenticated=False)
        self.assertEqual(sign_in(request).content, b"dashboard")
        login.assert_called_once_with(request, user)
        redirect.assert_called_once_with("dashboard")

    @patch("accounts.views.render", return_value=HttpResponse("login page"))
    def test_get_login_page_has_no_error(self, render):
        request = self.factory.get("/login/")
        request.user = SimpleNamespace(is_authenticated=False)
        self.assertEqual(sign_in(request).content, b"login page")
        self.assertEqual(render.call_args.args[2], {"error": None})


class DashboardUnitTests(SimpleTestCase):
    @patch("accounts.views.render", return_value=HttpResponse("dashboard"))
    def test_staff_dashboard_uses_the_matching_template(self, render):
        for role, template in (
            (User.Role.ADMIN, "accounts/dashboard_admin.html"),
            (User.Role.WARDEN, "accounts/dashboard_warden.html"),
        ):
            with self.subTest(role=role):
                request = RequestFactory().get("/dashboard/")
                request.user = SimpleNamespace(is_authenticated=True, role=role)
                self.assertEqual(dashboard(request).content, b"dashboard")
                self.assertEqual(render.call_args.args[1], template)
                self.assertEqual(render.call_args.args[2], {})

    @patch("accounts.views.render", return_value=HttpResponse("dashboard"))
    @patch("accounts.views.Bed.objects.filter")
    def test_student_dashboard_counts_only_active_hostel_available_beds(
        self, beds, render
    ):
        beds.return_value.count.return_value = 4
        request = RequestFactory().get("/dashboard/")
        request.user = SimpleNamespace(is_authenticated=True, role=User.Role.STUDENT)
        self.assertEqual(dashboard(request).content, b"dashboard")
        self.assertEqual(render.call_args.args[1], "accounts/dashboard_student.html")
        self.assertEqual(render.call_args.args[2]["available_bed_count"], 4)
        beds.assert_called_once_with(status="Available", room__hostel__is_active=True)
