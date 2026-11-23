#!/usr/bin/env python3
"""avisar_projetos_inbox.py - leave one inbox note, from a template file, in every project that consumes the kit.

Usage:
    python3 avisar_projetos_inbox.py --nota MODELO.md --slug ASSUNTO            # simulation (default): writes nothing
    python3 avisar_projetos_inbox.py --nota MODELO.md --slug ASSUNTO --apply    # writes/refreshes the notes
    (optional: --hub PASTA_DO_KIT, default: this kit)

MODELO.md is the note in the format of `inbox/README.md`, with these markers (plain text replacement, so other braces
are safe): {num} the note label (GERAL-NNN), {projeto} the project name, {hub} the kit path, {data} today (AAAA-MM-DD).
Ready-made templates live in `prompts-template/inbox-notas/`.

Projects come from `<kit>/instalacoes/*.md` (field "Caminho absoluto", same source as propagar_sip.py). Each one gets
`inbox/GERAL-NNN-<slug>.md` (GERAL = left by the kit; own sequence counting inbox/arquivo/; an existing note of this slug,
numbered the old way or not, is rewritten in place, so reruns do not pile up). Nothing else in the project is touched: the owner decides what to do with the note. The kit
itself, projects whose folder is missing and projects that already archived a note of this slug (inbox/arquivo/: the
owner dealt with it) are skipped and reported. Standard library only.
"""

import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import propagar_sip  # noqa: E402

KIT = Path(__file__).resolve().parent.parent.parent
SLUG_OK = re.compile(r"[a-z0-9][a-z0-9-]*\Z")


def render(template: str, num: str, project: str, hub: Path, today: str) -> str:
    for marker, value in (("{num}", num), ("{projeto}", project), ("{hub}", str(hub)), ("{data}", today)):
        template = template.replace(marker, value)
    return template


def run(hub: Path, template: str, slug: str, apply: bool, today: str) -> list[tuple[str, str, str]]:
    rows = []
    for name, project in propagar_sip.registry(hub):
        if project.resolve() == hub.resolve():
            rows.append((name, str(project), "ignorado: é o próprio kit"))
            continue
        if not project.is_dir():
            rows.append((name, str(project), "pasta não encontrada"))
            continue
        inbox = project / "inbox"
        if (inbox / "arquivo").is_dir() and any((inbox / "arquivo").glob(f"*-{slug}.md")):
            rows.append((name, str(project), "já resolvido (nota em inbox/arquivo/): pulado"))
            continue
        existing = sorted(inbox.glob(f"*-{slug}.md")) if inbox.is_dir() else []
        if existing:
            path, action = existing[0], "atualizar"
        else:
            path, action = inbox / f"GERAL-{propagar_sip.next_geral_number(inbox):03d}-{slug}.md", "criar"
        if apply:
            inbox.mkdir(exist_ok=True)
            path.write_text(render(template, propagar_sip.note_label(path), name, hub, today), encoding="utf-8")
        rows.append((name, str(project), f"{action}: inbox/{path.name}"))
    return rows


def option(argv: list[str], name: str):
    return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else None


def main(argv: list[str]) -> int:
    nota, slug = option(argv, "--nota"), option(argv, "--slug")
    if not nota or not slug:
        print("uso: avisar_projetos_inbox.py --nota MODELO.md --slug ASSUNTO [--apply] [--hub PASTA]")
        return 2
    if not SLUG_OK.match(slug):
        print(f"--slug inválido: {slug!r} (minúsculas, números e hífen)")
        return 2
    if not Path(nota).is_file():
        print(f"modelo de nota não encontrado: {nota}")
        return 2
    apply = "--apply" in argv
    hub = Path(option(argv, "--hub")).resolve() if option(argv, "--hub") else KIT
    rows = run(hub, Path(nota).read_text(encoding="utf-8"), slug, apply, datetime.date.today().isoformat())
    for name, _, action in rows:
        print(f"{name}\t{action}")
    done = sum(1 for _, _, a in rows if a.startswith(("criar", "atualizar")))
    print(f"\n{done} nota(s) {'gravada(s)' if apply else 'seriam gravadas (simulação; use --apply)'}; "
          f"{len(rows) - done} ignorado(s)/sem pasta.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
