#!/usr/bin/env python3
"""build_sip_index.py - Regenerates the item tables (skills, agents, workflows) inside a SIP hub resolver.

Usage (from the hub root, or pass --hub):
    python3 .agent/scripts/build_sip_index.py [--hub <dir>] [--resolver <nome>] [--check]

    --hub <dir>        hub root (default: current directory)
    --resolver <nome>  folder under .agent/skills/ whose SKILL.md holds the tables
                       (default: the only real sip-* folder; error when there are zero or several)
    --check            write nothing; exit 1 when a table is stale

Regions live in the resolver's SKILL.md, one per kind:
    <!-- skills:start (gerado por .agent/scripts/build_sip_index.py — não edite à mão) -->
    ...generated text...
    <!-- skills:end -->
The start line is kept as written. Options go in it as key=value; `group=prefix` groups the items
by the part of the name before the first "-". Kinds: skills, agents, workflows.

Items: .agent/skills/<name>/SKILL.md, .agent/agents/<name>.md, .agent/workflows/<name>.md (top level only).
Excluded: sip-*, names starting with "_" or ".", README.md, and symlinks that resolve outside the hub.

Exit codes: 0 up to date or rewritten, 1 stale under --check, 2 usage, marker or resolver error.
Standard library only (no PyYAML): reads plain, quoted and block (|, >, >-) descriptions.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Tuple

KINDS = ("skills", "agents", "workflows")
HEADERS = {"skills": "Skill", "agents": "Agent", "workflows": "Workflow"}
ALLOWED_OPTIONS = {"group": {"prefix"}}
USAGE = "Uso: build_sip_index.py [--hub <dir>] [--resolver <nome>] [--check]"

START_RE = re.compile(r"^<!--\s*(skills|agents|workflows):start\b(.*?)-->\s*$")
END_RE = re.compile(r"^<!--\s*(skills|agents|workflows):end\s*-->\s*$")
OPTION_RE = re.compile(r"(\w+)=(\S+)")
# Text from "NÃO use" / "Do NOT use" on is the "do not use" part; the table keeps only the trigger part.
NEGATIVE_CUT = re.compile(r"(?:^|\s+)(?:N[ÃA]O use|Do NOT use)\b", re.IGNORECASE)


class UsageError(Exception):
    """A usage, marker or resolver problem: reported on stderr, exit 2."""


class Options(NamedTuple):
    hub: Optional[str]
    resolver: Optional[str]
    check: bool


# ---------- YAML scalar reader (port of Astro's readScalar in lib/frontmatter.mjs) ----------

def read_scalar(fm: str, key: str) -> Optional[str]:
    lines = fm.split("\n")
    key_re = re.escape(key)
    idx = next((i for i, line in enumerate(lines) if re.match(rf"{key_re}\s*:", line)), None)
    if idx is None:
        return None
    rest = re.sub(rf"^{key_re}\s*:\s*", "", lines[idx]).rstrip()
    block = re.match(r"^([>|])([+-]?)\s*$", rest)
    if block:
        body = []
        for line in lines[idx + 1:]:
            if line.strip() == "":
                body.append("")
                continue
            if not line[:1].isspace():
                break
            body.append(line.strip())
        while body and body[-1] == "":
            body.pop()
        text = "\n".join(body) if block.group(1) == "|" else re.sub(r"\s+", " ", " ".join(body))
        return text.strip()
    if rest.startswith('"'):
        m = re.match(r'"((?:[^"\\]|\\.)*)"', rest)
        if not m:
            return None
        return re.sub(r'\\(["\\nt/])', lambda c: {"n": "\n", "t": "\t"}.get(c.group(1), c.group(1)), m.group(1))
    if rest.startswith("'"):
        m = re.match(r"'((?:[^']|'')*)'", rest)
        return m.group(1).replace("''", "'") if m else None
    return re.sub(r"\s+#.*$", "", rest)


def read_frontmatter(path: Path) -> str:
    """Text between the first two '---' lines of the file, or '' when there is no frontmatter."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].rstrip() != "---":
        return ""
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            return "\n".join(lines[1:i])
    return ""


def parse_description(fm: str) -> str:
    return (read_scalar(fm, "description") or "").strip()


def clean_description(desc: str) -> str:
    desc = desc.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")
    cut = NEGATIVE_CUT.search(desc)
    if cut:
        desc = desc[:cut.start()]
    desc = re.sub(r"\s+", " ", desc).strip().replace("|", "\\|")
    return desc or "(sem description)"


# ---------- items ----------

def is_listed(name: str) -> bool:
    return not name.startswith(("sip-", "_", "."))


def is_inside(path: Path, hub_real: str) -> bool:
    real = os.path.realpath(path)
    return real == hub_real or real.startswith(hub_real + os.sep)


def list_items(hub: Path, kind: str) -> List[Tuple[str, str]]:
    """(name, cleaned description) for every item of this kind, sorted by name."""
    base = hub / ".agent" / kind
    if not base.is_dir():
        return []
    hub_real = os.path.realpath(hub)
    if kind == "skills":
        entries = [p for p in base.iterdir() if p.is_dir()]
    else:
        entries = [p for p in base.glob("*.md") if p.is_file() and p.name != "README.md"]
    items = []
    for entry in entries:
        name = entry.name if kind == "skills" else entry.stem
        source = entry / "SKILL.md" if kind == "skills" else entry
        if not is_listed(name) or not source.is_file() or not is_inside(source, hub_real):
            continue
        items.append((name, clean_description(parse_description(read_frontmatter(source)))))
    return sorted(items)


# ---------- rendering ----------

