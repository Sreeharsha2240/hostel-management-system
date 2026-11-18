"""The availability screen must advertise beds the allocation operation accepts."""

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from allocations.services import allocate, release
from tests.factories import make_room, make_student

from .models import Bed


class BedAvailabilityConsistencyTests(TestCase):
    def setUp(self):
        self.warden = User.objects.create_user(
            username="availability-review-warden", role=User.Role.WARDEN
        )
        self.client.force_login(self.warden)

        self.full_room = make_room("AVL1", capacity=2)
        historical = allocate(
            student=make_student(980),
            bed=self.full_room.beds.get(label="AVL1-B"),
            actor=self.warden,
        )
        release(allocation_id=historical.pk, actor=self.warden)
        self.full_room.capacity = 1
        self.full_room.save(update_fields=["capacity"])
        allocate(
            student=make_student(981),
            bed=self.full_room.beds.get(label="AVL1-A"),
            actor=self.warden,
        )

        self.inactive_room = make_room("AVL2", capacity=3)
        for suffix, status in (
            ("B", Bed.BedStatus.OCCUPIED),
            ("C", Bed.BedStatus.MAINTENANCE),
        ):
            bed = self.inactive_room.beds.get(label=f"AVL2-{suffix}")
            bed.status = status
            bed.save(update_fields=["status"])
        hostel = self.inactive_room.hostel
        hostel.is_active = False
        hostel.save(update_fields=["is_active"])

        self.available_room = make_room("AVL3", capacity=1)

    def test_available_screen_and_api_exclude_inactive_and_full_room_spares(self):
        # Shrinking preserves B's history, but A already occupies the room's
        # entire admission capacity. The inactive hostel also retains its beds.
        self.assertEqual(self.full_room.beds.count(), 2)
        spare = self.full_room.beds.get(label="AVL1-B")
        self.assertEqual(spare.status, Bed.BedStatus.AVAILABLE)
        expected = {self.available_room.beds.get().pk}
        api = self.client.get(reverse("api-bed-availability"), secure=True)
        self.assertEqual(api.status_code, 200)
        self.assertEqual({bed["id"] for bed in api.json()["beds"]}, expected)

        for filters in ({}, {"status": Bed.BedStatus.AVAILABLE}):
            with self.subTest(filters=filters):
                page = self.client.get(reverse("bed-list"), filters, secure=True)
                self.assertEqual(page.status_code, 200)
                self.assertEqual({bed.pk for bed in page.context["beds"]}, expected)
                self.assertNotContains(page, "AVL1-B")
                self.assertNotContains(page, "AVL2-A")

    def test_other_statuses_and_all_inventory_keep_their_existing_scope(self):
        for status, expected in (
            (Bed.BedStatus.OCCUPIED, {"AVL1-A", "AVL2-B"}),
            (Bed.BedStatus.MAINTENANCE, {"AVL2-C"}),
            ("", {"AVL1-A", "AVL1-B", "AVL2-A", "AVL2-B", "AVL2-C", "AVL3-A"}),
        ):
            with self.subTest(status=status):
                page = self.client.get(
                    reverse("bed-list"), {"status": status}, secure=True
                )
                self.assertEqual(page.status_code, 200)
                self.assertEqual({bed.label for bed in page.context["beds"]}, expected)
