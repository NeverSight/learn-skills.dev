---
name: intake
description: Normalize an External Project Brief into accepted scope, sources, constraints, assumptions, and open questions.
disable-model-invocation: true
---

# Intake

Run intake before grilling or Agent OS initialization when project context comes from outside the coding agent.

## Inputs

Accept any source the user provides:

- Pasted notes.
- Notion or document exports.
- Markdown files.
- Links or references.
- User flows, screen sketches, feature ideas, or research notes.

Do not make the workflow source-specific. If another tool or skill can fetch context, use it; otherwise ask the user for the missing material.

## Normalize the brief

Extract and organize:

- Product vision and desired outcomes.
- Target users, personas, or jobs-to-be-done.
- Initial feature candidates.
- Conceptual user flows or screens.
- Constraints such as timeline, budget, hosting, stack preferences, compliance, and team size.
- Explicit decisions and non-goals.
- Open questions.
- Risky assumptions.
- Vocabulary candidates for `LANGUAGE.md`.

## Source authority

Treat an External Project Brief as upstream context, not accepted project truth. Keep source claims separate from decisions already accepted in the repo.

When possible, capture source provenance without copying full upstream content:

- Source name or type.
- Stable URL, ID, or file path.
- Child pages, sections, or references used.
- Fetch or access date when known.
- Any stated relationship to repo docs or issue trackers.

Flag contradictions between external context and existing repo docs instead of silently resolving them.

## Sort the scope

Separate active work from future possibility.

- Current implementation contract: what appears accepted for the current iteration.
- Backlog: likely future work, not part of the current contract.
- Someday or speculative ideas: weak commitments that should not shape the initial Agent Operating System.
- Non-goals: explicit exclusions.

Do not promote backlog or speculative ideas into current scope just because they appear in the external brief.

## Output

Return a concise intake summary:

```md
## Project intake

### Sources

### Goal

### Users

### Current scope

### Constraints

### Backlog and later

### Existing decisions

### Non-goals

### Source conflicts

### Assumptions to grill

### Vocabulary candidates

### Recommended next step
```

Omit empty sections. Recommend the next workflow based on what remains:

1. `init-agent-os` if the repo is greenfield or lacks an Agent Operating System.
2. `map-decisions` when the proposed work contains dependent decisions or unclear Milestone boundaries.
3. `grill` when a concrete plan has unresolved assumptions, vocabulary, scope boundaries, or authority questions.
4. `write-spec` when accepted scope needs product review or cross-session continuity.
5. `write-issues` when accepted scope would benefit from tracking separate outcomes.
6. `implement` when the scope is already accepted and no planning artifact would help.
7. A docs update when the intake finds accepted durable knowledge missing from repo docs.

Finish when every material source claim appears in the summary or is deliberately excluded, source conflicts remain visible, and current scope is distinct from backlog and speculation.
