#!/usr/bin/env python3
"""
projects_audit.py - READ-ONLY report of every project against the Antigravity Kit rules.

For each project (a folder that has a rules file) it reports which rules model it uses (modular = assembled
from the kit's modules; old = the pre-2026-11-12 rules), whether its `## Project` profile is filled, whether
`sip-geral` is installed, whether it has the destination map, whether `.claude/CLAUDE.md` duplicates
`./CLAUDE.md`, the `## Stack` block, `_projectdefines/`, and where its loops and handoffs live.

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
import unicodedata
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
# Third-party clones that have their own rules files: never audited, never changed.
THIRD_PARTY = {BASE / "_Plataforma" / "Firecrawl - local" / "docs", BASE / "_Plataforma" / "Firecrawl - local" / "firecrawl"}
WEB_MARKERS = ("next", "react", "vue", "svelte", "astro", "vite", "nuxt")


def read_text(path: Path, limit: int = 2_000_000) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return fh.read(limit)
    except OSError:
        return ""


def agent_linked_to_kit(folder: Path, kit_agent: Path = KIT / ".agent") -> bool:
    """True when the project's `.agent` is a link into the kit's `.agent` (its plans, rules and skills are the kit's)."""
    if folder.resolve() == kit_agent.resolve().parent:
        return False
    kit = kit_agent.resolve()
    for sub in (".agent", ".agent/rules", ".agent/plans", ".agent/skills"):
        link = folder / sub
        if link.is_symlink():
            target = link.resolve()
            if target == kit or kit in target.parents:
                return True
    return False


def rule_paths(folder: Path, skip_agent: bool = False):
    found = [folder / n for n in RULE_FILES if (folder / n).is_file()]
    if not skip_agent:
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


def discover(roots, skip=THIRD_PARTY):
    seen = set()
    for root in roots:
        root = Path(root)
        if not root.is_dir():
            continue
        base_depth = len(root.parts)
        for current, dirs, _files in os.walk(root):
            cur = Path(current)
            dirs[:] = [d for d in dirs if d not in PRUNE and cur / d not in skip]
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


def rules_model(text: str) -> str:
    """'modular' = assembled from the kit modules; 'old' = pre-2026-11-12 kit rules; 'none'."""
    if "Before acting (mandatory sequence)" in text:
        return "modular"
    if "Project Defines Gate" in text or "Latest Docs First" in text:
        return "old"
    return "none"


def profile_filled(text: str) -> bool:
    """True when a `- Produces:` line has a real value (the core module ships a `<...>` placeholder)."""
    return any(not m.group(1).startswith("<") for m in re.finditer(r"^\s*-\s*\**Produces:\**[ \t]*(\S.*)$", text, re.M))


def launch_profile_state(folder: Path) -> str:
    """'-' = no `_projectdefines/`; 'yes' = BRIEF has the Launch profile section; 'no' = BRIEF lacks it (or is missing)."""
    contract = folder / "_projectdefines"
    if not contract.is_dir():
        return "-"
    brief = contract / "BRIEF.md"
    return "yes" if brief.is_file() and "Launch profile" in read_text(brief) else "no"


def nfc_path(path: Path) -> Path:
    """Composed Unicode: macOS may hand back a folder decomposed (NFD) while a ficha cites it composed (NFC)."""
    return Path(unicodedata.normalize("NFC", str(path)))


def ficha_index() -> dict:
    """Map each project folder to its ficha in `projetos/`, via the first backticked path after 'Repositório / Caminho'."""
    index = {}
    for ficha in FICHAS.glob("*.md"):
        m = re.search(r"Repositório / Caminho:\*\*\s*`([^`]+)`", read_text(ficha))
        if m:
            index[nfc_path(Path(m.group(1)))] = ficha
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


def audit(folder: Path, fichas=None, kit_agent: Path = KIT / ".agent"):
    linked = agent_linked_to_kit(folder, kit_agent)
    text = "\n".join(read_text(p) for p in rule_paths(folder, skip_agent=linked))
    loops_new = (folder / ".agent" / "plans" / "execution-loops").is_dir()
    loops_old = (folder / "execution-loops").is_dir()
    hand_new = (folder / ".agent" / "plans" / "handoffs").is_dir()
    hand_old = (folder / "handoffs").is_dir()
    model = rules_model(text)
    profile = profile_filled(text)
    sip = any((folder / d / "skills" / "sip-geral").exists() for d in ((".claude",) if linked else (".agent", ".claude")))
    dest_map = (folder / "docs" / "mapa-de-destinos.md").is_file() or (folder / "mapa-de-destinos.md").is_file()
    duplicate = (folder / "CLAUDE.md").is_file() and (folder / ".claude" / "CLAUDE.md").is_file()
    stack = stack_state(text)
    synced, kit_changed = sync_state((fichas or {}).get(nfc_path(folder)))
    return {
        "path": folder,
        "type": project_type(folder),
        "model": model,
        "profile": profile,
        "sip": sip,
        "map": dest_map,
        "duplicate": duplicate,
        "agent_linked": linked,
        "stack": stack,
        "contract": (folder / "_projectdefines").is_dir(),
        "launch": launch_profile_state(folder),
        "loops": "new" if loops_new else ("legacy" if loops_old else "-"),
        "handoffs": "new" if hand_new else ("legacy" if hand_old else "-"),
        "up_to_date": model == "modular" and profile and sip and dest_map and not duplicate and not linked,
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
        "> *Modelo* = `modular` (regras montadas pelos módulos do kit) · `old` (regras anteriores a 2026-11-12) · `none` · *Perfil* = bloco `## Project` preenchido · *SIP geral* = `sip-geral` instalado · *Mapa* = `docs/mapa-de-destinos.md` · *.claude/CLAUDE.md* = `yes` quando duplica o `./CLAUDE.md` (regras em dobro) · *.agent → kit* = `yes` quando a pasta `.agent` do projeto é um link para o `.agent` do kit (planos, regras e skills do projeto caem dentro do kit; as regras de `.agent/rules/` não são lidas como do projeto) · *Stack* = bloco `## Stack` (`yes`; `old` = título sem o formato) · *Contract* = tem `_projectdefines/` · *Launch* = o BRIEF tem a seção Launch profile (`-` = sem contrato).",
        "> *Situação* `em dia` = Modelo `modular` + Perfil + SIP geral + Mapa + sem `.claude/CLAUDE.md` duplicado + `.agent` próprio.",
        "> *Sincronizado em* = data da linha \"Última sincronização com o kit\" na ficha (`nunca` = ficha sem a linha; `sem ficha` = nenhuma ficha aponta para esta pasta) · *Kit mudou desde então* = commits do kit em `.agent/` depois do hash registrado (os arquivos de regra do kit não são versionados; mudança não commitada não conta).",
        "> *Loops/Handoffs*: `new` = `.agent/plans/…` · `legacy` = na raiz do projeto (continua valendo até migrar) · `-` = não existe.",
        "",
        f"**{len(rows)} projetos encontrados · {len(rows) - len(behind)} com as regras novas · {len(behind)} atrás do kit.**",
        "",
        "| Projeto | Tipo | Modelo | Perfil | SIP geral | Mapa | .claude/CLAUDE.md | .agent → kit | Stack | Contract | Launch | Loops | Handoffs | Situação | Sincronizado em | Kit mudou desde então |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        rel = os.path.relpath(r["path"], BASE)
        lines.append(
            f"| {rel} | {r['type']} | {r['model']} | {mark(r['profile'])} | {mark(r['sip'])} | {mark(r['map'])} | "
            f"{mark(r['duplicate'])} | {mark(r['agent_linked'])} | {mark(r['stack'])} | "
            f"{mark(r['contract'])} | {r['launch']} | {r['loops']} | {r['handoffs']} | {'em dia' if r['up_to_date'] else 'atrás'} | "
            f"{r['synced']} | {r['kit_changed']} |"
        )
    lines += [
        "",
        "## Como usar",
        "- **Atrás do kit, ou `Kit mudou` = `sim`:** rode o prompt `projetos/prompts/01-atualizar-projeto-existente.md` no projeto (primeira adoção ou atualização; grava a data na ficha). Ele cobre cada coluna `no`: monta as regras pelos módulos (Modelo), preenche o `## Project` (Perfil), instala o `sip-geral`, cria o mapa de destinos e trata o `.claude/CLAUDE.md` duplicado (só apaga com o seu ok).",
        "- **`.agent → kit` = `yes`:** NÃO rode o 01 antes de decidir com o dono: o projeto escreveria dentro do kit. Primeiro troque o link por uma pasta `.agent/` própria (com aprovação), depois alinhe.",
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
