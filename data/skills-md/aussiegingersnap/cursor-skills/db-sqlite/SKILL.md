---
name: db-sqlite
description: SQLite database management with Prisma ORM, type-safe queries, and Railway deployment with Litestream backup. This skill should be used when creating database schemas, writing migrations, managing SQLite on Railway volumes, or troubleshooting database issues.
---

# SQLite Database Skill

Comprehensive patterns for SQLite database management in Node.js/TypeScript projects using Prisma ORM, including schema-first development and Railway deployment with Litestream backup.

## When to Use This Skill

- Setting up SQLite in a new project
- Defining database schemas with Prisma
- Running migrations with `prisma migrate`
- Deploying SQLite to Railway with persistent volumes
- Backing up production databases with Litestream
- Troubleshooting database issues

## Core Concepts

### SQLite vs Network Databases

SQLite is appropriate when:
- Single server/container deployment
- Read-heavy workloads (or moderate writes)
- Simplicity is valued over horizontal scaling
- Local-first or embedded scenarios
- Cost-sensitive deployments

Consider PostgreSQL when:
- Multiple servers need database access
- Remote database inspection is required
- High write concurrency is expected
- Team needs direct database access for debugging

### Railway Deployment Constraints

SQLite on Railway requires understanding these constraints:

1. **Volume mounting** - Database file must live on a Railway volume (not container filesystem)
2. **No remote access** - Cannot connect database GUI tools directly to production
3. **Single container** - Only one instance can write to the database
4. **Backup strategy** - Use Litestream for continuous backup to Railway Bucket

### Critical: Railway Volume Path vs Container Path

**This is the #1 cause of data loss on Railway SQLite deployments.**

Railway volumes mount at a specific path (e.g., `/data`). But your app runs in `/app/` by default. If your code writes to `./prisma/app.db`, it creates the file at `/app/prisma/app.db` — **which is NOT on the volume** and gets destroyed on every deploy.

**Solution**: Set `DATABASE_URL` to use the volume path in production.

```
# Wrong (data lost on each deploy):
file:/app/prisma/app.db  ← Container filesystem, not persistent

# Correct (data persists):
file:/data/app.db        ← Railway volume, persistent + backed up
```

## Database Setup Pattern

### Package Installation

```bash
npm install @prisma/client
npm install -D prisma
```

### Directory Structure

```
prisma/
├── schema.prisma    # Database schema (source of truth)
└── migrations/      # Generated SQL migrations

src/lib/db/
└── index.ts         # Prisma client singleton
```

### Environment Configuration

```bash
# .env.local (development)
DATABASE_URL="file:./prisma/dev.db"

# Railway (production) — REQUIRED
# Must point to volume mount path
DATABASE_URL="file:/data/app.db"
```

### Prisma Schema Setup

Create `prisma/schema.prisma`:

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}

// Define your models here
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### Prisma Client Singleton

Create `src/lib/db/index.ts`:

```typescript
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
})

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma
}

export default prisma
```

### Package.json Scripts

```json
{
  "scripts": {
    "db:generate": "prisma generate",
    "db:migrate": "prisma migrate dev",
    "db:migrate:prod": "prisma migrate deploy",
    "db:push": "prisma db push",
    "db:studio": "prisma studio",
    "db:reset": "prisma migrate reset"
  }
}
```

## Schema Patterns

### Primary Keys

Use CUID or UUID for user-facing entities:

```prisma
model User {
  id String @id @default(cuid())
  // or: id String @id @default(uuid())
}
```

### Timestamps

Always include created/updated timestamps:

```prisma
model Post {
  id        String   @id @default(cuid())
  title     String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### Relations

One-to-many:

```prisma
model User {
  id    String @id @default(cuid())
  posts Post[]
}

model Post {
  id       String @id @default(cuid())
  authorId String
  author   User   @relation(fields: [authorId], references: [id], onDelete: Cascade)
}
```

Many-to-many (explicit junction table):

```prisma
model Post {
  id   String     @id @default(cuid())
  tags PostTag[]
}

model Tag {
  id    String    @id @default(cuid())
  name  String    @unique
  posts PostTag[]
}

model PostTag {
  postId String
  tagId  String
  post   Post   @relation(fields: [postId], references: [id], onDelete: Cascade)
  tag    Tag    @relation(fields: [tagId], references: [id], onDelete: Cascade)

  @@id([postId, tagId])
}
```

### Enums

```prisma
enum Role {
  ADMIN
  USER
  GUEST
}

model User {
  id   String @id @default(cuid())
  role Role   @default(USER)
}
```

### Indexes

```prisma
model Post {
  id        String   @id @default(cuid())
  authorId  String
  published Boolean  @default(false)
  createdAt DateTime @default(now())

  @@index([authorId])
  @@index([published, createdAt])
}
```

### Unique Constraints

```prisma
model BookCollaborator {
  id     String @id @default(cuid())
  bookId String
  userId String

  @@unique([bookId, userId])
}
```

## Migration Workflow

### Development

```bash
# Make schema changes in prisma/schema.prisma

