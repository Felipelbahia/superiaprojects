"""Tests for sips_status.py: read-only status of the SIPs a project consumes.

Run from the 0 Padrões root: python3 -m unittest discover -s .agents/scripts/tests
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "sips_status.py"


def make_hub(root: Path, date: str, agents: list[str]) -> Path:
    hub = root / "hub"
    (hub / ".agents" / "skills" / "sip-x").mkdir(parents=True)
    (hub / ".agents" / "skills" / "sip-x" / "SKILL.md").write_text(f"- Última atualização do hub: {date}\n", encoding="utf-8")
    (hub / ".agents" / "agents").mkdir(parents=True)
    for a in agents:
        (hub / ".agents" / "agents" / f"{a}.md").write_text("x", encoding="utf-8")
    return hub


def make_project(root: Path, hub: Path, installed: str, seen: str, link: bool = True) -> Path:
    proj = root / "proj"
    for base in (".agents", ".claude"):
        (proj / base / "skills").mkdir(parents=True)
        if link:
            (proj / base / "skills" / "sip-x").symlink_to(hub / ".agents" / "skills" / "sip-x")
    manifest = (
        "# SIPs consumidos\n\n## SIP - X (`sip-x`)\n"
        f"- Hub: {hub}\n- Instalado/atualizado em: {installed}\n- Skill: sip-x\n- Agents: nenhum\n- Workflows: nenhum\n"
        f"- Vistos no hub: {seen}\n- Conflitos: nenhum\n- Para atualizar: cole de novo \"{hub}/prompts/i.md\"\n"
    )
    (proj / ".agents" / "SIPS-CONSUMIDOS.md").write_text(manifest, encoding="utf-8")
    return proj


def run(proj: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), str(proj)], capture_output=True, text=True, timeout=60, check=False)


class SipsStatusTests(unittest.TestCase):
    def test_up_to_date(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, "2026-11-12", ["a"])
            r = run(make_project(root, hub, "2026-11-12", "agents a; workflows nenhum"))
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("[em dia]", r.stdout)

    def test_hub_newer_date(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, "2026-11-13", ["a"])
            r = run(make_project(root, hub, "2026-11-12", "agents a; workflows nenhum"))
            self.assertEqual(r.returncode, 1)
            self.assertIn("hub atualizado em 2026-11-13", r.stdout)

    def test_new_and_removed_agents(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, "2026-11-12", ["a", "novo"])
            r = run(make_project(root, hub, "2026-11-12", "agents a, velho; workflows nenhum"))
            self.assertEqual(r.returncode, 1)
            self.assertIn("1 agents novos no hub: novo", r.stdout)
            self.assertNotIn("saíram do hub", r.stdout)  # not chosen by the project: no noise

    def test_chosen_agent_that_left_hub_is_flagged(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, "2026-11-12", ["a"])
            proj = make_project(root, hub, "2026-11-12", "agents a, velho; workflows nenhum")
            m = proj / ".agents" / "SIPS-CONSUMIDOS.md"
            m.write_text(m.read_text(encoding="utf-8").replace("- Agents: nenhum", "- Agents: velho"), encoding="utf-8")
            r = run(proj)
            self.assertEqual(r.returncode, 1)
            self.assertIn("1 agents saíram do hub: velho", r.stdout)

    def test_missing_link(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, "2026-11-12", ["a"])
            r = run(make_project(root, hub, "2026-11-12", "agents a; workflows nenhum", link=False))
            self.assertEqual(r.returncode, 1)
            self.assertIn("não existe", r.stdout)

    def test_real_stub_with_direct_claude_link_is_up_to_date(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, "2026-11-12", ["a"])
            proj = make_project(root, hub, "2026-11-12", "agents a; workflows nenhum", link=False)
            stub = proj / ".agents" / "skills" / "sip-x"
            stub.mkdir()
            (stub / "SKILL.md").write_text("stub", encoding="utf-8")
            (proj / ".claude" / "skills" / "sip-x").symlink_to(hub / ".agents" / "skills" / "sip-x")
            r = run(proj)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("[em dia]", r.stdout)

    def test_real_stub_without_claude_link_still_flags(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, "2026-11-12", ["a"])
            proj = make_project(root, hub, "2026-11-12", "agents a; workflows nenhum", link=False)
            (proj / ".agents" / "skills" / "sip-x").mkdir()
            r = run(proj)
            self.assertEqual(r.returncode, 1)

    def generated(self, proj: Path, expose: str = "link"):
        stub = proj / ".agents" / "skills" / "sip-x"
        stub.mkdir(parents=True, exist_ok=True)
        (stub / "SKILL.md").write_text("---\nname: sip-x\ndescription: Use when testing.\n---\n<!-- generated by SIP - X scripts/install-sip.mjs; do not edit, re-run the installer -->\nhub at /somewhere\n", encoding="utf-8")
        link = proj / ".claude" / "skills" / "sip-x"
        if expose == "link":
            link.symlink_to("../../.agents/skills/sip-x")
        return stub

    def test_generated_copy_exposed_through_local_stub_is_up_to_date(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, "2026-11-12", ["a"])
            proj = make_project(root, hub, "2026-11-12", "agents a; workflows nenhum", link=False)
            self.generated(proj)
            r = run(proj)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("[em dia]", r.stdout)

    def test_generated_copy_without_claude_exposure_still_flags(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, "2026-11-12", ["a"])
            proj = make_project(root, hub, "2026-11-12", "agents a; workflows nenhum", link=False)
            self.generated(proj, expose="none")
            r = run(proj)
            self.assertEqual(r.returncode, 1)
            self.assertIn(".claude/skills/sip-x", r.stdout)

    def test_real_stub_without_the_mark_is_not_a_generated_copy(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, "2026-11-12", ["a"])
            proj = make_project(root, hub, "2026-11-12", "agents a; workflows nenhum", link=False)
            stub = proj / ".agents" / "skills" / "sip-x"
            stub.mkdir()
            (stub / "SKILL.md").write_text("stub", encoding="utf-8")
            (proj / ".claude" / "skills" / "sip-x").symlink_to("../../.agents/skills/sip-x")
            r = run(proj)
            self.assertEqual(r.returncode, 1)

    def test_no_manifest(self):
        with tempfile.TemporaryDirectory() as t:
            r = run(Path(t))
            self.assertEqual(r.returncode, 0)
            self.assertIn("nenhum SIP registrado", r.stdout)


if __name__ == "__main__":
    unittest.main()
