---
name: db-prisma
description: Prisma 7 ORM with PostgreSQL — schema design, migrations, seeding, and Railway deployment patterns. This skill should be used when setting up Prisma in a new project, writing migrations, managing database schemas, or deploying Prisma-backed services to Railway.
---

# Prisma Database Skill

Production patterns for Prisma 7 ORM with PostgreSQL, including schema design, versioned migrations, seeding, and Railway-specific configuration.

## When to Use This Skill

- Setting up Prisma in a new project
- Designing database schemas (models, relations, enums)
- Writing and running migrations
- Seeding development databases
- Deploying Prisma-backed services to Railway
- Troubleshooting Prisma/PostgreSQL issues

## Project Setup

### Installation

```bash
npm install prisma @prisma/client
npx prisma init --datasource-provider postgresql
```

### Directory Structure

```
prisma/
  schema.prisma       # Schema definition
  migrations/         # Versioned SQL migrations
  seed.ts             # Database seeder
```

### Environment

```bash
# .env (development)
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/myapp?schema=public"

# Railway (production) — auto-wired from Postgres service
DATABASE_URL="postgresql://user:pass@host:port/railway?schema=public&connection_limit=5"
```

## Schema Patterns

### Base Schema

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

### Model Conventions

**Singular model names**, PascalCase. Fields use camelCase. Database columns use snake_case via `@map`.

```prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String
  role      Role     @default(MEMBER)
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  sessions Session[]
  posts    Post[]

  @@map("user")
}
```

### Timestamps

Every model gets `createdAt` and `updatedAt`:

```prisma
createdAt DateTime @default(now()) @map("created_at")
updatedAt DateTime @updatedAt @map("updated_at")
```

### Enums

```prisma
enum Role {
  ADMIN
  MEMBER
  GUEST
}

enum Status {
  DRAFT
  PUBLISHED
  ARCHIVED
}
```

### Relations

**One-to-Many:**

```prisma
model User {
  id       String    @id @default(uuid())
  posts    Post[]

  @@map("user")
}

model Post {
  id       String   @id @default(uuid())
  title    String
  userId   String   @map("user_id")
  user     User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@map("post")
}
```

**Many-to-Many (explicit join table):**

```prisma
model Post {
  id    String     @id @default(uuid())
  tags  PostTag[]

  @@map("post")
}

model Tag {
  id    String     @id @default(uuid())
  name  String     @unique
  posts PostTag[]

  @@map("tag")
}

model PostTag {
  postId String @map("post_id")
  tagId  String @map("tag_id")
  post   Post   @relation(fields: [postId], references: [id], onDelete: Cascade)
  tag    Tag    @relation(fields: [tagId], references: [id], onDelete: Cascade)

  @@id([postId, tagId])
  @@map("post_tag")
}
```

### Indexes

```prisma
model User {
  id    String @id @default(uuid())
  email String @unique
  name  String

  @@index([name])
  @@map("user")
}
```

### PostgreSQL-Specific Types

```prisma
model Product {
  id       String   @id @default(uuid())
  metadata Json?
  tags     String[]
  price    Decimal  @db.Decimal(10, 2)

  @@map("product")
}
```

## Migration Workflow

### Development

```bash
# Create migration from schema changes
npx prisma migrate dev --name add_user_table

# Apply without creating (schema push for prototyping)
npx prisma db push

# Reset database (drops all data)
npx prisma migrate reset

# Check migration status
npx prisma migrate status
```

### Production (Railway)

```bash
# Deploy pending migrations (non-interactive, no data loss prompts)
npx prisma migrate deploy
```

### Key Rules

1. **Never edit existing migrations** — they may have run in production
2. **Always review generated SQL** before committing
3. **Use `migrate dev` locally**, `migrate deploy` in CI/production
4. **Commit the `migrations/` directory** — it's your migration history
5. **Use `db push` only for prototyping** — no migration history

## Client Usage

### Generate Client

```bash
npx prisma generate
```

