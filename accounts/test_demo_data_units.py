"""Demo-data command decisions with database and write services mocked."""

from datetime import date
from io import StringIO
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.core.management.base import CommandError
from django.test import SimpleTestCase, override_settings

from .management.commands.create_demo_data import Command


class DemoDataCommandUnitTests(SimpleTestCase):
    @override_settings(DEBUG=False)
    @patch("accounts.management.commands.create_demo_data.User.objects.filter")
    def test_demo_data_is_disabled_outside_debug(self, accounts):
        with self.assertRaisesMessage(CommandError, "only be created"):
            Command.handle.__wrapped__(Command())
        accounts.assert_not_called()

    @override_settings(DEBUG=True)
    @patch("accounts.management.commands.create_demo_data.User.objects.filter")
    def test_missing_demo_accounts_are_reported_before_creating_data(self, accounts):
        accounts.return_value.first.return_value = None
        with self.assertRaisesMessage(CommandError, "create_demo_accounts"):
            Command.handle.__wrapped__(Command())

    @override_settings(DEBUG=True)
    @patch(
        "accounts.management.commands.create_demo_data.timezone.localdate",
        return_value=date(2026, 11, 13),
    )
    @patch("accounts.management.commands.create_demo_data.record_payment")
    @patch("accounts.management.commands.create_demo_data.allocate")
    @patch("accounts.management.commands.create_demo_data.Payment.objects.filter")
    @patch("accounts.management.commands.create_demo_data.Bed.objects.filter")
    @patch("accounts.management.commands.create_demo_data.Allocation.objects.filter")
    @patch("accounts.management.commands.create_demo_data.Student.objects.filter")
    @patch(
        "accounts.management.commands.create_demo_data.Student.objects.get_or_create"
    )
    @patch("accounts.management.commands.create_demo_data.Room.objects.get_or_create")
    @patch("accounts.management.commands.create_demo_data.Hostel.objects.get_or_create")
    @patch("accounts.management.commands.create_demo_data.User.objects.filter")
    def test_new_demo_records_use_existing_accounts_and_safe_services(
        self,
        accounts,
        hostels,
        rooms,
        students,
        linked,
        allocations,
        beds,
        payments,
        allocate,
        record_payment,
        today,
    ):
        admin, login = Mock(), Mock()
        accounts.return_value.first.side_effect = [admin, login]
        boys, girls = Mock(), Mock()
        hostels.side_effect = [(boys, True), (girls, True)]
        rooms.return_value = (Mock(), True)
        student_rows = [
            SimpleNamespace(name=f"Student {i}", user_id=None, save=Mock())
            for i in range(6)
        ]
        students.side_effect = [(student, True) for student in student_rows]
        linked.return_value.first.return_value = None
        allocations.return_value.exists.return_value = False
        beds.return_value.order_by.return_value.first.return_value = Mock()
        payments.return_value.exists.return_value = False
        output = StringIO()
        Command.handle.__wrapped__(Command(stdout=output))
        self.assertEqual(hostels.call_count, 2)
        self.assertEqual(rooms.call_count, 4)
        self.assertEqual(students.call_count, 6)
        self.assertIs(student_rows[0].user, login)
        student_rows[0].save.assert_called_once_with(update_fields=["user"])
        self.assertEqual(allocate.call_count, 4)
        self.assertEqual(record_payment.call_count, 3)
        self.assertTrue(
            all(c.kwargs["actor"] is admin for c in allocate.call_args_list)
        )
        self.assertTrue(
            all(c.kwargs["actor"] is admin for c in record_payment.call_args_list)
        )
        self.assertIn("Demo data is ready", output.getvalue())
        today.assert_called_once()

    @override_settings(DEBUG=True)
    @patch(
        "accounts.management.commands.create_demo_data.timezone.localdate",
        return_value=date(2026, 11, 13),
    )
    @patch("accounts.management.commands.create_demo_data.record_payment")
    @patch("accounts.management.commands.create_demo_data.allocate")
    @patch("accounts.management.commands.create_demo_data.Payment.objects.filter")
    @patch("accounts.management.commands.create_demo_data.Bed.objects.filter")
    @patch("accounts.management.commands.create_demo_data.Allocation.objects.filter")
    @patch("accounts.management.commands.create_demo_data.Student.objects.filter")
    @patch(
        "accounts.management.commands.create_demo_data.Student.objects.get_or_create"
    )
    @patch("accounts.management.commands.create_demo_data.Room.objects.get_or_create")
    @patch("accounts.management.commands.create_demo_data.Hostel.objects.get_or_create")
    @patch("accounts.management.commands.create_demo_data.User.objects.filter")
    def test_existing_allocations_payments_and_link_are_not_duplicated(
        self,
        accounts,
        hostels,
        rooms,
        students,
        linked,
        allocations,
        beds,
        payments,
        allocate,
        record_payment,
        today,
    ):
        accounts.return_value.first.side_effect = [Mock(), Mock()]
        hostels.side_effect = [(Mock(), False), (Mock(), False)]
        rooms.return_value = (Mock(), False)
        student_rows = [
            SimpleNamespace(name=f"Student {i}", user_id=None, save=Mock())
            for i in range(6)
        ]
        students.side_effect = [(student, False) for student in student_rows]
        linked.return_value.first.return_value = Mock()
        allocations.return_value.exists.return_value = True
        payments.return_value.exists.return_value = True
        Command.handle.__wrapped__(Command(stdout=StringIO()))
        student_rows[0].save.assert_not_called()
        beds.assert_not_called()
        allocate.assert_not_called()
        record_payment.assert_not_called()
