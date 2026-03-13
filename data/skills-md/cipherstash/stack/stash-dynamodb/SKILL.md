---
name: stash-dynamodb
description: Integrate CipherStash encryption with Amazon DynamoDB using @cipherstash/stack/dynamodb. Covers the encryptedDynamoDB helper for encrypting items before PutItem and decrypting after GetItem, bulk encrypt/decrypt for BatchWrite and BatchGet, querying with encrypted partition and sort keys via HMAC attributes, nested object encryption, audit logging, and the DynamoDB attribute naming conventions (__source/__hmac). Use when adding encryption to a DynamoDB project, encrypting items before writes, decrypting items after reads, or querying encrypted DynamoDB attributes.
---

# CipherStash Stack - DynamoDB Integration

Guide for integrating CipherStash field-level encryption with Amazon DynamoDB using `@cipherstash/stack/dynamodb`. The helper encrypts items before writing to DynamoDB and decrypts them after reading - it does not wrap the AWS SDK, so you keep full control of your DynamoDB operations.

## When to Use This Skill

- Adding field-level encryption to DynamoDB items
- Encrypting sensitive attributes before PutItem/BatchWrite
- Decrypting attributes after GetItem/BatchGet/Query/Scan
- Querying DynamoDB using encrypted partition or sort keys
- Building applications where PII or sensitive data is stored in DynamoDB
- Implementing audit logging for DynamoDB encryption operations

## Installation

```bash
npm install @cipherstash/stack @aws-sdk/client-dynamodb @aws-sdk/lib-dynamodb
```

## How It Works

CipherStash encrypts each attribute into two DynamoDB attributes:

| Original Attribute | Stored As | Purpose |
|---|---|---|
| `email` | `email__source` | Encrypted ciphertext |
| `email` | `email__hmac` | HMAC for equality lookups (only if `.equality()` index is set) |

Non-encrypted attributes pass through unchanged. On decryption, the `__source` and `__hmac` attributes are recombined back into the original attribute name with the plaintext value.

## Setup

### 1. Define Encrypted Schema

```typescript
import { encryptedTable, encryptedColumn, encryptedField } from "@cipherstash/stack/schema"

const users = encryptedTable("users", {
  email: encryptedColumn("email").equality(),   // searchable via HMAC
  name: encryptedColumn("name"),                // encrypt-only, no search
  phone: encryptedColumn("phone"),              // encrypt-only
  metadata: encryptedColumn("metadata").dataType("json"), // encrypt-only JSON (use .searchableJson() for queryable JSON)
})
```

> **Note:** `encryptedColumn` also supports `.orderAndRange()`, `.freeTextSearch()`, and `.searchableJson()` index methods, but only `.equality()` produces HMAC values usable for DynamoDB key condition queries.

Nested objects are supported with `encryptedField`:

```typescript
const users = encryptedTable("users", {
  email: encryptedColumn("email").equality(),
  profile: {
    ssn: encryptedField("profile.ssn"),
    address: {
      street: encryptedField("profile.address.street"),
    },
  },
})
```

### 2. Initialize Clients

```typescript
import { DynamoDBClient } from "@aws-sdk/client-dynamodb"
import { DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb"
import { Encryption } from "@cipherstash/stack"
import { encryptedDynamoDB } from "@cipherstash/stack/dynamodb"

const dynamoClient = new DynamoDBClient({ region: "us-east-1" })
const docClient = DynamoDBDocumentClient.from(dynamoClient)

const encryptionClient = await Encryption({ schemas: [users] })
const dynamo = encryptedDynamoDB({ encryptionClient })
```

### Optional: Logger and Error Handler

```typescript
const dynamo = encryptedDynamoDB({
  encryptionClient,
  options: {
    logger: {
      error: (message, error) => console.error(`[DynamoDB] ${message}`, error),
    },
    errorHandler: (error) => {
      // Send to monitoring, etc.
      console.error(`[${error.code}] ${error.message}`)
    },
  },
})
```

## Encrypt and Write

### Single Item

```typescript
import { PutCommand } from "@aws-sdk/lib-dynamodb"

const user = {
  pk: "user#1",
  email: "alice@example.com",  // will be encrypted
  name: "Alice Smith",         // will be encrypted
  role: "admin",               // not in schema, passes through
}

const result = await dynamo.encryptModel(user, users)

if (result.failure) {
  console.error("Encryption failed:", result.failure.message)
} else {
  await docClient.send(new PutCommand({
    TableName: "Users",
    Item: result.data,
    // result.data looks like:
    // {
    //   pk: "user#1",
    //   email__source: "<ciphertext>",
    //   email__hmac: "<hmac>",
    //   name__source: "<ciphertext>",
    //   role: "admin",
    // }
  }))
}
```

