---
name: prisma
description: |
  Prisma ORM — type-safe database toolkit for TypeScript/Node.js. Schema-first approach with Prisma Schema Language, auto-generated type-safe client, migrations via Prisma Migrate.
  Use when defining database models in schema.prisma, writing CRUD queries with Prisma Client, setting up relations (1-1, 1-n, m-n),
  running migrations (prisma migrate dev/deploy), configuring prisma.config.ts, using raw SQL/TypedSQL, creating client extensions,
  or working with PostgreSQL, MySQL, SQLite, SQL Server, MongoDB, CockroachDB.
---

# Prisma ORM

Schema-first, type-safe database toolkit. Auto-generated client from `schema.prisma`.

## Quick Start

### Install

```bash
npm install prisma --save-dev
npm install @prisma/client
npx prisma init
```

### Config

```ts
// prisma.config.ts
import "dotenv/config";
import { defineConfig, env } from "prisma/config";

export default defineConfig({
  schema: "./prisma/schema.prisma",
  migrations: { path: "prisma/migrations" },
  datasource: { url: env("DATABASE_URL") },
});
```

### Schema

```prisma
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
}

generator client {
  provider = "prisma-client"
  output   = "../src/generated/prisma"
}

model User {
  id        Int      @id @default(autoincrement())
  createdAt DateTime @default(now())
  email     String   @unique
  name      String?
  posts     Post[]
}

model Post {
  id       Int    @id @default(autoincrement())
  title    String
  author   User   @relation(fields: [authorId], references: [id])
  authorId Int
}
```

### Generate & Query

```bash
npx prisma migrate dev --name init
# or for prototyping: npx prisma db push
```

```ts
import { PrismaClient } from "./generated/prisma/client";
import { PrismaPg } from "@prisma/adapter-pg";

const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL! });
const prisma = new PrismaClient({ adapter });

// create
const user = await prisma.user.create({
  data: { email: "alice@prisma.io", name: "Alice" },
});

// read
const users = await prisma.user.findMany({
  where: { email: { endsWith: "@prisma.io" } },
});

// update
await prisma.user.update({
  where: { email: "alice@prisma.io" },
  data: { name: "Alice Updated" },
});

// delete
await prisma.user.delete({ where: { email: "alice@prisma.io" } });
```

See [references/connections.md](references/connections.md) for driver adapters (PostgreSQL, MySQL, SQL Server, edge runtimes) and singleton patterns.

## Schema

Models map to database tables. Fields map to columns.

```prisma
model User {
  id        Int      @id @default(autoincrement())
  createdAt DateTime @default(now())
  email     String   @unique
  name      String?            // optional (nullable)
  tags      String[]           // list (PostgreSQL/CockroachDB)
  role      Role     @default(USER)
}

enum Role {
  USER
  ADMIN
}
```

### Scalar Types

| Prisma     | PostgreSQL         | MySQL            | SQLite    |
| ---------- | ------------------ | ---------------- | --------- |
| `String`   | `text`             | `varchar(191)`   | `TEXT`    |
| `Boolean`  | `boolean`          | `tinyint(1)`     | `INTEGER` |
| `Int`      | `integer`          | `int`            | `INTEGER` |
| `BigInt`   | `bigint`           | `bigint`         | `INTEGER` |
| `Float`    | `double precision` | `double`         | `REAL`    |
| `Decimal`  | `decimal(65,30)`   | `decimal(65,30)` | `REAL`    |
| `DateTime` | `timestamp(3)`     | `datetime(3)`    | `NUMERIC` |
| `Json`     | `jsonb`            | `json`           | n/a       |
| `Bytes`    | `bytea`            | `longblob`       | n/a       |

### Key Attributes

```prisma
@id                          // primary key
@default(autoincrement())    // auto-increment
@default(now())              // current timestamp
@default(uuid())             // UUID v4
@default(cuid())             // CUID
@default(dbgenerated("...")) // native DB function
@unique                      // unique constraint
@updatedAt                   // auto-update timestamp
@map("column_name")          // custom column name
@db.VarChar(200)             // native type mapping
@relation(fields: [...], references: [...])

@@id([fieldA, fieldB])       // composite primary key
@@unique([fieldA, fieldB])   // composite unique
@@index([fieldA, fieldB])    // composite index
@@map("table_name")          // custom table name
```

