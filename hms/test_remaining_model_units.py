"""Remaining model and command decisions with database boundaries mocked.

Transaction wrappers are bypassed only for model/command decision bodies;
locking, database constraints and rollback remain integration-test concerns.
"""

from datetime import date
from decimal import Decimal
from io import StringIO
from types import SimpleNamespace
from unittest.mock import Mock, call, patch

from django.core.exceptions import ValidationError
from django.core.management.base import CommandError
from django.db import models
from django.test import SimpleTestCase, override_settings

from accounts.management.commands import create_demo_data
from allocations.models import Allocation
from audit.management.commands import purge_audit_logs
from audit.models import AuditEvent
from hostels.models import Bed, Hostel, Room
from payments.models import Payment, ReceiptSequence
from students.models import Student


class RemainingCommandUnitTests(SimpleTestCase):
    @override_settings(DEBUG=True)
    def test_exhausted_demo_beds_warn_and_other_allocations_and_payments_continue(self):
        boundaries = {
            "accounts": patch.object(create_demo_data.User.objects, "filter"),
            "hostels": patch.object(Hostel.objects, "get_or_create"),
            "rooms": patch.object(Room.objects, "get_or_create"),
            "students": patch.object(Student.objects, "get_or_create"),
            "linked": patch.object(Student.objects, "filter"),
            "allocations": patch.object(Allocation.objects, "filter"),
            "beds": patch.object(Bed.objects, "filter"),
            "payments": patch.object(Payment.objects, "filter"),
            "allocate": patch.object(create_demo_data, "allocate"),
            "record_payment": patch.object(create_demo_data, "record_payment"),
            "today": patch.object(
                create_demo_data.timezone, "localdate", return_value=date(2026, 11, 13)
            ),
        }
        mocks = {name: boundary.start() for name, boundary in boundaries.items()}
        for boundary in boundaries.values():
            self.addCleanup(boundary.stop)
        admin, login = Mock(), Mock()
        mocks["accounts"].return_value.first.side_effect = [admin, login]
        boys, girls = Mock(), Mock()
        mocks["hostels"].side_effect = [(boys, False), (girls, False)]
        mocks["rooms"].return_value = (Mock(), False)
        students = [
            SimpleNamespace(name=f"Student {index}", user_id=77, save=Mock())
            for index in range(6)
        ]
        mocks["students"].side_effect = [(student, False) for student in students]
        mocks["linked"].return_value.first.return_value = None
        mocks["allocations"].return_value.exists.return_value = False
        first_bed, second_bed = Mock(), Mock()
        available = mocks["beds"].return_value.order_by.return_value.first
        available.side_effect = [None, first_bed, None, second_bed]
        mocks["payments"].return_value.exists.return_value = False
        output, errors = StringIO(), StringIO()

        create_demo_data.Command.handle.__wrapped__(
            create_demo_data.Command(stdout=output, stderr=errors, no_color=True)
        )

        self.assertEqual(
            errors.getvalue().splitlines(),
            [
                "No available demo bed for Student 0; allocation skipped.",
                "No available demo bed for Student 3; allocation skipped.",
            ],
        )
        self.assertEqual(
            mocks["allocate"].call_args_list,
            [
                call(student=students[1], bed=first_bed, actor=admin),
                call(student=students[4], bed=second_bed, actor=admin),
            ],
        )
        self.assertEqual(mocks["record_payment"].call_count, 3)
        self.assertEqual(
            [item.kwargs["student"] for item in mocks["record_payment"].call_args_list],
            [students[0], students[1], students[4]],
        )
        students[0].save.assert_not_called()
        self.assertEqual(students[0].user_id, 77)
        self.assertIn("Demo data is ready", output.getvalue())

    def test_purge_cli_defaults_to_minimum_retention_and_parses_explicit_options(self):
        parser = purge_audit_logs.Command().create_parser(
            "manage.py", "purge_audit_logs"
        )

        defaults = parser.parse_args([])
        explicit = parser.parse_args(["--days", "730", "--dry-run"])

        self.assertEqual((defaults.days, defaults.dry_run), (366, False))
        self.assertEqual((explicit.days, explicit.dry_run), (730, True))
        with self.assertRaisesMessage(CommandError, "invalid int value"):
            parser.parse_args(["--days", "one-year"])


