---
name: hexagonal-typescript
description: Hexagonal Architecture (Ports and Adapters) with Domain-Driven Design for TypeScript and Node.js backends built with NestJS, Express or Fastify, Prisma, TypeORM or Drizzle, and Vitest. Use it to design, implement, review, refactor or migrate TypeScript server-side code - REST APIs, use cases, aggregates, value objects, repositories, unit of work, domain events and outbox, bounded contexts, error handling, idempotency, pagination and tests per boundary. Trigger it when the project has package.json with tsconfig.json or .ts sources and the user mentions hexagonal, ports and adapters, clean architecture, DDD, layers, use cases, repositories, services, a fat controller, decoupling from NestJS, Express, Fastify or the ORM, or how to structure a Node API, even if they never say "hexagonal". Also use it for architecture, SOLID or testability reviews of TypeScript backend code. Not for other languages - use the matching hexagonal-<language> skill.
---

# Hexagonal TypeScript: Ports & Adapters + DDD

Business rules must not know how they are delivered (HTTP, CLI, queue) or stored (SQL, API, files). That single property makes the core testable without infrastructure, lets you move from Express to NestJS or from TypeORM to Prisma without rewriting rules, and keeps a change at one edge from rippling through the system.

This skill applies that idea to TypeScript on Node.js. The domain and the use cases are plain TypeScript (classes, interfaces, discriminated unions) with no framework, ORM or validation library imports. NestJS, Express, Fastify, Prisma, TypeORM, Drizzle and Zod live only in adapters, and each has its own guide.

## How to use this skill

1. **Detect the stack** (Step 0) and read `references/idioms.md` before writing code. It holds the conventions, the layout and the base `PlaceOrder` slice every other file builds on.
2. **Pick the working mode** (BUILD, REVIEW or MIGRATE, described below) and the depth with the proportionality table.
3. **Load only what the task needs** from the reference index at the end: one framework guide, one persistence guide, and the recipes that match the use case.
4. **Verify** with the final checklist. Run the project's type checker, linter, architecture check and tests, and report the real result.

## Step 0: Detect the stack

Look at the repository, not at assumptions. In a monorepo apply the skill per package or service.

| Marker in `package.json` | Meaning | Read |
|---|---|---|
| `@nestjs/core` | NestJS inbound adapter and module system | `references/frameworks/nestjs.md` |
| `express` (without NestJS) | Express inbound adapter | `references/frameworks/express.md` |
| `fastify` (without NestJS) | Fastify inbound adapter | `references/frameworks/fastify.md` |
| `@prisma/client` | Prisma persistence adapter | `references/persistence/prisma.md` |
| `typeorm` | TypeORM persistence adapter | `references/persistence/typeorm.md` |
| `drizzle-orm` | Drizzle persistence adapter | `references/persistence/drizzle.md` |
| Another framework or ORM (Hono, Koa, MikroORM, Kysely...) | No dedicated guide | Apply "Integrating a framework without a dedicated guide" below |
| Nothing yet | Greenfield | Ask which framework and ORM to use in one short question, or build the core first: it does not depend on the answer |

Then detect the **existing conventions** and keep them: package manager (from the lockfile), module system (`"type": "module"` or CommonJS), `tsconfig.json` strictness, formatter and linter (Prettier + ESLint, or Biome), test runner (Vitest or Jest), file naming and suffixes, error style. Match the codebase first and this skill's defaults second.

**TypeScript version.** TypeScript 7 (the native compiler) has no JavaScript compiler API yet, so tools that load `typescript` programmatically (dependency-cruiser, some ESLint setups) need an alternative parser or a TypeScript 6 install. `references/idioms.md`, section 8, shows the working setup.

<!-- BEGIN GENERATED: shared/core.md -->
## Core model

Dependencies point **inward**. Nothing in an inner layer imports anything from an outer one.

```
 Inbound adapters ──► Application (use cases) ──► Domain
 (HTTP, CLI, queue)          │
                             ▼ depends on (interfaces owned by the application)
                      Outbound ports ◄── Outbound adapters (DB, HTTP clients, brokers)

 Composition root: the only place that knows concrete adapters and wires them.
```

| Layer | Responsibility | May depend on | Must NOT depend on |
|---|---|---|---|
| **Domain** | Entities, value objects, aggregates, domain services, domain events, domain errors | The language standard library only | Frameworks, ORM, HTTP, serialization libraries, SDKs, DI containers |
| **Application** | Use cases: orchestrate domain + ports, transaction boundary, input/output DTOs, application errors | Domain, its own port interfaces | Web framework types, ORM types, concrete adapters |
| **Inbound adapters** | Translate protocol → use case input, and result/error → protocol (HTTP routes, CLI, consumers, schedulers) | Application (use case contracts), the framework | Outbound adapters, persistence details |
| **Outbound adapters** | Implement outbound ports with a technology (SQL repository, payment SDK wrapper, storage, email) | Application ports, domain types, libraries | Inbound adapters, other adapters directly |
| **Composition root** | Build adapters, inject them into use cases, load config, start and stop the app | Everything | Nothing depends on it |

