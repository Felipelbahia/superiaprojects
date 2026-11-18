"""Tests for propagar_sip.py: propagate a SIP hub update to the projects that consume it.

Run from the 0 Padrões root: python3 -m unittest discover -s .agent/scripts/tests
"""

import os
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "propagar_sip.py"
TODAY = date.today().isoformat()


def make_hub(root: Path, agents: list[str]) -> Path:
    hub = root / "hub"
    (hub / ".agent" / "skills" / "sip-x").mkdir(parents=True)
    (hub / ".agent" / "skills" / "sip-x" / "SKILL.md").write_text("---\nname: sip-x\ndescription: Use when testing.\n---\n- Última atualização do hub: 2026-11-12\n", encoding="utf-8")
    (hub / ".agent" / "agents").mkdir(parents=True)
    for a in agents:
        (hub / ".agent" / "agents" / f"{a}.md").write_text("x", encoding="utf-8")
    (hub / "instalacoes").mkdir()
    (hub / "instalacoes" / "README.md").write_text("# readme\n", encoding="utf-8")
    return hub


def register(hub: Path, name: str, proj: Path) -> Path:
    f = hub / "instalacoes" / f"{name}.md"
    f.write_text(
        f"## Projeto\n{name}\n\n## Caminho absoluto\n{proj}\n\n## Instalado em\n2026-11-01\n\n"
        "## Última atualização\n2026-11-01\n\n## Recursos instalados\n- Skill: sip-x (sempre)\n",
        encoding="utf-8",
    )
    return f


def make_project(root: Path, hub: Path, name="proj", seen="agents a; workflows nenhum", agents="nenhum",
                 links=True, installed="2026-11-01") -> Path:
    proj = root / name
    for base in (".agent", ".claude"):
        (proj / base / "skills").mkdir(parents=True)
        if links:
            (proj / base / "skills" / "sip-x").symlink_to(hub / ".agent" / "skills" / "sip-x")
    (proj / "inbox").mkdir()
    manifest = (
        "# SIPs consumidos\n\n## SIP - X (`sip-x`)\n"
        f"- Hub: {hub}\n- Instalado/atualizado em: {installed}\n- Skill: sip-x\n- Agents: {agents}\n- Workflows: nenhum\n"
        f"- Vistos no hub: {seen}\n- Conflitos: nenhum\n- Para atualizar: cole de novo \"{hub}/prompts/i.md\"\n"
    )
    (proj / ".agent" / "SIPS-CONSUMIDOS.md").write_text(manifest, encoding="utf-8")
    return proj


def snapshot(root: Path) -> dict:
    out = {}
    for p in sorted(root.rglob("*")):
        rel = str(p.relative_to(root))
        if p.is_symlink():
            out[rel] = ("link", str(p.readlink()))
        elif p.is_file():
            out[rel] = ("file", p.read_text(encoding="utf-8", errors="replace"))
        else:
            out[rel] = ("dir", "")
    return out


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, timeout=120, check=False)


