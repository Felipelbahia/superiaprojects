#!/usr/bin/env python3
"""
assemble_rules.py - Build a project's rules file from the kit's rule modules.

Usage (from the project root):
  python3 <kit>/.agent/scripts/assemble_rules.py --modules core,sip-access,code --title "My Project" [--out CLAUDE.md]
  python3 <kit>/.agent/scripts/assemble_rules.py --list

Modules live in .agent/skills/project-initializer/modules/<name>.md. They are concatenated in a
fixed order (never the order given) and every "## " heading outside code fences is numbered.
Then run sync_rules.py to copy the result to GEMINI.md, AGENTS.md and the other rule files.
"""

import argparse
import sys
from pathlib import Path

ORDER = ["core", "sip-access", "code", "interface", "content", "automation"]
DEFAULT_DIR = Path(__file__).resolve().parent.parent / "skills" / "project-initializer" / "modules"


def assemble(names: list[str], title: str, out_name: str, modules_dir: Path) -> str:
    wanted = set(names)
    unknown = wanted - set(ORDER)
    if unknown:
        raise ValueError(f"unknown module(s): {', '.join(sorted(unknown))}. Available: {', '.join(ORDER)}")
    if "core" not in wanted:
        raise ValueError("module 'core' is mandatory")

    lines, number, in_fence = [], 0, False
    for name in (n for n in ORDER if n in wanted):
        for line in (modules_dir / f"{name}.md").read_text(encoding="utf-8").rstrip("\n").split("\n"):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
            elif not in_fence and line.startswith("## "):
                number += 1
                line = f"## {number}. {line[3:]}"
            lines.append(line)
        lines.append("")
    return f"# {out_name} - {title}\n\n" + "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--modules", help="comma-separated module names (core is mandatory)")
    parser.add_argument("--title", default="Project rules")
    parser.add_argument("--out", default="CLAUDE.md")
    parser.add_argument("--modules-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--list", action="store_true", help="print the available modules in assembly order")
    args = parser.parse_args()

    if args.list:
        print("\n".join(ORDER))
        return 0
    if not args.modules:
        parser.error("--modules is required (or use --list)")

    names = [n.strip() for n in args.modules.split(",") if n.strip()]
    out = Path(args.out)
    try:
        text = assemble(names, args.title, out.name, args.modules_dir)
    except ValueError as err:
        print(f"❌ {err}", file=sys.stderr)
        return 2
    out.write_text(text, encoding="utf-8")
    used = [n for n in ORDER if n in names]
    print(f"✅ {out} assembled from: {', '.join(used)}. Next: run sync_rules.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
