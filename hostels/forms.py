from django import forms

from .models import Hostel, Room


class BedFilterForm(forms.Form):
    hostel = forms.IntegerField(required=False, min_value=1, max_value=2**63 - 1)
    # Appendix B permits at most two numeric digits for the floor.
    floor = forms.IntegerField(required=False, min_value=0, max_value=99)


class HostelForm(forms.ModelForm):
    name = forms.CharField(max_length=40)

    class Meta:
        model = Hostel
        fields = ["name", "hostel_type", "is_active"]


class RoomForm(forms.ModelForm):
    room_number = forms.CharField(max_length=6, strip=False)
    floor = forms.IntegerField(min_value=0, max_value=99)

    class Meta:
        model = Room
        fields = [
            "hostel",
            "room_number",
            "floor",
            "room_type",
            "capacity",
            "fee_amount",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Creation requires an explicitly supplied fee. Existing HTML edits may
        # omit the fee to preserve their previously configured amount.
        self.fields["fee_amount"].required = self.instance._state.adding

    def clean_fee_amount(self):
        fee = self.cleaned_data.get("fee_amount")
        return self.instance.fee_amount if fee is None else fee

    def clean(self):
        cleaned_data = super().clean()
        room = self.instance
        capacity = cleaned_data.get("capacity")

        hostel = cleaned_data.get("hostel")
        if room.pk and hostel is not None and room.hostel_id != hostel.pk:
            if room.beds.filter(allocations__isnull=False).exists():
                self.add_error(
                    "hostel",
                    "A room with allocation history cannot be moved to another "
                    "hostel because that would rewrite historical location.",
                )

        if room.pk and capacity is not None:
            from allocations.models import Allocation

            active_bed_count = (
                room.beds.filter(allocations__status=Allocation.AllocationStatus.ACTIVE)
                .distinct()
                .count()
            )

            if active_bed_count > capacity:
                self.add_error(
                    "capacity",
                    f"This room has {active_bed_count} beds with active "
                    "allocations. Complete or move allocations before "
                    "reducing capacity further.",
                )

        return cleaned_data
