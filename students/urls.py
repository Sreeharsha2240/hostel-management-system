from django.urls import path

from . import views

urlpatterns = [
    path('students/', views.student_list, name='student-list'),
    path('students/new/', views.student_form, name='student-create'),
    path('students/<int:student_id>/', views.student_detail, name='student-detail'),
    path('students/<int:student_id>/edit/', views.student_form, name='student-update'),
    path('students/<int:student_id>/deactivate/', views.student_deactivate, name='student-deactivate'),
]
