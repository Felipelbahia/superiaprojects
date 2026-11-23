"""Tests for check_memoria.py (protocolo de check de memória, macOS).

Run from the 0 Padrões root: python3 -m unittest discover -s .agents/scripts/tests

Nothing here touches a real process: ps/lsof/kill/input are injected (FakeSystem) and the
fixtures in fixtures/memoria/ are synthetic, in the real format of ps/lsof/sysctl/vm_stat.
Synthetic secrets are assembled at run time so the kit's own secret scan never flags them.
"""

import ast
import io
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
FIX = Path(__file__).resolve().parent / "fixtures" / "memoria"
sys.path.insert(0, str(SCRIPTS))

import check_memoria as cm  # noqa: E402

SECRETS = {
    "@@SBP@@": "sb" + "p_" + "0123456789abcdef0123456789abcdef01234567",
    "@@CTX7@@": "ctx7" + "sk-" + "1111aaaa-2222-bbbb-3333-cccc4444dddd",
    "@@GOOG@@": "AIza" + "SyFAKE0000000000000000000000000000X",
}
ARG_MARKERS = ["--access-token", "--api-key", "--hub-port", "X-Goog-Api-Key", "--header", "--resume"]


def fixture(name: str) -> str:
    text = (FIX / name).read_text(encoding="utf-8")
    for placeholder, value in SECRETS.items():
        text = text.replace(placeholder, value)
    return text


class FakeSystem:
    """Same interface as check_memoria.System, fed by fixtures; records every signal."""

    def __init__(self, answers=(), stubborn=(), platform="darwin", pid=7000, drop=()):
        self.platform = platform
        self.pid = pid
        self.answers = list(answers)
        self.stubborn = set(stubborn)
        self.kills = []
        self.prompts = []
        self.sleeps = []
        self.dead = set(drop)
        self.calls = []

    def getpid(self):
        return self.pid

    def _filter(self, text):
        keep = []
        for line in text.splitlines():
            parts = line.split()
            if parts and int(parts[0]) in self.dead:
                continue
            keep.append(line)
        return "\n".join(keep) + "\n"

    def ps_comm(self):
        self.calls.append("ps_comm")
        return self._filter(fixture("ps_comm.txt"))

    def ps_args(self):
        self.calls.append("ps_args")
        return self._filter(fixture("ps_args.txt"))

    def lsof_established(self, pid):
        self.calls.append(f"lsof {pid}")
        path = FIX / f"lsof_{pid}.txt"
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def sysctl_swap(self):
        return fixture("sysctl_swap.txt")

    def sysctl_loadavg(self):
        return fixture("sysctl_loadavg.txt")

    def ncpu(self):
        return 12

    def vm_stat(self):
        return fixture("vm_stat.txt")

    def top_mem(self):
        return fixture("top_mem.txt")

    def kill(self, pid, sig):
        self.kills.append((pid, sig))
        if sig == 15 and pid not in self.stubborn:
            self.dead.add(pid)
        if sig == 9:
            self.dead.add(pid)

    def sleep(self, secs):
        self.sleeps.append(secs)

    def ask(self, prompt):
        self.prompts.append(prompt)
        return self.answers.pop(0) if self.answers else "n"

    def clock(self):
        return "18:40"


def run(argv, system):
    out = io.StringIO()
    code = cm.main(argv, system=system, out=out)
    return code, out.getvalue()


def snapshot(system=None):
    system = system or FakeSystem()
    procs = cm.build_procs(system.ps_comm(), system.ps_args())
    clients = {p.pid: cm.count_local_clients(system.lsof_established(p.pid), p.hub_port)
               for p in procs.values() if p.exe == "agy" and p.hub_port}
    return procs, clients


EXPECTED_TARGETS = {38449, 2052, 64027, 51000, 51001, 51002, 52000, 52010, 52020}


class Item1PlatformAndStdlib(unittest.TestCase):
    def test_only_stdlib_and_absolute_binaries(self):
        tree = ast.parse((SCRIPTS / "check_memoria.py").read_text(encoding="utf-8"))
        mods = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                mods |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module:
                mods.add(node.module.split(".")[0])
        self.assertTrue(mods <= set(sys.stdlib_module_names), mods - set(sys.stdlib_module_names))
        for name, path in cm.BIN.items():
            self.assertTrue(path.startswith("/"), name)

    def test_non_macos_exits_with_clear_message(self):
        code, out = run([], FakeSystem(platform="linux"))
        self.assertNotEqual(code, 0)
        self.assertIn("macOS", out)


