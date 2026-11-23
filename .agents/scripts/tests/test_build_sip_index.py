"""Tests for build_sip_index.py: parser and cleaning as pure functions, the CLI over a temp hub via subprocess."""

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "build_sip_index.py"
_spec = importlib.util.spec_from_file_location("build_sip_index", SCRIPT)
bsi = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bsi)

GEN = "(gerado por .agents/scripts/build_sip_index.py — não edite à mão)"


def desc_of(frontmatter: str) -> str:
    return bsi.clean_description(bsi.parse_description(frontmatter))


def skill_file(description: str) -> str:
    return f"---\nname: x\ndescription: {description}\n---\n\n# Corpo\n"


def start_line(kind: str, opt: str = "") -> str:
    return f"<!-- {kind}:start {opt}{GEN} -->"


def resolver_text(kinds=("skills", "agents", "workflows"), opts=None) -> str:
    opts = opts or {}
    parts = ["# Sip Teste", "", "Texto livre fora das regiões.", ""]
    for kind in kinds:
        parts += [f"## {kind.title()}", start_line(kind, opts.get(kind, "")), f"<!-- {kind}:end -->", ""]
    return "\n".join(parts)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_hub(root: Path) -> Path:
    """A hub with one item of each kind plus one item of every excluded kind; `fora/` lies outside the hub."""
    hub = root / "hub"
    outside = root / "fora"
    write(hub / ".agents/skills/sip-teste/SKILL.md", resolver_text())
    write(hub / ".agents/skills/alpha-um/SKILL.md", skill_file("Use quando A1."))
    write(hub / ".agents/skills/alpha-dois/SKILL.md", skill_file("Use quando A2."))
    write(hub / ".agents/skills/beta-tres/SKILL.md", skill_file("Use quando B. NÃO use para Z."))
    write(hub / ".agents/skills/_rascunho/SKILL.md", skill_file("Use quando RASCUNHO."))
    write(hub / ".agents/skills/.oculta/SKILL.md", skill_file("Use quando OCULTA."))
    write(outside / "skill-externa/SKILL.md", skill_file("Use quando EXTERNA."))
    os.symlink(outside / "skill-externa", hub / ".agents/skills/externa")
    write(hub / ".agents/agents/ag-um.md", skill_file("Use quando agente um."))
    write(hub / ".agents/agents/README.md", skill_file("Use quando README."))
    write(hub / ".agents/agents/_rascunho.md", skill_file("Use quando RASCUNHO AG."))
    write(hub / ".agents/agents/.oculto.md", skill_file("Use quando OCULTO AG."))
    write(outside / "ag-externo.md", skill_file("Use quando AG EXTERNO."))
    os.symlink(outside / "ag-externo.md", hub / ".agents/agents/ag-externo.md")
    write(hub / ".agents/workflows/wf-um.md", skill_file("Use quando fluxo um."))
    write(hub / ".agents/workflows/_arquivo/w-velho.md", skill_file("Use quando VELHO."))
    return hub


def run(hub: Path, *args: str, cwd=None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), "--hub", str(hub), *args],
                          capture_output=True, encoding="utf-8", cwd=cwd)


def read(hub: Path, resolver: str = "sip-teste") -> str:
    return (hub / ".agents/skills" / resolver / "SKILL.md").read_text(encoding="utf-8")


