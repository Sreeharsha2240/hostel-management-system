from django import forms
from django.utils import timezone

from hostels.models import Bed
from students.models import Student


class AllocationForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    bed = forms.ModelChoiceField(queryset=Bed.objects.select_related("room__hostel"))
    allocated_on = forms.DateField(
        required=False,
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={"type": "date"}),
    )


class TransferForm(forms.Form):
    new_bed = forms.ModelChoiceField(
        queryset=Bed.objects.select_related("room__hostel")
    )


class ReleaseForm(forms.Form):
    vacate_date = forms.DateField(
        initial=timezone.localdate, widget=forms.DateInput(attrs={"type": "date"})
    )
