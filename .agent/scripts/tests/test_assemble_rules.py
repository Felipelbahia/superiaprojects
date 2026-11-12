"""Tests for assemble_rules.py.

Run from the 0 Padrões root: python3 -m unittest discover -s .agent/scripts/tests
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
ASSEMBLE = SCRIPTS / "assemble_rules.py"
REAL_MODULES = SCRIPTS.parent / "skills" / "project-initializer" / "modules"


def run(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(ASSEMBLE), *args], cwd=cwd, capture_output=True, text=True)


class AssembleRulesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.mods = self.root / "mods"
        self.mods.mkdir()
        (self.mods / "core.md").write_text("> header\n\n## Alpha\n\n```\n## Not a heading\n```\n\n## Beta\n", encoding="utf-8")
        (self.mods / "code.md").write_text("## Gamma\n", encoding="utf-8")
        (self.mods / "content.md").write_text("## Delta\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_fixed_order_and_numbering_skip_code_fences(self):
        # Arrange: modules given out of order
        # Act
        result = run(self.root, "--modules", "content,core,code", "--title", "T", "--modules-dir", str(self.mods))
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        text = (self.root / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# CLAUDE.md - T\n"))
        headings = [l for l in text.splitlines() if l.startswith("## ")]
        self.assertEqual(headings, ["## 1. Alpha", "## Not a heading", "## 2. Beta", "## 3. Gamma", "## 4. Delta"])

    def test_core_is_mandatory(self):
        result = run(self.root, "--modules", "code", "--modules-dir", str(self.mods))
        self.assertEqual(result.returncode, 2)
        self.assertIn("core", result.stderr)
        self.assertFalse((self.root / "CLAUDE.md").exists())

    def test_unknown_module_is_rejected(self):
        result = run(self.root, "--modules", "core,mobile", "--modules-dir", str(self.mods))
        self.assertEqual(result.returncode, 2)
        self.assertIn("mobile", result.stderr)

    def test_out_name_goes_in_header(self):
        result = run(self.root, "--modules", "core", "--out", "GEMINI.md", "--modules-dir", str(self.mods))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "GEMINI.md").read_text(encoding="utf-8").startswith("# GEMINI.md - Project rules"))

    def test_real_modules_all_exist_and_assemble(self):
        names = run(self.root, "--list").stdout.split()
        for name in names:
            self.assertTrue((REAL_MODULES / f"{name}.md").is_file(), name)
        result = run(self.root, "--modules", ",".join(names))
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
