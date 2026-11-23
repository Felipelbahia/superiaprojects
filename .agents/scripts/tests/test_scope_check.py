"""Tests for scope_check.py (the diff stays inside the scope the plan declares in a `Scope:` line).

Run from the 0 Padrões root: python3 -m unittest discover -s .agents/scripts/tests
Real git repositories in a temp folder; nothing outside it is touched.
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))

import scope_check as sc


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def make_repo(tmp: str) -> Path:
    repo = Path(tmp)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "t")
    (repo / "src").mkdir()
    (repo / "src" / "a.py").write_text("a = 1\n", encoding="utf-8")
    (repo / "README.md").write_text("hi\n", encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "init")
    return repo


def write_plan(repo: Path, text: str) -> None:
    plan = repo / ".agents" / "plans" / "00 Plan.md"
    plan.parent.mkdir(parents=True, exist_ok=True)
    plan.write_text(text, encoding="utf-8")


class Globs(unittest.TestCase):
    def test_star_does_not_cross_folders_but_double_star_does(self):
        self.assertTrue(sc.in_scope("src/a.py", ["src/*.py"]))
        self.assertFalse(sc.in_scope("src/deep/a.py", ["src/*.py"]))
        self.assertTrue(sc.in_scope("src/deep/a.py", ["src/**"]))
        self.assertTrue(sc.in_scope("src/deep/a.py", ["**/a.py"]))

    def test_a_folder_name_covers_everything_under_it(self):
        self.assertTrue(sc.in_scope("src/deep/a.py", ["src/"]))
        self.assertTrue(sc.in_scope("src/deep/a.py", ["src"]))
        self.assertFalse(sc.in_scope("srcx/a.py", ["src"]))

    def test_globs_that_start_with_a_dot_match(self):
        # str.lstrip("./") strips every leading "." and "/", turning ".agents/x" into "agent/x": only the "./" prefix goes
        self.assertTrue(sc.in_scope(".agents/skills/x/SKILL.md", [".agents/skills/x/SKILL.md"]))
        self.assertTrue(sc.in_scope(".agents/skills/x/SKILL.md", [".agents/skills/"]))
        self.assertTrue(sc.in_scope(".agents/skills/x/SKILL.md", [".agents/**"]))
        self.assertTrue(sc.in_scope(".github/workflows/ci.yml", [".github/**"]))
        self.assertTrue(sc.in_scope(".githooks/pre-commit", [".githooks"]))
        self.assertTrue(sc.in_scope(".env.example", [".env.example"]))
        self.assertFalse(sc.in_scope("agent/skills/x/SKILL.md", [".agents/**"]))

    def test_a_leading_dot_slash_is_still_ignored(self):
        self.assertTrue(sc.in_scope("catalog/rules.json", ["./catalog/"]))
        self.assertTrue(sc.in_scope("src/a.py", ["./src/*.py"]))
        self.assertTrue(sc.in_scope(".agents/x.md", ["./.agents/x.md"]))

    def test_plans_and_inbox_are_always_allowed(self):
        self.assertTrue(sc.in_scope(".agents/plans/x/02 Plan.md", ["src/**"]))
        self.assertTrue(sc.in_scope("inbox/001-x.md", ["src/**"]))

    def test_scope_line_parsing(self):
        text = "# Plan\nScope: src/**, README.md\n- docs/*.md\n\nother\n"
        self.assertEqual(sc.parse_scope(text), ["src/**", "README.md", "docs/*.md"])
        self.assertEqual(sc.parse_scope("no scope here\n"), None)


class Run(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = make_repo(self.tmp.name)
        os.environ.pop("ALLOW_SCOPE_DIFF", None)

    def test_clean_diff_inside_scope_passes(self):
        write_plan(self.repo, "Scope: src/**\n")
        (self.repo / "src" / "a.py").write_text("a = 2\n", encoding="utf-8")
        self.assertEqual(sc.main([str(self.repo)]), 0)

    def test_file_outside_scope_fails_and_is_named(self):
        write_plan(self.repo, "Scope: src/**\n")
        (self.repo / "README.md").write_text("changed\n", encoding="utf-8")
        (self.repo / "new.txt").write_text("new\n", encoding="utf-8")
        files = sc.outside_scope(self.repo, ["src/**"])
        self.assertEqual(sorted(files), ["README.md", "new.txt"])
        self.assertEqual(sc.main([str(self.repo)]), 1)

    def test_plan_without_scope_passes_with_a_warning(self):
        write_plan(self.repo, "# Plan without a scope line\n")
        (self.repo / "README.md").write_text("changed\n", encoding="utf-8")
        self.assertEqual(sc.main([str(self.repo)]), 0)

    def test_no_plan_at_all_passes_with_a_warning(self):
        (self.repo / "README.md").write_text("changed\n", encoding="utf-8")
        self.assertEqual(sc.main([str(self.repo)]), 0)

    def test_owner_release_with_env_var(self):
        write_plan(self.repo, "Scope: src/**\n")
        (self.repo / "README.md").write_text("changed\n", encoding="utf-8")
        os.environ["ALLOW_SCOPE_DIFF"] = "1"
        self.addCleanup(os.environ.pop, "ALLOW_SCOPE_DIFF", None)
        self.assertEqual(sc.main([str(self.repo)]), 0)

    def test_staged_mode_ignores_what_is_not_staged(self):
        write_plan(self.repo, "Escopo: src/**\n")
        (self.repo / "README.md").write_text("changed, not staged\n", encoding="utf-8")
        (self.repo / "src" / "a.py").write_text("a = 3\n", encoding="utf-8")
        git(self.repo, "add", "src/a.py")
        self.assertEqual(sc.main([str(self.repo), "--staged"]), 0)
        git(self.repo, "add", "README.md")
        self.assertEqual(sc.main([str(self.repo), "--staged"]), 1)

    def test_outside_scope_mentions_previous_plan_when_covered_there(self):
        plan1 = self.repo / ".agents" / "plans" / "execution-loops" / "Loop 1" / "02 Plan.md"
        plan1.parent.mkdir(parents=True, exist_ok=True)
        plan1.write_text("Scope: src/a.py, README.md\n", encoding="utf-8")
        # Ensure distinct mtime
        os.utime(plan1, (1000, 1000))

        plan2 = self.repo / ".agents" / "plans" / "execution-loops" / "Loop 2" / "02 Plan.md"
        plan2.parent.mkdir(parents=True, exist_ok=True)
        plan2.write_text("Scope: src/a.py\n", encoding="utf-8")
        os.utime(plan2, (2000, 2000))

        (self.repo / "src" / "a.py").write_text("a = 99\n", encoding="utf-8")
        (self.repo / "README.md").write_text("modified in loop 1\n", encoding="utf-8")

        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            ret = sc.main([str(self.repo)])
        output = buf.getvalue()
        self.assertEqual(ret, 1)
        self.assertIn("README.md (covered by previous plan:", output)
        self.assertIn("To commit multiple loops together, expand the `Scope:`", output)

    def test_not_a_git_repo_passes_with_a_warning(self):
        with tempfile.TemporaryDirectory() as plain:
            self.assertEqual(sc.main([plain]), 0)


if __name__ == "__main__":
    unittest.main()
