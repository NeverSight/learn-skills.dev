---
name: stash-drizzle
description: Integrate CipherStash encryption with Drizzle ORM using @cipherstash/stack/drizzle. Covers the encryptedType column type, encrypted query operators (eq, like, ilike, gt/gte/lt/lte, between, inArray, asc/desc), schema extraction, batched and/or conditions, EQL migration generation, and the complete Drizzle integration workflow. Use when adding encryption to a Drizzle ORM project, defining encrypted Drizzle schemas, or querying encrypted columns with Drizzle.
---

# CipherStash Stack - Drizzle ORM Integration

Guide for integrating CipherStash field-level encryption with Drizzle ORM using `@cipherstash/stack/drizzle`. Provides a custom column type for encrypted fields and query operators that transparently encrypt search values.

## When to Use This Skill

- Adding field-level encryption to a Drizzle ORM project
- Defining encrypted columns in Drizzle table schemas
- Querying encrypted data with type-safe operators
- Sorting and filtering on encrypted columns
- Generating EQL database migrations
- Building Express/Hono/Next.js APIs with encrypted Drizzle queries

## Installation

```bash
npm install @cipherstash/stack drizzle-orm
```

The Drizzle integration is included in `@cipherstash/stack` and imports from `@cipherstash/stack/drizzle`.

## Database Setup

### Install EQL Extension

The EQL (Encrypt Query Language) PostgreSQL extension enables searchable encryption functions. Generate a migration:

```bash
npx generate-eql-migration
# Options:
#   -n, --name <name>   Migration name (default: "install-eql")
#   -o, --out <dir>     Output directory (default: "drizzle")
```

Then apply it:

```bash
npx drizzle-kit migrate
```

### Column Storage

Encrypted columns use the `eql_v2_encrypted` PostgreSQL type (installed by EQL). If not using EQL directly, use JSONB:

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email eql_v2_encrypted,    -- with EQL extension
  name jsonb NOT NULL,       -- or use jsonb
  age INTEGER                -- non-encrypted columns are normal types
);
```

## Schema Definition

Use `encryptedType<T>()` to define encrypted columns in Drizzle table schemas:

```typescript
import { pgTable, integer, timestamp, varchar } from "drizzle-orm/pg-core"
import { encryptedType } from "@cipherstash/stack/drizzle"

const usersTable = pgTable("users", {
  id: integer("id").primaryKey().generatedAlwaysAsIdentity(),

  // Encrypted string with search capabilities
  email: encryptedType<string>("email", {
    equality: true,        // enables: eq, ne, inArray
    freeTextSearch: true,  // enables: like, ilike
    orderAndRange: true,   // enables: gt, gte, lt, lte, between, asc, desc
  }),

  // Encrypted number
  age: encryptedType<number>("age", {
    dataType: "number",
    equality: true,
    orderAndRange: true,
  }),

  // Encrypted JSON object with searchable JSONB queries
  profile: encryptedType<{ name: string; bio: string }>("profile", {
    dataType: "json",
    searchableJson: true,
  }),

  // Non-encrypted columns
  role: varchar("role", { length: 50 }),
  createdAt: timestamp("created_at").defaultNow(),
})
```

### `encryptedType<TData>(name, config?)`

| Config Option | Type | Description |
|---|---|---|
| `dataType` | `"string"` \| `"number"` \| `"json"` \| `"boolean"` \| `"bigint"` \| `"date"` | Plaintext data type (default: `"string"`) |
| `equality` | `boolean` \| `TokenFilter[]` | Enable equality index |
| `freeTextSearch` | `boolean` \| `MatchIndexOpts` | Enable free-text search index |
| `orderAndRange` | `boolean` | Enable ORE index for sorting and range queries |
| `searchableJson` | `boolean` | Enable JSONB path queries (requires `dataType: "json"`) |

The generic type parameter `<TData>` sets the TypeScript type for the decrypted value.

## Initialization

### 1. Extract Schema from Drizzle Table

```typescript
import { extractEncryptionSchema, createEncryptionOperators } from "@cipherstash/stack/drizzle"
import { Encryption } from "@cipherstash/stack"

