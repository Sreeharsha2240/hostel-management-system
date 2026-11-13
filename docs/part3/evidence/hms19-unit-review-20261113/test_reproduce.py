"""Pure checks for frozen selection and coverage-denominator edge cases."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

from coverage.parser import PythonParser
from django.test import SimpleTestCase, TestCase

SPEC = importlib.util.spec_from_file_location(
    "hms19_reproduce", Path(__file__).with_name("reproduce.py")
)
reproduce = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reproduce)


class FixtureUnit(SimpleTestCase):
    def test_rule(self):
        pass


class FixtureDatabaseUnit(TestCase):
    def test_rule(self):
        pass


class FixtureOptInUnit(SimpleTestCase):
    databases = {"default"}

    def test_rule(self):
        pass


class HarnessContractTests(unittest.TestCase):
    def test_body_rule_includes_nested_decorators_and_excludes_module_declarations(
        self,
    ):
        source = """from functools import wraps
VALUE = 4
def outer(view):
    @wraps(view)
    def inner():
        return VALUE
    return inner
"""
        parser = PythonParser(text=source)
        parser.parse_source()
        self.assertEqual(
            reproduce.behavior_statements(source, parser.statements), {4, 5, 6, 7}
        )

    def test_new_class_decorators_inside_a_function_are_executable_body_logic(self):
        source = """def factory(decorate):
    @decorate
    class Result:
        VALUE = 1
    return Result
"""
        parser = PythonParser(text=source)
        parser.parse_source()
        self.assertEqual(
            reproduce.behavior_statements(source, parser.statements), {2, 3, 4, 5}
        )

    def test_explicit_method_selection_rejects_duplicates_and_module_labels(self):
        valid = "app.tests.Rules.test_allowed"
        self.assertEqual(
            reproduce.selection({"schema_version": 1, "selected_methods": [valid]}),
            [valid],
        )
        for labels in ([valid, valid], ["app.tests"], [], [None]):
            with self.subTest(labels=labels), self.assertRaises(ValueError):
                reproduce.selection({"schema_version": 1, "selected_methods": labels})

    def test_discovery_rejects_database_access_and_expanded_selections(self):
        for cls in (FixtureDatabaseUnit, FixtureOptInUnit):
            case = cls("test_rule")
            with self.subTest(cls=cls), self.assertRaises(ValueError):
                reproduce.validate_suite(unittest.TestSuite([case]), [case.id()])
        case = FixtureUnit("test_rule")
        self.assertEqual(
            reproduce.validate_suite(unittest.TestSuite([case]), [case.id()]),
            [case.id()],
        )
        with self.assertRaises(ValueError):
            reproduce.validate_suite(unittest.TestSuite([case]), [])
        with self.assertRaises(ValueError):
            reproduce.validate_suite(unittest.TestSuite([case, case]), [case.id()])
        ordinary = unittest.FunctionTestCase(lambda: None)
        with self.assertRaises(ValueError):
            reproduce.validate_suite(unittest.TestSuite([ordinary]), [ordinary.id()])

    def test_junit_requires_each_frozen_method_exactly_once(self):
        labels = ["app.tests.Rules.test_allowed", "app.tests.Rules.test_denied"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "TEST-rules.xml"
            path.write_text(
                '<testsuite><testcase classname="app.tests.Rules" name="test_allowed"/>'
                '<testcase classname="app.tests.Rules" name="test_denied"/></testsuite>',
                encoding="utf-8",
            )
            actual = reproduce.junit_identities(Path(directory))
            reproduce.validate_junit(actual, labels)
            for wrong in (actual[:1], [actual[0], actual[0]], []):
                with self.subTest(actual=wrong), self.assertRaises(ValueError):
                    reproduce.validate_junit(wrong, labels)

    def test_source_hash_is_portable_across_git_line_endings(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.py"
            path.write_bytes(b"first\r\nsecond\r\n")
            windows = reproduce.source_hash(path)
            path.write_bytes(b"first\nsecond\n")
            self.assertEqual(windows, reproduce.source_hash(path))


if __name__ == "__main__":
    unittest.main(defaultTest="HarnessContractTests", verbosity=2)
