"""Uncovered account presentation and authorization decisions, without a database."""

from inspect import unwrap
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase
from django.urls import reverse

from audit.models import AuditEvent

from .admin import HMSUserAdmin
from .decorators import roles_required
from .models import User
from .views import sign_out, update_user, user_management


class RemainingAccountViewUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.actor = SimpleNamespace(pk=1, is_authenticated=True, role=User.Role.ADMIN)

    def test_logout_requires_post_and_passes_authenticated_request_to_logout(self):
        with patch("accounts.views.logout") as logout:
            request = self.factory.get("/logout/")
            request.user = self.actor
            response = sign_out(request)
            self.assertEqual(response.status_code, 405)
            self.assertEqual(response["Allow"], "POST")
            logout.assert_not_called()

            request = self.factory.post("/logout/")
            request.user = self.actor
            response = sign_out(request)
            self.assertRedirects(
                response, reverse("login"), fetch_redirect_response=False
            )
            logout.assert_called_once_with(request)

    def test_html_role_denial_is_audited_before_returning_forbidden(self):
        view = Mock(__name__="private_view")
        request = self.factory.get("/private/")
        request.user = SimpleNamespace(is_authenticated=True, role=User.Role.STUDENT)
        with patch("accounts.decorators.record_event") as audit:
            response = roles_required(User.Role.ADMIN)(view)(request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b"Access denied")
        view.assert_not_called()
        audit.assert_called_once_with(
            user=request.user,
            action=AuditEvent.Action.ACCESS_DENIED,
            record_type="view",
            record_id="private_view",
        )

    def test_account_list_retains_new_or_invalid_form_and_username_order(self):
        for method in ("get", "post"):
            with (
                self.subTest(method=method),
                patch("accounts.views.AccountCreationForm") as form_type,
                patch(
                    "accounts.views.User.objects.order_by",
                    return_value=["alice", "zoe"],
                ) as users,
                patch("accounts.views.record_event") as audit,
                patch(
                    "accounts.views.render", return_value=HttpResponse("accounts")
                ) as render,
            ):
                form = form_type.return_value
                form.is_valid.return_value = False
                request = getattr(self.factory, method)("/users/", {"username": "bad"})
                request.user = self.actor
                self.assertEqual(unwrap(user_management)(request).content, b"accounts")
                if method == "get":
                    form_type.assert_called_once_with()
                    form.is_valid.assert_not_called()
                else:
                    form_type.assert_called_once_with(request.POST)
                users.assert_called_once_with("username")
                render.assert_called_once_with(
                    request,
                    "accounts/user_management.html",
                    {"form": form, "users": ["alice", "zoe"]},
                )
                form.save.assert_not_called()
                audit.assert_not_called()

    def test_account_update_get_and_invalid_post_keep_the_selected_account(self):
        target = SimpleNamespace(pk=8)
        for method in ("get", "post"):
            with (
                self.subTest(method=method),
                patch(
                    "accounts.views.get_object_or_404", return_value=target
                ) as lookup,
                patch("accounts.views.AccountUpdateForm") as form_type,
                patch("accounts.views.record_event") as audit,
                patch(
                    "accounts.views.render", return_value=HttpResponse("account")
                ) as render,
            ):
                form = form_type.return_value
                form.is_valid.return_value = False
                request = getattr(self.factory, method)(
                    "/users/8/", {"role": "invalid"}
                )
                request.user = self.actor
                self.assertEqual(unwrap(update_user)(request, 8).content, b"account")
                lookup.assert_called_once_with(User, pk=8)
                if method == "get":
                    form_type.assert_called_once_with(instance=target)
                else:
                    form_type.assert_called_once_with(request.POST, instance=target)
                render.assert_called_once_with(
                    request,
                    "accounts/user_update.html",
                    {"form": form, "account": target},
                )
                form.save.assert_not_called()
                audit.assert_not_called()

    def test_admin_password_change_preserves_parent_response_and_form_url(self):
        admin = HMSUserAdmin(User, AdminSite())
        request = self.factory.post("/admin/accounts/user/8/password/")
        response = HttpResponse("password errors", status=400)
        with patch.object(
            UserAdmin, "user_change_password", return_value=response
        ) as parent:
            actual = unwrap(HMSUserAdmin.user_change_password)(
                admin, request, "8", form_url="/admin/password-return/"
            )
        self.assertIs(actual, response)
        parent.assert_called_once_with(request, "8", "/admin/password-return/")
