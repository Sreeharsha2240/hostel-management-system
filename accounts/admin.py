from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from audit.services import record_event

from .models import User


@admin.register(User)
class HMSUserAdmin(UserAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser and request.user.role == User.Role.ADMIN

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser and request.user.role == User.Role.ADMIN

    def has_add_permission(self, request):
        return request.user.is_superuser and request.user.role == User.Role.ADMIN

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.user.role == User.Role.ADMIN

    def has_delete_permission(self, request, obj=None):
        return False  # Accounts are deactivated, never deleted.

    def save_model(self, request, obj, form, change):
        was_active = None
        if change:
            was_active = User.objects.filter(pk=obj.pk).values_list('is_active', flat=True).first()
        super().save_model(request, obj, form, change)
        if not change:
            action = 'user_create'
        elif was_active and not obj.is_active:
            action = 'user_deactivate'
        else:
            action = 'user_update'
        record_event(action, actor=request.user, record_type='user', record_id=obj.pk)
