---
name: db-postgres
description: PostgreSQL database management with Drizzle ORM, versioned migrations, and type-safe queries. This skill should be used when setting up a new database, writing migrations, managing schemas, or troubleshooting database issues in PostgreSQL projects.
---

# PostgreSQL Database Skill

Comprehensive patterns for PostgreSQL database management in Node.js/TypeScript projects using Drizzle ORM, including a versioned migration system and local Docker development.

## When to Use This Skill

- Setting up PostgreSQL in a new project
- Writing database migrations
- Adding tables or columns to existing schemas
- Configuring local PostgreSQL with Docker
- Troubleshooting database issues

## Core Concepts

### PostgreSQL vs SQLite

PostgreSQL is appropriate when:
- Multiple servers need database access
- Remote database inspection is required
- High write concurrency is expected
- Team needs direct database access for debugging
- Complex queries, full-text search, or JSON operations

### Naming Conventions

**Singular table names** are enforced:
- `user` not `users`
- `session` not `sessions`
- `account` not `accounts`

This convention improves readability in code where you reference `user.id` rather than `users.id`.

## Database Setup Pattern

### Package Installation

```bash
npm install drizzle-orm postgres
npm install -D drizzle-kit @types/node
```

### Directory Structure

```
src/lib/db/
├── index.ts      # Connection, migrations, types
├── schema.ts     # Drizzle schema definitions
├── migrate.ts    # Migration runner
└── queries.ts    # Typed query functions (optional)

drizzle/
├── migrations/   # Generated SQL migrations
└── meta/         # Migration metadata
```

### Environment Configuration

```bash
# .env.local (development)
DATABASE_URL=postgres://postgres:postgres@localhost:5432/myapp

# Production
DATABASE_URL=postgres://user:password@host:5432/myapp?sslmode=require
```

### Connection Setup

Create `src/lib/db/index.ts`:

```typescript
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

const connectionString = process.env.DATABASE_URL;

if (!connectionString) {
  throw new Error('DATABASE_URL environment variable is required');
}

// Connection for queries
const queryClient = postgres(connectionString);

// Connection for migrations (with max 1 connection)
const migrationClient = postgres(connectionString, { max: 1 });

export const db = drizzle(queryClient, { schema });
export const migrationDb = drizzle(migrationClient);

export * from './schema';
```

### Drizzle Configuration

Create `drizzle.config.ts` at project root:

```typescript
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/lib/db/schema.ts',
  out: './drizzle/migrations',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
  verbose: true,
  strict: true,
});
```

## Schema Patterns

### Basic Schema Structure

Create `src/lib/db/schema.ts`:

```typescript
import { pgTable, text, timestamp, integer, boolean, uuid, varchar, index, uniqueIndex } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';

// Example: Define tables here as needed
// Use singular table names: user, session, account

// Type exports - infer from schema
// export type User = typeof user.$inferSelect;
// export type NewUser = typeof user.$inferInsert;
```

### Schema Conventions

**Primary Keys** - Use TEXT UUIDs or SERIAL integers:

```typescript
// UUID primary key (recommended for user-facing entities)
export const user = pgTable('user', {
  id: uuid('id').primaryKey().defaultRandom(),
  // ...
});

// Serial primary key (for internal/junction tables)
export const auditLog = pgTable('audit_log', {
  id: integer('id').primaryKey().generatedAlwaysAsIdentity(),
  // ...
});
```

**Timestamps** - Always include created/updated:

```typescript
export const user = pgTable('user', {
  id: uuid('id').primaryKey().defaultRandom(),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
});
```

**Foreign Keys** - Use cascading deletes for dependent data:

```typescript
export const session = pgTable('session', {
  id: text('id').primaryKey(),
  userId: uuid('user_id').notNull().references(() => user.id, { onDelete: 'cascade' }),
  // ...
});
```

**Indexes** - Create for frequently queried columns:

```typescript
export const user = pgTable('user', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: varchar('email', { length: 255 }).notNull(),
}, (table) => ({
  emailIdx: uniqueIndex('user_email_idx').on(table.email),
}));
```

**Enums** - Use PostgreSQL enums for fixed values:

```typescript
import { pgEnum } from 'drizzle-orm/pg-core';

export const userRoleEnum = pgEnum('user_role', ['admin', 'member', 'guest']);

export const user = pgTable('user', {
  id: uuid('id').primaryKey().defaultRandom(),
  role: userRoleEnum('role').notNull().default('member'),
});
```

