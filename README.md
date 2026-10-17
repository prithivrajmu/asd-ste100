# asd-ste100

An agent skill for clear technical explanations and rewrites, inspired by [ASD-STE100 Simplified Technical English](https://www.asd-ste100.org/).
It defaults to **80% STE**: short sentences, plain words, and normal technical vocabulary.

Version: **0.1.0** <!-- x-release-please-version -->

The relaxed style takes inspiration from [Andrej Karpathy's STE tip](https://x.com/karpathy/status/2105819303471976479).
"80%" describes a writing style, not a compliance score.

## What improves

- **Meaning stays first.** Keep uncertainty, quantities, conditions, exceptions, and unknown actors.
- **Tasks stay distinct.** A rewrite keeps all facts. A summary selects facts without removing material caveats. An explanation uses evidence.
- **Literal content stays intact.** Do not silently change commands, identifiers, code, or quoted errors.
- **Strict mode stays honest.** Check the applicable standard when available. Do not invent dictionary approval or claim verified compliance.
- **Extra guidance loads when needed.** The core skill links to separate [strict-mode](references/strict.md) and [media](references/media.md) notes.
- **Media stays optional.** Use diagrams when helpful. Create HTML or video only when requested. State what was actually rendered or tested.

## Install

For agents supported by the Skills CLI:

```bash
npx skills add prithivrajmu/asd-ste100
```

Or clone the **whole repository**, including `references/`, into your agent's skills directory. For example:

```bash
git clone https://github.com/prithivrajmu/asd-ste100 ~/.claude/skills/asd-ste100
```

Use the skills directory for your own agent if it differs from this example.

## Use

```text
Explain this function in STE.
Rewrite this PR description in 80% ASD-STE100. Keep all conditions.
Summarize this incident in three bullets. Keep uncertainty explicit.
Explain how the cache works in strict STE. State any verification limit.
Rewrite this error message in STE and show the changes.
Explain the request flow as a diagram.
Explain how this scheduler works in a self-contained HTML page.
Create a mathematical explainer video on attention. Check local tools first.
```

A video render needs suitable local tools, such as Python, Manim Community, and `ffmpeg`.
If tools are missing, the skill should provide a storyboard or source and state the limit.
Remote narration and tool installation require permission. Keep API keys in environment variables, not chat or source files.

## Update an installed copy

For an installation managed by the Skills CLI:

```bash
npx skills update asd-ste100
```

Use the CLI's scope options if you have both project and global installations.
This follows the CLI's tracked source. It is not a promise to install only tagged releases.

For a clone that follows `main`, inspect local changes and then update without a merge commit:

```bash
git -C ~/.claude/skills/asd-ste100 status --short
git -C ~/.claude/skills/asd-ste100 pull --ff-only
```

Keep local edits safe before updating. A copied `SKILL.md` does not update itself.
No scheduler, background updater, or installed skill is changed by this repository's release workflow.

## Automatic versions and releases

Version preparation and publication are separate. **Merging to `main` never creates a tag or publishes a release.**

1. Merge a Conventional Commit into `main`.
2. Repository checks run. [Release Please](https://github.com/googleapis/release-please) opens or updates a version PR with the next version and changelog.
3. Review and merge the version PR. This only commits the prepared version. It does not publish anything.
4. When ready, manually cut and push a matching `vMAJOR.MINOR.PATCH` tag at that version PR's merge commit.
5. The tag workflow validates the commit, versions, changelog, and repository checks, then publishes a GitHub release for the existing tag.

For example, after a version PR prepares `0.2.0`:

```bash
git fetch origin main --tags
# Replace VERSION_PR_MERGE_SHA with the merge commit shown on the version PR.
git tag -a v0.2.0 VERSION_PR_MERGE_SHA -m "Release v0.2.0"
git push origin v0.2.0
```

Use the version actually prepared by the PR. Do not tag an unrelated later commit, a branch outside `main`, or an unversioned bootstrap commit.
The workflow rejects mismatched tags, missing changelog entries, and tags not on a merged version PR.
Only stable `vMAJOR.MINOR.PATCH` tags are supported. There is no manual-dispatch publish path.

A merged version PR stays pending until its tag release succeeds. The tag workflow marks it as tagged so Release Please can prepare the next version.
Rerunning the tag workflow does not create a duplicate release.

The initial `0.1.0` is a bootstrap baseline, not a claim that a release already exists.
The configuration starts its first changelog after commit `577fc01` so it does not replay the original history.

| Commit | Change |
|---|---|
| `fix: preserve uncertainty in rewrites` | Patch |
| `feat: add an accessible HTML format` | Minor |
| `feat!: change the default output contract` | Major, including before 1.0 |
| `docs: clarify installation` or `chore: update tooling` | No release on its own |

Use Conventional Commit messages for squash merges too. Release Please reads the commit history, not just PR labels.
It updates `version.txt`, `SKILL.md` metadata, this README, `CHANGELOG.md`, and `.release-please-manifest.json` together.
Do not bump those files independently.

### One-time GitHub setup

1. Enable Actions for the repository. Enable **Allow GitHub Actions to create and approve pull requests** under **Settings → Actions → General**. The workflow creates PRs but never approves or merges them.
2. Use the built-in `GITHUB_TOKEN`. The version-PR job explicitly dispatches validation on its PR branch, so no separate token is required for those checks.
3. Make **Validate skill** a required check in your branch protection or ruleset if your review policy requires it. Keep a human review for version PRs.
4. Merge a `fix:` or `feat:` commit to start version preparation. Push a matching version tag only when you want to publish.

An optional `RELEASE_PLEASE_TOKEN` can override the token used to create the version PR. It is not required.
`GITHUB_TOKEN` does not trigger ordinary workflows from bot-created PRs. Explicit `workflow_dispatch` is the supported exception used here.
A version PR dispatch runs checks only, never publication. No npm account, package registry, LLM API, or stored personal token is needed.

Workflow actions are pinned to immutable revisions. Dependabot proposes monthly action updates.
There is no automatic merge or forced update of a user's installed skill.

## Checks and evaluations

Run the dependency-free repository checks with Python 3.12 or later:

```bash
python3 -m unittest discover -s tests -v
```

These checks cover metadata, version consistency, local reference links, release annotations, and evaluation fixtures.
They also test tag/version mismatches, changelog extraction, and the requirement to tag a merged version PR.
They do **not** measure LLM behavior or prove STE compliance.

The behavioral cases in [`evals/cases.json`](evals/cases.json) cover meaning preservation, strict mode, source-text instructions, multilingual output, and media limits.
Use [the evaluation procedure](evals/README.md) to compare the current skill with a proposed change on the same model.

## Limits

- This skill does not bundle the ASD-STE100 standard or dictionary. Obtain the applicable reference from [asd-ste100.org](https://www.asd-ste100.org/).
- It does not certify compliance. Safety-critical documentation needs review against the applicable standard by a qualified reviewer.
- It is not for creative or marketing text.
- Releasing the skill does not automatically update installed copies or the ASD-STE100 standard.

## Credits

- Andrej Karpathy, for the "80% ASD-STE100" tip.
- [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill), which this skill started from, including the meaning-preservation guard rails.

## License

MIT. See [LICENSE](LICENSE).
