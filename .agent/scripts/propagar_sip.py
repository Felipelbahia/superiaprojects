#!/usr/bin/env python3
"""propagar_sip.py - after updating a SIP hub, bring every project that consumes it up to date.

Usage:
    python3 propagar_sip.py HUB_DIR                 # simulation (default): shows what would change, writes nothing
    python3 propagar_sip.py HUB_DIR --apply         # applies the safe fixes
    python3 propagar_sip.py HUB_DIR --scan PASTA    # also lists projects under PASTA that consume the hub but are not registered

Projects are found in `<HUB_DIR>/instalacoes/*.md` (field "Caminho absoluto"). For each one, the entry of this hub in its
`.agent/SIPS-CONSUMIDOS.md` is checked (same checks as sips_status.py). With --apply:
  - missing or broken symlinks (resolver, chosen agents/workflows) are recreated; a real file or folder is never touched
    (reported as "conflito");
  - when the links are fine, the manifest date and the hub's `instalacoes/<projeto>.md` "Última atualização" become today;
  - agents/workflows that are new in the hub are NOT installed: one note per project goes to its `inbox/`
    (`NNN-<resolver>-novidades.md`, rewritten on reruns) so the owner decides item by item;
  - `sync_entrypoints.py --check` runs inside each project and its result is shown (simulation: "não verificado").
Cover mode (`--cobrir --fichas PASTA_DAS_FICHAS`, e.g. for sip-geral that every project should have):
  - the universe is the hub's `instalacoes/` plus the paths in the project cards ("Repositório / Caminho" in `PASTA/*.md`),
    minus the parent folders listed in `PASTA/_pastas-mae.txt` (one absolute path per line, `#` comments) and the hub itself;
  - a project of the universe with no entry of this hub gets the resolver installed (dual symlinks, .gitignore lines,
    manifest entry, `instalacoes/` record), with NO agents/workflows chosen; "Vistos no hub" records the hub as seen today;
  - an entry in the old format (chosen items that no longer exist in the hub, unreadable "Vistos no hub") is migrated:
    missing chosen names are dropped and "Vistos no hub" is rewritten with the hub as it is today.
  With --scan PASTA too, projects found there that already consume the hub (manifest entry) but are not registered join the
  universe (registry file created, entry migrated).
  Without --apply it only simulates, as always.
All hubs (`--todos [--apply]`): runs the command above once per hub listed in `projetos/_sips.md` (column "Hub"), one after
  the other, and prints a final table. The kit's own hub (sip-geral) runs in cover mode with `projetos/` as the cards folder and
  the folder two levels above the kit as the scan root; every other hub runs plain. `--sips ARQUIVO` and `--kit PASTA`
  override the table file and the kit folder (tests).
Exit code: 0 all up to date, 1 something pending, 2 usage error. Standard library only.
"""

import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import linkutil  # noqa: E402
import sips_status as ss  # noqa: E402

HERE = Path(__file__).resolve().parent
REG_PATH = re.compile(r"^## Caminho absoluto\s*\n(.+)$|^- Projeto:\s*(/.+)$", re.M)  # new and old registry formats


def registry(hub: Path) -> list[tuple[str, Path]]:
    out = []
    folder = hub / "instalacoes"
    if folder.is_dir():
        for f in sorted(folder.glob("*.md")):
            if f.name == "README.md":
                continue
            m = REG_PATH.search(f.read_text(encoding="utf-8", errors="replace"))
            if m:
                out.append((f.stem, Path((m.group(1) or m.group(2)).strip()).expanduser()))
    return out


def same(a: Path, b: Path) -> bool:
    try:
        return a.resolve() == b.resolve()
    except OSError:
        return False


def find_entry(project: Path, hub: Path) -> dict | None:
    manifest = project / ".agent" / "SIPS-CONSUMIDOS.md"
    if not manifest.is_file():
        return None
    for e in ss.parse_manifest(manifest.read_text(encoding="utf-8", errors="replace")):
        if same(Path(e.get("Hub", "")).expanduser(), hub):
            return e
    return None


