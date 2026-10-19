from django.conf import settings
from django.db import models


class AuditEvent(models.Model):
    """Append-only event metadata. Never store credentials or session data here."""

    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                              on_delete=models.SET_NULL, related_name='audit_events')
    action = models.CharField(max_length=40, db_index=True)
    record_type = models.CharField(max_length=80, blank=True)
    record_id = models.CharField(max_length=80, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return f'{self.timestamp:%Y-%m-%d %H:%M:%S} {self.action}'
