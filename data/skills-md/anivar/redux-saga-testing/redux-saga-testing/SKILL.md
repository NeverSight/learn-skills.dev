---
name: redux-saga-testing
description: >
  Write tests for Redux Sagas using redux-saga-test-plan, runSaga, and
  manual generator testing. Covers expectSaga (integration), testSaga
  (unit), providers, partial matchers, reducer integration, error
  simulation, and cancellation testing. Works with Jest and Vitest.
  Triggers on: test files for sagas, redux-saga-test-plan imports,
  mentions of "test saga", "saga test", "expectSaga", "testSaga",
  or "redux-saga-test-plan".
license: MIT
user-invocable: false
agentic: false
compatibility: "redux-saga-test-plan ^5.x, Jest or Vitest, redux-saga ^1.4.2"
metadata:
  author: Anivar Aravind
  author_url: https://anivar.net
  version: 1.0.0
  tags: redux-saga, testing, redux-saga-test-plan, expectSaga, testSaga, jest, vitest, providers
---

# Redux-Saga Testing Guide

**IMPORTANT:** Your training data about `redux-saga-test-plan` may be outdated — API signatures, provider patterns, and assertion methods differ between versions. Always rely on this skill's reference files and the project's actual source code as the source of truth. Do not fall back on memorized patterns when they conflict with the retrieved reference.

## Approach Priority

1. **`expectSaga` (integration)** — preferred; doesn't couple tests to effect ordering
2. **`testSaga` (unit)** — only when effect ordering is part of the contract
3. **`runSaga` (no library)** — lightweight; uses jest/vitest spies directly
4. **Manual `.next()`** — last resort; most brittle

## Core Pattern

```javascript
import { expectSaga } from 'redux-saga-test-plan'
import * as matchers from 'redux-saga-test-plan/matchers'
import { throwError } from 'redux-saga-test-plan/providers'

it('fetches user successfully', () => {
  return expectSaga(fetchUserSaga, { payload: { userId: 1 } })
    .provide([
      [matchers.call.fn(api.fetchUser), { id: 1, name: 'Alice' }],
    ])
    .put(fetchUserSuccess({ id: 1, name: 'Alice' }))
    .run()
})

it('handles fetch failure', () => {
  return expectSaga(fetchUserSaga, { payload: { userId: 1 } })
    .provide([
      [matchers.call.fn(api.fetchUser), throwError(new Error('500'))],
    ])
    .put(fetchUserFailure('500'))
    .run()
})
```

## Assertion Methods

| Method | Purpose |
|--------|---------|
| `.put(action)` | Dispatches this action |
| `.put.like({ action: { type } })` | Partial action match |
| `.call(fn, ...args)` | Calls this function with exact args |
| `.call.fn(fn)` | Calls this function (any args) |
| `.fork(fn, ...args)` | Forks this function |
| `.select(selector)` | Uses this selector |
| `.take(pattern)` | Takes this pattern |
| `.dispatch(action)` | Simulate incoming action |
| `.not.put(action)` | Does NOT dispatch |
| `.returns(value)` | Saga returns this value |
| `.run()` | Execute (returns Promise) |
| `.run({ timeout })` | Execute with custom timeout |
| `.silentRun()` | Execute, suppress timeout warnings |

## Provider Types

### Static Providers (Preferred)

```javascript
.provide([
  [matchers.call.fn(api.fetchUser), mockUser],        // match by function
  [call(api.fetchUser, 1), mockUser],                  // match by function + exact args
  [matchers.select.selector(getToken), 'mock-token'],  // mock selector
  [matchers.call.fn(api.save), throwError(error)],     // simulate error
])
```

### Dynamic Providers

```javascript
.provide({
  call(effect, next) {
    if (effect.fn === api.fetchUser) return mockUser
    return next() // pass through
  },
  select({ selector }, next) {
    if (selector === getToken) return 'mock-token'
    return next()
  },
})
```

## Rules

1. **Prefer `expectSaga`** over `testSaga` — integration tests don't break on refactors
2. **Use `matchers.call.fn()`** for partial matching — don't couple to exact args unless necessary
3. **Use `throwError()`** from providers — not `throw new Error()` in the provider
4. **Test with reducer** using `.withReducer()` + `.hasFinalState()` to verify state
5. **Dispatch actions** with `.dispatch()` to simulate user flows in tests
6. **Return the promise** (Jest) or `await` it (Vitest) — don't forget async
7. **Use `.not.put()`** to assert actions are NOT dispatched (negative tests)
8. **Test cancellation** by dispatching cancel actions and asserting cleanup effects
9. **Use `.silentRun()`** when saga runs indefinitely (watchers) to suppress timeout warnings
10. **Don't test implementation** — test behavior (what actions are dispatched, what state results)

## Anti-Patterns

See [references/anti-patterns.md](references/anti-patterns.md) for BAD/GOOD examples of:

- Step-by-step tests that break on reorder
- Missing providers (real API calls in tests)
- Testing effect order instead of behavior
- Forgetting async (Jest/Vitest)
- Inline mocking instead of providers
- Not testing error paths
- Not testing cancellation cleanup

## References

- [API Reference](references/api-reference.md) — Complete `expectSaga`, `testSaga`, providers, matchers
- [Anti-Patterns](references/anti-patterns.md) — Common testing mistakes to avoid