class PropagarTests(unittest.TestCase):
    def test_discovery_reports_missing_project_and_missing_entry(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, ["a"])
            register(hub, "ghost", root / "nao-existe")
            bare = root / "bare"
            bare.mkdir()
            register(hub, "bare", bare)
            ok = make_project(root, hub, seen="agents a; workflows nenhum")
            register(hub, "ok", ok)
            r = run(str(hub))
            self.assertIn("ghost", r.stdout)
            self.assertIn("não existe em disco", r.stdout)
            self.assertIn("sem entrada deste hub no manifesto", r.stdout)
            self.assertNotIn("README", r.stdout)

    def test_dry_run_changes_nothing(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, ["a", "novo"])
            proj = make_project(root, hub, links=False)
            register(hub, "proj", proj)
            before = snapshot(root)
            r = run(str(hub))
            self.assertEqual(snapshot(root), before)
            self.assertIn("simulação", r.stdout)
            self.assertIn("não verificado", r.stdout)

    def test_apply_fixes_links_date_and_registry(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, ["a"])
            proj = make_project(root, hub, links=False)
            reg = register(hub, "proj", proj)
            run(str(hub), "--apply")
            for base in (".agent", ".claude"):
                link = proj / base / "skills" / "sip-x"
                self.assertTrue(link.is_symlink())
                self.assertTrue((link / "SKILL.md").exists())
            self.assertIn(f"Instalado/atualizado em: {TODAY}", (proj / ".agent" / "SIPS-CONSUMIDOS.md").read_text(encoding="utf-8"))
            self.assertRegex(reg.read_text(encoding="utf-8"), rf"## Última atualização\n{TODAY}")

    def test_apply_never_touches_real_files(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, ["a"])
            proj = make_project(root, hub, links=False)
            real = proj / ".agent" / "skills" / "sip-x"
            real.mkdir()
            (real / "SKILL.md").write_text("meu arquivo", encoding="utf-8")
            (proj / ".claude" / "skills" / "sip-x").symlink_to(hub / ".agent" / "skills" / "sip-x")
            register(hub, "proj", proj)
            # real dir at .agent + good link at .claude = stub-exception pattern: stays untouched
            run(str(hub), "--apply")
            self.assertFalse(real.is_symlink())
            self.assertEqual((real / "SKILL.md").read_text(encoding="utf-8"), "meu arquivo")

    def test_conflict_with_real_file_is_reported_not_overwritten(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, ["a"])
            proj = make_project(root, hub, links=False)
            (proj / ".claude" / "skills" / "sip-x").mkdir()
            (proj / ".claude" / "skills" / "sip-x" / "SKILL.md").write_text("meu", encoding="utf-8")
            register(hub, "proj", proj)
            r = run(str(hub), "--apply")
            self.assertFalse((proj / ".claude" / "skills" / "sip-x").is_symlink())
            self.assertIn("conflito", r.stdout)

    def test_new_agent_not_installed_and_note_is_idempotent(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, ["a", "novo"])
            proj = make_project(root, hub)
            (proj / "inbox" / "arquivo").mkdir()
            (proj / "inbox" / "arquivo" / "007-velho.md").write_text("x", encoding="utf-8")
            register(hub, "proj", proj)
            run(str(hub), "--apply")
            run(str(hub), "--apply")
            self.assertFalse((proj / ".agent" / "agents" / "novo.md").exists())
            notes = [p for p in (proj / "inbox").glob("*.md")]
            self.assertEqual(len(notes), 1, notes)
            self.assertRegex(notes[0].name, r"^008-sip-x-novidades\.md$")
            self.assertIn("novo", notes[0].read_text(encoding="utf-8"))

    def test_gone_item_not_chosen_makes_no_note(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, ["a"])
            proj = make_project(root, hub, seen="agents a, velho; workflows nenhum", installed=TODAY)
            register(hub, "proj", proj)
            r = run(str(hub), "--apply")
            self.assertEqual(list((proj / "inbox").glob("*.md")), [])
            self.assertNotIn("saíram", r.stdout)

    def test_old_format_seen_list_is_unverified_not_news(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, ["a", "b", "c"])
            proj = make_project(root, hub, seen="agents core; workflows core")
            register(hub, "proj", proj)
            r = run(str(hub), "--apply")
            self.assertEqual(list((proj / "inbox").glob("*.md")), [])
            self.assertIn("formato antigo", r.stdout)

    def test_chosen_item_that_left_hub_is_reported_not_recreated(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, ["a"])
            proj = make_project(root, hub, agents="sumiu", seen="agents a, sumiu; workflows nenhum")
            register(hub, "proj", proj)
            r = run(str(hub), "--apply")
            self.assertIn("agent sumiu escolhido pelo projeto saiu do hub", r.stdout)
            self.assertFalse(os.path.lexists(proj / ".agent" / "agents" / "sumiu.md"))

    def test_stub_exception_is_up_to_date(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, ["a"])
            proj = make_project(root, hub, links=False, installed=TODAY)
            stub = proj / ".agent" / "skills" / "sip-x"
            stub.mkdir()
            (stub / "SKILL.md").write_text("stub", encoding="utf-8")
            (proj / ".claude" / "skills" / "sip-x").symlink_to(hub / ".agent" / "skills" / "sip-x")
            register(hub, "proj", proj)
            r = run(str(hub))
            self.assertIn("em dia", r.stdout)
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_apply_runs_sync_check_reports_result(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, ["a"])
            proj = make_project(root, hub)
            register(hub, "proj", proj)
            r = run(str(hub), "--apply")
            self.assertRegex(r.stdout, r"sync_entrypoints: (ok|falhou)")
            self.assertNotIn("não verificado", r.stdout)

    def test_scan_lists_unregistered_consumers(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, ["a"])
            reg = make_project(root, hub, name="registrado")
            register(hub, "registrado", reg)
            make_project(root, hub, name="esquecido")
            r = run(str(hub), "--scan", str(root))
            self.assertIn("esquecido", r.stdout)
            self.assertRegex(r.stdout, r"consome o hub mas não está em instalacoes")
            self.assertNotRegex(r.stdout, r"registrado.*não está em instalacoes")

    def test_usage_errors(self):
        self.assertEqual(run().returncode, 2)
        self.assertEqual(run("/nao/existe/hub").returncode, 2)


