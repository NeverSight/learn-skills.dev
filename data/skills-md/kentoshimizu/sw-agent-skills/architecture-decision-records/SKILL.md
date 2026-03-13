---
name: architecture-decision-records
description: "Architecture Decision Record workflow for capturing technical decisions, alternatives, trade-offs, and revision triggers over time. Use when decisions materially affect system behavior, cost, or team workflow; do not use for trivial implementation choices."
---

# Architecture Decision Records

## Overview
Use this skill to make architecture decisions auditable, reversible when possible, and maintainable as constraints evolve.

## Scope Boundaries
- A technical decision changes long-term system direction.
- Multiple viable options exist and trade-offs must be explicit.
- Teams need a durable rationale for future reviewers.

## Core Judgments
- Decision scope: what is affected and what is intentionally out of scope.
- Option set quality: whether alternatives are truly viable.
- Reversibility: cost and risk if the decision is later changed.
- Expiry/revisit trigger: what future signal should force reevaluation.

## Practitioner Heuristics
- Record decisions at the same abstraction level as the problem; avoid mixing architecture and local code style debates.
- Rejected options are as important as selected ones for future context.
- State assumptions explicitly, especially around traffic, team capacity, and compliance constraints.
- Include consequences for operations and developer workflow, not only runtime behavior.

## Workflow
1. Define decision question and non-negotiable constraints.
2. Enumerate realistic options and decision criteria.
3. Analyze trade-offs including failure modes and operational impact.
4. Select a decision and capture why alternatives were rejected.
5. Define measurable revisit triggers and ownership.
6. Link the record to affected architecture artifacts and implementation work.

## Common Failure Modes
- ADRs describe outcomes after the fact without real alternative analysis.
- Decision records never revisit invalidated assumptions.
- Records duplicate design docs and lose decision focus.

## Failure Conditions
- Stop when constraints are incomplete or contradictory.
- Stop when no meaningful alternatives are considered.
- Escalate when decision ownership and revisit triggers are undefined.
