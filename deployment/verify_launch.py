"""Checks for console-free startup without services or private configuration."""

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from deployment import launch


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        self.config = self.root / "operations.json"
        self.operations = {"root": str(self.root), "release": str(self.root / "source")}

    def invoke(self):
        self.config.write_text(json.dumps(self.operations), encoding="utf-8")
        with patch.object(sys, "path", sys.path.copy()):
            return launch.main(["--config", str(self.config)])

    def test_console_free_launcher_creates_logs_and_preserves_exit_code(self):
        with patch("deployment.supervise.main", return_value=1) as supervise:
            self.assertEqual(self.invoke(), 1)
        supervise.assert_called_once_with(["--config", str(self.config)])
        self.assertTrue((self.root / "logs" / "launcher.log").is_file())

    def test_mismatched_root_never_starts_supervisor(self):
        self.operations["root"] = str(self.root / "other")
        with patch("deployment.supervise.main") as supervise:
            self.assertEqual(self.invoke(), 1)
        supervise.assert_not_called()

    def test_relative_source_never_starts_supervisor(self):
        self.operations["release"] = "relative-private-path"
        with patch("deployment.supervise.main") as supervise:
            self.assertEqual(self.invoke(), 1)
        supervise.assert_not_called()

    def test_startup_exception_is_redacted(self):
        with patch("deployment.supervise.main", side_effect=ValueError("secret-value")):
            self.assertEqual(self.invoke(), 1)
        output = (self.root / "logs" / "launcher.log").read_text()
        self.assertIn("ValueError", output)
        self.assertNotIn("secret-value", output)


if __name__ == "__main__":
    unittest.main()
