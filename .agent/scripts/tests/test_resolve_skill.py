"""Tests for resolve_skill.py: find a skill, agent or workflow by name or term in the project, the SIP hubs it consumes and the kit.

The project manifest (`.agent/SIPS-CONSUMIDOS.md`) is a snapshot taken at install time, so it only says WHERE the hubs are and which
SIPs are installed; what each hub contains is always read from disk.

Run from the 0 Padrões root: python3 -m unittest discover -s .agent/scripts/tests
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "resolve_skill.py"


def skill(hub: Path, name: str, description: str = "Use when testing.") -> Path:
    d = hub / ".agent" / "skills" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {description}\n---\nbody\n", encoding="utf-8")
    return d / "SKILL.md"


def md(hub: Path, kind: str, name: str, description: str) -> Path:
    f = hub / ".agent" / kind / f"{name}.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(f"---\nname: {name}\ndescription: {description}\n---\n", encoding="utf-8")
    return f


def world(root: Path) -> dict:
    """kit (sip-geral, installed) + hub n8n (installed) + hub mautic (listed in the kit table only) + a project."""
    kit, n8n, mautic, proj = root / "kit", root / "n8n", root / "mautic", root / "proj"
    for h in (kit, n8n, mautic):
        (h / ".agent" / "skills").mkdir(parents=True)
    (mautic / "prompts").mkdir()
    (mautic / "prompts" / "instalar-skill-sip-mautic.md").write_text("instalar", encoding="utf-8")
    (kit / "projetos").mkdir()
    (kit / "projetos" / "_sips.md").write_text(
        "| Domínio | Nome | Hub | Resolver | Prompt |\n| :-- | :-- | :-- | :-- | :-- |\n"
        f"| `geral` | SIP - Geral | `{kit}` | `sip-geral` | `x` |\n"
        f"| `n8n` | SIP - N8N | `{n8n}` | `sip-n8n` | `x` |\n"
        f"| `mautic` | SIP - Mautic | `{mautic}` | `sip-mautic` | `x` |\n", encoding="utf-8")
    (proj / ".agent" / "skills").mkdir(parents=True)
    (proj / ".agent" / "SIPS-CONSUMIDOS.md").write_text(
        "# SIPs consumidos\n\n"
        f"## SIP - Geral (`sip-geral`)\n- Hub: {kit}\n- Instalado/atualizado em: 2026-11-01\n- Skill: sip-geral\n- Agents: nenhum\n- Workflows: nenhum\n\n"
        f"## SIP - N8N (`sip-n8n`)\n- Hub: {n8n}\n- Instalado/atualizado em: 2026-11-01\n- Skill: sip-n8n\n- Agents: nenhum\n- Workflows: nenhum\n",
        encoding="utf-8")
    return {"kit": kit, "n8n": n8n, "mautic": mautic, "proj": proj}


def run(w: dict, *query: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *query, "--project", str(w["proj"]), "--kit", str(w["kit"])],
                          capture_output=True, text=True, timeout=60, check=False)


class ResolveSkill(unittest.TestCase):
    def test_exact_name_in_an_installed_hub_gives_the_absolute_path(self):
        with tempfile.TemporaryDirectory() as t:
            w = world(Path(t))
            path = skill(w["kit"], "execution-loop")
            r = run(w, "execution-loop")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn(str(path), r.stdout)
            self.assertIn("instalado neste projeto", r.stdout)

    def test_project_local_skill_is_reported_as_the_projects_own(self):
        with tempfile.TemporaryDirectory() as t:
            w = world(Path(t))
            path = skill(w["proj"], "minha-skill")
            r = run(w, "minha-skill")
            self.assertEqual(r.returncode, 0)
            self.assertIn(str(path), r.stdout)
            self.assertIn("do projeto", r.stdout)

    def test_skill_of_a_sip_that_is_not_installed_says_so_and_names_the_install_prompt(self):
        with tempfile.TemporaryDirectory() as t:
            w = world(Path(t))
            skill(w["mautic"], "mautic-campanhas")
            r = run(w, "mautic-campanhas")
            self.assertEqual(r.returncode, 0)
            self.assertIn("não instalado neste projeto", r.stdout)
            self.assertIn("instalar-skill-sip-mautic.md", r.stdout)

    def test_content_comes_from_disk_not_from_the_install_snapshot(self):
        with tempfile.TemporaryDirectory() as t:
            w = world(Path(t))
            self.assertEqual(run(w, "recente").returncode, 1)
            skill(w["n8n"], "recente")  # added to the hub after the project was installed
            self.assertEqual(run(w, "recente").returncode, 0)

    def test_term_matches_the_description(self):
        with tempfile.TemporaryDirectory() as t:
            w = world(Path(t))
            skill(w["n8n"], "fluxo-x", "Use when building webhooks and scraping pipelines.")
            r = run(w, "scraping")
            self.assertEqual(r.returncode, 0)
            self.assertIn("fluxo-x", r.stdout)

    def test_exact_name_ranks_before_partial_matches(self):
        with tempfile.TemporaryDirectory() as t:
            w = world(Path(t))
            skill(w["kit"], "alpha-extra")
            skill(w["kit"], "alpha")
            lines = [l for l in run(w, "alpha").stdout.splitlines() if l.startswith("[")]
            self.assertIn("alpha ", lines[0] + " ")
            self.assertNotIn("alpha-extra", lines[0])

    def test_agents_and_workflows_are_found_with_their_kind(self):
        with tempfile.TemporaryDirectory() as t:
            w = world(Path(t))
            md(w["kit"], "agents", "code-reviewer", "Reviews code.")
            md(w["kit"], "workflows", "tdd-cycle", "Runs red-green-refactor.")
            self.assertIn("[agent] code-reviewer", run(w, "code-reviewer").stdout)
            self.assertIn("[workflow] tdd-cycle", run(w, "tdd-cycle").stdout)

    def test_not_found_exits_1_and_shows_where_it_looked(self):
        with tempfile.TemporaryDirectory() as t:
            w = world(Path(t))
            r = run(w, "nao-existe-em-lugar-nenhum")
            self.assertEqual(r.returncode, 1)
            self.assertIn("não encontrada", r.stdout)
            for place in (str(w["proj"]), str(w["kit"]), str(w["n8n"]), str(w["mautic"])):
                self.assertIn(place, r.stdout)

    def test_a_hub_that_is_gone_is_reported_not_a_crash(self):
        with tempfile.TemporaryDirectory() as t:
            w = world(Path(t))
            skill(w["kit"], "alpha")
            n8n = w["n8n"]
            for p in sorted(n8n.rglob("*"), reverse=True):
                p.rmdir() if p.is_dir() else p.unlink()
            n8n.rmdir()
            r = run(w, "alpha")
            self.assertEqual(r.returncode, 0)
            self.assertIn("hub não encontrado", r.stdout)

    def test_usage_errors_exit_2(self):
        r = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, timeout=60, check=False)
        self.assertEqual(r.returncode, 2)
        with tempfile.TemporaryDirectory() as t:
            w = world(Path(t))
            r = subprocess.run([sys.executable, str(SCRIPT), "x", "--project", str(Path(t) / "nada"), "--kit", str(w["kit"])],
                               capture_output=True, text=True, timeout=60, check=False)
            self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
