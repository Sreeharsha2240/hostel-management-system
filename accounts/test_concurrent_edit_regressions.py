"""Limit settings writes so stale instances cannot restore account privileges."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group, Permission
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from audit.models import AuditEvent

from .admin import HMSUserAdmin
from .forms import AccountUpdateForm, ProfileSettingsForm
from .models import User


class AccountEditWriteUnitTests(SimpleTestCase):
    @patch("django.db.models.Model.save")
    def test_user_save_preserves_iterable_update_fields(self, save):
        User(role=User.Role.STUDENT).save(update_fields=iter(["first_name"]))

        self.assertEqual(set(save.call_args.kwargs["update_fields"]), {"first_name"})

    def test_group_permission_admin_rejects_warden_even_with_django_permissions(self):
        request = SimpleNamespace(
            user=Mock(
                is_superuser=False,
                role=User.Role.WARDEN,
                is_staff=True,
            )
        )
        request.user.has_perm.return_value = True
        model_admin = admin.site._registry[Group]

        self.assertFalse(model_admin.has_module_permission(request))
        self.assertFalse(model_admin.has_view_permission(request))
        self.assertFalse(model_admin.has_add_permission(request))
        self.assertFalse(model_admin.has_change_permission(request))
        self.assertFalse(model_admin.has_delete_permission(request))

    @patch("django.forms.models.BaseModelForm.save")
    def test_profile_edit_never_writes_stale_role_activation_or_password(self, parent):
        user = Mock()
        parent.return_value = user
        form = ProfileSettingsForm(instance=User(pk=7))

        self.assertIs(form.save(), user)

        parent.assert_called_once_with(commit=False)
        user.save.assert_called_once_with(update_fields=form.Meta.fields)

    @patch("django.forms.models.BaseModelForm.save")
    def test_role_edit_never_writes_stale_activation_or_password(self, parent):
        user = Mock()
        parent.return_value = user
        form = AccountUpdateForm(instance=User(pk=7))

        self.assertIs(form.save(), user)

        parent.assert_called_once_with(commit=False)
        user.save.assert_called_once_with(update_fields=form.Meta.fields)

    @patch("django.forms.models.BaseModelForm.save")
    def test_commit_false_does_not_persist_an_account_edit(self, parent):
        for form_type in (ProfileSettingsForm, AccountUpdateForm):
            with self.subTest(form=form_type.__name__):
                user = Mock()
                parent.return_value = user
                self.assertIs(form_type(instance=User(pk=7)).save(commit=False), user)
                user.save.assert_not_called()

    @patch("django.db.models.Model.save")
    def test_role_demotion_clears_staff_even_when_instance_predates_staff_grant(
        self, save
    ):
        user = User(pk=7, role=User.Role.STUDENT, is_staff=False)

        user.save(update_fields=["role"])

        self.assertIn("is_staff", save.call_args.kwargs["update_fields"])
        self.assertFalse(user.is_staff)

    @patch("django.contrib.auth.forms.AdminPasswordChangeForm.save")
    def test_admin_password_change_only_persists_password(self, parent):
        user = Mock()
        parent.return_value = user
        form_type = HMSUserAdmin(User, AdminSite()).change_password_form
        form = form_type(User(pk=7))

        self.assertIs(form.save(), user)

        parent.assert_called_once_with(commit=False)
        user.save.assert_called_once_with(update_fields=["password"])


class AccountStaleInstanceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="stale-account",
            password="Validpass123",
            role=User.Role.ADMIN,
            is_staff=True,
        )

    def revoke_account(self):
        current = User.objects.get(pk=self.user.pk)
        current.role = User.Role.STUDENT
        current.is_active = False
        current.save(update_fields=["role", "is_active"])

    def assert_account_stays_revoked(self):
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, User.Role.STUDENT)
        self.assertFalse(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_profile_edit_cannot_undo_a_concurrent_demotion_and_deactivation(self):
        form = ProfileSettingsForm({"first_name": "Edited"}, instance=self.user)
        self.assertTrue(form.is_valid(), form.errors)
        self.revoke_account()

        form.save()

        self.assert_account_stays_revoked()
        self.assertEqual(self.user.first_name, "Edited")

    def test_role_edit_cannot_reactivate_account_or_restore_old_password(self):
        form = AccountUpdateForm({"role": User.Role.WARDEN}, instance=self.user)
        self.assertTrue(form.is_valid(), form.errors)
        current = User.objects.get(pk=self.user.pk)
        current.is_active = False
        current.set_password("Changedpass456")
        current.save(update_fields=["is_active", "password"])

        form.save()

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertTrue(self.user.check_password("Changedpass456"))

    def test_settings_password_change_cannot_restore_revoked_privileges(self):
        # Exercise the concrete form class used by the settings view.
        from .views import PasswordChangeForm as SettingsPasswordChangeForm

        form = SettingsPasswordChangeForm(
            self.user,
            {
                "old_password": "Validpass123",
                "new_password1": "Changedpass456",
                "new_password2": "Changedpass456",
            },
        )
        self.assertIsInstance(form, PasswordChangeForm)
        self.assertTrue(form.is_valid(), form.errors)
        self.revoke_account()

        form.save()

        self.assert_account_stays_revoked()
        self.assertTrue(self.user.check_password("Changedpass456"))

    def test_admin_password_change_cannot_restore_revoked_privileges(self):
        form_type = HMSUserAdmin(User, AdminSite()).change_password_form
        form = form_type(
            self.user,
            {
                "password1": "Changedpass456",
                "password2": "Changedpass456",
            },
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.revoke_account()

        form.save()

        self.assert_account_stays_revoked()
        self.assertTrue(self.user.check_password("Changedpass456"))

    def test_regular_admin_edit_cannot_restore_stale_credentials_or_privileges(self):
        model_admin = HMSUserAdmin(User, AdminSite())
        stale = User.objects.get(pk=self.user.pk)
        stale.first_name = "Edited through admin"
        self.revoke_account()
        current = User.objects.get(pk=self.user.pk)
        current.set_password("Changedpass456")
        current.save(update_fields=["password"])

        model_admin.save_model(
            SimpleNamespace(user=self.user),
            stale,
            SimpleNamespace(changed_data=["first_name"]),
            change=True,
        )

        self.assert_account_stays_revoked()
        self.assertTrue(self.user.check_password("Changedpass456"))
        self.assertEqual(self.user.first_name, "Edited through admin")


class GroupAdministrationTests(TestCase):
    def test_warden_cannot_edit_permission_group_through_direct_admin_url(self):
        warden = User.objects.create_user(
            username="group-warden",
            role=User.Role.WARDEN,
            is_staff=True,
        )
        permission = Permission.objects.get(
            content_type__app_label="auth", codename="change_group"
        )
        warden.user_permissions.add(permission)
        group = Group.objects.create(name="Existing permission group")
        self.client.force_login(warden)

        response = self.client.get(reverse("admin:auth_group_change", args=[group.pk]))

        self.assertEqual(response.status_code, 403)

    def test_permission_group_changes_are_audited(self):
        administrator = User.objects.create_superuser(
            username="group-superuser", password="Validpass123"
        )
        self.client.force_login(administrator)

        response = self.client.post(
            reverse("admin:auth_group_add"), {"name": "Audited permission group"}
        )
        self.assertEqual(response.status_code, 302)
        group = Group.objects.get(name="Audited permission group")
        response = self.client.post(
            reverse("admin:auth_group_change", args=[group.pk]),
            {"name": "Renamed permission group"},
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            list(
                AuditEvent.objects.filter(
                    record_type="auth.group", record_id=str(group.pk)
                )
                .order_by("pk")
                .values_list("action", "user_id")
            ),
            [
                (AuditEvent.Action.CREATE, administrator.pk),
                (AuditEvent.Action.UPDATE, administrator.pk),
            ],
        )
