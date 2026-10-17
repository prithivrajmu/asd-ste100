"""Exercise tag-release guards without GitHub access or publication."""

from copy import deepcopy
import unittest

from scripts.release import release_notes, release_pr_number


SHA = "a" * 40
CHANGELOG = """# Changelog

## [0.2.0](https://example.test/compare/v0.1.0...v0.2.0) (2026-10-17)

### Features

* Preserve uncertainty.

## 0.1.0

* First version.
"""


def version_pr():
    return {
        "number": 7,
        "merged_at": "2026-10-17T10:00:00Z",
        "merge_commit_sha": SHA,
        "base": {"ref": "main"},
        "labels": [{"name": "autorelease: pending"}],
    }


class ReleaseNotesChecks(unittest.TestCase):
    def test_extracts_only_the_tagged_entry(self):
        self.assertEqual(
            release_notes(CHANGELOG, "v0.2.0", "0.2.0\n"),
            "### Features\n\n* Preserve uncertainty.\n",
        )

    def test_accepts_plain_heading_and_final_entry(self):
        self.assertEqual(
            release_notes(CHANGELOG, "v0.1.0", "0.1.0"),
            "* First version.\n",
        )

    def test_rejects_invalid_or_prerelease_tags(self):
        for tag in ("0.2.0", "v0.02.0", "v0.2", "v0.2.0-beta.1", "v0.2.0\n", "main"):
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                release_notes(CHANGELOG, tag, "0.2.0")

    def test_rejects_tag_version_mismatch(self):
        with self.assertRaisesRegex(ValueError, "match version.txt"):
            release_notes(CHANGELOG, "v0.3.0", "0.2.0")

    def test_rejects_missing_versioned_changelog(self):
        with self.assertRaisesRegex(ValueError, "Merge the version PR first"):
            release_notes("## Unreleased\n\n* A change.\n", "v0.2.0", "0.2.0")

    def test_rejects_empty_or_duplicate_entries(self):
        for changelog in ("## 0.2.0\n\n", CHANGELOG + "\n## 0.2.0\n\n* Duplicate.\n"):
            with self.subTest(changelog=changelog), self.assertRaises(ValueError):
                release_notes(changelog, "v0.2.0", "0.2.0")

    def test_does_not_match_a_version_prefix(self):
        with self.assertRaises(ValueError):
            release_notes("## 0.2.01\n\n* Wrong.\n", "v0.2.0", "0.2.0")


class VersionPRChecks(unittest.TestCase):
    def test_accepts_the_merged_pending_version_pr(self):
        self.assertEqual(release_pr_number([version_pr()], SHA), 7)

    def test_accepts_a_tagged_pr_on_rerun(self):
        pr = version_pr()
        pr["labels"] = [{"name": "autorelease: tagged"}]
        self.assertEqual(release_pr_number([pr], SHA), 7)

    def test_rejects_non_release_merge_commits(self):
        for changes in (
            {"labels": []},
            {"merged_at": None},
            {"merge_commit_sha": "b" * 40},
            {"base": {"ref": "other"}},
            {"number": 0},
            {"number": True},
        ):
            pr = version_pr()
            pr.update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                release_pr_number([pr], SHA)

    def test_rejects_missing_or_ambiguous_prs(self):
        for prs in ([], [version_pr(), deepcopy(version_pr())]):
            with self.subTest(prs=prs), self.assertRaises(ValueError):
                release_pr_number(prs, SHA)

    def test_ignores_unrelated_associated_prs(self):
        unrelated = version_pr()
        unrelated["number"] = 8
        unrelated["labels"] = []
        self.assertEqual(release_pr_number([unrelated, version_pr()], SHA), 7)

    def test_requires_full_sha_and_api_list(self):
        for prs, sha in (([], "abc123"), ({}, SHA), ([], "a" * 40 + "\n")):
            with self.subTest(prs=prs, sha=sha), self.assertRaises(ValueError):
                release_pr_number(prs, sha)


if __name__ == "__main__":
    unittest.main()
