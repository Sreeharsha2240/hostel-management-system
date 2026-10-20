"""Small shared helpers for the rendered pages and documented JSON APIs."""

import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse, QueryDict


def wants_json(request):
    return (
        request.content_type == 'application/json'
        or 'application/json' in request.headers.get('Accept', '')
    )


def request_data(request):
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
        except (ValueError, UnicodeDecodeError):
            raise ValidationError('Enter a valid JSON object.') from None
        if not isinstance(data, dict):
            raise ValidationError('Enter a valid JSON object.')
        return data
    if request.method == 'PATCH':
        return QueryDict(request.body)
    return request.POST


def add_validation_errors(form, error):
    if hasattr(error, 'error_dict'):
        for field, messages in error.error_dict.items():
            form.add_error(field if field in form.fields else None, messages)
    else:
        form.add_error(None, error)


def form_error(request, form, *, status=400, code='VALIDATION_ERROR'):
    if wants_json(request):
        return api_error(
            'Please correct the highlighted fields.', code=code, status=status,
            fields=form.errors.get_json_data(),
        )
    return None


def api_error(message, *, code='VALIDATION_ERROR', status=400, fields=None):
    error = {'code': code, 'message': message}
    if fields:
        error['fields'] = fields
    return JsonResponse({'error': error}, status=status)
