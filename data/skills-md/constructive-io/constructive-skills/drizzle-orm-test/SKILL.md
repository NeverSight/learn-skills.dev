---
name: drizzle-orm-test
description: Test PostgreSQL databases with Drizzle ORM using drizzle-orm-test. Use when asked to "test with Drizzle", "test Drizzle ORM", "write type-safe database tests", or when testing applications using Drizzle ORM.
compatibility: drizzle-orm-test, drizzle-orm, Jest/Vitest, PostgreSQL
metadata:
  author: constructive-io
  version: "1.0.0"
---

# Testing with Drizzle ORM

Test PostgreSQL databases with Drizzle ORM using drizzle-orm-test. Get type-safe queries, automatic context management, and RLS testing.

## When to Apply

Use this skill when:
- Testing applications using Drizzle ORM
- Writing type-safe database tests
- Testing RLS policies with Drizzle
- Migrating from pgsql-test to Drizzle

## Why drizzle-orm-test?

drizzle-orm-test is a drop-in replacement for pgsql-test that adds:
- Type-safe queries with Drizzle ORM
- Automatic context management
- Same test isolation patterns
- Compatible with existing pgsql-test workflows

## Setup

### Install Dependencies

```bash
pnpm add -D drizzle-orm-test drizzle-orm
```

### Define Drizzle Schema

Create `src/schema.ts`:

```typescript
import { pgTable, uuid, text, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: text('email').notNull().unique(),
  name: text('name'),
  createdAt: timestamp('created_at').defaultNow()
});

export const posts = pgTable('posts', {
  id: uuid('id').primaryKey().defaultRandom(),
  title: text('title').notNull(),
  content: text('content'),
  ownerId: uuid('owner_id').references(() => users.id),
  createdAt: timestamp('created_at').defaultNow()
});
```

## Core Concepts

### Three Database Clients

| Client | Purpose |
|--------|---------|
| `pg` | Superuser pgsql-test client (bypasses RLS) |
| `db` | User pgsql-test client (for RLS context) |
| `drizzleDb` | Drizzle ORM client (type-safe queries) |

### Test Isolation

Same as pgsql-test:
- `beforeEach()` starts transaction/savepoint
- `afterEach()` rolls back
- Tests are completely isolated

## Basic Test Structure

```typescript
import { getConnections, PgTestClient } from 'drizzle-orm-test';
import { drizzle } from 'drizzle-orm/node-postgres';
import { users, posts } from '../src/schema';

let pg: PgTestClient;
let db: PgTestClient;
let teardown: () => Promise<void>;
let drizzleDb: ReturnType<typeof drizzle>;

beforeAll(async () => {
  ({ pg, db, teardown } = await getConnections());
  
  // Create Drizzle client from pg connection
  drizzleDb = drizzle(pg.client);
});

afterAll(async () => {
  await teardown();
});

beforeEach(async () => {
  await pg.beforeEach();
  await db.beforeEach();
});

afterEach(async () => {
  await db.afterEach();
  await pg.afterEach();
});
```

## Type-Safe Queries

### Insert

```typescript
it('inserts a user with Drizzle', async () => {
  const [user] = await drizzleDb
    .insert(users)
    .values({
      email: 'alice@example.com',
      name: 'Alice'
    })
    .returning();

  expect(user.email).toBe('alice@example.com');
  expect(user.name).toBe('Alice');
  expect(user.id).toBeDefined();
});
```

### Select

```typescript
it('queries users with Drizzle', async () => {
  // Insert test data
  await drizzleDb.insert(users).values([
    { email: 'alice@example.com', name: 'Alice' },
    { email: 'bob@example.com', name: 'Bob' }
  ]);

  // Query with type safety
  const result = await drizzleDb
    .select()
    .from(users)
    .where(eq(users.name, 'Alice'));

  expect(result).toHaveLength(1);
  expect(result[0].email).toBe('alice@example.com');
});
```

### Update

```typescript
import { eq } from 'drizzle-orm';

it('updates a user', async () => {
  const [user] = await drizzleDb
    .insert(users)
    .values({ email: 'alice@example.com', name: 'Alice' })
    .returning();

  const [updated] = await drizzleDb
    .update(users)
    .set({ name: 'Alice Smith' })
    .where(eq(users.id, user.id))
    .returning();

  expect(updated.name).toBe('Alice Smith');
});
```

### Delete

```typescript
it('deletes a user', async () => {
  const [user] = await drizzleDb
    .insert(users)
    .values({ email: 'alice@example.com' })
    .returning();

  await drizzleDb
    .delete(users)
    .where(eq(users.id, user.id));

  const result = await drizzleDb
    .select()
    .from(users)
    .where(eq(users.id, user.id));

  expect(result).toHaveLength(0);
});
```

## Testing RLS with Drizzle

For RLS testing, use `db.setContext()` with the pgsql-test client, then query with Drizzle:

