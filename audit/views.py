from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from accounts.models import User
from .models import AuditEvent


@login_required
def event_list(request):
    if request.user.role != User.Role.ADMIN:
        raise PermissionDenied
    events = AuditEvent.objects.select_related('actor')[:200]
    return render(request, 'audit/event_list.html', {'events': events})
