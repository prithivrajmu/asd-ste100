"""Offline release guards. Only the tag workflow calls GitHub to publish."""

import argparse
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SEMVER = r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
RELEASE_LABELS = {"autorelease: pending", "autorelease: tagged"}


def release_notes(changelog, tag, version):
    """Require a stable tag matching the prepared version and changelog entry."""
    if not re.fullmatch(rf"v{SEMVER}", tag):
        raise ValueError("Release tags must use vMAJOR.MINOR.PATCH without leading zeros")
    if tag != f"v{version.strip()}":
        raise ValueError("The tag must match version.txt at the tagged commit")
    escaped = re.escape(version.strip())
    heading = rf"^## (?:\[{escaped}\](?:\([^\n)]*\))?|{escaped})(?:[ \t]+[^\n]*)?$"
    matches = list(re.finditer(heading, changelog, re.MULTILINE))
    if len(matches) != 1:
        raise ValueError("Merge the version PR first: need exactly one matching changelog entry")
    remainder = changelog[matches[0].end():]
    next_heading = re.search(r"^## ", remainder, re.MULTILINE)
    notes = remainder[:next_heading.start()] if next_heading else remainder
    if not notes.strip():
        raise ValueError("The versioned changelog entry must not be empty")
    return notes.strip() + "\n"


def release_pr_number(pull_requests, sha):
    """Require the tag to point to a merged version PR, not another main commit."""
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("Expected the full tagged commit SHA")
    if not isinstance(pull_requests, list):
        raise ValueError("Expected a list of pull requests from the commit API")
    candidates = []
    for pr in pull_requests:
        labels = {label["name"] for label in pr.get("labels", [])}
        if (
            pr.get("merged_at")
            and pr.get("merge_commit_sha") == sha
            and pr.get("base", {}).get("ref") == "main"
            and labels & RELEASE_LABELS
            and type(pr.get("number")) is int
            and pr["number"] > 0
        ):
            candidates.append(pr["number"])
    if len(candidates) != 1:
        raise ValueError("Tag the merge commit of exactly one prepared version PR on main")
    return candidates[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    notes = commands.add_parser("notes")
    notes.add_argument("--tag", required=True)
    notes.add_argument("--output", type=Path, required=True)
    pr = commands.add_parser("pr")
    pr.add_argument("--sha", required=True)
    args = parser.parse_args()
    try:
        if args.command == "notes":
            content = release_notes(
                (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"),
                args.tag,
                (ROOT / "version.txt").read_text(encoding="utf-8"),
            )
            args.output.write_text(content, encoding="utf-8")
        else:
            print(release_pr_number(json.load(sys.stdin), args.sha))
    except (ValueError, OSError) as error:
        parser.exit(1, f"Release blocked: {error}\n")


if __name__ == "__main__":
    main()
