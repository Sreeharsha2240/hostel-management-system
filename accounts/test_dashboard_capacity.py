"""Dashboard availability must agree with the actual admission policy."""

from django.test import TestCase
from django.urls import reverse

from allocations.services import allocate, release
from hostels.models import Bed
from tests.factories import make_room, make_student

from .models import User


class DashboardCapacityTests(TestCase):
    def test_available_historical_bed_in_full_room_is_not_advertised(self):
        room = make_room()
        warden = User.objects.create_user(
            username="dashboard-capacity-warden", role="warden"
        )
        previous = allocate(
            student=make_student(), bed=room.beds.get(label="101-B"), actor=warden
        )
        release(allocation_id=previous.pk, actor=warden)
        room.capacity = 1
        room.room_type = "Single"
        room.save(update_fields=["capacity", "room_type"])
        allocate(
            student=make_student(2), bed=room.beds.get(label="101-A"), actor=warden
        )
        self.assertEqual(room.beds.filter(status=Bed.BedStatus.AVAILABLE).count(), 1)
        student = User.objects.create_user(
            username="dashboard-capacity-student", role="student"
        )
        self.client.force_login(student)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["available_bed_count"], 0)
