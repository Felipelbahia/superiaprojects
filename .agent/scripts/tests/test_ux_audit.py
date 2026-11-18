"""Tests for frontend-design/scripts/ux_audit.py: generated files can opt out of the audit.

Run from the 0 Padrões root: python3 -m unittest discover -s .agent/scripts/tests
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / ".agent" / "skills" / "frontend-design" / "scripts" / "ux_audit.py"
GENERATOR = ROOT / ".agent" / "scripts" / "generate_catalog.py"
# Content that trips a blocking check (purple ban), like skill docs embedded in the catalog do.
BAD_BODY = "<p>Never use purple or #8B5CF6 in a UI.</p>\n"


def run_audit(folder: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(AUDIT), str(folder)], capture_output=True, text=True)


class UxAuditSkipMarker(unittest.TestCase):
    def test_unmarked_file_still_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "page.html").write_text("<!DOCTYPE html>\n" + BAD_BODY, encoding="utf-8")
            result = run_audit(Path(tmp))
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("PURPLE", result.stdout)

    def test_marked_generated_file_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "page.html").write_text(
                "<!DOCTYPE html>\n<!-- ux-audit: skip (generated; embeds documentation as data) -->\n" + BAD_BODY,
                encoding="utf-8")
            result = run_audit(Path(tmp))
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_marker_far_from_the_top_does_not_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            body = BAD_BODY + ("<p>x</p>\n" * 400) + "<!-- ux-audit: skip (late) -->\n"
            (Path(tmp) / "page.html").write_text("<!DOCTYPE html>\n" + body, encoding="utf-8")
            self.assertEqual(run_audit(Path(tmp)).returncode, 1)

    def test_catalog_generator_emits_the_marker(self):
        self.assertIn("ux-audit: skip", GENERATOR.read_text(encoding="utf-8"))


class UxAuditFormCheckOnlyForMarkup(unittest.TestCase):
    def test_css_with_card_class_is_not_a_form(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "app.css").write_text(".card { padding: 8px; }\n", encoding="utf-8")
            result = run_audit(Path(tmp))
            self.assertNotIn("Form inputs without labels", result.stdout)

    def test_html_form_without_labels_still_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "page.html").write_text(
                "<!DOCTYPE html>\n<form><input type=\"text\"></form>\n", encoding="utf-8")
            result = run_audit(Path(tmp))
            self.assertIn("Form inputs without labels", result.stdout)


if __name__ == "__main__":
    unittest.main()
