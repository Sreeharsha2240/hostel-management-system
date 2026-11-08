"""Explicit owner case executions; excluded from ordinary test discovery.

Run this module only through the owner evidence runner against its disposable
MySQL database. Existing companion tests and historical evidence are untouched.
"""

from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from decimal import Decimal
from threading import Barrier
from time import perf_counter
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db import close_old_connections, connection, connections
from django.db.models import Sum
from django.test import TransactionTestCase
from django.utils import timezone

from accounts.models import User
from allocations.models import Allocation
from allocations.services import allocate, release, transfer
from audit.models import AuditEvent
from hostels.models import Bed
from payments.models import Payment, ReceiptSequence
from payments.services import payment_status_queryset, record_payment, status_row
from scripts.part3.test_owned_case_support import OwnedCaseEvidenceMixin
from students.models import Student
from tests.factories import make_room, make_student


class _TransactionChecks:
    reset_sequences = True

    def setUp(self):
        super().setUp()
        self.assertEqual(connection.vendor, "mysql")
        self.assertFalse(connection.in_atomic_block)
        sequence, _created = ReceiptSequence.objects.get_or_create(
            pk=1, defaults={"last_value": 0}
        )
        self.assertEqual(sequence.last_value, 0)
        self.assertEqual(Payment.objects.count(), 0)

    def allocation_state(self):
        return {
            "allocations": list(Allocation.objects.order_by("pk").values()),
            "beds": list(Bed.objects.order_by("pk").values()),
            "audits": list(AuditEvent.objects.order_by("pk").values()),
        }

    def payment_state(self):
        return {
            "payments": list(Payment.objects.order_by("pk").values()),
            "receipt_counter": ReceiptSequence.objects.get(pk=1).last_value,
            "audits": list(AuditEvent.objects.order_by("pk").values()),
        }

    def assert_payment_audits(self, actor, payments):
        expected = [
            (actor.pk, "payment", "payments.payment", str(payment.pk))
            for payment in payments
        ]
        actual = list(
            AuditEvent.objects.order_by("pk").values_list(
                "user_id", "action", "record_type", "record_id"
            )
        )
        self.assertEqual(actual, expected)


