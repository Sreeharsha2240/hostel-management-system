"""HMS-17 field-preservation and transactional-audit acceptance gaps."""

from unittest.mock import patch

from django.forms.models import model_to_dict
from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from audit.models import AuditEvent
from hostels.models import Bed, Hostel, Room
from tests.factories import make_room, make_student

from .models import Student


class Issue39RegressionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="issue39-admin", role=User.Role.ADMIN
        )
        self.client.force_login(self.admin)
        self.student = make_student()
        self.hostel = Hostel.objects.create(name="Issue39", hostel_type="Boys")
        self.room = make_room(hostel=self.hostel)

    def test_empty_edits_preserve_all_stored_fields_and_audit(self):
        """TC-REG-S1-06: reject empty create/edit without any persisted change."""
        records = (self.student, self.hostel, self.room)
        before = [model_to_dict(record) for record in records]
        counts = (
            Student.objects.count(),
            Hostel.objects.count(),
            Room.objects.count(),
            Bed.objects.count(),
            AuditEvent.objects.count(),
        )
        for route, args in (
            ("student-create", []),
            ("student-update", [self.student.pk]),
            ("hostel-list", []),
            ("hostel-update", [self.hostel.pk]),
            ("room-create", []),
            ("room-update", [self.room.pk]),
        ):
            with self.subTest(route=route):
                response = self.client.post(reverse(route, args=args), {})
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["form"].errors)
                for record, original in zip(records, before, strict=True):
                    record.refresh_from_db()
                    self.assertEqual(model_to_dict(record), original)
                self.assertEqual(
                    counts,
                    (
                        Student.objects.count(),
                        Hostel.objects.count(),
                        Room.objects.count(),
                        Bed.objects.count(),
                        AuditEvent.objects.count(),
                    ),
                )

    def test_failed_audit_write_rolls_back_entities_beds_and_audit(self):
        """TC-REG-S1-08: even an audit inserted before failure must roll back."""
        from audit.services import record_event

        def fail_after_write(**kwargs):
            record_event(**kwargs)
            raise RuntimeError("Controlled HMS-17 post-audit failure")

        payload = model_to_dict(self.student)
        payload.update(student_id="ISSUE39000001", date_of_birth="2005-01-02", user="")
        counts = (
            Student.objects.count(),
            Room.objects.count(),
            Bed.objects.count(),
            AuditEvent.objects.count(),
        )
        for target, route, args, data in (
            ("students.views.record_event", "student-create", [], payload),
            (
                "hostels.views.record_event",
                "room-create",
                [],
                {
                    "hostel": self.hostel.pk,
                    "room_number": "999",
                    "floor": 1,
                    "room_type": "Double",
                    "capacity": 2,
                    "fee_amount": "1000",
                },
            ),
            (
                "students.views.record_event",
                "student-deactivate",
                [self.student.pk],
                {},
            ),
        ):
            with self.subTest(route=route), patch(target, side_effect=fail_after_write):
                with self.assertRaisesRegex(RuntimeError, "Controlled HMS-17"):
                    self.client.post(reverse(route, args=args), data)
                self.student.refresh_from_db()
                self.assertEqual(self.student.status, Student.Status.ACTIVE)
                self.assertEqual(
                    counts,
                    (
                        Student.objects.count(),
                        Room.objects.count(),
                        Bed.objects.count(),
                        AuditEvent.objects.count(),
                    ),
                )
