#!/usr/bin/env python3
"""resolve_skill.py - find a skill, agent or workflow by name or term, and print where it lives.

Usage:
    python3 resolve_skill.py TERM [TERM ...] [--project DIR] [--kit DIR]

Use it when a skill the rules name is not in the Skill tool's list (`Unknown skill` is not a project error): it answers with the
absolute path to read, so there is no guessing and no `find` by hand.

Looked at, in this order: the project's own `.agents/skills|agents|workflows`; the hubs of the SIPs in the project's
`.agents/SIPS-CONSUMIDOS.md`; the kit; the hubs of the SIPs listed in `<kit>/projetos/_sips.md` that the project did not install.
The manifest is a snapshot taken at install time, so it is used only to find the hubs and to say which SIPs are installed; what a hub
holds is always read from its disk now.

Match: exact name first, then name prefix, then part of the name, then part of the description (every TERM must match).
Output: one line per match `[kind] name - path - origin - description`, then the places searched. A skill of a SIP the project did not
install says so and names that SIP's install prompt. Read the file by the printed path; never copy or link it into the project.

Exit code: 0 found, 1 not found (the places searched are printed), 2 usage error. Standard library only.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sips_status as ss  # noqa: E402

sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import linkutil  # noqa: E402

KINDS = (("skill", "skills"), ("agent", "agents"), ("workflow", "workflows"))
MAX_LINES = 12


def table_hubs(kit: Path) -> list[tuple[str, Path]]:
    """(SIP name, hub) for each row of `<kit>/projetos/_sips.md`."""
    f = kit / "projetos" / "_sips.md"
    out = []
    if f.is_file():
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 4 and cells[0].startswith("`") and cells[2].startswith("`"):
                out.append((cells[1], Path(cells[2].strip("`")).expanduser()))
    return out


def description(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:30]:
            if line.startswith("description:"):
                return line.split(":", 1)[1].strip().strip("\"'")
    except OSError:
        pass
    return ""


def items(base: Path):
    """(kind, name, file) for what lives in `base/.agents/{skills,agents,workflows}`; SIP resolvers and `_` folders are not content."""
    for kind, folder in KINDS:
        d = base / linkutil.adir(base) / folder
        if not d.is_dir():
            continue
        for p in sorted(d.iterdir()):
            name = p.stem if kind != "skill" else p.name
            if name.startswith(("_", ".", "sip-")) or name == "README":
                continue
            f = p / "SKILL.md" if kind == "skill" else p
            if f.is_file() and (kind == "skill" or p.suffix == ".md"):
                yield kind, name, f


def rank(name: str, desc: str, terms: list[str]) -> int | None:
    low_name, low_desc = name.lower(), desc.lower()
    if not all(t in low_name or t in low_desc for t in terms):
        return None
    joined = " ".join(terms)
    if low_name == joined or low_name == "-".join(terms):
        return 0
    if low_name.startswith(terms[0]):
        return 1
    if all(t in low_name for t in terms):
        return 2
    return 3


def install_prompt(hub: Path) -> str:
    found = sorted((hub / "prompts").glob("instalar-skill-sip-*.md")) if (hub / "prompts").is_dir() else []
    return str(found[0]) if found else "(prompt de instalação não encontrado no hub)"


def sources(project: Path, kit: Path) -> list[dict]:
    """Places to search, in order. `origin` is what the output says about each."""
    out = [{"base": project, "origin": "do projeto", "hub": False}]
    seen = {project.resolve()}
    manifest = project / linkutil.adir(project) / "SIPS-CONSUMIDOS.md"
    installed = []
    if manifest.is_file():
        for e in ss.parse_manifest(manifest.read_text(encoding="utf-8", errors="replace")):
            hub = Path(e.get("Hub", "")).expanduser()
            installed.append(hub)
            if hub.resolve() not in seen:
                seen.add(hub.resolve())
                out.append({"base": hub, "origin": f"{e['name']} (instalado neste projeto)", "hub": True})
    if kit.resolve() not in seen:
        seen.add(kit.resolve())
        out.append({"base": kit, "origin": "kit 0 Padrões (não instalado neste projeto)", "hub": True, "install": True})
    for name, hub in table_hubs(kit):
        if hub.resolve() not in seen:
            seen.add(hub.resolve())
            out.append({"base": hub, "origin": f"{name} (não instalado neste projeto)", "hub": True, "install": True})
    return out


def main(argv: list[str]) -> int:
    args = argv[1:]
    if args[:1] in (["-h"], ["--help"]):
        print(__doc__)
        return 0
    project, kit, terms = Path("."), Path(__file__).resolve().parents[2], []
    it = iter(args)
    for a in it:
        if a == "--project":
            project = Path(next(it, "")).expanduser()
        elif a == "--kit":
            kit = Path(next(it, "")).expanduser()
        else:
            terms.append(a.lower())
    if not terms or not project.is_dir() or not kit.is_dir():
        print("uso: resolve_skill.py TERMO [TERMO ...] [--project PASTA] [--kit PASTA] (pastas precisam existir)", file=sys.stderr)
        return 2
    project = project.resolve()
    hits, searched = [], []
    for order, src in enumerate(sources(project, kit)):
        base = src["base"]
        if not base.is_dir():
            searched.append(f"{base}  (hub não encontrado)")
            continue
        searched.append(str(base))
        for kind, name, f in items(base):
            desc = description(f)
            r = rank(name, desc, terms)
            if r is not None:
                hits.append((r, order, kind, name, f, src, desc))
    hits.sort(key=lambda h: (h[0], h[1], h[3]))
    if not hits:
        print(f"skill não encontrada para: {' '.join(terms)}. Procurado em:")
        for s in searched:
            print(f"  - {s}")
        return 1
    for r, _, kind, name, f, src, desc in hits[:MAX_LINES]:
        line = f"[{kind}] {name} - {f} - {src['origin']}"
        if src.get("install"):
            line += f" - para instalar o SIP: {install_prompt(src['base'])}"
        print(line + (f" - {desc[:110]}" if desc else ""))
    if len(hits) > MAX_LINES:
        print(f"... e mais {len(hits) - MAX_LINES} resultados: refine o termo")
    print("Procurado em:")
    for s in searched:
        print(f"  - {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
