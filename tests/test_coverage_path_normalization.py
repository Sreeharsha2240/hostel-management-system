"""Every coverage export must use the same canonical data and test contexts."""

import ctypes
import hashlib
import io
import json
import os
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree

from coverage import Coverage, CoverageData
from django.test import SimpleTestCase

from scripts import run_checks


class CoveragePathNormalizationTests(SimpleTestCase):
    def test_short_or_symlink_paths_are_normalized_for_both_xml_and_json(self):
        with tempfile.TemporaryDirectory(prefix="coverage long path ") as directory:
            root = Path(directory).resolve()
            source = root / "source application"
            source.mkdir()
            for name in ("alpha", "beta"):
                package = source / name
                package.mkdir()
                (package / "__init__.py").write_text("", encoding="utf-8")
                (package / "models.py").write_text(
                    "def classify(value):\n    if value:\n"
                    '        return "yes"\n    return "no"\n',
                    encoding="utf-8",
                )
            if os.name == "nt":
                buffer = ctypes.create_unicode_buffer(32768)
                size = ctypes.windll.kernel32.GetShortPathNameW(
                    str(source), buffer, len(buffer)
                )
                self.assertGreater(size, 0)
                alias = Path(buffer.value)
                if str(alias) == str(source):
                    self.skipTest("This volume does not create Windows short names.")
            else:
                alias = root / "alias"
                alias.symlink_to(source, target_is_directory=True)
            raw = root / ".coverage.raw"
            data = CoverageData(basename=str(raw))
            names = {
                name: str(alias / name / "models.py") for name in ("alpha", "beta")
            }
            data.set_context("startup")
            data.add_arcs({name: [(-1, 1), (1, -1)] for name in names.values()})
            data.set_context("chosen.test_example")
            data.add_arcs(
                {
                    names["alpha"]: [(-1, 2), (2, 3), (3, -1)],
                    names["beta"]: [(-1, 2), (2, 4), (4, -1)],
                }
            )
            data.write()
            raw_hash = hashlib.sha256(raw.read_bytes()).hexdigest()
            config = root / "coverage.ini"
            config.write_text(
                "[run]\nbranch = True\nsource = "
                + ",".join(str(source / name) for name in names)
                + "\n[report]\ncontexts = ^chosen\\.test_example$\n",
                encoding="utf-8",
            )
            normalized = root / ".coverage.normalized"
            xml_file = root / "coverage.xml"
            json_file = root / "coverage.json"
            with (
                patch.dict(
                    os.environ,
                    {"COVERAGE_FILE": str(raw), "COVERAGE_RCFILE": str(config)},
                ),
                patch.object(run_checks, "ROOT", source),
                redirect_stdout(io.StringIO()),
            ):
                run_checks.normalize_coverage_data(normalized)
                run_checks.export_coverage_xml(xml_file, data_file=normalized)
                report = Coverage(data_file=str(normalized), config_file=str(config))
                report.load()
                report.json_report(outfile=str(json_file))
            self.assertEqual(hashlib.sha256(raw.read_bytes()).hexdigest(), raw_hash)
            xml = ElementTree.parse(xml_file).getroot()
            summary = json.loads(json_file.read_text(encoding="utf-8"))
            for attribute, key in (
                ("lines-valid", "num_statements"),
                ("lines-covered", "covered_lines"),
                ("branches-valid", "num_branches"),
                ("branches-covered", "covered_branches"),
            ):
                self.assertEqual(int(xml.get(attribute)), summary["totals"][key])
            self.assertEqual(int(xml.get("lines-covered")), 4)
            self.assertEqual(int(xml.get("branches-covered")), 2)
            hits = {
                item.get("filename"): {
                    int(line.get("number"))
                    for line in item.findall("lines/line")
                    if int(line.get("hits"))
                }
                for item in xml.iter("class")
            }
            self.assertEqual(
                hits, {"alpha/models.py": {2, 3}, "beta/models.py": {2, 4}}
            )

    def test_existing_normalized_data_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".coverage"
            path.write_bytes(b"prior evidence")
            with self.assertRaises(FileExistsError):
                run_checks.normalize_coverage_data(path)
            self.assertEqual(path.read_bytes(), b"prior evidence")
