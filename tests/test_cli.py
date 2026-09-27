"""End-to-end tests for the projseed CLI, run in a temp directory."""

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from projseed import templates
from projseed.cli import main


class CLITestBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def run_cli(self, *argv) -> int:
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(list(argv))
        self._stdout = buf.getvalue()
        return rc


class InitTests(CLITestBase):
    def test_init_non_interactive_generates_all_files(self):
        rc = self.run_cli(
            "init", "python", "general",
            "--out-dir", str(self.root),
            "--license", "mit",
            "--holder", "gitstq",
            "--year", "2026",
            "--project", "demo",
            "--non-interactive",
        )
        self.assertEqual(rc, 0, msg=self._stdout)
        for rel in [
            ".gitignore", "LICENSE", "README.md", ".editorconfig",
            "CONTRIBUTING.md", "CHANGELOG.md",
            ".github/ISSUE_TEMPLATE/bug_report.yml",
            ".github/ISSUE_TEMPLATE/feature_request.yml",
            "PULL_REQUEST_TEMPLATE.md",
        ]:
            self.assertTrue((self.root / rel).exists(), f"missing {rel}")

    def test_init_license_contains_holder_and_year(self):
        self.run_cli(
            "init", "--out-dir", str(self.root),
            "--license", "mit", "--holder", "gitstq", "--year", "2026",
            "--non-interactive",
        )
        lic = (self.root / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 gitstq", lic)
        self.assertIn("MIT License", lic)

    def test_init_idempotent_skips_existing(self):
        common = [
            "init", "--out-dir", str(self.root),
            "--license", "mit", "--holder", "gitstq", "--year", "2026",
            "--non-interactive",
        ]
        self.run_cli(*common)
        before = (self.root / "LICENSE").read_text(encoding="utf-8")
        rc = self.run_cli(*common)
        self.assertEqual(rc, 0)
        after = (self.root / "LICENSE").read_text(encoding="utf-8")
        self.assertEqual(before, after)
        self.assertIn("exists", self._stdout)

    def test_force_overwrites(self):
        common = [
            "init", "--out-dir", str(self.root),
            "--license", "mit", "--holder", "gitstq", "--year", "2026",
            "--project", "demo",
            "--non-interactive",
        ]
        self.run_cli(*common)
        (self.root / "README.md").write_text("CUSTOM CONTENT\n", encoding="utf-8")
        self.run_cli(*common, "--force")
        readme = (self.root / "README.md").read_text(encoding="utf-8")
        self.assertNotEqual(readme, "CUSTOM CONTENT\n")
        self.assertIn("# demo", readme)


class AddTests(CLITestBase):
    def test_add_appends_python_patterns(self):
        (self.root / ".gitignore").write_text("# custom\n.DS_Store\n", encoding="utf-8")
        rc = self.run_cli("add", "python", "--out-dir", str(self.root))
        self.assertEqual(rc, 0)
        body = (self.root / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("# custom", body)  # preserved
        self.assertIn("__pycache__/", body)

    def test_add_does_not_duplicate_existing(self):
        (self.root / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
        self.run_cli("add", "python", "--out-dir", str(self.root))
        body = (self.root / ".gitignore").read_text(encoding="utf-8")
        self.assertEqual(body.count("__pycache__/"), 1)


class LicenseTests(CLITestBase):
    def test_every_supported_license_renders(self):
        for key in templates.LICENSE_BUILDERS:
            rc = self.run_cli(
                "license", key, "--out-dir", str(self.root),
                "--holder", "gitstq", "--year", "2026", "--force",
            )
            self.assertEqual(rc, 0, msg=self._stdout)
            text = (self.root / "LICENSE").read_text(encoding="utf-8")
            self.assertIn("2026", text)
            self.assertIn("gitstq", text)

    def test_unknown_license_errors(self):
        rc = self.run_cli("license", "gpl-99", "--out-dir", str(self.root))
        self.assertEqual(rc, 2)


class SingleFileSubcommandTests(CLITestBase):
    def test_readme(self):
        rc = self.run_cli("readme", "--out-dir", str(self.root),
                          "--holder", "x", "--year", "2026", "--project", "demo")
        self.assertEqual(rc, 0)
        self.assertIn("# demo", (self.root / "README.md").read_text(encoding="utf-8"))

    def test_editorconfig(self):
        rc = self.run_cli("editorconfig", "--out-dir", str(self.root))
        self.assertEqual(rc, 0)
        self.assertIn("root = true", (self.root / ".editorconfig").read_text(encoding="utf-8"))

    def test_contributing(self):
        rc = self.run_cli("contributing", "--out-dir", str(self.root), "--project", "demo")
        self.assertEqual(rc, 0)
        self.assertIn("demo", (self.root / "CONTRIBUTING.md").read_text(encoding="utf-8"))

    def test_changelog(self):
        rc = self.run_cli("changelog", "--out-dir", str(self.root),
                           "--holder", "x", "--year", "2026")
        self.assertEqual(rc, 0)
        body = (self.root / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("Keep a Changelog", body)
        self.assertIn("2026", body)

    def test_issue_templates(self):
        rc = self.run_cli("issue-templates", "--out-dir", str(self.root))
        self.assertEqual(rc, 0)
        self.assertTrue((self.root / ".github/ISSUE_TEMPLATE/bug_report.yml").exists())
        self.assertTrue((self.root / ".github/ISSUE_TEMPLATE/feature_request.yml").exists())
        self.assertTrue((self.root / "PULL_REQUEST_TEMPLATE.md").exists())


class DetectTests(CLITestBase):
    def test_detect_reports_missing(self):
        rc = self.run_cli("detect", "--out-dir", str(self.root))
        self.assertEqual(rc, 1)
        self.assertIn("missing meta files", self._stdout)

    def test_detect_clean_repo_returns_zero(self):
        # Generate everything first.
        self.run_cli(
            "init", "--out-dir", str(self.root),
            "--license", "mit", "--holder", "x", "--year", "2026",
            "--non-interactive",
        )
        rc = self.run_cli("detect", "--out-dir", str(self.root))
        self.assertEqual(rc, 0, msg=self._stdout)
        self.assertIn("all expected meta files", self._stdout)


if __name__ == "__main__":
    unittest.main()
