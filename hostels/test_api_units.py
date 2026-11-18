"""Isolated API contracts using real forms and unsaved domain objects."""

import json
from contextlib import nullcontext
from decimal import Decimal
from unittest.mock import MagicMock, call, patch

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from accounts.models import User
from audit.models import AuditEvent

from . import api
from .models import Bed, BedQuerySet, Hostel, HostelQuerySet, Room


class HostelApiUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin = User(pk=5, role=User.Role.ADMIN)
        self.hostel = Hostel(pk=7, name="North", hostel_type=Hostel.HostelType.BOYS)
        self.audit = self.enterContext(patch("hostels.api.record_event"))
        self.enterContext(
            patch("hostels.api.transaction.atomic", side_effect=lambda: nullcontext())
        )
        self.hostel_unique = self.enterContext(patch.object(Hostel, "validate_unique"))
        self.constraints = self.enterContext(patch.object(Room, "validate_constraints"))
        self.lookup = self.enterContext(
            patch.object(HostelQuerySet, "get", return_value=self.hostel)
        )
        self.enterContext(patch.object(HostelQuerySet, "exists", return_value=True))
        # ForeignKey.validate uses the plain _base_manager query set.
        self.enterContext(
            patch.object(
                type(Hostel._base_manager.get_queryset()), "exists", return_value=True
            )
        )
        self.saved = []
        self.beds = []

        def save_hostel(instance, *args, **kwargs):
            instance.pk = 41
            self.saved.append(instance)

        def save_room(instance, *args, **kwargs):
            instance.pk = 51
            self.saved.append(instance)
            self.beds = [
                Bed(pk=61, room=instance, label=f"{instance.room_number}-A"),
                Bed(pk=62, room=instance, label=f"{instance.room_number}-B"),
            ]

        self.hostel_save = self.enterContext(
            patch.object(Hostel, "save", autospec=True, side_effect=save_hostel)
        )
        self.room_save = self.enterContext(
            patch.object(Room, "save", autospec=True, side_effect=save_room)
        )
        self.bed_order = self.enterContext(
            patch.object(
                Room.beds.related_manager_cls,
                "order_by",
                side_effect=lambda *args: self.beds,
            )
        )

    def post(self, data, *, json_body=True, user=None):
        if json_body:
            request = self.factory.post(
                "/api/hostels/", json.dumps(data), content_type="application/json"
            )
        else:
            request = self.factory.post("/api/hostels/", data)
        request.user = self.admin if user is None else user
        return request

    def room_data(self, **changes):
        return {
            "room_number": "N101",
            "floor": 0,
            "room_type": "Double",
            "capacity": 2,
            "fee_amount": "1250.50",
            **changes,
        }

    def assert_error(self, response, status=400, code="VALIDATION_ERROR"):
        self.assertEqual(response.status_code, status)
        self.assertEqual(json.loads(response.content)["error"]["code"], code)
        self.assertEqual(self.saved, [])
        self.audit.assert_not_called()

    def test_hostel_creation_maps_documented_type_and_forces_active(self):
        request = self.post({"name": "  East Wing  ", "type": "Girls"})
        result = api.hostel_create(request)
        self.assertEqual(result.status_code, 201)
        self.assertEqual(json.loads(result.content), {"id": 41})
        hostel = self.saved[0]
        self.assertEqual(
            (hostel.name, hostel.hostel_type, hostel.is_active),
            ("East Wing", "Girls", True),
        )
        self.hostel_save.assert_called_once_with(hostel)
        self.audit.assert_called_once_with(
            user=self.admin, action=AuditEvent.Action.CREATE, record=hostel
        )

    def test_hostel_bad_fields_and_types_do_not_write(self):
        for data in (
            {"name": "East", "type": "Mixed"},
            {"name": "", "type": "Boys"},
            {"name": "x" * 101, "type": "Boys"},
            {"name": True, "type": "Boys"},
            {"name": "East", "type": "Boys", "is_active": False},
        ):
            with self.subTest(data=data):
                self.assert_error(api.hostel_create(self.post(data)))
        self.hostel_save.assert_not_called()

    def test_hostel_uniqueness_form_error_and_write_race_are_conflicts(self):
        data = {"name": "East", "type": "Boys"}
        self.hostel_unique.side_effect = ValidationError(
            {"name": ValidationError("duplicate", code="unique")}
        )
        self.assert_error(api.hostel_create(self.post(data)), 409, "DUPLICATE")
        self.hostel_save.assert_not_called()
        self.hostel_unique.side_effect = None
        self.hostel_save.side_effect = IntegrityError("duplicate key")
        self.assert_error(api.hostel_create(self.post(data)), 409, "DUPLICATE")

    def test_room_creation_uses_route_hostel_and_serializes_saved_beds(self):
        request = self.post(self.room_data())
        result = api.room_create(request, self.hostel.pk)
        self.assertEqual(result.status_code, 201)
        self.assertEqual(
            json.loads(result.content),
            {
                "room_id": 51,
                "beds": [
                    {"id": 61, "label": "N101-A", "status": "Available"},
                    {"id": 62, "label": "N101-B", "status": "Available"},
                ],
            },
        )
        room = self.saved[0]
        self.assertIs(room.hostel, self.hostel)
        self.assertEqual(
            (room.room_number, room.floor, room.capacity, room.fee_amount),
            ("N101", 0, 2, Decimal("1250.50")),
        )
        self.room_save.assert_called_once_with(room)
        self.bed_order.assert_called_once_with("pk")
        self.audit.assert_called_once_with(
            user=self.admin, action=AuditEvent.Action.CREATE, record=room
        )

    def test_form_encoded_room_numbers_and_default_fee_use_real_form_cleaning(self):
        # Frozen method ID: the old implicit-default behavior violated API-H2.
        data = self.room_data(floor="2", capacity="2")
        data.pop("fee_amount")
        self.assert_error(
            api.room_create(self.post(data, json_body=False), self.hostel.pk)
        )
        self.assert_error(
            api.room_create(self.post(self.room_data(fee_amount=None)), self.hostel.pk)
        )
        result = api.room_create(
            self.post(
                self.room_data(floor="2", capacity="2", fee_amount="0.00"),
                json_body=False,
            ),
            self.hostel.pk,
        )
        self.assertEqual(result.status_code, 201)
        room = self.saved[0]
        self.assertEqual(
            (room.floor, room.capacity, room.fee_amount), (2, 2, Decimal("0.00"))
        )

    def test_room_rejects_scalar_coercion_unsupported_fields_and_invalid_form_values(
        self,
    ):
        for changes in (
            {"floor": True},
            {"floor": "1"},
            {"capacity": 2.0},
            {"fee_amount": True},
            {"fee_amount": "-0.01"},
            {"capacity": 0},
            {"capacity": 5},
            {"floor": -1},
            {"room_type": "Dormitory"},
            {"room_number": ""},
            {"hostel": 99},
        ):
            with self.subTest(changes=changes):
                self.assert_error(
                    api.room_create(
                        self.post(self.room_data(**changes)), self.hostel.pk
                    )
                )
        self.room_save.assert_not_called()

    def test_room_uniqueness_form_error_and_integrity_race_are_conflicts(self):
        self.constraints.side_effect = ValidationError(
            {"__all__": ValidationError("duplicate", code="unique_together")}
        )
        self.assert_error(
            api.room_create(self.post(self.room_data()), self.hostel.pk),
            409,
            "DUPLICATE",
        )
        self.room_save.assert_not_called()
        self.constraints.side_effect = None
        self.room_save.side_effect = IntegrityError("duplicate key")
        self.assert_error(
            api.room_create(self.post(self.room_data()), self.hostel.pk),
            409,
            "DUPLICATE",
        )

    def test_model_validation_failure_during_room_save_returns_validation_response(
        self,
    ):
        self.room_save.side_effect = ValidationError("Room eligibility changed.")
        result = api.room_create(self.post(self.room_data()), self.hostel.pk)
        self.assert_error(result)
        self.assertEqual(
            json.loads(result.content)["error"]["message"], "Room eligibility changed."
        )

    def test_missing_hostel_and_roles_stop_before_room_write(self):
        self.lookup.side_effect = Hostel.DoesNotExist
        self.assert_error(
            api.room_create(self.post(self.room_data()), 999), 404, "NOT_FOUND"
        )
        self.room_save.assert_not_called()
        self.lookup.side_effect = None
        self.assert_error(
            api.room_create(self.post(self.room_data(), user=AnonymousUser()), 7),
            401,
            "AUTH_REQUIRED",
        )

    def test_hostel_endpoint_routes_json_posts_and_preserves_html_entrypoint(self):
        json_result = HttpResponse("json branch")
        html_result = HttpResponse("html branch")
        with (
            patch("hostels.api.hostel_create", return_value=json_result) as create,
            patch("hostels.views.hostel_list", return_value=html_result) as listing,
        ):
            request = self.post({"name": "East", "type": "Boys"})
            self.assertIs(api.hostel_endpoint(request), json_result)
            create.assert_called_once_with(request)
            listing.assert_not_called()
            for request in (
                self.factory.get("/hostels/", HTTP_ACCEPT="application/json"),
                self.factory.post("/hostels/", {"name": "East"}),
            ):
                self.assertIs(api.hostel_endpoint(request), html_result)
            self.assertEqual(listing.call_count, 2)


class BedAvailabilityApiUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.query = MagicMock(spec=BedQuerySet)
        self.query.filter.return_value = self.query
        self.query.order_by.return_value = []
        self.available = self.enterContext(
            patch("hostels.api.available_beds", return_value=self.query)
        )

    def request(self, data=None, role=User.Role.WARDEN):
        request = self.factory.get("/api/beds/available/", data or {})
        request.user = User(pk=4, role=role)
        return request

    def test_filters_clean_numbers_build_exact_lookups_and_serialize_domain_objects(
        self,
    ):
        hostel = Hostel(pk=7, name="North", hostel_type="Boys")
        room = Room(
            pk=11,
            hostel=hostel,
            room_number="101",
            floor=0,
            room_type="Double",
            capacity=2,
        )
        bed = Bed(pk=13, room=room, label="101-A")
        self.query.order_by.return_value = [bed]
        result = api.bed_availability(
            self.request({"hostel": "7", "floor": "0", "room_type": "Double"})
        )
        self.assertEqual(result.status_code, 200)
        self.query.filter.assert_has_calls(
            [
                call(room__hostel_id=7),
                call(room__floor=0),
                call(room__room_type="Double"),
            ]
        )
        self.assertEqual(self.query.filter.call_count, 3)
        self.query.order_by.assert_called_once_with("room_id", "label")
        self.assertEqual(
            json.loads(result.content),
            {
                "beds": [
                    {
                        "id": 13,
                        "label": "101-A",
                        "status": "Available",
                        "room_id": 11,
                        "room_number": "101",
                        "hostel_id": 7,
                        "hostel": "North",
                    }
                ]
            },
        )

    def test_absent_filters_return_empty_list_without_filtering(self):
        result = api.bed_availability(self.request())
        self.assertEqual(json.loads(result.content), {"beds": []})
        self.query.filter.assert_not_called()

    def test_invalid_numeric_and_unknown_filters_do_not_query_availability(self):
        for data in (
            {"extra": "value"},
            {"hostel": "0"},
            {"hostel": str(2**63)},
            {"floor": "-1"},
            {"floor": "100"},
            {"floor": "1.5"},
        ):
            with self.subTest(data=data):
                result = api.bed_availability(self.request(data))
                self.assertEqual(result.status_code, 400)
                self.assertEqual(
                    json.loads(result.content)["error"]["code"], "VALIDATION_ERROR"
                )
        self.available.assert_not_called()

    def test_invalid_room_type_stops_before_evaluation(self):
        result = api.bed_availability(self.request({"room_type": "Dormitory"}))
        self.assertEqual(result.status_code, 400)
        self.assertEqual(
            json.loads(result.content)["error"]["message"], "Choose a valid room type."
        )
        self.query.filter.assert_not_called()
        self.query.order_by.assert_not_called()

    @patch("hms.api.record_event")
    def test_student_role_cannot_read_availability(self, audit):
        request = self.request(role=User.Role.STUDENT)
        result = api.bed_availability(request)
        self.assertEqual(result.status_code, 403)
        self.assertEqual(json.loads(result.content)["error"]["code"], "ACCESS_DENIED")
        self.available.assert_not_called()
        audit.assert_called_once_with(
            user=request.user,
            action=AuditEvent.Action.ACCESS_DENIED,
            record_type="view",
            record_id="bed_availability",
        )
