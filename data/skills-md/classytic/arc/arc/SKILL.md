---
name: arc
description: |
  @classytic/arc — Resource-oriented backend framework for Fastify.
  Use when building REST APIs with Fastify, resource CRUD, defineResource, createApp,
  permissions, presets, database adapters, hooks, events, QueryCache, authentication,
  multi-tenant SaaS, OpenAPI, job queues, WebSocket, or production deployment.
  Triggers: arc, fastify resource, defineResource, createApp, BaseController, arc preset,
  arc auth, arc events, arc jobs, arc websocket, arc plugin, arc testing, arc cli,
  arc permissions, arc hooks, arc pipeline, arc factory, arc cache, arc QueryCache.
version: 2.1.0
license: MIT
metadata:
  author: Classytic
  version: "2.1.0"
tags:
  - fastify
  - rest-api
  - resource-framework
  - crud
  - permissions
  - multi-tenant
  - presets
  - typescript
  - cache
  - events
  - openapi
progressive_disclosure:
  entry_point:
    summary: "Resource-oriented Fastify framework: defineResource(), presets, permissions, QueryCache, events, multi-tenant, OpenAPI"
    when_to_use: "Building REST APIs with Fastify, resource CRUD, authentication, presets, caching, events, or production deployment"
    quick_start: "1. npm install @classytic/arc fastify 2. createApp({ preset: 'production', auth: { type: 'jwt', jwt: { secret } } }) 3. defineResource({ name, adapter, presets, permissions })"
  context_limit: 700
---

# @classytic/arc

Resource-oriented backend framework for Fastify. Database-agnostic, tree-shakable, production-ready.

**Requires:** Fastify `^5.0.0` | Node.js `>=22` | ESM only

## Install

```bash
npm install @classytic/arc fastify
npm install @classytic/mongokit mongoose    # MongoDB adapter
```

## Quick Start

```typescript
import { createApp } from '@classytic/arc/factory';
import mongoose from 'mongoose';

await mongoose.connect(process.env.DB_URI);

const app = await createApp({
  preset: 'production',
  auth: { type: 'jwt', jwt: { secret: process.env.JWT_SECRET } },
  cors: { origin: process.env.ALLOWED_ORIGINS?.split(',') },
});

await app.register(productResource.toPlugin());
await app.listen({ port: 8040, host: '0.0.0.0' });
```

## defineResource()

Single API to define a full REST resource:

```typescript
import { defineResource, createMongooseAdapter, allowPublic, requireRoles } from '@classytic/arc';

const productResource = defineResource({
  name: 'product',
  adapter: createMongooseAdapter({ model: ProductModel, repository: productRepo }),
  controller: productController,  // optional — auto-created if omitted
  presets: ['softDelete', 'slugLookup', { name: 'multiTenant', tenantField: 'orgId' }],
  permissions: {
    list: allowPublic(),
    get: allowPublic(),
    create: requireRoles(['admin']),
    update: requireRoles(['admin']),
    delete: requireRoles(['admin']),
  },
  cache: { staleTime: 30, gcTime: 300, tags: ['catalog'] },
  additionalRoutes: [
    { method: 'GET', path: '/featured', handler: 'getFeatured', permissions: allowPublic(), wrapHandler: true },
  ],
});

await fastify.register(productResource.toPlugin());
// Auto-generates: GET /, GET /:id, POST /, PATCH /:id, DELETE /:id
```

## Authentication

Auth uses a **discriminated union** with `type` field:

```typescript
// Arc JWT
auth: { type: 'jwt', jwt: { secret, expiresIn: '15m', refreshSecret, refreshExpiresIn: '7d' } }

// Better Auth (recommended for SaaS with orgs)
import { createBetterAuthAdapter } from '@classytic/arc/auth';
auth: { type: 'betterAuth', betterAuth: createBetterAuthAdapter({ auth, orgContext: true }) }

// Custom Fastify plugin (must decorate fastify.authenticate)
auth: { type: 'custom', plugin: myAuthPlugin }

// Custom function (decorates fastify.authenticate directly)
auth: { type: 'authenticator', authenticate: async (req, reply) => { ... } }

// Disabled
auth: false
```

**Decorates:** `app.authenticate`, `app.optionalAuthenticate`, `app.authorize`

## Permissions

Function-based. A `PermissionCheck` returns `boolean | { granted, reason?, filters? }`:

