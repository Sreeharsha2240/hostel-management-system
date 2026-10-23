
from django import forms

from .models import Hostel, Room


class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ["name", "hostel_type", "is_active"]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["hostel", "room_number", "floor", "room_type", "capacity"]

    def clean(self):
        cleaned_data = super().clean()
        room = self.instance
        capacity = cleaned_data.get("capacity")

        if room.pk and capacity is not None:
            from allocations.models import Allocation

            active_bed_count = room.beds.filter(
                allocations__status=Allocation.AllocationStatus.ACTIVE
            ).distinct().count()

            if active_bed_count > capacity:
                self.add_error(
                    "capacity",
                    f"This room has {active_bed_count} beds with active "
                    "allocations. Complete or move allocations before "
                    "reducing capacity further.",
                )

        return cleaned_data
