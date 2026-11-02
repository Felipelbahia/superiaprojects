#!/usr/bin/env python3
"""
projects_audit.py - READ-ONLY report of every project against the Antigravity Kit rules.

For each project (a folder that has a rules file) it reports whether its copy of the rules already has
the newer kit rules, whether it has the `## Stack` block, whether it adopted `_projectdefines/`, and where
its execution loops and handoffs live (project root = legacy, `.agent/plans/` = current).

It never writes inside a project. The only file it writes is the report (default:
`<kit>/.agent/plans/Relatório de projetos vs kit.md`).

Usage:
    python3 projects_audit.py                 # scan the default roots, print the table and write the report
    python3 projects_audit.py --no-write      # print only
    python3 projects_audit.py --roots "/path/a" "/path/b" --out "/path/report.md"
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

BASE = Path("/Users/macbookpro/Documents/IA Projects")
DEFAULT_ROOTS = ["Compartilhado", "Pessoal", "Plinq", "Projetos", "WaiMonitor", "_Plataforma"]
KIT = BASE / "_Plataforma" / "0 Padrões"
DEFAULT_OUT = KIT / ".agent" / "plans" / "Relatório de projetos vs kit.md"

FICHAS = KIT / "projetos"
KIT_RULE_PATHS = ["CLAUDE.md", "GEMINI.md", "AGENTS.md", ".cursorrules", ".agent"]
RULE_FILES = ["CLAUDE.md", "AGENTS.md", "GEMINI.md", ".cursorrules"]
AGENT_RULE_FILES = [Path(".agent/rules") / n for n in ("CLAUDE.md", "GEMINI.md", "AGENTS.md")]
PRUNE = {
    "node_modules", ".git", ".venv", "venv", "__pycache__", "dist", "build", ".next", ".agent", ".agents", ".claude",
    "Output", "snapshot", "skills", "bak", ".firecrawl", "data", "temporario",
}
MAX_DEPTH = 4
WEB_MARKERS = ("next", "react", "vue", "svelte", "astro", "vite", "nuxt")


def read_text(path: Path, limit: int = 2_000_000) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return fh.read(limit)
    except OSError:
        return ""


def rule_paths(folder: Path):
    found = [folder / n for n in RULE_FILES if (folder / n).is_file()]
    found += [folder / p for p in AGENT_RULE_FILES if (folder / p).is_file()]
    return found


def project_type(folder: Path) -> str:
    pkg = folder / "package.json"
    if pkg.is_file():
        try:
            data = json.loads(read_text(pkg))
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            if any(m in deps for m in WEB_MARKERS):
                return "web app"
            return "node"
        except ValueError:
            return "node"
    for marker in ("pyproject.toml", "requirements.txt"):
        if (folder / marker).is_file():
            return "python"
    try:
        if any(p.suffix == ".py" for p in folder.iterdir() if p.is_file()):
            return "python"
    except OSError:
        pass
    return "other/docs"


def discover(roots):
    seen = set()
    for root in roots:
        root = Path(root)
        if not root.is_dir():
            continue
        base_depth = len(root.parts)
        for current, dirs, _files in os.walk(root):
            cur = Path(current)
            dirs[:] = [d for d in dirs if d not in PRUNE]
            if len(cur.parts) - base_depth >= MAX_DEPTH:
                dirs[:] = []
            if cur in seen:
                continue
            if rule_paths(cur):
                seen.add(cur)
                yield cur


def stack_state(text: str) -> str:
    """'yes' = the kit's `## Stack` block (exact heading + Context7 line); 'old' = exact heading without it; 'no'."""
    m = re.search(r"^## Stack[ \t]*$", text, re.M)
    if not m:
        return "no"
    return "yes" if "Context7" in text[m.end():m.end() + 700] else "old"


def launch_profile_state(folder: Path) -> str:
    """'-' = no `_projectdefines/`; 'yes' = BRIEF has the Launch profile section; 'no' = BRIEF lacks it (or is missing)."""
    contract = folder / "_projectdefines"
    if not contract.is_dir():
        return "-"
    brief = contract / "BRIEF.md"
    return "yes" if brief.is_file() and "Launch profile" in read_text(brief) else "no"


def ficha_index() -> dict:
    """Map each project folder to its ficha in `projetos/`, via the first backticked path after 'Repositório / Caminho'."""
    index = {}
    for ficha in FICHAS.glob("*.md"):
        m = re.search(r"Repositório / Caminho:\*\*\s*`([^`]+)`", read_text(ficha))
        if m:
            index[Path(m.group(1))] = ficha
    return index


def sync_state(ficha) -> tuple:
    """(date, kit_changed): reads '> **Última sincronização com o kit:** AAAA-MM-DD (kit @ hash)' from the ficha.
    No ficha -> ('sem ficha', '-'); no line -> ('nunca', '-'); kit_changed = 'sim (N)', 'não' or '?'."""
    if ficha is None:
        return "sem ficha", "-"
    m = re.search(r"Última sincronização com o kit:\*\*\s*(\d{4}-\d{2}-\d{2})\s*\(kit @ ([0-9a-f]{4,40})\)", read_text(ficha))
    if not m:
        return "nunca", "-"
    date, sha = m.groups()
    try:
        out = subprocess.run(
            ["git", "-C", str(KIT), "rev-list", "--count", f"{sha}..HEAD", "--", *KIT_RULE_PATHS],
            capture_output=True, text=True, timeout=30, check=True,
        ).stdout.strip()
        return date, ("não" if out == "0" else f"sim ({out})")
    except (subprocess.SubprocessError, OSError):
        return date, "?"


