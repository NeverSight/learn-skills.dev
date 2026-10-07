---
name: typescript-standards
description: "Domain modeling and module design in TypeScript: DDD roles, ports and adapters, branded types, tagged errors, and tests through real seams. Use when writing or reviewing any TypeScript."
license: Apache-2.0
---
These standards describe how to design and write TypeScript code in this codebase. They are especially intended for agents: inspect existing code before adding patterns, libraries, Adapters, or abstractions, but apply these standards to all new and refactored behavior. Follow existing conventions only when they are compatible with these standards.

## Rule ownership

This skill owns types, schemas, module design, comments, and general tests.
Use [tanstack-frontend](../tanstack-frontend/SKILL.md) for FSD, React, queries, mutations, and UI conventions.
Use [cloudflare-backend](../cloudflare-backend/SKILL.md) for application boundaries, transport contracts, retries, and persistence.

Those skills define their assigned topics. An internal Result convention does not prescribe a transport envelope.
Explicit task instructions and global workflow constraints still apply.
Apply these standards to new and refactored behavior. Contain incompatible existing patterns at their boundary.
Keep unrelated code unchanged. Record lasting architectural decisions when they need an ADR.

## Core principles

- Default to typed thrown errors and rejected promises. Preserve established Result or Effect contracts.
- **Parse don't validate**. Parse early and as close to composition or application roots as possible. Do not merely validate and throw away the information learned.
- Make **illegal states unrepresentable** where practical.
- Prefer **correct-by-construction** APIs over convention-based invariants.
- Use branded/refined/domain types when they prevent a realistic mistake, such as mixing identifiers or units, bypassing parsing, or constructing an invalid value.
- Prefer **composition over inheritance**.
- Prefer **imperative shell / functional core**.
- Design **deep, cohesive modules** with **low caller burden**.
- Test behavior through real seams; **avoid** module mocks and spy-driven tests.
- Keep code discoverable for humans and agents.

## Reuse and operation contracts

Before writing general-purpose logic, identify which runtime, framework, SDK, or installed dependency could own it.
Check its exports and documentation. Consider a maintained library if the stack has no suitable capability.
Write custom logic last, with a reason.

An owned operation must answer only when its promised effect exists.
Fix that operation instead of adding downstream polling, deferred registries, or completion waiters.
Bridge an event to a promise only at its owner, when the event source cannot provide completion directly.
An asynchronous operation may return an accepted job. Its contract must distinguish acceptance from completion.

A signature declares exactly what the function receives. Do not pass a broader object than the parameter type admits.
Consume declared API response types. Check client configuration and generic inference before reconstructing response types with ad-hoc guards.
For owned APIs, fix missing schemas or types at the boundary. Parse untrusted input with schemas.

## Adapting to existing codebases

Before adding a new pattern or library, inspect the repo for existing choices around:

- error handling
- schema parsing
- dependency injection
- testing
- observability
- adapters/services
- module layout

Apply these standards to all new code and to the full behavior being refactored. Do not preserve weaker patterns merely for consistency. Keep unrelated old code unchanged and translate incompatible patterns at the nearest boundary.

Most apps use thrown errors and rejected promises. Follow that convention in new and refactored code.
A dependency on `better-result`, including a transitive dependency, does not justify adopting Result.
Preserve existing logging, tracing, metrics, and error-reporting hooks.

## Minimal diffs

A change touches only the lines that its agreed behavior needs. Keep every other existing line byte-identical.
Do not move, re-indent, re-wrap, reword, rename, or retype existing code. Add new code around it; do not restructure it to fit.
Make an unrequested cleanup only when the user agrees or it is a real improvement, and then as a separate change.
A refactor is the exception only when the user asked for one. If a change forces other lines to move, say why first.

Unrequested edits hide the real change in review and move `git blame` to the wrong commit. A renamed exported symbol can also break callers.

## Errors and failures

### Define each operation's failures

Think through known failures even when TypeScript cannot declare thrown errors in the return type.
Use typed errors with stable tags or codes and useful context. Never classify errors from message text.

