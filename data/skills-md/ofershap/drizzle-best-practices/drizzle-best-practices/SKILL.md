---
name: drizzle-best-practices
description:
  Drizzle ORM done right. Schema design, relations, type-safe queries, migrations, and performance
  patterns.
metadata:
  tags: drizzle, database, orm, best-practices
---

## When to use

Use this skill when working with Drizzle ORM code. Agents often confuse Drizzle with Prisma and
produce wrong schema syntax, incorrect relation patterns, or manual SQL where the query builder
should be used.

## Critical Rules

### 1. Schema definition: use pgTable/mysqlTable/sqliteTable, not Prisma-style

**Wrong (agents do this):**

```
model User {
  id    Int    @id @default(autoincrement())
  name  String
  posts Post[]
}
```

**Correct:**

```
import { pgTable, serial, text } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
});
```

**Why:** Drizzle uses table-definition functions, not a Prisma-like DSL. Wrong syntax fails at
compile time.

### 2. Relations: use relations(), not foreign key decorators

**Wrong:**

```
// Expecting Prisma-style @relation or Sequelize belongsTo
```

**Correct:**

```
import { relations } from 'drizzle-orm';

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, { fields: [posts.authorId], references: [users.id] }),
}));
```

**Why:** Drizzle relations are defined separately from tables via `relations()`. Foreign keys go on
the table; relation metadata goes in relations.

### 3. Queries: use query builder API, not raw SQL

**Wrong:**

```
const users = await db.execute(sql`SELECT * FROM users WHERE id = ${id}`);
```

**Correct:**

```
import { eq } from 'drizzle-orm';

const result = await db.select().from(users).where(eq(users.id, id));
```

**Why:** Query builder gives type safety, SQL injection protection, and dialect portability. Raw SQL
only when the builder cannot express the query.

### 4. Type inference: use $inferSelect and $inferInsert

**Wrong:**

```
interface User {
  id: number;
  name: string;
}
```

**Correct:**

```
type SelectUser = typeof users.$inferSelect;
type InsertUser = typeof users.$inferInsert;
```

**Why:** Inferred types stay in sync with schema. Manual types drift and break on schema changes.

### 5. Prepared statements for frequent queries

**Wrong:**

```
for (const id of ids) {
  await db.select().from(users).where(eq(users.id, id));
}
```

**Correct:**

```
import { sql } from 'drizzle-orm';

const getById = db
  .select()
  .from(users)
  .where(eq(users.id, sql.placeholder('id')))
  .prepare();

for (const id of ids) {
  await getById.execute({ id });
}
```

**Why:** Prepared statements reduce parse/plan overhead and improve performance for repeated
queries.

### 6. Transactions: use db.transaction()

**Wrong:**

```
await db.execute(sql`BEGIN`);
await db.insert(users).values(u);
await db.execute(sql`COMMIT`);
```

**Correct:**

```
await db.transaction(async (tx) => {
  await tx.insert(users).values(u);
  await tx.insert(posts).values(p);
});
```

**Why:** Drizzle transactions handle BEGIN/COMMIT/ROLLBACK and ensure the same connection is used
throughout.

### 7. Migrations: drizzle-kit generate and migrate

**Wrong:**

```
// Hand-written 001_create_users.sql
```

**Correct:**

```
drizzle-kit generate
drizzle-kit migrate
```

**Why:** Generated migrations stay in sync with schema and support rollback. Manual SQL bypasses
Drizzle's migration tracking.

### 8. Where clauses: use operators from drizzle-orm

**Wrong:**

```
db.select().from(users).where(sql`name = ${name}`);
```

**Correct:**

```
import { eq, like, gt, lt } from 'drizzle-orm';

db.select().from(users).where(eq(users.name, name));
db.select().from(users).where(like(users.name, '%foo%'));
```

**Why:** Operators are type-safe and parameterized. Raw template strings risk SQL injection.

### 9. Nested data: use relational queries

**Wrong:**

```
const users = await db.select().from(users);
for (const u of users) {
  u.posts = await db.select().from(posts).where(eq(posts.authorId, u.id));
}
```

**Correct:**

```
const usersWithPosts = await db.query.users.findMany({
  with: { posts: true },
});
```

**Why:** Relational API fetches nested data in one call with correct joins and typing.

### 10. Indexes: define in schema

**Wrong:**

```
// Separate migration: CREATE INDEX ...
```

**Correct:**

```
import { index } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: text('email').notNull(),
}, (t) => [
  index('users_email_idx').on(t.email),
]);
```

**Why:** Indexes in schema are versioned and migrated with the rest of the schema.

### 11. Validation: use drizzle-zod

**Wrong:**

```
// Manually maintaining Zod schema that mirrors DB
```

**Correct:**

```
import { createInsertSchema } from 'drizzle-zod';

const insertUserSchema = createInsertSchema(usersTable);
```

**Why:** drizzle-zod derives Zod schemas from Drizzle tables, keeping validation in sync.

### 12. Connection pooling: configure for serverless

**Wrong:**

```
const db = drizzle(process.env.DATABASE_URL);
```

**Correct:**

```
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';

const client = postgres(url, { max: 10, idle_timeout: 20 });
const db = drizzle(client);
```

**Why:** Serverless needs bounded connections. Default pooling can exhaust DB connections.

## Patterns

- Export schema object for drizzle({ schema }) when using relational queries
- Use `.returning()` after insert/update to get affected rows
- Prefer `findFirst` over `findMany` when expecting a single row
- Use `.$dynamic()` for conditional where/orderBy/limit

## Anti-Patterns

- Do not mix Prisma and Drizzle syntax
- Do not use raw SQL for simple CRUD
- Do not define manual types that duplicate schema
- Do not use push in production; use generate + migrate
- Do not create new db/drizzle instances per request in serverless
