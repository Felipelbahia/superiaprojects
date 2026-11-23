#!/usr/bin/env python3
"""check_sip_hub.py - Check a SIP hub against the superiaprojects-criar-sip model (tables, opt-in install, inbox, update, gitignore).

Usage: python3 .agents/scripts/check_sip_hub.py "<hub path>" <resolver skill name>
Exit 0 when every check passes, 1 otherwise. Read-only.
"""

import os
import re
import subprocess
import unicodedata
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import linkutil  # noqa: E402

PROBE = "zzz-check-sip-hub-probe.md"
INDEXER = Path(__file__).resolve().parent / "build_sip_index.py"
KINDS = ("skills", "agents", "workflows")
MAX_RESOLVER_LINES = 120  # two-level resolver: steps, modes and the vertical table; the lists live in verticais/


def resolver_dir(hub: Path, skill: str) -> Path:
    """`<hub>/prompts/resolver/<skill>` (new layout) when it exists, else `<hub>/.agents/skills/<skill>` (legacy)."""
    new = hub / "prompts" / "resolver" / skill
    return new if new.is_dir() else hub / linkutil.adir(hub) / "skills" / skill


def ignored(hub: Path, rel: str) -> bool:
    """Evaluate the hub's .gitignore with a throwaway git dir, so hubs that are not git repos are checked too."""
    with tempfile.TemporaryDirectory() as git_dir:
        subprocess.run(["git", "init", "-q", "--bare", git_dir], check=True)
        cmd = ["git", f"--git-dir={git_dir}", f"--work-tree={hub}", "-C", str(hub), "check-ignore", "-q", "--no-index", rel]
        return subprocess.run(cmd).returncode == 0


def tracked(hub: Path, folder: str) -> list[str]:
    if not (hub / ".git").exists():
        return []  # not a git repo: nothing can be tracked
    out = subprocess.run(["git", "-C", str(hub), "ls-files", "-z", folder], capture_output=True, text=True).stdout.split("\0")
    return [f for f in out if f and f != f"{folder}/README.md"]


def tables_fresh(hub: Path, skill: str) -> tuple[bool, str]:
    """Run the kit's table generator in --check mode (read-only)."""
    cmd = [sys.executable, str(INDEXER), "--hub", str(hub), "--resolver", skill, "--check"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    return out.returncode == 0, (out.stderr or out.stdout).strip().splitlines()[0] if (out.stderr or out.stdout).strip() else ""


def nfc(text: str) -> str:
    """Composed Unicode: macOS may hand back a path decomposed (NFD) while the text cites it composed."""
    return unicodedata.normalize("NFC", text)


def checks(hub: Path, skill: str) -> list[tuple[str, bool, str]]:
    resolver = resolver_dir(hub, skill) / "SKILL.md"
    prompt = hub / "prompts" / f"instalar-skill-{skill}.md"
    inbox = hub / "inbox" / "README.md"
    r = resolver.read_text(encoding="utf-8") if resolver.is_file() else ""
    p = prompt.read_text(encoding="utf-8") if prompt.is_file() else ""
    i = inbox.read_text(encoding="utf-8") if inbox.is_file() else ""
    sections = ["## O quê", "## Como", "## Onde", "## Por quê", "## Para quê", "## Quem",
                "## Efeitos e impactos", "## Exemplos", "## Gatilho para sair da inbox", "## Enquanto isso"]
    two_level = "<!-- indice:start" in r and "<!-- indice:end -->" in r  # small resolver + one file per vertical
    missing_regions = [] if two_level else [k for k in KINDS if f"<!-- {k}:start" not in r or f"<!-- {k}:end -->" not in r]
    fresh, fresh_detail = tables_fresh(hub, skill) if resolver.is_file() else (False, "")
    new_layout = (hub / "prompts" / "resolver" / skill).is_dir()
    leftovers = [str(x.relative_to(hub)) for x in (hub / linkutil.adir(hub) / "skills" / skill, hub / ".claude" / "skills" / skill)
                 if os.path.lexists(x)] if new_layout else []
    size = len(r.splitlines())
    result = [
        ("resolver exists", resolver.is_file(), str(resolver)),
        ("resolver (new layout): no copy or link left in the hub's own .agents/skills or .claude/skills", not leftovers, ", ".join(leftovers)),
        (f"resolver (new layout): small enough, at most {MAX_RESOLVER_LINES} lines", not new_layout or size <= MAX_RESOLVER_LINES, f"{size} lines"),
        ("resolver: regions for skills, agents and workflows (or the `indice` region)", not missing_regions, ", ".join(missing_regions)),
        ("resolver: tables up to date (build_sip_index.py --check)", fresh, fresh_detail),
        ("prompt exists", prompt.is_file(), str(prompt)),
        ("resolver: section '## Atualização'", "## Atualização" in r, ""),
        ("resolver: 'Última atualização do hub: AAAA-MM-DD' with a real date",
         bool(re.search(r"Última atualização do hub: \d{4}-\d{2}-\d{2}", r)), ""),
        ("resolver: cites the prompt path",
         (nfc(f"{hub}/prompts/instalar-skill-{skill}.md") in nfc(r) or f"<HUB>/prompts/instalar-skill-{skill}.md" in r), ""),
        ("resolver: contribution as inbox/NNN-<assunto>.md", "inbox/NNN-" in r, ""),
        ("prompt: manifest line 'Para atualizar: cole de novo'", "Para atualizar: cole de novo" in p, ""),
        ("prompt: runs sync_entrypoints.py --check", "sync_entrypoints.py" in p and "--check" in p, ""),
        ("prompt: asks which agents/workflows to install (nenhum / todos / quais)", "nenhum / todos" in p, ""),
        ("prompt: reinstall asks only new items ('Vistos no hub')", "Vistos no hub" in p, ""),
        ("prompt: real file with the same name -> ask case by case, never ln over it", "caso a caso" in p, ""),
        ("inbox README: NNN naming", "NNN-" in i, ""),
        ("inbox README: move to inbox/arquivo/, never delete", "inbox/arquivo/" in i and "Nunca apague" in i, ""),
        ("inbox README: all sections", all(s in i for s in sections), ", ".join(s for s in sections if s not in i)),
        ("gitignore: inbox items ignored", ignored(hub, f"inbox/{PROBE}"), ""),
        ("gitignore: inbox/README.md versioned", not ignored(hub, "inbox/README.md"), ""),
        ("gitignore: instalacoes items ignored", ignored(hub, f"instalacoes/{PROBE}"), ""),
        ("gitignore: instalacoes/README.md versioned", not ignored(hub, "instalacoes/README.md"), ""),
        ("no tracked items in inbox/ or instalacoes/ (README excepted)",
         not (tracked(hub, "inbox") + tracked(hub, "instalacoes")), " ".join(tracked(hub, "inbox") + tracked(hub, "instalacoes"))),
    ]
    return result


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    hub, skill = Path(os.path.abspath(sys.argv[1])), sys.argv[2]
    failed = 0
    results = checks(hub, skill)
    for label, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {label}{'' if ok or not detail else '  -> ' + detail}")
        failed += not ok
    print(f"{hub.name}: {len(results) - failed}/{len(results)} PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
