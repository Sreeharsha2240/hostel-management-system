"""Django-admin access and inline-audit decisions without persistence."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.contrib.admin.sites import AdminSite
from django.test import SimpleTestCase

from accounts.admin import HMSUserAdmin
from accounts.models import User
from allocations.admin import AllocationAdmin
from allocations.models import Allocation
from audit.admin import AuditEventAdmin
from audit.models import AuditEvent
from hostels.admin import HostelAdmin, RoomAdmin, save_audited_formset
from hostels.models import Hostel, Room
from payments.admin import PaymentAdmin
from payments.models import Payment


class AdminSecurityUnitTests(SimpleTestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_user_and_audit_admin_require_admin_superuser(self):
        for superuser, role, expected in (
            (True, "admin", True),
            (True, "warden", False),
            (False, "admin", False),
        ):
            with self.subTest(superuser=superuser, role=role):
                request = SimpleNamespace(
                    user=SimpleNamespace(is_superuser=superuser, role=role)
                )
                users, audit = (
                    HMSUserAdmin(User, self.site),
                    AuditEventAdmin(AuditEvent, self.site),
                )
                self.assertEqual(users.has_module_permission(request), expected)
                self.assertEqual(users.has_view_permission(request), expected)
                self.assertEqual(users.has_add_permission(request), expected)
                self.assertEqual(users.has_change_permission(request), expected)
                self.assertEqual(audit.has_module_permission(request), expected)
                self.assertEqual(audit.has_view_permission(request), expected)
                self.assertFalse(users.has_delete_permission(request))
                self.assertFalse(audit.has_add_permission(request))
                self.assertFalse(audit.has_change_permission(request))
                self.assertFalse(audit.has_delete_permission(request))

    def test_payment_and_allocation_admin_are_read_only(self):
        request = SimpleNamespace(user=SimpleNamespace(is_superuser=True, role="admin"))
        for admin in (
            PaymentAdmin(Payment, self.site),
            AllocationAdmin(Allocation, self.site),
        ):
            with self.subTest(admin=type(admin).__name__):
                self.assertFalse(admin.has_add_permission(request))
                self.assertFalse(admin.has_change_permission(request))
                self.assertFalse(admin.has_delete_permission(request))

    @patch("hostels.admin.record_event")
    def test_inline_formset_saves_and_audits_each_record(self, audit):
        new, existing = Mock(), Mock()
        new._state.adding, existing._state.adding = True, False
        formset = Mock()
        formset.save.return_value = [new, existing]
        request = SimpleNamespace(user="admin")
        save_audited_formset(request, formset)
        formset.save.assert_called_once_with(commit=False)
        new.save.assert_called_once()
        existing.save.assert_called_once()
        formset.save_m2m.assert_called_once()
        self.assertEqual(
            [c.kwargs["action"] for c in audit.call_args_list],
            [AuditEvent.Action.CREATE, AuditEvent.Action.UPDATE],
        )
        self.assertEqual(
            [c.kwargs["record"] for c in audit.call_args_list], [new, existing]
        )

    @patch("hostels.admin.save_audited_formset")
    def test_hostel_and_room_admin_delegate_inline_saves(self, save):
        request, formset = Mock(), Mock()
        HostelAdmin(Hostel, self.site).save_formset(request, None, formset, False)
        RoomAdmin(Room, self.site).save_formset(request, None, formset, True)
        self.assertEqual(save.call_count, 2)
        save.assert_called_with(request, formset)
