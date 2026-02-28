---
name: pgsql-test-rls
description: Test Row-Level Security (RLS) policies with pgsql-test. Use when asked to "test RLS", "test permissions", "test user access", "verify security policies", or when writing tests for multi-tenant applications.
compatibility: pgsql-test, Jest/Vitest, PostgreSQL
metadata:
  author: constructive-io
  version: "1.0.0"
---

# Testing RLS Policies with pgsql-test

Test Row-Level Security policies by simulating different users and roles. Verify your security policies work correctly with isolated, transactional tests.

## When to Apply

Use this skill when:
- Testing RLS policies for multi-tenant applications
- Verifying user isolation (users only see their own data)
- Testing role-based access (anonymous, authenticated, admin)
- Validating INSERT/UPDATE/DELETE policies

## Setup

Install pgsql-test:
```bash
pnpm add -D pgsql-test
```

Configure Jest/Vitest with the test database.

## Core Concepts

### Two Database Clients

pgsql-test provides two clients:

| Client | Purpose |
|--------|---------|
| `pg` | Superuser client for setup/teardown (bypasses RLS) |
| `db` | User client for testing with RLS enforcement |

### Test Isolation

Each test runs in a transaction with savepoints:
- `beforeEach()` starts a savepoint
- `afterEach()` rolls back to savepoint
- Tests are completely isolated

## Basic RLS Test Structure

```typescript
import { getConnections, PgTestClient } from 'pgsql-test';

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
  await pg.beforeEach();
  await db.beforeEach();
});

afterEach(async () => {
  await db.afterEach();
  await pg.afterEach();
});
```

## Setting User Context

Use `setContext()` to simulate different users:

```typescript
// Simulate authenticated user
db.setContext({
  role: 'authenticated',
  'request.jwt.claim.sub': userId
});

// Simulate anonymous user
db.setContext({ role: 'anonymous' });

// Simulate admin
db.setContext({
  role: 'administrator',
  'request.jwt.claim.sub': adminId
});
```

## Testing SELECT Policies

Verify users only see their own data:

```typescript
it('users only see their own records', async () => {
  // Setup: Insert data as superuser
  await pg.query(`
    INSERT INTO app.posts (id, title, owner_id) VALUES
    ('post-1', 'User 1 Post', $1),
    ('post-2', 'User 2 Post', $2)
  `, [user1Id, user2Id]);

  // Test: User 1 queries
  db.setContext({
    role: 'authenticated',
    'request.jwt.claim.sub': user1Id
  });

  const result = await db.query('SELECT * FROM app.posts');
  
  expect(result.rows).toHaveLength(1);
  expect(result.rows[0].title).toBe('User 1 Post');
});
```

## Testing INSERT Policies

Verify users can only insert their own data:

```typescript
it('user can insert own record', async () => {
  db.setContext({
    role: 'authenticated',
    'request.jwt.claim.sub': userId
  });

  const result = await db.one(`
    INSERT INTO app.posts (title, owner_id)
    VALUES ('My Post', $1)
    RETURNING id, title, owner_id
  `, [userId]);

  expect(result.title).toBe('My Post');
  expect(result.owner_id).toBe(userId);
});

it('user cannot insert for another user', async () => {
  db.setContext({
    role: 'authenticated',
    'request.jwt.claim.sub': user1Id
  });

  // Use savepoint pattern for expected failures
  const point = 'insert_other_user';
  await db.savepoint(point);

  await expect(
    db.query(`
      INSERT INTO app.posts (title, owner_id)
      VALUES ('Hacked Post', $1)
    `, [user2Id])
  ).rejects.toThrow(/permission denied|violates row-level security/);

  await db.rollback(point);
});
```

## Testing UPDATE Policies

