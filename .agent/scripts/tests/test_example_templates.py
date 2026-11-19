"""CLAUDE.example.md and ClaudeExample.md (what install.sh / install.py copy to a new kit's CLAUDE.md) follow the modules.

Each template is a hand-written header plus a body assembled from the modules `core`, `code` and `interface`.
The body, from "## 1. Project profile" on, must equal what assemble_rules.py builds from those modules today.
When this fails, regenerate the body (see the diff) instead of editing the template by hand.

Run from the 0 Padrões root: python3 -m unittest discover -s .agent/scripts/tests
"""

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
KIT = SCRIPTS.parent.parent
sys.path.insert(0, str(SCRIPTS))

import assemble_rules as ar  # noqa: E402

START = "## 1. Project profile"
MODULES = ["core", "code", "interface"]


def expected_body() -> str:
    text = ar.assemble(MODULES, "x", "x.md", ar.DEFAULT_DIR)
    return text[text.index(START):]


class ExampleTemplates(unittest.TestCase):
    def test_templates_match_the_modules(self):
        expected = expected_body()
        for name in ("CLAUDE.example.md", "ClaudeExample.md"):
            text = (KIT / name).read_text(encoding="utf-8")
            self.assertIn(START, text, name)
            self.assertEqual(text[text.index(START):], expected, f"{name} is behind the modules: regenerate its body")


if __name__ == "__main__":
    unittest.main()