Before implementation, identify:

1. Which failures the operation can produce, including cancellation and partial completion.
2. Which failures the caller must distinguish and what action each requires.
3. Which layer converts external failures and which boundary logs the final error.
4. Whether repetition is safe and which layer owns retries.
5. Which focused tests prove important failure behavior and cleanup.

Document non-obvious thrown failures with `@throws`. Do not add unused error unions to imply checked exceptions.
Convert external failures at the owning adapter when needed. Preserve their causes and distinctions the caller needs.
Expected absence, completion, and no-op outcomes may be ordinary data rather than errors.

### Limited use of Result

Use `better-result` for an isolated operation only when explicit result composition provides a concrete benefit.
Examples include nuanced retry classification or exceptional workflows with several recoverable outcomes.
Retries alone do not require Result. Check the project's existing retry capability first.
State the local benefit and keep conversion at that operation's boundary. Do not spread Result through callers to satisfy this skill.
Do not adopt it merely because the dependency is available or expected failures exist.
Adopting Result across an app requires a separate, explicitly approved change.
Preserve established Result or Effect code; this default does not require migrating it to throws.

### Transport conversion

A transport adapter uses the transport's failure channel. Shared middleware owns serialization and error conversion.
When an isolated operation returns Result, its adapter can extract success or throw the typed error into existing middleware.
Use the project's existing conversion helper. Do not add a success envelope or repeat serialization in every function.
Read the backend skill before changing this contract, including when adding server stubs.

### Defects may throw or panic

Never use `throw new Error(...)` in production code. Use a typed error with a stable tag or code.
Migrate raw throws when touched. Deliberate test and failure-probe throws are exempt.

Typed throws can represent expected failures. Reserve panic and defect helpers for conditions that make correct execution impossible. Defects include:

- violated internal invariants
- impossible branches
- temporary `notYetImplemented` paths
- catastrophic runtime conditions

Known configuration failures use typed errors; the composition root reports them safely and terminates startup.

Use established shared defect helpers where available, or the panic helper from the project's result library:

```ts
export function casesHandled(unexpectedCase: never): never;
export function shouldNeverHappen(msg?: string): never;
export function notYetImplemented(msg?: string): never;
```

Use `casesHandled` for exhaustive union handling. Avoid names like `absurd` or one-off `assertNever` helpers when the project already has these helpers.

### Custom errors

Expected failures should use custom tagged errors, generally extending:

- `Error`
- `TaggedError` from `better-result`
- `Schema.TaggedErrorClass` in Effect codebases

Custom errors should include:

- stable tag using 'as const'
- useful message
- structured contextual fields
- safe telemetry fields
- optional `cause: unknown`

Example:

```ts
export class UserStoreUnavailable extends Error {
  readonly _tag = "UserStoreUnavailable" as const;

  constructor(
    readonly operation: "findActiveByEmail",
    readonly provider: "postgres",
    readonly cause: unknown,
  ) {
    super(`User store unavailable during ${operation}`);
  }
}
```

Keep error unions precise at module boundaries:

```ts
Result<User, UserNotFound | UserStoreUnavailable>
```

Avoid broad `AppError`-style types except near entrypoints, orchestration, logging, and rendering layers.

### Wrapping and rethrowing

Wrap only when crossing a port whose callers must not see the inner error types. Map each inner tag onto one outer tag that callers already branch on. Preserve the inner error as `cause`. Callers match the outer tag; they must not unwrap `cause` to decide.

Do not wrap when:

- you are still in the layer that owns the inner tags
- every inner failure becomes the same outer tag (a lie: invalid input is not "unavailable")
- the wrap exists only to avoid importing the inner type

The examples below preserve an existing throw-based boundary contract.
For an internal Result port, return the mapped error as a typed value.

**Good — map at the port:**

```ts
async function startGrok(signal: AbortSignal): Promise<AcpTransport> {
  try {
    return await AcpTransport.start({ command: "grok", signal, /* … */ })
  } catch (cause) {
    throw new CodingAgentUnavailableError({ cause })
  }
}
```

