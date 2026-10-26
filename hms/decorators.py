from functools import wraps

from django.http import Http404

from accounts.decorators import roles_required
from accounts.models import User

from .http import api_error, wants_json


def staff_required(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        try:
            return view(request, *args, **kwargs)
        except Http404:
            if wants_json(request):
                return api_error("Record not found.", code="NOT_FOUND", status=404)
            raise

    return roles_required(User.Role.ADMIN, User.Role.WARDEN)(wrapped)
