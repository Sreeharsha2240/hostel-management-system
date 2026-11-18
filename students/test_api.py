"""SAD student JSON contracts, privacy, validation and transactional audit."""

from decimal import Decimal
from unittest.mock import patch

from django.forms.models import model_to_dict
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import User
from allocations.models import Allocation
from allocations.services import allocate, release
from audit.models import AuditEvent
from hostels.models import Hostel
from payments.services import record_payment
from tests.factories import make_room, make_student

from .forms import StudentForm
from .models import Student


class StudentApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            username="student-json-admin", role=User.Role.ADMIN
        )
        cls.warden = User.objects.create_user(
            username="student-json-warden", role=User.Role.WARDEN
        )
        cls.student_user = User.objects.create_user(
            username="student-json-login", role=User.Role.STUDENT
        )

    def setUp(self):
        self.student = make_student(821, user=self.student_user)
        self.client.force_login(self.warden)

    def payload(self, **changes):
        values = model_to_dict(self.student)
        data = {
            key: value
            for key, value in values.items()
            if key not in {"id", "user", "status", "date_of_birth"}
        }
        data["dob"] = self.student.date_of_birth.isoformat()
        data["student_id"] = "PES0000000822"
        data.update(changes)
        return data

    def create(self, data):
        return self.client.post(
            reverse("student-list"), data, content_type="application/json"
        )

    def patch_student(self, data, pk=None):
        return self.client.patch(
            reverse("api-student-update", args=[pk or self.student.pk]),
            data,
            content_type="application/json",
        )

    def deactivate(self, pk=None):
        return self.client.post(
            reverse("student-deactivate", args=[pk or self.student.pk]),
            {},
            content_type="application/json",
        )

    def allocation(self, student=None, name="Student API hostel"):
        hostel = Hostel.objects.create(name=name, hostel_type="Boys")
        room = make_room(hostel=hostel, fee_amount=Decimal("1000.00"))
        return allocate(
            student=student or self.student, bed=room.beds.first(), actor=self.warden
        )

    def test_create_uses_sad_dob_and_returns_identifiers_with_audit(self):
        response = self.create(self.payload())
        self.assertEqual(response.status_code, 201)
        student = Student.objects.get(pk=response.json()["id"])
        self.assertEqual(response.json()["student_id"], student.student_id)
        self.assertEqual(student.date_of_birth, self.student.date_of_birth)
        self.assertEqual(student.status, Student.Status.ACTIVE)
        self.assertIsNone(student.user_id)
        self.assertTrue(
            AuditEvent.objects.filter(
                user=self.warden,
                action="create",
                record_type="students.student",
                record_id=str(student.pk),
            ).exists()
        )

    def test_create_rejects_duplicate_invalid_date_year_types_and_extra_fields(self):
        for changes, status in (
            ({"student_id": self.student.student_id.lower()}, 409),
            ({"dob": "not-a-date"}, 400),
            ({"year": True}, 400),
            ({"year": 2.0}, 400),
            ({"year": "2"}, 400),
            ({"year": 6}, 400),
            ({"mobile": 9876543210}, 400),
            ({"status": "Inactive"}, 400),
            ({"user": self.student_user.pk}, 400),
            ({"name": {"value": "nested"}}, 400),
        ):
            with self.subTest(changes=changes):
                response = self.create(self.payload(**changes))
                self.assertEqual(response.status_code, status)
        self.assertEqual(Student.objects.count(), 1)

    def test_partial_update_preserves_identity_status_and_unsubmitted_fields(self):
        response = self.patch_student({"mobile": "9000000000", "year": 4})
        self.assertEqual(response.status_code, 200)
        self.student.refresh_from_db()
        self.assertEqual(self.student.mobile, "9000000000")
        self.assertEqual(self.student.year, 4)
        self.assertEqual(self.student.user_id, self.student_user.pk)
        self.assertEqual(self.student.status, Student.Status.ACTIVE)
        self.assertEqual(
            response.json()["student"]["dob"], self.student.date_of_birth.isoformat()
        )
        self.assertTrue(
            AuditEvent.objects.filter(
                user=self.warden, action="update", record_id=str(self.student.pk)
            ).exists()
        )

    def test_patch_rejects_immutable_id_unknown_fields_and_invalid_scalars(self):
        response = self.patch_student({"student_id": "PES0000000999"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "IMMUTABLE_FIELD")
        for data in (
            {},
            {"year": True},
            {"year": 1.5},
            {"status": "Inactive"},
            {"gender": "Female"},
            {"user": self.admin.pk},
            {"mobile": None},
            {"course": ["CS"]},
        ):
            with self.subTest(data=data):
                self.assertEqual(self.patch_student(data).status_code, 400)
        self.assertEqual(
            self.patch_student({"mobile": "9000000000"}, 999999).status_code, 404
        )

    def test_search_and_hostel_filter_use_only_current_allocations(self):
        allocation = self.allocation()
        other = make_student(823)
        other_allocation = self.allocation(other, "Other API hostel")
        response = self.client.get(
            reverse("student-list"),
            {"hostel": allocation.bed.room.hostel_id},
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [row["id"] for row in response.json()["results"]], [self.student.pk]
        )
        for query in (
            self.student.student_id,
            self.student.name[1:],
            "Student API hostel",
        ):
            response = self.client.get(
                reverse("student-list"),
                {"q": query, "hostel": allocation.bed.room.hostel_id},
                HTTP_ACCEPT="application/json",
            )
            self.assertEqual(response.json()["total"], 1)
        release(allocation_id=allocation.pk, actor=self.warden)
        response = self.client.get(
            reverse("student-list"),
            {"hostel": allocation.bed.room.hostel_id},
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.json()["total"], 0)
        self.assertTrue(
            Allocation.objects.filter(pk=other_allocation.pk, status="Active").exists()
        )
        self.assertEqual(
            self.client.get(
                reverse("student-list"),
                {"hostel": "invalid"},
                HTTP_ACCEPT="application/json",
            ).status_code,
            400,
        )
        self.assertEqual(
            self.client.get(
                reverse("student-list"),
                {"hostel": 999999},
                HTTP_ACCEPT="application/json",
            ).status_code,
            404,
        )

    def test_list_json_is_paginated_while_browser_route_remains_html(self):
        for number in range(830, 856):
            make_student(number)
        response = self.client.get(
            reverse("student-list"), {"page": 2}, HTTP_ACCEPT="application/json"
        )
        self.assertEqual(response.json()["page"], 2)
        self.assertEqual(response.json()["total"], 27)
        self.assertEqual(len(response.json()["results"]), 2)
        browser = self.client.get(reverse("student-list"))
        self.assertTrue(browser["Content-Type"].startswith("text/html"))

    def test_deactivation_conflict_identifies_bed_then_succeeds_after_release(self):
        allocation = self.allocation()
        response = self.deactivate()
        self.assertEqual(response.status_code, 409)
        self.assertIn(allocation.bed.label, response.json()["error"]["message"])
        release(allocation_id=allocation.pk, actor=self.warden)
        response = self.deactivate()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "Inactive"})
        self.assertEqual(self.deactivate().status_code, 200)
        self.assertEqual(
            AuditEvent.objects.filter(
                action="deactivate",
                record_type="students.student",
                record_id=str(self.student.pk),
            ).count(),
            1,
        )

    def test_all_student_management_json_routes_require_staff_role(self):
        for actor, expected in ((None, 401), (self.student_user, 403)):
            with self.subTest(actor=actor):
                self.client.logout()
                if actor is not None:
                    self.client.force_login(actor)
                self.assertEqual(
                    self.client.get(
                        reverse("student-list"), HTTP_ACCEPT="application/json"
                    ).status_code,
                    expected,
                )
                self.assertEqual(self.create(self.payload()).status_code, expected)
                self.assertEqual(
                    self.patch_student({"mobile": "9000000000"}).status_code, expected
                )
                self.assertEqual(self.deactivate().status_code, expected)

    def test_self_service_returns_only_linked_profile_allocation_and_balance(self):
        allocation = self.allocation()
        record_payment(
            actor=self.warden,
            student=self.student,
            amount=Decimal("400.00"),
            date=allocation.allocated_on,
            mode="Cash",
        )
        other = make_student(824)
        self.allocation(other, "Private other hostel")
        self.client.force_login(self.student_user)

        response = self.client.get(
            reverse("api-student-self-service"), {"student_id": other.pk}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["profile"]["id"], self.student.pk)
        self.assertEqual(data["allocation"]["allocation_id"], allocation.pk)
        self.assertEqual(data["payment_status"]["status"], "Partial")
        self.assertEqual(data["payment_status"]["paid"], "400.00")
        self.assertNotIn(other.student_id, response.content.decode())
        self.assertNotIn("Private other hostel", response.content.decode())

    def test_self_service_requires_student_and_unlinked_login_is_empty(self):
        self.assertEqual(
            self.client.get(reverse("api-student-self-service")).status_code, 403
        )
        self.client.logout()
        self.assertEqual(
            self.client.get(reverse("api-student-self-service")).status_code, 401
        )
        unlinked = User.objects.create_user(username="unlinked-json", role="student")
        self.client.force_login(unlinked)
        self.assertEqual(
            self.client.get(reverse("api-student-self-service")).json(),
            {"profile": None, "allocation": None, "payment_status": None},
        )

    def test_audit_failure_rolls_back_student_changes(self):
        with patch(
            "students.api.record_event", side_effect=RuntimeError("audit unavailable")
        ):
            with self.assertRaises(RuntimeError):
                self.create(self.payload())
            with self.assertRaises(RuntimeError):
                self.patch_student({"mobile": "9111111111"})
            with self.assertRaises(RuntimeError):
                self.deactivate()
        self.student.refresh_from_db()
        self.assertNotEqual(self.student.mobile, "9111111111")
        self.assertEqual(self.student.status, Student.Status.ACTIVE)
        self.assertEqual(Student.objects.count(), 1)

    def test_create_duplicate_race_returns_409_and_html_bound_error(self):
        for module, json_mode in (("students.api", True), ("students.views", False)):
            with self.subTest(module=module):
                payload = self.payload(
                    student_id="PES0000000825" if json_mode else "PES0000000826"
                )
                values = payload.copy()
                values["date_of_birth"] = values.pop("dob")
                values["status"] = "Active"
                form = StudentForm(values)
                self.assertTrue(form.is_valid(), form.errors)
                make_student(
                    825 if json_mode else 826, student_id=payload["student_id"]
                )
                with patch(f"{module}.StudentForm", return_value=form):
                    response = (
                        self.create(payload)
                        if json_mode
                        else self.client.post(reverse("student-create"), values)
                    )
                self.assertEqual(response.status_code, 409 if json_mode else 200)
                if not json_mode:
                    self.assertIn("student_id", response.context["form"].errors)

    def test_student_json_writes_require_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.warden)
        for method, url, payload in (
            ("post", reverse("student-list"), self.payload()),
            (
                "patch",
                reverse("api-student-update", args=[self.student.pk]),
                {"mobile": "9000000000"},
            ),
            ("post", reverse("student-deactivate", args=[self.student.pk]), {}),
        ):
            with self.subTest(method=method, url=url):
                self.assertEqual(
                    getattr(client, method)(
                        url, payload, content_type="application/json"
                    ).status_code,
                    403,
                )
        self.student.refresh_from_db()
        self.assertEqual(self.student.status, "Active")
        self.assertEqual(Student.objects.count(), 1)

    def test_multipart_deactivation_with_json_accept_and_csrf_stays_json(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.warden)
        client.get(reverse("settings"))

        response = client.post(
            reverse("student-deactivate", args=[self.student.pk]),
            {},
            HTTP_ACCEPT="application/json",
            HTTP_X_CSRFTOKEN=client.cookies["csrftoken"].value,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "Inactive"})
