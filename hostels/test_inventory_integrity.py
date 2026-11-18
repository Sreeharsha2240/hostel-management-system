"""Inventory edits must preserve admission, capacity, and historical location."""

from concurrent.futures import ThreadPoolExecutor
from datetime import date
from threading import Barrier
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db import close_old_connections, connections
from django.test import SimpleTestCase, TestCase, TransactionTestCase
from django.urls import reverse

from accounts.models import User
from allocations.models import Allocation
from audit.models import AuditEvent
from tests.factories import make_room, make_student

from .forms import HostelForm, RoomForm
from .models import Bed, Hostel, Room


class InventoryBypassPolicyUnitTests(SimpleTestCase):
    def test_hostel_eligibility_queryset_and_generator_bulk_updates_are_rejected(self):
        for field, value in (("hostel_type", "Girls"), ("is_active", False)):
            with self.subTest(field=field):
                with self.assertRaisesMessage(ValueError, "Hostel.save"):
                    Hostel.objects.update(**{field: value})
                with self.assertRaisesMessage(ValueError, "Hostel.save"):
                    Hostel.objects.bulk_update([], iter([field]))

    def test_room_bulk_creation_cannot_skip_automatic_beds_or_history_checks(self):
        with self.assertRaisesMessage(ValueError, "Room.save"):
            Room.objects.bulk_create([Room(capacity=2)])

    def test_generator_bulk_updates_cannot_consume_room_or_bed_protected_fields(self):
        for model, field in (
            (Room, "hostel_id"),
            (Room, "capacity"),
            (Bed, "room_id"),
            (Bed, "status"),
        ):
            with self.subTest(model=model.__name__, field=field):
                with self.assertRaisesMessage(ValueError, ".save"):
                    model.objects.bulk_update([], iter([field]))

    def test_bed_status_queryset_updates_are_rejected(self):
        with self.assertRaisesMessage(ValueError, "Bed.save"):
            Bed.objects.update(status=Bed.BedStatus.AVAILABLE)

    def test_conflict_upserts_cannot_rewrite_existing_inventory(self):
        for model in (Hostel, Bed):
            with self.subTest(model=model.__name__):
                with self.assertRaisesMessage(ValueError, ".save"):
                    model.objects.bulk_create(
                        [], update_conflicts=True, update_fields=["status"]
                    )
                # Django accepts update_conflicts positionally too.
                with self.assertRaisesMessage(ValueError, ".save"):
                    model.objects.bulk_create([], None, False, True, ["status"])