Spawn failed. The coding-agent port has no ACP spawn type. `Unavailable` is the fact the caller can act on.

**Bad — catch-all rethrow:**

```ts
async function grokRequest(transport: AcpTransport, input: Request): Promise<Response> {
  try {
    return await transport.request(input)
  } catch (cause) {
    throw new CodingAgentUnavailableError({ cause })
  }
}
```

`request` already classified timeout, process exit, and JSON-RPC rejection. This wrap deletes that distinction. A bad `configId` looks like "Grok is down." Call `transport.request` instead, or map `AcpRpcError` to `CodingAgentRequestError` and only the transport/timeout/exit tags to `CodingAgentUnavailableError`.

## Sensitive data, telemetry, and debugging

Prefer end-to-end structured tracing across requests, jobs, workflows, application modules, adapters, and external calls.

Tracing/logging should make failures diagnosable with safe fields:

- domain IDs
- operation names
- dependency/provider names
- state tags
- retry counts
- typed error tags
- safe summaries

Do not put secrets in errors, traces, logs, or snapshots.

Use a `Redacted<T>` wrapper for sensitive values such as tokens, API keys, passwords, raw credentials, and secrets. Prefer Effect's `Redacted.Redacted` in Effect codebases or a local shared `Redacted<T>` wrapper.

Wrap sensitive values at the boundary and unwrap only where the raw value is needed, usually inside an adapter making an external call.

## Parse, don't validate

Boundary code should turn unknown or less-structured input into application or domain types before it enters inner code.

Use a separate protocol projection only when its shape or meaning differs enough to be useful. `DTO` describes a boundary role in prose; never use `DTO` or `Dto` in a symbol name. Name the symbol after its actual protocol or persistence meaning, such as `CreateUserRequest`, `StripeCustomerResponse`, or `UserRecord`:

```ts
unknown -> CreateUserRequest -> CreateUserInput -> EmailAddress/UserId/etc.
```

Otherwise, parse directly into the application input:

```ts
unknown -> CreateUserInput
```

Do not pass a schema-inferred transport shape throughout the application:

```ts
unknown -> z.infer<typeof CreateUserSchema>
```

Use names that preserve meaning:

- `parseX(input): Result<X, ParseXError>` for untrusted or less-structured input
- `makeX(...)` / `createX(...)` for smart constructors from already-typed pieces
- `isX(value): value is X` for true predicates
- `assertX(...)` rarely, mostly at tests/framework boundaries

Avoid `validateX` when the function returns a refined value. It parsed something.

### Schemas

Use schema libraries as boundary parsers, not as ad-hoc validators sprinkled through core logic.

Preference:

- use the repo's established schema library if one exists
- use Effect Schema in Effect codebases
- prefer Standard Schema compatibility for generic helpers
- otherwise prefer Zod 4
- use hand-written smart constructors/parsers for small domain types when clearer

Schema parsing should produce refined/domain types and typed custom errors where practical.

For Zod 4:

- Use top-level format helpers: `z.uuid()`, `z.email()`, `z.url()`, `z.httpUrl()`, `z.iso.datetime()`, `z.iso.date()`, and `z.iso.time()`.
- Use `z.uuidv7()`, `z.nanoid()`, `z.ipv4()`, `z.base64()`, `z.jwt()`, and `z.stringbool()` where applicable.
- Set messages with `{ error: "message" }`, not `message` or `invalid_type_error`.
- Use branded ID schemas, such as `UserIdSchema`, instead of bare `z.string()` for typed IDs.

## Branded types and correct construction

Use branded/refined types when they prevent realistic misuse or invalid construction, especially for:

- IDs: `UserId`, `OrgId`, `WorkflowId`
- parsed strings: `EmailAddress`, `NonEmptyString`, `Url`
- constrained numbers: `PositiveInt`, `Cents`, `Percentage`
- units: `Milliseconds`, `Bytes`, `UsdCents`

