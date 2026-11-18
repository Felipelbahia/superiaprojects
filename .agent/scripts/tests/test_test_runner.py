"""Tests for testing-patterns/scripts/test_runner.py: Python projects run with the current interpreter.

Run from the 0 Padrões root: python3 -m unittest discover -s .agent/scripts/tests
"""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

RUNNER = Path(__file__).resolve().parents[3] / ".agent" / "skills" / "testing-patterns" / "scripts" / "test_runner.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("kit_test_runner", RUNNER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def detect(files: dict[str, str], pytest_installed: bool) -> dict:
    runner = load_runner()
    with tempfile.TemporaryDirectory() as tmp:
        for name, text in files.items():
            path = Path(tmp) / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        found = object() if pytest_installed else None  # any truthy spec means "pytest is importable"
        with mock.patch.object(runner.importlib.util, "find_spec", return_value=found):
            return runner.detect_test_framework(Path(tmp))


class PythonCommand(unittest.TestCase):
    def test_never_uses_a_bare_python(self):
        info = detect({"pyproject.toml": "[project]\nname='x'\n"}, pytest_installed=True)
        self.assertEqual(info["cmd"][0], sys.executable)
        self.assertNotEqual(info["cmd"][0], "python")

    def test_without_pytest_falls_back_to_unittest(self):
        info = detect({"pyproject.toml": "[project]\nname='x'\n", "tests/test_a.py": "x=1\n"}, pytest_installed=False)
        self.assertEqual(info["framework"], "unittest")
        self.assertEqual(info["cmd"][:4], [sys.executable, "-m", "unittest", "discover"])
        self.assertIn("tests", info["cmd"])

    def test_with_pytest_uses_pytest(self):
        info = detect({"pyproject.toml": "[project]\nname='x'\n"}, pytest_installed=True)
        self.assertEqual(info["framework"], "pytest")


if __name__ == "__main__":
    unittest.main()