Full schema reference: [references/schema.md](references/schema.md)

## Relations

### One-to-One

```prisma
model User {
  id      Int      @id @default(autoincrement())
  profile Profile?
}

model Profile {
  id     Int  @id @default(autoincrement())
  user   User @relation(fields: [userId], references: [id])
  userId Int  @unique
}
```

### One-to-Many

```prisma
model User {
  id    Int    @id @default(autoincrement())
  posts Post[]
}

model Post {
  id       Int  @id @default(autoincrement())
  author   User @relation(fields: [authorId], references: [id])
  authorId Int
}
```

### Many-to-Many (Implicit)

```prisma
model Post {
  id         Int        @id @default(autoincrement())
  categories Category[]
}

model Category {
  id    Int    @id @default(autoincrement())
  posts Post[]
}
```

Prisma manages the join table automatically. For extra fields on the relation, use explicit m-n with a join model.

### Referential Actions

```prisma
model Post {
  author   User @relation(fields: [authorId], references: [id], onDelete: Cascade)
  authorId Int
}
```

Actions: `Cascade`, `Restrict`, `NoAction`, `SetNull`, `SetDefault`.

Full relations reference: [references/relations.md](references/relations.md)

## CRUD Operations

### Read

```ts
// findUnique — by unique field
const user = await prisma.user.findUnique({ where: { email: "a@b.io" } });

// findFirst — first match
const user = await prisma.user.findFirst({
  where: { posts: { some: { likes: { gt: 100 } } } },
});

// findMany — all matching
const users = await prisma.user.findMany({
  where: { email: { endsWith: "@prisma.io" } },
  orderBy: { name: "asc" },
  skip: 10,
  take: 20,
});
```

### Write

```ts
// create
const user = await prisma.user.create({
  data: { email: "elsa@prisma.io", name: "Elsa" },
});

// createMany
await prisma.user.createMany({
  data: [{ email: "a@b.io" }, { email: "b@b.io" }],
  skipDuplicates: true,
});

// update
await prisma.user.update({
  where: { email: "viola@prisma.io" },
  data: { name: "Viola the Magnificent" },
});

// upsert
await prisma.user.upsert({
  where: { email: "viola@prisma.io" },
  update: { name: "Viola" },
  create: { email: "viola@prisma.io", name: "Viola" },
});

// delete
await prisma.user.delete({ where: { email: "bert@prisma.io" } });
```

### Select / Include / Omit

```ts
// select — return only specified fields
const user = await prisma.user.findFirst({
  select: { email: true, name: true },
});

// include — return all fields + relations
const user = await prisma.user.findFirst({
  include: { posts: true },
});

// omit — exclude specific fields
const user = await prisma.user.findFirst({ omit: { password: true } });
```

### Filtering

```ts
where: {
  email: { contains: "prisma", mode: "insensitive" },
  age: { gte: 18 },
  id: { in: [1, 2, 3] },
  OR: [{ name: { startsWith: "A" } }, { role: "ADMIN" }],
  posts: { some: { published: true } },  // relation filter
}
```

### Nested Writes

```ts
// create with nested child
await prisma.user.create({
  data: {
    email: "alice@prisma.io",
    posts: { create: [{ title: "Hello" }, { title: "World" }] },
  },
});

// connect to existing record
await prisma.post.create({
  data: {
    title: "New Post",
    author: { connect: { id: 1 } },
  },
});
```

Full queries reference: [references/queries.md](references/queries.md)

## Aggregation

```ts
const result = await prisma.user.aggregate({
  _avg: { age: true },
  _count: { _all: true },
  where: { role: "ADMIN" },
});

const groups = await prisma.user.groupBy({
  by: ["country"],
  _count: { country: true },
  having: { profileViews: { _avg: { gt: 100 } } },
});
```

## Transactions

### Sequential (array)

```ts
const [posts, count] = await prisma.$transaction([
  prisma.post.findMany({ where: { title: { contains: "prisma" } } }),
  prisma.post.count(),
]);
```

