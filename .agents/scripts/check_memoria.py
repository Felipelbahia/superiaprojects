#!/usr/bin/env python3
"""
Check de memória do Mac (macOS), só leitura por padrão.

Mostra um semáforo (swap, compressor, load, nº de node) e os processos órfãos de extensões
de IDE (Gemini/agy e seus MCPs, OpenAI/codex, Kilo, Claude) e hosts "Plugin" do Antigravity
parados, com o que é, por que pesa e como resolver. Com --limpar, lista os alvos, pede ok e
encerra com SIGTERM (SIGKILL só com um segundo ok).

Uso (a partir da raiz do projeto):
    python3 .agents/scripts/check_memoria.py            # só leitura
    python3 .agents/scripts/check_memoria.py --limpar   # lista, pede ok, encerra

Regras que o script cumpre (ver .agents/skills/auditing-memory-usage):
  - Nunca imprime argumentos de processo: lê `ps args` só para extrair a porta do hub do agy
    e o nome do pacote do MCP, e descarta o resto. A saída ainda passa por redact().
  - Nunca propõe encerrar a cadeia de pais da própria sessão (até o Electron).
  - Só estes alvos recebem sinal: agy órfão, host "Plugin" parado, MCP/claude/kilo/codex órfão.
  - Não mexe em Docker: só orienta.
Só biblioteca padrão. Binários do macOS por caminho absoluto (o `grep` do Mac é alias de ugrep).
"""

import argparse
import os
import re
import signal
import subprocess
import sys
import time
from collections import defaultdict
from typing import NamedTuple, Optional

BIN = {
    "ps": "/bin/ps",
    "lsof": "/usr/sbin/lsof",
    "sysctl": "/usr/sbin/sysctl",
    "vm_stat": "/usr/bin/vm_stat",
    "top": "/usr/bin/top",
}

# Limites (amarelo, vermelho). Absolutos: o swap total do macOS cresce sozinho ao longo do dia.
LIMITS = {
    "swap": (3.0, 5.0),        # GB usados
    "compressor": (4.0, 7.0),  # GB ocupados
    "load": (1.0, 2.0),        # load 1 min / nº de CPUs
    "node": (50, 90),          # processos node vivos
}

HOST_MARK = "Helper (Plugin)"
HOST_MIN_AGE = 20 * 60
ORPHAN_EXES = {"claude": "claude_orfao", "kilo": "kilo_orfao", "codex": "codex_orfao"}
PROTECTED_EXES = {"Antigravity IDE", "Electron", "launchd"}
MCP_RUNNERS = {"node", "npm", "npx"}
MCP_MARKERS = ("mcp", "sequential-thinking", "testsprite", "shadcn", "context7", "stitch", "openapi")
ALLOWED_KINDS = {"agy_orfao", "host_parado", "mcp_orfao", "claude_orfao", "kilo_orfao", "codex_orfao"}
KILL_WAIT = 8

SECRET_RE = re.compile(
    r"sbp_[A-Za-z0-9]+|ctx7sk-[\w-]+|AIza[\w-]{20,}|\bAQ\.[\w-]{20,}|\bsk-[A-Za-z0-9_-]{16,}"
    r"|x-goog-api-key\S*(?:\s+\S+)?"
    r"|--(?:api-key|access-token|token|key|secret|password)(?:[= ]\S+)?",
    re.IGNORECASE,
)


class Proc(NamedTuple):
    pid: int
    ppid: int
    age: int
    stat: str
    path: str
    exe: str
    hub_port: Optional[int]
    pkg: Optional[str]
    mcp: bool


class Finding(NamedTuple):
    kind: str
    pid: int
    detail: str


class Snapshot(NamedTuple):
    procs: dict
    clients: dict
    swap_total: float
    swap_used: float
    load: float
    ncpu: int
    compressor: float
    nodes: int
    top: list


# ---------------------------------------------------------------- redact / parsing

def redact(text: str) -> str:
    return SECRET_RE.sub("[oculto]", text)


