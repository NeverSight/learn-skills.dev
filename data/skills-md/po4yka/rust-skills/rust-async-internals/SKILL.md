---
name: rust-async-internals
description: Use when writing or debugging tokio task and future mechanics, including cancel safety in tokio::select!, timeout, JoinSet, or FuturesUnordered; task ownership and shutdown with JoinHandle, TaskTracker, or CancellationToken; blocking work via spawn_blocking, block_in_place, or block_on from a foreign thread; Waker::noop polling from a synchronous loop; and Send bounds on an async closure, AsyncFn, or async fn in traits. Triggers on "disabled select branch", "shutdown hang", "async hang", a !Send future, broadcast Lagged, and a MutexGuard held across .await.
license: BSD-3-Clause
---

# Rust Async Internals

## Decision table

| You must | Use | Do not use |
|---|---|---|
| Run N futures and keep only the first result | `tokio::select!` | `join!` |
| Run N futures to completion | `tokio::join!` or `try_join!` | `select!` |
| Own a set of spawned tasks and collect their results | `JoinSet` + `join_next` | a bare `Vec<JoinHandle>` |
| Track a long-lived, unbounded task set (an accept loop) for shutdown | `tokio_util::task::TaskTracker` + `close()` + `wait()` | a `JoinSet` that nobody drains; it keeps every result |
| Abort a task when its owner drops the handle | `tokio_util::task::AbortOnDropHandle` | a bare `JoinHandle`; its drop detaches the task |
| Bound the concurrency of a work stream | `stream::iter(..).buffer_unordered(K)` | `spawn` in an unbounded loop |
| Shut down a task tree | `CancellationToken` + `child_token()` | `Notify` |
| Cancel on any early return or panic | `token.drop_guard()` | manual cleanup at each `?` |
| Race work against shutdown and keep the value | `token.run_until_cancelled(fut)` | a hand-written `select!` |
| Do bounded blocking or CPU work | `spawn_blocking` | `block_in_place` |
| Run an indefinite blocking loop | `std::thread::spawn` | `spawn_blocking` |
| Deliver every message without loss | `mpsc` | `broadcast` |
| Keep a critical `.await` sequence atomic | `tokio::spawn` + join the handle | `select!` around it |

## Stall and hang triage

