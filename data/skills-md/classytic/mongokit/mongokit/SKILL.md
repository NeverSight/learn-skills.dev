---
name: mongokit
description: |
  @classytic/mongokit — Production-grade MongoDB repository pattern for Node.js/TypeScript.
  Use when building MongoDB CRUD, REST APIs with Mongoose 9, repository pattern,
  pagination, caching, soft delete, audit trail, multi-tenant, custom ID generation, or query parsing.
  Triggers: mongoose model, repository pattern, mongokit, mongo crud, pagination,
  soft delete, audit trail, multi-tenant, custom id, query parser, cache plugin, BaseController.
version: 3.2.3
license: MIT
metadata:
  author: Classytic
  version: "3.2.3"
tags:
  - mongodb
  - mongoose
  - repository-pattern
  - crud
  - pagination
  - typescript
  - plugins
  - caching
  - soft-delete
  - audit-trail
  - multi-tenant
  - custom-id
  - query-parser
  - rest-api
progressive_disclosure:
  entry_point:
    summary: "Type-safe MongoDB repository with 17 plugins: pagination, caching, soft delete, audit trail, multi-tenant, custom IDs, observability"
    when_to_use: "Building MongoDB CRUD, REST APIs with Mongoose 9, repository pattern, pagination, caching, audit trail, or query parsing"
    quick_start: "1. npm install @classytic/mongokit mongoose 2. new Repository(Model, [plugins]) 3. repo.create/getAll/update/delete"
  context_limit: 700
---

# @classytic/mongokit

Production-grade MongoDB repository pattern with zero external dependencies. 17 built-in plugins, smart pagination, event-driven hooks, and full TypeScript support. **687 tests.**

**Requires:** Mongoose `^9.0.0` | Node.js `>=18`

## Installation

```bash
npm install @classytic/mongokit mongoose
```

## Core Pattern

Every interaction starts with a Repository wrapping a Mongoose model:

```typescript
import { Repository } from "@classytic/mongokit";

const repo = new Repository(UserModel);

const user = await repo.create({ name: "John", email: "john@example.com" });
const users = await repo.getAll({ page: 1, limit: 20 });
const found = await repo.getById(id);
const updated = await repo.update(id, { name: "Jane" });
await repo.delete(id);
const exists = await repo.exists({ email: "john@example.com" });
const count = await repo.count({ status: "active" });
const userOrNew = await repo.getOrCreate({ email: "x@y.com" }, { name: "X" });
```

## Full API

| Method                           | Description                                    |
| -------------------------------- | ---------------------------------------------- |
| `create(data, opts)`             | Create single document                         |
| `createMany(data[], opts)`       | Create multiple documents                      |
| `getById(id, opts)`              | Find by ID                                     |
| `getByQuery(query, opts)`        | Find one by query                              |
| `getAll(params, opts)`           | Paginated list (auto-detects offset vs keyset) |
| `getOrCreate(query, data, opts)` | Find or create                                 |
| `update(id, data, opts)`         | Update document                                |
| `delete(id, opts)`               | Delete document                                |
| `count(query, opts)`             | Count documents                                |
| `exists(query, opts)`            | Check existence                                |
| `aggregate(pipeline, opts)`      | Run aggregation                                |
| `aggregatePaginate(opts)`        | Paginated aggregation                          |
| `distinct(field, query)`         | Distinct values                                |
| `withTransaction(fn)`            | Atomic transaction                             |

## Pagination (Auto-Detected)

```typescript
// Offset (dashboards) — pass `page`
const result = await repo.getAll({
  page: 1,
  limit: 20,
  filters: { status: "active" },
  sort: { createdAt: -1 },
});
// → { method: 'offset', docs, total, pages, hasNext, hasPrev }

// Keyset (infinite scroll) — pass `sort` without `page`, or `after`
const stream = await repo.getAll({ sort: { createdAt: -1 }, limit: 20 });
// → { method: 'keyset', docs, hasMore, next: 'eyJ2IjoxLC...' }
const next = await repo.getAll({
  after: stream.next,
  sort: { createdAt: -1 },
  limit: 20,
});
```

**Detection:** `page` → offset | `after`/`cursor` → keyset | `sort` only → keyset | default → offset

**Required indexes for keyset:**

```javascript
Schema.index({ createdAt: -1, _id: -1 });
Schema.index({ organizationId: 1, createdAt: -1, _id: -1 }); // multi-tenant
```

