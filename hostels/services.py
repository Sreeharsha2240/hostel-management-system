from django.db import transaction

from audit.models import AuditEvent
from audit.services import record_event

from .models import Room


@transaction.atomic
def save_room_with_audit(room, *, actor):
    creating = room.pk is None
    if not creating:
        Room.objects.select_for_update().get(pk=room.pk)
    before = dict(room.beds.values_list('pk', 'bed_number')) if not creating else {}
    room.save()
    record_event(
        user=actor,
        action=AuditEvent.Action.CREATE if creating else AuditEvent.Action.UPDATE,
        record=room,
    )
    after = dict(room.beds.values_list('pk', 'bed_number'))
    for bed_id in before.keys() | after.keys():
        if bed_id not in before or before.get(bed_id) != after.get(bed_id):
            record_event(
                user=actor,
                action=AuditEvent.Action.CREATE
                if bed_id not in before
                else AuditEvent.Action.UPDATE,
                record_type='hostels.bed',
                record_id=str(bed_id),
            )
    return Room.objects.get(pk=room.pk)
