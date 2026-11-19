#!/usr/bin/env python3
"""scope_check.py - the diff stays inside the scope the plan declares (rule: smallest change that does the request).

Usage:
    python3 scope_check.py [PROJECT]            # default: current folder
    python3 scope_check.py PROJECT --plan FILE  # use this plan instead of the newest one with a `Scope:` line
    python3 scope_check.py PROJECT --staged     # only what is staged for the next commit (pre-commit hook)

The plan declares its scope in a line `Scope:` (or `Escopo:`) with paths or globs separated by commas; further lines starting
with `- ` (until a blank line) add more. `*` stays inside a folder, `**` crosses folders, a folder name covers
everything under it. `.agent/plans/`, `inbox/` and `memory.md` are always allowed.
Exit 0: every changed file is in scope, or there is nothing to compare (no git, no plan, no `Scope:` line: a
warning is printed). Exit 1: files outside the scope, named one per line. The owner releases one commit with
ALLOW_SCOPE_DIFF=1 (after saying so in chat; the reason goes in the plan). Standard library only.
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import git_changes  # noqa: E402

ALWAYS = [".agent/plans/", "inbox/", "memory.md"]
SCOPE_LINE = re.compile(r"^\s*(?:Scope|Escopo):\s*(.*)$", re.IGNORECASE)


def parse_scope(text: str):
    """The globs of the first `Scope:` line (plus its `- ` continuation lines), or None when there is none."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        match = SCOPE_LINE.match(line)
        if not match:
            continue
        globs = [g.strip() for g in match.group(1).split(",") if g.strip()]
        for extra in lines[i + 1:]:
            if not extra.strip().startswith("- "):
                break
            globs.append(extra.strip()[2:].strip())
        return globs
    return None


def norm_glob(glob: str) -> str:
    """Trim spaces and a leading `./` only. (str.lstrip("./") would also eat the dot of `.agent/`, `.github/`, `.env.example`.)"""
    glob = glob.strip()
    while glob.startswith("./"):
        glob = glob[2:]
    return glob


def glob_regex(glob: str) -> re.Pattern:
    glob = norm_glob(glob)
    if glob.endswith("/") or "*" not in glob and "?" not in glob:
        glob = glob.rstrip("/") + "/**"
    out, i = "", 0
    while i < len(glob):
        if glob.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif glob.startswith("**", i):
            out, i = out + ".*", i + 2
        elif glob[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif glob[i] == "?":
            out, i = out + "[^/]", i + 1
        else:
            out, i = out + re.escape(glob[i]), i + 1
    return re.compile(out + r"\Z")


def in_scope(path: str, globs: list[str]) -> bool:
    if any(path == a.rstrip("/") or path.startswith(a) for a in ALWAYS):
        return True
    for glob in globs:
        # a file named exactly (no wildcard) also matches itself, not just a folder of that name
        if path == norm_glob(glob) or glob_regex(glob).match(path):
            return True
    return False


def outside_scope(repo: Path, globs: list[str], staged: bool = False) -> list[str]:
    return [p for p in git_changes.changed_paths(repo, staged) if not in_scope(p, globs)]


def newest_plan_with_scope(repo: Path):
    candidates = [p for p in (repo / ".agent" / "plans").rglob("*.md") if p.is_file()]
    for plan in sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            if parse_scope(plan.read_text(encoding="utf-8")) is not None:
                return plan
        except (UnicodeDecodeError, OSError):
            continue
    return None


def main(argv: list[str]) -> int:
    args = [a for a in argv if a != "--staged"]
    staged = "--staged" in argv
    plan = None
    if "--plan" in args:
        i = args.index("--plan")
        plan = Path(args[i + 1])
        del args[i:i + 2]
    repo = Path(args[0] if args else ".").resolve()
    if not git_changes.is_git_repo(repo):
        print(f"scope_check: {repo} is not a git repository, nothing to compare (warning)")
        return 0
    plan = plan or newest_plan_with_scope(repo)
    if plan is None:
        print("scope_check: no plan with a `Scope:` line found under .agent/plans/, nothing to compare (warning)")
        return 0
    globs = parse_scope(plan.read_text(encoding="utf-8"))
    files = outside_scope(repo, globs, staged)
    if not files:
        print(f"scope_check: OK, every changed file is inside the scope of {plan.name}")
        return 0
    if os.environ.get("ALLOW_SCOPE_DIFF") == "1":
        print(f"scope_check: {len(files)} file(s) outside the scope of {plan.name}, released by ALLOW_SCOPE_DIFF=1")
        return 0
    print(f"scope_check: {len(files)} file(s) outside the scope declared in {plan.name}:")
    for path in files:
        print(f"  {path}")
    print("Name them to the owner and say why, or ask for ALLOW_SCOPE_DIFF=1 for this commit.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
