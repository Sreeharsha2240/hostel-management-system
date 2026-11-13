"""Capacity edits must preserve occupied beds before any persistence occurs."""

from decimal import Decimal
from unittest.mock import Mock, PropertyMock, call, patch

from django.core.exceptions import ValidationError
from django.forms.utils import ErrorDict
from django.test import SimpleTestCase

from allocations.models import Allocation

from .forms import RoomForm
from .models import Room


class RoomFormCapacityUnitTests(SimpleTestCase):
    def form(self, *, pk=12, capacity=2):
        form = RoomForm(instance=Room(pk=pk, capacity=2))
        form.cleaned_data = {"capacity": capacity}
        form._errors = ErrorDict()
        return form

    @patch.object(Room, "beds", new_callable=PropertyMock)
    def test_new_room_or_invalid_capacity_never_queries_related_beds(self, beds):
        for form in (self.form(pk=None), self.form(capacity=None)):
            with self.subTest(
                pk=form.instance.pk, capacity=form.cleaned_data["capacity"]
            ):
                self.assertIs(form.clean(), form.cleaned_data)
                self.assertEqual(form.errors, {})
        beds.assert_not_called()

    @patch.object(Room, "beds", new_callable=PropertyMock)
    def test_equal_or_larger_capacity_keeps_cleaned_value(self, descriptor):
        beds = Mock()
        descriptor.return_value = beds
        beds.filter.return_value.distinct.return_value.count.return_value = 2
        for capacity in (2, 3, 4):
            with self.subTest(capacity=capacity):
                form = self.form(capacity=capacity)
                self.assertEqual(form.clean()["capacity"], capacity)
                self.assertEqual(form.errors, {})
        self.assertEqual(
            beds.filter.call_args_list,
            [call(allocations__status=Allocation.AllocationStatus.ACTIVE)] * 3,
        )

    @patch.object(Room, "beds", new_callable=PropertyMock)
    def test_reducing_below_active_beds_attaches_error_and_removes_capacity(
        self, descriptor
    ):
        descriptor.return_value.filter.return_value.distinct.return_value.count.return_value = 3
        form = self.form(capacity=2)

        cleaned = form.clean()

        self.assertNotIn("capacity", cleaned)
        self.assertEqual(
            form.errors["capacity"],
            [
                "This room has 3 beds with active allocations. Complete or move "
                "allocations before reducing capacity further."
            ],
        )
        self.assertEqual(set(form.errors), {"capacity"})

    @patch.object(Room, "beds", new_callable=PropertyMock)
    def test_room_with_no_active_beds_can_reduce_to_minimum(self, descriptor):
        descriptor.return_value.filter.return_value.distinct.return_value.count.return_value = 0
        form = self.form(capacity=1)
        self.assertEqual(form.clean()["capacity"], 1)
        self.assertEqual(form.errors, {})

    def test_declared_capacity_and_fee_bounds_remain_enforced(self):
        form = RoomForm()
        room = Room()
        capacity = Room._meta.get_field("capacity")
        fee = Room._meta.get_field("fee_amount")
        # ModelForm applies model validators in _post_clean, after field cleaning.
        for value in (0, 5):
            with self.subTest(capacity=value), self.assertRaises(ValidationError):
                capacity.clean(value, room)
        for value in (1, 4):
            self.assertEqual(capacity.clean(value, room), value)
        with self.assertRaises(ValidationError):
            fee.clean("-0.01", room)
        self.assertEqual(form.fields["fee_amount"].clean("0.00"), Decimal("0.00"))
        self.assertIsNone(form.fields["fee_amount"].clean(""))