| Symptom | Likely cause | Check or fix |
|---|---|---|
| Every task is slow, one looks stuck | a blocking call in async context | grep for `std::thread::sleep`, `std::fs`, `std::net`, synchronous HTTP or DB calls; move them as [Blocking work](#blocking-work) says |
| Shutdown never completes | a `select!` loop without a `cancelled()` arm | add `biased;` + `_ = cancel.cancelled() => break` |
| Tasks abort, but the process does not exit | a started `spawn_blocking` closure; nothing can abort it | pass a `CancellationToken` into the closure and check it; `Runtime::shutdown_timeout` stops only the wait |
| Latency spikes, no clear cause | long-lived tasks fill the blocking pool | move indefinite work to `std::thread::spawn` |
| `spawn_blocking` work hangs on tokio 1.52.0 | a regression in exactly 1.52.0 (tokio issue #8056) | `cargo update -p tokio` to 1.52.1 or later |
| A timeout is exceeded but returns `Ok`, or never returns | one poll does not yield | see [Timeouts](#timeouts) |
| Panic: "can call blocking only when running on the multi-threaded runtime" | `block_in_place` on a `current_thread` runtime, including a default `#[tokio::test]` | use `spawn_blocking` |
| Panic: "Cannot start a runtime from within a runtime" | `block_on` on a thread that drives async tasks | `.await` the future; block only on a `std::thread` or in `spawn_blocking` with a `Handle` |
| Events are missing, no error is logged | `while let Ok(..)` on a `broadcast` receiver ends at the first `Lagged` | match `RecvError::Lagged(n)`, or switch to `mpsc` |
| Deadlock only under concurrent load | a `std::sync::Mutex` guard held across `.await` | run `clippy::await_holding_lock`; drop the guard before the `.await` |
| A stream stalls after one `Pending`, a peer sees no write, or io_uring hangs after a cancel | a synchronous-loop bridge defect | read [references/manual-poll-bridge.md](references/manual-poll-bridge.md#triage) |
| File descriptors accumulate | a raw fd without an owner on an error path | hold every fd as `OwnedFd` so each early return closes it |

## Verify

| Claim | Check | A green result does not prove |
|---|---|---|
| No lock guard or `RefCell` borrow crosses `.await` | `cargo clippy --locked --all-targets -- -D clippy::await_holding_lock -D clippy::await_holding_refcell_ref` | cancel safety, or lock order between tasks |
| Shutdown is bounded | keep one task busy, cancel the token, assert `tokio::time::timeout(deadline, handle).await.is_ok()`; also under `flavor = "multi_thread"` | shutdown under production load |
| Timeout and retry logic | `#[tokio::test(start_paused = true)]` (tokio `test-util` feature) with `tokio::time::advance` | a blocking poll; paused time does not bound CPU work |
| Code that calls `block_in_place` works | `#[tokio::test(flavor = "multi_thread")]` | the default `#[tokio::test]` flavor, which panics |
| No known tokio or tokio-util advisory | `cargo deny --config deny.toml --locked check advisories` with `unsound = "all"`, or `cargo audit --deny warnings` | regressions that have no advisory |

No tool checks cancel safety. Review the `cancel-safe:` annotations, and test a cancel-sensitive
future by dropping it at each `.await` (race it in `select!` against a `oneshot` that fires at a
chosen step), then assert the state invariant.

Plain `cargo audit` exits 0 on an `unsound` advisory. Read
`references/runtime-and-foreign-threads.md` (section "Tokio advisories") before you set a tokio
version floor.

## Completion criteria

Before you call async work done or approve a merge, walk the checklist in
[references/cancellation-and-shutdown.md](references/cancellation-and-shutdown.md#completion-checklist).

## Cancellation

`select!` drops every other branch future when the first branch finishes, and the work in
progress inside a dropped branch is lost. `join!` waits for all branches. Every future in a
`select!` arm, in `timeout`, or in `FuturesUnordered` must therefore be cancel safe. A disabled
branch still evaluates its async expression, so keep side effects inside the async body. Read
[references/cancellation-and-shutdown.md](references/cancellation-and-shutdown.md) when you
annotate cancel safety, pick a library method for a `select!` arm, or protect a sequence of
`.await`s that must not be split.

### Put shutdown first with `biased`

```rust
loop {
    tokio::select! {
        biased;
        _ = cancel.cancelled() => break,  // always polled first
        Some(msg) = rx.recv() => process(msg),
    }
}
```

Without `biased`, the arms poll in random order, and the loop can run after cancellation. Under `biased;`, never put an always-ready data arm above the shutdown arm:
that order starves it. Give every long-lived `select!` loop a `cancelled()` arm unless another
arm ends the loop on shutdown. Otherwise shutdown hangs.

### CancellationToken tree

Use `tokio_util::sync::CancellationToken`, not `tokio::sync::Notify`. Give each task
`master.child_token()`, spawn it on a `TaskTracker`, and on shutdown call `master.cancel()`,
`tracker.close()`, and `tracker.wait().await`. `run_until_cancelled(fut)` drops the losing `fut`,
so `fut` must be cancel safe. Read
[references/cancellation-and-shutdown.md](references/cancellation-and-shutdown.md#cancellationtoken-idioms)
when you write the tree, a `drop_guard`, or a `run_until_cancelled` call.

## Task ownership and concurrency

Give every spawned task an owner: a `JoinSet` (keeps results; drain it with `join_next`), a
`TaskTracker` (keeps none; pair it with a `CancellationToken`), or a `FuturesUnordered` (no
spawn). Dropping a bare `JoinHandle` detaches its task: it is not cancelled, and its result or
panic is lost. Keep the handle, signal cancellation, and await it, also after `abort()`. Replace
a `for x in xs { tokio::spawn(work(x)); }` loop with one of those owners or with
`buffer_unordered(K)`. Give every long-lived task its own `tracing` span. Read
[references/cancellation-and-shutdown.md](references/cancellation-and-shutdown.md#task-sets-and-supervision)
when you choose an owner or bound a `buffer_unordered(K)` stream.

## Blocking work

Put bounded blocking or CPU work (target < 100 ms) in `spawn_blocking`, and an indefinite loop
on `std::thread::spawn`. Do not call `block_in_place` on a `current_thread` runtime: it panics.
Read [references/runtime-and-foreign-threads.md](references/runtime-and-foreign-threads.md#blocking-work)
when you choose a mechanism for many CPU-bound jobs, `rayon` work, or a synchronous client.

## Send, 'static, and async bounds

`tokio::spawn` requires `Send + 'static`. A value that lives across an `.await` becomes part of
the future, so one `!Send` value makes the whole future `!Send`. A `std::sync::MutexGuard` or a
`RefCell` borrow held across `.await` still compiles where the future need not be `Send` (the
root of `block_on` or `#[tokio::main]`, `spawn_local`), and deadlocks or panics under load. Copy
what you need, drop the guard, then `.await`; use `tokio::sync::Mutex` only when the lock must
span the `.await`. Move owned values or `Arc<T>` into a spawned task.

A native `async fn` in a trait spawns on a concrete type but fails through a generic
`T: Trait` bound with `error: future cannot be sent between threads safely` (no error code). Do
not emit return type notation (`T::m(..): Send`): it is nightly-only on Rust 1.99.1 (E0658 on
stable). Read [references/async-bounds.md](references/async-bounds.md) when you pick a callback
or trait shape for a future that crosses `tokio::spawn` or `dyn`, when a bound fails to compile,
before you migrate off `#[async_trait]`, when edition 2024 changes what an `impl Future` return
captures, or when concurrent futures need one `&mut State`.

## Timeouts

`tokio::time::timeout` cannot preempt one call to `Future::poll`, so
`timeout(d, async { cpu_work() })` does not bound `cpu_work`. Write
`timeout(d, spawn_blocking(work))`; it bounds only the wait, and the closure keeps running. When
the work must stop, pass a `CancellationToken` into it and cancel it on `Elapsed`. Read
[references/cancellation-and-shutdown.md](references/cancellation-and-shutdown.md#cooperative-cancellation-of-cpu-work)
when you write such a loop.

## Runtime setup and foreign threads

Build one runtime and share it from a `static OnceLock<Runtime>`. A foreign thread (JNI, a C
callback) enters through `block_on`, which polls on the calling thread, so `thread_stack_size`
does not size that stack. Under an `extern "C"` entry, wrap the `block_on` body in
`catch_unwind`: since Rust 1.81 a panic there aborts the process. A UniFFI async export that uses
Tokio resources needs `#[uniffi::export(async_runtime = "tokio")]`. Read
[references/runtime-and-foreign-threads.md](references/runtime-and-foreign-threads.md) when you
write the runtime initializer, pick a flavor, size a stack, or make a foreign thread wait for
async work.

## Manual polling from a synchronous loop

A synchronous, step-driven engine and waker-driven tokio tasks share no waker. The bridge is a
`poll_read` / `poll_write` call with `Context::from_waker(Waker::noop())` (Rust 1.85), made from
the loop tick. Never call such a helper from async code or wrap it in an `async fn`: under a
no-op waker, `Poll::Pending` gets no wake, and the task stalls for ever. Read
[references/manual-poll-bridge.md](references/manual-poll-bridge.md) when you write or extend the
helper or drive an io_uring backend from the loop.

## Related skills

Each applies when it is installed: `rust-pin-projection` (`Pin`, `Unpin`, projection),
`rust-send-sync` (why a type is `Send`), `rust-event-loop-state` (`&mut State` in a synchronous
loop), `rust-networking` and `rust-database` (cancellation at a network or transaction boundary),
`rust-debugging` (tokio-console), and `rust-test-tools` (loom, run with `RUSTFLAGS="--cfg loom"`).
