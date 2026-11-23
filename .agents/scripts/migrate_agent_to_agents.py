#!/usr/bin/env python3
"""migrate_agent_to_agents.py - rename a project's `.agent/` folder to `.agents/` (the name the Codex reads).

Usage:
    python3 migrate_agent_to_agents.py PROJECT [PROJECT ...]            # simulation (default): writes nothing
    python3 migrate_agent_to_agents.py PROJECT [...] --apply            # migrates
    python3 migrate_agent_to_agents.py PROJECT [...] --apply --hub      # also fix prompts/, README*.md, docs/ (a SIP hub)
    (the kit's own scripts used to refresh copies are found from this file: the kit is `<this>/../..`)

Per project, with --apply:
  1. `.agent/` is renamed to `.agents/` (plain rename; nothing is staged or committed). When `.agents/` already exists,
     the two are merged if no file or folder name clashes; a clash stops the project and is reported.
  2. Symlinks under .claude/, .cursor/, .githooks/ and .agents/ (except plans/) whose target names `.agent` are re-pointed
     at `.agents`, but only when the new target exists (a hub not migrated yet leaves the link alone and is reported).
  3. In the rule files (CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules, .gitignore, STANDARDS.md, .claude/CLAUDE.md,
     .claude/settings.json), .githooks/, .github/ and the text files of `.agents/` (not plans/, vendor/), the folder name
     `.agent` becomes `.agents`. A local copy of a kit script that is byte-identical to the kit's previous version is
     replaced by the kit's current one; any other copy gets the same text replacement.
  4. Prints the symlinks that still dangle.
No symlink `.agent -> .agents` is created. A `.agent` that is itself a link (into the kit) is skipped: the owner decides.
Standard library only.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent.parent
OLD = re.compile(r"(?<![A-Za-z0-9_])\.agent(?![A-Za-z0-9_-])")
OLD_PATH = re.compile(r"(?<![A-Za-z0-9_])\.agent(?=/|$)")
ROOT_FILES = ["CLAUDE.md", "AGENTS.md", "GEMINI.md", ".cursorrules", ".gitignore", "STANDARDS.md",
              ".claude/CLAUDE.md", ".claude/settings.json"]
TEXT_SUFFIXES = {".md", ".py", ".json", ".txt", ".sh", ".yml", ".yaml", ".toml", ".js", ".html", ".css", ""}
LINK_DIRS = [".agents", ".claude", ".cursor", ".githooks"]  # .agents first: the other links point into it
SKIP_DIRS = {"plans", "vendor", "node_modules", ".git", "__pycache__"}
MAX_BYTES = 3_000_000


def walk(base: Path):
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files + [d for d in dirs if (Path(root) / d).is_symlink()]:
            yield Path(root) / name


def clashes(src: Path, dst: Path) -> list[str]:
    out = []
    for item in src.iterdir():
        target = dst / item.name
        if not os.path.lexists(target):
            continue
        if item.is_dir() and not item.is_symlink() and target.is_dir() and not target.is_symlink():
            out += clashes(item, target)
        else:
            out.append(str(target))
    return out


def merge(src: Path, dst: Path) -> None:
    for item in sorted(src.iterdir()):
        target = dst / item.name
        if not os.path.lexists(target):
            os.rename(item, target)
        else:
            merge(item, target)
    src.rmdir()


def text_files(project: Path, hub: bool, folder: str = ".agents"):
    seen = set()
    candidates = [project / f for f in ROOT_FILES]
    for d in [".githooks", ".github", folder] + (["prompts", "docs"] if hub else []):
        if (project / d).is_dir():
            candidates += list(walk(project / d))
    if hub:
        candidates += [project / "README.md", project / "README.en.md"]
    for f in candidates:
        if f in seen:
            continue
        seen.add(f)
        if f.is_symlink() or not f.is_file() or f.suffix not in TEXT_SUFFIXES:
            continue
        rel = f.relative_to(project).parts
        if rel[0] == folder and len(rel) > 1 and rel[1] in SKIP_DIRS:
            continue
        if f.stat().st_size > MAX_BYTES:
            continue
        yield f


def previous_kit_version(name: str) -> bytes | None:
    """The kit's script as committed before this migration (`.agent/scripts/<name>` at the migration's parent commit)."""
    for ref in (f"HEAD:.agent/scripts/{name}", f"HEAD~1:.agent/scripts/{name}"):
        r = subprocess.run(["git", "-C", str(KIT), "show", ref], capture_output=True)
        if r.returncode == 0 and r.stdout:
            return r.stdout
    return None


def refresh_copy(f: Path) -> bool:
    """Replace a byte-identical old copy of a kit script by the kit's current one."""
    kit_file = KIT / ".agents" / "scripts" / f.name
    if f.parent.name != "scripts" or f.suffix != ".py" or not kit_file.is_file():
        return False
    old = previous_kit_version(f.name)
    if old is not None and f.read_bytes() == old:
        f.write_bytes(kit_file.read_bytes())
        return True
    return False


