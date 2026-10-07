---
name: cloudflare-backend
description: "DDD and CQRS backends on Cloudflare Workers: thin entrypoints, message bus, unit of work, outbox, idempotency, and rules for D1, Postgres, Queues, Workflows, and Durable Objects. Use for server code, bindings, or `wrangler.jsonc`."
license: Apache-2.0
---

# Backend Architecture — Clean Backends on Cloudflare Workers

Projects preserve clean dependency direction, explicit boundaries, testability, and one composition root, but may use DDD or hexagonal architecture. Detect and follow the existing architecture; do not force DDD terminology onto ports-and-adapters code. Sections marked `[detect: …]` name evidence to read before editing. Select reference code by its contract and responsibility, not repository age. Existing RPC envelopes are compatibility cases, not the default for a bare-value server function.

When Effect is present, treat `Context.Tag` services as ports, Layers as adapter constructors and dependency composition, and Effects as typed programs. Keep pure domain logic pure, provide Layers at the composition root, and run Effects only at entrypoint/runtime boundaries. Do not create hidden global runtimes or duplicate error logging.

Backends live inside the TanStack Start app: `apps/<app>/src/server/`. No separate worker app.

## Layering

- **Domain** — entities, value objects, pure business logic. Zero dependencies on other layers, framework-agnostic.
- **Application** — use cases and handlers. Orchestrates domain models and outbound ports. Depends on Domain and application-owned port contracts.
- **Infrastructure** — DB, external APIs, queues, storage, and subprocess adapters. Implements outbound ports without owning use-case sequences.
- **Entrypoints** — receive external input or control across the system boundary and translate it into application calls.

```
server/
├── entrypoints/        # functions/ (server fns), queue/, scheduled/, middleware/ — transport only
├── application/        # message bus, handlers, registry
├── domain/             # messages/, models/, services/, errors/ — pure, framework-free
└── infrastructure/     # app-deps.ts, persistence/, auth/, resilience/, external clients
```

Dependencies flow inward. Domain imports nothing from other layers — including `Db*` row types from persistence schemas.

> Standard, not fully practiced: repository interfaces belong in domain (older code keeps them in `infrastructure/persistence/repositories/interfaces.ts`). Apply to new code; don't churn existing files unprompted.

## Identify System Entrypoints

An entrypoint is where external input or control crosses a defined system boundary.

Name the boundary, the external caller or runtime, and the receiving operation.
Derive entrypoints from that invocation contract; use code to locate them.

Examples: Worker `fetch` → API routes/server functions, `scheduled`, and `queue`; Durable Object RPC, `fetch`, and `alarm`; Workflow `run` and external events; local CLI input.

A webhook uses an API route.
Internal SDK callbacks and Workflow step callbacks do not create another system entrypoint.

## Bootstrap Dependencies

Code entrypoints initialize or register the system, such as `server.ts` or a class constructor.
Operational entrypoints receive external invocations.

Build dependencies at the scope that owns their lifetime: invocation, instance, or transaction.
Pass them through context or explicit arguments.

For example, `src/server.ts` calls `createAppDeps(env, ctx)` for each HTTP, queue, and scheduled invocation.
`infrastructure/app-deps.ts` owns the dependency graph.

Keep construction separate from application policy.
Inner services receive dependencies; they do not construct providers or retrieve runtime bindings.

## DI — AppDeps Composition Root

Keep application wiring in `infrastructure/app-deps.ts`; bootstrap code supplies its runtime inputs.

- `createAppDeps(env, ctx)` builds repos, services, gateways; services lazily memoized with `once()`.
- Bootstrap supplies `AppDeps` through request context or the project's composition middleware: `context.deps.services.messageBus()`.
- Handler signature: `(message, deps: AppDeps) => Promise<TResult>`.
- `once()`-memoized services must not capture transaction-scoped repos — they outlive any tx.
- **Every entry is a client for something outside the process** — database, queue, Durable Object, Workflow, external API. Group them: `services` (clients wrapped in our interfaces, e.g. `queueClient(): IQueueClient`), `clients` (raw SDK clients), `dos` (Durable Object clients), `workflows`. Never a raw binding type in the interface.
- **A rule is not a dep, data is not a dep.** A policy object (`DestinationPolicy`, `RateTable`, allow-lists, config-fed decisions) belongs in the domain as a pure function; the handler reads its inputs from the database via `readDb` and calls it. Named after a message kind (`commands()`) is always wrong — name the capability.

