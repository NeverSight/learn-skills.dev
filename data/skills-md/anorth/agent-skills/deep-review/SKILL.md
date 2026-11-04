---
name: deep-review
description: >-
  Deep, themed review of a diff: the review-diff flow and its standard lenses, plus one cheap reviewer subagent
  per theme, using distinctive preferences distilled from Alex North's public GitHub reviews
  (naming, API shape, errors, tests, coupling, and related themes). Needs the review-diff skill.
  Use when the user asks for a deep review, themed review, or anorth-style review.
disable-model-invocation: false
---

# Deep review

Run the `/review-diff` skill's flow with a bigger lens set.
If `review-diff` isn't available, tell the user and stop.

At its Lenses step, read the change set and decide which themes below are relevant. The lens set is:

- `review-diff`'s standard lenses, on their usual tiers, by their absolute paths in `review-diff`'s directory;
- each theme under **Always**, and each theme under **When the diff matches** that fits the diff,
  on the `cheap` tier. Pass the theme file's absolute path as the lens.

Everything else follows `review-diff`: models, launch, check, triage, fix, and report.
Theme reviewers on the `cheap` tier are noisy, so the check step matters most for them.

## Always

- [`Naming`](themes/naming.md) — identifiers
- [`Style`](themes/style.md) — dead weight, constants, order, locality
- [`Comments`](themes/comments.md) — comments, docs, stale nearby comments

## When the diff matches

- [`API Shape`](themes/api-shape.md) — public functions, types, endpoints, events, persisted formats
- [`Architecture`](themes/architecture.md) — modules, layers, where state or effects live
- [`Change Scope`](themes/change-scope.md) — mixed features, refactors, or cleanups in one PR
- [`Concurrency`](themes/concurrency.md) — shared mutable state, threads/coroutines, timers
- [`Coupling`](themes/coupling.md) — module boundaries, wiring, cross-component APIs
- [`Dependencies`](themes/dependencies.md) — manifests, lockfiles, vendored or generated code, new libraries
- [`CI locally`](themes/developer-experience.md) — CI, build, lint, or codegen steps
- [`Errors`](themes/errors.md) — new or changed failure paths, error types, panics
- [`Invariants`](themes/invariants.md) — validation, state transitions, persistence, aggregates
- [`Observability`](themes/observability.md) — logs, metrics, journals, or swallowed failures
- [`Tests`](themes/tests.md) — tests, fixtures, doubles, or test helpers
