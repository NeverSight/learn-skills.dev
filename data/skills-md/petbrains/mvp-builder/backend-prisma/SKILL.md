---
name: backend-prisma
description: Type-safe database ORM for TypeScript/Node.js. Use when you need database access with full TypeScript integration — auto-generated types from schema, migrations, and query builder. Best for PostgreSQL, MySQL, SQLite, MongoDB. Choose Prisma over raw SQL or Knex when type safety and developer experience are priorities.
allowed-tools: Read, Edit, Write, Bash (*)
---

# Prisma (Database ORM)

## Overview

Prisma is a next-generation ORM with auto-generated TypeScript types from your database schema. Define models in `schema.prisma`, run migrations, get fully typed queries.

**Version**: Prisma 6.x/7.x (2024-2025)  
**Prisma 7 Changes**: ES module by default, `prisma.config.ts`, middleware deprecated

**Key Benefit**: Change schema → regenerate client → TypeScript errors show everywhere you need updates.

## When to Use This Skill

✅ **Use Prisma when:**
- Building TypeScript backend with PostgreSQL/MySQL/SQLite
- Need type-safe database queries
- Want declarative schema with migrations
- Working with relational data and relations
- Building APIs with tRPC (perfect pair)

❌ **Consider alternatives when:**
- Complex raw SQL needed (use Prisma + `$queryRaw`)
- Ultra-high performance critical (consider Drizzle)
- Document-heavy MongoDB (native driver may be better)
- Legacy database with unusual schema

---

## Quick Start

### Installation

```bash
npm install prisma @prisma/client
npx prisma init
```

### Basic Schema

```prisma
// prisma/schema.prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_DATABASE_URL") // For migrations with pooler
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
}

model Post {
  id        String   @id @default(cuid())
  title     String   @db.VarChar(255)
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  createdAt DateTime @default(now())

  @@index([authorId])
  @@index([createdAt(sort: Desc)])
}

enum Role {
  USER
  ADMIN
}
```

---

## Singleton Client Pattern

**Always use singleton in long-running servers:**

```typescript
// src/lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || new PrismaClient({
  log: process.env.NODE_ENV === 'development' 
    ? ['query', 'error', 'warn'] 
    : ['error'],
});

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;

export default prisma;
```

---

## Query Patterns

### CRUD Operations

```typescript
// Create with relations
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    posts: {
      create: [{ title: 'First Post' }],
    },
    profile: {
      create: { bio: 'Developer' },
    },
  },
  include: { posts: true, profile: true },
});

// Find with filters
const posts = await prisma.post.findMany({
  where: {
    published: true,
    author: { role: 'ADMIN' },
  },
  orderBy: { createdAt: 'desc' },
  include: { author: { select: { name: true } } },
});

// Upsert
const user = await prisma.user.upsert({
  where: { email: 'user@example.com' },
  update: { name: 'Updated Name' },
  create: { email: 'user@example.com', name: 'New User' },
});

// Delete
await prisma.user.delete({ where: { id: userId } });
```

### Cursor-Based Pagination

```typescript
const posts = await prisma.post.findMany({
  take: 10,
  cursor: lastId ? { id: lastId } : undefined,
  orderBy: { createdAt: 'desc' },
  skip: lastId ? 1 : 0, // Skip the cursor itself
});
```

### Transactions

```typescript
// Interactive transaction
const transfer = await prisma.$transaction(async (tx) => {
  const sender = await tx.account.update({
    where: { id: senderId },
    data: { balance: { decrement: amount } },
  });
  
  if (sender.balance < 0) throw new Error('Insufficient funds');
  
  await tx.account.update({
    where: { id: receiverId },
    data: { balance: { increment: amount } },
  });
  
  return sender;
}, {
  maxWait: 5000,
  timeout: 10000,
});
```

### Select vs Include