This example assumes the application returns a bare value and uses the existing throw-based contract.
For internal Result handlers, use the established adapter conversion described under Error Handling.

```typescript
// The shared function middleware owns error conversion.
export const createProduct = createServerFn({ method: 'POST' })
  .middleware([depsMiddleware, requireAuth])
  .validator(createProductSchema)
  .handler(async ({ data, context }) => {
    const result = await context.deps.services.messageBus().handle(
      createCommand('CreateProduct', { ...data, userId: context.user.id }),
    )
    return result
  })
```

## Error Handling

This skill owns transport contracts, error conversion, logging ownership, and external retries.
Use [typescript-standards](../typescript-standards/SKILL.md) for internal Result types, schemas, and general module design.

Before editing a server function or stub:

1. Read its caller, shared contracts, and a comparable existing function.
2. Read `src/start.ts` and the registered error, authentication, and CSRF middleware.
3. Read the error payload module and any installed helper used by that middleware.
4. Confirm the success type, failure channel, and logging owner.
5. State material differences between the specification, reference code, and current project.

Read [transport contracts](references/transport-contracts.md) for server functions, HTTP, Durable Object RPC, or WebSockets.
Read [error paths and retries](references/error-paths.md) when changing failure behavior or an external client.
Read [RPC compatibility](references/rpc-compatibility.md) only when the existing boundary uses a result envelope.

Current server functions return bare values. Shared middleware converts thrown failures to plain tagged payloads once.
An internal Result becomes success or a typed throw at the adapter; it does not require a wire envelope.
Reuse global middleware registration. Do not install a second error boundary in each function.
Preserve Router redirects and not-found control flow through the existing middleware.

For a stub, use the project's unimplemented helper and declare the intended return type.
Keep required validation and authentication. Do not fake success or add production behavior outside the requested scope.

## Entrypoints and Application Orchestration

For every task that writes or reviews an entrypoint, application handler, use case, or service adapter, read [references/entrypoints-and-application.md](references/entrypoints-and-application.md) before proposing or editing code.

Inspect layers in any useful order. Before accepting the design, trace the complete flow across the entrypoint, application, domain, and infrastructure boundaries.

The application flow must be visible at a glance. A typical handler loads data, prepares or decides, calls a capability, persists, and returns. This is a shape, not a required action count. One-step reads are valid. Deep nesting, repeated branches, or a handler that forwards everything to one broad service are warnings that ownership is unclear.

### Entrypoint rule

An operational entrypoint owns boundary work only. Apply the boundary test above before assigning that role.

- **Message-bus architecture:** validate and authorize when required, build or parse a `Command | Query | Event`, await `bus.handle(message)`, then convert the result.
- **Direct-handler architecture:** validate and authorize when required, build typed input, await one application handler, then convert the result.
- Each platform boundary owns its delivery semantics: HTTP responses, queue acknowledgement, or scheduled invocation failures. Workflow orchestration owns durable step configuration.

### Application rule

The application handler is the main orchestrator. It owns use-case policy, plans, ordering, port coordination, transaction boundaries, cleanup or compensation, and useful error behavior.

It does not own transport conversion, framework code, provider commands, SQL, SDK calls, or domain invariants.

Use the forwarding-wrapper test: if removing the handler leaves the same broad service call and result, inspect that service. If it coordinates multiple external capabilities, split those capabilities into ports and move the sequence into the handler. Do not invent steps for a genuine one-port read.

## Business Logic Placement

| Layer | Business logic? |
|---|---|
| Entrypoint | ❌ parse, authorize, dispatch, respond |
| Handler | Orchestration policy only |
| Domain model | ✅ invariants, state transitions |
| Domain service | ✅ cross-entity algorithms |
| Repository | ❌ persistence only |

**Escape hatch ("two gates"):** an entrypoint may call a dedicated service client directly when the operation is transport coordination. The client must expose one narrow capability. Inline use-case logic in entrypoints is never allowed.

---

## Server Mental Model — Every Entrypoint Has the Same Role

```
Message bus:    Entrypoint → Command | Query | Event → Bus → Handler → Domain + Ports
Direct handler: Entrypoint → Typed input → Handler → Domain + Ports
```

An identified operational entrypoint dispatches into the application and converts the result for its external contract. The transport is incidental.

