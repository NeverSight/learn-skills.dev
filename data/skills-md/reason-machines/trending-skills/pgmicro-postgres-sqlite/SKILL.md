---
name: pgmicro-postgres-sqlite
description: Use pgmicro — an in-process PostgreSQL reimplementation backed by SQLite-compatible storage, embeddable as a library or CLI
triggers:
  - use pgmicro in my project
  - embed postgres in my app
  - in-process postgresql database
  - pgmicro setup and usage
  - sqlite backed postgres
  - run postgresql without a server
  - pgmicro javascript sdk
  - embeddable postgres database rust

---

# pgmicro

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

pgmicro is an in-process reimplementation of PostgreSQL backed by a SQLite-compatible storage engine. It parses PostgreSQL SQL using the real PostgreSQL parser (`libpg_query`) and compiles it directly to SQLite VDBE bytecode, executed by [Turso](https://github.com/tursodatabase/turso). The result is a fast, embeddable, single-file (or in-memory) database that speaks PostgreSQL — no server process required.

## Key capabilities

- Full PostgreSQL SQL syntax (via the actual PG parser)
- SQLite-compatible `.db` file format (readable by any SQLite tool)
- JavaScript/TypeScript SDK (WASM-based, runs in Node.js and browsers)
- PostgreSQL wire protocol server mode (connect with `psql`, ORMs, etc.)
- Dialect switching: access the same database with PG or SQLite syntax
- PostgreSQL system catalog virtual tables (`pg_class`, `pg_attribute`, `pg_type`, etc.)

## Installation

### CLI (Node.js)

```bash
# Run without installing
npx pg-micro

# Install globally
npm install -g pg-micro
pg-micro myapp.db
```

### JavaScript/TypeScript SDK

```bash
npm install pg-micro
```

### From source (Rust)

```bash
git clone https://github.com/glommer/pgmicro
cd pgmicro
cargo build --release
./target/release/pgmicro
```

## CLI usage

```bash
# In-memory database (ephemeral)
pgmicro

# File-backed database
pgmicro myapp.db

# PostgreSQL wire protocol server
pgmicro myapp.db --server 127.0.0.1:5432

# In-memory server (useful for testing)
pgmicro :memory: --server 127.0.0.1:5432
```

### CLI meta-commands

```
\?          Show help
\q          Quit
\dt         List tables
\d <table>  Describe table schema
```

## JavaScript/TypeScript SDK

### Basic usage

```typescript
import { connect } from "pg-micro";

// In-memory database
const db = await connect(":memory:");

// File-backed database
const db = await connect("./myapp.db");

// DDL
await db.exec(`
  CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

// Insert
await db.exec(`
  INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')
`);

// Prepared statement — fetch all rows
const stmt = await db.prepare("SELECT * FROM users WHERE name = ?");
const rows = await stmt.all("Alice");
console.log(rows);
// [{ id: 1, name: 'Alice', email: 'alice@example.com', created_at: '...' }]

// Fetch single row
const row = await stmt.get("Alice");

// Execute with bound parameters
await db.exec("INSERT INTO users (name, email) VALUES (?, ?)", ["Bob", "bob@example.com"]);

await db.close();
```

### Parameterized queries

```typescript
import { connect } from "pg-micro";

const db = await connect(":memory:");

await db.exec(`
  CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,
    payload TEXT,
    ts TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

// Positional parameters
const insert = await db.prepare(
  "INSERT INTO events (type, payload) VALUES ($1, $2)"
);
await insert.run("user.signup", JSON.stringify({ userId: 42 }));
await insert.run("page.view", JSON.stringify({ path: "/home" }));

// Query with filter
const query = await db.prepare(
  "SELECT * FROM events WHERE type = $1 ORDER BY id DESC"
);
const signups = await query.all("user.signup");
console.log(signups);

await db.close();
```

### Transactions

```typescript
import { connect } from "pg-micro";

const db = await connect(":memory:");

await db.exec("CREATE TABLE accounts (id INT PRIMARY KEY, balance INT)");
await db.exec("INSERT INTO accounts VALUES (1, 1000), (2, 500)");

// Manual transaction
await db.exec("BEGIN");
try {
  await db.exec("UPDATE accounts SET balance = balance - 100 WHERE id = 1");
  await db.exec("UPDATE accounts SET balance = balance + 100 WHERE id = 2");
  await db.exec("COMMIT");
} catch (err) {
  await db.exec("ROLLBACK");
  throw err;
}

const rows = await db.prepare("SELECT * FROM accounts").all();
console.log(rows); // [{ id: 1, balance: 900 }, { id: 2, balance: 600 }]

await db.close();
```

### Using with TypeScript types

```typescript
import { connect } from "pg-micro";

interface User {
  id: number;
  name: string;
  email: string;
  created_at: string;
}

const db = await connect(":memory:");

await db.exec(`
  CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

await db.exec("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')");

const stmt = db.prepare<User>("SELECT * FROM users");
const users: User[] = await stmt.all();
console.log(users[0].name); // 'Alice'

await db.close();
```

## PostgreSQL features supported

```sql
-- SERIAL / auto-increment
CREATE TABLE items (id SERIAL PRIMARY KEY, name TEXT);

-- Dollar-quoted strings
CREATE FUNCTION hello() RETURNS TEXT AS $$
  SELECT 'hello world';
$$ LANGUAGE SQL;

-- Cast syntax
SELECT '42'::int;
SELECT NOW()::text;

-- JSON operators (where implemented)
SELECT data->>'key' FROM records;

-- Standard PG types
CREATE TABLE typed (
  n   INT,
  f   FLOAT8,
  t   TEXT,
  b   BOOLEAN,
  ts  TIMESTAMP,
  j   JSON
);

-- PostgreSQL-style constraints
CREATE TABLE orders (
  id    SERIAL PRIMARY KEY,
  total NUMERIC NOT NULL CHECK (total >= 0),
  state TEXT DEFAULT 'pending'
);
```

## Server mode with psql / ORMs

```bash
# Start server
pgmicro myapp.db --server 127.0.0.1:5432

# Connect with psql
psql -h 127.0.0.1 -p 5432 -U turso -d main

# Connect with libpq connection string (Node.js pg driver)
# DATABASE_URL=postgresql://turso@127.0.0.1:5432/main
```

```typescript
// Using node-postgres (pg) against pgmicro server
import { Client } from "pg";

const client = new Client({
  host: "127.0.0.1",
  port: 5432,
  user: "turso",
  database: "main",
});

await client.connect();
const res = await client.query("SELECT * FROM users");
console.log(res.rows);
await client.end();
```

## Architecture overview

```
PostgreSQL SQL → libpg_query (real PG parser) → PG parse tree
                                                      │
                                              Translator (parser_pg/)
                                                      │ Turso AST
                                              Turso Compiler
                                                      │ VDBE bytecode
                                              Bytecode Engine (vdbe/)
                                                      │
                                              SQLite B-tree storage (.db file)
```

- The `.db` output file is a **standard SQLite database** — open it with DB Browser for SQLite, the `sqlite3` CLI, or any SQLite library.
- PostgreSQL system catalog tables (`pg_class`, `pg_attribute`, `pg_type`, `pg_namespace`) are exposed as virtual tables so `psql` meta-commands like `\dt` and `\d` work correctly.

## Common patterns

### Per-request ephemeral databases (AI agents, sandboxes)

```typescript
import { connect } from "pg-micro";

async function runAgentSession(agentId: string, sql: string) {
  // Each session gets its own isolated in-memory DB — no cleanup needed
  const db = await connect(":memory:");

  await db.exec("CREATE TABLE scratch (key TEXT PRIMARY KEY, value TEXT)");

  // Agent writes intermediate results
  await db.exec(
    "INSERT INTO scratch VALUES ($1, $2)",
    [`agent-${agentId}`, sql]
  );

  const result = await db.prepare("SELECT * FROM scratch").all();
  await db.close();
  return result;
}
```

### Inspecting the SQLite file directly

```bash
# pgmicro writes standard SQLite — use sqlite3 CLI to inspect
sqlite3 myapp.db ".tables"
sqlite3 myapp.db "SELECT * FROM users"
sqlite3 myapp.db ".schema users"
```

### Schema introspection via pg catalog

```sql
-- List all user tables
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- List columns for a table
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'users';
```

## Troubleshooting

**`SERIAL` column not auto-incrementing**
Ensure you are not explicitly inserting `NULL` into the `id` column — insert without the column name and pgmicro will auto-assign.

**`psql` meta-commands (`\dt`, `\d`) show nothing**
Make sure you created tables in the `public` schema (the default). The PostgreSQL catalog virtual tables are populated from actual schema metadata.

**File database not persisting**
Pass a real file path, not `:memory:`. Confirm the process has write permission to the target directory.

**Wire protocol server refused by client**
The server supports a subset of the PostgreSQL wire protocol. Some advanced client features (SSL, SCRAM auth, extended query protocol edge cases) may not be implemented yet. Use simple query mode when possible.

**Unsupported PostgreSQL syntax**
pgmicro is experimental — not all PostgreSQL features are translated. Check the translator layer (`parser_pg/`) for what is currently mapped. Common gaps: stored procedures with complex PL/pgSQL, window functions, CTEs (may be partial), `COPY` command.

**Build errors from source**
Ensure you have a recent stable Rust toolchain (`rustup update stable`) and that `libpg_query` native dependencies (C compiler, `cmake`) are available on your system.

## Resources

- [GitHub: glommer/pgmicro](https://github.com/glommer/pgmicro)
- [Turso (upstream engine)](https://github.com/tursodatabase/turso)
- [libpg_query](https://github.com/pganalyze/libpg_query) — the PostgreSQL parser extraction library
- [pg_query Rust crate](https://crates.io/crates/pg_query)
- [npm: pg-micro](https://www.npmjs.com/package/pg-micro)
