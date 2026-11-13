"""Database-free tests of authentication lockout decisions."""

from contextlib import nullcontext
from datetime import timedelta
from unittest.mock import patch

from django.test import SimpleTestCase
from django.utils import timezone

from .backends import LockoutBackend
from .models import User


class LockoutDecisionUnitTests(SimpleTestCase):
    def setUp(self):
        self.now = timezone.now()
        self.initial = User(pk=7, username="warden", is_active=True)
        self.initial.set_password("Validpass123")
        self.current = User(pk=7, username="warden", is_active=True)
        self.current.password = self.initial.password

    def authenticate(self, password):
        with (
            patch.object(
                User._default_manager, "get_by_natural_key", return_value=self.initial
            ),
            patch.object(User.objects, "select_for_update") as locked,
            patch.object(self.current, "save") as save,
            patch("accounts.backends.transaction.atomic", return_value=nullcontext()),
            patch("accounts.backends.timezone.now", return_value=self.now),
        ):
            locked.return_value.get.return_value = self.current
            result = LockoutBackend().authenticate(
                None, username="warden", password=password
            )
        return result, save

    def test_missing_credentials_do_not_query_user(self):
        with patch.object(User._default_manager, "get_by_natural_key") as lookup:
            self.assertIsNone(
                LockoutBackend().authenticate(None, username=None, password="x")
            )
            self.assertIsNone(
                LockoutBackend().authenticate(None, username="warden", password=None)
            )
        lookup.assert_not_called()

    def test_unknown_user_returns_none(self):
        with patch.object(
            User._default_manager, "get_by_natural_key", side_effect=User.DoesNotExist
        ):
            self.assertIsNone(
                LockoutBackend().authenticate(None, username="missing", password="x")
            )

    def test_wrong_password_increments_attempts(self):
        self.current.failed_attempts = 2
        result, save = self.authenticate("wrong")
        self.assertIsNone(result)
        self.assertEqual(self.current.failed_attempts, 3)
        self.assertIsNone(self.current.locked_until)
        save.assert_called_once_with(update_fields=["failed_attempts", "locked_until"])

    def test_fifth_failure_locks_for_fifteen_minutes(self):
        self.current.failed_attempts = 4
        result, save = self.authenticate("wrong")
        self.assertIsNone(result)
        self.assertEqual(self.current.failed_attempts, 0)
        self.assertEqual(self.current.locked_until, self.now + timedelta(minutes=15))
        save.assert_called_once()

    def test_active_lock_and_inactive_user_are_rejected_without_write(self):
        for active, locked_until in (
            (True, self.now + timedelta(minutes=1)),
            (False, None),
        ):
            with self.subTest(active=active):
                self.current.is_active = active
                self.current.locked_until = locked_until
                result, save = self.authenticate("Validpass123")
                self.assertIsNone(result)
                save.assert_not_called()

    def test_success_clears_expired_lock_and_failed_attempts(self):
        self.current.failed_attempts = 4
        self.current.locked_until = self.now - timedelta(seconds=1)
        result, save = self.authenticate("Validpass123")
        self.assertIs(result, self.current)
        self.assertEqual(self.current.failed_attempts, 0)
        self.assertIsNone(self.current.locked_until)
        save.assert_called_once()
