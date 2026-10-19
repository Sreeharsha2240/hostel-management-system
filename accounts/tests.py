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
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 200)
        self.assertTrue(AuditEvent.objects.filter(action='login_success', actor=self.student).exists())
        self.client.post(reverse('logout'))
        self.assertRedirects(self.client.get(reverse('dashboard')), f'{reverse("login")}?next={reverse("dashboard")}')

    def test_session_cookie_is_http_only_and_uses_fifteen_minute_rolling_expiry(self):
        response = self.client.post(reverse('login'), {'username': 'student1', 'password': 'Validpass123'})
        cookie = response.cookies[settings.SESSION_COOKIE_NAME]
        self.assertTrue(cookie['httponly'])
        self.assertEqual(int(cookie['max-age']), 15 * 60)
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
