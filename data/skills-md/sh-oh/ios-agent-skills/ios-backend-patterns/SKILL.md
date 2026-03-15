---
name: ios-backend-patterns
description: Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes.
license: MIT
metadata:
  author: OkminLee
  version: "2.0.0"
---

# Backend Development Patterns

Backend architecture patterns and best practices for scalable server-side applications using Node.js, Express, and Next.js API routes.

## When to Apply

Use these patterns when:
- Building REST APIs with Express or Next.js API routes
- Designing data access layers (Repository, Service patterns)
- Implementing authentication, authorization, or rate limiting
- Optimizing database queries (N+1 prevention, caching)
- Adding error handling, retries, logging, or background jobs
- Reviewing backend code for architectural consistency

## Quick Reference

| Pattern | Purpose | Reference |
|---------|---------|-----------|
| RESTful API | Resource-based URL design | [api-design.md](references/api-design.md) |
| Repository | Abstract data access logic | [api-design.md](references/api-design.md) |
| Service Layer | Separate business logic from data access | [api-design.md](references/api-design.md) |
| Middleware | Request/response processing pipeline | [api-design.md](references/api-design.md) |
| JWT Auth | Token-based authentication | [api-design.md](references/api-design.md) |
| RBAC | Role-based access control | [api-design.md](references/api-design.md) |
| Rate Limiting | Throttle requests per client | [api-design.md](references/api-design.md) |
| Query Optimization | Select only needed columns | [database-patterns.md](references/database-patterns.md) |
| N+1 Prevention | Batch fetch related data | [database-patterns.md](references/database-patterns.md) |
| Transactions | Atomic multi-table writes | [database-patterns.md](references/database-patterns.md) |
| Redis Caching | Cache-aside with TTL | [database-patterns.md](references/database-patterns.md) |
| Error Handling | Centralized error classes | [database-patterns.md](references/database-patterns.md) |
| Retry with Backoff | Resilient external calls | [database-patterns.md](references/database-patterns.md) |
| Background Jobs | Non-blocking async processing | [database-patterns.md](references/database-patterns.md) |
| Structured Logging | JSON logs with context | [database-patterns.md](references/database-patterns.md) |

## Key Patterns

### RESTful API Structure

```typescript
// Resource-based URLs with standard HTTP methods
GET    /api/markets                 // List resources
GET    /api/markets/:id             // Get single resource
POST   /api/markets                 // Create resource
PUT    /api/markets/:id             // Replace resource
PATCH  /api/markets/:id             // Update resource
DELETE /api/markets/:id             // Delete resource

// Query parameters for filtering, sorting, pagination
GET /api/markets?status=active&sort=volume&limit=20&offset=0
```

### Repository Pattern

```typescript
// Abstract data access behind an interface
interface MarketRepository {
  findAll(filters?: MarketFilters): Promise<Market[]>
  findById(id: string): Promise<Market | null>
  create(data: CreateMarketDto): Promise<Market>
  update(id: string, data: UpdateMarketDto): Promise<Market>
  delete(id: string): Promise<void>
}

class SupabaseMarketRepository implements MarketRepository {
  async findAll(filters?: MarketFilters): Promise<Market[]> {
    let query = supabase.from('markets').select('*')
    if (filters?.status) query = query.eq('status', filters.status)
    if (filters?.limit) query = query.limit(filters.limit)
    const { data, error } = await query
    if (error) throw new Error(error.message)
    return data
  }
}
```

### Service Layer Pattern

```typescript
// Business logic separated from data access
class MarketService {
  constructor(private marketRepo: MarketRepository) {}

  async searchMarkets(query: string, limit = 10): Promise<Market[]> {
    const embedding = await generateEmbedding(query)
    const results = await this.vectorSearch(embedding, limit)
    const markets = await this.marketRepo.findByIds(results.map(r => r.id))
    return markets.sort((a, b) => {
      const scoreA = results.find(r => r.id === a.id)?.score || 0
      const scoreB = results.find(r => r.id === b.id)?.score || 0
      return scoreA - scoreB
    })
  }
}
```

### Middleware Pattern

```typescript
// Request/response processing pipeline (Next.js)
export function withAuth(handler: NextApiHandler): NextApiHandler {
  return async (req, res) => {
    const token = req.headers.authorization?.replace('Bearer ', '')
    if (!token) return res.status(401).json({ error: 'Unauthorized' })
    try {
      req.user = await verifyToken(token)
      return handler(req, res)
    } catch {
      return res.status(401).json({ error: 'Invalid token' })
    }
  }
}

// Usage
export default withAuth(async (req, res) => {
  // Handler has access to req.user
})
```

### Centralized Error Handling

```typescript
class ApiError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public isOperational = true
  ) {
    super(message)
  }
}

export function errorHandler(error: unknown, req: Request): Response {
  if (error instanceof ApiError) {
    return NextResponse.json(
      { success: false, error: error.message },
      { status: error.statusCode }
    )
  }
  if (error instanceof z.ZodError) {
    return NextResponse.json(
      { success: false, error: 'Validation failed', details: error.errors },
      { status: 400 }
    )
  }
  console.error('Unexpected error:', error)
  return NextResponse.json(
    { success: false, error: 'Internal server error' },
    { status: 500 }
  )
}
```

### Cache-Aside Pattern

```typescript
async function getMarketWithCache(id: string): Promise<Market> {
  const cached = await redis.get(`market:${id}`)
  if (cached) return JSON.parse(cached)

  const market = await db.markets.findUnique({ where: { id } })
  if (!market) throw new Error('Market not found')

  await redis.setex(`market:${id}`, 300, JSON.stringify(market))
  return market
}
```

## Common Mistakes

### 1. No Data Access Abstraction

Calling the database directly from route handlers. Use the Repository pattern to keep data access testable and swappable.

### 2. N+1 Queries

Fetching related records in a loop instead of batch-fetching. Always collect IDs first and query once with an `IN` clause.

### 3. Missing Error Classification

Catching all errors with a generic 500 response. Use typed error classes (`ApiError`, `ZodError`) so clients receive accurate status codes.

### 4. No Rate Limiting on Public Endpoints

Exposing APIs without throttling invites abuse. Apply rate limiting at minimum on authentication and write endpoints.

### 5. Blocking the Request with Heavy Work

Running expensive operations (indexing, email, image processing) synchronously in the request handler. Use a job queue to process work in the background.

---

> See the [references/](references/) directory for full implementations of every pattern listed above.
