---
name: drizzle-orm
description: |
  Drizzle ORM — type-safe, lightweight TypeScript ORM for SQL databases. Schema declaration, CRUD queries, joins, relations, migrations with Drizzle Kit, and database seeding.
  Use when defining database schemas, writing queries (select/insert/update/delete), setting up migrations, configuring drizzle.config.ts, establishing database connections,
  validating data with drizzle-zod/valibot, or working with PostgreSQL, MySQL, SQLite, Turso, Bun SQL, Neon, Supabase, PGlite,
  Expo SQLite, Cloudflare D1, PlanetScale, SingleStore, MSSQL, CockroachDB.
---

# Drizzle ORM

~7.4kb minified+gzipped, zero dependencies, serverless-ready.

## Quick Start

### Install

```bash
# PostgreSQL
npm i drizzle-orm pg
npm i -D drizzle-kit @types/pg

# MySQL
npm i drizzle-orm mysql2
npm i -D drizzle-kit

# SQLite
npm i drizzle-orm better-sqlite3
npm i -D drizzle-kit @types/better-sqlite3

# Turso / LibSQL
npm i drizzle-orm @libsql/client
npm i -D drizzle-kit

# Bun SQL (PostgreSQL — zero extra deps)
bun add drizzle-orm
bun add -D drizzle-kit

# Bun SQLite (zero extra deps, sync APIs)
bun add drizzle-orm
bun add -D drizzle-kit
```

### Config

```ts
// drizzle.config.ts
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  dialect: "postgresql", // "postgresql" | "mysql" | "sqlite" | "turso" | "singlestore"
  schema: "./src/db/schema.ts",
  out: "./drizzle",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

### Schema

```ts
// src/db/schema.ts
import { pgTable, serial, text, integer, timestamp } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: serial().primaryKey(),
  name: text().notNull(),
  email: text().unique(),
  createdAt: timestamp().defaultNow(),
});

export const posts = pgTable("posts", {
  id: serial().primaryKey(),
  title: text().notNull(),
  content: text(),
  authorId: integer("author_id").references(() => users.id),
});
```

### Connect & Query

```ts
import { drizzle } from "drizzle-orm/node-postgres";
import { eq } from "drizzle-orm";
import * as schema from "./schema";

const db = drizzle(process.env.DATABASE_URL!, { schema });

// select
const allUsers = await db.select().from(schema.users);

// insert
const [user] = await db.insert(schema.users)
  .values({ name: "Dan", email: "dan@example.com" })
  .returning();

// update
await db.update(schema.users)
  .set({ name: "Daniel" })
  .where(eq(schema.users.id, 1));

// delete
await db.delete(schema.users).where(eq(schema.users.id, 1));
```

See [references/connections.md](references/connections.md) for all provider setups (Neon, Turso, Supabase, D1, etc.).

## Schema Declaration

Import table/column builders from the dialect-specific module:

```ts
// PG:     import { pgTable, serial, text, ... } from "drizzle-orm/pg-core";
// MySQL:  import { mysqlTable, int, varchar, ... } from "drizzle-orm/mysql-core";
// SQLite: import { sqliteTable, integer, text, ... } from "drizzle-orm/sqlite-core";
```

### Common Column Types (PG)

| Type | Usage | Notes |
|------|-------|-------|
| `serial()` | Auto-increment PK | Use `integer().generatedAlwaysAsIdentity()` for new projects |
| `integer()` | 4-byte int | |
| `bigint({ mode: "number" })` | 8-byte int | `"bigint"` mode for >2^53 |
| `text()` | Unlimited text | `{ enum: [...] }` for TS union |
| `varchar({ length: n })` | Variable-length | |
| `boolean()` | true/false | |
| `timestamp()` | Date/time | `{ withTimezone: true }`, `mode: "date"` |
| `date()` | Calendar date | `mode: "date"` for JS Date |
| `json()` / `jsonb()` | JSON data | `.$type<T>()` for typing |
| `uuid()` | UUID | `.defaultRandom()` for gen_random_uuid() |
| `numeric({ precision, scale })` | Exact decimal | Returns string by default |

### Constraint Modifiers

```ts
column.notNull()
column.default(value)
column.default(sql`now()`)
column.$defaultFn(() => createId())   // runtime default
column.$onUpdate(() => new Date())    // runtime on update
column.primaryKey()
column.unique()
column.references(() => other.id, { onDelete: "cascade" })
column.$type<CustomType>()            // branded types
```

### Auto-map Casing

```ts
// drizzle.config.ts
export default defineConfig({
  casing: "snake_case", // camelCase TS keys -> snake_case DB columns
});
```

Full column type catalogs: [PG](references/schema-postgresql.md) | [MySQL](references/schema-mysql.md) | [SQLite](references/schema-sqlite.md) | [MSSQL/CockroachDB/SingleStore](references/column-types-minor-dialects.md)

## CRUD Operations

All operators imported from `"drizzle-orm"`:

```ts
import { eq, ne, gt, gte, lt, lte, and, or, not, like, ilike, inArray, between, isNull, sql } from "drizzle-orm";
```

### Select

```ts
// basic
await db.select().from(users);

// partial + where
await db.select({ id: users.id, name: users.name })
  .from(users)
  .where(and(eq(users.role, "admin"), gt(users.age, 18)))
  .orderBy(asc(users.name))
  .limit(10).offset(20);

