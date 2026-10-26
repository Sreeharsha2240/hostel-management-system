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
    path(
        "allocations/<int:pk>/transfer/",
        views.allocation_transfer,
        name="allocation-transfer",
    ),
    path(
        "allocations/<int:pk>/release/",
        views.allocation_release,
        name="allocation-release",
    ),
    path(
        "students/<int:pk>/allocations/",
        views.allocation_history,
        name="allocation-history",
    ),
]
