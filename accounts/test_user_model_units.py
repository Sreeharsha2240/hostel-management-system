"""User role and lockout model decisions without database access."""

from datetime import UTC, datetime, timedelta
from unittest.mock import patch

from django.test import SimpleTestCase

from .models import User


class UserModelUnitTests(SimpleTestCase):
    @patch(
        "accounts.models.timezone.now", return_value=datetime(2026, 11, 13, tzinfo=UTC)
    )
    def test_lock_is_active_only_before_expiry(self, now):
        for until, expected in (
            (None, False),
            (now.return_value - timedelta(seconds=1), False),
            (now.return_value, False),
            (now.return_value + timedelta(seconds=1), True),
        ):
            with self.subTest(until=until):
                self.assertEqual(User(locked_until=until).is_locked(), expected)

    @patch("django.db.models.Model.save", return_value=None)
    def test_superuser_save_enforces_admin_role_and_update_fields(self, save):
        user = User(is_superuser=True, role=User.Role.STUDENT)
        user.save(update_fields=["first_name"])
        self.assertEqual(user.role, User.Role.ADMIN)
        self.assertEqual(save.call_args.kwargs["update_fields"], {"first_name", "role"})

    @patch("django.db.models.Model.save", return_value=None)
    def test_ordinary_user_save_preserves_role(self, save):
        user = User(is_superuser=False, role=User.Role.WARDEN)
        user.save(update_fields=["first_name"])
        self.assertEqual(user.role, User.Role.WARDEN)
        self.assertEqual(save.call_args.kwargs["update_fields"], ["first_name"])

    @patch("django.db.models.Model.save", return_value=None)
    def test_student_save_revokes_staff_and_persists_it_with_update_fields(self, save):
        user = User(role=User.Role.STUDENT, is_staff=True)
        user.save(update_fields=["role"])
        self.assertFalse(user.is_staff)
        self.assertEqual(save.call_args.kwargs["update_fields"], {"role", "is_staff"})
