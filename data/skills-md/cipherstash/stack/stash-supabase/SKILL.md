---
name: stash-supabase
description: Integrate CipherStash encryption with Supabase using @cipherstash/stack/supabase. Covers the encryptedSupabase wrapper, transparent encryption/decryption on insert/update/select, encrypted query filters (eq, like, ilike, gt/gte/lt/lte, in, or, match), identity-aware encryption, and the complete query builder API. Use when adding encryption to a Supabase project, querying encrypted columns, or building secure Supabase applications.
---

# CipherStash Stack - Supabase Integration

Guide for integrating CipherStash field-level encryption with Supabase using the `encryptedSupabase` wrapper. The wrapper provides transparent encryption on mutations and decryption on selects, with full support for querying encrypted columns.

## When to Use This Skill

- Adding field-level encryption to a Supabase project
- Querying encrypted data with Supabase's query builder (eq, like, gt, in, or, etc.)
- Inserting, updating, or upserting encrypted data
- Using identity-aware encryption (lock contexts) with Supabase
- Building applications where sensitive columns need encryption at rest and in transit

## Installation

```bash
npm install @cipherstash/stack @supabase/supabase-js
```

## Database Schema

Encrypted columns must be stored as JSONB in your Supabase database:

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email jsonb NOT NULL,        -- encrypted column
  name jsonb NOT NULL,         -- encrypted column
  age jsonb,                   -- encrypted column (numeric)
  role VARCHAR(50),            -- regular column (not encrypted)
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

For searchable encryption (equality, range, text search), install the EQL extension:

```sql
CREATE EXTENSION IF NOT EXISTS eql_v2;
```

## Setup

### 1. Define Encrypted Schema

```typescript
import { encryptedTable, encryptedColumn } from "@cipherstash/stack/schema"

const users = encryptedTable("users", {
  email: encryptedColumn("email")
    .equality()         // eq, neq, in
    .freeTextSearch(),  // like, ilike

  name: encryptedColumn("name")
    .equality()
    .freeTextSearch(),

  age: encryptedColumn("age")
    .dataType("number")
    .equality()
    .orderAndRange(),   // gt, gte, lt, lte
})
```

### 2. Initialize Clients

```typescript
import { createClient } from "@supabase/supabase-js"
import { Encryption } from "@cipherstash/stack"
import { encryptedSupabase } from "@cipherstash/stack/supabase"

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_ANON_KEY!,
)

const encryptionClient = await Encryption({ schemas: [users] })

const eSupabase = encryptedSupabase({
  encryptionClient,
  supabaseClient: supabase,
})
```

### 3. Use the Wrapper

All queries go through `eSupabase.from(tableName, schema)`:

```typescript
const { data, error } = await eSupabase
  .from("users", users)
  .select("id, email, name")
  .eq("email", "alice@example.com")
```

## Insert (Encrypted Automatically)

```typescript
// Single insert
const { data, error } = await eSupabase
  .from("users", users)
  .insert({
    email: "alice@example.com",  // encrypted automatically
    name: "Alice Smith",         // encrypted automatically
    age: 30,                     // encrypted automatically
    role: "admin",               // not in schema, passed through
  })
  .select("id")

// Bulk insert
const { data, error } = await eSupabase
  .from("users", users)
  .insert([
    { email: "alice@example.com", name: "Alice", age: 30, role: "admin" },
    { email: "bob@example.com", name: "Bob", age: 25, role: "user" },
  ])
  .select("id")
```

## Update (Encrypted Automatically)

```typescript
const { data, error } = await eSupabase
  .from("users", users)
  .update({ name: "Alice Johnson" })  // encrypted automatically
  .eq("id", 1)
  .select("id, name")
```

## Upsert

```typescript
const { data, error } = await eSupabase
  .from("users", users)
  .upsert(
    { id: 1, email: "alice@example.com", name: "Alice", role: "admin" },
    { onConflict: "id" },
  )
  .select("id, email, name")
```

## Select (Decrypted Automatically)

```typescript
// List query - returns decrypted array
const { data, error } = await eSupabase
  .from("users", users)
  .select("id, email, name, role")
// data: [{ id: 1, email: "alice@example.com", name: "Alice Smith", role: "admin" }]

// Single result
const { data, error } = await eSupabase
  .from("users", users)
  .select("id, email, name")
  .eq("id", 1)
  .single()
// data: { id: 1, email: "alice@example.com", name: "Alice Smith" }

// Maybe single (returns null if no match)
const { data, error } = await eSupabase
  .from("users", users)
  .select("id, email")
  .eq("email", "nobody@example.com")
  .maybeSingle()
// data: null
```

**Important:** You must list columns explicitly in `select()` — using `select('*')` will throw an error. The wrapper automatically adds `::jsonb` casts to encrypted columns so PostgreSQL parses them correctly.

`select()` also accepts an optional second parameter: `select(columns, { head?: boolean, count?: 'exact' | 'planned' | 'estimated' })`.

## Query Filters

All filter values for encrypted columns are automatically encrypted before the query executes. Multiple filters are batch-encrypted in a single ZeroKMS call for efficiency.

### Equality Filters

```typescript
// Exact match (requires .equality() on column)
.eq("email", "alice@example.com")

// Not equal
.neq("email", "alice@example.com")

// IN array (requires .equality())
.in("email", ["alice@example.com", "bob@example.com"])

// NULL check (no encryption needed)
.is("email", null)
```