def parse_etime(s: str) -> int:
    days = 0
    if "-" in s:
        d, s = s.split("-", 1)
        days = int(d)
    parts = [int(x) for x in s.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, sec = parts
    return days * 86400 + h * 3600 + m * 60 + sec


def package_name(args: str) -> Optional[str]:
    """Nome do pacote de um MCP (npm exec <pkg> ou node .../node_modules/<pkg>/...). Nunca devolve argumentos."""
    toks = args.split()
    if not toks:
        return None
    runner = os.path.basename(toks[0])
    cand = None
    if runner in ("npm", "npx"):
        rest = toks[toks.index("exec") + 1:] if runner == "npm" and "exec" in toks else (toks[1:] if runner == "npx" else [])
        cand = next((t for t in rest if not t.startswith("-")), None)
    elif runner == "node":
        for t in toks[1:]:
            if t.startswith("-"):
                continue
            m = re.search(r"node_modules/(@[^/\s]+/[^/\s]+|[^/\s]+)", t)
            cand = (os.path.basename(t) if m.group(1) == ".bin" else m.group(1)) if m else os.path.basename(t)
            break
    if not cand:
        return None
    cand = re.sub(r"(?<=.)@[\w.\-]+$", "", cand)  # @latest, @1.2.3
    if not re.fullmatch(r"@?[A-Za-z0-9._/-]{1,60}", cand) or SECRET_RE.search(cand):
        return None
    return cand


def title_package(exe: str) -> Optional[str]:
    """Nome de pacote a partir do título do processo (já sem argumentos), p.ex. 'npm exec x@latest'."""
    toks = exe.split()
    if not toks:
        return None
    if toks[0] in ("npm", "npx") and "exec" in toks:
        toks = toks[toks.index("exec") + 1:]
    cand = next((x for x in toks if not x.startswith("-")), None)
    if not cand:
        return None
    cand = re.sub(r"(?<=.)@[\w.\-]+$", "", cand)
    return cand if re.fullmatch(r"@?[A-Za-z0-9._/-]{1,60}", cand) and not SECRET_RE.search(cand) else None


def build_procs(comm_text: str, args_text: str) -> dict:
    """Junta `ps ... comm=` (seguro) com `ps ... args=`; dos argumentos só sobram porta do hub e nome do pacote."""
    args_by_pid = {}
    for line in args_text.splitlines():
        m = re.match(r"^\s*(\d+)\s+(.*)$", line)
        if m:
            args_by_pid[int(m.group(1))] = m.group(2)
    procs = {}
    for line in comm_text.splitlines():
        m = re.match(r"^\s*(\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(.*\S)\s*$", line)
        if not m:
            continue
        pid, ppid, etime, stat, path = int(m.group(1)), int(m.group(2)), m.group(3), m.group(4), m.group(5)
        # `comm` NÃO é seguro: node/npm reescrevem o título do processo e o `comm` passa a trazer os
        # argumentos (inclusive tokens). Fica só o nome, cortado antes do primeiro argumento.
        exe = re.split(r"\s+-|\s+\S+=", os.path.basename(path), maxsplit=1)[0]
        path = redact(path)
        if stat.startswith("Z"):
            exe = exe.strip("()")
        args = args_by_pid.get(pid, "")
        hub_port = None
        if exe == "agy":
            hp = re.search(r"--hub-port[= ](\d+)", args)
            hub_port = int(hp.group(1)) if hp else None
        pkg, mcp = None, False
        low_exe = exe.lower()
        runner = exe.split()[0] in MCP_RUNNERS if exe.split() else False
        if runner or any(k in low_exe for k in MCP_MARKERS):
            blob = (args or exe).lower()
            mcp = any(k in blob for k in MCP_MARKERS)
            if mcp:
                pkg = (package_name(args) if args and runner else None) or title_package(exe)
        procs[pid] = Proc(pid, ppid, parse_etime(etime), stat, path, exe, hub_port, pkg, mcp)
    return procs


def parse_swap(text: str):
    m = re.search(r"total = ([\d.]+)([MG]).*?used = ([\d.]+)([MG])", text)
    if not m:
        return 0.0, 0.0
    conv = lambda v, u: float(v) / (1024 if u == "M" else 1)
    return conv(m.group(1), m.group(2)), conv(m.group(3), m.group(4))


def parse_loadavg(text: str) -> float:
    m = re.search(r"[\d.]+", text)
    return float(m.group(0)) if m else 0.0


def parse_compressor_gb(text: str) -> float:
    size = re.search(r"page size of (\d+) bytes", text)
    pages = re.search(r"Pages occupied by compressor:\s+(\d+)", text)
    if not pages:
        return 0.0
    return int(pages.group(1)) * (int(size.group(1)) if size else 4096) / 1024 ** 3


def count_local_clients(lsof_text: str, port: Optional[int]) -> Optional[int]:
    """Conexões ESTABLISHED de clientes locais na porta do hub (lado servidor: <porta>-><loopback>)."""
    if not port:
        return None
    rx = re.compile(rf":{port}->(?:127\.0\.0\.1|\[::1\]|localhost):\d+")
    return sum(1 for line in lsof_text.splitlines() if rx.search(line) and "ESTABLISHED" in line)


def _to_mb(token: str) -> float:
    m = re.fullmatch(r"([\d.]+)([BKMG]?)[+-]?", token)
    if not m:
        return 0.0
    return float(m.group(1)) * {"B": 1 / 1048576, "K": 1 / 1024, "M": 1, "G": 1024, "": 1}[m.group(2)]


def parse_top(text: str) -> list:
    rows, seen_header = [], False
    for line in text.splitlines():
        if line.strip().startswith("PID"):
            seen_header = True
            continue
        m = re.match(r"^\s*(\d+)\s+(.+?)\s+(\S+)\s+(\S+)\s*$", line)
        if seen_header and m:
            mem, cmp_ = _to_mb(m.group(3)), _to_mb(m.group(4))
            rows.append((int(m.group(1)), m.group(2).strip(), m.group(3), m.group(4), mem + cmp_))
    return rows


# ---------------------------------------------------------------- classification

def classify(metric: str, value: float) -> str:
    yellow, red = LIMITS[metric]
    return "vermelho" if value >= red else "amarelo" if value >= yellow else "verde"


def _alive(p: Proc) -> bool:
    return not p.stat.startswith("Z")


def _descendants(procs: dict, pid: int) -> list:
    kids = defaultdict(list)
    for p in procs.values():
        kids[p.ppid].append(p.pid)
    out, stack = [], list(kids.get(pid, []))
    while stack:
        cur = stack.pop()
        if cur in out or cur == pid:
            continue
        out.append(cur)
        stack.extend(kids.get(cur, []))
    return [procs[c] for c in out]


def fmt_age(sec: int) -> str:
    return f"{sec // 3600}h{sec % 3600 // 60:02d}" if sec >= 3600 else f"{sec // 60}min"


def find_findings(procs: dict, clients: dict) -> list:
    out = []
    for p in sorted(procs.values(), key=lambda x: x.pid):
        if not _alive(p):
            continue
        if p.exe == "agy":
            # Órfão = sem pai (ppid 1) E zero clientes locais na porta do hub. Contagem desconhecida = nunca órfão.
            if p.ppid == 1 and p.hub_port and clients.get(p.pid) == 0:
                n = sum(1 for d in _descendants(procs, p.pid) if _alive(d))
                out.append(Finding("agy_orfao", p.pid, f"{fmt_age(p.age)}, {n} filhos, sem cliente local"))
        elif p.exe in ORPHAN_EXES and p.ppid == 1:
            out.append(Finding(ORPHAN_EXES[p.exe], p.pid, f"{p.exe}, {fmt_age(p.age)}, sem pai vivo"))
        elif p.mcp and p.ppid == 1:
            safe_exe = p.exe if re.fullmatch(r"[A-Za-z0-9._-]{1,40}", p.exe) and not SECRET_RE.search(p.exe) else "MCP"
            out.append(Finding("mcp_orfao", p.pid, f"{p.pkg or safe_exe}, {fmt_age(p.age)}, sem pai vivo"))
        elif HOST_MARK in p.exe and p.age >= HOST_MIN_AGE:
            parent = procs.get(p.ppid)
            if parent is not None and HOST_MARK in parent.exe:
                continue  # sub-helper de outro host
            live = [d for d in _descendants(procs, p.pid) if _alive(d) and HOST_MARK not in d.exe]
            if not live:
                out.append(Finding("host_parado", p.pid, f"{fmt_age(p.age)}, nada vivo dentro"))
    return out


def protected_pids(procs: dict, start_pid: int) -> set:
    """Cadeia de pais do processo do script até a raiz (terminal, host, Electron) + nomes intocáveis."""
    chain, pid = {start_pid}, start_pid
    while pid in procs:
        chain.add(pid)
        nxt = procs[pid].ppid
        if nxt == pid or nxt not in procs:
            break
        pid = nxt
    chain |= {p.pid for p in procs.values() if p.exe in PROTECTED_EXES}
    return chain


def select_targets(findings: list, protected: set) -> list:
    return [f for f in findings if f.kind in ALLOWED_KINDS and f.pid not in protected]


# ---------------------------------------------------------------- system access

class System:
    """Acesso real ao macOS. Os testes trocam esta classe por uma de fixtures."""

    platform = sys.platform

    def _run(self, key, *args, timeout=20, ok=(0,)):
        r = subprocess.run([BIN[key], *args], capture_output=True, text=True, timeout=timeout,
                           env={**os.environ, "LC_ALL": "C"})
        if r.returncode not in ok:
            raise RuntimeError(f"{key} saiu com {r.returncode}")
        return r.stdout

    def getpid(self):
        return os.getpid()

    def ps_comm(self):
        return self._run("ps", "-axo", "pid=,ppid=,etime=,stat=,comm=")

    def ps_args(self):
        return self._run("ps", "-axo", "pid=,command=")

    def lsof_established(self, pid):
        r = subprocess.run([BIN["lsof"], "-nP", "-a", "-p", str(pid), "-iTCP", "-sTCP:ESTABLISHED"],
                           capture_output=True, text=True, timeout=15)
        if r.returncode == 0 or (r.returncode == 1 and not r.stderr.strip()):
            return r.stdout  # 1 sem erro = nenhuma conexão
        raise RuntimeError("lsof falhou")

    def sysctl_swap(self):
        return self._run("sysctl", "-n", "vm.swapusage")

    def sysctl_loadavg(self):
        return self._run("sysctl", "-n", "vm.loadavg")

    def ncpu(self):
        return int(self._run("sysctl", "-n", "hw.ncpu").strip() or 1)

    def vm_stat(self):
        return self._run("vm_stat")

    def top_mem(self):
        try:
            return self._run("top", "-l", "1", "-o", "mem", "-n", "15", "-stats", "pid,command,mem,cmprs", timeout=40)
        except Exception:
            return ""

    def kill(self, pid, sig):
        os.kill(pid, sig)

    def sleep(self, secs):
        time.sleep(secs)

    def ask(self, prompt):
        return input(prompt)

    def clock(self):
        return time.strftime("%H:%M")


def collect(system) -> Snapshot:
    procs = build_procs(system.ps_comm(), system.ps_args())
    clients = {}
    for p in procs.values():
        if p.exe == "agy" and p.hub_port:
            try:
                clients[p.pid] = count_local_clients(system.lsof_established(p.pid), p.hub_port)
            except Exception:
                clients[p.pid] = None  # não deu para medir: nunca tratar como órfão
    total, used = parse_swap(system.sysctl_swap())
    top = parse_top(system.top_mem()) if hasattr(system, "top_mem") else []
    return Snapshot(procs, clients, total, used, parse_loadavg(system.sysctl_loadavg()),
                    max(system.ncpu(), 1), parse_compressor_gb(system.vm_stat()),
                    sum(1 for p in procs.values() if p.exe == "node" and _alive(p)), top)


# ---------------------------------------------------------------- report

def _n(x: float) -> str:
    return f"{x:.1f}".replace(".", ",")


def _gb(x: float) -> str:
    return f"{x:.1f}".replace(".", ",") + " GB"


ICON = {"verde": "🟢", "amarelo": "🟡", "vermelho": "🔴"}
WHAT = {
    "agy_orfao": "agy órfão = hub do Gemini sem pai e sem janela ligada; segura 4 MCPs (npm + node) que seguem rodando.",
    "host_parado": 'host "Plugin" parado = processo de extensões do Antigravity sem nada vivo dentro; fica com GBs no compressor.',
    "outros": "órfão de claude/kilo/codex/MCP = processo cujo pai morreu (ppid 1) e que ninguém mais usa.",
}


def render_report(snap: Snapshot, targets: list, clock: str) -> str:
    lines = [f"Check de memória, {clock}"]
    levels = {
        "swap": classify("swap", snap.swap_used),
        "compressor": classify("compressor", snap.compressor),
        "load": classify("load", snap.load / snap.ncpu),
        "node": classify("node", snap.nodes),
    }
    rows = {
        "swap": f"Swap        {_gb(snap.swap_used)} de {_gb(snap.swap_total)}   (limite {LIMITS['swap'][0]:g}/{LIMITS['swap'][1]:g} GB)",
        "compressor": f"Compressor  {_gb(snap.compressor)}   (limite {LIMITS['compressor'][0]:g}/{LIMITS['compressor'][1]:g} GB)",
        "load": f"Load        {_n(snap.load)} em {snap.ncpu} CPUs   (limite {LIMITS['load'][0]:g}/{LIMITS['load'][1]:g} por CPU)",
        "node": f"node        {snap.nodes} processos   (limite {LIMITS['node'][0]}/{LIMITS['node'][1]})",
    }
    short = {"swap": f"Swap {_gb(snap.swap_used)}", "compressor": f"Compressor {_gb(snap.compressor)}",
             "load": "Load " + _n(snap.load), "node": f"node {snap.nodes}"}
    greens = [f"🟢 {short[m]}" for m, lv in levels.items() if lv == "verde"]
    bad = False
    for m, lv in levels.items():
        if lv != "verde":
            bad = True
            lines.append(f"{ICON[lv]} {rows[m]}")
    by_kind = defaultdict(list)
    for f in targets:
        by_kind[f.kind].append(f)
    if by_kind["agy_orfao"]:
        fs = by_kind["agy_orfao"]
        lines.append(f"🔴 agy órfãos            {len(fs)}   " + "; ".join(f"PID {f.pid} ({f.detail})" for f in fs))
    if by_kind["host_parado"]:
        fs = by_kind["host_parado"]
        lines.append(f'🔴 Hosts "Plugin" parados {len(fs)}   ' + "; ".join(f"PID {f.pid} ({f.detail})" for f in fs))
    others = [f for k in ("claude_orfao", "kilo_orfao", "codex_orfao", "mcp_orfao") for f in by_kind[k]]
    if others:
        lines.append(f"🔴 Órfãos claude/kilo/codex/MCP {len(others)}   " + "; ".join(f"PID {f.pid} ({f.detail})" for f in others))
    if not targets:
        greens.append("🟢 sem órfãos")
    if greens:
        lines.append("   ".join(greens))
    if not (bad or targets):
        return "\n".join(lines)

    lines += ["", "O que é:"]
    if by_kind["agy_orfao"]:
        lines.append("  " + WHAT["agy_orfao"])
    if by_kind["host_parado"]:
        lines.append("  " + WHAT["host_parado"])
    if others:
        lines.append("  " + WHAT["outros"])
    lines += ["", "Como resolver:"]
    if targets:
        lines.append("  órfão / host parado -> kill -TERM <PID>  (ou: python3 .agents/scripts/check_memoria.py --limpar)")
    if levels["swap"] != "verde" or levels["compressor"] != "verde":
        lines.append("  swap/compressor altos sem órfão -> reiniciar o Antigravity; se persistir, reiniciar o Mac")
    if levels["load"] != "verde" or levels["node"] != "verde":
        lines.append("  load ou node altos -> ver os mais pesados abaixo e fechar o que não está em uso")
    lines.append("  Docker (o script não mexe em containers) -> docker stats --no-stream; docker update --restart=no <nome>")
    if targets:
        lines += ["", "Para limpar:  python3 .agents/scripts/check_memoria.py --limpar"]
    flagged = {f.pid for f in targets}
    heavy = [r for r in snap.top if r[0] not in flagged][:5]
    if heavy:
        lines += ["", "Mais pesados agora (só informativo, o script nunca encerra estes):"]
        for pid, name, mem, cmp_, _ in heavy:
            pr = snap.procs.get(pid)
            extra = ""
            if pr:
                live = sum(1 for d in _descendants(snap.procs, pid) if _alive(d))
                extra = f"  [aberto há {fmt_age(pr.age)}, {live} processos vivos dentro]"
            lines.append(f"  PID {pid}  {name}  {mem} (comprimido {cmp_}){extra}")
        lines.append("  Compressão alta sem órfão: o peso está nas janelas abertas. Feche a conversa ou janela do Antigravity "
                     "que o dono não usa (a mais antiga e com menos processos vivos dentro é a melhor candidata).")
    return "\n".join(lines)


def _metrics_line(snap: Snapshot) -> str:
    return f"swap {_gb(snap.swap_used)}, compressor {_gb(snap.compressor)}, node {snap.nodes}, load {_n(snap.load)}"


def _yes(answer: str) -> bool:
    return answer.strip().lower() in ("s", "sim", "y", "yes")


# ---------------------------------------------------------------- main

def main(argv=None, system=None, out=None) -> int:
    system = system or System()
    out = out or sys.stdout

    def emit(text=""):
        out.write(redact(text) + "\n")

    if system.platform != "darwin":
        emit("check_memoria.py só funciona no macOS (usa ps, lsof, sysctl e vm_stat do Mac). Nada foi feito.")
        return 2
    parser = argparse.ArgumentParser(prog="check_memoria.py", description="Check de memória do Mac (só leitura por padrão).")
    parser.add_argument("--limpar", action="store_true", help="lista os alvos, pede ok e encerra com SIGTERM")
    args = parser.parse_args(argv)

    snap = collect(system)
    protected = protected_pids(snap.procs, system.getpid())
    targets = select_targets(find_findings(snap.procs, snap.clients), protected)
    emit(render_report(snap, targets, system.clock()))
    if not args.limpar:
        return 0

    emit("")
    if not targets:
        emit("Nada para encerrar.")
        return 0
    emit("Vou encerrar (SIGTERM):")
    for f in targets:
        emit(f"  PID {f.pid}  {f.kind}  ({f.detail})")
    if not _yes(system.ask(f"Encerrar estes {len(targets)} processos? [s/N] ")):
        emit("Nada foi encerrado.")
        return 0
    before = snap
    ids = [f.pid for f in targets]
    for pid in ids:
        try:
            system.kill(pid, signal.SIGTERM)
        except (ProcessLookupError, PermissionError) as exc:
            emit(f"  PID {pid}: {type(exc).__name__}")
    system.sleep(KILL_WAIT)
    after = collect(system)
    left = [pid for pid in ids if pid in after.procs and _alive(after.procs[pid])]
    if left:
        emit(f"Ainda vivos depois de {KILL_WAIT}s: " + ", ".join(str(p) for p in left))
        if _yes(system.ask(f"Enviar SIGKILL a estes {len(left)}? [s/N] ")):
            for pid in left:
                try:
                    system.kill(pid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError) as exc:
                    emit(f"  PID {pid}: {type(exc).__name__}")
            system.sleep(2)
            after = collect(system)
        else:
            emit("SIGKILL não enviado.")
    emit("")
    emit("Antes:  " + _metrics_line(before))
    emit("Depois: " + _metrics_line(after))
    emit("Rode o check de novo: filhos do que foi encerrado podem ter virado órfãos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
