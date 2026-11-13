"""Decorated report endpoints choose their report and enforce read-only methods."""

from types import SimpleNamespace
from unittest.mock import patch

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from accounts.models import User

from .views import occupancy_report, payment_status_report


class RemainingReportViewUnitTests(SimpleTestCase):
    def test_report_endpoints_select_kind_and_reject_writes_before_aggregation(self):
        factory = RequestFactory()
        actor = SimpleNamespace(is_authenticated=True, role=User.Role.WARDEN)
        for view, kind in (
            (occupancy_report, "occupancy"),
            (payment_status_report, "payment-status"),
        ):
            with (
                self.subTest(view=view.__name__),
                patch(
                    "reports.views.report_response", return_value=HttpResponse("report")
                ) as report,
            ):
                request = factory.get("/reports/", {"hostel": "3", "format": "csv"})
                request.user = actor
                self.assertEqual(view(request).content, b"report")
                report.assert_called_once_with(request, kind)
                report.reset_mock()
                request = factory.post("/reports/", {"hostel": "3"})
                request.user = actor
                response = view(request)
                self.assertEqual(response.status_code, 405)
                self.assertEqual(response["Allow"], "GET")
                report.assert_not_called()