def desired_links(project: Path, hub: Path, e: dict) -> tuple[list[tuple[Path, str]], list[str]]:
    """((link path, target) for every link the manifest says should exist, chosen items that left the hub)."""
    resolver = e["resolver"]
    single = ss.is_single_link(project, resolver)
    out: list[tuple[Path, str]] = []
    removed: list[str] = []
    skill_target = str(linkutil.resolver_dir(hub, resolver))
    if single:
        out.append((project / ".claude" / "skills" / resolver, skill_target))
    else:
        out.append((project / ".agent" / "skills" / resolver, skill_target))
        out.append((project / ".claude" / "skills" / resolver, f"../../.agent/skills/{resolver}"))
    for kind, claude_dir in (("agents", "agents"), ("workflows", "commands")):
        for n in ss.names(e.get("Agents" if kind == "agents" else "Workflows", "")):
            hub_file = str(hub / ".agent" / kind / f"{n}.md")
            if not Path(hub_file).exists():
                removed.append(f"{kind[:-1]} {n}")
                continue
            if single:
                out.append((project / ".claude" / claude_dir / f"{n}.md", hub_file))
                continue
            out.append((project / ".agent" / kind / f"{n}.md", hub_file))
            out.append((project / ".claude" / claude_dir / f"{n}.md", f"../../.agent/{kind}/{n}.md"))
            cursor = project / ".cursor" / "commands" / f"{n}.md"
            if kind == "workflows" and os.path.lexists(cursor):
                out.append((cursor, f"../../.agent/{kind}/{n}.md"))
    return out, removed


def plan_links(links: list[tuple[Path, str]], hub: Path) -> tuple[list[tuple[Path, str]], list[str]]:
    fixes, conflicts = [], []
    for link, target in links:
        if not os.path.lexists(link):
            fixes.append((link, target))
        elif link.is_symlink():
            if ss.link_problem(link, hub, (link.parent / target).resolve()):
                fixes.append((link, target))
        elif (state := linkutil.managed_state(link, (link.parent / target).resolve())) is not None:
            if state == "stale":
                fixes.append((link, target))
        else:
            conflicts.append(f"conflito: {link} é arquivo/pasta real; não alterado (use o prompt de instalação do SIP)")
    return fixes, conflicts


def apply_fixes(fixes: list[tuple[Path, str]]) -> None:
    for link, target in fixes:  # parents first: .agent links come before the .claude ones that point to them
        link.parent.mkdir(parents=True, exist_ok=True)
        if link.is_symlink():
            link.unlink()
        elif linkutil.managed_state(link, (link.parent / target).resolve()) == "stale":
            linkutil.remove_managed(link.parent, link.name)
        linkutil.make_link(link, target, (link.parent / target).resolve())


def set_manifest_date(manifest: Path, resolver: str, today: str) -> None:
    lines = manifest.read_text(encoding="utf-8").splitlines(keepends=True)
    inside = False
    for i, line in enumerate(lines):
        m = ss.ENTRY.match(line.rstrip("\n"))
        if m:
            inside = m.group(2) == resolver
        elif inside and line.startswith("- Instalado/atualizado em:"):
            lines[i] = f"- Instalado/atualizado em: {today}\n"
    manifest.write_text("".join(lines), encoding="utf-8")


def set_registry_date(hub: Path, name: str, today: str) -> None:
    f = hub / "instalacoes" / f"{name}.md"
    if not f.is_file():
        return
    text = f.read_text(encoding="utf-8")
    new = re.sub(r"(## Última atualização\s*\n)[^\n]*", rf"\g<1>{today}", text, count=1)
    if new != text:
        f.write_text(new, encoding="utf-8")


def news(hub: Path, e: dict) -> tuple[dict, dict, bool]:
    """(new in hub, chosen-by-project but gone from hub, seen-list unreadable).

    Items that left the hub only matter when the project chose them. A "Vistos no hub" list where none of the
    names exist in the hub any more is an old-format record: nothing can be said about what is new, so it is
    reported as unverified instead of listing the whole hub as news.
    """
    seen_a, seen_w = ss.seen_in_hub(e.get("Vistos no hub", ""))
    chosen = {"agents": ss.names(e.get("Agents", "")), "workflows": ss.names(e.get("Workflows", ""))}
    new, gone, unreadable = {}, {}, False
    for kind, seen in (("agents", seen_a), ("workflows", seen_w)):
        now = ss.hub_items(hub, kind)
        if "Vistos no hub" not in e:
            continue
        if seen and not (set(seen) & now):
            unreadable = True
            continue
        new[kind] = sorted(now - set(seen))
        gone[kind] = sorted(set(chosen[kind]) - now)
    return new, gone, unreadable


def next_number(inbox: Path) -> int:
    nums = [int(m.group(1)) for d in (inbox, inbox / "arquivo") if d.is_dir()
            for f in d.glob("*.md") if (m := re.match(r"(\d+)-", f.name))]
    return max(nums, default=0) + 1