class OwnedAllocationTransactions(
    _TransactionChecks, OwnedCaseEvidenceMixin, TransactionTestCase
):
    def setUp(self):
        super().setUp()
        self.actor = User.objects.create_user(username="workflow-warden", role="warden")
        self.student = make_student()
        self.room = make_room()
        self.source, self.target = self.room.beds.all()

    def test_tc_reg_s2_08_rollback_and_retry(self):
        self.begin_case("TC-REG-S2-08")
        today = timezone.localdate()
        allocated_on = today - timedelta(days=2)
        before_allocate = self.allocation_state()
        with (
            patch(
                "allocations.services.record_event",
                side_effect=RuntimeError("controlled allocate audit failure"),
            ) as failed_audit,
            self.assertRaisesRegex(RuntimeError, "controlled allocate audit failure"),
        ):
            allocate(
                student=self.student,
                bed=self.source,
                actor=self.actor,
                allocated_on=allocated_on,
            )
        failed_audit.assert_called_once()
        after_allocate = self.allocation_state()
        self.assertEqual(after_allocate, before_allocate)
        self.source.refresh_from_db()
        self.target.refresh_from_db()
        self.assertEqual(
            (self.source.status, self.target.status), ("Available", "Available")
        )
        self.assertFalse(Allocation.objects.exists())
        self.record_step(
            "1",
            expected="Failed allocate audit leaves no allocation, Available beds and unchanged audits.",
            actual={
                "fault": "controlled allocate audit failure",
                "audit_call_count": failed_audit.call_count,
                "before": before_allocate,
                "after": after_allocate,
            },
        )

        original = allocate(
            student=self.student,
            bed=self.source,
            actor=self.actor,
            allocated_on=allocated_on,
        )
        before_release = self.allocation_state()
        self.assertEqual(len(before_release["allocations"]), 1)
        event = AuditEvent.objects.get()
        self.assertEqual(
            (event.user_id, event.action, event.record_type, event.record_id),
            (self.actor.pk, "allocate", "allocations.allocation", str(original.pk)),
        )
        with (
            patch(
                "allocations.services.record_event",
                side_effect=RuntimeError("controlled release audit failure"),
            ) as failed_audit,
            self.assertRaisesRegex(RuntimeError, "controlled release audit failure"),
        ):
            release(
                allocation_id=original.pk,
                actor=self.actor,
                vacate_date=today - timedelta(days=1),
            )
        failed_audit.assert_called_once()
        after_release = self.allocation_state()
        self.assertEqual(after_release, before_release)
        original.refresh_from_db()
        self.source.refresh_from_db()
        self.assertEqual((original.status, self.source.status), ("Active", "Occupied"))
        self.assertEqual(original.allocated_on, allocated_on)
        self.assertIsNone(original.vacated_on)
        self.record_step(
            "2",
            expected="Created allocation survives a release audit failure as Active/Occupied with all history and audits unchanged.",
            actual={
                "fault": "controlled release audit failure",
                "audit_call_count": failed_audit.call_count,
                "before": before_release,
                "after": after_release,
            },
        )

        before_transfer = self.allocation_state()
        save_bed = Bed.save
        fault_hits = []

        def fail_target(bed, *args, **kwargs):
            if bed.pk == self.target.pk and bed.status == "Occupied":
                fault_hits.append({"bed_id": bed.pk, "attempted_status": bed.status})
                raise RuntimeError("controlled target storage failure")
            return save_bed(bed, *args, **kwargs)

        with (
            patch.object(Bed, "save", new=fail_target),
            self.assertRaisesRegex(RuntimeError, "controlled target storage failure"),
        ):
            transfer(allocation_id=original.pk, new_bed=self.target, actor=self.actor)
        self.assertEqual(
            fault_hits, [{"bed_id": self.target.pk, "attempted_status": "Occupied"}]
        )
        after_transfer = self.allocation_state()
        self.assertEqual(after_transfer, before_transfer)
        original.refresh_from_db()
        self.source.refresh_from_db()
        self.target.refresh_from_db()
        self.assertEqual(
            (original.status, self.source.status, self.target.status),
            ("Active", "Occupied", "Available"),
        )
        self.assertEqual(original.allocated_on, allocated_on)
        self.assertIsNone(original.vacated_on)
        self.assertFalse(AuditEvent.objects.filter(action="transfer").exists())
        self.record_step(
            "3",
            expected="Failed target Occupied save rolls back both beds, complete original history/dates/active keys and every audit.",
            actual={
                "fault_hits": fault_hits,
                "before": before_transfer,
                "after": after_transfer,
            },
        )

        successor = transfer(
            allocation_id=original.pk, new_bed=self.target, actor=self.actor
        )
        original.refresh_from_db()
        successor.refresh_from_db()
        self.source.refresh_from_db()
        self.target.refresh_from_db()
        self.assertNotEqual(successor.pk, original.pk)
        self.assertEqual(Allocation.objects.count(), 2)
        self.assertEqual(
            (original.student_id, original.bed_id, original.allocated_on),
            (self.student.pk, self.source.pk, allocated_on),
        )
        self.assertEqual(
            (
                original.status,
                original.vacated_on,
                original.active_student_id,
                original.active_bed_id,
            ),
            ("Completed", today, None, None),
        )
        self.assertEqual(
            (
                successor.student_id,
                successor.bed_id,
                successor.status,
                successor.allocated_on,
                successor.vacated_on,
                successor.active_student_id,
                successor.active_bed_id,
            ),
            (
                self.student.pk,
                self.target.pk,
                "Active",
                today,
                None,
                self.student.pk,
                self.target.pk,
            ),
        )
        self.assertEqual(
            (self.source.status, self.target.status), ("Available", "Occupied")
        )
        self.assertEqual(
            Allocation.objects.filter(student=self.student, status="Active").count(), 1
        )
        self.assertEqual(
            Allocation.objects.filter(bed=self.target, status="Active").count(), 1
        )
        after_retry = self.allocation_state()
        self.assertEqual(after_retry["audits"][:-1], before_transfer["audits"])
        self.assertEqual(len(after_retry["audits"]), len(before_transfer["audits"]) + 1)
        event = AuditEvent.objects.get(action="transfer")
        self.assertEqual(
            (event.user_id, event.record_type, event.record_id),
            (self.actor.pk, "allocations.allocation", str(successor.pk)),
        )
        self.record_step(
            "4",
            expected="Same transfer retry completes original, creates exactly one active successor and one attributable transfer audit.",
            actual={
                "original_id": original.pk,
                "successor_id": successor.pk,
                "after": after_retry,
            },
        )
        self.finish_case()


