from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django.db import transaction

from audit.mixins import AuditedAdminMixin
from audit.models import AuditEvent

from .forms import AdminPasswordChangeForm
from .models import User


class _AccountAdministrationPermissions:
    def has_module_permission(self, request):
        return request.user.is_superuser and request.user.role == User.Role.ADMIN

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_add_permission(self, request):
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request)


@admin.register(User)
class HMSUserAdmin(_AccountAdministrationPermissions, AuditedAdminMixin, UserAdmin):
    change_password_form = AdminPasswordChangeForm
    fieldsets = UserAdmin.fieldsets + (
        ("HMS access", {"fields": ("role", "failed_attempts", "locked_until")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (("HMS access", {"fields": ("role",)}),)
    readonly_fields = ("failed_attempts", "locked_until")

    def get_object(self, request, object_id, from_field=None):
        account = super().get_object(request, object_id, from_field)
        if account is not None and request.method == "POST":
            return User.objects.select_for_update().get(pk=account.pk)
        return account

    def save_model(self, request, obj, form, change):
        if not change:
            return super().save_model(request, obj, form, change)
        editable = {
            field.name
            for field in obj._meta.concrete_fields
            if field.editable and not field.primary_key
        }
        fields = set(form.changed_data).intersection(editable) - {"password"}
        previous = User.objects.get(pk=obj.pk)
        obj._audit_action = (
            AuditEvent.Action.DEACTIVATE
            if "is_active" in fields and previous.is_active and not obj.is_active
            else AuditEvent.Action.UPDATE
        )
        if fields:
            # Passwords use the separate password-change form. Group and
            # permission relationships are saved by Django's save_related.
            obj.save(update_fields=fields)

    @transaction.atomic
    def user_change_password(self, request, id, form_url=""):
        return super().user_change_password(request, id, form_url)

    def has_delete_permission(self, request, obj=None):
        return False  # Accounts are deactivated, never deleted.


admin.site.unregister(Group)


@admin.register(Group)
class HMSGroupAdmin(_AccountAdministrationPermissions, AuditedAdminMixin, GroupAdmin):
    """Treat permission-group changes as account administration too."""
