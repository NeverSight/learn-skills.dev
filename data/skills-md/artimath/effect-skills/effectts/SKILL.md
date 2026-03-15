---
name: effectts
description: "Idiomatic Effect-TS patterns for TypeScript functional programming. USE THIS SKILL WHEN: Writing new Effect services or layers, debugging Effect type errors (layer composition, error types), choosing between Effect patterns, setting up Effect testing. TRIGGERS ON: 'effect pattern', 'Layer.provide', 'Context.Tag', 'effect service', 'effect error', 'effect test', 'idiomatic effect'. NOT FOR: general TypeScript without Effect."
version: 1.0.0
---

# Idiomatic Effect-TS

Write Effect code that looks like it came from the Effect core team.

## Prerequisites (Optional)

- **Effect source** (recommended): `git clone https://github.com/Effect-TS/effect` for pattern verification
- **Effect MCP**: https://github.com/tim-smart/effect-mcp for API lookups (fallback: https://effect.website/docs)

## Research First (ALWAYS)

### 1. Effect Docs MCP (preferred for concepts)

If you have effect-mcp configured:

```typescript
// Search documentation
mcp__effect-docs__effect_docs_search({ query: "Layer composition" })

// Then read specific doc
mcp__effect-docs__get_effect_doc({ documentId: 123 })
```

Otherwise, check https://effect.website/docs for API reference.

### 2. Effect Source (preferred for real patterns)

```bash
# Clone Effect source for pattern verification (if not already done)
# git clone https://github.com/Effect-TS/effect <effect-repo>

# Service patterns (Context.Tag for libraries)
rg "class .* extends Context\.Tag" <effect-repo>/packages/workflow/src
rg "class .* extends Context\.Tag" <effect-repo>/packages/cluster/src

# Effect.Service for concrete impls/tests
rg "Effect\.Service" <effect-repo>/packages/cluster/src

# Error patterns
rg "Schema\.TaggedError" <effect-repo>/packages/cluster/src

# Layer composition
rg "Layer.provideMerge" <effect-repo>/packages/platform/src
```

**Use parallel searches when patterns are unclear.**

## Quick Reference

### Service Patterns (Choose Based on Use Case)

| Pattern | Use When | Layer Access |
|---------|----------|--------------|
| `Context.Tag` | Library interfaces, multiple impls | `ServiceName.Live` |
| `Effect.Service` | Concrete impls, tests, apps | `ServiceName.Default` |

```typescript
// Library interface (Context.Tag) - canonical for libraries
export class MyService extends Context.Tag("app/MyService")<MyService, {
  readonly doThing: (x: string) => Effect.Effect<Result, MyError>
}>() {
  static readonly Live: Layer.Layer<MyService, never, Deps> = Layer.effect(...)
}

// Concrete impl (Effect.Service) - convenient for apps/tests
export class AppCache extends Effect.Service<AppCache>()("app/Cache", {
  effect: Effect.gen(function* () {
    return { get: (k) => ..., set: (k, v) => ... }
  }),
  dependencies: [SomeDep.Default]  // auto-composed
}) {}
```

### Domain Errors

```typescript
export class MyError extends Schema.TaggedError<MyError>()("MyError", {
  reason: Schema.Literal("NotFound", "Invalid"),
  cause: Schema.optional(Schema.Defect)
}) {
  static is(u: unknown): u is MyError {
    return hasProperty(u, "_tag") && isTagged(u, "MyError")
  }
}
```

### Domain Types

```typescript
// Value objects
export class Address extends Schema.Class<Address>("Address")({
  host: Schema.String,
  port: Schema.Number
}) {}

// Branded IDs — always with REAL constraints
export const UserId = Schema.NonEmptyString.pipe(
  Schema.pattern(/^usr_[a-z0-9]+$/),
  Schema.brand("UserId")
)
export type UserId = typeof UserId.Type
```

### Layer Composition — COMMON GOTCHA

**This causes most Effect type errors.** Know the difference:

| Method | Deps Satisfied | Available to Program | Use When |
|--------|---------------|---------------------|----------|
| `Layer.provide` | Yes | No | Internal layer building |
| `Layer.provideMerge` | Yes | Yes | **Tests using multiple services** |
| `Layer.mergeAll` | No | Yes | Combining independent layers |

```typescript
// WRONG - test can't access FileSystem
const TestLive = MyService.Live.pipe(Layer.provide(PlatformLive))
// yield* FileSystem.FileSystem -> ERROR

// RIGHT - both services available
const TestLive = MyService.Live.pipe(Layer.provideMerge(PlatformLive))
// yield* MyService -> works
// yield* FileSystem.FileSystem -> also works!
```

**Error pattern to recognize:**
```
Effect<A, E, SomeService> is not assignable to Effect<A, E, never>
```
or diagnostic: `Missing 'SomeService' in the expected Effect context`

-> Means `SomeService` still required. Use `provideMerge` instead of `provide`.

### Test Pattern

```typescript
it.effect("works", () =>
  Effect.gen(function* () {
    const svc = yield* MyService
    expect(yield* svc.doThing("x")).toBe(expected)
  }).pipe(Effect.provide(TestLive))  // <- MUST provide at boundary
)
```

## References (Read When Needed)

| Topic | File | When to Read |
|-------|------|--------------|
| Service & Layer patterns | [references/services.md](references/services.md) | Creating services, Context.Tag vs Effect.Service, layer composition |
| **Layer dependencies** | [references/layer-dependencies.md](references/layer-dependencies.md) | **How services access deps (yield + closure), why NOT factory functions** |
| **Schema decision matrix** | [references/schema-decision.md](references/schema-decision.md) | **Schema.Class vs Struct vs TaggedClass, branded types, migration patterns** |
| Error handling | [references/errors.md](references/errors.md) | Schema.TaggedError, TypeId, refail patterns |
| Domain types | [references/domain-types.md](references/domain-types.md) | Schema.Class, branded types, TaggedRequest |
| Testing | [references/testing.md](references/testing.md) | @effect/vitest setup, TDD workflow, test helpers |
| Collections & State | [references/data.md](references/data.md) | Chunk, Option, Ref patterns |
| Process management | [references/processes.md](references/processes.md) | Scope, Command, background processes |

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| `Data.TaggedError` for domain errors | Use `Schema.TaggedError` |
| `Layer.mergeAll` with dependent layers | Use `Layer.provideMerge` |
| `try/catch` in Effect.gen | Use `Effect.try` or `mapError` |
| Missing `Effect.provide(...)` in tests | Always provide at test boundary |
| Plain interfaces for domain types | Use `Schema.Struct` (or `Schema.Class` if needs behavior) |
| String IDs without branding | Use `Schema.brand()` |
| Guessing patterns | Grep Effect source first |
| `Effect.Service` for library interfaces | Use `Context.Tag` |
| Factory function with service param | Yield deps in Effect.gen, close over (see layer-dependencies.md) |
| `Schema.Class` for simple DTOs | Use `Schema.Struct` unless needs Equal/Hash |
| String literal union in struct | Use `Schema.TaggedClass` for variants |
| Phantom type `& { _tag }` | Use `Schema.brand()` for runtime validation |
| Bare `Schema.String.pipe(Schema.brand(...))` | Add real constraints: NonEmptyString, pattern(), etc. |