### Text Search Filters

```typescript
// LIKE - case sensitive (requires .freeTextSearch())
.like("name", "%alice%")

// ILIKE - case insensitive (requires .freeTextSearch())
.ilike("name", "%alice%")
```

### Range/Comparison Filters

```typescript
// Greater than (requires .orderAndRange())
.gt("age", 21)

// Greater than or equal
.gte("age", 18)

// Less than
.lt("age", 65)

// Less than or equal
.lte("age", 100)
```

### Match (Multi-Column Equality)

```typescript
.match({ email: "alice@example.com", name: "Alice" })
```

### OR Conditions

```typescript
// String format
.or("email.eq.alice@example.com,email.eq.bob@example.com")

// Structured format (more type-safe)
.or([
  { column: "email", op: "eq", value: "alice@example.com" },
  { column: "email", op: "eq", value: "bob@example.com" },
])
```

Both forms encrypt values for encrypted columns automatically.

### NOT Filter

```typescript
.not("email", "eq", "alice@example.com")
```

### Raw Filter

```typescript
.filter("email", "eq", "alice@example.com")
```

## Delete

```typescript
const { data, error } = await eSupabase
  .from("users", users)
  .delete()
  .eq("id", 1)
```

## Transforms

These are passed through to Supabase directly:

```typescript
.order("name", { ascending: true })
.limit(10)
.range(0, 9)
.csv()
.abortSignal(signal)
.throwOnError()
.returns<U>()
```

### Ordering by Encrypted Columns

**`ORDER BY` on encrypted columns is not currently supported** on databases without operator family support (including Supabase).

Without operator families installed in PostgreSQL, the database cannot sort on `eql_v2_encrypted` columns. This affects all clients — the Supabase JS SDK, Drizzle, raw SQL, and any other ORM.

**Workaround:** Sort application-side after decrypting the results.

Operator family support is currently being developed in collaboration with the Supabase and CipherStash teams and will be available in a future release.

`.order()` on non-encrypted columns works normally.

## Identity-Aware Encryption

Chain `.withLockContext()` to tie encryption to a specific user's JWT:

```typescript
import { LockContext } from "@cipherstash/stack/identity"

const lc = new LockContext()
const identified = await lc.identify(userJwt)
if (identified.failure) throw new Error(identified.failure.message)
const lockContext = identified.data

const { data, error } = await eSupabase
  .from("users", users)
  .insert({ email: "alice@example.com", name: "Alice" })
  .withLockContext(lockContext)
  .select("id")
```

## Audit Logging

Chain `.audit()` to attach metadata for ZeroKMS audit logging:

```typescript
const { data, error } = await eSupabase
  .from("users", users)
  .select("id, email, name")
  .eq("email", "alice@example.com")
  .audit({ metadata: { action: "user-lookup", requestId: "abc-123" } })
```

## Complete Example

```typescript
import { createClient } from "@supabase/supabase-js"
import { Encryption } from "@cipherstash/stack"
import { encryptedSupabase } from "@cipherstash/stack/supabase"
import { encryptedTable, encryptedColumn } from "@cipherstash/stack/schema"

// Schema
const users = encryptedTable("users", {
  email: encryptedColumn("email").equality().freeTextSearch(),
  name: encryptedColumn("name").equality().freeTextSearch(),
  age: encryptedColumn("age").dataType("number").equality().orderAndRange(),
})

// Clients
const supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_ANON_KEY!)
const encryptionClient = await Encryption({ schemas: [users] })
const eSupabase = encryptedSupabase({ encryptionClient, supabaseClient: supabase })

// Insert
await eSupabase
  .from("users", users)
  .insert([
    { email: "alice@example.com", name: "Alice", age: 30 },
    { email: "bob@example.com", name: "Bob", age: 25 },
  ])

// Query with multiple filters
const { data } = await eSupabase
  .from("users", users)
  .select("id, email, name, age")
  .gte("age", 18)
  .lte("age", 35)
  .ilike("name", "%ali%")

// data is fully decrypted:
// [{ id: 1, email: "alice@example.com", name: "Alice", age: 30 }]
```

## Response Type

```typescript
type EncryptedSupabaseResponse<T> = {
  data: T | null                     // Decrypted rows
  error: EncryptedSupabaseError | null
  count: number | null
  status: number
  statusText: string
}
```

Errors can come from Supabase (API errors) or from encryption operations. Check `error.encryptionError` for encryption-specific failures.

The full `EncryptedSupabaseError` type:

```typescript
type EncryptedSupabaseError = {
  message: string
  details?: string       // Supabase error details
  hint?: string          // Supabase error hint
  code?: string          // Supabase/PostgreSQL error code
  encryptionError?: EncryptionError  // CipherStash encryption-specific error
}
```

## Filter to Index Mapping

| Filter Method | Required Index | Query Type |
|---|---|---|
| `eq`, `neq`, `in` | `.equality()` | `'equality'` |
| `like`, `ilike` | `.freeTextSearch()` | `'freeTextSearch'` |
| `gt`, `gte`, `lt`, `lte` | `.orderAndRange()` | `'orderAndRange'` |
| `is` | None | No encryption (NULL/boolean check) |

## Exported Types

`@cipherstash/stack/supabase` also exports the following types:

- `EncryptedSupabaseConfig`
- `EncryptedSupabaseInstance`
- `EncryptedQueryBuilder`
- `PendingOrCondition`
- `SupabaseClientLike`
