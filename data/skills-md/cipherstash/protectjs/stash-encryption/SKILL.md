---
name: stash-encryption
description: Implement field-level encryption with @cipherstash/stack. Covers schema definition, encrypt/decrypt operations, searchable encryption (equality, free-text, range, JSON), bulk operations, model operations, identity-aware encryption with LockContext, multi-tenant keysets, and the full TypeScript type system. Use when adding encryption to a project, defining encrypted schemas, or working with the CipherStash Encryption API.
---

# CipherStash Stack - Encryption

Comprehensive guide for implementing field-level encryption with `@cipherstash/stack`. Every value is encrypted with its own unique key via ZeroKMS (backed by AWS KMS). Encryption happens client-side before data leaves the application.

## When to Use This Skill

- Adding field-level encryption to a TypeScript/Node.js project
- Defining encrypted table schemas
- Encrypting and decrypting individual values or entire models
- Implementing searchable encryption (equality, free-text, range, JSON queries)
- Bulk encrypting/decrypting large datasets
- Implementing identity-aware encryption with JWT-based lock contexts
- Setting up multi-tenant encryption with keysets
- Migrating from `@cipherstash/protect` to `@cipherstash/stack`

## Installation

```bash
npm install @cipherstash/stack
```

The package includes a native FFI module (`@cipherstash/protect-ffi`). You must opt out of bundling it in tools like Webpack, esbuild, or Next.js (`serverExternalPackages`).

## Configuration

### Environment Variables

Set these in `.env` or your hosting platform:

```bash
CS_WORKSPACE_CRN=crn:ap-southeast-2.aws:your-workspace-id
CS_CLIENT_ID=your-client-id
CS_CLIENT_KEY=your-client-key
CS_CLIENT_ACCESS_KEY=your-access-key
```

