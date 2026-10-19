from .models import AuditEvent


def record_event(action, *, actor=None, record_type='', record_id=''):
    """Persist audit metadata only; callers must never pass secrets or PII."""
    return AuditEvent.objects.create(
        actor=actor if getattr(actor, 'is_authenticated', False) else None,
        action=action,
        record_type=record_type,
        record_id=str(record_id)[:80] if record_id != '' else '',
    )
