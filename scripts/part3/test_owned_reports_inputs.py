"""Independent, explicitly invoked execution of Devansh's S2-12 through S2-16."""

import csv
import hashlib
import json
import logging
from decimal import Decimal
from html.parser import HTMLParser
from io import StringIO
from types import SimpleNamespace

from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.test import TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from allocations.models import Allocation
from allocations.services import allocate, release, transfer
from audit.models import AuditEvent
from hms.http import request_data
from hostels.models import Bed, Hostel, Room
from payments.models import Payment, ReceiptSequence
from payments.services import record_payment
from scripts.part3.test_owned_case_support import OwnedCaseEvidenceMixin
from students.models import Student
from tests.factories import make_room, make_student


class ReportTable(HTMLParser):
    """Read rendered table cells, decoding entities as a browser does."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.tags = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == "tr":
            self.row = []
        elif tag in {"td", "th"} and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in {"td", "th"} and self.cell is not None:
            self.row.append("".join(self.cell))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None


class OwnedReportInputCases(OwnedCaseEvidenceMixin, TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        super().setUp()
        ReceiptSequence.objects.get_or_create(pk=1)
        self.actor = User.objects.create_user(
            username="owned-report-warden", role="warden"
        )
        self.student = make_student()
        self.room = make_room(capacity=4, fee_amount=Decimal("1000.00"))
        self.beds = list(self.room.beds.all())
        self.empty = Hostel.objects.create(
            name="Empty hostel", hostel_type="Girls", is_active=False
        )
        self.client.force_login(self.actor)
        self.today = timezone.localdate().isoformat()

    @staticmethod
    def safe(value):
        return json.loads(json.dumps(value, cls=DjangoJSONEncoder, ensure_ascii=True))

    def state(self):
        return self.safe(
            {
                model._meta.label_lower: list(model.objects.order_by("pk").values())
                for model in (
                    Student,
                    Hostel,
                    Room,
                    Bed,
                    Allocation,
                    Payment,
                    ReceiptSequence,
                    AuditEvent,
                )
            }
        )

    @staticmethod
    def state_hash(state):
        return hashlib.sha256(
            json.dumps(state, sort_keys=True, ensure_ascii=True).encode()
        ).hexdigest()

    def post_json(self, name, data, *args):
        return self.client.post(
            reverse(name, args=args), data, content_type="application/json"
        )

    def pay(self, student=None, **overrides):
        return record_payment(
            actor=self.actor,
            **(
                {"student": student or self.student, "amount": "250", "mode": "Cash"}
                | overrides
            ),
        )

    def report(self, name="payment-status-report", **query):
        response = self.client.get(reverse(name), query, HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200, response.content)
        self.assertIn("generated_on", response.json())
        return response.json()["rows"]

    def csv_report(self, name="payment-status-report", **query):
        response = self.client.get(reverse(name), query | {"format": "csv"})
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response["Content-Type"], "text/csv; charset=utf-8")
        self.assertIn("attachment;", response["Content-Disposition"])
        self.assertTrue(response.content.startswith(b"\xef\xbb\xbf"))
        rows = list(csv.DictReader(StringIO(response.content.decode("utf-8-sig"))))
        for row in rows:
            self.assertNotIn(None, row, "CSV must have exactly one value per header")
            self.assertTrue(row["Generated On"].endswith(" IST"))
        return rows

    def html_report(self, name="payment-status-report", **query):
        response = self.client.get(reverse(name), query)
        self.assertEqual(response.status_code, 200, response.content)
        parsed = ReportTable()
        parsed.feed(response.content.decode("utf-8"))
        return response, parsed

    def matching_row(self, student):
        return next(
            row for row in self.report() if row["student_id"] == student.student_id
        )

    def all_formats(self, student, *, location, balance):
        row = self.matching_row(student)
        self.assertEqual(tuple(row[key] for key in ("hostel", "room", "bed")), location)
        self.assertEqual(
            tuple(row[key] for key in ("fee", "paid", "due", "status")), balance
        )
        exported = next(
            item
            for item in self.csv_report()
            if item["Student ID"] == student.student_id
        )
        columns = (
            ("Student ID", "student_id"),
            ("Student Name", "student_name"),
            ("Hostel Name", "hostel"),
            ("Room", "room"),
            ("Bed", "bed"),
            ("Fee Amount (INR)", "fee"),
            ("Amount Paid (INR)", "paid"),
            ("Due (INR)", "due"),
            ("Payment Status", "status"),
        )
        for heading, key in columns:
            self.assertEqual(exported[heading], row[key])
        _, html = self.html_report()
        self.assertIn("Bed", html.rows[0])
        rendered = next(item for item in html.rows[1:] if item[0] == student.student_id)
        expected = [student.student_id, student.name]
        expected.extend(value or "Unassigned" for value in location)
        expected.extend(balance)
        self.assertEqual(rendered, expected)
        return {"json": row, "csv": exported, "html_cells": rendered}

    def rejected(
        self,
        step,
        name,
        data,
        *,
        status=400,
        code="VALIDATION_ERROR",
        field=None,
        field_code=None,
        args=(),
        raw=False,
        form=False,
        generic=False,
        no_fields=False,
    ):
        before = self.state()
        if form:
            response = self.client.post(
                reverse(name, args=args), data, HTTP_ACCEPT="application/json"
            )
        else:
            body = data if raw else json.dumps(data, ensure_ascii=True)
            response = self.client.post(
                reverse(name, args=args), body, content_type="application/json"
            )
        self.assertEqual(response.status_code, status, response.content)
        error = response.json()["error"]
        self.assertEqual(error["code"], code)
        if field:
            self.assertEqual(error["fields"][field][0]["code"], field_code)
        if generic:
            self.assertEqual(
                error,
                {"code": "VALIDATION_ERROR", "message": "Enter a valid JSON object."},
            )
        if no_fields:
            self.assertNotIn("fields", error)
        after = self.state()
        self.assertEqual(after, before)
        result = {
            "route": reverse(name, args=args),
            "status": response.status_code,
            "error": error,
            "state_unchanged": True,
            "state_before_sha256": self.state_hash(before),
            "state_after_sha256": self.state_hash(after),
        }
        self.record_step(
            step,
            expected=f"HTTP {status}, {code}; complete domain state unchanged",
            actual=result,
        )
        return result

    def test_tc_reg_s2_12_report_history_balances_and_locations(self):
        self.begin_case("TC-REG-S2-12")
        original = allocate(student=self.student, bed=self.beds[0], actor=self.actor)
        self.assertEqual(self.matching_row(self.student)["status"], "Pending")
        second_room = make_room("202", fee_amount=Decimal("2000.00"))
        current = transfer(
            allocation_id=original.pk,
            new_bed=second_room.beds.first(),
            actor=self.actor,
        )
        self.pay()
        self.pay(amount="750", mode="UPI")
        unassigned = make_student(2)
        self.pay(student=unassigned, amount="25")
        location = (second_room.hostel.name, "202", current.bed.label)
        current_formats = self.all_formats(
            self.student,
            location=location,
            balance=("2000.00", "1000.00", "1000.00", "Partial"),
        )
        self.assertEqual(self.report(hostel=self.room.hostel_id), [])
        self.assertEqual(len(self.report(hostel=second_room.hostel_id)), 1)
        release(allocation_id=current.pk, actor=self.actor)
        historical = self.all_formats(
            self.student,
            location=location,
            balance=("2000.00", "1000.00", "1000.00", "Partial"),
        )
        self.assertEqual(self.report(hostel=self.room.hostel_id), [])
        self.assertEqual(len(self.report(hostel=second_room.hostel_id)), 1)
        self.record_step(
            "1",
            expected="Transfer/release preserve latest Bed and fee; two payments total 1000 once; old/new hostel filters follow location",
            actual={
                "after_transfer": current_formats,
                "after_release": historical,
                "old_hostel_rows": [],
                "new_hostel_row_count": 1,
            },
        )

        corrected = make_student(3)
        correction_room = make_room("404", fee_amount=Decimal("1000.00"))
        allocate(student=corrected, bed=correction_room.beds.first(), actor=self.actor)
        payment = self.pay(student=corrected, amount="1000")
        self.assertEqual(self.matching_row(corrected)["status"], "Paid")
        self.pay(
            student=corrected,
            amount="-250",
            adjustment_of=payment,
            adjustment_reason="Refund",
        )
        compared = self.all_formats(
            corrected,
            location=(
                correction_room.hostel.name,
                "404",
                correction_room.beds.first().label,
            ),
            balance=("1000.00", "750.00", "250.00", "Partial"),
        )
        self.record_step(
            "2",
            expected="1000 less 250 gives paid 750/due 250/Partial with matching HTML/CSV/JSON and Bed",
            actual=compared,
        )

        never_assigned = self.all_formats(
            unassigned,
            location=("", "", ""),
            balance=("0.00", "25.00", "0.00", "Pending"),
        )
        self.assertFalse(Allocation.objects.filter(student=unassigned).exists())
        cancelled_room = make_room("303", fee_amount=Decimal("3000.00"))
        for student, bed in zip(
            (self.student, unassigned), cancelled_room.beds.all(), strict=True
        ):
            Allocation.objects.create(
                student=student,
                bed=bed,
                status="Cancelled",
                vacated_on=timezone.localdate(),
            )
        self.assertEqual(self.report(hostel=cancelled_room.hostel_id), [])
        retained = self.all_formats(
            self.student,
            location=location,
            balance=("2000.00", "1000.00", "1000.00", "Partial"),
        )
        blank = self.all_formats(
            unassigned,
            location=("", "", ""),
            balance=("0.00", "25.00", "0.00", "Pending"),
        )
        self.assertFalse(blank["json"]["fee_configured"])
        no_fee = make_student(4)
        no_fee_room = make_room("505", fee_amount=Decimal("0.00"))
        self.pay(student=no_fee, amount="1500")
        self.assertEqual(self.matching_row(no_fee)["status"], "Pending")
        allocate(student=no_fee, bed=no_fee_room.beds.first(), actor=self.actor)
        zero = self.all_formats(
            no_fee,
            location=(no_fee_room.hostel.name, "505", no_fee_room.beds.first().label),
            balance=("0.00", "1500.00", "0.00", "Pending"),
        )
        self.assertFalse(zero["json"]["fee_configured"])
        self.record_step(
            "3",
            expected="Cancelled locations ignored; cancelled-only location blank/Unassigned; advance with zero fee remains Pending",
            actual={
                "retained_history": retained,
                "never_assigned": never_assigned,
                "cancelled_only": blank,
                "zero_fee": zero,
                "cancelled_hostel_rows": [],
            },
        )
        self.finish_case()

    def test_tc_reg_s2_13_csv_literals_unicode_and_html(self):
        self.begin_case("TC-REG-S2-13")
        allocate(student=self.student, bed=self.beds[0], actor=self.actor)
        vectors = (
            ('  =2+2, "North"\nWing', True),
            ("+SUM(1,2)", True),
            ("-2+3", True),
            ("@SUM(1,2)", True),
            (" \t+SUM(1,2)", True),
            ("\ttext", True),
            ("\rtext", True),
            ("\ntext", True),
            ('नमस्ते 😀, "Élève"\nWing', False),
        )
        for index, (label, dangerous) in enumerate(vectors, 1):
            self.room.hostel.name = label
            self.room.hostel.save()
            self.student.name = label + " <b>Élève</b>"
            self.student.save()
            occupancy = self.csv_report("occupancy-report", hostel=self.room.hostel_id)[
                0
            ]
            payment = self.csv_report()[0]
            prefix = "'" if dangerous else ""
            self.assertEqual(occupancy["Hostel Name"], prefix + label)
            self.assertEqual(payment["Hostel Name"], prefix + label)
            self.assertEqual(payment["Student Name"], prefix + self.student.name)
            response, parsed = self.html_report()
            self.assertEqual(parsed.rows[1][1], self.student.name)
            self.assertEqual(parsed.rows[1][2], label)
            self.assertNotIn("b", parsed.tags)
            self.assertContains(response, "&lt;b&gt;Élève&lt;/b&gt;")
            self.record_step(
                f"1-3.vector-{index}",
                expected="CSV quoting preserves text/Unicode; dangerous prefixes receive apostrophe; rendered HTML contains literal labels without injected element",
                actual={
                    "input_hostel": label,
                    "input_student": self.student.name,
                    "occupancy_csv_hostel": occupancy["Hostel Name"],
                    "payment_csv_hostel": payment["Hostel Name"],
                    "payment_csv_student": payment["Student Name"],
                    "html_cells": parsed.rows[1],
                    "injected_b_elements": 0,
                },
            )
        self.finish_case()

    def test_tc_reg_s2_14_report_boundaries(self):
        self.begin_case("TC-REG-S2-14")
        self.assertEqual(self.report(hostel=self.empty.pk), [])
        empty = self.csv_report("occupancy-report", hostel=self.empty.pk)[0]
        self.assertEqual(
            tuple(
                empty[key]
                for key in (
                    "Total Beds",
                    "Occupied Beds",
                    "Available Beds",
                    "Beds Under Maintenance",
                    "Occupancy %",
                )
            ),
            ("0", "0", "0", "0", "0.00"),
        )
        self.record_step(
            "1",
            expected="Empty filtered payment rows; zero-bed occupancy 0.00 percent without division error",
            actual={"payment_rows": [], "zero_bed_csv": empty},
        )
        allocation = allocate(student=self.student, bed=self.beds[0], actor=self.actor)
        before = self.state()
        identifiers = (
            "bad",
            "-1",
            "0",
            "1.5",
            "9" * 100,
            "9" * 5000,
            "0" * 5000,
            "١",
            str(2**63),
        )
        for name in ("occupancy-report", "payment-status-report"):
            outcomes = []
            for index, identifier in enumerate(identifiers, 1):
                response = self.client.get(
                    reverse(name),
                    {"hostel": identifier},
                    HTTP_ACCEPT="application/json",
                )
                self.assertEqual(response.status_code, 400, response.content)
                self.assertEqual(response.json()["error"]["code"], "VALIDATION_ERROR")
                outcomes.append(
                    {
                        "vector": index,
                        "length": len(identifier),
                        "prefix": identifier[:20],
                        "status": 400,
                        "error": response.json()["error"],
                    }
                )
            self.record_step(
                f"2.{name}",
                expected="Malformed, zero, negative, fractional, non-ASCII and extreme hostel IDs return 400",
                actual={"results": outcomes},
            )
            missing = self.client.get(
                reverse(name), {"hostel": 999999}, HTTP_ACCEPT="application/json"
            )
            self.assertEqual(missing.status_code, 404)
            self.assertEqual(missing.json()["error"]["code"], "NOT_FOUND")
            unsupported = self.client.get(reverse(name), {"format": "pdf"})
            self.assertEqual(unsupported.status_code, 400)
            self.assertEqual(unsupported.json()["error"]["code"], "VALIDATION_ERROR")
            method = self.client.post(reverse(name))
            self.assertEqual(method.status_code, 405)
            self.assertEqual(method["Allow"], "GET")
            self.record_step(
                f"3.{name}",
                expected="Absent well-formed hostel 404; unsupported format 400; POST 405 with Allow GET",
                actual={
                    "missing": missing.json(),
                    "missing_status": 404,
                    "format": unsupported.json(),
                    "format_status": 400,
                    "post_status": 405,
                    "allow": method["Allow"],
                },
            )
            leading = self.report(name, hostel="0" * 5000 + str(self.room.hostel_id))
            canonical = self.report(name, hostel=self.room.hostel_id)
            self.assertEqual(len(canonical), 1)
            if name == "payment-status-report":
                self.assertEqual(canonical[0]["student_id"], self.student.student_id)
                self.assertEqual(canonical[0]["bed"], allocation.bed.label)
                self.assertEqual(canonical[0]["hostel"], self.room.hostel.name)
            else:
                self.assertEqual(canonical[0]["hostel_id"], self.room.hostel_id)
            self.assertEqual(leading, canonical)
            self.record_step(
                f"4.{name}",
                expected="5000 leading zeros select exactly the known hostel",
                actual={
                    "leading_zero_count": 5000,
                    "rows": leading,
                    "matches_canonical_filter": True,
                },
            )
        self.assertEqual(self.state(), before)
        self.finish_case()

    def test_tc_reg_s2_15_malformed_json_and_controls(self):
        self.begin_case("TC-REG-S2-15")
        allocation = allocate(student=self.student, bed=self.beds[0], actor=self.actor)
        payment = self.pay(amount="400")
        vectors = [
            ("incomplete", b"{"),
            ("missing-value", b'{"value":}'),
            ("invalid-utf8", b"\xff"),
            ("invalid-string-utf8", b'{"value":"\xff"}'),
            ("array", b"[]"),
            ("number", b"123"),
            ("null", b"null"),
            ("string", b'"text"'),
            ("boolean", b"true"),
            ("field-array", b'{"bed_id":[]}'),
            ("field-object", b'{"bed_id":{}}'),
            ("mode-array", b'{"mode":["cash"]}'),
            ("high-surrogate", b'{"student_id":"\\ud800"}'),
            ("low-surrogate", b'{"student_id":"\\udfff"}'),
            ("surrogate-key", b'{"\\ud800":"value"}'),
            ("low-surrogate-key", b'{"\\udfff":"value"}'),
            ("surrogate-text", b'{"student_id":"\\ud800text"}'),
        ]
        for number in ("NaN", "Infinity", "-Infinity", "1e999", "-1e999"):
            vectors.append((number, ('{"bed_id":' + number + "}").encode()))
            vectors.append(
                (number + "-nested", ('{"nested":[{"value":' + number + "}]}").encode())
            )
        for depth in (1500, 20000):
            vectors.append(
                (
                    f"depth-{depth}",
                    ('{"bed_id":' + "[" * depth + "0" + "]" * depth + "}").encode(),
                )
            )
        for label, body in vectors:
            with self.assertRaises(ValidationError) as raised:
                request_data(
                    SimpleNamespace(content_type="application/json", body=body)
                )
            self.assertEqual(raised.exception.messages, ["Enter a valid JSON object."])
            for name in ("allocation-list", "payment-list"):
                self.rejected(f"1+3.{name}.{label}", name, body, raw=True, generic=True)
        for name, args in (
            ("allocation-transfer", (allocation.pk,)),
            ("allocation-release", (allocation.pk,)),
            ("payment-adjust", (payment.receipt_no,)),
        ):
            self.rejected(f"3.{name}", name, b"{", args=args, raw=True, generic=True)

        controls = b'{"student_id":"TEST123","bed_id":12,"amount":1.25,"enabled":true,"empty":null,"\\u0928\\u093e\\u092e":"\\u0928\\u092e\\u0938\\u094d\\u0924\\u0947","symbol":"\\ud83d\\ude00"}'
        parsed = request_data(
            SimpleNamespace(content_type="application/json", body=controls)
        )
        self.assertEqual(
            parsed,
            {
                "student_id": "TEST123",
                "bed_id": 12,
                "amount": 1.25,
                "enabled": True,
                "empty": None,
                "नाम": "नमस्ते",
                "symbol": "😀",
            },
        )
        self.assertIs(type(parsed["bed_id"]), int)
        self.assertIs(type(parsed["amount"]), float)
        submitted = object()
        self.assertIs(
            request_data(
                SimpleNamespace(
                    content_type="application/x-www-form-urlencoded", POST=submitted
                )
            ),
            submitted,
        )
        free = make_student(2)
        response = self.post_json(
            "allocation-list",
            {"student_id": free.student_id, "bed_id": self.beds[1].pk},
        )
        self.assertEqual(response.status_code, 201, response.content)
        valid_payment = self.post_json(
            "payment-list",
            {
                "student_id": free.student_id,
                "amount": 1.25,
                "date": self.today,
                "mode": "Cash",
            },
        )
        self.assertEqual(valid_payment.status_code, 201, valid_payment.content)
        self.assertEqual(valid_payment.json()["amount"], "1.25")
        paired = self.post_json(
            "payment-adjust",
            {
                "amount": "1.25",
                "date": self.today,
                "mode": "Cash",
                "adjustment_reason": "नमस्ते 😀",
            },
            payment.receipt_no,
        )
        self.assertEqual(paired.status_code, 201, paired.content)
        self.assertEqual(paired.json()["adjustment_reason"], "नमस्ते 😀")
        self.record_step(
            "2",
            expected="Finite scalar types and paired Unicode preserved; non-JSON POST returned unchanged; valid HTTP controls succeed",
            actual={
                "parser_control": parsed,
                "form_identity_preserved": True,
                "allocation": response.json(),
                "payment": valid_payment.json(),
                "unicode_adjustment": paired.json(),
            },
        )
        logs = StringIO()
        handler = logging.StreamHandler(logs)
        logger = logging.getLogger("django.request")
        logger.addHandler(handler)
        try:
            self.rejected(
                "3.no-raw-payload",
                "payment-list",
                b'{"probe":"HMS_RAW_BODY_DO_NOT_LOG","bed_id":[]}',
                raw=True,
                generic=True,
            )
        finally:
            logger.removeHandler(handler)
        self.assertNotIn("HMS_RAW_BODY_DO_NOT_LOG", logs.getvalue())
        self.record_step(
            "3.log-check",
            expected="Rejected synthetic raw payload absent from captured django.request log messages and no audit writes",
            actual={
                "logger": "django.request",
                "captured_messages": logs.getvalue(),
                "raw_payload_marker_present": False,
            },
        )
        self.finish_case()

    def test_tc_reg_s2_16_typed_dates_references_and_contracts(self):
        self.begin_case("TC-REG-S2-16")
        allocation = allocate(student=self.student, bed=self.beds[0], actor=self.actor)
        original = self.pay(amount="400")
        free = make_student(2)
        create = {"student_id": free.student_id, "bed_id": self.beds[1].pk}
        payment = {
            "student_id": free.student_id,
            "amount": "10.00",
            "date": self.today,
            "mode": "Cash",
        }
        adjustment = {
            "amount": "10.00",
            "date": self.today,
            "mode": "Cash",
            "adjustment_reason": "Correct payment",
        }
        for index, value in enumerate(
            (0, 123, 1.5, True, False, [], [self.today], {}, {"day": 26}), 1
        ):
            for name, args, data, field in (
                (
                    "allocation-list",
                    (),
                    create | {"allocated_on": value},
                    "allocated_on",
                ),
                (
                    "allocation-release",
                    (allocation.pk,),
                    {"vacate_date": value},
                    "vacate_date",
                ),
                ("payment-list", (), payment | {"date": value}, "date"),
                (
                    "payment-adjust",
                    (original.receipt_no,),
                    adjustment | {"date": value},
                    "date",
                ),
            ):
                container = isinstance(value, (dict, list))
                self.rejected(
                    f"1.{name}.type-{index}",
                    name,
                    data,
                    args=args,
                    field=None if container else field,
                    field_code=None if container else "invalid",
                    generic=container,
                )
        for name, args, key, field, bed in (
            ("allocation-list", (), "bed_id", "bed", self.beds[1]),
            (
                "allocation-transfer",
                (allocation.pk,),
                "new_bed_id",
                "new_bed",
                self.beds[1],
            ),
        ):
            for index, value in enumerate(
                (bed.pk + 0.5, float(bed.pk), True, False), 1
            ):
                data = (create if name == "allocation-list" else {}) | {key: value}
                self.rejected(
                    f"2.{name}.type-{index}",
                    name,
                    data,
                    args=args,
                    status=404,
                    code="NOT_FOUND",
                    field=field,
                    field_code="invalid_choice",
                )

        checks = (
            (
                "missing-bed",
                "allocation-list",
                {"student_id": free.student_id},
                (),
                False,
                400,
                "bed",
                "required",
            ),
            (
                "missing-new-bed",
                "allocation-transfer",
                {},
                (allocation.pk,),
                False,
                400,
                "new_bed",
                "required",
            ),
            (
                "unknown-bed",
                "allocation-create",
                create | {"bed_id": 999999},
                (),
                False,
                404,
                "bed",
                "invalid_choice",
            ),
            (
                "unknown-new-bed",
                "allocation-transfer",
                {"new_bed_id": 999999},
                (allocation.pk,),
                False,
                404,
                "new_bed",
                "invalid_choice",
            ),
            (
                "form-missing-student-allocation",
                "allocation-create",
                {"bed": self.beds[1].pk},
                (),
                True,
                400,
                "student",
                "required",
            ),
            (
                "form-missing-bed",
                "allocation-create",
                {"student": free.pk},
                (),
                True,
                400,
                "bed",
                "required",
            ),
            (
                "form-missing-student-payment",
                "payment-create",
                {key: value for key, value in payment.items() if key != "student_id"},
                (),
                True,
                400,
                "student",
                "required",
            ),
            (
                "form-unknown-student-allocation",
                "allocation-create",
                {"student": 999999, "bed": self.beds[1].pk},
                (),
                True,
                404,
                "student",
                "invalid_choice",
            ),
            (
                "form-unknown-student-payment",
                "payment-create",
                payment | {"student": 999999},
                (),
                True,
                404,
                "student",
                "invalid_choice",
            ),
            (
                "required-release-date",
                "allocation-release",
                {},
                (allocation.pk,),
                False,
                400,
                "vacate_date",
                "required",
            ),
            (
                "required-payment-date",
                "payment-create",
                {key: value for key, value in payment.items() if key != "date"},
                (),
                False,
                400,
                "date",
                "required",
            ),
            (
                "required-adjustment-date",
                "payment-adjust",
                {key: value for key, value in adjustment.items() if key != "date"},
                (original.receipt_no,),
                False,
                400,
                "date",
                "required",
            ),
            (
                "non-reference-choice",
                "payment-create",
                payment | {"mode": "Card"},
                (),
                False,
                400,
                "mode",
                "invalid_choice",
            ),
        )
        for label, name, data, args, form, status, field, field_code in checks:
            self.rejected(
                f"3.{label}",
                name,
                data,
                args=args,
                form=form,
                status=status,
                code="NOT_FOUND" if status == 404 else "VALIDATION_ERROR",
                field=field,
                field_code=field_code,
            )
        for name, data in (("allocation-create", create), ("payment-create", payment)):
            for label, identifier in (
                ("omitted", None),
                ("unknown", "missing"),
                ("boolean", True),
            ):
                body = {
                    key: value for key, value in data.items() if key != "student_id"
                }
                if label != "omitted":
                    body["student_id"] = identifier
                self.rejected(
                    f"3.{name}.student-{label}",
                    name,
                    body,
                    status=404,
                    code="NOT_FOUND",
                    no_fields=True,
                )
        self.record_step(
            "4",
            expected="Every rejected vector preserves allocations, Bed flags, history, all payments/receipts, receipt counter, student/hostel/room values and audits",
            actual={
                "snapshot_models": list(self.state()),
                "snapshot_comparison": "full ordered rows before and after every rejected request",
            },
        )
        controls = []
        for index, optional in enumerate(("omitted", None, ""), 2):
            student = free if index == 2 else make_student(index)
            data = {"student_id": student.student_id, "bed_id": self.beds[index - 1].pk}
            if optional != "omitted":
                data["allocated_on"] = optional
            response = self.post_json("allocation-create", data)
            self.assertEqual(response.status_code, 201, response.content)
            self.assertEqual(response.json()["allocated_on"], self.today)
            controls.append(
                {
                    "optional_date": optional,
                    "status": 201,
                    "allocation": response.json(),
                }
            )
        self.record_step(
            "3.optional-date-controls",
            expected="Allocation allocated_on is optional; omitted, null and empty dates use today successfully",
            actual={"controls": controls},
        )
        self.finish_case()
