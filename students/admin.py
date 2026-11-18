from django.contrib import admin

from audit.mixins import AuditedAdminMixin

from .forms import StudentForm
from .models import Student


@admin.register(Student)
class StudentAdmin(AuditedAdminMixin, admin.ModelAdmin):
    form = StudentForm
    list_display = ("student_id", "name", "course", "year", "mobile", "status")
    search_fields = ("student_id", "name", "email", "course", "mobile")
    list_filter = ("status", "gender", "course", "year")
    ordering = ("name",)

    def get_object(self, request, object_id, from_field=None):
        student = super().get_object(request, object_id, from_field)
        if student is not None and request.method == "POST":
            # Django wraps POST change forms in a transaction. Keep eligibility
            # checks and save serialized with allocation's student row lock.
            return Student.objects.select_for_update().get(pk=student.pk)
        return student

    def get_readonly_fields(self, request, obj=None):
        return ("student_id",) if obj is not None else ()