// Convert Drizzle table definition to CipherStash schema
const usersSchema = extractEncryptionSchema(usersTable)
```

### 2. Initialize Encryption Client

```typescript
const encryptionClient = await Encryption({
  schemas: [usersSchema],
})
```

### 3. Create Query Operators

```typescript
const encryptionOps = createEncryptionOperators(encryptionClient)
```

### 4. Create Drizzle Instance

```typescript
import { drizzle } from "drizzle-orm/postgres-js"
import postgres from "postgres"

const db = drizzle({ client: postgres(process.env.DATABASE_URL!) })
```

## Insert Encrypted Data

Encrypt models before inserting:

```typescript
// Single insert
const encrypted = await encryptionClient.encryptModel(
  { email: "alice@example.com", age: 30, role: "admin" },
  usersSchema,
)
if (!encrypted.failure) {
  await db.insert(usersTable).values(encrypted.data)
}

// Bulk insert
const encrypted = await encryptionClient.bulkEncryptModels(
  [
    { email: "alice@example.com", age: 30, role: "admin" },
    { email: "bob@example.com", age: 25, role: "user" },
  ],
  usersSchema,
)
if (!encrypted.failure) {
  await db.insert(usersTable).values(encrypted.data)
}
```

## Query Encrypted Data

### Equality

```typescript
// Exact match - await the operator
const results = await db
  .select()
  .from(usersTable)
  .where(await encryptionOps.eq(usersTable.email, "alice@example.com"))
```

### Text Search

```typescript
// Case-insensitive search
const results = await db
  .select()
  .from(usersTable)
  .where(await encryptionOps.ilike(usersTable.email, "%alice%"))

// Case-sensitive search
const results = await db
  .select()
  .from(usersTable)
  .where(await encryptionOps.like(usersTable.name, "%Smith%"))
```

### Range Queries

```typescript
const results = await db
  .select()
  .from(usersTable)
  .where(await encryptionOps.gte(usersTable.age, 18))

const results = await db
  .select()
  .from(usersTable)
  .where(await encryptionOps.between(usersTable.age, 18, 65))
```

### Array Operators

```typescript
const results = await db
  .select()
  .from(usersTable)
  .where(await encryptionOps.inArray(usersTable.email, [
    "alice@example.com",
    "bob@example.com",
  ]))
```

### Sorting

```typescript
// Sort by encrypted column (sync - no await needed)
const results = await db
  .select()
  .from(usersTable)
  .orderBy(encryptionOps.asc(usersTable.age))

const results = await db
  .select()
  .from(usersTable)
  .orderBy(encryptionOps.desc(usersTable.age))
```

**Note:** Sorting on encrypted columns requires operator family support in the database. On databases without operator families (e.g. Supabase, or when installed with `--exclude-operator-family`), `ORDER BY` on encrypted columns is not currently supported. Sort application-side after decrypting instead. Operator family support for Supabase is being developed with the Supabase and CipherStash teams.

## JSONB Queries

Query encrypted JSON columns using JSONB operators. These require `searchableJson: true` and `dataType: "json"` in the column's `encryptedType` config.

### Check path existence

```typescript
// Check if a JSONB path exists in an encrypted column
const results = await db
  .select()
  .from(usersTable)
  .where(await encryptionOps.jsonbPathExists(usersTable.profile, "$.bio"))
```

### Extract value at path

```typescript
// Extract the first matching value at a JSONB path
const result = await encryptionOps.jsonbPathQueryFirst(usersTable.profile, "$.name")
```

### Get value with `->` operator

```typescript
// Get a value using the JSONB -> operator
const result = await encryptionOps.jsonbGet(usersTable.profile, "$.name")
```

> **Note:** `jsonbPathExists` returns a boolean and can be used in `WHERE` clauses. `jsonbPathQueryFirst` and `jsonbGet` return encrypted values — use them in `SELECT` expressions.

### Combine JSONB with other operators

```typescript
const results = await db
  .select()
  .from(usersTable)
  .where(
    await encryptionOps.and(
      encryptionOps.jsonbPathExists(usersTable.profile, "$.name"),
      encryptionOps.eq(usersTable.email, "jane@example.com"),
    ),
  )
