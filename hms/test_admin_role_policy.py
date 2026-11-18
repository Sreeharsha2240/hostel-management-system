"""Staff/model permissions must not bypass HMS business roles in Django admin."""

from types import SimpleNamespace
from unittest.mock import Mock

from django.contrib.admin.sites import AdminSite
from django.test import SimpleTestCase

from allocations.admin import AllocationAdmin
from allocations.models import Allocation
from hostels.admin import BedAdmin, BedInline, HostelAdmin, RoomAdmin, RoomInline
from hostels.models import Bed, Hostel, Room
from payments.admin import PaymentAdmin
from payments.models import Payment
from students.admin import StudentAdmin
from students.models import Student


class AdminRolePolicyTests(SimpleTestCase):
    def test_inline_add_permission_accepts_its_parent_object(self):
        for inline_class, parent in ((RoomInline, Hostel), (BedInline, Room)):
            inline = inline_class(parent, AdminSite())
            self.assertTrue(inline.has_add_permission(self.request("admin"), parent()))
            self.assertFalse(
                inline.has_add_permission(self.request("warden"), parent())
            )

    def request(self, role):
        user = SimpleNamespace(
            is_authenticated=True,
            is_active=True,
            is_staff=True,
            is_superuser=False,
            role=role,
            has_perm=Mock(return_value=True),
            has_module_perms=Mock(return_value=True),
        )
        return SimpleNamespace(user=user)

    def test_warden_inventory_is_read_only_despite_all_django_permissions(self):
        request = self.request("warden")
        for admin_class, model in (
            (HostelAdmin, Hostel),
            (RoomAdmin, Room),
            (BedAdmin, Bed),
        ):
            with self.subTest(model=model.__name__):
                admin = admin_class(model, AdminSite())
                self.assertTrue(admin.has_module_permission(request))
                self.assertTrue(admin.has_view_permission(request))
                self.assertFalse(admin.has_add_permission(request))
                self.assertFalse(admin.has_change_permission(request))

    def test_admin_inventory_and_warden_student_management_remain_allowed(self):
        request = self.request("admin")
        for admin_class, model in (
            (HostelAdmin, Hostel),
            (RoomAdmin, Room),
            (BedAdmin, Bed),
        ):
            admin = admin_class(model, AdminSite())
            self.assertTrue(admin.has_add_permission(request))
            self.assertTrue(admin.has_change_permission(request))
        students = StudentAdmin(Student, AdminSite())
        self.assertTrue(students.has_add_permission(self.request("warden")))
        self.assertTrue(students.has_change_permission(self.request("warden")))

    def test_student_or_unknown_role_cannot_read_legacy_staff_admin_records(self):
        for role in ("student", "unknown"):
            request = self.request(role)
            for admin_class, model in (
                (StudentAdmin, Student),
                (HostelAdmin, Hostel),
                (RoomAdmin, Room),
                (BedAdmin, Bed),
                (AllocationAdmin, Allocation),
                (PaymentAdmin, Payment),
            ):
                with self.subTest(role=role, model=model.__name__):
                    admin = admin_class(model, AdminSite())
                    self.assertFalse(admin.has_module_permission(request))
                    self.assertFalse(admin.has_view_permission(request))
                    self.assertFalse(admin.has_add_permission(request))
                    self.assertFalse(admin.has_change_permission(request))
