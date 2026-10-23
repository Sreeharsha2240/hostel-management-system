
from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "student_id",
            "name",
            "date_of_birth",
            "gender",
            "course",
            "year",
            "mobile",
            "email",
            "guardian_name",
            "guardian_mobile",
            "address",
            "status",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_student_id(self):
        return self.cleaned_data["student_id"].strip().upper()

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_mobile(self):
        return self.cleaned_data["mobile"].strip()

    def clean_guardian_mobile(self):
        return self.cleaned_data["guardian_mobile"].strip()
