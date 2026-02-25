---
name: effective-effect
description: Enforces Effect-TS patterns for services, errors, layers, and atoms. Use when writing code with Context.Tag, Schema.TaggedError, Layer composition, or effect-atom React components.
version: 3.0.2
---

# Effect-TS Best Practices

This skill enforces opinionated, consistent patterns for Effect-TS codebases. These patterns optimize for type safety, testability, observability, and maintainability.

## Core Principles

### Effect Type Signature

```
Effect<Success, Error, Requirements>
//      ↑        ↑       ↑
//      |        |       └── Dependencies (provided via Layers)
//      |        └── Expected errors (typed, must be handled)
//      └── Success value
```

### Prefer Explicit Over Generic Errors

**Every distinct failure reason deserves its own error type.** Don't collapse multiple failure modes into generic HTTP errors like `NotFoundError` or `BadRequestError`.

```typescript
// BAD - Generic errors lose context
class NotFoundError extends Schema.TaggedError<NotFoundError>()("NotFoundError", {
  message: Schema.String, // Dont use `message` as it may hide context when using Effect.log
}) {}

// GOOD - Specific errors enable precise handling
class UserNotFoundError extends Schema.TaggedError<UserNotFoundError>()("UserNotFoundError", {
  userId: UserId,
  userMessage: Schema.String,
}) {}

class SessionExpiredError extends Schema.TaggedError<SessionExpiredError>()("SessionExpiredError", {
  expiredAt: Schema.Date,
  userMessage: Schema.String,
}) {}

// GOOD - Wrapping errors with cause preserves stack traces
class UserLookupError extends Schema.TaggedError<UserLookupError>()("UserLookupError", {
  userId: UserId,
  reason: Schema.String, // prefer using `reason` over `message` for logging
  cause: Schema.Defect, // Wraps the underlying error - Effect.log prints as stack trace
}) {}
```

**Benefits:**

- `UserNotFoundError` with `userId` → Frontend shows "User doesn't exist"
- `SessionExpiredError` with `expiredAt` → Frontend shows "Session expired, please log in"
- Type-safe error handling with `catchTag`/`catchTags`
- Not using the `message` field allows `Effect.log` to log all error context values. This way we will see both the `expiredAt` and `userMessage` fields in the logs, if we log the error.
- Using a `cause` field of type `Schema.Defect` preserves the original stack trace when logging the error.

## Quick Reference: Critical Rules

| Category       | DO                                            | DON'T                                   |
| -------------- | --------------------------------------------- | --------------------------------------- |
| Services (app) | `Effect.Service` with default implementation  | Inline dependencies in methods          |
| Services (lib) | `Context.Tag` when no sensible default exists | Assuming implementation in library code |
| Dependencies   | `dependencies: [...]` or yield in Layer       | Pass services as function parameters    |
| Errors         | `Schema.TaggedError` (yieldable)              | Plain classes or generic Error          |
| Error Recovery | `catchTag`/`catchTags` with pattern matching  | `catchAll` losing type info             |
| IDs            | `Schema.String.pipe(Schema.brand("UserId"))`  | Plain `string` for entity IDs           |
| Functions      | `Effect.fn("Service.method")`                 | Anonymous generators                    |
| Sequencing     | `Effect.gen` with `yield*`                    | Nested `.then()` or `.pipe()` chains    |
| Logging        | `Effect.log` with structured data             | `console.log`                           |
| Config         | `Schema.Config` or `Config.*` primitives      | `process.env` directly                  |
| Options        | `Option.match` with both cases                | `Option.getOrThrow`                     |
| Nullability    | `Option<T>` in domain types                   | `null`/`undefined`                      |
| Test Layers    | `Layer.sync` with in-memory state             | Mocking frameworks                      |
| Atoms          | `Atom.make` outside components                | Creating atoms inside render            |
| Atom Results   | `Result.builder` with `onErrorTag`            | Ignoring loading/error states           |

## Basics

### Effect.gen