Construct branded values through parsers or smart constructors. Avoid passing raw strings/numbers where a domain type exists.

Avoid optional/null/undefined values in functions that require a value. Push optionality outward. Branch or parse before calling.

Avoid `Partial<T>` as an application/domain input unless partiality is the real domain concept. Prefer explicit input types for each operation.

## One fact, one representation

Represent each independent fact once in rows, contracts, events, caches, state, props, and configuration.
Keep canonical facts or an authoritative result. Derive deterministic values at the owning or consuming layer.
Expose a result when its derivation contains business policy. Do not duplicate its inputs for convenience.

Before adding a field:

1. Is this an independent fact?
2. Can existing fields determine it exactly?
3. What happens if the values disagree?
4. Which value is canonical?
5. Which layer owns the derivation?

Allow redundancy only for external compatibility, immutable audit snapshots, measured performance, or unavailable private source data.
Identify the canonical source. Synchronize atomically and enforce the invariant where possible. Test disagreement cases.

## State machines and boolean blindness

When an entity has meaningful lifecycle states, model them with tagged unions or equivalent value classes.

Prefer:

```ts
type Invoice =
  | { readonly _tag: "Draft"; readonly id: InvoiceId; readonly lines: NonEmptyArray<LineItem> }
  | { readonly _tag: "Sent"; readonly id: InvoiceId; readonly sentAt: Instant }
  | { readonly _tag: "Paid"; readonly id: InvoiceId; readonly paidAt: Instant };
```

Avoid:

```ts
type Invoice = {
  readonly isSent: boolean;
  readonly isPaid: boolean;
  readonly sentAt?: Date;
  readonly paidAt?: Date;
};
```

Avoid boolean parameters that control behavior:

```ts
createUser(input, true);
```

Prefer named options or domain types:

```ts
createUser(input, { emailVerification: "skip" });
```

Booleans are fine as clear predicate return values:

```ts
isExpired(token): boolean;
hasPermission(user, permission): boolean;
```

## Modules and abstractions

Domain Module, Application Service Module, and Adapter Module name responsibilities, not folders. Before you design or review a module, port, or adapter, read [modules and ports](references/modules-and-ports.md). It defines each role, deep modules, application-owned ports, the adapter reuse audit, and repositories.

## Functional core, imperative shell, and entrypoints

Domain Modules form the functional core. Application Service Modules and Adapter Modules form the imperative shell, but only Adapters contain technology-specific concerns. This keeps the same application operation reusable across REST, CLI, GraphQL, workers, and other entrypoints.

The functional core contains domain parsers, invariants, state transitions, calculations, combinators, and decision functions. It avoids I/O, hidden dependencies, ambient time/randomness, thrown expected failures, and framework-specific concerns.

The imperative shell has two distinct responsibilities:

- Application Services apply application policy and sequence effects through explicit ports.
- Adapters parse or project boundary values, classify external failures, and perform concrete I/O.

Entrypoint Adapters should be thin protocol translation layers. They parse protocol-specific input, call Domain Module parsers to obtain refined values, invoke an Application Service when application policy or effects are involved, and render protocol-specific output. A pure operation may call a Domain Module directly, as [modules and ports](references/modules-and-ports.md) describes. Do not duplicate business rules in controllers, resolvers, commands, or handlers.

Within authentication and authorization, inbound Adapters verify boundary credentials and produce a parsed identity such as `Principal`, `Session`, or `CommandActor`. Domain Modules may define pure permission decisions over parsed domain values. Application Services gather the required context and enforce those decisions while carrying out an application operation. Adapters project missing or invalid credentials and denied operations into protocol-specific outcomes; they do not define permission policy.

## Workflows, transactions, and idempotency

Use ordinary function calls or database transactions for simple single-boundary operations.

Use a saga or durable workflow when progress must survive process loss or redelivery, or when the operation requires long delays, compensation, resumability, timers, human approval, cross-service coordination, or multiple transaction boundaries. A short-lived retry by itself does not require durable workflow machinery.