### Bulk Items

```typescript
import { BatchWriteCommand } from "@aws-sdk/lib-dynamodb"

const items = [
  { pk: "user#1", email: "alice@example.com", name: "Alice" },
  { pk: "user#2", email: "bob@example.com", name: "Bob" },
]

const result = await dynamo.bulkEncryptModels(items, users)

if (!result.failure) {
  await docClient.send(new BatchWriteCommand({
    RequestItems: {
      Users: result.data.map(item => ({
        PutRequest: { Item: item },
      })),
    },
  }))
}
```

## Read and Decrypt

### Single Item

```typescript
import { GetCommand } from "@aws-sdk/lib-dynamodb"

const getResult = await docClient.send(new GetCommand({
  TableName: "Users",
  Key: { pk: "user#1" },
}))

const result = await dynamo.decryptModel(getResult.Item, users)

if (!result.failure) {
  console.log(result.data)
  // { pk: "user#1", email: "alice@example.com", name: "Alice Smith", role: "admin" }
}
```

### Bulk Items

```typescript
import { BatchGetCommand } from "@aws-sdk/lib-dynamodb"

const batchResult = await docClient.send(new BatchGetCommand({
  RequestItems: {
    Users: {
      Keys: [{ pk: "user#1" }, { pk: "user#2" }],
    },
  },
}))

const result = await dynamo.bulkDecryptModels(
  batchResult.Responses?.Users ?? [],
  users,
)

if (!result.failure) {
  for (const user of result.data) {
    console.log(user.email) // plaintext
  }
}
```

## Querying with Encrypted Keys

DynamoDB queries use key conditions, so you need to encrypt the search value into its HMAC form. Use `encryptionClient.encryptQuery()` to get the HMAC, then use it in your key condition.

### Encrypted Partition Key

When an encrypted attribute is the partition key (e.g., `email__hmac`):

```typescript
import { QueryCommand } from "@aws-sdk/lib-dynamodb"

// 1. Encrypt the search value to get the HMAC
const queryResult = await encryptionClient.encryptQuery([{
  value: "alice@example.com",
  column: users.email,
  table: users,
  queryType: "equality",
}])

if (queryResult.failure) {
  throw new Error(`Query encryption failed: ${queryResult.failure.message}`)
}

const emailHmac = queryResult.data[0]?.hm

// 2. Use the HMAC in a DynamoDB query
const result = await docClient.send(new QueryCommand({
  TableName: "Users",
  KeyConditionExpression: "email__hmac = :email",
  ExpressionAttributeValues: {
    ":email": emailHmac,
  },
}))

// 3. Decrypt the results
const decrypted = await dynamo.bulkDecryptModels(result.Items ?? [], users)
```

### Encrypted Sort Key

When an encrypted attribute is the sort key:

```typescript
const result = await docClient.send(new GetCommand({
  TableName: "Users",
  Key: {
    pk: "org#1",              // partition key (plain)
    email__hmac: emailHmac,   // sort key (encrypted HMAC)
  },
}))

const decrypted = await dynamo.decryptModel(result.Item, users)
```

### Encrypted Attribute in GSI

When querying a Global Secondary Index where the GSI key is an encrypted HMAC:

```typescript
const result = await docClient.send(new QueryCommand({
  TableName: "Users",
  IndexName: "EmailIndex",
  KeyConditionExpression: "email__hmac = :email",
  ExpressionAttributeValues: {
    ":email": emailHmac,
  },
  Limit: 1,
}))

if (result.Items?.length) {
  const decrypted = await dynamo.decryptModel(result.Items[0], users)
}
```

## Audit Logging

All operations support `.audit()` chaining for audit metadata:

```typescript
const result = await dynamo
  .encryptModel(user, users)
  .audit({
    metadata: {
      sub: "user-id-123",
      action: "user_registration",
      timestamp: new Date().toISOString(),
    },
  })
```

## DynamoDB Table Design Considerations

### Attribute Naming

For each encrypted field with an equality index, two attributes are stored:

- `{field}__source` - The encrypted ciphertext (binary/string)
- `{field}__hmac` - Deterministic HMAC for equality lookups

