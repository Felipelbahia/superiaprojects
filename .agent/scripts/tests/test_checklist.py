"""Tests for checklist.py: a project may declare, with a reason, that a non-critical check does not apply.

Run from the 0 Padrões root: python3 -m unittest discover -s .agent/scripts/tests
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECKLIST = Path(__file__).resolve().parent.parent / "checklist.py"


def run_on(config: object | None) -> subprocess.CompletedProcess:
    """Run checklist.py on an empty project, with `.agent/checklist.json` = config (raw str written as is)."""
    with tempfile.TemporaryDirectory() as tmp:
        if config is not None:
            (Path(tmp) / ".agent").mkdir()
            text = config if isinstance(config, str) else json.dumps(config)
            (Path(tmp) / ".agent" / "checklist.json").write_text(text, encoding="utf-8")
        return subprocess.run([sys.executable, str(CHECKLIST), tmp], capture_output=True, text=True, timeout=120, check=False)


class NotApplicableTest(unittest.TestCase):
    def test_declared_check_is_skipped_with_reason(self):
        r = run_on({"not_applicable": {"UX Audit": "no web app, only email templates"}})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("UX Audit: not applicable (no web app, only email templates)", r.stdout)
        self.assertNotIn("Running: UX Audit", r.stdout)
        self.assertIn("Skipped: 1", r.stdout)

    def test_without_config_every_check_runs(self):
        r = run_on(None)
        self.assertIn("Running: UX Audit", r.stdout)
        self.assertIn("Skipped: 0", r.stdout)

    def test_change_discipline_checks_run_and_env_check_is_critical(self):
        r = run_on(None)
        self.assertIn("Running: Env Diff Check", r.stdout)
        self.assertIn("Running: Scope Check", r.stdout)
        r = run_on({"not_applicable": {"Env Diff Check": "trust me"}})
        self.assertEqual(r.returncode, 1)
        self.assertIn("Env Diff Check", r.stdout)

    def test_empty_reason_is_refused(self):
        r = run_on({"not_applicable": {"UX Audit": "  "}})
        self.assertEqual(r.returncode, 1)
        self.assertIn("reason", r.stdout.lower())

    def test_critical_check_cannot_be_declared(self):
        r = run_on({"not_applicable": {"Security Scan": "trust me"}})
        self.assertEqual(r.returncode, 1)
        self.assertIn("Security Scan", r.stdout)
        self.assertNotIn("Running:", r.stdout)

    def test_unknown_check_name_is_refused(self):
        r = run_on({"not_applicable": {"UX Audt": "typo"}})
        self.assertEqual(r.returncode, 1)
        self.assertIn("UX Audt", r.stdout)

    def test_invalid_json_is_refused(self):
        r = run_on("{not json")
        self.assertEqual(r.returncode, 1)
        self.assertIn("checklist.json", r.stdout)


if __name__ == "__main__":
    unittest.main()
