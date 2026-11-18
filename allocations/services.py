from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from audit.models import AuditEvent
from audit.services import record_event
from hostels.models import Bed, Room
from students.models import Student

from .models import Allocation


@transaction.atomic
def allocate(*, student, bed, actor, allocated_on=None):
    allocation = Allocation(student=student, bed=bed)
    if allocated_on is not None:
        allocation.allocated_on = allocated_on
    allocation.save()
    record_event(user=actor, action=AuditEvent.Action.ALLOCATE, record=allocation)
    return allocation


def lock_allocation(pk, extra_bed=None):
    source = Allocation.objects.get(pk=pk)
    Student.objects.select_for_update().get(pk=source.student_id)
    bed_ids = sorted({source.bed_id} | ({extra_bed.pk} if extra_bed else set()))
    bed_rooms = dict(Bed.objects.filter(pk__in=bed_ids).values_list("pk", "room_id"))
    if len(bed_rooms) != len(bed_ids):
        raise ValidationError("The selected bed no longer exists.", code="NOT_FOUND")
    room_ids = sorted(set(bed_rooms.values()))
    list(Room.objects.select_for_update().filter(pk__in=room_ids).order_by("pk"))
    beds = list(Bed.objects.select_for_update().filter(pk__in=bed_ids).order_by("pk"))
    if len(beds) != len(bed_ids):
        raise ValidationError("The selected bed no longer exists.", code="NOT_FOUND")
    if any(bed.room_id != bed_rooms[bed.pk] for bed in beds):
        # A free transfer target can move after the room snapshot. Do not lock
        # its new Room after already taking Bed: inventory uses Room -> Bed.
        raise ValidationError(
            "A selected bed has moved to another room. Refresh and try again.",
            code="BED_MOVED",
        )
    source = Allocation.objects.select_for_update().get(pk=pk)
    if source.status != Allocation.AllocationStatus.ACTIVE:
        raise ValidationError(
            "This allocation is already inactive.", code="ALREADY_RELEASED"
        )
    return source


@transaction.atomic
def release(*, allocation_id, actor, vacate_date=None):
    allocation = lock_allocation(allocation_id)
    allocation.status = Allocation.AllocationStatus.COMPLETED
    allocation.vacated_on = vacate_date or timezone.localdate()
    allocation.save(update_fields=["status", "vacated_on"])
    record_event(user=actor, action=AuditEvent.Action.RELEASE, record=allocation)
    return allocation


@transaction.atomic
def transfer(*, allocation_id, new_bed, actor):
    original = lock_allocation(allocation_id, extra_bed=new_bed)
    if original.bed_id == new_bed.pk:
        raise ValidationError("Choose a different available bed.", code="BED_OCCUPIED")
    original.status = Allocation.AllocationStatus.COMPLETED
    original.vacated_on = timezone.localdate()
    original.save(update_fields=["status", "vacated_on"])
    successor = Allocation(student_id=original.student_id, bed=new_bed)
    successor.save()
    record_event(user=actor, action=AuditEvent.Action.TRANSFER, record=successor)
    return successor
