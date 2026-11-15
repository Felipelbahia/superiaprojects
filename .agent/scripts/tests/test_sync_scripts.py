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


def run(script: Path, cwd: Path, *args: str, stdin: str = "") -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(script), *args], cwd=cwd, capture_output=True, text=True, input=stdin)


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


BRAIN_FILES = ("contextos.md", "licoes.md", "decisoes.md")


class SyncEntrypointsBrain(unittest.TestCase):
    """An agent that declares `autonomy` adopted the brain model; the others are not checked."""

    def setUp(self):
        self.project = Path(tempfile.mkdtemp()) / "project"

    def agent(self, autonomy: str = "propose", name: str = "dir"):
        extra = f"autonomy: {autonomy}\n" if autonomy else ""
        write(self.project / ".agent" / "agents" / f"{name}.md", f"---\nname: {name}\ndescription: Use when testing\n{extra}---\n")
        link = self.project / ".claude" / "agents" / f"{name}.md"
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(f"../../.agent/agents/{name}.md")

    def brain(self, skip: tuple[str, ...] = (), name: str = "dir"):
        base = self.project / ".agent" / "agents" / "agents_brains" / name
        base.mkdir(parents=True, exist_ok=True)
        for item in BRAIN_FILES:
            if item not in skip:
                write(base / item, "x\n")
        if "inbox" not in skip:
            (base / "inbox").mkdir(exist_ok=True)

    def check(self):
        return run(ENTRYPOINTS, self.project, "--check")

    def test_complete_brain_passes(self):
        self.agent()
        self.brain()
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_contexts_level_is_valid(self):
        self.agent("contexts")
        self.brain()
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_missing_brain_folder_fails(self):
        self.agent()
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("agent dir has no brain", result.stdout)

    def test_missing_brain_file_fails_and_names_it(self):
        self.agent()
        self.brain(skip=("licoes.md",))
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("licoes.md", result.stdout)

    def test_missing_inbox_fails(self):
        self.agent()
        self.brain(skip=("inbox",))
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("inbox", result.stdout)

    def test_invalid_autonomy_fails(self):
        self.agent("free")
        self.brain()
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("autonomy", result.stdout)

    def test_agent_without_autonomy_is_not_checked(self):
        self.agent("")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_empty_skills_line_does_not_swallow_the_next_field(self):
        write(self.project / ".agent" / "agents" / "dir.md", "---\nname: dir\ndescription: Use when testing\nskills:\nautonomy: propose\n---\n")
        link = self.project / ".claude" / "agents" / "dir.md"
        link.parent.mkdir(parents=True)
        link.symlink_to("../../.agent/agents/dir.md")
        self.brain()
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_brains_folder_is_not_counted_as_an_agent(self):
        self.agent()
        self.brain()
        result = self.check()
        self.assertIn("agents=1 ", result.stdout)


