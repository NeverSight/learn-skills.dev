---
name: nitro-backend
description: Use when creating or modifying backend TypeScript code with Nitro/H3 - new routes, domain modules, branded types, zod validation, storage, middleware, plugins, or any server-side business logic
---

# Nitro Backend Conventions

## Overview

Backend TypeScript organized by **business domain**, with maximum type-safety via `ts-brand` and Zod validation. Business logic lives in **namespaces**, business errors are **string literals** (`as const`), and routes are minimal orchestrators.

Stack: Nitro (H3), TypeScript strict, Bun, Biome, `ts-brand`, `ts-pattern`, Zod.

## 1. Domain Structure

Each business domain is a folder with 3 files. Technical folders (`routes/`, `middleware/`, `plugins/`, `config/`) are separate.

```
server/
├── {domain}/           # One folder per business domain
│   ├── types.ts        # Types + Branded types
│   ├── primitives.ts   # Zod validators → Branded values
│   └── index.ts        # Namespace with business logic
├── config/
│   ├── types.ts
│   ├── primitives.ts
│   └── index.ts        # config() factory
├── routes/             # HTTP endpoints (orchestration only)
│   ├── {resource}.{method}.ts
│   └── {resource}/
│       └── {action}.{method}.ts
├── middleware/          # Per-request processing
└── plugins/            # Nitro lifecycle hooks
```

**Example** — `order` domain:
```
server/order/types.ts
server/order/primitives.ts
server/order/index.ts
server/routes/order/create.post.ts
server/routes/order/[id].get.ts
```

## 2. Branded Types (`types.ts`)

Each semantically distinct value gets its own branded type. This prevents the compiler from confusing an `OrderId` with a `UserId`, even though both are `string`.

```typescript
import type { Brand } from 'ts-brand'

// IDs — always branded
export type OrderId = Brand<string, 'OrderId'>
export type UserId = Brand<string, 'UserId'>

// Constrained values — always branded
export type Email = Brand<string, 'Email'>
export type Price = Brand<number, 'Price'>

// Enums — plain union types, no branding needed
export type OrderStatus = 'pending' | 'shipped' | 'delivered'

// Aggregate
export type Order = {
  id: OrderId
  userId: UserId
  status: OrderStatus
  total: Price
  createdAt: Date
}
```

**Rules:**
- One branded type per semantically distinct value (never a raw `string` for an ID)
- Enums are plain union types — no branding, just `'a' | 'b' | 'c'`
- Aggregates compose branded types
- `import type` for types (never `import`)

## 3. Zod Validation (`primitives.ts`)

Each branded type has a **validator function with the same PascalCase name**. It takes `unknown`, validates with Zod, and returns the branded value.

```typescript
import { make } from 'ts-brand'
import { z } from 'zod'
import type { OrderId as OrderIdType, Email as EmailType, Price as PriceType } from './types'

// Simple validator
export const OrderId = (value: unknown) => {
  const validatedValue = z.uuid().parse(value)
  return make<OrderIdType>()(validatedValue)
}

// With preprocessing (string → number)
export const Price = (value: unknown) => {
  const validatedValue = z
    .preprocess(
      (v) => (typeof v === 'string' ? Number(v) : v),
      z.number().positive(),
    )
    .parse(value)
  return make<PriceType>()(validatedValue)
}

// With normalization
export const Email = (value: unknown) => {
  const validatedValue = z.email().parse(value)
  const normalized = validatedValue.toLowerCase().trim()
  return make<EmailType>()(normalized)
}

// ID generator
export const randomOrderId = () => OrderId(crypto.randomUUID())
```

**Consistent pattern:**
1. Validate with `z.{schema}().parse(value)`
2. Optional: preprocessing or normalization
3. Wrap with `make<Type>()(validatedValue)`

**Import renaming:** types are imported with `as {Name}Type` alias to avoid conflict with the validator function of the same name.

**No branded validators for enums** — use `z.enum()` directly where needed in routes:
```typescript
const status = z.enum(['pending', 'shipped', 'delivered']).parse(query.status)
```

## 4. Business Namespaces (`index.ts`)

All business logic lives in a **TypeScript namespace**. `export` functions are public, without `export` they are private. Never type return values — let the compiler infer them.

```typescript
import { randomOrderId } from '~/order/primitives'
import type { Order } from '~/order/types'

export namespace Orders {
  export const create = async (userId: UserId, total: Price) => {
    const storage = useStorage('orders')
    const id = randomOrderId()
    const order: Order = {
      id,
      userId,
      total,
      status: 'pending',
      createdAt: new Date(),
    }
    await storage.setItem<Order>(id, order)
    return order
  }

  export const getById = async (id: OrderId) => {
    const storage = useStorage('orders')
    const order = await storage.getItem<Order>(id)
    if (!order) return 'not-found' as const
    return order
  }

  export const ship = async (id: OrderId) => {
    const order = await getById(id)
    if (order === 'not-found') return 'not-found' as const
    if (order.status !== 'pending') return 'invalid-status' as const
    await useStorage('orders').setItem<Order>(id, { ...order, status: 'shipped' })
    return order
  }

  // Private — no `export`
  const notifyWarehouse = async (order: Order) => {
    // ...
  }
}
```