```typescript
it('user can update own record', async () => {
  // Setup
  await pg.query(`
    INSERT INTO app.posts (id, title, owner_id)
    VALUES ('post-1', 'Original', $1)
  `, [userId]);

  // Test
  db.setContext({
    role: 'authenticated',
    'request.jwt.claim.sub': userId
  });

  const result = await db.one(`
    UPDATE app.posts SET title = 'Updated'
    WHERE id = 'post-1'
    RETURNING title
  `);

  expect(result.title).toBe('Updated');
});

it('user cannot update another user record', async () => {
  await pg.query(`
    INSERT INTO app.posts (id, title, owner_id)
    VALUES ('post-1', 'Original', $1)
  `, [user2Id]);

  db.setContext({
    role: 'authenticated',
    'request.jwt.claim.sub': user1Id
  });

  // Update returns no rows (RLS filters it out)
  const result = await db.query(`
    UPDATE app.posts SET title = 'Hacked'
    WHERE id = 'post-1'
    RETURNING id
  `);

  expect(result.rows).toHaveLength(0);
});
```

## Testing DELETE Policies

```typescript
it('user can delete own record', async () => {
  await pg.query(`
    INSERT INTO app.posts (id, title, owner_id)
    VALUES ('post-1', 'To Delete', $1)
  `, [userId]);

  db.setContext({
    role: 'authenticated',
    'request.jwt.claim.sub': userId
  });

  await db.query(`DELETE FROM app.posts WHERE id = 'post-1'`);

  // Verify as superuser
  const result = await pg.query(`
    SELECT * FROM app.posts WHERE id = 'post-1'
  `);
  expect(result.rows).toHaveLength(0);
});
```

## Testing Anonymous Access

```typescript
it('anonymous users have read-only access', async () => {
  await pg.query(`
    INSERT INTO app.public_posts (id, title)
    VALUES ('post-1', 'Public Post')
  `);

  db.setContext({ role: 'anonymous' });

  // Can read public data
  const result = await db.query('SELECT * FROM app.public_posts');
  expect(result.rows).toHaveLength(1);

  // Cannot modify
  const point = 'anon_insert';
  await db.savepoint(point);
  await expect(
    db.query(`INSERT INTO app.public_posts (title) VALUES ('Hacked')`)
  ).rejects.toThrow(/permission denied/);
  await db.rollback(point);
});
```

## Multi-User Scenarios

Test interactions between multiple users:

```typescript
describe('multi-user isolation', () => {
  const alice = '550e8400-e29b-41d4-a716-446655440001';
  const bob = '550e8400-e29b-41d4-a716-446655440002';

  beforeEach(async () => {
    // Seed data for both users
    await pg.query(`
      INSERT INTO app.posts (title, owner_id) VALUES
      ('Alice Post 1', $1),
      ('Alice Post 2', $1),
      ('Bob Post 1', $2)
    `, [alice, bob]);
  });

  it('alice sees only her posts', async () => {
    db.setContext({
      role: 'authenticated',
      'request.jwt.claim.sub': alice
    });

    const result = await db.query('SELECT title FROM app.posts ORDER BY title');
    expect(result.rows).toHaveLength(2);
    expect(result.rows.map(r => r.title)).toEqual(['Alice Post 1', 'Alice Post 2']);
  });

  it('bob sees only his posts', async () => {
    db.setContext({
      role: 'authenticated',
      'request.jwt.claim.sub': bob
    });

    const result = await db.query('SELECT title FROM app.posts');
    expect(result.rows).toHaveLength(1);
    expect(result.rows[0].title).toBe('Bob Post 1');
  });
});
```

## Handling Expected Failures

When testing operations that should fail, use the savepoint pattern to avoid "current transaction is aborted" errors:

```typescript
it('rejects unauthorized access', async () => {
  db.setContext({ role: 'anonymous' });

  const point = 'unauthorized_access';
  await db.savepoint(point);

  await expect(
    db.query('INSERT INTO app.private_data (secret) VALUES ($1)', ['hack'])
  ).rejects.toThrow(/permission denied/);

  await db.rollback(point);

  // Can continue using db connection
  const result = await db.query('SELECT 1 as ok');
  expect(result.rows[0].ok).toBe(1);
});
```

## Watch Mode

Run tests in watch mode for rapid feedback:
```bash
pnpm test:watch
```

## References

- Related skill: `pgsql-test-exceptions` for handling aborted transactions
- Related skill: `pgsql-test-seeding` for seeding test data
- Related skill: `pgpm-testing` for general test setup