class Parsing(unittest.TestCase):
    def test_etime_formats(self):
        self.assertEqual(cm.parse_etime("26:47"), 26 * 60 + 47)
        self.assertEqual(cm.parse_etime("03:18:24"), 3 * 3600 + 18 * 60 + 24)
        self.assertEqual(cm.parse_etime("05-11:02:10"), 5 * 86400 + 11 * 3600 + 2 * 60 + 10)

    def test_comm_with_spaces_and_zombies(self):
        procs, _ = snapshot()
        self.assertEqual(procs[2056].exe, "Antigravity IDE Helper (Plugin)")
        self.assertEqual(procs[53000].exe, "python")
        self.assertIn("RSS Feed", procs[53000].path)
        self.assertTrue(procs[2053].stat.startswith("Z"))

    def test_metrics(self):
        s = FakeSystem()
        self.assertAlmostEqual(cm.parse_swap(s.sysctl_swap())[1], 4915 / 1024, places=2)
        self.assertAlmostEqual(cm.parse_loadavg(s.sysctl_loadavg()), 9.40)
        self.assertAlmostEqual(cm.parse_compressor_gb(s.vm_stat()), 5.0, places=2)

    def test_local_clients_counted_on_the_hub_port_only(self):
        s = FakeSystem()
        self.assertEqual(cm.count_local_clients(s.lsof_established(6978), 50777), 2)  # 3rd line is remote
        self.assertEqual(cm.count_local_clients(s.lsof_established(47042), 50888), 2)
        self.assertEqual(cm.count_local_clients(s.lsof_established(38449), 50123), 0)


class Item2AgyOrphan(unittest.TestCase):
    def test_orphan_flagged_active_not(self):
        procs, clients = snapshot()
        found = [f.pid for f in cm.find_findings(procs, clients) if f.kind == "agy_orfao"]
        self.assertEqual(found, [38449])

    def test_unknown_client_count_is_never_orphan(self):
        procs, clients = snapshot()
        clients[38449] = None  # lsof failed
        found = [f.pid for f in cm.find_findings(procs, clients) if f.kind == "agy_orfao"]
        self.assertEqual(found, [])

    def test_parent_alive_with_zero_clients_is_not_orphan(self):
        procs, clients = snapshot()
        clients[6978] = 0
        found = [f.pid for f in cm.find_findings(procs, clients) if f.kind == "agy_orfao"]
        self.assertEqual(found, [38449])


class Item3StoppedHosts(unittest.TestCase):
    def test_only_stopped_old_hosts(self):
        procs, clients = snapshot()
        found = sorted(f.pid for f in cm.find_findings(procs, clients) if f.kind == "host_parado")
        self.assertEqual(found, [2052, 64027])  # zombies don't count; 48583 is too new; 48880/46989/6701 have live kids


class Item4OtherOrphans(unittest.TestCase):
    def test_orphans_by_origin_and_unknowns_untouched(self):
        procs, clients = snapshot()
        kinds = {(f.kind, f.pid) for f in cm.find_findings(procs, clients)}
        for expected in [("claude_orfao", 51000), ("kilo_orfao", 51001), ("codex_orfao", 51002),
                         ("mcp_orfao", 52000), ("mcp_orfao", 52010), ("mcp_orfao", 52020)]:
            self.assertIn(expected, kinds)
        pids = {pid for _, pid in kinds}
        self.assertNotIn(53000, pids)  # unknown owner (python ppid=1): shown elsewhere, never a target
        self.assertNotIn(2012, pids)  # Electron main
        self.assertNotIn(49502, pids)  # kilo with a live parent
        self.assertNotIn(47105, pids)  # claude with a live parent
        self.assertNotIn(60001, pids)  # plain node with a live parent


