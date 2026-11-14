"""Allocation eligibility decisions with persistence boundaries replaced by fakes.

These tests exercise the save body without its transaction wrapper. Database
locking, constraints and rollback remain the responsibility of integration tests.
"""

from datetime import date
from unittest.mock import call, patch

from django.core.exceptions import ValidationError
from django.db import models
from django.test import SimpleTestCase

from hostels.models import Bed, Hostel, Room
from students.models import Student

from .models import Allocation


class AllocationSaveDecisionUnitTests(SimpleTestCase):
    def setUp(self):
        self.student = Student(
            pk=11, status=Student.Status.ACTIVE, gender=Student.Gender.MALE
        )
        self.hostel = Hostel(pk=3, hostel_type=Hostel.HostelType.BOYS, is_active=True)
        self.room = Room(pk=4, hostel=self.hostel, capacity=2)
        self.bed = Bed(pk=5, room=self.room, status=Bed.BedStatus.AVAILABLE)
        self.allocation = Allocation(
            student_id=11, bed_id=5, allocated_on=date(2026, 11, 1)
        )

        patches = {
            "students": patch.object(Student.objects, "select_for_update"),
            "bed_room": patch.object(Bed.objects, "values_list"),
            "rooms": patch.object(Room.objects, "select_for_update"),
            "beds": patch.object(Bed.objects, "select_for_update"),
            "existing": patch.object(Allocation.objects, "filter"),
            "previous": patch.object(Allocation.objects, "select_for_update"),
            "clean": patch.object(self.allocation, "full_clean"),
            "save": patch.object(models.Model, "save", return_value=None),
            "bed_save": patch.object(self.bed, "save"),
        }
        self.mocks = {name: item.start() for name, item in patches.items()}
        for item in patches.values():
            self.addCleanup(item.stop)
        self.mocks["students"].return_value.get.return_value = self.student
        self.mocks["bed_room"].return_value.get.return_value = self.room.pk
        self.mocks["rooms"].return_value.get.return_value = self.room
        self.mocks[
            "beds"
        ].return_value.select_related.return_value.get.return_value = self.bed
        self.mocks[
            "existing"
        ].return_value.exclude.return_value.exists.return_value = False
        self.mocks["existing"].return_value.exclude.return_value.count.return_value = 0

    def save_body(self, **kwargs):
        return Allocation.save.__wrapped__(self.allocation, **kwargs)

    def test_new_allocation_sets_keys_and_marks_bed_occupied(self):
        self.save_body()
        self.assertEqual(
            (self.allocation.active_student_id, self.allocation.active_bed_id), (11, 5)
        )
        self.assertEqual(self.bed.status, Bed.BedStatus.OCCUPIED)
        self.mocks["clean"].assert_called_once()
        self.assertTrue(self.mocks["save"].call_args.kwargs["force_insert"])
        self.mocks["bed_save"].assert_called_once_with(update_fields=["status"])

    def test_inactive_student_is_rejected_before_save(self):
        self.student.status = Student.Status.INACTIVE
        with self.assertRaises(ValidationError) as error:
            self.save_body()
        self.assertEqual(error.exception.code, "INACTIVE_STUDENT")
        self.mocks["save"].assert_not_called()

    def test_inactive_hostel_and_gender_mismatch_are_rejected(self):
        for active, hostel_type, expected in (
            (False, Hostel.HostelType.BOYS, "INACTIVE_HOSTEL"),
            (True, Hostel.HostelType.GIRLS, "GENDER_MISMATCH"),
        ):
            with self.subTest(expected=expected):
                self.hostel.is_active, self.hostel.hostel_type = active, hostel_type
                with self.assertRaises(ValidationError) as error:
                    self.save_body()
                self.assertEqual(error.exception.code, expected)
        self.mocks["save"].assert_not_called()

    def test_existing_student_or_bed_allocation_is_rejected(self):
        for existing, expected in (
            ([True], "ALREADY_ALLOCATED"),
            ([False, True], "BED_OCCUPIED"),
        ):
            with self.subTest(expected=expected):
                self.mocks[
                    "existing"
                ].return_value.exclude.return_value.exists.side_effect = existing
                with self.assertRaises(ValidationError) as error:
                    self.save_body()
                self.assertEqual(error.exception.code, expected)
        self.mocks["save"].assert_not_called()

    def test_maintenance_bed_cannot_receive_new_allocation(self):
        self.bed.status = Bed.BedStatus.MAINTENANCE
        with self.assertRaises(ValidationError) as error:
            self.save_body()
        self.assertEqual(error.exception.code, "BED_OCCUPIED")
        self.mocks["save"].assert_not_called()

    def test_missing_student_maps_to_not_found(self):
        self.mocks["students"].return_value.get.side_effect = Student.DoesNotExist
        with self.assertRaises(ValidationError) as error:
            self.save_body()
        self.assertEqual(error.exception.code, "NOT_FOUND")
        self.mocks["save"].assert_not_called()

    def test_existing_allocation_history_is_immutable(self):
        self.allocation.pk = 20
        self.allocation._state.adding = False
        previous = Allocation(
            pk=20, student_id=11, bed_id=99, allocated_on=date(2026, 11, 1)
        )
        self.mocks["previous"].return_value.get.return_value = previous
        with self.assertRaises(ValidationError) as error:
            self.save_body()
        self.assertEqual(error.exception.code, "IMMUTABLE_FIELD")
        self.mocks["save"].assert_not_called()

    def test_release_clears_active_keys_and_frees_occupied_bed(self):
        self.allocation.pk = 20
        self.allocation._state.adding = False
        self.allocation.status = Allocation.AllocationStatus.COMPLETED
        previous = Allocation(
            pk=20,
            student_id=11,
            bed_id=5,
            allocated_on=date(2026, 11, 1),
            status=Allocation.AllocationStatus.ACTIVE,
        )
        self.mocks["previous"].return_value.get.return_value = previous
        self.bed.status = Bed.BedStatus.OCCUPIED
        self.save_body(update_fields=["status"])
        self.assertIsNone(self.allocation.active_student_id)
        self.assertIsNone(self.allocation.active_bed_id)
        self.assertEqual(self.bed.status, Bed.BedStatus.AVAILABLE)
        self.assertEqual(
            self.mocks["save"].call_args.kwargs["update_fields"],
            {"status", "active_student_id", "active_bed_id"},
        )

    def test_full_room_uses_locked_capacity_instead_of_cached_bed_room_capacity(self):
        self.room.capacity = 4
        locked_room = Room(pk=4, hostel=self.hostel, capacity=1)
        self.mocks["rooms"].return_value.get.return_value = locked_room
        self.mocks["existing"].return_value.exclude.return_value.count.return_value = 1

        with self.assertRaises(ValidationError) as error:
            self.save_body()

        self.assertEqual(error.exception.code, "ROOM_FULL")
        self.mocks["rooms"].return_value.get.assert_called_once_with(pk=4)
        self.mocks["existing"].assert_called_with(
            bed__room_id=locked_room.pk, status=Allocation.AllocationStatus.ACTIVE
        )
        self.mocks["clean"].assert_not_called()
        self.mocks["save"].assert_not_called()
        self.mocks["bed_save"].assert_not_called()
        self.assertEqual(self.bed.status, Bed.BedStatus.AVAILABLE)

    def test_bed_moved_to_another_room_after_lookup_is_rejected_before_writes(self):
        self.bed.room = Room(pk=9, hostel=self.hostel, capacity=2)

        with self.assertRaises(ValidationError) as error:
            self.save_body()

        self.assertEqual(error.exception.code, "BED_MOVED")
        self.mocks["rooms"].return_value.get.assert_called_once_with(pk=4)
        self.mocks["existing"].assert_not_called()
        self.mocks["clean"].assert_not_called()
        self.mocks["save"].assert_not_called()
        self.mocks["bed_save"].assert_not_called()
        self.assertEqual(self.bed.status, Bed.BedStatus.AVAILABLE)

    def test_last_room_capacity_slot_is_admitted(self):
        self.mocks["existing"].return_value.exclude.return_value.count.return_value = 1

        self.save_body()

        self.mocks["existing"].assert_called_with(
            bed__room_id=4, status=Allocation.AllocationStatus.ACTIVE
        )
        self.mocks["existing"].return_value.exclude.assert_called_with(pk=None)
        self.mocks[
            "existing"
        ].return_value.exclude.return_value.count.assert_called_once_with()
        self.assertEqual(self.bed.status, Bed.BedStatus.OCCUPIED)
        self.mocks["clean"].assert_called_once()
        self.mocks["save"].assert_called_once_with(force_insert=True)
        self.mocks["bed_save"].assert_called_once_with(update_fields=["status"])

    def test_existing_active_allocation_is_excluded_from_room_capacity_count(self):
        self.allocation.pk = 20
        self.allocation._state.adding = False
        self.room.capacity = 1
        self.mocks["previous"].return_value.get.return_value = Allocation(
            pk=20, student_id=11, bed_id=5, allocated_on=date(2026, 11, 1)
        )
        self.bed.status = Bed.BedStatus.OCCUPIED

        self.save_body(update_fields=["status"])

        self.assertEqual(
            self.mocks["existing"].call_args_list[-1],
            call(bed__room_id=4, status=Allocation.AllocationStatus.ACTIVE),
        )
        self.mocks["existing"].return_value.exclude.assert_called_with(pk=20)
        self.mocks[
            "existing"
        ].return_value.exclude.return_value.count.assert_called_once_with()
        self.mocks["save"].assert_called_once_with(
            update_fields={"status", "active_student_id", "active_bed_id"}
        )

    def test_release_skips_capacity_guard_even_when_room_count_is_at_limit(self):
        self.allocation.pk = 20
        self.allocation._state.adding = False
        self.allocation.status = Allocation.AllocationStatus.COMPLETED
        self.allocation.vacated_on = date(2026, 11, 2)
        self.room.capacity = 1
        self.mocks["existing"].return_value.exclude.return_value.count.return_value = 1
        self.mocks["previous"].return_value.get.return_value = Allocation(
            pk=20, student_id=11, bed_id=5, allocated_on=date(2026, 11, 1)
        )
        self.bed.status = Bed.BedStatus.OCCUPIED

        self.save_body(update_fields=["status", "vacated_on"])

        self.mocks["existing"].assert_not_called()
        self.mocks["save"].assert_called_once_with(
            update_fields={"status", "vacated_on", "active_student_id", "active_bed_id"}
        )
        self.mocks["bed_save"].assert_called_once_with(update_fields=["status"])
        self.assertIsNone(self.allocation.active_student_id)
        self.assertIsNone(self.allocation.active_bed_id)
        self.assertEqual(self.bed.status, Bed.BedStatus.AVAILABLE)