```

## Batched Conditions (and / or)

Use `encryptionOps.and()` and `encryptionOps.or()` to batch multiple encrypted conditions into a single ZeroKMS call. This is more efficient than awaiting each operator individually.

```typescript
// Batched AND - all encryptions happen in one call
const results = await db
  .select()
  .from(usersTable)
  .where(
    await encryptionOps.and(
      encryptionOps.gte(usersTable.age, 18),     // no await needed
      encryptionOps.lte(usersTable.age, 65),     // lazy operators
      encryptionOps.ilike(usersTable.email, "%example.com"),
      eq(usersTable.role, "admin"),           // mix with regular Drizzle ops
    ),
  )

// Batched OR
const results = await db
  .select()
  .from(usersTable)
  .where(
    await encryptionOps.or(
      encryptionOps.eq(usersTable.email, "alice@example.com"),
      encryptionOps.eq(usersTable.email, "bob@example.com"),
    ),
  )
```

**Key pattern:** Pass lazy operators (no `await`) to `and()`/`or()`, then `await` the outer call. This batches all encryption into a single operation.

## Decrypt Results

```typescript
// Single model
const decrypted = await encryptionClient.decryptModel(results[0])
if (!decrypted.failure) {
  console.log(decrypted.data.email) // "alice@example.com"
}

// Bulk decrypt
const decrypted = await encryptionClient.bulkDecryptModels(results)
if (!decrypted.failure) {
  for (const user of decrypted.data) {
    console.log(user.email)
  }
}
```

## Complete Operator Reference

### Encrypted Operators (async)

| Operator | Usage | Required Index |
|---|---|---|
| `eq(col, value)` | Equality | `equality: true` or `orderAndRange: true` |
| `ne(col, value)` | Not equal | `equality: true` or `orderAndRange: true` |
| `gt(col, value)` | Greater than | `orderAndRange: true` |
| `gte(col, value)` | Greater than or equal | `orderAndRange: true` |
| `lt(col, value)` | Less than | `orderAndRange: true` |
| `lte(col, value)` | Less than or equal | `orderAndRange: true` |
| `between(col, min, max)` | Between (inclusive) | `orderAndRange: true` |
| `notBetween(col, min, max)` | Not between | `orderAndRange: true` |
| `like(col, pattern)` | LIKE pattern match | `freeTextSearch: true` |
| `ilike(col, pattern)` | ILIKE case-insensitive | `freeTextSearch: true` |
| `notIlike(col, pattern)` | NOT ILIKE | `freeTextSearch: true` |
| `inArray(col, values)` | IN array | `equality: true` |
| `notInArray(col, values)` | NOT IN array | `equality: true` |
| `jsonbPathQueryFirst(col, selector)` | Extract first value at JSONB path | `searchableJson: true` |
| `jsonbGet(col, selector)` | Get value using JSONB `->` operator | `searchableJson: true` |
| `jsonbPathExists(col, selector)` | Check if JSONB path exists | `searchableJson: true` |

### Sort Operators (sync)

| Operator | Usage | Required Index |
|---|---|---|
| `asc(col)` | Ascending sort | `orderAndRange: true` |
| `desc(col)` | Descending sort | `orderAndRange: true` |

### Logical Operators (async, batched)

| Operator | Usage | Description |
|---|---|---|
| `and(...conditions)` | Combine with AND | Batches encryption |
| `or(...conditions)` | Combine with OR | Batches encryption |

Both `and()` and `or()` accept `undefined` conditions, which are filtered out. This is useful for conditional query building:

```typescript
const results = await db
  .select()
  .from(usersTable)
  .where(
    await encryptionOps.and(
      maybeCond ? encryptionOps.eq(usersTable.email, value) : undefined,
      encryptionOps.gte(usersTable.age, 18),
    ),
  )
