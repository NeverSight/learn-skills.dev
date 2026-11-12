---
name: spec
description: Interview the user to produce a feature spec (PRD), grounded in the project's domain model, context map, and ubiquitous language. Outputs a structured spec document. Use when starting a new feature, enhancement, or significant change.
user-invocable: true
argument-hint: "[feature or problem to specify]"
---

# Feature Spec

Produce a structured spec for a feature or change through a focused interview, grounded in the project's domain model.

## Process

### 1. Discover project context

Read existing domain documentation:

1. `docs/CONTEXT_MAP.md` — which contexts exist and how they relate
2. `docs/UBIQUITOUS_LANGUAGE.md` — canonical terminology
3. `docs/contexts/*/CONTEXT.md` — ownership, invariants, contracts for relevant contexts
4. `CLAUDE.md` — project-level context

### 2. Understand the request

If the user hasn't provided enough context, interview briefly (3-5 questions max):

- What problem does this solve? For whom?
- What does success look like?
- What's explicitly out of scope?
- Are there constraints (timeline, tech, compatibility)?

Don't over-interview. If the intent is clear from conversation context, skip to the next step.

### 3. Explore the codebase

Explore the relevant areas to understand:

- Current state of related features
- Existing patterns and conventions
- Which bounded contexts this feature touches
- What interfaces already exist that this feature should use or extend

### 4. Identify modules and test boundaries

Sketch the major modules to build or modify. For each:

- What bounded context does it belong to?
- Is it a new concept or an extension of an existing one?
- Does it cross context boundaries? (If so, what contracts are needed?)
- Is there an opportunity for a deep module (small interface, significant implementation)?
- Should it have tests? (Use pragmatic TDD: test core logic and boundaries, skip glue/UI)

**Check with the user** that these modules match their expectations and which should have tests.

### 5. Write the spec

Write the spec using the template below. Use domain language from `UBIQUITOUS_LANGUAGE.md` throughout. Save to `docs/contexts/<primary-context>/specs/<slug>.md`.

If the feature spans multiple contexts, save to the primary context and note the cross-context impact.

<spec-template>

# [Feature Name]

**Status:** Draft
**Context(s):** [Which bounded context(s) this touches]
**Date:** [YYYY-MM-DD]

## Problem

The problem from the user's perspective. What's broken, missing, or suboptimal?

## Solution

The solution from the user's perspective. What will they be able to do after this ships?

## User Stories

1. As a [actor], I want [capability], so that [benefit]
2. ...

Cover the full scope. Include edge cases and error scenarios.

## Implementation Decisions

Decisions made during the spec process. Include:

- Modules to build or modify (by domain concept, not file path)
- Interface contracts between modules
- Schema changes (Convex tables, ClickHouse tables)
- API contracts (new endpoints, changed responses)
- Cross-context contracts (what this feature needs from or exposes to other contexts)
- Architectural decisions (with brief rationale)

Do NOT include file paths or code snippets — they go stale.

## Testing Strategy

- Which modules will have tests (pragmatic TDD: core logic + boundaries)
- What makes a good test for this feature (behavioral, through public interfaces)
- Prior art (similar tests that already exist in the codebase)
- What to mock (only system boundaries: external APIs, databases)

## Out of Scope

What this spec explicitly does NOT cover. Be specific.

## Open Questions

Unresolved decisions that need answers before or during implementation.

</spec-template>

### 6. Domain model updates

If the spec introduced new terms, refined existing ones, or made decisions that affect the domain model:

- Update `docs/UBIQUITOUS_LANGUAGE.md` with new terms
- Update relevant `docs/contexts/<name>/CONTEXT.md` with new invariants or contracts
- Consider whether any decisions warrant an ADR (hard to reverse + surprising + real trade-off)

## Related skills

- `/domain` — stress-test the spec against the domain model before implementation
- `/slice` — break the spec into vertical slices for implementation
- `/tdd` — implement each slice with tracer-bullet TDD
