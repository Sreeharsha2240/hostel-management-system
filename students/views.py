from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from accounts.decorators import roles_required
from accounts.models import User
from hms.forms import bind_model_form
from hms.http import add_validation_errors, api_error, form_error, wants_json

from .allocation_access import active_allocation, student_ids_for_hostel
from .forms import StudentRegistrationForm, StudentSearchForm, StudentUpdateForm
from .models import Student
from .services import deactivate_student, save_student_with_audit


STAFF_ROLES = (User.Role.ADMIN, User.Role.WARDEN)


def student_data(student):
    return {
        'id': student.pk, 'student_id': student.student_id, 'name': student.name,
        'dob': student.dob.strftime('%d-%m-%Y'), 'gender': student.gender,
        'course': student.course, 'year': student.year, 'mobile': student.mobile,
        'email': student.email, 'guardian_name': student.guardian_name,
        'guardian_mobile': student.guardian_mobile, 'address': student.address,
        'status': student.status,
    }


@roles_required(*STAFF_ROLES)
@require_http_methods(['GET', 'POST'])
def student_list(request):
    if request.method == 'POST':
        return student_form(request)
    form = StudentSearchForm(request.GET)
    students = Student.objects.all()
    valid = form.is_valid()
    if valid:
        query = form.cleaned_data['q']
        if query:
            students = students.filter(Q(student_id__iexact=query) | Q(name__icontains=query))
        if form.cleaned_data['hostel']:
            students = students.filter(pk__in=student_ids_for_hostel(form.cleaned_data['hostel']))
    else:
        students = students.none()
        response = form_error(request, form)
        if response:
            return response
    page = Paginator(students, 25).get_page(request.GET.get('page'))
    if wants_json(request):
        return JsonResponse({
            'results': [student_data(student) for student in page],
            'page': page.number, 'total': page.paginator.count,
        })
    return render(request, 'students/student_list.html', {
        'form': form, 'page_obj': page,
    }, status=200 if valid else 400)


@roles_required(*STAFF_ROLES)
@require_http_methods(['GET', 'POST', 'PATCH'])
def student_form(request, student_id=None):
    student = get_object_or_404(Student, pk=student_id) if student_id else Student()
    creating = student.pk is None
    form_class = StudentRegistrationForm if creating else StudentUpdateForm
    form = bind_model_form(request, form_class, instance=student)
    title = 'Register student' if creating else f'Update {student.name}'
    if request.method != 'GET':
        if form.is_valid():
            try:
                student = save_student_with_audit(form.save(commit=False), actor=request.user)
            except ValidationError as exception:
                add_validation_errors(form, exception)
            except IntegrityError:
                form.add_error('student_id', ValidationError('Student ID already registered', code='unique'))
            else:
                if wants_json(request):
                    return JsonResponse(student_data(student), status=201 if creating else 200)
                messages.success(request, 'Student registered.' if creating else 'Student details updated.')
                return redirect('student-detail', student_id=student.pk)
        codes = {error.code for errors in form.errors.as_data().values() for error in errors}
        status, code = (422, 'IMMUTABLE_FIELD') if 'IMMUTABLE_FIELD' in codes else (
            (409, 'DUPLICATE') if 'unique' in codes else (400, 'VALIDATION_ERROR')
        )
        response = form_error(request, form, status=status, code=code)
        return response or render(request, 'students/form.html', {
            'form': form, 'title': title, 'student': student,
        }, status=status)
    return render(request, 'students/form.html', {'form': form, 'title': title, 'student': student})


@roles_required(*STAFF_ROLES)
@require_http_methods(['GET', 'PATCH'])
def student_detail(request, student_id):
    if request.method == 'PATCH':
        return student_form(request, student_id=student_id)
    student = get_object_or_404(Student, pk=student_id)
    if wants_json(request):
        return JsonResponse(student_data(student))
    return render(request, 'students/student_detail.html', {
        'student': student, 'allocation': active_allocation(student),
    })


@roles_required(*STAFF_ROLES)
@require_POST
def student_deactivate(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    try:
        student = deactivate_student(student_id, actor=request.user)
    except ValidationError as error:
        message = ' '.join(error.messages)
        if wants_json(request):
            return api_error(message, code='HAS_ACTIVE_ALLOCATION', status=409)
        return render(request, 'students/student_detail.html', {
            'student': student, 'allocation': active_allocation(student), 'error': message,
        }, status=409)
    if wants_json(request):
        return JsonResponse({'id': student.pk, 'status': student.status})
    messages.success(request, 'Student deactivated. The record has been retained.')
    return redirect('student-detail', student_id=student.pk)
