---
name: typescript:effect-ts
description: Type-safe functional effects with Effect-TS. Use when building applications with Effect, using Effect.gen generators, handling typed errors, managing services with Layer and Context.Tag, validating data with Schema, or managing resources with acquireRelease.
user-invocable: false
---

# Effect-TS

Effect is a powerful TypeScript library for building robust, type-safe applications. It provides a functional effect system with typed errors, dependency injection, resource management, and concurrency primitives.

## Why Effect?

**Type-safe errors**: Unlike Promise which loses error type information, Effect tracks errors in the type system with `Effect<Success, Error, Requirements>`.

**Dependency injection**: Services are declared explicitly using `Context.Tag` and provided via `Layer`, making dependencies visible in types.

**Resource safety**: `Effect.acquireRelease` ensures resources are always cleaned up, even on failure or interruption.

**Composability**: Effects compose naturally with `pipe`, `Effect.gen` generators, and combinators like `Effect.all`, `Effect.flatMap`.

## Quick Reference

For detailed patterns and examples, see:
- [Core Concepts](./references/core.md) - Effect type, creating and running effects, generators
- [Error Handling](./references/error-handling.md) - Typed errors, catchAll, catchTag, Either
- [Services & Layers](./references/services.md) - Dependency injection with Context.Tag and Layer
- [Schema](./references/schema.md) - Data validation with encode/decode
- [Resources](./references/resources.md) - Resource management with acquireRelease and Scope

## The Effect Type

The core type `Effect<Success, Error, Requirements>` represents a computation that:
- Produces a value of type `Success` on success
- May fail with an error of type `Error`
- Requires a context of type `Requirements` to run

```typescript
import { Effect } from "effect"

// Effect<number, never, never> - succeeds with number, cannot fail, no requirements
const succeed = Effect.succeed(42)

// Effect<never, string, never> - always fails with string error
const fail = Effect.fail("Something went wrong")

// Effect<string, Error, never> - may succeed with string or fail with Error
const parse = (input: string): Effect.Effect<number, Error> =>
  Effect.try({
    try: () => JSON.parse(input),
    catch: (e) => new Error(`Parse failed: ${e}`)
  })
```

## Creating Effects

```typescript
import { Effect } from "effect"

// From synchronous values
const fromValue = Effect.succeed(42)
const fromThunk = Effect.sync(() => Date.now())

// From failures
const fromError = Effect.fail(new Error("Failed"))
const fromDie = Effect.die("Unexpected error") // Defect, not typed

// From async operations
const fromPromise = Effect.tryPromise({
  try: () => fetch("/api/data").then(r => r.json()),
  catch: (e) => new Error(`Fetch failed: ${e}`)
})

// From nullable values
const fromNullable = Effect.fromNullable(maybeValue)
```

## Running Effects

```typescript
import { Effect } from "effect"

const program = Effect.succeed(42)

// Synchronous (throws if effect is async or fails)
const result = Effect.runSync(program) // 42

// Promise-based
const promise = Effect.runPromise(program) // Promise<42>

// With exit status
const exit = Effect.runSyncExit(program)
const exitPromise = Effect.runPromiseExit(program)
```

## Effect.gen Generators

Write async-looking code with full type safety using generators:

```typescript
import { Effect } from "effect"

const program = Effect.gen(function* () {
  const user = yield* fetchUser(userId)
  const posts = yield* fetchPosts(user.id)
  const enriched = yield* enrichPosts(posts)
  return { user, posts: enriched }
})

// Equivalent to:
const programPipe = fetchUser(userId).pipe(
  Effect.flatMap(user =>
    fetchPosts(user.id).pipe(
      Effect.flatMap(posts =>
        enrichPosts(posts).pipe(
          Effect.map(enriched => ({ user, posts: enriched }))
        )
      )
    )
  )
)
```

## Error Handling

Effect tracks errors in the type system, making error handling explicit:

```typescript
import { Effect } from "effect"

class UserNotFound extends Error {
  readonly _tag = "UserNotFound"
  constructor(readonly userId: string) {
    super(`User not found: ${userId}`)
  }
}

class DatabaseError extends Error {
  readonly _tag = "DatabaseError"
  constructor(readonly cause: unknown) {
    super("Database error")
  }
}

// Effect<User, UserNotFound | DatabaseError, never>
const getUser = (id: string) => Effect.gen(function* () {
  const record = yield* queryDatabase(id)
  if (!record) {
    return yield* Effect.fail(new UserNotFound(id))
  }
  return record
})

// Handle specific errors
const handled = getUser("123").pipe(
  Effect.catchTag("UserNotFound", (e) =>
    Effect.succeed({ id: e.userId, name: "Anonymous" })
  )
)

// Handle all errors
const recovered = getUser("123").pipe(
  Effect.catchAll((error) =>
    Effect.succeed({ id: "unknown", name: "Fallback" })
  )
)
```

