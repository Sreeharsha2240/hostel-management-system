from django import forms

from .models import Bed, Hostel, Room


class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ('name', 'type')


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_number', 'floor', 'room_type', 'capacity', 'fee_amount')
        labels = {'fee_amount': 'Room fee (INR)'}


class BedStatusForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ('status',)


class AvailableBedFilterForm(forms.Form):
    hostel = forms.ModelChoiceField(queryset=Hostel.objects.all(), required=False)
    floor = forms.IntegerField(min_value=0, max_value=99, required=False)
    room_type = forms.ChoiceField(choices=[('', 'All room types'), *Room.Type.choices], required=False)
