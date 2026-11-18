"""Keep CSRF enforcement and JSON error responses consistent."""

from django.views.csrf import csrf_failure as html_csrf_failure

from audit.models import AuditEvent
from audit.services import record_event

from .http import api_error, wants_json


def csrf_failure(request, reason=""):
    route = getattr(request, "resolver_match", None)
    route_name = getattr(route, "url_name", "") or ""
    record_event(
        user=getattr(request, "user", None),
        action=AuditEvent.Action.ACCESS_DENIED,
        record_type="csrf",
        record_id=route_name[:64] or "unresolved",
    )
    request._access_denied_audited = True
    if wants_json(request) or route_name.startswith("api-"):
        return api_error(
            "CSRF verification failed. Refresh the page and try again.",
            code="ACCESS_DENIED",
            status=403,
        )
    return html_csrf_failure(request, reason=reason)
