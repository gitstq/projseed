"""Tests for projseed.gitignore: merge, dedupe, negation preservation."""

import unittest

from projseed.gitignore import existing_patterns, merge_into
from projseed import templates


class ExistingPatternsTests(unittest.TestCase):
    def test_skips_blank_and_comments(self):
        text = "# a comment\n\n__pycache__/\n\n# another\nnode_modules/\n"
        self.assertEqual(existing_patterns(text), {"__pycache__/", "node_modules/"})

    def test_keeps_negation_distinct(self):
        text = "build/\n!important.log\n"
        pats = existing_patterns(text)
        self.assertIn("build/", pats)
        self.assertIn("!important.log", pats)


class MergeIntoTests(unittest.TestCase):
    def test_empty_existing_returns_block(self):
        out = merge_into("", "python", ["__pycache__/", "*.pyc"])
        self.assertIn("# --- projseed: python ---", out)
        self.assertIn("__pycache__/", out)
        self.assertIn("*.pyc", out)

    def test_appends_without_overwriting(self):
        existing = "# my custom rules\n.DS_Store\n"
        out = merge_into(existing, "python", ["__pycache__/"])
        self.assertTrue(out.startswith("# my custom rules\n.DS_Store\n"))
        self.assertIn("__pycache__/", out)

    def test_dedupes_already_present(self):
        existing = "__pycache__/\n"
        out = merge_into(existing, "python", ["__pycache__/", "*.pyc"])
        # The existing line is kept once; the incoming duplicate is dropped.
        self.assertEqual(out.count("__pycache__/"), 1)
        self.assertIn("*.pyc", out)

    def test_dedupe_within_incoming_batch(self):
        out = merge_into("", "x", ["a/", "a/", "b/"])
        self.assertEqual(out.count("a/"), 1)
        self.assertEqual(out.count("b/"), 1)

    def test_preserves_negation(self):
        existing = "build/\n"
        out = merge_into(existing, "x", ["!build/keep.me"])
        self.assertIn("!build/keep.me", out)
        # The positive rule is still there.
        self.assertIn("build/", out)

    def test_negation_not_dropped_when_positive_exists(self):
        # A later "foo" must not cancel out an earlier "!foo".
        existing = "!foo\n"
        out = merge_into(existing, "x", ["foo"])
        self.assertIn("!foo", out)
        self.assertIn("foo", out)

    def test_idempotent_when_nothing_new(self):
        existing = "# header\n__pycache__/\n"
        out = merge_into(existing, "python", ["__pycache__/"])
        self.assertEqual(out, existing)

    def test_header_comment_always_kept(self):
        out = merge_into("", "python", ["# Python section", "__pycache__/"])
        self.assertIn("# Python section", out)

    def test_all_presets_render(self):
        for name, pats in templates.GITIGNORE_PRESETS.items():
            out = merge_into("", name, pats)
            self.assertIn(f"# --- projseed: {name} ---", out)
            for p in pats:
                if p.startswith("#"):
                    continue
                self.assertIn(p, out, f"preset {name} missing pattern {p}")


if __name__ == "__main__":
    unittest.main()