Ports model **capabilities, not technologies**: `OrderRepository`, `PaymentGateway`, `Clock`, `EventPublisher`, never `PostgresService` or `StripeClient`. Outbound ports live in the application layer because they express what the use case needs. Inbound ports are the use case contracts: an explicit interface when several adapters or a decorator share it, otherwise the use case class or function itself.

**The framework is an adapter.** Routing, controllers, request validation libraries, DI containers and ORMs are details of the outer ring. The domain and the use cases must compile, run and be tested without the web framework installed. That is what "framework-agnostic" means here: the core is portable; the adapters are deliberately framework-specific.

## Proportionality: how much architecture?

Every abstraction costs files, indirection and reading time. Add a layer or port only when you can name the pain it removes: swapping infrastructure, testing without it, isolating a system you do not control, or protecting real business rules from churn. Use the **subdomain type** (see `references/ddd.md`) to decide where to invest:

| Situation | Subdomain | Depth |
|---|---|---|
| Pure CRUD, no business rules, one storage | Generic / supporting | **Thin slice**: route → use case (or thin service) → repository port + adapter. A plain data type is fine; skip aggregates and events. Still keep SQL and HTTP types out of the use case. |
| Real rules, state transitions, several collaborators | Core | **Full hexagonal + tactical DDD** (default for core features): aggregates, value objects, use cases, ports, adapters, composition. |
| Cross-context consistency, audit, strong read/write asymmetry | Core | Add **domain events, outbox or a read model** for that feature only. |
| Capability someone else does better (auth, email, payments) | Generic | Buy or integrate. Wrap it behind a port (Anti-Corruption Layer); do not model it. |

Create ports for the clock, id generation and randomness when behavior or tests depend on them. Do not create a port for stable standard-library behavior that is never faked, and do not create single-implementation interfaces with no boundary reason.

## Working modes

Identify the mode from the request and follow its steps.

**BUILD** (new feature or service)
1. Name the bounded context and the subdomain type; pick the depth with the proportionality table.
2. State the use case in words: actor, input, output, business rules, side effects, expected failures. One use case = one verb (`PlaceOrder`, `CancelOrder`), never an `OrderService` with fifteen methods.
3. Model the domain: value objects and aggregates with invariants enforced at construction; separate "create new" from "rehydrate from storage". Raise or return domain errors for rule violations.
4. Define outbound ports from the use case's point of view: only the methods it needs, domain types in and out.
5. Write the use case: ports injected through the constructor (or parameters), plain input DTO in, plain output DTO out, orchestration only, transaction boundary decided here.
6. Test the use case with in-memory fakes before any adapter exists.
7. Write the inbound adapter for the detected framework: parse and validate the request shape, map to the input DTO, call the use case, map the result or error to the response. Nothing else.
8. Write the outbound adapters: map between domain and persistence/wire models inside the adapter; translate infrastructure errors into application errors.
9. Wire everything in the composition root; add adapter integration tests and the architecture test.

**REVIEW** (existing code)
Report findings ordered by severity, each one as:
`[severity] path:line — rule broken — consequence — smallest fix`.
Severities: `blocker` (dependency rule broken, business rule in the wrong layer, data leak), `major` (missing boundary test, leaky port, error mapping scattered), `minor` (naming, idiom, style). Do not propose rewrites when a local fix is enough. Finish with what is already well done, in one or two lines.

**MIGRATE** (legacy or framework-coupled code)
Never rewrite big-bang. Use the strangler approach:
1. Pick one vertical slice with high change pain and low blast radius.
2. Pin current behavior with characterization tests at the HTTP level.
3. Extract a use case with explicit input/output types; make the old controller delegate to it.
4. Put existing infrastructure calls behind outbound ports (the legacy code becomes the first adapter).
5. Move orchestration and rules inward; replace adapter internals later.
6. Keep a reversible switch (route or flag) until the new path is verified. Repeat slice by slice.

## Rules by layer

