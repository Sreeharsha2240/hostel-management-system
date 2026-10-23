
from django.urls import path

from . import views

urlpatterns = [
    path(
        "allocations/",
        views.allocation_list,
        name="allocation-list",
    ),
    path(
        "allocations/create/",
        views.allocation_create,
        name="allocation-create",
    ),
    path(
        "allocations/<int:pk>/complete/",
        views.allocation_complete,
        name="allocation-complete",
    ),
]
