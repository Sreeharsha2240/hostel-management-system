"""Account-management view decisions with persistence and wrappers isolated.

Permission and real transaction behavior have separate integration tests.
"""

from inspect import unwrap
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from audit.models import AuditEvent

from .views import deactivate_user, settings_view, update_user, user_management


class AccountSettingsViewUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.actor = SimpleNamespace(pk=1, is_authenticated=True)

    def request(self, data):
        request = self.factory.post("/settings/", data)
        request.user = self.actor
        return request

    @patch("accounts.views.redirect", return_value=HttpResponse("redirected"))
    @patch("accounts.views.messages.success")
    @patch("accounts.views.record_event")
    @patch("accounts.views.PasswordChangeForm")
    @patch("accounts.views.ProfileSettingsForm")
    def test_changed_profile_is_saved_and_audited(
        self, profile, password, audit, message, redirect
    ):
        profile.return_value.is_valid.return_value = True
        profile.return_value.has_changed.return_value = True
        request = self.request({"section": "profile", "first_name": "A"})
        self.assertEqual(unwrap(settings_view)(request).content, b"redirected")
        profile.return_value.save.assert_called_once()
        audit.assert_called_once_with(
            user=self.actor, action=AuditEvent.Action.UPDATE, record=self.actor
        )
        redirect.assert_called_once_with("settings")

    @patch("accounts.views.redirect", return_value=HttpResponse("redirected"))
    @patch("accounts.views.messages.success")
    @patch("accounts.views.record_event")
    @patch("accounts.views.PasswordChangeForm")
    @patch("accounts.views.ProfileSettingsForm")
    def test_unchanged_profile_is_not_saved_or_audited(
        self, profile, password, audit, message, redirect
    ):
        profile.return_value.is_valid.return_value = True
        profile.return_value.has_changed.return_value = False
        self.assertEqual(
            unwrap(settings_view)(self.request({"section": "profile"})).content,
            b"redirected",
        )
        profile.return_value.save.assert_not_called()
        audit.assert_not_called()

    @patch("accounts.views.redirect", return_value=HttpResponse("redirected"))
    @patch("accounts.views.messages.success")
    @patch("accounts.views.record_event")
    @patch("accounts.views.update_session_auth_hash")
    @patch("accounts.views.PasswordChangeForm")
    @patch("accounts.views.ProfileSettingsForm")
    def test_valid_password_change_updates_session_and_audits(
        self, profile, password, update_session, audit, message, redirect
    ):
        user = Mock()
        password.return_value.is_valid.return_value = True
        password.return_value.save.return_value = user
        request = self.request({"section": "password", "new_password1": "fake"})
        self.assertEqual(unwrap(settings_view)(request).content, b"redirected")
        update_session.assert_called_once_with(request, user)
        audit.assert_called_once_with(
            user=user, action=AuditEvent.Action.UPDATE, record=user
        )

    @patch("accounts.views.render", return_value=HttpResponse("form"))
    @patch("accounts.views.record_event")
    @patch("accounts.views.PasswordChangeForm")
    @patch("accounts.views.ProfileSettingsForm")
    def test_invalid_password_is_rendered_without_audit(
        self, profile, password, audit, render
    ):
        password.return_value.is_valid.return_value = False
        self.assertEqual(
            unwrap(settings_view)(self.request({"section": "password"})).content,
            b"form",
        )
        password.return_value.save.assert_not_called()
        audit.assert_not_called()
        self.assertEqual(render.call_args.args[1], "accounts/settings.html")

    @patch("accounts.views.redirect", return_value=HttpResponse("redirected"))
    @patch("accounts.views.record_event")
    @patch("accounts.views.AccountCreationForm")
    def test_valid_account_creation_saves_and_audits(self, form, audit, redirect):
        form.return_value.is_valid.return_value = True
        account = form.return_value.save.return_value
        self.assertEqual(
            unwrap(user_management)(self.request({"username": "new"})).content,
            b"redirected",
        )
        audit.assert_called_once_with(
            user=self.actor, action=AuditEvent.Action.CREATE, record=account
        )
        redirect.assert_called_once_with("user-management")

    @patch("accounts.views.redirect", return_value=HttpResponse("redirected"))
    @patch("accounts.views.record_event")
    @patch("accounts.views.AccountUpdateForm")
    @patch("accounts.views.get_object_or_404")
    def test_account_update_audits_only_when_changed(
        self, lookup, form, audit, redirect
    ):
        target = lookup.return_value
        form.return_value.is_valid.return_value = True
        for changed in (False, True):
            with self.subTest(changed=changed):
                form.return_value.has_changed.return_value = changed
                self.assertEqual(
                    unwrap(update_user)(self.request({"first_name": "A"}), 8).content,
                    b"redirected",
                )
        form.return_value.save.assert_called_once()
        audit.assert_called_once_with(
            user=self.actor, action=AuditEvent.Action.UPDATE, record=target
        )

    @patch("accounts.views.record_event")
    @patch("accounts.views.get_object_or_404")
    @patch("accounts.views.User.objects.select_for_update")
    def test_admin_cannot_deactivate_their_own_account(self, locked, lookup, audit):
        target = Mock(pk=1, is_active=True)
        lookup.return_value = target
        response = unwrap(deactivate_user)(self.request({}), 1)
        self.assertEqual(response.status_code, 403)
        target.save.assert_not_called()
        audit.assert_not_called()

    @patch("accounts.views.redirect", return_value=HttpResponse("redirected"))
    @patch("accounts.views.record_event")
    @patch("accounts.views.get_object_or_404")
    @patch("accounts.views.User.objects.select_for_update")
    def test_deactivation_updates_active_account_only_once(
        self, locked, lookup, audit, redirect
    ):
        target = Mock(pk=8, is_active=True)
        lookup.return_value = target
        self.assertEqual(
            unwrap(deactivate_user)(self.request({}), 8).content, b"redirected"
        )
        self.assertFalse(target.is_active)
        target.save.assert_called_once_with(update_fields=["is_active"])
        audit.assert_called_once_with(
            user=self.actor, action=AuditEvent.Action.DEACTIVATE, record=target
        )
        unwrap(deactivate_user)(self.request({}), 8)
        target.save.assert_called_once()
        audit.assert_called_once()
