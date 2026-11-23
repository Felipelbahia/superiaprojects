"""Tests for the `.agents` / `.agent` dual support (linkutil.adir and the scripts that read projects not migrated yet).

Run from the 0 Padrões root: python3 -m unittest discover -s .agents/scripts/tests
"""

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import linkutil  # noqa: E402
import resolve_skill  # noqa: E402


class AdirTest(unittest.TestCase):
    def test_standard_name_wins_and_is_the_default_to_create(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.assertEqual(linkutil.adir(root), ".agents")  # neither exists: the one to create
            (root / ".agent").mkdir()
            self.assertEqual(linkutil.adir(root), ".agent")  # project not migrated yet
            (root / ".agents").mkdir()
            self.assertEqual(linkutil.adir(root), ".agents")  # both: the standard one

    def test_resolver_finds_a_skill_in_a_legacy_hub(self):
        with tempfile.TemporaryDirectory() as d:
            skill = Path(d) / ".agent" / "skills" / "old-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: old-skill\ndescription: legacy\n---\n", encoding="utf-8")
            self.assertEqual([n for _, n, _ in resolve_skill.items(Path(d))], ["old-skill"])


KIT = Path(__file__).resolve().parents[3]
OLD_NAME = re.compile(r"(?<![A-Za-z0-9_])\.agent(?![A-Za-z0-9_-])")
# Files third parties copy or read on GitHub: they must teach the new folder name. The one allowed mention is the
# migration step of prompt 01 (a project still on `.agent/`), which says so on the same line.
PUBLIC = ["prompts", "prompts-template", ".agents/skills/project-initializer/modules", "README.md", "README.en.md",
          "SETUP.md", "install.sh", "install.py", "CONTRIBUTING.md", "STANDARDS.md", "CLAUDE.md", "AGENTS.md"]


class PublicFilesUseNewNameTest(unittest.TestCase):
    def test_no_singular_agent_folder_in_public_files(self):
        bad = []
        for name in PUBLIC:
            base = KIT / name
            files = [base] if base.is_file() else sorted(base.rglob("*.md")) + sorted(base.rglob("*.txt"))
            for f in files:
                if f.name == "migracao-agent-para-agents.md":
                    continue  # the migration note names the old folder on purpose
                for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                    if OLD_NAME.search(line) and "o nome antigo" not in line and "ainda tem `.agent/`" not in line \
                            and "Se o projeto ainda tem" not in line and "Sem o meu OK" not in line:
                        bad.append(f"{f.relative_to(KIT)}:{n}")
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
