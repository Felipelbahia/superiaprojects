"""Tests for deliverable-verification: the fixture passes, and every planted error fails its own check.

Run: python3 -I -m unittest discover -s "<skill>/tests" -v
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import build  # noqa: E402
import next_id  # noqa: E402
import verify  # noqa: E402
from common import load_config  # noqa: E402


class FixtureCase(unittest.TestCase):
    """Each test gets a fresh copy of tests/fixture with a freshly built document."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "project"
        shutil.copytree(HERE / "fixture", self.root)
        self.config = self.root / "verification.json"
        cfg = load_config(self.config)
        (self.root / cfg["document"]["output"]).write_text(build.build(cfg), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def edit(self, rel, old, new):
        path = self.root / rel
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, f"fixture changed: '{old}' not in {rel}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def append(self, rel, text):
        with open(self.root / rel, "a", encoding="utf-8") as handle:
            handle.write(text)

    def results(self):
        return {key: (ok, note) for key, ok, note in verify.run(load_config(self.config))}

    def assertFails(self, check, evidence_part=""):
        ok, note = self.results()[check]
        self.assertFalse(ok, f"{check} should FAIL, got OK: {note}")
        self.assertIn(evidence_part, note)


class TestFixturePasses(FixtureCase):
    def test_all_checks_ok(self):
        results = self.results()
        self.assertEqual(len(results), 11)
        self.assertTrue(all(ok for ok, _ in results.values()), results)

    def test_cli_exit_codes(self):
        cmd = [sys.executable, "-I", str(SCRIPTS / "verify.py"), "--config", str(self.config)]
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
        self.append("partes/01-feed.md", "\nVer A-999.\n")
        run = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(run.returncode, 1)
        self.assertIn("| FAIL |", run.stdout)


class TestPlantedErrors(FixtureCase):
    def test_registries_duplicated_id(self):
        self.append("achados.md", "| A-003 | Logout sem motivo (duplicado) |\n")
        self.assertFails("registries", "A-003")

    def test_counts_wrong_number(self):
        self.edit("partes/00-resumo.md", "**3 achados**", "**4 achados**")
        self.assertFails("counts", "4 achados")

    def test_counts_rows_not_ids(self):
        # a row with a non-numeric id ('2b') still counts: rows, not ids
        self.append("backlog.csv", "2b;Evento extra;Engenharia\n")
        self.assertFails("counts", "backlog: 3")

    def test_references_unknown_id(self):
        self.append("partes/01-feed.md", "\nVer também A-009.\n")
        self.assertFails("references", "A-009")

    def test_index_cites_missing_file(self):
        self.append("00-INDEX.md", "\nNova parte: `partes/09-paywall.md`.\n")
        self.assertFails("index", "partes/09-paywall.md")

    def test_index_misses_new_part(self):
        (self.root / "partes/03-paywall.md").write_text("# Paywall\n", encoding="utf-8")
        self.assertFails("index", "partes/03-paywall.md")

    def test_document_edited_by_hand(self):
        self.append("DIAGNOSTICO.md", "\nLinha escrita à mão.\n")
        self.assertFails("document", "stale")

    def test_document_part_changed_without_rebuild(self):
        self.append("partes/02-conta.md", "\nParágrafo novo.\n")
        self.assertFails("document", "stale")

    def test_document_missing_section(self):
        self.edit("verification.json", '"partes/02-conta.md", "achados.md"', '"partes/02-conta.md", "partes/03-sumiu.md", "achados.md"')
        self.assertFails("document", "partes/03-sumiu.md")

    def test_source_not_cited(self):
        (self.root / "fontes/telas/paywall-01.png").write_bytes(b"")
        self.assertFails("source_coverage", "paywall-01.png")

    def test_forbidden_default_pattern(self):
        self.append("partes/02-conta.md", "\nCPF de teste 123.456.789-00.\n")
        self.assertFails("forbidden", "CPF")

    def test_forbidden_project_pattern_and_allow(self):
        self.append("partes/02-conta.md", "\nServidor em api.interno.local.\n")
        self.assertFails("forbidden", "internal host")
        self.edit("verification.json", '"allow": []', '"allow": ["interno\\\\.local"]')
        self.assertTrue(self.results()["forbidden"][0])

    def test_required_mention_missing(self):
        self.append("achados.md", "| A-004 | Paywall sem plano |\n")
        self.assertFails("required_mentions", "A-004")

    def test_loop_counter_gap(self):
        (self.root / "loop/02 Plan.md").unlink()
        self.assertFails("loop_counter", "gaps [2]")

    def test_loop_counter_repeated(self):
        (self.root / "loop/03 Outra Execução.md").write_text("# x\n", encoding="utf-8")
        self.assertFails("loop_counter", "repeated [3]")

    def test_unique_column_repeated(self):
        self.append("catalogo.csv", "feed_scrolled;evento\n")
        self.assertFails("unique_columns", "feed_scrolled")

    def test_custom_check_fails(self):
        self.append("catalogo.csv", "ProfileOpened;evento\n")
        self.assertFails("custom:catalog_events_snake_case", "ProfileOpened")

    def test_custom_check_crash_is_a_failure(self):
        self.append("verification_custom.py", "\n\ndef check_broken(ctx):\n    raise ValueError('boom')\n")
        self.assertFails("custom:broken", "crashed")


class TestCycle2Fixes(FixtureCase):
    def test_date_changed_inside_a_part_is_stale(self):
        self.append("partes/01-feed.md", "\nMedido em 2026-01-01.\n")
        cfg = load_config(self.config)
        (self.root / "DIAGNOSTICO.md").write_text(build.build(cfg), encoding="utf-8")
        self.edit("partes/01-feed.md", "2026-01-01", "2026-02-02")
        self.assertFails("document", "stale")

    def test_generated_file_cannot_satisfy_mentions_or_coverage(self):
        self.edit("verification.json", '"files": ["partes/00-resumo.md"]}]', '"files": ["partes/00-resumo.md", "DIAGNOSTICO.md"]}]')
        self.edit("verification.json", '"cited_in": ["partes/*.md"]', '"cited_in": ["partes/*.md", "DIAGNOSTICO.md"]')
        self.edit("partes/00-resumo.md", "A-002 e A-003", "A-002")
        self.edit("partes/02-conta.md", "`conta-01.png`", "a tela de conta")
        results = self.results()
        self.assertFalse(results["required_mentions"][0], results["required_mentions"])
        self.assertFalse(results["source_coverage"][0], results["source_coverage"])

    def test_missing_registry_file_is_a_fail_row(self):
        (self.root / "backlog.csv").unlink()
        results = self.results()
        self.assertFalse(results["registries"][0])
        self.assertIn("not run: counts, references, required_mentions", results["registries"][1])
        self.assertTrue(results["loop_counter"][0], "the other checks still run")

    def test_broken_custom_module_is_a_fail_row(self):
        self.append("verification_custom.py", "\ndef broken(:\n")
        results = self.results()
        self.assertFalse(results["custom:load"][0])
        self.assertTrue(results["loop_counter"][0])

    def test_uppercase_email_is_forbidden(self):
        self.append("partes/02-conta.md", "\nContato: Joao@Example.COM\n")
        self.assertFails("forbidden", "e-mail")

    def test_tilde_fences_are_not_demoted(self):
        self.assertEqual(build.demote("~~~\n# code\n~~~\n# T"), "~~~\n# code\n~~~\n## T")

    def test_ragged_csv_row_fails(self):
        self.append("backlog.csv", "3;Linha sem dono\n")
        self.assertFails("registries", "2 columns (header: 3)")


class TestCycle3Fixes(FixtureCase):
    def test_nested_fences(self):
        text = "~~~\n```\n# inside tilde\n~~~\n# after\n````\n```\n# inside\n```\n````\n# end"
        expected = "~~~\n```\n# inside tilde\n~~~\n## after\n````\n```\n# inside\n```\n````\n## end"
        self.assertEqual(build.demote(text), expected)

    def test_sys_exit_in_custom_module_is_a_fail_row(self):
        self.append("verification_custom.py", "\nimport sys\nsys.exit(0)\n")
        self.assertFails("custom:load", "SystemExit")

    def test_sys_exit_in_custom_check_is_a_fail_row(self):
        self.append("verification_custom.py", "\n\ndef check_quit(ctx):\n    raise SystemExit(0)\n")
        self.assertFails("custom:quit", "crashed")

    def test_generated_output_path_is_normalized(self):
        self.edit("verification.json", '"output": "DIAGNOSTICO.md"', '"output": "./DIAGNOSTICO.md"')
        self.edit("verification.json", '"files": ["partes/00-resumo.md"]}]', '"files": ["partes/00-resumo.md", "DIAGNOSTICO.md"]}]')
        self.edit("partes/00-resumo.md", "A-002 e A-003", "A-002")
        self.assertFails("required_mentions", "A-003")

    def test_email_in_csv_section_is_forbidden(self):
        self.append("backlog.csv", "3;Avisar ana@empresa.com;Produto\n")
        self.assertFails("forbidden", "backlog.csv: e-mail")


    def test_output_name_with_brackets_is_excluded(self):
        self.edit("verification.json", '"output": "DIAGNOSTICO.md"', '"output": "Relatorio [final].md"')
        self.edit("verification.json", '"files": ["partes/00-resumo.md"]}]', '"files": ["partes/00-resumo.md", "Relatorio*.md"]}]')
        (self.root / "DIAGNOSTICO.md").unlink()  # old output name: it would satisfy the mention on its own
        cfg = load_config(self.config)
        (self.root / "Relatorio [final].md").write_text(build.build(cfg), encoding="utf-8")
        self.edit("partes/00-resumo.md", "A-002 e A-003", "A-002")
        self.assertFails("required_mentions", "A-003")

    def test_fence_indented_four_spaces_is_not_a_fence(self):
        self.assertEqual(build.demote("    ```\n# h"), "    ```\n## h")


class TestBuild(FixtureCase):
    def test_demote_skips_fenced_code(self):
        text = build.demote("# Title\n```\n# not a heading\n```\n## Sub")
        self.assertEqual(text, "## Title\n```\n# not a heading\n```\n### Sub")

    def test_document_has_notice_and_csv_table(self):
        doc = build.build(load_config(self.config), today=date(2026, 1, 2))
        self.assertIn("2026-01-02", doc.splitlines()[2])
        self.assertIn("| id | item | dono |", doc)
        self.assertIn("## Backlog", doc)

    def test_check_flag_exit_codes(self):
        cmd = [sys.executable, "-I", str(SCRIPTS / "build.py"), "--config", str(self.config), "--check"]
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
        self.append("DIAGNOSTICO.md", "\nmanual\n")
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)


class TestNextId(unittest.TestCase):
    def test_per_prefix_and_padding(self):
        ids = ["A-001", "A-009", "Q-X13", "P-E2", "2b", "D-010"]
        self.assertEqual(next_id.next_ids(ids), {"A-": "A-010", "D-": "D-011", "P-E": "P-E3", "Q-X": "Q-X14"})

    def test_cli_on_fixture(self):
        cmd = [sys.executable, "-I", str(SCRIPTS / "next_id.py"), "--config", str(HERE / "fixture" / "verification.json")]
        out = subprocess.run(cmd, capture_output=True, text=True).stdout
        self.assertIn("achados: 3 rows -> next A-004", out)
        self.assertIn("backlog: 2 rows -> next 3", out)


if __name__ == "__main__":
    unittest.main()
