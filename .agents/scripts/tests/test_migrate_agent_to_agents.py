"""Tests for migrate_agent_to_agents.py (renames a project's `.agent/` to `.agents/`).

Run from the 0 Padrões root: python3 -m unittest discover -s .agents/scripts/tests
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import migrate_agent_to_agents as mig  # noqa: E402


def project(root: Path) -> Path:
    p = root / "proj"
    (p / ".agent" / "skills" / "mine").mkdir(parents=True)
    (p / ".agent" / "skills" / "mine" / "SKILL.md").write_text("see .agent/skills/mine", encoding="utf-8")
    (p / ".agent" / "plans").mkdir()
    (p / ".agent" / "plans" / "old.md").write_text("history .agent/plans", encoding="utf-8")
    (p / ".claude" / "skills").mkdir(parents=True)
    (p / ".claude" / "skills" / "mine").symlink_to("../../.agent/skills/mine")
    (p / "CLAUDE.md").write_text("rules in `.agent/` and navigator.agent and conversation_config.agent.prompt\n", encoding="utf-8")
    (p / ".gitignore").write_text(".agent/plans/\n", encoding="utf-8")
    return p


class MigrateTest(unittest.TestCase):
    def test_simulation_writes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            p = project(Path(d))
            status, _ = mig.migrate(p, apply=False)
            self.assertEqual(status, "simulado")
            self.assertTrue((p / ".agent").is_dir())
            self.assertFalse((p / ".agents").exists())
            self.assertIn(".agent/", (p / "CLAUDE.md").read_text(encoding="utf-8"))

    def test_apply_renames_relinks_and_replaces_text_but_not_history(self):
        with tempfile.TemporaryDirectory() as d:
            p = project(Path(d))
            status, notes = mig.migrate(p, apply=True)
            self.assertEqual(status, "migrado", notes)
            self.assertFalse((p / ".agent").exists())
            self.assertFalse((p / ".agent").is_symlink())  # no compatibility link
            self.assertTrue((p / ".claude" / "skills" / "mine" / "SKILL.md").is_file())
            self.assertEqual(os.readlink(p / ".claude" / "skills" / "mine"), "../../.agents/skills/mine")
            self.assertIn(".agents/skills/mine", (p / ".agents" / "skills" / "mine" / "SKILL.md").read_text(encoding="utf-8"))
            self.assertEqual((p / ".agents" / "plans" / "old.md").read_text(encoding="utf-8"), "history .agent/plans")
            self.assertEqual((p / ".gitignore").read_text(encoding="utf-8"), ".agents/plans/\n")
            text = (p / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertIn("`.agents/`", text)
            self.assertIn("navigator.agent", text)
            self.assertIn("conversation_config.agent.prompt", text)

    def test_merge_when_no_clash_and_stop_on_clash(self):
        with tempfile.TemporaryDirectory() as d:
            p = project(Path(d))
            (p / ".agents" / "skills" / "other").mkdir(parents=True)
            status, _ = mig.migrate(p, apply=True)
            self.assertEqual(status, "migrado")
            self.assertTrue((p / ".agents" / "skills" / "other").is_dir())
            self.assertTrue((p / ".agents" / "skills" / "mine").is_dir())
        with tempfile.TemporaryDirectory() as d:
            p = project(Path(d))
            (p / ".agents" / "skills" / "mine").mkdir(parents=True)
            (p / ".agents" / "skills" / "mine" / "SKILL.md").write_text("theirs", encoding="utf-8")
            status, notes = mig.migrate(p, apply=True)
            self.assertEqual(status, "conflito")
            self.assertTrue((p / ".agent").is_dir())  # untouched

    def test_agent_that_is_a_link_is_skipped_and_nothing_to_do_is_reported(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "p"
            p.mkdir()
            self.assertEqual(mig.migrate(p, apply=True)[0], "nada")
            (Path(d) / "kit").mkdir()
            (p / ".agent").symlink_to(Path(d) / "kit")
            self.assertEqual(mig.migrate(p, apply=True)[0], "pulado")
            self.assertTrue((p / ".agent").is_symlink())


if __name__ == "__main__":
    unittest.main()
