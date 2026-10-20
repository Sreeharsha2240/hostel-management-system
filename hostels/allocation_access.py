"""Read-only integration with the Allocation model supplied by HMS-08."""

from django.apps import apps


def get_allocation_model():
    try:
        return apps.get_model('allocations', 'Allocation')
    except LookupError:
        return None


def bed_has_active_allocation(bed):
    allocation_model = get_allocation_model()
    return (
        allocation_model is not None
        and allocation_model.objects.filter(
            bed_id=bed.pk,
            vacated_on__isnull=True,
        ).exists()
    )


def active_bed_ids():
    allocation_model = get_allocation_model()
    if allocation_model is None:
        return []
    return allocation_model.objects.filter(vacated_on__isnull=True).values_list(
        'bed_id', flat=True
    )