**Rules:**
1. Entrypoints are thin: validate when required → authorize when required → dispatch → convert.
2. Messages are pure data. No methods.
3. Handlers orchestrate. Zero business logic in handlers.
4. Domain is pure. No framework or infrastructure imports.
5. Dependencies flow inward — never the reverse.
6. Repository pattern: interface in domain, implementation in infrastructure.

## Messages — Command / Event / Query

| Type | Handlers | Idempotency | Semantics |
|---|---|---|---|
| **Command** | exactly 1 | `id` claimed in UoW | mutation |
| **Event** | 0..N subscribers | per-subscriber claim | domain fact, fan-out |
| **Query** | exactly 1 | none — no `id` | read, bypasses UoW |

Base message facts:
- `type: 'command' | 'event' | 'query'` discriminant + `name` literal + optional `userId` (observability).
- `id` is `uuid | externalMessageId`. External ids are namespaced provider keys — `stripe:event:evt_123` — giving provider-keyed idempotency for webhooks. Factories (`createCommand(...)`) default the uuid. `[detect base.messages.ts]`: current generation uses `z.uuidv7()` (time-ordered); older uses `z.uuidv4()`.
- `[detect]` message location: shared with client → `packages/core/src/domain/**`; server-only → `apps/<app>/src/server/domain/messages/`.
- Payload IDs use branded schemas (`UserIdSchema`, `ProductIdSchema`); Zod v4 helpers (`z.uuid()`, `z.uuidv7()`, `z.iso.datetime()`).

```typescript
export const createProductSchema = baseCommandSchema.extend({
  name: z.literal('CreateProduct'),
  productName: z.string(),
  userId: UserIdSchema,
})
```

## Registry

One registry file (`application/registry/registry.ts` or `application/handlers/registry.ts`) wires names to handlers; `satisfies CommandRegistry / QueryRegistry` makes the compiler prove exhaustiveness. If the compiler doesn't error when you add a message, it isn't wired.

```typescript
export const COMMAND_HANDLERS = {
  CreateProduct: createProduct,
} satisfies CommandRegistry

export const EVENT_HANDLERS: EventRegistry = {
  ProductCreated: [
    { id: 'project-product-view',  mode: 'state',  handle: projectProductView },
    { id: 'track-product-created', mode: 'effect', handle: trackProductCreated },
  ],
}
```

### State vs effect subscribers — the load-bearing dispatch rule

The species test for every event subscriber: **does it write our DB?**

| Kind | Runs in | Idempotency | For |
|---|---|---|---|
| `state` | its own per-subscriber UoW | receipt keyed by event id (+ subscriber id) | DB writes: projections, denormalizations |
| `effect` | no tx, no claim | idempotency key delegated to the target system | analytics, email, external APIs |

A failing `state` subscriber rolls back only its own UoW. An `effect` subscriber must be safe to re-run — never wrap an effect in a DB claim (claim-then-effect loses the effect on crash; effect-then-claim leaves an orphan window). A subscriber that does both → split it.

`[detect registry.ts]` wiring: newer generation registers subscriber objects `{ id, mode, handle }` and the dispatch machinery opens each state subscriber's UoW; older generation registers plain `(event, deps)` functions, each state subscriber opening its own UoW keyed off the event id.

## Message Bus

Single choke point from typed message to handler; the bus **routes**, it does not open transactions. Event subscribers run in parallel (`Promise.allSettled`) — one failure doesn't abort siblings. Duplicate handling: `DuplicateMessageError` from an event subscriber → swallowed as success; from a command → rethrown to the caller; the queue consumer acks duplicates as skip.

## Unit of Work

