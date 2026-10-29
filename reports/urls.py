from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path(
        "reports/",
        RedirectView.as_view(pattern_name="occupancy-report", permanent=False),
        name="reports-home",
    ),
    path("reports/occupancy/", views.occupancy_report, name="occupancy-report"),
    path(
        "reports/payment-status/",
        views.payment_status_report,
        name="payment-status-report",
    ),
]