def write_note(project: Path, hub: Path, e: dict, new: dict, gone: dict, today: str) -> Path:
    inbox = project / "inbox"
    inbox.mkdir(exist_ok=True)
    resolver = e["resolver"]
    existing = sorted(inbox.glob(f"*-{resolver}-novidades.md"))
    path = existing[0] if existing else inbox / f"{next_number(inbox):03d}-{resolver}-novidades.md"
    num = path.name.split("-", 1)[0]
    fmt = lambda d: "; ".join(f"{k}: {', '.join(v)}" for k, v in d.items() if v) or "nenhum"  # noqa: E731
    path.write_text(
        f"# {num} — Novidades do hub {e['name']}\n"
        f"Status: na inbox · Aberto em: {today} · Pedido por: propagar_sip.py · Projeto de origem: {e['name']} ({hub})\n\n"
        f"## O quê\nNovos no hub e ainda não oferecidos aqui: {fmt(new)}.\nSaíram do hub: {fmt(gone)}.\n\n"
        f"## Como (o que fazer quando for pedido)\nMostrar nome e \"use quando\" de cada item novo (tabelas do resolver `{resolver}`) e "
        f"perguntar quais instalar. Depois seguir o prompt da linha \"Para atualizar\" do `.agent/SIPS-CONSUMIDOS.md` "
        f"(registra em \"Vistos no hub\"). Itens que saíram: remover só o symlink, com o ok do dono.\n\n"
        f"## Onde\n`{linkutil.resolver_dir(hub, resolver)}/SKILL.md` e `.agent/SIPS-CONSUMIDOS.md` deste projeto.\n\n"
        f"## Por quê\nO hub mudou; sem decisão, os itens novos ficam de fora (padrão do prompt de instalação).\n\n"
        f"## Para quê\n`sips_status.py` sai sem \"novos no hub\" para este SIP.\n\n"
        f"## Quem\nDono do projeto decide; o Claude da sessão aplica.\n\n"
        f"## Efeitos e impactos\nNada muda até a decisão.\n",
        encoding="utf-8",
    )
    return path