### Interactive

```ts
const result = await prisma.$transaction(async (tx) => {
  const sender = await tx.account.update({
    data: { balance: { decrement: 100 } },
    where: { email: "alice@prisma.io" },
  });
  if (sender.balance < 0) throw new Error("Insufficient funds");
  return tx.account.update({
    data: { balance: { increment: 100 } },
    where: { email: "bob@prisma.io" },
  });
});
```

## Raw SQL

```ts
// queryRaw — returns records (tagged template for SQL injection safety)
const users = await prisma.$queryRaw`SELECT * FROM "User" WHERE email = ${email}`;

// executeRaw — returns affected row count
const count = await prisma.$executeRaw`UPDATE "User" SET active = true WHERE "emailValidated" = true`;
```

TypedSQL: write `.sql` files in `prisma/sql/`, generate with `prisma generate --sql`, get fully type-safe query functions.

Full raw SQL reference: [references/raw-sql.md](references/raw-sql.md)

## Prisma Migrate

| Command | Env | Description |
|---------|-----|-------------|
| `prisma migrate dev` | dev | Generate + apply migrations |
| `prisma migrate dev --name <name>` | dev | Named migration |
| `prisma migrate dev --create-only` | dev | Generate without applying (for editing) |
| `prisma migrate deploy` | prod | Apply pending migrations only |
| `prisma migrate reset` | dev | Drop DB, reapply all, run seed |
| `prisma db push` | dev | Sync schema without migration files |
| `prisma db pull` | any | Introspect DB into Prisma schema |
| `prisma db seed` | any | Run seed command |

Full migrations reference: [references/migrations.md](references/migrations.md)

## Client Extensions

Extend Prisma Client with custom model methods, query hooks, computed fields, and client-level methods via `$extends`:

```ts
const prisma = new PrismaClient({ adapter }).$extends({
  model: {
    user: {
      async signUp(email: string) {
        return prisma.user.create({ data: { email } });
      },
    },
  },
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

Four component types: `model`, `client`, `query`, `result`.

Full extensions reference: [references/client-extensions.md](references/client-extensions.md)

## Type Safety

```ts
import { Prisma } from "./generated/prisma/client";

// Derive return type for a query shape
type UserWithPosts = Prisma.UserGetPayload<{ include: { posts: true } }>;

// Input types
const data: Prisma.UserCreateInput = { email: "alice@prisma.io" };

// Type-safe reusable fragments
const withPosts = { include: { posts: true } } satisfies Prisma.UserDefaultArgs;
type UserWithPosts2 = Prisma.UserGetPayload<typeof withPosts>;
```

Full type safety reference: [references/type-safety.md](references/type-safety.md)

## Error Handling

```ts
import { Prisma } from "./generated/prisma/client";

try {
  await prisma.user.create({ data: { email: "existing@mail.com" } });
} catch (e) {
  if (e instanceof Prisma.PrismaClientKnownRequestError) {
    if (e.code === "P2002") console.log("Unique constraint violated");
    if (e.code === "P2025") console.log("Record not found");
  }
}
```

## Reference Index

| Topic | File |
|-------|------|
| Full Prisma Schema Language, types, attributes, enums, views, multi-schema | [references/schema.md](references/schema.md) |
| All relation types, self-relations, referential actions, relation mode | [references/relations.md](references/relations.md) |
| Full CRUD, filters, nested reads/writes, aggregation, transactions, JSON, scalar lists | [references/queries.md](references/queries.md) |
| $extends API, model/client/query/result components, read replicas | [references/client-extensions.md](references/client-extensions.md) |
| Prisma Migrate, db push/pull, seeding, squashing, down migrations | [references/migrations.md](references/migrations.md) |
| $queryRaw, $executeRaw, TypedSQL, parameterized queries | [references/raw-sql.md](references/raw-sql.md) |
| Driver adapters, connection pools, singleton pattern, serverless, edge | [references/connections.md](references/connections.md) |
| Generated types, Prisma.validator, payload types, utility types | [references/type-safety.md](references/type-safety.md) |
| Logging, error handling, testing, deployment, best practices | [references/advanced-patterns.md](references/advanced-patterns.md) |