```typescript
import {
  allowPublic, requireAuth, requireRoles, requireOwnership,
  requireOrgMembership, requireOrgRole, requireTeamMembership,
  allOf, anyOf, when, denyAll,
  createDynamicPermissionMatrix,
} from '@classytic/arc';

permissions: {
  list: allowPublic(),
  get: requireAuth(),
  create: requireRoles(['admin', 'editor']),
  update: anyOf(requireOwnership('userId'), requireRoles(['admin'])),
  delete: allOf(requireAuth(), requireRoles(['admin'])),
}
```

**Custom permission:**

```typescript
const requirePro = (): PermissionCheck => async (ctx) => {
  if (!ctx.user) return { granted: false, reason: 'Auth required' };
  return { granted: ctx.user.plan === 'pro' };
};
```

**Field-level permissions:**

```typescript
import { fields } from '@classytic/arc';

fields: {
  password: fields.hidden(),
  salary: fields.visibleTo(['admin', 'hr']),
  role: fields.writableBy(['admin']),
  email: fields.redactFor(['viewer'], '***'),
}
```

**Dynamic ACL (DB-managed):**

```typescript
const acl = createDynamicPermissionMatrix({
  resolveRolePermissions: async (ctx) => aclService.getRoleMatrix(orgId),
  cacheStore: new RedisCacheStore({ client: redis, prefix: 'acl:' }),
});
permissions: { list: acl.canAction('product', 'read') }
```

## Presets

| Preset | Routes Added | Controller Interface | Config |
|--------|-------------|---------------------|--------|
| `softDelete` | GET /deleted, POST /:id/restore | `ISoftDeleteController` | `{ deletedField }` |
| `slugLookup` | GET /slug/:slug | `ISlugLookupController` | `{ slugField }` |
| `tree` | GET /tree, GET /:parent/children | `ITreeController` | `{ parentField }` |
| `ownedByUser` | none (middleware) | — | `{ ownerField }` |
| `multiTenant` | none (middleware) | — | `{ tenantField }` |
| `audited` | none (middleware) | — | — |

```typescript
presets: ['softDelete', { name: 'multiTenant', tenantField: 'organizationId' }]
```

## QueryCache

TanStack Query-inspired server cache with stale-while-revalidate and auto-invalidation on mutations.

```typescript
// Enable globally
const app = await createApp({ arcPlugins: { queryCache: true } });

// Per-resource config
defineResource({
  name: 'product',
  cache: {
    staleTime: 30,      // seconds fresh (no revalidation)
    gcTime: 300,         // seconds stale data kept (SWR window)
    tags: ['catalog'],   // cross-resource grouping
    invalidateOn: { 'category.*': ['catalog'] },  // event pattern → tag targets
    list: { staleTime: 60 },  // per-operation override
    byId: { staleTime: 10 },
  },
});
```

**Auto-invalidation:** POST/PATCH/DELETE bumps resource version. Old cached queries expire naturally via TTL.

**Runtime modes:** `memory` (default, zero-config) | `distributed` (requires `stores.queryCache: RedisCacheStore`)

**Response header:** `x-cache: HIT | STALE | MISS`

## BaseController

```typescript
import { BaseController } from '@classytic/arc';
import type { IRequestContext, IControllerResponse } from '@classytic/arc';

class ProductController extends BaseController<Product> {
  constructor() { super(productRepo); }

  async getFeatured(req: IRequestContext): Promise<IControllerResponse> {
    const products = await this.repository.getAll({ filters: { isFeatured: true } });
    return { success: true, data: products };
  }
}
```

**IRequestContext:** `{ params, query, body, user, headers, context, metadata, server }`

**IControllerResponse:** `{ success, data?, error?, status?, meta?, headers? }`

## Adapters (Database-Agnostic)

```typescript
// Mongoose
import { createMongooseAdapter } from '@classytic/arc';
const adapter = createMongooseAdapter({ model: ProductModel, repository: productRepo });

// Custom adapter — implement CrudRepository interface:
interface CrudRepository<TDoc> {
  getAll(params?): Promise<TDoc[] | PaginatedResult<TDoc>>;
  getById(id: string): Promise<TDoc | null>;
  create(data): Promise<TDoc>;
  update(id: string, data): Promise<TDoc | null>;
  delete(id: string): Promise<boolean>;
}
```

## Events

The factory auto-registers `eventPlugin` — no manual setup needed:

```typescript
// createApp() registers eventPlugin automatically (default: MemoryEventTransport)
const app = await createApp({
  stores: { events: new RedisEventTransport(redis) },  // optional, defaults to memory
  arcPlugins: {
    events: {                     // event plugin config (default: true, false to disable)
      logEvents: true,
      retry: { maxRetries: 3, backoffMs: 1000 },
    },
  },
});

await app.events.publish('order.created', { orderId: '123' });
await app.events.subscribe('order.*', async (event) => { ... });
```

