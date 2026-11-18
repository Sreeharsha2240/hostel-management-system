"""SAD student JSON interfaces; authorization never depends on browser headers."""

from django import forms
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from accounts.models import User
from allocations.models import Allocation
from audit.models import AuditEvent
from audit.services import record_event
from hms.api import api_payload, api_roles_required, validate_api_types
from hms.http import api_error
from hms.responses import form_error_response, validation_response
from hostels.models import Hostel
from payments.services import payment_status_queryset, status_row

from .forms import StudentForm
from .models import Student

CREATE_FIELDS = {
    "student_id",
    "name",
    "dob",
    "gender",
    "course",
    "year",
    "mobile",
    "email",
    "guardian_name",
    "guardian_mobile",
    "address",
}
EDIT_FIELDS = {
    "mobile",
    "email",
    "course",
    "year",
    "guardian_name",
    "guardian_mobile",
    "address",
}


def serialize(student):
    return {
        "id": student.pk,
        "student_id": student.student_id,
        "name": student.name,
        "dob": student.date_of_birth.isoformat(),
        "gender": student.gender,
        "course": student.course,
        "year": student.year,
        "mobile": student.mobile,
        "email": student.email,
        "guardian_name": student.guardian_name,
        "guardian_mobile": student.guardian_mobile,
        "address": student.address,
        "status": student.status,
    }


def _duplicate_student(form=None):
    return api_error(
        "Student ID already registered",
        code="DUPLICATE",
        status=409,
        fields=form.errors.get_json_data() if form is not None else None,
    )


@api_roles_required(User.Role.ADMIN, User.Role.WARDEN)
@require_http_methods(["GET", "POST"])
def student_collection(request):
    if request.method == "POST":
        return _student_create(request)
    students = Student.objects.all()
    query = request.GET.get("q", "").strip()
    if query:
        students = students.filter(
            Q(student_id__icontains=query)
            | Q(name__icontains=query)
            | Q(
                allocations__status=Allocation.AllocationStatus.ACTIVE,
                allocations__bed__room__hostel__name__icontains=query,
            )
        ).distinct()
    hostel = request.GET.get("hostel", "")
    if hostel:
        try:
            hostel_id = forms.IntegerField(
                min_value=1, max_value=9223372036854775807
            ).clean(hostel)
        except ValidationError as error:
            return validation_response(error)
        get_object_or_404(Hostel, pk=hostel_id)
        students = students.filter(
            allocations__status=Allocation.AllocationStatus.ACTIVE,
            allocations__bed__room__hostel_id=hostel_id,
        ).distinct()
    page = Paginator(students, 25).get_page(request.GET.get("page"))
    return JsonResponse(
        {
            "results": [serialize(student) for student in page],
            "page": page.number,
            "total": page.paginator.count,
        }
    )


def _student_create(request):
    try:
        data = api_payload(request, CREATE_FIELDS)
        validate_api_types(
            data, text_fields=CREATE_FIELDS - {"year"}, integer_fields={"year"}
        )
    except ValidationError as error:
        return validation_response(error)
    values = dict(data.items())
    if "dob" in values:
        values["date_of_birth"] = values.pop("dob")
    values["status"] = Student.Status.ACTIVE
    form = StudentForm(values)
    if not form.is_valid():
        if any(
            error.message == "Student ID already registered"
            for error in form.errors.as_data().get("student_id", [])
        ):
            return _duplicate_student(form)
        return form_error_response(form)
    try:
        with transaction.atomic():
            student = form.save()
            record_event(
                user=request.user, action=AuditEvent.Action.CREATE, record=student
            )
    except IntegrityError:
        if Student.objects.filter(
            student_id__iexact=form.cleaned_data["student_id"]
        ).exists():
            return _duplicate_student()
        raise
    return JsonResponse(
        {"id": student.pk, "student_id": student.student_id, "name": student.name},
        status=201,
    )


@api_roles_required(User.Role.ADMIN, User.Role.WARDEN)
@require_http_methods(["PATCH"])
def student_update(request, pk):
    try:
        data = api_payload(request, EDIT_FIELDS | {"student_id"})
        validate_api_types(
            data,
            text_fields=(EDIT_FIELDS | {"student_id"}) - {"year"},
            integer_fields={"year"},
        )
        if not data:
            raise ValidationError("Supply at least one field to update.")
    except ValidationError as error:
        return validation_response(error)

    with transaction.atomic():
        student = get_object_or_404(Student.objects.select_for_update(), pk=pk)
        if "student_id" in data and data["student_id"] != student.student_id:
            return api_error(
                "Student ID cannot be changed.", code="IMMUTABLE_FIELD", status=422
            )
        values = model_to_dict(student)
        values.update({key: value for key, value in data.items() if key in EDIT_FIELDS})
        form = StudentForm(values, instance=student)
        for field in set(form.fields) - EDIT_FIELDS:
            form.fields.pop(field)
        if not form.is_valid():
            return form_error_response(form)
        if form.has_changed():
            student = form.save()
            record_event(
                user=request.user, action=AuditEvent.Action.UPDATE, record=student
            )
    return JsonResponse({"student": serialize(student)})


@api_roles_required(User.Role.ADMIN, User.Role.WARDEN)
@require_POST
def student_deactivate(request, pk):
    try:
        if request.content_type != "application/json" or request.body:
            api_payload(request, set())
    except ValidationError as error:
        return validation_response(error)
    with transaction.atomic():
        student = get_object_or_404(Student.objects.select_for_update(), pk=pk)
        allocation = (
            student.allocations.filter(status=Allocation.AllocationStatus.ACTIVE)
            .select_related("bed")
            .first()
        )
        if allocation:
            return api_error(
                f"Release active bed {allocation.bed.label} before deactivation.",
                code="HAS_ACTIVE_ALLOCATION",
                status=409,
            )
        if student.status != Student.Status.INACTIVE:
            student.status = Student.Status.INACTIVE
            student.save(update_fields={"status", "updated_at"})
            record_event(
                user=request.user, action=AuditEvent.Action.DEACTIVATE, record=student
            )
    return JsonResponse({"status": student.status})


@api_roles_required(User.Role.STUDENT)
@require_GET
def my_records(request):
    student = payment_status_queryset(
        Student.objects.filter(user_id=request.user.pk)
    ).first()
    if student is None:
        return JsonResponse(
            {"profile": None, "allocation": None, "payment_status": None}
        )
    allocation = (
        student.allocations.filter(status=Allocation.AllocationStatus.ACTIVE)
        .select_related("bed__room__hostel")
        .first()
    )
    current = None
    if allocation is not None:
        current = {
            "allocation_id": allocation.pk,
            "bed_id": allocation.bed_id,
            "bed": allocation.bed.label,
            "room": allocation.bed.room.room_number,
            "hostel": allocation.bed.room.hostel.name,
            "allocated_on": allocation.allocated_on.isoformat(),
        }
    return JsonResponse(
        {
            "profile": serialize(student),
            "allocation": current,
            "payment_status": status_row(student),
        }
    )