def make_fichas(root: Path, *projects: Path, mothers: tuple = ()) -> Path:
    fichas = root / "fichas"
    fichas.mkdir()
    for p in projects:
        (fichas / f"{p.name}.md").write_text(
            f"# Ficha de Projeto: {p.name}\n\n> **Repositório / Caminho:** `{p}`\n", encoding="utf-8")
    if mothers:
        (fichas / "_pastas-mae.txt").write_text("# mães\n" + "\n".join(str(m) for m in mothers) + "\n", encoding="utf-8")
    return fichas


class CobrirTests(unittest.TestCase):
    def setup(self, root: Path):
        hub = make_hub(root, ["a"])
        reg = make_project(root, hub, name="registrado", seen="agents a; workflows nenhum", installed=TODAY)
        register(hub, "registrado", reg)
        new = root / "novo"
        (new / ".agent").mkdir(parents=True)
        mae = root / "mae"
        mae.mkdir()
        return hub, reg, new, mae

    def test_requires_fichas(self):
        with tempfile.TemporaryDirectory() as t:
            hub = make_hub(Path(t), ["a"])
            self.assertEqual(run(str(hub), "--cobrir").returncode, 2)

    def test_dry_run_changes_nothing_and_mother_is_excluded(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub, reg, new, mae = self.setup(root)
            fichas = make_fichas(root, new, mae, mothers=(mae,))
            before = snapshot(root)
            r = run(str(hub), "--cobrir", "--fichas", str(fichas))
            self.assertEqual(snapshot(root), before)
            self.assertIn("criaria link", r.stdout)
            self.assertNotIn("# mae", r.stdout)

    def test_apply_installs_resolver_only_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub, reg, new, mae = self.setup(root)
            fichas = make_fichas(root, new, mae, mothers=(mae,))
            run(str(hub), "--cobrir", "--fichas", str(fichas), "--apply")
            for base in (".agent", ".claude"):
                self.assertTrue((new / base / "skills" / "sip-x" / "SKILL.md").exists())
            gi = (new / ".gitignore").read_text(encoding="utf-8")
            self.assertIn(".agent/skills/sip-x", gi)
            self.assertIn(".claude/skills/sip-x", gi)
            man = (new / ".agent" / "SIPS-CONSUMIDOS.md").read_text(encoding="utf-8")
            self.assertIn("- Agents: nenhum", man)
            self.assertIn("agents a; workflows nenhum", man)
            self.assertTrue((hub / "instalacoes" / "novo.md").is_file())
            self.assertFalse((mae / ".agent").exists())
            snap = snapshot(root)
            r2 = run(str(hub), "--cobrir", "--fichas", str(fichas), "--apply")
            man2 = (new / ".agent" / "SIPS-CONSUMIDOS.md").read_text(encoding="utf-8")
            self.assertEqual(man2.count("## SIP - X"), 1)
            self.assertEqual((new / ".gitignore").read_text(encoding="utf-8").count(".agent/skills/sip-x"), 1)
            self.assertNotIn("criar link", r2.stdout)
            self.assertEqual(r2.returncode, 0, r2.stdout)

    def test_conflict_with_real_folder_is_not_touched(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub, reg, new, mae = self.setup(root)
            (new / ".claude" / "skills" / "sip-x").mkdir(parents=True)
            (new / ".claude" / "skills" / "sip-x" / "SKILL.md").write_text("meu", encoding="utf-8")
            fichas = make_fichas(root, new)
            r = run(str(hub), "--cobrir", "--fichas", str(fichas), "--apply")
            self.assertIn("conflito", r.stdout)
            self.assertEqual((new / ".claude" / "skills" / "sip-x" / "SKILL.md").read_text(encoding="utf-8"), "meu")
            self.assertFalse((new / ".agent" / "SIPS-CONSUMIDOS.md").exists())

    def test_old_format_entry_is_migrated(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, ["a", "b"])
            proj = make_project(root, hub, agents="core", seen="agents core; workflows core", installed=TODAY)
            register(hub, "proj", proj)
            fichas = make_fichas(root)
            dry = run(str(hub), "--cobrir", "--fichas", str(fichas))
            self.assertIn("migraria registro antigo", dry.stdout)
            self.assertIn("agents core", (proj / ".agent" / "SIPS-CONSUMIDOS.md").read_text(encoding="utf-8"))
            run(str(hub), "--cobrir", "--fichas", str(fichas), "--apply")
            man = (proj / ".agent" / "SIPS-CONSUMIDOS.md").read_text(encoding="utf-8")
            self.assertIn("- Agents: nenhum", man)
            self.assertIn("- Vistos no hub: agents a, b; workflows nenhum", man)
            self.assertEqual(list((proj / "inbox").glob("*.md")), [])

    def test_old_registry_format_and_missing_update_line(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, ["a"])
            good = make_project(root, hub, name="good", installed=TODAY)
            register(hub, "good", good)
            old = make_project(root, hub, name="velho", installed=TODAY)
            m = old / ".agent" / "SIPS-CONSUMIDOS.md"
            m.write_text("\n".join(l for l in m.read_text(encoding="utf-8").splitlines() if "Para atualizar" not in l) + "\n", encoding="utf-8")
            (hub / "instalacoes" / "velho.md").write_text(f"# Instalação: velho\n\n- Projeto: {old}\n- Hub: {hub}\n", encoding="utf-8")
            fichas = make_fichas(root)
            r = run(str(hub), "--cobrir", "--fichas", str(fichas), "--apply")
            self.assertIn("# velho", r.stdout)
            self.assertIn("- Para atualizar: cole de novo", m.read_text(encoding="utf-8"))

    def test_scan_adds_unregistered_consumer_and_registers_it(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root, ["a"])
            reg = make_project(root, hub, name="registrado", installed=TODAY)
            register(hub, "registrado", reg)
            esquecido = make_project(root, hub, name="esquecido", installed=TODAY)
            fichas = make_fichas(root)
            r = run(str(hub), "--cobrir", "--fichas", str(fichas), "--scan", str(root), "--apply")
            self.assertIn("# esquecido", r.stdout)
            self.assertTrue((hub / "instalacoes" / "esquecido.md").is_file())
            self.assertIn(str(esquecido), (hub / "instalacoes" / "esquecido.md").read_text(encoding="utf-8"))

    def test_ficha_path_with_trailing_text_and_raiz(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub, reg, new, mae = self.setup(root)
            fichas = root / "fichas"
            fichas.mkdir()
            (fichas / "novo.md").write_text(f"> **Repositório / Caminho:** `{new}` · [GitHub](https://x/y) (remoto)\n", encoding="utf-8")
            (fichas / "mae.md").write_text(f"> **Repositório / Caminho Raiz:** `{mae}`  \n", encoding="utf-8")
            (fichas / "_pastas-mae.txt").write_text(f"{mae}\n", encoding="utf-8")
            r = run(str(hub), "--cobrir", "--fichas", str(fichas))
            self.assertIn("# novo", r.stdout)
            self.assertNotIn("# mae", r.stdout)


class TodosTests(unittest.TestCase):
    def test_runs_each_hub_in_the_table_and_summarises(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub1 = make_hub(root / "a", ["a"])
            p1 = make_project(root / "a", hub1, installed=TODAY)
            register(hub1, "proj", p1)
            hub2 = make_hub(root / "b", ["a"])
            p2 = make_project(root / "b", hub2, installed=TODAY)
            register(hub2, "proj", p2)
            kit = root / "kit"
            (kit / "projetos").mkdir(parents=True)
            sips = kit / "projetos" / "_sips.md"
            sips.write_text(
                "| Domínio | Nome | Hub | Skill |\n| :-- | :-- | :-- | :-- |\n"
                f"| `x` | SIP - X | `{hub1}` | `sip-x` |\n| `y` | SIP - Y | `{hub2}` | `sip-x` |\n", encoding="utf-8")
            r = run("--todos", "--sips", str(sips), "--kit", str(kit))
            self.assertIn("== Todos os hubs ==", r.stdout)
            self.assertEqual(r.stdout.count("Resumo:"), 4)  # 2 hubs, each printed in its own run and in the table
            self.assertIn("[ok] hub:", r.stdout)

    def test_missing_table_is_usage_error(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(run("--todos", "--sips", str(Path(t) / "nao.md")).returncode, 2)


if __name__ == "__main__":
    unittest.main()
