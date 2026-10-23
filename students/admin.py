from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "name", "course", "year", "mobile", "status")
    search_fields = ("student_id", "name", "email", "course", "mobile")
    list_filter = ("status", "gender", "course", "year")
    ordering = ("name",)