"""Persistence regressions for Room.save(update_fields=...)."""

from decimal import Decimal

from django.test import TestCase

from tests.factories import make_room

from .models import Bed


class RoomPartialSaveIntegrationTests(TestCase):
    def setUp(self):
        self.room = make_room("201", fee_amount=Decimal("750.00"))
        self.room.beds.filter(label="201-B").update(status=Bed.BedStatus.MAINTENANCE)

    def bed_state(self):
        return list(self.room.beds.order_by("label").values_list("label", "status"))

    def test_fee_only_save_keeps_stored_number_capacity_and_all_beds(self):
        before = self.bed_state()
        self.room.room_number = "UNSAVED"
        self.room.capacity = 4
        self.room.fee_amount = Decimal("950.00")

        self.room.save(update_fields=["fee_amount"])

        self.room.refresh_from_db()
        self.assertEqual(self.room.fee_amount, Decimal("950.00"))
        self.assertEqual((self.room.room_number, self.room.capacity), ("201", 2))
        self.assertEqual(self.bed_state(), before)

    def test_number_only_save_renames_beds_using_stored_capacity(self):
        self.room.room_number = "202"
        self.room.capacity = 4

        self.room.save(update_fields=["room_number"])

        self.room.refresh_from_db()
        self.assertEqual((self.room.room_number, self.room.capacity), ("202", 2))
        self.assertEqual(
            self.bed_state(),
            [
                ("202-A", Bed.BedStatus.AVAILABLE),
                ("202-B", Bed.BedStatus.MAINTENANCE),
            ],
        )

    def test_capacity_only_save_creates_beds_using_stored_room_number(self):
        self.room.room_number = "UNSAVED"
        self.room.capacity = 3

        self.room.save(update_fields=["capacity"])

        self.room.refresh_from_db()
        self.assertEqual((self.room.room_number, self.room.capacity), ("201", 3))
        self.assertEqual(
            self.bed_state(),
            [
                ("201-A", Bed.BedStatus.AVAILABLE),
                ("201-B", Bed.BedStatus.MAINTENANCE),
                ("201-C", Bed.BedStatus.AVAILABLE),
            ],
        )