## Plugin System

Plugins compose via array — order matters:

```typescript
import {
  Repository,
  timestampPlugin,
  softDeletePlugin,
  cachePlugin,
  createMemoryCache,
  customIdPlugin,
  sequentialId,
} from "@classytic/mongokit";

const repo = new Repository(UserModel, [
  timestampPlugin(),
  softDeletePlugin(),
  cachePlugin({ adapter: createMemoryCache(), ttl: 60 }),
]);
```

### All 17 Plugins

| Plugin                              | Description                              | Needs methodRegistry? |
| ----------------------------------- | ---------------------------------------- | --------------------- |
| `timestampPlugin()`                 | Auto `createdAt`/`updatedAt`             | No                    |
| `softDeletePlugin(opts)`            | Mark deleted instead of removing         | No                    |
| `auditLogPlugin(logger)`            | Log all CUD operations (external logger) | No                    |
| `auditTrailPlugin(opts)`            | DB-persisted audit trail + change diffs  | No (Yes for queries)  |
| `cachePlugin(opts)`                 | Redis/memory caching + auto-invalidation | No                    |
| `validationChainPlugin(validators)` | Custom validation rules                  | No                    |
| `fieldFilterPlugin(preset)`         | Role-based field visibility (RBAC)       | No                    |
| `cascadePlugin(opts)`               | Auto-delete related documents            | No                    |
| `multiTenantPlugin(opts)`           | Auto-inject tenant isolation             | No                    |
| `customIdPlugin(opts)`              | Sequential/random ID generation          | No                    |
| `observabilityPlugin(opts)`         | Timing, metrics, slow queries            | No                    |
| `methodRegistryPlugin()`            | Dynamic method registration              | No (base for below)   |
| `mongoOperationsPlugin()`           | `increment`, `pushToArray`, `upsert`     | Yes                   |
| `batchOperationsPlugin()`           | `updateMany`, `deleteMany`               | Yes                   |
| `aggregateHelpersPlugin()`          | `groupBy`, `sum`, `average`              | Yes                   |
| `subdocumentPlugin()`               | Manage subdocument arrays                | Yes                   |
| `elasticSearchPlugin(opts)`         | Delegate search to ES/OpenSearch         | Yes                   |

### Soft Delete

```typescript
const repo = new Repository(UserModel, [
  softDeletePlugin({ deletedField: "deletedAt" }),
]);
await repo.delete(id); // Sets deletedAt
await repo.getAll(); // Auto-excludes deleted
await repo.getAll({ includeDeleted: true }); // Include deleted
```

**Unique index gotcha:** Use partial filter expressions:

```javascript
Schema.index(
  { email: 1 },
  { unique: true, partialFilterExpression: { deletedAt: null } },
);
```

### Caching

```typescript
const repo = new Repository(UserModel, [
  cachePlugin({
    adapter: createMemoryCache(),
    ttl: 60,
    byIdTtl: 300,
    queryTtl: 30,
  }),
]);
const user = await repo.getById(id); // Cached
const fresh = await repo.getById(id, { skipCache: true }); // Skip cache
await repo.update(id, { name: "New" }); // Auto-invalidates
```

**Redis adapter:**

```typescript
const redisAdapter = {
  async get(key) {
    return JSON.parse((await redis.get(key)) || "null");
  },
  async set(key, value, ttl) {
    await redis.setex(key, ttl, JSON.stringify(value));
  },
  async del(key) {
    await redis.del(key);
  },
  async clear(pattern) {
    /* bulk invalidation */
  },
};
```

### Multi-Tenant

```typescript
const repo = new Repository(UserModel, [
  multiTenantPlugin({
    tenantField: "organizationId",
    contextKey: "organizationId",
    required: true,
  }),
]);
// All ops auto-scoped: repo.getAll({ organizationId: 'org_123' })
// Cross-tenant → returns "not found"
```

### Custom ID Generation

Atomic MongoDB counters — concurrency-safe, zero duplicates:

```typescript
import {
  customIdPlugin,
  sequentialId,
  dateSequentialId,
  prefixedId,
  getNextSequence,
} from "@classytic/mongokit";

// Sequential: INV-0001, INV-0002, ...
customIdPlugin({
  field: "invoiceNumber",
  generator: sequentialId({ prefix: "INV", model: InvoiceModel }),
});

// Date-partitioned: BILL-2026-02-0001 (resets monthly/yearly/daily)
customIdPlugin({
  field: "billNumber",
  generator: dateSequentialId({
    prefix: "BILL",
    model: BillModel,
    partition: "monthly",
  }),
});

// Random: ORD_a7b3xk9m2p (no DB round-trip)
customIdPlugin({
  field: "orderRef",
  generator: prefixedId({ prefix: "ORD", length: 10 }),
});

// Custom generator with getNextSequence()
customIdPlugin({
  field: "ref",
  generator: async (ctx) =>
    `ORD-${ctx.data?.region || "US"}-${String(await getNextSequence("orders")).padStart(4, "0")}`,
});
```

**Options:** `sequentialId({ prefix, model, padding?: 4, separator?: '-', counterKey? })`
**Partitions:** `'yearly'` | `'monthly'` | `'daily'`
**Behavior:** Counters never decrement on delete (standard for invoices/bills).

### Validation Chain

```typescript
import {
  validationChainPlugin,
  requireField,
  uniqueField,
  immutableField,
  blockIf,
  autoInject,
} from "@classytic/mongokit";
validationChainPlugin([
  requireField("email", ["create"]),
  uniqueField("email", "Email already exists"),
  immutableField("userId"),
  blockIf(
    "noAdminDelete",
    ["delete"],
    (ctx) => ctx.data?.role === "admin",
    "Cannot delete admins",
  ),
  autoInject("slug", (ctx) => slugify(ctx.data?.name), ["create"]),
]);
```

### Cascade Delete

```typescript
cascadePlugin({
  relations: [
    { model: "StockEntry", foreignKey: "product" },
    { model: "Review", foreignKey: "product", softDelete: false },
  ],
  parallel: true,
});
```

### MongoDB Operations (Atomic)

```typescript
import type { MongoOperationsMethods } from "@classytic/mongokit";
type Repo = Repository<IUser> & MongoOperationsMethods<IUser>;
const repo = new Repository(UserModel, [
  methodRegistryPlugin(),
  mongoOperationsPlugin(),
]) as Repo;

await repo.increment(id, "views", 1);
await repo.pushToArray(id, "tags", "featured");
await repo.upsert({ sku: "ABC" }, { name: "Product", price: 99 });
await repo.addToSet(id, "roles", "admin");
```

### Audit Trail (DB-Persisted)

```typescript
import { auditTrailPlugin, AuditTrailQuery } from "@classytic/mongokit";
import type { AuditTrailMethods } from "@classytic/mongokit";

// Per-repo: track operations with change diffs
const repo = new Repository(JobModel, [
  methodRegistryPlugin(),
  auditTrailPlugin({
    operations: ["create", "update", "delete"],
    trackChanges: true, // before/after diff
    ttlDays: 90, // auto-purge
    excludeFields: ["password"],
    metadata: (ctx) => ({ ip: ctx.req?.ip }),
  }),
]);
const trail = await repo.getAuditTrail(docId, { operation: "update" });

// Standalone: query across all models (admin dashboards)
const auditQuery = new AuditTrailQuery();
await auditQuery.getOrgTrail(orgId);
await auditQuery.getUserTrail(userId);
await auditQuery.getDocumentTrail("Job", jobId);
await auditQuery.query({ orgId, operation: "delete", from: startDate, to: endDate });
```

**Options:** `operations`, `trackChanges` (default: true), `trackDocument` (default: false), `ttlDays`, `collectionName` (default: `'audit_trails'`), `excludeFields`, `metadata`

### Observability

```typescript
observabilityPlugin({
  onMetric: (m) => statsd.histogram(`mongokit.${m.operation}`, m.duration),
  slowThresholdMs: 200,
});
```

## Event System

```typescript
repo.on("before:create", async (ctx) => {
  ctx.data.processedAt = new Date();
});
repo.on("after:create", ({ context, result }) => {
  console.log("Created:", result._id);
});
repo.on("error:create", ({ context, error }) => {
  reportError(error);
});
```

**Events:** `before:*`, `after:*`, `error:*` for `create`, `createMany`, `update`, `delete`, `getById`, `getByQuery`, `getAll`, `aggregatePaginate`

## QueryParser (HTTP to MongoDB)

