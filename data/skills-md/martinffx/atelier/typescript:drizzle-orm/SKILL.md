---
name: typescript:drizzle-orm
description: Type-safe SQL with Drizzle ORM in TypeScript. Use when defining database schemas, writing queries, setting up relations, running migrations, or working with PostgreSQL/MySQL/SQLite/Cloudflare D1/Durable Objects data layers.
user-invocable: false
---

# Drizzle ORM

Lightweight, type-safe ORM with SQL-like and relational query APIs for PostgreSQL, MySQL, SQLite, Cloudflare D1, and Durable Objects.

## Quick Start (PostgreSQL)

```typescript
import {
  pgTable,
  serial,
  text,
  integer,
  timestamp,
  boolean,
  varchar,
  uuid,
  primaryKey,
  unique,
  index
} from 'drizzle-orm/pg-core'

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  age: integer('age'),
  isActive: boolean('is_active').default(true),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').$onUpdate(() => new Date()),
})

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  content: text('content'),
  authorId: integer('author_id')
    .notNull()
    .references(() => users.id, { onDelete: 'cascade' }),
  createdAt: timestamp('created_at').defaultNow().notNull(),
})
```

See [references/postgresql.md](./references/postgresql.md) for detailed PostgreSQL patterns.

## Quick Start (SQLite/D1)

```typescript
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core'

export const users = sqliteTable('users', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull(),
  isActive: integer('is_active', { mode: 'boolean' }).default(true),
  createdAt: text('created_at').notNull(),
})

export const posts = sqliteTable('posts', {
  id: text('id').primaryKey(),
  title: text('title').notNull(),
  content: text('content'),
  authorId: text('author_id')
    .notNull()
    .references(() => users.id, { onDelete: 'cascade' }),
  createdAt: text('created_at').notNull(),
})
```

See [references/sqlite.md](./references/sqlite.md) for SQLite patterns and [references/cloudflare.md](./references/cloudflare.md) for D1 and Durable Objects.

## Type Inference

```typescript
// Infer types from schema - no manual interfaces needed
export type User = typeof users.$inferSelect
export type NewUser = typeof users.$inferInsert

export type Post = typeof posts.$inferSelect
export type NewPost = typeof posts.$inferInsert
```

## Relations

```typescript
import { relations } from 'drizzle-orm'

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}))

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}))
```

## SQL-like Queries

```typescript
import { eq, and, or, gt, like, isNull, desc, asc } from 'drizzle-orm'

// Select all
const allUsers = await db.select().from(users)

// Select specific columns
const names = await db.select({ name: users.name }).from(users)

// Where clause
const activeUsers = await db
  .select()
  .from(users)
  .where(eq(users.isActive, true))

// Multiple conditions
const filtered = await db
  .select()
  .from(users)
  .where(and(
    eq(users.isActive, true),
    gt(users.age, 18)
  ))

// Like/pattern matching
const matching = await db
  .select()
  .from(users)
  .where(like(users.email, '%@example.com'))

// Order and limit
const recent = await db
  .select()
  .from(posts)
  .orderBy(desc(posts.createdAt))
  .limit(10)

// Joins
const postsWithAuthors = await db
  .select({
    postTitle: posts.title,
    authorName: users.name,
  })
  .from(posts)
  .leftJoin(users, eq(posts.authorId, users.id))
```

## Relational Queries

```typescript
// Requires schema with relations passed to drizzle()
const db = drizzle(pool, { schema })

// Find many with relations
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: true,
  },
})

// Partial columns + nested relations
const partial = await db.query.users.findMany({
  columns: {
    id: true,
    name: true,
  },
  with: {
    posts: {
      columns: {
        title: true,
        createdAt: true,
      },
    },
  },
})

// Find first
const user = await db.query.users.findFirst({
  where: eq(users.id, 1),
  with: { posts: true },
})

// Exclude columns
const withoutEmail = await db.query.users.findMany({
  columns: {
    email: false, // exclude
  },
})
```

## Insert

```typescript
// Single insert
const [newUser] = await db
  .insert(users)
  .values({ name: 'Alice', email: 'alice@example.com' })
  .returning()

// Multiple insert
await db.insert(users).values([
  { name: 'Bob', email: 'bob@example.com' },
  { name: 'Carol', email: 'carol@example.com' },
])

// Upsert (on conflict)
await db
  .insert(users)
  .values({ name: 'Alice', email: 'alice@example.com' })
  .onConflictDoUpdate({
    target: users.email,
    set: { name: 'Alice Updated' },
  })
```

## Update