## Services and Dependency Injection

Define services with `Context.Tag` and provide them with `Layer`:

```typescript
import { Context, Effect, Layer } from "effect"

// Define a service interface and tag
class Database extends Context.Tag("Database")<
  Database,
  {
    readonly query: (sql: string) => Effect.Effect<unknown[]>
    readonly execute: (sql: string) => Effect.Effect<void>
  }
>() {}

// Use the service in effects
const getUsers = Effect.gen(function* () {
  const db = yield* Database
  return yield* db.query("SELECT * FROM users")
})

// Create a layer that provides the service
const DatabaseLive = Layer.succeed(Database, {
  query: (sql) => Effect.sync(() => {
    console.log(`Executing: ${sql}`)
    return []
  }),
  execute: (sql) => Effect.sync(() => {
    console.log(`Executing: ${sql}`)
  })
})

// Provide the layer to run the effect
const runnable = Effect.provide(getUsers, DatabaseLive)
Effect.runPromise(runnable)
```

## Schema Validation

Use Effect Schema for type-safe data validation:

```typescript
import { Schema } from "effect"

// Define a schema
const User = Schema.Struct({
  id: Schema.String,
  name: Schema.String,
  email: Schema.String,
  age: Schema.Number
})

// Infer types from schema
type User = Schema.Schema.Type<typeof User>

// Decode unknown data
const decoded = Schema.decodeUnknownSync(User)({
  id: "123",
  name: "Alice",
  email: "alice@example.com",
  age: 30
})

// Decode with Effect (for better error handling)
const decodeEffect = Schema.decodeUnknown(User)
const result = decodeEffect({ id: "123", name: "Alice", email: "a@b.com", age: 30 })
// Effect<User, ParseError, never>
```

## Resource Management

Safely manage resources that need cleanup:

```typescript
import { Effect, Scope } from "effect"

// Define a resource with acquisition and release
const withConnection = Effect.acquireRelease(
  // Acquire
  Effect.sync(() => {
    console.log("Opening connection")
    return { query: (sql: string) => sql }
  }),
  // Release
  (conn) => Effect.sync(() => {
    console.log("Closing connection")
  })
)

// Use the resource in a scoped effect
const program = Effect.scoped(
  Effect.gen(function* () {
    const conn = yield* withConnection
    return conn.query("SELECT * FROM users")
  })
)

// Connection is automatically closed after use
Effect.runPromise(program)
```

## Common Patterns

### Sequential vs Parallel Execution

```typescript
import { Effect } from "effect"

const tasks = [task1, task2, task3]

// Sequential execution
const sequential = Effect.all(tasks, { concurrency: 1 })

// Parallel execution (all at once)
const parallel = Effect.all(tasks, { concurrency: "unbounded" })

// Parallel with limit
const limited = Effect.all(tasks, { concurrency: 5 })
```

### Retry with Backoff

```typescript
import { Effect, Schedule } from "effect"

const retried = fetchData.pipe(
  Effect.retry(
    Schedule.exponential("100 millis").pipe(
      Schedule.jittered,
      Schedule.compose(Schedule.recurs(5))
    )
  )
)
```

### Timeouts

```typescript
import { Effect, Duration } from "effect"

const withTimeout = longRunningTask.pipe(
  Effect.timeout(Duration.seconds(30))
)
```

## Guidelines

1. **Use `Effect.gen` for complex flows** - Generators make sequential operations readable
2. **Tag errors with `_tag`** - Enables `catchTag` for precise error handling
3. **Define services with `Context.Tag`** - Makes dependencies explicit and testable
4. **Use `Layer` for service composition** - Layers compose and manage lifecycle
5. **Prefer `Effect.try` over manual try/catch** - Keeps errors in the Effect channel
6. **Use Schema for external data** - Validates and transforms API/DB data
7. **Scope resources with `acquireRelease`** - Guarantees cleanup on success or failure
8. **Run effects at the edge** - Keep `runPromise`/`runSync` at application boundaries

## Integration with Other Skills

Effect-TS integrates well with:
- [Functional Patterns](../functional-patterns/SKILL.md) - Effect builds on Option/Either concepts
- [Drizzle ORM](../drizzle-orm/SKILL.md) - Wrap Drizzle queries in Effect for typed errors
- [Fastify](../fastify/SKILL.md) - Use Effect for request handling with typed errors

## When This Skill Loads

This skill automatically loads when discussing:
- Effect-TS library usage
- Typed error handling in TypeScript
- Dependency injection with Context and Layer
- Effect.gen generators
- Schema validation with Effect
- Resource management and Scope
- Functional effect systems
