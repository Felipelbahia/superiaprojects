#!/usr/bin/env python3
"""
assemble_rules.py - Build a project's rules file from the kit's rule modules.

Usage (from the project root):
  python3 <kit>/.agent/scripts/assemble_rules.py --modules core,sip-access,code --title "My Project" [--out CLAUDE.md]
  python3 <kit>/.agent/scripts/assemble_rules.py --list

Modules live in .agent/skills/project-initializer/modules/<name>.md. They are concatenated in a
fixed order (never the order given) and every "## " heading outside code fences is numbered.
Re-running over a file it assembled keeps the project's ## Project, ## Stack and ## Local rules blocks
and moves other hand-written sections into ## Local rules. Sections of the kit and the text before the first
section are regenerated; local edits there are not kept and are reported. A file from the old model is refused
unless --replace is given (back it up first). Then run sync_rules.py to copy the result to GEMINI.md,
AGENTS.md and the other rule files.
"""

import argparse
import re
import sys
from pathlib import Path

ORDER = ["core", "sip-access", "code", "interface", "content", "automation"]
DEFAULT_DIR = Path(__file__).resolve().parent.parent / "skills" / "project-initializer" / "modules"
MARKER = "Before acting (mandatory sequence)"
KEPT_TITLES = ("Project", "Stack", "Local rules")


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


def fence_states(lines: list[str]) -> list[bool]:
    """For each line: True when it is outside a code fence (fence lines count as inside)."""
    states, in_fence = [], False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            states.append(False)
        else:
            states.append(not in_fence)
    return states


def section_starts(lines: list[str]) -> list[int]:
    return [i for i, (line, outside) in enumerate(zip(lines, fence_states(lines))) if outside and line.startswith("## ")]


def split_sections(text: str) -> list[list[str]]:
    """Split at "## " lines outside code fences. Each section starts with its heading; the preamble is dropped."""
    lines = text.split("\n")
    starts = section_starts(lines)
    ends = starts[1:] + [len(lines)]
    return [lines[start:end] for start, end in zip(starts, ends)]


def preamble(text: str) -> list[str]:
    """The text before the first "## " section, trailing blank lines trimmed."""
    lines = text.split("\n")
    starts = section_starts(lines)
    return trim(lines[:starts[0]] if starts else lines)


def section_title(heading: str) -> str:
    return re.sub(r"^\d+\.\s+", "", heading[3:]).strip()


def trim(lines: list[str]) -> list[str]:
    while lines and not lines[-1].strip():
        lines = lines[:-1]
    return lines


def demote(lines: list[str]) -> list[str]:
    """Move the headings outside code fences one level down (## Deploy -> ### Deploy)."""
    return [("#" + line) if outside and re.match(r"#+ ", line) else line
            for line, outside in zip(lines, fence_states(lines))]


def normalized(section: list[str]) -> list[str]:
    """A section with its heading reduced to "## Title", trailing blank lines trimmed."""
    return trim([f"## {section_title(section[0])}", *section[1:]])


def module_sections(modules_dir: Path) -> dict[str, tuple[str, list[str]]]:
    """Title -> (module name, normalized text) for every "## " section of the module files present in modules_dir."""
    sections = {}
    for name in ORDER:
        path = modules_dir / f"{name}.md"
        if path.is_file():
            for section in split_sections(path.read_text(encoding="utf-8")):
                sections[section_title(section[0])] = (name, normalized(section))
    return sections


def reassemble(existing: str, fresh: str, used: list[str], modules_dir: Path) -> tuple[str, list[str], list[str]]:
    """Fresh module text plus the project's own blocks from an assembled file.
    Returns (text, moved titles, replaced: regenerated sections or preamble whose local text was not kept)."""
    known = module_sections(modules_dir)
    blocks, moved, moved_texts, replaced = {}, [], [], []
    if preamble(existing) != preamble(fresh):
        replaced.append("preamble (text before the first section)")
    for section in split_sections(existing):
        title = section_title(section[0])
        if title in known:
            module, text = known[title]
            if module not in used or normalized(section) != text:
                replaced.append(title)
            continue
        if title in KEPT_TITLES and title not in blocks:
            blocks[title] = "\n".join(trim(section))
        else:
            moved.append(title)
            moved_texts.append("\n".join(trim(demote(section))))

    if "Project" in blocks:
        blocks["Project"] = "\n".join(
            f"- Modules: {', '.join(used)}" if line.lstrip().startswith("- Modules:") else line
            for line in blocks["Project"].split("\n")
        )
    if moved_texts:
        blocks["Local rules"] = "\n\n".join([blocks.get("Local rules", "## Local rules"), *moved_texts])

    text = fresh
    for title in KEPT_TITLES:
        if title in blocks:
            text += "\n" + blocks[title] + "\n"
    return text, moved, replaced


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--modules", help="comma-separated module names (core is mandatory)")
    parser.add_argument("--title", default="Project rules")
    parser.add_argument("--out", default="CLAUDE.md")
    parser.add_argument("--modules-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--replace", action="store_true",
                        help="overwrite a rules file that is not assembled from the kit modules, after you backed it up")
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
        fresh = assemble(names, args.title, out.name, args.modules_dir)
    except ValueError as err:
        print(f"❌ {err}", file=sys.stderr)
        return 2

    existing = out.read_text(encoding="utf-8") if out.exists() else ""
    moved, replaced = [], []
    if not existing.strip():
        text = fresh
    elif MARKER in existing:
        used = [n for n in ORDER if n in names]
        text, moved, replaced = reassemble(existing, fresh, used, args.modules_dir)
    elif args.replace:
        text = fresh
    else:
        print(f"❌ {out} is not assembled from the kit modules (old model). Make a backup, then rerun with --replace.",
              file=sys.stderr)
        return 3

    if moved:
        print(f"⚠️ moved to ## Local rules: {', '.join(moved)}", file=sys.stderr)
    if replaced:
        print(f"⚠️ regenerated from the kit, local text not kept (check the diff with your backup): {', '.join(replaced)}",
              file=sys.stderr)
    out.write_text(text, encoding="utf-8")
    used = [n for n in ORDER if n in names]
    print(f"✅ {out} assembled from: {', '.join(used)}. Next: run sync_rules.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
