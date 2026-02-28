---
name: pgsql-test-snapshot
description: Snapshot testing utilities for PostgreSQL tests. Use when asked to "snapshot test", "prune IDs from snapshots", "deterministic test output", or when writing tests that need stable, reproducible assertions.
compatibility: pgsql-test, drizzle-orm-test, Jest/Vitest, PostgreSQL
metadata:
  author: constructive-io
  version: "1.0.0"
---

# Snapshot Testing with pgsql-test

Use snapshot utilities from `pgsql-test/utils` to create deterministic, reproducible test assertions. These helpers replace dynamic values (IDs, UUIDs, dates, hashes) with stable placeholders.

## When to Apply

Use this skill when:
- Writing snapshot tests for database queries
- Need deterministic output from queries with UUIDs or timestamps
- Testing API responses that include database-generated values
- Comparing query results across test runs

## Core Utilities

Import from `pgsql-test/utils` or `drizzle-orm-test/utils`:

```typescript
import { 
  snapshot,
  prune,
  pruneIds,
  pruneDates,
  pruneUUIDs,
  pruneHashes,
  pruneTokens,
  composePruners,
  createSnapshot
} from 'pgsql-test/utils';
```

## Basic Usage

### snapshot()

The main utility that applies all default pruners recursively:

```typescript
import { snapshot } from 'pgsql-test/utils';

const result = await db.query('SELECT * FROM users');
expect(snapshot(result.rows)).toMatchSnapshot();
```

Output transforms dynamic values to stable placeholders:

```typescript
// Before snapshot()
{
  id: '550e8400-e29b-41d4-a716-446655440000',
  name: 'Alice',
  created_at: '2024-01-15T10:30:00.000Z',
  password_hash: '$2b$10$...'
}

// After snapshot()
{
  id: '[ID]',
  name: 'Alice',
  created_at: '[DATE]',
  password_hash: '[hash]'
}
```

### With Drizzle ORM

```typescript
import { drizzle } from 'drizzle-orm/node-postgres';
import { snapshot } from 'drizzle-orm-test/utils';
import { users } from './schema';

const drizzleDb = drizzle(db.client);
const result = await drizzleDb.select().from(users);
expect(snapshot(result)).toMatchSnapshot();
```

## Individual Pruners

### pruneIds()

Replaces `id` and `*_id` fields with `[ID]`:

```typescript
import { pruneIds } from 'pgsql-test/utils';

pruneIds({ id: 123, user_id: 'abc-123', name: 'Alice' });
// { id: '[ID]', user_id: '[ID]', name: 'Alice' }
```

### pruneDates()

Replaces Date objects and ISO date strings in `*_at` or `*At` fields:

```typescript
import { pruneDates } from 'pgsql-test/utils';

pruneDates({ 
  created_at: '2024-01-15T10:30:00.000Z',
  updatedAt: new Date(),
  name: 'Alice'
});
// { created_at: '[DATE]', updatedAt: '[DATE]', name: 'Alice' }
```

### pruneUUIDs()

Replaces UUID values in `uuid` and `queue_name` fields:

```typescript
import { pruneUUIDs } from 'pgsql-test/utils';

pruneUUIDs({ uuid: '550e8400-e29b-41d4-a716-446655440000' });
// { uuid: '[UUID]' }
```

### pruneHashes()

Replaces `*_hash` fields starting with `$`:

```typescript
import { pruneHashes } from 'pgsql-test/utils';

pruneHashes({ password_hash: '$2b$10$xyz...' });
// { password_hash: '[hash]' }
```

### pruneTokens()

Replaces `token` and `*_token` fields:

```typescript
import { pruneTokens } from 'pgsql-test/utils';

pruneTokens({ access_token: 'eyJhbGciOiJIUzI1NiIs...' });
// { access_token: '[token]' }
```

### pruneIdArrays()

Replaces `*_ids` array fields with count placeholder:

```typescript
import { pruneIdArrays } from 'pgsql-test/utils';

pruneIdArrays({ member_ids: ['id1', 'id2', 'id3'] });
// { member_ids: '[UUIDs-3]' }
```

### prunePeoplestamps()

Replaces `*_by` fields (audit columns):

```typescript
import { prunePeoplestamps } from 'pgsql-test/utils';

prunePeoplestamps({ created_by: 'user-123', updated_by: 'user-456' });
// { created_by: '[peoplestamp]', updated_by: '[peoplestamp]' }
```

### pruneSchemas()

Replaces schema names starting with `zz-`:

```typescript
import { pruneSchemas } from 'pgsql-test/utils';

pruneSchemas({ schema: 'zz-abc123' });
// { schema: '[schemahash]' }
```