class InventoryMutationRegressionTests(TestCase):
    def setUp(self):
        self.room = make_room("INV1", capacity=2)
        self.hostel = self.room.hostel
        self.bed = self.room.beds.get(label="INV1-A")
        self.student = make_student(950)

    def allocate(self):
        allocation = Allocation.objects.create(student=self.student, bed=self.bed)
        self.bed.refresh_from_db()
        return allocation

    def admin_login(self):
        admin = User.objects.create_superuser(
            username="inventory_superuser",
            password="TestPassword123!",
            role=User.Role.ADMIN,
        )
        self.client.force_login(admin)
        return admin

    def test_model_save_rejects_capacity_outside_one_to_four_without_writes(self):
        for capacity in (0, 5):
            with self.subTest(capacity=capacity):
                self.room.capacity = capacity
                with self.assertRaises(ValidationError):
                    self.room.save(update_fields=["capacity"])
                self.room.refresh_from_db()
                self.assertEqual(self.room.capacity, 2)
                self.assertEqual(self.room.beds.count(), 2)
        for capacity in (1, 4):
            self.room.capacity = capacity
            self.room.save(update_fields=["capacity"])
            self.assertEqual(self.room.beds.count(), capacity)

    def test_active_bed_cannot_be_made_available(self):
        allocation = self.allocate()
        for state in (Bed.BedStatus.AVAILABLE,):
            for positional in (False, True):
                with self.subTest(state=state, positional=positional):
                    self.bed.status = state
                    with self.assertRaisesMessage(ValidationError, "active allocation"):
                        if positional:
                            self.bed.save(False, False, None, iter(["status"]))
                        else:
                            self.bed.save(update_fields=iter(["status"]))
                    self.bed.refresh_from_db()
                    allocation.refresh_from_db()
                    self.assertEqual(self.bed.status, Bed.BedStatus.OCCUPIED)
                    self.assertEqual(
                        allocation.status, Allocation.AllocationStatus.ACTIVE
                    )

    def test_release_can_make_bed_available_then_maintenance(self):
        allocation = self.allocate()
        allocation.status = Allocation.AllocationStatus.COMPLETED
        allocation.vacated_on = date.today()
        allocation.save(update_fields=["status", "vacated_on"])
        self.bed.refresh_from_db()
        self.assertEqual(self.bed.status, Bed.BedStatus.AVAILABLE)
        self.bed.status = Bed.BedStatus.MAINTENANCE
        self.bed.save(update_fields=iter(["status"]))
        self.bed.refresh_from_db()
        self.assertEqual(self.bed.status, Bed.BedStatus.MAINTENANCE)

    def test_active_bed_can_be_reserved_for_maintenance_and_release_preserves_it(self):
        allocation = self.allocate()
        self.bed.status = Bed.BedStatus.MAINTENANCE
        self.bed.save(update_fields=iter(["status"]))
        allocation.status = Allocation.AllocationStatus.COMPLETED
        allocation.vacated_on = date.today()
        allocation.save(update_fields=["status", "vacated_on"])
        self.bed.refresh_from_db()
        self.assertEqual(self.bed.status, Bed.BedStatus.MAINTENANCE)

    def test_partial_bed_save_ignores_unsaved_status_and_room_changes(self):
        self.allocate()
        destination = make_room("INV2", hostel=self.hostel)
        self.bed.room = destination
        self.bed.status = Bed.BedStatus.MAINTENANCE
        self.bed.label = "kept"
        self.bed.save(update_fields=iter(["label"]))
        self.bed.refresh_from_db()
        self.assertEqual(self.bed.room_id, self.room.pk)
        self.assertEqual(self.bed.status, Bed.BedStatus.OCCUPIED)
        self.assertEqual(self.bed.label, "kept")

    def test_partial_room_save_ignores_invalid_excluded_capacity(self):
        self.room.capacity = 0
        self.room.floor = 2
        self.room.save(update_fields=iter(["floor"]))
        self.room.refresh_from_db()
        self.assertEqual((self.room.capacity, self.room.floor), (2, 2))

    def test_hostel_partial_saves_validate_only_persisted_eligibility(self):
        self.allocate()
        self.hostel.hostel_type = Hostel.HostelType.GIRLS
        self.hostel.is_active = False
        self.hostel.name = "Renamed occupied hostel"
        self.hostel.save(update_fields=iter(["name"]))
        self.hostel.refresh_from_db()
        self.assertTrue(self.hostel.is_active)
        self.assertEqual(self.hostel.hostel_type, Hostel.HostelType.BOYS)
        self.hostel.hostel_type = Hostel.HostelType.GIRLS
        with self.assertRaises(ValidationError):
            self.hostel.save(False, False, None, iter(["hostel_type"]))
        self.hostel.refresh_from_db()
        self.assertEqual(self.hostel.hostel_type, Hostel.HostelType.BOYS)
        self.hostel.is_active = False
        with self.assertRaises(ValidationError):
            self.hostel.save(update_fields=iter(["is_active"]))

    def test_active_hostel_cannot_escape_gender_validation_with_unknown_type(self):
        self.allocate()
        self.hostel.hostel_type = "Other"
        with self.assertRaises(ValidationError):
            self.hostel.save(update_fields=["hostel_type"])
        self.hostel.refresh_from_db()
        self.assertEqual(self.hostel.hostel_type, Hostel.HostelType.BOYS)

    def test_hostel_save_ignores_an_excluded_incompatible_in_memory_type(self):
        self.allocate()
        self.hostel.hostel_type = Hostel.HostelType.GIRLS
        self.hostel.save(update_fields=iter(["is_active"]))
        self.hostel.refresh_from_db()
        self.assertEqual(self.hostel.hostel_type, Hostel.HostelType.BOYS)

    def test_completed_allocation_location_is_preserved_by_clean_and_bed_save(self):
        allocation = self.allocate()
        allocation.status = Allocation.AllocationStatus.COMPLETED
        allocation.vacated_on = date.today()
        allocation.save(update_fields=["status", "vacated_on"])
        target = make_room("INV3", capacity=1)
        self.room.hostel = target.hostel
        with self.assertRaisesMessage(ValidationError, "historical location"):
            self.room.clean()
        self.bed.room = target
        with self.assertRaisesMessage(ValidationError, "historical location"):
            self.bed.save(update_fields=iter(["room_id"]))
        self.bed.refresh_from_db()
        self.assertEqual(self.bed.room_id, self.room.pk)
        self.room.refresh_from_db()
        self.assertEqual(self.room.hostel_id, self.hostel.pk)

    def test_ordinary_hostel_edit_race_is_rendered_as_error_and_not_audited(self):
        self.admin_login()
        # ModelForm validated before another request admitted a resident.
        original = HostelForm.is_valid

        def validate_then_allocate(form):
            valid = original(form)
            if valid:
                self.allocate()
            return valid

        audit_before = AuditEvent.objects.count()
        with patch.object(HostelForm, "is_valid", validate_then_allocate):
            response = self.client.post(
                reverse("hostel-update", args=[self.hostel.pk]),
                {
                    "name": self.hostel.name,
                    "hostel_type": self.hostel.hostel_type,
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn("is_active", response.context["form"].errors)
        self.hostel.refresh_from_db()
        self.assertTrue(self.hostel.is_active)
        self.assertEqual(AuditEvent.objects.count(), audit_before)

    def test_admin_cannot_move_occupied_bed_into_full_room_or_change_its_status(self):
        self.admin_login()
        allocation = self.allocate()
        destination = make_room("INV4", hostel=self.hostel, capacity=1)
        Allocation.objects.create(student=make_student(951), bed=destination.beds.get())
        audit_before = AuditEvent.objects.count()
        response = self.client.post(
            reverse("admin:hostels_bed_change", args=[self.bed.pk]),
            {
                "room": destination.pk,
                "label": self.bed.label,
                "status": Bed.BedStatus.AVAILABLE,
                "_save": "Save",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("room", response.context["adminform"].form.errors)
        self.assertIn("status", response.context["adminform"].form.errors)
        self.bed.refresh_from_db()
        allocation.refresh_from_db()
        self.assertEqual(self.bed.room_id, self.room.pk)
        self.assertEqual(self.bed.status, Bed.BedStatus.OCCUPIED)
        self.assertEqual(
            destination.beds.filter(allocations__status="Active").count(), 1
        )
        self.assertEqual(AuditEvent.objects.count(), audit_before)

    def test_admin_bed_inline_cannot_change_active_bed_to_available(self):
        self.admin_login()
        self.allocate()
        beds = list(self.room.beds.order_by("pk"))
        data = {
            "hostel": self.hostel.pk,
            "room_number": self.room.room_number,
            "floor": self.room.floor,
            "room_type": self.room.room_type,
            "capacity": self.room.capacity,
            "fee_amount": self.room.fee_amount,
            "beds-TOTAL_FORMS": len(beds),
            "beds-INITIAL_FORMS": len(beds),
            "beds-MIN_NUM_FORMS": "0",
            "beds-MAX_NUM_FORMS": "1000",
            "_save": "Save",
        }
        for index, bed in enumerate(beds):
            data.update(
                {
                    f"beds-{index}-id": bed.pk,
                    f"beds-{index}-room": self.room.pk,
                    f"beds-{index}-status": Bed.BedStatus.AVAILABLE,
                }
            )
        audit_before = AuditEvent.objects.count()
        response = self.client.post(
            reverse("admin:hostels_room_change", args=[self.room.pk]), data
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "active allocation")
        self.bed.refresh_from_db()
        self.assertEqual(self.bed.status, Bed.BedStatus.OCCUPIED)
        self.assertEqual(AuditEvent.objects.count(), audit_before)

    def test_admin_save_time_validation_race_returns_bound_error_without_audit(self):
        self.admin_login()
        audit_before = AuditEvent.objects.count()
        with patch.object(
            Bed,
            "save",
            side_effect=ValidationError({"status": "Concurrent resident admitted."}),
        ):
            response = self.client.post(
                reverse("admin:hostels_bed_change", args=[self.bed.pk]),
                {
                    "room": self.room.pk,
                    "label": self.bed.label,
                    "status": Bed.BedStatus.MAINTENANCE,
                    "_save": "Save",
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Concurrent resident admitted.")
        self.bed.refresh_from_db()
        self.assertEqual(self.bed.status, Bed.BedStatus.AVAILABLE)
        self.assertEqual(AuditEvent.objects.count(), audit_before)

    def test_admin_inline_save_rejection_rolls_back_parent_and_returns_form_error(self):
        self.admin_login()
        original_fee = self.room.fee_amount
        beds = list(self.room.beds.order_by("pk"))
        data = {
            "hostel": self.hostel.pk,
            "room_number": self.room.room_number,
            "floor": self.room.floor,
            "room_type": self.room.room_type,
            "capacity": self.room.capacity,
            "fee_amount": "500.00",
            "beds-TOTAL_FORMS": len(beds),
            "beds-INITIAL_FORMS": len(beds),
            "beds-MIN_NUM_FORMS": "0",
            "beds-MAX_NUM_FORMS": "1000",
            "_save": "Save",
        }
        for index, bed in enumerate(beds):
            data.update(
                {
                    f"beds-{index}-id": bed.pk,
                    f"beds-{index}-room": self.room.pk,
                    f"beds-{index}-status": Bed.BedStatus.MAINTENANCE,
                }
            )
        audit_before = AuditEvent.objects.count()
        with patch(
            "hostels.admin.save_audited_formset",
            side_effect=ValidationError("The bed changed; refresh."),
        ):
            response = self.client.post(
                reverse("admin:hostels_room_change", args=[self.room.pk]), data
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The bed changed; refresh.")
        self.room.refresh_from_db()
        self.assertEqual(self.room.fee_amount, original_fee)
        self.assertEqual(AuditEvent.objects.count(), audit_before)

    def test_ordinary_capacity_edit_race_preserves_allocations_and_renders_error(self):
        self.admin_login()
        original = RoomForm.is_valid

        def validate_then_fill(form):
            valid = original(form)
            if valid:
                self.allocate()
                Allocation.objects.create(
                    student=make_student(953), bed=self.room.beds.get(label="INV1-B")
                )
            return valid

        audit_before = AuditEvent.objects.count()
        with patch.object(RoomForm, "is_valid", validate_then_fill):
            response = self.client.post(
                reverse("room-update", args=[self.room.pk]),
                {
                    "hostel": self.hostel.pk,
                    "room_number": self.room.room_number,
                    "floor": self.room.floor,
                    "room_type": self.room.room_type,
                    "capacity": 1,
                    "fee_amount": self.room.fee_amount,
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.room.refresh_from_db()
        self.assertEqual(self.room.capacity, 2)
        self.assertEqual(self.room.beds.filter(allocations__status="Active").count(), 2)
        self.assertEqual(AuditEvent.objects.count(), audit_before)


class InventoryEligibilityRaceTests(TransactionTestCase):
    def setUp(self):
        self.room = make_room("RACE", capacity=1)
        self.bed = self.room.beds.get()
        self.student = make_student(952)

    def race(self, left, right):
        barrier = Barrier(2, timeout=20)

        def run(operation):
            close_old_connections()
            try:
                barrier.wait()
                operation()
                return "ok"
            except ValidationError:
                return "rejected"
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            return sorted(pool.map(run, (left, right)))

    def allocate(self):
        Allocation.objects.create(student_id=self.student.pk, bed_id=self.bed.pk)

    def test_hostel_deactivation_racing_allocation_has_one_valid_winner(self):
        def deactivate():
            hostel = Hostel.objects.get(pk=self.room.hostel_id)
            hostel.is_active = False
            hostel.save(update_fields=iter(["is_active"]))

        self.assertEqual(self.race(self.allocate, deactivate), ["ok", "rejected"])
        self.room.hostel.refresh_from_db()
        active = Allocation.objects.filter(bed=self.bed, status="Active").exists()
        self.assertEqual(self.room.hostel.is_active, active)

    def test_bed_available_edit_racing_allocation_preserves_occupied_state(self):
        def mark_available():
            bed = Bed.objects.get(pk=self.bed.pk)
            bed.status = Bed.BedStatus.AVAILABLE
            bed.save(update_fields=iter(["status"]))

        outcomes = self.race(self.allocate, mark_available)
        self.assertIn(outcomes, (["ok", "ok"], ["ok", "rejected"]))
        self.bed.refresh_from_db()
        self.assertTrue(
            Allocation.objects.filter(bed=self.bed, status="Active").exists()
        )
        self.assertEqual(self.bed.status, Bed.BedStatus.OCCUPIED)
