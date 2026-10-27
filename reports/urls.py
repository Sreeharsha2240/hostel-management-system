from django.urls import path

from . import views

urlpatterns = [
    path("reports/occupancy/", views.occupancy_report, name="occupancy-report"),
    path(
        "reports/payment-status/",
        views.payment_status_report,
        name="payment-status-report",
    ),
]
