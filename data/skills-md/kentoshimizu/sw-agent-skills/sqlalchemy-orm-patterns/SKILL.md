---
name: sqlalchemy-orm-patterns
description: "SQLAlchemy ORM workflow for model mapping, session/transaction boundaries, and query loading strategy. Use when SQLAlchemy ORM behavior must be implemented or revised with explicit persistence decisions; do not use for repository-wide architecture governance or release policy decisions."
---

# Sqlalchemy Orm Patterns

## Overview
Use this skill to design SQLAlchemy usage that remains correct, efficient, and maintainable under production load.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- ORM loading and session rules:
  - `references/orm-loading-and-session-rules.md`

## Templates And Assets
- ORM modeling template:
  - `assets/sqlalchemy-modeling-template.py`
- Session/transaction checklist:
  - `assets/sqlalchemy-session-transaction-checklist.md`

## Inputs To Gather
- Domain model and relationship constraints.
- Transaction consistency requirements.
- Query access patterns and performance constraints.
- Session lifecycle boundaries.

## Deliverables
- ORM model and relationship design.
- Session and transaction boundary policy.
- Query loading strategy with hotspot validation.

## Workflow
1. Draft model structure using `assets/sqlalchemy-modeling-template.py`.
2. Define session/transaction boundaries.
3. Apply loading strategy rules from `references/orm-loading-and-session-rules.md`.
4. Validate SQL behavior for hot queries.
5. Finalize with `assets/sqlalchemy-session-transaction-checklist.md`.

## Quality Standard
- Session ownership is explicit and leak-free.
- Transaction boundaries preserve business atomicity.
- Query strategy avoids N+1/overfetch patterns.
- ORM abstractions remain transparent for critical SQL paths.

## Failure Conditions
- Stop when session ownership is ambiguous across layers.
- Stop when ORM hides critical SQL behavior on hot paths.
- Escalate when transaction guarantees cannot be met safely.
