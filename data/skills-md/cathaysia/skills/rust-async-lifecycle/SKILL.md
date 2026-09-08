---
name: rust-async-lifecycle
description: >-
  Structured-concurrency patterns for Rust async lifecycles: RAII (the object
  is both the resource and its handler), TaskScope/AsyncClose, and the
  spawn+select pattern with cancellation selected at the top. Use when
  (1) auditing or fixing every tokio::spawn / select! against "spawn outside,
  select cancellation at the top, keep functions pure"; (2) refactoring
  anti-patterns such as handle/resource separation, selects buried inside
  functions, nested spawn+select chains, or abort() used as routine
  cancellation; (3) designing background tasks, accept loops, graceful
  shutdown, and resource draining. Triggers: concurrency audit, spawn/select
  review, task leaks, CancellationToken, TaskScope, structured concurrency,
  graceful shutdown.
---

# Rust Async Lifecycle: Structured-Concurrency Patterns

One sentence: **RAII (object = resource + handler) + TaskScope structured concurrency + the spawn+select pattern where spawn lives at the call site, the cancellation select sits at the top of the spawned task, and functions stay pure.**

## 1. The object is both the resource and its handler (RAII)

One object owns the resource, the lifecycle, and the operations - do not split them:

```rust
pub struct X {
    inner: Arc<XInner>,
    scope: TaskScope,                        // lifecycle = token + tracker
}

impl Drop for X {
    fn drop(&mut self) { self.scope.cancel(); }   // Drop only signals cancellation, never aborts
}

impl X {
    pub async fn close(&self) { self.scope.close().await; }   // cancel + drain
    pub async fn op(&self) -> Result<T> { ... }               // methods return real values
}
```

Anti-pattern: handle separation - the object is just `Arc<RwLock<state>>` or a bag of Arc fields; the resource is shared everywhere, the lifecycle depends on manual calls, and nobody drains.

## 2. The spawn+select pattern (core rule)

**Every spawn is paired with a select; the select on the cancellation token lives at the top of the spawned task; spawn moves to the call site; the spawned function stays pure:**

```rust
// Correct: pure function, spawn at the call site, select at the top
impl FastnetClient {
    pub(crate) async fn token_rotation(self: Arc<Self>, config: Arc<dyn ConfigProvider>) { /* pure loop, no token, no select */ }
}

let rotation = client.clone().token_rotation(config);   // method only produces a future
let shutdown = scope.token();
scope.spawn(async move {
    tokio::select! {
        _ = shutdown.cancelled() => {}     // cancellation branch at the top
        _ = rotation => {}                 // the function never sees cancellation
    }
});
```

**Anti-patterns:**
- Wrong: select inside the function: `select! { shutdown.cancelled() ... }` inside `run_api_server(port, client, shutdown)`
- Wrong: spawn inside a helper method: `spawn_token_rotation(...)` calls `tokio::spawn` itself, so callers cannot track or drain it
- Wrong: function signatures carrying a token and selecting on it in a loop
- Wrong: deeply nested spawn+select chains along one call path (4+ layers)

**Key point:** when a task is tracked by `scope.spawn`, the select must use `scope.token()` (not an external token) - `scope.close()` cancels the scope token first and then waits; the task observes the scope token and exits, so `wait()` returns. Selecting on an external token makes `close()` hang forever.

## 3. TaskScope / AsyncClose primitives

```rust
pub trait AsyncClose {
    fn close(&self) -> impl Future<Output = ()> + Send;   // cancel + tracker.close + wait
}

#[derive(Clone)]
pub struct TaskScope {
    token: CancellationToken,
    tracker: TaskTracker,
}
// new / child (parent-token cascade + independent tracker) / token / is_cancelled / cancel / spawn
```

Companions:
- `join_outcome`: turns a JoinHandle result into "normal / unexpected stop / join failure"
- `shutdown_signal`: Ctrl-C + SIGTERM

Top-level daemon shape: `run() = serve() + close()`, draining on every exit path including errors.

## 4. Decision table for spawn and select

| Situation | Approach |
|---|---|
| Return value needed | `await`, never spawn |
| Independent long-lived task | spawn once at construction, `scope.spawn` + select at the top |
| accept -> per connection | spawn at the fan-out point, tracked by scope |
| Blocking synchronous code | `spawn_blocking` |
| Cancellation | always `scope.token()` select at the top |
| abort | only for abandoning a pending one-shot RPC; never for long-lived tasks |
| Only exception | engines owning child tasks (e.g., WireGuardEngine) must observe the token internally to drain children |

## 5. Audit workflow

1. `grep -rn "tokio::spawn|spawn_blocking|select!" --include="*.rs" --exclude-dir=target .`, tally per file, exclude tests.
2. Tag every spawn: tracked by scope/tracker? observes cancellation? is the return value needed by the caller? uses abort? drains on close?
3. Tag every select: has a cancellation branch? lives inside a function? awaits a JoinHandle (use JoinSet or a channel instead)? deeply nested?
4. Check top-level daemons: does the main select have `shutdown_signal()`? does exit call `token.cancel()`? do session/connection handlers await cleanup on the exit path?

## 6. Fix guidelines (in priority order)

1. Create a shared crate extracting `TaskScope` / `AsyncClose` / `join_outcome` / `shutdown_signal`.
2. Replace bare spawns with `scope.spawn`; split helper-method spawns into pure futures and move the spawn to the call site.
3. Move selects out of functions to the top of the spawned task; the top select backs every loop's cancellation.
4. Replace "spawn per tick" with a single background loop plus a top select.
5. Add a `shutdown_signal` branch to the top-level select.
6. Verify: `cargo clippy --workspace --all-targets -- -D warnings`, full tests, `cargo fmt --check`, and pre-commit (line limits, no unwrap, no `#[allow(dead_code)]`).