# Create and apply migration
npm run db:migrate
# Prompts for migration name, e.g., "add_posts_table"

# Quick iteration (no migration file, just sync)
npm run db:push
```

### Production

```bash
# Apply pending migrations (run in CI/CD or startup)
npm run db:migrate:prod
```

### Migration Best Practices

1. **Never edit applied migrations** - They may have run in production
2. **Name migrations descriptively** - `add_user_avatar`, `create_posts_table`
3. **Review generated SQL** - Check `prisma/migrations/` before deploying
4. **Use db:push for prototyping** - Switch to migrations when schema stabilizes
5. **Commit migrations** - They're part of your codebase

## Query Patterns

### Basic CRUD

```typescript
import { prisma } from '@/lib/db'

// Create
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    name: 'John Doe',
  },
})

// Read one
const user = await prisma.user.findUnique({
  where: { email: 'user@example.com' },
})

// Read many with filters
const users = await prisma.user.findMany({
  where: {
    role: 'ADMIN',
    createdAt: { gte: new Date('2024-01-01') },
  },
  orderBy: { createdAt: 'desc' },
  take: 10,
})

// Update
const updated = await prisma.user.update({
  where: { id: userId },
  data: { name: 'Jane Doe' },
})

// Delete
await prisma.user.delete({
  where: { id: userId },
})
```

### With Relations

```typescript
// Include related data
const userWithPosts = await prisma.user.findUnique({
  where: { id: userId },
  include: {
    posts: {
      where: { published: true },
      orderBy: { createdAt: 'desc' },
    },
  },
})

// Select specific fields
const userEmail = await prisma.user.findUnique({
  where: { id: userId },
  select: {
    email: true,
    posts: {
      select: { title: true },
    },
  },
})

// Nested create
const userWithPost = await prisma.user.create({
  data: {
    email: 'author@example.com',
    posts: {
      create: {
        title: 'My First Post',
      },
    },
  },
  include: { posts: true },
})
```

### Transactions

```typescript
// Sequential operations
const [user, post] = await prisma.$transaction([
  prisma.user.create({ data: { email: 'user@example.com' } }),
  prisma.post.create({ data: { title: 'Hello', authorId: 'temp' } }),
])

// Interactive transaction
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({
    data: { email: 'user@example.com' },
  })
  
  await tx.post.create({
    data: {
      title: 'My Post',
      authorId: user.id,
    },
  })
})
```

### Upsert

```typescript
const user = await prisma.user.upsert({
  where: { email: 'user@example.com' },
  update: { name: 'Updated Name' },
  create: { email: 'user@example.com', name: 'New User' },
})
```

## Railway Operations

### Environment Variables

Required Railway configuration:

```
DATABASE_URL=file:/data/app.db
```

Ensure volume is mounted at `/data`.

### Shell Access

```bash
# Open interactive shell in Railway container
railway shell

# Inside container - use Prisma Studio (opens web UI)
npx prisma studio

# Or use sqlite3 directly
sqlite3 /data/app.db
.tables
.schema User
SELECT * FROM User LIMIT 5;
.quit
```

### Check Migration Status

```bash
railway shell
npx prisma migrate status
```

## Continuous Backup with Litestream

Litestream provides real-time SQLite replication to S3-compatible storage. Combined with Railway Buckets, this gives you continuous backups without external providers.

**See `references/litestream.md` for complete setup guide.**

### Quick Overview

1. Litestream monitors SQLite WAL changes
2. Streams changes to Railway Bucket every ~10 seconds
3. On container restart, restores from bucket if local DB is missing
4. ~10 second recovery point objective (RPO)

### Minimal Setup

```bash
# 1. Create Railway Bucket
railway add --service bucket

# 2. Add litestream.yml to project root
# 3. Update nixpacks.toml to install litestream
# 4. Update railway.toml start command
# 5. Add restore script for empty volumes
```

## Troubleshooting

### "Cannot find module '@prisma/client'"

Generate the client after schema changes:
```bash
npm run db:generate
```

### "Migration failed"

Check migration status and pending migrations:
```bash
npx prisma migrate status
```

For stuck migrations, you may need to mark as applied or reset:
```bash
# Mark a migration as applied (use with caution)
npx prisma migrate resolve --applied <migration_name>

# Reset database (development only)
npx prisma migrate reset
```

### "Database is locked"

SQLite allows only one writer at a time. Solutions:
1. Keep transactions short
2. Avoid long-running queries during writes
3. Use connection pooling sparingly (usually singleton is fine)

### Production Database Issues

1. Check Litestream backup status
2. Restore from backup if needed
3. Review `references/litestream.md` for restore procedures

## References

- `references/boilerplate.md` - Complete Prisma setup code
- `references/migrations.md` - Migration patterns and examples
- `references/litestream.md` - Continuous backup setup with Railway Buckets
- [Prisma Docs](https://www.prisma.io/docs) - Official documentation
- [Railway SQLite Guide](https://docs.railway.com/guides/sqlite) - Railway-specific patterns
