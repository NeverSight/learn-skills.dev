---
name: drizzle-orm-v0
description: Drizzle ORM for TypeScript — type-safe SQL queries, schema definitions, migrations, and relations. Use when building database layers in TypeScript applications.
---

# Skill: drizzle-orm

## Scope

- Applies to: Drizzle ORM v0.45+ for PostgreSQL, MySQL, SQLite - schema definitions, type-safe queries, migrations
- Does NOT cover: Database driver setup, connection pooling configuration, other ORMs

## Assumptions

- Drizzle ORM v0.45+
- Drizzle Kit v0.31+ (dev dependency) for migrations
- PostgreSQL, MySQL, or SQLite database
- TypeScript v5+ with strict mode
- ESM module system

## Principles

- Schemas defined using table builders (`pgTable`, `mysqlTable`, `sqliteTable`) with typed columns
- Column types match database constraints (`varchar` with length, `timestamp` with mode)
- Indexes defined in table definition second parameter using `index()` helper
- Text primary keys with `.references()` for foreign keys are a valid default
- Query helpers (`eq`, `and`, `or`, `like`) provide type-safe SQL construction
- Type inference via `$inferSelect` and `$inferInsert` eliminates manual types
- Migrations generated with `drizzle-kit generate` (not `push` in production)
- Prepared statements optimize frequently executed queries
- Schemas organized by domain (one file per entity/table)
- Transactions (`db.transaction`) ensure atomic multi-step operations

## Constraints

### MUST

- Use Drizzle Kit for migrations (`drizzle-kit generate`, `drizzle-kit migrate`)
- Define column types matching database constraints
- Use query helpers instead of raw SQL

### SHOULD

- Use transactions for multi-step operations
- Use prepared statements for frequently executed queries
- Export types via `$inferSelect` and `$inferInsert`
- Handle `DrizzleQueryError` for structured error handling
- Organize schemas by domain (one file per entity)
- Use selective field loading (not full rows)
- Specify length for `varchar` columns
- Use `index()` helper in table definitions
- Use PGLite for testing PostgreSQL schemas
- Use `relations()` and relational query builder when the project already uses them

### OPTIONAL

- Identity columns (`generatedAlwaysAsIdentity`) instead of `serial` in PostgreSQL
- Relational query builder (`db.query.*`) for complex joins when relations are defined

### AVOID

- Raw SQL unless necessary
- Manual type assertions (use inferred types)
- Skipping migration generation
- `serial` in new PostgreSQL tables (use identity columns)
- Over-indexing (index only where queries justify)
- Fetching full rows when only few columns needed
- `push` in production (use `generate` + `migrate`)
- String-based timestamp mode when DB supports date/time types

## Interactions

- Works with [next](../next-v16/SKILL.md) Server Components and API routes
- Complements [fastify](../fastify-v5/SKILL.md) for API development

## Patterns

### Schema Definition

```typescript
import { index, pgTable, text, timestamp, varchar } from 'drizzle-orm/pg-core'

export const users = pgTable(
  'users',
  {
    id: text('id').primaryKey(),
    email: varchar('email', { length: 255 }).notNull().unique(),
    createdAt: timestamp('created_at').defaultNow().notNull(),
    updatedAt: timestamp('updated_at').defaultNow().notNull(),
  },
  table => [index('users_email_idx').on(table.email)],
)

export type User = typeof users.$inferSelect
export type NewUser = typeof users.$inferInsert
```

### Identity Columns

```typescript
import { pgTable, integer, generatedAlwaysAsIdentity } from 'drizzle-orm/pg-core'

export const posts = pgTable('posts', {
  id: integer('id').primaryKey().generatedAlwaysAsIdentity(),
})
```

### Query Builder

```typescript
import { eq } from 'drizzle-orm'

const user = await db
  .select()
  .from(users)
  .where(eq(users.id, userId))
  .limit(1)

const userWithPosts = await db.query.users.findFirst({
  where: eq(users.id, userId),
  with: { posts: true },
})

const userEmail = await db
  .select({ email: users.email })
  .from(users)
  .where(eq(users.id, userId))
```

### Transactions

```typescript
await db.transaction(async (tx) => {
  const [user] = await tx.insert(users).values(userData).returning()
  await tx.insert(profiles).values({ userId: user.id, ...profileData })
})
```

### Prepared Statements

```typescript
import { placeholder } from 'drizzle-orm'

const getUserByEmail = db
  .select()
  .from(users)
  .where(eq(users.email, placeholder('email')))
  .prepare('get_user_by_email')

const user = await getUserByEmail.execute({ email: 'user@example.com' })
```

### Error Handling

```typescript
import { DrizzleQueryError } from 'drizzle-orm'

try {
  const user = await db.select().from(users).where(eq(users.id, userId))
} catch (error) {
  if (error instanceof DrizzleQueryError) {
    if (error.cause?.code === '23505') {
      throw new Error('User already exists')
    }
  }
  throw error
}
```

### Relations

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

### Database Connection

```typescript
import { drizzle } from 'drizzle-orm/node-postgres'
import { Pool } from 'pg'
import * as schema from './schema'

const pool = new Pool({ connectionString: process.env.DATABASE_URL })
export const db = drizzle(pool, { schema })
```

### Drizzle Kit Config

```typescript
import { defineConfig } from 'drizzle-kit'

export default defineConfig({
  dialect: 'postgresql',
  schema: './src/db/schema/index.ts',
  out: './src/db/migrations',
  dbCredentials: { url: process.env.DATABASE_URL! },
  migrations: {
    table: '__drizzle_migrations',
    schema: 'public',
  },
  verbose: true,
  strict: true,
})
```

## References

- [Query Patterns](references/queries.md) - CRUD operations, joins, aggregations
- [PostgreSQL Patterns](references/postgresql-patterns.md) - PostgreSQL-specific patterns
