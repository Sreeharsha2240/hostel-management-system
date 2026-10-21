from .models import AuditEvent


def record_event(*, user, action, record=None, record_type='', record_id=''):
    """Store identifiers only; never accept credentials or request bodies.

    Call this inside the business operation's transaction. Allocation, release
    and payment services can use the corresponding Action values in Sprint 2.
    """
    if record is not None:
        record_type = record._meta.label_lower
        record_id = str(record.pk)
    if not record_type or action not in AuditEvent.Action.values:
        raise ValueError('A known action and affected record type are required.')
    return AuditEvent.objects.create(
        user=user if user and user.is_authenticated else None,
        action=action, record_type=record_type, record_id=record_id,
    )
