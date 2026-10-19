from django.contrib import admin

from .models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'actor', 'action', 'record_type', 'record_id')
    list_filter = ('action', 'record_type', 'timestamp')
    search_fields = ('record_id', 'actor__username')
    readonly_fields = ('actor', 'action', 'record_type', 'record_id', 'timestamp')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
