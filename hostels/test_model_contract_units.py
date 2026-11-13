"""Additional room mutation contracts with database boundaries replaced."""

from decimal import Decimal
from unittest.mock import Mock, PropertyMock, call, patch

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from allocations.models import Allocation

from .models import Bed, Room


class RoomQuerySetContractUnitTests(SimpleTestCase):
    @patch("django.db.models.query.QuerySet.update", return_value=3)
    def test_unrelated_field_update_preserves_arguments_and_affected_count(
        self, update
    ):
        queryset = Room.objects.all()

        result = queryset.update(floor=2, fee_amount=Decimal("950.00"))

        self.assertEqual(result, 3)
        update.assert_called_once_with(floor=2, fee_amount=Decimal("950.00"))

    @patch("django.db.models.query.QuerySet.bulk_update", return_value=2)
    def test_fee_bulk_update_preserves_objects_fields_and_batch_size(self, bulk_update):
        rooms = [Room(pk=1), Room(pk=2)]
        fields = ("fee_amount",)

        result = Room.objects.all().bulk_update(rooms, fields, batch_size=10)

        self.assertEqual(result, 2)
        bulk_update.assert_called_once_with(rooms, fields, batch_size=10)


class RoomSaveContractUnitTests(SimpleTestCase):
    def setUp(self):
        self.room = Room(
            pk=8, room_number="201", capacity=2, fee_amount=Decimal("750.00")
        )
        self.beds = Mock()
        self.beds.count.return_value = 2
        descriptor = patch.object(
            Room, "beds", new_callable=PropertyMock, return_value=self.beds
        )
        descriptor.start()
        self.addCleanup(descriptor.stop)

    def test_missing_capacity_defers_allocation_checks_to_field_validation(self):
        self.room.capacity = None

        self.room.clean()

        self.beds.filter.assert_not_called()

    @patch("hostels.models.Bed.objects.get_or_create")
    @patch("django.db.models.Model.save", return_value=None)
    @patch("hostels.models.Room.objects.select_for_update")
    def test_fee_strings_become_decimals_and_save_arguments_are_preserved(
        self, locked, save, create
    ):
        self.room.pk = None
        self.room.fee_amount = "0.00"
        self.beds.count.return_value = 0

        Room.save.__wrapped__(self.room, force_insert=True, using="default")

        self.assertIsInstance(self.room.fee_amount, Decimal)
        self.assertEqual(self.room.fee_amount, Decimal("0.00"))
        save.assert_called_once_with(force_insert=True, using="default")
        locked.assert_not_called()
        self.assertEqual(create.call_count, 2)

    @patch("hostels.models.Bed.objects.get_or_create")
    @patch("django.db.models.Model.save", return_value=None)
    @patch("hostels.models.Room.objects.select_for_update")
    def test_invalid_fees_fail_before_locks_writes_or_bed_changes(
        self, locked, save, create
    ):
        for fee in ("-0.01", "not-a-price", "NaN", "1.001", "100000000.00"):
            with self.subTest(fee=fee):
                self.room.fee_amount = fee

                with self.assertRaises(ValidationError):
                    Room.save.__wrapped__(self.room)

        locked.assert_not_called()
        save.assert_not_called()
        create.assert_not_called()
        self.assertEqual(self.beds.mock_calls, [])

    @patch("hostels.models.Bed.objects.get_or_create")
    @patch("django.db.models.Model.save", return_value=None)
    @patch("hostels.models.Room.objects.select_for_update")
    def test_unchanged_number_preserves_existing_bed_labels_and_statuses(
        self, locked, save, create
    ):
        locked.return_value.get.return_value = Room(room_number="201", capacity=2)
        maintenance = Bed(label="201-A", status=Bed.BedStatus.MAINTENANCE)
        occupied = Bed(label="201-B", status=Bed.BedStatus.OCCUPIED)
        create.side_effect = [(maintenance, False), (occupied, False)]

        Room.save.__wrapped__(self.room)

        locked.return_value.get.assert_called_once_with(pk=8)
        self.beds.select_for_update.assert_not_called()
        self.beds.exclude.assert_not_called()
        self.assertEqual(
            [(bed.label, bed.status) for bed in (maintenance, occupied)],
            [
                ("201-A", Bed.BedStatus.MAINTENANCE),
                ("201-B", Bed.BedStatus.OCCUPIED),
            ],
        )
        self.assertEqual(
            create.call_args_list,
            [
                call(
                    room=self.room,
                    label=f"201-{suffix}",
                    defaults={"status": Bed.BedStatus.AVAILABLE},
                )
                for suffix in ("A", "B")
            ],
        )
        save.assert_called_once_with()

    @patch("hostels.models.Bed.objects.get_or_create")
    @patch("django.db.models.Model.save", return_value=None)
    @patch("hostels.models.Room.objects.select_for_update")
    def test_historical_beds_can_remain_beyond_capacity_when_active_beds_fit(
        self, locked, save, create
    ):
        locked.return_value.get.return_value = Room(room_number="201")
        self.beds.count.return_value = 3
        self.beds.exclude.return_value.order_by.return_value.distinct.return_value = []
        self.beds.filter.return_value.distinct.return_value.count.return_value = 2

        Room.save.__wrapped__(self.room)

        self.beds.exclude.assert_called_once_with(allocations__isnull=False)
        self.beds.filter.assert_called_once_with(
            allocations__status=Allocation.AllocationStatus.ACTIVE
        )
        self.assertEqual(
            create.call_args_list,
            [
                call(
                    room=self.room,
                    label=f"201-{suffix}",
                    defaults={"status": Bed.BedStatus.AVAILABLE},
                )
                for suffix in ("A", "B")
            ],
        )
        save.assert_called_once()

    @patch("hostels.models.Bed.objects.get_or_create")
    @patch("django.db.models.Model.save", return_value=None)
    @patch("hostels.models.Room.objects.select_for_update")
    def test_save_rejects_capacity_below_active_beds_even_without_clean(
        self, locked, save, create
    ):
        locked.return_value.get.return_value = Room(room_number="201")
        self.beds.count.return_value = 3
        self.beds.exclude.return_value.order_by.return_value.distinct.return_value = []
        self.beds.filter.return_value.distinct.return_value.count.return_value = 3

        with self.assertRaisesMessage(
            ValidationError,
            "Capacity cannot be reduced below the number of beds with active allocations.",
        ):
            Room.save.__wrapped__(self.room)

        self.beds.filter.assert_called_once_with(
            allocations__status=Allocation.AllocationStatus.ACTIVE
        )

    @patch("hostels.models.Bed.objects.get_or_create")
    @patch("django.db.models.Model.save", side_effect=RuntimeError("write failed"))
    @patch("hostels.models.Room.objects.select_for_update")
    def test_room_write_failure_stops_bed_synchronization(self, locked, save, create):
        locked.return_value.get.return_value = Room(room_number="OLD")

        with self.assertRaisesMessage(RuntimeError, "write failed"):
            Room.save.__wrapped__(self.room)

        self.assertEqual(self.beds.mock_calls, [])
        create.assert_not_called()


