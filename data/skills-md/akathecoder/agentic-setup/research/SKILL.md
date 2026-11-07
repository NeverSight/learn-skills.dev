---
name: research
description: Investigate a question against primary sources and write cited findings. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated.
argument-hint: "What question should I research?"
---

# Research

Investigate a question against **primary sources** and capture the findings as a
project artifact. Dispatch the investigation to a background agent when the harness
can; otherwise research in this session.

Resolve every `.agents/projects/` path from the opened workspace root, including
when the active repository is nested inside it. In a single-repository workspace,
that is the repository root. Keep this artifact root fixed when changing directories;
never use nested repositories or global agent-installation directories for artifacts.

## Process

1. Identify the active project and the question. Read its `CONTEXT.md` and `LINKS.md`
   when they exist so the investigation uses confirmed project language.

   Done when the question and the project slug are known.

2. Follow every claim back to the source that owns it: official docs, specs, source
   code, first-party APIs. Prefer those over a secondary write-up.

   Done when every retained finding traces to a primary source.

3. Write `.agents/projects/<project>/research-<slug>.md` using the structure below.
   Cite each claim. Record the path in `LINKS.md`.

   Done when a later session can use the file without this conversation, and the user
   has the path.

## Document

```md
# Research: <question>

## Findings

<Each claim, with the source that owns it.>

## Sources

<Primary sources consulted.>

## Open

<What the sources did not settle.>
```

## Done when

- Every finding cites a primary source.
- `.agents/projects/<project>/research-<slug>.md` holds the investigation.
- Project links point at the file.
