---
name: arc-framework
description: "ARC framework knowledge base for building business-model-first applications with CQRS and Event Sourcing. Use when writing code with @arcote.tech/arc, creating commands, events, views, listeners, routes, or working with ArcContext, ArcElement types, React hooks (useQuery, useCommands), Form components, or Bun host server. Use when user mentions ARC framework, arcote, or narzedziadlatworcow."
---

# ARC Framework

ARC is a full-stack TypeScript framework implementing **Business Model First** — code organized around business model, not technology. Built on **CQRS** (Command Query Responsibility Segregation) and **Event Sourcing** patterns.

**Monorepo packages:**
- `@arcote.tech/arc` (core) — types, model, events, storage
- `@arcote.tech/arc-react` (react) — hooks, Form, Provider
- `@arcote.tech/arc-host` (host) — Bun HTTP + WebSocket server
- `@arcote.tech/arc-cli` (cli) — `arc dev` / `arc build`

**Runtime:** Bun. **Deps:** RxJS, Mutative (immutable state).

## Architecture Overview

```
Client (React)                         Server (Bun :5005)
┌──────────────────────┐               ┌──────────────────────────┐
│ LiveModelProvider    │               │ hostLiveModel(ctx, opts) │
│ ├─ useQuery()        │──── HTTP ────▶│ ├─ /command/:name POST   │
│ ├─ useCommands()     │               │ ├─ /query POST           │
│ └─ Form              │◀── WebSocket─│ ├─ /route/* ANY          │
│    RemoteModelClient │               │ └─ /ws (sync broadcast)  │
└──────────────────────┘               │    Model (local)         │
                                       │    ├─ ArcContext          │
                                       │    ├─ EventPublisher      │
                                       │    └─ MasterDataStorage   │
                                       └──────────────────────────┘
```

## Type System (Elements)

ARC has its own schema system (like Zod). Every element provides `validate()`, `serialize()`, `deserialize()`, `parse()`, `toJsonSchema()`.

```typescript
import { string, number, boolean, date, id, object, array, or, stringEnum, record } from "@arcote.tech/arc"

// Primitives
const name = string().minLength(1).maxLength(100)
const age = number().min(0).max(150)
const active = boolean()
const mustAgree = boolean().hasToBeTrue()
const created = date().after(new Date("2020-01-01"))

// ID — auto-generates hex timestamp + 16 random hex chars
const userId = id("UserId")
const customUserId = id("UserId", () => crypto.randomUUID()) // custom generator

// Object schema — like Zod's z.object()
const userSchema = object({
  id: userId,
  name: name,
  email: string().email(),
  age: number().optional(),
})

// Array, Union, Enum
const tags = array(string()).minLength(1).nonEmpty()
const status = stringEnum("active", "inactive", "banned")  // spread args, NOT array
const idOrEmail = or(id("UserId"), string().email())  // spread args, NOT array

// Object utilities
const extended = userSchema.merge({ role: string() }) // merge takes raw shape
const patch = userSchema.partial()   // all fields optional
const fieldNames = userSchema.keys() // typed key array
const picked = userSchema.pick("name", "email")
const omitted = userSchema.omit("id")
```

**Full type reference:** See `references/type-system.md`

## ArcContext (DI Container)

Context registers all domain elements and provides type-safe access:

```typescript
import { context } from "@arcote.tech/arc"

const appContext = context([
  userCreatedEvent,
  userView,
  createUserCommand,
  getUserRoute,
  onUserCreatedListener,
])

// Type-safe element lookup
const el = appContext.get("userCreated")

// Compose contexts (supports lazy imports & conditionals)
const fullContext = appContext.pipe([
  NOT_ON_BROWSER && serverOnlyElement,
  ONLY_BROWSER && browserOnlyElement,
  () => import("./other-context"),
])
```

## Commands (Write Side)

Commands mutate state. They fork DataStorage, run the handler, then merge on success.

```typescript
import { command, object, string, id } from "@arcote.tech/arc"

const createUser = command("createUser")
  .use([userCreatedEvent])           // required context elements
  .withParams({                      // input schema (raw shape or ArcObject)
    name: string().minLength(1),
    email: string().email(),
  })
  .withResult({ id: id("UserId") }) // output schema (spread args for union results)
  .public()                          // accessible from client
  .handle(async (ctx, params) => {
    const newId = userId.generate()
    await ctx.get(userCreatedEvent).emit({
      userId: newId,
      name: params.name,
      email: params.email,
    })
    return { id: newId }
  })
```

