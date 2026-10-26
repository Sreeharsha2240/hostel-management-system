from django.contrib import admin

from .models import Allocation


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ("student", "bed", "allocated_on", "vacated_on", "status")
    readonly_fields = (
        "student",
        "bed",
        "allocated_on",
        "vacated_on",
        "status",
        "active_student_id",
        "active_bed_id",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
