"""Account form password validation and save decisions without a database."""

from unittest.mock import Mock, patch

from django.core.exceptions import ValidationError
from django.forms.utils import ErrorDict
from django.test import SimpleTestCase

from .forms import AccountCreationForm


class AccountCreationFormUnitTests(SimpleTestCase):
    def form(self, password):
        form = AccountCreationForm()
        form.cleaned_data = {"password": password}
        form._errors = ErrorDict()
        return form

    @patch("accounts.forms.validate_password")
    @patch("django.forms.models.BaseModelForm._post_clean")
    def test_empty_password_does_not_invoke_password_validators(self, parent, validate):
        form = self.form("")
        form._post_clean()
        parent.assert_called_once()
        validate.assert_not_called()

    @patch("accounts.forms.validate_password")
    @patch("django.forms.models.BaseModelForm._post_clean")
    def test_valid_password_is_checked_against_the_new_user(self, parent, validate):
        form = self.form("Validpass123")
        form._post_clean()
        validate.assert_called_once_with("Validpass123", form.instance)
        self.assertNotIn("password", form.errors)

    @patch(
        "accounts.forms.validate_password", side_effect=ValidationError("Weak password")
    )
    @patch("django.forms.models.BaseModelForm._post_clean")
    def test_password_validation_error_is_attached_to_password_field(
        self, parent, validate
    ):
        form = self.form("weak")
        form._post_clean()
        self.assertIn("Weak password", form.errors["password"])
        self.assertNotIn("password", form.cleaned_data)

    @patch("django.forms.models.BaseModelForm.save")
    def test_commit_false_hashes_password_without_saving(self, parent):
        user = Mock()
        parent.return_value = user
        self.assertIs(self.form("Validpass123").save(commit=False), user)
        parent.assert_called_once_with(commit=False)
        user.set_password.assert_called_once_with("Validpass123")
        user.save.assert_not_called()

    @patch("django.forms.models.BaseModelForm.save")
    def test_commit_true_hashes_password_and_saves(self, parent):
        user = Mock()
        parent.return_value = user
        self.assertIs(self.form("Validpass123").save(), user)
        user.set_password.assert_called_once_with("Validpass123")
        user.save.assert_called_once()