```typescript
// Include — return full related records
const user = await prisma.user.findUnique({
  where: { id },
  include: { posts: true }, // All post fields
});

// Select — pick specific fields (better performance)
const user = await prisma.user.findUnique({
  where: { id },
  select: {
    name: true,
    posts: { select: { title: true } }, // Only titles
  },
});
```

---

## Migration Commands

```bash
# Development — create and apply migration
npx prisma migrate dev --name add_user_role

# Production — apply pending migrations
npx prisma migrate deploy

# Quick sync without history (prototyping only)
npx prisma db push

# Generate client after schema changes
npx prisma generate

# Reset database (dev only!)
npx prisma migrate reset

# View database in browser
npx prisma studio
```

---

## Type Utilities

```typescript
import { Prisma } from '@prisma/client';

// Payload type with relations
type UserWithPosts = Prisma.UserGetPayload<{
  include: { posts: true }
}>;

// Input types
type UserCreateInput = Prisma.UserCreateInput;
type UserUpdateInput = Prisma.UserUpdateInput;

// Where types
type UserWhereInput = Prisma.UserWhereInput;
```

---

## Prisma + Zod Schema Sync

### Manual Pattern (Recommended)

```typescript
// src/schemas/user.schema.ts
import { z } from 'zod';

export const UserSchema = z.object({
  id: z.string().cuid(),
  email: z.string().email(),
  name: z.string().nullable(),
  role: z.enum(['USER', 'ADMIN']),
  createdAt: z.date(),
  updatedAt: z.date(),
});

export const CreateUserSchema = UserSchema.omit({
  id: true,
  createdAt: true,
  updatedAt: true,
}).extend({
  password: z.string().min(8),
});

export type User = z.infer<typeof UserSchema>;
```

### Code Generation (Optional)

```bash
npm install -D zod-prisma-types
```

```prisma
generator zod {
  provider = "zod-prisma-types"
  output   = "../src/generated/zod"
}
```

---

## Rules

### Do ✅

- Use singleton pattern for PrismaClient
- Use `include` or `select` to avoid overfetching
- Use cursor-based pagination for large datasets
- Use `directUrl` for migrations with connection poolers
- Run `prisma generate` after schema changes
- Add indexes for frequently queried fields

### Avoid ❌

- Creating multiple PrismaClient instances
- Using `db push` in production
- N+1 queries — use `include` or `relationLoadStrategy: 'join'`
- Calling `$disconnect()` in serverless (let runtime handle it)
- Skipping migrations in team environments

---

## Common Schema Patterns

### Soft Delete

```prisma
model Post {
  id        String    @id @default(cuid())
  deletedAt DateTime?
  
  @@index([deletedAt])
}
```

```typescript
// Always filter
const posts = await prisma.post.findMany({
  where: { deletedAt: null },
});
```

### Polymorphic Relations

```prisma
model Comment {
  id           String @id @default(cuid())
  content      String
  targetType   String // "Post" | "Video"
  targetId     String
  
  @@index([targetType, targetId])
}
```

---

## Troubleshooting

```yaml
"Types not updating":
  → Run: npx prisma generate
  → Restart TypeScript server
  → Check @prisma/client version matches prisma

"Migration failed":
  → Check DATABASE_URL is correct
  → For pooled connections, use directUrl for migrations
  → Try: npx prisma migrate reset (dev only!)

"Connection pool exhausted":
  → Use singleton pattern
  → Set connection_limit in DATABASE_URL
  → For serverless: npx prisma accelerate

"N+1 query performance":
  → Add include: { relation: true }
  → Use relationLoadStrategy: 'join' (Prisma 5+)
  → Use select instead of include
```

---

## File Structure

```
prisma/
├── schema.prisma        # Database schema
├── migrations/          # Migration history
└── seed.ts              # Seed script

src/lib/
└── prisma.ts            # Singleton client
```

## References

- https://prisma.io/docs — Official documentation
- https://prisma.io/docs/concepts/components/prisma-schema — Schema reference
- https://prisma.io/docs/concepts/components/prisma-client — Client API
