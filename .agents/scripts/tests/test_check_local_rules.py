"""Tests for check_local_rules.py (local rules must survive a rules update, whole, with no old generic text).

Run from the 0 Padrões root: python3 -m unittest discover -s .agents/scripts/tests
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
CHECK = SCRIPTS / "check_local_rules.py"
FIX = Path(__file__).resolve().parent / "fixtures"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CHECK), *args], capture_output=True, text=True)


class RealCaseTest(unittest.TestCase):
    """Remote Brain, 2026-11-12: the update cut item 7 and dropped the routing table."""

    def test_propagated_file_fails_and_names_the_losses(self):
        r = run(str(FIX / "remote-brain-original-CLAUDE.md"), str(FIX / "remote-brain-propagado-CLAUDE.md"))
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("Modo Agente", r.stdout)  # item 7 was cut
        self.assertIn("KNOWLEDGE & REMOTE BRAIN", r.stdout)  # routing table dropped

    def test_corrected_file_passes(self):
        # adaptadas: customized text of generic old-kit sections, dropped on purpose or already covered by local rule 3
        r = run(str(FIX / "remote-brain-original-CLAUDE.md"), str(FIX / "remote-brain-corrigido-CLAUDE.md"),
                "--adapted", str(FIX / "remote-brain-adaptadas.md"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_old_file_as_new_is_all_junk(self):
        r = run(str(FIX / "remote-brain-original-CLAUDE.md"), str(FIX / "remote-brain-original-CLAUDE.md"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("generic", r.stdout.lower())


class SyntheticTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name: str, text: str) -> str:
        p = self.root / name
        p.write_text(text, encoding="utf-8")
        return str(p)

    def test_cut_line_is_reported(self):
        old = self.write("old.md", "## Local rules\n- Always confirm deletes with the owner before running anything destructive.\n")
        new = self.write("new.md", "## Local rules\n- Always confirm deletes with the owner\n")
        r = run(old, new)
        self.assertEqual(r.returncode, 1)
        self.assertIn("cut", r.stdout.lower())

    def test_adapted_line_is_accepted(self):
        old = self.write("old.md", "## Local rules\n- Always confirm deletes with the owner before running anything destructive.\n")
        new = self.write("new.md", "## Local rules\n- Confirm destructive actions with the owner.\n")
        adapted = self.write("adaptadas.md", "Always confirm deletes with the owner before running anything destructive.\n")
        r = run(old, new, "--adapted", adapted)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_identical_local_rule_passes(self):
        text = "## Local rules\n- Always confirm deletes with the owner before running anything destructive.\n"
        r = run(self.write("old.md", text), self.write("new.md", text))
        self.assertEqual(r.returncode, 0, r.stdout)


if __name__ == "__main__":
    unittest.main()