class SyncRulesCheck(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.claude = write(self.root / "CLAUDE.md", "# CLAUDE.md\nSame rules. See CLAUDE.md.\n")
        self.agents = write(self.root / "AGENTS.md", "# AGENTS.md\nSame rules. See AGENTS.md.\n")

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


RULES_TEXT = "# CLAUDE.md\nSame rules. See CLAUDE.md.\n"


class SyncRulesWrite(unittest.TestCase):
    """The standard is CLAUDE.md + AGENTS.md at the root; GEMINI.md and .agent/rules/ are legacy."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.claude = write(self.root / "CLAUDE.md", RULES_TEXT)

    def names(self):
        return sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*") if p.is_file())

    def test_sync_writes_only_claude_and_agents(self):
        result = run(RULES, self.root)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.names(), ["AGENTS.md", "CLAUDE.md"])
        self.assertEqual((self.root / "AGENTS.md").read_text(encoding="utf-8").splitlines()[0], "# AGENTS.md")

    def test_sync_does_not_touch_existing_legacy_files(self):
        legacy = write(self.root / "GEMINI.md", "# GEMINI.md\nOld rules.\n")
        rules = write(self.root / ".agent" / "rules" / "CLAUDE.md", "# CLAUDE.md\nOld rules.\n")
        run(RULES, self.root)
        self.assertEqual(self.claude.read_text(encoding="utf-8"), RULES_TEXT)  # a newer legacy file is never the source
        self.assertEqual(legacy.read_text(encoding="utf-8"), "# GEMINI.md\nOld rules.\n")
        self.assertEqual(rules.read_text(encoding="utf-8"), "# CLAUDE.md\nOld rules.\n")

    def test_cursorrules_is_synced_only_when_it_exists(self):
        run(RULES, self.root)
        self.assertFalse((self.root / ".cursorrules").exists())
        write(self.root / ".cursorrules", "Different.\n")
        self.assertEqual(run(RULES, self.root, "--check").returncode, 1)
        run(RULES, self.root)
        self.assertEqual(run(RULES, self.root, "--check").returncode, 0)

    def test_check_warns_about_legacy_without_failing(self):
        run(RULES, self.root)
        write(self.root / "GEMINI.md", "# GEMINI.md\nOld rules.\n")
        result = run(RULES, self.root, "--check")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("GEMINI.md", result.stdout)
        self.assertIn("--clean-legacy", result.stdout)


class SyncRulesCleanLegacy(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        write(self.root / "CLAUDE.md", RULES_TEXT)
        write(self.root / "AGENTS.md", "# AGENTS.md\nSame rules. See AGENTS.md.\n")
        self.gemini = write(self.root / "GEMINI.md", "# GEMINI.md\nSame rules. See GEMINI.md.\n")
        self.rules = write(self.root / ".agent" / "rules" / "CLAUDE.md", RULES_TEXT)

    def test_without_confirmation_nothing_is_deleted(self):
        for answer in ("n\n", ""):
            result = run(RULES, self.root, "--clean-legacy", stdin=answer)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertTrue(self.gemini.exists() and self.rules.exists())
            self.assertIn("GEMINI.md", result.stdout)

    def test_confirmed_removes_identical_legacy_and_the_empty_folder(self):
        result = run(RULES, self.root, "--clean-legacy", stdin="s\n")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertFalse(self.gemini.exists())
        self.assertFalse((self.root / ".agent" / "rules").exists())
        self.assertTrue((self.root / "CLAUDE.md").exists() and (self.root / "AGENTS.md").exists())

    def test_diverged_legacy_is_never_deleted_and_is_named(self):
        write(self.gemini, "# GEMINI.md\nA local rule only here.\n")
        result = run(RULES, self.root, "--clean-legacy", stdin="s\n")
        self.assertTrue(self.gemini.exists())
        self.assertIn("GEMINI.md", result.stdout)
        self.assertIn("differs", result.stdout)
        self.assertFalse(self.rules.exists())  # the identical one still went

    def test_folder_with_other_files_is_kept(self):
        other = write(self.root / ".agent" / "rules" / "notes.md", "mine\n")
        run(RULES, self.root, "--clean-legacy", stdin="s\n")
        self.assertTrue(other.exists())


class SyncEntrypointsModelConversion(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.project = self.tmp / "project"
        skill(self.project, "local-skill")
        link_skill(self.project, "local-skill", "../../.agent/skills/local-skill")

    def run_sync(self, *args):
        return run(ENTRYPOINTS, self.project, *args)

    def test_agent_with_inherit_model_creates_symlink(self):
        write(self.project / ".agent" / "agents" / "agent-inherit.md", "---\nname: agent-inherit\ndescription: Test agent\nmodel: inherit\n---\n# Agent\n")
        res = self.run_sync()
        self.assertEqual(res.returncode, 0, res.stdout)
        dest = self.project / ".claude" / "agents" / "agent-inherit.md"
        self.assertTrue(dest.is_symlink())
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_agent_with_flash_lite_creates_converted_file(self):
        write(self.project / ".agent" / "agents" / "agent-fast.md", "---\nname: agent-fast\ndescription: Fast agent\nmodel: flash_lite\n---\n# Fast Agent\n")
        res = self.run_sync()
        self.assertEqual(res.returncode, 0, res.stdout)
        dest = self.project / ".claude" / "agents" / "agent-fast.md"
        self.assertFalse(dest.is_symlink())
        self.assertTrue(dest.is_file())
        content = dest.read_text(encoding="utf-8")
        self.assertIn("<!-- antigravity-kit:generated", content)
        self.assertIn("model: haiku", content)
        self.assertNotIn("model: flash_lite", content)
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_agent_with_pro_creates_converted_file(self):
        write(self.project / ".agent" / "agents" / "agent-pro.md", "---\nname: agent-pro\ndescription: Pro agent\nmodel: pro\n---\n# Pro Agent\n")
        res = self.run_sync()
        self.assertEqual(res.returncode, 0, res.stdout)
        dest = self.project / ".claude" / "agents" / "agent-pro.md"
        self.assertFalse(dest.is_symlink())
        content = dest.read_text(encoding="utf-8")
        self.assertIn("model: sonnet", content)
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_converted_agent_out_of_date_fails_check(self):
        write(self.project / ".agent" / "agents" / "agent-fast.md", "---\nname: agent-fast\ndescription: Fast agent\nmodel: flash_lite\n---\n# Fast Agent\n")
        self.run_sync()
        self.assertEqual(self.run_sync("--check").returncode, 0)
        # Edit source without syncing
        write(self.project / ".agent" / "agents" / "agent-fast.md", "---\nname: agent-fast\ndescription: Fast agent\nmodel: flash_lite\n---\n# Fast Agent Modified\n")
        res = self.run_sync("--check")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("out of date", res.stdout)
        # Run sync and check passes again
        self.run_sync()
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_unexpected_real_file_fails_check(self):
        write(self.project / ".agent" / "agents" / "fake.md", "---\nname: fake\ndescription: Fake\nmodel: inherit\n---\n# Fake\n")
        dest = write(self.project / ".claude" / "agents" / "fake.md", "# Real file not generated\n")
        res = self.run_sync("--check")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("REAL (not symlink)", res.stdout)

    def test_model_changed_from_flash_lite_to_inherit_replaces_file_with_symlink(self):
        src = write(self.project / ".agent" / "agents" / "toggle.md", "---\nname: toggle\ndescription: Toggle\nmodel: flash_lite\n---\n# Toggle\n")
        self.run_sync()
        dest = self.project / ".claude" / "agents" / "toggle.md"
        self.assertFalse(dest.is_symlink())
        self.assertTrue(dest.is_file())
        # Change model back to inherit
        write(src, "---\nname: toggle\ndescription: Toggle\nmodel: inherit\n---\n# Toggle\n")
        self.run_sync()
        self.assertTrue(dest.is_symlink())
        self.assertEqual(self.run_sync("--check").returncode, 0)


if __name__ == "__main__":
    unittest.main()
