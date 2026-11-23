"""Tests for frontend-design/scripts/ux_audit.py: generated files can opt out of the audit.

Run from the 0 Padrões root: python3 -m unittest discover -s .agents/scripts/tests
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / ".agents" / "skills" / "frontend-design" / "scripts" / "ux_audit.py"
GENERATOR = ROOT / ".agents" / "scripts" / "generate_catalog.py"
# Content that trips a blocking check (purple ban on a CSS value).
BAD_BODY = "<style>.x { color: #8B5CF6; }</style>\n"


def run_audit(folder: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(AUDIT), str(folder)], capture_output=True, text=True, check=False)


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


LINKS = "".join(f'<a href="/p{i}">Link {i}</a>\n' for i in range(9))  # 9 nav items: a Hick's Law issue in an app
# Real excerpt of the Inngage e-mail mensageria/broadcast/2026-10-migracao-web-app/email-01-historia-da-plinq.html
EMAIL_TABLE = '<table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="background-color: #FFF0F5;">\n'


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class UxAuditScope(unittest.TestCase):
    def test_agent_folder_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(Path(tmp) / ".agents" / "catalog.html", "<!DOCTYPE html>\n" + BAD_BODY)
            self.assertEqual(run_audit(Path(tmp)).returncode, 0)

    def test_exclude_glob_from_checklist_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / ".agents" / "checklist.json", json.dumps({"ux_audit": {"exclude": ["legacy/**"]}}))
            write(root / "legacy" / "old" / "page.html", "<!DOCTYPE html>\n" + BAD_BODY)
            self.assertEqual(run_audit(root).returncode, 0)
            write(root / "src" / "page.html", "<!DOCTYPE html>\n" + BAD_BODY)
            self.assertEqual(run_audit(root).returncode, 1)

    def test_app_page_keeps_app_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(Path(tmp) / "page.html", "<!DOCTYPE html>\n" + LINKS)
            self.assertIn("Hick's Law", run_audit(Path(tmp)).stdout)

    def test_email_markup_gets_reduced_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(Path(tmp) / "page.html", "<!DOCTYPE html>\n" + EMAIL_TABLE + LINKS + "</table>\n")
            result = run_audit(Path(tmp))
            self.assertNotIn("Hick's Law", result.stdout)
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_email_folder_gets_reduced_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(Path(tmp) / "mensageria" / "jornada" / "page.html", "<!DOCTYPE html>\n" + LINKS)
            self.assertNotIn("Hick's Law", run_audit(Path(tmp)).stdout)

    def test_email_still_checked_for_img_alt_and_purple(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(Path(tmp) / "page.html", "<!DOCTYPE html>\n" + EMAIL_TABLE + '<img src="a.png">\n</table>\n')
            self.assertIn("Missing img alt text", run_audit(Path(tmp)).stdout)
            write(Path(tmp) / "page.html", "<!DOCTYPE html>\n" + EMAIL_TABLE + BAD_BODY + "</table>\n")
            self.assertIn("PURPLE", run_audit(Path(tmp)).stdout)


class UxAuditFormNeedsRealMarkup(unittest.TestCase):
    def issue_for(self, body: str) -> bool:
        with tempfile.TemporaryDirectory() as tmp:
            write(Path(tmp) / "page.html", "<!DOCTYPE html>\n" + body)
            return "Form inputs without labels" in run_audit(Path(tmp)).stdout

    def test_word_containing_credit_is_not_a_form(self):
        # Inngage e-mail text: "acreditando no projeto"
        self.assertFalse(self.issue_for("<p>ter a mulher do nosso lado, acreditando no projeto.</p>\n"))

    def test_card_and_password_in_plain_text_are_not_a_form(self):
        self.assertFalse(self.issue_for('<div class="card"><p>Pay by card. Reset your password.</p></div>\n'))

    def test_real_select_and_textarea_without_labels_fail(self):
        self.assertTrue(self.issue_for("<select><option>a</option></select>\n"))
        self.assertTrue(self.issue_for("<textarea></textarea>\n"))

    def test_card_attribute_as_whole_word_counts(self):
        self.assertTrue(self.issue_for('<x-field name="card-number"></x-field>\n'))

    def test_labelled_form_passes(self):
        self.assertFalse(self.issue_for('<form><label>Nome <input type="text"></label></form>\n'))


class UxAuditPurpleOnlyInValues(unittest.TestCase):
    def audit(self, body: str, options: dict | None = None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            if options is not None:
                write(root / ".agents" / "checklist.json", json.dumps({"ux_audit": options}))
            write(root / "page.html", "<!DOCTYPE html>\n" + body)
            return run_audit(root)

    def test_css_comment_with_magenta_is_not_flagged(self):
        # Inngage in-app comment (Magenta is the Plinq brand colour)
        result = self.audit("<style>\n/* Destaque Rosa/Magenta */\n.x { color: #E6007E; }\n</style>\n")
        self.assertNotIn("PURPLE", result.stdout)

    def test_html_comment_and_prose_are_not_flagged(self):
        result = self.audit("<!-- never use violet -->\n<p>Never use purple in a UI.</p>\n")
        self.assertNotIn("PURPLE", result.stdout)

    def test_purple_values_are_flagged(self):
        for body in ("<style>.x { color: purple; }</style>\n",
                     "<style>.x { background: linear-gradient(violet, red); }</style>\n",
                     '<svg><path fill="#8B5CF6"/></svg>\n',
                     '<div class="bg-purple-500">x</div>\n'):
            self.assertIn("PURPLE", self.audit(body).stdout, body)

    def test_brand_colors_exempt_a_named_colour(self):
        body = "<style>.x { color: magenta; }</style>\n"
        self.assertIn("PURPLE", self.audit(body).stdout)
        self.assertNotIn("PURPLE", self.audit(body, {"brand_colors": ["Magenta"]}).stdout)

    def test_brand_colors_do_not_exempt_other_purples(self):
        body = "<style>.x { color: magenta; background: #8B5CF6; }</style>\n"
        self.assertIn("PURPLE", self.audit(body, {"brand_colors": ["magenta"]}).stdout)


if __name__ == "__main__":
    unittest.main()
