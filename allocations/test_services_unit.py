"""Service-level decisions with persistence and audit boundaries mocked."""

from datetime import date
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from audit.models import AuditEvent
from payments.services import record_payment

from .models import Allocation
from .services import allocate, release, transfer


class AllocationServiceUnitTests(SimpleTestCase):
    @patch("allocations.services.record_event")
    @patch("allocations.services.Allocation")
    def test_allocate_saves_requested_date_and_records_actor(self, allocation, audit):
        allocation.return_value = Mock()
        result = allocate.__wrapped__(
            student="student", bed="bed", actor="warden", allocated_on=date(2026, 11, 1)
        )
        allocation.assert_called_once_with(student="student", bed="bed")
        self.assertEqual(result.allocated_on, date(2026, 11, 1))
        result.save.assert_called_once()
        audit.assert_called_once_with(
            user="warden", action=AuditEvent.Action.ALLOCATE, record=result
        )

    @patch("allocations.services.record_event")
    @patch("allocations.services.Allocation")
    def test_failed_allocation_does_not_emit_audit_event(self, allocation, audit):
        allocation.return_value.save.side_effect = ValidationError("unavailable")
        with self.assertRaises(ValidationError):
            allocate.__wrapped__(student="student", bed="bed", actor="warden")
        audit.assert_not_called()

    @patch("allocations.services.record_event")
    @patch("allocations.services.lock_allocation")
    def test_release_uses_explicit_date_and_records_actor(self, lock, audit):
        item = Mock()
        lock.return_value = item
        result = release.__wrapped__(
            allocation_id=7, actor="warden", vacate_date=date(2026, 11, 13)
        )
        self.assertIs(result, item)
        self.assertEqual(
            (item.status, item.vacated_on),
            (Allocation.AllocationStatus.COMPLETED, date(2026, 11, 13)),
        )
        item.save.assert_called_once_with(update_fields=["status", "vacated_on"])
        audit.assert_called_once_with(
            user="warden", action=AuditEvent.Action.RELEASE, record=item
        )

    @patch("allocations.services.timezone.localdate", return_value=date(2026, 11, 13))
    @patch("allocations.services.record_event")
    @patch("allocations.services.lock_allocation")
    def test_release_defaults_to_local_date(self, lock, audit, today):
        item = Mock()
        lock.return_value = item
        release.__wrapped__(allocation_id=7, actor="warden")
        self.assertEqual(item.vacated_on, date(2026, 11, 13))
        today.assert_called_once()

    @patch("allocations.services.record_event")
    @patch("allocations.services.lock_allocation")
    def test_transfer_to_same_bed_is_rejected_before_write(self, lock, audit):
        original = Mock(bed_id=5)
        lock.return_value = original
        with self.assertRaises(ValidationError) as error:
            transfer.__wrapped__(
                allocation_id=7, new_bed=SimpleNamespace(pk=5), actor="warden"
            )
        self.assertEqual(error.exception.code, "BED_OCCUPIED")
        original.save.assert_not_called()
        audit.assert_not_called()

    @patch("allocations.services.timezone.localdate", return_value=date(2026, 11, 13))
    @patch("allocations.services.record_event")
    @patch("allocations.services.Allocation")
    @patch("allocations.services.lock_allocation")
    def test_transfer_completes_old_allocation_and_saves_successor(
        self, lock, allocation, audit, today
    ):
        original = Mock(bed_id=5, student_id=11)
        lock.return_value = original
        allocation.AllocationStatus.COMPLETED = Allocation.AllocationStatus.COMPLETED
        successor = allocation.return_value
        bed = SimpleNamespace(pk=6)
        self.assertIs(
            transfer.__wrapped__(allocation_id=7, new_bed=bed, actor="warden"),
            successor,
        )
        self.assertEqual(original.status, Allocation.AllocationStatus.COMPLETED)
        self.assertEqual(original.vacated_on, date(2026, 11, 13))
        allocation.assert_called_once_with(student_id=11, bed=bed)
        successor.save.assert_called_once()
        audit.assert_called_once_with(
            user="warden", action=AuditEvent.Action.TRANSFER, record=successor
        )


class PaymentServiceUnitTests(SimpleTestCase):
    @patch("payments.services.record_event")
    @patch("payments.services.Payment")
    def test_payment_service_saves_before_recording_event(self, payment, audit):
        result = record_payment.__wrapped__(actor="warden", amount="25")
        payment.assert_called_once_with(amount="25")
        result.save.assert_called_once()
        audit.assert_called_once_with(
            user="warden", action=AuditEvent.Action.PAYMENT, record=result
        )

    @patch("payments.services.record_event")
    @patch("payments.services.Payment")
    def test_failed_payment_does_not_emit_audit_event(self, payment, audit):
        payment.return_value.save.side_effect = ValidationError("invalid")
        with self.assertRaises(ValidationError):
            record_payment.__wrapped__(actor="warden", amount="-1")
        audit.assert_not_called()
