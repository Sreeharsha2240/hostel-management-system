"""Account API decisions with real forms and no database access.

Persistence, authentication/session and audit calls are external boundaries here;
the integration suite separately proves their database and transaction behavior.
"""

import inspect
import json
from contextlib import nullcontext
from datetime import timedelta
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import RequestFactory, SimpleTestCase
from django.utils import timezone

from . import api
from .models import User


class AccountApiUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin = User(pk=1, username="administrator", role=User.Role.ADMIN)
        self.account = User(pk=2, username="resident", role=User.Role.WARDEN)
        self.audit = self.enterContext(patch("accounts.api.record_event"))
        self.atomic = self.enterContext(
            patch("accounts.api.transaction.atomic", side_effect=lambda: nullcontext())
        )
        self.unique = self.enterContext(patch.object(User, "validate_unique"))
        self.save = self.enterContext(patch.object(User, "save", autospec=True))
        self.lookup = self.enterContext(
            patch("accounts.api.get_object_or_404", return_value=self.account)
        )

    def request(self, method, data, user=None):
        request = getattr(self.factory, method)(
            "/users/", data, content_type="application/json"
        )
        request.user = self.admin if user is None else user
        return request

    def body(self, response):
        return json.loads(response.content)

    def assert_error(self, response, status, code):
        self.assertEqual(response.status_code, status, response.content)
        self.assertEqual(self.body(response)["error"]["code"], code)

    def login(self, data):
        # The atomic decorator is an integration boundary; exercise the real body.
        return inspect.unwrap(api.sign_in)(self.request("post", data))

    def test_sign_in_trims_username_but_preserves_password_and_returns_role(self):
        with (
            patch(
                "accounts.api.authenticate", return_value=self.account
            ) as authenticate,
            patch("accounts.api.login") as login,
        ):
            request = self.request(
                "post", {"username": " resident ", "password": " secret "}
            )
            response = inspect.unwrap(api.sign_in)(request)
        self.assertEqual(
            self.body(response), {"role": "warden", "redirect": "/dashboard/"}
        )
        authenticate.assert_called_once_with(
            request, username="resident", password=" secret "
        )
        login.assert_called_once_with(request, self.account)
        self.audit.assert_not_called()

    def test_sign_in_validation_never_calls_authentication(self):
        for data in (
            {},
            {"username": " ", "password": "p"},
            {"username": "x" * 151, "password": "p"},
            {"username": True, "password": "p"},
            {"username": "resident", "password": 1},
            {"username": "resident", "password": "p", "role": "admin"},
        ):
            with (
                self.subTest(data=data),
                patch("accounts.api.authenticate") as authenticate,
            ):
                self.assert_error(self.login(data), 400, "VALIDATION_ERROR")
                authenticate.assert_not_called()
        self.save.assert_not_called()

    def test_sign_in_failure_distinguishes_only_active_current_lock(self):
        locked = User(
            pk=3, role="warden", locked_until=timezone.now() + timedelta(minutes=1)
        )
        inactive = User(
            pk=4, role="warden", is_active=False, locked_until=locked.locked_until
        )
        expired = User(
            pk=5, role="warden", locked_until=timezone.now() - timedelta(seconds=1)
        )
        for target, status, code in (
            (None, 401, "INVALID_CREDENTIALS"),
            (self.account, 401, "INVALID_CREDENTIALS"),
            (locked, 423, "ACCOUNT_LOCKED"),
            (inactive, 401, "INVALID_CREDENTIALS"),
            (expired, 401, "INVALID_CREDENTIALS"),
        ):
            with (
                self.subTest(target=target),
                patch("accounts.api.authenticate", return_value=None),
                patch.object(User.objects, "filter") as lookup,
                patch("accounts.api.login") as login,
            ):
                lookup.return_value.first.return_value = target
                self.assert_error(
                    self.login({"username": "resident", "password": "wrong"}),
                    status,
                    code,
                )
                lookup.assert_called_once_with(username="resident")
                login.assert_not_called()

    def test_sign_in_invalid_stored_role_is_audited_without_opening_session(self):
        self.account.role = "unrecognized"
        request = self.request("post", {"username": "resident", "password": "secret"})
        with (
            patch("accounts.api.authenticate", return_value=self.account),
            patch("accounts.api.login") as login,
        ):
            self.assert_error(
                inspect.unwrap(api.sign_in)(request), 403, "ACCESS_DENIED"
            )
        self.audit.assert_called_once_with(
            user=self.account,
            action="access_denied",
            record_type="view",
            record_id="sign_in",
        )
        self.assertTrue(request._access_denied_audited)
        login.assert_not_called()

    def test_sign_out_accepts_empty_json_body_and_rejects_extra_fields(self):
        with patch("accounts.api.logout") as logout:
            for request in (
                self.request("post", {}),
                self.factory.generic(
                    "POST", "/auth/logout/", CONTENT_TYPE="application/json"
                ),
                self.factory.post("/auth/logout/", {}),
            ):
                request.user = self.admin
                response = api.sign_out(request)
                self.assertEqual((response.status_code, response.content), (204, b""))
            self.assertEqual(logout.call_count, 3)
            logout.reset_mock()
            self.assert_error(
                api.sign_out(self.request("post", {"is_active": False})),
                400,
                "VALIDATION_ERROR",
            )
            logout.assert_not_called()

    def test_create_uses_real_password_validation_and_hashing(self):
        captured = []

        def save(account, **kwargs):
            account.pk = 17
            captured.append(account)

        self.save.side_effect = save
        request = self.request(
            "post",
            {
                "username": "new-warden",
                "password": "DistinctStrongPass784!",
                "role": "warden",
            },
        )
        response = api.user_create(request)
        self.assertEqual(
            (response.status_code, self.body(response)),
            (201, {"id": 17, "role": "warden"}),
        )
        self.assertTrue(captured[0].check_password("DistinctStrongPass784!"))
        self.assertFalse(captured[0].is_superuser)
        self.audit.assert_called_once_with(
            user=self.admin, action="create", record=captured[0]
        )

    def test_create_rejects_weak_password_invalid_role_and_undeclared_fields_without_write(
        self,
    ):
        base = {
            "username": "new-warden",
            "password": "DistinctStrongPass784!",
            "role": "warden",
        }
        for changes in (
            {"password": "abc"},
            {"role": "owner"},
            {"role": False},
            {"is_staff": True},
        ):
            with self.subTest(changes=changes):
                self.assert_error(
                    api.user_create(self.request("post", base | changes)),
                    400,
                    "VALIDATION_ERROR",
                )
        self.save.assert_not_called()
        self.audit.assert_not_called()

    def test_create_duplicate_validation_preserves_field_errors(self):
        self.unique.side_effect = ValidationError(
            {"username": ValidationError("Already used.", code="unique")}
        )
        response = api.user_create(
            self.request(
                "post",
                {
                    "username": "taken",
                    "password": "DistinctStrongPass784!",
                    "role": "warden",
                },
            )
        )
        self.assert_error(response, 409, "DUPLICATE")
        self.assertEqual(
            self.body(response)["error"]["fields"]["username"][0]["code"], "unique"
        )
        self.save.assert_not_called()

    def test_create_integrity_error_is_duplicate_only_when_username_exists(self):
        self.save.side_effect = IntegrityError("write rejected")
        data = {
            "username": "new-warden",
            "password": "DistinctStrongPass784!",
            "role": "warden",
        }
        for exists in (True, False):
            with (
                self.subTest(exists=exists),
                patch.object(User.objects, "filter") as lookup,
            ):
                lookup.return_value.exists.return_value = exists
                if exists:
                    self.assert_error(
                        api.user_create(self.request("post", data)), 409, "DUPLICATE"
                    )
                else:
                    with self.assertRaisesMessage(IntegrityError, "write rejected"):
                        api.user_create(self.request("post", data))
                lookup.assert_called_once_with(username="new-warden")
        self.audit.assert_not_called()

    def test_update_changes_only_declared_fields_and_chooses_audit_action(self):
        for payload, action in (
            ({"role": "student"}, "update"),
            ({"is_active": False}, "deactivate"),
            ({"is_active": True}, "update"),
        ):
            with self.subTest(payload=payload):
                self.account.role = "warden"
                self.account.is_active = not payload.get("is_active", False)
                self.save.reset_mock()
                self.audit.reset_mock()
                response = api.user_update(
                    self.request("patch", payload), self.account.pk
                )
                self.assertEqual(response.status_code, 200, response.content)
                self.save.assert_called_once_with(
                    self.account, update_fields=set(payload)
                )
                self.audit.assert_called_once_with(
                    user=self.admin, action=action, record=self.account
                )
                self.assertEqual(
                    self.body(response),
                    {
                        "id": 2,
                        "role": self.account.role,
                        "is_active": self.account.is_active,
                    },
                )

    def test_update_identical_values_do_not_write_or_audit(self):
        response = api.user_update(
            self.request("patch", {"role": "warden", "is_active": True}), 2
        )
        self.assertEqual(response.status_code, 200)
        self.save.assert_not_called()
        self.audit.assert_not_called()

    def test_update_invalid_payload_does_not_look_up_or_write_account(self):
        for payload in ({}, {"is_active": 0}, {"role": False}, {"password": "changed"}):
            with self.subTest(payload=payload):
                self.assert_error(
                    api.user_update(self.request("patch", payload), 2),
                    400,
                    "VALIDATION_ERROR",
                )
        self.lookup.assert_not_called()
        self.save.assert_not_called()

    def test_update_self_deactivation_is_denied_and_audited(self):
        self.lookup.return_value = self.admin
        request = self.request("patch", {"is_active": False})
        self.assert_error(api.user_update(request, 1), 403, "ACCESS_DENIED")
        self.assertTrue(request._access_denied_audited)
        self.assertTrue(self.admin.is_active)
        self.audit.assert_called_once_with(
            user=self.admin,
            action="access_denied",
            record_type="view",
            record_id="user_update",
        )
        self.save.assert_not_called()

    def test_update_cannot_demote_superuser_and_propagates_audit_failure(self):
        self.account.is_superuser = True
        self.account.role = "admin"
        self.assert_error(
            api.user_update(self.request("patch", {"role": "student"}), 2),
            400,
            "VALIDATION_ERROR",
        )
        self.save.assert_not_called()
        self.account.is_superuser = False
        self.audit.side_effect = RuntimeError("audit unavailable")
        exits = []

        class AtomicBoundary:
            def __enter__(self):
                return self

            def __exit__(self, exception_type, exception, traceback):
                exits.append(exception_type)
                return False

        self.atomic.side_effect = AtomicBoundary
        with self.assertRaisesMessage(RuntimeError, "audit unavailable"):
            api.user_update(self.request("patch", {"is_active": False}), 2)
        self.save.assert_called_once_with(self.account, update_fields={"is_active"})
        self.assertEqual(exits, [RuntimeError])
