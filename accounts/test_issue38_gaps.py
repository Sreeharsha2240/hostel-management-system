from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.hashers import identify_hasher
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from allocations.models import Allocation
from audit.models import AuditEvent
from hostels.models import Hostel
from payments.models import Payment
from students.models import Student
from tests.factories import make_room, make_student


class Issue38GapTests(TestCase):
    password = "FixtureOnly-Hms38-9q"  # synthetic, never a real account credential

    def setUp(self):
        self.admin = User.objects.create_user(
            username="gap-admin", password=self.password, role=User.Role.ADMIN
        )
        self.warden = User.objects.create_user(
            username="gap-warden", password=self.password, role=User.Role.WARDEN
        )
        self.student_user = User.objects.create_user(
            username="gap-student-a", password=self.password, role=User.Role.STUDENT
        )

    def student_data(self, number=701, **overrides):
        return {
            "student_id": f"PES1UG24CS{number:03d}",
            "name": "Gap Student",
            "date_of_birth": "2005-01-02",
            "gender": "Male",
            "course": "CSE",
            "year": "2",
            "mobile": "9000000000",
            "email": "gap@example.test",
            "guardian_name": "Gap Guardian",
            "guardian_mobile": "9000000001",
            "address": "Synthetic fixture",
            "user": "",
            "status": "Active",
        } | overrides

    def test_auth02_and_sec03_known_unknown_and_sql_username_stay_logged_out(self):
        for username in (self.warden.username, "gap-no-such-user", "' OR '1'='1"):
            with self.subTest(
                kind="known" if username == self.warden.username else "other"
            ):
                client = Client()
                response = client.post(
                    reverse("login"),
                    {"username": username, "password": "IntentionallyWrong-9q"},
                )
                self.assertContains(response, "Invalid username or password")
                self.assertNotIn("_auth_user_id", client.session)
                for text in ("Traceback", "ProgrammingError", "OperationalError"):
                    self.assertNotContains(response, text)

    def test_auth03_exact_lock_duration_and_correct_password_boundary(self):
        start = timezone.now()
        with patch("accounts.backends.timezone.now", return_value=start):
            for _ in range(5):
                self.client.post(
                    reverse("login"),
                    {"username": self.warden.username, "password": "Wrong-9q"},
                )
        self.warden.refresh_from_db()
        self.assertEqual(self.warden.locked_until, start + timedelta(minutes=15))
        with patch(
            "accounts.backends.timezone.now",
            return_value=start + timedelta(minutes=14, seconds=59),
        ):
            response = self.client.post(
                reverse("login"),
                {"username": self.warden.username, "password": self.password},
            )
        self.assertContains(response, "Invalid username or password")
        self.assertNotIn("_auth_user_id", self.client.session)
        with patch(
            "accounts.backends.timezone.now", return_value=start + timedelta(minutes=15)
        ):
            response = self.client.post(
                reverse("login"),
                {"username": self.warden.username, "password": self.password},
            )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("dashboard"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.warden.pk)

    def test_usr01_and_sec04_same_created_warden_deactivation_hash_and_abc(self):
        self.client.force_login(self.admin)
        data = {
            "username": "gap-new-warden",
            "password": self.password,
            "role": "warden",
        }
        self.assertEqual(
            self.client.post(reverse("user-management"), data).status_code, 302
        )
        target = User.objects.get(username=data["username"])
        self.assertEqual(identify_hasher(target.password).algorithm, "pbkdf2_sha256")
        self.assertTrue(target.check_password(self.password))
        self.assertNotEqual(target.password, self.password)
        self.assertEqual(
            self.client.post(reverse("user-management"), data).status_code, 200
        )
        self.assertEqual(User.objects.filter(username=data["username"]).count(), 1)
        weak = data | {"username": "gap-weak", "password": "abc"}
        self.assertEqual(
            self.client.post(reverse("user-management"), weak).status_code, 200
        )
        self.assertFalse(User.objects.filter(username="gap-weak").exists())
        self.assertEqual(
            self.client.post(reverse("user-deactivate", args=[target.pk])).status_code,
            302,
        )
        target.refresh_from_db()
        self.assertFalse(target.is_active)
        client = Client()
        response = client.post(
            reverse("login"), {"username": target.username, "password": self.password}
        )
        self.assertContains(response, "Invalid username or password")
        self.assertNotIn("_auth_user_id", client.session)

    def test_sec01_direct_denials_preserve_domain_rows(self):
        # SRS NFR-7 status/no-mutation checks. Original literal response wording
        # must be separately retained/dispositioned; this is not a wording pass.
        models = (User, Hostel, Student, Allocation, Payment)
        for actor, endpoints in (
            (self.warden, ("user-management", "hostel-list")),
            (
                self.student_user,
                (
                    "student-list",
                    "student-create",
                    "allocation-list",
                    "allocation-create",
                ),
            ),
        ):
            self.client.force_login(actor)
            before = [list(model.objects.order_by("pk").values()) for model in models]
            for endpoint in endpoints:
                self.assertEqual(self.client.get(reverse(endpoint)).status_code, 403)
                self.assertEqual(
                    self.client.post(
                        reverse(endpoint), self.student_data()
                    ).status_code,
                    403,
                )
            self.assertEqual(
                [list(model.objects.order_by("pk").values()) for model in models],
                before,
            )

    def test_sec02_changed_ids_do_not_expose_other_student(self):
        own = make_student(711, user=self.student_user)
        other_user = User.objects.create_user(username="gap-student-b", role="student")
        other = make_student(712, user=other_user, name="Other Private Marker")
        self.client.force_login(self.student_user)
        response = self.client.get(
            reverse("student-self-service"), {"student_id": other.pk}
        )
        self.assertContains(response, own.student_id)
        self.assertNotContains(response, other.student_id)
        self.assertNotContains(response, other.name)
        for endpoint in (
            "allocation-history",
            "student-payment-status",
            "student-update",
        ):
            response = self.client.get(reverse(endpoint, args=[other.pk]))
            self.assertIn(response.status_code, (403, 404))
            self.assertNotIn(other.student_id.encode(), response.content)
            self.assertNotIn(other.name.encode(), response.content)

    def test_sec03_sec05_authorized_student_post_csrf_and_persisted_script(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.warden)
        url = reverse("student-create")
        self.assertEqual(client.get(url).status_code, 200)
        token = client.cookies["csrftoken"].value
        payload = self.student_data(name="<script>alert(1)</script>")
        before = (Student.objects.count(), AuditEvent.objects.count())
        self.assertEqual(client.post(url, payload).status_code, 403)
        self.assertEqual(
            client.post(url, payload, HTTP_X_CSRFTOKEN="invalid").status_code, 403
        )
        self.assertEqual((Student.objects.count(), AuditEvent.objects.count()), before)
        self.assertEqual(
            client.post(url, payload, HTTP_X_CSRFTOKEN=token).status_code, 302
        )
        stored = Student.objects.get(student_id=payload["student_id"])
        self.assertEqual(stored.name, payload["name"])
        response = client.get(reverse("student-list"))
        self.assertContains(response, "&lt;script&gt;alert(1)&lt;/script&gt;")
        self.assertNotContains(response, payload["name"])
        response = client.get(reverse("student-list"), {"q": "' OR '1'='1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].paginator.count, 0)

    def test_sec07_original_six_actions_have_records_times_and_expected_actors(self):
        started = timezone.now()
        self.client.post(
            reverse("login"), {"username": self.warden.username, "password": "Wrong-9q"}
        )
        response = self.client.post(
            reverse("login"),
            {"username": self.warden.username, "password": self.password},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.client.post(
                reverse("student-create"), self.student_data()
            ).status_code,
            302,
        )
        student = Student.objects.get(student_id=self.student_data()["student_id"])
        room = make_room("738", fee_amount="1000.00")
        today = timezone.localdate().isoformat()
        self.assertEqual(
            self.client.post(
                reverse("allocation-create"),
                {
                    "student": student.pk,
                    "bed": room.beds.first().pk,
                    "allocated_on": today,
                },
            ).status_code,
            302,
        )
        allocation = Allocation.objects.get(student=student)
        self.assertEqual(
            self.client.post(
                reverse("allocation-release", args=[allocation.pk]),
                {"vacate_date": today},
            ).status_code,
            302,
        )
        self.assertEqual(
            self.client.post(
                reverse("payment-create"),
                {
                    "student": student.pk,
                    "amount": "100.00",
                    "date": today,
                    "mode": "UPI",
                    "reference": "GAP738",
                },
            ).status_code,
            302,
        )
        payment = Payment.objects.get(student=student)
        expected = (
            ("login_failed", None, "accounts.user", self.warden.pk),
            ("login", self.warden.pk, "accounts.user", self.warden.pk),
            ("create", self.warden.pk, "students.student", student.pk),
            ("allocate", self.warden.pk, "allocations.allocation", allocation.pk),
            ("release", self.warden.pk, "allocations.allocation", allocation.pk),
            ("payment", self.warden.pk, "payments.payment", payment.pk),
        )
        events = []
        for action, actor, kind, pk in expected:
            event = AuditEvent.objects.get(
                action=action, user_id=actor, record_type=kind, record_id=str(pk)
            )
            self.assertGreaterEqual(event.timestamp, started)
            self.assertLessEqual(event.timestamp, timezone.now())
            events.append(event)
        self.client.force_login(self.admin)
        response = self.client.get(reverse("audit-log"), HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)
        visible_ids = {item["id"] for item in response.json()["results"]}
        self.assertTrue({event.pk for event in events}.issubset(visible_ids))
