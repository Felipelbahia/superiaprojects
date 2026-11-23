#!/usr/bin/env python3
"""render_prompts.py - refresh the local, ready-to-paste copy of the prompt templates.

`prompts-template/` is the versioned original and carries the placeholder <SUPER_IA_PROJECTS_PATH>.
This script writes `projetos/prompts/` (local, not versioned) with the placeholder replaced by the real
path of this kit. It runs on every install, so the copy never falls behind the templates.

    python .agents/scripts/render_prompts.py            # from the kit root, or anywhere (the kit is found from this file)

Files are always overwritten from the template. A file that exists only in the local copy is kept and listed.
The path is written with forward slashes (C:/Users/... on Windows works in Python, bash and PowerShell).
"""

import sys
from pathlib import Path

PLACEHOLDER = "<SUPER_IA_PROJECTS_PATH>"


def render(kit: Path) -> tuple[list[str], list[str]]:
    """Returns (files written, local-only files kept)."""
    source = kit / "prompts-template"
    dest = kit / "projetos" / "prompts"
    if not source.is_dir():
        return [], []
    dest.mkdir(parents=True, exist_ok=True)
    path = kit.resolve().as_posix()
    written = []
    for src in sorted(source.glob("*.md")):
        text = src.read_text(encoding="utf-8").replace(PLACEHOLDER, path)
        (dest / src.name).write_text(text, encoding="utf-8", newline="\n")
        written.append(src.name)
    kept = sorted(p.name for p in dest.glob("*.md") if p.name not in written)
    return written, kept


def main() -> int:
    kit = Path(__file__).resolve().parents[2]
    written, kept = render(kit)
    if not written:
        print("prompts-template/ not found: nothing to render.")
        return 1
    print(f"Prompts atualizados em projetos/prompts/: {len(written)} arquivos (caminho do kit: {kit.resolve().as_posix()})")
    for name in kept:
        print(f"  mantido (só existe na cópia local): {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
