"""Tests for env_diff_check.py (no local config, .env, migrations or database targets slip into a commit).

Run from the 0 Padrões root: python3 -m unittest discover -s .agents/scripts/tests
Real git repositories in a temp folder. Synthetic database URLs are assembled at run time so the
kit's own secret scan never flags this file.
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))

import env_diff_check as ec  # noqa: E402

DB_URL = "post" + "gres://" + "user:pw" + "@db.example.com:5432/app"


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def make_repo(tmp: str) -> Path:
    repo = Path(tmp)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "t")
    (repo / "src").mkdir()
    (repo / "src" / "a.py").write_text("a = 1\n", encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "init")
    return repo


class PathRules(unittest.TestCase):
    def test_env_files_are_flagged_but_examples_are_not(self):
        for bad in [".env", ".env.local", "app/.env.production", "prod.env", "web/.env.staging"]:
            self.assertIsNotNone(ec.path_problem(bad), bad)
        for ok in [".env.example", ".env.sample", "app/.env.example", "src/environment.py"]:
            self.assertIsNone(ec.path_problem(ok), ok)

    def test_local_config_is_flagged(self):
        for bad in ["settings.local.json", ".claude/settings.local.json", "config.local.yaml", "local_settings.py", ".mcp.json"]:
            self.assertIsNotNone(ec.path_problem(bad), bad)

    def test_migrations_and_schema_are_flagged(self):
        for bad in ["supabase/migrations/001_init.sql", "db/migration/2.sql", "prisma/schema.prisma", "schema.sql"]:
            self.assertIsNotNone(ec.path_problem(bad), bad)
        self.assertIsNone(ec.path_problem("docs/SCHEMA.md"))

    def test_ordinary_files_pass(self):
        for ok in ["src/a.py", "README.md", "package.json", "docs/env-guide.md"]:
            self.assertIsNone(ec.path_problem(ok), ok)


class ContentRules(unittest.TestCase):
    def test_database_url_in_an_added_line_is_flagged(self):
        self.assertIsNotNone(ec.line_problem(f"DATABASE_URL = '{DB_URL}'"))
        self.assertIsNone(ec.line_problem("url = os.environ['DATABASE_URL']"))
        self.assertIsNone(ec.line_problem("see https://example.com/docs"))


class Run(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = make_repo(self.tmp.name)
        os.environ.pop("ALLOW_ENV_DIFF", None)

    def test_clean_diff_passes(self):
        (self.repo / "src" / "a.py").write_text("a = 2\n", encoding="utf-8")
        self.assertEqual(ec.main([str(self.repo)]), 0)

    def test_env_file_in_the_diff_fails(self):
        (self.repo / ".env.local").write_text("KEY=1\n", encoding="utf-8")
        self.assertEqual(ec.main([str(self.repo)]), 1)

    def test_gitignored_env_never_shows_up(self):
        (self.repo / ".gitignore").write_text(".env*\n!.env.example\n", encoding="utf-8")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "ignore")
        (self.repo / ".env").write_text("KEY=1\n", encoding="utf-8")
        self.assertEqual(ec.main([str(self.repo)]), 0)

    def test_env_example_passes(self):
        (self.repo / ".env.example").write_text("KEY=\n", encoding="utf-8")
        self.assertEqual(ec.main([str(self.repo)]), 0)

    def test_migration_added_fails(self):
        (self.repo / "migrations").mkdir()
        (self.repo / "migrations" / "001.sql").write_text("select 1;\n", encoding="utf-8")
        self.assertEqual(ec.main([str(self.repo)]), 1)

    def test_database_url_added_to_a_tracked_file_fails(self):
        (self.repo / "src" / "a.py").write_text(f"URL = '{DB_URL}'\n", encoding="utf-8")
        self.assertEqual(ec.main([str(self.repo)]), 1)

    def test_owner_release_with_env_var(self):
        (self.repo / ".env.local").write_text("KEY=1\n", encoding="utf-8")
        os.environ["ALLOW_ENV_DIFF"] = "1"
        self.addCleanup(os.environ.pop, "ALLOW_ENV_DIFF", None)
        self.assertEqual(ec.main([str(self.repo)]), 0)

    def test_staged_mode_ignores_what_is_not_staged(self):
        (self.repo / ".env.local").write_text("KEY=1\n", encoding="utf-8")
        self.assertEqual(ec.main([str(self.repo), "--staged"]), 0)
        git(self.repo, "add", "-f", ".env.local")
        self.assertEqual(ec.main([str(self.repo), "--staged"]), 1)

    def test_not_a_git_repo_passes_with_a_warning(self):
        with tempfile.TemporaryDirectory() as plain:
            self.assertEqual(ec.main([plain]), 0)


if __name__ == "__main__":
    unittest.main()
