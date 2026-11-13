"""Isolated checks of form rules and report aggregation contracts."""

import csv
import io
import json
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import RequestFactory, SimpleTestCase

from accounts.forms import AccountUpdateForm
from accounts.models import User
from hostels.forms import BedFilterForm, RoomForm
from hostels.models import Room
from payments.forms import AdjustmentForm, PaymentForm
from reports.services import occupancy_rows, payment_status_rows
from reports.views import report_response
from students.forms import StudentForm


class FormRuleUnitTests(SimpleTestCase):
    def test_bed_filter_accepts_exact_storage_boundaries(self):
        form = BedFilterForm({"hostel": str(2**63 - 1), "floor": "65535"})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data, {"hostel": 2**63 - 1, "floor": 65535})
        self.assertTrue(BedFilterForm({"floor": "0"}).is_valid())

    def test_bed_filter_rejects_out_of_range_identifiers(self):
        for data, field in (
            ({"hostel": "0"}, "hostel"),
            ({"hostel": str(2**63)}, "hostel"),
            ({"floor": "-1"}, "floor"),
            ({"floor": "65536"}, "floor"),
        ):
            with self.subTest(data=data):
                form = BedFilterForm(data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_room_fee_preserves_existing_value_only_when_blank(self):
        form = RoomForm(instance=Room(fee_amount=Decimal("1200")))
        for value, expected in (
            (None, Decimal("1200")),
            (Decimal("0"), Decimal("0")),
            (Decimal("1500"), Decimal("1500")),
        ):
            with self.subTest(value=value):
                form.cleaned_data = {"fee_amount": value}
                self.assertEqual(form.clean_fee_amount(), expected)

    def test_superuser_must_keep_admin_role(self):
        form = AccountUpdateForm(instance=User(is_superuser=True))
        form.cleaned_data = {"role": User.Role.STUDENT}
        with self.assertRaises(ValidationError):
            form.clean_role()
        form.cleaned_data = {"role": User.Role.ADMIN}
        self.assertEqual(form.clean_role(), User.Role.ADMIN)
        form.instance.is_superuser = False
        form.cleaned_data = {"role": User.Role.STUDENT}
        self.assertEqual(form.clean_role(), User.Role.STUDENT)

    @patch("students.forms.Student.objects.filter")
    def test_student_id_is_normalized_and_excludes_current_record(self, query):
        form = StudentForm.__new__(StudentForm)
        form.cleaned_data = {"student_id": "abc123def456g"}
        form.instance = SimpleNamespace(pk=7)
        query.return_value.exclude.return_value.exists.return_value = False
        self.assertEqual(form.clean_student_id(), "ABC123DEF456G")
        query.assert_called_once_with(student_id__iexact="ABC123DEF456G")
        query.return_value.exclude.assert_called_once_with(pk=7)

    @patch("students.forms.Student.objects.filter")
    def test_duplicate_student_id_is_rejected(self, query):
        form = StudentForm.__new__(StudentForm)
        form.cleaned_data = {"student_id": "abc123def456g"}
        form.instance = SimpleNamespace(pk=None)
        query.return_value.exists.return_value = True
        with self.assertRaisesMessage(ValidationError, "Student ID already registered"):
            form.clean_student_id()

    def test_payment_amount_and_reference_field_validation(self):
        form = PaymentForm()
        with self.assertRaises(ValidationError):
            form.fields["amount"].clean("0")
        self.assertEqual(form.fields["amount"].clean("1.25"), Decimal("1.25"))
        with self.assertRaises(ValidationError):
            form.fields["reference"].clean("bad-ref!")
        self.assertEqual(form.fields["reference"].clean("UPI123"), "UPI123")

    def test_adjustment_accepts_negative_amount_and_requires_reason(self):
        form = AdjustmentForm()
        self.assertNotIn("student", form.fields)
        self.assertEqual(form.fields["amount"].clean("-12.50"), Decimal("-12.50"))
        with self.assertRaises(ValidationError):
            form.fields["adjustment_reason"].clean(" ")


class ReportAggregationUnitTests(SimpleTestCase):
    @patch("reports.services.Allocation.objects.filter")
    @patch("reports.services.Bed.objects.all")
    @patch("reports.services.Hostel.objects.all")
    def test_occupancy_handles_populated_and_empty_hostels(self, hostels, beds, active):
        hostels.return_value = [
            SimpleNamespace(pk=1, name="A"),
            SimpleNamespace(pk=2, name="Empty"),
        ]
        chain = beds.return_value.annotate.return_value.order_by.return_value.values.return_value
        chain.annotate.return_value = [
            {
                "room__hostel_id": 1,
                "total": 3,
                "occupied": 1,
                "available": 1,
                "maintenance": 1,
            }
        ]
        rows = occupancy_rows()
        self.assertEqual(rows[0]["occupancy_percent"], "33.33")
        self.assertEqual(
            (rows[0]["available_beds"], rows[0]["maintenance_beds"]), (1, 1)
        )
        self.assertEqual(
            (rows[1]["total_beds"], rows[1]["occupancy_percent"]), (0, "0.00")
        )
        active.assert_called_once()

    @patch("reports.services.Allocation.objects.filter")
    @patch("reports.services.Bed.objects.all")
    @patch("reports.services.Hostel.objects.all")
    def test_occupancy_filters_both_hostels_and_beds(self, hostels, beds, active):
        hostels.return_value.filter.return_value = []
        chain = beds.return_value.filter.return_value.annotate.return_value.order_by.return_value.values.return_value
        chain.annotate.return_value = []
        self.assertEqual(occupancy_rows(4), [])
        hostels.return_value.filter.assert_called_once_with(pk=4)
        beds.return_value.filter.assert_called_once_with(room__hostel_id=4)
        active.assert_called_once()

    @patch("reports.services.status_row")
    @patch("reports.services.payment_status_queryset")
    def test_payment_report_filters_before_converting_rows(self, queryset, status):
        ordered = queryset.return_value.order_by.return_value
        ordered.filter.return_value = ["student"]
        status.return_value = {"student_id": "S1"}
        self.assertEqual(payment_status_rows(4), [{"student_id": "S1"}])
        ordered.filter.assert_called_once_with(billing_hostel_id=4)
        status.assert_called_once_with("student")


class ReportResponseUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch("reports.views.occupancy_rows")
    def test_invalid_hostel_ids_and_format_return_validation_error(self, rows):
        for query in (
            {"hostel": "0"},
            {"hostel": "-1"},
            {"hostel": "١"},
            {"hostel": str(2**63)},
            {"format": "pdf"},
        ):
            with self.subTest(query=query):
                response = report_response(
                    self.factory.get("/reports/", query), "occupancy"
                )
                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    json.loads(response.content)["error"]["code"], "VALIDATION_ERROR"
                )
        rows.assert_not_called()

    @patch("reports.views.get_object_or_404")
    @patch("reports.views.occupancy_rows")
    def test_json_report_normalizes_hostel_id_and_returns_rows(self, rows, lookup):
        lookup.return_value = SimpleNamespace(pk=42)
        rows.return_value = [{"hostel": "A", "total_beds": 2}]
        request = self.factory.get("/reports/", {"hostel": "00042", "format": "json"})
        response = report_response(request, "occupancy")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["rows"], rows.return_value)
        self.assertIn("generated_on", json.loads(response.content))
        self.assertEqual(lookup.call_args.kwargs, {"pk": 42})
        rows.assert_called_once_with(42)

    @patch("reports.views.payment_status_rows")
    def test_payment_csv_escapes_formula_text_and_preserves_values(self, rows):
        rows.return_value = [
            {
                "student_id": "S1",
                "student_name": "=CMD",
                "hostel": "H",
                "room": "1",
                "bed": "A",
                "fee": "100.00",
                "paid": "25.00",
                "due": "75.00",
                "status": "Partial",
            }
        ]
        response = report_response(
            self.factory.get("/reports/", {"format": "csv"}), "payment-status"
        )
        parsed = list(csv.reader(io.StringIO(response.content.decode("utf-8-sig"))))
        self.assertEqual(response.status_code, 200)
        self.assertIn('filename="payment-status.csv"', response["Content-Disposition"])
        self.assertEqual(parsed[1][:3], ["S1", "'=CMD", "H"])
        self.assertEqual(parsed[1][5:9], ["100.00", "25.00", "75.00", "Partial"])
        rows.assert_called_once_with(None)

    @patch("reports.views.render")
    @patch("reports.views.Hostel.objects.all")
    @patch("reports.views.occupancy_rows")
    def test_html_report_passes_rows_and_filter_to_template(
        self, rows, hostels, render
    ):
        rows.return_value = [{"hostel": "A"}]
        hostels.return_value = ["hostel"]
        request = self.factory.get("/reports/")
        report_response(request, "occupancy")
        self.assertEqual(render.call_args.args[1], "reports/report.html")
        context = render.call_args.args[2]
        self.assertEqual(context["rows"], rows.return_value)
        self.assertEqual(context["hostels"], ["hostel"])
        self.assertIsNone(context["selected_hostel"])
        self.assertTrue(context["occupancy"])
