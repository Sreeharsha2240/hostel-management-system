"""The hostel, room, and available-bed JSON interfaces from SAD section 4.3."""

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from accounts.models import User
from allocations.views import available_beds
from audit.models import AuditEvent
from audit.services import record_event
from hms.api import api_payload, api_roles_required, validate_api_types
from hms.http import api_error, wants_json
from hms.responses import form_error_response, validation_response

from .forms import BedFilterForm, HostelForm, RoomForm
from .models import Bed, Hostel, Room


def hostel_endpoint(request):
    """Preserve the HTML view while authenticating JSON before redirect logic."""
    if request.method == "POST" and wants_json(request):
        return hostel_create(request)
    from .views import hostel_list

    return hostel_list(request)


@api_roles_required(User.Role.ADMIN)
@require_POST
def hostel_create(request):
    try:
        data = api_payload(request, {"name", "type"})
        validate_api_types(data, text_fields=("name", "type"))
        form = HostelForm(
            {
                "name": data.get("name"),
                "hostel_type": data.get("type"),
                "is_active": True,
            }
        )
        if not form.is_valid():
            if form.has_error("name", "unique"):
                return api_error(
                    "A hostel with that name already exists.",
                    code="DUPLICATE",
                    status=409,
                )
            return form_error_response(form)
        with transaction.atomic():
            hostel = form.save()
            record_event(
                user=request.user, action=AuditEvent.Action.CREATE, record=hostel
            )
        return JsonResponse({"id": hostel.pk}, status=201)
    except IntegrityError:
        return api_error(
            "A hostel with that name already exists.", code="DUPLICATE", status=409
        )
    except ValidationError as error:
        return validation_response(error)


@api_roles_required(User.Role.ADMIN)
@require_POST
def room_create(request, pk):
    hostel = get_object_or_404(Hostel, pk=pk)
    try:
        data = dict(
            api_payload(
                request, {"room_number", "floor", "room_type", "capacity", "fee_amount"}
            )
        )
        if request.content_type != "application/json":
            data = request.POST.dict()
        validate_api_types(data, text_fields=("room_number", "room_type"))
        if request.content_type == "application/json":
            validate_api_types(data, integer_fields=("floor", "capacity"))
        if isinstance(data.get("fee_amount"), bool):
            raise ValidationError("Enter a valid room fee.")
        data["hostel"] = hostel.pk
        form = RoomForm(data)
        if not form.is_valid():
            if any(
                error.code == "unique_together"
                for error in form.non_field_errors().as_data()
            ):
                return api_error(
                    "That room number already exists in this hostel.",
                    code="DUPLICATE",
                    status=409,
                )
            return form_error_response(form)
        with transaction.atomic():
            room = form.save()
            record_event(
                user=request.user, action=AuditEvent.Action.CREATE, record=room
            )
        return JsonResponse(
            {
                "room_id": room.pk,
                "beds": [
                    {"id": bed.pk, "label": bed.label, "status": bed.status}
                    for bed in room.beds.order_by("pk")
                ],
            },
            status=201,
        )
    except IntegrityError:
        return api_error(
            "That room number already exists in this hostel.",
            code="DUPLICATE",
            status=409,
        )
    except ValidationError as error:
        return validation_response(error)


@api_roles_required(User.Role.ADMIN, User.Role.WARDEN)
@require_GET
def bed_availability(request):
    if set(request.GET).difference({"hostel", "floor", "room_type"}):
        return api_error("The request contains unsupported filters.")
    form = BedFilterForm(request.GET)
    if not form.is_valid():
        return form_error_response(form)
    beds = available_beds()
    for key, lookup in (("hostel", "room__hostel_id"), ("floor", "room__floor")):
        if form.cleaned_data[key] is not None:
            beds = beds.filter(**{lookup: form.cleaned_data[key]})
    room_type = request.GET.get("room_type")
    if room_type:
        if room_type not in Room.RoomType.values:
            return api_error("Choose a valid room type.")
        beds = beds.filter(room__room_type=room_type)
    return JsonResponse(
        {
            "beds": [
                {
                    "id": bed.pk,
                    "label": bed.label,
                    "status": Bed.BedStatus.AVAILABLE,
                    "room_id": bed.room_id,
                    "room_number": bed.room.room_number,
                    "hostel_id": bed.room.hostel_id,
                    "hostel": bed.room.hostel.name,
                }
                for bed in beds.order_by("room_id", "label")
            ]
        }
    )
