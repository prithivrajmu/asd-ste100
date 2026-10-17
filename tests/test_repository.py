"""Static repository checks. These do not run or grade an LLM."""

import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SEMVER = r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
RELEASE_MARKER = "x-release-please-version"


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


class SkillChecks(unittest.TestCase):
    def test_frontmatter(self):
        # Check this repository's deliberately small frontmatter shape.
        # This is not a general YAML parser or an Agent Skills certifier.
        match = re.match(r"\A---\n(.*?)\n---\n", read("SKILL.md"), re.DOTALL)
        self.assertIsNotNone(match, "SKILL.md needs delimited frontmatter")
        header = match.group(1)
        self.assertEqual(
            re.findall(r"^([a-z-]+):", header, re.MULTILINE),
            ["name", "description", "license", "metadata"],
        )
        self.assertRegex(header, r"(?m)^name: asd-ste100$")
        self.assertRegex(header, r"(?m)^license: MIT$")
        description = re.search(r"(?m)^description: (.+)$", header)
        self.assertIsNotNone(description)
        text = json.loads(description.group(1))
        self.assertIsInstance(text, str)
        self.assertTrue(0 < len(text) <= 1024)
        self.assertRegex(
            header,
            rf'(?m)^  version: "{SEMVER}" # {RELEASE_MARKER}$',
        )

    def test_core_stays_small(self):
        self.assertLess(len(read("SKILL.md").encode("utf-8")), 7500)
        self.assertLess(len(read("SKILL.md").splitlines()), 150)

    def test_references_are_discoverable(self):
        core = read("SKILL.md")
        for path in ("references/strict.md", "references/media.md"):
            with self.subTest(path=path):
                self.assertIn(f"]({path})", core)
                self.assertTrue(read(path).strip())

    def test_local_markdown_links(self):
        paths = [ROOT / name for name in ("SKILL.md", "README.md", "CHANGELOG.md")]
        paths += sorted((ROOT / "references").glob("*.md"))
        paths += sorted((ROOT / "evals").glob("*.md"))
        for path in paths:
            for target in re.findall(r"\]\(([^)\s]+)\)", path.read_text()):
                url = urlsplit(target)
                if url.scheme or url.netloc or not url.path:
                    continue
                destination = (path.parent / unquote(url.path)).resolve()
                with self.subTest(file=path.name, target=target):
                    self.assertTrue(destination.is_relative_to(ROOT))
                    self.assertTrue(destination.is_file(), f"Missing link: {target}")


class ReleaseChecks(unittest.TestCase):
    def setUp(self):
        self.version = read("version.txt").strip()
        self.config = json.loads(read("release-please-config.json"))
        self.package = self.config["packages"]["."]

    def test_version_is_stable_semver(self):
        self.assertRegex(self.version, rf"^{SEMVER}$")
        self.assertEqual(read("version.txt"), self.version + "\n")

    def test_versions_match(self):
        manifest = json.loads(read(".release-please-manifest.json"))
        self.assertEqual(manifest, {".": self.version})
        for path in ("SKILL.md", "README.md"):
            lines = [line for line in read(path).splitlines() if RELEASE_MARKER in line]
            with self.subTest(path=path):
                self.assertEqual(len(lines), 1, "Need one annotated version line")
                self.assertEqual(re.findall(SEMVER, lines[0]), [self.version])

    def test_release_updater_targets(self):
        self.assertEqual(self.package["release-type"], "simple")
        self.assertEqual(self.package["version-file"], "version.txt")
        self.assertEqual(
            self.package["extra-files"],
            [
                {"type": "generic", "path": "SKILL.md"},
                {"type": "generic", "path": "README.md"},
            ],
        )
        self.assertTrue((ROOT / "CHANGELOG.md").is_file())
        self.assertRegex(self.config["bootstrap-sha"], r"^[0-9a-f]{40}$")

    def test_release_version_policy(self):
        self.assertIs(self.package["include-component-in-tag"], False)
        self.assertIs(self.package["include-v-in-tag"], True)
        self.assertIs(self.package["bump-minor-pre-major"], False)
        self.assertIs(self.package["bump-patch-for-minor-pre-major"], False)

    def test_actions_are_pinned(self):
        for path in sorted((ROOT / ".github/workflows").glob("*.yml")):
            actions = re.findall(r"(?m)^\s+- uses: (\S+)", path.read_text())
            self.assertTrue(actions)
            for action in actions:
                with self.subTest(workflow=path.name, action=action):
                    self.assertRegex(action, r"^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_./-]+@[0-9a-f]{40}$")

    def test_main_only_prepares_versions(self):
        workflow = read(".github/workflows/checks.yml")
        self.assertIn("needs: validate", workflow)
        self.assertIn("github.event_name == 'push' && github.ref == 'refs/heads/main'", workflow)
        self.assertIn("skip-github-release: true", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("secrets.RELEASE_PLEASE_TOKEN || github.token", workflow)
        self.assertIn("python -m unittest discover -s tests -v", workflow)
        self.assertIn('gh workflow run checks.yml --ref "$branch"', workflow)
        self.assertNotIn("gh release create", workflow)
        self.assertNotIn("git tag", workflow)
        self.assertNotIn("pull_request_target", workflow)

    def test_publishing_requires_a_validated_tag(self):
        workflow = read(".github/workflows/release.yml")
        self.assertIn('tags: ["v*"]', workflow)
        self.assertIn("needs: validate", workflow)
        self.assertIn("github.event_name == 'push' && startsWith(github.ref, 'refs/tags/v')", workflow)
        self.assertIn("python -m unittest discover -s tests -v", workflow)
        self.assertIn("git merge-base --is-ancestor HEAD origin/main", workflow)
        self.assertIn('python scripts/release.py notes --tag "$TAG_NAME"', workflow)
        self.assertIn('python scripts/release.py pr --sha "$sha"', workflow)
        self.assertIn('gh release create "$TAG_NAME" --verify-tag', workflow)
        self.assertIn('gh pr edit "$PR_NUMBER" --remove-label "autorelease: pending"', workflow)
        self.assertNotIn("branches:", workflow)
        self.assertNotIn("workflow_dispatch:", workflow)
        self.assertNotIn("pull_request:", workflow)
        self.assertNotIn("git tag", workflow)


class EvaluationFixtureChecks(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads(read("evals/cases.json"))

    def test_case_shape(self):
        self.assertIsInstance(self.cases, list)
        self.assertGreaterEqual(len(self.cases), 12)
        for case in self.cases:
            with self.subTest(case=case.get("id")):
                self.assertEqual(
                    set(case), {"id", "task", "prompt", "source", "must", "must_not"}
                )
                self.assertRegex(case["id"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                for field in ("task", "prompt", "source"):
                    self.assertIsInstance(case[field], str)
                    self.assertTrue(case[field].strip())
                for field in ("must", "must_not"):
                    self.assertIsInstance(case[field], list)
                    self.assertTrue(case[field])
                    self.assertTrue(all(isinstance(item, str) and item.strip() for item in case[field]))

    def test_case_ids_are_unique(self):
        ids = [case["id"] for case in self.cases]
        self.assertEqual(len(ids), len(set(ids)))

    def test_task_coverage(self):
        self.assertEqual(
            {case["task"] for case in self.cases},
            {"rewrite", "explain", "summarize", "strict", "diagram", "html", "video"},
        )

    def test_evaluation_procedure_exists(self):
        self.assertTrue(read("evals/README.md").strip())


if __name__ == "__main__":
    unittest.main()
