"""Tests for check_sip_hub.py: a conforming temp hub passes, each broken piece fails."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "check_sip_hub.py"
INDEXER = Path(__file__).resolve().parent.parent / "build_sip_index.py"
REGIONS = "".join(f"<!-- {k}:start -->\n<!-- {k}:end -->\n" for k in ("skills", "agents", "workflows"))
SECTIONS = "## O quê\n## Como\n## Onde\n## Por quê\n## Para quê\n## Quem\n## Efeitos e impactos\n## Exemplos\n## Gatilho para sair da inbox\n## Enquanto isso\n"


def build_hub(name: str = "SIP - Teste", cite: str | None = None) -> Path:
    hub = Path(tempfile.mkdtemp()) / name
    (hub / ".agent/skills/sip-teste").mkdir(parents=True)
    (hub / "prompts").mkdir()
    (hub / "inbox").mkdir()
    (hub / "instalacoes").mkdir()
    (hub / ".agent/skills/sip-teste/SKILL.md").write_text(
        f"## Atualização\n- Última atualização do hub: 2026-11-11\n- cole `\"{cite or hub}/prompts/instalar-skill-sip-teste.md\"`\n"
        f"Crie `\"{hub}/inbox/NNN-<assunto>.md\"`\n" + REGIONS)
    (hub / "prompts/instalar-skill-sip-teste.md").write_text(
        "rode sync_entrypoints.py --check\n- Para atualizar: cole de novo \"x\"\n"
        "pergunte \"nenhum / todos / quais\"; pergunte só os itens fora de \"Vistos no hub\"; arquivo real: caso a caso\n")
    (hub / "inbox/README.md").write_text("inbox/NNN-<assunto>.md ... mova para `inbox/arquivo/`. Nunca apague.\n" + SECTIONS)
    (hub / "instalacoes/README.md").write_text("formato\n")
    (hub / ".gitignore").write_text("inbox/*\n!inbox/README.md\ninstalacoes/*\n!instalacoes/README.md\n")
    subprocess.run(["git", "init", "-q", str(hub)], check=True)
    subprocess.run([sys.executable, str(INDEXER), "--hub", str(hub)], check=True, capture_output=True)
    return hub


def run(hub: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), str(hub), "sip-teste"], capture_output=True, text=True)


class CheckSipHub(unittest.TestCase):
    def test_conforming_hub_passes(self):
        result = run(build_hub())
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_accented_hub_path_stored_decomposed_still_matches_the_resolver(self):
        # Arrange: Finder stores "Previsão" decomposed (NFD); the resolver text cites it composed (NFC)
        import unicodedata
        nfd = unicodedata.normalize("NFD", "SIP - Previsão")
        hub = build_hub(nfd)
        resolver = hub / ".agent/skills/sip-teste/SKILL.md"
        import os
        text = resolver.read_text(encoding="utf-8").replace(str(hub), os.path.realpath(hub))  # /var -> /private/var
        resolver.write_text(unicodedata.normalize("NFC", text), encoding="utf-8")
        # Act: the hub given as "." from inside it, as a pre-commit hook does
        result = subprocess.run([sys.executable, str(SCRIPT), ".", "sip-teste"], capture_output=True, text=True, cwd=hub)
        # Assert
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_whole_inbox_ignored_fails_readme_check(self):
        hub = build_hub()
        (hub / ".gitignore").write_text("inbox/\ninstalacoes/\n")
        result = run(hub)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL  gitignore: inbox/README.md versioned", result.stdout)

    def test_resolver_without_update_section_fails(self):
        hub = build_hub()
        (hub / ".agent/skills/sip-teste/SKILL.md").write_text("sem seção\n")
        result = run(hub)
        self.assertIn("FAIL  resolver: section '## Atualização'", result.stdout)

    def test_tracked_inbox_item_fails(self):
        hub = build_hub()
        (hub / "inbox/001-x.md").write_text("x")
        subprocess.run(["git", "-C", str(hub), "add", "-f", "inbox/001-x.md"], check=True)
        result = run(hub)
        self.assertIn("FAIL  no tracked items", result.stdout)
        self.assertIn("inbox/001-x.md", result.stdout)

    def test_stale_tables_fail(self):
        hub = build_hub()
        (hub / ".agent/agents").mkdir(parents=True)
        (hub / ".agent/agents/novo.md").write_text("---\ndescription: Use quando novo.\n---\n")
        result = run(hub)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL  resolver: tables up to date", result.stdout)

    def test_missing_agents_region_fails(self):
        hub = build_hub()
        resolver = hub / ".agent/skills/sip-teste/SKILL.md"
        resolver.write_text(resolver.read_text().replace("<!-- agents:start -->", ""))
        result = run(hub)
        self.assertIn("FAIL  resolver: regions for skills, agents and workflows", result.stdout)

    def test_prompt_installing_everything_fails(self):
        hub = build_hub()
        (hub / "prompts/instalar-skill-sip-teste.md").write_text(
            "rode sync_entrypoints.py --check\n- Para atualizar: cole de novo \"x\"\nPara cada agent: symlink.\n")
        result = run(hub)
        self.assertIn("FAIL  prompt: asks which agents/workflows to install", result.stdout)
        self.assertIn("FAIL  prompt: real file with the same name", result.stdout)

    def test_old_inbox_format_fails(self):
        hub = build_hub()
        (hub / "inbox/README.md").write_text("Crie AAAA-MM-DD_<projeto>_<assunto>.md\n## Tipo\n")
        result = run(hub)
        self.assertIn("FAIL  inbox README: NNN naming", result.stdout)


if __name__ == "__main__":
    unittest.main()
