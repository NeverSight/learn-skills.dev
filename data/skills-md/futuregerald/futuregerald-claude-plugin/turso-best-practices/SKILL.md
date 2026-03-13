---
name: turso-best-practices
description: Turso and libSQL best practices for SQLite-compatible cloud database development with edge distribution, embedded replicas, and vector search.
tags: [framework, database]
---

# Turso & libSQL Best Practices

## Overview

Turso is a fully managed SQLite-compatible database platform built on libSQL, a fork of SQLite. It provides edge distribution, embedded replicas, native vector search, branching, and point-in-time recovery. Core principle: **SQLite simplicity with cloud-scale distribution**.

## When to Use

- Building applications needing SQLite with cloud features
- Implementing embedded replicas for offline-first apps
- Adding vector search/AI embeddings to applications
- Setting up local development with Turso
- Managing database migrations and branching
- Configuring encryption at rest
- Working with the Turso CLI or Platform API

## Quick Reference

| Task                  | Command/Pattern                                                             |
| --------------------- | --------------------------------------------------------------------------- |
| Install CLI (macOS)   | `brew install tursodatabase/tap/turso`                                      |
| Install CLI (Linux)   | `curl -sSfL https://get.tur.so/install.sh \| bash`                          |
| Login                 | `turso auth login`                                                          |
| Create database       | `turso db create my-db`                                                     |
| Connect to shell      | `turso db shell my-db`                                                      |
| Get credentials       | `turso db show my-db --url` and `turso db tokens create my-db`              |
| Local dev server      | `turso dev`                                                                 |
| Local with file       | `turso dev --db-file local.db`                                              |
| Create branch         | `turso db create branch-db --from-db my-db`                                 |
| Point-in-time restore | `turso db create restored --from-db my-db --timestamp 2024-01-01T00:00:00Z` |
| Database dump         | `turso db shell my-db .dump > dump.sql`                                     |

## Installation & Setup

### CLI Installation

```bash
# macOS
brew install tursodatabase/tap/turso

# Linux / Windows (WSL)
curl -sSfL https://get.tur.so/install.sh | bash
```

### Authentication

```bash
# Sign up (opens browser)
turso auth signup

# Login (opens browser)
turso auth login

# Headless mode (WSL/CI)
turso auth login --headless
```

### Create Your First Database

```bash
# Create database (auto-detects closest region)
turso db create my-db

# Show database info
turso db show my-db

# Get connection URL
turso db show my-db --url

# Create auth token
turso db tokens create my-db

# Connect to shell
turso db shell my-db
```

## SDK Usage (TypeScript/JavaScript)

### Installation

```bash
npm install @libsql/client
# or
pnpm add @libsql/client
```

### Basic Connection

```typescript
import { createClient } from '@libsql/client'

const client = createClient({
  url: process.env.TURSO_DATABASE_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN,
})
```

### Execute Queries

```typescript
// Simple query
const result = await client.execute('SELECT * FROM users')

// Positional placeholders
const result = await client.execute({
  sql: 'SELECT * FROM users WHERE id = ?',
  args: [1],
})

// Named placeholders (:, @, or $)
const result = await client.execute({
  sql: 'INSERT INTO users (name, email) VALUES (:name, :email)',
  args: { name: 'Alice', email: 'alice@example.com' },
})
```

### Response Structure

```typescript
interface ResultSet {
  rows: Array<Row> // Row data (empty for writes)
  columns: Array<string> // Column names
  rowsAffected: number // Affected rows (writes)
  lastInsertRowid?: bigint // Last inserted row ID
}
```

### Batch Transactions

Batch executes multiple statements in an implicit transaction:

```typescript
const results = await client.batch(
  [
    { sql: 'INSERT INTO users (name) VALUES (?)', args: ['Alice'] },
    { sql: 'INSERT INTO users (name) VALUES (?)', args: ['Bob'] },
  ],
  'write' // Transaction mode: "write" | "read" | "deferred"
)
```

### Interactive Transactions

For complex logic with conditional commits/rollbacks:

```typescript
const transaction = await client.transaction('write')

try {
  const balance = await transaction.execute({
    sql: 'SELECT balance FROM accounts WHERE id = ?',
    args: [userId],
  })

  if (balance.rows[0].balance >= amount) {
    await transaction.execute({
      sql: 'UPDATE accounts SET balance = balance - ? WHERE id = ?',
      args: [amount, userId],
    })
    await transaction.commit()
  } else {
    await transaction.rollback()
  }
} catch (e) {
  await transaction.rollback()
  throw e
}
```

