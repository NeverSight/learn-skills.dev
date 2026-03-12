---
name: safe-ts
description: Enforce "safe-ts" coding principles in TypeScript. Use when writing, reading, reviewing, or refactoring TypeScript code to ensure maximum safety, predictable execution, and zero technical debt.
---

# Safe TypeScript

Build highly predictable, robust, and performant TypeScript/Node.js applications with a "zero technical debt" policy.

## Retrieval-First Development

**Always verify standards against the reference documentation before implementing.**

| Resource | URL / Path |
|----------|------------|
| Safety & Control Flow | `./references/safety.md` |
| Performance Patterns | `./references/performance.md` |
| Developer Experience | `./references/dx.md` |

Review the relevant documentation when writing new logic or performing code reviews.

## When to Use

- Writing new TypeScript logic from scratch
- Refactoring existing TS/JS code to improve safety, performance, or memory stability
- Reviewing PRs for code quality and strict compiler standard adherence
- Optimizing memory allocations or V8 hot paths (e.g., GC pause mitigation)
- Implementing strict error handling without `throw` / `try-catch`

## Reference Documentation

- `./references/safety.md` - Control flow limits, bounded Promises, assertions, Result types
- `./references/performance.md` - Object pools, TypedArrays, monomorphic shapes
- `./references/dx.md` - Naming conventions, options structs, strict compiler flags, zero dependencies

Search: `no recursion`, `AbortSignal`, `ObjectPool`, `Result<T,E>`, `noUncheckedIndexedAccess`, `Zod`

## Core Principles

### Apply Safe TypeScript For

| Need | Example |
|------|---------|
| Predictable Execution | Bounded `for` loops, bounded `Promise`s via `AbortSignal.timeout()` |
| Memory Stability | Pre-allocating arrays/pools at startup, `Uint8Array`, in-place object mutation |
| Operational Reliability | Returning explicit `Result<T, E>` types, never throwing operational errors |
| Maintainability | Maximum 70 lines per function, max 100 columns per line, options interfaces |

### Do NOT Use

- Unbounded `while(true)` loops or `Promise`s without timeouts
- Dynamic memory allocations (`new Object()`, `[]`, `{}`) inside hot paths (triggers GC pauses)
- Unchecked array indices or implicit `any` types
- Expected control flow via `throw` and `catch` (Exceptions are for bugs/panics *only*)
- `Proxy`, `Reflect`, or runtime decorator magic

## Quick Reference

### Bounded Asynchronous Pattern (No Leaked Promises)

```typescript
// Always bound asynchronous operations with a timeout
async function fetchWithBounds(url: string, timeoutMs: number): Promise<Result<Response, Error>> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(new Error("Timeout")), timeoutMs);
    
    try {
        const res = await fetch(url, { signal: controller.signal });
        if (!res.ok) return { ok: false, error: new Error(`HTTP ${res.status}`) };
        return { ok: true, value: res };
    } catch (err) {
        // Only catch native exceptions/abort errors to wrap them into Results
        return { ok: false, error: err instanceof Error ? err : new Error(String(err)) };
    } finally {
        clearTimeout(timeoutId);
    }
}
```

### Allocation-Free Hot Path (Object Pooling)

```typescript
// Pre-allocate at startup to avoid GC pauses during execution
class BufferPool {
    private pool: Uint8Array[];
    
    constructor(size: number, bufferSize: number) {
        this.pool = Array.from({ length: size }, () => new Uint8Array(bufferSize));
    }
    
    acquire(): Uint8Array | null {
        return this.pool.pop() || null;
    }
    
    release(buf: Uint8Array): void {
        // Reset state before returning to pool
        buf.fill(0);
        this.pool.push(buf);
    }
}

const pool = new BufferPool(100, 1024);

function processData(target: Uint8Array): Result<void, Error> {
    // Acquire from pool instead of `new Uint8Array(1024)`
    const buf = pool.acquire();
    if (!buf) return { ok: false, error: new Error("Pool exhausted") };

    try {
        // ... mutate target or buf in-place
        return { ok: true, value: undefined };
    } finally {
        pool.release(buf);
    }
}
```

### Result Types over Exceptions

```typescript
// Define explicit union returns instead of throwing
type Result<T, E = Error> = 
  | { ok: true; value: T }
  | { ok: false; error: E };

function parseData(input: string): Result<ParsedData, ValidationError> {
    if (!input) return { ok: false, error: new ValidationError("Empty input") };
    
    // ...
    return { ok: true, value: data };
}
```

## Critical Rules

1. **No Recursion** - Keep control flow simple and execution bounds completely static.
2. **Fixed Upper Bounds** - All loops, arrays, and Promises must be bounded (e.g., by size or timeouts).
3. **No Dynamic Memory After Init** - Allocate all significant memory (Object Pools/Arrays) at startup.
4. **Short Functions** - Hard limit of 70 lines per function. Push `if`s up, push `for`s down.
5. **Check All Returns** - Never ignore the result of a `Result<T, E>` or a `Promise`. Await everything.
6. **Explicit Panics Only** - `throw` *only* for programmer errors/broken invariants (like assertion failures). Use standard explicit `Result` returns for operational issues.
7. **Strict Compilation** - Must use `strict: true`, `noUncheckedIndexedAccess: true`, and `noImplicitReturns: true`.
8. **Options Interfaces** - Use explicit options interfaces for configuration instead of multiple boolean/primitive arguments.
9. **Zero Dependencies** - Strictly avoid third-party NPM dependencies outside standard library tools or extensively vetted utilities (like `zod`).
10. **Strict Naming** - Add units or qualifiers at the end of variables (e.g., `timeoutMs`, `latencyMaxMs`).

## Anti-Patterns (NEVER)

- Using `any` or explicit type assertions (`as Type`) to bypass the compiler
- Throwing exceptions for expected business logic errors (e.g., `throw new Error("Invalid User")`)
- Using unbounded `while(true)` loops or `new Promise(() => {})` without a reject mechanism
- Accessing arrays without verifying the index exists (requires `noUncheckedIndexedAccess`)
- Returning implicitly or ignoring awaited variables (`void myAsyncFunc()`)
- Magic metaprogramming (`Proxy`, `Reflect`, dynamically adding/deleting object properties `delete obj.prop`)

## Credits

- [TIGER_STYLE.md](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/TIGER_STYLE.md)
