"""Hostel form rendering and denied-management boundaries without persistence."""

from types import SimpleNamespace
from unittest.mock import patch

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from accounts.models import User

from .models import Hostel, Room
from .views import hostel_list, hostel_update, room_create, room_update


class RemainingHostelViewUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin = SimpleNamespace(is_authenticated=True, role=User.Role.ADMIN)

    def request(self, method="get"):
        request = getattr(self.factory, method)("/hostels/", {"name": ""})
        request.user = self.admin
        return request

    def test_warden_cannot_update_hostels_or_create_or_update_rooms(self):
        for view, args, noun in (
            (hostel_update, (5,), "hostels"),
            (room_create, (), "rooms"),
            (room_update, (6,), "rooms"),
        ):
            with (
                self.subTest(view=view.__name__),
                patch("hostels.views.get_object_or_404") as lookup,
                patch("hostels.views.HostelForm") as hostel_form,
                patch("hostels.views.RoomForm") as room_form,
                patch("hostels.views.record_event") as audit,
            ):
                request = self.request("post")
                request.user = SimpleNamespace(
                    is_authenticated=True, role=User.Role.WARDEN
                )
                response = view(request, *args)
                self.assertEqual(response.status_code, 403)
                self.assertEqual(
                    response.content, f"Only admins can manage {noun}.".encode()
                )
                lookup.assert_not_called()
                hostel_form.assert_not_called()
                room_form.assert_not_called()
                audit.assert_not_called()

    def test_hostel_list_get_and_invalid_post_keep_form_and_current_hostels(self):
        for method in ("get", "post"):
            with (
                self.subTest(method=method),
                patch("hostels.views.HostelForm") as form_type,
                patch(
                    "hostels.views.Hostel.objects.all", return_value=["existing hostel"]
                ) as query,
                patch(
                    "hostels.views.render", return_value=HttpResponse("hostels")
                ) as render,
                patch("hostels.views.record_event") as audit,
            ):
                request = self.request(method)
                form = form_type.return_value
                form.is_valid.return_value = False
                self.assertEqual(hostel_list(request).content, b"hostels")
                form_type.assert_called_once_with(
                    request.POST if method == "post" else None
                )
                query.assert_called_once_with()
                render.assert_called_once_with(
                    request,
                    "hostels/hostel_list.html",
                    {"hostels": ["existing hostel"], "form": form},
                )
                form.save.assert_not_called()
                audit.assert_not_called()

    def test_hostel_and_room_forms_get_and_invalid_post_preserve_instance_and_heading(
        self,
    ):
        for view, args, model, form_name, template, heading in (
            (
                hostel_update,
                (5,),
                Hostel,
                "HostelForm",
                "hostels/hostel_form.html",
                "Edit Hostel",
            ),
            (room_create, (), None, "RoomForm", "hostels/room_form.html", "Add Room"),
            (
                room_update,
                (6,),
                Room,
                "RoomForm",
                "hostels/room_form.html",
                "Edit Room",
            ),
        ):
            for method in ("get", "post"):
                with (
                    self.subTest(view=view.__name__, method=method),
                    patch("hostels.views.get_object_or_404") as lookup,
                    patch(f"hostels.views.{form_name}") as form_type,
                    patch(
                        "hostels.views.render", return_value=HttpResponse("form")
                    ) as render,
                    patch("hostels.views.record_event") as audit,
                ):
                    request = self.request(method)
                    form = form_type.return_value
                    form.is_valid.return_value = False
                    self.assertEqual(view(request, *args).content, b"form")
                    data = request.POST if method == "post" else None
                    if model:
                        lookup.assert_called_once_with(model, pk=args[0])
                        form_type.assert_called_once_with(
                            data, instance=lookup.return_value
                        )
                    else:
                        lookup.assert_not_called()
                        form_type.assert_called_once_with(data)
                    render.assert_called_once_with(
                        request, template, {"form": form, "heading": heading}
                    )
                    form.save.assert_not_called()
                    audit.assert_not_called()
