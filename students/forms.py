from django import forms
from django.db.models import Q

from accounts.models import User

from .models import Student


class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        accounts = User.objects.filter(role=User.Role.STUDENT)
        if self.instance.pk and self.instance.user_id:
            accounts = accounts.filter(
                Q(student_profile__isnull=True) | Q(pk=self.instance.user_id)
            )
        else:
            accounts = accounts.filter(student_profile__isnull=True)
        self.fields["user"].queryset = accounts.order_by("username")
        self.fields["user"].label = "Linked student login"
        self.fields["user"].required = False
        self.fields["user"].help_text = (
            "Only this Student account can view the profile's allocation and "
            "payment details."
        )

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
            "user",
            "status",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_student_id(self):
        student_id = self.cleaned_data["student_id"].upper()

        existing_students = Student.objects.filter(student_id__iexact=student_id)

        if self.instance.pk:
            existing_students = existing_students.exclude(pk=self.instance.pk)

        if existing_students.exists():
            raise forms.ValidationError("Student ID already registered")

        return student_id

    def clean_status(self):
        status = self.cleaned_data["status"]
        if self.instance.pk and status == Student.Status.INACTIVE:
            from allocations.models import Allocation

            allocation = (
                Allocation.objects.select_related("bed")
                .filter(
                    student_id=self.instance.pk,
                    status=Allocation.AllocationStatus.ACTIVE,
                )
                .first()
            )
            if allocation:
                raise forms.ValidationError(
                    f"Release active bed {allocation.bed.label} before deactivation.",
                    code="HAS_ACTIVE_ALLOCATION",
                )
        return status

    def clean_gender(self):
        gender = self.cleaned_data["gender"]
        if self.instance.pk and gender != self.instance.gender:
            self.instance.validate_allocation_gender(gender)
        return gender

    def save(self, commit=True):
        student = super().save(commit=False)
        if commit:
            if student._state.adding:
                student.save()
            else:
                # The update screen deliberately removes status. Saving every
                # model field could restore a concurrent deactivation.
                student.save(update_fields=set(self.fields) | {"updated_at"})
            self._save_m2m()
        return student
