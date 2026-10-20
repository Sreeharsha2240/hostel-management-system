"""Read the SAD Allocation contract without implementing Sprint 2 operations.

HMS-08 must expose Allocation(student, bed, vacated_on) and acquire the Student
row lock before allocating. Until that model exists there are no allocations.
"""

from django.apps import apps


def get_allocation_model():
    try:
        return apps.get_model('allocations', 'Allocation')
    except LookupError:
        return None


def active_allocation(student):
    allocation_model = get_allocation_model()
    if allocation_model is None:
        return None
    return (
        allocation_model.objects.filter(
            student_id=student.pk,
            vacated_on__isnull=True,
        )
        .select_related('bed__room__hostel')
        .order_by('-pk')
        .first()
    )


def student_ids_for_hostel(hostel):
    allocation_model = get_allocation_model()
    if allocation_model is None:
        return []
    return allocation_model.objects.filter(
        bed__room__hostel=hostel,
        vacated_on__isnull=True,
    ).values_list('student_id', flat=True)