class HubCase(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.hub = make_hub(self.root)


# ---------- pure: YAML scalar reader (port of Astro readScalar) ----------

class ParseDescriptionTests(unittest.TestCase):
    def test_plain_value(self):
        # Arrange
        fm = "name: x\ndescription: Use quando X"
        # Act
        result = bsi.parse_description(fm)
        # Assert
        self.assertEqual(result, "Use quando X")

    def test_plain_value_drops_trailing_comment(self):
        fm = "description: Use quando X # nota interna"
        self.assertEqual(bsi.parse_description(fm), "Use quando X")

    def test_double_quoted_with_escaped_quote(self):
        fm = 'description: "Use quando diz \\"oi\\""'
        self.assertEqual(bsi.parse_description(fm), 'Use quando diz "oi"')

    def test_single_quoted_with_doubled_apostrophe(self):
        fm = "description: 'Use quando o cliente diz ''sim'''"
        self.assertEqual(bsi.parse_description(fm), "Use quando o cliente diz 'sim'")

    def test_literal_block_keeps_line_breaks(self):
        fm = "description: |\n  linha um\n  linha dois\nname: x"
        self.assertEqual(bsi.parse_description(fm), "linha um\nlinha dois")

    def test_folded_block_joins_lines(self):
        fm = "description: >\n  linha um\n  linha dois"
        self.assertEqual(bsi.parse_description(fm), "linha um linha dois")

    def test_folded_strip_block_joins_lines(self):
        fm = "description: >-\n  linha um\n\n  linha dois"
        self.assertEqual(bsi.parse_description(fm), "linha um linha dois")

    def test_block_ends_at_next_key(self):
        fm = "description: >-\n  a\n  b\nname: x"
        self.assertEqual(bsi.parse_description(fm), "a b")

    def test_missing_description_is_empty(self):
        self.assertEqual(bsi.parse_description("name: x"), "")

    def test_unclosed_quote_is_empty(self):
        self.assertEqual(bsi.parse_description('description: "sem fechar'), "")


# ---------- pure: cleaning (0 Mkt rules) ----------

class CleanDescriptionTests(unittest.TestCase):
    def test_html_entities_are_decoded(self):
        self.assertEqual(bsi.clean_description("A &gt; B &lt; C &amp; D"), "A > B < C & D")

    def test_cut_before_nao_use(self):
        self.assertEqual(bsi.clean_description("Use quando X. NÃO use para Y."), "Use quando X.")

    def test_cut_before_nao_use_without_accent_and_lowercase(self):
        self.assertEqual(bsi.clean_description("Use quando X. não use para Y"), "Use quando X.")

    def test_cut_before_do_not_use_case_insensitive(self):
        self.assertEqual(bsi.clean_description("Use quando X. do not use Y"), "Use quando X.")

    def test_entities_are_decoded_before_cut(self):
        self.assertEqual(bsi.clean_description("Use &gt; X. NÃO use Y"), "Use > X.")

    def test_whitespace_is_collapsed(self):
        self.assertEqual(bsi.clean_description("Use\n   quando\tX"), "Use quando X")

    def test_pipe_is_escaped(self):
        self.assertEqual(bsi.clean_description("Compara a | b"), "Compara a \\| b")

    def test_empty_becomes_placeholder(self):
        self.assertEqual(bsi.clean_description(""), "(sem description)")
        self.assertEqual(bsi.clean_description("   "), "(sem description)")

    def test_only_negative_text_becomes_placeholder(self):
        self.assertEqual(bsi.clean_description("NÃO use para nada"), "(sem description)")

    def test_literal_block_end_to_end(self):
        fm = "description: |\n  Use quando X.\n  NÃO use Y."
        self.assertEqual(desc_of(fm), "Use quando X.")


# ---------- pure: table rendering ----------

class RenderBodyTests(unittest.TestCase):
    def test_flat_table_has_total_and_blank_lines(self):
        # Arrange
        items = [("a-x", "Use A.")]
        # Act
        body = bsi.render_body("skills", items, None)
        # Assert
        self.assertEqual(body, ["", "Total: 1.", "", "| Skill | Use quando |", "| --- | --- |",
                                "| `a-x` | Use A. |", ""])

    def test_workflow_name_cell_uses_slash(self):
        body = bsi.render_body("workflows", [("w", "Use W.")], None)
        self.assertIn("| `/w` | Use W. |", body)

    def test_empty_region_says_nenhum(self):
        self.assertEqual(bsi.render_body("agents", [], None), ["", "Nenhum por enquanto.", ""])

    def test_grouped_prefixes_are_sorted_with_one_total(self):
        items = [("beta-1", "b"), ("alpha-1", "a1"), ("alpha-2", "a2")]
        body = bsi.render_body("skills", items, "prefix")
        self.assertEqual(body.count("Total: 3."), 1)
        self.assertLess(body.index("### alpha"), body.index("### beta"))
        self.assertEqual(body[body.index("### alpha") + 1:body.index("### alpha") + 4], ["", "| Skill | Use quando |", "| --- | --- |"])


# ---------- CLI: regions and exclusions ----------

class CliRegionsTests(HubCase):
    def test_three_regions_are_generated(self):
        # Act
        result = run(self.hub, "--resolver", "sip-teste")
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        text = read(self.hub)
        self.assertIn("| `alpha-um` | Use quando A1. |", text)
        self.assertIn("| `beta-tres` | Use quando B. |", text)
        self.assertIn("| `ag-um` | Use quando agente um. |", text)
        self.assertIn("| `/wf-um` | Use quando fluxo um. |", text)
        self.assertIn("Total: 3.", text)
        self.assertIn("Total: 1.", text)

    def test_default_resolver_is_the_only_real_sip_folder(self):
        result = run(self.hub)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| `alpha-um` |", read(self.hub))


class CliExclusionTests(HubCase):
    def generate(self):
        result = run(self.hub)
        self.assertEqual(result.returncode, 0, result.stderr)
        return read(self.hub)

    def test_sip_resolvers_are_not_listed(self):
        # Arrange
        write(self.hub / ".agents/skills/sip-outro/SKILL.md", skill_file("Use quando SIP OUTRO."))
        # Act
        result = run(self.hub, "--resolver", "sip-teste")
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        text = read(self.hub)
        self.assertNotIn("SIP OUTRO", text)
        self.assertNotIn("`sip-outro`", text)
        self.assertNotIn("`sip-teste`", text)

    def test_underscore_items_are_excluded(self):
        self.assertNotIn("RASCUNHO", self.generate())

    def test_dot_items_are_excluded(self):
        text = self.generate()
        self.assertNotIn("OCULTA", text)
        self.assertNotIn("OCULTO AG", text)

    def test_readme_is_excluded_from_agents(self):
        text = self.generate()
        self.assertNotIn("README", text)
        self.assertIn("| `ag-um` |", text)

    def test_archived_workflows_are_excluded(self):
        self.assertNotIn("VELHO", self.generate())

    def test_symlinks_resolving_outside_hub_are_excluded(self):
        text = self.generate()
        self.assertNotIn("EXTERNA", text)
        self.assertNotIn("AG EXTERNO", text)


# ---------- CLI: markers and options ----------

class CliMarkerTests(HubCase):
    def test_start_line_text_is_preserved_and_text_outside_regions_is_untouched(self):
        # Arrange
        original = read(self.hub)
        # Act
        result = run(self.hub)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        text = read(self.hub)
        self.assertIn(start_line("skills"), text)
        self.assertIn(start_line("agents"), text)
        self.assertEqual(text.split(start_line("skills"))[0], original.split(start_line("skills"))[0])

    def test_group_prefix_option_groups_by_prefix(self):
        # Arrange
        write(self.hub / ".agents/skills/sip-teste/SKILL.md", resolver_text(opts={"skills": "group=prefix "}))
        # Act
        result = run(self.hub)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        text = read(self.hub)
        self.assertIn(start_line("skills", "group=prefix "), text)
        self.assertIn("### alpha", text)
        self.assertIn("### beta", text)
        self.assertLess(text.index("Total: 3."), text.index("### alpha"))
        self.assertLess(text.index("### alpha"), text.index("### beta"))

    def test_unknown_marker_option_is_usage_error(self):
        write(self.hub / ".agents/skills/sip-teste/SKILL.md", resolver_text(opts={"skills": "color=red "}))
        self.assertEqual(run(self.hub).returncode, 2)


# ---------- CLI: idempotency and --check ----------

class CliIdempotencyTests(HubCase):
    def test_second_run_reports_no_changes_and_file_is_unchanged(self):
        # Arrange
        self.assertEqual(run(self.hub).returncode, 0)
        first = read(self.hub)
        # Act
        result = run(self.hub)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Sem mudanças.", result.stdout)
        self.assertEqual(read(self.hub), first)

    def test_rewrite_reports_all_changed_regions(self):
        result = run(self.hub)
        self.assertTrue(result.stdout.strip().endswith(": skills, agents, workflows"), result.stdout)

    def test_only_changed_region_is_reported_and_rewritten(self):
        # Arrange
        self.assertEqual(run(self.hub).returncode, 0)
        path = self.hub / ".agents/skills/alpha-um/SKILL.md"
        write(path, skill_file("Use quando A1 novo."))
        # Act
        result = run(self.hub)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.strip().endswith(": skills"), result.stdout)
        self.assertIn("| `alpha-um` | Use quando A1 novo. |", read(self.hub))


