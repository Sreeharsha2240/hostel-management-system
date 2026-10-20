from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier
from unittest.mock import patch

from django.contrib.sessions.models import Session
from django.db import close_old_connections, connections
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from audit.models import AuditEvent
from hostels.models import Bed
from students.models import Student

from .factories import student_fields


class Sprint1WorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for role in User.Role.values:
            User.objects.create_user(
                username=f'workflow-{role}', password='Strongpass123', role=role
            )

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def post(self, url, data, *, json=False):
        arguments = {'HTTP_X_CSRFTOKEN': self.client.cookies['csrftoken'].value}
        if json:
            arguments['content_type'] = 'application/json'
        return self.client.post(url, data, **arguments)

    def sign_in(self, role):
        self.client.get(reverse('login'))
        response = self.post(
            reverse('login'),
            {
                'username': f'workflow-{role}',
                'password': 'Strongpass123',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 200)

    def test_staff_workflow_with_real_login_csrf_role_changes_and_audit(self):
        self.sign_in('admin')
        response = self.post(
            reverse('hostel-list'),
            {'name': 'Workflow hostel', 'type': 'Boys'},
            json=True,
        )
        self.assertEqual(response.status_code, 201)
        hostel_id = response.json()['id']
        response = self.post(
            reverse('room-create', args=[hostel_id]),
            {
                'room_number': '101',
                'floor': 0,
                'room_type': 'Double',
                'capacity': 2,
                'fee_amount': '5000.00',
            },
            json=True,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Bed.objects.count(), 2)
        self.post(reverse('logout'), {})

        self.sign_in('warden')
        response = self.post(
            reverse('student-list'), student_fields(dob='2006-01-02'), json=True
        )
        self.assertEqual(response.status_code, 201)
        student_id = response.json()['id']
        response = self.client.patch(
            reverse('student-detail', args=[student_id]),
            {'mobile': '9999999999'},
            content_type='application/json',
            HTTP_X_CSRFTOKEN=self.client.cookies['csrftoken'].value,
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse('available-beds'),
            {'hostel': hostel_id},
            HTTP_ACCEPT='application/json',
        )
        self.assertEqual(len(response.json()['beds']), 2)
        self.assertEqual(
            self.post(
                reverse('hostel-list'), {'name': 'Denied', 'type': 'Boys'}, json=True
            ).status_code,
            403,
        )
        response = self.post(
            reverse('student-deactivate', args=[student_id]), {}, json=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.get(pk=student_id).status, 'Inactive')
        self.post(reverse('logout'), {})

        self.sign_in('student')
        for name in ('student-list', 'hostel-list', 'available-beds', 'audit-log'):
            self.assertEqual(self.client.get(reverse(name)).status_code, 403)
        self.post(reverse('logout'), {})

        self.sign_in('admin')
        response = self.client.get(
            reverse('audit-log'),
            {'action': 'deactivate'},
            HTTP_ACCEPT='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            any(
                row['record_type'] == 'students.student'
                for row in response.json()['results']
            )
        )

    def test_session_expiry_rolls_forward_after_activity_then_expires_when_idle(self):
        account = User.objects.get(username='workflow-warden')
        now = timezone.now()
        with patch('django.utils.timezone.now', return_value=now):
            self.client.force_login(account)
        key = self.client.session.session_key
        with patch(
            'django.utils.timezone.now', return_value=now + timedelta(minutes=10)
        ):
            self.assertEqual(self.client.get(reverse('dashboard')).status_code, 200)
        self.assertEqual(
            Session.objects.get(session_key=key).expire_date,
            now + timedelta(minutes=25),
        )
        with patch(
            'django.utils.timezone.now', return_value=now + timedelta(minutes=24)
        ):
            self.assertEqual(self.client.get(reverse('dashboard')).status_code, 200)
        with patch(
            'django.utils.timezone.now', return_value=now + timedelta(minutes=40)
        ):
            self.assertEqual(self.client.get(reverse('dashboard')).status_code, 302)


class ConcurrentRequestTests(TransactionTestCase):
    def test_five_simultaneous_failed_logins_do_not_lose_lockout_attempts(self):
        account = User.objects.create_user(
            username='concurrent-login', password='Strongpass123'
        )
        barrier = Barrier(5, timeout=20)

        def fail_login(_):
            close_old_connections()
            try:
                barrier.wait()
                return (
                    Client()
                    .post(
                        reverse('login'),
                        {
                            'username': account.username,
                            'password': 'Wrongpass123',
                        },
                    )
                    .status_code
                )
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=5) as pool:
            statuses = list(pool.map(fail_login, range(5)))
        self.assertEqual(statuses, [200] * 5)
        account.refresh_from_db()
        self.assertTrue(account.is_locked())
        self.assertEqual(account.failed_attempts, 0)
        self.assertEqual(AuditEvent.objects.filter(action='login_failed').count(), 5)

    def test_simultaneous_duplicate_student_registration_saves_only_one_record(self):
        actor = User.objects.create_user(
            username='concurrent-warden', role=User.Role.WARDEN
        )
        barrier = Barrier(2, timeout=20)

        def register_student(_):
            close_old_connections()
            try:
                client = Client()
                client.force_login(User.objects.get(pk=actor.pk))
                barrier.wait()
                return client.post(
                    reverse('student-list'),
                    student_fields(dob='2006-01-02'),
                    content_type='application/json',
                ).status_code
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            statuses = list(pool.map(register_student, range(2)))
        self.assertEqual(sorted(statuses), [201, 409])
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(
            AuditEvent.objects.filter(
                action='create', record_type='students.student'
            ).count(),
            1,
        )
