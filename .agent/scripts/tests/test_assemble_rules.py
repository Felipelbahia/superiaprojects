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


LOCAL_BLOCKS = {
    "Project": "## Project\n- Produces: software\n- Modules: core, code\n- Primary agent: backend-specialist\n",
    "Stack": "## Stack\n- Language/runtime: Python\n- Last checked: 2026-11-01 (Context7)\n",
    "Local rules": "## Local rules\n- Keep the cache folder.\n\n```\n## Inside fence\n```\n",
}


class PreserveLocalBlocksTest(unittest.TestCase):
    """Re-assembling over an existing CLAUDE.md keeps the project's own blocks (owner decision 2026-11-12)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.mods = self.root / "mods"
        self.mods.mkdir()
        (self.mods / "core.md").write_text(
            "> header\n\n## Project profile\n\n```\n## Project\n- Modules: <core, ...>\n```\n\n"
            "## Before acting (mandatory sequence)\n\nsteps\n",
            encoding="utf-8",
        )
        (self.mods / "code.md").write_text("## Code rules\n\nrule\n", encoding="utf-8")
        (self.mods / "content.md").write_text("## Content rules\n", encoding="utf-8")
        self.out = self.root / "CLAUDE.md"

    def tearDown(self):
        self.tmp.cleanup()

    def assemble(self, modules: str, *extra: str) -> subprocess.CompletedProcess:
        return run(self.root, "--modules", modules, "--title", "T", "--modules-dir", str(self.mods), *extra)

    def fresh(self, modules: str) -> str:
        self.assertEqual(self.assemble(modules).returncode, 0)
        return self.out.read_text(encoding="utf-8")

    def test_reassembly_keeps_the_three_blocks_in_canonical_order(self):
        # Arrange: assembled file with the blocks appended out of order
        base = self.fresh("core,code")
        self.out.write_text(
            base + "\n" + LOCAL_BLOCKS["Local rules"] + "\n" + LOCAL_BLOCKS["Project"] + "\n" + LOCAL_BLOCKS["Stack"],
            encoding="utf-8",
        )
        # Act
        result = self.assemble("core,code")
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        text = self.out.read_text(encoding="utf-8")
        self.assertTrue(text.startswith(base))
        tail = text[len(base):]
        self.assertLess(tail.index("## Project\n"), tail.index("## Stack\n"))
        self.assertLess(tail.index("## Stack\n"), tail.index("## Local rules\n"))
        for block in LOCAL_BLOCKS.values():
            self.assertIn(block.rstrip("\n"), text)
        self.assertEqual(text.count("## 1. Project profile"), 1)
        self.assertEqual(text.count("- Modules: <core, ...>"), 1)  # the fenced template is not a block
        self.assertEqual(text.count("## Inside fence"), 1)  # a fenced heading stays inside Local rules

    def test_modules_line_is_rewritten_with_the_modules_used(self):
        self.out.write_text(self.fresh("core,code") + "\n" + LOCAL_BLOCKS["Project"], encoding="utf-8")
        result = self.assemble("content,core")
        self.assertEqual(result.returncode, 0, result.stderr)
        text = self.out.read_text(encoding="utf-8")
        self.assertIn("## Project\n- Produces: software\n- Modules: core, content\n- Primary agent: backend-specialist", text)
        self.assertNotIn("- Modules: core, code", text)

    def test_unknown_section_moves_into_local_rules_with_a_warning(self):
        # Arrange: a hand-written section and an existing Local rules block
        self.out.write_text(
            self.fresh("core,code") + "\n## Deploy\n\n### Steps\nrun deploy.sh\n\n" + LOCAL_BLOCKS["Local rules"],
            encoding="utf-8",
        )
        # Act
        result = self.assemble("core,code")
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        text = self.out.read_text(encoding="utf-8")
        local = text[text.index("## Local rules\n"):]
        self.assertIn("- Keep the cache folder.", local)
        self.assertIn("### Deploy\n", local)
        self.assertIn("#### Steps\nrun deploy.sh", local)
        self.assertLess(local.index("- Keep the cache folder."), local.index("### Deploy"))
        self.assertNotIn("\n## Deploy", text)
        self.assertIn("Deploy", result.stdout + result.stderr)

    def test_unknown_section_creates_local_rules_when_missing(self):
        self.out.write_text(self.fresh("core") + "\n## Deploy\nrun deploy.sh\n", encoding="utf-8")
        result = self.assemble("core")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("## Local rules\n\n### Deploy\nrun deploy.sh", self.out.read_text(encoding="utf-8"))

    def test_sections_of_a_module_left_out_are_dropped_not_moved(self):
        self.out.write_text(self.fresh("core,code"), encoding="utf-8")
        result = self.assemble("core")
        self.assertEqual(result.returncode, 0, result.stderr)
        text = self.out.read_text(encoding="utf-8")
        self.assertNotIn("Code rules", text)
        self.assertNotIn("## Local rules", text)

    def test_reassembly_without_local_blocks_is_idempotent(self):
        base = self.fresh("core,code")
        result = self.assemble("core,code")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.out.read_text(encoding="utf-8"), base)

    def test_hand_edit_inside_a_kit_section_is_reported(self):
        base = self.fresh("core,code")
        self.out.write_text(base.replace("rule\n", "rule\nmy own tweak\n"), encoding="utf-8")
        result = self.assemble("core,code")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("my own tweak", self.out.read_text(encoding="utf-8"))
        self.assertIn("Code rules", result.stderr)

    def test_section_of_a_module_not_assembled_is_reported(self):
        self.out.write_text(self.fresh("core") + "\n## Code rules\nhand-written code rules\n", encoding="utf-8")
        result = self.assemble("core")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Code rules", result.stderr)

    def test_edited_preamble_is_reported(self):
        base = self.fresh("core")
        self.out.write_text(base.replace("> header", "> header\nlocal note"), encoding="utf-8")
        result = self.assemble("core")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("preamble", result.stderr.lower())

    def test_unchanged_reassembly_prints_no_warning(self):
        self.out.write_text(self.fresh("core,code") + "\n" + LOCAL_BLOCKS["Project"], encoding="utf-8")
        result = self.assemble("core,code")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("⚠️", result.stderr)

    def test_old_model_file_is_refused_without_replace(self):
        old = "# CLAUDE.md\n\n## Project Defines Gate\nold local rule\n"
        self.out.write_text(old, encoding="utf-8")
        result = self.assemble("core")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(self.out.read_text(encoding="utf-8"), old)
        self.assertIn("--replace", result.stderr)
        self.assertIn("backup", result.stderr.lower())

    def test_replace_overwrites_an_old_model_file(self):
        self.out.write_text("# CLAUDE.md\n\n## Project Defines Gate\nold local rule\n", encoding="utf-8")
        result = self.assemble("core", "--replace")
        self.assertEqual(result.returncode, 0, result.stderr)
        text = self.out.read_text(encoding="utf-8")
        self.assertNotIn("old local rule", text)
        self.assertTrue(text.startswith("# CLAUDE.md - T\n"))

    def test_empty_existing_file_is_assembled_normally(self):
        self.out.write_text("", encoding="utf-8")
        result = self.assemble("core")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("## 1. Project profile", self.out.read_text(encoding="utf-8"))

    def test_real_modules_keep_the_blocks(self):
        # Arrange: the kit's own modules, including their fenced ## Project / ## Stack templates
        self.assertEqual(run(self.root, "--modules", "core,code,interface").returncode, 0)
        blocks = "\n" + LOCAL_BLOCKS["Project"] + "\n" + LOCAL_BLOCKS["Stack"] + "\n" + LOCAL_BLOCKS["Local rules"]
        self.out.write_text(self.out.read_text(encoding="utf-8") + blocks, encoding="utf-8")
        # Act
        result = run(self.root, "--modules", "core,code,interface")
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        text = self.out.read_text(encoding="utf-8")
        self.assertIn("- Modules: core, code, interface\n- Primary agent: backend-specialist", text)
        self.assertIn(LOCAL_BLOCKS["Stack"].rstrip("\n"), text)
        self.assertNotIn("### ", text[text.index("## Local rules\n"):])  # no module section was mistaken for a local one


if __name__ == "__main__":
    unittest.main()
