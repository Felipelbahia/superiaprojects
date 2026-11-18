"""Tests for lint-and-validate/scripts/lint_runner.py: Python projects lint only the files touched in git.

Run from the 0 Padrões root: python3 -m unittest discover -s .agent/scripts/tests
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RUNNER = Path(__file__).resolve().parents[3] / ".agent" / "skills" / "lint-and-validate" / "scripts" / "lint_runner.py"
BAD = "import os\n"  # ruff F401
GOOD = "X = 1\n"


def git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def make_repo(tmp: str) -> Path:
    """A committed Python project holding one old file with a ruff finding."""
    root = Path(tmp)
    git(root, "init", "-q")
    git(root, "config", "user.email", "t@t")
    git(root, "config", "user.name", "t")
    (root / "pyproject.toml").write_text("[project]\nname = 'x'\n", encoding="utf-8")
    (root / "old.py").write_text(BAD, encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "init")
    return root


def run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(RUNNER), str(root), *args], capture_output=True, text=True, timeout=120, check=False)


@unittest.skipUnless(shutil.which("ruff") and shutil.which("mypy"), "ruff and mypy are required")
class TouchedFilesOnly(unittest.TestCase):
    def test_old_findings_in_untouched_files_do_not_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            (root / "new.py").write_text(GOOD, encoding="utf-8")
            r = run(root)
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_finding_in_a_new_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            (root / "new.py").write_text(BAD, encoding="utf-8")
            r = run(root)
            self.assertEqual(r.returncode, 1, r.stdout)

    def test_finding_in_an_edited_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            (root / "old.py").write_text(BAD + "Y = 2\n", encoding="utf-8")
            self.assertEqual(run(root).returncode, 1)

    def test_no_touched_python_files_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            self.assertEqual(run(root).returncode, 0)

    def test_all_flag_lints_the_whole_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            self.assertEqual(run(root, "--all").returncode, 1)

    def test_since_ref_covers_committed_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            (root / "new.py").write_text(BAD, encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-q", "-m", "add")
            self.assertEqual(run(root).returncode, 0)  # nothing touched since HEAD
            self.assertEqual(run(root, "--since", "HEAD~1").returncode, 1)

    def test_not_a_git_repo_lints_everything(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pyproject.toml").write_text("[project]\nname = 'x'\n", encoding="utf-8")
            (root / "old.py").write_text(BAD, encoding="utf-8")
            self.assertEqual(run(root).returncode, 1)


if __name__ == "__main__":
    unittest.main()
