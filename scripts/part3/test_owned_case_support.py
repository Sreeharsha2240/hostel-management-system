"""Persist synthetic step observations for the explicit-only regression run.

These helpers do not assign a PASS. The runner reconciles completed assertions
with the actual JUnit outcome after database teardown.
"""

import json
import os
from datetime import UTC, datetime
from pathlib import Path

from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection

CASE_IDS = tuple(f"TC-REG-S2-{number:02d}" for number in range(8, 17))


class OwnedCaseEvidenceMixin:
    def setUp(self):
        super().setUp()
        self.assertEqual(connection.vendor, "mysql")
        self.assertEqual(connection.settings_dict["NAME"], "test_hms")
        self.assertFalse(connection.in_atomic_block)
        self._case_record = None

    def begin_case(self, case_id):
        self.assertIsNone(self._case_record)
        self.assertIn(case_id, CASE_IDS)
        self._case_record = {
            "case_id": case_id,
            "test_id": self.id(),
            "started_at": datetime.now(UTC).isoformat(),
            "execution_status": "IN_PROGRESS",
            "steps": [],
            "scope": "Synthetic integration case on disposable MySQL test_hms",
        }
        output = os.environ.get("HMS_OWNED_CASE_OUTPUT_DIR")
        self.assertTrue(output, "Run through run_owned_regressions.py.")
        self._case_path = Path(output) / f"{case_id}.json"
        self.assertFalse(self._case_path.exists(), "Preserve prior case evidence.")
        self._write_case()

    def record_step(self, step_id, *, expected, actual):
        self.assertIsNotNone(self._case_record)
        self.assertTrue(expected)
        self.assertNotIn(step_id, [step["step"] for step in self._case_record["steps"]])
        self._case_record["steps"].append(
            {"step": step_id, "expected": expected, "actual": actual}
        )
        self._write_case()

    def finish_case(self):
        self.assertTrue(self._case_record["steps"])
        self._case_record["execution_status"] = "ASSERTIONS_COMPLETED"
        self._case_record["completed_at"] = datetime.now(UTC).isoformat()
        self._write_case()

    def _write_case(self):
        self._case_path.write_text(
            json.dumps(self._case_record, cls=DjangoJSONEncoder, indent=2) + "\n",
            encoding="utf-8",
        )
