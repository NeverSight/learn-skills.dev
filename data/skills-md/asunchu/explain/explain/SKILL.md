---
name: explain
description: Write clear technical English for replies, documentation, procedures, and explanations. Use 80% STE by default and strict writing rules for instructions. Choose text, diagrams, interactive HTML, or narrated video when they help. Preserve code, exact quotations, and the user's requested style.
---

# Explain

Make the idea easy to understand. Start with clear words and use a richer format only when it helps.

## Shared contract

Read [CORE.md](CORE.md) before composing the explanation unless its contents are already present in the active instructions.
This is the same contract for every harness and model. Do not infer a different contract from the harness name.
Read [RULES.md](RULES.md) and [WORDS.md](WORDS.md) for detailed writing checks.
Our word guide is not the official ASD-STE100 dictionary; do not claim formal compliance without checking the official sources.

## Choose the evidence

Use the research rules in the shared core. Read [references/research.md](references/research.md) when choosing sources or resolving conflicting evidence.
Context7 and search are optional capabilities, not required dependencies. Use an available equivalent when it supplies suitable evidence.
Do not send private code or sensitive text to a research service without authorization.

## Choose the output

Honor the requested medium. Otherwise use the smallest format that resolves the understanding problem:

| Understanding problem | Output |
| --- | --- |
| Definition or short conceptual question | Concise prose, with a small example |
| Structure, relationships, or a short sequence | Mermaid source rendered locally with Pele, or custom SVG |
| Cause and effect, adjustable parameters, comparing scenarios | Interactive HTML with meaningful controls |
| A process over time or a story best taught through narration | Animated video with narration and captions |

A recommendation or script request does not authorize producing a video.
For ambiguous artifact requests, infer sensible defaults and state them: technically curious adult, English, and local output.
For requested video, start around 60–90 seconds at 1080p/30 fps unless the user provides other constraints.
Ask only when missing facts, audience, format, or budget materially affect the result.

Read [references/diagrams.md](references/diagrams.md) when producing diagrams.
Use its pinned local renderer for standard diagrams. Keep custom React/SVG when illustration or precise motion needs it.

## Build and check

1. Establish what the reader should understand afterward.
2. Gather evidence when the shared research rules require it.
3. Build a sequence from a familiar example through its mechanism to a useful takeaway.
4. Check meaning, evidence, and scope before polishing the words.

For substantial artifacts, draft a compact storyboard with teaching points, visible objects, actions, narration, and sources.
Proceed within existing authorization; add no approval gate unless the user requests one or the action requires it.
For animation, HTML, or video production, read [references/production.md](references/production.md).
For video scripts and export checks, also read [VIDEO.md](VIDEO.md).
A working source project does not prove that the output plays or its controls work.

## Invocation

Ordinary requests can select this skill when the harness makes it available.
Codex supports `$explain`; Claude Code supports `/explain`; OpenCode can use a natural-language request to load Explain.
Global writing defaults and explicit skill loading are separate mechanisms. Neither guarantees a correct answer.