```

### Passthrough Operators (sync, no encryption)

`exists`, `notExists`, `isNull`, `isNotNull`, `not`, `arrayContains`, `arrayContained`, `arrayOverlaps`

These are re-exported from Drizzle and work identically.

## Non-Encrypted Column Fallback

All operators automatically detect whether a column is encrypted. If the column is not encrypted (regular Drizzle column), the operator falls back to the standard Drizzle operator:

```typescript
// This works for both encrypted and non-encrypted columns
await encryptionOps.eq(usersTable.email, "alice@example.com") // encrypted
await encryptionOps.eq(usersTable.role, "admin")              // falls back to drizzle eq()
```

## Complete Example: Express API

```typescript
import "dotenv/config"
import express from "express"
import { eq } from "drizzle-orm"
import { drizzle } from "drizzle-orm/postgres-js"
import postgres from "postgres"
import { pgTable, integer, timestamp, varchar } from "drizzle-orm/pg-core"
import { encryptedType, extractEncryptionSchema, createEncryptionOperators, EncryptionOperatorError, EncryptionConfigError } from "@cipherstash/stack/drizzle"
import { Encryption } from "@cipherstash/stack"

// Schema
const usersTable = pgTable("users", {
  id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
  email: encryptedType<string>("email", { equality: true, freeTextSearch: true }),
  age: encryptedType<number>("age", { dataType: "number", orderAndRange: true }),
  role: varchar("role", { length: 50 }),
  createdAt: timestamp("created_at").defaultNow(),
})

// Init
const usersSchema = extractEncryptionSchema(usersTable)
const encryptionClient = await Encryption({ schemas: [usersSchema] })
const encryptionOps = createEncryptionOperators(encryptionClient)
const db = drizzle({ client: postgres(process.env.DATABASE_URL!) })

const app = express()
app.use(express.json())

// Create user
app.post("/users", async (req, res) => {
  const encrypted = await encryptionClient.encryptModel(req.body, usersSchema)
  if (encrypted.failure) return res.status(500).json({ error: encrypted.failure.message })

  const [user] = await db.insert(usersTable).values(encrypted.data).returning()
  res.json(user)
})

// Search users
app.get("/users", async (req, res) => {
  const conditions = []

  if (req.query.email) {
    conditions.push(encryptionOps.ilike(usersTable.email, `%${req.query.email}%`))
  }
  if (req.query.minAge) {
    conditions.push(encryptionOps.gte(usersTable.age, Number(req.query.minAge)))
  }
  if (req.query.role) {
    conditions.push(eq(usersTable.role, req.query.role as string))
  }

  let query = db.select().from(usersTable)
  if (conditions.length > 0) {
    query = query.where(await encryptionOps.and(...conditions)) as typeof query
  }

  const results = await query
  const decrypted = await encryptionClient.bulkDecryptModels(results)
  if (decrypted.failure) return res.status(500).json({ error: decrypted.failure.message })

  res.json(decrypted.data)
})

app.listen(3000)
```

## Error Handling

Individual operators (e.g., `eq()`, `gte()`, `like()`) throw errors when invoked with invalid configuration or missing indexes:

- **`EncryptionOperatorError`** — thrown for operator-level issues (e.g., invalid arguments, unsupported operations).
- **`EncryptionConfigError`** — thrown for configuration issues (e.g., using `like` on a column without `freeTextSearch: true`).

```typescript
import { createEncryptionOperators, EncryptionOperatorError, EncryptionConfigError } from "@cipherstash/stack/drizzle"

class EncryptionOperatorError extends Error {
  context?: {
    tableName?: string
    columnName?: string
    operator?: string
  }
}

class EncryptionConfigError extends Error {
  context?: {
    tableName?: string
    columnName?: string
    operator?: string
  }
}
```

Encryption client operations return `Result` objects with `data` or `failure`.
