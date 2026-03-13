---
name: adr-keeper
description: >
  Create and maintain Architectural Decision Records (ADRs) with date-named
  files sorted like migrations. Use when making structural decisions (new deps,
  pattern changes, tech choices), when asked to "record a decision",
  "create an ADR", "log an architecture choice", or "why did we do it this way".
---

# ADR Keeper

Architectural Decision Records capture the **WHY** behind structural choices.
They are append-only (never edit old decisions — supersede with new ones)
and sorted chronologically like database migrations.

## When to Create an ADR

- Choosing or changing a dependency
- Establishing or changing an architectural pattern
- Making a trade-off that future developers (or agents) need to understand
- Any decision where "why did we do it this way?" would be asked later

## File Location & Naming

ADRs live in `docs/adrs/` (created by `create-agents-md`, or create manually).

**Naming:** `YYYY-MM-DD-short-kebab-description.md`

Examples:
- `2026-03-01-use-vitest-over-jest.md`
- `2026-03-05-separate-ui-from-business-logic.md`
- `2026-03-07-adopt-gherkin-acceptance-tests.md`
- `2026-03-07-cloudflare-worker-as-api-proxy.md`

The date prefix ensures ADRs sort chronologically, like migrations.

## Creating an ADR

1. Create the file using the template below (see [references/adr-template.md](references/adr-template.md))
2. Fill all sections — Context is the most important (it captures the forces)
3. Add the entry to `docs/adrs/index.md`

## Template

```markdown
# ADR: [Short Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Superseded by [link]

## Context

[What forces led to this decision? What problem were we solving?
What constraints did we face? Be specific — this is the most valuable
section because it captures WHY.]

## Decision

[What did we decide? State it clearly and concisely.]

## Consequences

### Positive
- [What we gain]

### Negative
- [What we trade away]

### Neutral
- [Side effects that are neither clearly good nor bad]
```

## Managing ADRs

### Superseding a Decision

Never edit an old ADR. Instead:

1. Create a new ADR explaining the new decision
2. Update the old ADR's status: `**Status:** Superseded by [2026-04-15-new-decision.md](2026-04-15-new-decision.md)`
3. Update `docs/adrs/index.md` for both entries

### Maintaining the Index

After every ADR change, update `docs/adrs/index.md`:

```markdown
# Architectural Decision Records

| Date       | Decision                              | Status                   |
|------------|---------------------------------------|--------------------------|
| 2026-03-07 | Adopt Gherkin acceptance tests        | Accepted                 |
| 2026-03-05 | Separate UI from business logic       | Accepted                 |
| 2026-03-01 | Use Vitest over Jest                  | Superseded by 2026-04-01 |
```

### For Agents

- **Before making structural decisions**: Check `docs/adrs/` for existing
  decisions that may justify or contradict the approach
- **After making structural decisions**: Create an ADR so the next agent
  (or human) understands why
- ADRs referenced from AGENTS.md Knowledge Base table (set up by `create-agents-md`)

## Seeding ADRs from Existing Projects

When bootstrapping ADRs for a project that already has undocumented decisions
(common when running `create-agents-md` for the first time):

1. Look for "Key Decisions" sections in existing AGENTS.md or CLAUDE.md
2. Look for inline comments explaining WHY something was done
3. Look for TODO/HACK/FIXME comments that hint at trade-offs
4. Create one ADR per decision, all dated today
5. Update `docs/adrs/index.md` with all entries
