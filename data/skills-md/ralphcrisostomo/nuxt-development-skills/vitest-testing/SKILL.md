---
name: vitest-testing
model: sonnet
description: >
  Write and run Vitest unit tests for this Nuxt 4 project. Auto-triggers when
  creating or modifying composables, components, services, utils, or Lambda handlers.
  Use this skill whenever writing tests, adding test coverage, testing new features,
  fixing bugs (write regression test first), or when the user mentions testing,
  unit tests, vitest, TDD, coverage, or test coverage. Also use when creating any
  new file in app/composables/, app/components/, app/utils/, services/, or
  terraform/lambda/src/.
---

# Vitest Testing

## Test File Placement

| Source location | Test location |
|---|---|
| `app/composables/<name>.ts` | `tests/app/composables/<name>.test.ts` |
| `app/components/<Name>.vue` | `app/components/__tests__/<Name>.test.ts` (DOM tests) OR `tests/app/components/<Name>.test.ts` (logic-only) |
| `app/utils/<name>.ts` | `tests/app/utils/<name>.test.ts` |
| `services/<name>.ts` | `tests/services/<name>.test.ts` |
| `utils/<name>.ts` | `tests/utils/<name>.test.ts` |
| `terraform/lambda/src/<Name>/index.ts` | `terraform/lambda/src/<Name>/__tests__/index.test.ts` |

Use `__tests__/` co-location only for component DOM tests and Lambda handlers. Everything else goes in the top-level `tests/` mirror tree.

## Environment Selection

- **Default:** `node` (composables, services, utils, Lambda handlers)
- **DOM tests only:** Add `/** @vitest-environment happy-dom */` as the first line of the test file
- Never change `vitest.config.ts` environment globally

## Test Writing Rules

1. **Imports** — always explicit: `import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'`
2. **Nuxt auto-imports** — call `mockNuxtImports()` from `tests/helpers` in `beforeEach` for any code using `useRuntimeConfig`, `useState`, `computed`, `ref`, `watch`, `onMounted`, `onUnmounted`, `navigateTo`
3. **Naming** — always `*.test.ts`, never `*.spec.ts`
4. **Timers** — use `vi.useFakeTimers()` in `beforeEach` and `vi.useRealTimers()` in `afterEach` for async/timer tests
5. **Console noise** — suppress with `vi.spyOn(console, 'log').mockImplementation(() => {})` in `beforeEach`
6. **Logic extraction** — prefer testing extracted logic over DOM rendering; test behavior, not templates
7. **Component DOM tests** — use `@vue/test-utils` `mount()` with stubbed Nuxt UI components
8. **AWS service mocks** — use `mockSend` + `vi.mock('@aws-sdk/...')` pattern (see `references/testing-patterns.md`)

## What to Test (per code type)

- **Composables:** return values, state mutations, reactive updates, edge cases
- **Components:** props, emits, slot rendering, conditional rendering (via logic extraction where possible)
- **Services:** success path, error handling (custom error classes), edge cases (empty input, missing fields)
- **Utils:** pure function I/O, boundary conditions
- **Lambda handlers:** each resolver action, valid/invalid input, DynamoDB mock responses, error paths

## Running Tests

```bash
bun run test             # Single run
bun run test:watch       # Watch mode
bun run test:coverage    # With v8 coverage report
```

## Coverage

Coverage uses `@vitest/coverage-v8`. Config is in `vitest.config.ts`. Thresholds: lines 80%, functions 80%, branches 70%, statements 80%.

## Reference

Read `references/testing-patterns.md` for detailed mock patterns, full templates, and real codebase examples.
