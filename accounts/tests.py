from datetime import timedelta

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from audit.models import AuditEvent
from .models import User


@override_settings(DJANGO_SECRET_KEY='test-secret')
class AuthenticationTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username='student1', password='Validpass123', role=User.Role.STUDENT)

    def test_login_shows_role_dashboard_and_logout_clears_session(self):
        response = self.client.post(reverse('login'), {'username': 'student1', 'password': 'Validpass123'})
        self.assertRedirects(response, reverse('dashboard'))
        dashboard = self.client.get(reverse('dashboard'))
        self.assertEqual(dashboard.status_code, 200)
        self.assertContains(dashboard, 'Student')
        self.assertTrue(AuditEvent.objects.filter(action='login_success', actor=self.student).exists())
        session_key = self.client.session.session_key
        self.client.post(reverse('logout'))
        self.assertNotEqual(self.client.session.session_key, session_key)
        self.assertRedirects(self.client.get(reverse('dashboard')), f'{reverse("login")}?next={reverse("dashboard")}')

    def test_each_role_can_access_dashboard_and_dashboard_reflects_role(self):
        for role, label in ((User.Role.ADMIN, 'Admin'), (User.Role.WARDEN, 'Warden'),
                            (User.Role.STUDENT, 'Student')):
            with self.subTest(role=role):
                account = User.objects.create_user(
                    username=f'{role}-dashboard', password='Validpass123', role=role,
                )
                self.client.force_login(account)
                self.assertContains(self.client.get(reverse('dashboard')), label)

    def test_session_cookie_is_http_only_and_uses_fifteen_minute_rolling_expiry(self):
        response = self.client.post(reverse('login'), {'username': 'student1', 'password': 'Validpass123'})
        cookie = response.cookies[settings.SESSION_COOKIE_NAME]
        self.assertTrue(cookie['httponly'])
        self.assertEqual(self.client.session.get_expiry_age(), 15 * 60)
        self.assertTrue(settings.SESSION_EXPIRE_AT_BROWSER_CLOSE)
        self.assertTrue(settings.SESSION_SAVE_EVERY_REQUEST)

    def test_invalid_password_is_generic_and_locks_after_five_attempts(self):
        first = self.client.post(reverse('login'), {'username': 'student1', 'password': 'wrong'})
        self.assertContains(first, 'Invalid username or password')
        for _ in range(4):
            self.client.post(reverse('login'), {'username': 'student1', 'password': 'wrong'})
        self.student.refresh_from_db()
        self.assertIsNotNone(self.student.locked_until)
        self.assertGreater(self.student.locked_until, timezone.now())
        self.assertEqual(self.student.failed_attempts, 0)
        self.assertEqual(AuditEvent.objects.filter(action='login_failure').count(), 5)
        self.assertTrue(AuditEvent.objects.filter(
            action='login_failure', actor=self.student, record_id=str(self.student.pk),
        ).exists())

    def test_locked_account_keeps_generic_error_and_records_affected_user(self):
        self.student.locked_until = timezone.now() + timedelta(minutes=15)
        self.student.save(update_fields=['locked_until'])
        response = self.client.post(reverse('login'), {'username': 'student1', 'password': 'wrong'})
        self.assertContains(response, 'Invalid username or password')
        event = AuditEvent.objects.get(action='login_failure')
        self.assertEqual(event.actor, self.student)
        self.assertEqual(event.record_id, str(self.student.pk))

    def test_expired_session_requires_login(self):
        self.client.force_login(self.student)
        session = self.client.session
        session.set_expiry(-1)
        session.save()
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("dashboard")}')

    def test_admin_can_create_and_deactivate_accounts(self):
        admin_user = User.objects.create_user(username='admin1', password='Validpass123', role=User.Role.ADMIN)
        self.client.force_login(admin_user)
        response = self.client.post(reverse('user-management'), {
            'username': 'newwarden', 'password': 'Securepass42', 'role': User.Role.WARDEN,
        })
        self.assertRedirects(response, reverse('user-management'))
        target = User.objects.get(username='newwarden')
        self.assertTrue(target.check_password('Securepass42'))
        self.client.post(reverse('user-deactivate', args=[target.pk]))
        target.refresh_from_db()
        self.assertFalse(target.is_active)
        self.assertTrue(AuditEvent.objects.filter(action='user_create', record_id=str(target.pk)).exists())
        self.assertTrue(AuditEvent.objects.filter(action='user_deactivate', record_id=str(target.pk)).exists())

    def test_non_admin_cannot_manage_accounts(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(reverse('user-management')).status_code, 403)

    def test_non_admin_cannot_read_audit_events(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(reverse('audit-events')).status_code, 403)

    def test_anonymous_user_cannot_read_audit_events(self):
        self.assertRedirects(
            self.client.get(reverse('audit-events')),
            f'{reverse("login")}?next={reverse("audit-events")}',
        )

    def test_password_policy_rejects_password_without_letter_or_digit(self):
        admin_user = User.objects.create_user(username='admin2', password='Validpass123', role=User.Role.ADMIN)
        self.client.force_login(admin_user)
        response = self.client.post(reverse('user-management'), {
            'username': 'weak-password-user', 'password': 'onlyletters', 'role': User.Role.STUDENT,
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='weak-password-user').exists())

    def test_duplicate_username_is_rejected(self):
        admin_user = User.objects.create_user(username='admin3', password='Validpass123', role=User.Role.ADMIN)
        self.client.force_login(admin_user)
        response = self.client.post(reverse('user-management'), {
            'username': 'student1', 'password': 'Validpass123', 'role': User.Role.STUDENT,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username='student1').count(), 1)
