"""Exercise allocation error paths with real request parsing and form validation."""

import json
from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.messages import get_messages
from django.contrib.messages.storage.cookie import CookieStorage
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase
from django.urls import reverse

from accounts.models import User
from hostels.models import Bed, Hostel, Room
from students.models import Student

from .models import Allocation
from .views import (
    allocation_complete,
    allocation_create,
    allocation_release,
    allocation_transfer,
)


class AllocationViewErrorUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = SimpleNamespace(is_authenticated=True, role=User.Role.WARDEN)
        self.student = Student(pk=12, student_id="STUDENT000012", name="Student Twelve")
        hostel = Hostel(pk=2, name="North Hostel")
        room = Room(pk=3, hostel=hostel, room_number="101")
        self.bed = Bed(pk=5, room=room, label="101-A")
        self.new_bed = Bed(pk=6, room=room, label="101-B")
        self.allocation = Allocation(
            pk=8,
            student=self.student,
            bed=self.bed,
            allocated_on=date(2026, 11, 1),
            status=Allocation.AllocationStatus.ACTIVE,
        )
        self.choice_reads = []

    def request(self, payload, *, json_input=True, url_name="allocation-release"):
        request = (
            self.factory.post(
                "/allocations/test/",
                data=json.dumps(payload),
                content_type="application/json",
            )
            if json_input
            else self.factory.post("/allocations/test/", payload)
        )
        request.user = self.user
        request.resolver_match = SimpleNamespace(url_name=url_name)
        request._messages = CookieStorage(request)
        return request

    def choice_lookup(self, queryset, **kwargs):
        """Replace the database get used by real ModelChoiceFields."""
        self.choice_reads.append((queryset.model, kwargs))
        choices = {
            (Student, "12"): self.student,
            (Bed, "5"): self.bed,
            (Bed, "6"): self.new_bed,
        }
        self.assertEqual(set(kwargs), {"pk"})
        return choices[(queryset.model, str(kwargs["pk"]))]

    def expected_payload(self, *, released=False):
        return {
            "allocation_id": 8,
            "student_id": self.student.student_id,
            "bed_id": 5,
            "bed": "101-A",
            "hostel": "North Hostel",
            "status": "Released" if released else "Active",
            "allocated_on": "2026-11-01",
            "vacated_on": "2026-11-12" if released else None,
        }

    @patch("allocations.views.allocate")
    @patch("allocations.views.Student.objects.filter")
    def test_non_string_public_student_identifiers_cannot_use_internal_student_key(
        self, students, allocate
    ):
        for identifier in (None, 12, True, 12.5):
            with self.subTest(identifier=identifier):
                response = allocation_create(
                    self.request({"student_id": identifier, "student": 12, "bed_id": 5})
                )

                self.assertEqual(response.status_code, 404)
                self.assertEqual(
                    json.loads(response.content),
                    {"error": {"code": "NOT_FOUND", "message": "Student not found."}},
                )
        students.assert_not_called()
        allocate.assert_not_called()

    @patch("allocations.views.allocate")
    @patch("allocations.views.transfer")
    @patch("allocations.views.release")
    @patch("allocations.views.get_object_or_404")
    def test_write_views_return_json_parse_errors_before_invoking_services(
        self, lookup, release, transfer, allocate
    ):
        lookup.return_value = self.allocation
        for view, args in (
            (allocation_create, ()),
            (allocation_transfer, (8,)),
            (allocation_release, (8,)),
        ):
            with self.subTest(view=view.__name__):
                request = self.factory.post(
                    "/allocations/test/",
                    data="{broken",
                    content_type="application/json",
                )
                request.user = self.user
                request.resolver_match = SimpleNamespace(url_name="allocation-release")

                response = view(request, *args)

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    json.loads(response.content),
                    {
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "message": "Enter a valid JSON object.",
                        }
                    },
                )
        allocate.assert_not_called()
        transfer.assert_not_called()
        release.assert_not_called()

    @patch("allocations.views.allocate")
    @patch("allocations.views.Student.objects.filter")
    def test_public_json_identifiers_override_conflicting_internal_form_keys(
        self, students, allocate
    ):
        students.return_value.first.return_value = self.student
        allocate.return_value = self.allocation
        with patch(
            "django.db.models.query.QuerySet.get",
            autospec=True,
            side_effect=self.choice_lookup,
        ):
            response = allocation_create(
                self.request(
                    {
                        "student_id": self.student.student_id,
                        "student": 999,
                        "bed_id": 5,
                        "bed": 999,
                        "allocated_on": "2026-11-01",
                    }
                )
            )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content), self.expected_payload())
        students.assert_called_once_with(student_id=self.student.student_id)
        self.assertEqual(self.choice_reads, [(Student, {"pk": 12}), (Bed, {"pk": 5})])
        allocate.assert_called_once_with(
            actor=self.user,
            student=self.student,
            bed=self.bed,
            allocated_on=date(2026, 11, 1),
        )

    @patch("allocations.views.render", return_value=HttpResponse("invalid allocation"))
    @patch(
        "allocations.views.allocate",
        side_effect=ValidationError(["Student is inactive.", "Bed is unavailable."]),
    )
    def test_html_create_retains_bound_form_and_domain_errors(self, allocate, render):
        request = self.request(
            {"student": "12", "bed": "5", "allocated_on": "2026-11-01"},
            json_input=False,
        )
        with patch(
            "django.db.models.query.QuerySet.get",
            autospec=True,
            side_effect=self.choice_lookup,
        ):
            response = allocation_create(request)

        self.assertIs(response, render.return_value)
        rendered_request, template, context = render.call_args.args
        self.assertIs(rendered_request, request)
        self.assertEqual(template, "allocations/allocation_form.html")
        self.assertEqual(context["heading"], "Create Hostel Allocation")
        self.assertTrue(context["form"].is_bound)
        self.assertEqual(context["form"].data, request.POST)
        self.assertEqual(
            list(context["form"].non_field_errors()),
            ["Student is inactive.; Bed is unavailable."],
        )
        allocate.assert_called_once_with(
            actor=self.user,
            student=self.student,
            bed=self.bed,
            allocated_on=date(2026, 11, 1),
        )

    @patch("allocations.views.transfer")
    @patch("allocations.views.get_object_or_404")
    def test_transfer_invalid_reference_uses_real_form_error_statuses(
        self, lookup, transfer
    ):
        lookup.return_value = self.allocation
        for value, status, code, field_code in (
            (None, 400, "VALIDATION_ERROR", "required"),
            (True, 404, "NOT_FOUND", "invalid_choice"),
            (6.5, 404, "NOT_FOUND", "invalid_choice"),
        ):
            with self.subTest(new_bed_id=value):
                response = allocation_transfer(self.request({"new_bed_id": value}), 8)

                self.assertEqual(response.status_code, status)
                error = json.loads(response.content)["error"]
                self.assertEqual(error["code"], code)
                self.assertEqual(
                    error["message"], "Please correct the highlighted fields."
                )
                self.assertEqual(set(error["fields"]), {"new_bed"})
                self.assertEqual(error["fields"]["new_bed"][0]["code"], field_code)
        transfer.assert_not_called()

    @patch("allocations.views.get_object_or_404")
    @patch(
        "allocations.views.transfer",
        side_effect=ValidationError("Hostel is inactive.", code="INACTIVE_HOSTEL"),
    )
    def test_transfer_service_validation_maps_to_json_without_losing_error_code(
        self, transfer, lookup
    ):
        lookup.return_value = self.allocation
        with patch(
            "django.db.models.query.QuerySet.get",
            autospec=True,
            side_effect=self.choice_lookup,
        ):
            response = allocation_transfer(self.request({"new_bed_id": 6}), 8)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.content),
            {"error": {"code": "INACTIVE_HOSTEL", "message": "Hostel is inactive."}},
        )
        self.assertEqual(self.choice_reads, [(Bed, {"pk": 6})])
        transfer.assert_called_once_with(
            allocation_id=8, actor=self.user, new_bed=self.new_bed
        )

    @patch("allocations.views.transfer")
    @patch("allocations.views.get_object_or_404")
    def test_html_transfer_redirects_and_adds_history_preservation_message(
        self, lookup, transfer
    ):
        lookup.return_value = self.allocation
        request = self.request({"new_bed": "6"}, json_input=False)
        with patch(
            "django.db.models.query.QuerySet.get",
            autospec=True,
            side_effect=self.choice_lookup,
        ):
            response = allocation_transfer(request, 8)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("allocation-list"))
        self.assertEqual(
            [str(message) for message in get_messages(request)],
            ["Transfer completed; allocation history is preserved."],
        )
        transfer.assert_called_once_with(
            allocation_id=8, actor=self.user, new_bed=self.new_bed
        )

    @patch("allocations.views.render", return_value=HttpResponse("invalid transfer"))
    @patch("allocations.views.get_object_or_404")
    @patch(
        "allocations.views.transfer",
        side_effect=ValidationError(
            "Allocation was already released.", code="ALREADY_RELEASED"
        ),
    )
    def test_html_transfer_domain_error_preserves_confirmation_context(
        self, transfer, lookup, render
    ):
        lookup.return_value = self.allocation
        request = self.request({"new_bed": "6"}, json_input=False)
        with patch(
            "django.db.models.query.QuerySet.get",
            autospec=True,
            side_effect=self.choice_lookup,
        ):
            response = allocation_transfer(request, 8)

        self.assertIs(response, render.return_value)
        rendered_request, template, context = render.call_args.args
        self.assertIs(rendered_request, request)
        self.assertEqual(template, "allocations/allocation_form.html")
        self.assertEqual(context["heading"], "Transfer Allocation")
        self.assertIs(context["allocation"], self.allocation)
        self.assertEqual(context["confirmation_message"], "Transfer this allocation?")
        self.assertEqual(
            list(context["form"].non_field_errors()),
            ["Allocation was already released."],
        )
        self.assertEqual(context["form"].data, request.POST)
        transfer.assert_called_once_with(
            allocation_id=8, actor=self.user, new_bed=self.new_bed
        )

    @patch("allocations.views.get_object_or_404")
    @patch(
        "allocations.views.release",
        side_effect=ValidationError(
            "Allocation was already released.", code="ALREADY_RELEASED"
        ),
    )
    def test_release_domain_conflict_returns_json_error_and_parsed_date(
        self, release, lookup
    ):
        lookup.return_value = self.allocation

        response = allocation_release(self.request({"vacate_date": "2026-11-12"}), 8)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            json.loads(response.content),
            {
                "error": {
                    "code": "ALREADY_RELEASED",
                    "message": "Allocation was already released.",
                }
            },
        )
        release.assert_called_once_with(
            allocation_id=8, actor=self.user, vacate_date=date(2026, 11, 12)
        )

    @patch("allocations.views.timezone.localdate")
    @patch("allocations.views.release")
    @patch("allocations.views.get_object_or_404")
    def test_completion_preserves_explicit_date_and_serializes_completed_record(
        self, lookup, release, today
    ):
        lookup.return_value = self.allocation
        self.allocation.status = Allocation.AllocationStatus.COMPLETED
        self.allocation.vacated_on = date(2026, 11, 12)
        release.return_value = self.allocation

        response = allocation_complete(
            self.request({"vacate_date": "2026-11-12"}, url_name="allocation-complete"),
            8,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content), self.expected_payload(released=True)
        )
        self.assertEqual(self.allocation.status, Allocation.AllocationStatus.COMPLETED)
        today.assert_not_called()
        release.assert_called_once_with(
            allocation_id=8, actor=self.user, vacate_date=date(2026, 11, 12)
        )

    @patch("allocations.views.timezone.localdate")
    @patch("allocations.views.release")
    @patch("allocations.views.get_object_or_404")
    def test_release_requires_date_and_completion_does_not_replace_explicit_blank(
        self, lookup, release, today
    ):
        lookup.return_value = self.allocation
        for view, payload, url_name in (
            (allocation_release, {}, "allocation-release"),
            (allocation_complete, {"vacate_date": ""}, "allocation-complete"),
        ):
            with self.subTest(route=url_name):
                response = view(self.request(payload, url_name=url_name), 8)

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    json.loads(response.content),
                    {
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "message": "Please correct the highlighted fields.",
                            "fields": {
                                "vacate_date": [
                                    {
                                        "message": "This field is required.",
                                        "code": "required",
                                    }
                                ]
                            },
                        }
                    },
                )
        today.assert_not_called()
        release.assert_not_called()

    @patch("allocations.views.get_object_or_404")
    def test_completion_rejects_get_before_looking_up_an_allocation(self, lookup):
        request = self.factory.get("/allocations/8/complete/")
        request.user = self.user

        response = allocation_complete(request, 8)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response["Allow"], "POST")
        lookup.assert_not_called()

    @patch("allocations.views.release")
    @patch("allocations.views.get_object_or_404")
    def test_html_release_redirects_and_adds_success_message(self, lookup, release):
        lookup.return_value = self.allocation
        request = self.request({"vacate_date": "2026-11-12"}, json_input=False)

        response = allocation_release(request, 8)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("allocation-list"))
        self.assertEqual(
            [str(message) for message in get_messages(request)],
            ["Allocation released."],
        )
        release.assert_called_once_with(
            allocation_id=8, actor=self.user, vacate_date=date(2026, 11, 12)
        )

    @patch("allocations.views.render", return_value=HttpResponse("invalid release"))
    @patch("allocations.views.get_object_or_404")
    @patch(
        "allocations.views.release",
        side_effect=ValidationError("Cannot release before allocation."),
    )
    def test_html_release_domain_error_retains_date_and_confirmation_context(
        self, release, lookup, render
    ):
        lookup.return_value = self.allocation
        request = self.request({"vacate_date": "2026-10-31"}, json_input=False)

        response = allocation_release(request, 8)

        self.assertIs(response, render.return_value)
        rendered_request, template, context = render.call_args.args
        self.assertIs(rendered_request, request)
        self.assertEqual(template, "allocations/allocation_form.html")
        self.assertEqual(context["heading"], "Release Allocation")
        self.assertIs(context["allocation"], self.allocation)
        self.assertEqual(context["confirmation_message"], "Release this allocation?")
        self.assertEqual(context["form"].data, request.POST)
        self.assertEqual(
            list(context["form"].non_field_errors()),
            ["Cannot release before allocation."],
        )
        release.assert_called_once_with(
            allocation_id=8, actor=self.user, vacate_date=date(2026, 10, 31)
        )
