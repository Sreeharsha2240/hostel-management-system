"""Isolated checks for hostel management and bed-filter view decisions."""

from contextlib import nullcontext
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from accounts.models import User
from audit.models import AuditEvent

from .views import (
    bed_list,
    can_manage_hostels,
    hostel_list,
    hostel_update,
    room_create,
    room_update,
)


class HostelViewUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin = SimpleNamespace(is_authenticated=True, role=User.Role.ADMIN)

    def request(self, method="GET", data=None):
        request = getattr(self.factory, method.lower())("/hostels/", data or {})
        request.user = self.admin
        return request

    def test_only_authenticated_admin_can_manage_hostels(self):
        for authenticated, role, expected in (
            (False, User.Role.ADMIN, False),
            (True, User.Role.ADMIN, True),
            (True, User.Role.WARDEN, False),
            (True, User.Role.STUDENT, False),
        ):
            with self.subTest(authenticated=authenticated, role=role):
                self.assertEqual(
                    can_manage_hostels(
                        SimpleNamespace(is_authenticated=authenticated, role=role)
                    ),
                    expected,
                )

    @patch("hostels.views.HostelForm")
    def test_warden_cannot_open_hostel_management(self, form):
        request = self.request()
        request.user = SimpleNamespace(is_authenticated=True, role=User.Role.WARDEN)
        self.assertEqual(hostel_list(request).status_code, 403)
        form.assert_not_called()

    @patch("hostels.views.redirect", return_value=HttpResponse("ok"))
    @patch("hostels.views.record_event")
    @patch("hostels.views.transaction.atomic", return_value=nullcontext())
    @patch("hostels.views.HostelForm")
    def test_valid_hostel_creation_is_saved_and_audited(
        self, form, atomic, audit, redirect
    ):
        hostel = Mock()
        form.return_value.is_valid.return_value = True
        form.return_value.save.return_value = hostel
        self.assertEqual(
            hostel_list(self.request("POST", {"name": "A"})).content, b"ok"
        )
        audit.assert_called_once_with(
            user=self.admin, action=AuditEvent.Action.CREATE, record=hostel
        )
        redirect.assert_called_once_with("hostel-list")

    @patch("hostels.views.redirect", return_value=HttpResponse("ok"))
    @patch("hostels.views.record_event")
    @patch("hostels.views.Hostel.objects.values_list")
    @patch("hostels.views.transaction.atomic", return_value=nullcontext())
    @patch("hostels.views.HostelForm")
    @patch("hostels.views.get_object_or_404")
    def test_hostel_deactivation_uses_persisted_previous_state(
        self, lookup, form, atomic, previous, audit, redirect
    ):
        hostel = SimpleNamespace(pk=5, is_active=False)
        lookup.return_value = hostel
        previous.return_value.get.return_value = True
        form.return_value.is_valid.return_value = True
        form.return_value.save.return_value = hostel
        self.assertEqual(hostel_update(self.request("POST"), 5).content, b"ok")
        previous.return_value.get.assert_called_once_with(pk=5)
        audit.assert_called_once_with(
            user=self.admin, action=AuditEvent.Action.DEACTIVATE, record=hostel
        )

    @patch("hostels.views.redirect", return_value=HttpResponse("ok"))
    @patch("hostels.views.record_event")
    @patch("hostels.views.transaction.atomic", return_value=nullcontext())
    @patch("hostels.views.RoomForm")
    def test_valid_room_creation_is_saved_and_audited(
        self, form, atomic, audit, redirect
    ):
        room = Mock()
        form.return_value.is_valid.return_value = True
        form.return_value.save.return_value = room
        self.assertEqual(room_create(self.request("POST")).content, b"ok")
        audit.assert_called_once_with(
            user=self.admin, action=AuditEvent.Action.CREATE, record=room
        )
        redirect.assert_called_once_with("bed-list")

    @patch("hostels.views.redirect", return_value=HttpResponse("ok"))
    @patch("hostels.views.record_event")
    @patch("hostels.views.transaction.atomic", return_value=nullcontext())
    @patch("hostels.views.RoomForm")
    @patch("hostels.views.get_object_or_404")
    def test_valid_room_update_is_saved_and_audited(
        self, lookup, form, atomic, audit, redirect
    ):
        room = Mock()
        lookup.return_value = room
        form.return_value.is_valid.return_value = True
        form.return_value.save.return_value = room
        self.assertEqual(room_update(self.request("POST"), 8).content, b"ok")
        form.assert_called_once_with(self.request("POST").POST, instance=room)
        audit.assert_called_once_with(
            user=self.admin, action=AuditEvent.Action.UPDATE, record=room
        )

    @patch("hostels.views.render", return_value=HttpResponse("beds"))
    @patch("hostels.views.Hostel.objects.filter")
    @patch("hostels.views.Paginator")
    @patch("hostels.views.Bed.objects.select_related")
    def test_invalid_bed_filter_returns_400_and_empty_queryset(
        self, beds, paginator, hostels, render
    ):
        request = self.request(data={"floor": "-1"})
        self.assertEqual(bed_list(request).content, b"beds")
        beds.return_value.none.assert_called_once()
        self.assertEqual(render.call_args.kwargs["status"], 400)

    @patch("hostels.views.render", return_value=HttpResponse("beds"))
    @patch("hostels.views.Hostel.objects.filter")
    @patch("hostels.views.Paginator")
    @patch("hostels.views.Bed.objects.select_related")
    def test_valid_bed_filters_are_applied_and_retained(
        self, beds, paginator, hostels, render
    ):
        filtered = beds.return_value
        filtered.filter.return_value = filtered
        request = self.request(
            data={
                "hostel": "2",
                "floor": "1",
                "room_type": "Double",
                "status": "Available",
            }
        )
        self.assertEqual(bed_list(request).content, b"beds")
        self.assertEqual(filtered.filter.call_count, 4)
        context = render.call_args.args[2]
        self.assertEqual(
            (context["selected_hostel"], context["selected_floor"]), ("2", "1")
        )
        self.assertEqual(render.call_args.kwargs["status"], 200)
