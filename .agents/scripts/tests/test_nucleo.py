"""Tests for the SIP "núcleo": the few process skills a SIP resolver asks every consumer to have linked.

The list lives in `nucleo.json` next to the resolver (`{"skills": [...]}`), so it is versioned with the hub and any SIP can
declare its own. sips_status.py reports a missing, broken or wrong núcleo link; propagar_sip.py recreates it (and installs it
in cover mode) without ever touching a real file or folder, and keeps the links out of git.

Run from the 0 Padrões root: python3 -m unittest discover -s .agents/scripts/tests
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
KIT = SCRIPTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import linkutil  # noqa: E402
import test_propagar_sip as tp  # noqa: E402

STATUS = SCRIPTS / "sips_status.py"
HUB_DATE_OK = "2026-11-12"  # same date as the hub resolver in the fixtures, so the date hint is never the reason


def add_nucleo(hub: Path, names: list[str], resolver: str = "sip-x") -> None:
    (hub / ".agents" / "skills" / resolver / "nucleo.json").write_text(json.dumps({"skills": names}), encoding="utf-8")
    for n in names:
        d = hub / ".agents" / "skills" / n
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(f"---\nname: {n}\ndescription: Use when testing.\n---\n", encoding="utf-8")


def link_nucleo(proj: Path, hub: Path, name: str) -> None:
    (proj / ".agents" / "skills" / name).symlink_to(hub / ".agents" / "skills" / name)
    (proj / ".claude" / "skills" / name).symlink_to(f"../../.agents/skills/{name}")


def status(proj: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(STATUS), str(proj)], capture_output=True, text=True, timeout=60, check=False)


class LinkutilNucleo(unittest.TestCase):
    def test_reads_names_from_the_resolver_folder(self):
        with tempfile.TemporaryDirectory() as t:
            hub = tp.make_hub(Path(t), [])
            add_nucleo(hub, ["alpha", "beta"])
            self.assertEqual(linkutil.nucleo(hub, "sip-x"), ["alpha", "beta"])

    def test_no_file_means_no_nucleo(self):
        with tempfile.TemporaryDirectory() as t:
            hub = tp.make_hub(Path(t), [])
            self.assertEqual(linkutil.nucleo(hub, "sip-x"), [])

    def test_malformed_file_is_an_error_not_silence(self):
        with tempfile.TemporaryDirectory() as t:
            hub = tp.make_hub(Path(t), [])
            (hub / ".agents" / "skills" / "sip-x" / "nucleo.json").write_text("{not json", encoding="utf-8")
            with self.assertRaises(ValueError):
                linkutil.nucleo(hub, "sip-x")


class StatusNucleo(unittest.TestCase):
    def setup(self, root: Path, linked: bool):
        hub = tp.make_hub(root, ["a"])
        add_nucleo(hub, ["alpha"])
        proj = tp.make_project(root, hub, installed=HUB_DATE_OK)
        if linked:
            link_nucleo(proj, hub, "alpha")
        return hub, proj

    def test_missing_nucleo_link_is_reported(self):
        with tempfile.TemporaryDirectory() as t:
            _, proj = self.setup(Path(t), linked=False)
            r = status(proj)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("núcleo", r.stdout)
            self.assertIn("alpha", r.stdout)

    def test_complete_nucleo_is_up_to_date(self):
        with tempfile.TemporaryDirectory() as t:
            _, proj = self.setup(Path(t), linked=True)
            r = status(proj)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("[em dia]", r.stdout)

    def test_link_to_the_wrong_place_is_reported(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub, proj = self.setup(root, linked=False)
            (hub / ".agents" / "skills" / "outra").mkdir()
            (proj / ".agents" / "skills" / "alpha").symlink_to(hub / ".agents" / "skills" / "outra")
            (proj / ".claude" / "skills" / "alpha").symlink_to("../../.agents/skills/alpha")
            r = status(proj)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("alpha", r.stdout)

    def test_a_local_real_skill_with_the_same_name_is_the_projects_own(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub, proj = self.setup(root, linked=False)
            local = proj / ".agents" / "skills" / "alpha"
            local.mkdir()
            (local / "SKILL.md").write_text("minha", encoding="utf-8")
            (proj / ".claude" / "skills" / "alpha").symlink_to("../../.agents/skills/alpha")
            r = status(proj)
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_stub_exception_hub_does_not_need_the_nucleo_links(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = tp.make_hub(root, ["a"])
            add_nucleo(hub, ["alpha"])
            proj = tp.make_project(root, hub, installed=HUB_DATE_OK, links=False)
            real = proj / ".agents" / "skills" / "sip-x"
            real.mkdir()
            (real / "SKILL.md").write_text("stub", encoding="utf-8")
            (proj / ".claude" / "skills" / "sip-x").symlink_to(hub / ".agents" / "skills" / "sip-x")
            self.assertEqual(status(proj).returncode, 0, status(proj).stdout)


class PropagarNucleo(unittest.TestCase):
    def setup(self, root: Path):
        hub = tp.make_hub(root, ["a"])
        add_nucleo(hub, ["alpha", "beta"])
        proj = tp.make_project(root, hub, installed=HUB_DATE_OK)
        tp.register(hub, "proj", proj)
        return hub, proj

    def test_dry_run_lists_the_links_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub, proj = self.setup(root)
            before = tp.snapshot(root)
            r = tp.run(str(hub))
            self.assertEqual(tp.snapshot(root), before)
            self.assertIn("criaria link .agents/skills/alpha", r.stdout.replace("recriaria", "criaria"))
            self.assertIn("beta", r.stdout)

    def test_apply_creates_links_and_gitignore_lines_once(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub, proj = self.setup(root)
            tp.run(str(hub), "--apply")
            for n in ("alpha", "beta"):
                self.assertTrue((proj / ".agents" / "skills" / n / "SKILL.md").exists())
                self.assertTrue((proj / ".claude" / "skills" / n / "SKILL.md").exists())
            gi = (proj / ".gitignore").read_text(encoding="utf-8")
            for n in ("alpha", "beta"):
                self.assertEqual(gi.count(f".agents/skills/{n}\n"), 1)
                self.assertEqual(gi.count(f".claude/skills/{n}\n"), 1)
            tp.run(str(hub), "--apply")
            self.assertEqual((proj / ".gitignore").read_text(encoding="utf-8"), gi)

    def test_a_local_real_skill_is_not_touched_and_is_not_a_conflict(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub, proj = self.setup(root)
            local = proj / ".agents" / "skills" / "alpha"
            local.mkdir()
            (local / "SKILL.md").write_text("minha", encoding="utf-8")
            r = tp.run(str(hub), "--apply")
            self.assertFalse(local.is_symlink())
            self.assertEqual((local / "SKILL.md").read_text(encoding="utf-8"), "minha")
            self.assertNotIn("conflito", r.stdout)
            self.assertTrue((proj / ".claude" / "skills" / "alpha").is_symlink())
            self.assertEqual((proj / ".claude" / "skills" / "alpha" / "SKILL.md").read_text(encoding="utf-8"), "minha")
            self.assertNotIn(".agents/skills/alpha", (proj / ".gitignore").read_text(encoding="utf-8").splitlines())

    def test_cover_mode_installs_the_nucleo_in_a_new_project(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            hub = tp.make_hub(root, ["a"])
            add_nucleo(hub, ["alpha"])
            reg = tp.make_project(root, hub, name="registrado", installed=HUB_DATE_OK)
            link_nucleo(reg, hub, "alpha")
            tp.register(hub, "registrado", reg)
            new = root / "novo"
            (new / ".agents").mkdir(parents=True)
            fichas = tp.make_fichas(root, new)
            tp.run(str(hub), "--cobrir", "--fichas", str(fichas), "--apply")
            for base in (".agents", ".claude"):
                self.assertTrue((new / base / "skills" / "alpha" / "SKILL.md").exists(), base)
            gi = (new / ".gitignore").read_text(encoding="utf-8")
            self.assertIn(".claude/skills/alpha", gi)


class RealKitNucleo(unittest.TestCase):
    NUCLEO = KIT / "prompts" / "resolver" / "sip-geral" / "nucleo.json"

    def test_the_sip_geral_nucleo_exists_and_is_small_and_real(self):
        self.assertTrue(self.NUCLEO.is_file(), "falta prompts/resolver/sip-geral/nucleo.json")
        names = json.loads(self.NUCLEO.read_text(encoding="utf-8"))["skills"]
        self.assertTrue(0 < len(names) <= 10, f"o núcleo deve ter de 1 a 10 skills (tem {len(names)}): cada uma custa contexto em toda sessão")
        self.assertEqual(len(names), len(set(names)), "nome repetido no núcleo")
        for n in names:
            self.assertTrue((KIT / ".agents" / "skills" / n / "SKILL.md").is_file(), f"núcleo cita skill que não existe no hub: {n}")
        self.assertIn("execution-loop", names)


if __name__ == "__main__":
    unittest.main()
