from django.contrib import admin
from django.core.exceptions import ValidationError

from audit.mixins import AuditedAdminMixin, RoleRestrictedAdminMixin
from audit.models import AuditEvent
from audit.services import record_event

from .forms import RoomForm
from .models import Bed, Hostel, Room


class InventoryValidationAdminMixin:
    """Render a race-time model rejection as a bound admin form error."""

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        try:
            return super().changeform_view(request, object_id, form_url, extra_context)
        except ValidationError as error:
            # ModelAdmin's atomic block has rolled back every parent/inline save.
            request._inventory_validation_error = error
            return super().changeform_view(request, object_id, form_url, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        form_class = super().get_form(request, obj, **kwargs)
        error = getattr(request, "_inventory_validation_error", None)
        if error is None:
            return form_class

        class RejectedInventoryForm(form_class):
            def clean(self):
                cleaned = super().clean()
                if hasattr(error, "message_dict"):
                    for field, messages in error.message_dict.items():
                        self.add_error(
                            field if field in self.fields else None, messages
                        )
                else:
                    self.add_error(None, error.messages)
                return cleaned

        return RejectedInventoryForm


class RoomInline(RoleRestrictedAdminMixin, admin.TabularInline):
    write_roles = ("admin",)
    model = Room
    form = RoomForm
    extra = 1
    can_delete = False


class BedInline(RoleRestrictedAdminMixin, admin.TabularInline):
    write_roles = ("admin",)
    model = Bed
    extra = 0
    readonly_fields = ("label",)
    can_delete = False


def save_audited_formset(request, formset):
    """Save inline records with audit events in the admin transaction."""
    instances = formset.save(commit=False)
    for obj in instances:
        action = (
            AuditEvent.Action.CREATE if obj._state.adding else AuditEvent.Action.UPDATE
        )
        obj.save()
        record_event(user=request.user, action=action, record=obj)
    formset.save_m2m()


@admin.register(Hostel)
class HostelAdmin(InventoryValidationAdminMixin, AuditedAdminMixin, admin.ModelAdmin):
    write_roles = ("admin",)
    list_display = ("name", "hostel_type", "is_active")
    search_fields = ("name",)
    list_filter = ("hostel_type", "is_active")
    inlines = (RoomInline,)

    def save_formset(self, request, form, formset, change):
        save_audited_formset(request, formset)


@admin.register(Room)
class RoomAdmin(InventoryValidationAdminMixin, AuditedAdminMixin, admin.ModelAdmin):
    write_roles = ("admin",)
    form = RoomForm
    list_display = ("room_number", "hostel", "floor", "room_type", "capacity")
    list_filter = ("hostel", "floor", "room_type")
    search_fields = ("room_number", "hostel__name")
    inlines = (BedInline,)

    def save_formset(self, request, form, formset, change):
        save_audited_formset(request, formset)


@admin.register(Bed)
class BedAdmin(InventoryValidationAdminMixin, AuditedAdminMixin, admin.ModelAdmin):
    write_roles = ("admin",)
    list_display = ("label", "room", "status")
    list_filter = ("status", "room__hostel")
    search_fields = ("label", "room__room_number", "room__hostel__name")
