from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from .models import AuditEvent
from .services import record_event


class AuditEventTests(TestCase):
    def test_record_event_saves_actor_action_record_reference_and_timestamp(self):
        actor = User.objects.create_user(username='warden', password='Validpass123', role=User.Role.WARDEN)

        event = record_event(
            'allocation_create', actor=actor, record_type='allocation', record_id=123,
        )

        self.assertEqual(event.actor, actor)
        self.assertEqual(event.action, 'allocation_create')
        self.assertEqual(event.record_type, 'allocation')
        self.assertEqual(event.record_id, '123')
        self.assertIsNotNone(event.timestamp)

    def test_record_event_does_not_attach_anonymous_actor(self):
        event = record_event('login_failure', actor=None, record_type='authentication')
        self.assertIsNone(event.actor)

    def test_record_id_is_bounded_to_model_field_length(self):
        event = record_event('user_update', record_id='x' * 100)
        self.assertEqual(len(event.record_id), 80)

    def test_events_are_ordered_newest_first(self):
        first = record_event('login_success')
        second = record_event('logout')
        AuditEvent.objects.filter(pk=first.pk).update(timestamp=timezone.now() - timedelta(seconds=1))
        self.assertEqual(list(AuditEvent.objects.all()), [second, first])

    def test_audit_events_cannot_be_deleted_from_admin(self):
        from audit.admin import AuditEventAdmin

        self.assertFalse(AuditEventAdmin.has_delete_permission(None, None))
