
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from accounts.models import User
from allocations.models import Allocation
from audit.models import AuditEvent
from audit.services import record_event
from hostels.models import Bed
from students.models import Student


def can_manage_allocations(user):
    return user.is_authenticated and user.role in (
        User.Role.ADMIN,
        User.Role.WARDEN,
    )


@login_required
def allocation_list(request):
    if not can_manage_allocations(request.user):
        return HttpResponseForbidden(
            "You do not have permission to manage allocations."
        )

    query = request.GET.get("q", "").strip()
    allocations = Allocation.objects.select_related(
        "student",
        "bed",
        "bed__room",
        "bed__room__hostel",
    )

    if query:
        allocations = allocations.filter(
            Q(student__student_id__icontains=query)
            | Q(student__name__icontains=query)
            | Q(bed__label__icontains=query)
            | Q(bed__room__hostel__name__icontains=query)
        )

    return render(
        request,
        "allocations/allocation_list.html",
        {"allocations": allocations, "query": query},
    )



@login_required
@require_http_methods(["GET", "POST"])
def allocation_create(request):
    if not can_manage_allocations(request.user):
        return HttpResponseForbidden(
            "You do not have permission to create allocations."
        )

    students = Student.objects.filter(status=Student.Status.ACTIVE)
    beds = Bed.objects.filter(
        status=Bed.BedStatus.AVAILABLE
    ).select_related("room", "room__hostel")

    if request.method == "POST":
        student_id = request.POST.get("student", "")
        bed_id = request.POST.get("bed", "")
        allocated_on = request.POST.get("allocated_on", "")

        student = Student.objects.filter(
            pk=student_id,
            status=Student.Status.ACTIVE,
        ).first()

        bed = Bed.objects.filter(
            pk=bed_id,
            status=Bed.BedStatus.AVAILABLE,
        ).select_related("room", "room__hostel").first()

        if student is None:
            messages.error(
                request, "Please select a valid active student."
            )
        elif bed is None:
            messages.error(
                request, "Please select an available bed."
            )
        else:
            allocation = Allocation(student=student, bed=bed)

            if allocated_on:
                allocation.allocated_on = allocated_on

            try:
                with transaction.atomic():
                    allocation.save()
                    record_event(
                        user=request.user,
                        action=AuditEvent.Action.ALLOCATE,
                        record=allocation,
                    )
            except (ValidationError, ValueError) as exc:
                if hasattr(exc, "message_dict"):
                    for errors in exc.message_dict.values():
                        for error in errors:
                            messages.error(request, error)
                elif hasattr(exc, "messages"):
                    for error in exc.messages:
                        messages.error(request, error)
                else:
                    messages.error(request, str(exc))
            else:
                messages.success(
                    request,
                    f"Bed {bed.label} allocated to {student.name}.",
                )
                return redirect("allocation-list")

    return render(
        request,
        "allocations/allocation_form.html",
        {
            "students": students,
            "beds": beds,
        },
    )



@login_required
@require_http_methods(["POST"])
@transaction.atomic
def allocation_complete(request, pk):
    if not can_manage_allocations(request.user):
        return HttpResponseForbidden(
            "You do not have permission to complete allocations."
        )

    allocation = get_object_or_404(
        Allocation.objects.select_for_update(),
        pk=pk,
    )

    if allocation.status != Allocation.AllocationStatus.ACTIVE:
        messages.info(request, "This allocation is already inactive.")
        return redirect("allocation-list")

    from django.utils import timezone

    allocation.status = Allocation.AllocationStatus.COMPLETED
    allocation.vacated_on = timezone.localdate()

    try:
        allocation.save()
        record_event(
            user=request.user,
            action=AuditEvent.Action.RELEASE,
            record=allocation,
        )
    except ValidationError as exc:
        messages.error(request, str(exc))
    else:
        messages.success(
            request,
            f"Allocation for {allocation.student.name} has been completed.",
        )

    return redirect("allocation-list")
