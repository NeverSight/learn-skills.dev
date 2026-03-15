---
name: effect-v4
description: Effect v4 implementation and migration guidance for current Effect APIs. Use when writing or reviewing code that depends on Effect v4, migrating v3-style APIs (Context.Tag, Effect.Service, FiberRef, catchAll/catchSome, fork/forkDaemon), debugging service/layer wiring, or validating compatibility with effect-smol/effect@4.0.0-beta.x.
---

# Effect v4

## Overview

Use this skill to produce Effect code and reviews that match the current v4 APIs in `effect-smol`, not legacy v3 patterns.

Treat migration docs as intent and `packages/effect/src` + tests as ground truth.

## Workflow

1. Classify the task.
- New implementation
- v3-to-v4 migration
- Code review / compatibility audit

2. Load only the needed reference file.
- Migration mapping: `references/migration-map.md`
- Current idioms with evidence: `references/idioms-and-evidence.md`
- Deterministic audit procedure: `references/review-checklist.md`

3. Apply v4-first rules.
- Prefer `ServiceMap.Service` / `ServiceMap.Reference` over `Context.*`, `Effect.Tag`, `Effect.Service`, `FiberRef`.
- Prefer `Effect.catch`, `catchCause`, `catchFilter`, `catchReason`, `catchReasons`.
- Prefer `Effect.forkChild` / `forkDetach` and explicit `Fiber.join` / `Fiber.await`.
- Prefer `Scope.provide` over `Scope.extend`.
- Use `Yieldable` correctly: `yield*` is fine; non-`Effect` combinator inputs need `.asEffect()`.

4. Validate with local evidence.
- Confirm symbols exist in `packages/effect/src/*.ts`.
- Confirm behavior with nearby tests in `packages/effect/test`.
- Do not claim semantics not evidenced by code/tests.

## Response Contract

When this skill is used, produce:

1. Exact API replacements (old -> new) used.
2. Behavior-impact notes (memoization, keep-alive, Cause flattening, equality).
3. Concrete file references used as evidence.
4. Known limitations or unresolved migrations.

## Guardrails

- Do not reintroduce v3 APIs in generated code.
- Do not claim stable semantics for `effect/unstable/*` modules.
- Do not infer runtime guarantees without source/test confirmation.
