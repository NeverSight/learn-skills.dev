---
name: effect-ts-errors
description: Use when implementing error handling, validation logic, or custom error types in Effect-TS.
version: 1.0.0
---

# Effect-TS Error Handling

## Overview
Effect-TS provides a type-safe error channel (`E` in `Effect<A, E, R>`) that tracks potential failures. Use Tagged Errors for distinguishability and specialized combinators for handling or accumulating errors.

## When to Use
- Defining custom error types for domain logic.
- Handling specific errors without catching everything.
- Validating multiple fields and collecting all failures.

**When NOT to use:**
- Simple `try/catch` for non-Effect code.
- When error types don't need to be distinguished (use `Effect.fail(message)`).

## Core Pattern
**Before (Generic Errors):**
```typescript
if (!user) throw new Error("Not found");
```

**After (Tagged Errors):**
```typescript
if (!user) return yield* new UserNotFoundError({ userId: id });
```

## Quick Reference
| Feature | Method | Purpose |
|---------|--------|---------|
| Define Error | `Data.TaggedError` | Create distinguishable, typed errors. |
| Catch One | `Effect.catchTag` | Handle a specific tagged error by its `_tag`. |
| Catch All | `Effect.catchAll` | Handle all errors in the channel. |
| Accumulate | `Effect.all(..., { mode: 'either' })` | Collect multiple results/errors into `Either[]`. |

## Implementation

### 1. Tagged Errors
```typescript
import { Data, Effect } from 'effect';

export class UserNotFoundError extends Data.TaggedError('UserNotFoundError')<{
  userId: string;
}> {}

export class DatabaseError extends Data.TaggedError('DatabaseError')<{
  message: string;
}> {}

const getUser = (id: string): Effect.Effect<User, UserNotFoundError | DatabaseError> =>
  Effect.gen(function* () {
    const result = yield* queryDatabase(id);
    if (!result) return yield* new UserNotFoundError({ userId: id });
    return result;
  });
```

### 2. Catching Specific Errors
```typescript
const handled = getUser(id).pipe(
  // catchTag only works on objects with a _tag property
  Effect.catchTag('UserNotFoundError', (e) => 
    Effect.succeed({ id: e.userId, name: 'Guest' })
  )
);
// Result: Effect<User, DatabaseError>
```

### 3. Error Accumulation
```typescript
import { Either, Effect } from 'effect';

const validateAll = (data: Input) =>
  Effect.gen(function* () {
    const results = yield* Effect.all([
      validateEmail(data.email),
      validateAge(data.age)
    ], { mode: 'either' });
    
    const errors = results.filter(Either.isLeft).map(e => e.left);
    if (errors.length > 0) return yield* Effect.fail(errors);
    return results.map(e => (e as Either.Right<any, any>).right);
  });
```

## Common Mistakes
- **Using `throw`**: Breaks the error channel. Always use `Effect.fail` or `yield* new TaggedError()`.
- **Generic `catchAll`**: Swallows errors you didn't intend to handle. Prefer `catchTag`.
- **Short-circuiting**: `Effect.all` stops at the first error by default. Use `{ mode: 'either' }` or `{ mode: 'validate' }` for accumulation.

**REQUIRED BACKGROUND:** Use effect-ts-fundamentals for core concepts.
