---
name: architecture-clean-architecture
description: "Clean Architecture workflow for enforcing dependency direction, stable domain boundaries, and use-case-centered application design. Use when teams must separate business rules from frameworks and delivery mechanisms; do not use for isolated module cleanup without boundary implications."
---

# Architecture Clean Architecture

## Overview
Use this skill to structure systems so business rules remain stable while infrastructure and frameworks evolve.

## Scope Boundaries
- Framework and infrastructure details are leaking into domain logic.
- Dependency direction is inconsistent and change cost is rising.
- Teams need explicit boundaries between use cases, adapters, and delivery layers.

## Core Judgments
- Domain boundary: what business rules must stay framework-independent.
- Use-case orchestration: what belongs in application services versus domain entities.
- Dependency inversion points: where interfaces must isolate infra concerns.
- Transaction and consistency scope: where atomicity belongs in the stack.

## Practitioner Heuristics
- Domain layer should not import transport, ORM, queue, or UI frameworks.
- Application layer coordinates workflows; domain layer owns business invariants.
- For dynamic languages, define explicit data contracts (schema/types) at boundaries instead of passing untyped `any`/`object` payloads that force downstream casts.
- Prefer narrow ports with stable semantics over generic "utility" interfaces.

## Workflow
1. Map current modules to domain, application, interface-adapter, and infrastructure responsibilities.
2. Identify dependency violations and hidden framework coupling in business rules.
3. Define or refine ports where infrastructure currently bleeds into domain logic.
4. Move orchestration responsibilities to application use cases and invariants to domain objects.
5. Align transaction boundaries with use-case semantics, not repository convenience.
6. Record remaining boundary debt and migration sequence.

## Common Failure Modes
- "Clean" layers exist physically but still share mutable models across boundaries.
- Domain services become anemic wrappers while business logic moves to adapters.
- Generic DTOs and untyped maps cross layers, increasing casts and null checks.

## Failure Conditions
- Stop when dependency direction cannot be explained by domain intent.
- Stop when boundary contracts remain implicit or loosely typed.
- Escalate when required boundary changes are blocked by organizational ownership constraints.
