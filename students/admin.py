from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'course', 'year', 'status')
    search_fields = ('student_id', 'name')
    list_filter = ('status', 'gender')

    def has_module_permission(self, request):
        return request.user.is_superuser and request.user.role == 'admin'

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
