"""Admission must not invert the inventory Hostel -> Room lock order."""

from concurrent.futures import ThreadPoolExecutor, TimeoutError
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db import close_old_connections, connections, transaction
from django.test import TestCase, TransactionTestCase, skipUnlessDBFeature
from django.utils import timezone

from accounts.models import User
from audit.models import AuditEvent
from hostels.models import Bed, Hostel, Room
from tests.factories import make_room, make_student

from .models import Allocation
from .services import allocate, transfer


class AllocationInventoryLockOrderTests(TransactionTestCase):
    @skipUnlessDBFeature("has_select_for_update")
    def test_transfer_rejects_target_moved_after_room_snapshot(self):
        source = make_room("source")
        target = make_room("target", hostel=source.hostel)
        destination = make_room("new", hostel=source.hostel)
        student = make_student()
        actor = User.objects.create_user(username="moving-bed-warden", role="warden")
        original = allocate(student=student, bed=source.beds.first(), actor=actor)
        target_bed = target.beds.first()
        lock_rooms = Room.objects.select_for_update
        moved = False

        def move_free_target():
            close_old_connections()
            try:
                bed = Bed.objects.get(pk=target_bed.pk)
                bed.room_id = destination.pk
                bed.save(update_fields=["room"])
            finally:
                connections.close_all()

        def move_between_snapshot_and_locks(*args, **kwargs):
            nonlocal moved
            if not moved:
                moved = True
                with ThreadPoolExecutor(max_workers=1) as workers:
                    workers.submit(move_free_target).result(timeout=15)
            return lock_rooms(*args, **kwargs)

        with patch.object(
            Room.objects,
            "select_for_update",
            side_effect=move_between_snapshot_and_locks,
        ):
            with self.assertRaises(ValidationError) as error:
                transfer(allocation_id=original.pk, new_bed=target_bed, actor=actor)
        self.assertEqual(error.exception.code, "BED_MOVED")
        original.refresh_from_db()
        target_bed.refresh_from_db()
        self.assertEqual(original.status, Allocation.AllocationStatus.ACTIVE)
        self.assertEqual(target_bed.room_id, destination.pk)
        self.assertEqual(Allocation.objects.count(), 1)
        self.assertFalse(
            AuditEvent.objects.filter(action=AuditEvent.Action.TRANSFER).exists()
        )

    @skipUnlessDBFeature("has_select_for_update")
    def test_admission_finishes_while_hostel_editor_holds_only_hostel_lock(self):
        room = make_room("lock1")
        student = make_student()
        actor = User.objects.create_user(
            username="inventory-lock-warden", role=User.Role.WARDEN
        )
        bed = room.beds.first()

        def admit():
            close_old_connections()
            try:
                return allocate(student=student, bed=bed, actor=actor).pk
            finally:
                connections.close_all()

        blocked_on_hostel = False
        with ThreadPoolExecutor(max_workers=1) as workers:
            with transaction.atomic():
                # A real hostel edit takes this before locking its Rooms. The
                # admission already takes Room, so a joined Hostel lock would
                # create the opposite order and permit a deadlock.
                Hostel.objects.select_for_update().get(pk=room.hostel_id)
                future = workers.submit(admit)
                try:
                    allocation_id = future.result(timeout=5)
                except TimeoutError:
                    blocked_on_hostel = True
            # Always release the lock and join the worker, even on a regression.
            allocation_id = future.result(timeout=15)

        self.assertFalse(
            blocked_on_hostel,
            "Admission waits for Hostel while holding Room, inverting inventory locks.",
        )
        self.assertTrue(
            Allocation.objects.filter(
                pk=allocation_id, status=Allocation.AllocationStatus.ACTIVE
            ).exists()
        )


class AllocationPartialWriteTests(TestCase):
    def setUp(self):
        self.room = make_room()
        self.actor = User.objects.create_user(
            username="partial-save-warden", role="warden"
        )
        self.allocation = allocate(
            student=make_student(), bed=self.room.beds.first(), actor=self.actor
        )

    def finish_in_memory(self):
        self.allocation.status = Allocation.AllocationStatus.COMPLETED
        self.allocation.vacated_on = timezone.localdate()

    def test_positional_generator_partial_release_updates_derived_keys(self):
        self.finish_in_memory()
        self.allocation.save(False, False, None, iter(["status", "vacated_on"]))
        self.allocation.refresh_from_db()
        self.assertIsNone(self.allocation.active_bed_id)
        self.assertIsNone(self.allocation.active_student_id)
        self.assertEqual(self.allocation.status, Allocation.AllocationStatus.COMPLETED)
        self.assertEqual(
            Bed.objects.get(pk=self.allocation.bed_id).status, Bed.BedStatus.AVAILABLE
        )

    def test_empty_update_fields_is_a_complete_noop(self):
        self.finish_in_memory()
        self.allocation.save(update_fields=iter(()))
        self.allocation.refresh_from_db()
        self.assertEqual(self.allocation.status, Allocation.AllocationStatus.ACTIVE)
        self.assertEqual(self.allocation.active_bed_id, self.allocation.bed_id)
        self.assertEqual(
            Bed.objects.get(pk=self.allocation.bed_id).status, Bed.BedStatus.OCCUPIED
        )

    def test_excluded_dirty_status_cannot_desynchronize_bed_and_allocation(self):
        self.finish_in_memory()
        self.allocation.save(update_fields=["allocated_on"])
        self.allocation.refresh_from_db()
        self.assertEqual(self.allocation.status, Allocation.AllocationStatus.ACTIVE)
        self.assertIsNone(self.allocation.vacated_on)
        self.assertEqual(self.allocation.active_student_id, self.allocation.student_id)
        self.assertEqual(
            Bed.objects.get(pk=self.allocation.bed_id).status, Bed.BedStatus.OCCUPIED
        )

    def test_incomplete_partial_release_is_validation_error_not_integrity_error(self):
        self.finish_in_memory()
        with self.assertRaises(ValidationError):
            self.allocation.save(update_fields=["status"])
        self.allocation.refresh_from_db()
        self.assertEqual(self.allocation.status, Allocation.AllocationStatus.ACTIVE)
