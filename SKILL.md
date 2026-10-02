---
name: asd-ste100
description: "Explain or rewrite text in ASD-STE100 Simplified Technical English so a human can read it fast. Default is Karpathy's '80% of the way to ASD-STE100'. Also makes the stronger explainer formats Karpathy recommends: a diagram, an interactive HTML page, or a 3b1b-style explainer video. Use when the user asks for STE, ASD-STE100, Simplified Technical English, '80% STE', 'Karpathy-style', a plain explanation of code, a system, a diff, or any LLM output, or asks to explain something as a diagram, an HTML page, or an explainer video. Not for creative or marketing copy."
---

# ASD-STE100 for readable LLM output

> "Ask your LLM to explain something in ASD-STE100, it's a controlled language specification originally developed for aerospace maintenance documentation. LLMs well-versed in this language and it comes with heavy constraints on clean writing style that I often find a lot more readable. Sometimes I've tried to soften it a bit e.g. ask for '80% of the way to ASD-STE100' because the spec is quite stringent."
> — Andrej Karpathy, 2 Oct 2026

The reader is a person who must understand what you produced. Your job is to make that reading fast. You already know ASD-STE100 (Issue 9). Use what you know. This file only sets the level and the guard rails.

## Pick the level

| Level | When | What changes |
|---|---|---|
| **80%** (default) | Explanations, summaries, code walk-throughs, reviews, status reports | Keep the sentence rules. Relax the vocabulary. |
| **100%** | The user says "strict", "100%", "full STE", or the text is a procedure or safety text | Apply the full standard. |

Do not announce the level unless the user asks.

## 80% rules

1. One idea in each sentence.
2. Aim for 20 words or fewer. Never go above 25.
3. Use the active voice. Say who does the action.
4. Use simple tenses: present, past, future with "will".
5. Use the verb, not a noun made from it: "check the log", not "perform a check of the log".
6. Use one word for one thing. Do not change to a synonym in the middle of a text.
7. Use plain words: "use", "start", "stop", "before", "because", "to". Do not use "utilize", "commence", "prior to", "in order to".
8. Do not use phrasal verbs when a single verb exists: "start", not "spin up". "Find", not "figure out".
9. Do not use semicolons. Write two sentences.
10. Put a maximum of 3 nouns in a row.
11. Use a numbered list for steps. Use a list or a table for 3 or more items.
12. Write a maximum of 6 sentences in a paragraph. Put the most important point first.

You can keep: technical terms (API, cache, container), code names, contractions, "e.g.", and a present perfect tense when it says something the simple past cannot ("the job has finished", so the output is ready now).

## 100% additions

Apply the full ASD-STE100 standard as you know it. Specially:

- Procedures: 20 words maximum, imperative, one instruction in each step.
- Descriptions: 25 words maximum.
- No "-ing" forms, except in technical nouns.
- No contractions. No Latin abbreviations.
- Do not omit articles or "that".
- Use approved dictionary words with their approved meaning. Use other words only as technical nouns or technical verbs.
- Safety text starts with WARNING (injury, or for software: data loss, security risk, outage) or CAUTION (damage), then the command, then the risk.

## Guard rails

These rules are stronger than the STE rules.

- **Keep every fact.** Do not remove a number, a condition, an exception, or a scope limit to make a sentence shorter. Write a longer sentence or two sentences.
- **Keep the confidence of the source.** "May have failed" stays "may have failed". Do not change a possibility into a fact.
- **Add no facts.** Do not add a cause, a frequency, or a mechanism that the source does not state.
- **Keep code unchanged.** Do not rewrite code blocks, identifiers, commands, or quoted error text.
- **Write in the user's language.** For a different language, apply the same principles: short sentences, one idea, active voice, literal words.
- **Stop when it is clear.** The goal is clarity, not the shortest text.

## Output

Give the explanation or the rewritten text only. Do not add a preamble, a list of the rules you applied, or a summary of the changes.

If the user asks "show the changes" or "which rules", give a table:

| Rule | Before | After |
|---|---|---|
| Active voice | "The file is deleted by the job." | "The job deletes the file." |

## Examples

**Before:** "In order to utilize the cache, it is necessary that the client be authenticated prior to the commencement of any requests; otherwise the requests will be rejected."
**After (80%):** "Log in before you use the cache. The server rejects requests from a client that is not logged in."

**Before:** "An error may have occurred due to a possible mismatch in the data format, which could be caused by an outdated client."
**After (80%):** "The request may have failed. A possible cause is a data format that does not match. An old client version can cause this."

**Before:** "Spin up the container, and once it's healthy, kick off the migration."
**After (100%):**
1. Start the container.
2. Make sure that the container is healthy.
3. Start the migration.

## Better than text: diagram, HTML page, video

Karpathy puts these formats in order. Each one is better than the one before it, but it also costs more to make:

1. **STE text** (the rules above)
2. **Diagram.** "These can be a lot easier to process, parse, and understand."
3. **HTML page.** "Ask for output 'in HTML' to get a beautiful, interactive webpage."
4. **Explainer video.** "The output format I am most bullish on." For example: "Create a 3b1b style video explainer on X."

### Which format to use

- If the user names a format, use that format.
- If the user does not name a format, write STE text. If the subject has 3 or more parts that interact, or has a sequence or a change of state, add a diagram.
- Do not make an HTML page or a video unless the user asks for one. You can offer one in a single line at the end of your answer.

Write all text in these formats in STE: labels, captions, page text, and narration. The guard rails above apply to all formats.

### Diagram

- Use Mermaid, because GitHub, many editors, and many chat tools show it. Use SVG if the subject needs a free layout, for example a geometry or a memory layout.
- Show one idea in each diagram. If a diagram has more than about 12 boxes, divide it into 2 diagrams.
- Use the same name for a thing in the diagram and in the text.
- Use short labels: 1 to 4 words. Put a verb on each arrow ("sends", "reads", "retries").
- Put one sentence below the diagram that tells the reader where to start.

### HTML page

- Make one file that contains all of the HTML, CSS, and JavaScript. Load libraries from a CDN only if necessary.
- Make the reader do something, not only read: step through a process, move a slider, toggle between 2 states, or see the result of an input.
- Start with the main idea at the top. Put details below it.
- The page must work on a phone screen, and in light mode and dark mode.
- Do not use real data, keys, or personal information unless the user gives them for this purpose.

### Explainer video

Make a 3Blue1Brown-style video with [Manim](https://www.manim.community/) (the Python animation library that 3Blue1Brown uses):

1. Write a script. Divide it into scenes. For each scene, write the narration in STE and describe the animation.
2. Write the Manim code. Make one class for each scene. Keep each scene short: about 10 to 40 seconds.
3. Make the narration audio:
   - If the user gives an ElevenLabs API key (or a key for a different text-to-speech service), use it. Read the key from an environment variable. Do not write the key into a file.
   - If the user does not give a key, use a free text-to-speech tool that runs on the local computer, and tell the user which tool you chose.
4. Put each audio clip with its scene. Make the animation of each scene as long as its audio.
5. Render the scenes and join them into one video file, for example with `ffmpeg`.
6. Tell the user the path of the video file and the command that renders it again.

Render at low quality first (`manim -ql`) to find errors fast. Render at high quality only at the end.

## Why

As LLMs do more of the work, more of your work becomes oversight and understanding. You can now ask for large, custom software artifacts that you use once and then discard. A web page or a video that explains one topic to one person did not make sense to create before. Now it does.
