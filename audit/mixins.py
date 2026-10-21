from .models import AuditEvent
from .services import record_event


class AuditedAdminMixin:
    """Include changes made through Django admin in the application audit log."""

    def save_model(self, request, obj, form, change):
        action = AuditEvent.Action.UPDATE if change else AuditEvent.Action.CREATE
        if change and hasattr(obj, 'is_active') and not obj.is_active:
            previous = type(obj).objects.get(pk=obj.pk)
            if previous.is_active:
                action = AuditEvent.Action.DEACTIVATE
        obj._audit_action = action
        super().save_model(request, obj, form, change)

    def log_addition(self, request, obj, message):
        super().log_addition(request, obj, message)
        record_event(user=request.user, action=AuditEvent.Action.CREATE, record=obj)

    def log_change(self, request, obj, message):
        super().log_change(request, obj, message)
        record_event(
            user=request.user,
            action=getattr(obj, '_audit_action', AuditEvent.Action.UPDATE),
            record=obj,
        )
