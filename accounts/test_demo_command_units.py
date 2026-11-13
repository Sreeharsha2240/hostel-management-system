"""Isolated checks for the demo-account command's safety and retry rules."""

from contextlib import nullcontext
from io import StringIO
from unittest.mock import Mock, patch

from django.core.exceptions import ValidationError
from django.core.management.base import CommandError
from django.test import SimpleTestCase, override_settings

from .management.commands.create_demo_accounts import Command


class DemoAccountCommandUnitTests(SimpleTestCase):
    @override_settings(DEBUG=False)
    @patch("accounts.management.commands.create_demo_accounts.getpass")
    def test_command_is_disabled_outside_debug(self, getpass):
        with self.assertRaisesMessage(CommandError, "only be created"):
            Command().handle()
        getpass.assert_not_called()

    @override_settings(DEBUG=True)
    @patch(
        "accounts.management.commands.create_demo_accounts.transaction.atomic",
        return_value=nullcontext(),
    )
    @patch(
        "accounts.management.commands.create_demo_accounts.User.objects.get_or_create"
    )
    @patch("accounts.management.commands.create_demo_accounts.validate_password")
    @patch("accounts.management.commands.create_demo_accounts.getpass")
    def test_command_retries_bad_passwords_then_sets_roles(
        self, getpass, validate, get_or_create, atomic
    ):
        getpass.side_effect = [
            "bad",
            "mismatch",
            "weak",
            "weak",
            "Validpass123",
            "Validpass123",
            "Validpass234",
            "Validpass234",
            "Validpass345",
            "Validpass345",
        ]
        validate.side_effect = [ValidationError("Too weak"), None, None, None]
        users = [Mock(), Mock(), Mock()]
        get_or_create.side_effect = [
            (users[0], True),
            (users[1], False),
            (users[2], True),
        ]
        output, errors = StringIO(), StringIO()
        command = Command(stdout=output, stderr=errors)
        command.handle()
        self.assertIn("Passwords must be non-empty and match", errors.getvalue())
        self.assertIn("Too weak", errors.getvalue())
        self.assertEqual(get_or_create.call_count, 3)
        self.assertEqual([user.role for user in users], ["admin", "warden", "student"])
        self.assertEqual([user.is_superuser for user in users], [True, False, False])
        for user in users:
            user.set_password.assert_called_once()
            user.save.assert_called_once()
        self.assertIn("Reset warden login", output.getvalue())
        atomic.assert_called_once_with()
