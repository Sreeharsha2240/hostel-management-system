"""Authentication audit-signal decisions with writes mocked."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from .models import AuditEvent
from .signals import log_login, log_login_failure, log_logout


class AuthenticationAuditSignalUnitTests(SimpleTestCase):
    @patch("audit.signals.record_event")
    def test_login_records_authenticated_user(self, record):
        user = SimpleNamespace(is_authenticated=True, pk=1)
        log_login(sender=None, request=None, user=user)
        record.assert_called_once_with(
            user=user, action=AuditEvent.Action.LOGIN, record=user
        )

    @patch("audit.signals.record_event")
    @patch("audit.signals.get_user_model")
    def test_login_failure_records_user_identity_without_password(
        self, get_user, record
    ):
        target = Mock()
        get_user.return_value.objects.filter.return_value.first.return_value = target
        log_login_failure(
            sender=None,
            credentials={"username": "Alice", "password": "secret"},
            request=None,
        )
        get_user.return_value.objects.filter.assert_called_once_with(
            username__iexact="Alice"
        )
        record.assert_called_once_with(
            user=None,
            action=AuditEvent.Action.LOGIN_FAILED,
            record=target,
            record_type="accounts.user",
        )
        self.assertNotIn("secret", str(record.call_args))

    @patch("audit.signals.record_event")
    @patch("audit.signals.get_user_model")
    def test_invalid_or_oversized_usernames_are_not_queried(self, get_user, record):
        for username in (None, ["alice"], "a" * 151):
            with self.subTest(username=username):
                log_login_failure(
                    sender=None, credentials={"username": username}, request=None
                )
        get_user.assert_not_called()
        self.assertEqual(record.call_count, 3)
        for entry in record.call_args_list:
            self.assertIsNone(entry.kwargs["record"])

    @patch("audit.signals.record_event")
    def test_logout_only_records_authenticated_user(self, record):
        log_logout(sender=None, request=None, user=None)
        log_logout(
            sender=None, request=None, user=SimpleNamespace(is_authenticated=False)
        )
        record.assert_not_called()
        user = SimpleNamespace(is_authenticated=True)
        log_logout(sender=None, request=None, user=user)
        record.assert_called_once_with(
            user=user, action=AuditEvent.Action.LOGOUT, record=user
        )
