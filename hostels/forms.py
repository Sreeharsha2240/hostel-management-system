
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
            existing_beds = room.beds.count()
            if capacity < existing_beds:
                self.add_error(
                    "capacity",
                    f"This room already has {existing_beds} beds. "
                    "Capacity cannot be reduced below the existing bed count.",
                )

        return cleaned_data
