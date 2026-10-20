from django import forms
from django.core.exceptions import ValidationError

from hostels.models import Hostel

from .models import Student


class StudentRegistrationForm(forms.ModelForm):
    dob = forms.DateField(
        label='Date of birth', input_formats=['%d-%m-%Y', '%Y-%m-%d'],
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
    )

    class Meta:
        model = Student
        fields = (
            'student_id', 'name', 'dob', 'gender', 'course', 'year', 'mobile',
            'email', 'guardian_name', 'guardian_mobile', 'address',
        )
        labels = {'student_id': 'Student ID (SRN)'}
        widgets = {'address': forms.Textarea(attrs={'rows': 3})}

    def clean_student_id(self):
        return self.cleaned_data['student_id'].upper()


class StudentUpdateForm(forms.ModelForm):
    student_id = forms.CharField(label='Student ID (SRN)', disabled=True)

    class Meta:
        model = Student
        fields = (
            'student_id', 'mobile', 'email', 'course', 'year',
            'guardian_name', 'guardian_mobile', 'address',
        )
        widgets = {'address': forms.Textarea(attrs={'rows': 3})}

    def clean(self):
        data = super().clean()
        if 'student_id' in self.data and str(self.data['student_id']).strip().upper() != self.instance.student_id:
            self.add_error('student_id', ValidationError(
                'Student ID cannot be changed.', code='IMMUTABLE_FIELD',
            ))
        return data


class StudentSearchForm(forms.Form):
    q = forms.CharField(label='Student ID or name', max_length=60, required=False)
    hostel = forms.ModelChoiceField(queryset=Hostel.objects.all(), required=False)
