from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from accounts.decorators import roles_required
from accounts.models import User
from allocations.models import Allocation
from audit.models import AuditEvent
from audit.services import record_event
from hms.http import wants_json
from payments.models import Payment
from payments.services import payment_status_queryset, status_row

from . import api
from .forms import StudentForm
from .models import Student


def can_manage_students(user):
    return user.is_authenticated and user.role in (
        User.Role.ADMIN,
        User.Role.WARDEN,
    )


def _access_denied(request, view_name, message):
    record_event(
        user=request.user,
        action=AuditEvent.Action.ACCESS_DENIED,
        record_type="view",
        record_id=view_name,
    )
    request._access_denied_audited = True
    return HttpResponseForbidden(message)


def _json_requests(api_view):
    def decorate(html_view):
        @wraps(html_view)
        def wrapped(request, *args, **kwargs):
            if wants_json(request):
                return api_view(request, *args, **kwargs)
            return html_view(request, *args, **kwargs)

        return wrapped

    return decorate


def _add_duplicate_error(form):
    if (
        Student.objects.filter(student_id__iexact=form.cleaned_data["student_id"])
        .exclude(pk=form.instance.pk)
        .exists()
    ):
        form.add_error("student_id", "Student ID already registered")
        return
    account = form.cleaned_data.get("user")
    if (
        account is not None
        and Student.objects.filter(user=account).exclude(pk=form.instance.pk).exists()
    ):
        form.add_error("user", "This account is already linked to another student.")
        return
    raise


@_json_requests(api.student_collection)
@login_required
def student_list(request):
    if not can_manage_students(request.user):
        return _access_denied(
            request, "student_list", "You do not have permission to manage students."
        )

    query = request.GET.get("q", "").strip()
    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(student_id__icontains=query)
            | Q(name__icontains=query)
            | Q(
                allocations__status=Allocation.AllocationStatus.ACTIVE,
                allocations__bed__room__hostel__name__icontains=query,
            )
        ).distinct()

    paginator = Paginator(students, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "students/student_list.html",
        {"page_obj": page_obj, "query": query},
    )


@login_required
@require_http_methods(["GET", "POST"])
def student_create(request):
    if not can_manage_students(request.user):
        return _access_denied(
            request,
            "student_create",
            "You do not have permission to register students.",
        )

    form = StudentForm(request.POST if request.method == "POST" else None)

    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                student = form.save()
                record_event(
                    user=request.user,
                    action=AuditEvent.Action.CREATE,
                    record=student,
                )
        except IntegrityError:
            _add_duplicate_error(form)
        else:
            messages.success(
                request,
                f"Student {student.student_id} registered successfully.",
            )
            return redirect("student-list")

    return render(
        request,
        "students/student_form.html",
        {"form": form, "heading": "Register Student"},
    )


@login_required
@require_http_methods(["GET", "POST"])
def student_update(request, pk):
    if not can_manage_students(request.user):
        return _access_denied(
            request, "student_update", "You do not have permission to update students."
        )

    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(
        request.POST if request.method == "POST" else None, instance=student
    )

    form.fields["student_id"].disabled = True
    form.fields.pop("status")

    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                student = form.save()
                record_event(
                    user=request.user,
                    action=AuditEvent.Action.UPDATE,
                    record=student,
                )
        except ValidationError as error:
            # An allocation can appear after form validation. The model
            # rechecks eligibility while holding the student row lock.
            form.add_error(None, error)
        except IntegrityError:
            _add_duplicate_error(form)
        else:
            messages.success(
                request,
                f"Student {student.student_id} updated successfully.",
            )
            return redirect("student-list")

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "heading": "Update Student",
            "student": student,
        },
    )


@_json_requests(api.student_deactivate)
@login_required
@require_http_methods(["POST"])
@transaction.atomic
def student_deactivate(request, pk):
    if not can_manage_students(request.user):
        return _access_denied(
            request,
            "student_deactivate",
            "You do not have permission to deactivate students.",
        )

    student = get_object_or_404(
        Student.objects.select_for_update(),
        pk=pk,
    )

    allocation = (
        Allocation.objects.select_related("bed__room__hostel")
        .filter(
            student=student,
            status=Allocation.AllocationStatus.ACTIVE,
        )
        .first()
    )

    if allocation:
        messages.error(
            request,
            f"Cannot deactivate {student.student_id}: "
            f"active bed {allocation.bed.label} in "
            f"{allocation.bed.room.hostel.name} is allocated to this student. "
            "Complete the allocation first.",
        )
        return redirect("student-list")

    if student.status == Student.Status.INACTIVE:
        messages.info(request, "This student is already inactive.")
    else:
        student.status = Student.Status.INACTIVE
        student.save(update_fields=["status", "updated_at"])
        record_event(
            user=request.user,
            action=AuditEvent.Action.DEACTIVATE,
            record=student,
        )
        messages.success(
            request,
            f"Student {student.student_id} deactivated successfully.",
        )

    return redirect("student-list")


@roles_required(User.Role.STUDENT)
@require_GET
def my_records(request):
    """Show only the student profile explicitly linked to this login."""
    student = payment_status_queryset(
        Student.objects.filter(user_id=request.user.pk)
    ).first()
    if student is None:
        return render(request, "students/my_records.html", {"student": None})

    allocations = list(
        student.allocations.exclude(status=Allocation.AllocationStatus.CANCELLED)
        .select_related("bed__room__hostel")
        .order_by("-allocated_on", "-pk")
    )
    payments = (
        Payment.objects.filter(student_id=student.pk)
        .select_related("adjustment_of")
        .order_by("-date", "-pk")
    )
    return render(
        request,
        "students/my_records.html",
        {
            "student": student,
            "allocations": allocations,
            "current_allocation": next(
                (
                    allocation
                    for allocation in allocations
                    if allocation.status == Allocation.AllocationStatus.ACTIVE
                ),
                None,
            ),
            "payments": payments,
            "payment_summary": status_row(student),
        },
    )
