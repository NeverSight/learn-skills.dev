---
name: codebase-investigation
description: "Use when explaining how a codebase works or investigating why a design was chosen. Excludes direct symbol lookups, defect diagnosis, implementation requests, and architecture audits."
---

# Codebase investigation

Answer a concrete question about current behavior or recorded design rationale. Investigation is read-only unless the user separately authorizes changes. Keep implementation with engineering, unknown failures with debugging, and architecture audits with their review owner.

## Trace the question

Start at the relevant entrypoint or named behavior. Follow the actual calls, data, state ownership, and external boundaries needed to answer it. Check callers and consumers when they change the meaning. Use focused searches and nearby tests; expand only where an unresolved claim depends on more evidence.

A direct location or symbol question usually needs only a local lookup. Substantial independent angles may justify an explorer; external documentation or historical records may justify a librarian. Give each a bounded question and required evidence. Keep synthesis with the main agent. Avoid automatic repository sweeps, fixed panels, and delegation that adds no independent evidence.

Distinguish:

- Current behavior supported by code or a relevant executed observation.
- Recorded intent supported by contemporaneous documents or discussion.
- Inferences, with their supporting facts and remaining alternatives.
- Unknowns or contradictions that the available sources cannot resolve.

Cite concrete paths and symbols for code claims, and permalinks or identifiers for external records. Include the relevant revision or date when a source may describe a different state. Reading a test establishes its expectations; claim it passes only with applicable execution evidence.

## Conditional depth

- For historical rationale, disputed intent, or previous failed approaches, read [historical-evidence.md](references/historical-evidence.md).
- For a requested walkthrough or teaching explanation, read [teaching.md](references/teaching.md).

## Completion

Answer the question first, then give the shortest trace that supports it and any material caveat. Stop when the requested claims are supported or the missing evidence is identified. For a broad question, state the examined scope so the answer does not imply exhaustive coverage.

Preserve unresolved contradictions. Do not turn a plausible explanation into recorded intent or a repair recommendation into an authorized edit. Name the next source or observation only when it could materially resolve the remaining uncertainty.

## Provenance

Inspired by pstack's [how](https://github.com/cursor/plugins/blob/6ed0f7a9504f577d7529064103cecce9be7dfc5e/pstack/skills/how/SKILL.md), [why](https://github.com/cursor/plugins/blob/6ed0f7a9504f577d7529064103cecce9be7dfc5e/pstack/skills/why/SKILL.md), and [teach](https://github.com/cursor/plugins/blob/6ed0f7a9504f577d7529064103cecce9be7dfc5e/pstack/skills/teach/SKILL.md), v0.15.2. Adapted as one Codex investigation owner.