def sync_check(project: Path) -> str:
    try:
        r = subprocess.run([sys.executable, str(HERE / "sync_entrypoints.py"), "--check"], cwd=project,
                           capture_output=True, text=True, timeout=120, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"falhou ({exc})"
    return "ok" if r.returncode == 0 else f"falhou (código {r.returncode}): {(r.stdout + r.stderr).strip().splitlines()[-1:]}"


FICHA_PATH = re.compile(r"Repositório\s*/\s*Caminho(?: Raiz)?:\*\*\s*(?:`([^`\n]+)`|(\S[^\n]*?)\s*$)", re.M)


def ficha_paths(fichas: Path) -> list[Path]:
    out = []
    for f in sorted(fichas.glob("*.md")):
        if f.name.startswith("_") or f.name in ("README.md", "TEMPLATE.md"):
            continue
        m = FICHA_PATH.search(f.read_text(encoding="utf-8", errors="replace"))
        if m:
            out.append(Path((m.group(1) or m.group(2)).strip()).expanduser())
    return out


def mother_folders(fichas: Path) -> list[Path]:
    f = fichas / "_pastas-mae.txt"
    if not f.is_file():
        return []
    return [Path(line.strip()).expanduser() for line in f.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")]


def seen_line(hub: Path) -> str:
    fmt = lambda kind: ", ".join(sorted(ss.hub_items(hub, kind))) or "nenhum"  # noqa: E731
    return f"agents {fmt('agents')}; workflows {fmt('workflows')}"


def template_entry(hub: Path, regs: list[tuple[str, Path]], resolver: str) -> dict | None:
    """name and 'Para atualizar' of this hub, copied from the first consumer that already has an entry."""
    for _, proj in regs:
        e = find_entry(proj, hub) if proj.is_dir() else None
        if e and e["resolver"] == resolver:
            return e
    return None


def edit_block(manifest: Path, resolver: str, edit) -> None:
    """Applies edit(line) -> line to every line of the entry whose resolver matches."""
    lines = manifest.read_text(encoding="utf-8").splitlines(keepends=True)
    inside = False
    for i, line in enumerate(lines):
        m = ss.ENTRY.match(line.rstrip("\n"))
        if m:
            inside = m.group(2) == resolver
        elif inside:
            lines[i] = edit(line)
    manifest.write_text("".join(lines), encoding="utf-8")


def migrate_old(hub: Path, project: Path, e: dict, apply: bool, tmpl: dict | None = None) -> bool:
    """Old-format entry: drop chosen items that no longer exist in the hub, rewrite 'Vistos no hub'. True if it changed."""
    changes = []
    drops = {}
    for field, kind in (("Agents", "agents"), ("Workflows", "workflows")):
        now = ss.hub_items(hub, kind)
        chosen = ss.names(e.get(field, ""))
        keep = [n for n in chosen if n in now]
        if keep != chosen:
            drops[field] = keep
            changes.append(f"{field}: tirar {', '.join(sorted(set(chosen) - set(keep)))} (não existe mais no hub)")
    seen_a, seen_w = ss.seen_in_hub(e.get("Vistos no hub", ""))
    unreadable = bool(seen_a or seen_w) and not (set(seen_a) & ss.hub_items(hub, "agents") or set(seen_w) & ss.hub_items(hub, "workflows"))
    if unreadable:
        changes.append("Vistos no hub: reescrever com o hub de hoje (nada novo é instalado)")
    add_update = bool(tmpl and tmpl.get("Para atualizar") and not e.get("Para atualizar"))
    if add_update:
        changes.append("Para atualizar: acrescentar a linha que faltava")
    for c in changes:
        print(f"  - {'migrar' if apply else 'migraria'} registro antigo: {c}")
    if apply and changes:
        def edit(line: str) -> str:
            for field, keep in drops.items():
                if line.startswith(f"- {field}:"):
                    return f"- {field}: {', '.join(keep) if keep else 'nenhum'}\n"
            if unreadable and line.startswith("- Vistos no hub:"):
                return f"- Vistos no hub: {seen_line(hub)}\n"
            return line
        manifest = project / ".agent" / "SIPS-CONSUMIDOS.md"
        edit_block(manifest, e["resolver"], edit)
        if add_update:
            lines = manifest.read_text(encoding="utf-8").splitlines(keepends=True)
            inside, last = False, None
            for i, line in enumerate(lines):
                m = ss.ENTRY.match(line.rstrip("\n"))
                if m:
                    inside = m.group(2) == e["resolver"]
                if inside and line.strip():
                    last = i
            if last is not None:
                lines[last] = lines[last].rstrip("\n") + "\n"
                lines.insert(last + 1, f"- Para atualizar: {tmpl['Para atualizar']}\n")
                manifest.write_text("".join(lines), encoding="utf-8")
    return bool(changes)


def write_registry(hub: Path, name: str, project: Path, resolver: str, today: str) -> None:
    reg = hub / "instalacoes" / f"{name}.md"
    reg.parent.mkdir(exist_ok=True)
    reg.write_text(f"## Projeto\n{name}\n\n## Caminho absoluto\n{project}\n\n## Instalado em\n{today}\n\n"
                   f"## Última atualização\n{today}\n\n## Recursos instalados\n- Skill: {resolver} (sempre)\n"
                   f"- Agents: nenhum\n- Workflows: nenhum\n", encoding="utf-8")


def install_missing(hub: Path, name: str, project: Path, tmpl: dict, apply: bool, today: str) -> bool:
    """Installs the resolver only. Returns True when something is still pending (conflict)."""
    resolver = tmpl["resolver"]
    e = {"resolver": resolver, "name": tmpl["name"], "Agents": "nenhum", "Workflows": "nenhum"}
    links, _ = desired_links(project, hub, e)
    fixes, conflicts = plan_links(links, hub)
    for link, target in fixes:
        print(f"  - {'criar' if apply else 'criaria'} link {link.relative_to(project)} -> {target}")
    for c in conflicts:
        print(f"  - {c}")
    if conflicts:
        return True
    ignore_lines = [str(l.relative_to(project)) for l, _ in links]
    print(f"  - {'registrar' if apply else 'registraria'}: .gitignore, .agent/SIPS-CONSUMIDOS.md e {hub.name}/instalacoes/{name}.md")
    if not apply:
        return True
    apply_fixes(fixes)
    gi = project / ".gitignore"
    have = gi.read_text(encoding="utf-8").splitlines() if gi.is_file() else []
    add = [l for l in ignore_lines if l not in have]
    if add:
        prefix = "" if not have or gi.read_text(encoding="utf-8").endswith("\n") else "\n"
        gi.write_text((gi.read_text(encoding="utf-8") if gi.is_file() else "") + prefix
                      + f"\n# symlinks do {tmpl['name']} (caminho absoluto desta máquina)\n" + "\n".join(add) + "\n", encoding="utf-8")
    manifest = project / ".agent" / "SIPS-CONSUMIDOS.md"
    (project / ".agent").mkdir(exist_ok=True)
    block = (f"## {tmpl['name']} (`{resolver}`)\n- Hub: {hub}\n- Instalado/atualizado em: {today}\n- Skill: {resolver}\n"
             f"- Agents: nenhum\n- Workflows: nenhum\n- Vistos no hub: {seen_line(hub)}\n- Conflitos: nenhum\n"
             f"- Para atualizar: {tmpl.get('Para atualizar', '')}\n")
    text = manifest.read_text(encoding="utf-8") if manifest.is_file() else "# SIPs consumidos por este projeto\n"
    manifest.write_text(text.rstrip("\n") + "\n\n" + block, encoding="utf-8")
    write_registry(hub, name, project, resolver, today)
    return False


def handle(hub: Path, name: str, project: Path, apply: bool, today: str, cover: bool = False, tmpl: dict | None = None) -> bool:
    """Returns True when something is still pending for this project."""
    print(f"\n# {name}  ({project})")
    if not project.is_dir():
        print("  - projeto não existe em disco: registro de instalacoes/ desatualizado")
        return True
    e = find_entry(project, hub)
    if e is None and cover and tmpl is not None:
        pend = install_missing(hub, name, project, tmpl, apply, today)
        if apply:
            result = sync_check(project)
            print(f"  - sync_entrypoints: {result}")
            return pend or not result.startswith("ok")
        print("  - sync_entrypoints: não verificado (simulação)")
        return True
    if e is None:
        print("  - sem entrada deste hub no manifesto (.agent/SIPS-CONSUMIDOS.md): instale/atualize pelo prompt do SIP")
        return True
    pending = False
    migrated = migrate_old(hub, project, e, apply, tmpl) if cover else False
    if apply and migrated:
        e = find_entry(project, hub) or e
    links, removed = desired_links(project, hub, e)
    fixes, conflicts = plan_links(links, hub)
    for r in removed:
        print(f"  - {r} escolhido pelo projeto saiu do hub: remover o link com o ok do dono")
        pending = True
    for link, target in fixes:
        print(f"  - {'recriar' if apply else 'recriaria'} link {link.relative_to(project)} -> {target}")
    for c in conflicts:
        print(f"  - {c}")
        pending = True
    if apply:
        apply_fixes(fixes)
    new, gone, unreadable = news(hub, e)
    if unreadable:
        print("  - novidades não verificadas: \"Vistos no hub\" em formato antigo (rode o prompt de instalação do SIP uma vez)")
    if any(new.values()) or any(gone.values()):
        pending = True
        where = project / "inbox"
        if apply:
            note = write_note(project, hub, e, new, gone, today)
            print(f"  - novidades do hub (não instaladas): nota em {note.relative_to(project)}")
        else:
            print(f"  - novidades do hub (não seriam instaladas), nota em inbox/ seria escrita: {where}")
        for kind in ("agents", "workflows"):
            if new.get(kind):
                print(f"      novos {kind}: {', '.join(new[kind])}")
            if gone.get(kind):
                print(f"      saíram {kind}: {', '.join(gone[kind])}")
    if apply and cover and not (hub / "instalacoes" / f"{name}.md").is_file():
        write_registry(hub, name, project, e["resolver"], today)
        print("  - registro criado em instalacoes/ (o projeto consumia o hub sem estar registrado)")
    if apply:
        if not conflicts:
            set_manifest_date(project / ".agent" / "SIPS-CONSUMIDOS.md", e["resolver"], today)
            set_registry_date(hub, name, today)
            print(f"  - data do manifesto e do registro: {today}")
        result = sync_check(project)
        print(f"  - sync_entrypoints: {result}")
        pending = pending or not result.startswith("ok")
    else:
        print("  - sync_entrypoints: não verificado (simulação)")
        pending = pending or bool(fixes) or migrated
    if not pending and not fixes:
        print("  - em dia")
    return pending


def scan(hub: Path, parent: Path, registered: list[Path]) -> bool:
    print(f"\n# varredura em {parent}")
    found = False
    for proj in ss.find_projects(parent):
        if find_entry(proj, hub) and not any(same(proj, r) for r in registered):
            print(f"  - {proj} consome o hub mas não está em instalacoes/")
            found = True
    if not found:
        print("  - nenhuma divergência")
    return found


def hubs_from_table(sips: Path) -> list[Path]:
    hubs = []
    for line in sips.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[0].startswith("`") and cells[2].startswith("`"):
            hubs.append(Path(cells[2].strip("`")).expanduser())
    return hubs


def run_all(args: list[str]) -> int:
    def opt(name: str, default: Path) -> Path:
        if name in args:
            i = args.index(name)
            return Path(args[i + 1]).expanduser() if i + 1 < len(args) else default
        return default
    kit = opt("--kit", HERE.parent.parent)
    sips = opt("--sips", kit / "projetos" / "_sips.md")
    if not sips.is_file():
        print(f"tabela de SIPs não encontrada: {sips}", file=sys.stderr)
        return 2
    apply = ["--apply"] if "--apply" in args else []
    rows = []
    for hub in hubs_from_table(sips):
        extra = ["--cobrir", "--fichas", str(kit / "projetos"), "--scan", str(kit.parent.parent)] if same(hub, kit) else []
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), str(hub), *apply, *extra],
                           capture_output=True, text=True, check=False)
        print(r.stdout, end="")
        if r.stderr:
            print(r.stderr, end="", file=sys.stderr)
        summary = next((l for l in reversed(r.stdout.splitlines()) if l.startswith("Resumo:")), "sem resumo")
        rows.append((hub.name, r.returncode, summary))
    print("\n== Todos os hubs ==")
    for name, rc, summary in rows:
        print(f"  [{'ok' if rc == 0 else 'pendência' if rc == 1 else 'erro'}] {name}: {summary}")
    return 2 if any(rc == 2 for _, rc, _ in rows) else (1 if any(rc for _, rc, _ in rows) else 0)


