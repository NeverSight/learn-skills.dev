---
name: supabase-test
description: Test Supabase applications with supabase-test. Use when asked to "test Supabase", "test RLS with Supabase", "write Supabase tests", or when testing applications built on Supabase.
compatibility: supabase-test, Jest/Vitest, Supabase, PostgreSQL
metadata:
  author: constructive-io
  version: "1.0.0"
---

# Testing Supabase Applications with supabase-test

TypeScript-native testing for Supabase with ephemeral databases, RLS testing, and multi-user simulation.

## When to Apply

Use this skill when:
- Testing Supabase applications
- Testing RLS policies with Supabase roles (anon, authenticated)
- Simulating authenticated users in tests
- Testing with Supabase's auth.users table

## Why supabase-test?

Traditional Supabase testing uses pgTap (SQL-based). supabase-test provides:
- Pure TypeScript tests (Jest/Vitest)
- Multi-user RLS simulation
- Direct Postgres access
- Instant test isolation
- CI-ready ephemeral databases

## Setup

### Install Dependencies

```bash
pnpm add -D supabase-test
```

### Initialize Supabase

```bash
npx supabase init
npx supabase start
```

### Configure pgpm (Optional)

If using pgpm for schema management:
```bash
pgpm init workspace
cd packages/myapp
pgpm init
pgpm install @pgpm/supabase
```

## Core Concepts

### Two Database Clients

| Client | Purpose |
|--------|---------|
| `pg` | Superuser client for setup/teardown (bypasses RLS) |
| `db` | User client for testing with Supabase roles |

### Test Isolation

Each test runs in a transaction:
- `beforeEach()` starts transaction/savepoint
- `afterEach()` rolls back
- Tests are completely isolated

## Basic Test Structure

```typescript
import { getConnections, PgTestClient } from 'supabase-test';

let pg: PgTestClient;
let db: PgTestClient;
let teardown: () => Promise<void>;

beforeAll(async () => {
  ({ pg, db, teardown } = await getConnections());
});

afterAll(async () => {
  await teardown();
});

beforeEach(async () => {
  await db.beforeEach();
});

afterEach(async () => {
  await db.afterEach();
});

it('queries the database', async () => {
  const result = await db.query('SELECT 1 + 1 AS sum');
  expect(result.rows[0].sum).toBe(2);
});
```

## Creating Test Users

Use `insertUser()` to create users in `auth.users`:

```typescript
import { getConnections, PgTestClient, insertUser } from 'supabase-test';

let pg: PgTestClient;
let db: PgTestClient;
let teardown: () => Promise<void>;

let alice: any;
let bob: any;

beforeAll(async () => {
  ({ pg, db, teardown } = await getConnections());

  // Create users in auth.users (requires superuser)
  alice = await insertUser(pg, 'alice@example.com', '550e8400-e29b-41d4-a716-446655440001');
  bob = await insertUser(pg, 'bob@example.com', '550e8400-e29b-41d4-a716-446655440002');
});
```

**Parameters:**
- `pg` - Superuser client (required for auth.users)
- `email` - User's email
- `id` - Optional UUID (auto-generated if omitted)

## Setting User Context

Simulate Supabase roles with `setContext()`:

```typescript
// Authenticated user
db.setContext({
  role: 'authenticated',
  'request.jwt.claim.sub': alice.id
});

// Anonymous user
db.setContext({ role: 'anon' });

// Service role (admin)
db.setContext({ role: 'service_role' });
```

## Testing RLS Policies

### User Can Access Own Data

```typescript
it('user can insert own record', async () => {
  db.setContext({
    role: 'authenticated',
    'request.jwt.claim.sub': alice.id
  });

  const result = await db.one(`
    INSERT INTO app.posts (title, owner_id)
    VALUES ($1, $2)
    RETURNING id, title, owner_id
  `, ['My Post', alice.id]);

  expect(result.title).toBe('My Post');
  expect(result.owner_id).toBe(alice.id);
});
```

### User Cannot Access Others' Data

```typescript
it('user cannot see other users data', async () => {
  // Bob creates a post
  db.setContext({
    role: 'authenticated',
    'request.jwt.claim.sub': bob.id
  });

  await db.one(`
    INSERT INTO app.posts (title, owner_id)
    VALUES ($1, $2)
    RETURNING id
  `, ['Bob Post', bob.id]);

  // Alice queries - should not see Bob's post
  db.setContext({
    role: 'authenticated',
    'request.jwt.claim.sub': alice.id
  });

  const result = await db.query('SELECT * FROM app.posts');
  expect(result.rows).toHaveLength(0);
});
```

