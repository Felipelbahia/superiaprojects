#!/usr/bin/env python3
"""localize_paths.py - point the kit's own docs at the folder where the kit is installed.

The versioned skills, prompts and docs were written on the owner's machine and cite its absolute path of the kit.
On install this script rewrites that path (plain and file:// forms) to the real location of this kit, so the
instructions an AI reads ("read <kit>/.agent/skills/...") work wherever the kit lives (macOS, Linux, Windows).

    python .agent/scripts/localize_paths.py            # rewrite
    python .agent/scripts/localize_paths.py --check    # only report files that still cite another location

Safe to run again: the last location is remembered in `.agent/.kit-path` (git-ignored), so moving the kit to
another folder and running it again also works. Only .md/.txt files are touched; plans, the user's own
`projetos/` and `instalacoes/`, `inbox/arquivo/` and test fixtures are skipped.
"""

import sys
from pathlib import Path
from urllib.parse import quote

KIT = Path(__file__).resolve().parents[2]
OWNER_PATH = "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões"  # where the versioned text was written
MEMO = KIT / ".agent" / ".kit-path"
SKIP_DIRS = {".git", "plans", "projetos", "instalacoes", "arquivo", "fixtures", "node_modules", "__pycache__", "vendor"}
SUFFIXES = {".md", ".txt"}
SKIP_FILES = {"legacy-generic-lines.txt"}  # baseline of OLD text that check_local_rules.py matches literally: data, never rewritten


def targets(kit: Path):
    for p in kit.rglob("*"):
        if p.suffix in SUFFIXES and p.name not in SKIP_FILES and p.is_file() and not (set(p.relative_to(kit).parts[:-1]) & SKIP_DIRS):
            yield p


def pairs(old: str, new: str) -> list[tuple[str, str]]:
    """Ordered replacements. file:// URLs are percent-encoded, plain text is not, and the order matters: a path
    without spaces or accents is identical in both forms, so URLs go first and plain text second."""
    uri_old = old if old.startswith("/") else "/" + old
    uri_new = new if new.startswith("/") else "/" + new
    return [
        ("file://" + quote(uri_old, safe="/:"), "file://" + quote(uri_new, safe="/:")),
        (old, new),
        (quote(old, safe="/"), quote(uri_new, safe="/:")),  # encoded link without a scheme
    ]


def localize(kit: Path = KIT, check_only: bool = False) -> list[Path]:
    new = kit.resolve().as_posix()
    memo = kit / ".agent" / ".kit-path"
    olds = [OWNER_PATH]
    if memo.is_file():
        olds.append(memo.read_text(encoding="utf-8").strip())
    olds = [o for o in dict.fromkeys(olds) if o and o != new]
    changed = []
    for path in targets(kit):
        text = path.read_text(encoding="utf-8", errors="ignore")
        out = text
        for old in olds:
            for a, b in pairs(old, new):
                out = out.replace(a, b)
        if out != text:
            changed.append(path)
            if not check_only:
                path.write_text(out, encoding="utf-8", newline="")
    if not check_only and memo.parent.is_dir():
        memo.write_text(new + "\n", encoding="utf-8")
    return changed


def main() -> int:
    check = "--check" in sys.argv
    changed = localize(KIT, check_only=check)
    verb = "ainda citam outro local" if check else "atualizados para este local"
    print(f"{len(changed)} arquivo(s) {verb} (kit: {KIT.as_posix()})")
    for p in changed[:15]:
        print(f"  {p.relative_to(KIT).as_posix()}")
    if len(changed) > 15:
        print(f"  ... e mais {len(changed) - 15}")
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