def retarget_links(project: Path, apply: bool) -> tuple[int, list[str]]:
    changed, left = 0, []
    for d in LINK_DIRS:
        base = project / d
        if not base.is_dir():
            continue
        for link in walk(base):
            if not link.is_symlink():
                continue
            raw = os.readlink(link)
            new = OLD_PATH.sub(".agents", raw.replace("\\", "/"))
            if new == raw:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(link), new)) if not os.path.isabs(new) else new
            if not os.path.exists(resolved) and not (not apply and os.path.lexists(project / ".agent")):
                left.append(f"{link.relative_to(project)} -> {new} (alvo novo não existe)")
                continue
            changed += 1
            if apply:
                is_dir = os.path.isdir(resolved)
                link.unlink()
                link.symlink_to(new, target_is_directory=is_dir)
    return changed, left


def dangling(project: Path) -> list[str]:
    out = []
    for d in LINK_DIRS:
        base = project / d
        if base.is_dir():
            out += [str(p.relative_to(project)) for p in walk(base) if p.is_symlink() and not p.exists()]
    return out


def migrate(project: Path, apply: bool, hub: bool = False) -> tuple[str, list[str]]:
    """(status, details). Status: migrado | simulado | nada | pulado | conflito."""
    old, new = project / ".agent", project / ".agents"
    notes: list[str] = []
    if not os.path.lexists(old) and not new.is_dir():
        return "nada", ["sem .agent/"]
    repair = not os.path.lexists(old)  # already renamed: only re-point links and text (safe to run again)
    if not repair and old.is_symlink():
        return "pulado", [f".agent é um link ({os.readlink(old)}): o dono decide"]
    if repair:
        notes.append("pasta já renomeada: só links e texto")
    elif os.path.lexists(new) and new.is_dir() and not new.is_symlink():
        found = clashes(old, new)
        if found:
            return "conflito", [f"já existe {x}" for x in found[:5]]
        notes.append("mescla com .agents/ existente")
    elif os.path.lexists(new):
        return "conflito", [".agents existe e não é pasta"]
    if apply and not repair:
        if new.is_dir():
            merge(old, new)
        else:
            os.rename(old, new)
    fixed, left = retarget_links(project, apply)
    notes.append(f"{fixed} link(s) reapontados")
    notes += left
    files = 0
    folder = ".agents" if apply or new.exists() else ".agent"
    for f in text_files(project, hub, folder):
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if apply and refresh_copy(f):
            notes.append(f"{f.relative_to(project)} atualizado com a versão do kit")
            files += 1
            continue
        replaced, n = OLD.subn(".agents", text)
        if n:
            files += 1
            if apply:
                f.write_text(replaced, encoding="utf-8")
    notes.append(f"{files} arquivo(s) de texto")
    if apply:
        dang = dangling(project)
        if dang:
            notes.append(f"LINKS QUEBRADOS: {', '.join(dang[:5])}{' ...' if len(dang) > 5 else ''}")
    return ("reparado" if repair and apply else "migrado" if apply else "simulado"), notes


def main(argv: list[str]) -> int:
    apply, hub = "--apply" in argv, "--hub" in argv
    projects = [Path(a).expanduser().resolve() for a in argv if not a.startswith("--")]
    if not projects:
        print(__doc__)
        return 2
    bad = 0
    for p in projects:
        status, notes = migrate(p, apply, hub)
        print(f"{status:9} {p.name}: " + "; ".join(notes))
        bad += status == "conflito" or any("QUEBRADOS" in n for n in notes)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
