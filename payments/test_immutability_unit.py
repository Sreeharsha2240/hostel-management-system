"""Payment and allocation bulk-operation safeguards without database writes."""

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from allocations.models import Allocation

from .models import Payment


class FinancialHistoryUnitTests(SimpleTestCase):
    def test_payment_bulk_mutations_are_rejected(self):
        payments = Payment.objects.all()
        operations = (
            lambda: payments.update(amount=1),
            lambda: payments.delete(),
            lambda: payments.bulk_create([]),
            lambda: payments.bulk_update([], ["amount"]),
        )
        for operation in operations:
            with (
                self.subTest(operation=operation),
                self.assertRaises(ValidationError) as error,
            ):
                operation()
            self.assertEqual(error.exception.code, "IMMUTABLE_FIELD")

    def test_payment_and_allocation_records_cannot_be_deleted(self):
        for record in (Payment(), Allocation()):
            with (
                self.subTest(record=type(record).__name__),
                self.assertRaises(ValidationError),
            ):
                record.delete()

    def test_allocation_bulk_writes_are_rejected(self):
        allocations = Allocation.objects.all()
        for operation in (
            lambda: allocations.update(status="Completed"),
            lambda: allocations.bulk_create([]),
            lambda: allocations.delete(),
        ):
            with self.subTest(operation=operation), self.assertRaises(ValidationError):
                operation()