def audit(folder: Path, fichas=None):
    text = "\n".join(read_text(p) for p in rule_paths(folder))
    loops_new = (folder / ".agent" / "plans" / "execution-loops").is_dir()
    loops_old = (folder / "execution-loops").is_dir()
    hand_new = (folder / ".agent" / "plans" / "handoffs").is_dir()
    hand_old = (folder / "handoffs").is_dir()
    gate = "Project Defines Gate" in text
    latest = "Latest Docs First" in text
    stack = stack_state(text)
    synced, kit_changed = sync_state((fichas or {}).get(folder))
    return {
        "path": folder,
        "type": project_type(folder),
        "gate": gate,
        "latest": latest,
        "stack": stack,
        "contract": (folder / "_projectdefines").is_dir(),
        "launch": launch_profile_state(folder),
        "loops": "new" if loops_new else ("legacy" if loops_old else "-"),
        "handoffs": "new" if hand_new else ("legacy" if hand_old else "-"),
        "up_to_date": gate and latest,
        "synced": synced,
        "kit_changed": kit_changed,
    }


def mark(flag) -> str:
    if isinstance(flag, str):
        return flag
    return "yes" if flag else "no"


def render(rows) -> str:
    today = datetime.date.today().isoformat()
    behind = [r for r in rows if not r["up_to_date"]]
    lines = [
        "# Relatório de projetos vs kit",
        "",
        f"> Gerado em {today} por `.agent/scripts/projects_audit.py`. **Somente leitura**: nenhum arquivo de projeto foi alterado.",
        "> *Gate* = tem o Project Defines Gate · *Latest* = tem Latest Docs First · *Stack* = bloco `## Stack` do kit (`yes`; `old` = título igual mas sem o formato) · *Contract* = tem `_projectdefines/` · *Launch* = o BRIEF dele tem a seção Launch profile (`no` = contrato sem perfil de lançamento; `-` = sem contrato).",
        "> *Sincronizado em* = data da linha \"Última sincronização com o kit\" na ficha (`nunca` = ficha sem a linha; `sem ficha` = nenhuma ficha aponta para esta pasta) · *Kit mudou desde então* = commits do kit em regras e `.agent/` depois do hash registrado.",
        "> *Loops/Handoffs*: `new` = `.agent/plans/…` · `legacy` = na raiz do projeto (continua valendo até migrar) · `-` = não existe.",
        "",
        f"**{len(rows)} projetos encontrados · {len(rows) - len(behind)} com as regras novas · {len(behind)} atrás do kit.**",
        "",
        "| Projeto | Tipo | Gate | Latest | Stack | Contract | Launch | Loops | Handoffs | Situação | Sincronizado em | Kit mudou desde então |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        rel = os.path.relpath(r["path"], BASE)
        lines.append(
            f"| {rel} | {r['type']} | {mark(r['gate'])} | {mark(r['latest'])} | {mark(r['stack'])} | "
            f"{mark(r['contract'])} | {r['launch']} | {r['loops']} | {r['handoffs']} | {'em dia' if r['up_to_date'] else 'atrás'} | "
            f"{r['synced']} | {r['kit_changed']} |"
        )
    lines += [
        "",
        "## Como usar",
        "- **Atrás do kit, ou `Kit mudou` = `sim`:** rode o prompt `projetos/prompts/08-sincronizar-com-o-kit.md` no projeto (incremental; grava a data na ficha). Primeira adoção do padrão: `01-atualizar-projeto-existente.md` (Merge & Preserve).",
        "- **Aplicação com interface e sem contrato:** candidata ao modo brownfield (`projetos/prompts/03-adotar-contrato-brownfield.md`).",
        "- **Contract `yes` e Launch `no`:** o contrato foi aprovado antes do perfil de lançamento; propor ao dono a adoção da seção (`project-defines/launch-profile.md`), sem editar o BRIEF aprovado por conta própria.",
        "- **`legacy` em loops/handoffs:** nada a fazer; a migração é opcional e só a pedido do dono.",
    ]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--roots", nargs="*", help="folders to scan (default: the standard project roots)")
    ap.add_argument("--out", help="report path (default inside the kit's .agent/plans/)")
    ap.add_argument("--no-write", action="store_true", help="print only; write nothing")
    args = ap.parse_args()

    roots = [Path(r) for r in args.roots] if args.roots else [BASE / r for r in DEFAULT_ROOTS]
    fichas = ficha_index()
    rows = sorted((audit(p, fichas) for p in discover(roots)), key=lambda r: str(r["path"]).lower())
    report = render(rows)
    print(report)
    if not args.no_write:
        out = Path(args.out) if args.out else DEFAULT_OUT
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"[ok] report written to: {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