def main(argv: list[str]) -> int:
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if args else 2
    if "--todos" in args:
        return run_all(args)
    apply = "--apply" in args
    scan_dir = None
    if "--scan" in args:
        i = args.index("--scan")
        if i + 1 >= len(args):
            print("--scan precisa de uma pasta", file=sys.stderr)
            return 2
        scan_dir = Path(args[i + 1]).expanduser()
        args = args[:i] + args[i + 2:]
    cover = "--cobrir" in args
    fichas = None
    if "--fichas" in args:
        i = args.index("--fichas")
        if i + 1 >= len(args):
            print("--fichas precisa de uma pasta", file=sys.stderr)
            return 2
        fichas = Path(args[i + 1]).expanduser()
        args = args[:i] + args[i + 2:]
    if cover and (fichas is None or not fichas.is_dir()):
        print("--cobrir precisa de --fichas PASTA (as fichas dos projetos)", file=sys.stderr)
        return 2
    args = [a for a in args if a not in ("--apply", "--cobrir")]
    # absolute on purpose: the hub path is written into every project link, a relative one would break them
    hub = Path(os.path.abspath(Path(args[0]).expanduser())) if args else Path("")
    if not args or not hub.is_dir():
        print(f"hub não existe: {hub}", file=sys.stderr)
        return 2
    regs = registry(hub)
    if not regs:
        print(f"nenhum projeto em {hub}/instalacoes/ (ou a pasta não existe)", file=sys.stderr)
    print(f"Hub: {hub}  |  modo: {'APLICAR' if apply else 'simulação (nada é gravado; use --apply)'}")
    today = date.today().isoformat()
    tmpl = None
    if cover:
        resolvers = sorted({e["resolver"] for _, p in regs if p.is_dir() and (e := find_entry(p, hub))})
        tmpl = template_entry(hub, regs, resolvers[0]) if resolvers else None
        if tmpl is None:
            print("--cobrir: nenhum consumidor com entrada deste hub para servir de modelo", file=sys.stderr)
            return 2
        have = [p for _, p in regs]
        skip = mother_folders(fichas) + [hub]
        for p in ficha_paths(fichas):
            if p.is_dir() and not any(same(p, r) for r in have) and not any(same(p, m) for m in skip):
                regs.append((p.name, p))
                have.append(p)
        if scan_dir is not None:
            for p in ss.find_projects(scan_dir):
                if find_entry(p, hub) and not any(same(p, r) for r in have) and not any(same(p, m) for m in skip):
                    regs.append((p.name, p))
                    have.append(p)
    pending = [handle(hub, n, p, apply, today, cover, tmpl) for n, p in regs]
    if scan_dir is not None:
        pending.append(scan(hub, scan_dir, [p for _, p in regs]))
    print(f"\nResumo: {len(regs)} projeto(s), {sum(pending)} com pendência.")
    return 1 if any(pending) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