class Item5SessionProtection(unittest.TestCase):
    def test_chain_is_excluded_even_when_it_looks_like_an_orphan(self):
        procs, clients = snapshot()
        self.assertEqual(cm.protected_pids(procs, 7000), {7000, 6855, 6716, 2056, 2012, 1})
        procs[6855] = procs[6855]._replace(ppid=1)  # the session's own claude looks orphaned
        findings = cm.find_findings(procs, clients)
        self.assertIn(6855, {f.pid for f in findings})
        protected = cm.protected_pids(procs, 7000)
        targets = {f.pid for f in cm.select_targets(findings, protected)}
        self.assertNotIn(6855, targets)
        self.assertEqual(targets, EXPECTED_TARGETS)


class Item6Secrets(unittest.TestCase):
    def test_no_secret_or_argument_in_any_output(self):
        outputs = []
        outputs.append(run([], FakeSystem())[1])
        outputs.append(run(["--limpar"], FakeSystem(answers=["n"]))[1])
        outputs.append(run(["--limpar"], FakeSystem(answers=["s", "s"], stubborn=EXPECTED_TARGETS))[1])
        text = "\n".join(outputs)
        for secret in SECRETS.values():
            self.assertNotIn(secret, text)
        for marker in ARG_MARKERS:
            self.assertNotIn(marker, text)
        self.assertIn("context7-mcp", text)  # package name is shown, arguments are not
        self.assertIn("mcp-server-supabase", text)  # title-rewritten process: name only, token cut off

    def test_comm_with_rewritten_title_never_leaks_arguments(self):
        procs, _ = snapshot()
        self.assertEqual(procs[52020].exe, "mcp-server-supabase@latest")
        self.assertEqual(procs[52020].pkg, "mcp-server-supabase")
        self.assertNotIn("sbp_", procs[52020].path)

    def test_redact_is_defense_in_depth(self):
        extra = "AQ" + "." + "Ab8RN6L7GdjIVbYKS8zedhq4I4Oudrs9JOZB"  # new-style Google key
        for secret in [*SECRETS.values(), extra]:
            self.assertNotIn(secret, cm.redact(f"x --token {secret} y"))
            self.assertNotIn(secret, cm.redact(f"bare {secret} end"))


class Item6bMcpNameFallback(unittest.TestCase):
    def test_exe_without_a_package_name_is_never_printed_raw(self):
        procs, clients = snapshot()
        weird = "mcp-x " + SECRETS["@@SBP@@"]
        procs[52020] = procs[52020]._replace(exe=weird, pkg=None)
        detail = [f.detail for f in cm.find_findings(procs, clients) if f.pid == 52020][0]
        self.assertTrue(detail.startswith("MCP,"), detail)
        self.assertNotIn("sbp_", detail)


class Item7Semaphore(unittest.TestCase):
    def test_boundaries(self):
        cases = {
            "swap": (2.99, 3.0, 5.0),
            "compressor": (3.99, 4.0, 7.0),
            "load": (0.99, 1.0, 2.0),
            "node": (49, 50, 90),
        }
        for metric, (below, yellow, red) in cases.items():
            self.assertEqual(cm.classify(metric, below), "verde", metric)
            self.assertEqual(cm.classify(metric, yellow), "amarelo", metric)
            self.assertEqual(cm.classify(metric, red), "vermelho", metric)

    def test_report_format(self):
        code, out = run([], FakeSystem())
        self.assertEqual(code, 0)
        for line in ["🟡 Swap", "🟡 Compressor", "🔴 agy órfãos", "🔴 Hosts", "38449", "2052", "Como resolver", "--limpar", "kill -TERM"]:
            self.assertIn(line, out)
        self.assertNotIn("6978", out)  # the active hub is never mentioned as a problem

    def test_heavy_list_is_informational_and_skips_flagged(self):
        s = FakeSystem()
        _, out = run([], s)
        tail = out.split("Mais pesados agora")[1]
        self.assertIn("só informativo", out)
        self.assertIn("53000", tail)  # unknown owner: shown, never a target
        self.assertNotIn("38449", tail)  # already listed as a finding
        self.assertNotIn("2052", tail)

    def test_heavy_list_says_how_old_and_how_busy(self):
        _, out = run([], FakeSystem())
        tail = out.split("Mais pesados agora")[1]
        self.assertIn("PID 6701  Antigravity IDE  1000M (comprimido 3000M)  [aberto há 3h18, 4 processos vivos dentro]", tail)
        self.assertIn("aberto há 6h00", tail)  # 53000, unknown owner: still informational
        self.assertIn("Feche a conversa ou janela", tail)

    def test_all_green_is_short(self):
        clean = FakeSystem(drop={38449, 38460, 38461, 38470, 38471, 2052, 2053, 64027, 64030,
                                 51000, 51001, 51002, 52000, 52010, 52020, 53000})
        clean.sysctl_swap = lambda: "total = 7168.00M  used = 500.00M  free = 6668.00M  (encrypted)\n"
        clean.vm_stat = lambda: "Mach Virtual Memory Statistics: (page size of 4096 bytes)\nPages occupied by compressor: 262144.\n"
        code, out = run([], clean)
        self.assertEqual(code, 0)
        self.assertIn("🟢", out)
        self.assertNotIn("Como resolver", out)
        self.assertNotIn("🔴", out)


