# Media guide

Read only the section for the requested format.
Apply the core skill's meaning checks to labels, captions, page text, and narration.

## Diagram

- Use Mermaid for relationships and flows. Use SVG when spatial layout matters.
- Show one main idea. Split a diagram with more than about 12 nodes.
- Keep names consistent with the source and the explanation.
- Use short labels. Label arrows when their meaning would otherwise be unclear.
- Distinguish a possible path from a confirmed path. Do not invent links.
- Quote Mermaid labels that contain punctuation or code-like text.
- Give a text equivalent when the diagram carries information that is not in the surrounding text.
- Keep any requested starting point or reading order clear.

## Interactive HTML

- Prefer one self-contained HTML file. Avoid external libraries, fonts, tracking, and network calls by default.
- Add a useful interaction: step through a process, change a value, or compare states.
- Start with the main idea. Put details below it.
- Support narrow screens, light and dark modes, and reduced motion.
- Use semantic HTML, visible focus, labelled controls, keyboard access, and readable contrast.
- Do not communicate a state by color alone. Explain each control's effect in text.
- Put untrusted source text in text nodes, not `innerHTML`. Do not execute embedded source code.
- Use synthetic data unless the user authorizes real data for this artifact.
- Keep the main explanation readable if JavaScript is unavailable.
- If browser tools are available, test keyboard operation, a narrow viewport, and the core interaction.
- State which checks actually ran. Do not claim browser testing from a source-code review alone.

## Explainer video

Use an original mathematical-explainer presentation when the user asks for a 3Blue1Brown-style video.
Do not imply affiliation or copy a creator's voice, branding, or assets.

1. Check which tools are available: Python, Manim Community, `ffmpeg`, and an audio tool if narration is requested.
2. If a dependency is missing, explain the limit. Ask before installation. Offer a storyboard and runnable source instead of claiming a render.
3. Write a scene plan with the main idea, source facts, visual action, and short narration.
4. Write Manim Community code that matches the available version. Do not assume it is interchangeable with 3Blue1Brown's own animation code.
5. Use local speech tools if available and authorized. Use a paid or remote speech service only with permission to send the narration and spend credits.
6. Read credentials from environment variables. Do not request a key in chat or put it in source files, logs, or output artifacts.
7. Match each scene's duration to the actual audio. If no audio tool is available, provide captions or state that the result is silent.
8. Render a low-quality preview first, for example with `manim -ql`. Inspect it before a final render if rendering tools are available.
9. Join the scenes and audio with available tools. Give the output path and the exact command that reproduces the render.
10. Distinguish a storyboard, generated source, a preview, and a completed video. Never claim a render that did not run.

Do not make the animation longer or more complex than the topic needs.
