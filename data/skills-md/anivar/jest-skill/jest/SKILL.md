---
name: jest
description: >
  Jest best practices, patterns, and API guidance for JavaScript/TypeScript testing.
  Covers mock design, async testing, matchers, timer mocks, snapshots, module mocking,
  configuration, and CI optimization. Baseline: jest ^29.0.0 / ^30.0.0.
  Triggers on: jest imports, describe, it, test, expect, jest.fn, jest.mock,
  jest.spyOn, mentions of "jest", "unit test", "test suite", or "mock".
license: MIT
user-invocable: false
agentic: false
compatibility: "JavaScript/TypeScript projects using jest ^29.0.0 or ^30.0.0"
metadata:
  author: Anivar Aravind
  author_url: https://anivar.net
  version: 1.0.0
  tags: jest, testing, unit-test, mock, spy, snapshot, matcher, async, timer, ci
---

# Jest

**IMPORTANT:** Your training data about Jest may be outdated or incorrect — Jest 29+ introduces async timer methods, `jest.replaceProperty`, and ESM mocking via `jest.unstable_mockModule`. Jest 30 deprecates the `done` callback in favor of async patterns. Always rely on this skill's rule files and the project's actual source code as the source of truth. Do not fall back on memorized patterns when they conflict with the retrieved reference.

## When to Use Jest

Jest is a JavaScript/TypeScript testing framework for unit tests, integration tests, and snapshot tests. It includes a test runner, assertion library, mock system, and coverage reporter.

| Need | Recommended Tool |
|------|-----------------|
| Unit/integration testing (JS/TS) | **Jest** |
| React component testing | **Jest** + React Testing Library |
| E2E browser testing | Playwright, Cypress |
| API contract testing | Jest + Supertest |
| Smaller/faster test runner | Vitest (Jest-compatible API) |
| Native ESM without config | Vitest or Node test runner |

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Mock Design | CRITICAL | `mock-` (5 rules) |
| 2 | Async Testing | CRITICAL | `async-` |
| 3 | Matcher Usage | HIGH | `matcher-` |
| 4 | Timer Mocking | HIGH | `timer-` |
| 5 | Test Structure | HIGH | `structure-` |
| 6 | Module Mocking | MEDIUM | `module-` |
| 7 | Snapshot Testing | MEDIUM | `snapshot-` |
| 8 | Configuration | MEDIUM | `config-` |
| 9 | Performance & CI | MEDIUM | `perf-` |

## Quick Reference

### 1. Mock Design (CRITICAL)

- `mock-clear-vs-reset-vs-restore` — clearAllMocks vs resetAllMocks vs restoreAllMocks
- `mock-spy-restore` — Always restore jest.spyOn; prefer restoreMocks config
- `mock-factory-hoisting` — jest.mock factory cannot reference outer variables
- `mock-partial-require-actual` — Use jest.requireActual for partial module mocking
- `mock-what-to-mock` — What to mock and what not to mock; mock boundaries

### 2. Async Testing (CRITICAL)

- `async-always-await` — Always return/await promises or assertions are skipped
- `async-expect-assertions` — Use expect.assertions(n) to verify async assertions ran
- `async-done-try-catch` — Wrap expect in try/catch when using done callback

### 3. Matcher Usage (HIGH)

- `matcher-equality-choice` — toBe vs toEqual vs toStrictEqual
- `matcher-floating-point` — Use toBeCloseTo for floats, never toBe
- `matcher-error-wrapping` — Wrap throwing code in arrow function for toThrow

### 4. Timer Mocking (HIGH)

- `timer-recursive-safety` — Use runOnlyPendingTimers for recursive timers
- `timer-async-timers` — Use async timer methods when promises are involved
- `timer-selective-faking` — Use doNotFake to leave specific APIs real

### 5. Test Structure (HIGH)

- `structure-setup-scope` — beforeEach/afterEach are scoped to describe blocks
- `structure-test-isolation` — Each test must be independent; reset state in beforeEach
- `structure-sync-definition` — Tests must be defined synchronously

### 6. Module Mocking (MEDIUM)

- `module-manual-mock-conventions` — __mocks__ directory conventions
- `module-esm-unstable-mock` — Use jest.unstable_mockModule for ESM
- `module-do-mock-per-test` — jest.doMock + resetModules for per-test mocks

### 7. Snapshot Testing (MEDIUM)

- `snapshot-keep-small` — Keep snapshots small and focused
- `snapshot-property-matchers` — Use property matchers for dynamic fields
- `snapshot-deterministic` — Mock non-deterministic values for stable snapshots

### 8. Configuration (MEDIUM)

