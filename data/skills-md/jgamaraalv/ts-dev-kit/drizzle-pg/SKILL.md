---
name: drizzle-pg
description: "Drizzle ORM reference for PostgreSQL — schema definition, typesafe queries, relations, and migrations with drizzle-kit. Use when: (1) defining pgTable schemas with column types, indexes, constraints, or enums, (2) writing select/insert/update/delete queries or joins, (3) defining relations and using the relational query API (db.query.*), (4) running drizzle-kit generate/migrate/push/pull, (5) configuring drizzle.config.ts, (6) using the sql`` template operator, or (7) working with PostGIS/pg_vector extensions."
---

# Drizzle ORM — PostgreSQL

Drizzle is a headless TypeScript ORM. Zero dependencies, SQL-like API, single-query output.
Packages: `drizzle-orm` (runtime), `drizzle-kit` (CLI/migrations).

## Table of Contents

- [Quick Start](#quick-start)
- [Import Cheat Sheet](#import-cheat-sheet)
- [Common Patterns](#common-patterns)
- [Reference Files](#reference-files)

## Quick Start

### Connect

```typescript
import { drizzle } from "drizzle-orm/node-postgres";
import * as schema from "./schema";
import { relations } from "./relations";

const db = drizzle(process.env.DATABASE_URL, { schema, relations });
```

Or with existing Pool:

```typescript
import { Pool } from "pg";
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const db = drizzle({ client: pool, schema, relations });
```

### Define Schema

```typescript
import {
  pgTable,
  pgEnum,
  serial,
  text,
  integer,
  timestamp,
  uuid,
  jsonb,
  index,
  uniqueIndex,
} from "drizzle-orm/pg-core";
import { sql } from "drizzle-orm";

export const statusEnum = pgEnum("status", ["active", "inactive", "banned"]);

export const users = pgTable(
  "users",
  {
    id: uuid("id")
      .default(sql`gen_random_uuid()`)
      .primaryKey(),
    name: text("name").notNull(),
    email: text("email").notNull().unique(),
    status: statusEnum().default("active").notNull(),
    metadata: jsonb("metadata").$type<{ roles: string[] }>(),
    createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
  },
  (t) => [index("users_email_idx").on(t.email)],
);

export const posts = pgTable("posts", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  authorId: uuid("author_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
});
```

### Define Relations

```typescript
import { defineRelations } from "drizzle-orm";
import * as schema from "./schema";

export const relations = defineRelations(schema, (r) => ({
  users: {
    posts: r.many.posts({ from: r.users.id, to: r.posts.authorId }),
  },
  posts: {
    author: r.one.users({ from: r.posts.authorId, to: r.users.id }),
  },
}));
```

### CRUD

```typescript
import { eq, and, ilike, sql } from "drizzle-orm";

// SELECT
const allUsers = await db.select().from(users);
const user = await db.select().from(users).where(eq(users.id, id));

// INSERT
const [created] = await db
  .insert(users)
  .values({ name: "Dan", email: "dan@example.com" })
  .returning();

// UPDATE
await db.update(users).set({ name: "Updated" }).where(eq(users.id, id));

// DELETE
await db.delete(users).where(eq(users.id, id));

// UPSERT
await db
  .insert(users)
  .values({ id, name: "Dan", email: "dan@ex.com" })
  .onConflictDoUpdate({ target: users.id, set: { name: "Dan" } });
```

### Relational Queries

```typescript
// Nested eager loading (single SQL query)
const usersWithPosts = await db.query.users.findMany({
  with: { posts: true },
  where: { status: "active" },
  orderBy: { createdAt: "desc" },
  limit: 10,
});

const user = await db.query.users.findFirst({
  where: { id: userId },
  with: { posts: { columns: { id: true, title: true } } },
});
```

### Migrations

```bash
# drizzle.config.ts -> see references/migrations.md
npx drizzle-kit generate     # schema diff -> SQL files
npx drizzle-kit migrate      # apply SQL to database
npx drizzle-kit push         # direct push (no SQL files)
npx drizzle-kit pull         # introspect DB -> Drizzle schema
npx drizzle-kit studio       # visual browser UI
```

## Import Cheat Sheet

| Import path           | Key exports                                                                                                                                                                                                                                   |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `drizzle-orm/pg-core` | `pgTable`, `pgEnum`, column types (`serial`, `text`, `integer`, `uuid`, `timestamp`, `jsonb`, `varchar`, `boolean`, `numeric`, `bigint`, `geometry`, `vector`, ...), `index`, `uniqueIndex`, `unique`, `check`, `primaryKey`, `foreignKey`    |
| `drizzle-orm`         | Operators: `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `and`, `or`, `not`, `isNull`, `isNotNull`, `inArray`, `between`, `like`, `ilike`, `exists`, `sql`, `asc`, `desc`. Utilities: `getColumns`, `defineRelations`, `cosineDistance`, `l2Distance` |
| `drizzle-orm` (types) | `InferSelectModel`, `InferInsertModel`                                                                                                                                                                                                        |
| `drizzle-zod`         | `createInsertSchema`, `createSelectSchema`                                                                                                                                                                                                    |

## Common Patterns

### Conditional filters

```typescript
const filters: SQL[] = [];
if (name) filters.push(ilike(users.name, `%${name}%`));
if (status) filters.push(eq(users.status, status));
await db
  .select()
  .from(users)
  .where(and(...filters));
```

### Transactions

```typescript
await db.transaction(async (tx) => {
  const [user] = await tx.insert(users).values({ name: "Dan" }).returning();
  await tx.insert(posts).values({ title: "Hello", authorId: user.id });
});
```

### Type inference

```typescript
type User = typeof users.$inferSelect;
type NewUser = typeof users.$inferInsert;
```

## Reference Files

For detailed API coverage, see:

- **Column types, indexes, constraints, enums, PostGIS, pg_vector**: [references/schema-pg.md](references/schema-pg.md)
- **Select, insert, update, delete, joins, filters**: [references/queries.md](references/queries.md)
- **Relations definition, relational query API (findMany/findFirst)**: [references/relations.md](references/relations.md)
- **sql`` template: raw, empty, join, identifier, placeholders**: [references/sql-operator.md](references/sql-operator.md)
- **drizzle-kit commands, drizzle.config.ts, migration workflows**: [references/migrations.md](references/migrations.md)
- **Dynamic queries, transactions, custom types, Zod, utilities**: [references/advanced.md](references/advanced.md)
