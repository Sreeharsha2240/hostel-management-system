"""Shared session-authenticated boundaries for the documented JSON interfaces."""

from functools import wraps

from django.core.exceptions import ValidationError
from django.http import Http404

from audit.models import AuditEvent
from audit.services import record_event

from .http import api_error, request_data


def api_roles_required(*roles):
    """Use JSON authentication/authorization errors even without Accept headers."""

    def decorate(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated or not request.user.is_active:
                return api_error(
                    "Sign in to continue.", code="AUTH_REQUIRED", status=401
                )
            if request.user.role not in roles:
                record_event(
                    user=request.user,
                    action=AuditEvent.Action.ACCESS_DENIED,
                    record_type="view",
                    record_id=view.__name__,
                )
                request._access_denied_audited = True
                return api_error("Access denied.", code="ACCESS_DENIED", status=403)
            try:
                return view(request, *args, **kwargs)
            except Http404:
                return api_error("Record not found.", code="NOT_FOUND", status=404)

        return wrapped

    return decorate


def api_payload(request, allowed_fields):
    """Reject undeclared fields rather than silently accepting mass assignment."""
    data = request_data(request)
    if set(data).difference(allowed_fields):
        raise ValidationError("The request contains unsupported fields.")
    return data


class ErrorResponseMiddleware:
    """Audit served denials and preserve the JSON error contract on API routes."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        route = getattr(request, "resolver_match", None)
        name = getattr(route, "url_name", "") or ""
        if response.status_code == 403 and not getattr(
            request, "_access_denied_audited", False
        ):
            record_event(
                user=getattr(request, "user", None),
                action=AuditEvent.Action.ACCESS_DENIED,
                record_type="view",
                record_id=name[:64] or "unresolved",
            )
            request._access_denied_audited = True
        if response.status_code < 400 or response.headers.get(
            "Content-Type", ""
        ).startswith("application/json"):
            return response
        from .http import wants_json

        if not (wants_json(request) or name.startswith("api-")):
            return response
        message, code = {
            400: ("Enter a valid request.", "VALIDATION_ERROR"),
            401: ("Sign in to continue.", "AUTH_REQUIRED"),
            403: ("Access denied.", "ACCESS_DENIED"),
            404: ("Record not found.", "NOT_FOUND"),
            405: ("This request method is not allowed.", "METHOD_NOT_ALLOWED"),
        }.get(
            response.status_code,
            ("The request could not be completed.", "SERVER_ERROR"),
        )
        result = api_error(message, code=code, status=response.status_code)
        for header, value in response.headers.items():
            if header.lower() not in {"content-type", "content-length"}:
                result.headers[header] = value
        result.cookies = response.cookies
        return result


def validate_api_types(data, *, text_fields=(), integer_fields=(), boolean_fields=()):
    """Reject JSON coercions such as true becoming integer one."""
    errors = {}
    for fields, value_type, message in (
        (text_fields, str, "Enter a text value."),
        (integer_fields, int, "Enter a whole number."),
        (boolean_fields, bool, "Enter true or false."),
    ):
        for field in fields:
            if field in data and type(data[field]) is not value_type:
                errors[field] = [message]
    if errors:
        raise ValidationError(errors)
