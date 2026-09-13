---
name: neo4j-driver-javascript-skill
description: Neo4j JavaScript/TypeScript Driver v6 — driver lifecycle, executeQuery,
  managed transactions (executeRead/executeWrite), session.run, Integer handling, JSON
  serialization, record access, async/await patterns, TypeScript types, error handling,
  and connection setup for Node.js and browser. Use when writing JS/TS code that connects
  to Neo4j — neo4j.driver(), executeQuery, executeRead, executeWrite, session.run,
  neo4j.int, record.get, Integer, BookmarkManager, bolt://, neo4j+s://.
  Does NOT handle Cypher query authoring — use neo4j-cypher-skill.
  Does NOT cover driver version migration — use neo4j-migration-skill.
compatibility: neo4j-driver v6; Node.js >=18; TypeScript supported via bundled types
version: 1.0.5
allowed-tools: Bash WebFetch
---

## When to Use
- Writing JS/TS code that connects to Neo4j (Node.js or browser)
- Setting up driver, sessions, transactions, or query execution
- Debugging Integer handling, result consumption, session leaks, async errors
- TypeScript type annotations for driver objects

## When NOT to Use
- **Writing/optimizing Cypher** → `neo4j-cypher-skill`
- **Upgrading driver version** → `neo4j-migration-skill`
- **RxJS session API** → [references/rxjs-session.md](references/rxjs-session.md)

---

## Install

```bash
npm install neo4j-driver   # or: yarn add neo4j-driver
```

---

## Environment Variables

Load connection config from environment — never hardcode credentials.

```bash
# .env file (add to .gitignore)
NEO4J_URI=neo4j+s://xxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=secret
NEO4J_DATABASE=neo4j
```

```javascript
// npm install dotenv (for Node.js < 20 or when .env auto-load is off)
import 'dotenv/config'   // or: require('dotenv').config()

const URI      = process.env.NEO4J_URI
const USER     = process.env.NEO4J_USERNAME
const PASSWORD = process.env.NEO4J_PASSWORD
const DATABASE = process.env.NEO4J_DATABASE ?? 'neo4j'
```

Node 20+ natively loads `.env` with `--env-file .env`. Next.js / Vite auto-load `.env` — no dotenv import needed.

---

## Driver Lifecycle

Create **one driver instance** at startup. Share everywhere. Never create per-request.

```javascript
// CommonJS
const neo4j = require('neo4j-driver')
// ESM / TypeScript
import neo4j from 'neo4j-driver'

const driver = neo4j.driver(
  process.env.NEO4J_URI,                              // 'neo4j+s://xxx.databases.neo4j.io'
  neo4j.auth.basic(process.env.NEO4J_USER, process.env.NEO4J_PASSWORD)
)
await driver.verifyConnectivity()   // fail fast on startup if unreachable
// On shutdown:
await driver.close()
```

**URI schemes:**
| Scheme | Transport | Use |
|---|---|---|
| `neo4j+s://` | TLS + cluster routing | Aura; production clusters |
| `neo4j://` | plaintext + cluster routing | local dev cluster |
| `bolt+s://` | TLS, single instance | single Neo4j instance with TLS |
| `bolt://` | plaintext, single instance | local single instance |

**Auth options:**
```javascript
neo4j.auth.basic(user, password)   // username/password
neo4j.auth.bearer(token)           // SSO / JWT
neo4j.auth.kerberos(base64Ticket)  // Kerberos
neo4j.auth.none()                  // unauthenticated (dev only)
```

**Singleton for web frameworks** — create once, import everywhere:
```javascript
// db.js
let _driver = null
export function getDriver() {
  if (!_driver) _driver = neo4j.driver(process.env.NEO4J_URI,
    neo4j.auth.basic(process.env.NEO4J_USER, process.env.NEO4J_PASSWORD))
  return _driver
}
export async function closeDriver() {
  if (_driver) { await _driver.close(); _driver = null }
}
```

**Serverless** (Lambda/Vercel/Workers): keep `maxConnectionPoolSize: 5`; no guaranteed `SIGTERM`.

---

## Choose the Right API

| API | Use when | Auto-retry | Result |
|---|---|---|---|
| `driver.executeQuery()` | Default for most queries | ✅ | eager (all records) |
| `session.executeRead/Write()` | Large results, streaming, multi-query tx | ✅ | lazy stream |
| `session.run()` | `LOAD CSV`, `CALL IN TRANSACTIONS`, scripts | ❌ | lazy stream |

---

## `executeQuery` — Default

```javascript
const { records, summary, keys } = await driver.executeQuery(
  'MATCH (p:Person {name: $name})-[:KNOWS]->(f) RETURN f.name AS name',
  { name: 'Alice' },
  { database: 'neo4j', routing: neo4j.routing.READ }
)
for (const record of records) {
  console.log(record.get('name'))   // use .get() — records are NOT plain objects
}

// Write and count results
const { summary: s } = await driver.executeQuery(
  'CREATE (p:Person {name: $name, age: $age})',
  { name: 'Bob', age: neo4j.int(30) },
  { database: 'neo4j' }
)
console.log(s.counters.updates().nodesCreated)   // ✅ must call .updates()
```

