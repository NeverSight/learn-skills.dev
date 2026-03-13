---
name: aureuserp-test-case-builder
description: Build and refactor Pest feature tests for AureusERP plugin APIs with reusable helpers, policy-permission auth setup, factory-first payloads, stable JSON assertions, and plugin-install bootstrap strategy. Use when creating or updating API tests under `plugins/*/*/tests`. This skill is structured to support a future Filament test-case track without changing current API behavior.
---

# AureusERP Test Case Builder

Use this skill to build plugin API tests with Pest using test-only fixes and reusable helpers.

## Scope Tracks

1. API test-case track (active now)
- Follow `references/api.md` for end-to-end workflow, helper boundaries, assertions, and guardrails.

2. Filament test-case track (reserved for future)
- Do not invent Filament-specific testing rules in this skill yet.
- Keep API conventions unchanged.
- When Filament guidance is added later, it should be added as separate references (for example `references/filament-*.md`) and selected explicitly by task type.

## Core Rules

1. Use Pest feature tests for API endpoints (`getJson`, `postJson`, `patchJson`, `deleteJson`).
2. Prefer factories for setup and payload creation.
3. Keep helper responsibility split strict:
- `SecurityHelper` for auth/permissions/guards.
- `TestBootstrapHelper` for non-security bootstrap and plugin installation.
4. Do not use `RefreshDatabase` or `LazilyRefreshDatabase` in test files; use global `DatabaseTransactions` wiring.
5. Prefer test/helper fixes before app code edits.
6. Do not use skip-as-solution.

## Quick Routing

1. API controller endpoint tests (`index/store/show/update/destroy`, auth, validation, restore/force-delete): use `references/api.md`.
2. API refactor/bugfix with helper cleanup: use `references/api.md`.
3. Template generation for a new plugin API test file: use `references/api.md`.

## Output Expectations

1. Keep tests plugin-scoped and reusable.
2. Keep assertions deterministic and aligned with JSON resources.
3. Keep payloads factory-first with targeted overrides only.
4. Keep install/bootstrap non-interactive and environment-safe.