```typescript
import { getConnections, PgTestClient } from 'drizzle-orm-test';
import { drizzle } from 'drizzle-orm/node-postgres';
import { eq } from 'drizzle-orm';
import { posts } from '../src/schema';

let pg: PgTestClient;
let db: PgTestClient;
let teardown: () => Promise<void>;
let drizzleDb: ReturnType<typeof drizzle>;

const alice = '550e8400-e29b-41d4-a716-446655440001';
const bob = '550e8400-e29b-41d4-a716-446655440002';

beforeAll(async () => {
  ({ pg, db, teardown } = await getConnections());
  
  // Create Drizzle client from db connection (respects RLS)
  drizzleDb = drizzle(db.client);
});

afterAll(async () => {
  await teardown();
});

beforeEach(async () => {
  await pg.beforeEach();
  await db.beforeEach();
});

afterEach(async () => {
  await db.afterEach();
  await pg.afterEach();
});

it('user only sees own posts', async () => {
  // Seed as superuser
  await pg.loadJson({
    'posts': [
      { title: 'Alice Post', owner_id: alice },
      { title: 'Bob Post', owner_id: bob }
    ]
  });

  // Set context to Alice
  db.setContext({
    role: 'authenticated',
    'request.jwt.claim.sub': alice
  });

  // Query with Drizzle - RLS filters results
  const result = await drizzleDb
    .select()
    .from(posts);

  expect(result).toHaveLength(1);
  expect(result[0].title).toBe('Alice Post');
});
```

## Testing INSERT Policies

```typescript
it('user can insert own post', async () => {
  db.setContext({
    role: 'authenticated',
    'request.jwt.claim.sub': alice
  });

  const [post] = await drizzleDb
    .insert(posts)
    .values({
      title: 'My Post',
      ownerId: alice
    })
    .returning();

  expect(post.title).toBe('My Post');
  expect(post.ownerId).toBe(alice);
});

it('user cannot insert for another user', async () => {
  db.setContext({
    role: 'authenticated',
    'request.jwt.claim.sub': alice
  });

  const point = 'insert_other';
  await db.savepoint(point);

  await expect(
    drizzleDb
      .insert(posts)
      .values({
        title: 'Hacked Post',
        ownerId: bob
      })
  ).rejects.toThrow(/permission denied|violates row-level security/);

  await db.rollback(point);
});
```

## Testing UPDATE Policies

```typescript
it('user can update own post', async () => {
  // Seed
  await pg.loadJson({
    'posts': [{ id: 'post-1', title: 'Original', owner_id: alice }]
  });

  db.setContext({
    role: 'authenticated',
    'request.jwt.claim.sub': alice
  });

  const [updated] = await drizzleDb
    .update(posts)
    .set({ title: 'Updated' })
    .where(eq(posts.id, 'post-1'))
    .returning();

  expect(updated.title).toBe('Updated');
});

it('user cannot update other user post', async () => {
  await pg.loadJson({
    'posts': [{ id: 'post-1', title: 'Bob Post', owner_id: bob }]
  });

  db.setContext({
    role: 'authenticated',
    'request.jwt.claim.sub': alice
  });

  // RLS filters - update affects 0 rows
  const result = await drizzleDb
    .update(posts)
    .set({ title: 'Hacked' })
    .where(eq(posts.id, 'post-1'))
    .returning();

  expect(result).toHaveLength(0);
});
```

## Testing DELETE Policies

```typescript
it('user can delete own post', async () => {
  await pg.loadJson({
    'posts': [{ id: 'post-1', title: 'My Post', owner_id: alice }]
  });

  db.setContext({
    role: 'authenticated',
    'request.jwt.claim.sub': alice
  });

  await drizzleDb
    .delete(posts)
    .where(eq(posts.id, 'post-1'));

  // Verify as superuser
  const result = await pg.query('SELECT * FROM posts WHERE id = $1', ['post-1']);
  expect(result.rows).toHaveLength(0);
});
```

## Handling Expected Failures

Use savepoint pattern with Drizzle:

```typescript
it('anonymous cannot insert', async () => {
  db.setContext({ role: 'anonymous' });

  const point = 'anon_insert';
  await db.savepoint(point);

  await expect(
    drizzleDb
      .insert(posts)
      .values({ title: 'Hacked' })
  ).rejects.toThrow(/permission denied/);

  await db.rollback(point);
});
```

## Watch Mode

```bash
pnpm test:watch
```

## Best Practices

1. **Use `pg` for setup**: Bypass RLS when seeding
2. **Use `db` for context**: Set role/user context
3. **Use Drizzle for queries**: Type-safe assertions
4. **Savepoint for failures**: Handle expected errors
5. **Schema in sync**: Keep Drizzle schema matching database

## References

- Related skill: `pgsql-test-rls` for RLS testing patterns
- Related skill: `pgsql-test-exceptions` for handling aborted transactions
- Related skill: `pgsql-test-seeding` for seeding strategies
