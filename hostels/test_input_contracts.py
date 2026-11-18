"""Appendix B inventory inputs and explicit creation fees, without data truncation."""

from decimal import Decimal
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db import models
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from accounts.models import User
from audit.models import AuditEvent
from tests.factories import make_room

from .forms import BedFilterForm, HostelForm, RoomForm
from .models import Bed, Hostel, Room


class InventoryInputBoundaryUnitTests(SimpleTestCase):
    def test_storage_widths_preserve_legacy_values_and_validators_enforce_appendix_b(
        self,
    ):
        for model, name, width, valid, invalid in (
            (Hostel, "name", 100, "H" * 40, "H" * 41),
            (Room, "room_number", 10, "A12b34", "A12b345"),
            (Bed, "label", 20, "A12b34-D", "A12b345-D"),
        ):
            with self.subTest(model=model.__name__, field=name):
                field = model._meta.get_field(name)
                self.assertEqual(field.max_length, width)
                self.assertEqual(field.clean(valid, model()), valid)
                with self.assertRaises(ValidationError):
                    field.clean(invalid, model())

    def test_room_number_accepts_only_one_to_six_ascii_alphanumeric_characters(self):
        field = Room._meta.get_field("room_number")
        for number in ("", "A-101", "A 101", "A_101", "é101", "101\n"):
            with self.subTest(number=number), self.assertRaises(ValidationError):
                field.clean(number, Room())
        for number in ("1", "a101", "A12b34"):
            self.assertEqual(field.clean(number, Room()), number)

    def test_floor_limits_apply_to_model_filters_and_html_widget(self):
        field = Room._meta.get_field("floor")
        for floor in (-1, 100, 65535):
            with self.subTest(floor=floor), self.assertRaises(ValidationError):
                field.clean(floor, Room())
            self.assertFalse(BedFilterForm({"floor": floor}).is_valid())
        for floor in (0, 99):
            self.assertEqual(field.clean(floor, Room()), floor)
            self.assertTrue(BedFilterForm({"floor": floor}).is_valid())
        self.assertEqual(RoomForm().fields["floor"].widget.attrs["max"], 99)
        self.assertEqual(
            RoomForm().fields["room_number"].widget.attrs["maxlength"], "6"
        )
        self.assertEqual(HostelForm().fields["name"].widget.attrs["maxlength"], "40")

    def test_new_room_fee_is_required_and_explicit_zero_is_valid(self):
        form = RoomForm()
        self.assertTrue(form.fields["fee_amount"].required)
        for missing in (None, ""):
            with self.subTest(value=missing), self.assertRaises(ValidationError):
                form.fields["fee_amount"].clean(missing)
        self.assertEqual(form.fields["fee_amount"].clean("0.00"), Decimal("0.00"))
        # Internal constructors retain the documented unconfigured-fee state.
        self.assertEqual(Room().fee_amount, Decimal("0.00"))

    @patch("hostels.models.Hostel.objects.select_for_update")
    @patch("django.db.models.Model.save")
    def test_invalid_inputs_fail_model_save_before_locking_or_writing(
        self, write, lock
    ):
        records = [Hostel(name="H" * 41, hostel_type="Boys")]
        for changes in (
            {"room_number": "LONG777"},
            {"room_number": "A-101"},
            {"floor": 100},
        ):
            records.append(
                Room(
                    hostel_id=1,
                    room_number="101",
                    floor=0,
                    room_type="Double",
                    capacity=2,
                )
            )
            for key, value in changes.items():
                setattr(records[-1], key, value)
        records.append(Bed(room_id=1, label="longlabel", status="Available"))
        for record in records:
            with (
                self.subTest(model=type(record).__name__),
                self.assertRaises(ValidationError),
            ):
                type(record).save.__wrapped__(record)
        write.assert_not_called()
        lock.assert_not_called()

    def test_public_queryset_and_bulk_methods_cannot_skip_new_limits(self):
        for queryset, changes in (
            (Hostel.objects.all(), {"name": "H" * 41}),
            (Room.objects.all(), {"floor": 100}),
        ):
            with self.subTest(changes=changes), self.assertRaises(ValidationError):
                queryset.update(**changes)
        with self.assertRaisesMessage(ValueError, "Room.save"):
            Room.objects.bulk_update([], ["floor"])
        with self.assertRaisesMessage(ValueError, "Hostel.save"):
            Hostel.objects.bulk_update([], ["name"])
        with self.assertRaisesMessage(ValueError, "Bed.save"):
            Bed.objects.update(label="newlabel")
        with self.assertRaises(ValidationError):
            Hostel.objects.bulk_create([Hostel(name="H" * 41, hostel_type="Boys")])
        with self.assertRaises(ValidationError):
            Bed.objects.bulk_create([Bed(room_id=1, label="longlabel")])


class InventoryInputContractTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="input-admin", role="admin")
        self.client.force_login(self.admin)
        self.hostel = Hostel.objects.create(name="Input limits", hostel_type="Boys")

    def room_data(self, **changes):
        return {
            "room_number": "A12b34",
            "floor": 99,
            "room_type": "Double",
            "capacity": 4,
            "fee_amount": "0.00",
        } | changes

    def test_api_requires_creation_fee_and_rejects_appendix_b_overflows(self):
        baseline_audits = AuditEvent.objects.count()
        for changes in (
            {"fee_amount": None},
            {"room_number": "A123456"},
            {"room_number": "A-101"},
            {"floor": 100},
        ):
            with self.subTest(changes=changes):
                response = self.client.post(
                    f"/hostels/{self.hostel.pk}/rooms/",
                    self.room_data(**changes),
                    content_type="application/json",
                )
                self.assertEqual(response.status_code, 400, response.content)
        missing = self.room_data()
        missing.pop("fee_amount")
        response = self.client.post(
            f"/hostels/{self.hostel.pk}/rooms/",
            missing,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Room.objects.exists())
        self.assertEqual(AuditEvent.objects.count(), baseline_audits)
        response = self.client.post(
            f"/hostels/{self.hostel.pk}/rooms/",
            self.room_data(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201, response.content)
        room = Room.objects.get()
        self.assertEqual(room.fee_amount, Decimal("0.00"))
        self.assertEqual(
            set(room.beds.values_list("label", flat=True)),
            {f"A12b34-{suffix}" for suffix in "ABCD"},
        )
        self.assertTrue(
            all(len(label) == 8 for label in room.beds.values_list("label", flat=True))
        )

    def test_html_creation_requires_fee_and_edit_omission_preserves_existing_fee(self):
        missing = {"hostel": self.hostel.pk} | self.room_data()
        missing.pop("fee_amount")
        response = self.client.post(reverse("room-create"), missing)
        self.assertEqual(response.status_code, 200)
        self.assertIn("fee_amount", response.context["form"].errors)
        self.assertFalse(Room.objects.exists())
        room = make_room("101", hostel=self.hostel, fee_amount=Decimal("1234.50"))
        edit = {"hostel": self.hostel.pk} | self.room_data(
            room_number="101", capacity=2
        )
        edit.pop("fee_amount")
        response = self.client.post(reverse("room-update", args=[room.pk]), edit)
        self.assertEqual(response.status_code, 302, response.content)
        room.refresh_from_db()
        self.assertEqual(room.fee_amount, Decimal("1234.50"))

    def test_model_saves_enforce_name_floor_and_bed_label_bounds(self):
        self.hostel.name = "H" * 40
        self.hostel.save(update_fields=["name"])
        self.hostel.name = "H" * 41
        with self.assertRaises(ValidationError):
            self.hostel.save(update_fields=["name"])
        room = make_room("A12b34", hostel=self.hostel, floor=99)
        room.floor = 100
        with self.assertRaises(ValidationError):
            room.save(update_fields=["floor"])
        bed = room.beds.first()
        bed.label = "custom88"
        bed.save(update_fields=["label"])
        bed.label = "custom999"
        with self.assertRaises(ValidationError):
            bed.save(update_fields=["label"])
        bed.refresh_from_db()
        self.assertEqual(bed.label, "custom88")

    def test_validation_migration_preserves_legacy_values_during_unrelated_edits(self):
        room = make_room("101", hostel=self.hostel)
        bed = room.beds.first()
        # Simulate pre-migration rows using the base SQL primitive intentionally.
        models.QuerySet.update(Hostel.objects.filter(pk=self.hostel.pk), name="H" * 50)
        models.QuerySet.update(
            Room.objects.filter(pk=room.pk), room_number="LEGACY77", floor=100
        )
        models.QuerySet.update(Bed.objects.filter(pk=bed.pk), label="legacy-label")
        self.hostel.refresh_from_db()
        room.refresh_from_db()
        bed.refresh_from_db()
        self.hostel.save(update_fields=["is_active"])
        room.fee_amount = Decimal("100.00")
        room.save(update_fields=["fee_amount"])
        bed.status = Bed.BedStatus.MAINTENANCE
        bed.save(update_fields=["status"])
        self.hostel.refresh_from_db()
        room.refresh_from_db()
        bed.refresh_from_db()
        self.assertEqual(self.hostel.name, "H" * 50)
        self.assertEqual((room.room_number, room.floor), ("LEGACY77", 100))
        self.assertEqual(bed.label, "legacy-label")
