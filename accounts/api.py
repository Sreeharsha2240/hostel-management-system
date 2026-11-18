"""Session-authenticated JSON interfaces from SAD API-A1 through API-A3."""

from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods, require_POST

from audit.models import AuditEvent
from audit.services import record_event
from hms.api import api_payload, api_roles_required, validate_api_types
from hms.http import api_error
from hms.responses import form_error_response, validation_response

from .forms import AccountCreationForm, AccountUpdateForm
from .models import User


@never_cache
@require_POST
@transaction.atomic
def sign_in(request):
    try:
        data = api_payload(request, {"username", "password"})
        validate_api_types(data, text_fields={"username", "password"})
        username = data.get("username", "").strip()
        password = data.get("password", "")
        if not username or not password or len(username) > 150:
            raise ValidationError("Enter a username and password.")
    except ValidationError as error:
        return validation_response(error)

    account = authenticate(request, username=username, password=password)
    if account is None:
        target = User.objects.filter(username=username).first()
        if target is not None and target.is_active and target.is_locked():
            return api_error(
                "Account locked for 15 minutes.", code="ACCOUNT_LOCKED", status=423
            )
        return api_error(
            "Invalid username or password", code="INVALID_CREDENTIALS", status=401
        )
    if account.role not in User.Role.values:
        record_event(
            user=account,
            action=AuditEvent.Action.ACCESS_DENIED,
            record_type="view",
            record_id="sign_in",
        )
        request._access_denied_audited = True
        return api_error("Access denied.", code="ACCESS_DENIED", status=403)
    login(request, account)
    return JsonResponse({"role": account.role, "redirect": reverse("dashboard")})


@api_roles_required(*User.Role.values)
@require_POST
def sign_out(request):
    try:
        if request.content_type != "application/json" or request.body:
            api_payload(request, set())
    except ValidationError as error:
        return validation_response(error)
    logout(request)
    return HttpResponse(status=204)


def _duplicate_username(form=None):
    return api_error(
        "Username already registered.",
        code="DUPLICATE",
        status=409,
        fields=form.errors.get_json_data() if form is not None else None,
    )


@api_roles_required(User.Role.ADMIN)
@require_POST
def user_create(request):
    try:
        data = api_payload(request, {"username", "password", "role"})
        validate_api_types(data, text_fields={"username", "password", "role"})
    except ValidationError as error:
        return validation_response(error)
    form = AccountCreationForm(data)
    if not form.is_valid():
        if any(
            error.code == "unique"
            for error in form.errors.as_data().get("username", [])
        ):
            return _duplicate_username(form)
        return form_error_response(form)
    try:
        with transaction.atomic():
            account = form.save()
            record_event(
                user=request.user, action=AuditEvent.Action.CREATE, record=account
            )
    except IntegrityError:
        if User.objects.filter(username=form.instance.username).exists():
            return _duplicate_username()
        raise
    return JsonResponse({"id": account.pk, "role": account.role}, status=201)


@api_roles_required(User.Role.ADMIN)
@require_http_methods(["PATCH"])
def user_update(request, user_id):
    try:
        data = api_payload(request, {"is_active", "role"})
        validate_api_types(data, text_fields={"role"}, boolean_fields={"is_active"})
        if not data:
            raise ValidationError("Supply at least one field to update.")
    except ValidationError as error:
        return validation_response(error)

    with transaction.atomic():
        account = get_object_or_404(User.objects.select_for_update(), pk=user_id)
        was_active = account.is_active
        if data.get("is_active") is False and account.pk == request.user.pk:
            record_event(
                user=request.user,
                action=AuditEvent.Action.ACCESS_DENIED,
                record_type="view",
                record_id="user_update",
            )
            request._access_denied_audited = True
            return api_error(
                "You cannot deactivate your own account.",
                code="ACCESS_DENIED",
                status=403,
            )
        values = model_to_dict(account, fields=AccountUpdateForm._meta.fields)
        if "role" in data:
            values["role"] = data["role"]
        form = AccountUpdateForm(values, instance=account)
        if not form.is_valid():
            return form_error_response(form)
        active_changed = "is_active" in data and account.is_active != data["is_active"]
        if form.has_changed() or active_changed:
            account = form.save(commit=False)
            if "is_active" in data:
                account.is_active = data["is_active"]
            account.save(update_fields=set(data))
            record_event(
                user=request.user,
                action=AuditEvent.Action.DEACTIVATE
                if was_active and not account.is_active
                else AuditEvent.Action.UPDATE,
                record=account,
            )
    return JsonResponse(
        {"id": account.pk, "role": account.role, "is_active": account.is_active}
    )
