---
name: sota-async-concurrency
description: >-
  State-of-the-art rules for writing and auditing asynchronous and concurrent
  code across runtimes (Python asyncio, JS/Node, Go, Rust, JVM). Use when
  building anything with async/await, threads, processes, event loops, task
  groups, channels, or queues — and when auditing existing code for race
  conditions, deadlocks, leaked tasks, blocked event loops, missing
  cancellation, or backpressure failures. Not for latency/throughput profiling
  and optimization — use sota-performance. Trigger keywords: async, await,
  concurrency, parallelism, threads, race condition, deadlock, event loop,
  channels, queues, semaphore, mutex, cancellation, timeout, backpressure,
  task group, goroutine, tokio, asyncio.
---

# SOTA Async & Concurrency

## Purpose

Concurrency bugs are the most expensive class of defect: they pass tests, ship,
and then corrupt data or hang production under load. This skill encodes the
2026 state of the art for concurrent design and the bug catalog auditors need
to spot defects **by reading code**, without reproducing them. Concepts are
cross-language; per-runtime notes are inlined where semantics genuinely differ
(GIL, goroutine scheduling, tokio executors, Node's single loop).

Two operating modes. Pick one explicitly before starting.

## BUILD mode

When writing new concurrent code:

1. **Classify the workload first.** I/O-bound → async/event loop. CPU-bound →
   threads (if runtime has real parallelism) or processes. Mixed → async
   front-end + bounded worker pool. Read [`rules/01`](rules/01-models-and-structure.md) before choosing; on an event
   loop, keep blocking and CPU work off it ([`rules/04`](rules/04-event-loop-hygiene.md)).
2. **Structured concurrency is the default.** Every task lives inside a scope
   (TaskGroup / nursery / errgroup / JoinSet) that joins or cancels it.
   Spawning a task with no owner is a design smell requiring written
   justification.
3. **Bound everything.** Every queue, channel, connection pool, in-flight
   request set, and spawn loop gets an explicit capacity. Unbounded = OOM with
   a delay timer.
4. **Every await gets a timeout policy** — a number, or a documented reason
   why it inherits one from an enclosing scope ([`rules/05`](rules/05-cancellation-timeouts-shutdown.md)).
5. **Cancellation is a feature you build, not an exception you ignore.**
   Propagate context/AbortSignal/CancelledError; clean up in finally blocks;
   design shutdown order (stop intake → drain → deadline → force) ([`rules/05`](rules/05-cancellation-timeouts-shutdown.md)).
6. **Shared mutable state needs an owner.** Prefer message passing or
   single-owner tasks; if you must lock, define lock ordering and never hold a
   lock across an await. Races vs race conditions, atomicity and TOCTOU: [`rules/02`](rules/02-correctness.md);
   choosing the primitive: [`rules/03`](rules/03-primitives.md). Ambient per-request context
   (tenant, user) is reset when the request ends, or a reused worker serves the next request
   with it: [`rules/07`](rules/07-audit-bug-catalog.md) §3.
7. Re-read the audit checklists at the end of each rules file against your own
   diff before declaring done.

## AUDIT mode

**Coverage:** every `rules/` file's Audit checklist applies in AUDIT mode. Mark one *not applicable* only with its reason in the report — never skip a file because the thing it checks for is absent, since that absence may be the finding.

When auditing existing code, you find races, deadlocks, and leaks by reading —
grep is your debugger. Workflow:

1. **Map the concurrency topology.** What spawns tasks/threads? What shares
   state? What are the queues and their bounds? Draw the lock set and the
   channel graph mentally before judging any line.
2. **Sweep with targeted greps**, then read each hit in context:
   - Fire-and-forget: `create_task(` / `ensure_future(` without a stored
     handle; bare `go func(`; `.then(` with no `.catch(`; floating promises;
     `tokio::spawn` whose JoinHandle is dropped.
   - Missing await: async calls whose return value is discarded.
   - Blocking in async: `time.sleep`, `requests.`, `open(` , sync DB drivers,
     `fs.readFileSync`, `bcrypt.hashSync`, `std::thread::sleep` inside async fns.
   - Lock across await: `async with lock:` / `mutex.lock()` bodies containing
     `await` / `.await`.
   - Unbounded: `Queue()` with no maxsize, `make(chan T)` fed by fast
     producers, `unbounded_channel`, spawn-in-loop with no semaphore.
   - Check-then-act: `if x in d:` … `d[x]`, exists-then-create, read-modify-write
     on shared counters without atomics/locks.
3. **For each suspect, prove the interleaving.** State the two (or more)
   execution orders and which one breaks. A finding without an interleaving is
   a style note, not a concurrency bug.
4. Read [`rules/07`](rules/07-audit-bug-catalog.md) for the full bug catalog with signatures.

### Severity conventions

| Severity | Criteria | Examples |
|---|---|---|
| CRITICAL | Data corruption, deadlock, or unbounded resource growth reachable under normal load | Lost-update race on money/state; lock-ordering deadlock on hot path; unbounded queue fed by network input |
| HIGH | Hang, leak, or wrong result under plausible (load/error/timeout) conditions | Fire-and-forget swallowing exceptions; no timeout on external call; lock held across await; blocking call on event loop |
| MEDIUM | Degraded behavior, starvation, or fragility under contention | Writer starvation on RwLock; missing jitter on retries; thundering herd on cache expiry; spurious-wakeup-unsafe condvar wait |
| LOW | Latent hazard or convention violation with no current trigger | Orphanable task that today happens to finish first; missing cancellation propagation in a path that is never cancelled yet |

Escalate one level when the affected state is money, auth, or durability.

### Finding format

```
[SEVERITY] file:line — short title
Race window / failure mode: the exact interleaving or condition (T1 does X,
  T2 does Y between X and Z → consequence).
Trigger likelihood: what load/error pattern makes it fire.
Fix: concrete minimal change (primitive, bound, timeout value, scope).
```

## Rules index

| File | Read this when... |
|---|---|
| [`rules/01-models-and-structure.md`](rules/01-models-and-structure.md) | Choosing event loop vs threads vs processes vs actors; CPU/I-O decision tree; structured concurrency, task groups, no orphaned tasks |
| [`rules/02-correctness.md`](rules/02-correctness.md) | Reasoning about data races vs race conditions, atomicity, memory ordering/visibility, TOCTOU, deadlock prevention, livelock, starvation, idempotency under retries |
| [`rules/03-primitives.md`](rules/03-primitives.md) | Picking or reviewing mutexes, RwLocks, semaphores, condition variables, channels (bounded vs unbounded), select/race, once/lazy init |
| [`rules/04-event-loop-hygiene.md`](rules/04-event-loop-hygiene.md) | Anything runs on an event loop: blocking calls, CPU work, offloading to pools, long-task chunking, microtask vs macrotask |
| [`rules/05-cancellation-timeouts-shutdown.md`](rules/05-cancellation-timeouts-shutdown.md) | Timeout policy, propagating cancellation (context/AbortSignal/CancelledError), cleanup on cancel, graceful shutdown sequencing, retry interplay (cancellable backoff) |
| [`rules/06-backpressure-flow-control.md`](rules/06-backpressure-flow-control.md) | Queues between components, producer/consumer rate mismatch, load shedding, token buckets, pull-based streaming |
| [`rules/07-audit-bug-catalog.md`](rules/07-audit-bug-catalog.md) | AUDIT mode: the signature, severity, and fix for every common async bug — fire-and-forget, missing await, lock-across-await, retry storms, thundering herd, unbounded spawns, ambient per-request context (tenant, user) not reset |

## Per-language detail

This skill holds the cross-runtime model. Each language skill carries its runtime's half — its primitives, its executor, its leak and deadlock shapes — in one file. Read it beside this one whenever the code is in that language:

| Language | File |
|---|---|
| Python | [`sota-python` rules/04](../sota-python/rules/04-async.md) |
| Go | [`sota-golang` rules/03](../sota-golang/rules/03-concurrency.md) |
| Rust | [`sota-rust` rules/04](../sota-rust/rules/04-async-tokio.md) |
| C / C++ | [`sota-c-cpp` rules/05](../sota-c-cpp/rules/05-concurrency.md) |
| Java / Kotlin | [`sota-jvm` rules/03](../sota-jvm/rules/03-concurrency.md) |
| C# / .NET | [`sota-dotnet` rules/03](../sota-dotnet/rules/03-async-concurrency.md) |
| JavaScript / TypeScript | [`sota-javascript-typescript` rules/03](../sota-javascript-typescript/rules/03-async-patterns.md) |
| PHP | [`sota-php` rules/01](../sota-php/rules/01-language-baseline.md) §6 (fibers; worker mode is [rules/06](../sota-php/rules/06-performance-runtime.md) §4a) |
| Ruby | [`sota-ruby` rules/05](../sota-ruby/rules/05-concurrency-performance.md) |
| Swift | [`sota-swift` rules/03](../sota-swift/rules/03-concurrency.md) |

## Top 10 non-negotiables

1. **No orphaned tasks.** Every spawned task has an owner that awaits/joins it
   or cancels it on scope exit. Fire-and-forget requires an error handler and a
   written reason.
2. **No unbounded queues or channels.** An unbounded queue is a memory leak
   with extra steps. Choose a capacity and a full-policy (block, drop, shed).
3. **Never block the event loop.** No sync I/O, sync crypto, or CPU loops on
   the loop thread — offload to a worker pool.
4. **Never hold a *blocking* lock across an await point.** It serializes the system at
   best and deadlocks it at worst. The **stated exception**: when exclusive access genuinely
   must span an await — a protocol exchange on one connection, say — use the runtime's
   *async-aware* mutex (`tokio::sync::Mutex`, `asyncio.Lock`) and accept the serialization
   you are buying. [`sota-rust` rules/04](../sota-rust/rules/04-async-tokio.md) prescribes exactly that case; without this exception
   the two skills contradict each other on the same code.
5. **Every await has a timeout policy.** External calls get explicit deadlines;
   internal ones inherit a scope deadline. "Forever" is a decision, not a
   default.
6. **No check-then-act on shared state.** Make the check and the act atomic:
   one lock region, an atomic primitive, or a DB constraint/UPSERT.
7. **Acquire locks in one global order**, and never call unknown/user code
   while holding a lock.
8. **Cancellation propagates and cleans up.** Catch-and-rethrow CancelledError;
   pass context/AbortSignal down every call chain that can block.
9. **Retries are bounded, jittered, and idempotent.** Exponential backoff +
   full jitter + retry budget; never retry a non-idempotent operation without a
   dedupe key.
10. **Condition-variable waits loop on the predicate** (`while not pred:
    wait()`), and shutdown follows the sequence: stop accepting → drain with
    deadline → cancel stragglers → release resources.