```typescript
import { QueryParser } from "@classytic/mongokit";
const parser = new QueryParser({
  maxLimit: 100,
  maxFilterDepth: 5,
  maxRegexLength: 100,
});
const { filters, limit, page, sort, search, populateOptions } = parser.parse(
  req.query,
);
```

**URL patterns:**

```
?status=active&role=admin             # exact match
?age[gte]=18&age[lte]=65             # range
?role[in]=admin,user                  # in-set
?name[regex]=^John                    # regex
?sort=-createdAt,name                 # multi-sort
?page=2&limit=50                      # offset pagination
?after=eyJfaWQiOi...&limit=20        # cursor pagination
?search=john                          # full-text
?populate[author][select]=name,email  # advanced populate
```

**Security:** Blocks `$where`/`$function`/`$accumulator`/`$expr` | ReDoS protection | `$options` restricted to `[imsx]` | Populate path sanitization

## BaseController (Auto-CRUD)

The package includes a `BaseController` reference implementation (see `examples/api/BaseController.ts`) that provides instant auto-generated CRUD with security:

```typescript
import { BaseController } from "./BaseController";

class UserController extends BaseController<IUser> {
  constructor(repository: Repository<IUser>) {
    super(repository, {
      fieldRules: {
        role: { systemManaged: true }, // Users cannot set role
        credits: { systemManaged: true }, // Users cannot set credits
      },
      query: {
        allowedLookups: ["departments", "teams"], // Only these collections can be joined
        allowedLookupFields: {
          departments: { localFields: ["deptId"], foreignFields: ["_id"] },
        },
      },
    });
  }

  // Override specific methods — the rest are auto-generated
  async create(ctx: IRequestContext) {
    await sendVerificationEmail(ctx.body.email);
    return super.create(ctx);
  }
}
```

**Features:**

- Auto list/get/create/update/delete from `IController` interface
- System-managed field sanitization (strips protected fields from user input)
- 3-level lookup security: collection allowlist → per-collection field allowlist → pipeline/let blocking
- Override any method, keep the rest auto-generated

## JSON Schema Generation

```typescript
import { buildCrudSchemasFromModel } from "@classytic/mongokit";
const { crudSchemas } = buildCrudSchemasFromModel(UserModel, {
  fieldRules: {
    organizationId: { immutable: true },
    role: { systemManaged: true },
  },
  strictAdditionalProperties: true,
});
// crudSchemas.createBody, updateBody, params, listQuery — use with Fastify schema validation or OpenAPI
```

## Configuration

```typescript
new Repository(UserModel, plugins, {
  defaultLimit: 20,
  maxLimit: 100,
  maxPage: 10000,
  deepPageThreshold: 100,
  useEstimatedCount: false,
  cursorVersion: 1,
});
```

## Extending Repository

```typescript
class UserRepository extends Repository<IUser> {
  constructor() {
    super(UserModel, [timestampPlugin(), softDeletePlugin()], {
      defaultLimit: 20,
    });
  }
  async findByEmail(email: string) {
    return this.getByQuery({ email });
  }
  async findActive() {
    return this.getAll({
      filters: { status: "active" },
      sort: { createdAt: -1 },
    });
  }
}
```

## TypeScript Type Safety

```typescript
import type { WithPlugins } from "@classytic/mongokit";
const repo = new Repository(UserModel, [
  methodRegistryPlugin(),
  mongoOperationsPlugin(),
  softDeletePlugin(),
  cachePlugin({ adapter: createMemoryCache() }),
]) as WithPlugins<IUser, Repository<IUser>>;
// Full autocomplete: repo.increment, repo.restore, repo.invalidateCache
```

**Types:** `MongoOperationsMethods<T>`, `BatchOperationsMethods`, `AggregateHelpersMethods`, `SubdocumentMethods<T>`, `SoftDeleteMethods<T>`, `CacheMethods`, `AuditTrailMethods`

## Architecture Decisions

- **Zero external deps** — only Mongoose as peer dep
- **Own event system** — not Mongoose middleware, fully async with `emitAsync`
- **Own `FilterQuery` type** — immune to Mongoose 9's rename to `RootFilterQuery`
- **Update pipelines gated** — must pass `{ updatePipeline: true }` explicitly
- **Atomic counters** — `findOneAndUpdate` + `$inc`, not `countDocuments` (race-safe)
- **Cache versioning** — `Date.now()` timestamps, not incrementing integers (survives Redis eviction)
