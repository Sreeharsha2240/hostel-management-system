"""Audit retention command safety decisions without database writes."""

from datetime import UTC, datetime, timedelta
from io import StringIO
from unittest.mock import patch

from django.core.management.base import CommandError
from django.test import SimpleTestCase

from .management.commands.purge_audit_logs import Command


class PurgeAuditCommandUnitTests(SimpleTestCase):
    @patch("audit.management.commands.purge_audit_logs.AuditEvent.objects.filter")
    def test_short_retention_is_rejected_without_query(self, query):
        with self.assertRaisesMessage(CommandError, "at least 366"):
            Command().handle(days=365, dry_run=False)
        query.assert_not_called()

    @patch(
        "audit.management.commands.purge_audit_logs.timezone.now",
        return_value=datetime(2026, 11, 13, tzinfo=UTC),
    )
    @patch("audit.management.commands.purge_audit_logs.AuditEvent.objects.purge_before")
    @patch("audit.management.commands.purge_audit_logs.AuditEvent.objects.filter")
    def test_dry_run_counts_without_deleting(self, query, purge, now):
        query.return_value.count.return_value = 3
        output = StringIO()
        Command(stdout=output).handle(days=366, dry_run=True)
        query.assert_called_once_with(
            timestamp__lt=now.return_value - timedelta(days=366)
        )
        self.assertIn("3 audit entries eligible", output.getvalue())
        purge.assert_not_called()

    @patch(
        "audit.management.commands.purge_audit_logs.timezone.now",
        return_value=datetime(2026, 11, 13, tzinfo=UTC),
    )
    @patch(
        "audit.management.commands.purge_audit_logs.AuditEvent.objects.purge_before",
        return_value=(2, {}),
    )
    @patch("audit.management.commands.purge_audit_logs.AuditEvent.objects.filter")
    def test_purge_uses_valid_cutoff_and_reports_count(self, query, purge, now):
        output = StringIO()
        Command(stdout=output).handle(days=400, dry_run=False)
        cutoff = now.return_value - timedelta(days=400)
        query.assert_called_once_with(timestamp__lt=cutoff)
        purge.assert_called_once_with(cutoff)
        self.assertIn("Removed 2 expired audit entries", output.getvalue())
