"""Lock-order and inactive-allocation decisions with database calls mocked."""

from types import SimpleNamespace
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from .models import Allocation
from .services import lock_allocation


class LockAllocationUnitTests(SimpleTestCase):
    @patch("allocations.services.Allocation.objects.select_for_update")
    @patch("allocations.services.Allocation.objects.get")
    @patch("allocations.services.Room.objects.select_for_update")
    @patch("allocations.services.Bed.objects.select_for_update")
    @patch("allocations.services.Bed.objects.filter")
    @patch("allocations.services.Student.objects.select_for_update")
    def test_locks_student_and_uses_sorted_room_and_bed_ids(
        self, student, bed_query, bed_lock, room_lock, allocation_get, allocation_lock
    ):
        source = SimpleNamespace(
            student_id=8, bed_id=9, status=Allocation.AllocationStatus.ACTIVE
        )
        allocation_get.return_value = source
        allocation_lock.return_value.get.return_value = source
        bed_query.return_value.values_list.return_value = [4, 2, 4]
        room_lock.return_value.filter.return_value.order_by.return_value = []
        bed_lock.return_value.filter.return_value.order_by.return_value = []
        self.assertIs(lock_allocation(10, extra_bed=SimpleNamespace(pk=3)), source)
        student.return_value.get.assert_called_once_with(pk=8)
        bed_query.assert_called_once_with(pk__in=[3, 9])
        room_lock.return_value.filter.assert_called_once_with(pk__in=[2, 4])
        bed_lock.return_value.filter.assert_called_once_with(pk__in=[3, 9])
        room_lock.return_value.filter.return_value.order_by.assert_called_once_with(
            "pk"
        )
        bed_lock.return_value.filter.return_value.order_by.assert_called_once_with("pk")

    @patch("allocations.services.Allocation.objects.select_for_update")
    @patch("allocations.services.Allocation.objects.get")
    @patch("allocations.services.Room.objects.select_for_update")
    @patch("allocations.services.Bed.objects.select_for_update")
    @patch("allocations.services.Bed.objects.filter")
    @patch("allocations.services.Student.objects.select_for_update")
    def test_inactive_allocation_is_rejected_after_locked_reread(
        self, student, bed_query, bed_lock, room_lock, allocation_get, allocation_lock
    ):
        allocation_get.return_value = SimpleNamespace(student_id=8, bed_id=9)
        allocation_lock.return_value.get.return_value = SimpleNamespace(
            status=Allocation.AllocationStatus.COMPLETED
        )
        bed_query.return_value.values_list.return_value = [4]
        room_lock.return_value.filter.return_value.order_by.return_value = []
        bed_lock.return_value.filter.return_value.order_by.return_value = []
        with self.assertRaises(ValidationError) as error:
            lock_allocation(10)
        self.assertEqual(error.exception.code, "ALREADY_RELEASED")
        allocation_lock.return_value.get.assert_called_once_with(pk=10)
