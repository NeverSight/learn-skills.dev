---
name: db-logical-design
description: "Logical database design workflow for table structure, key strategy, constraints, and relational consistency. Use when durable schema semantics must be defined before physical tuning; do not use for query-only optimization tasks."
---

# DB Logical Design

## Overview
Use this skill to define schema semantics that preserve integrity and support maintainable application behavior.

## Scope Boundaries
- New domain models must be translated into relational schema.
- Existing schema suffers from integrity drift or unclear constraints.
- Teams need consistent key and relationship semantics.

## Core Judgments
- Primary and alternate key strategy.
- Nullability and optionality semantics.
- Referential integrity rules and cascade behavior.
- Audit and lifecycle columns (created/updated/deleted/effective time).

## Practitioner Heuristics
- Model constraints in the database when they are universal invariants.
- Use explicit unique constraints to encode business identity rules.
- Avoid ambiguous nullable fields that represent multiple meanings.
- For dynamic-language apps, define explicit typed schema mappings to avoid broad `object` payloads and repetitive casts at repository boundaries.

## Workflow
1. Map conceptual entities to relational structures.
2. Define keys, uniqueness, and relationship cardinality rules.
3. Specify integrity constraints and lifecycle semantics.
4. Validate design against expected write/read workflows.
5. Identify migration implications and compatibility constraints.
6. Document deferred trade-offs and boundary assumptions.

## Common Failure Modes
- Business identity handled only in application code.
- Soft-delete semantics conflict with uniqueness and reporting.
- Overloaded JSON columns hide core relational structure.

## Failure Conditions
- Stop when key strategy cannot guarantee entity identity.
- Stop when critical invariants rely on informal conventions.
- Escalate when logical model conflicts with required consistency semantics.
