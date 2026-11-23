"""Offline tests for vet_package.py (no network). Run: python3 -I -m unittest discover -s tests"""
import datetime as dt
import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location("vet", pathlib.Path(__file__).parent.parent / "scripts" / "vet_package.py")
vet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vet)

NOW = dt.datetime(2026, 10, 12, tzinfo=dt.timezone.utc)


def meta(**kw):
    base = {"created": "2020-01-01T00:00:00Z", "weekly_downloads": 500000, "has_repo": True,
            "maintainers": 3, "install_scripts": [], "deprecated": False}
    base.update(kw)
    return base


class VetPackageTests(unittest.TestCase):
    def test_edit_distance(self):
        self.assertEqual(vet.edit_distance("express", "expresss"), 1)
        self.assertEqual(vet.edit_distance("requests", "reqeusts"), 2)
        self.assertEqual(vet.edit_distance("abc", "abc"), 0)

    def test_lookalike_found_and_exact_excluded(self):
        self.assertIn("express", vet.lookalikes("expresss", "npm"))
        self.assertIn("requests", vet.lookalikes("reqeusts", "pypi"))
        self.assertEqual(vet.lookalikes("express", "npm"), [])

    def test_short_names_are_not_flagged(self):
        self.assertEqual(vet.lookalikes("vue", "npm"), [])

    def test_missing_package_is_fail(self):
        out = vet.assess("zz-fake", "npm", None, 1000, 30, NOW)
        self.assertEqual(out[0][0], "FAIL")

    def test_healthy_package_has_no_warning(self):
        out = vet.assess("left-padder", "npm", meta(), 1000, 30, NOW)
        self.assertFalse([s for s, _ in out if s != "PASS"])

    def test_young_unpopular_package_warns(self):
        out = vet.assess("fresh-lib", "npm", meta(created="2026-10-01T00:00:00Z", weekly_downloads=12), 1000, 30, NOW)
        warns = [m for s, m in out if s == "WARN"]
        self.assertTrue(any("days ago" in m for m in warns))
        self.assertTrue(any("downloads" in m for m in warns))

    def test_install_script_and_missing_repo_warn(self):
        out = vet.assess("sketchy", "npm", meta(install_scripts=["postinstall"], has_repo=False), 1000, 30, NOW)
        text = " ".join(m for s, m in out if s == "WARN")
        self.assertIn("postinstall", text)
        self.assertIn("repository", text)


if __name__ == "__main__":
    unittest.main()
