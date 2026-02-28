---
name: pgpm-testing
description: Run PostgreSQL integration tests with isolated databases using pgsql-test. Use when asked to "run database tests", "set up test database", "write integration tests", "test PGPM modules", or when implementing tests that need PostgreSQL.
compatibility: Node.js 18+, Jest or compatible test runner, pgsql-test package, PostgreSQL running locally
metadata:
  author: constructive-io
  version: "1.0.0"
---

# PGPM Testing

Run PostgreSQL integration tests with isolated databases using the `pgsql-test` package.

## Testing Framework Standard

**IMPORTANT**: Constructive projects use **Jest** as the standard testing framework. Do NOT use vitest, mocha, or other test runners unless explicitly approved. Jest provides:
- Consistent testing experience across all packages
- Built-in mocking and assertion libraries
- Snapshot testing support
- Parallel test execution

## When to Apply

Use this skill when:
- Writing integration tests that need a database
- Testing PGPM modules or migrations
- Setting up isolated test databases
- Seeding test data from SQL files or PGPM modules
- Running PostGraphile/GraphQL integration tests

## Quick Start

### Installation

```bash
pnpm add -D pgsql-test
```

### Basic Test Setup

```typescript
import { getConnections } from 'pgsql-test';

let db: any;
let teardown: () => Promise<void>;

beforeAll(async () => {
  ({ db, teardown } = await getConnections());
});

afterAll(() => teardown());
beforeEach(() => db.beforeEach());
afterEach(() => db.afterEach());

test('database query works', async () => {
  const result = await db.query('SELECT 1 as num');
  expect(result.rows[0].num).toBe(1);
});
```

## Core API

### getConnections()

Creates an isolated test database and returns clients plus cleanup function.

```typescript
import { getConnections } from 'pgsql-test';

const { db, teardown } = await getConnections(
  connectionOptions?,  // Optional: custom connection settings
  seedAdapters?        // Optional: array of seed adapters
);
```

Returns:
- `db` - PgTestClient with query methods and transaction helpers
- `teardown` - Cleanup function to drop the test database

### PgTestClient Methods

| Method | Description |
|--------|-------------|
| `db.query(sql, params?)` | Execute SQL query |
| `db.beforeEach()` | Start savepoint (call in beforeEach) |
| `db.afterEach()` | Rollback to savepoint (call in afterEach) |
| `db.setContext(key, value)` | Set session context variable |
| `db.getPool()` | Get underlying pg Pool |

## Seeding Data

### SQL File Seeding

```typescript
import { getConnections, seed } from 'pgsql-test';

const { db, teardown } = await getConnections({}, [
  seed.sqlfile(['./fixtures/schema.sql', './fixtures/data.sql'])
]);
```

### Function Seeding

```typescript
import { getConnections, seed } from 'pgsql-test';

const { db, teardown } = await getConnections({}, [
  seed.fn(async (client) => {
    await client.query(`
      CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
      )
    `);
    await client.query(`
      INSERT INTO users (name) VALUES ('Alice'), ('Bob')
    `);
  })
]);
```

### PGPM Module Seeding

Deploy a PGPM module into the test database:

```typescript
import { getConnections, seed } from 'pgsql-test';

const { db, teardown } = await getConnections({}, [
  seed.pgpm(process.cwd())  // Deploy module from current directory
]);
```

### CSV Seeding

```typescript
import { getConnections, seed } from 'pgsql-test';

const { db, teardown } = await getConnections({}, [
  seed.sqlfile(['./fixtures/schema.sql']),
  seed.csv('users', './fixtures/users.csv')
]);
```

## Test Patterns

### Transaction Isolation

Each test runs in a savepoint that gets rolled back:

```typescript
beforeEach(() => db.beforeEach());  // Creates savepoint
afterEach(() => db.afterEach());    // Rolls back to savepoint

test('insert is isolated', async () => {
  await db.query("INSERT INTO users (name) VALUES ('Test')");
  // This insert is rolled back after the test
});

test('previous insert not visible', async () => {
  const result = await db.query("SELECT * FROM users WHERE name = 'Test'");
  expect(result.rows).toHaveLength(0);  // Rolled back!
});
```

### Setting User Context

For RLS (Row Level Security) testing:

```typescript
test('user can only see own data', async () => {
  await db.setContext('user_id', 'user-123');
  
  const result = await db.query('SELECT * FROM user_data');
  // Only returns rows where user_id = 'user-123'
});
```

### Multiple Connections

```typescript
const { db: adminDb, teardown: teardownAdmin } = await getConnections({
  user: 'postgres'
});

const { db: appDb, teardown: teardownApp } = await getConnections({
  user: 'app_user'
});
```

## Running Tests

### Prerequisites

1. Start PostgreSQL:
```bash
pgpm docker start
```

2. Load environment:
```bash
eval "$(pgpm env)"
```

3. Run tests:
```bash
pnpm test
```

### One-liner

```bash
pgpm env pnpm test
```

### Watch Mode

```bash
pgpm env pnpm test --watch
```

## Common Workflows

### Testing PGPM Module

```typescript
import { getConnections, seed } from 'pgsql-test';

describe('my-module', () => {
  let db: any, teardown: () => Promise<void>;

  beforeAll(async () => {
    ({ db, teardown } = await getConnections({}, [
      seed.pgpm(__dirname + '/..')  // Deploy parent module
    ]));
  });

  afterAll(() => teardown());
  beforeEach(() => db.beforeEach());
  afterEach(() => db.afterEach());

  test('function works correctly', async () => {
    const result = await db.query('SELECT my_function($1)', ['input']);
    expect(result.rows[0].my_function).toBe('expected');
  });
});
```

### Testing with Fixtures

```typescript
import { getConnections, seed } from 'pgsql-test';
import path from 'path';

const fixtures = path.join(__dirname, '__fixtures__');

beforeAll(async () => {
  ({ db, teardown } = await getConnections({}, [
    seed.sqlfile([
      path.join(fixtures, 'schema.sql'),
      path.join(fixtures, 'seed-data.sql')
    ])
  ]));
});
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Connection refused" | Run `pgpm docker start` first |
| "Database does not exist" | Check PGDATABASE env var or use `pgpm env` |
| Tests hang | Ensure `teardown()` is called in afterAll |
| Data leaking between tests | Add `beforeEach/afterEach` savepoint calls |
| Permission denied | Check database user has CREATE DATABASE permission |
| Slow tests | Use savepoints instead of recreating database per test |

## File Structure

Recommended test file organization:

```
my-module/
  __tests__/
    __fixtures__/
      schema.sql
      seed-data.sql
    my-feature.test.ts
  deploy/
  revert/
  verify/
  pgpm.plan
```

## References

For related skills:
- Docker container management: See `pgpm-docker` skill
- Environment variables: See `pgpm-env` skill
- GraphQL codegen: See `constructive-graphql-codegen` skill