Adapters own safe, short-lived technical retries. Application Services decide whether an application operation should be attempted again. Durable workflows own retries that must survive crashes, delays, or redelivery.

Do not hold database transactions open across network calls or long-running operations.

Any externally observable mutation or state transition that may be retried needs an explicit idempotency strategy:

- idempotency key
- natural unique constraint
- deduplication record
- state-machine transition guard
- transactional outbox/inbox

Retrying should not rely on “probably safe” side effects.

## Testing

Never use `vi.mock` or `jest.mock`; test through real seams. Before you write, review, or speed up a test, read [testing](references/testing.md).
It is the default for every project. A project testing document records only exceptions.

## TypeScript style and safety

No `any`, no non-null assertions, and no `as` cast without a `SAFETY:` comment. Before you write or review TypeScript, read [style and files](references/style-and-files.md). It covers compiler settings, casts, imports, exports, and file names.

## Comments and JSDoc

Every non-JSDoc comment is exactly one line. Explain why: a constraint, rejected alternative, or external rule.
Delete comments that describe what the code already shows.

JSDoc defaults to two or three lines. Add lines only for a caller's non-obvious contract, side effect, ordering, or lifetime rule.
Document key modules and exported architectural boundaries. Stop when the caller can use them correctly.
Do not repeat TypeScript types or add boilerplate to every field. Document the original declaration, not its re-exports.
Do not use `@inheritDoc` or `@inherit`.

Use `@throws` for defects, framework-required throws, and temporary unimplemented paths.
Document internal expected failures as return values. Transport failure channels follow the backend skill.

Use the language's deprecation directive for each deprecated symbol or path.
Use a one-line comment only when no directive exists. Create a Linear issue for each deprecation.
State the removal condition, why the path remains, and how verification proves removal.

## Workspace boundaries

Use `apps/` for applications and `packages/` for shared code.
Workspace dependency direction is `packages → ∅` and `apps → packages`. Never import between applications.
Core exports shared types, schemas, constants, and common logic.
Use `workspace:*` for local dependencies. Follow AGENTS.md for third-party version and catalog management.
Build shared dependencies before consumers through the project's scripts or task graph.

## Configuration and resources

Parse environment/config at startup or the earliest boundary into typed config with branded/redacted values where appropriate. Return known configuration failures as tagged error values. The composition root should report a safe startup message and terminate rather than treating invalid configuration as an internal defect.

Do not read `process.env` throughout the app. Missing or invalid config is a startup failure with useful, safe context.

Avoid top-level side effects except in true entrypoint/bootstrap files. Modules should not start servers, open connections, read env, register handlers, or perform I/O at import time.

Resource creation and cleanup should be explicit and owned by bootstrap/imperative shell code or Effect layers when using Effect.

Avoid mutable singletons/global state. Constants and pure lookup tables are fine. If a singleton is required by a framework/runtime, isolate it at the boundary.

Inject `Clock` / `Random` services into dependency-bearing modules. Pure domain functions may accept explicit `now` / random values.

## Quick agent checklist

Before coding:

- Read existing conventions for errors, schemas, tests, adapters, telemetry, and module layout.
- Classify each changed concern as Domain Module, Application Service Module, Adapter Module, or composition-root wiring.
- Reuse existing Domain Modules, Application Services, and Adapters before creating new ones.
- Define effect dependencies as narrow, application-owned ports; keep raw external types in Adapters or the composition root.
- Parse inputs at the edge and use domain types internally.
- Avoid raw DTOs, raw IDs, nullable bags, and `Partial<T>` in core/application logic.
- Prefer typed errors as values for new expected failures.
- Preserve existing observability/error mechanics.
- Test through public interfaces and real seams.
- Use `fast-check` arbitraries for generated test data when practical.
- Document exported contracts when callers need information the types cannot show.
- Add an ADR only for a lasting architectural boundary, shared pattern, provider strategy, or deliberate exception discovered through the Adapter/Application Service reuse audit.