Fields without `.equality()` only get `__source` (no HMAC, so they can't be queried).

### Key Schema Design

| Pattern | Partition Key | Sort Key | Use Case |
|---|---|---|---|
| Plain PK | `pk` (plain) | - | Standard lookup by ID |
| Encrypted PK | `email__hmac` | - | Lookup by encrypted attribute |
| Encrypted SK | `pk` (plain) | `email__hmac` | Composite key with encrypted sort |
| GSI on HMAC | `pk` (plain) | - | Query by encrypted attribute via GSI with `email__hmac` as GSI PK |

### What You CAN Query

- Equality on `__hmac` attributes (exact match only)
- `attribute_exists(email__source)` / `attribute_not_exists(email__source)` in condition expressions

### What You CANNOT Query

- Range/comparison on encrypted attributes (no `BETWEEN`, `<`, `>` on `__source`)
- Substring matching on encrypted attributes (no `begins_with`, `contains` on `__source`)
- `__source` values are encrypted binary - only equality via `__hmac` is supported

## Error Handling

All operations return `Result<T, EncryptedDynamoDBError>` with either `data` or `failure`:

```typescript
const result = await dynamo.encryptModel(user, users)

if (result.failure) {
  console.error(result.failure.message)
  console.error(result.failure.code)
  // code: ProtectErrorCode | "DYNAMODB_ENCRYPTION_ERROR"
  console.error(result.failure.details)
}
```

## Complete API Reference

### `encryptedDynamoDB(config)`

```typescript
import { encryptedDynamoDB } from "@cipherstash/stack/dynamodb"

const dynamo = encryptedDynamoDB({
  encryptionClient,  // EncryptionClient instance
  options: {         // optional
    logger: { error: (message, error) => void },
    errorHandler: (error) => void,
  }
})
```

### Instance Methods

| Method | Signature | Returns |
|---|---|---|
| `encryptModel` | `(item: T, table: EncryptedTable)` | `EncryptModelOperation<T>` |
| `bulkEncryptModels` | `(items: T[], table: EncryptedTable)` | `BulkEncryptModelsOperation<T>` |
| `decryptModel` | `(item: Record<string, EncryptedValue \| unknown>, table: EncryptedTable)` | `DecryptModelOperation<T>` (resolves to `Decrypted<T>`) |
| `bulkDecryptModels` | `(items: Record<string, EncryptedValue \| unknown>[], table: EncryptedTable)` | `BulkDecryptModelsOperation<T>` (resolves to `Decrypted<T>[]`) |

All operations are thenable (awaitable) and support `.audit({ metadata })` chaining.

### Querying Encrypted Attributes

Use the encryption client directly (not the DynamoDB helper):

```typescript
// Single value form (recommended for DynamoDB lookups):
const result = await encryptionClient.encryptQuery(
  "search-value",
  { column: schema.fieldName, table: schema, queryType: "equality" }
)
const hmac = result.data?.hm

// Batch array form:
const batchResult = await encryptionClient.encryptQuery([{
  value: "search-value",
  column: schema.fieldName,
  table: schema,
  queryType: "equality",
}])
const hmac = batchResult.data[0]?.hm  // Use this in DynamoDB key conditions
```

## Complete Example

```typescript
import { DynamoDBClient } from "@aws-sdk/client-dynamodb"
import { DynamoDBDocumentClient, PutCommand, GetCommand, QueryCommand } from "@aws-sdk/lib-dynamodb"
import { Encryption } from "@cipherstash/stack"
import { encryptedDynamoDB } from "@cipherstash/stack/dynamodb"
import { encryptedTable, encryptedColumn } from "@cipherstash/stack/schema"

// Schema
const users = encryptedTable("users", {
  email: encryptedColumn("email").equality(),
  name: encryptedColumn("name"),
})

// Clients
const dynamoClient = new DynamoDBClient({ region: "us-east-1" })
const docClient = DynamoDBDocumentClient.from(dynamoClient)
const encryptionClient = await Encryption({ schemas: [users] })
const dynamo = encryptedDynamoDB({ encryptionClient })

// Write
const user = { pk: "user#1", email: "alice@example.com", name: "Alice" }
const encResult = await dynamo.encryptModel(user, users)
if (!encResult.failure) {
  await docClient.send(new PutCommand({ TableName: "Users", Item: encResult.data }))
}

// Read by primary key
const getResult = await docClient.send(new GetCommand({
  TableName: "Users",
  Key: { pk: "user#1" },
}))
const decResult = await dynamo.decryptModel(getResult.Item, users)
if (!decResult.failure) {
  console.log(decResult.data.email) // "alice@example.com"
}

// Query by encrypted email (via HMAC)
const queryEnc = await encryptionClient.encryptQuery([{
  value: "alice@example.com",
  column: users.email,
  table: users,
  queryType: "equality",
}])
const hmac = queryEnc.data[0]?.hm

const queryResult = await docClient.send(new QueryCommand({
  TableName: "Users",
  IndexName: "EmailIndex",
  KeyConditionExpression: "email__hmac = :e",
  ExpressionAttributeValues: { ":e": hmac },
}))

const decrypted = await dynamo.bulkDecryptModels(queryResult.Items ?? [], users)
```
