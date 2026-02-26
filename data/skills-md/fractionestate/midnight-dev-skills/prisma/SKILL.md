---
name: prisma
description: >-
  Type-safe database access with Prisma ORM for Node.js and TypeScript. Use when designing schemas,
  writing queries, running migrations, or optimizing database operations. Triggers on Prisma,
  database, ORM, migration, or SQL questions.
---

# Prisma ORM

Prisma is a next-generation ORM for Node.js and TypeScript. It provides type-safe database access,
auto-generated migrations, and an intuitive data modeling language.

## Core Concepts

### Schema Definition (schema.prisma)

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  password  String
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
}

model Profile {
  id     String @id @default(cuid())
  bio    String?
  avatar String?
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
  userId String @unique
}

model Post {
  id        String     @id @default(cuid())
  title     String
  content   String?
  published Boolean    @default(false)
  author    User       @relation(fields: [authorId], references: [id])
  authorId  String
  tags      Tag[]
  comments  Comment[]
  createdAt DateTime   @default(now())
  updatedAt DateTime   @updatedAt

  @@index([authorId])
  @@index([published, createdAt])
}

model Tag {
  id    String @id @default(cuid())
  name  String @unique
  posts Post[]
}

model Comment {
  id        String   @id @default(cuid())
  content   String
  post      Post     @relation(fields: [postId], references: [id], onDelete: Cascade)
  postId    String
  createdAt DateTime @default(now())
}

enum Role {
  USER
  ADMIN
  MODERATOR
}
```

## Client Setup

### Singleton Pattern (Next.js)

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
  });

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
```

### With Extensions

```typescript
const prisma = new PrismaClient().$extends({
  result: {
    user: {
      fullName: {
        needs: { firstName: true, lastName: true },
        compute(user) {
          return `${user.firstName} ${user.lastName}`;
        },
      },
    },
  },
});
```

## CRUD Operations

### Create

```typescript
// Single record
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    name: 'John Doe',
    profile: {
      create: { bio: 'Developer' },
    },
  },
  include: { profile: true },
});

// Multiple records
const users = await prisma.user.createMany({
  data: [
    { email: 'user1@example.com', name: 'User 1' },
    { email: 'user2@example.com', name: 'User 2' },
  ],
  skipDuplicates: true,
});

// With nested creation
const post = await prisma.post.create({
  data: {
    title: 'Hello World',
    author: { connect: { id: userId } },
    tags: {
      connectOrCreate: [
        { where: { name: 'tech' }, create: { name: 'tech' } },
        { where: { name: 'news' }, create: { name: 'news' } },
      ],
    },
  },
});
```

### Read

```typescript
// Find unique
const user = await prisma.user.findUnique({
  where: { email: 'user@example.com' },
  include: { posts: true },
});

// Find many with filtering
const posts = await prisma.post.findMany({
  where: {
    published: true,
    author: { email: { contains: '@example.com' } },
    OR: [{ title: { contains: 'prisma' } }, { content: { contains: 'prisma' } }],
  },
  orderBy: { createdAt: 'desc' },
  take: 10,
  skip: 0,
  select: {
    id: true,
    title: true,
    author: { select: { name: true } },
  },
});

// Pagination
const [posts, total] = await Promise.all([
  prisma.post.findMany({
    take: 10,
    skip: (page - 1) * 10,
    orderBy: { createdAt: 'desc' },
  }),
  prisma.post.count(),
]);
```

### Update

```typescript
// Single update
const user = await prisma.user.update({
  where: { id: userId },
  data: { name: 'Updated Name' },
});

// Update or create (upsert)
const user = await prisma.user.upsert({
  where: { email: 'user@example.com' },
  update: { name: 'Updated' },
  create: { email: 'user@example.com', name: 'New User' },
});

// Update many
const result = await prisma.post.updateMany({
  where: { authorId: userId },
  data: { published: false },
});

// Atomic operations
const post = await prisma.post.update({
  where: { id: postId },
  data: {
    views: { increment: 1 },
    likes: { decrement: 1 },
  },
});
```

### Delete

```typescript
// Single delete
await prisma.user.delete({
  where: { id: userId },
});

// Delete many
await prisma.post.deleteMany({
  where: {
    published: false,
    createdAt: { lt: new Date('2024-01-01') },
  },
});
```

## Transactions

### Sequential Operations

```typescript
const [posts, totalPosts, users] = await prisma.$transaction([
  prisma.post.findMany({ where: { published: true } }),
  prisma.post.count({ where: { published: true } }),
  prisma.user.findMany(),
]);
```

### Interactive Transactions

```typescript
const result = await prisma.$transaction(
  async (tx) => {
    // Decrement sender balance
    const sender = await tx.account.update({
      where: { id: senderId },
      data: { balance: { decrement: amount } },
    });

    if (sender.balance < 0) {
      throw new Error('Insufficient funds');
    }

    // Increment receiver balance
    const receiver = await tx.account.update({
      where: { id: receiverId },
      data: { balance: { increment: amount } },
    });

    return { sender, receiver };
  },
  {
    maxWait: 5000,
    timeout: 10000,
  }
);
```

## Relations

### One-to-One

```prisma
model User {
  id      String   @id
  profile Profile?
}

model Profile {
  id     String @id
  user   User   @relation(fields: [userId], references: [id])
  userId String @unique
}
```

### One-to-Many

```prisma
model User {
  id    String @id
  posts Post[]
}

model Post {
  id       String @id
  author   User   @relation(fields: [authorId], references: [id])
  authorId String
}
```

### Many-to-Many

```prisma
model Post {
  id   String @id
  tags Tag[]
}

model Tag {
  id    String @id
  posts Post[]
}
```

## Migrations

```bash
# Create migration
npx prisma migrate dev --name init

# Apply migrations (production)
npx prisma migrate deploy

# Reset database
npx prisma migrate reset

# Generate client
npx prisma generate

# Open Prisma Studio
npx prisma studio
```

## Best Practices

1. **Use cuid() or uuid()** for IDs instead of autoincrement
2. **Always include indexes** for frequently queried fields
3. **Use select/include** to avoid over-fetching
4. **Singleton pattern** in Next.js to prevent connection exhaustion
5. **Interactive transactions** for complex operations
6. **Soft deletes** with `deletedAt` field for important data

## References

- [references/schema.md](references/schema.md) - Schema patterns
- [references/query-patterns.md](references/query-patterns.md) - Advanced queries
- [references/migrations.md](references/migrations.md) - Migration strategies
