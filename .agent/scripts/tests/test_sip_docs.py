"""Cross-file check: step numbers that the SIP registry/manifest reference cites must match the install-prompt template."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / ".agent/skills/superiaprojects-criar-sip/SKILL.md"
SIPS = ROOT / ".agent/skills/superiaprojects-criar-sip/references/sips-registro-e-manifesto.md"

# _sips.md section heading -> template step it talks about
SECTION_STEP = {
    "## Registro de instalações": r"^(\d+)\. Registre esta instalação no hub",
    "## Manifesto local": r"^(\d+)\. Atualize o manifesto local",
}


def template_step(pattern: str) -> str:
    match = re.search(pattern, SKILL.read_text(encoding="utf-8"), re.MULTILINE)
    assert match, f"step not found in template: {pattern}"
    return match.group(1)


def section(text: str, heading: str) -> str:
    start = text.index(heading)
    end = text.find("\n## ", start + len(heading))
    return text[start:end if end != -1 else len(text)]


class SipsStepReferences(unittest.TestCase):
    def test_cited_steps_match_template(self):
        # Arrange
        sips = SIPS.read_text(encoding="utf-8")
        # Act / Assert
        for heading, pattern in SECTION_STEP.items():
            expected = template_step(pattern)
            for cited in re.findall(r"\(passo (\d+)\)", section(sips, heading)):
                self.assertEqual(cited, expected, f"{heading}: cita passo {cited}, template diz {expected}")


class SkillPassoReferences(unittest.TestCase):
    def test_every_cited_passo_has_a_heading(self):
        # Arrange
        text = SKILL.read_text(encoding="utf-8")
        headings = set(re.findall(r"^## Passo (\d+) —", text, re.MULTILINE))
        # Act
        cited = set(re.findall(r"(?<!## )Passo (\d+)", text))
        # Assert
        self.assertEqual(cited - headings, set(), f"citados sem título: {sorted(cited - headings)}")


if __name__ == "__main__":
    unittest.main()