## ID Hash Tracking

Track ID relationships across snapshots using `IdHash`:

```typescript
import { snapshot, pruneIds, IdHash } from 'pgsql-test/utils';

const idHash: IdHash = {
  '550e8400-e29b-41d4-a716-446655440001': 'alice',
  '550e8400-e29b-41d4-a716-446655440002': 'bob'
};

const result = [
  { id: '550e8400-e29b-41d4-a716-446655440001', name: 'Alice' },
  { id: '550e8400-e29b-41d4-a716-446655440002', name: 'Bob' }
];

expect(snapshot(result, idHash)).toMatchSnapshot();
// [
//   { id: '[ID-alice]', name: 'Alice' },
//   { id: '[ID-bob]', name: 'Bob' }
// ]
```

Numeric ID tracking:

```typescript
const idHash: IdHash = {};
let counter = 1;

// Assign IDs as you encounter them
for (const row of result) {
  if (!idHash[row.id]) {
    idHash[row.id] = counter++;
  }
}

expect(snapshot(result, idHash)).toMatchSnapshot();
// [
//   { id: '[ID-1]', name: 'Alice' },
//   { id: '[ID-2]', name: 'Bob' }
// ]
```

## Custom Pruners

### composePruners()

Combine multiple pruners into one:

```typescript
import { composePruners, pruneDates, pruneIds } from 'pgsql-test/utils';

const myPruner = composePruners(pruneDates, pruneIds);
const result = myPruner({ id: 123, created_at: new Date() });
// { id: '[ID]', created_at: '[DATE]' }
```

### createSnapshot()

Create a custom snapshot function with specific pruners:

```typescript
import { createSnapshot, pruneDates, pruneIds, pruneHashes } from 'pgsql-test/utils';

const mySnapshot = createSnapshot([pruneDates, pruneIds, pruneHashes]);

const result = await db.query('SELECT * FROM users');
expect(mySnapshot(result.rows)).toMatchSnapshot();
```

## Default Pruners

The `snapshot()` function applies these pruners by default:

1. `pruneTokens` — `token`, `*_token`
2. `prunePeoplestamps` — `*_by`
3. `pruneDates` — `*_at`, `*At`, Date objects
4. `pruneIdArrays` — `*_ids` arrays
5. `pruneUUIDs` — `uuid`, `queue_name`
6. `pruneHashes` — `*_hash`
7. `pruneIds` — `id`, `*_id`

## Error Code Extraction

Extract error codes from enhanced error messages:

```typescript
import { getErrorCode } from 'pgsql-test/utils';

try {
  await db.query('SELECT * FROM nonexistent');
} catch (err) {
  const code = getErrorCode(err.message);
  // Returns first line only, stripping debug context
  expect(code).toBe('UNDEFINED_TABLE');
}
```

## PostgreSQL Error Formatting

Format PostgreSQL errors for readable output:

```typescript
import { 
  extractPgErrorFields, 
  formatPgError,
  formatPgErrorFields 
} from 'pgsql-test/utils';

try {
  await db.query('invalid sql');
} catch (err) {
  const fields = extractPgErrorFields(err);
  console.log(formatPgError(err));
  // Formatted error with context
}
```

## Complete Test Example

```typescript
import { getConnections, PgTestClient } from 'pgsql-test';
import { snapshot, IdHash } from 'pgsql-test/utils';

let db: PgTestClient;
let teardown: () => Promise<void>;

beforeAll(async () => {
  ({ db, teardown } = await getConnections());
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

describe('User queries', () => {
  it('returns users with stable snapshot', async () => {
    // Seed test data
    await db.query(`
      INSERT INTO users (email, name) VALUES
      ('alice@example.com', 'Alice'),
      ('bob@example.com', 'Bob')
    `);

    const result = await db.query('SELECT * FROM users ORDER BY email');
    
    // Snapshot with ID tracking
    const idHash: IdHash = {};
    result.rows.forEach((row, i) => {
      idHash[row.id] = i + 1;
    });

    expect(snapshot(result.rows, idHash)).toMatchSnapshot();
  });
});
```

## Best Practices

1. **Use snapshot() by default**: Covers most common dynamic fields
2. **Track IDs with IdHash**: When relationships between records matter
3. **Custom pruners for special fields**: Create domain-specific pruners
4. **Order results**: Use ORDER BY for deterministic row order
5. **Prune before comparing**: Apply pruners before any assertions

## References

- Related skill: `pgsql-test-seeding` for seeding test data
- Related skill: `pgsql-test-rls` for RLS testing
- Related skill: `drizzle-orm-test` for Drizzle ORM integration