Sign up at [cipherstash.com/signup](https://cipherstash.com/signup) to generate credentials.

### Programmatic Config

```typescript
const client = await Encryption({
  schemas: [users],
  config: {
    workspaceCrn: "crn:ap-southeast-2.aws:your-workspace-id",
    clientId: "your-client-id",
    clientKey: "your-client-key",
    accessKey: "your-access-key",
    keyset: { name: "my-keyset" }, // optional: multi-tenant isolation
  },
})
```

If `config` is omitted, the client reads `CS_*` environment variables automatically.

### Logging

Logging is disabled by default. Enable it via environment variable or programmatically:

```bash
STASH_LOG_LEVEL=debug  # debug | info | warn | error (enables logging automatically)
```

#### Programmatic Logging Configuration

```typescript
const client = await Encryption({
  schemas: [users],
  logging: {
    enabled: true,     // toggle logging on/off (default: false, auto-enabled by STASH_LOG_LEVEL)
    pretty: true,      // pretty-print in development (default: auto-detected)
  },
})
```

#### Log Draining

Send structured logs to an external observability platform:

```typescript
const client = await Encryption({
  schemas: [users],
  logging: {
    drain: (ctx) => {
      // Forward to Axiom, Datadog, OTLP, etc.
      fetch("https://your-service.com/logs", {
        method: "POST",
        body: JSON.stringify(ctx.event),
      })
    },
  },
})
```

The SDK never logs plaintext data.

## Subpath Exports

| Import Path | Provides |
|---|---|
| `@cipherstash/stack` | `Encryption` function (main entry point) |
| `@cipherstash/stack/schema` | `encryptedTable`, `encryptedColumn`, `encryptedField`, schema types |
| `@cipherstash/stack/identity` | `LockContext` class and identity types |
| `@cipherstash/stack/secrets` | `Secrets` class and secrets types |
| `@cipherstash/stack/drizzle` | `encryptedType`, `extractEncryptionSchema`, `createEncryptionOperators` for Drizzle ORM |
| `@cipherstash/stack/supabase` | `encryptedSupabase` wrapper for Supabase |
| `@cipherstash/stack/dynamodb` | `encryptedDynamoDB` helper for DynamoDB |
| `@cipherstash/stack/client` | Client-safe exports (schema builders + types only, no native FFI) |
| `@cipherstash/stack/types` | All TypeScript types |

## Schema Definition

Define which tables and columns to encrypt using `encryptedTable` and `encryptedColumn`:

```typescript
import { encryptedTable, encryptedColumn } from "@cipherstash/stack/schema"

const users = encryptedTable("users", {
  email: encryptedColumn("email")
    .equality()         // exact-match queries
    .freeTextSearch()   // full-text / fuzzy search
    .orderAndRange(),   // sorting and range queries

  age: encryptedColumn("age")
    .dataType("number")
    .equality()
    .orderAndRange(),

  address: encryptedColumn("address"), // encrypt-only, no search indexes
})

const documents = encryptedTable("documents", {
  metadata: encryptedColumn("metadata")
    .searchableJson(), // encrypted JSONB queries (JSONPath + containment)
})
```

### Index Types

| Method | Purpose | Query Type |
|---|---|---|
| `.equality()` | Exact match lookups | `'equality'` |
| `.freeTextSearch(opts?)` | Full-text / fuzzy search | `'freeTextSearch'` |
| `.orderAndRange()` | Sorting, comparison, range queries | `'orderAndRange'` |
| `.searchableJson()` | Encrypted JSONB path and containment queries (auto-sets `dataType` to `'json'`) | `'searchableJson'` |
| `.dataType(cast)` | Set plaintext data type | N/A |

**Supported data types:** `'string'` (default), `'number'`, `'boolean'`, `'date'`, `'bigint'`, `'json'`

Methods are chainable - call as many as you need on a single column.

### Free-Text Search Options

```typescript
encryptedColumn("bio").freeTextSearch({
  tokenizer: { kind: "ngram", token_length: 3 },  // or { kind: "standard" }
  token_filters: [{ kind: "downcase" }],
  k: 6,
  m: 2048,
  include_original: false,
})
```

### Type Inference

```typescript
import type { InferPlaintext, InferEncrypted } from "@cipherstash/stack/schema"

type UserPlaintext = InferPlaintext<typeof users>
// { email: string; age: string; address: string }

type UserEncrypted = InferEncrypted<typeof users>
// { email: Encrypted; age: Encrypted; address: Encrypted }
```

## Client Initialization

```typescript
import { Encryption } from "@cipherstash/stack"

const client = await Encryption({ schemas: [users, documents] })
```

The `Encryption()` function returns `Promise<EncryptionClient>` and throws on error (e.g., bad credentials, missing config, invalid keyset UUID). At least one schema is required.

```typescript
// Error handling
try {
  const client = await Encryption({ schemas: [users] })
} catch (error) {
  console.error("Init failed:", error.message)
}
```

## Encrypt and Decrypt Single Values

```typescript
// Encrypt
const encrypted = await client.encrypt("hello@example.com", {
  column: users.email,
  table: users,
})

if (encrypted.failure) {
  console.error(encrypted.failure.message)
} else {
  console.log(encrypted.data) // Encrypted payload (opaque object)
}

// Decrypt
const decrypted = await client.decrypt(encrypted.data)

if (!decrypted.failure) {
  console.log(decrypted.data) // "hello@example.com"
}
```

All plaintext values must be non-null. Null handling is managed at the model level by `encryptModel` and `decryptModel`.

## Model Operations

Encrypt or decrypt an entire object. Only fields matching your schema are encrypted; other fields pass through unchanged.

The return type is **schema-aware**: fields matching the table schema are typed as `Encrypted`, while other fields retain their original types. For best results, let TypeScript infer the type parameters from the arguments rather than providing an explicit `<User>`.

```typescript
type User = { id: string; email: string; createdAt: Date }

const user = {
  id: "user_123",
  email: "alice@example.com",  // defined in schema -> encrypted
  createdAt: new Date(),       // not in schema -> unchanged
}

// Encrypt model — let TypeScript infer the return type from the schema
const encResult = await client.encryptModel(user, users)
if (!encResult.failure) {
  // encResult.data.email is typed as Encrypted
  // encResult.data.id is typed as string
  // encResult.data.createdAt is typed as Date
}

// Decrypt model
const decResult = await client.decryptModel(encResult.data)
if (!decResult.failure) {
  console.log(decResult.data.email) // "alice@example.com"
}
```

The `Decrypted<T>` type maps encrypted fields back to their plaintext types.

Passing an explicit type parameter (e.g., `client.encryptModel<User>(...)`) still works for backward compatibility — the return type degrades to `User` in that case.

## Bulk Operations

All bulk methods make a single call to ZeroKMS regardless of record count, while still using a unique key per value.

### Bulk Encrypt / Decrypt (Raw Values)

```typescript
const plaintexts = [
  { id: "u1", plaintext: "alice@example.com" },
  { id: "u2", plaintext: "bob@example.com" },
  { id: "u3", plaintext: "charlie@example.com" },
]

const encrypted = await client.bulkEncrypt(plaintexts, {
  column: users.email,
  table: users,
})
// encrypted.data = [{ id: "u1", data: EncryptedPayload }, ...]

const decrypted = await client.bulkDecrypt(encrypted.data)
// Per-item error handling:
for (const item of decrypted.data) {
  if ("data" in item) {
    console.log(`${item.id}: ${item.data}`)
  } else {
    console.error(`${item.id} failed: ${item.error}`)
  }
}
```

### Bulk Encrypt / Decrypt Models

```typescript
const userModels = [
  { id: "1", email: "alice@example.com" },
  { id: "2", email: "bob@example.com" },
]

const encrypted = await client.bulkEncryptModels(userModels, users)
const decrypted = await client.bulkDecryptModels(encrypted.data)
```

## Searchable Encryption

Encrypt query terms so you can search encrypted data in PostgreSQL.

### Single Query Encryption

```typescript
// Equality query
const eqQuery = await client.encryptQuery("alice@example.com", {
  column: users.email,
  table: users,
  queryType: "equality",
})

// Free-text search
const matchQuery = await client.encryptQuery("alice", {
  column: users.email,
  table: users,
  queryType: "freeTextSearch",
})

// Order and range
const rangeQuery = await client.encryptQuery(25, {
  column: users.age,
  table: users,
  queryType: "orderAndRange",
})
```

If `queryType` is omitted, it's auto-inferred from the column's configured indexes (priority: unique > match > ore > ste_vec).

### Query Result Formatting (`returnType`)

By default `encryptQuery` returns an `Encrypted` object (the raw EQL JSON payload). Use `returnType` to change the output format:

| `returnType` | Output | Use case |
|---|---|---|
| `'eql'` (default) | `Encrypted` object | Parameterized queries, ORMs accepting JSON |
| `'composite-literal'` | `string` | Supabase `.eq()`, string-based APIs |
| `'escaped-composite-literal'` | `string` | Embedding inside another string or JSON value |

```typescript
// Get a composite literal string for use with Supabase
const term = await client.encryptQuery("alice@example.com", {
  column: users.email,
  table: users,
  queryType: "equality",
  returnType: "composite-literal",
})
// term.data is a string
```

Each term in a batch can have its own `returnType`.

### Searchable JSON

For columns using `.searchableJson()`, the query type is auto-inferred from the plaintext:

```typescript
// String -> JSONPath selector query
const pathQuery = await client.encryptQuery("$.user.email", {
  column: documents.metadata,
  table: documents,
})

// Object/Array -> containment query
const containsQuery = await client.encryptQuery({ role: "admin" }, {
  column: documents.metadata,
  table: documents,
})
```

### Batch Query Encryption

Encrypt multiple query terms in one ZeroKMS call:

```typescript
const terms = [
  { value: "alice@example.com", column: users.email, table: users, queryType: "equality" as const },
  { value: "bob", column: users.email, table: users, queryType: "freeTextSearch" as const },
]

const results = await client.encryptQuery(terms)
// results.data = [EncryptedPayload, EncryptedPayload]
```

All values in the array must be non-null.

## Identity-Aware Encryption (Lock Contexts)

Lock encryption to a specific user by requiring a valid JWT for decryption.

```typescript
import { LockContext } from "@cipherstash/stack/identity"

// 1. Create a lock context (defaults to the "sub" claim)
const lc = new LockContext()
// Or with custom claims: new LockContext({ context: { identityClaim: ["sub", "org_id"] } })

// 2. Identify the user with their JWT
const identifyResult = await lc.identify(userJwt)
if (identifyResult.failure) {
  throw new Error(identifyResult.failure.message)
}
const lockContext = identifyResult.data

// 3. Encrypt with lock context
const encrypted = await client
  .encrypt("sensitive data", { column: users.email, table: users })
  .withLockContext(lockContext)

// 4. Decrypt with the same lock context
const decrypted = await client
  .decrypt(encrypted.data)
  .withLockContext(lockContext)
```

Lock contexts work with ALL operations: `encrypt`, `decrypt`, `encryptModel`, `decryptModel`, `bulkEncrypt`, `bulkDecrypt`, `bulkEncryptModels`, `bulkDecryptModels`, `encryptQuery`.

### CTS Token Service

The lock context exchanges the JWT for a CTS (CipherStash Token Service) token. Set the endpoint:

```bash
CS_CTS_ENDPOINT=https://ap-southeast-2.aws.auth.viturhosted.net
```

## Multi-Tenant Encryption (Keysets)

Isolate encryption keys per tenant:

```typescript
// By name
const client = await Encryption({
  schemas: [users],
  config: { keyset: { name: "Company A" } },
})

// By UUID
const client = await Encryption({
  schemas: [users],
  config: { keyset: { id: "123e4567-e89b-12d3-a456-426614174000" } },
})
```

Each keyset provides full cryptographic isolation between tenants.

## Operation Chaining

All operations return thenable objects that support chaining:

```typescript
const result = await client
  .encrypt(plaintext, { column: users.email, table: users })
  .withLockContext(lockContext)         // optional: identity-aware
  .audit({ metadata: { action: "create" } }) // optional: audit trail
```

## Error Handling

All async methods return a `Result` object - a discriminated union with either `data` (success) or `failure` (error), never both.

```typescript
const result = await client.encrypt("hello", { column: users.email, table: users })

if (result.failure) {
  console.error(result.failure.type, result.failure.message)
  // type is one of: "ClientInitError" | "EncryptionError" | "DecryptionError"
  //                  | "LockContextError" | "CtsTokenError"
} else {
  console.log(result.data)
}
```

### Error Types

| Type | When |
|---|---|
| `ClientInitError` | Client initialization fails (bad credentials, missing config) |
| `EncryptionError` | An encrypt operation fails |
| `DecryptionError` | A decrypt operation fails |
| `LockContextError` | Lock context creation or usage fails |
| `CtsTokenError` | Identity token exchange fails |

### Validation Rules

- NaN and Infinity are rejected for numeric values
- `freeTextSearch` index only supports string values
- At least one `encryptedTable` schema must be provided
- Keyset UUIDs must be valid format

## PostgreSQL Storage

Encrypted data is stored as EQL (Encrypt Query Language) JSON payloads. Install the EQL extension in PostgreSQL:

```sql
CREATE EXTENSION IF NOT EXISTS eql_v2;

CREATE TABLE users (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email eql_v2_encrypted
);
```

Or store as JSONB if not using the EQL extension directly:

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email jsonb NOT NULL
);
```

## Migration from @cipherstash/protect

| `@cipherstash/protect` | `@cipherstash/stack` | Import Path |
|---|---|---|
| `protect(config)` | `Encryption(config)` | `@cipherstash/stack` |
| `csTable(name, cols)` | `encryptedTable(name, cols)` | `@cipherstash/stack/schema` |
| `csColumn(name)` | `encryptedColumn(name)` | `@cipherstash/stack/schema` |
| `LockContext` from `/identify` | `LockContext` from `/identity` | `@cipherstash/stack/identity` |

All method signatures on the encryption client remain the same. The `Result` pattern is unchanged.

## Complete API Reference

### EncryptionClient Methods

| Method | Signature | Returns |
|---|---|---|
| `encrypt` | `(plaintext, { column, table })` | `EncryptOperation` |
| `decrypt` | `(encryptedData)` | `DecryptOperation` |
| `encryptQuery` | `(plaintext, { column, table, queryType?, returnType? })` | `EncryptQueryOperation` |
| `encryptQuery` | `(terms: readonly ScalarQueryTerm[])` | `BatchEncryptQueryOperation` |
| `encryptModel` | `(model, table)` | `EncryptModelOperation<EncryptedFromSchema<T, S>>` |
| `decryptModel` | `(encryptedModel)` | `DecryptModelOperation<T>` |
| `bulkEncrypt` | `(plaintexts, { column, table })` | `BulkEncryptOperation` |
| `bulkDecrypt` | `(encryptedPayloads)` | `BulkDecryptOperation` |
| `bulkEncryptModels` | `(models, table)` | `BulkEncryptModelsOperation<EncryptedFromSchema<T, S>>` |
| `bulkDecryptModels` | `(encryptedModels)` | `BulkDecryptModelsOperation<T>` |

All operations are thenable (awaitable) and support `.withLockContext()` and `.audit()` chaining.

### Schema Builders

```typescript
encryptedTable(tableName: string, columns: Record<string, EncryptedColumn | EncryptedField | nested>)
encryptedColumn(columnName: string) // chainable: .equality(), .freeTextSearch(), .orderAndRange(), .searchableJson(), .dataType()
encryptedField(valueName: string)   // for nested encrypted fields (not searchable), chainable: .dataType()
```
