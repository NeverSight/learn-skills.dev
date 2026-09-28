---
name: shape
description: >-
  Shape software work into clear product behavior and decisions. Use when a feature/request is
  ambiguous, has unresolved human decisions, needs a behavioral specification, or is too uncertain
  for implementation planning. Supports normal shaping, spec mode, and wayfinding for large fog-
  of-war work. Inspect the project for facts instead of asking the user to relay them.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.2"
---


# Shape

Convert ambiguous intent into behavior and decisions clear enough for planning.

## Modes

- **shape** — normal product/behavior clarification.
- **spec** — user already knows the desired behavior; produce or update the behavioral contract directly.
- **wayfind** — large uncertain work where bounded research/prototypes are needed before a stable plan exists.

## Workflow

1. Run a focused reality check and read relevant durable product/architecture decisions from the current project workspace first. Treat harness/global/personal memory as non-authoritative project context unless the user explicitly asks to reuse prior context or the workspace itself points to it; verify any reused memory against current workspace truth before making durable changes.
2. Separate project facts from human decisions. Discover facts yourself when tools/environment expose them.
3. Identify the current decision frontier: questions whose answers actually change behavior, scope, compatibility, or architecture.
4. Do not silently promote an ambiguous phrase into a durable product requirement when multiple interpretations would materially change persistence, offline behavior, synchronization, security/privacy, compatibility, or platform scope. Ask one focused human decision when needed, or leave the point explicitly open if it does not block the current shaping outcome.
5. Resolve only the behavior that is actually decided. When a human answers one decision, close only the decision(s) logically entailed by that answer. Preserve adjacent unresolved decisions explicitly rather than collapsing, deleting, or inferring them because they are related. For example, deciding that add/edit/remove participate in sync does not by itself decide which fields sync, how edit conflicts resolve, how deletion propagates, whether restore exists, how local data links to an account, or what sign-out does.
6. Do not interrogate the user about naming/file-placement decisions the project can decide locally.
7. Detect material domain/architecture concerns and surface them without selecting implementation technology or providers. For example, phone-first plus offline behavior may surface mobile/local-first concerns without deciding framework, storage, or sync design.
8. Produce/update a specification or durable product artifact when the work is substantial enough to benefit from one. When updating an artifact after a decision, re-read the neighboring open-decision section and verify that only answered questions were removed or narrowed.

## Specification boundary

The spec states WHAT must be true: behavior, invariants, lifecycle/failure semantics, compatibility expectations, acceptance criteria, and explicit non-goals. Implementation details belong in the plan.

## Stop

Stop when the work is clear enough to plan. If a genuine human decision remains and guessing would create meaningful product/architecture risk, ask it or record it explicitly as open rather than silently resolving it.
## Reference Guide

Load only the references needed for the current task:

- [spec mode](references/spec-mode.md)
- [wayfinding](references/wayfinding.md)
- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [reality check](references/_shared/orchestration/reality-check.md)
- [depth](references/_shared/orchestration/depth.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [artifact model](references/_shared/artifacts/artifact-model.md)
- [spec](references/_shared/artifacts/spec.md)
- [provider neutrality](references/_shared/engineering/provider-neutrality.md)
