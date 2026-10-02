# asd-ste100

An agent skill that makes Claude explain things in [ASD-STE100 Simplified Technical English](https://www.asd-ste100.org/). It defaults to "80% of the way to ASD-STE100".

The idea comes from [Andrej Karpathy](https://x.com/karpathy/status/2105819303471976479) (2 Oct 2026):

> Ask your LLM to explain something in ASD-STE100 ... it comes with heavy constraints on clean writing style that I often find a lot more readable. Sometimes I've tried to soften it a bit e.g. ask for "80% of the way to ASD-STE100" because the spec is quite stringent.

LLMs already know the standard. So the skill is one short file. It does three things:

1. It sets the level: **80%** by default, **100%** when you ask for "strict".
2. It lists the 80% rules, so that "80%" means the same thing every time.
3. It adds guard rails: keep every fact, keep every hedge, add no facts, do not touch code.

## Install

```bash
npx skills add prithivrajmu/asd-ste100
```

Or clone it into your skills folder:

```bash
git clone https://github.com/prithivrajmu/asd-ste100 ~/.claude/skills/asd-ste100
```

## Use

```
Explain this function in STE.
Rewrite this PR description, 80% ASD-STE100.
Explain how the cache works, strict STE.
Rewrite this error message in STE and show the changes.
```

## What it does not do

- It does not include the ASD-STE100 dictionary. ASD does not permit redistribution. You can request the standard free of charge from [asd-ste100.org](https://www.asd-ste100.org/).
- It does not certify STE compliance. For real aerospace documentation, use the standard and a certified checker.
- It is not for creative or marketing text.

## Credits

- Andrej Karpathy, for the "80% ASD-STE100" tip.
- [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill), which this skill started from. The "keep the hedge" and "add no facts" guard rails come from it.

## License

MIT. See [LICENSE](LICENSE).
