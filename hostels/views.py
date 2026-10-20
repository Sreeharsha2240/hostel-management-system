from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from accounts.decorators import roles_required
from accounts.models import User
from audit.models import AuditEvent
from audit.services import record_event
from hms.forms import bind_model_form as bind_form
from hms.http import add_validation_errors, form_error, wants_json

from .forms import AvailableBedFilterForm, BedStatusForm, HostelForm, RoomForm
from .models import Bed, Hostel, Room
from .services import save_room_with_audit


STAFF_ROLES = (User.Role.ADMIN, User.Role.WARDEN)


def invalid_form(request, form, **context):
    duplicate = any(
        error.code in ('unique', 'unique_together', 'conflict')
        for errors in form.errors.as_data().values() for error in errors
    )
    status = 409 if duplicate else 400
    response = form_error(request, form, status=status, code='DUPLICATE' if duplicate else 'VALIDATION_ERROR')
    return response or render(request, 'hostels/form.html', {'form': form, **context}, status=status)


@roles_required(*STAFF_ROLES)
@require_http_methods(['GET', 'POST'])
def hostel_list(request):
    if request.method == 'POST':
        return hostel_form(request)
    hostels = Hostel.objects.annotate(
        room_count=Count('rooms', distinct=True), bed_count=Count('rooms__beds', distinct=True),
    ).order_by('name', 'pk')
    page = Paginator(hostels, 25).get_page(request.GET.get('page'))
    if wants_json(request):
        return JsonResponse({'results': [
            {'id': hostel.pk, 'name': hostel.name, 'type': hostel.type,
             'rooms': hostel.room_count, 'beds': hostel.bed_count} for hostel in page
        ], 'page': page.number, 'total': page.paginator.count})
    return render(request, 'hostels/hostel_list.html', {'page_obj': page})


@roles_required(User.Role.ADMIN)
@require_http_methods(['GET', 'POST', 'PATCH'])
def hostel_form(request, hostel_id=None):
    hostel = get_object_or_404(Hostel, pk=hostel_id) if hostel_id else Hostel()
    creating = hostel.pk is None
    form = bind_form(request, HostelForm, instance=hostel)
    title = 'Add hostel' if creating else 'Edit hostel'
    if request.method != 'GET':
        if form.is_valid():
            try:
                with transaction.atomic():
                    if not creating:
                        Hostel.objects.select_for_update().get(pk=hostel.pk)
                    hostel = form.save()
                    record_event(
                        user=request.user,
                        action=AuditEvent.Action.CREATE if creating else AuditEvent.Action.UPDATE,
                        record=hostel,
                    )
            except ValidationError as error:
                add_validation_errors(form, error)
            except IntegrityError:
                form.add_error('name', ValidationError('Hostel name already exists.', code='conflict'))
            else:
                if wants_json(request):
                    return JsonResponse({'id': hostel.pk, 'name': hostel.name, 'type': hostel.type}, status=201 if creating else 200)
                messages.success(request, 'Hostel saved.')
                return redirect('hostel-detail', hostel_id=hostel.pk)
        return invalid_form(request, form, title=title)
    if wants_json(request) and not creating:
        return JsonResponse({'id': hostel.pk, 'name': hostel.name, 'type': hostel.type})
    return render(request, 'hostels/form.html', {'form': form, 'title': title})


@roles_required(*STAFF_ROLES)
@require_GET
def hostel_detail(request, hostel_id):
    hostel = get_object_or_404(Hostel, pk=hostel_id)
    rooms = hostel.rooms.prefetch_related('beds')
    return render(request, 'hostels/hostel_detail.html', {'hostel': hostel, 'rooms': rooms})


@roles_required(User.Role.ADMIN)
@require_http_methods(['GET', 'POST', 'PATCH'])
def room_form(request, hostel_id=None, room_id=None):
    room = get_object_or_404(Room.objects.select_related('hostel'), pk=room_id) if room_id else Room(
        hostel=get_object_or_404(Hostel, pk=hostel_id),
    )
    creating = room.pk is None
    form = bind_form(request, RoomForm, instance=room)
    title = f'{"Add" if creating else "Edit"} room in {room.hostel.name}'
    if request.method != 'GET':
        if form.is_valid():
            try:
                room = save_room_with_audit(form.save(commit=False), actor=request.user)
            except ValidationError as error:
                add_validation_errors(form, error)
            except IntegrityError:
                form.add_error(None, ValidationError('Room already exists in this hostel.', code='conflict'))
            else:
                if wants_json(request):
                    return JsonResponse({
                        'room_id': room.pk,
                        'beds': list(room.beds.values('id', 'bed_number', 'status')),
                    }, status=201 if creating else 200)
                messages.success(request, 'Room and beds saved.')
                return redirect('hostel-detail', hostel_id=room.hostel_id)
        return invalid_form(request, form, title=title)
    return render(request, 'hostels/form.html', {'form': form, 'title': title})


@roles_required(User.Role.ADMIN)
@require_http_methods(['GET', 'POST', 'PATCH'])
def bed_status(request, bed_id):
    bed = get_object_or_404(Bed.objects.select_related('room__hostel'), pk=bed_id)
    form = bind_form(request, BedStatusForm, instance=bed)
    title = f'Edit {bed}'
    if request.method != 'GET':
        if form.is_valid():
            try:
                with transaction.atomic():
                    bed = Bed.objects.select_for_update().get(pk=bed.pk)
                    bed.status = form.cleaned_data['status']
                    bed.save(update_fields=['status'])
                    record_event(user=request.user, action=AuditEvent.Action.UPDATE, record=bed)
            except ValidationError as error:
                add_validation_errors(form, error)
            else:
                if wants_json(request):
                    return JsonResponse({'id': bed.pk, 'status': bed.status})
                messages.success(request, 'Bed status saved.')
                return redirect('hostel-detail', hostel_id=bed.room.hostel_id)
        return invalid_form(request, form, title=title)
    return render(request, 'hostels/form.html', {'form': form, 'title': title})


@roles_required(*STAFF_ROLES)
@require_GET
def available_beds(request):
    form = AvailableBedFilterForm(request.GET)
    beds = Bed.objects.select_related('room__hostel').filter(status=Bed.Status.AVAILABLE)
    valid = form.is_valid()
    if valid:
        for field, lookup in (('hostel', 'room__hostel'), ('floor', 'room__floor'), ('room_type', 'room__room_type')):
            value = form.cleaned_data[field]
            if value is not None and value != '':
                beds = beds.filter(**{lookup: value})
    else:
        beds = beds.none()
        response = form_error(request, form)
        if response:
            return response
    page = Paginator(beds, 25).get_page(request.GET.get('page'))
    if wants_json(request):
        return JsonResponse({'beds': [
            {'id': bed.pk, 'bed_number': bed.bed_number, 'status': bed.status,
             'hostel_id': bed.room.hostel_id, 'hostel': bed.room.hostel.name,
             'floor': bed.room.floor, 'room_type': bed.room.room_type} for bed in page
        ], 'page': page.number, 'total': page.paginator.count})
    return render(request, 'hostels/available_beds.html', {
        'form': form, 'page_obj': page,
    }, status=200 if valid else 400)
