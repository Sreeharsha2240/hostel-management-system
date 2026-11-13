"""Isolated audit immutability, retention and event-recording contracts."""

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from .mixins import AuditedAdminMixin
from .models import AuditEvent
from .services import record_event


class AuditEventUnitTests(SimpleTestCase):
    def test_bulk_mutations_and_delete_are_rejected(self):
        events = AuditEvent.objects.all()
        operations = (
            lambda: events.update(action="create"),
            lambda: events.delete(),
            lambda: events.bulk_update([], ["action"]),
            lambda: events.bulk_create([], update_conflicts=True),
        )
        for operation in operations:
            with self.subTest(operation=operation), self.assertRaises(ValidationError):
                operation()

    @patch("audit.models.timezone.now", return_value=datetime(2026, 11, 13, tzinfo=UTC))
    def test_retention_rejects_cutoff_younger_than_366_days(self, now):
        with self.assertRaisesMessage(ValidationError, "at least one year"):
            AuditEvent.objects.all().purge_before(
                now.return_value - timedelta(days=365)
            )

    @patch(
        "django.db.models.QuerySet.delete", return_value=(2, {"audit.AuditEvent": 2})
    )
    @patch("audit.models.timezone.now", return_value=datetime(2026, 11, 13, tzinfo=UTC))
    def test_retention_allows_366_day_cutoff(self, now, delete):
        cutoff = now.return_value - timedelta(days=366)
        result = AuditEvent.objects.all().purge_before(cutoff)
        self.assertEqual(result[0], 2)
        delete.assert_called_once()

    @patch("django.db.models.Model.save", return_value=None)
    def test_new_event_is_force_inserted_and_existing_event_is_immutable(self, save):
        event = AuditEvent(action=AuditEvent.Action.CREATE, record_type="student")
        event.save()
        self.assertTrue(save.call_args.kwargs["force_insert"])
        event._state.adding = False
        with self.assertRaisesMessage(ValidationError, "cannot be changed"):
            event.save()
        with self.assertRaisesMessage(ValidationError, "one-year retention"):
            event.delete()

    @patch("audit.services.AuditEvent.objects.create")
    def test_record_event_uses_only_record_identifiers(self, create):
        user = SimpleNamespace(is_authenticated=True)
        record = SimpleNamespace(
            pk=42, _meta=SimpleNamespace(label_lower="students.student")
        )
        result = record_event(user=user, action=AuditEvent.Action.UPDATE, record=record)
        create.assert_called_once_with(
            user=user,
            action=AuditEvent.Action.UPDATE,
            record_type="students.student",
            record_id="42",
        )
        self.assertIs(result, create.return_value)

    @patch("audit.services.AuditEvent.objects.create")
    def test_anonymous_actor_is_recorded_without_user(self, create):
        user = SimpleNamespace(is_authenticated=False)
        record_event(
            user=user,
            action=AuditEvent.Action.LOGIN_FAILED,
            record_type="login",
            record_id="x",
        )
        self.assertIsNone(create.call_args.kwargs["user"])

    @patch("audit.services.AuditEvent.objects.create")
    def test_unknown_action_or_missing_record_type_is_rejected(self, create):
        for action, record_type in (
            ("invalid", "student"),
            (AuditEvent.Action.CREATE, ""),
        ):
            with self.subTest(action=action), self.assertRaises(ValueError):
                record_event(user=None, action=action, record_type=record_type)
        create.assert_not_called()


class _AdminParent:
    def save_model(self, request, obj, form, change):
        self.saved = (request, obj, form, change)

    def log_addition(self, request, obj, message):
        self.logged = (request, obj, message)

    def log_change(self, request, obj, message):
        self.logged = (request, obj, message)


class _TestAdmin(AuditedAdminMixin, _AdminParent):
    pass


class AuditAdminUnitTests(SimpleTestCase):
    def test_save_model_classifies_create_update_and_deactivation(self):
        class Record:
            objects = Mock()

        admin = _TestAdmin()
        obj = Record()
        obj.pk, obj.is_active, obj.status = 1, True, "Active"
        admin.save_model(None, obj, None, False)
        self.assertEqual(obj._audit_action, AuditEvent.Action.CREATE)
        Record.objects.get.return_value = SimpleNamespace(
            is_active=True, status="Active"
        )
        admin.save_model(None, obj, None, True)
        self.assertEqual(obj._audit_action, AuditEvent.Action.UPDATE)
        obj.is_active = False
        admin.save_model(None, obj, None, True)
        self.assertEqual(obj._audit_action, AuditEvent.Action.DEACTIVATE)
        self.assertFalse(admin.has_delete_permission(None, obj))

    @patch("audit.mixins.record_event")
    def test_admin_log_methods_record_correct_actor_and_action(self, record):
        admin = _TestAdmin()
        request, obj = (
            SimpleNamespace(user="actor"),
            SimpleNamespace(_audit_action=AuditEvent.Action.DEACTIVATE),
        )
        admin.log_addition(request, obj, "created")
        record.assert_called_with(
            user="actor", action=AuditEvent.Action.CREATE, record=obj
        )
        admin.log_change(request, obj, "changed")
        record.assert_called_with(
            user="actor", action=AuditEvent.Action.DEACTIVATE, record=obj
        )
        self.assertEqual(record.call_count, 2)
