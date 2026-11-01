---
name: dependency-governance
description: use when a completed change introduces new third-party packages, new internal shared modules, wrappers around existing libraries, or convenience helpers that broaden coupling. trigger after implementation when any import graph edge is new, when a "shared" or "common" layer has grown, or when one feature now depends on abstractions owned by another.
---

# Dependency Governance

Announce at the start: "I'm using dependency-governance to check whether the new dependencies are deliberate or reflexive."

## Core idea

The goal is not zero dependencies. The goal is deliberate dependencies. Every new third-party package, shared module, or wrapper is a long-term liability with a short-term benefit — the review confirms the benefit is real and the liability is accepted.

## Workflow

1. List every new edge the change introduced: third-party packages, new internal packages, new imports across module boundaries, new wrappers, new helper layers.
2. For each edge, run [`checklist.md`](./checklist.md) to decide whether it is justified, risky-but-acceptable, or should be removed or deferred.
3. Check findings against [`anti-patterns.md`](./anti-patterns.md) to catch the common reflexive-abstraction patterns.
4. Classify severity using [`../../references/severity-model.md`](../../references/severity-model.md). Most dependency findings are Medium; a dependency backflow or single-consumer "generic" abstraction is usually High.

## Heuristics

Prefer:

- a small vendored helper over a new dependency used in one place
- a function over a class, a class over a framework, a framework over a platform
- dependencies with clear owners and clear removal paths

## Do not

- flag every new library; flag libraries that buy little and cost a lot
- demand the team remove a dependency that already paid for itself
- treat an internal shared module as automatically good because it is internal

## Supporting files

- [`checklist.md`](./checklist.md) — inspection steps for new libraries, shared modules, wrappers, and cross-feature coupling.
- [`anti-patterns.md`](./anti-patterns.md) — dependency-specific anti-patterns extending [`../../references/anti-patterns.md`](../../references/anti-patterns.md).

## Output

Use the review report format in [`../../references/report-templates.md`](../../references/report-templates.md). For each dependency finding, state: (a) the edge, (b) the justification offered by the implementation, (c) your verdict, (d) the smallest corrective action if any.
