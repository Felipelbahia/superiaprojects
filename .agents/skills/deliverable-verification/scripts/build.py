"""Assemble the single deliverable from its versioned parts (deliverable-verification).

Usage: python3 -I build.py --config verification.json            # write the document
       python3 -I build.py --config verification.json --check    # exit 1 if the file on disk is stale
Never edit the generated file by hand: edit the parts and run this again.
"""

import argparse
import csv
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load_config  # noqa: E402

HEADING = re.compile(r"^(#{1,5}) (.+)$")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
MISSING = "## (missing) "
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
HEADER_LINES = 3  # title, blank line, generated notice: the only place where the date is ignored


def mask_header(text):
    lines = text.split("\n")
    return "\n".join([DATE.sub("DATE", line) for line in lines[:HEADER_LINES]] + lines[HEADER_LINES:])


def demote(text):
    """Push every heading one level down, leaving fenced code blocks untouched."""
    out, fence = [], None  # fence = (char, length) of the open code block, CommonMark-style
    for line in text.splitlines():
        match = FENCE.match(line)
        if match:
            mark = match.group(1)
            if fence is None:
                fence = (mark[0], len(mark))
            elif mark[0] == fence[0] and len(mark) >= fence[1] and not line.strip()[len(mark):].strip():
                fence = None
            out.append(line)
            continue
        out.append(f"#{line}" if fence is None and HEADING.match(line) else line)
    return "\n".join(out)


def csv_table(root, section):
    with open(Path(root) / section["csv"], newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle, delimiter=section.get("delimiter", ",")))
    head, body = rows[0], rows[1:]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    lines += ["| " + " | ".join(cell.replace("|", "/") for cell in row) + " |" for row in body]
    return section.get("title", f"## {section['csv']}") + "\n\n" + "\n".join(lines)


def build(cfg, today=None):
    doc, root = cfg["document"], cfg["_root"]
    stamp = (today or date.today()).isoformat()
    notice = doc.get("notice", "> Generated file ({date}) by `build.py`. Do not edit: edit the parts and rebuild.")
    parts = [doc.get("title", "# Document") + "\n\n" + notice.replace("{date}", stamp)]
    for section in doc["sections"]:
        if isinstance(section, dict):
            name = section["csv"]
            parts.append(csv_table(root, section) if (root / name).exists() else MISSING + name)
            continue
        path = root / section
        parts.append(demote(path.read_text(encoding="utf-8")) if path.exists() else MISSING + section)
    return doc.get("separator", "\n\n---\n\n").join(parts) + "\n"


def is_current(cfg):
    """(ok, evidence): the file on disk equals a fresh build, dates ignored, and no section is missing."""
    output = cfg["_root"] / cfg["document"]["output"]
    if not output.exists():
        return False, f"{cfg['document']['output']} does not exist"
    fresh = build(cfg)
    problems = []
    if mask_header(fresh) != mask_header(output.read_text(encoding="utf-8")):
        problems.append(f"{cfg['document']['output']} is stale (rebuild it, never edit it)")
    missing = [line[len(MISSING):] for line in fresh.splitlines() if line.startswith(MISSING)]
    if missing:
        problems.append("missing sections: " + ", ".join(missing))
    return not problems, "; ".join(problems) or "up to date"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    cfg = load_config(args.config)
    if args.check:
        ok, note = is_current(cfg)
        print(("OK: " if ok else "FAIL: ") + note)
        return 0 if ok else 1
    output = cfg["_root"] / cfg["document"]["output"]
    output.write_text(build(cfg), encoding="utf-8")
    print(f"written {output} ({output.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
