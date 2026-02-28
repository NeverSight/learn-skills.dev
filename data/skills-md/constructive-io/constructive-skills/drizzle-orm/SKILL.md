---
name: drizzle-orm
description: Drizzle ORM patterns for PostgreSQL schema design and queries. Use when asked to "design Drizzle schema", "write Drizzle queries", "set up Drizzle ORM", or when building type-safe database layers.
compatibility: drizzle-orm, drizzle-kit, PostgreSQL, TypeScript
metadata:
  author: constructive-io
  version: "1.0.0"
---

# Drizzle ORM Patterns

Design PostgreSQL schemas and write type-safe queries with Drizzle ORM. This skill covers schema design patterns, query building, and integration with the Constructive ecosystem.

## When to Apply

Use this skill when:
- Designing database schemas with Drizzle
- Writing type-safe database queries
- Setting up Drizzle ORM in a project
- Integrating Drizzle with pgsql-test or drizzle-orm-test

## Installation

```bash
pnpm add drizzle-orm
pnpm add -D drizzle-kit
```

## Schema Design

### Basic Table Definition

```typescript
import { pgTable, uuid, text, timestamp, boolean, integer } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: text('email').notNull().unique(),
  name: text('name'),
  isActive: boolean('is_active').default(true),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow()
});
```

### Foreign Key Relations

```typescript
import { pgTable, uuid, text, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: text('email').notNull().unique()
});

export const posts = pgTable('posts', {
  id: uuid('id').primaryKey().defaultRandom(),
  title: text('title').notNull(),
  content: text('content'),
  authorId: uuid('author_id').references(() => users.id).notNull(),
  createdAt: timestamp('created_at').defaultNow()
});

export const comments = pgTable('comments', {
  id: uuid('id').primaryKey().defaultRandom(),
  content: text('content').notNull(),
  postId: uuid('post_id').references(() => posts.id).notNull(),
  authorId: uuid('author_id').references(() => users.id).notNull()
});
```

### Indexes

```typescript
import { pgTable, uuid, text, index, uniqueIndex } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: text('email').notNull(),
  organizationId: uuid('organization_id').notNull()
}, (table) => [
  uniqueIndex('users_email_idx').on(table.email),
  index('users_org_idx').on(table.organizationId)
]);
```

### Composite Primary Keys

```typescript
import { pgTable, uuid, primaryKey } from 'drizzle-orm/pg-core';

export const userRoles = pgTable('user_roles', {
  userId: uuid('user_id').references(() => users.id).notNull(),
  roleId: uuid('role_id').references(() => roles.id).notNull()
}, (table) => [
  primaryKey({ columns: [table.userId, table.roleId] })
]);
```

### Enums

```typescript
import { pgTable, uuid, pgEnum } from 'drizzle-orm/pg-core';

export const statusEnum = pgEnum('status', ['pending', 'active', 'archived']);

export const projects = pgTable('projects', {
  id: uuid('id').primaryKey().defaultRandom(),
  name: text('name').notNull(),
  status: statusEnum('status').default('pending')
});
```

### JSON Columns

```typescript
import { pgTable, uuid, jsonb } from 'drizzle-orm/pg-core';

export const settings = pgTable('settings', {
  id: uuid('id').primaryKey().defaultRandom(),
  userId: uuid('user_id').references(() => users.id).notNull(),
  preferences: jsonb('preferences').$type<{
    theme: 'light' | 'dark';
    notifications: boolean;
  }>()
});
```

## Query Patterns

### Setup Client

```typescript
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';
import * as schema from './schema';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

export const db = drizzle(pool, { schema });
```

### Select Queries

```typescript
import { eq, and, or, like, gt, lt, isNull, inArray } from 'drizzle-orm';
import { users, posts } from './schema';

// Select all
const allUsers = await db.select().from(users);

// Select with where
const activeUsers = await db
  .select()
  .from(users)
  .where(eq(users.isActive, true));

// Select specific columns
const userEmails = await db
  .select({ email: users.email, name: users.name })
  .from(users);

// Multiple conditions
const filteredUsers = await db
  .select()
  .from(users)
  .where(and(
    eq(users.isActive, true),
    like(users.email, '%@example.com')
  ));

// OR conditions
const result = await db
  .select()
  .from(users)
  .where(or(
    eq(users.name, 'Alice'),
    eq(users.name, 'Bob')
  ));

// IN clause
const specificUsers = await db
  .select()
  .from(users)
  .where(inArray(users.id, ['id1', 'id2', 'id3']));

// NULL checks
const usersWithoutName = await db
  .select()
  .from(users)
  .where(isNull(users.name));
```

### Insert Queries

```typescript
// Single insert
const [newUser] = await db
  .insert(users)
  .values({
    email: 'alice@example.com',
    name: 'Alice'
  })
  .returning();

// Multiple insert
const newUsers = await db
  .insert(users)
  .values([
    { email: 'alice@example.com', name: 'Alice' },
    { email: 'bob@example.com', name: 'Bob' }
  ])
  .returning();

// Insert with conflict handling
await db
  .insert(users)
  .values({ email: 'alice@example.com', name: 'Alice' })
  .onConflictDoNothing();

// Upsert
await db
  .insert(users)
  .values({ email: 'alice@example.com', name: 'Alice' })
  .onConflictDoUpdate({
    target: users.email,
    set: { name: 'Alice Updated' }
  });
```

