from datetime import date, timedelta
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from .models import Allocation


class AllocationCleanTests(SimpleTestCase):
    def setUp(self):
        self.today = date(2026, 11, 9)
        self.allocated_on = self.today - timedelta(days=2)
        localdate = patch(
            "allocations.models.timezone.localdate", return_value=self.today
        )
        localdate.start()
        self.addCleanup(localdate.stop)

    def allocation(self, **overrides):
        values = {
            "student_id": 1,
            "bed_id": 1,
            "allocated_on": self.allocated_on,
        }
        return Allocation(**(values | overrides))

    def test_status_requires_a_matching_vacate_date(self):
        cases = (
            (
                Allocation.AllocationStatus.ACTIVE,
                self.today,
                "An active allocation cannot have a vacate date.",
            ),
            (
                Allocation.AllocationStatus.COMPLETED,
                None,
                "Enter a vacate date for an inactive allocation.",
            ),
            (
                Allocation.AllocationStatus.CANCELLED,
                None,
                "Enter a vacate date for an inactive allocation.",
            ),
        )
        for status, vacated_on, message in cases:
            with self.subTest(status=status):
                allocation = self.allocation(status=status, vacated_on=vacated_on)
                with self.assertRaises(ValidationError) as error:
                    allocation.clean()
                self.assertEqual(
                    error.exception.message_dict, {"vacated_on": [message]}
                )

    def test_dates_outside_the_allocation_period_are_rejected(self):
        cases = (
            (
                {"allocated_on": self.today + timedelta(days=1)},
                "allocated_on",
                "Allocation date cannot be in the future.",
            ),
            (
                {
                    "status": Allocation.AllocationStatus.COMPLETED,
                    "vacated_on": self.allocated_on - timedelta(days=1),
                },
                "vacated_on",
                "Vacate date must be between allocation date and today.",
            ),
            (
                {
                    "status": Allocation.AllocationStatus.COMPLETED,
                    "vacated_on": self.today + timedelta(days=1),
                },
                "vacated_on",
                "Vacate date must be between allocation date and today.",
            ),
        )
        for values, field, message in cases:
            with self.subTest(values=values):
                with self.assertRaises(ValidationError) as error:
                    self.allocation(**values).clean()
                self.assertEqual(error.exception.message_dict, {field: [message]})

    def test_allocation_and_vacate_date_boundaries_are_inclusive(self):
        self.allocation(allocated_on=self.today).clean()
        for status in (
            Allocation.AllocationStatus.COMPLETED,
            Allocation.AllocationStatus.CANCELLED,
        ):
            for allocated_on, vacated_on in (
                (self.allocated_on, self.allocated_on),
                (self.allocated_on, self.today),
                (self.today, self.today),
            ):
                with self.subTest(
                    status=status, allocated_on=allocated_on, vacated_on=vacated_on
                ):
                    self.allocation(
                        status=status,
                        allocated_on=allocated_on,
                        vacated_on=vacated_on,
                    ).clean()
