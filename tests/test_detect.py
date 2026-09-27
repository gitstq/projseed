"""Tests for projseed.detect."""

import tempfile
import unittest
from pathlib import Path

from projseed.detect import detect_ecosystems, missing_meta


class DetectEcosystemsTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_empty_dir_no_ecosystems(self):
        self.assertEqual(detect_ecosystems(self.root), [])

    def test_detects_python(self):
        (self.root / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
        self.assertIn("python", detect_ecosystems(self.root))

    def test_detects_node_via_package_json(self):
        (self.root / "package.json").write_text("{}", encoding="utf-8")
        self.assertIn("node", detect_ecosystems(self.root))

    def test_detects_go(self):
        (self.root / "go.mod").write_text("module example.com/x\n", encoding="utf-8")
        self.assertIn("go", detect_ecosystems(self.root))

    def test_detects_rust(self):
        (self.root / "Cargo.toml").write_text("[package]\n", encoding="utf-8")
        self.assertIn("rust", detect_ecosystems(self.root))

    def test_detects_java(self):
        (self.root / "pom.xml").write_text("<project/>", encoding="utf-8")
        self.assertIn("java", detect_ecosystems(self.root))

    def test_multiple_ecosystems_sorted(self):
        (self.root / "pyproject.toml").write_text("", encoding="utf-8")
        (self.root / "go.mod").write_text("", encoding="utf-8")
        self.assertEqual(detect_ecosystems(self.root), ["go", "python"])


class MissingMetaTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_empty_dir_reports_everything(self):
        missing = missing_meta(self.root)
        rels = [m[0] for m in missing]
        self.assertIn(".gitignore", rels)
        self.assertIn("LICENSE", rels)
        self.assertIn("README.md", rels)
        self.assertIn(".editorconfig", rels)
        self.assertIn("CONTRIBUTING.md", rels)
        self.assertIn("CHANGELOG.md", rels)
        self.assertIn(".github/ISSUE_TEMPLATE/bug_report.yml", rels)
        self.assertIn("PULL_REQUEST_TEMPLATE.md", rels)

    def test_present_file_not_reported(self):
        (self.root / "README.md").write_text("# hi\n", encoding="utf-8")
        rels = [m[0] for m in missing_meta(self.root)]
        self.assertNotIn("README.md", rels)
        self.assertIn(".gitignore", rels)


if __name__ == "__main__":
    unittest.main()
