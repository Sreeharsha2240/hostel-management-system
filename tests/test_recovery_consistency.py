"""Recovery verification must agree with supported maintenance reservations."""

from unittest import skipUnless

from django.db import connection, models
from django.test import TransactionTestCase

from accounts.models import User
from allocations.services import allocate
from hostels.models import Bed
from payments.models import ReceiptSequence
from scripts.part3.backup_issue40 import consistency
from tests.factories import make_room, make_student


@skipUnless(connection.vendor == "mysql", "Recovery verification uses MySQL SQL.")
class RecoveryReservationConsistencyTests(TransactionTestCase):
    def setUp(self):
        ReceiptSequence.objects.get_or_create(pk=1)
        room = make_room()
        self.bed = room.beds.first()
        self.actor = User.objects.create_user(
            username="recovery-reservation-warden", role=User.Role.WARDEN
        )
        allocate(student=make_student(), bed=self.bed, actor=self.actor)
        self.bed.refresh_from_db()

    def report(self):
        return consistency(connection.settings_dict, connection.settings_dict["NAME"])

    def test_active_maintenance_reservation_is_consistent(self):
        self.bed.status = Bed.BedStatus.MAINTENANCE
        self.bed.save(update_fields=["status"])
        report = self.report()
        self.assertTrue(report["all_consistency_checks_pass"], report["violations"])

    def test_corrupt_available_active_bed_is_still_detected(self):
        # Deliberately bypass supported save guards to simulate a corrupt restore.
        models.QuerySet(model=Bed, using=connection.alias).filter(
            pk=self.bed.pk
        ).update(status=Bed.BedStatus.AVAILABLE)
        self.assertFalse(self.report()["all_consistency_checks_pass"])
