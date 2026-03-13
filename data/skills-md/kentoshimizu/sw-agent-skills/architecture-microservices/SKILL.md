---
name: architecture-microservices
description: "Microservices architecture workflow for service boundary design, independent deployability, and distributed operational safety. Use when domain and team structure justify independent service evolution; do not use as a default scaling strategy for all systems."
---

# Architecture Microservices

## Overview
Use this skill to design microservice architectures that trade monolithic simplicity for bounded autonomy intentionally.

## Scope Boundaries
- Different domain areas change at different speeds and require independent release cadence.
- Team autonomy and ownership boundaries are blocked by shared code/runtime coupling.
- Operational platform maturity exists to absorb distributed-system overhead.

## Core Judgments
- Service boundary: domain capability, data ownership, and team ownership alignment.
- Integration model: synchronous calls, events, or hybrid by invariant type.
- Consistency strategy: local transactions plus saga/compensation where needed.
- Operational budget: observability, incident response, platform engineering capacity.

## Practitioner Heuristics
- Split services by business capability and change cadence, not by technical layer.
- One service owns its data model; cross-service joins in request path are a smell.
- Start with fewer coarse services, then split where pain is observed.
- Define service contracts with explicit schema types; avoid generic untyped payloads that drive cast-heavy consumers.

## Workflow
1. Identify candidate service boundaries from domain and ownership signals.
2. Evaluate coupling and consistency needs across candidate boundaries.
3. Choose integration patterns per interaction type.
4. Define contract and data ownership rules, including versioning strategy.
5. Estimate operational overhead and staffing implications.
6. Document migration path from current architecture.

## Common Failure Modes
- Premature decomposition creates chatty synchronous dependencies.
- Shared utility libraries become hidden coupling channel.
- Service count grows faster than team ownership maturity.

## Failure Conditions
- Stop when service boundaries cannot be mapped to stable ownership.
- Stop when end-to-end reliability depends on fragile RPC chains.
- Escalate when platform and operations readiness is insufficient for distributed complexity.
