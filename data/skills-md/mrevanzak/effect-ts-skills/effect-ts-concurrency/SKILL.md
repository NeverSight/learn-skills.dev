---
name: effect-ts-concurrency
description: Use when performing parallel operations, rate limiting, or signaling between fibers in Effect-TS.
version: 1.0.0
---

# Effect-TS Concurrency

## Overview
Effect-TS provides lightweight fibers for high-performance concurrency. The core principle is **explicit control**: always bound parallelism to prevent resource exhaustion.

## When to Use
- Processing large arrays of effects (e.g., `Effect.all`, `Effect.forEach`)
- Rate limiting external API calls or database connections
- Coordinating work between background processes (fibers)
- Signaling completion or state changes across different parts of the app

**When NOT to use:**
- Simple sequential operations
- When standard `Promise.all` is sufficient (though Effect is usually preferred for consistency)

## Core Pattern: Bounded Parallelism
Unbounded parallelism is the most common source of "Too many open files" or "Connection timeout" errors.

| Pattern | Implementation | Result |
|---------|----------------|--------|
| **BAD** | `Effect.all(effects)` | Unbounded - crashes on large inputs |
| **GOOD** | `Effect.all(effects, { concurrency: 10 })` | Bounded - safe and predictable |

## Quick Reference
| Tool | Purpose | Key Method |
|------|---------|------------|
| **Fiber** | Background execution | `Effect.fork` / `Fiber.join` |
| **Semaphore** | Bounded concurrency / Rate limiting | `semaphore.withPermits(n)` |
| **Deferred** | One-shot signaling / Promises | `Deferred.await` / `Deferred.succeed` |
| **concurrency** | Option for `all`, `forEach`, `mapEffect` | `{ concurrency: number | 'unbounded' }` |

## Implementation

### 1. Bounded Parallelism (Critical)
Always specify concurrency when processing collections.

```typescript
import { Effect } from 'effect';

// Process 1000 items, max 10 concurrent
const results = yield* Effect.all(
  items.map(processItem),
  { concurrency: 10 }
);
```

### 2. Semaphore for Rate Limiting
Use a Semaphore when multiple independent operations must share a global limit.

```typescript
import { Effect } from 'effect';

const program = Effect.gen(function* () {
  const semaphore = yield* Effect.makeSemaphore(5); // Max 5 concurrent
  
  yield* Effect.all(
    requests.map((req) => 
      semaphore.withPermits(1)(handleRequest(req))
    ),
    { concurrency: 'unbounded' } // Semaphore controls actual concurrency
  );
});
```

### 3. Deferred for Signaling
Use Deferred to wait for a specific event or value from another fiber.

```typescript
import { Deferred, Effect, Fiber } from 'effect';

const program = Effect.gen(function* () {
  const signal = yield* Deferred.make<void>();
  
  const worker = yield* Effect.fork(
    Effect.gen(function* () {
      yield* Deferred.await(signal); // Wait for signal
      yield* doWork();
    })
  );
  
  yield* setup();
  yield* Deferred.succeed(signal, undefined); // Trigger worker
  yield* Fiber.join(worker);
});
```

## Common Mistakes
- **Unbounded parallelism:** Forgetting `{ concurrency: n }` in `Effect.all`.
- **Leaking Fibers:** Forking fibers without joining or interrupting them (use `Effect.scoped` for safety).
- **Deadlocks:** Circular dependencies between semaphores or deferreds.

## Red Flags - STOP and Start Over
- Using `Effect.all` on a large array without `{ concurrency: n }`.
- Using `Promise.all` inside an Effect-TS codebase.
- Manual `setTimeout` for rate limiting instead of `Effect.makeRateLimiter` or `Semaphore`.

## Rationalization Table
| Excuse | Reality |
|--------|---------|
| "It's only 100 items" | 100 items today, 10,000 tomorrow. Bound it now. |
| "The API is fast" | Network latency and server load are unpredictable. |
| "I'll add concurrency later" | Unbounded parallelism is a ticking time bomb. |

**REQUIRED BACKGROUND:** See effect-ts-anti-patterns for more on unbounded parallelism.