**Rules:**
- One namespace per domain, plural name (`Orders`, `Users`, `Products`) or singular for singletons (`Canvas`, `Config`)
- Namespaces compose with each other: `Orders` can call `Users.getById()`
- Storage accessed via `useStorage('bucket')` with generic typing
- Never type return values — let TypeScript infer the return type automatically
- Don't create one-liner functions called only once or twice — inline the code directly

## 5. Error Handling

### Business errors: `as const` (no throw)

Business functions return **string literals** for error cases. TypeScript narrowing handles them cleanly in routes.

```typescript
// In the namespace — return type is inferred automatically
export const withdraw = async (accountId: AccountId, amount: Price) => {
  const account = await getById(accountId)
  if (!account) return 'account-not-found' as const
  if (account.balance < amount) return 'insufficient-funds' as const
  // ...
  return updatedAccount
}
```

**Why:** simple, type-safe, no try/catch needed, narrowing handles everything.

### HTTP errors: `createError` (routes only)

```typescript
if (result === 'account-not-found')
  throw createError({ statusCode: 404, statusMessage: 'Account not found' })
```

### System errors: `throw new Error` (bugs, impossible states)

```typescript
if (items.length === 0) throw new Error('items must not be empty')
```

### Exhaustive pattern matching (`ts-pattern`)

For statuses with multiple branches, `match().with().exhaustive()` guarantees at compile-time that all cases are covered.

```typescript
import { match } from 'ts-pattern'

return await match(order.status)
  .with('pending', async () => { /* ... */ })
  .with('shipped', async () => { /* ... */ })
  .with('delivered', async () => { /* ... */ })
  .exhaustive()
```

## 6. Routes

Routes are **minimal orchestrators**: extract, validate, call, match, respond.

```typescript
import { Orders } from '~/order/index'
import { OrderId } from '~/order/primitives'

export default defineEventHandler(async (event) => {
  // 1. Extract inputs
  const id = getRouterParam(event, 'id')

  // 2. Validate (validator throws if invalid → automatic 400)
  const orderId = OrderId(id)

  // 3. Call business logic
  const order = await Orders.getById(orderId)

  // 4. Match business errors
  if (order === 'not-found')
    throw createError({ statusCode: 404, statusMessage: 'Order not found' })

  // 5. Respond
  return { status: 200, data: order }
})
```

**Nitro input sources:**
- `getQuery(event).key` — query params
- `getRouterParam(event, 'name')` — URL params
- `await readBody(event)` — JSON body
- `await readRawBody(event, false)` — raw bytes (Buffer)

**Route file naming:** `{resource}.{method}.ts` or `{resource}/{action}.{method}.ts`

### Middleware

Lightweight, early-return if not applicable:

```typescript
export default defineEventHandler(async (event) => {
  const { apiKey } = getQuery(event)
  if (!apiKey) return
  await logApiUsage(ApiKey(apiKey))
})
```

### Plugins

Nitro lifecycle hooks:

```typescript
export default defineNitroPlugin((nitroApp) => {
  nitroApp.hooks.hook('request', (event) => { /* ... */ })
  nitroApp.hooks.hook('beforeResponse', (event, { body }) => { /* ... */ })
  nitroApp.hooks.hook('error', (error) => { /* ... */ })
})
```

## 7. Config

Runtime config is a factory that validates values at call time:

```typescript
// server/config/index.ts
export const config = () => {
  const runtimeConfig = useRuntimeConfig()
  return {
    serverUrl: ServerUrl(runtimeConfig.serverUrl),
    apiSecret: ApiSecret(runtimeConfig.apiSecret),
  }
}

// Usage in a route
const { serverUrl } = config()
```

## 8. Principles

| Principle | Application |
|-----------|------------|
| **No useless one-liners** | If a function is called only once or twice and is one line, inline it |
| **No over-engineering** | No premature abstractions, no factory patterns, no complex DI |
| **Validate at boundaries** | Zod validators run in routes, not inside namespaces |
| **Namespaces, not classes** | No `new`, no `this`, no inheritance |
| **Tests via `.http`** | `api.http` file with ready-to-run requests, no test runner |
| **Absolute imports** | `~/domain/file` via tsconfig alias, never `../../` |
| **Branded types everywhere** | Every ID, URL, constrained value gets its own branded type |
| **Business errors = strings** | `return 'not-found' as const`, never throw for business logic |
| **Typed storage** | `storage.getItem<Type>(key)` with business type as generic |
| **Simple JSON responses** | `{ status: number, data?: any, message?: string }` |
| **No explicit return types** | Let TypeScript infer return types — never annotate them on functions |

## Anti-Patterns

```typescript
// DON'T do this:

// ❌ Class instead of namespace
class OrderService { constructor(private storage: Storage) {} }

// ❌ Useless one-liner function
const isFound = (result: string) => result !== 'not-found'

// ❌ Throw for business error
throw new NotFoundError('Order not found')

// ❌ Try/catch in route for business error
try { await Orders.create(...) } catch (e) { if (e instanceof NotFoundError) ... }

// ❌ Raw string for an ID
const getOrder = async (id: string) => { ... }

// ❌ Relative import
import { Orders } from '../../order/index'

// ❌ Validation inside namespace
export const create = async (rawEmail: string) => {
  const email = z.email().parse(rawEmail) // ← Should be in the route
}

// ❌ Explicit return type
export const getById = async (id: OrderId): Promise<Order | 'not-found'> => { ... }

// ❌ Branded enum
export type OrderStatus = Brand<'pending' | 'shipped', 'OrderStatus'>
```
