"""Student JSON decisions without a database; persistence is tested separately."""

import json
from contextlib import nullcontext
from datetime import date
from decimal import Decimal
from unittest.mock import Mock, patch

from django.db import IntegrityError
from django.db.models import Q
from django.db.models.query import QuerySet
from django.test import RequestFactory, SimpleTestCase

from accounts.models import User
from allocations.models import Allocation
from hostels.models import Bed, Hostel, Room

from . import api
from .models import Student, StudentQuerySet


class StudentApiUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.warden = User(pk=3, username="warden", role=User.Role.WARDEN)
        self.student = Student(pk=41, **self.values())
        self.student._state.adding = False
        self.audit = self.enterContext(patch("students.api.record_event"))
        self.atomic = self.enterContext(
            patch("students.api.transaction.atomic", side_effect=lambda: nullcontext())
        )
        self.lookup = self.enterContext(
            patch("students.api.get_object_or_404", return_value=self.student)
        )
        self.unique = self.enterContext(patch.object(Student, "validate_unique"))
        self.exists = self.enterContext(
            patch.object(StudentQuerySet, "exists", return_value=False)
        )
        self.save = self.enterContext(patch.object(Student, "save", autospec=True))

    def values(self, **changes):
        return {
            "student_id": "PES1UG24CS163",
            "name": "Ananya Rao",
            "date_of_birth": date(2005, 4, 8),
            "gender": "Female",
            "course": "Computer Science",
            "year": 2,
            "mobile": "9876543210",
            "email": "ananya@example.com",
            "guardian_name": "Rao",
            "guardian_mobile": "9123456789",
            "address": "Room 4, College Road",
            "status": "Active",
        } | changes

    def payload(self, **changes):
        result = self.values()
        result.pop("status")
        result["dob"] = result.pop("date_of_birth").isoformat()
        return result | changes

    def request(self, method, data, user=None):
        if method == "get":
            request = self.factory.get("/students/", data)
        else:
            request = getattr(self.factory, method)(
                "/students/", data, content_type="application/json"
            )
        request.user = self.warden if user is None else user
        return request

    def body(self, response):
        return json.loads(response.content)

    def assert_error(self, response, status, code):
        self.assertEqual(response.status_code, status, response.content)
        self.assertEqual(self.body(response)["error"]["code"], code)

    def allocation(self):
        hostel = Hostel(pk=7, name="Girls Hostel", hostel_type="Girls")
        room = Room(
            pk=8,
            hostel=hostel,
            room_number="204",
            floor=2,
            room_type="Double",
            capacity=2,
        )
        bed = Bed(pk=9, room=room, label="204-A", status="Occupied")
        return Allocation(
            pk=11, student=self.student, bed=bed, allocated_on=date(2026, 8, 1)
        )

    def test_serialize_explicit_public_fields_and_iso_date(self):
        self.student.user_id = 999
        self.assertEqual(
            api.serialize(self.student),
            {
                "id": 41,
                "student_id": "PES1UG24CS163",
                "name": "Ananya Rao",
                "dob": "2005-04-08",
                "gender": "Female",
                "course": "Computer Science",
                "year": 2,
                "mobile": "9876543210",
                "email": "ananya@example.com",
                "guardian_name": "Rao",
                "guardian_mobile": "9123456789",
                "address": "Room 4, College Road",
                "status": "Active",
            },
        )

    def test_create_maps_dob_normalizes_id_and_uses_real_form(self):
        created = []

        def save(student, **kwargs):
            student.pk = 55
            created.append(student)

        self.save.side_effect = save
        response = api.student_collection(
            self.request("post", self.payload(student_id="pes1ug24cs163"))
        )
        self.assertEqual(
            (response.status_code, self.body(response)),
            (201, {"id": 55, "student_id": "PES1UG24CS163", "name": "Ananya Rao"}),
        )
        self.assertEqual(created[0].date_of_birth, date(2005, 4, 8))
        self.assertEqual(created[0].status, "Active")
        self.assertIsNone(created[0].user_id)
        self.audit.assert_called_once_with(
            user=self.warden, action="create", record=created[0]
        )

    def test_create_validation_errors_never_write(self):
        for changes in (
            {"year": True},
            {"year": 0},
            {"year": 6},
            {"email": "bad"},
            {"dob": "2026-02-30"},
            {"mobile": "123"},
            {"student_id": "short"},
            {"name": 17},
            {"status": "Inactive"},
            {"user": 10},
        ):
            with self.subTest(changes=changes):
                self.assert_error(
                    api._student_create(self.request("post", self.payload(**changes))),
                    400,
                    "VALIDATION_ERROR",
                )
        self.save.assert_not_called()
        self.audit.assert_not_called()

    def test_create_duplicate_form_error_and_integrity_race(self):
        self.exists.return_value = True
        response = api._student_create(self.request("post", self.payload()))
        self.assert_error(response, 409, "DUPLICATE")
        self.assertIn("student_id", self.body(response)["error"]["fields"])
        self.save.assert_not_called()
        self.exists.side_effect = [False, True]
        self.save.side_effect = IntegrityError("duplicate after validation")
        response = api._student_create(self.request("post", self.payload()))
        self.assert_error(response, 409, "DUPLICATE")
        self.assertNotIn("fields", self.body(response)["error"])
        self.audit.assert_not_called()

    def test_create_requires_dob_even_when_other_fields_are_valid(self):
        payload = self.payload()
        payload.pop("dob")
        response = api._student_create(self.request("post", payload))
        self.assert_error(response, 400, "VALIDATION_ERROR")
        self.assertEqual(
            self.body(response)["error"]["fields"]["date_of_birth"][0]["code"],
            "required",
        )
        self.save.assert_not_called()

    def test_create_unrelated_integrity_error_is_not_hidden_as_duplicate(self):
        self.save.side_effect = IntegrityError("unrelated constraint")
        with self.assertRaisesMessage(IntegrityError, "unrelated constraint"):
            api._student_create(self.request("post", self.payload()))
        self.audit.assert_not_called()

    def test_collection_paginates_25_and_builds_active_hostel_search(self):
        class Rows(list):
            pass

        rows = Rows(
            Student(pk=number, **self.values(name=f"Student {number}"))
            for number in range(1, 28)
        )
        rows.filter = Mock(return_value=rows)
        rows.distinct = Mock(return_value=rows)
        with patch.object(Student.objects, "all", return_value=rows):
            response = api.student_collection(
                self.request("get", {"q": "  Girls  ", "hostel": "7", "page": "2"})
            )
        body = self.body(response)
        self.assertEqual((body["page"], body["total"]), (2, 27))
        self.assertEqual([student["id"] for student in body["results"]], [26, 27])
        rows.filter.assert_any_call(
            Q(student_id__icontains="Girls")
            | Q(name__icontains="Girls")
            | Q(
                allocations__status="Active",
                allocations__bed__room__hostel__name__icontains="Girls",
            )
        )
        rows.filter.assert_any_call(
            allocations__status="Active", allocations__bed__room__hostel_id=7
        )
        self.assertEqual(rows.distinct.call_count, 2)
        self.lookup.assert_called_once_with(Hostel, pk=7)

    def test_collection_rejects_invalid_hostel_id_before_lookup(self):
        for value in ("0", "-1", "bad", str(2**63)):
            with (
                self.subTest(value=value),
                patch.object(Student.objects, "all", return_value=[]),
            ):
                self.assert_error(
                    api.student_collection(self.request("get", {"hostel": value})),
                    400,
                    "invalid" if value == "bad" else "VALIDATION_ERROR",
                )
        self.lookup.assert_not_called()

    def test_collection_empty_and_invalid_page_use_first_page(self):
        with patch.object(Student.objects, "all", return_value=[]):
            response = api.student_collection(self.request("get", {"page": "bad"}))
        self.assertEqual(self.body(response), {"results": [], "page": 1, "total": 0})

    def test_update_real_form_keeps_identity_status_and_uneditable_fields(self):
        payload = {
            "mobile": "9000000000",
            "course": "Mathematics",
            "year": 3,
            "address": "New address",
        }
        response = api.student_update(self.request("patch", payload), 41)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(self.body(response)["student"]["mobile"], "9000000000")
        self.assertEqual(self.student.student_id, "PES1UG24CS163")
        self.assertEqual(self.student.name, "Ananya Rao")
        self.assertEqual(self.student.status, "Active")
        self.save.assert_called_once_with(
            self.student,
            update_fields={
                "mobile",
                "email",
                "course",
                "year",
                "guardian_name",
                "guardian_mobile",
                "address",
                "updated_at",
            },
        )
        self.audit.assert_called_once_with(
            user=self.warden, action="update", record=self.student
        )

    def test_update_same_values_and_same_student_id_do_not_write(self):
        response = api.student_update(
            self.request(
                "patch",
                {"student_id": self.student.student_id, "mobile": self.student.mobile},
            ),
            41,
        )
        self.assertEqual(response.status_code, 200)
        self.save.assert_not_called()
        self.audit.assert_not_called()

    def test_update_identity_change_is_conflict_without_form_or_write(self):
        response = api.student_update(
            self.request(
                "patch", {"student_id": "PES1UG24CS164", "mobile": "9000000000"}
            ),
            41,
        )
        self.assert_error(response, 422, "IMMUTABLE_FIELD")
        self.assertEqual(self.student.mobile, "9876543210")
        self.save.assert_not_called()
        self.audit.assert_not_called()

    def test_update_rejects_empty_unknown_wrong_type_and_invalid_form(self):
        for payload in (
            {},
            {"status": "Inactive"},
            {"name": "Changed"},
            {"year": True},
            {"email": 3},
            {"year": 6},
            {"guardian_mobile": "1"},
        ):
            with self.subTest(payload=payload):
                self.assert_error(
                    api.student_update(self.request("patch", payload), 41),
                    400,
                    "VALIDATION_ERROR",
                )
        self.save.assert_not_called()
        self.audit.assert_not_called()

    def test_deactivate_conflict_names_bed_and_does_not_write(self):
        with patch.object(QuerySet, "first", return_value=self.allocation()):
            response = api.student_deactivate(self.request("post", {}), 41)
        self.assert_error(response, 409, "HAS_ACTIVE_ALLOCATION")
        self.assertEqual(
            self.body(response)["error"]["message"],
            "Release active bed 204-A before deactivation.",
        )
        self.assertEqual(self.student.status, "Active")
        self.save.assert_not_called()
        self.audit.assert_not_called()

    def test_deactivate_changes_only_status_and_timestamp_once(self):
        with patch.object(QuerySet, "first", return_value=None):
            response = api.student_deactivate(self.request("post", {}), 41)
            repeated = api.student_deactivate(self.request("post", {}), 41)
        self.assertEqual(self.body(response), {"status": "Inactive"})
        self.assertEqual(self.body(repeated), {"status": "Inactive"})
        self.save.assert_called_once_with(
            self.student, update_fields={"status", "updated_at"}
        )
        self.audit.assert_called_once_with(
            user=self.warden, action="deactivate", record=self.student
        )

    def test_deactivate_accepts_empty_json_body_and_empty_form_post(self):
        requests = [
            self.factory.generic(
                "POST", "/students/41/deactivate/", CONTENT_TYPE="application/json"
            ),
            self.factory.post("/students/41/deactivate/", {}),
        ]
        with patch.object(QuerySet, "first", return_value=None):
            for request in requests:
                request.user = self.warden
                self.assertEqual(
                    self.body(api.student_deactivate(request, 41)),
                    {"status": "Inactive"},
                )
        self.save.assert_called_once_with(
            self.student, update_fields={"status", "updated_at"}
        )

    def test_deactivate_rejects_body_fields_without_looking_up_student(self):
        self.assert_error(
            api.student_deactivate(self.request("post", {"status": "Inactive"}), 41),
            400,
            "VALIDATION_ERROR",
        )
        self.lookup.assert_not_called()
        self.save.assert_not_called()

    def test_self_service_unlinked_profile_is_empty_and_query_is_scoped(self):
        user = User(pk=81, role="student")
        with (
            patch.object(
                Student.objects, "filter", wraps=Student.objects.filter
            ) as lookup,
            patch.object(QuerySet, "first", return_value=None),
        ):
            response = api.my_records(
                self.request("get", {"student_id": "someone-else"}, user=user)
            )
        lookup.assert_called_once_with(user_id=81)
        self.assertEqual(
            self.body(response),
            {"profile": None, "allocation": None, "payment_status": None},
        )

    def test_self_service_serializes_real_allocation_and_calculates_status(self):
        user = User(pk=81, role="student")
        self.student.fee_amount = Decimal("1000.00")
        self.student.amount_paid = Decimal("400.00")
        self.student.billing_hostel_id = 7
        self.student.billing_hostel = "Girls Hostel"
        self.student.billing_room = "204"
        self.student.billing_bed = "204-A"
        for allocation in (None, self.allocation()):
            with (
                self.subTest(allocation=allocation),
                patch.object(QuerySet, "first", side_effect=[self.student, allocation]),
            ):
                response = api.my_records(self.request("get", {}, user=user))
            result = self.body(response)
            self.assertEqual(result["profile"]["id"], 41)
            self.assertEqual(result["payment_status"]["status"], "Partial")
            self.assertEqual(result["payment_status"]["due"], "600.00")
            self.assertEqual(
                result["allocation"],
                None
                if allocation is None
                else {
                    "allocation_id": 11,
                    "bed_id": 9,
                    "bed": "204-A",
                    "room": "204",
                    "hostel": "Girls Hostel",
                    "allocated_on": "2026-08-01",
                },
            )

    def test_audit_failure_exits_atomic_with_error_for_each_mutation(self):
        exits = []

        class AtomicBoundary:
            def __enter__(self):
                return self

            def __exit__(self, exception_type, exception, traceback):
                exits.append(exception_type)
                return False

        self.atomic.side_effect = AtomicBoundary
        self.audit.side_effect = RuntimeError("audit unavailable")
        with patch.object(QuerySet, "first", return_value=None):
            for view, args in (
                (api._student_create, (self.request("post", self.payload()),)),
                (
                    api.student_update,
                    (self.request("patch", {"mobile": "9000000000"}), 41),
                ),
                (api.student_deactivate, (self.request("post", {}), 41)),
            ):
                with (
                    self.subTest(view=view.__name__),
                    self.assertRaisesMessage(RuntimeError, "audit unavailable"),
                ):
                    view(*args)
        self.assertEqual(exits, [RuntimeError, RuntimeError, RuntimeError])