class OwnedPaymentTransactions(
    _TransactionChecks, OwnedCaseEvidenceMixin, TransactionTestCase
):
    def setUp(self):
        super().setUp()
        self.actor = User.objects.create_user(username="payments-warden", role="warden")
        self.student = make_student(name="A & B <Smith>")
        self.room = make_room(fee_amount=Decimal("1000.00"))

    def record_payment(self, **overrides):
        data = {
            "student": self.student,
            "amount": "400.00",
            "date": timezone.localdate(),
            "mode": "UPI",
            "reference": "TEST123",
        }
        return record_payment(actor=self.actor, **(data | overrides))

    def test_tc_reg_s2_09_payment_permanence(self):
        self.begin_case("TC-REG-S2-09")
        first = self.record_payment()
        second = self.record_payment(mode="Bank Transfer")
        self.assertEqual(
            (first.receipt_no, second.receipt_no), ("R00000000001", "R00000000002")
        )
        self.assertNotEqual(first.pk, second.pk)
        self.assertEqual(
            (first.amount, second.amount), (Decimal("400.00"), Decimal("400.00"))
        )
        self.assertEqual(
            (first.student_id, second.student_id), (self.student.pk, self.student.pk)
        )
        self.assertEqual(ReceiptSequence.objects.get(pk=1).last_value, 2)
        self.assert_payment_audits(self.actor, [first, second])
        originals = self.payment_state()
        self.record_step(
            "1",
            expected="Two genuine payments have distinct sequential receipts, counter 2 and one actor audit per payment.",
            actual=originals,
        )

        first.amount = Decimal("1.00")
        attempts = [
            ("unchanged_save", second.save),
            ("edited_save", first.save),
            ("partial_save", lambda: first.save(update_fields=["amount"])),
            ("instance_delete", first.delete),
            ("queryset_delete", lambda: Payment.objects.all().delete()),
            ("queryset_update", lambda: Payment.objects.update(amount=1)),
            ("bulk_update", lambda: Payment.objects.bulk_update([first], ["amount"])),
            (
                "bulk_create",
                lambda: Payment.objects.bulk_create(
                    [Payment(student=self.student, amount=1, mode="Cash")]
                ),
            ),
            (
                "primary_key_replay",
                lambda: Payment(
                    pk=first.pk, student=self.student, amount=1, mode="Cash"
                ).save(),
            ),
            (
                "receipt_reuse",
                lambda: Payment(
                    student=self.student,
                    amount=1,
                    mode="Cash",
                    receipt_no=first.receipt_no,
                ).save(),
            ),
        ]
        for name, attempt in attempts:
            with (
                self.subTest(mutation=name),
                self.assertRaises(ValidationError) as failure,
            ):
                attempt()
            self.assertEqual(failure.exception.code, "IMMUTABLE_FIELD")
            state = self.payment_state()
            self.assertEqual(state, originals)
            self.record_step(
                f"2.{name}",
                expected="Guarded mutation rejects without changing any original field, receipt counter or audit.",
                actual={
                    "mutation": name,
                    "error_code": failure.exception.code,
                    "error_messages": failure.exception.messages,
                    "after": state,
                },
            )

        first.refresh_from_db()
        second.refresh_from_db()
        reloaded = self.payment_state()
        self.assertEqual(reloaded, originals)
        self.assertEqual(first.amount, Decimal("400.00"))
        self.assertEqual(first.student_id, self.student.pk)
        self.record_step(
            "3",
            expected="Reloaded originals retain complete amount, identity, receipt and creation history.",
            actual=reloaded,
        )

        correction = self.record_payment(
            amount="-100",
            adjustment_of=first,
            adjustment_reason="Duplicate part of entry",
        )
        corrected = self.payment_state()
        self.assertEqual(corrected["payments"][:2], originals["payments"])
        self.assertEqual(corrected["audits"][:2], originals["audits"])
        self.assertEqual(len(corrected["payments"]), 3)
        self.assertEqual(corrected["receipt_counter"], 3)
        self.assertNotIn(correction.pk, (first.pk, second.pk))
        self.assertEqual(
            (
                correction.receipt_no,
                correction.amount,
                correction.adjustment_of_id,
                correction.student_id,
            ),
            ("R00000000003", Decimal("-100.00"), first.pk, self.student.pk),
        )
        self.assertEqual(correction.adjustment_reason, "Duplicate part of entry")
        self.assertEqual(
            Payment.objects.aggregate(total=Sum("amount"))["total"], Decimal("700.00")
        )
        self.assert_payment_audits(self.actor, [first, second, correction])
        self.record_step(
            "expected.adjusting_entry",
            expected="Correction is a new linked adjusting entry with its own sequential receipt/audit; originals remain unchanged.",
            actual={"after": corrected, "net_amount": Decimal("700.00")},
        )
        self.finish_case()

    def test_tc_reg_s2_10_rejected_failed_and_exhausted_receipts(self):
        self.begin_case("TC-REG-S2-10")
        initial = self.payment_state()
        invalid = [
            (f"amount_{index}", {"amount": amount})
            for index, amount in enumerate(
                (
                    "0",
                    "-1",
                    "NaN",
                    "Infinity",
                    "-Infinity",
                    "1.001",
                    "100000000",
                    "text",
                ),
                start=1,
            )
        ]
        invalid.extend(
            [
                ("unsupported_mode", {"mode": "Card"}),
                ("future_date", {"date": timezone.localdate() + timedelta(days=1)}),
                ("invalid_date", {"date": "invalid"}),
                ("overlength_reference", {"reference": "A" * 31}),
                ("invalid_reference", {"reference": "invalid/ref"}),
            ]
        )
        for name, overrides in invalid:
            with (
                self.subTest(rejection=name),
                self.assertRaises(ValidationError) as failure,
            ):
                self.record_payment(**overrides)
            state = self.payment_state()
            self.assertEqual(state, initial)
            self.record_step(
                f"1.{name}",
                expected="Invalid payment creates no row or audit and consumes no receipt number.",
                actual={
                    "input_overrides": overrides,
                    "error_messages": failure.exception.messages,
                    "after": state,
                },
            )

        with (
            patch(
                "payments.services.record_event",
                side_effect=RuntimeError("controlled payment audit failure"),
            ) as failed_audit,
            self.assertRaisesRegex(RuntimeError, "controlled payment audit failure"),
        ):
            self.record_payment()
        failed_audit.assert_called_once()
        after_failure = self.payment_state()
        self.assertEqual(after_failure, initial)
        self.record_step(
            "2",
            expected="Valid payment with failed audit rolls back payment and counter together.",
            actual={
                "fault": "controlled payment audit failure",
                "audit_call_count": failed_audit.call_count,
                "after": after_failure,
            },
        )

        payment = self.record_payment()
        self.assertEqual(payment.receipt_no, "R00000000001")
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(ReceiptSequence.objects.get(pk=1).last_value, 1)
        self.assert_payment_audits(self.actor, [payment])
        successful = self.payment_state()
        self.record_step(
            "3",
            expected="Fresh valid retry after removing fault receives R00000000001 and one actor payment audit.",
            actual=successful,
        )

        limit = 99999999999
        self.assertEqual(
            ReceiptSequence.objects.filter(pk=1).update(last_value=limit), 1
        )
        before_exhaustion = self.payment_state()
        with self.assertRaisesMessage(
            ValidationError, "receipt number range is exhausted"
        ) as failure:
            self.record_payment()
        after_exhaustion = self.payment_state()
        self.assertEqual(after_exhaustion, before_exhaustion)
        self.assertEqual(after_exhaustion["payments"], successful["payments"])
        self.assertEqual(after_exhaustion["audits"], successful["audits"])
        self.assertEqual(after_exhaustion["receipt_counter"], limit)
        payment.refresh_from_db()
        self.assertEqual(payment.receipt_no, "R00000000001")
        self.record_step(
            "4",
            expected="Exhausted range rejects without overwriting existing payment/receipt history, audits or maximum counter.",
            actual={
                "counter_fixture": limit,
                "error_messages": failure.exception.messages,
                "before": before_exhaustion,
                "after": after_exhaustion,
            },
        )
        self.finish_case()


