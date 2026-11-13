"""Audit filtering and pagination with only the persistence boundary replaced."""

import json
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import patch

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from accounts.models import User

from .models import AuditEvent
from .views import event_list


class AuditEventListUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = SimpleNamespace(is_authenticated=True, role=User.Role.ADMIN)
        self.events = [
            AuditEvent(
                pk=index,
                user_id=7 if index % 2 else None,
                action=AuditEvent.Action.CREATE,
                record_type="students.student",
                record_id=str(100 + index),
                timestamp=datetime(2026, 11, 13, 12, tzinfo=UTC)
                - timedelta(minutes=index),
            )
            for index in range(1, 28)
        ]

    def request(self, parameters=None, *, json_output=True):
        request = self.factory.get(
            "/audit/",
            parameters or {},
            HTTP_ACCEPT="application/json" if json_output else "text/html",
        )
        request.user = self.user
        return request

    def serialized(self, events):
        return [
            {
                "id": event.pk,
                "user_id": event.user_id,
                "action": event.action,
                "record_type": event.record_type,
                "record_id": event.record_id,
                "timestamp": event.timestamp.isoformat(),
            }
            for event in events
        ]

    @patch("audit.views.AuditEvent.objects.select_related")
    def test_valid_action_filters_before_real_pagination_and_serializes_all_fields(
        self, select_related
    ):
        select_related.return_value.filter.return_value = self.events

        response = event_list(self.request({"action": "create", "page": "2"}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {"results": self.serialized(self.events[25:]), "page": 2, "total": 27},
        )
        select_related.assert_called_once_with("user")
        select_related.return_value.filter.assert_called_once_with(action="create")

    @patch("audit.views.render", return_value=HttpResponse("audit template"))
    @patch("audit.views.AuditEvent.objects.select_related")
    def test_invalid_action_is_not_filtered_and_is_preserved_in_html_context(
        self, select_related, render
    ):
        for action in ("unknown", "CREATE", "create ", ""):
            with self.subTest(action=action):
                # A plain result list also rejects an unintended filter() call.
                select_related.return_value = self.events
                request = self.request({"action": action}, json_output=False)

                response = event_list(request)

                self.assertIs(response, render.return_value)
                select_related.assert_called_with("user")
                rendered_request, template, context = render.call_args.args
                self.assertIs(rendered_request, request)
                self.assertEqual(template, "audit/event_list.html")
                self.assertEqual(context["action"], action)
                self.assertEqual(context["actions"], AuditEvent.Action.choices)
                page = context["page_obj"]
                self.assertEqual(list(page), self.events[:25])
                self.assertEqual(page.number, 1)
                self.assertEqual(page.paginator.count, 27)
                self.assertEqual(page.paginator.per_page, 25)

    @patch("audit.views.AuditEvent.objects.select_related")
    def test_real_paginator_handles_invalid_and_out_of_range_page_parameters(
        self, select_related
    ):
        select_related.return_value = self.events
        for parameter, number, expected in (
            ("nonnumeric", 1, self.events[:25]),
            ("0", 2, self.events[25:]),
            ("-1", 2, self.events[25:]),
            ("999999", 2, self.events[25:]),
        ):
            with self.subTest(page=parameter):
                response = event_list(self.request({"page": parameter}))

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    json.loads(response.content),
                    {"results": self.serialized(expected), "page": number, "total": 27},
                )

    @patch("audit.views.AuditEvent.objects.select_related", return_value=[])
    def test_empty_audit_log_still_has_one_empty_page(self, select_related):
        response = event_list(self.request({"page": "999999"}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content), {"results": [], "page": 1, "total": 0}
        )
        select_related.assert_called_once_with("user")

    @patch("audit.views.render", return_value=HttpResponse("filtered audit template"))
    @patch("audit.views.AuditEvent.objects.select_related")
    def test_html_context_contains_filtered_page_and_action_choices(
        self, select_related, render
    ):
        filtered_events = self.events[25:]
        for event in filtered_events:
            event.action = AuditEvent.Action.RELEASE
        select_related.return_value.filter.return_value = filtered_events
        request = self.request({"action": "release"}, json_output=False)

        response = event_list(request)

        self.assertIs(response, render.return_value)
        select_related.return_value.filter.assert_called_once_with(action="release")
        rendered_request, template, context = render.call_args.args
        self.assertIs(rendered_request, request)
        self.assertEqual(template, "audit/event_list.html")
        self.assertEqual(context["action"], "release")
        self.assertEqual(context["actions"], AuditEvent.Action.choices)
        self.assertEqual(list(context["page_obj"]), filtered_events)
        self.assertEqual(context["page_obj"].paginator.count, 2)
