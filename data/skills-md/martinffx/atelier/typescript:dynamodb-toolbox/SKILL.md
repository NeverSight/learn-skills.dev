---
name: typescript:dynamodb-toolbox
description: DynamoDB single-table design using dynamodb-toolbox v2. Use when creating entities, defining key patterns, designing GSIs, writing queries, implementing pagination, or working with any DynamoDB data layer in TypeScript projects.
user-invocable: false
---

# DynamoDB with dynamodb-toolbox v2

Type-safe DynamoDB interactions with Entity and Table abstractions for single-table design.

## When to Use DynamoDB

✓ **Use when:**
- Access patterns are known upfront and stable
- Need predictable sub-10ms performance at scale
- Microservice with clear data boundaries
- Willing to commit to single-table design

✗ **Avoid when:**
- Prototyping with fluid requirements
- Need ad-hoc analytical queries
- Team lacks DynamoDB expertise
- GraphQL resolvers drive access patterns

> DynamoDB inverts the relational paradigm: design for known access patterns, not flexible querying.

## Modeling Checklist

Before implementing:
1. **Define Entity Relationships** - Create ERD with all entities and relationships
2. **Create Entity Chart** - Map each entity to PK/SK patterns
3. **Design GSI Strategy** - Plan secondary access patterns
4. **Document Access Patterns** - List every query the application needs

See [references/modeling.md](references/modeling.md) for detailed methodology.

## Table Configuration

```typescript
import { Table } from 'dynamodb-toolbox/table'

const AppTable = new Table({
  name: process.env.TABLE_NAME || "AppTable",
  partitionKey: { name: "PK", type: "string" },
  sortKey: { name: "SK", type: "string" },
  indexes: {
    GSI1: {
      type: "global",
      partitionKey: { name: "GSI1PK", type: "string" },
      sortKey: { name: "GSI1SK", type: "string" },
    },
    GSI2: {
      type: "global",
      partitionKey: { name: "GSI2PK", type: "string" },
      sortKey: { name: "GSI2SK", type: "string" },
    },
    GSI3: {
      type: "global",
      partitionKey: { name: "GSI3PK", type: "string" },
      sortKey: { name: "GSI3SK", type: "string" },
    },
  },
  entityAttributeSavedAs: "_et", // default, customize if needed
});
```

### Index Purpose

| Index | Purpose |
|-------|---------|
| Main Table (PK/SK) | Primary entity access |
| GSI1 | Collection queries (issues by repo, members by org) |
| GSI2 | Entity-specific queries and relationships (forks) |
| GSI3 | Hierarchical queries with temporal sorting (repos by owner) |

## Entity Definition (v2 syntax)

### Basic Pattern with Linked Keys

```typescript
import { Entity } from 'dynamodb-toolbox/entity'
import { item } from 'dynamodb-toolbox/schema/item'
import { string } from 'dynamodb-toolbox/schema/string'

const UserEntity = new Entity({
  name: "USER",
  table: AppTable,
  schema: item({
    // Business attributes
    username: string().required().key(),
    email: string().required(),
    bio: string().optional(),
  }).and(_schema => ({
    // Computed keys (PK/SK/GSI keys derived from business attributes)
    PK: string().key().link<typeof _schema>(
      ({ username }) => `ACCOUNT#${username}`
    ),
    SK: string().key().link<typeof _schema>(
      ({ username }) => `ACCOUNT#${username}`
    ),
    GSI1PK: string().link<typeof _schema>(
      ({ username }) => `ACCOUNT#${username}`
    ),
    GSI1SK: string().link<typeof _schema>(
      ({ username }) => `ACCOUNT#${username}`
    ),
  })),
});
```

### With Validation

```typescript
const RepoEntity = new Entity({
  name: "REPO",
  table: AppTable,
  schema: item({
    owner: string()
      .required()
      .validate((value: string) => /^[a-zA-Z0-9_-]+$/.test(value))
      .key(),
    repo_name: string()
      .required()
      .validate((value: string) => /^[a-zA-Z0-9_-]+$/.test(value))
      .key(),
    description: string().optional(),
    is_private: boolean().default(false),
  }).and(_schema => ({
    PK: string().key().link<typeof _schema>(
      ({ owner, repo_name }) => `REPO#${owner}#${repo_name}`
    ),
    SK: string().key().link<typeof _schema>(
      ({ owner, repo_name }) => `REPO#${owner}#${repo_name}`
    ),
    // GSI3 for temporal sorting (repos by owner, newest first)
    GSI3PK: string().link<typeof _schema>(
      ({ owner }) => `ACCOUNT#${owner}`
    ),
    GSI3SK: string()
      .default(() => `#${new Date().toISOString()}`)
      .savedAs("GSI3SK"),
  })),
});
```

## Entity Chart (Key Patterns)

| Entity | PK | SK | Purpose |
|--------|----|----|---------|
| User | `ACCOUNT#{username}` | `ACCOUNT#{username}` | Direct access |
| Repository | `REPO#{owner}#{name}` | `REPO#{owner}#{name}` | Direct access |
| Issue | `ISSUE#{owner}#{repo}#{padded_num}` | Same as PK | Direct access + enumeration |
| Comment | `REPO#{owner}#{repo}` | `ISSUE#{padded_num}#COMMENT#{id}` | Comments under issue |
| Star | `ACCOUNT#{username}` | `STAR#{owner}#{repo}#{timestamp}` | Adjacency list pattern |