class CliCheckTests(HubCase):
    def test_check_fresh_returns_0(self):
        self.assertEqual(run(self.hub).returncode, 0)
        self.assertEqual(run(self.hub, "--check").returncode, 0)

    def test_check_stale_returns_1_and_writes_nothing(self):
        # Arrange
        before = read(self.hub)
        # Act
        result = run(self.hub, "--check")
        # Assert
        self.assertEqual(result.returncode, 1)
        self.assertIn("Tabelas desatualizadas: skills, agents, workflows", result.stderr)
        self.assertEqual(read(self.hub), before)


# ---------- CLI: missing and empty regions ----------

class CliMissingRegionTests(HubCase):
    def test_missing_region_with_items_is_usage_error(self):
        # Arrange
        write(self.hub / ".agents/skills/sip-teste/SKILL.md", resolver_text(kinds=("skills", "workflows")))
        # Act
        result = run(self.hub)
        # Assert
        self.assertEqual(result.returncode, 2)
        self.assertIn("agents", result.stderr)

    def test_missing_region_without_items_is_dismissed(self):
        # Arrange
        shutil.rmtree(self.hub / ".agents/agents")
        write(self.hub / ".agents/skills/sip-teste/SKILL.md", resolver_text(kinds=("skills", "workflows")))
        # Act
        result = run(self.hub)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_empty_region_says_nenhum_por_enquanto(self):
        # Arrange
        shutil.rmtree(self.hub / ".agents/workflows")
        # Act
        result = run(self.hub)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        text = read(self.hub)
        section = text.split(start_line("workflows"))[1].split("<!-- workflows:end -->")[0]
        self.assertEqual(section.strip(), "Nenhum por enquanto.")

    def test_start_without_end_is_usage_error(self):
        write(self.hub / ".agents/skills/sip-teste/SKILL.md", resolver_text().replace("<!-- skills:end -->", ""))
        self.assertEqual(run(self.hub).returncode, 2)


