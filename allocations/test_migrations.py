from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase
from django.utils import timezone

from tests.factories import make_room, make_student


class AllocationMigrationTests(TransactionTestCase):
    def setUp(self):
        executor = MigrationExecutor(connection)
        self.latest = executor.loader.graph.leaf_nodes()
        self.old = [
            (
                "allocations",
                "0002_remove_allocation_unique_active_allocation_per_student_and_more",
            )
        ]
        executor.migrate(self.old)
        self.apps = executor.loader.project_state(self.old).apps

    def tearDown(self):
        MigrationExecutor(connection).migrate(self.latest)
        super().tearDown()

    def legacy_allocation(self, **overrides):
        student = make_student()
        bed = make_room().beds.first()
        model = self.apps.get_model("allocations", "Allocation")
        data = dict(
            student_id=student.pk,
            bed_id=bed.pk,
            allocated_on=timezone.localdate(),
            status="Active",
        )
        return model.objects.create(**(data | overrides))

    def test_existing_active_rows_receive_unique_keys_and_bed_status(self):
        old = self.legacy_allocation()
        MigrationExecutor(connection).migrate(self.latest)
        from .models import Allocation

        upgraded = Allocation.objects.get(pk=old.pk)
        self.assertEqual(upgraded.active_student_id, old.student_id)
        self.assertEqual(upgraded.active_bed_id, old.bed_id)
        self.assertEqual(upgraded.bed.status, "Occupied")

    def test_unknown_historical_vacate_date_is_not_invented(self):
        old = self.legacy_allocation(status="Completed")
        try:
            with self.assertRaisesMessage(RuntimeError, "actual vacate dates"):
                MigrationExecutor(connection).migrate(self.latest)
            old.refresh_from_db()
            self.assertIsNone(old.vacated_on)
        finally:
            # Remove this deliberately invalid synthetic record before restoring schema.
            self.apps.get_model("allocations", "Allocation").objects.filter(
                pk=old.pk
            ).delete()
