---
name: schema-indexing
description: >
  Create MongoDB index management scripts for NestJS + Mongoose projects.
  Use when asked to add, change, or manage database indexes on any collection.
  Enforces the "indexes as scripts, never inline" pattern — never puts index
  definitions inside schema files or relies on autoIndex.
risk: safe
source: self
date_added: "2026-05-15"
---

# Schema Indexing — Indexes as Scripts

## Use this skill when

- Asked to add, modify, or remove indexes on a MongoDB collection
- Creating a new schema and need to define its indexes
- Reviewing whether indexes are defined correctly
- Setting up a fresh environment and need to apply indexes

## Do not use this skill when

- The project is not MongoDB / Mongoose
- The task is only about schema field definitions (not indexes)
- The task is about SQL indexing strategies

---

## The Rule

**Never define indexes inline in schema files. Never rely on `autoIndex`.**

`autoIndex: true` (Mongoose default) drops and rebuilds all indexes on every
application boot. In production this burns CPU, causes startup latency spikes,
and can briefly lock writes on large collections.

The correct pattern: **a standalone TypeScript script** that connects directly
via `MongoClient` and calls `createIndexes()`. This is idempotent (MongoDB skips
indexes that already exist with matching options) and runs only when you
explicitly trigger it.

---

## Step 1 — Locate the collection name

Read the Mongoose schema file for the target collection. The collection name is
in `@Schema({ collection: '...' })`.

## Step 2 — Create the index script

**Path:** `scripts/indexes/<collection-name>.index.ts`

Use this exact structure:

```typescript
import { MongoClient } from 'mongodb';
import { loadAppConfig } from '../../libs/common/src/config/app.config';

async function main(): Promise<void> {
  const { mongodb } = loadAppConfig();
  const mongoUri = mongodb.uri;

  console.log('[INFO] Connecting to MongoDB...');
  const client = new MongoClient(mongoUri);
  await client.connect();
  console.log('[INFO] Connected.');

  try {
    const dbName =
      new URL(mongoUri).pathname.replace(/^\//, '') || 'travel-datahub';
    const col = client.db(dbName).collection('<collection_name>');

    console.log('[INFO] Creating indexes on <collection_name>...');

    await col.createIndexes([
      // unique indexes first
      {
        key: { field_a: 1, field_b: 1 },
        unique: true,
        name: 'field_a_field_b_unique',
      },
      // query-support indexes
      {
        key: { is_active: 1, category: 1 },
        name: 'active_category',
      },
    ]);

    console.log('[DONE] All indexes created (or already exist — idempotent).');
  } finally {
    await client.close();
  }
}

async function run(): Promise<void> {
  try {
    await main();
    process.exit(0);
  } catch (err: unknown) {
    console.error(
      '[ERROR] Index creation failed:',
      err instanceof Error ? err.message : err,
    );
    if (err instanceof Error && err.stack) console.error(err.stack);
    process.exit(1);
  }
}

void run();
```

### Naming indexes

Always provide an explicit `name` in each index spec. This makes `db.collection.getIndexes()` readable and allows targeted `dropIndex('name')` later.

**Convention:** `<fields>_<modifier>` — e.g., `provider_external_unique`, `active_city_categories`, `enrichment_status`.

## Step 3 — Strip indexes from the schema file

Remove any `SomeSchema.index(...)` calls from the schema file. The schema should
only define the document shape, not indexes.

Do NOT add `autoIndex: false` to individual `@Schema()` decorators — it is
already set globally at the `MongooseModule.forRootAsync` connection level.

## Step 4 — Run the script

```bash
npm run script scripts/indexes/<collection-name>.index.ts
```

Requires all env vars from `.env` to be present (including any that `loadAppConfig()` validates beyond MongoDB).

---

## Anti-patterns to reject

| Anti-pattern | Why it's wrong |
|---|---|
| `TravelProductSchema.index({ ... })` in schema file | Runs on every import; does nothing with autoIndex=false but misleads readers |
| `autoIndex: true` in connection config | Drops + rebuilds indexes on every app boot |
| Mongoose `autoIndex: true` in `@Schema()` decorator | Same problem, per-collection |
| Index creation inside NestJS module `onModuleInit` | Ties index management to app lifecycle; not a script, can't be CI-gated |
| Indexes without explicit `name` | Hard to manage/drop later |

---

## Reference implementation

`scripts/indexes/products.index.ts` in this project is the canonical example
with all 6 indexes for the `travel_products` collection.
