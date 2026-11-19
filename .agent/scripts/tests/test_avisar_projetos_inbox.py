"""Tests for avisar_projetos_inbox.py (one inbox note, from any template, in every consumer project).

Run from the 0 Padrões root: python3 -m unittest discover -s .agent/scripts/tests
Everything happens in a temp folder: a fake hub with `instalacoes/` and fake projects.
"""

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))

import avisar_projetos_inbox as ar  # noqa: E402


def registry_file(hub: Path, name: str, project: Path) -> None:
    folder = hub / "instalacoes"
    folder.mkdir(exist_ok=True)
    (folder / f"{name}.md").write_text(f"## Projeto\n{name}\n\n## Caminho absoluto\n{project}\n", encoding="utf-8")


SLUG = "assunto-qualquer"
TEMPLATE = "# {num} — Aviso\nStatus: na inbox · Aberto em: {data} · Projeto de origem: {projeto} (kit: {hub})\n\n## O quê\nTexto com chaves {soltas} que ficam.\n"


class Notes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.hub = root / "hub"
        self.hub.mkdir()
        self.proj = root / "proj"
        (self.proj / "inbox" / "arquivo").mkdir(parents=True)
        (self.proj / "inbox" / "007-algo.md").write_text("x\n", encoding="utf-8")
        registry_file(self.hub, "proj", self.proj)
        registry_file(self.hub, "sumiu", root / "nao-existe")
        registry_file(self.hub, "hub", self.hub)

    def test_simulation_writes_nothing(self):
        rows = ar.run(self.hub, TEMPLATE, SLUG, apply=False, today="2026-11-19")
        self.assertEqual(list((self.proj / "inbox").glob("*assunto-qualquer*")), [])
        actions = {name: action for name, _, action in rows}
        self.assertTrue(actions["proj"].startswith("criar: inbox/GERAL-001-"))
        self.assertEqual(actions["sumiu"], "pasta não encontrada")
        self.assertTrue(actions["hub"].startswith("ignorado"))

    def test_apply_fills_the_markers_and_keeps_other_braces(self):
        ar.run(self.hub, TEMPLATE, SLUG, apply=True, today="2026-11-19")
        text = (self.proj / "inbox" / f"GERAL-001-{SLUG}.md").read_text(encoding="utf-8")
        self.assertIn("# GERAL-001 — Aviso", text)
        self.assertIn("Aberto em: 2026-11-19 · Projeto de origem: proj (kit: " + str(self.hub) + ")", text)
        self.assertIn("{soltas}", text)

    def test_the_shipped_template_has_every_field_of_the_inbox_format(self):
        shipped = (ar.KIT / "prompts-template" / "inbox-notas" / "regras-do-kit-busca-no-sip-e-disciplina-de-mudanca.md").read_text(encoding="utf-8")
        for heading in ("## O quê", "## Como", "## Onde", "## Por quê", "## Para quê", "## Quem", "## Efeitos e impactos",
                        "## Exemplos", "## Gatilho para sair da inbox", "## Enquanto isso"):
            self.assertIn(heading, shipped)
        for marker in ("{num}", "{data}", "{projeto}", "{hub}"):
            self.assertIn(marker, shipped)

    def test_main_refuses_missing_arguments_and_bad_slugs(self):
        self.assertEqual(ar.main([]), 2)
        self.assertEqual(ar.main(["--nota", "x.md", "--slug", "Ruim Slug"]), 2)
        self.assertEqual(ar.main(["--nota", "/nao/existe.md", "--slug", "ok"]), 2)

    def test_rerun_rewrites_in_place_without_piling_up(self):
        ar.run(self.hub, TEMPLATE, SLUG, apply=True, today="2026-11-19")
        rows = ar.run(self.hub, TEMPLATE, SLUG, apply=True, today="2026-11-20")
        self.assertEqual(len(list((self.proj / "inbox").glob("*assunto-qualquer*"))), 1)
        self.assertTrue(dict((n, a) for n, _, a in rows)["proj"].startswith("atualizar"))

    def test_geral_sequence_is_its_own_and_counts_the_archive(self):
        (self.proj / "inbox" / "arquivo" / "GERAL-006-outro.md").write_text("x\n", encoding="utf-8")
        ar.run(self.hub, TEMPLATE, SLUG, apply=True, today="2026-11-19")
        self.assertTrue((self.proj / "inbox" / f"GERAL-007-{SLUG}.md").is_file())

    def test_an_old_numbered_note_of_the_slug_is_rewritten_in_place(self):
        old = self.proj / "inbox" / f"008-{SLUG}.md"
        old.write_text("antiga\n", encoding="utf-8")
        rows = ar.run(self.hub, TEMPLATE, SLUG, apply=True, today="2026-11-19")
        self.assertTrue(dict((n, a) for n, _, a in rows)["proj"].startswith(f"atualizar: inbox/008-{SLUG}"))
        self.assertEqual(list((self.proj / "inbox").glob("GERAL-*")), [])

    def test_a_note_already_archived_is_not_recreated(self):
        (self.proj / "inbox" / "arquivo" / f"003-{SLUG}.md").write_text("resolvido\n", encoding="utf-8")
        rows = ar.run(self.hub, TEMPLATE, SLUG, apply=True, today="2026-11-19")
        self.assertTrue(dict((n, a) for n, _, a in rows)["proj"].startswith("já resolvido"))
        self.assertEqual(list((self.proj / "inbox").glob(f"*{SLUG}.md")), [])

    def test_nothing_else_in_the_project_is_touched(self):
        before = sorted(p.name for p in self.proj.rglob("*"))
        ar.run(self.hub, TEMPLATE, SLUG, apply=True, today="2026-11-19")
        after = sorted(p.name for p in self.proj.rglob("*"))
        self.assertEqual(set(after) - set(before), {f"GERAL-001-{SLUG}.md"})


if __name__ == "__main__":
    unittest.main()