Just as `async/await` provides a sequential, readable way to work with `Promise` values, `Effect.gen` and `yield*` provide the same ergonomic benefits for `Effect` values:

```typescript
import { Effect } from "effect";

const program = Effect.gen(function* () {
  const data = yield* fetchData;
  yield* Effect.logInfo(`Processing data: ${data}`);
  return yield* processData(data);
});
```

### Effect.fn

Use `Effect.fn` with generator functions for traced, named effects. `Effect.fn` traces where the function is called from, not just where it's defined:

```typescript
import { Effect } from "effect";

const processUser = Effect.fn("processUser")(function* (userId: string) {
  yield* Effect.logInfo(`Processing user ${userId}`);
  const user = yield* getUser(userId);
  return yield* processData(user);
});
```

**Benefits:**

- Call-site tracing for each invocation
- Stack traces with location details
- Clean signatures
- Automatic spans for telemetry

### Pipe for Instrumentation

Use `.pipe()` to add cross-cutting concerns to Effect values:

```typescript
import { Effect, Schedule } from "effect";

const program = fetchData.pipe(
  Effect.timeout("5 seconds"),
  Effect.retry(Schedule.exponential("100 millis").pipe(Schedule.compose(Schedule.recurs(3)))),
  Effect.tap((data) => Effect.logInfo(`Fetched: ${data}`)),
  Effect.withSpan("fetchData"),
);
```

**Common instrumentation:**

- `Effect.timeout` - fail if effect takes too long
- `Effect.retry` - retry on failure with a schedule
- `Effect.tap` - run side effect without changing the value
- `Effect.withSpan` - add tracing span

## Service Definition Pattern

Effect provides two ways to model services: `Effect.Service` and `Context.Tag`. Choose based on your use case:

| Feature      | Effect.Service                             | Context.Tag                               |
| ------------ | ------------------------------------------ | ----------------------------------------- |
| Best for     | Application code with clear implementation | Library code or dynamically-scoped values |
| Default impl | Required (becomes `.Default` layer)        | Optional - supplied later                 |
| Boilerplate  | Less - tag + layer generated               | More - build layers yourself              |

### Effect.Service (Preferred for App Code)

Use `Effect.Service` when you have a sensible default implementation:

```typescript
import { Effect } from "effect";

export class UserService extends Effect.Service<UserService>()("@app/UserService", {
  accessors: true,
  dependencies: [UserRepo.Default, CacheService.Default],
  effect: Effect.gen(function* () {
    const repo = yield* UserRepo;
    const cache = yield* CacheService;

    const findById = Effect.fn("UserService.findById")(function* (id: UserId) {
      const cached = yield* cache.get(id);
      if (Option.isSome(cached)) return cached.value;
      const user = yield* repo.findById(id);
      yield* cache.set(id, user);
      return user;
    });

    const create = Effect.fn("UserService.create")(function* (data: CreateUserInput) {
      const user = yield* repo.create(data);
      yield* Effect.log("User created", { userId: user.id });
      return user;
    });

    return { findById, create };
  }),
}) {}

// Usage - dependencies automatically wired via .Default
const program = Effect.gen(function* () {
  const user = yield* UserService.findById(userId); // accessors enabled
});

// At app root
const MainLive = Layer.mergeAll(UserService.Default, OtherService.Default);
```

**The class is the tag:** You can provide alternate implementations for testing:

```typescript
const mock = new UserService({ findById: () => Effect.succeed(mockUser) });
program.pipe(Effect.provideService(UserService, mock));
```

### Context.Tag (For Libraries / No Default)

Use `Context.Tag` when no sensible default exists or you're writing library code:

```typescript
import { Context, Effect, Layer } from "effect";

// Per-request database handle - no sensible global default
class RequestDb extends Context.Tag("@app/RequestDb")<
  RequestDb,
  { readonly query: (sql: string) => Effect.Effect<unknown[]> }
>() {}

// Library code - callers provide implementation
class PaymentGateway extends Context.Tag("@lib/PaymentGateway")<
  PaymentGateway,
  { readonly charge: (amount: number) => Effect.Effect<Receipt, PaymentError> }
>() {}

// Implement with Layer.effect when needed
const RequestDbLive = Layer.effect(
  RequestDb,
  Effect.gen(function* () {
    const pool = yield* DatabasePool;
    return RequestDb.of({
      query: (sql) => pool.query(sql),
    });
  }),
);
```