class OwnedPaymentCorrectionConcurrency(
    _TransactionChecks, OwnedCaseEvidenceMixin, TransactionTestCase
):
    def setUp(self):
        super().setUp()
        self.actor = User.objects.create_user(
            username="parallel-payments", role="warden"
        )
        self.students = [make_student(index) for index in range(1, 5)]

    def test_tc_reg_s2_11_competing_corrections(self):
        self.begin_case("TC-REG-S2-11")
        original = record_payment(
            actor=self.actor, student=self.students[0], amount="100", mode="Cash"
        )
        self.assertEqual(original.receipt_no, "R00000000001")
        before = self.payment_state()
        self.assertEqual(before["receipt_counter"], 1)
        self.assert_payment_audits(self.actor, [original])
        actor_id = self.actor.pk
        student_id = self.students[0].pk
        original_id = original.pk
        barrier = Barrier(2, timeout=20)
        locking_query_barrier = Barrier(2, timeout=20)

        def attempt(worker):
            close_old_connections()
            try:
                actor = User.objects.get(pk=actor_id)
                student = Student.objects.get(pk=student_id)
                source = Payment.objects.get(pk=original_id)
                with connection.cursor() as cursor:
                    cursor.execute("SELECT CONNECTION_ID()")
                    connection_id = cursor.fetchone()[0]
                barrier.wait()
                started = perf_counter()
                locking_query_entries = []

                def synchronize_lock_query(execute, sql, params, many, context):
                    normalized = sql.upper()
                    if "FOR UPDATE" in normalized and "STUDENTS_STUDENT" in normalized:
                        locking_query_entries.append(perf_counter())
                        locking_query_barrier.wait()
                    return execute(sql, params, many, context)

                try:
                    with connection.execute_wrapper(synchronize_lock_query):
                        correction = record_payment(
                            actor=actor,
                            student=student,
                            amount="-80",
                            mode="Cash",
                            adjustment_of=source,
                            adjustment_reason="Correction",
                        )
                except ValidationError as error:
                    outcome = {"result": "rejected", "error_messages": error.messages}
                else:
                    outcome = {
                        "result": "created",
                        "payment_id": correction.pk,
                        "receipt_no": correction.receipt_no,
                    }
                return {
                    "worker": worker,
                    "connection_id": connection_id,
                    "attempt_started_monotonic": started,
                    "attempt_finished_monotonic": perf_counter(),
                    "locking_query_entries_monotonic": locking_query_entries,
                    **outcome,
                }
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(attempt, range(2)))
        self.assertEqual(len({item["connection_id"] for item in outcomes}), 2)
        self.assertTrue(
            all(len(item["locking_query_entries_monotonic"]) == 1 for item in outcomes)
        )
        self.assertLess(
            max(item["attempt_started_monotonic"] for item in outcomes),
            min(item["attempt_finished_monotonic"] for item in outcomes),
        )
        winners = [item for item in outcomes if item["result"] == "created"]
        rejected = [item for item in outcomes if item["result"] == "rejected"]
        self.assertEqual(len(winners), 1)
        self.assertEqual(len(rejected), 1)
        self.assertEqual(winners[0]["receipt_no"], "R00000000002")
        self.assertTrue(
            any(
                "cannot reverse more" in message
                for message in rejected[0]["error_messages"]
            )
        )
        self.record_step(
            "1",
            expected="Two barrier-synchronized corrections on distinct MySQL connections produce one new receipt and one over-reversal rejection.",
            actual={
                "original": before,
                "correction_amount": "-80.00",
                "barrier_parties": 2,
                "attempt_intervals_include_initial_barrier_wait": False,
                "both_services_synchronized_at_student_lock_query": True,
                "database_lock_wait_duration_measured": False,
                "outcomes": outcomes,
            },
        )

        after = self.payment_state()
        self.assertEqual(len(after["payments"]), 2)
        self.assertEqual(after["receipt_counter"], 2)
        self.assertEqual(after["payments"][0], before["payments"][0])
        self.assertEqual(after["audits"][:1], before["audits"])
        self.assertEqual(
            [row["receipt_no"] for row in after["payments"]],
            ["R00000000001", "R00000000002"],
        )
        original.refresh_from_db()
        correction = Payment.objects.get(pk=winners[0]["payment_id"])
        self.assertEqual(
            (original.amount, original.student_id, original.adjustment_of_id),
            (Decimal("100.00"), student_id, None),
        )
        self.assertEqual(
            (
                correction.amount,
                correction.student_id,
                correction.adjustment_of_id,
                correction.adjustment_reason,
            ),
            (Decimal("-80.00"), student_id, original.pk, "Correction"),
        )
        net = Payment.objects.filter(student_id=student_id).aggregate(
            total=Sum("amount")
        )["total"]
        self.assertEqual(net, Decimal("20.00"))
        balance = status_row(payment_status_queryset().get(pk=student_id))
        self.assertEqual(balance["paid"], "20.00")
        self.assert_payment_audits(self.actor, [original, correction])
        self.record_step(
            "2",
            expected="Exactly two unchanged-original/correction rows, receipts 1/2, counter 2, two actor audits and net INR20 remain.",
            actual={"after": after, "net_amount": net, "status": balance},
        )
        self.finish_case()
