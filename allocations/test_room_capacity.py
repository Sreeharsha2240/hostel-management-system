"""Capacity regressions when a room retains beds with allocation history."""

from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db import close_old_connections, connections
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from audit.models import AuditEvent
from hostels.models import Bed, Room
from tests.factories import make_room, make_student

from .models import Allocation
from .services import allocate, release, transfer
from .views import available_beds


def _make_room_with_retained_beds(
    *, actor, historical_student, number="101", hostel=None, historical_suffixes=("B",)
):
    room = make_room(number, hostel=hostel)
    today = timezone.localdate()
    for index, suffix in enumerate(historical_suffixes):
        historical = allocate(
            student=historical_student,
            bed=room.beds.get(label=f"{number}-{suffix}"),
            actor=actor,
            allocated_on=today - timedelta(days=10 - index * 2),
        )
        release(
            allocation_id=historical.pk,
            actor=actor,
            vacate_date=today - timedelta(days=9 - index * 2),
        )

    # A valid reduction keeps beds with history and regenerates A if needed.
    room.capacity = 1
    room.room_type = "Single"
    room.full_clean()
    room.save(update_fields=["capacity", "room_type"])
    return room


class AllocationRoomCapacityTests(TestCase):
    def setUp(self):
        self.actor = User.objects.create_user(
            username="capacity-warden", role=User.Role.WARDEN
        )
        self.historical_student = make_student()
        self.resident = make_student(2)
        self.incoming = make_student(3)
        self.today = timezone.localdate()
        self.room = _make_room_with_retained_beds(
            actor=self.actor,
            historical_student=self.historical_student,
        )
        self.bed = self.room.beds.get(label="101-A")
        self.historical_bed = self.room.beds.get(label="101-B")
        self.assertEqual(self.room.beds.count(), 2)
        self.assertEqual(
            {self.bed.status, self.historical_bed.status},
            {Bed.BedStatus.AVAILABLE},
        )

    def active_room_count(self):
        return Allocation.objects.filter(
            bed__room=self.room, status=Allocation.AllocationStatus.ACTIVE
        ).count()

    def other_full_room(self):
        room = _make_room_with_retained_beds(
            actor=self.actor,
            historical_student=make_student(4),
            number="202",
            hostel=self.room.hostel,
        )
        allocate(
            student=self.incoming,
            bed=room.beds.get(label="202-A"),
            actor=self.actor,
        )
        return room

    def snapshot(self):
        return {
            "allocations": list(
                Allocation.objects.order_by("pk").values_list(
                    "pk",
                    "student_id",
                    "bed_id",
                    "allocated_on",
                    "vacated_on",
                    "status",
                    "active_student_id",
                    "active_bed_id",
                )
            ),
            "beds": list(
                Bed.objects.order_by("pk").values_list("pk", "room_id", "status")
            ),
            "audit": list(
                AuditEvent.objects.order_by("pk").values_list(
                    "pk", "user_id", "action", "record_type", "record_id"
                )
            ),
        }

    def test_direct_save_rejects_available_historical_bed_when_room_is_full(self):
        allocate(student=self.resident, bed=self.bed, actor=self.actor)
        before = self.snapshot()
        candidate = Allocation(student=self.incoming, bed=self.historical_bed)

        with self.assertRaises(ValidationError) as error:
            candidate.save()

        self.assertEqual(error.exception.code, "ROOM_FULL")
        self.assertIsNone(candidate.pk)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.active_room_count(), self.room.capacity)

    def test_service_rejects_regenerated_bed_when_historical_bed_fills_room(self):
        allocate(student=self.resident, bed=self.historical_bed, actor=self.actor)
        before = self.snapshot()

        with self.assertRaises(ValidationError) as error:
            allocate(student=self.incoming, bed=self.bed, actor=self.actor)

        self.assertEqual(error.exception.code, "ROOM_FULL")
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.active_room_count(), self.room.capacity)

    def test_json_create_returns_room_full_conflict_without_changing_state(self):
        allocate(student=self.resident, bed=self.bed, actor=self.actor)
        self.client.force_login(self.actor)
        before = self.snapshot()

        response = self.client.post(
            reverse("allocation-list"),
            {
                "student_id": self.incoming.student_id,
                "bed_id": self.historical_bed.pk,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["error"]["code"], "ROOM_FULL")
        self.assertEqual(self.snapshot(), before)

    def test_json_transfer_returns_room_full_conflict_and_rolls_back(self):
        allocate(student=self.resident, bed=self.bed, actor=self.actor)
        source_bed = make_room(
            "202", hostel=self.room.hostel, room_type="Single", capacity=1
        ).beds.get()
        original = allocate(student=self.incoming, bed=source_bed, actor=self.actor)
        self.client.force_login(self.actor)
        before = self.snapshot()

        response = self.client.post(
            reverse("allocation-transfer", args=[original.pk]),
            {"new_bed_id": self.historical_bed.pk},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["error"]["code"], "ROOM_FULL")
        self.assertEqual(self.snapshot(), before)

    def test_controlled_bed_move_after_room_lock_is_rejected_and_rolled_back(self):
        target = make_room(
            "202", hostel=self.room.hostel, room_type="Single", capacity=1
        )
        allocate(student=self.resident, bed=target.beds.get(), actor=self.actor)
        before = self.snapshot()
        candidate = Allocation(student=self.incoming, bed=self.historical_bed)
        locked_rooms = Room.objects.select_for_update()
        get_locked_room = locked_rooms.get
        moved_to = []

        def move_bed_after_lock(*args, **kwargs):
            locked_room = get_locked_room(*args, **kwargs)
            self.assertEqual(locked_room.pk, self.room.pk)
            # Control the gap between the room lookup and locked bed load.
            moved_bed = Bed.objects.get(pk=self.historical_bed.pk)
            moved_bed.room = target
            moved_bed.save(update_fields=["room"])
            moved_to.append(moved_bed.room_id)
            return locked_room

        with (
            patch.object(Room.objects, "select_for_update", return_value=locked_rooms),
            patch.object(locked_rooms, "get", side_effect=move_bed_after_lock),
            self.assertRaises(ValidationError) as error,
        ):
            candidate.save()

        self.assertEqual(moved_to, [target.pk])
        self.assertEqual(error.exception.code, "BED_MOVED")
        self.assertIsNone(candidate.pk)
        self.assertEqual(self.snapshot(), before)
        self.historical_bed.refresh_from_db()
        self.assertEqual(self.historical_bed.room_id, self.room.pk)
        self.assertEqual(self.historical_bed.status, Bed.BedStatus.AVAILABLE)

    def test_transfer_to_full_room_rolls_back_original_beds_and_audit(self):
        allocate(student=self.resident, bed=self.bed, actor=self.actor)
        source_bed = make_room(
            "202", hostel=self.room.hostel, room_type="Single", capacity=1
        ).beds.get()
        original = allocate(student=self.incoming, bed=source_bed, actor=self.actor)
        before = self.snapshot()

        with self.assertRaises(ValidationError) as error:
            transfer(
                allocation_id=original.pk,
                new_bed=self.historical_bed,
                actor=self.actor,
            )

        self.assertEqual(error.exception.code, "ROOM_FULL")
        self.assertEqual(self.snapshot(), before)
        original.refresh_from_db()
        self.assertEqual(original.status, Allocation.AllocationStatus.ACTIVE)
        self.assertIsNone(original.vacated_on)
        self.assertEqual(self.active_room_count(), self.room.capacity)

    def test_same_room_transfer_succeeds_at_capacity(self):
        original = allocate(student=self.resident, bed=self.bed, actor=self.actor)
        before_audits = AuditEvent.objects.count()
        self.assertEqual(self.active_room_count(), self.room.capacity)

        successor = transfer(
            allocation_id=original.pk,
            new_bed=self.historical_bed,
            actor=self.actor,
        )

        original.refresh_from_db()
        self.bed.refresh_from_db()
        self.historical_bed.refresh_from_db()
        self.assertEqual(original.status, Allocation.AllocationStatus.COMPLETED)
        self.assertEqual(original.vacated_on, self.today)
        self.assertNotEqual(successor.pk, original.pk)
        self.assertEqual(successor.student_id, self.resident.pk)
        self.assertEqual(successor.bed_id, self.historical_bed.pk)
        self.assertEqual(successor.status, Allocation.AllocationStatus.ACTIVE)
        self.assertEqual(self.bed.status, Bed.BedStatus.AVAILABLE)
        self.assertEqual(self.historical_bed.status, Bed.BedStatus.OCCUPIED)
        self.assertEqual(self.active_room_count(), self.room.capacity)
        self.assertEqual(AuditEvent.objects.count(), before_audits + 1)
        event = AuditEvent.objects.get(action=AuditEvent.Action.TRANSFER)
        self.assertEqual(
            (event.user_id, event.record_type, event.record_id),
            (self.actor.pk, "allocations.allocation", str(successor.pk)),
        )

    def test_backdated_release_frees_capacity_for_a_backdated_allocation(self):
        original = allocate(
            student=self.resident,
            bed=self.bed,
            actor=self.actor,
            allocated_on=self.today - timedelta(days=4),
        )
        vacate_date = self.today - timedelta(days=2)

        released = release(
            allocation_id=original.pk, actor=self.actor, vacate_date=vacate_date
        )
        self.assertEqual(self.active_room_count(), 0)
        successor = allocate(
            student=self.incoming,
            bed=self.historical_bed,
            actor=self.actor,
            allocated_on=self.today - timedelta(days=1),
        )

        self.bed.refresh_from_db()
        self.historical_bed.refresh_from_db()
        self.assertEqual(released.status, Allocation.AllocationStatus.COMPLETED)
        self.assertEqual(released.vacated_on, vacate_date)
        self.assertIsNone(released.active_student_id)
        self.assertIsNone(released.active_bed_id)
        self.assertEqual(successor.allocated_on, self.today - timedelta(days=1))
        self.assertEqual(self.bed.status, Bed.BedStatus.AVAILABLE)
        self.assertEqual(self.historical_bed.status, Bed.BedStatus.OCCUPIED)
        self.assertEqual(self.active_room_count(), self.room.capacity)

    def test_completed_backdated_history_can_be_saved_while_room_is_full(self):
        current = allocate(student=self.resident, bed=self.bed, actor=self.actor)
        before_audits = AuditEvent.objects.count()

        historical = Allocation.objects.create(
            student=self.incoming,
            bed=self.historical_bed,
            allocated_on=self.today - timedelta(days=7),
            vacated_on=self.today - timedelta(days=6),
            status=Allocation.AllocationStatus.COMPLETED,
        )

        current.refresh_from_db()
        self.bed.refresh_from_db()
        self.historical_bed.refresh_from_db()
        self.assertIsNone(historical.active_student_id)
        self.assertIsNone(historical.active_bed_id)
        self.assertEqual(current.status, Allocation.AllocationStatus.ACTIVE)
        self.assertEqual(self.bed.status, Bed.BedStatus.OCCUPIED)
        self.assertEqual(self.historical_bed.status, Bed.BedStatus.AVAILABLE)
        self.assertEqual(self.active_room_count(), self.room.capacity)
        self.assertEqual(AuditEvent.objects.count(), before_audits)

    def test_saving_existing_active_allocation_does_not_count_it_twice(self):
        current = allocate(student=self.resident, bed=self.bed, actor=self.actor)
        before = self.snapshot()

        current.save(update_fields=["status"])

        current.refresh_from_db()
        self.assertEqual(current.active_student_id, self.resident.pk)
        self.assertEqual(current.active_bed_id, self.bed.pk)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.active_room_count(), self.room.capacity)

    def test_available_beds_hide_full_rooms_but_keep_underfull_candidates(self):
        self.assertEqual(
            set(available_beds().values_list("pk", flat=True)),
            {self.bed.pk, self.historical_bed.pk},
        )
        allocate(student=self.resident, bed=self.bed, actor=self.actor)
        underfull = make_room("202", hostel=self.room.hostel)
        occupied, available = underfull.beds.all()
        allocate(student=self.incoming, bed=occupied, actor=self.actor)

        self.assertEqual(
            set(available_beds().values_list("pk", flat=True)), {available.pk}
        )

    def test_available_beds_discount_only_the_transfer_source_allocation(self):
        original = allocate(student=self.resident, bed=self.bed, actor=self.actor)
        self.other_full_room()
        self.assertFalse(available_beds().exists())

        candidates = available_beds(exclude_allocation_id=original.pk)

        self.assertEqual(
            set(candidates.values_list("pk", flat=True)), {self.historical_bed.pk}
        )

    def test_create_form_hides_full_rooms_but_retains_underfull_beds(self):
        allocate(student=self.resident, bed=self.bed, actor=self.actor)
        underfull = make_room("202", hostel=self.room.hostel)
        occupied, available = underfull.beds.all()
        allocate(student=self.incoming, bed=occupied, actor=self.actor)
        self.client.force_login(self.actor)
        before = self.snapshot()

        response = self.client.get(reverse("allocation-create"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(
                response.context["form"]
                .fields["bed"]
                .queryset.values_list("pk", flat=True)
            ),
            {available.pk},
        )
        self.assertEqual(self.snapshot(), before)

    def test_transfer_form_allows_same_room_but_hides_other_full_rooms(self):
        original = allocate(student=self.resident, bed=self.bed, actor=self.actor)
        self.other_full_room()
        underfull = make_room("303", hostel=self.room.hostel)
        occupied, available = underfull.beds.all()
        allocate(student=make_student(5), bed=occupied, actor=self.actor)
        self.client.force_login(self.actor)
        before = self.snapshot()

        response = self.client.get(reverse("allocation-transfer", args=[original.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(
                response.context["form"]
                .fields["new_bed"]
                .queryset.values_list("pk", flat=True)
            ),
            {self.historical_bed.pk, available.pk},
        )
        self.assertEqual(self.snapshot(), before)


class AllocationRoomCapacityConcurrencyTests(TransactionTestCase):
    def setUp(self):
        self.actor = User.objects.create_user(
            username="capacity-concurrent-warden", role=User.Role.WARDEN
        )
        self.room = _make_room_with_retained_beds(
            actor=self.actor,
            historical_student=make_student(),
            historical_suffixes=("A", "B"),
        )
        self.students = [make_student(2), make_student(3)]
        self.beds = list(self.room.beds.all())
        self.assertEqual(len(self.beds), 2)
        self.assertTrue(all(bed.status == Bed.BedStatus.AVAILABLE for bed in self.beds))

    def test_two_students_racing_for_different_beds_cannot_exceed_capacity(self):
        barrier = Barrier(2, timeout=20)
        before_audits = AuditEvent.objects.count()

        def attempt(pair):
            close_old_connections()
            try:
                student, bed = pair
                barrier.wait()
                allocate(student=student, bed=bed, actor=self.actor)
                return "ok"
            except ValidationError as error:
                return error.code
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(
                pool.map(attempt, zip(self.students, self.beds, strict=True))
            )

        self.assertCountEqual(outcomes, ["ok", "ROOM_FULL"])
        active = Allocation.objects.filter(
            bed__room=self.room, status=Allocation.AllocationStatus.ACTIVE
        )
        self.assertEqual(active.count(), self.room.capacity)
        self.assertIn(
            active.get().student_id, {student.pk for student in self.students}
        )
        self.assertEqual(
            self.room.beds.filter(status=Bed.BedStatus.OCCUPIED).count(), 1
        )
        self.assertEqual(
            self.room.beds.filter(status=Bed.BedStatus.AVAILABLE).count(), 1
        )
        self.assertEqual(AuditEvent.objects.count(), before_audits + 1)
