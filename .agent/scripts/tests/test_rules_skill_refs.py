"""Every skill the rule modules cite by name can be found by an agent that follows the rules.

A rule that says "use skill `x`" is only useful when `x` exists. In a consumer project the skill is usually not
installed locally (only the `sip-*` pointers are), so it must live in this hub: `.agent/skills/<x>/`, a resolver
`prompts/resolver/<x>/`, or be listed in EXTERNAL (a skill of another SIP hub, with the SIP that owns it).

Run from the 0 Padrões root: python3 -m unittest discover -s .agent/scripts/tests
"""

import json
import json
import re
import tempfile
import unittest
from pathlib import Path

KIT = Path(__file__).resolve().parents[3]
MODULES = KIT / ".agent" / "skills" / "project-initializer" / "modules"
# Skills owned by another SIP hub: name -> SIP that owns it. The module line must name that SIP.
EXTERNAL = {"geral-anti-slop": "sip-marketing"}
CITATION = re.compile(r"skills? `([a-z0-9][a-z0-9-]*)`|skill \(`([a-z0-9][a-z0-9-]*)`\)")


def citations(text: str) -> list[tuple[str, str]]:
    """(skill name, the line that cites it) for every skill cited by name in the text."""
    found = []
    for line in text.splitlines():
        for match in CITATION.finditer(line):
            found.append((match.group(1) or match.group(2), line))
    return found


def missing(modules_dir: Path, kit: Path = KIT) -> list[str]:
    problems = []
    for module in sorted(modules_dir.glob("*.md")):
        for name, line in citations(module.read_text(encoding="utf-8")):
            if (kit / ".agent" / "skills" / name).is_dir() or (kit / "prompts" / "resolver" / name).is_dir():
                continue
            owner = EXTERNAL.get(name)
            if owner and owner in line:
                continue
            problems.append(f"{module.name}: skill `{name}` not found in the hub (and not listed in EXTERNAL)")
    return problems


NUCLEO_FILE = KIT / "prompts" / "resolver" / "sip-geral" / "nucleo.json"
# Skills core.md cites that stay out of the núcleo: used only in one situation, found on demand through `sip-geral`
# (`resolve_skill.py`). A skill that every project needs goes to nucleo.json instead.
ON_DEMAND = {
    "launch-readiness": "only before a go-live or a bulk e-mail",
    "mapa-de-destinos": "only when a deliverable has no row in docs/mapa-de-destinos.md",
    "vulnerability-scanner": "only before publishing an app or site",
}


def outside_nucleo(core_text: str, nucleo: list[str]) -> list[str]:
    """Skills cited in core.md that are neither linked in every project (núcleo) nor listed as on demand."""
    return sorted({n for n, _ in citations(core_text)} - set(nucleo) - set(ON_DEMAND) - set(EXTERNAL))


class RulesSkillRefs(unittest.TestCase):
    def test_core_cites_only_nucleo_or_on_demand_skills(self):
        nucleo = json.loads(NUCLEO_FILE.read_text(encoding="utf-8"))["skills"]
        self.assertEqual(outside_nucleo((MODULES / "core.md").read_text(encoding="utf-8"), nucleo), [],
                         "core.md cites a skill that is not linked in projects: add it to nucleo.json or to ON_DEMAND")

    def test_a_new_core_citation_outside_the_nucleo_is_reported(self):
        self.assertEqual(outside_nucleo("- Use skill `nova-skill` here.\n", ["execution-loop"]), ["nova-skill"])
        self.assertEqual(outside_nucleo("- Use skill `brainstorming` here.\n", ["brainstorming"]), [])
        self.assertEqual(outside_nucleo("- Use skill `launch-readiness` here.\n", []), [])

    def test_real_modules_cite_only_findable_skills(self):
        self.assertEqual(missing(MODULES), [])

    def test_a_made_up_skill_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp)
            (fake / "core.md").write_text("- Use skill `skill-que-nao-existe` here.\n", encoding="utf-8")
            self.assertEqual(len(missing(fake)), 1)

    def test_external_skill_must_name_its_sip_on_the_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp)
            (fake / "a.md").write_text("- Run skill `geral-anti-slop` (via `sip-marketing`).\n", encoding="utf-8")
            self.assertEqual(missing(fake), [])
            (fake / "a.md").write_text("- Run skill `geral-anti-slop`.\n", encoding="utf-8")
            self.assertEqual(len(missing(fake)), 1)


if __name__ == "__main__":
    unittest.main()