**Key rules:**

- Tag identifiers must be unique. Use `@path/to/ServiceName` prefix pattern
- Service methods should have no dependencies (`R = never`)
- Use readonly properties

See `references/service-patterns.md` for service-driven development and test layers.

## Error Definition Pattern

**Use `Schema.TaggedError`** for errors. They are serializable (required for RPC) and **yieldable** (no need for `Effect.fail()`):

```typescript
import { Schema } from "effect";

class UserNotFoundError extends Schema.TaggedError<UserNotFoundError>()("UserNotFoundError", {
  userId: UserId,
  userMessage: Schema.String,
}) {}

// Usage - yieldable errors can be used directly
const findUser = Effect.fn("findUser")(function* (id: UserId) {
  const user = yield* repo.findById(id);
  if (Option.isNone(user)) {
    return yield* UserNotFoundError.make({ userId: id, userMessage: "User not found" });
  }
  return user.value;
});
```

### Error Recovery

Use `catchTag`/`catchTags` for type-safe error handling:

```typescript
// Single error type
yield *
  repo
    .findById(id)
    .pipe(
      Effect.catchTag("DatabaseError", (err) =>
        UserLookupError.make({ userId: id, reason: err.reason, cause: err }),
      ),
    );

// Multiple error types
yield *
  effect.pipe(
    Effect.catchTags({
      DatabaseError: (err) => UserLookupError.make({ userId: id, reason: err.reason, cause: err }),
      ValidationError: (err) =>
        InvalidInputError.make({ field: err.field, reason: err.reason, cause: err }),
    }),
  );
```

### Schema.Defect for Unknown Errors

Wrap errors from external libraries with `Schema.Defect`:

```typescript
class ApiError extends Schema.TaggedError<ApiError>()("ApiError", {
  endpoint: Schema.String,
  statusCode: Schema.Number,
  error: Schema.Defect, // Wraps unknown errors
}) {}
```

See `references/error-patterns.md` for expected vs defects and retry patterns.

## Data Modeling

### Branded Types

**Brand all entity IDs** to prevent mixing values with the same underlying type:

```typescript
import { Schema } from "effect";

export const UserId = Schema.String.pipe(Schema.brand("UserId"));
export type UserId = typeof UserId.Type;

export const PostId = Schema.String.pipe(Schema.brand("PostId"));
export type PostId = typeof PostId.Type;

// Type error: can't pass PostId where UserId expected
function getUser(id: UserId) {
  /* ... */
}
getUser(PostId.make("post-123")); // Error!
```

### Schema.Class for Records

Use `Schema.Class` for composite data models:

```typescript
export class User extends Schema.Class<User>("User")({
  id: UserId,
  name: Schema.String,
  email: Schema.String,
  createdAt: Schema.Date,
}) {
  get displayName() {
    return `${this.name} (${this.email})`;
  }
}
```

### Schema.TaggedClass for Variants

Use `Schema.TaggedClass` with `Schema.Union` for discriminated unions:

```typescript
import { Match, Schema } from "effect";

export class Success extends Schema.TaggedClass<Success>()("Success", {
  value: Schema.Number,
}) {}

export class Failure extends Schema.TaggedClass<Failure>()("Failure", {
  error: Schema.String,
}) {}

export const Result = Schema.Union(Success, Failure);

// Pattern match with Match.valueTags
Match.valueTags(result, {
  Success: ({ value }) => `Got: ${value}`,
  Failure: ({ error }) => `Error: ${error}`,
});
```

See `references/schema-patterns.md` for JSON encoding and advanced patterns.

## Layer Composition & Memoization

**Provide layers once at the top** of your application:

```typescript
const appLayer = userServiceLayer.pipe(
  Layer.provideMerge(databaseLayer),
  Layer.provideMerge(loggerLayer),
);

const main = program.pipe(Effect.provide(appLayer));
Effect.runPromise(main);
```

### Layer Memoization Warning

Effect memoizes layers by reference identity. Store parameterized layers in constants:

```typescript
// BAD: creates TWO connection pools
const badLayer = Layer.merge(
  UserRepo.layer.pipe(Layer.provide(Postgres.layer({ url: "..." }))),
  OrderRepo.layer.pipe(Layer.provide(Postgres.layer({ url: "..." }))), // Different reference!
);

// GOOD: single connection pool
const postgresLayer = Postgres.layer({ url: "..." });
const goodLayer = Layer.merge(
  UserRepo.layer.pipe(Layer.provide(postgresLayer)),
  OrderRepo.layer.pipe(Layer.provide(postgresLayer)), // Same reference!
);
```

See `references/layer-patterns.md` for test layers and config-dependent layers.

## Config

Use `Config.*` primitives or `Schema.Config` for type-safe configuration:

```typescript
import { Config, Effect, Schema } from "effect";

const Port = Schema.Int.pipe(Schema.between(1, 65535));

const program = Effect.gen(function* () {
  // Basic primitives
  const apiKey = yield* Config.redacted("API_KEY");
  const port = yield* Config.integer("PORT");

  // With Schema validation
  const validatedPort = yield* Schema.Config("PORT", Port);
});
```

### Config Service Pattern

Create config services with test layers:

```typescript
class ApiConfig extends Context.Tag("@app/ApiConfig")<
  ApiConfig,
  { readonly apiKey: Redacted.Redacted; readonly baseUrl: string }
>() {
  static readonly layer = Layer.effect(
    ApiConfig,
    Effect.gen(function* () {
      const apiKey = yield* Config.redacted("API_KEY");
      const baseUrl = yield* Config.string("API_BASE_URL");
      return ApiConfig.of({ apiKey, baseUrl });
    }),
  );

  // For tests - hardcoded values
  static readonly testLayer = Layer.succeed(ApiConfig, {
    apiKey: Redacted.make("test-key"),
    baseUrl: "https://test.example.com",
  });
}
```

See `references/config-patterns.md` for ConfigProvider and advanced patterns.

## Testing

Use `@effect/vitest` for Effect-native testing:

```typescript
import { Effect } from "effect";
import { describe, expect, it } from "@effect/vitest";

describe("Calculator", () => {
  it.effect("adds numbers", () =>
    Effect.gen(function* () {
      const result = yield* Effect.succeed(1 + 1);
      expect(result).toBe(2);
    }),
  );

  // With scoped resources
  it.scoped("cleans up resources", () =>
    Effect.gen(function* () {
      const tempDir = yield* fs.makeTempDirectoryScoped();
      // tempDir deleted when scope closes
    }),
  );
});
```

### Test Layers

Create in-memory test layers with `Layer.sync`:

```typescript
class Users extends Context.Tag("@app/Users")<
  Users,
  {
    /* ... */
  }
>() {
  static readonly testLayer = Layer.sync(Users, () => {
    const store = new Map<UserId, User>();

    const create = (user: User) => Effect.sync(() => void store.set(user.id, user));
    const findById = (id: UserId) => Effect.fromNullable(store.get(id));

    return Users.of({ create, findById });
  });
}
```

See `references/testing-patterns.md` for TestClock and worked examples.

## CLI

Use `@effect/cli` for typed argument parsing:

```typescript
import { Args, Command, Options } from "@effect/cli";
import { BunContext, BunRuntime } from "@effect/platform-bun";
import { Console, Effect } from "effect";

const name = Args.text({ name: "name" }).pipe(Args.withDefault("World"));
const shout = Options.boolean("shout").pipe(Options.withAlias("s"));

const greet = Command.make("greet", { name, shout }, ({ name, shout }) => {
  const message = `Hello, ${name}`;
  return Console.log(shout ? message.toUpperCase() : message);
});

const cli = Command.run(greet, { name: "greet", version: "1.0.0" });

cli(process.argv).pipe(Effect.provide(BunContext.layer), BunRuntime.runMain);
```

