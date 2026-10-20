from django.db import transaction

from audit.models import AuditEvent
from audit.services import record_event

from .models import Student


@transaction.atomic
def save_student_with_audit(student, *, actor):
    creating = student.pk is None
    student.save()
    record_event(
        user=actor,
        action=AuditEvent.Action.CREATE if creating else AuditEvent.Action.UPDATE,
        record=student,
    )
    return student


@transaction.atomic
def deactivate_student(student_id, *, actor):
    student = Student.objects.select_for_update().get(pk=student_id)
    if student.status != Student.Status.INACTIVE:
        student.status = Student.Status.INACTIVE
        student.save(update_fields=['status'])
        record_event(user=actor, action=AuditEvent.Action.DEACTIVATE, record=student)
    return student
