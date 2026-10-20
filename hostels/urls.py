from django.urls import path

from . import views

urlpatterns = [
    path('hostels/', views.hostel_list, name='hostel-list'),
    path('hostels/new/', views.hostel_form, name='hostel-create'),
    path('hostels/<int:hostel_id>/', views.hostel_detail, name='hostel-detail'),
    path('hostels/<int:hostel_id>/edit/', views.hostel_form, name='hostel-update'),
    path('hostels/<int:hostel_id>/rooms/', views.room_form, name='room-create'),
    path('rooms/<int:room_id>/edit/', views.room_form, name='room-update'),
    path('beds/<int:bed_id>/edit/', views.bed_status, name='bed-update'),
    path('beds/available/', views.available_beds, name='available-beds'),
]