def render_body(kind: str, items: List[Tuple[str, str]], group: Optional[str]) -> List[str]:
    """Lines between the start marker and the end marker (both excluded)."""
    if not items:
        return ["", "Nenhum por enquanto.", ""]

    def cell(name: str) -> str:
        return f"`/{name}`" if kind == "workflows" else f"`{name}`"

    header = f"| {HEADERS[kind]} | Use quando |"
    rows = [f"| {cell(name)} | {desc} |" for name, desc in items]
    out = ["", f"Total: {len(items)}.", ""]
    if group == "prefix":
        by_prefix: Dict[str, List[str]] = {}
        for (name, _), row in zip(items, rows):
            by_prefix.setdefault(name.split("-", 1)[0], []).append(row)
        for prefix in sorted(by_prefix):
            out += [f"### {prefix}", "", header, "| --- | --- |", *by_prefix[prefix], ""]
    else:
        out += [header, "| --- | --- |", *rows, ""]
    return out


# ---------- resolver regions ----------

def parse_options(kind: str, text: str) -> Dict[str, str]:
    options = {}
    for key, value in OPTION_RE.findall(text):
        if key not in ALLOWED_OPTIONS:
            raise UsageError(f"opção desconhecida em {kind}:start: {key}")
        if value not in ALLOWED_OPTIONS[key]:
            raise UsageError(f"valor inválido em {kind}:start: {key}={value}")
        options[key] = value
    return options


def find_regions(lines: List[str]) -> Dict[str, Tuple[int, int, Dict[str, str]]]:
    """kind -> (index of start line, index of its end line, options)."""
    starts: Dict[str, Tuple[int, Dict[str, str]]] = {}
    ends: Dict[str, List[int]] = {}
    for i, line in enumerate(lines):
        start = START_RE.match(line)
        if start:
            kind = start.group(1)
            if kind in starts:
                raise UsageError(f"marcador duplicado: {kind}:start")
            starts[kind] = (i, parse_options(kind, start.group(2)))
            continue
        end = END_RE.match(line)
        if end:
            ends.setdefault(end.group(1), []).append(i)
    regions = {}
    for kind, (start_idx, options) in starts.items():
        after = [e for e in ends.get(kind, []) if e > start_idx]
        if not after:
            raise UsageError(f"falta o marcador <!-- {kind}:end --> depois de {kind}:start")
        regions[kind] = (start_idx, after[0], options)
    return regions


def default_resolver(hub: Path) -> str:
    base = hub / ".agent" / "skills"
    found = sorted(p.name for p in base.glob("sip-*") if p.is_dir() and not p.is_symlink()) if base.is_dir() else []
    if len(found) != 1:
        raise UsageError(f"preciso de exatamente uma pasta sip-* real em {base} (achei {len(found)}); use --resolver <nome>")
    return found[0]


# ---------- CLI ----------

def parse_cli(argv: List[str]) -> Options:
    hub: Optional[str] = None
    resolver: Optional[str] = None
    check = False
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--check":
            check = True
        elif arg in ("--hub", "--resolver"):
            if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
                raise UsageError(f"faltou o valor de {arg}")
            i += 1
            if arg == "--hub":
                hub = argv[i]
            else:
                resolver = argv[i]
        else:
            raise UsageError(f"argumento desconhecido: {arg}")
        i += 1
    return Options(hub, resolver, check)


def run(argv: List[str]) -> int:
    opts = parse_cli(argv)
    hub = Path(opts.hub) if opts.hub is not None else Path.cwd()
    if opts.resolver is not None and ("/" in opts.resolver or opts.resolver in ("", ".", "..")):
        raise UsageError(f"nome de resolver inválido: {opts.resolver!r}")
    resolver = opts.resolver if opts.resolver is not None else default_resolver(hub)
    skill_md = hub / ".agent" / "skills" / resolver / "SKILL.md"
    if not skill_md.is_file():
        raise UsageError(f"resolver não encontrado: {skill_md}")

    raw = skill_md.read_bytes().decode("utf-8")
    eol = "\r" if "\r\n" in raw else ""
    lines = raw.split("\n")
    regions = find_regions(lines)

    plan = []  # (start, end, kind, body) in KINDS order
    for kind in KINDS:
        items = list_items(hub, kind)
        if kind not in regions:
            if items:
                raise UsageError(f"marcadores ausentes para {kind} em {skill_md}: acrescente "
                                 f"<!-- {kind}:start --> e <!-- {kind}:end -->")
            continue
        start, end, options = regions[kind]
        plan.append((start, end, kind, [line + eol for line in render_body(kind, items, options.get("group"))]))

    changed = [kind for start, end, kind, body in plan
               if [line.rstrip("\r") for line in lines[start + 1:end]] != [line.rstrip("\r") for line in body]]
    if not changed:
        print("Sem mudanças.")
        return 0
    if opts.check:
        print(f"Tabelas desatualizadas: {', '.join(changed)} — rode build_sip_index.py", file=sys.stderr)
        return 1

    new_lines = list(lines)
    for start, end, kind, body in sorted(plan, reverse=True):
        new_lines[start + 1:end] = body
    skill_md.write_bytes("\n".join(new_lines).encode("utf-8"))
    print(f"Regiões atualizadas em {skill_md.relative_to(hub).as_posix()}: {', '.join(changed)}")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if any(a in ("-h", "--help") for a in args):
        print(__doc__)
        return 0
    try:
        return run(args)
    except UsageError as err:
        print(f"Erro: {err}", file=sys.stderr)
        print(USAGE, file=sys.stderr)
        return 2
    except (OSError, UnicodeDecodeError) as err:
        print(f"Erro ao ler ou gravar: {err}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
