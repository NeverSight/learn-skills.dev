---
name: distributed-monolith-detection-and-remediation
description: Detect distributed monolith anti-patterns and remediate with decoupling, contract stabilization, and ownership realignment. Use when microservices are tightly coupled and hard to change.
disable-model-invocation: true
---

# Distributed Monolith Detection And Remediation

## Use When

- Multiple services require lockstep releases
- Synchronous call chains frequently fail under load

## Workflow

1. Audit coupling hotspots: synchronous depth, shared schemas, release dependencies.
2. Identify anti-patterns (shared DB, chatty RPC, implicit contracts).
3. Define target decoupling strategy by dependency class.
4. Introduce contract versioning and async boundaries where needed.
5. Track dependency reduction and release independence metrics.

## Required Checks

- Lockstep deployment paths are identified and prioritized
- Shared database write paths have migration plan
- New boundaries reduce runtime blast radius

## Decision Framework

- Measure coupling by release independence, synchronous call depth, and shared mutable state—not folder layout.
- Prioritize breaking synchronous chains before splitting services; async boundaries reduce lockstep deploy pressure.
- Extract along bounded contexts with anti-corruption layers; avoid shared-database writes across services.
- Track decoupling metrics release-over-release (deploy coupling index, blast-radius score).

## Common Rationalizations And Rebuttals

- "We already have microservices." -> Shared DBs and chatty sync RPC still form a distributed monolith.
- "Big-bang decomposition is faster." -> Big-bang cutovers fail on hidden dependencies; extract incrementally with strangler patterns.
- "Team structure can follow later." -> Conway's law will re-couple services; align ownership with extraction slices.

## Evidence Pack

- Coupling heatmap: sync call graph depth, shared schema writes, co-deploy frequency
- Target boundary map with anti-corruption layer design per extraction slice
- Contract stabilization plan with versioning policy for extracted services
- Before/after deploy independence metrics with baseline and target

## Exit Criteria

- Architectural coupling trends downward release-over-release
- Teams can ship high-priority services independently