**Command handlers open the UoW** (not the bus): `deps.uow.run(messageId, (repos, emit) => …)` — tx-scoped repos plus an `emit` for domain events. Event `state` subscribers get their own per-subscriber UoW (opened per the generation's wiring, above). One atomic scope does, in order:

1. **Claim receipt** — insert `message.id` into `message_receipts`; conflict → `DuplicateMessageError`.
2. **Handler writes.**
3. **Persist emitted events to `message_outbox`** — state change and events commit or roll back together.
4. **Commit.**

`[detect unit-of-work implementation]`:
- **D1**: no interactive transactions — receipt + writes + outbox staged into one `db.batch()`, committed with retry; receipt UNIQUE violation → `DuplicateMessageError`.
- **Postgres**: real tx; Result-based with a rollback bridge (store `Result.err` → `tx.rollback()` → return stored err), branded `Tx` type, events collected via AsyncLocalStorage.

Transaction rules:
- **No cross-boundary I/O inside a tx** — no fetch/queue/R2 while holding a connection (Hyperdrive pool exhaustion).
- One aggregate per tx. Retry the whole UoW at the caller boundary. Never nest UoWs.
- Queries bypass UoW entirely; the read path may skip repositories — query handlers can do inline Drizzle `select({...})` → DTO. The DTO is a product resource, not a row. Do not leak a storage accident. Keep expensive associations off unless the caller asks.

### Outbox relay

Events in `message_outbox` are delivered by a relay, not by the request: a sweep (cron `*/1 * * * *`, or a relay DO alarm draining into Queues — `[detect wrangler.jsonc]`). Post-commit `deps.hooks.onEventsCommitted()` wakes the relay via `waitUntil` as a **latency optimization only** — the sweep is the source of truth; a lost wake loses no events.

## Idempotency

Everything that mutates must be idempotent. Three layers:

1. **Message receipts** — automatic via UoW (above). Safe to retry commands / redeliver events.
2. **External side effects** — pass idempotency keys derived from stable operation properties:
   ```typescript
   await stripe.charges.create({ amount }, { idempotencyKey: `${runId}-${nodeId}` })
   ```
   Webhook-driven messages reuse the provider's key as the message id (`stripe:event:evt_123`).
3. **DB level** — atomic insert, not check-then-insert: `.onConflictDoNothing()` / `.onConflictDoUpdate()`. No TOCTOU window.

## Repositories

Writes and entity reads go through repositories.

- **Closed method list**: `byId` / `findByX` / `insert` / `save` / `delete`. No generic `update(id, fields)`.
- `insert` ≠ `save`: insert fails on existing (`AlreadyExists`); save is version-guarded (`RevisionConflictError` on stale version).
- Choose the insert type for each aggregate before you write the handler. Never check, then insert: two concurrent requests both pass the check.
  - **Created once:** a repeat is a mistake. `insert` fails with `AlreadyExists`, and the caller reports it.
  - **Natural key, repeatable arrival:** the same input must return the same aggregate, such as a file identified by its hash. `insert` runs `ON CONFLICT (key) DO NOTHING RETURNING id`, then reads the existing ID. It returns the ID and dispatches events only for a new row. The handler returns the ID and does not report "new" or "existing".
- Each repository defines one `toDomain(row: DbRow): Entity` mapper for persisted entities.
- `toDomain` builds the entity's plain data and passes it to `Entity.restore(data)`.
- `toDomain` maps field names and flat database rows to nested plain data. It does not validate or parse values.
- When flat database nullability conflicts with a domain union, use a narrow cast before `restore`; the constructor enforces domain invariants.
- Writes map `entity.toPlainObject()` to the database insert or update shape inside the repository.
- Migrate old database values. Do not keep old-value conversion in `toDomain` after the migration.
- **Drizzle, never raw SQL in handlers.** Raw SQL only when Drizzle can't express the query — documented in the repo.

```typescript
export class ProductRepository implements IProductRepository {
  async byId(id: ProductId, userId: UserId) {
    const row = await this.db.query.product.findFirst({
      where: and(eq(product.id, id), eq(product.userId, userId)),
    })
    if (!row) return Result.err(new EntityNotFoundError('Product', id))
    return Result.ok(this.toDomain(row))
  }

  private toDomain(row: DbProduct): Product {
    return Product.restore({
      id: row.id,
      name: row.name,
      state: { status: row.status },
    })
  }
}
```

Drizzle table definitions use the **array** return for indexes:

```typescript
sqliteTable('t', { ... }, (t) => [index('idx').on(t.col)])
```

## Domain Entities

Entity pattern only where there's identity + state transitions + invariants; plain types otherwise.

- Base `Entity`: `addEvent` / `collectEvents` / `clearEvents`; serialization via `toPlainObject()`.
- A persisted entity exposes `toPlainObject(): EntityData` and `static restore(data: EntityData): Entity`.
- `restore` accepts the exact type that `toPlainObject` returns.
- Use a private constructor. Validate key business invariants in the constructor or in one shared assertion that it calls.
- Do not repeat Zod validation from HTTP or I/O boundaries in the domain model.
- Do not repeat database type, nullability, or constraint checks in the domain model.
- Domain assertions augment boundary validation with rules that the type and database schema cannot express.
- `create`, `restore`, and state transitions must use the same invariant validation.
- `restore` rebuilds domain state without emitting domain events.
- Domain entities must not import database types or expose `fromPersistence` and `toPersistence` methods.
- `static create(...)` — current generation returns `Result<Entity, ValidationError>` (throw = bug only); older generation throws on invariant violation.

```typescript
export class Product extends Entity {
  private constructor(private readonly data: ProductData) {
    super()
    assertValidProduct(data)
  }

  static restore(data: ProductData): Product {
    return new Product(data)
  }

  toPlainObject(): ProductData {
    return { ...this.data }
  }
}
```

Mutations guard their transitions:

```typescript
markLive(): Result<void, PlaybookEditError> {
  if (this.status === 'archived') return Result.err(new PlaybookEditError('archived'))
  this.status = 'live'
  this.updatedAt = new Date()
  return Result.ok()
}
```

## `/core` Package Boundary

`packages/core` has two entry points — `index.ts` (full, server) and `client.ts` (browser-safe). Browser code imports `@<scope>/core/client` ONLY; the subpath is the firewall against pulling server-only modules into the bundle.

Core contains browser-safe contracts and domain types, plus explicitly separated server infrastructure where the project uses it. A wire-envelope module is required only by an existing envelope contract. **DB schema and migrations live in the app** (`apps/<app>/src/server/infrastructure/{db|persistence}/`), not in core.

## Published contracts

Classify the surface before you change a shape.

| Surface | Examples | Break rule |
|---|---|---|
| Internal | TanStack server functions that ship with the web client | Coordinated break allowed in the same deploy |
| Published | MCP tool input/output, extension contract, HTTP `/api`, outbound webhook payload, `@<scope>/core/client` schemas other clients import | Overlap, warn, then remove |

A published shape may change. It may not vanish in the same change that replaces it.

1. Ship the new field, tool, or shape next to the old one.
2. Mark the old one deprecated where a machine can see it: `Deprecation` + `Sunset` on HTTP, `deprecated: true` on an MCP tool or argument, `@deprecated` on an exported symbol.
3. State when it goes away (date, release, or no traffic for N days).
4. After that window, delete the old one in its own change.

Keep one business core. Fill both shapes from the same handler. Do not fork `/v1/` handlers. Do not keep dual fields forever.

A silent rename is forbidden. Keep the old path only if a client you cannot reach still depends on it.

Published rules:

- Consumers must ignore unknown fields.
- The DTO hides storage accidents. Do not publish a persistence shape.
- Expensive associations are off by default. The caller opts in.
- Any operation exposed to code (MCP, HTTP, extension) needs a rate limit. Tighter limits on expensive work. Return `Retry-After` on 429. Keep a per-customer kill switch.

### Pagination

- Small user-scoped lists: `?page=1&limit=20` (max 100) → `{ items, page, limit, total, hasNextPage, hasPrevPage }`.
- Unbounded collections (job history, audit, MCP list tools): cursor + `next` token. Query is `WHERE id > cursor ORDER BY id LIMIT n`. Never offset those lists.

---

## Platform Patterns

### Queue consumers

Class-based consumer in `entrypoints/queue/`:
- Per-message Sentry isolation scope.
- `classifyForRetry` — typed errors decide retry vs park; explicit exponential backoff with caps.
- `max_retries` + DLQ configured in wrangler.jsonc; poison messages parked; duplicates acked as skip.

### Cron / scheduled

- Cron registry (`entrypoints/scheduled/cron-registry.ts`) maps expressions → handlers; includes the outbox relay sweep.
- **Cron does not retry.** Each unit of work catches its own errors; one bad item must not kill the sweep.
- Local trigger: `curl "http://localhost:8787/cdn-cgi/handler/scheduled"`.

### Cloudflare Workflows

- One unit of work per step — steps are the retry boundary.
- **Fetch-then-record**: external call in one step, outcome recorded in the next; a retried step must never redo a committed effect.
- Intent → effect → outcome: mint durable intent (DB row) before the external effect.
- Map non-retryable typed errors to `NonRetryableError`; internal vs external step configs carry the retry policies.

### Durable Objects

In use: rate limiting (`RateLimiterDO`), outbox relay, agents/gates (Agents SDK), container supervisors. Wrap with `Sentry.instrumentDurableObjectWithSentry(...)`.

Migrations: each change = new migration, unique tag, append-only — never edit or remove shipped entries. **Default `new_sqlite_classes`** for new DOs; `new_classes` only with a documented reason (legacy DOs exist — don't migrate them unprompted). Use the new class name in code after rename; never manually create destination classes for rename/transfer.

```jsonc
"migrations": [
  { "tag": "v1", "new_sqlite_classes": ["SessionDO"] },
  { "tag": "v2", "renamed_classes": [{"from": "OldDO", "to": "NewDO"}] }
]
```

### Containers

Reference usage: a Python service (uv/pyproject) in its own app dir; the Start app's wrangler `containers` entry points at its Dockerfile with a supervising DO (`class_name`), Sentry-instrumented. Linux/amd64 only; images upload to Cloudflare Registry.

### Workers KV

Before adding, reviewing, or tuning a KV key, read [workers KV](references/workers-kv.md): long `cacheTtl` on keys that never change, versioned keys, shared keys, one read per request, write at publish time.

### Remote bindings

`"remote": true` on a binding connects local dev to deployed resources (billing applies). Supported: AI, D1, KV, R2, Queues, Vectorize, Workflows. Local-only: Durable Objects, Hyperdrive, Rate Limiting. Vitest always uses local simulations.

### Typegen

Run the project's `cf-typegen` script after configuration or binding changes. Never edit generated types.
Plain `wrangler types` combines configured environments into strict unions and emits `Cloudflare.<EnvName>Env`.
Use `--env` only when generating for one environment intentionally. Never hide differences with `--strict-vars=false`.
For cross-Worker RPC, pass the caller and every bound Worker configuration with repeated `-c` flags.
Keep required binding names in each environment so Wrangler resolves `Service<typeof Entrypoint>` without casts.

### Local Explorer API

Cloudflare Vite exposes local resources at `http://localhost:<project-port>/cdn-cgi/explorer/api`.
Discover the active project URL from configuration or process output. Never assume a shared port.
Fetch the OpenAPI schema from that API root before using it. Use only documented operations.

Read the `cloudflare`, `durable-objects`, `wrangler`, or `workers-best-practices` skill for platform changes in its scope.

### Deployment

**Workers, never Pages.** TanStack Start apps use `@cloudflare/vite-plugin`: `CLOUDFLARE_ENV=<env> vite build` resolves the env from `wrangler.jsonc` and generates a flattened `dist/server/wrangler.json` with computed `main`/`assets` — those fields are not hand-written.

Env names and deploy scripts are per-project — read `wrangler.jsonc` + `package.json` (e.g. `dev/preview/prod`, `dev/staging/test/prod`; `pnpm deploy` targets the pre-prod env, `pnpm deploy:prod` targets prod, both run migrations first).

---

## Database Workflow

Before a schema change, migration, or database query, read [database workflow](references/database-workflow.md). It covers D1 and Postgres detection, migration commands, migration rules, and constraint ownership.

## Testing

Before you write, review, or speed up a Worker, binding, or database test, read [Workers testing](references/testing.md).

## Security and operations

For Turnstile setup, repair, or CAPTCHA migration, use the official [Turnstile Spin skill](https://github.com/cloudflare/skills/tree/main/skills/turnstile-spin) first.
Start with its agent workflow, not manual setup or the dashboard.

For authentication, authorization, public inputs, uploads, or secret handling, read [security](references/security.md).
For backend performance, logging, metrics, or alerts, read [operations](references/operations.md).
To measure the speed or failures of a deployed Worker, read [measure a Worker](references/measure-worker.md).

### Secrets — dotenvx

- Encrypted `.env` files are committed; private keys (`.env.keys`) are gitignored. Scripts run under `dotenvx run --`.
- wrangler `secrets.required` manifests declare what prod needs.
- This is the secrets mechanism for these projects — it supersedes `.dev.vars`.

---

## Standards Not Yet Practiced (apply to new code; don't churn existing)

- **List pagination** on new list endpoints. Use the Published contracts rule: offset envelope for small user-scoped lists; cursor + `next` for unbounded collections.
- Repository interfaces in domain.
- Branded IDs on every message payload (legacy payloads have plain strings).

## MCP Server Config

MCP tool input and output schemas are published contracts. Change them with overlap, warn, then remove.

```bash
claude mcp add --transport http <name> <url> --header "Authorization: Bearer <token>"
```

Windows npx servers need the `cmd /c` wrapper:
```json
{ "command": "cmd", "args": ["/c", "npx", "-y", "@package/name"] }
```
