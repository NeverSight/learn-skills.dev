---
name: db-conceptual-modeling
description: "Conceptual data modeling workflow for domain entities, relationships, and lifecycle boundaries. Use when teams must align on domain meaning before logical/physical schema decisions; do not use for index-only or migration-only tasks."
---

# DB Conceptual Modeling

## Overview
Use this skill to model domain meaning first, so later schema decisions reflect business semantics rather than accidental implementation details.

## Scope Boundaries
- Teams disagree on entity meaning or relationship semantics.
- A new domain area is being introduced.
- Existing schema complexity suggests conceptual drift.

## Core Judgments
- Entity versus value concept boundaries.
- Cardinality and ownership semantics of relationships.
- Lifecycle states and temporal meaning.
- Bounded-context boundaries and shared concepts.

## Practitioner Heuristics
- Model business invariants explicitly before table design.
- Use language from domain experts, not only engineering jargon.
- Treat temporal facts (history, validity windows) as first-class concepts.
- Avoid polymorphic catch-all concepts that hide domain distinctions.

## Workflow
1. Identify core concepts, actors, and business events.
2. Define entity relationships with ownership and lifecycle semantics.
3. Capture key invariants and conflict rules.
4. Resolve term collisions across bounded contexts.
5. Document conceptual assumptions that drive downstream logical design.

## Common Failure Modes
- Conceptual model mirrors current tables instead of domain reality.
- Relationship ownership is left implicit, causing write conflicts later.
- State transitions are not modeled, forcing ad hoc status flags.

## Failure Conditions
- Stop when core terms remain ambiguous across stakeholders.
- Stop when invariants cannot be expressed at conceptual level.
- Escalate when bounded context boundaries are politically unresolved.