class RoomPartialSaveContractUnitTests(SimpleTestCase):
    def setUp(self):
        self.room = Room(
            pk=8, room_number="201", capacity=2, fee_amount=Decimal("750.00")
        )
        self.beds = Mock()
        self.beds.count.return_value = 2
        self.previous = Room(
            pk=8, room_number="201", capacity=2, fee_amount=Decimal("750.00")
        )
        self.locked = self.enterContext(
            patch("hostels.models.Room.objects.select_for_update")
        )
        self.locked.return_value.get.return_value = self.previous
        self.persist = self.enterContext(
            patch("django.db.models.Model.save", return_value=None)
        )
        self.create = self.enterContext(
            patch("hostels.models.Bed.objects.get_or_create")
        )
        self.enterContext(
            patch.object(
                Room, "beds", new_callable=PropertyMock, return_value=self.beds
            )
        )

    def test_fee_only_save_does_not_sync_excluded_number_or_capacity(self):
        self.room.room_number = "UNSAVED"
        self.room.capacity = 4
        self.room.fee_amount = "950.00"
        existing = Mock(label="201-A")
        self.beds.select_for_update.return_value.all.return_value = [existing]

        Room.save.__wrapped__(self.room, update_fields=["fee_amount"])

        self.assertEqual(self.room.fee_amount, Decimal("950.00"))
        self.assertEqual(self.beds.mock_calls, [])
        self.create.assert_not_called()
        self.assertEqual(existing.label, "201-A")
        existing.save.assert_not_called()
        self.assertEqual((self.room.room_number, self.room.capacity), ("UNSAVED", 4))
        self.assertEqual(
            set(self.persist.call_args.kwargs["update_fields"]), {"fee_amount"}
        )

    def test_invalid_excluded_fee_does_not_block_floor_update(self):
        self.room.floor = 3
        self.room.fee_amount = "invalid-unsaved-fee"

        Room.save.__wrapped__(self.room, update_fields=["floor"])

        self.assertEqual(self.room.fee_amount, "invalid-unsaved-fee")
        self.assertEqual(set(self.persist.call_args.kwargs["update_fields"]), {"floor"})
        self.assertEqual(self.beds.mock_calls, [])
        self.create.assert_not_called()

    def test_number_only_save_uses_locked_capacity_and_accepts_field_generators(self):
        for fields in (["room_number"], iter(["room_number"])):
            with self.subTest(fields_type=type(fields).__name__):
                self.beds.reset_mock()
                self.create.reset_mock()
                self.persist.reset_mock()
                self.room.room_number = "202"
                self.room.capacity = 4
                bed = Mock(label="201-A")
                self.beds.select_for_update.return_value.all.return_value = [bed]

                Room.save.__wrapped__(self.room, update_fields=fields)

                self.assertEqual(bed.label, "202-A")
                bed.save.assert_called_once_with(update_fields=["label"])
                self.assertEqual(
                    [entry.kwargs["label"] for entry in self.create.call_args_list],
                    ["202-A", "202-B"],
                )
                self.assertEqual(self.room.capacity, 4)
                self.assertEqual(
                    set(self.persist.call_args.kwargs["update_fields"]), {"room_number"}
                )

    def test_capacity_only_save_uses_locked_number_including_positional_save_api(self):
        for positional in (False, True):
            with self.subTest(positional=positional):
                self.beds.reset_mock()
                self.create.reset_mock()
                self.persist.reset_mock()
                self.room.room_number = "UNSAVED"
                self.room.capacity = 3
                self.beds.select_for_update.return_value.all.return_value = []

                if positional:
                    Room.save.__wrapped__(self.room, False, False, None, ["capacity"])
                    saved_fields = self.persist.call_args.args[3]
                else:
                    Room.save.__wrapped__(self.room, update_fields=["capacity"])
                    saved_fields = self.persist.call_args.kwargs["update_fields"]

                self.assertEqual(set(saved_fields), {"capacity"})
                self.beds.select_for_update.assert_not_called()
                self.assertEqual(
                    [entry.kwargs["label"] for entry in self.create.call_args_list],
                    ["201-A", "201-B", "201-C"],
                )
                self.assertEqual(self.room.room_number, "UNSAVED")

    def test_including_both_sync_fields_uses_both_new_values(self):
        self.room.room_number = "202"
        self.room.capacity = 3
        bed = Mock(label="201-A")
        self.beds.select_for_update.return_value.all.return_value = [bed]

        Room.save.__wrapped__(self.room, update_fields=["room_number", "capacity"])

        self.assertEqual(bed.label, "202-A")
        self.assertEqual(
            [entry.kwargs["label"] for entry in self.create.call_args_list],
            ["202-A", "202-B", "202-C"],
        )

    def test_empty_update_fields_skip_validation_locks_and_all_writes(self):
        for fields in ([], iter([])):
            with self.subTest(fields_type=type(fields).__name__):
                self.room.room_number = "UNSAVED"
                self.room.capacity = 4
                self.room.fee_amount = "invalid-unsaved-fee"

                Room.save.__wrapped__(self.room, update_fields=fields)

                self.locked.assert_not_called()
                self.persist.assert_not_called()
                self.assertEqual(self.beds.mock_calls, [])
                self.create.assert_not_called()

    def test_invalid_included_fee_still_fails_before_any_writes(self):
        self.room.fee_amount = "-0.01"

        with self.assertRaises(ValidationError):
            Room.save.__wrapped__(self.room, update_fields=["fee_amount"])

        self.locked.assert_not_called()
        self.persist.assert_not_called()
        self.assertEqual(self.beds.mock_calls, [])
        self.create.assert_not_called()