See `references/cli-patterns.md` for subcommands and service integration.

## Effect Atom (Frontend State)

Effect Atom provides reactive state management for React with Effect integration.

### Basic Atoms

```typescript
import { Atom } from "@effect-atom/atom-react";

// Define atoms OUTSIDE components
const countAtom = Atom.make(0);

// Use keepAlive for global state that should persist
const userPrefsAtom = Atom.make({ theme: "dark" }).pipe(Atom.keepAlive);

// Atom families for per-entity state
const modalAtomFamily = Atom.family((type: string) =>
  Atom.make({ isOpen: false }).pipe(Atom.keepAlive),
);
```

### React Integration

```typescript
import { useAtomValue, useAtomSet, useAtom } from "@effect-atom/atom-react"

function Counter() {
  const count = useAtomValue(countAtom)           // Read only
  const setCount = useAtomSet(countAtom)          // Write only
  const [value, setValue] = useAtom(countAtom)    // Read + write

  return <button onClick={() => setCount((c) => c + 1)}>{count}</button>
}
```

### Handling Results with Result.builder

```typescript
import { Result } from "@effect-atom/atom-react"

function UserProfile() {
  const userResult = useAtomValue(userAtom)

  return Result.builder(userResult)
    .onInitial(() => <div>Loading...</div>)
    .onErrorTag("NotFoundError", () => <div>User not found</div>)
    .onError((error) => <div>Error: {error.message}</div>)
    .onSuccess((user) => <div>Hello, {user.name}</div>)
    .render()
}
```

See `references/effect-atom-patterns.md` for complete patterns.

## Anti-Patterns (Forbidden)

```typescript
// FORBIDDEN - runSync/runPromise inside services
yield *
  Effect.gen(function* () {
    const result = Effect.runPromise(someEffect);
  }); // Always prefer yielding the effect. As a workaround for libraries requiring promises etc, extract the current runtime using `const runtime = yield* Effect.runtime<never>();` then use it to run the promise.

// FORBIDDEN - throw inside Effect.gen
yield *
  Effect.gen(function* () {
    if (bad) throw new Error("No!"); // Use Effect.fail or yieldable error
  });

// FORBIDDEN - catchAll losing type info
yield * effect.pipe(Effect.catchAll(() => Effect.fail(new GenericError())));

// FORBIDDEN - console.log
console.log("debug"); // Use Effect.log

// FORBIDDEN - process.env directly
const key = process.env.API_KEY; // Use Config.string("API_KEY")

// FORBIDDEN - null/undefined in domain types
type User = { name: string | null }; // Use Option<string>
```

See `references/anti-patterns.md` for the complete list with rationale.

## Reference Files / How to use

For detailed patterns or in the case of any ambiguity you must consult these reference files in the `references/` directory:

- `anti-patterns.md` - Complete list of forbidden patterns
- `cli-patterns.md` - @effect/cli Commands, Args, Options, subcommands
- `config-patterns.md` - Config primitives, Schema.Config, ConfigProvider
- `domain-predicates.md` - Equivalence, Order, Schema.Data for equality and sorting
- `effect-atom-patterns.md` - Atom, families, React hooks, Result handling
- `error-patterns.md` - Schema.TaggedError, yieldable errors, Schema.Defect
- `layer-patterns.md` - Dependency composition, memoization, testing layers
- `observability-patterns.md` - Logging, metrics, config patterns
- `rpc-cluster-patterns.md` - RpcGroup, Workflow, Activity patterns
- `schema-patterns.md` - Branded types, Schema.Class, JSON encoding
- `service-patterns.md` - Effect.Service vs Context.Tag, dependencies, test layers
- `testing-patterns.md` - @effect/vitest, it.effect, it.scoped, TestClock, property-based testing
