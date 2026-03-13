---
name: prisma
description: Database management with Prisma ORM including schema modeling, migrations, and query optimization. Use when working with database schemas, managing data models, running migrations, or optimizing database queries.
license: MIT
metadata:
  author: devrecruit
  version: "1.0"
compatibility: Prisma 5.0+, supports PostgreSQL, MySQL, SQLite, MongoDB
---

# Prisma Skills

This skill covers best practices for using Prisma ORM effectively, including schema design, migrations, and query optimization.

## Database Migrations

### Purpose

Safely manage database schema changes with reproducible migrations.

### Migration Workflow

1. **Modify Schema**

   - Update `prisma/schema.prisma` with new models or fields
   - Use descriptive names following conventions
   - Add comments for complex relationships

2. **Create Migration**

   ```bash
   pnpm prisma migrate dev --name add_feature_name
   ```

   - Creates a new migration file automatically
   - Applies migration to development database
   - Regenerates Prisma Client

3. **Review Migration**

   - Check generated SQL in `prisma/migrations/<timestamp>_<name>/migration.sql`
   - Verify indexes and constraints are appropriate
   - Check for data loss risks if modifying existing fields

4. **Push to Production**
   ```bash
   pnpm prisma migrate deploy
   ```
   - Applies all pending migrations
   - Use in CI/CD pipelines before deployment
   - Always back up production database first

### Common Patterns

```prisma
// Adding a new model
model Quiz {
  id        String   @id @default(cuid())
  title     String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

// Adding a relationship
model Question {
  id    String @id @default(cuid())
  quiz  Quiz   @relation(fields: [quizId], references: [id], onDelete: Cascade)
  quizId String
}

// Adding a unique constraint
model User {
  id    String @id @default(cuid())
  email String @unique
  name  String
}

// Adding an index for query performance
model Interview {
  id        String   @id @default(cuid())
  candidateId String
  createdAt DateTime @default(now())

  @@index([candidateId])
  @@index([createdAt])
}
```

### Rollback Strategies

- **Never delete migrations** - they form the audit trail
- Create a new migration to undo changes if needed
- Test migrations locally before deploying
- Keep migration files small and focused

## Data Modeling

### Purpose

Design effective database schemas that support application requirements efficiently.

### Schema Design Principles

1. **Naming Conventions**

   - Use PascalCase for model names
   - Use camelCase for field names
   - Use clear, descriptive names
   - Avoid abbreviations unless standard

2. **Relationships**

   ```prisma
   // One-to-Many
   model User {
     id String @id @default(cuid())
     interviews Interview[]
   }

   model Interview {
     id String @id @default(cuid())
     user User @relation(fields: [userId], references: [id])
     userId String
   }

   // Many-to-Many (with join table)
   model Quiz {
     id String @id @default(cuid())
     questions QuizQuestion[]
   }

   model Question {
     id String @id @default(cuid())
     quizzes QuizQuestion[]
   }

   model QuizQuestion {
     id String @id @default(cuid())
     quiz Quiz @relation(fields: [quizId], references: [id], onDelete: Cascade)
     quizId String
     question Question @relation(fields: [questionId], references: [id], onDelete: Cascade)
     questionId String
     order Int

     @@unique([quizId, questionId])
   }
   ```

3. **Field Types**

   - Use appropriate types (String, Int, Boolean, DateTime, Json)
   - Use `@db.Text` for large text fields
   - Use `Json` type for flexible data structures
   - Consider enum types for fixed values

4. **Timestamps and Metadata**
   ```prisma
   model Entity {
     id String @id @default(cuid())
     createdAt DateTime @default(now())
     updatedAt DateTime @updatedAt
     createdBy String?
   }
   ```

### Indexes and Performance

```prisma
model Candidate {
  id String @id @default(cuid())
  email String @unique
  name String
  createdAt DateTime @default(now())

  // Single field index
  @@index([email])

  // Composite index for common queries
  @@index([createdAt, id])

  // Full-text search index (PostgreSQL)
  @@fulltext([name])
}
```

## Query Optimization

### Purpose

Write efficient database queries that minimize load and improve application performance.

### Query Patterns

1. **Use select() to Fetch Only Needed Fields**

   ```typescript
   // Bad - fetches all fields
   const user = await prisma.user.findUnique({
     where: { id: "user-1" },
   });

   // Good - fetch only needed fields
   const user = await prisma.user.findUnique({
     where: { id: "user-1" },
     select: {
       id: true,
       email: true,
       name: true,
     },
   });
   ```

2. **Batch Queries Efficiently**

   ```typescript
   // Avoid N+1 queries
   const users = await prisma.user.findMany();
   for (const user of users) {
     const interviews = await prisma.interview.findMany({
       where: { userId: user.id },
     }); // N+1 problem!
   }

   // Solution - use include or nested queries
   const users = await prisma.user.findMany({
     include: {
       interviews: true,
     },
   });
   ```

3. **Use Relations with include() or select()**

   ```typescript
   const quiz = await prisma.quiz.findUnique({
     where: { id: "quiz-1" },
     include: {
       quizQuestions: {
         include: {
           question: true,
         },
         orderBy: { order: "asc" },
       },
     },
   });
   ```

4. **Pagination for Large Result Sets**

   ```typescript
   const quizzes = await prisma.quiz.findMany({
     skip: (page - 1) * pageSize,
     take: pageSize,
     orderBy: { createdAt: "desc" },
   });
   ```

5. **Aggregations**

   ```typescript
   const stats = await prisma.interview.aggregate({
     where: { candidateId: "candidate-1" },
     _count: true,
     _avg: { score: true },
   });
   ```

6. **Raw Queries for Complex Operations**
   ```typescript
   const results = await prisma.$queryRaw`
     SELECT u.*, COUNT(i.id) as interview_count
     FROM User u
     LEFT JOIN Interview i ON u.id = i.userId
     GROUP BY u.id
   `;
   ```

### Performance Tips

- Always use indexes on frequently queried fields
- Use `select()` instead of fetching entire records
- Implement pagination for large datasets
- Use `distinct()` to avoid duplicate results
- Consider denormalization for frequently accessed aggregations
- Monitor slow queries in production
- Use Prisma Studio to analyze query patterns

### Caching Strategies

Combine Prisma queries with cache components in server components, and use server actions for mutations:

```typescript
// Data fetching (in server component or cached function)
"use cache";
import { cacheLife, cacheTag } from "next/cache";

export async function getCachedQuiz(id: string) {
  cacheLife({ max: 3600 });
  cacheTag("quizzes");

  return await prisma.quiz.findUnique({
    where: { id },
    include: {
      quizQuestions: {
        include: { question: true },
        orderBy: { order: "asc" },
      },
    },
  });
}

// Mutations (in server action, NOT API route)
("use server");
import { updateTag } from "@/lib/utils/cache-utils";

export async function updateQuizAction(id: string, data: QuizInput) {
  const user = await requireUser();

  const quiz = await prisma.quiz.update({
    where: { id },
    data,
  });

  // Invalidate cache after mutation
  updateTag("quizzes");

  return { success: true, data: quiz };
}
```

## Development Checklist

When working with Prisma:

- [ ] Schema follows naming conventions
- [ ] Relationships are properly defined
- [ ] Indexes are added for query performance
- [ ] Timestamps (createdAt, updatedAt) are included
- [ ] Migrations are reviewed before deployment
- [ ] Queries use select() or include() appropriately
- [ ] N+1 query problems are avoided
- [ ] Pagination is implemented for large datasets
- [ ] Mutations are in server actions, not API routes
- [ ] Cache invalidation (updateTag) is called after mutations in server actions