**Key Pattern Rules:**
- `ENTITY#{id}` - Simple identifier
- `PARENT#{id}#CHILD#{id}` - Hierarchy
- `TYPE#{category}#{identifier}` - Categorization
- `#{timestamp}` - Temporal sorting (# prefix ensures ordering)

## Type Safety

```typescript
import { type InputItem, type FormattedItem } from 'dynamodb-toolbox/entity'

// Type exports
type UserRecord = typeof UserEntity
type UserInput = InputItem<typeof UserEntity>      // For writes
type UserFormatted = FormattedItem<typeof UserEntity> // For reads

// Usage in entities
class User {
  static fromRecord(record: UserFormatted): User { /* ... */ }
  toRecord(): UserInput { /* ... */ }
}
```

See [references/entity-layer.md](references/entity-layer.md) for transformation patterns.

## Repository Pattern

```typescript
import { PutItemCommand, GetItemCommand, DeleteItemCommand } from 'dynamodb-toolbox'

class UserRepository {
  constructor(private entity: UserRecord) {}

  // CREATE with duplicate check
  async create(user: User): Promise<User> {
    try {
      const result = await this.entity
        .build(PutItemCommand)
        .item(user.toRecord())
        .options({
          condition: { attr: "PK", exists: false }, // Prevent duplicates
        })
        .send()

      return User.fromRecord(result.ToolboxItem)
    } catch (error) {
      if (error instanceof ConditionalCheckFailedException) {
        throw new DuplicateEntityError("User", user.username)
      }
      throw error
    }
  }

  // GET by key
  async get(username: string): Promise<User | undefined> {
    const result = await this.entity
      .build(GetItemCommand)
      .key({ username })
      .send()

    return result.Item ? User.fromRecord(result.Item) : undefined
  }

  // UPDATE with existence check
  async update(user: User): Promise<User> {
    try {
      const result = await this.entity
        .build(PutItemCommand)
        .item(user.toRecord())
        .options({
          condition: { attr: "PK", exists: true }, // Must exist
        })
        .send()

      return User.fromRecord(result.ToolboxItem)
    } catch (error) {
      if (error instanceof ConditionalCheckFailedException) {
        throw new EntityNotFoundError("User", user.username)
      }
      throw error
    }
  }

  // DELETE
  async delete(username: string): Promise<void> {
    await this.entity.build(DeleteItemCommand).key({ username }).send()
  }
}
```

See [references/error-handling.md](references/error-handling.md) for error patterns.

## Query Patterns

### Query GSI

```typescript
import { QueryCommand } from 'dynamodb-toolbox/table/actions/query'

// List issues for a repository using GSI1
async listIssues(owner: string, repoName: string): Promise<Issue[]> {
  const result = await this.table
    .build(QueryCommand)
    .entities(this.issueEntity)
    .query({
      partition: `ISSUE#${owner}#${repoName}`,
      index: "GSI1",
    })
    .send()

  return result.Items?.map(item => Issue.fromRecord(item)) || []
}
```

### Query with Range Filter

```typescript
// List by status using beginsWith on SK
async listOpenIssues(owner: string, repoName: string): Promise<Issue[]> {
  const result = await this.table
    .build(QueryCommand)
    .entities(this.issueEntity)
    .query({
      partition: `ISSUE#${owner}#${repoName}`,
      index: "GSI4",
      range: {
        beginsWith: "ISSUE#OPEN#", // Filter to open issues only
      },
    })
    .send()

  return result.Items?.map(item => Issue.fromRecord(item)) || []
}
```

### Pagination

```typescript
// Encode/decode pagination tokens
function encodePageToken(lastEvaluated?: Record<string, unknown>): string | undefined {
  return lastEvaluated
    ? Buffer.from(JSON.stringify(lastEvaluated)).toString("base64")
    : undefined
}

function decodePageToken(token?: string): Record<string, unknown> | undefined {
  return token ? JSON.parse(Buffer.from(token, "base64").toString()) : undefined
}

// Query with pagination
async listReposByOwner(owner: string, limit = 50, offset?: string) {
  const result = await this.table
    .build(QueryCommand)
    .entities(this.repoEntity)
    .query({
      partition: `ACCOUNT#${owner}`,
      index: "GSI3",
      range: { lt: "ACCOUNT#" }, // Filter to only repos (not account itself)
    })
    .options({
      reverse: true,                              // Newest first
      exclusiveStartKey: decodePageToken(offset), // Continue from cursor
      limit,
    })
    .send()

  return {
    items: result.Items?.map(item => Repo.fromRecord(item)) || [],
    nextOffset: encodePageToken(result.LastEvaluatedKey),
  }
}
```

## Transactions

See [references/transactions.md](references/transactions.md) for:
- Multi-entity transactions (PutTransaction + ConditionCheck)
- Atomic counters with `$add(1)`
- TransactionCanceledException handling

## Testing

See [references/testing.md](references/testing.md) for:
- DynamoDB Local setup
- Test fixtures and factories
- Concurrency and temporal sorting tests

## Quick Reference

**Schema:**
- Use `item({})` for schema definition
- Mark key attributes with `.key()`
- Separate business attributes from computed keys using `.and()`
- Use `.link<typeof _schema>()` to compute PK/SK/GSI keys
- Use `.validate()` for field validation
- Use `.savedAs()` when DynamoDB name differs from schema name

**Types:**
- `InputItem<T>` for writes (excludes computed attributes)
- `FormattedItem<T>` for reads (includes all attributes)

**Repository:**
- Use `PutItemCommand` with `{ attr: "PK", exists: false }` for creates
- Use `PutItemCommand` with `{ attr: "PK", exists: true }` for updates
- Use `GetItemCommand` with `.key()` for reads
- Use `QueryCommand` with `.entities()` for type-safe queries

**Errors:**
- `ConditionalCheckFailedException` → DuplicateEntityError (create) or EntityNotFoundError (update)
- Always catch and convert to domain errors

**Testing:**
- Use unique IDs per test run (timestamp-based)
- Clean up test data after each test
- Use DynamoDB Local for development
