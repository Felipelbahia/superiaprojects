#!/usr/bin/env python3
"""git_changes.py - what changed in a project's working tree, for scope_check.py and env_diff_check.py.

Changed = tracked files that differ from HEAD (staged or not, deleted included) plus untracked files that
git does not ignore; with staged=True only what is staged for the next commit. Paths are relative to the project folder, so a project inside a bigger repository only
sees its own files. Standard library only.
"""

import subprocess
from pathlib import Path

MAX_UNTRACKED_BYTES = 200_000


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def is_git_repo(repo: Path) -> bool:
    return git(repo, "rev-parse", "--is-inside-work-tree").stdout.strip() == "true"


def has_head(repo: Path) -> bool:
    return git(repo, "rev-parse", "--verify", "-q", "HEAD").returncode == 0


def changed_paths(repo: Path, staged: bool = False) -> list[str]:
    base = ["HEAD"] if has_head(repo) and not staged else ["--cached"]
    tracked = git(repo, "diff", "--relative", "--name-only", "-z", *base).stdout
    untracked = "" if staged else git(repo, "ls-files", "--others", "--exclude-standard", "-z").stdout
    paths = [p for p in (tracked + "\0" + untracked).split("\0") if p]
    return sorted(set(paths))


def added_lines(repo: Path, staged: bool = False) -> list[tuple[str, str]]:
    """(path, line) for every line added to a tracked file, plus every line of small untracked text files."""
    base = ["HEAD"] if has_head(repo) and not staged else ["--cached"]
    out = git(repo, "diff", "--relative", "-U0", "--no-color", *base).stdout
    found, current = [], None
    for line in out.splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else None
        elif line.startswith("+") and current:
            found.append((current, line[1:]))
    untracked = "" if staged else git(repo, "ls-files", "--others", "--exclude-standard", "-z").stdout
    for path in untracked.split("\0"):
        file = repo / path
        if path and file.is_file() and file.stat().st_size <= MAX_UNTRACKED_BYTES:
            try:
                found += [(path, text) for text in file.read_text(encoding="utf-8").splitlines()]
            except (UnicodeDecodeError, OSError):
                pass
    return found