CRUD events auto-emit: `{resource}.created`, `{resource}.updated`, `{resource}.deleted`.

## Factory — createApp()

```typescript
const app = await createApp({
  preset: 'production',            // production | development | testing | edge
  runtime: 'memory',              // memory (default) | distributed
  auth: { type: 'jwt', jwt: { secret } },
  cors: { origin: ['https://myapp.com'] },
  helmet: true,                    // false to disable
  rateLimit: { max: 100 },         // false to disable
  arcPlugins: {
    events: true,                  // event plugin (default: true, false to disable)
    emitEvents: true,              // CRUD event emission (default: true)
    queryCache: true,              // server cache (default: false)
    sse: true,                     // SSE streaming (default: false)
    caching: true,                 // ETag + Cache-Control (default: false)
  },
  stores: {                        // required when runtime: 'distributed'
    events: new RedisEventTransport({ client: redis }),
    queryCache: new RedisCacheStore({ client: redis }),
  },
});
```

## Hooks

```typescript
import { createHookSystem, beforeCreate, afterUpdate } from '@classytic/arc/hooks';

const hooks = createHookSystem();
beforeCreate(hooks, 'product', async (ctx) => { ctx.data.slug = slugify(ctx.data.name); });
afterUpdate(hooks, 'product', async (ctx) => { await invalidateCache(ctx.result._id); });
```

## Pipeline

```typescript
import { guard, transform, intercept } from '@classytic/arc';

defineResource({
  pipe: {
    create: [
      guard('verified', async (ctx) => ctx.user?.verified === true),
      transform('inject', async (ctx) => { ctx.body.createdBy = ctx.user._id; }),
    ],
  },
});
```

## Query Parsing

```
GET /products?page=2&limit=20&sort=-createdAt&select=name,price
GET /products?price[gte]=100&status[in]=active,featured&search=keyword
GET /products?populate=category,brand
```

Operators: `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `in`, `nin`, `like`, `regex`, `exists`

## Error Classes

```typescript
import { ArcError, NotFoundError, ValidationError, UnauthorizedError, ForbiddenError } from '@classytic/arc';
throw new NotFoundError('Product not found');  // 404
```

## CLI

```bash
arc init my-api --mongokit --better-auth --ts
arc generate resource product
arc docs ./openapi.json --entry ./dist/index.js
arc introspect --entry ./dist/index.js
arc doctor
```

## Subpath Imports

```typescript
import { defineResource, BaseController, allowPublic } from '@classytic/arc';
import { createApp } from '@classytic/arc/factory';
import { MemoryCacheStore, RedisCacheStore, QueryCache } from '@classytic/arc/cache';
import { createBetterAuthAdapter, extractBetterAuthOpenApi } from '@classytic/arc/auth';
import type { ExternalOpenApiPaths } from '@classytic/arc/docs';
import { eventPlugin } from '@classytic/arc/events';
import { RedisEventTransport } from '@classytic/arc/events/redis';
import { healthPlugin, gracefulShutdownPlugin } from '@classytic/arc/plugins';
import { tracingPlugin } from '@classytic/arc/plugins/tracing';
import { auditPlugin } from '@classytic/arc/audit';
import { idempotencyPlugin } from '@classytic/arc/idempotency';
import { ssePlugin } from '@classytic/arc/plugins';
import { jobsPlugin } from '@classytic/arc/integrations/jobs';
import { websocketPlugin } from '@classytic/arc/integrations/websocket';
import { eventGatewayPlugin } from '@classytic/arc/integrations/event-gateway';
import { createHookSystem } from '@classytic/arc/hooks';
import { createTestApp } from '@classytic/arc/testing';
import { Type, ArcListResponse } from '@classytic/arc/schemas';
import { createStateMachine, CircuitBreaker } from '@classytic/arc/utils';
import { defineMigration } from '@classytic/arc/migrations';
import { isMember, isElevated, getOrgId } from '@classytic/arc/scope';
```

## References (Progressive Disclosure)

- **[auth](references/auth.md)** — JWT, Better Auth, API key auth, custom auth, multi-tenant
- **[events](references/events.md)** — Domain events, transports, retry, auto-emission
- **[integrations](references/integrations.md)** — BullMQ jobs, WebSocket, EventGateway, Streamline workflows
- **[production](references/production.md)** — Health, audit, idempotency, tracing, SSE, QueryCache, OpenAPI
- **[testing](references/testing.md)** — Test app, mocks, data factories, in-memory MongoDB