### Update Queries

```typescript
// Update with where
const [updated] = await db
  .update(users)
  .set({ name: 'Alice Smith' })
  .where(eq(users.id, userId))
  .returning();

// Update multiple fields
await db
  .update(users)
  .set({
    name: 'Alice Smith',
    updatedAt: new Date()
  })
  .where(eq(users.id, userId));
```

### Delete Queries

```typescript
// Delete with where
await db
  .delete(users)
  .where(eq(users.id, userId));

// Delete with returning
const [deleted] = await db
  .delete(users)
  .where(eq(users.id, userId))
  .returning();
```

### Joins

```typescript
// Inner join
const postsWithAuthors = await db
  .select({
    postTitle: posts.title,
    authorName: users.name
  })
  .from(posts)
  .innerJoin(users, eq(posts.authorId, users.id));

// Left join
const usersWithPosts = await db
  .select({
    userName: users.name,
    postTitle: posts.title
  })
  .from(users)
  .leftJoin(posts, eq(users.id, posts.authorId));
```

### Relational Queries

With schema relations defined:

```typescript
import { relations } from 'drizzle-orm';

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts)
}));

export const postsRelations = relations(posts, ({ one, many }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id]
  }),
  comments: many(comments)
}));
```

Query with relations:

```typescript
// Fetch users with their posts
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: true
  }
});

// Nested relations
const usersWithPostsAndComments = await db.query.users.findMany({
  with: {
    posts: {
      with: {
        comments: true
      }
    }
  }
});

// Selective columns with relations
const result = await db.query.users.findMany({
  columns: {
    id: true,
    name: true
  },
  with: {
    posts: {
      columns: {
        title: true
      }
    }
  }
});
```

### Aggregations

```typescript
import { count, sum, avg, max, min } from 'drizzle-orm';

// Count
const [{ total }] = await db
  .select({ total: count() })
  .from(users);

// Count with condition
const [{ activeCount }] = await db
  .select({ activeCount: count() })
  .from(users)
  .where(eq(users.isActive, true));

// Group by
const postCounts = await db
  .select({
    authorId: posts.authorId,
    postCount: count()
  })
  .from(posts)
  .groupBy(posts.authorId);
```

### Ordering and Pagination

```typescript
import { desc, asc } from 'drizzle-orm';

// Order by
const sortedUsers = await db
  .select()
  .from(users)
  .orderBy(desc(users.createdAt));

// Multiple order columns
const sorted = await db
  .select()
  .from(users)
  .orderBy(asc(users.name), desc(users.createdAt));

// Pagination
const page = await db
  .select()
  .from(users)
  .limit(10)
  .offset(20);
```

### Transactions

```typescript
await db.transaction(async (tx) => {
  const [user] = await tx
    .insert(users)
    .values({ email: 'alice@example.com' })
    .returning();

  await tx
    .insert(posts)
    .values({
      title: 'First Post',
      authorId: user.id
    });
});
```

## Integration with pgsql-test

```typescript
import { getConnections, PgTestClient } from 'drizzle-orm-test';
import { drizzle } from 'drizzle-orm/node-postgres';
import * as schema from './schema';

let pg: PgTestClient;
let db: ReturnType<typeof drizzle>;
let teardown: () => Promise<void>;

beforeAll(async () => {
  ({ pg, teardown } = await getConnections());
  db = drizzle(pg.client, { schema });
});

afterAll(async () => {
  await teardown();
});

beforeEach(async () => {
  await pg.beforeEach();
});

afterEach(async () => {
  await pg.afterEach();
});

it('creates a user', async () => {
  const [user] = await db
    .insert(schema.users)
    .values({ email: 'test@example.com' })
    .returning();

  expect(user.email).toBe('test@example.com');
});
```

## Schema Organization

For larger projects, organize schemas by domain:

```
src/
  db/
    schema/
      index.ts        # Re-exports all schemas
      users.ts        # User-related tables
      posts.ts        # Post-related tables
      relations.ts    # All relations
    client.ts         # Drizzle client setup
```

```typescript
// src/db/schema/index.ts
export * from './users';
export * from './posts';
export * from './relations';
```

## Best Practices

1. **Use UUID primary keys**: `uuid('id').primaryKey().defaultRandom()`
2. **Add timestamps**: Include `createdAt` and `updatedAt` on most tables
3. **Define relations**: Enable relational queries with `relations()`
4. **Type JSON columns**: Use `.$type<T>()` for type-safe JSON
5. **Index foreign keys**: Add indexes on frequently queried foreign keys
6. **Use transactions**: Wrap related operations in transactions
7. **Return inserted/updated rows**: Use `.returning()` to get results

## References

- Related skill: `drizzle-orm-test` for testing with Drizzle
- Related skill: `pgsql-test-snapshot` for snapshot testing
- Related skill: `pgsql-test-rls` for RLS testing with Drizzle