Always specify `database` — omitting causes an extra round-trip.

**❌ Never template-literal Cypher:**
```javascript
// ❌ injection risk + disables plan caching
await driver.executeQuery(`MATCH (p:Person {name: '${name}'}) RETURN p`)
// ✅ parameterised
await driver.executeQuery('MATCH (p:Person {name: $name}) RETURN p', { name })
```

---

## Managed Transactions (`executeRead` / `executeWrite`)

Auto-retried on transient failures. **Consume records inside the callback — the stream is gone when the callback returns.**

```javascript
const session = driver.session({ database: 'neo4j' })
try {
  const names = await session.executeRead(async tx => {
    const result = await tx.run(
      'MATCH (p:Person) WHERE p.name STARTS WITH $prefix RETURN p.name AS name',
      { prefix: 'Al' }
    )
    // ✅ collect() while tx is open; return plain data
    return (await result.collect()).map(r => r.get('name'))
  })

  await session.executeWrite(async tx => {
    await tx.run('MERGE (p:Person {name: $name})', { name: 'Carol' })
  })
} finally {
  await session.close()   // always in finally
}
```

**Critical: `await tx.run()` returns a stream handle, not records.**
```javascript
// ❌ returns stream; tx closes; records = []
return await tx.run('MATCH (p:Person) RETURN p.name AS name')

// ✅ collect fully inside callback
const result = await tx.run('MATCH (p:Person) RETURN p.name AS name')
return (await result.collect()).map(r => r.get('name'))

// ✅ or stream with for-await
for await (const record of result) { names.push(record.get('name')) }
```

**Callback may execute more than once** (retry on transient failure) — no side effects inside:
```javascript
// ❌ fetch() called on every retry
await session.executeWrite(async tx => {
  await fetch('https://api.example.com/notify')
  await tx.run('CREATE ...')
})
// ✅ side effects after confirmed commit
await session.executeWrite(async tx => { await tx.run('MERGE ...') })
await fetch('https://api.example.com/notify')
```

---

## `session.run` — Implicit Transactions

Not auto-retried. Use for `LOAD CSV` / `CALL IN TRANSACTIONS` / scripting only.

```javascript
const session = driver.session({ database: 'neo4j' })
try {
  const result = await session.run('CREATE (p:Person {name: $name}) RETURN p', { name: 'Alice' })
  console.log(result.summary.counters.updates().nodesCreated)
} finally {
  await session.close()
}
```

---

## Session Close — Always in `finally`

```javascript
// ❌ session leaks if executeRead rejects
session.executeRead(async tx => { ... })
  .then(result => doSomething(result))
  .then(() => session.close())

// ✅ guaranteed close
try {
  const result = await session.executeRead(async tx => { ... })
  doSomething(result)
} finally {
  await session.close()
}

// ✅ promise-chain equivalent
session.executeRead(async tx => { ... })
  .then(doSomething)
  .catch(handleError)
  .finally(() => session.close())
```

---

## Integer Handling

Neo4j integers are 64-bit; JS `Number` is IEEE 754 (safe up to 2^53−1). Driver returns custom `Integer` by default.

**Three modes:**
```javascript
// Mode 1 (default): Integer class — safe for all values, requires conversion
const driver1 = neo4j.driver(URI, auth)
// record.get('count') → Integer { low: 42, high: 0 }

// Mode 2: native JS number — only safe within Number.MAX_SAFE_INTEGER
const driver2 = neo4j.driver(URI, auth, { disableLosslessIntegers: true })
// record.get('count') → 42

// Mode 3: BigInt — precise but breaks JSON.stringify
const driver3 = neo4j.driver(URI, auth, { useBigInt: true })
// record.get('count') → 42n
```

**Working with Integer class:**
```javascript
const count = record.get('count')        // Integer { low: 42, high: 0 }
neo4j.isInt(count)                       // true
neo4j.integer.inSafeRange(count)         // check before toNumber()
count.toNumber()                         // 42  (only safe within MAX_SAFE_INTEGER)
count.toString()                         // '42' (always safe)
count.toBigInt()                         // 42n

// Send integer parameter — plain JS number sends as FLOAT
await driver.executeQuery('CREATE (p:Person {age: $age})', { age: neo4j.int(30) })
```

**JSON serialization pitfalls:**
```javascript
// ❌ Integer → {"low":42,"high":0}
JSON.stringify({ age: record.get('age') })
// ❌ BigInt → TypeError: Do not know how to serialize a BigInt
// ✅ convert first
JSON.stringify({ age: record.get('age').toNumber() })
// ✅ or use disableLosslessIntegers: true
// ❌ temporal types → {} silently
JSON.stringify({ dt: record.get('created') })
// ✅
JSON.stringify({ dt: record.get('created').toString() })
```