Run after every schema change. The build command should include this.

### Basic CRUD

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Create
const user = await prisma.user.create({
  data: { email: 'user@example.com', name: 'John' },
});

// Read one
const found = await prisma.user.findUnique({
  where: { email: 'user@example.com' },
});

// Read many with filter
const users = await prisma.user.findMany({
  where: { role: 'MEMBER' },
  orderBy: { createdAt: 'desc' },
  take: 10,
});

// Update
await prisma.user.update({
  where: { id: user.id },
  data: { name: 'Jane' },
});

// Delete
await prisma.user.delete({ where: { id: user.id } });
```

### Relations

```typescript
// Include relations
const userWithPosts = await prisma.user.findUnique({
  where: { id: userId },
  include: { posts: true, sessions: true },
});

// Nested create
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    name: 'John',
    posts: {
      create: [
        { title: 'First Post' },
        { title: 'Second Post' },
      ],
    },
  },
  include: { posts: true },
});

// Select specific fields
const emails = await prisma.user.findMany({
  select: { id: true, email: true },
});
```

### Transactions

```typescript
const [user, post] = await prisma.$transaction([
  prisma.user.create({ data: { email: 'a@b.com', name: 'A' } }),
  prisma.post.create({ data: { title: 'Hello', userId: 'known-id' } }),
]);

// Interactive transaction
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({
    data: { email: 'a@b.com', name: 'A' },
  });
  await tx.post.create({
    data: { title: 'Hello', userId: user.id },
  });
});
```

## Seeding

### seed.ts

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  await prisma.user.upsert({
    where: { email: 'admin@example.com' },
    update: {},
    create: {
      email: 'admin@example.com',
      name: 'Admin',
      role: 'ADMIN',
    },
  });

  console.log('Seed complete');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
```

### package.json config

```json
{
  "prisma": {
    "seed": "tsx prisma/seed.ts"
  }
}
```

### Run seed

```bash
npx prisma db seed
```

Seed runs automatically after `prisma migrate reset`.

## Railway Deployment

### Connection String

Railway Postgres provides `DATABASE_URL` automatically when the backend service references the Postgres service. Append connection pooling for production:

```
DATABASE_URL="postgresql://user:pass@host:port/railway?schema=public&connection_limit=5"
```

### Build Command

```bash
npx prisma generate && npx prisma migrate deploy && npm run build
```

This sequence:
1. Generates the Prisma client
2. Applies any pending migrations
3. Builds the application

### railway.toml

```toml
[build]
builder = "nixpacks"
buildCommand = "npx prisma generate && npx prisma migrate deploy && npm run build"

[deploy]
startCommand = "node dist/main.js"
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

## Prisma Studio

```bash
npx prisma studio
```

Opens a browser-based GUI for viewing and editing data at `http://localhost:5555`.

## Package Scripts

```json
{
  "scripts": {
    "db:generate": "prisma generate",
    "db:migrate": "prisma migrate dev",
    "db:migrate:deploy": "prisma migrate deploy",
    "db:push": "prisma db push",
    "db:reset": "prisma migrate reset",
    "db:seed": "prisma db seed",
    "db:studio": "prisma studio"
  }
}
```

## Troubleshooting

### "Can't reach database server"

Check `DATABASE_URL` is set and Postgres is running:
```bash
echo $DATABASE_URL
docker compose ps  # if using Docker locally
```

### "Migration failed"

Check migration status and logs:
```bash
npx prisma migrate status
npx prisma migrate resolve --rolled-back <migration-name>
```

### "Prisma Client not generated"

Run generate after schema changes:
```bash
npx prisma generate
```

### Connection pool exhaustion on Railway

Append `&connection_limit=5` to `DATABASE_URL`. Railway instances have limited connections.

### Type errors after schema change

Regenerate client and restart TypeScript server:
```bash
npx prisma generate
# Restart TS server in IDE: Cmd+Shift+P → "TypeScript: Restart TS Server"
```
