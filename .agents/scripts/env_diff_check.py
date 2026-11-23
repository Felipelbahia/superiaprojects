#!/usr/bin/env python3
"""env_diff_check.py - no local config, .env file, migration/schema or database target slips into a commit.

Usage:
    python3 env_diff_check.py [PROJECT]            # default: current folder
    python3 env_diff_check.py [PROJECT] --staged   # only what is staged for the next commit (pre-commit hook)

Looks at what changed against HEAD (tracked and untracked, never gitignored files):
  - paths: `.env*` and `*.env` (except `.example` / `.sample` / `.template`), local config (`*.local.*`,
    `local_settings.py`, `.mcp.json`), migrations and schema files;
  - added lines: a database connection URL with credentials.
Exit 0: nothing found (or not a git repository: a warning is printed). Exit 1: every finding, one per line.
The owner releases one commit with ALLOW_ENV_DIFF=1 (after saying so in chat; the reason goes in the plan).
Standard library only.
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import git_changes  # noqa: E402

TEMPLATE_SUFFIX = (".example", ".sample", ".template")
MIGRATION_DIRS = {"migrations", "migration"}
SCHEMA_FILES = {"schema.prisma", "schema.sql"}
DB_URL = re.compile(r"\b(postgres(?:ql)?|mysql|mariadb|mongodb(?:\+srv)?|redis|rediss)://[^/\s'\"]*@")


def path_problem(path: str):
    parts = path.split("/")
    name = parts[-1]
    if name.endswith(TEMPLATE_SUFFIX):
        return None
    if name == ".env" or name.startswith(".env.") or name.endswith(".env"):
        return "environment file"
    if name == ".mcp.json" or name == "local_settings.py" or re.search(r"\.local(\.[^/]+)?$", name):
        return "local config"
    if MIGRATION_DIRS & set(parts[:-1]) or name in SCHEMA_FILES:
        return "migration or schema"
    return None


def line_problem(line: str):
    return "database connection URL with credentials" if DB_URL.search(line) else None


def findings(repo: Path, staged: bool = False) -> list[str]:
    out = []
    for path in git_changes.changed_paths(repo, staged):
        problem = path_problem(path)
        if problem:
            out.append(f"{path}: {problem}")
    seen = set()
    for path, line in git_changes.added_lines(repo, staged):
        problem = line_problem(line)
        if problem and (path, problem) not in seen:
            seen.add((path, problem))
            out.append(f"{path}: {problem}")
    return out


def main(argv: list[str]) -> int:
    staged = "--staged" in argv
    argv = [a for a in argv if a != "--staged"]
    repo = Path(argv[0] if argv else ".").resolve()
    if not git_changes.is_git_repo(repo):
        print(f"env_diff_check: {repo} is not a git repository, nothing to compare (warning)")
        return 0
    found = findings(repo, staged)
    if not found:
        print("env_diff_check: OK, no config, environment, migration or database target in the diff")
        return 0
    if os.environ.get("ALLOW_ENV_DIFF") == "1":
        print(f"env_diff_check: {len(found)} finding(s), released by ALLOW_ENV_DIFF=1")
        return 0
    print(f"env_diff_check: {len(found)} finding(s) in the diff:")
    for item in found:
        print(f"  {item}")
    print("Tell the owner before committing. Migrations, schema and production data need explicit OK; "
          "the owner may release one commit with ALLOW_ENV_DIFF=1.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
