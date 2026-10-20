from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

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

