"""The rule-file standard is CLAUDE.md + AGENTS.md at the root; GEMINI.md and .agents/rules/ are legacy.

Run from the 0 Padrões root: python3 -m unittest discover -s .agents/scripts/tests
A tracked text file may name the legacy paths only to handle them (the line says legacy/legado, or is the
`test -L` link check), or when the file is code/fixture/history/upstream text listed below.
"""

import re
import subprocess
import unittest
from pathlib import Path

KIT = Path(__file__).resolve().parents[3]
LEGACY = re.compile(r"GEMINI\.md|\.agents/rules")
HANDLED = re.compile(r"legacy|legado|test -L", re.IGNORECASE)
EXEMPT_PREFIXES = (
    ".agents/scripts/",  # code and tests that handle the legacy files
    ".agents/plans/",
    ".agents/skills/using-superpowers/",  # upstream text about other harnesses (Gemini CLI really reads GEMINI.md)
    ".agents/skills/diagnosing-superpowers/",
    "prompts-template/_arquivo/",
)
EXEMPT_FILES = {
    "prompts-template/HISTORICO.md",
    ".agents/skills/project-initializer/legacy-generic-lines.txt",  # old kit text, on purpose
    ".agents/catalog-data.js",  # generated from the files above
    ".agents/catalog.html",
    ".gitignore",
}


def tracked_text_files():
    try:
        out = subprocess.run(["git", "ls-files"], cwd=KIT, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return [f for f in out.splitlines() if f not in EXEMPT_FILES and not f.startswith(EXEMPT_PREFIXES)]


class RulesStandardTest(unittest.TestCase):
    def test_tracked_files_do_not_mandate_gemini_md_or_agent_rules(self):
        files = tracked_text_files()
        if files is None:
            self.skipTest("not a git checkout")
        offenders = []
        for rel in files:
            path = KIT / rel
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeDecodeError):
                continue
            offenders += [f"{rel}:{n}: {line.strip()[:120]}" for n, line in enumerate(lines, 1) if LEGACY.search(line) and not HANDLED.search(line)]
        self.assertEqual(offenders, [], "\n".join(offenders))


if __name__ == "__main__":
    unittest.main()