**Domain**
- Enforce invariants in constructors or factories so an invalid object cannot exist. Rehydration from storage skips creation rules but not structural validity.
- Model money, ids, emails and quantities as value objects or at least dedicated types; avoid primitive obsession. Never use binary floating point for money.
- Keep behavior with the data that owns it (tell, don't ask). A rule that spans two aggregates or needs a lookup belongs in a domain service or the use case.
- No framework annotations, decorators or ORM mapping in domain classes. Persistence and JSON mapping belong to adapters.

**Application**
- One public entry point per use case. Input and output are plain, serialization-agnostic DTOs.
- Validate **business invariants** here or in the domain; validate **request shape** (types, required fields, ranges, formats) in the inbound adapter. Both validate, for different reasons.
- Depend on port interfaces only. Never import an ORM session, an HTTP client, a request object or a framework-specific logger type.
- Do not return persistence models. Expect application/domain errors from ports, never adapter exceptions.
- No `if provider == "stripe"` branching: that is a strategy or a different adapter.

**Inbound adapters**
- Thin: no business rules, no SQL, no calls to outbound adapters. An `if` that encodes a business decision moves inward.
- Own the request/response DTOs and their mapping. Never expose domain entities or persistence models in responses; the API contract must evolve independently.
- Translate errors in **one central place** (exception handler, middleware, error mapper), not with try/catch in every route. See `references/rest-api.md`.
- Authentication, request ids, rate limiting, CORS and body size limits are adapter or middleware concerns.

**Outbound adapters**
- Implement one port each (or a small cohesive set). Map to and from the domain inside the adapter.
- Own retries, timeouts, circuit breaking, vendor pagination, SQL and schema. Set a timeout on every network call.
- Translate technology errors (unique violation, timeout, vendor 404) into the application's error vocabulary, keeping the original as the cause.

**Composition root**
- Single, explicit and auditable. Load and validate configuration at startup and fail fast; inject values instead of reading environment variables inside adapters or use cases.
- Open long-lived resources (pools, clients) at startup and close them on graceful shutdown.

## Error model

Three families, mapped once at the inbound edge:

| Family | Examples | Typical HTTP |
|---|---|---|
| **Validation** (request shape) | missing field, wrong type, out of range | 400 (or 422, consistently) |
| **Business** (expected outcomes) | not found, already paid, insufficient stock, version conflict | 404, 409, 422 |
| **Infrastructure / unexpected** | database down, upstream timeout, bug | 500, 502, 503, 504 with a generic body; details only in logs |

Domain and application code never know status codes. Every business error carries a stable machine-readable `code` (`ORDER_ALREADY_PAID`) so clients never parse messages. Never swallow errors, and log once, at the edge that handles the error, not at every layer.

## Transactions and consistency

- The transaction boundary is the **use case**: a Unit of Work port, a decorator around the use case, or a declarative transaction at the application boundary (a documented trade-off when it adds a framework annotation to the application layer).
- Modify one aggregate per transaction; reference other aggregates by id.
- Never call a remote system inside a database transaction and assume atomicity. Publish events reliably with the **outbox** pattern.
- Make retried operations safe: idempotency keys for non-idempotent commands, optimistic concurrency (version / ETag) for updates.

## Cross-cutting concerns

- **Logging**: structured, with a correlation id; never secrets or full PII.
- **Configuration**: typed, validated at startup, injected.
- **Time and ids**: injected where behavior or tests depend on them.
- **AuthN/AuthZ**: authenticate in an inbound adapter; pass a plain principal to the use case; enforce resource-level permissions in the use case or a domain policy, not only in the route.
- **Observability**: health and readiness endpoints, metrics and tracing in adapters or decorators, never inside domain logic.

## Integrating a framework without a dedicated guide

When the detected framework has no file in `references/frameworks/`, answer these five questions from its documentation and the existing code, then apply the rules above:

1. **Routing** — where are handlers declared? That is the inbound adapter; keep it thin.
2. **Dependency injection** — is there a container? It is the composition root; bind ports to adapters there and keep container APIs out of the domain and use cases.
3. **Error handling** — how is a global error handler registered? Map domain/application errors to Problem Details there, once.
4. **Persistence** — is the ORM Active Record (models save themselves) or Data Mapper? With Active Record, the ORM model is a persistence detail inside the outbound adapter and is always mapped to the domain.
5. **Lifecycle and transactions** — where do startup, shutdown and request-scoped resources live? Open resources there and expose transactions to the application only through a port or a decorator.

## Anti-patterns to flag and fix

- Domain objects importing ORM models, web framework types or SDK clients; one class used as ORM entity, domain object and API response at once.
- Controllers containing business rules, transactions or SQL; use cases reading request, response or queue metadata objects.
- Adapters calling each other directly instead of going through the application layer.
- Anemic domain plus a giant `*Service`; `manager`, `helper`, `util` classes holding business logic.
- Hidden global singletons, service locators, static access to the database or configuration.
- Ports shaped like the vendor SDK, or one interface per class "just in case".
- Mapping layers with no boundary purpose (DTO copies of DTOs within the same layer).
- Catching a generic exception and returning 200 or an empty result; leaking stack traces to clients.
- Tests that need a running database to verify a business rule.
<!-- END GENERATED: shared/core.md -->

## TypeScript essentials

These apply in every file; `references/idioms.md` has the details and examples.

- **Ports are `interface`s** in the application layer; adapters and fakes `implements` them. Frameworks that need runtime tokens (NestJS) bind interfaces to `Symbol` tokens in the adapter layer.
- **Value objects are classes with a private constructor** and a validating static factory (`Money.of`). Aggregates expose getters and intention-revealing methods; `create` applies rules, `rehydrate` loads stored state.
- **Ids are branded types** (`type OrderId = string & { readonly __brand: "OrderId" }`), closed sets are string-literal unions, domain events are a discriminated union, invariants use types where cheap (a non-empty tuple for order lines).
- **Money is integer minor units** (or a decimal library), never a float. Time comes from an injected `Clock`.
- **Errors are classes extending `Error`** with a stable `code`, grouped in families (`DomainError`, `NotFoundError`, `ConflictError`) that one HTTP error handler maps by `instanceof`. Keep the cause: `new ConflictError(message, { cause })`.
- **The unit of work takes a callback**: `uow.run(async ({ orders }) => ...)` commits when the callback resolves and rolls back when it rejects, which maps directly onto Prisma, TypeORM and Drizzle transactions.
- **Zod schemas, ORM types and framework request objects stay in adapters.** Use cases take and return plain readonly types.
- **Strict compiler**: `strict`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax` (`import type` for types), no `any` (use `unknown` at the edges and narrow). Named exports, no barrel files that re-export whole layers.
- **Tooling:** `tsc --noEmit`, the project's linter/formatter, Vitest (or Jest), and dependency-cruiser to enforce the dependency rule in CI.

## Reference index

| Read | When |
|---|---|
| `references/idioms.md` | Always: naming, layout, base `PlaceOrder` slice, composition root, architecture check |
| `references/testing.md` | Writing or reviewing tests: Vitest, fakes, contract suites, containers |
| `references/frameworks/nestjs.md` | NestJS modules, providers and tokens, controllers, exception filter |
| `references/frameworks/express.md` | Express 5 router, error middleware, app factory |
| `references/frameworks/fastify.md` | Fastify plugins, error handler, `inject` tests |
| `references/persistence/prisma.md` | Prisma 7 client, repositories, interactive transactions, migrations |
| `references/persistence/typeorm.md` | TypeORM entity schemas, repositories, transactions, migrations |
| `references/persistence/drizzle.md` | Drizzle schema, repositories, transactions, drizzle-kit migrations |
| `references/recipes/crud-thin-slice.md` | Supporting subdomain with no real business rules |
| `references/recipes/aggregate-state-machine.md` | Aggregate with guarded state transitions and optimistic concurrency |
| `references/recipes/external-api-acl.md` | Integrating a third-party API (payments, shipping) behind an Anti-Corruption Layer |
| `references/recipes/domain-events-outbox.md` | Domain events, integration events and reliable publishing |
| `references/recipes/read-model-pagination.md` | List endpoints, read ports, cursor pagination |
| `references/recipes/idempotent-command.md` | `Idempotency-Key` for commands that must not run twice |
| `references/ddd.md` | Subdomains, bounded contexts, context mapping, aggregate design |
| `references/rest-api.md` | HTTP contract: status codes, Problem Details, pagination, versioning, security |
| `references/solid-patterns.md` | SOLID, design patterns and when to skip them, clean code, smells |
| `references/testing-strategy.md` | What to test at each boundary, fakes vs mocks, CI order |

<!-- BEGIN GENERATED: shared/checklist.md -->
## Final checklist

- [ ] Domain and application import no framework, ORM, HTTP or SDK types (an architecture test enforces it).
- [ ] The bounded context and subdomain type are clear, and the depth matches the proportionality table.
- [ ] Aggregates protect their invariants; value objects replace primitives that carry rules.
- [ ] Every external dependency sits behind an outbound port named for a capability.
- [ ] Each use case has explicit input/output types and one responsibility.
- [ ] Adapters map to and from the domain and never leak persistence or vendor models into the API.
- [ ] Request shape validated at the edge; business invariants enforced in the domain or use case.
- [ ] Errors translated once at the inbound edge, with stable codes and correct statuses.
- [ ] Transaction boundary at the use case; no remote call assumed atomic with the database.
- [ ] Wiring is explicit in a composition root; configuration validated at startup; graceful shutdown handled.
- [ ] Naming, formatting and tooling follow the language conventions and the project's existing configuration.
- [ ] Tests exist per boundary; use cases tested with fakes; formatter, linter, type checker and tests were run and their result reported.
- [ ] No abstraction was added without a nameable reason.
<!-- END GENERATED: shared/checklist.md -->