# ---------- CLI: resolver selection ----------

class CliResolverTests(HubCase):
    def test_ambiguous_default_resolver_is_usage_error(self):
        # Arrange
        write(self.hub / ".agents/skills/sip-outro/SKILL.md", resolver_text())
        # Act
        result = run(self.hub)
        # Assert
        self.assertEqual(result.returncode, 2)
        self.assertIn("sip-*", result.stderr)

    def test_no_sip_folder_is_usage_error(self):
        shutil.rmtree(self.hub / ".agents/skills/sip-teste")
        self.assertEqual(run(self.hub).returncode, 2)

    def test_resolver_flag_picks_one_explicitly(self):
        # Arrange
        write(self.hub / ".agents/skills/sip-outro/SKILL.md", resolver_text())
        untouched = read(self.hub, "sip-teste")
        # Act
        result = run(self.hub, "--resolver", "sip-outro")
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| `alpha-um` |", read(self.hub, "sip-outro"))
        self.assertEqual(read(self.hub, "sip-teste"), untouched)

    def test_missing_resolver_name_is_usage_error(self):
        self.assertEqual(run(self.hub, "--resolver", "nao-existe").returncode, 2)


# ---------- CLI: usage errors ----------

class CliUsageTests(HubCase):
    def raw(self, *args: str, cwd=None) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, encoding="utf-8", cwd=cwd)

    def test_unknown_argument_is_usage_error(self):
        self.assertEqual(run(self.hub, "--foo").returncode, 2)

    def test_help_prints_usage_and_writes_nothing(self):
        before = read(self.hub)
        result = self.raw("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("--check", result.stdout)
        self.assertEqual(read(self.hub), before)

    def test_positional_argument_is_usage_error(self):
        self.assertEqual(run(self.hub, "extra").returncode, 2)

    def test_hub_without_value_is_usage_error(self):
        self.assertEqual(self.raw("--hub").returncode, 2)
        self.assertEqual(self.raw("--hub", "--check").returncode, 2)

    def test_resolver_without_value_is_usage_error(self):
        self.assertEqual(self.raw("--hub", str(self.hub), "--resolver").returncode, 2)

    def test_hub_defaults_to_current_directory(self):
        result = self.raw(cwd=self.hub)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| `alpha-um` |", read(self.hub))


if __name__ == "__main__":
    unittest.main()
