
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from accounts.models import User
from allocations.models import Allocation
from .forms import StudentForm
from .models import Student


def can_manage_students(user):
    return user.is_authenticated and user.role in (
        User.Role.ADMIN,
        User.Role.WARDEN,
    )


@login_required
def student_list(request):
    if not can_manage_students(request.user):
        return HttpResponseForbidden(
            "You do not have permission to manage students."
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
        return HttpResponseForbidden(
            "You do not have permission to register students."
        )

    form = StudentForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        student = form.save()
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
        return HttpResponseForbidden(
            "You do not have permission to update students."
        )

    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)

    form.fields["student_id"].disabled = True
    form.fields.pop("status")

    if request.method == "POST" and form.is_valid():
        form.save()
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


@login_required
@require_http_methods(["POST"])
@transaction.atomic
def student_deactivate(request, pk):
    if not can_manage_students(request.user):
        return HttpResponseForbidden(
            "You do not have permission to deactivate students."
        )

    student = get_object_or_404(
        Student.objects.select_for_update(),
        pk=pk,
    )

    allocation = (
        Allocation.objects.select_related(
            "bed",
            "bed__room",
            "bed__room__hostel",
        )
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
        messages.success(
            request,
            f"Student {student.student_id} deactivated successfully.",
        )

    return redirect("student-list")