class RemainingQuerySetUnitTests(SimpleTestCase):
    def test_append_only_audit_bulk_insert_preserves_backend_options_and_result(self):
        events = [AuditEvent(action=AuditEvent.Action.CREATE, record_type="student")]
        queryset = AuditEvent.objects.all()
        with patch.object(models.QuerySet, "bulk_create", autospec=True) as insert:
            insert.return_value = events

            result = queryset.bulk_create(
                events, batch_size=25, ignore_conflicts=True, unique_fields=["id"]
            )

        self.assertIs(result, events)
        insert.assert_called_once_with(
            queryset,
            events,
            batch_size=25,
            ignore_conflicts=True,
            update_conflicts=False,
            update_fields=None,
            unique_fields=["id"],
        )

    def test_non_status_student_update_delegates_on_the_original_filtered_queryset(
        self,
    ):
        queryset = Student.objects.filter(course="Legacy Course")
        with patch.object(
            models.QuerySet, "update", autospec=True, return_value=3
        ) as update:
            count = queryset.update(course="Computer Science", year=2)

        self.assertEqual(count, 3)
        update.assert_called_once_with(queryset, course="Computer Science", year=2)

    def test_active_student_save_locks_row_without_checking_deactivation(self):
        student = Student(pk=8, status=Student.Status.ACTIVE)
        with (
            patch.object(Student.objects, "select_for_update") as locked,
            patch.object(Allocation.objects, "filter") as allocations,
            patch.object(models.Model, "save", return_value="saved") as save,
        ):
            result = Student.save.__wrapped__(student, update_fields=["name"])

        self.assertEqual(result, "saved")
        locked.return_value.get.assert_called_once_with(pk=8)
        allocations.assert_not_called()
        save.assert_called_once_with(update_fields=["name"])


class RemainingAllocationUnitTests(SimpleTestCase):
    def test_non_date_allocation_and_vacate_values_return_field_validation_errors(self):
        cases = (
            (None, None, "allocated_on"),
            ("2026-11-01", None, "allocated_on"),
            (date(2026, 11, 1), "2026-11-02", "vacated_on"),
            (date(2026, 11, 1), 2, "vacated_on"),
        )
        with patch("allocations.models.timezone.localdate") as today:
            for allocated_on, vacated_on, field in cases:
                with self.subTest(allocated_on=allocated_on, vacated_on=vacated_on):
                    allocation = Allocation(
                        allocated_on=allocated_on, vacated_on=vacated_on
                    )
                    with self.assertRaises(ValidationError) as error:
                        allocation.clean()
                    self.assertEqual(set(error.exception.message_dict), {field})
                    self.assertIn("valid", error.exception.message_dict[field][0])
            today.assert_not_called()

    def test_completed_or_cancelled_allocation_cannot_be_saved_again(self):
        student = Student(pk=11)
        bed = Bed(pk=5, room_id=4)
        allocation = Allocation(
            pk=20, student_id=11, bed_id=5, allocated_on=date(2026, 11, 1)
        )
        allocation._state.adding = False
        with (
            patch.object(Student.objects, "select_for_update") as students,
            patch.object(Bed.objects, "values_list") as bed_room,
            patch.object(Room.objects, "select_for_update"),
            patch.object(Bed.objects, "select_for_update") as beds,
            patch.object(Allocation.objects, "select_for_update") as previous,
            patch.object(allocation, "full_clean") as clean,
            patch.object(models.Model, "save") as persist,
            patch.object(bed, "save") as save_bed,
        ):
            students.return_value.get.return_value = student
            bed_room.return_value.get.return_value = 4
            beds.return_value.select_related.return_value.get.return_value = bed
            for status in (
                Allocation.AllocationStatus.COMPLETED,
                Allocation.AllocationStatus.CANCELLED,
            ):
                with self.subTest(status=status):
                    previous.return_value.get.return_value = Allocation(
                        pk=20,
                        student_id=11,
                        bed_id=5,
                        allocated_on=date(2026, 11, 1),
                        vacated_on=date(2026, 11, 2),
                        status=status,
                    )
                    with self.assertRaises(ValidationError) as error:
                        Allocation.save.__wrapped__(allocation)
                    self.assertEqual(error.exception.code, "ALREADY_RELEASED")
            clean.assert_not_called()
            persist.assert_not_called()
            save_bed.assert_not_called()