**Command execution flow:**
1. Fork DataStorage (transaction isolation)
2. Execute handler
3. Run sync listeners (same transaction — rollback on failure)
4. Merge fork to master (DB updated)
5. Run async listeners (separate forks, parallel, errors don't break command)

## Events (Immutable Facts)

Events are stored immutably in a single `events` table with columns: `id` (PK), `type`, `payload`, `createdAt`.

```typescript
import { event, object, string, id } from "@arcote.tech/arc"

const userCreated = event("userCreated", object({
  userId: id("UserId"),
  name: string(),
  email: string(),
}))
  .auth(authCtx => ({
    read: true,
    write: authCtx.role === "admin",
  }))
```

Events are emitted inside command handlers via `ctx.get(eventElement).emit(payload)`.

## Views (Materialized Projections)

Views are read-optimized projections built from events. They support replay for reinitialization.

```typescript
import { view, id, object, number } from "@arcote.tech/arc"

const userStats = view("userStats",
  id("userId"),
  object({ totalPosts: number(), totalLikes: number() })
)
  .use([postCreatedEvent, postLikedEvent])
  .version(1)
  .handleEvent(postCreatedEvent, async (ctx, event) => {
    const existing = await ctx.findOne({ userId: event.payload.userId })
    if (existing) {
      await ctx.modify(existing._id, { totalPosts: existing.totalPosts + 1 })
    } else {
      await ctx.set(event.payload.userId, { totalPosts: 1, totalLikes: 0 })
    }
  })
  .handleEvent(postLikedEvent, async (ctx, event) => {
    const existing = await ctx.findOne({ userId: event.payload.userId })
    if (existing) await ctx.modify(existing._id, { totalLikes: existing.totalLikes + 1 })
  })
```

## Listeners (Side Effects)

React to events — sync (transactional) or async (fire-and-forget).

```typescript
import { listener } from "@arcote.tech/arc"

const onUserCreated = listener("onUserCreated")
  .use([welcomeEmailCommand])
  .listenTo([userCreatedEvent])
  .async()                              // runs after commit
  .handle(async (ctx, event) => {
    // Commands return callable functions, NOT objects with .execute()
    await ctx.get(welcomeEmailCommand)({
      email: event.payload.email,
    })
  })
```

## Translator (Event-to-Event Mapping)

```typescript
import { translate } from "@arcote.tech/arc"

const translator = translate(userCreatedEvent, welcomeEmailEvent,
  (event) => ({ email: event.payload.email, template: "welcome" })
)
```

> **Note:** The current implementation has a known issue where `ctx.get(from)` is used instead of `ctx.get(to)` — verify behavior when using translators.

## Routes (HTTP Handlers)

```typescript
import { route } from "@arcote.tech/arc"

const usersRoute = route("users")
  .use([userView])
  .path("/api/users/:id")
  .public()
  .handle({
    GET: async (ctx, req, params, url) => {
      const user = await ctx.get(userView).findOne({ _id: params.id })
      return new Response(JSON.stringify(user))
    },
  })
```

## Model (API Layer)

```typescript
import { Model, RemoteModelClient } from "@arcote.tech/arc"

// Server-side (local)
const model = new Model(appContext, dataStorage)
const authCtx = { userId: "admin" }
const result = await model.query(q => q.userStats.find({}), authCtx)
const { id } = await model.commands(authCtx).createUser({ name: "Jan", email: "jan@example.com" })

// Client-side (remote)
const remoteModel = new RemoteModelClient(appContext, "http://localhost:5005", "web", onError)
```

## React Integration

```typescript
import { reactModel } from "@arcote.tech/arc-react"

// reactModel returns an array, NOT an object — use array destructuring
const [
  LiveModelProvider,
  LocalModelProvider,
  useQuery,
  useRevalidate,
  useCommands,
  query,          // imperative query function
  useLocalModel,
  useModel,
] = reactModel(appContext, { remoteUrl: "http://localhost:5005" })

// Provider — note: token and catchErrorCallback, not authToken/onError
<LiveModelProvider client="web" token={jwt} catchErrorCallback={onError}>
  <App />
</LiveModelProvider>

// Query hook — returns [data, loading]. Args: queryFn, dependencies[], cacheKey?
const [users, loading] = useQuery(q => q.userView.find({}), [], "users")

// Commands hook
const commands = useCommands()
await commands.createUser({ name: "Jan", email: "jan@example.com" })

// Revalidation
const revalidate = useRevalidate()
await revalidate("users")
```

**Forms & details:** See `references/react-integration.md`

## Host Server (Bun)

```typescript
import { hostLiveModel } from "@arcote.tech/arc-host"

hostLiveModel(appContext, { db: "app.db", version: 1 })
// Starts on port 5005: /command/:name, /query, /route/*, /ws, /sync
```

**Details:** See `references/host-server.md`

## Data Storage & Database

Two adapters: **PostgreSQL** (via `Bun.SQL`) and **SQLite** (Bun native).

**Where operators:** `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`, `$exists`

```typescript
await store.find({
  where: { age: { $gte: 18 }, status: { $in: ["active", "verified"] } },
  orderBy: { createdAt: "desc" },
  limit: 10,
  offset: 0,
})
```

**Details:** See `references/data-storage.md`

## CLI & Multi-Client Builds

`arc.config.json`:
```json
{ "file": "index.ts", "outDir": "dist", "clients": ["browser", "server", "api"] }
```

Generates compile-time constants dynamically: `BROWSER`, `NOT_ON_BROWSER`, `ONLY_BROWSER`, `SERVER`, etc.

**Details:** See `references/cli-builds.md`

## Key Patterns

1. **Builder Pattern** — All domain elements (Command, Event, View, Listener, Route) use chainable methods returning clones
2. **Proxy Pattern** — `commands()`, `queryBuilder()` return proxies for type-safe dot-notation access
3. **Event Sourcing** — Events are immutable facts; Views are derived projections
4. **CQRS** — Separate read (query) and write (command) paths
5. **Transaction Isolation** — Commands fork DataStorage; merge on success only
6. **Schema-Driven** — Single ArcElement definition drives validation, serialization, DB schema, and JSON Schema

## References

- `references/type-system.md` — Complete ArcElement type reference
- `references/commands-events.md` — Commands, Events, Listeners, Translator deep dive
- `references/views-queries.md` — Views, Queries, Subscriptions
- `references/data-storage.md` — DataStorage architecture, DB adapters, transactions
- `references/react-integration.md` — React hooks, Form system, Provider
- `references/host-server.md` — Bun server endpoints, JWT auth, WebSocket
- `references/cli-builds.md` — CLI commands, multi-client build system
