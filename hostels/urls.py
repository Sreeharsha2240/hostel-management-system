from django.urls import path

from . import api, views

urlpatterns = [
    path("hostels/", api.hostel_endpoint, name="hostel-list"),
    path("hostels/<int:pk>/edit/", views.hostel_update, name="hostel-update"),
    path("rooms/add/", views.room_create, name="room-create"),
    path("rooms/<int:pk>/edit/", views.room_update, name="room-update"),
    path("beds/", views.bed_list, name="bed-list"),
    path("hostels/<int:pk>/rooms/", api.room_create, name="api-room-create"),
    path("beds/available/", api.bed_availability, name="api-bed-availability"),
]
