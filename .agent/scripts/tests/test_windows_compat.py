"""Windows/portability regression tests: symlinks denied (WinError 1314), no owner paths, prompts rendered on install.

Run from the 0 Padrões root: python3 -m unittest discover -s .agent/scripts/tests
"""

import contextlib
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parent.parent
KIT = SCRIPTS.parent.parent
sys.path.insert(0, str(SCRIPTS))

import generate_catalog  # noqa: E402
import localize_paths  # noqa: E402
import linkutil  # noqa: E402
import render_prompts  # noqa: E402
import sync_entrypoints as se  # noqa: E402


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def denied(*args, **kwargs):
    raise OSError(1314, "A required privilege is not held by the client")


class NoOwnerPaths(unittest.TestCase):
    def test_runtime_scripts_have_no_hardcoded_user_path(self):
        for name in ("generate_catalog.py", "projects_audit.py"):
            text = (SCRIPTS / name).read_text(encoding="utf-8")
            self.assertNotIn("/Users/", text, name)

    def test_catalog_kit_root_comes_from_the_script_location(self):
        self.assertEqual(generate_catalog.GLOBAL_PADROES_DIR, KIT)

    def test_unwritable_cache_does_not_fail(self):
        with mock.patch.object(Path, "write_text", side_effect=PermissionError("denied")), contextlib.redirect_stdout(io.StringIO()) as out:
            generate_catalog.save_cache({"a": "b"})
        self.assertIn("cache", out.getvalue())

    def test_html_skips_central_files_that_do_not_exist(self):
        tag = generate_catalog.central_tag(Path("/nonexistent/x.js"), '<script src="{uri}"></script>')
        self.assertNotIn("<script", tag)


