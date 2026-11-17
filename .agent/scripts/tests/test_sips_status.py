"""Tests for sips_status.py: read-only status of the SIPs a project consumes.

Run from the 0 Padrões root: python3 -m unittest discover -s .agent/scripts/tests
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "sips_status.py"


def make_hub(root: Path, date: str, agents: list[str]) -> Path:
    hub = root / "hub"
    (hub / ".agent" / "skills" / "sip-x").mkdir(parents=True)
    (hub / ".agent" / "skills" / "sip-x" / "SKILL.md").write_text(f"- Última atualização do hub: {date}\n", encoding="utf-8")
    (hub / ".agent" / "agents").mkdir(parents=True)
    for a in agents:
        (hub / ".agent" / "agents" / f"{a}.md").write_text("x", encoding="utf-8")
    return hub


def make_project(root: Path, hub: Path, installed: str, seen: str, link: bool = True) -> Path:
    proj = root / "proj"
    for base in (".agent", ".claude"):
        (proj / base / "skills").mkdir(parents=True)
        if link:
            (proj / base / "skills" / "sip-x").symlink_to(hub / ".agent" / "skills" / "sip-x")
    manifest = (
        "# SIPs consumidos\n\n## SIP - X (`sip-x`)\n"
        f"- Hub: {hub}\n- Instalado/atualizado em: {installed}\n- Skill: sip-x\n- Agents: nenhum\n- Workflows: nenhum\n"
        f"- Vistos no hub: {seen}\n- Conflitos: nenhum\n- Para atualizar: cole de novo \"{hub}/prompts/i.md\"\n"
    )
    (proj / ".agent" / "SIPS-CONSUMIDOS.md").write_text(manifest, encoding="utf-8")
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
            self.assertIn("1 agents saíram do hub: velho", r.stdout)

    def test_missing_link(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, "2026-11-12", ["a"])
            r = run(make_project(root, hub, "2026-11-12", "agents a; workflows nenhum", link=False))
            self.assertEqual(r.returncode, 1)
            self.assertIn("não existe", r.stdout)

    def test_no_manifest(self):
        with tempfile.TemporaryDirectory() as t:
            r = run(Path(t))
            self.assertEqual(r.returncode, 0)
            self.assertIn("nenhum SIP registrado", r.stdout)


if __name__ == "__main__":
    unittest.main()
