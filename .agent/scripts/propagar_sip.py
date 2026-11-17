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
Exit code: 0 all up to date, 1 something pending, 2 usage error. Standard library only.
"""

import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sips_status as ss  # noqa: E402

HERE = Path(__file__).resolve().parent
REG_PATH = re.compile(r"^## Caminho absoluto\s*\n(.+)$", re.M)


def registry(hub: Path) -> list[tuple[str, Path]]:
    out = []
    folder = hub / "instalacoes"
    if folder.is_dir():
        for f in sorted(folder.glob("*.md")):
            if f.name == "README.md":
                continue
            m = REG_PATH.search(f.read_text(encoding="utf-8", errors="replace"))
            if m:
                out.append((f.stem, Path(m.group(1).strip()).expanduser()))
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
    skill_target = str(hub / ".agent" / "skills" / resolver)
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
            if ss.link_problem(link, hub):
                fixes.append((link, target))
        else:
            conflicts.append(f"conflito: {link} é arquivo/pasta real; não alterado (use o prompt de instalação do SIP)")
    return fixes, conflicts


def apply_fixes(fixes: list[tuple[Path, str]]) -> None:
    for link, target in fixes:  # parents first: .agent links come before the .claude ones that point to them
        link.parent.mkdir(parents=True, exist_ok=True)
        if link.is_symlink():
            link.unlink()
        os.symlink(target, link)


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
        f"## Onde\n`{hub}/.agent/skills/{resolver}/SKILL.md` e `.agent/SIPS-CONSUMIDOS.md` deste projeto.\n\n"
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


def handle(hub: Path, name: str, project: Path, apply: bool, today: str) -> bool:
    """Returns True when something is still pending for this project."""
    print(f"\n# {name}  ({project})")
    if not project.is_dir():
        print("  - projeto não existe em disco: registro de instalacoes/ desatualizado")
        return True
    e = find_entry(project, hub)
    if e is None:
        print("  - sem entrada deste hub no manifesto (.agent/SIPS-CONSUMIDOS.md): instale/atualize pelo prompt do SIP")
        return True
    pending = False
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
        pending = pending or bool(fixes)
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


def main(argv: list[str]) -> int:
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if args else 2
    apply = "--apply" in args
    scan_dir = None
    if "--scan" in args:
        i = args.index("--scan")
        if i + 1 >= len(args):
            print("--scan precisa de uma pasta", file=sys.stderr)
            return 2
        scan_dir = Path(args[i + 1]).expanduser()
        args = args[:i] + args[i + 2:]
    args = [a for a in args if a != "--apply"]
    hub = Path(args[0]).expanduser() if args else Path("")
    if not args or not hub.is_dir():
        print(f"hub não existe: {hub}", file=sys.stderr)
        return 2
    regs = registry(hub)
    if not regs:
        print(f"nenhum projeto em {hub}/instalacoes/ (ou a pasta não existe)", file=sys.stderr)
    print(f"Hub: {hub}  |  modo: {'APLICAR' if apply else 'simulação (nada é gravado; use --apply)'}")
    today = date.today().isoformat()
    pending = [handle(hub, n, p, apply, today) for n, p in regs]
    if scan_dir is not None:
        pending.append(scan(hub, scan_dir, [p for _, p in regs]))
    print(f"\nResumo: {len(regs)} projeto(s), {sum(pending)} com pendência.")
    return 1 if any(pending) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