### Transaction Modes

| Mode       | SQLite Command               | Description                                      |
| ---------- | ---------------------------- | ------------------------------------------------ |
| `write`    | `BEGIN IMMEDIATE`            | Read/write, serialized on primary                |
| `read`     | `BEGIN TRANSACTION READONLY` | Read-only, can run on replicas in parallel       |
| `deferred` | `BEGIN DEFERRED`             | Starts as read, upgrades to write on first write |

## Local Development

### Option 1: SQLite File (Simplest)

```typescript
const client = createClient({
  url: 'file:local.db',
})
```

No auth token needed. Works with standard SQLite features.

### Option 2: Turso Dev Server (Full Features)

```bash
# Start local libSQL server
turso dev

# With persistent file
turso dev --db-file local.db
```

```typescript
const client = createClient({
  url: 'http://127.0.0.1:8080',
})
```

Supports all libSQL features including extensions.

### Option 3: Production Database Dump

```bash
# Export production data
turso db shell prod-db .dump > dump.sql

# Create local file from dump
cat dump.sql | sqlite3 local.db
```

### Environment Variables Pattern

```typescript
const client = createClient({
  url: process.env.TURSO_DATABASE_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN, // undefined locally
})
```

```env
# Production
TURSO_DATABASE_URL=libsql://my-db-org.turso.io
TURSO_AUTH_TOKEN=eyJ...

# Development
TURSO_DATABASE_URL=file:local.db
# No auth token needed
```

## Embedded Replicas

Local database that syncs with remote Turso database. Reads are instant (local), writes go to remote.

### Configuration

```typescript
const client = createClient({
  url: 'file:replica.db', // Local file
  syncUrl: 'libsql://my-db.turso.io', // Remote primary
  authToken: '...',
  syncInterval: 60, // Auto-sync every 60 seconds
})
```

### Manual Sync

```typescript
await client.sync()
```

### Offline Mode

```typescript
const client = createClient({
  url: 'file:replica.db',
  syncUrl: 'libsql://my-db.turso.io',
  authToken: '...',
  offline: true, // Writes go to local, sync later
})
```

### Important Notes

- Reads always from local replica
- Writes go to remote primary (unless offline mode)
- Read-your-writes guaranteed after successful write
- Don't open local file while syncing (corruption risk)
- One frame = 4KB (minimum write unit)

## Vector Search (AI & Embeddings)

Native vector search without extensions.

### Create Table with Vector Column

```sql
CREATE TABLE movies (
  id INTEGER PRIMARY KEY,
  title TEXT,
  embedding F32_BLOB(384)  -- 384-dimensional float32 vector
);
```

### Vector Types

| Type                       | Storage       | Description                           |
| -------------------------- | ------------- | ------------------------------------- |
| `FLOAT64` / `F64_BLOB`     | 8D + 1 bytes  | 64-bit double precision               |
| `FLOAT32` / `F32_BLOB`     | 4D bytes      | 32-bit single precision (recommended) |
| `FLOAT16` / `F16_BLOB`     | 2D + 1 bytes  | 16-bit half precision                 |
| `FLOAT8` / `F8_BLOB`       | D + 14 bytes  | 8-bit compressed                      |
| `FLOAT1BIT` / `F1BIT_BLOB` | D/8 + 3 bytes | 1-bit binary                          |

### Insert Vectors

```sql
INSERT INTO movies (title, embedding)
VALUES ('Inception', vector32('[0.1, 0.2, 0.3, ...]'));
```

### Similarity Search

```sql
SELECT title,
       vector_distance_cos(embedding, vector32('[0.1, 0.2, ...]')) AS distance
FROM movies
ORDER BY distance ASC
LIMIT 10;
```

### Vector Index (DiskANN)

```sql
-- Create index
CREATE INDEX movies_idx ON movies(libsql_vector_idx(embedding));

-- Query with index (much faster for large tables)
SELECT title
FROM vector_top_k('movies_idx', vector32('[0.1, 0.2, ...]'), 10)
JOIN movies ON movies.rowid = id;
```

### Index Settings

```sql
CREATE INDEX movies_idx ON movies(
  libsql_vector_idx(embedding, 'metric=cosine', 'compress_neighbors=float8')
);
```

| Setting              | Values         | Description               |
| -------------------- | -------------- | ------------------------- |
| `metric`             | `cosine`, `l2` | Distance function         |
| `max_neighbors`      | integer        | Graph connectivity        |
| `compress_neighbors` | vector type    | Compression for storage   |
| `search_l`           | integer        | Search precision vs speed |