class SymlinkDenied(unittest.TestCase):
    """os-level symlink creation fails, as on Windows without Developer Mode."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        write(self.root / ".agent/skills/demo/SKILL.md", "---\nname: demo\ndescription: Use when demo\n---\nv1\n")
        write(self.root / ".agent/workflows/go.md", "---\ndescription: go\n---\nv1\n")
        self.patches = [
            mock.patch.object(se, "ROOT", self.root),
            mock.patch.object(se, "AGENT", self.root / ".agent"),
            mock.patch.object(Path, "symlink_to", denied),
        ]
        for p in self.patches:
            p.start()
        self.addCleanup(lambda: [p.stop() for p in self.patches])
        self.addCleanup(shutil.rmtree, self.root, True)

    def sync(self, check=False):
        with contextlib.redirect_stdout(io.StringIO()):
            return se.sync_links(check_only=check)

    def test_falls_back_to_copies(self):
        self.assertEqual(self.sync(), [])
        self.assertEqual((self.root / ".claude/commands/go.md").read_text(encoding="utf-8"), "---\ndescription: go\n---\nv1\n")
        self.assertTrue((self.root / ".claude/skills/demo/SKILL.md").is_file())
        self.assertTrue((self.root / ".cursor/commands/go.md").is_file())

    def test_copy_keeps_frontmatter_on_line_one(self):
        self.sync()
        self.assertTrue((self.root / ".claude/commands/go.md").read_text(encoding="utf-8").startswith("---"))

    def test_check_passes_after_sync_and_detects_stale_copy(self):
        self.sync()
        self.assertEqual(self.sync(check=True), [])
        write(self.root / ".agent/workflows/go.md", "---\ndescription: go\n---\nv2\n")
        problems = self.sync(check=True)
        self.assertTrue(any("out of date copy" in p for p in problems), problems)

    def test_sync_refreshes_stale_copy(self):
        self.sync()
        write(self.root / ".agent/skills/demo/SKILL.md", "---\nname: demo\ndescription: Use when demo\n---\nv2\n")
        self.assertEqual(self.sync(), [])
        self.assertIn("v2", (self.root / ".claude/skills/demo/SKILL.md").read_text(encoding="utf-8"))
        self.assertEqual(self.sync(check=True), [])

    def test_real_user_file_is_never_overwritten(self):
        mine = write(self.root / ".claude/commands/go.md", "my own command\n")
        problems = self.sync()
        self.assertEqual(mine.read_text(encoding="utf-8"), "my own command\n")
        self.assertTrue(any("REAL" in p for p in problems), problems)

    def test_removed_source_removes_the_managed_copy(self):
        self.sync()
        (self.root / ".agent/workflows/go.md").unlink()
        write(self.root / ".agent/workflows/other.md", "---\ndescription: other\n---\n")
        self.sync()
        self.assertFalse((self.root / ".claude/commands/go.md").exists())
        self.assertTrue((self.root / ".claude/commands/other.md").exists())

    def test_directory_junction_is_preferred_for_folders(self):
        def fake_junction(link, source):
            link.mkdir()
            return True

        with mock.patch.object(linkutil, "make_junction", fake_junction):
            how = linkutil.make_link(self.root / "j", "x", self.root / ".agent/skills/demo")
        self.assertEqual(how, "junction")


class LocalizePaths(unittest.TestCase):
    def setUp(self):
        self.kit = Path(tempfile.mkdtemp()) / "Pasta Ünica"
        (self.kit / ".agent").mkdir(parents=True)
        owner = localize_paths.OWNER_PATH
        self.plain = write(self.kit / ".agent/skills/x/SKILL.md", f'Leia "{owner}/.agent/skills/a/SKILL.md"\n')
        self.uri = write(self.kit / "docs/link.md", "[a](file:///Users/macbookpro/Documents/IA%20Projects/_Plataforma/0%20Padr%C3%B5es/x.md)\n")
        self.fixture = write(self.kit / ".agent/scripts/tests/fixtures/f.md", f"{owner}\n")
        self.arquivo = write(self.kit / "inbox/arquivo/old.md", f"{owner}\n")
        self.baseline = write(self.kit / ".agent/skills/project-initializer/legacy-generic-lines.txt", f"{owner}/x\n")
        self.hub = write(self.kit / "docs/hub.md", "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Mkt/x\n")
        self.addCleanup(shutil.rmtree, self.kit.parent, True)

    def test_plain_and_uri_forms_are_rewritten(self):
        localize_paths.localize(self.kit)
        here = self.kit.resolve().as_posix()
        self.assertIn(f'"{here}/.agent/skills/a/SKILL.md"', self.plain.read_text(encoding="utf-8"))
        self.assertIn("/Pasta%20%C3%9Cnica/x.md", self.uri.read_text(encoding="utf-8"))
        self.assertNotIn("macbookpro", self.uri.read_text(encoding="utf-8"))

    def test_skipped_areas_and_other_hubs_untouched(self):
        localize_paths.localize(self.kit)
        for f in (self.fixture, self.arquivo, self.baseline):
            self.assertIn(localize_paths.OWNER_PATH, f.read_text(encoding="utf-8"))
        self.assertIn("0 Mkt", self.hub.read_text(encoding="utf-8"))

    def test_idempotent_and_follows_a_move(self):
        localize_paths.localize(self.kit)
        self.assertEqual(localize_paths.localize(self.kit), [])
        moved = self.kit.parent / "Outro Lugar"
        self.kit.rename(moved)
        changed = localize_paths.localize(moved)
        self.assertTrue(changed)
        self.assertIn(moved.resolve().as_posix(), (moved / ".agent/skills/x/SKILL.md").read_text(encoding="utf-8"))

    def test_old_path_without_special_chars_keeps_plain_text_plain(self):
        plain_old = "/opt/kit"
        doc = write(self.kit / "docs/p.md", f"Leia {plain_old}/x.md e file://{plain_old}/y.md\n")
        (self.kit / ".agent/.kit-path").write_text(plain_old + "\n", encoding="utf-8")
        localize_paths.localize(self.kit)
        here = self.kit.resolve().as_posix()
        text = doc.read_text(encoding="utf-8")
        self.assertIn(f"Leia {here}/x.md", text)
        self.assertIn("file://" + here.replace(" ", "%20").replace("\u00dc", "%C3%9C") + "/y.md", text)

    def test_check_mode_reports_without_writing(self):
        before = self.plain.read_text(encoding="utf-8")
        reported = localize_paths.localize(self.kit, check_only=True)
        self.assertEqual(sorted(reported), sorted([self.plain, self.uri]))
        self.assertEqual(self.plain.read_text(encoding="utf-8"), before)

    def test_noop_on_the_owner_machine(self):
        with mock.patch.object(localize_paths, "OWNER_PATH", self.kit.resolve().as_posix()):
            self.assertEqual(localize_paths.localize(self.kit), [])


class RenderPrompts(unittest.TestCase):
    def setUp(self):
        self.kit = Path(tempfile.mkdtemp()) / "kit dir"
        write(self.kit / "prompts-template/01-a.md", 'Use "<SUPER_IA_PROJECTS_PATH>/.agent" aqui. <SUPER_IA_PROJECTS_PATH>\n')
        write(self.kit / "prompts-template/README.md", "indice\n")
        self.addCleanup(shutil.rmtree, self.kit.parent, True)

    def test_placeholder_replaced_with_kit_path(self):
        render_prompts.render(self.kit)
        text = (self.kit / "projetos/prompts/01-a.md").read_text(encoding="utf-8")
        self.assertNotIn("<SUPER_IA_PROJECTS_PATH>", text)
        self.assertIn(self.kit.resolve().as_posix() + "/.agent", text)

    def test_rewritten_on_every_run_and_local_only_files_kept(self):
        render_prompts.render(self.kit)
        write(self.kit / "projetos/prompts/01-a.md", "stale\n")
        write(self.kit / "projetos/prompts/99-mine.md", "mine\n")
        written, kept = render_prompts.render(self.kit)
        self.assertIn("kit dir", (self.kit / "projetos/prompts/01-a.md").read_text(encoding="utf-8"))
        self.assertEqual(kept, ["99-mine.md"])
        self.assertEqual(sorted(written), ["01-a.md", "README.md"])

    def test_real_templates_have_no_leftover_placeholder_after_render(self):
        tmp = Path(tempfile.mkdtemp()) / "k"
        shutil.copytree(KIT / "prompts-template", tmp / "prompts-template")
        self.addCleanup(shutil.rmtree, tmp.parent, True)
        render_prompts.render(tmp)
        for f in (tmp / "projetos/prompts").glob("*.md"):
            self.assertNotIn("<SUPER_IA_PROJECTS_PATH>", f.read_text(encoding="utf-8"), f.name)


class RelocatedKit(unittest.TestCase):
    """The kit is a wildcard: copied to any folder (spaces, accents), install.py must work and write only local paths."""

    @classmethod
    def setUpClass(cls):
        cls.base = Path(tempfile.mkdtemp())
        cls.kit = cls.base / "Meu Super Projeto de IA"
        ignore = shutil.ignore_patterns(".git", "__pycache__", "plans", "catalog.html", "catalog-data.js", "CATALOG.md", "projetos", "inbox", "instalacoes")
        cls.kit.mkdir()
        for item in (".agent", "prompts-template", "prompts"):  # prompts/ holds the sip-geral resolver
            shutil.copytree(KIT / item, cls.kit / item, ignore=ignore, symlinks=True)
        for name in ("CLAUDE.example.md", "install.py"):
            shutil.copyfile(KIT / name, cls.kit / name)
        cls.result = subprocess.run([sys.executable, str(cls.kit / "install.py")], cwd=cls.base, capture_output=True, text=True, encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.base, True)

    def test_install_succeeds_from_any_folder_and_any_cwd(self):
        self.assertEqual(self.result.returncode, 0, self.result.stdout + self.result.stderr)

    def test_catalog_has_no_foreign_absolute_paths(self):
        import json
        data = (self.kit / ".agent/catalog-data.js").read_text(encoding="utf-8")
        payload = json.loads(data[data.index("{"):data.rindex("}") + 1].replace("<\\!--", "<!--"))  # JS-only escapes of the generator
        paths = [i["abs_path"] for i in payload["items"]]
        self.assertTrue(paths)
        self.assertFalse([p for p in paths if "macbookpro" in p or Path(p).is_absolute()][:3], "catalog data must hold no machine-specific absolute path")
        head = (self.kit / ".agent/catalog.html").read_text(encoding="utf-8")[:4000]
        self.assertNotIn("/Users/macbookpro", head)

    def test_prompts_rendered_with_the_local_path(self):
        text = (self.kit / "projetos/prompts/01-atualizar-projeto-existente.md").read_text(encoding="utf-8")
        self.assertIn(self.kit.resolve().as_posix(), text)
        self.assertNotIn("<SUPER_IA_PROJECTS_PATH>", text)

    def test_versioned_docs_point_to_the_new_location(self):
        text = (self.kit / "prompts/resolver/sip-geral/SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn(localize_paths.OWNER_PATH, text)
        self.assertIn(self.kit.resolve().as_posix() + "/.agent/skills/", text)

    def test_rules_files_created(self):
        self.assertTrue((self.kit / "CLAUDE.md").is_file() and (self.kit / "AGENTS.md").is_file())


class Installer(unittest.TestCase):
    def test_install_sh_and_py_both_render_prompts(self):
        self.assertIn("render_prompts.py", (KIT / "install.sh").read_text(encoding="utf-8"))
        self.assertIn("render_prompts.py", (KIT / "install.py").read_text(encoding="utf-8"))
        self.assertTrue(subprocess.run([sys.executable, "-m", "py_compile", str(KIT / "install.py")]).returncode == 0)


if __name__ == "__main__":
    unittest.main()
