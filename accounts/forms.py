from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import User


class AccountCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, strip=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role')

    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            validate_password(password)
        except ValidationError as error:
            self.add_error('password', error)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