// aggregation
await db.select({ role: users.role, count: sql<number>`count(*)` })
  .from(users).groupBy(users.role).having(gt(sql`count(*)`, 5));
```

### Insert

```ts
// single + returning
const [user] = await db.insert(users).values({ name: "Dan" }).returning();

// bulk
await db.insert(users).values([{ name: "A" }, { name: "B" }]);

// upsert (PG/SQLite)
await db.insert(users).values({ id: 1, name: "Dan" })
  .onConflictDoUpdate({ target: users.id, set: { name: "Dan" } });

// upsert (MySQL)
await db.insert(users).values({ id: 1, name: "Dan" })
  .onDuplicateKeyUpdate({ set: { name: "Dan" } });
```

### Update / Delete

```ts
await db.update(users).set({ name: "Jane" }).where(eq(users.id, 1)).returning();
await db.delete(users).where(eq(users.id, 1)).returning();
```

Full queries reference: [references/queries.md](references/queries.md)

## Joins

```ts
// inner join
await db.select().from(users)
  .innerJoin(posts, eq(users.id, posts.authorId));

// left join
await db.select().from(users)
  .leftJoin(orders, eq(users.id, orders.userId));

// self-join with alias
import { alias } from "drizzle-orm/pg-core";
const parent = alias(users, "parent");
await db.select().from(users).leftJoin(parent, eq(users.managerId, parent.id));
```

## Relations

### V1 (Stable)

```ts
import { relations } from "drizzle-orm";

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, { fields: [posts.authorId], references: [users.id] }),
}));
```

### Relational Queries

Pass `schema` to drizzle to enable `db.query`:

```ts
const db = drizzle(url, { schema });

const result = await db.query.users.findMany({
  columns: { id: true, name: true },
  with: { posts: { with: { comments: true } } },
  where: (users, { eq }) => eq(users.id, 1),
  orderBy: (users, { desc }) => desc(users.createdAt),
  limit: 10,
});

const user = await db.query.users.findFirst({
  where: (users, { eq }) => eq(users.name, "Dan"),
  with: { posts: true },
});
```

### V2 (Beta)

```ts
import { defineRelations } from "drizzle-orm";

export const relations = defineRelations(schema, (r) => ({
  users: { posts: r.many.posts() },
  posts: { author: r.one.users({ from: r.posts.authorId, to: r.users.id }) },
}));
```

V2 adds `.through()` for many-to-many without junction table boilerplate.

Full relations reference: [references/relations.md](references/relations.md)

## Drizzle Kit

| Command | Description |
|---------|-------------|
| `npx drizzle-kit generate` | Create SQL migration files from schema diff |
| `npx drizzle-kit migrate` | Apply pending migrations |
| `npx drizzle-kit push` | Sync schema directly (prototyping only) |
| `npx drizzle-kit pull` | Introspect DB → Drizzle schema |
| `npx drizzle-kit check` | Validate migration consistency |
| `npx drizzle-kit studio` | Visual database browser |

Full migrations reference: [references/migrations.md](references/migrations.md)

## Transactions

```ts
const result = await db.transaction(async (tx) => {
  const [user] = await tx.insert(users).values({ name: "Dan" }).returning();
  await tx.insert(accounts).values({ userId: user.id, balance: 0 });
  return user;
});
```

Rollback with `tx.rollback()`. Nested transactions create savepoints.

Full reference: [references/transactions-and-batch.md](references/transactions-and-batch.md)

## Raw SQL

```ts
import { sql } from "drizzle-orm";

// typed expression
const lower = sql<string>`lower(${users.name})`;

// full raw query
await db.execute(sql`SELECT * FROM ${users} WHERE ${users.id} = ${id}`);

// placeholder for prepared statements
const prepared = db.select().from(users)
  .where(eq(users.id, sql.placeholder("id")))
  .prepare("get_user");
await prepared.execute({ id: 1 });
```

## Reference Index

| Topic | File |
|-------|------|
| PostgreSQL column types, enums, schemas, indexes, views, RLS | [references/schema-postgresql.md](references/schema-postgresql.md) |
| MySQL column types, enums, indexes, views | [references/schema-mysql.md](references/schema-mysql.md) |
| SQLite column types, indexes, views | [references/schema-sqlite.md](references/schema-sqlite.md) |
| MSSQL, CockroachDB, SingleStore types | [references/column-types-minor-dialects.md](references/column-types-minor-dialects.md) |
| Full query operators, advanced select, joins, CTEs, set ops, $count | [references/queries.md](references/queries.md) |
| Relations v1 + v2, relational queries API | [references/relations.md](references/relations.md) |
| Drizzle Kit config, commands, programmatic migration | [references/migrations.md](references/migrations.md) |
| Transactions, savepoints, batch API | [references/transactions-and-batch.md](references/transactions-and-batch.md) |
| drizzle-zod, drizzle-valibot, drizzle-typebox, etc. | [references/schema-validation.md](references/schema-validation.md) |
| Connection setup per provider (Neon, Turso, Supabase, D1, PGlite, Expo, etc.) | [references/connections.md](references/connections.md) |
| Database seeding with drizzle-seed, versioning | [references/drizzle-seed.md](references/drizzle-seed.md) |
| Read replicas, custom types, caching, ESLint, gotchas, drizzle-graphql | [references/advanced-patterns.md](references/advanced-patterns.md) |