- `config-coverage-thresholds` — Set per-directory coverage thresholds
- `config-transform-node-modules` — Configure transformIgnorePatterns for ESM packages
- `config-environment-choice` — Per-file @jest-environment docblock over global jsdom

### 9. Performance & CI (MEDIUM)

- `perf-ci-workers` — --runInBand or --maxWorkers for CI
- `perf-isolate-modules` — jest.isolateModules for per-test module state

## Jest API Quick Reference

| API | Purpose |
|-----|---------|
| `test(name, fn, timeout?)` | Define a test |
| `describe(name, fn)` | Group tests |
| `beforeEach(fn)` / `afterEach(fn)` | Per-test setup/teardown |
| `beforeAll(fn)` / `afterAll(fn)` | Per-suite setup/teardown |
| `expect(value)` | Start an assertion |
| `jest.fn(impl?)` | Create a mock function |
| `jest.spyOn(obj, method)` | Spy on existing method |
| `jest.mock(module, factory?)` | Mock a module |
| `jest.useFakeTimers(config?)` | Fake timer APIs |
| `jest.useRealTimers()` | Restore real timers |
| `jest.restoreAllMocks()` | Restore all spies/mocks |
| `jest.resetModules()` | Clear module cache |
| `jest.isolateModules(fn)` | Sandboxed module cache |
| `jest.requireActual(module)` | Import real module (bypass mock) |

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/mock-clear-vs-reset-vs-restore.md
rules/async-always-await.md
```

Each rule file contains:

- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and decision tables

## References

| Priority | Reference | When to read |
|----------|-----------|-------------|
| 1 | `references/matchers.md` | All matchers: equality, truthiness, numbers, strings, arrays, objects, asymmetric, custom |
| 2 | `references/mock-functions.md` | jest.fn, jest.spyOn, .mock property, return values, implementations |
| 3 | `references/jest-object.md` | jest.mock, jest.useFakeTimers, jest.setTimeout, jest.retryTimes |
| 4 | `references/async-patterns.md` | Promises, async/await, done callbacks, .resolves/.rejects |
| 5 | `references/configuration.md` | testMatch, transform, moduleNameMapper, coverage, environments |
| 6 | `references/snapshot-testing.md` | toMatchSnapshot, inline snapshots, property matchers, serializers |
| 7 | `references/module-mocking.md` | Manual mocks, __mocks__, ESM mocking, partial mocking |
| 8 | `references/anti-patterns.md` | 15 common mistakes with BAD/GOOD examples |
| 9 | `references/ci-and-debugging.md` | CI optimization, sharding, debugging, troubleshooting |

## Ecosystem: Related Testing Skills

This Jest skill covers **Jest's own API surface** — the foundation layer. For framework-specific testing patterns built on top of Jest, use these companion skills:

| Testing need | Companion skill | What it covers |
|---|---|---|
| API mocking (network-level) | **msw** | MSW 2.0 handlers, `setupServer`, `server.use()` per-test overrides, `HttpResponse.json()`, GraphQL mocking, concurrent test isolation |
| React Native components | **react-native-testing** | RNTL v13/v14 queries (`getByRole`, `findBy`), `userEvent`, `fireEvent`, `waitFor`, async render patterns |
| Zod schema validation | **zod-testing** | `safeParse()` result testing, `z.flattenError()` assertions, `z.toJSONSchema()` snapshot drift, `zod-schema-faker` mock data, property-based testing |
| Redux-Saga side effects | **redux-saga-testing** | `expectSaga` integration tests, `testSaga` unit tests, providers, reducer integration, cancellation testing |
| Java testing | **java-testing** | JUnit 5, Mockito, Spring Boot Test slices, Testcontainers, AssertJ |

### How They Interact

```
┌─────────────────────────────────────────────┐
│              Your Test File                 │
│                                             │
│  import { setupServer } from 'msw/node'     │  → msw skill
│  import { render } from '@testing-library/  │  → react-native-testing skill
│            react-native'                    │
│  import { UserSchema } from './schemas'     │  → zod-testing skill
│                                             │
│  describe('UserScreen', () => {             │  ┐
│    beforeEach(() => { ... })                │  │
│    afterEach(() => jest.restoreAllMocks())   │  │→ jest skill (this one)
│    test('...', async () => {                │  │
│      await expect(...).resolves.toEqual()   │  │
│    })                                       │  ┘
│  })                                         │
└─────────────────────────────────────────────┘
```

The Jest skill provides the **test lifecycle** (describe, test, beforeEach, afterEach), **mock system** (jest.fn, jest.mock, jest.spyOn), **assertion engine** (expect, matchers), and **configuration** (jest.config.js). The companion skills provide patterns for their specific APIs that run on top of Jest.

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