## Drizzle ORM Integration

### Setup

```bash
npm install drizzle-orm @libsql/client
npm install -D drizzle-kit
```

### Configuration

```typescript
// drizzle.config.ts
import type { Config } from 'drizzle-kit'

export default {
  schema: './db/schema.ts',
  out: './migrations',
  dialect: 'turso',
  dbCredentials: {
    url: process.env.TURSO_DATABASE_URL!,
    authToken: process.env.TURSO_AUTH_TOKEN,
  },
} satisfies Config
```

### Schema Definition

```typescript
// db/schema.ts
import { text, integer, sqliteTable } from 'drizzle-orm/sqlite-core'

export const users = sqliteTable('users', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
})
```

### Client Setup

```typescript
import { drizzle } from 'drizzle-orm/libsql'
import { createClient } from '@libsql/client'

const turso = createClient({
  url: process.env.TURSO_DATABASE_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN,
})

export const db = drizzle(turso)
```

### Migrations

```bash
# Generate migrations
npm run drizzle-kit generate

# Apply migrations
npm run drizzle-kit migrate
```

## Branching & Point-in-Time Recovery

### Create Branch

```bash
turso db create feature-branch --from-db production-db
```

### Point-in-Time Restore

```bash
turso db create restored-db --from-db production-db --timestamp 2024-01-15T10:00:00Z
```

### CI/CD Branching (GitHub Actions)

```yaml
name: Create Database Branch
on: create

jobs:
  create-branch:
    runs-on: ubuntu-latest
    steps:
      - name: Create Database
        run: |
          curl -X POST \
            -H "Authorization: Bearer ${{ secrets.TURSO_API_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d '{"name": "${{ github.ref_name }}", "group": "default", "seed": {"type": "database", "name": "production"}}' \
            "https://api.turso.tech/v1/organizations/${{ secrets.ORG }}/databases"
```

### Important Notes

- Branches are separate databases (no auto-merge)
- Need new token or group token for branch
- Count toward database quota
- Delete manually when done

## Encryption at Rest

### Generate Key

```bash
# 256-bit key for AEGIS-256/AES-256
openssl rand -base64 32

# 128-bit key for AEGIS-128/AES-128
openssl rand -base64 16
```

### Create Encrypted Database

```bash
turso db create secure-db \
  --remote-encryption-key "YOUR_KEY" \
  --remote-encryption-cipher aegis256
```

### Connect to Encrypted Database

```bash
turso db shell secure-db --remote-encryption-key "YOUR_KEY"
```

### Supported Ciphers

| Cipher             | Key Size | Recommendation           |
| ------------------ | -------- | ------------------------ |
| `aegis128l`        | 128-bit  | Recommended for speed    |
| `aegis256`         | 256-bit  | Recommended for security |
| `aes128gcm`        | 128-bit  | NIST compliance          |
| `aes256gcm`        | 256-bit  | NIST compliance          |
| `chacha20poly1305` | 256-bit  | AES alternative          |

## SQLite Extensions

### Preloaded (Always Available)

| Extension     | Description           |
| ------------- | --------------------- |
| JSON          | JSON functions        |
| FTS5          | Full-text search      |
| R\*Tree       | Spatial indexing      |
| SQLean Crypto | Hashing, encoding     |
| SQLean Fuzzy  | Fuzzy string matching |
| SQLean Math   | Advanced math         |
| SQLean Stats  | Statistical functions |
| SQLean Text   | String manipulation   |
| SQLean UUID   | UUID generation       |

### Enable Additional Extensions

```bash
turso db create my-db --enable-extensions
```

## Common Mistakes

| Mistake                                    | Fix                                         |
| ------------------------------------------ | ------------------------------------------- |
| Using `@libsql/client/web` with file URLs  | Use `@libsql/client` for local files        |
| Long-running write transactions            | Keep writes short, they block other writes  |
| Opening local file during sync             | Wait for sync to complete                   |
| Forgetting to sync embedded replicas       | Call `sync()` or use `syncInterval`         |
| Hardcoding credentials                     | Use environment variables                   |
| Not using transactions for related writes  | Use `batch()` or `transaction()`            |
| Creating vector index on wrong column type | Column must be vector type (F32_BLOB, etc.) |

## Performance Tips

- Use `batch()` for multiple related operations
- Use `read` transactions for read-only queries (parallel on replicas)
- Set appropriate `syncInterval` for embedded replicas
- Use vector indexes for tables with >1000 rows
- Consider `compress_neighbors` for large vector indexes
- Use positional placeholders for frequently executed queries
