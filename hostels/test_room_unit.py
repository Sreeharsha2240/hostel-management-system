"""Room capacity and bed-synchronization decisions with persistence mocked."""

from decimal import Decimal
from unittest.mock import Mock, PropertyMock, call, patch

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from .models import Bed, Hostel, Room


class RoomDecisionUnitTests(SimpleTestCase):
    def setUp(self):
        self.hostel = Hostel(pk=1, name="Test", hostel_type=Hostel.HostelType.BOYS)
        self.room = Room(
            pk=2,
            hostel=self.hostel,
            room_number="101",
            capacity=2,
            fee_amount=Decimal("1000"),
        )
        self.beds = Mock()
        descriptor = patch.object(
            Room, "beds", new_callable=PropertyMock, return_value=self.beds
        )
        descriptor.start()
        self.addCleanup(descriptor.stop)

    def test_clean_rejects_capacity_outside_one_to_four(self):
        for capacity in (0, 5):
            with self.subTest(capacity=capacity):
                self.room.capacity = capacity
                with self.assertRaises(ValidationError) as error:
                    self.room.clean()
                self.assertIn("capacity", error.exception.message_dict)

    def test_clean_rejects_reduction_below_active_allocations(self):
        self.beds.filter.return_value.distinct.return_value.count.return_value = 3
        with self.assertRaises(ValidationError) as error:
            self.room.clean()
        self.assertIn("capacity", error.exception.message_dict)
        self.beds.filter.return_value.distinct.return_value.count.return_value = 2
        self.room.clean()

    def test_new_room_clean_does_not_query_related_beds(self):
        self.room.pk = None
        self.room.clean()
        self.beds.filter.assert_not_called()

    @patch("hostels.models.Bed.objects.get_or_create")
    @patch("django.db.models.Model.save", return_value=None)
    def test_new_room_creates_one_available_bed_per_capacity(self, save, create):
        self.room.pk = None
        self.beds.count.return_value = 0
        Room.save.__wrapped__(self.room)
        self.assertEqual(
            create.call_args_list,
            [
                call(
                    room=self.room,
                    label="101-A",
                    defaults={"status": Bed.BedStatus.AVAILABLE},
                ),
                call(
                    room=self.room,
                    label="101-B",
                    defaults={"status": Bed.BedStatus.AVAILABLE},
                ),
            ],
        )
        save.assert_called_once()

    @patch("hostels.models.Bed.objects.get_or_create")
    @patch("django.db.models.Model.save", return_value=None)
    @patch("hostels.models.Room.objects.select_for_update")
    def test_renaming_room_updates_existing_bed_labels(self, previous, save, create):
        previous.return_value.get.return_value = Room(room_number="OLD")
        bed_a, bed_b = Mock(label="OLD-A"), Mock(label="OLD-B")
        self.beds.select_for_update.return_value.all.return_value = [bed_a, bed_b]
        self.beds.count.return_value = 2
        Room.save.__wrapped__(self.room)
        self.assertEqual((bed_a.label, bed_b.label), ("101-A", "101-B"))
        bed_a.save.assert_called_once_with(update_fields=["label"])
        bed_b.save.assert_called_once_with(update_fields=["label"])
        self.assertEqual(create.call_count, 2)
        save.assert_called_once()

    @patch("hostels.models.Bed.objects.get_or_create")
    @patch("django.db.models.Model.save", return_value=None)
    @patch("hostels.models.Room.objects.select_for_update")
    def test_reduction_deletes_only_removable_excess_beds(self, previous, save, create):
        previous.return_value.get.return_value = Room(room_number="101")
        excess = Mock()
        self.beds.count.side_effect = [3, 3, 2]
        self.beds.exclude.return_value.order_by.return_value.distinct.return_value = [
            excess
        ]
        Room.save.__wrapped__(self.room)
        self.beds.exclude.assert_called_once_with(allocations__isnull=False)
        excess.delete.assert_called_once()
        self.assertEqual(create.call_count, 2)

    def test_bulk_room_updates_cannot_bypass_bed_synchronization(self):
        for field in ("capacity", "room_number"):
            with self.subTest(field=field):
                with self.assertRaisesMessage(ValueError, "Room.save"):
                    Room.objects.all().update(**{field: 1})
                with self.assertRaisesMessage(ValueError, "Room.save"):
                    Room.objects.all().bulk_update([], [field])
