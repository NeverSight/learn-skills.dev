---
name: effect-ts-resources
description: Use when managing resource lifecycles (DB connections, file handles, sockets) where cleanup must be guaranteed despite failures, interruptions, or potential resource leaks.
version: 1.0.0
---

# Effect-TS Resource Management

## Overview
Manage resource lifecycles using `Scope` and `acquireRelease` to guarantee cleanup. Cleanup always runs, even if the program fails, throws, or is interrupted.

## When to Use
- **Symptoms**: Resource leaks (hanging connections), manual `try/finally` blocks, complex cleanup logic.
- **Triggers**: Opening files, connecting to databases, starting servers, acquiring locks.
- **When NOT to use**: For simple data transformations or values that don't require explicit closing/release.

## Core Pattern
Manual `try/finally` is error-prone in Effect because it bypasses interruption handling.

| Anti-Pattern (Manual) | Effect Pattern (Safe) |
| :--- | :--- |
| `try { conn.open() } finally { conn.close() }` | `Effect.acquireRelease(open, close)` |

## Quick Reference
| Function | Purpose |
| :--- | :--- |
| `Effect.acquireRelease` | Define acquisition and guaranteed release logic. |
| `Effect.scoped` | Create a boundary where all resources in scope are released. |
| `Effect.addFinalizer` | Add a cleanup action to the current scope. |

## Implementation

### 1. acquireRelease pattern
Guarantees cleanup even on failure or interruption.
```typescript
import { Effect } from 'effect';

const withDatabaseConnection = Effect.acquireRelease(
  Effect.tryPromise(() => pool.connect()), // Acquire
  (connection) => Effect.sync(() => connection.release()) // Release
);

const program = Effect.gen(function* () {
  const conn = yield* withDatabaseConnection;
  return yield* conn.query('SELECT * FROM users');
});
```

### 2. Scoped resources
Multiple resources share a lifecycle boundary. Resources are released in **LIFO** (Last-In, First-Out) order.
```typescript
import { Effect, Scope } from 'effect';

const program = Effect.scoped(
  Effect.gen(function* () {
    const db = yield* managedConnection;
    const cache = yield* managedCache;
    // Both cleaned up when scope closes (cache first, then db)
    return yield* doWork(db, cache);
  })
);
```

### 3. File handling
```typescript
const withFile = (path: string) => Effect.acquireRelease(
  Effect.tryPromise(() => fs.open(path, 'r')),
  (handle) => Effect.promise(() => handle.close())
);
```

## Common Mistakes
- **Using `try/finally`**: Bypasses Effect's interruption model. Use `acquireRelease`.
- **Forgetting `Effect.scoped`**: Resources won't be released until the parent scope closes (often the app end).
- **Wrong Order**: Resources are released in reverse order of acquisition. Ensure dependencies are acquired first.

**REQUIRED BACKGROUND:** Use effect-ts-fundamentals for core generator patterns.