```typescript
await db
  .update(users)
  .set({ isActive: false })
  .where(eq(users.id, 1))

// Update with returning
const [updated] = await db
  .update(users)
  .set({ name: 'New Name' })
  .where(eq(users.id, 1))
  .returning()
```

## Delete

```typescript
await db.delete(users).where(eq(users.id, 1))

// Delete with returning
const [deleted] = await db
  .delete(users)
  .where(eq(users.id, 1))
  .returning()
```

## Transactions

```typescript
await db.transaction(async (tx) => {
  const [user] = await tx
    .insert(users)
    .values({ name: 'Alice', email: 'alice@example.com' })
    .returning()

  await tx.insert(posts).values({
    title: 'First Post',
    authorId: user.id,
  })
})
```

## Entity Pattern

Domain entities encapsulate data transformations between API, domain, and database layers.

```typescript
import type { InferInsertModel, InferSelectModel } from 'drizzle-orm'
import type { users } from './schema'

type UserRecord = InferSelectModel<typeof users>
type UserInsert = InferInsertModel<typeof users>

class UserEntity {
  public readonly id: string
  public readonly name: string
  public readonly email: string
  public readonly createdAt: Date

  private constructor(data: UserEntityData) {
    Object.assign(this, data)
  }

  // API request → Entity
  static fromRequest(rq: CreateUserRequest, id?: string): UserEntity {
    return new UserEntity({
      id: id ?? crypto.randomUUID(),
      name: rq.name,
      email: rq.email,
      createdAt: new Date(),
    })
  }

  // DB record → Entity
  static fromRecord(record: UserRecord): UserEntity {
    return new UserEntity({
      id: record.id,
      name: record.name,
      email: record.email,
      createdAt: record.createdAt,
    })
  }

  // Entity → DB insert
  toRecord(): UserInsert {
    return {
      id: this.id,
      name: this.name,
      email: this.email,
      createdAt: this.createdAt,
    }
  }

  // Entity → API response
  toResponse(): UserResponse {
    return {
      id: this.id,
      name: this.name,
      email: this.email,
      createdAt: this.createdAt.toISOString(),
    }
  }
}
```

See [references/entity-pattern.md](./references/entity-pattern.md) for detailed examples.

## Repository Pattern

Repositories wrap database access with error handling and business logic.

```typescript
import { eq, and } from 'drizzle-orm'
import { users } from './schema'
import { UserEntity } from './entities/UserEntity'

class UserRepo {
  constructor(private db: DrizzleDB) {}

  async getById(id: string): Promise<UserEntity> {
    const record = await this.db.query.users.findFirst({
      where: eq(users.id, id),
    })
    if (!record) throw new NotFoundError('User not found')
    return UserEntity.fromRecord(record)
  }

  async create(entity: UserEntity): Promise<UserEntity> {
    try {
      const [record] = await this.db
        .insert(users)
        .values(entity.toRecord())
        .returning()
      return UserEntity.fromRecord(record)
    } catch (error) {
      throw handleDBError(error, { userId: entity.id })
    }
  }

  async update(entity: UserEntity): Promise<UserEntity> {
    const [record] = await this.db
      .update(users)
      .set(entity.toRecord())
      .where(eq(users.id, entity.id))
      .returning()
    if (!record) throw new NotFoundError('User not found')
    return UserEntity.fromRecord(record)
  }
}
```

See [references/repository-pattern.md](./references/repository-pattern.md) for detailed examples.

## Database-Specific Guides

For database-specific patterns, connection setup, migrations, and testing:

- **[PostgreSQL patterns](./references/postgresql.md)** - Connection, migrations, column types, error codes, optimistic locking
- **[SQLite patterns](./references/sqlite.md)** - Schema definition, type differences, better-sqlite3 testing
- **[Cloudflare D1 & Durable Objects](./references/cloudflare.md)** - D1 connection, DO SQLite, testing with vitest-pool-workers, D1 vs DO decision guide

## Guidelines

1. Define schema in dedicated `schema.ts` file(s)
2. Use `$inferSelect` and `$inferInsert` for types - don't duplicate
3. Always define relations for nested queries with `db.query`
4. Pass `{ schema }` to `drizzle()` to enable relational queries
5. Use SQL-like API (`db.select()`) for complex joins
6. Use relational API (`db.query`) for nested data fetching
7. Foreign keys need explicit `references(() => table.column)`
8. Use `returning()` to get inserted/updated/deleted rows
9. Wrap database access in Repository classes for error handling
10. Use Entity classes for all data transformations (fromRequest, fromRecord, toRecord, toResponse)
11. Add `lockVersion` column for optimistic locking on mutable resources
12. Handle DB errors with specific error types (23505=conflict, 23503=not found, 40001/OC000=retry)