### Testing Permission Denied

Use savepoint pattern for expected failures:

```typescript
it('anonymous cannot insert', async () => {
  db.setContext({ role: 'anon' });

  const point = 'anon_insert';
  await db.savepoint(point);

  await expect(
    db.query(`INSERT INTO app.posts (title) VALUES ('Hacked')`)
  ).rejects.toThrow(/permission denied/);

  await db.rollback(point);
});
```

## Seeding Test Data

### With insertUser()

```typescript
beforeAll(async () => {
  ({ pg, db, teardown } = await getConnections());

  alice = await insertUser(pg, 'alice@example.com');
  bob = await insertUser(pg, 'bob@example.com');
});
```

### With loadJson()

```typescript
beforeAll(async () => {
  ({ pg, db, teardown } = await getConnections());

  alice = await insertUser(pg, 'alice@example.com', '550e8400-e29b-41d4-a716-446655440001');

  await pg.loadJson({
    'app.posts': [
      { title: 'Post 1', owner_id: alice.id },
      { title: 'Post 2', owner_id: alice.id }
    ]
  });
});
```

### With loadSql()

```typescript
import path from 'path';

beforeAll(async () => {
  ({ pg, db, teardown } = await getConnections());

  await pg.loadSql([
    path.join(__dirname, 'fixtures/seed.sql')
  ]);
});
```

### With loadCsv()

```typescript
import path from 'path';

beforeAll(async () => {
  ({ pg, db, teardown } = await getConnections());

  await pg.loadCsv({
    'app.posts': path.join(__dirname, 'fixtures/posts.csv')
  });
});
```

**Note:** `loadCsv()` bypasses RLS (uses COPY). Always use `pg` client.

## Query Methods

| Method | Returns | Use Case |
|--------|---------|----------|
| `db.query(sql, params)` | `{ rows: [...] }` | Multiple rows |
| `db.one(sql, params)` | Single row object | Exactly one row |
| `db.many(sql, params)` | Array of rows | Multiple rows (array) |

```typescript
// Multiple rows
const result = await db.query('SELECT * FROM app.posts');
console.log(result.rows);

// Single row (throws if not exactly one)
const post = await db.one('SELECT * FROM app.posts WHERE id = $1', [postId]);
console.log(post.title);

// Array of rows
const posts = await db.many('SELECT * FROM app.posts');
console.log(posts.length);
```

## Complete Example

```typescript
import { getConnections, PgTestClient, insertUser } from 'supabase-test';

let pg: PgTestClient;
let db: PgTestClient;
let teardown: () => Promise<void>;

let alice: any;
let bob: any;

beforeAll(async () => {
  ({ pg, db, teardown } = await getConnections());

  alice = await insertUser(pg, 'alice@example.com');
  bob = await insertUser(pg, 'bob@example.com');
});

afterAll(async () => {
  await teardown();
});

beforeEach(async () => {
  await db.beforeEach();
});

afterEach(async () => {
  await db.afterEach();
});

describe('RLS policies', () => {
  it('users only see their own posts', async () => {
    // Alice creates a post
    db.setContext({
      role: 'authenticated',
      'request.jwt.claim.sub': alice.id
    });

    await db.one(`
      INSERT INTO app.posts (title, owner_id)
      VALUES ('Alice Post', $1)
      RETURNING id
    `, [alice.id]);

    // Bob creates a post
    db.setContext({
      role: 'authenticated',
      'request.jwt.claim.sub': bob.id
    });

    await db.one(`
      INSERT INTO app.posts (title, owner_id)
      VALUES ('Bob Post', $1)
      RETURNING id
    `, [bob.id]);

    // Alice queries - only sees her post
    db.setContext({
      role: 'authenticated',
      'request.jwt.claim.sub': alice.id
    });

    const result = await db.many('SELECT title FROM app.posts');
    expect(result).toHaveLength(1);
    expect(result[0].title).toBe('Alice Post');
  });
});
```

## Running Tests

```bash
# Run all tests
pnpm test

# Watch mode
pnpm test:watch
```

## References

- Related skill: `pgsql-test-rls` for general RLS testing patterns
- Related skill: `pgsql-test-seeding` for seeding strategies
- Related skill: `pgsql-test-exceptions` for handling aborted transactions
