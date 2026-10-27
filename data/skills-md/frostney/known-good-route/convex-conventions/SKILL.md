---
name: convex-conventions
description: >-
  Applies the user's Convex backend conventions while deferring mechanics to
  upstream Convex skills and current APIs to the live Convex docs. Use when
  scaffolding, reviewing, or refactoring Convex functions, schemas, or auth.
license: Unlicense OR MIT
compatibility: >-
  Assumes a Bun-based Convex project; verifies APIs against live Convex docs.
---

# Convex conventions

These are house-style defaults, not a Convex manual. Use current official Convex
skills, when installed, for scaffolding, auth, migrations, performance work,
components, and API mechanics; this skill adds project policy. Apply only what
the requested change touches.

## Authority

Verify each touched API against live Convex docs and the installed version.
Read release notes before a major or minor upgrade. Live docs win over this
skill; memory and prior turns do not establish current API behavior.

## Layout and shared shapes

- Keep `convex/` at root and never edit `_generated/`.
- `schema.ts` owns `defineSchema` and table declarations.
- `auth.config.ts` owns the Clerk JWT provider.
- Keep one module each for reusable table validators, semantic validation, auth
  helpers, and rate-limit configuration.
- Add `crons.ts` and `http.ts` only when used.
- Public feature surfaces and their tests are co-located.
- Define table validators once and compose them into schema, `args`, and
  `returns`; do not redeclare an existing shape inline.

## Auth and public functions

- Clerk is the identity provider. Server code derives identity from
  `ctx.auth.getUserIdentity()` through one helper; clients never submit `userId`.
- Every public function authenticates at the top and declares both `args` and
  `returns` validators.
- Use internal functions for scheduling, sensitive side effects, and
  cross-function reuse that must not be public.
- Keep structural validation in validators and semantic checks such as date
  correctness, length caps, and sanitization in the handler.

## Reads, writes, and effects

- Indexes narrow candidates; further filtering happens in code. Give indexes
  semantic names and avoid redundant ones.
- Cap every otherwise unbounded query with `.take()`; comment only when the cap
  is load-bearing.
- Queries are pure and deterministic: no `Date.now()` inside them.
- Mutations write. Actions call external systems. An action persists through an
  internal mutation rather than mixing the roles.
- Rate-limit every public mutation with the current
  `@convex-dev/rate-limiter` API. Token bucket suits high-frequency operations;
  fixed window suits low-frequency operations.

## Stored data

- User-created rows use soft deletion with optional numeric `deletedAt`; public
  mutations do not hard-delete them.
- Audit trails are append-only records.
- Server metadata such as identity and timestamps comes from handler context,
  never client args.
- Data-at-rest schema changes use widen, migrate, then narrow through the
  official migration workflow.
- Aggregate additions include a backfill. Aggregate synchronization failure
  must not block the primary write.

## Client types and components

- Derive client types from generated `Doc<...>` and `Id<...>`.
- One dedicated module re-exports semantic client aliases; app code imports
  there, never directly from `convex/_generated`, and never manually copies table
  shapes.
- Prefer official Convex components for existing capabilities and verify each
  component README. Use the official component workflow when authoring a new
  reusable component.

## Completion

- Codegen and typecheck pass.
- Relevant function tests, an independent review of the diff, such as
  `/code-review`, and the project gate pass on the final content. Function
  tests that call the public function and assert its observable result are its
  behavior evidence. Started directly, the change then continues through
  `/deliver` under the [delivery settings](../deliver/SKILL.md#delivery-settings).
- Any schema migration ran against the development deployment and its result is
  recorded.
- No public function lacks auth, `args`, or `returns`; no public mutation lacks
  rate limiting; no unbounded query lacks a cap.
