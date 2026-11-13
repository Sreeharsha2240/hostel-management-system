"""Payment invariants with transactions and persistence replaced by fakes.

Concurrency, rollback, and database constraints are tested separately.
"""

from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.core.exceptions import ValidationError
from django.db import models
from django.test import SimpleTestCase

from students.models import Student

from .models import Payment, ReceiptSequence


class PaymentSaveDecisionUnitTests(SimpleTestCase):
    def setUp(self):
        self.student = Student(pk=11)
        self.payment = Payment(
            student_id=11, amount=Decimal("25"), date=date(2026, 11, 13), mode="Cash"
        )
        self.sequence = ReceiptSequence(pk=1, last_value=41)
        patches = {
            "students": patch.object(Student.objects, "select_for_update"),
            "payments": patch.object(Payment.objects, "select_for_update"),
            "sequences": patch.object(ReceiptSequence.objects, "select_for_update"),
            "clean": patch.object(self.payment, "full_clean"),
            "save": patch.object(models.Model, "save", return_value=None),
            "sequence_save": patch.object(self.sequence, "save"),
        }
        self.mocks = {name: item.start() for name, item in patches.items()}
        for item in patches.values():
            self.addCleanup(item.stop)
        self.mocks["students"].return_value.get.return_value = self.student
        self.mocks["sequences"].return_value.get.return_value = self.sequence

    def save_body(self, *args, **kwargs):
        return Payment.save.__wrapped__(self.payment, *args, **kwargs)

    def test_new_payment_allocates_one_receipt_and_forces_insert(self):
        self.save_body()
        self.assertEqual(self.payment.receipt_no, "R00000000042")
        self.assertEqual(self.sequence.last_value, 42)
        self.mocks["sequence_save"].assert_called_once_with(
            update_fields=["last_value"]
        )
        self.mocks["clean"].assert_called_once_with(exclude=["receipt_no"])
        self.assertTrue(self.mocks["save"].call_args.kwargs["force_insert"])

    def test_existing_payment_cannot_be_edited(self):
        self.payment.pk = 8
        with self.assertRaises(ValidationError) as error:
            self.save_body()
        self.assertEqual(error.exception.code, "IMMUTABLE_FIELD")
        self.mocks["students"].assert_not_called()

    def test_incomplete_update_operation_is_rejected(self):
        with self.assertRaisesMessage(ValidationError, "complete new records"):
            self.save_body(update_fields=["amount"])
        self.mocks["students"].assert_not_called()

    def test_missing_student_returns_not_found(self):
        self.mocks["students"].return_value.get.side_effect = Student.DoesNotExist
        with self.assertRaises(ValidationError) as error:
            self.save_body()
        self.assertEqual(error.exception.code, "NOT_FOUND")
        self.mocks["sequence_save"].assert_not_called()

    def original(self, **overrides):
        values = {
            "student_id": 11,
            "adjustment_of_id": None,
            "date": date(2026, 11, 1),
            "amount": Decimal("100"),
            "adjustments": Mock(),
        }
        original = SimpleNamespace(**(values | overrides))
        original.adjustments.aggregate.return_value = {"total": Decimal("-30")}
        self.payment.adjustment_of_id = 3
        self.mocks["payments"].return_value.get.return_value = original
        return original

    def test_correction_cannot_target_another_student_or_correction(self):
        for values in ({"student_id": 12}, {"adjustment_of_id": 9}):
            with self.subTest(values=values):
                self.original(**values)
                with self.assertRaisesMessage(ValidationError, "same student"):
                    self.save_body()
        self.mocks["sequence_save"].assert_not_called()

    def test_correction_cannot_predate_or_over_reverse_original(self):
        self.original(date=date(2026, 11, 14))
        with self.assertRaises(ValidationError) as error:
            self.save_body()
        self.assertIn("date", error.exception.message_dict)
        self.original()
        self.payment.amount = Decimal("-71")
        with self.assertRaises(ValidationError) as error:
            self.save_body()
        self.assertIn("amount", error.exception.message_dict)
        self.mocks["sequence_save"].assert_not_called()

    def test_valid_correction_cannot_overwrite_original(self):
        self.original()
        self.payment.amount = Decimal("-70")
        self.save_body()
        self.assertEqual(self.payment.receipt_no, "R00000000042")
        self.assertTrue(self.mocks["save"].call_args.kwargs["force_insert"])

    def test_missing_or_exhausted_sequence_is_rejected(self):
        self.mocks[
            "sequences"
        ].return_value.get.side_effect = ReceiptSequence.DoesNotExist
        with self.assertRaisesMessage(ValidationError, "not initialized"):
            self.save_body()
        self.mocks["sequences"].return_value.get.side_effect = None
        self.sequence.last_value = 99999999999
        with self.assertRaisesMessage(ValidationError, "exhausted"):
            self.save_body()
        self.mocks["save"].assert_not_called()
