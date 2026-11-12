"""Tests for projects_audit.py (classification of a project against the modular kit rules).

Run from the 0 Padrões root: python3 -m unittest discover -s .agent/scripts/tests
"""

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "projects_audit.py"
spec = importlib.util.spec_from_file_location("projects_audit", SCRIPT)
audit_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_mod)
_aspec = importlib.util.spec_from_file_location("assemble_rules", SCRIPT.parent / "assemble_rules.py")
assemble_mod = importlib.util.module_from_spec(_aspec)
_aspec.loader.exec_module(assemble_mod)

# Built from the real kit modules, so a renamed heading in core.md breaks these tests.
MODULAR_RULES = assemble_mod.assemble(["core", "code"], "Demo", "CLAUDE.md", assemble_mod.DEFAULT_DIR)
FILLED_PROFILE = "\n## Project\n- Produces: software\n- Modules: core, sip-access, code\n"
OLD_RULES = "# CLAUDE.md\n\n### Project Defines Gate\n\n### Latest Docs First (Context7 MCP)\n"


def write(path: Path, text: str = "x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class ProjectsAuditTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def complete_project(self) -> Path:
        p = self.root / "proj"
        write(p / "CLAUDE.md", MODULAR_RULES + FILLED_PROFILE)
        write(p / ".agent/skills/sip-geral/SKILL.md")
        write(p / "docs/mapa-de-destinos.md")
        return p

    def test_complete_modular_project_is_up_to_date(self):
        # Arrange
        p = self.complete_project()
        # Act
        row = audit_mod.audit(p)
        # Assert
        self.assertEqual(row["model"], "modular")
        self.assertTrue(row["profile"] and row["sip"] and row["map"])
        self.assertFalse(row["duplicate"])
        self.assertTrue(row["up_to_date"])

    def test_old_rules_are_classified_old_and_behind(self):
        p = self.root / "old"
        write(p / "CLAUDE.md", OLD_RULES)
        row = audit_mod.audit(p)
        self.assertEqual(row["model"], "old")
        self.assertFalse(row["up_to_date"])

    def test_profile_placeholder_from_template_does_not_count(self):
        p = self.complete_project()
        write(p / "CLAUDE.md", MODULAR_RULES)  # only the template block, nothing filled
        row = audit_mod.audit(p)
        self.assertFalse(row["profile"])
        self.assertFalse(row["up_to_date"])

    def test_duplicate_claude_md_is_detected_and_blocks(self):
        p = self.complete_project()
        write(p / ".claude/CLAUDE.md", MODULAR_RULES + FILLED_PROFILE)
        row = audit_mod.audit(p)
        self.assertTrue(row["duplicate"])
        self.assertFalse(row["up_to_date"])

    def test_legacy_map_at_root_is_accepted(self):
        p = self.complete_project()
        (p / "docs/mapa-de-destinos.md").unlink()
        write(p / "mapa-de-destinos.md")
        self.assertTrue(audit_mod.audit(p)["map"])

    def test_agent_folder_linked_to_the_kit_is_flagged_and_not_read(self):
        # Arrange: a fake kit whose .agent has modular rules and sip-geral; the project links to it
        kit_agent = self.root / "kit" / ".agent"
        write(kit_agent / "rules/CLAUDE.md", MODULAR_RULES + FILLED_PROFILE)
        write(kit_agent / "skills/sip-geral/SKILL.md")
        p = self.root / "linked"
        write(p / "CLAUDE.md", OLD_RULES)
        (p / ".agent").symlink_to(kit_agent)
        # Act
        row = audit_mod.audit(p, kit_agent=kit_agent)
        # Assert
        self.assertTrue(row["agent_linked"])
        self.assertEqual(row["model"], "old")
        self.assertFalse(row["sip"])
        self.assertFalse(row["up_to_date"])

    def linked_setup(self):
        kit_agent = self.root / "kit" / ".agent"
        write(kit_agent / "rules/CLAUDE.md", MODULAR_RULES + FILLED_PROFILE)
        write(kit_agent / "skills/sip-geral/SKILL.md")
        p = self.root / "proj2"
        write(p / "CLAUDE.md", OLD_RULES)
        return kit_agent, p

    def test_relative_link_to_the_kit_is_flagged(self):
        kit_agent, p = self.linked_setup()
        (p / ".agent").symlink_to("../kit/.agent")
        self.assertTrue(audit_mod.audit(p, kit_agent=kit_agent)["agent_linked"])

    def test_link_to_a_subfolder_of_the_kit_agent_is_flagged(self):
        kit_agent, p = self.linked_setup()
        (p / ".agent").symlink_to(kit_agent / "skills")
        self.assertTrue(audit_mod.audit(p, kit_agent=kit_agent)["agent_linked"])

    def test_partial_link_inside_a_real_agent_folder_is_flagged(self):
        kit_agent, p = self.linked_setup()
        (p / ".agent").mkdir()
        (p / ".agent" / "rules").symlink_to(kit_agent / "rules")
        self.assertTrue(audit_mod.audit(p, kit_agent=kit_agent)["agent_linked"])

    def test_the_kit_itself_is_not_flagged(self):
        kit_agent, _ = self.linked_setup()
        row = audit_mod.audit(kit_agent.parent, kit_agent=kit_agent)
        self.assertFalse(row["agent_linked"])
        self.assertEqual(row["model"], "modular")

    def test_profile_variants_are_detected(self):
        for line in ("  - Produces: content", "- **Produces:** content"):
            with self.subTest(line=line):
                self.assertTrue(audit_mod.profile_filled(MODULAR_RULES + "\n## Project\n" + line + "\n"))

    def test_render_has_new_columns_and_no_old_ones(self):
        report = audit_mod.render([audit_mod.audit(self.complete_project())])
        header = next(l for l in report.splitlines() if l.startswith("| Projeto"))
        for col in ("Modelo", "Perfil", "SIP geral", "Mapa", ".claude/CLAUDE.md", ".agent → kit"):
            self.assertIn(col, header)
        self.assertNotIn("Gate", header)
        self.assertNotIn("Latest", header)


if __name__ == "__main__":
    unittest.main()
