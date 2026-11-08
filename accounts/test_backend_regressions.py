"""A password replacement must take effect during an in-flight login."""

from contextlib import nullcontext
from unittest.mock import patch

from django.test import SimpleTestCase

from .backends import LockoutBackend
from .models import User


class ChangedPasswordAuthenticationTests(SimpleTestCase):
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
