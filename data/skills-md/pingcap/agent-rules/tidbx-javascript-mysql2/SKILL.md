---
name: tidbx-javascript-mysql2
description: Connect to TiDB from JavaScript/Node.js using the mysql2 driver (mysql2/promise). Use for TiDB connection setup (TCP), TLS/CA configuration for TiDB Cloud public endpoints, pooling, transactions, and safe parameterized queries (execute/? placeholders) plus small runnable connection/CRUD templates.
---

# TiDB + JavaScript (mysql2)

Use this skill to connect to TiDB from Node.js with the `mysql2` driver (promise API), configure TLS correctly for TiDB Cloud, and provide small runnable snippets you can copy into a project.

## Important: mysql vs mysql2

These two drivers are easy to mix up:

- This skill is for **mysql2** (`npm i mysql2`) and uses the promise API (`mysql2/promise`).
- If you meant **mysqljs/mysql** (`npm i mysql`) which is callback-based, jump to the `tidbx-javascript-mysqljs` skill instead.

## Recommendation: prefer an ORM for app code

For most application code (models, migrations, types), prefer an ORM/query builder:

- Prisma ORM: use `tidbx-prisma`
- Kysely query builder: use `tidbx-kysely`

## When to use this skill

- Connect to TiDB from JavaScript/TypeScript (Node.js runtime) via `mysql2` / `mysql2/promise`.
- Need TLS guidance (TiDB Cloud public endpoint) or CA certificate setup (TiDB Cloud Dedicated).
- Want a minimal "connect -> SELECT VERSION() -> CRUD" template.

## Code generation rules (Node.js)

- Never hardcode credentials; use `DATABASE_URL` or `TIDB_*` env vars.
- Prefer `mysql2/promise` and parameterized queries (`?` placeholders via `execute()` / `query()`).
- Default to a pool for apps/services (`createPool`), and `await pool.end()` on shutdown.
- When using a pool against TiDB Cloud, set an idle timeout <= 300s (e.g. `idleTimeout: 300_000`) and keep `connectionLimit` small in serverless environments.
- Do not recommend `multipleStatements: true` unless the user explicitly needs it.

## Connection checklist

1. Confirm deployment type: TiDB Cloud (Starter/Essential vs Dedicated) or self-managed.
2. Confirm endpoint type: public vs private/VPC.
3. Decide config style:
   - **Preferred**: `DATABASE_URL` (easy for deployment).
   - **Alternative**: `TIDB_HOST/TIDB_USER/...` options (handy for local/dev).
4. If using a **public endpoint** on TiDB Cloud, enable **TLS**.

## Install

```bash
npm i mysql2
```

If you want `.env` support:

```bash
npm i dotenv
```

## Minimal snippets

### Option A: connect with `DATABASE_URL` (recommended)

```js
import { createConnection } from 'mysql2/promise'

const conn = await createConnection(process.env.DATABASE_URL)
const [[row]] = await conn.query('SELECT VERSION() AS v')
console.log(row.v)
await conn.end()
```

Notes:
- URL-encode special characters in passwords (best: copy the URL from the TiDB Cloud "Connect" dialog).
- If the TiDB Cloud connect dialog provides TLS options in the URL, keep them as-is.

### Option B: connect with connection options (TLS / CA)

Use this when you want explicit TLS config (common for TiDB Cloud Dedicated with a downloaded CA).

```js
import { createPool } from 'mysql2/promise'
import fs from 'node:fs'

const pool = createPool({
  host: process.env.TIDB_HOST,
  port: Number(process.env.TIDB_PORT ?? 4000),
  user: process.env.TIDB_USER,
  password: process.env.TIDB_PASSWORD,
  database: process.env.TIDB_DATABASE ?? 'test',
  ssl: process.env.TIDB_ENABLE_SSL === 'true'
    ? {
        minVersion: 'TLSv1.2',
        ca: process.env.TIDB_CA_PATH ? fs.readFileSync(process.env.TIDB_CA_PATH) : undefined,
      }
    : undefined,
})
```

Suggested env vars:

```bash
TIDB_HOST=...
TIDB_PORT=4000
TIDB_USER=...
TIDB_PASSWORD=...
TIDB_DATABASE=test
TIDB_ENABLE_SSL=true
# Optional (commonly used for TiDB Cloud Dedicated):
TIDB_CA_PATH=/absolute/path/to/ca.pem
```

## CRUD + safety patterns

- Prefer `execute()` for parameterized SQL:

```js
const [result] = await pool.execute(
  'INSERT INTO players (coins, goods) VALUES (?, ?)',
  [100, 100],
)
```

- Use explicit transactions for multi-step updates:

```js
const conn = await pool.getConnection()
try {
  await conn.beginTransaction()
  await conn.execute('UPDATE players SET coins = coins + ? WHERE id = ?', [50, id])
  await conn.commit()
} catch (e) {
  await conn.rollback()
  throw e
} finally {
  conn.release()
}
```

## Templates & scripts in this skill

- `scripts/validate_connection.mjs` -- reads `DATABASE_URL` or `TIDB_*`, connects, prints `SELECT VERSION()`, then exits.
- `templates/quickstart.mjs` -- minimal end-to-end: connect -> create table -> insert -> query -> update -> delete.
