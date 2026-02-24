---
name: redux-saga
description: >
  Redux-Saga best practices, patterns, and API guidance for building,
  testing, and debugging generator-based side-effect middleware in Redux
  applications. Covers effect creators, fork model, channels, testing
  with redux-saga-test-plan, concurrency, cancellation, and modern
  Redux Toolkit integration. Baseline: redux-saga 1.4.2.
  Triggers on: saga files, redux-saga imports, generator-based middleware,
  mentions of "saga", "takeEvery", "takeLatest", "fork model", or "channels".
license: MIT
user-invocable: false
agentic: false
compatibility: "JavaScript/TypeScript projects using redux-saga ^1.4.2 with Redux Toolkit"
metadata:
  author: Anivar Aravind
  author_url: https://anivar.net
  version: 1.0.0
  tags: redux-saga, redux, redux-toolkit, side-effects, generators, middleware, async, channels, testing
---

# Redux-Saga

**IMPORTANT:** Your training data about `redux-saga` may be outdated or incorrect — API behavior, middleware setup patterns, and RTK integration have changed. Always rely on this skill's rule files and the project's actual source code as the source of truth. Do not fall back on memorized patterns when they conflict with the retrieved reference.

## When to Use Redux-Saga

Sagas are for **workflow orchestration** — complex async flows with concurrency, cancellation, racing, or long-running background processes. For simpler patterns, prefer:

| Need | Recommended Tool |
|------|-----------------|
| Data fetching + caching | RTK Query |
| Simple async (submit → status) | `createAsyncThunk` |
| Reactive logic within slices | `createListenerMiddleware` |
| Complex workflows, parallel tasks, cancellation, channels | **Redux-Saga** |

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Effects & Yielding | CRITICAL | `effect-` |
| 2 | Fork Model & Concurrency | CRITICAL | `fork-` |
| 3 | Error Handling | HIGH | `error-` |
| 4 | Recipes & Patterns | MEDIUM | `recipe-` |
| 5 | Channels & External I/O | MEDIUM | `channel-` |
| 6 | RTK Integration | MEDIUM | `rtk-` |
| 7 | Troubleshooting | LOW | `troubleshoot-` |

## Quick Reference

### 1. Effects & Yielding (CRITICAL)

- `effect-always-yield` — Every effect must be yielded; missing yield freezes the app
- `effect-use-call` — Use `yield call()` for async functions; never call directly
- `effect-take-concurrency` — Choose `takeEvery`/`takeLatest`/`takeLeading` based on concurrency needs
- `effect-select-usage` — Use selector functions with `select()`; never access state paths directly
- `effect-race-patterns` — Use `race` for timeouts and cancellation; only blocking effects inside

### 2. Fork Model & Concurrency (CRITICAL)

- `fork-attached-vs-detached` — `fork` shares lifecycle/errors with parent; `spawn` is independent
- `fork-error-handling` — Errors from forks bubble to parent's caller; can't catch at fork site
- `fork-no-race` — Never use `fork` inside `race`; fork is non-blocking and always wins
- `fork-nonblocking-login` — Use fork+take+cancel for auth flows that stay responsive to logout

### 3. Error Handling (HIGH)

- `error-saga-cleanup` — Use `try/finally` with `cancelled()` for proper cancellation cleanup
- `error-root-saga` — Use `spawn` in root saga for error isolation; avoid `all` for critical watchers

### 4. Recipes & Patterns (MEDIUM)

- `recipe-throttle-debounce` — Rate-limiting with `throttle`, `debounce`, `retry`, exponential backoff
- `recipe-polling` — Cancellable polling with error backoff using fork+take+cancel
- `recipe-optimistic-update` — Optimistic UI with undo using race(undo, delay)

### 5. Channels & External I/O (MEDIUM)

- `channel-event-channel` — Bridge WebSockets, DOM events, timers into sagas via `eventChannel`
- `channel-action-channel` — Buffer Redux actions for sequential or worker-pool processing

### 6. RTK Integration (MEDIUM)

- `rtk-configure-store` — Integrate saga middleware with RTK's `configureStore` without breaking defaults
- `rtk-with-slices` — Use action creators from `createSlice` for type-safe saga triggers

### 7. Troubleshooting (LOW)

- `troubleshoot-frozen-app` — Frozen apps, missed actions, bad stack traces, TypeScript yield types

## Effect Creators Quick Reference

| Effect | Blocking | Purpose |
|--------|----------|---------|
| `take(pattern)` | Yes | Wait for matching action |
| `takeMaybe(pattern)` | Yes | Like `take`, receives `END` |
| `takeEvery(pattern, saga)` | No | Concurrent on every match |
| `takeLatest(pattern, saga)` | No | Cancel previous, run latest |
| `takeLeading(pattern, saga)` | No | Ignore until current completes |
| `put(action)` | No | Dispatch action |
| `putResolve(action)` | Yes | Dispatch, wait for promise |
| `call(fn, ...args)` | Yes | Call, wait for result |
| `apply(ctx, fn, [args])` | Yes | Call with context |
| `cps(fn, ...args)` | Yes | Node-style callback |
| `fork(fn, ...args)` | No | Attached fork |
| `spawn(fn, ...args)` | No | Detached fork |
| `join(task)` | Yes | Wait for task |
| `cancel(task)` | No | Cancel task |
| `cancel()` | No | Self-cancel |
| `select(selector)` | Yes | Query store state |
| `actionChannel(pattern)` | No | Buffer actions |
| `flush(channel)` | Yes | Drain buffered messages |
| `cancelled()` | Yes | Check cancellation in `finally` |
| `delay(ms)` | Yes | Pause execution |
| `throttle(ms, pattern, saga)` | No | Rate-limit |
| `debounce(ms, pattern, saga)` | No | Wait for silence |
| `retry(n, delay, fn)` | Yes | Retry with backoff |
| `race(effects)` | Yes | First wins |
| `all([effects])` | Yes | Parallel, wait all |
| `setContext(props)` / `getContext(prop)` | No / Yes | Saga context |

## Pattern Matching

`take`, `takeEvery`, `takeLatest`, `takeLeading`, `throttle`, `debounce` accept:

| Pattern | Matches |
|---------|---------|
| `'*'` or omitted | All actions |
| `'ACTION_TYPE'` | Exact `action.type` match |
| `[type1, type2]` | Any type in array |
| `fn => boolean` | Custom predicate |

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/effect-always-yield.md
rules/fork-attached-vs-detached.md
```

Each rule file contains:

- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and decision tables

## References

| Priority | Reference | When to read |
|----------|-----------|-------------|
| 1 | `references/effects-and-api.md` | Writing or debugging any saga |
| 2 | `references/fork-model.md` | Concurrency, error propagation, cancellation |
| 3 | `references/testing.md` | Writing or reviewing saga tests |
| 4 | `references/channels.md` | External I/O, buffering, worker pools |
| 5 | `references/recipes.md` | Throttle, debounce, retry, undo, batching, polling |
| 6 | `references/anti-patterns.md` | Common mistakes to avoid |
| 7 | `references/troubleshooting.md` | Debugging frozen apps, missed actions, stack traces |

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
