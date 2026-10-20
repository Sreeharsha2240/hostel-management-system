from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict

from .http import request_data


def bind_model_form(request, form_class, *, instance):
    error = None
    try:
        data = request_data(request) if request.method != 'GET' else None
    except ValidationError as exception:
        data, error = {}, exception
    if request.method == 'PATCH' and instance.pk and error is None:
        submitted = data.dict() if hasattr(data, 'dict') else data
        data = {**model_to_dict(instance, fields=form_class._meta.fields), **submitted}
    form = form_class(data, instance=instance)
    if error:
        form.is_valid()
        form.add_error(None, error)
    return form
