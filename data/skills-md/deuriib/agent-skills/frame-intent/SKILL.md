---
name: frame-intent
description: Convert CEO/COO strategic direction into a structured Product Brief and OKR set. Use when a new initiative starts, quarterly planning begins, or a strategic pivot is considered. Triggered by "start a new initiative", "define OKRs", or "strategic planning".
---

# Frame-Intent — Strategic Intent to Product Brief

> *"Haces las cosas como para Dios, por eso trabajas con excelencia y dedicación."*

## 1. Purpose

Elicit strategic intent and freeze it into a Product Brief + OKRs before any
domain work starts. No specs, no code, no budgets committed here.

## 2. Chain Contract

- Previous: none (chain entry for this pack)
- Next: translate-to-spec

```text
frame-intent → translate-to-spec → propose-changes → review-* → execute-spec
  → quality-gate → verify-handoff → ship-release
```

## 2b. Role Binding (Org)

- **Bound to:** `montilla` (CEO) — classifies intent and owns the brief.
- C-levels do NOT write briefs; they receive them via reference.

## 3. Process

1. Ask the initiator: What problem? Who is affected? What does success look like?
2. Produce `docs/briefs/BRIEF-<slug>.md` using `references/product-brief.md`.
3. Define 2–4 OKRs using `references/okr-template.md`.
4. Identify required C-levels (vasquez, dauhajre, subero, vera, santana, barrera, montero, espinoza) and flag cross-cutting concerns.
5. Hand off the brief reference to `translate-to-spec`.

## 4. What I won't do

- Write implementation specs (→ `translate-to-spec`).
- Allocate budgets without `dauhajre` (CFO).
- Commit to timelines without `vasquez` (CTO) feasibility input.

## 5. References

- `references/product-brief.md` — Product Brief template.
- `references/okr-template.md` — OKR template.