class Item8Cleanup(unittest.TestCase):
    def test_no_ok_no_signal(self):
        s = FakeSystem(answers=["n"])
        run(["--limpar"], s)
        self.assertEqual(s.kills, [])
        self.assertEqual(len(s.prompts), 1)

    def test_ok_sends_only_sigterm_to_allowed_targets(self):
        s = FakeSystem(answers=["s"])
        code, out = run(["--limpar"], s)
        self.assertEqual(code, 0)
        self.assertEqual({pid for pid, _ in s.kills}, EXPECTED_TARGETS)
        self.assertEqual({sig for _, sig in s.kills}, {15})
        self.assertIn(8, s.sleeps)
        self.assertIn("Antes", out)
        self.assertIn("Depois", out)
        for protected in (7000, 6855, 6716, 2056, 2012, 6978, 47042, 6701, 53000):
            self.assertNotIn(protected, {pid for pid, _ in s.kills})

    def test_sigkill_needs_a_second_ok(self):
        s = FakeSystem(answers=["s", "n"], stubborn={38449})
        run(["--limpar"], s)
        self.assertNotIn(9, {sig for _, sig in s.kills})
        self.assertEqual(len(s.prompts), 2)

        s = FakeSystem(answers=["s", "s"], stubborn={38449})
        run(["--limpar"], s)
        self.assertEqual([(p, g) for p, g in s.kills if g == 9], [(38449, 9)])

    def test_nothing_to_clean(self):
        s = FakeSystem(answers=["s"], drop=EXPECTED_TARGETS | {38460, 38461, 38470, 38471, 2053, 64030})
        code, out = run(["--limpar"], s)
        self.assertEqual(s.kills, [])
        self.assertEqual(s.prompts, [])
        self.assertIn("Nada para encerrar", out)


class Item9DockerOnlyAdvises(unittest.TestCase):
    def test_no_docker_binary_and_advice_present(self):
        self.assertNotIn("docker", " ".join(cm.BIN.values()).lower())
        s = FakeSystem()
        _, out = run([], s)
        self.assertIn("docker stats --no-stream", out)
        self.assertFalse([c for c in s.calls if "docker" in c])
        src = (SCRIPTS / "check_memoria.py").read_text(encoding="utf-8")
        self.assertNotIn('"docker"', src)


class DocsMatchCode(unittest.TestCase):
    """What the skill's reference promises about thresholds, markers, protection and waits must match the code."""

    def setUp(self):
        doc = SCRIPTS.parent / "skills" / "auditing-memory-usage" / "references" / "ambiente-macos.md"
        self.doc = doc.read_text(encoding="utf-8")

    def test_every_mcp_marker_and_protected_name_is_documented(self):
        for marker in cm.MCP_MARKERS:
            self.assertIn(f"`{marker}`", self.doc)
        for name in cm.PROTECTED_EXES:
            self.assertIn(f"`{name}`", self.doc)

    def test_limits_wait_and_age_are_documented_as_coded(self):
        pair = lambda k: "{:g}/{:g}".format(*cm.LIMITS[k])
        for text in (f"swap {pair('swap')} GB", f"compressor {pair('compressor')} GB",
                     f"load por CPU {pair('load')}", f"`node` {pair('node')}",
                     f"{cm.KILL_WAIT} s", f"{cm.HOST_MIN_AGE // 60} min"):
            self.assertIn(text, self.doc)


if __name__ == "__main__":
    unittest.main()
