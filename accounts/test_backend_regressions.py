"""A password replacement must take effect during an in-flight login."""

from contextlib import nullcontext
from unittest.mock import patch

from django.contrib.auth.hashers import PBKDF2PasswordHasher, check_password
from django.test import SimpleTestCase

from .backends import LockoutBackend
from .models import User


class ChangedPasswordAuthenticationTests(SimpleTestCase):
    def test_hash_upgrade_cannot_overwrite_a_concurrent_password_reset(self):
        initial = User(pk=41, username="hash-upgrade")
        initial.password = PBKDF2PasswordHasher().encode(
            "Originalpass123", "old-salt", iterations=1
        )
        current = User(pk=41, username=initial.username)
        current.set_password("Replacementpass123")
        replacement_hash = current.password

        def stale_upgrade_write(*args, **kwargs):
            # Reproduce the old check_password setter writing its upgraded
            # hash after the separate password reset has already committed.
            current.password = initial.password

        with (
            patch.object(
                User._default_manager, "get_by_natural_key", return_value=initial
            ),
            patch.object(User.objects, "select_for_update") as locked,
            patch.object(
                initial, "save", side_effect=stale_upgrade_write
            ) as stale_save,
            patch.object(current, "save"),
            patch("accounts.backends.transaction.atomic", return_value=nullcontext()),
        ):
            locked.return_value.get.return_value = current
            result = LockoutBackend().authenticate(
                None, username=initial.username, password="Originalpass123"
            )

        self.assertIsNone(result)
        stale_save.assert_not_called()
        self.assertEqual(current.password, replacement_hash)

    def test_legacy_password_hash_is_upgraded_only_on_the_locked_instance(self):
        initial = User(pk=41, username="hash-upgrade")
        initial.password = PBKDF2PasswordHasher().encode(
            "Originalpass123", "old-salt", iterations=1
        )
        current = User(pk=41, username=initial.username, password=initial.password)

        with (
            patch.object(
                User._default_manager, "get_by_natural_key", return_value=initial
            ),
            patch.object(User.objects, "select_for_update") as locked,
            patch.object(initial, "save") as stale_save,
            patch.object(current, "save") as current_save,
            patch("accounts.backends.transaction.atomic", return_value=nullcontext()),
        ):
            locked.return_value.get.return_value = current
            result = LockoutBackend().authenticate(
                None, username=initial.username, password="Originalpass123"
            )

        self.assertIs(result, current)
        self.assertNotEqual(current.password, initial.password)
        self.assertTrue(check_password("Originalpass123", current.password))
        stale_save.assert_not_called()
        self.assertIn("password", current_save.call_args.kwargs["update_fields"])

    def authenticate_after_password_change(self, password):
        initial = User(pk=41, username="changing-password", failed_attempts=1)
        initial.set_password("Originalpass123")
        current = User(pk=initial.pk, username=initial.username, failed_attempts=3)
        current.set_password("Replacementpass123")

        with (
            patch.object(
                User._default_manager, "get_by_natural_key", return_value=initial
            ) as lookup,
            patch.object(User.objects, "select_for_update") as locked_lookup,
            patch.object(current, "save") as save,
            patch(
                "accounts.backends.transaction.atomic", return_value=nullcontext()
            ) as atomic,
        ):
            locked_lookup.return_value.get.return_value = current

            result = LockoutBackend().authenticate(
                None, username=initial.username, password=password
            )

            lookup.assert_called_once_with(initial.username)
            atomic.assert_called_once_with()
            locked_lookup.assert_called_once_with()
            locked_lookup.return_value.get.assert_called_once_with(pk=initial.pk)
            save.assert_called_once_with(
                update_fields=["failed_attempts", "locked_until"]
            )

        self.assertEqual(initial.failed_attempts, 1)
        self.assertIsNone(current.locked_until)
        return result, current

    def test_replaced_password_is_rejected_after_locked_reread(self):
        result, current = self.authenticate_after_password_change("Originalpass123")

        self.assertIsNone(result)
        self.assertEqual(current.failed_attempts, 4)

    def test_new_password_is_accepted_after_locked_reread(self):
        result, current = self.authenticate_after_password_change("Replacementpass123")

        self.assertIs(result, current)
        self.assertEqual(current.failed_attempts, 0)