---

## Record Access

Records are **not plain objects** — use `.get()`:

```javascript
const record = records[0]
record.get('name')    // ✅ by key
record.get(0)         // ✅ by index
record.keys           // ['name', 'age']
record.has('name')    // true
record.name           // ❌ undefined
record['name']        // ❌ undefined
```

`record.toObject()` returns plain JS keys **but values are still driver types** (Integers, temporals). Not JSON-safe without conversion.

---

## Error Handling

```javascript
import { Neo4jError, SERVICE_UNAVAILABLE, SESSION_EXPIRED } from 'neo4j-driver'

try {
  await driver.executeQuery('...', {}, { database: 'neo4j' })
} catch (err) {
  if (err instanceof Neo4jError) {
    if (err.code === 'Neo.ClientError.Schema.ConstraintValidationFailed') { /* unique constraint */ }
    if (err.code === SERVICE_UNAVAILABLE) { /* unreachable */ }
    if (err.code === SESSION_EXPIRED)     { /* open a new session */ }
    if (err.retriable) { /* transient — executeQuery already retried to exhaustion */ }
  }
}
```

`executeQuery` and `executeRead/Write` auto-retry retriable errors. `session.run` does not.

---

## TypeScript

```typescript
import neo4j, { Driver, Session, ManagedTransaction, Record, Node, Integer } from 'neo4j-driver'

const driver: Driver = neo4j.driver(URI, neo4j.auth.basic(USER, PASSWORD))
const session: Session = driver.session({ database: 'neo4j' })

const names: string[] = await session.executeRead(
  async (tx: ManagedTransaction): Promise<string[]> => {
    const result = await tx.run('MATCH (p:Person) RETURN p.name AS name')
    return (await result.collect()).map((r: Record) => r.get('name') as string)
  }
)

// Typed node — Integer generic changes with disableLosslessIntegers
const node = record.get('p') as Node<Integer>
const age: number = node.properties.age.toNumber()
// With disableLosslessIntegers: true → Node<number>; age is already number
```

---

## Batch Writes with UNWIND

```javascript
// ❌ one transaction per item
for (const p of people) { await driver.executeQuery('CREATE ...', p) }

// ✅ single transaction
await driver.executeQuery(
  `UNWIND $people AS person
   MERGE (p:Person {name: person.name})
   SET p.age = person.age`,
  { people },   // array of plain objects; numeric fields must be JS numbers, not neo4j.int()
  { database: 'neo4j' }
)
```

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Template literal Cypher | Use `$param` placeholders |
| `record.name` / `record['name']` | `record.get('name')` |
| `JSON.stringify` on Integer | `.toNumber()` or `disableLosslessIntegers` |
| `JSON.stringify` on temporal | `.toString()` first |
| `summary.counters.nodesCreated` | `summary.counters.updates().nodesCreated` |
| Omit `database` | Always `{ database: 'neo4j' }` |
| Return `result` from tx callback | Return `await result.collect()` or mapped data |
| `.then(() => session.close())` | `try/finally { await session.close() }` |
| Side effects inside tx callback | Move outside — callback may retry |
| New driver per request | Create once at startup |
| `bolt://` or `neo4j://` in browser | Use `neo4j+s://` (WSS) |
| Integer in UNWIND array | Convert to plain JS `Number` first |
| `maxConnectionPoolSize: 100` in serverless | Use 5–10 per function instance |

---

## References

Load on demand:
- [references/data-types.md](references/data-types.md) — full type mapping table, temporal types, graph types (Node/Relationship/Path), spatial types (Point/WGS-84/Cartesian), `toNative()` conversion helper
- [references/advanced-patterns.md](references/advanced-patterns.md) — explicit transactions, causal consistency/bookmarks, connection pool tuning, result transformers, lazy streaming, repository pattern
- [references/browser-usage.md](references/browser-usage.md) — WebSocket URIs, CORS, bundler config, security guidance
- [references/rxjs-session.md](references/rxjs-session.md) — RxJS session API (`rxSession.run()`, observable patterns)

---

## Checklist
- [ ] One driver instance created at startup; shared everywhere
- [ ] `database` specified on every query/session
- [ ] `await driver.verifyConnectivity()` called at startup
- [ ] `session.close()` in `finally` block
- [ ] Records accessed with `.get()` — not dot/bracket notation
- [ ] Integer `.toNumber()` / `.toString()` called before JSON serialization
- [ ] Temporal `.toString()` called before JSON serialization
- [ ] `summary.counters.updates()` called before accessing counter fields
- [ ] `$param` placeholders used — no string concatenation in Cypher
- [ ] Tx callback returns plain data (not stream); side effects outside callback
- [ ] Write uses `neo4j.int()` for integer parameters
- [ ] `executeRead` for reads; `executeWrite` for writes
- [ ] Browser: `neo4j+s://` URI (WebSocket)
