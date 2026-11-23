"""Tests for the resolver layout: `<hub>/prompts/resolver/<sip>` (new) and `<hub>/.agents/skills/<sip>` (legacy).

Covers linkutil.resolver_dir, the two-level mode of build_sip_index.py (`indice` region + verticais.json),
sips_status.py, propagar_sip.py, sync_entrypoints.py (stub link of 0 Padrões) and check_sip_hub.py.
Run from the 0 Padrões root: python3 -m unittest discover -s .agents/scripts/tests
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))
import linkutil  # noqa: E402

INDEXER = SCRIPTS / "build_sip_index.py"
STATUS = SCRIPTS / "sips_status.py"
PROPAGAR = SCRIPTS / "propagar_sip.py"
ENTRYPOINTS = SCRIPTS / "sync_entrypoints.py"
CHECK_HUB = SCRIPTS / "check_sip_hub.py"

_spec = importlib.util.spec_from_file_location("build_sip_index", INDEXER)
bsi = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bsi)

GEN = "(gerado por .agents/scripts/build_sip_index.py — não edite à mão)"


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def item(description: str) -> str:
    return f"---\nname: x\ndescription: {description}\n---\n"


def resolver_text(two_level: bool) -> str:
    body = (f"<!-- indice:start dir=verticais {GEN} -->\n<!-- indice:end -->\n" if two_level else
            "".join(f"<!-- {k}:start {GEN} -->\n<!-- {k}:end -->\n" for k in ("skills", "agents", "workflows")))
    return "# sip-t\n\n- Última atualização do hub: 2026-11-18\n\n" + body


VERTICAIS = {"padrao": "outros", "verticais": [
    {"nome": "copy", "quando": "Texto que converte.", "match": ["copy-*"]},
    {"nome": "seo", "quando": "Busca orgânica.", "match": ["seo-*"]},
    {"nome": "outros", "quando": "O que não coube em outra vertical.", "match": []},
]}


def make_hub(root: Path, new_layout: bool = True, two_level: bool = True) -> Path:
    hub = root / "hub"
    base = hub / "prompts" / "resolver" / "sip-t" if new_layout else hub / ".agents" / "skills" / "sip-t"
    write(base / "SKILL.md", resolver_text(two_level))
    if two_level:
        write(base / "verticais.json", json.dumps(VERTICAIS))
    write(hub / ".agents/skills/copy-um/SKILL.md", item("Use quando copy um."))
    write(hub / ".agents/skills/seo-um/SKILL.md", item("Use quando seo um."))
    write(hub / ".agents/skills/livre-um/SKILL.md", item("Use quando livre."))
    write(hub / ".agents/agents/copy-redator.md", item("Use quando redigir."))
    write(hub / ".agents/workflows/seo-auditar.md", item("Use quando auditar."))
    write(hub / "instalacoes/README.md", "# r\n")
    return hub


def run(script: Path, *args: str, cwd=None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, timeout=120, cwd=cwd)


class ResolverDirHelper(unittest.TestCase):
    def test_new_layout_wins(self):
        with tempfile.TemporaryDirectory() as t:
            hub = make_hub(Path(t))
            self.assertEqual(linkutil.resolver_dir(hub, "sip-t"), hub / "prompts" / "resolver" / "sip-t")

    def test_legacy_layout_is_the_fallback(self):
        with tempfile.TemporaryDirectory() as t:
            hub = make_hub(Path(t), new_layout=False, two_level=False)
            self.assertEqual(linkutil.resolver_dir(hub, "sip-t"), hub / ".agents" / "skills" / "sip-t")

    def test_indexer_and_check_hub_agree_with_linkutil(self):
        with tempfile.TemporaryDirectory() as t:
            for new in (True, False):
                hub = make_hub(Path(t) / str(new), new_layout=new, two_level=False)
                self.assertEqual(bsi.resolver_dir(hub, "sip-t"), linkutil.resolver_dir(hub, "sip-t"))


class TwoLevelIndex(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.hub = make_hub(Path(self._t.name))
        self.resolver = self.hub / "prompts" / "resolver" / "sip-t"

    def tearDown(self):
        self._t.cleanup()

    def build(self, *extra):
        return run(INDEXER, "--hub", str(self.hub), *extra)

    def test_default_resolver_is_found_in_the_new_layout(self):
        self.assertEqual(self.build().returncode, 0)
        self.assertTrue((self.resolver / "verticais" / "copy.md").is_file())

    def test_every_item_lands_in_exactly_one_vertical_file(self):
        self.build()
        text = {p.name: p.read_text(encoding="utf-8") for p in (self.resolver / "verticais").glob("*.md")}
        self.assertEqual(sorted(text), ["copy.md", "outros.md", "seo.md"])
        for needle, home in (("`copy-um`", "copy.md"), ("`copy-redator`", "copy.md"), ("`seo-um`", "seo.md"),
                             ("`/seo-auditar`", "seo.md"), ("`livre-um`", "outros.md")):
            self.assertEqual([n for n, body in text.items() if needle in body], [home], needle)

    def test_summary_table_in_skill_md_counts_per_vertical(self):
        self.build()
        body = (self.resolver / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Total: 3 skills, 1 agents, 1 workflows.", body)
        self.assertIn("| `copy` | Texto que converte. | 1 | 1 | 0 | `verticais/copy.md` |", body)

    def test_second_run_changes_nothing_and_check_is_fresh(self):
        self.build()
        self.assertEqual(self.build("--check").returncode, 0)
        self.assertIn("Sem mudanças", self.build().stdout)

    def test_check_goes_stale_when_a_skill_appears_and_writes_nothing(self):
        self.build()
        write(self.hub / ".agents/skills/copy-dois/SKILL.md", item("Use quando copy dois."))
        before = (self.resolver / "verticais" / "copy.md").read_text(encoding="utf-8")
        result = self.build("--check")
        self.assertEqual(result.returncode, 1)
        self.assertEqual((self.resolver / "verticais" / "copy.md").read_text(encoding="utf-8"), before)

    def test_vertical_without_quando_is_an_error(self):
        data = json.loads((self.resolver / "verticais.json").read_text(encoding="utf-8"))
        data["verticais"][0]["quando"] = " "
        (self.resolver / "verticais.json").write_text(json.dumps(data), encoding="utf-8")
        result = self.build("--check")
        self.assertEqual(result.returncode, 2)
        self.assertIn("quando", result.stderr)

    def test_item_without_vertical_and_without_padrao_is_an_error(self):
        data = json.loads((self.resolver / "verticais.json").read_text(encoding="utf-8"))
        data.pop("padrao")
        data["verticais"] = data["verticais"][:2]
        (self.resolver / "verticais.json").write_text(json.dumps(data), encoding="utf-8")
        result = self.build("--check")
        self.assertEqual(result.returncode, 2)
        self.assertIn("livre-um", result.stderr)

    def test_missing_verticais_json_is_an_error(self):
        (self.resolver / "verticais.json").unlink()
        self.assertEqual(self.build("--check").returncode, 2)

    def test_stale_generated_vertical_file_is_removed(self):
        self.build()
        (self.hub / ".agents/skills/seo-um/SKILL.md").unlink()
        (self.hub / ".agents/skills/seo-um").rmdir()
        (self.hub / ".agents/workflows/seo-auditar.md").unlink()
        self.assertEqual(self.build("--check").returncode, 1)
        self.build()
        self.assertFalse((self.resolver / "verticais" / "seo.md").exists())

    def test_hand_written_file_in_the_folder_is_never_removed(self):
        self.build()
        mine = write(self.resolver / "verticais" / "notas.md", "# minhas notas\n")
        self.build()
        self.assertTrue(mine.is_file())

    def test_legacy_three_regions_still_work(self):
        with tempfile.TemporaryDirectory() as t:
            hub = make_hub(Path(t), new_layout=False, two_level=False)
            self.assertEqual(run(INDEXER, "--hub", str(hub)).returncode, 0)
            body = (hub / ".agents/skills/sip-t/SKILL.md").read_text(encoding="utf-8")
            self.assertIn("`copy-um`", body)
            self.assertEqual(run(INDEXER, "--hub", str(hub), "--check").returncode, 0)


def manifest(hub: Path, installed: str = "2026-11-18") -> str:
    return (f"# SIPs consumidos\n\n## SIP - T (`sip-t`)\n- Hub: {hub}\n- Instalado/atualizado em: {installed}\n"
            f"- Skill: sip-t\n- Agents: nenhum\n- Workflows: nenhum\n- Vistos no hub: agents copy-redator; workflows seo-auditar\n"
            f"- Conflitos: nenhum\n- Para atualizar: cole de novo \"{hub}/prompts/i.md\"\n")


def make_project(root: Path, hub: Path, target: Path | None) -> Path:
    proj = root / "proj"
    write(proj / ".agents" / "SIPS-CONSUMIDOS.md", manifest(hub))
    (proj / "inbox").mkdir()
    for base in (".agents", ".claude"):
        (proj / base / "skills").mkdir(parents=True)
    if target is not None:
        (proj / ".agents" / "skills" / "sip-t").symlink_to(target)
        (proj / ".claude" / "skills" / "sip-t").symlink_to("../../.agents/skills/sip-t")
    return proj


class StatusAndPropagation(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.root = Path(self._t.name)

    def tearDown(self):
        self._t.cleanup()

    def register(self, hub: Path, proj: Path):
        write(hub / "instalacoes" / "proj.md",
              f"## Projeto\nproj\n\n## Caminho absoluto\n{proj}\n\n## Instalado em\n2026-11-18\n\n"
              "## Última atualização\n2026-11-18\n\n## Recursos instalados\n- Skill: sip-t (sempre)\n")

    def test_status_is_up_to_date_for_a_project_linked_to_the_new_layout(self):
        hub = make_hub(self.root)
        proj = make_project(self.root, hub, hub / "prompts" / "resolver" / "sip-t")
        result = run(STATUS, str(proj))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("resolver não existe no hub", result.stdout)

    def test_status_reads_the_hub_date_from_the_legacy_layout_too(self):
        hub = make_hub(self.root, new_layout=False, two_level=False)
        proj = make_project(self.root, hub, hub / ".agents" / "skills" / "sip-t")
        result = run(STATUS, str(proj))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_status_flags_a_link_left_on_the_old_path_after_the_move(self):
        hub = make_hub(self.root)
        proj = make_project(self.root, hub, hub / ".agents" / "skills" / "sip-t")  # old path: no longer exists
        result = run(STATUS, str(proj))
        self.assertEqual(result.returncode, 1)
        self.assertIn("link quebrado", result.stdout)

    def test_propagar_apply_repoints_a_broken_link_to_the_new_layout(self):
        hub = make_hub(self.root)
        proj = make_project(self.root, hub, hub / ".agents" / "skills" / "sip-t")
        self.register(hub, proj)
        result = run(PROPAGAR, str(hub), "--apply")
        self.assertIn("sip-t", result.stdout + result.stderr)
        link = proj / ".agents" / "skills" / "sip-t"
        self.assertTrue(link.is_symlink())
        self.assertEqual(Path(os.readlink(link)), hub / "prompts" / "resolver" / "sip-t")
        self.assertTrue((proj / ".claude" / "skills" / "sip-t" / "SKILL.md").is_file())

    def test_status_flags_a_link_that_points_to_the_hub_root_instead_of_the_resolver(self):
        hub = make_hub(self.root)
        proj = make_project(self.root, hub, hub)  # lands inside the hub, but not on the resolver folder
        result = run(STATUS, str(proj))
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("aponta para outro lugar do hub", result.stdout)

    def test_propagar_apply_repoints_a_link_that_points_to_the_hub_root(self):
        hub = make_hub(self.root)
        proj = make_project(self.root, hub, hub)
        self.register(hub, proj)
        run(PROPAGAR, str(hub), "--apply")
        link = proj / ".agents" / "skills" / "sip-t"
        self.assertEqual(Path(os.readlink(link)), hub / "prompts" / "resolver" / "sip-t")
        self.assertTrue((proj / ".claude" / "skills" / "sip-t" / "SKILL.md").is_file())

    def test_propagar_with_a_relative_hub_path_still_writes_absolute_link_targets(self):
        hub = make_hub(self.root)
        proj = make_project(self.root, hub, hub / ".agents" / "skills" / "sip-t")
        self.register(hub, proj)
        run(PROPAGAR, "hub", "--apply", cwd=self.root)  # relative to the working directory
        link = proj / ".agents" / "skills" / "sip-t"
        target = Path(os.readlink(link))
        self.assertTrue(target.is_absolute(), target)
        self.assertEqual(target.resolve(), (hub / "prompts" / "resolver" / "sip-t").resolve())  # /var vs /private/var on macOS
        self.assertTrue((link / "SKILL.md").is_file())

    def test_propagar_simulation_writes_nothing(self):
        hub = make_hub(self.root)
        proj = make_project(self.root, hub, hub / ".agents" / "skills" / "sip-t")
        self.register(hub, proj)
        run(PROPAGAR, str(hub))
        self.assertEqual(Path(os.readlink(proj / ".agents" / "skills" / "sip-t")), hub / ".agents" / "skills" / "sip-t")

    def test_propagar_never_replaces_a_real_folder(self):
        hub = make_hub(self.root)
        proj = make_project(self.root, hub, None)
        write(proj / ".agents" / "skills" / "sip-t" / "SKILL.md", "stub real\n")
        self.register(hub, proj)
        run(PROPAGAR, str(hub), "--apply")
        self.assertFalse((proj / ".agents" / "skills" / "sip-t").is_symlink())
        self.assertEqual((proj / ".agents" / "skills" / "sip-t" / "SKILL.md").read_text(encoding="utf-8"), "stub real\n")


class StubLinkOf0Padroes(unittest.TestCase):
    def test_claude_link_straight_to_the_new_resolver_folder_passes_sync_check(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = make_hub(root)
            proj = root / "project"
            write(proj / ".agents/skills/sip-t/SKILL.md", item("stub local"))  # the 0 Padrões stub
            write(proj / ".agents/skills/local-skill/SKILL.md", item("Use quando local."))
            (proj / ".claude" / "skills").mkdir(parents=True)
            (proj / ".claude/skills/local-skill").symlink_to("../../.agents/skills/local-skill")
            (proj / ".claude/skills/sip-t").symlink_to(hub / "prompts" / "resolver" / "sip-t")
            result = run(ENTRYPOINTS, "--check", cwd=proj)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_link_to_a_folder_that_is_not_a_resolver_still_fails(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            proj = root / "project"
            write(proj / ".agents/skills/sip-t/SKILL.md", item("stub local"))
            target = write(root / "hub" / "qualquer" / "sip-t" / "SKILL.md", item("x")).parent
            (proj / ".claude" / "skills").mkdir(parents=True)
            (proj / ".claude/skills/sip-t").symlink_to(target)
            self.assertEqual(run(ENTRYPOINTS, "--check", cwd=proj).returncode, 1)


class CheckHub(unittest.TestCase):
    def test_check_hub_fails_when_a_copy_of_the_resolver_is_left_in_the_hub_skills(self):
        with tempfile.TemporaryDirectory() as t:
            hub = make_hub(Path(t))
            run(INDEXER, "--hub", str(hub))
            write(hub / ".agents/skills/sip-t/SKILL.md", item("copia esquecida"))
            out = run(CHECK_HUB, str(hub), "sip-t").stdout
            self.assertIn("FAIL  resolver (new layout): no copy or link left", out)

    def test_check_hub_fails_when_the_new_layout_resolver_is_too_big(self):
        with tempfile.TemporaryDirectory() as t:
            hub = make_hub(Path(t))
            run(INDEXER, "--hub", str(hub))
            skill_md = hub / "prompts" / "resolver" / "sip-t" / "SKILL.md"
            skill_md.write_text(skill_md.read_text(encoding="utf-8") + "linha\n" * 130, encoding="utf-8")
            out = run(CHECK_HUB, str(hub), "sip-t").stdout
            self.assertIn("FAIL  resolver (new layout): small enough", out)

    def test_legacy_layout_is_not_held_to_the_size_limit(self):
        with tempfile.TemporaryDirectory() as t:
            hub = make_hub(Path(t), new_layout=False, two_level=False)
            run(INDEXER, "--hub", str(hub))
            skill_md = hub / ".agents" / "skills" / "sip-t" / "SKILL.md"
            skill_md.write_text(skill_md.read_text(encoding="utf-8") + "linha\n" * 300, encoding="utf-8")
            out = run(CHECK_HUB, str(hub), "sip-t").stdout
            self.assertIn("PASS  resolver (new layout): small enough", out)

    def test_check_hub_finds_the_resolver_in_the_new_layout_and_accepts_the_index_region(self):
        with tempfile.TemporaryDirectory() as t:
            hub = make_hub(Path(t))
            run(INDEXER, "--hub", str(hub))
            out = run(CHECK_HUB, str(hub), "sip-t").stdout
            self.assertIn("PASS  resolver exists", out)
            self.assertIn("PASS  resolver: regions for skills, agents and workflows (or the `indice` region)", out)
            self.assertIn("PASS  resolver: tables up to date", out)


if __name__ == "__main__":
    unittest.main()