class RemainingPaymentUnitTests(SimpleTestCase):
    def test_full_clean_reports_invalid_amount_and_date_without_type_errors(self):
        for amount, payment_date, field in (
            (Decimal("NaN"), date(2026, 11, 13), "amount"),
            (Decimal("Infinity"), date(2026, 11, 13), "amount"),
            ("invalid", date(2026, 11, 13), "amount"),
            (Decimal("1"), "invalid-date", "date"),
        ):
            with self.subTest(amount=amount, payment_date=payment_date):
                payment = Payment(
                    amount=amount, date=payment_date, mode=Payment.Mode.CASH
                )
                with self.assertRaises(ValidationError) as error:
                    payment.full_clean(
                        exclude=["student", "receipt_no"],
                        validate_unique=False,
                        validate_constraints=False,
                    )
                self.assertEqual(set(error.exception.message_dict), {field})

    def test_first_adjustment_without_prior_adjustments_can_reverse_original_exactly(
        self,
    ):
        payment = Payment(
            student_id=11,
            amount=Decimal("-100.00"),
            date=date(2026, 11, 13),
            mode=Payment.Mode.CASH,
            adjustment_of_id=3,
            adjustment_reason="Duplicate collection",
        )
        original = SimpleNamespace(
            student_id=11,
            adjustment_of_id=None,
            date=date(2026, 11, 1),
            amount=Decimal("100.00"),
            adjustments=Mock(),
        )
        original.adjustments.aggregate.return_value = {"total": None}
        sequence = ReceiptSequence(pk=1, last_value=0)
        with (
            patch.object(Student.objects, "select_for_update") as students,
            patch.object(Payment.objects, "select_for_update") as payments,
            patch.object(ReceiptSequence.objects, "select_for_update") as sequences,
            patch.object(payment, "full_clean") as clean,
            patch.object(sequence, "save") as save_sequence,
            patch.object(models.Model, "save", return_value="inserted") as insert,
        ):
            students.return_value.get.return_value = Student(pk=11)
            payments.return_value.get.return_value = original
            sequences.return_value.get.return_value = sequence

            result = Payment.save.__wrapped__(payment)

        self.assertEqual(result, "inserted")
        self.assertEqual(payment.receipt_no, "R00000000001")
        self.assertEqual(sequence.last_value, 1)
        clean.assert_called_once_with(exclude=["receipt_no"])
        save_sequence.assert_called_once_with(update_fields=["last_value"])
        insert.assert_called_once_with(force_insert=True)

    def test_positional_or_force_update_saves_are_rejected_before_any_query(self):
        with patch.object(Student.objects, "select_for_update") as students:
            for args, kwargs in (
                ((False,), {}),
                ((), {"force_update": True}),
                ((), {"update_fields": []}),
            ):
                with self.subTest(args=args, kwargs=kwargs):
                    with self.assertRaisesMessage(
                        ValidationError, "complete new records"
                    ):
                        Payment.save.__wrapped__(Payment(), *args, **kwargs)
            students.assert_not_called()


class ModelDisplayUnitTests(SimpleTestCase):
    def test_display_labels_use_public_identifiers_and_human_action_names(self):
        student = Student(student_id="ABC123DEF456G", name="Aarav")
        hostel = Hostel(name="North Hostel")
        room = Room(hostel=hostel, room_number="201")
        bed = Bed(room=room, label="201-A")
        allocation = Allocation(
            student=student, bed=bed, status=Allocation.AllocationStatus.ACTIVE
        )
        event = AuditEvent(
            action=AuditEvent.Action.LOGIN_FAILED,
            record_type="login",
            record_id="aarav",
        )
        for record, label in (
            (student, "ABC123DEF456G - Aarav"),
            (hostel, "North Hostel"),
            (room, "North Hostel - Room 201"),
            (bed, "201-A"),
            (allocation, "ABC123DEF456G - 201-A (Active)"),
            (Payment(receipt_no="R00000000042"), "R00000000042"),
            (event, "Failed login: login aarav"),
        ):
            with self.subTest(model=type(record).__name__):
                self.assertEqual(str(record), label)