### Relations

Define relations for type-safe joins:

```typescript
export const userRelations = relations(user, ({ many }) => ({
  sessions: many(session),
  accounts: many(account),
}));

export const sessionRelations = relations(session, ({ one }) => ({
  user: one(user, {
    fields: [session.userId],
    references: [user.id],
  }),
}));
```

## Migration System

### Generating Migrations

```bash
# Generate migration from schema changes
npx drizzle-kit generate

# Generate with custom name
npx drizzle-kit generate --name add_user_table
```

### Running Migrations

Create `src/lib/db/migrate.ts`:

```typescript
import { migrate } from 'drizzle-orm/postgres-js/migrator';
import { migrationDb } from './index';

async function runMigrations() {
  console.log('Running migrations...');
  
  await migrate(migrationDb, {
    migrationsFolder: './drizzle/migrations',
  });
  
  console.log('Migrations complete');
  process.exit(0);
}

runMigrations().catch((err) => {
  console.error('Migration failed:', err);
  process.exit(1);
});
```

Add to `package.json`:

```json
{
  "scripts": {
    "db:generate": "drizzle-kit generate",
    "db:migrate": "tsx src/lib/db/migrate.ts",
    "db:push": "drizzle-kit push",
    "db:studio": "drizzle-kit studio"
  }
}
```

### Migration Workflow

1. **Modify schema** in `src/lib/db/schema.ts`
2. **Generate migration**: `npm run db:generate`
3. **Review** the generated SQL in `drizzle/migrations/`
4. **Apply migration**: `npm run db:migrate`

### Key Rules

1. **Never modify existing migrations** - They may have already run in production
2. **Always review generated SQL** - Drizzle generates migrations automatically
3. **Use db:push for prototyping** - Syncs schema without migrations (dev only)
4. **Commit migrations** - They're part of your codebase

## Query Patterns

### Basic CRUD

```typescript
import { db, user } from '@/lib/db';
import { eq, and, or, desc, asc } from 'drizzle-orm';

// Insert
const newUser = await db.insert(user).values({
  email: 'user@example.com',
  name: 'John Doe',
}).returning();

// Select one
const foundUser = await db.query.user.findFirst({
  where: eq(user.email, 'user@example.com'),
});

// Select many with conditions
const users = await db.query.user.findMany({
  where: and(
    eq(user.role, 'member'),
    eq(user.active, true)
  ),
  orderBy: desc(user.createdAt),
  limit: 10,
});

// Update
await db.update(user)
  .set({ name: 'Jane Doe', updatedAt: new Date() })
  .where(eq(user.id, userId));

// Delete
await db.delete(user).where(eq(user.id, userId));
```

### With Relations

```typescript
// Fetch user with sessions
const userWithSessions = await db.query.user.findFirst({
  where: eq(user.id, userId),
  with: {
    sessions: true,
  },
});

// Nested relations
const userFull = await db.query.user.findFirst({
  where: eq(user.id, userId),
  with: {
    sessions: true,
    accounts: {
      columns: {
        provider: true,
        providerAccountId: true,
      },
    },
  },
});
```

### Transactions

```typescript
await db.transaction(async (tx) => {
  const [newUser] = await tx.insert(user).values({
    email: 'user@example.com',
  }).returning();
  
  await tx.insert(session).values({
    id: generateSessionId(),
    userId: newUser.id,
    expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
  });
});
```

## Local Development with Docker

See `docker-local` skill for complete Docker Compose setup.

Quick start:

```bash
# Start PostgreSQL
docker compose up -d postgres

# Run migrations
npm run db:migrate

# Open Drizzle Studio
npm run db:studio
```

## Troubleshooting

### "Connection refused"

Ensure PostgreSQL is running:
```bash
docker compose ps
docker compose logs postgres
```

### "Relation does not exist"

Migrations haven't run:
```bash
npm run db:migrate
```

### Type errors with schema

Regenerate types:
```bash
npx drizzle-kit generate
```

### Connection pool exhausted

For serverless environments, use connection pooling:
```typescript
const queryClient = postgres(connectionString, {
  max: 10, // Adjust based on your needs
  idle_timeout: 20,
  connect_timeout: 10,
});
```

## References

- `references/drizzle-boilerplate.md` - Complete setup code
- `references/migrations.md` - Advanced migration patterns
