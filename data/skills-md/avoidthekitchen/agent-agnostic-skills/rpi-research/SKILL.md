---
name: rpi-research
description: Run deep, evidence-backed codebase research with parallel sub-investigations and produce a structured memo with file/line citations. Use this whenever the user asks to research, analyze, trace, debug, audit, or understand how code connects, including requests like "analyze this repo," "trace this flow," "where is this handled," root-cause investigations, architecture deep-dives, behavior comparisons, and implementation mapping, even if the user never says "research."
---

# RPI Research

Use this skill to answer complex codebase questions by combining targeted file reading, parallel investigation, and synthesis into a saved research note.

## Initial Response

When the skill is invoked, respond with:

```text
I'm ready to research the codebase. Please provide your research question or area of interest, and I'll analyze it thoroughly by exploring relevant components and connections.
```

Then wait for the user's research query.

## Workflow After Receiving the Query

1. Read directly referenced files first.
- If the user names specific files, read those files fully before delegating work.
- Read in the main context first so sub-investigations start from accurate context.

2. Decompose the question into research tracks.
- Break the request into clear research areas (components, flows, patterns, ownership boundaries).
- Track subtasks in a task list so coverage is visible and no branch is dropped.
- Map likely directories/files before parallel execution.

3. Run parallel sub-investigations.
- Spawn multiple focused sub-agents/tasks to research different tracks concurrently.
- Keep each sub-task narrow and concrete (for example: API entrypoints, data model usage, or error handling path).
- If sub-agents are unavailable, execute the same tracks sequentially and keep notes separated by track.

4. Synthesize findings after all tracks finish.
- Wait for all active tracks to complete before writing conclusions.
- Reconcile overlaps and conflicts across tracks.
- Capture concrete file references with 1-based line numbers.
- Highlight cross-component relationships and architectural decisions.

5. Produce the research memo in this structure.

```markdown
---
date: [Current date and time in ISO format]
researcher: [User's Name] / [AI Agent Name]
topic: "[User's Question/Topic]"
tags: [research, codebase, relevant-component-names]
status: complete
---

# Research: [User's Question/Topic]

## Research Question
[Original user query]

## Summary
[Direct answer with high-signal findings]

## Detailed Findings

### [Component/Area 1]
- Finding with citation (`path/to/file.ext:line`)
- Why it matters to the question
- Connection to other areas

### [Component/Area 2]
- Finding with citation (`path/to/file.ext:line`)
- Why it matters to the question
- Connection to other areas

## Code References
- `path/to/file.ext:line` - What is relevant there
- `path/to/other.ext:line` - Why it supports the conclusion

## Architecture Insights
[Design patterns, conventions, and notable tradeoffs]

## Open Questions
[Remaining unknowns and how to resolve them]
```

6. Save and present the result.
- Save research notes to `rpi/research/TIMESTAMP_research_topic.md`.
  - For `TIMESTAMP`, Use a Windows-safe timestamp for `TIMESTAMP`: `YYYY-MM-DD-HH-MM` (e.g., `2026-03-05-22-10`).
- Use a short snake_case topic slug for the filename suffix `topic`.
- Reply to the user with a concise summary plus key file references.

## Quality Bar

- Prefer evidence over speculation; when inferring, label it clearly.
- Cite enough references that another engineer can quickly verify conclusions.
- Keep the memo self-contained so it is useful without reading raw task logs.
- Prioritize high-signal findings over exhaustive but low-value dumps.
