"""SAD authentication/account JSON contracts and authorization boundaries."""

from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from audit.models import AuditEvent

from .forms import AccountCreationForm
from .models import User


class AccountApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(
            username="api-admin", password="Validpass123"
        )
        cls.warden = User.objects.create_user(
            username="api-warden",
            password="Validpass123",
            role=User.Role.WARDEN,
            is_staff=True,
        )
        cls.student = User.objects.create_user(
            username="api-student", password="Validpass123", role=User.Role.STUDENT
        )

    def post(self, route, data, **kwargs):
        return self.client.post(
            reverse(route), data, content_type="application/json", **kwargs
        )

    def patch_user(self, data, pk=None):
        return self.client.patch(
            reverse("api-user-update", args=[pk or self.warden.pk]),
            data,
            content_type="application/json",
        )

    def test_login_logout_start_and_end_session_and_write_audit(self):
        response = self.post(
            "api-login", {"username": "api-warden", "password": "Validpass123"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"role": "warden", "redirect": "/dashboard/"})
        self.assertEqual(self.client.session["_auth_user_id"], str(self.warden.pk))
        response = self.post("api-logout", {})
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(
            list(
                AuditEvent.objects.filter(user=self.warden)
                .order_by("pk")
                .values_list("action", flat=True)
            ),
            ["login", "logout"],
        )

    def test_wrong_or_unknown_credentials_return_same_generic_json(self):
        responses = [
            self.post("api-login", {"username": username, "password": "incorrect"})
            for username in (self.warden.username, "unknown-api-user")
        ]
        for response in responses:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(
                response.json()["error"],
                {
                    "code": "INVALID_CREDENTIALS",
                    "message": "Invalid username or password",
                },
            )
        self.assertEqual(AuditEvent.objects.filter(action="login_failed").count(), 2)

    def test_fifth_failure_and_correct_password_during_lock_return_423(self):
        for index in range(5):
            response = self.post(
                "api-login", {"username": self.warden.username, "password": "incorrect"}
            )
            self.assertEqual(response.status_code, 423 if index == 4 else 401)
        response = self.post(
            "api-login", {"username": self.warden.username, "password": "Validpass123"}
        )
        self.assertEqual(response.status_code, 423)
        self.assertEqual(response.json()["error"]["code"], "ACCOUNT_LOCKED")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_rejects_missing_structured_unknown_and_non_text_fields(self):
        for data in (
            {},
            {"username": True, "password": "valid"},
            {"username": "api-warden", "password": 123},
            {"username": "api-warden", "password": "valid", "is_superuser": True},
            {"username": ["api-warden"], "password": "valid"},
        ):
            with self.subTest(data=data):
                self.assertEqual(self.post("api-login", data).status_code, 400)

    def test_logout_requires_authentication_even_without_accept_header(self):
        response = self.client.post(reverse("api-logout"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"]["code"], "AUTH_REQUIRED")

    def test_account_create_and_patch_require_admin_role(self):
        for actor, status in ((None, 401), (self.warden, 403), (self.student, 403)):
            with self.subTest(actor=actor):
                if actor is not None:
                    self.client.force_login(actor)
                self.assertEqual(
                    self.post(
                        "api-user-create",
                        {
                            "username": "forbidden-user",
                            "password": "Validpass123",
                            "role": "admin",
                        },
                    ).status_code,
                    status,
                )
                self.assertEqual(self.patch_user({"role": "admin"}).status_code, status)
        self.assertFalse(User.objects.filter(username="forbidden-user").exists())

    def test_admin_creates_hashed_password_and_audited_account(self):
        self.client.force_login(self.admin)
        response = self.post(
            "api-user-create",
            {
                "username": "created-api-user",
                "password": "Differentpass456",
                "role": "warden",
            },
        )
        self.assertEqual(response.status_code, 201)
        account = User.objects.get(pk=response.json()["id"])
        self.assertTrue(account.check_password("Differentpass456"))
        self.assertNotIn("password", response.json())
        self.assertTrue(
            AuditEvent.objects.filter(
                user=self.admin,
                action="create",
                record_id=str(account.pk),
                record_type="accounts.user",
            ).exists()
        )

    def test_create_rejects_duplicates_weak_passwords_and_mass_assignment(self):
        self.client.force_login(self.admin)
        base = {
            "username": "new-api-user",
            "password": "Differentpass456",
            "role": "warden",
        }
        for changes, status in (
            ({"username": self.warden.username}, 409),
            ({"password": "abc"}, 400),
            ({"role": True}, 400),
            ({"is_staff": True}, 400),
            ({"is_superuser": True}, 400),
            ({"role": "unknown"}, 400),
        ):
            with self.subTest(changes=changes):
                response = self.post("api-user-create", base | changes)
                self.assertEqual(response.status_code, status)
        self.assertFalse(User.objects.filter(username="new-api-user").exists())

    def test_patch_role_and_activation_is_partial_and_audited(self):
        self.client.force_login(self.admin)
        response = self.patch_user({"role": "student", "is_active": False})
        self.assertEqual(response.status_code, 200)
        self.warden.refresh_from_db()
        self.assertFalse(self.warden.is_active)
        self.assertFalse(self.warden.is_staff)
        self.assertEqual(self.warden.role, User.Role.STUDENT)
        self.assertTrue(self.warden.check_password("Validpass123"))
        self.assertTrue(
            AuditEvent.objects.filter(
                user=self.admin, action="deactivate", record_id=str(self.warden.pk)
            ).exists()
        )

    def test_patch_rejects_ambiguous_types_unknown_fields_and_self_deactivation(self):
        self.client.force_login(self.admin)
        for data in (
            {},
            {"is_active": "false"},
            {"is_active": 0},
            {"is_active": None},
            {"role": False},
            {"username": "changed"},
            {"is_staff": True},
        ):
            with self.subTest(data=data):
                self.assertEqual(self.patch_user(data).status_code, 400)
        self.assertEqual(
            self.patch_user({"is_active": False}, self.admin.pk).status_code, 403
        )
        self.assertEqual(
            self.patch_user({"role": "student"}, self.admin.pk).status_code, 400
        )
        self.assertEqual(self.patch_user({"is_active": False}, 999999).status_code, 404)
        self.warden.refresh_from_db()
        self.assertTrue(self.warden.is_active)

    def test_api_audit_failure_rolls_back_account_and_role_changes(self):
        self.client.force_login(self.admin)
        with patch(
            "accounts.api.record_event", side_effect=RuntimeError("audit unavailable")
        ):
            with self.assertRaises(RuntimeError):
                self.post(
                    "api-user-create",
                    {
                        "username": "api-must-rollback",
                        "password": "Differentpass456",
                        "role": "warden",
                    },
                )
            with self.assertRaises(RuntimeError):
                self.patch_user({"role": "student"})
        self.assertFalse(User.objects.filter(username="api-must-rollback").exists())
        self.warden.refresh_from_db()
        self.assertEqual(self.warden.role, User.Role.WARDEN)

    def test_duplicate_race_returns_json_conflict_and_bound_html_error(self):
        self.client.force_login(self.admin)
        for module, route, expected_status in (
            ("accounts.api", "api-user-create", 409),
            ("accounts.views", "user-management", 200),
        ):
            with self.subTest(module=module):
                username = "api-race" if module.endswith("api") else "html-race"
                payload = {
                    "username": username,
                    "password": "Differentpass456",
                    "role": "warden",
                }
                form = AccountCreationForm(payload)
                self.assertTrue(form.is_valid(), form.errors)
                User.objects.create_user(username=username, role=User.Role.STUDENT)
                with patch(f"{module}.AccountCreationForm", return_value=form):
                    response = (
                        self.post(route, payload)
                        if module.endswith("api")
                        else self.client.post(reverse(route), payload)
                    )
                self.assertEqual(response.status_code, expected_status)
                if expected_status == 200:
                    self.assertIn("username", response.context["form"].errors)
                self.assertEqual(User.objects.filter(username=username).count(), 1)

    def test_json_login_and_writes_remain_csrf_protected(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(
            reverse("api-login"),
            {"username": self.admin.username, "password": "Validpass123"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertNotIn("_auth_user_id", client.session)
        client.force_login(self.admin)
        self.assertEqual(
            client.post(
                reverse("api-user-create"),
                {
                    "username": "csrf-api-user",
                    "password": "Differentpass456",
                    "role": "student",
                },
                content_type="application/json",
            ).status_code,
            403,
        )
        self.assertFalse(User.objects.filter(username="csrf-api-user").exists())

    def test_multipart_logout_with_valid_csrf_does_not_reread_consumed_body(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.warden)
        client.get(reverse("settings"))

        response = client.post(
            reverse("api-logout"),
            {},
            HTTP_X_CSRFTOKEN=client.cookies["csrftoken"].value,
        )

        self.assertEqual(response.status_code, 204)
        self.assertNotIn("_auth_user_id", client.session)
