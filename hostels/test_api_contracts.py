"""Session, role, validation and persistence contracts for SAD API-H1/H2/H3."""

from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse

from accounts.models import User
from allocations.services import allocate
from audit.models import AuditEvent
from tests.factories import make_room, make_student

from .forms import HostelForm, RoomForm
from .models import Hostel, Room


class RoomValidationBoundaryTests(SimpleTestCase):
    def test_invalid_capacity_is_validation_error_even_after_field_validation_fails(
        self,
    ):
        for capacity in ("bad", [], {}, None):
            with (
                self.subTest(capacity=capacity),
                self.assertRaises(ValidationError) as error,
            ):
                Room(
                    hostel_id=1,
                    room_number="101",
                    floor=0,
                    room_type="Double",
                    capacity=capacity,
                ).full_clean(
                    exclude=["hostel"],
                    validate_unique=False,
                    validate_constraints=False,
                )
            self.assertIn("capacity", error.exception.message_dict)


class InventoryUniqueRaceTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="unique-race-admin", role="admin"
        )
        self.client.force_login(self.admin)

    def test_hostel_create_duplicate_after_validation_is_rendered_and_not_audited(self):
        data = {"name": "Unique race", "hostel_type": "Boys", "is_active": True}
        form = HostelForm(data)
        self.assertTrue(form.is_valid(), form.errors)
        Hostel.objects.create(name="Unique race", hostel_type="Boys")
        with patch("hostels.views.HostelForm", return_value=form):
            response = self.client.post(reverse("hostel-list"), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.context["form"].errors)
        self.assertEqual(Hostel.objects.filter(name="Unique race").count(), 1)
        self.assertFalse(
            AuditEvent.objects.filter(action=AuditEvent.Action.CREATE).exists()
        )

    def test_hostel_update_duplicate_after_validation_preserves_original(self):
        hostel = Hostel.objects.create(name="Original", hostel_type="Boys")
        data = {"name": "Competing", "hostel_type": "Boys", "is_active": True}
        form = HostelForm(data, instance=hostel)
        self.assertTrue(form.is_valid(), form.errors)
        Hostel.objects.create(name="Competing", hostel_type="Boys")
        with patch("hostels.views.HostelForm", return_value=form):
            response = self.client.post(
                reverse("hostel-update", args=[hostel.pk]), data
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.context["form"].errors)
        hostel.refresh_from_db()
        self.assertEqual(hostel.name, "Original")
        self.assertFalse(
            AuditEvent.objects.filter(action=AuditEvent.Action.UPDATE).exists()
        )

    def test_room_create_duplicate_after_validation_leaves_no_extra_beds(self):
        hostel = Hostel.objects.create(name="Room race", hostel_type="Boys")
        data = {
            "hostel": hostel.pk,
            "room_number": "101",
            "floor": 0,
            "room_type": "Double",
            "capacity": 2,
            "fee_amount": "1000.00",
        }
        form = RoomForm(data)
        self.assertTrue(form.is_valid(), form.errors)
        existing = make_room("101", hostel=hostel)
        with patch("hostels.views.RoomForm", return_value=form):
            response = self.client.post(reverse("room-create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("room_number", response.context["form"].errors)
        self.assertEqual(hostel.rooms.count(), 1)
        self.assertEqual(existing.beds.count(), 2)
        self.assertFalse(
            AuditEvent.objects.filter(action=AuditEvent.Action.CREATE).exists()
        )

    def test_room_update_duplicate_after_validation_preserves_original_labels(self):
        room = make_room("101")
        data = {
            "hostel": room.hostel_id,
            "room_number": "202",
            "floor": 0,
            "room_type": "Double",
            "capacity": 2,
            "fee_amount": "1000.00",
        }
        form = RoomForm(data, instance=room)
        self.assertTrue(form.is_valid(), form.errors)
        make_room("202", hostel=room.hostel)
        with patch("hostels.views.RoomForm", return_value=form):
            response = self.client.post(reverse("room-update", args=[room.pk]), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("room_number", response.context["form"].errors)
        room.refresh_from_db()
        self.assertEqual(room.room_number, "101")
        self.assertEqual(
            set(room.beds.values_list("label", flat=True)), {"101-A", "101-B"}
        )
        self.assertFalse(
            AuditEvent.objects.filter(action=AuditEvent.Action.UPDATE).exists()
        )


class HostelApiContractTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="inventory-api-admin", role="admin"
        )
        self.warden = User.objects.create_user(
            username="inventory-api-warden", role="warden"
        )
        self.student = User.objects.create_user(
            username="inventory-api-student", role="student"
        )
        self.client.force_login(self.admin)

    def create_hostel(self, **changes):
        return self.client.post(
            "/hostels/",
            {"name": "API Boys", "type": "Boys"} | changes,
            content_type="application/json",
        )

    def create_room(self, hostel, **changes):
        return self.client.post(
            f"/hostels/{hostel.pk}/rooms/",
            {
                "room_number": "A101",
                "floor": 1,
                "room_type": "Double",
                "capacity": 2,
                "fee_amount": "5000.00",
            }
            | changes,
            content_type="application/json",
        )

    def test_creation_contract_persists_beds_and_audit(self):
        response = self.create_hostel()
        self.assertEqual(response.status_code, 201, response.content)
        hostel = Hostel.objects.get(pk=response.json()["id"])
        self.assertTrue(hostel.is_active)
        response = self.create_room(hostel)
        self.assertEqual(response.status_code, 201, response.content)
        room = Room.objects.get(pk=response.json()["room_id"])
        self.assertEqual(room.hostel, hostel)
        self.assertEqual(
            [bed["label"] for bed in response.json()["beds"]], ["A101-A", "A101-B"]
        )
        self.assertEqual(
            AuditEvent.objects.filter(action=AuditEvent.Action.CREATE).count(), 2
        )

    def test_duplicates_are_conflicts_and_preserve_original_inventory(self):
        self.assertEqual(self.create_hostel().status_code, 201)
        self.assertEqual(self.create_hostel().status_code, 409)
        hostel = Hostel.objects.get(name="API Boys")
        self.assertEqual(self.create_room(hostel).status_code, 201)
        self.assertEqual(self.create_room(hostel).status_code, 409)
        self.assertEqual(hostel.rooms.count(), 1)
        self.assertEqual(hostel.rooms.get().beds.count(), 2)

    def test_invalid_types_bounds_and_unknown_fields_do_not_create_records(self):
        hostel = Hostel.objects.create(name="Boundary Boys", hostel_type="Boys")
        for capacity in (True, 0, 5, 2.5, "2", [2], None):
            with self.subTest(capacity=capacity):
                self.assertEqual(
                    self.create_room(hostel, capacity=capacity).status_code, 400
                )
        self.assertEqual(self.create_room(hostel, floor=-1).status_code, 400)
        self.assertEqual(self.create_room(hostel, fee_amount=True).status_code, 400)
        self.assertEqual(self.create_hostel(is_active=False).status_code, 400)
        self.assertEqual(self.create_hostel(name=True).status_code, 400)
        self.assertFalse(Room.objects.exists())
        self.assertFalse(Hostel.objects.filter(name="API Boys").exists())

    def test_anonymous_and_student_cannot_read_inventory_or_create_it(self):
        anonymous = Client()
        self.assertEqual(
            anonymous.post(
                "/hostels/", {}, content_type="application/json"
            ).status_code,
            401,
        )
        self.assertEqual(anonymous.get("/beds/available/").status_code, 401)
        for user in (self.warden, self.student):
            self.client.force_login(user)
            self.assertEqual(self.create_hostel().status_code, 403)
        self.assertEqual(self.client.get("/beds/available/").status_code, 403)
        self.assertEqual(
            self.client.get(reverse("bed-list"), {"status": "Occupied"}).status_code,
            403,
        )
        dashboard = self.client.get(reverse("dashboard"))
        self.assertNotContains(dashboard, 'href="/beds/"')

    def test_warden_availability_filters_only_allocatable_beds(self):
        room = make_room()
        second = make_room("202", hostel=room.hostel, floor=2)
        inactive = Hostel.objects.create(
            name="Inactive API", hostel_type="Boys", is_active=False
        )
        make_room("303", hostel=inactive)
        occupied = room.beds.first()
        allocate(student=make_student(), bed=occupied, actor=self.warden)
        self.client.force_login(self.warden)
        response = self.client.get(
            "/beds/available/",
            {"hostel": room.hostel_id, "floor": 0, "room_type": "Double"},
        )
        self.assertEqual(response.status_code, 200)
        beds = response.json()["beds"]
        self.assertEqual(
            [item["id"] for item in beds], [room.beds.exclude(pk=occupied.pk).get().pk]
        )
        all_ids = {
            item["id"] for item in self.client.get("/beds/available/").json()["beds"]
        }
        self.assertTrue(set(second.beds.values_list("pk", flat=True)).issubset(all_ids))
        self.assertEqual(len(all_ids), 3)

    def test_invalid_filter_and_missing_hostel_are_json_errors(self):
        self.assertEqual(
            self.client.get("/beds/available/", {"floor": "bad"}).status_code, 400
        )
        self.assertEqual(
            self.client.get("/beds/available/", {"room_type": "unknown"}).status_code,
            400,
        )
        self.assertEqual(
            self.client.get("/beds/available/", {"status": "Occupied"}).status_code, 400
        )
        response = self.client.post(
            "/hostels/999999/rooms/", {}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"]["code"], "NOT_FOUND")

    def test_audit_failure_rolls_back_hostel_creation(self):
        with patch(
            "hostels.api.record_event",
            side_effect=ValidationError("injected audit rejection"),
        ):
            self.assertEqual(self.create_hostel().status_code, 400)
        self.assertFalse(Hostel.objects.filter(name="API Boys").exists())

    def test_json_writes_require_real_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.admin)
        data = {"name": "CSRF Boys", "type": "Boys"}
        self.assertEqual(
            client.post("/hostels/", data, content_type="application/json").status_code,
            403,
        )
        self.assertEqual(client.get("/hostels/").status_code, 200)
        token = client.cookies["csrftoken"].value
        response = client.post(
            "/hostels/", data, content_type="application/json", HTTP_X_CSRFTOKEN=token
        )
        self.assertEqual(response.status_code, 201, response.content)
