"""Regression tests for sync_entrypoints.py and sync_rules.py.

Run from the 0 Padrões root: python3 -m unittest discover -s .agent/scripts/tests
Each test builds throwaway projects in a temp dir and runs the real script with cwd set there.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
ENTRYPOINTS = SCRIPTS / "sync_entrypoints.py"
RULES = SCRIPTS / "sync_rules.py"


def run(script: Path, cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(script), *args], cwd=cwd, capture_output=True, text=True)


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def skill(root: Path, name: str) -> Path:
    return write(root / ".agent" / "skills" / name / "SKILL.md", f"---\nname: {name}\ndescription: Use when testing {name}\n---\n")


def link_skill(project: Path, name: str, target) -> Path:
    link = project / ".claude" / "skills" / name
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(target)
    return link


class SyncEntrypointsCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.project = self.tmp / "project"
        self.hub = self.tmp / "hub"
        skill(self.project, "local-skill")
        link_skill(self.project, "local-skill", "../../.agent/skills/local-skill")

    def check(self):
        return run(ENTRYPOINTS, self.project, "--check")

    def hub_agent(self, skills: str):
        agent = write(self.hub / ".agent" / "agents" / "hub-agent.md", f"---\nname: hub-agent\ndescription: Hub agent\nskills: {skills}\n---\n")
        (self.project / ".agent" / "agents").mkdir(parents=True)
        (self.project / ".agent" / "agents" / "hub-agent.md").symlink_to(agent)
        (self.project / ".claude" / "agents").mkdir(parents=True)
        (self.project / ".claude" / "agents" / "hub-agent.md").symlink_to("../../.agent/agents/hub-agent.md")

    def test_clean_project_passes(self):
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_agent_linked_from_hub_finds_hub_skills(self):
        skill(self.hub, "hub-skill")
        self.hub_agent("hub-skill, local-skill")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_agent_linked_from_hub_still_flags_missing_skill(self):
        skill(self.hub, "hub-skill")
        self.hub_agent("hub-skill, ghost-skill")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("references missing skill: ghost-skill", result.stdout)
        self.assertNotIn("missing skill: hub-skill", result.stdout)

    def test_local_agent_does_not_see_hub_skills(self):
        skill(self.hub, "hub-skill")
        write(self.project / ".agent" / "agents" / "mine.md", "---\nname: mine\ndescription: Local agent\nskills: hub-skill\n---\n")
        (self.project / ".claude" / "agents").mkdir(parents=True)
        (self.project / ".claude" / "agents" / "mine.md").symlink_to("../../.agent/agents/mine.md")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("agent mine references missing skill: hub-skill", result.stdout)

    def test_skill_link_to_same_named_hub_skill_passes(self):
        skill(self.project, "sip-x")  # local stub
        link_skill(self.project, "sip-x", skill(self.hub, "sip-x").parent)
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout)

    def git_init(self, ignore: str):
        subprocess.run(["git", "init", "-q"], cwd=self.project, check=True)
        write(self.project / ".gitignore", ignore)

    def test_missing_link_ignored_by_gitignore_passes(self):
        # Arrange: a fresh clone has the stub but not the machine-local link to the hub
        skill(self.project, "sip-x")
        self.git_init(".claude/skills/sip-*\n")
        # Act
        result = self.check()
        # Assert
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_missing_link_not_ignored_still_fails(self):
        skill(self.project, "sip-x")
        self.git_init("node_modules/\n")
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("missing/broken symlink: .claude/skills/sip-x", result.stdout)

    def test_hub_whose_agent_folder_is_a_symlink_passes(self):
        shared = self.tmp / "shared-agent"
        write(shared / "skills" / "sip-x" / "SKILL.md", "---\nname: sip-x\ndescription: x\n---\n")
        write(shared / "skills" / "hub-skill" / "SKILL.md", "---\nname: hub-skill\ndescription: x\n---\n")
        write(shared / "agents" / "hub-agent.md", "---\nname: hub-agent\ndescription: Hub agent\nskills: hub-skill\n---\n")
        self.hub.mkdir()
        (self.hub / ".agent").symlink_to(shared)
        skill(self.project, "sip-x")
        link_skill(self.project, "sip-x", self.hub / ".agent" / "skills" / "sip-x")
        (self.project / ".agent" / "agents").mkdir(parents=True)
        (self.project / ".agent" / "agents" / "hub-agent.md").symlink_to(self.hub / ".agent" / "agents" / "hub-agent.md")
        (self.project / ".claude" / "agents").mkdir(parents=True)
        (self.project / ".claude" / "agents" / "hub-agent.md").symlink_to("../../.agent/agents/hub-agent.md")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_skill_link_to_other_named_skill_fails(self):
        skill(self.project, "sip-x")
        link_skill(self.project, "sip-x", skill(self.hub, "sip-y").parent)
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("points elsewhere", result.stdout)

    def test_skill_link_to_folder_without_skill_md_fails(self):
        skill(self.project, "sip-x")
        folder = self.hub / ".agent" / "skills" / "sip-x"
        folder.mkdir(parents=True)
        link_skill(self.project, "sip-x", folder)
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("points elsewhere", result.stdout)

    def test_skill_link_outside_agent_skills_fails(self):
        skill(self.project, "sip-x")
        target = write(self.hub / "random" / "sip-x" / "SKILL.md", "---\nname: sip-x\ndescription: x\n---\n").parent
        link_skill(self.project, "sip-x", target)
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("points elsewhere", result.stdout)


class SyncRulesCheck(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.claude = write(self.root / "CLAUDE.md", "# CLAUDE.md\nSame rules. See CLAUDE.md.\n")
        self.gemini = write(self.root / ".agent" / "rules" / "GEMINI.md", "# GEMINI.md\nSame rules. See GEMINI.md.\n")

    def snapshot(self):
        return {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def test_parity_passes_without_writing(self):
        before = self.snapshot()
        result = run(RULES, self.root, "--check")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(before, self.snapshot())

    def test_checkout_without_rule_files_passes(self):
        empty = Path(tempfile.mkdtemp())
        result = run(RULES, empty, "--check")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(list(empty.iterdir()), [])

    def test_divergence_fails_without_writing(self):
        write(self.claude, "# CLAUDE.md\nDifferent rules.\n")
        before = self.snapshot()
        result = run(RULES, self.root, "--check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("CLAUDE.md", result.stdout)
        self.assertEqual(before, self.snapshot())


if __name__ == "__main__":
    unittest.main()
