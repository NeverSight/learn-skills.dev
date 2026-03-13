---
name: API Design
slug: api-design
description: Expert guide for RESTful API design, Next.js API routes, error handling, validation, and best practices. Use when building endpoints, handling requests, or designing API architecture.
category: backend
complexity: moderate
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "create API"
  - "design API"
  - "API routes"
  - "REST endpoints"
  - "API validation"
  - "API error handling"
  - "build endpoint"
  - "route handler"
tags:
  - api
  - rest
  - endpoints
  - validation
  - backend
  - routes
  - http
  - zod
---

# API Design & Integration Skill

Comprehensive guide for designing and implementing robust, scalable APIs in Next.js applications. From RESTful endpoint design to request validation, error handling, authentication, and rate limiting, this skill covers all aspects of production-ready API development.

Build APIs that are intuitive to use, well-documented, and follow industry best practices. Implement proper HTTP semantics, consistent error responses, and type-safe request/response handling.

## Core Workflows

### Workflow 1: RESTful Route Handlers
**Purpose:** Create well-organized API routes following REST conventions

**Steps:**
1. Plan resource-based URL structure
2. Create route handlers for each HTTP method
3. Implement request validation
4. Add proper error handling
5. Return consistent response format

**Implementation:**
```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    const users = await db.users.findMany()
    return NextResponse.json({ users })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch users' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const user = await db.users.create({ data: body })
    return NextResponse.json({ user }, { status: 201 })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create user' },
      { status: 400 }
    )
  }
}

// app/api/users/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await db.users.findUnique({ where: { id: params.id } })

  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    )
  }

  return NextResponse.json({ user })
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const body = await request.json()
  const user = await db.users.update({
    where: { id: params.id },
    data: body
  })

  return NextResponse.json({ user })
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  await db.users.delete({ where: { id: params.id } })
  return new NextResponse(null, { status: 204 })
}
```

### Workflow 2: Request Validation with Zod
**Purpose:** Type-safe request validation with detailed error messages

**Implementation:**
```typescript
import { z } from 'zod'
import { NextRequest, NextResponse } from 'next/server'

const userSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  age: z.number().int().min(18).optional()
})

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const validated = userSchema.parse(body)

    const user = await db.users.create({ data: validated })
    return NextResponse.json({ user }, { status: 201 })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', issues: error.issues },
        { status: 400 }
      )
    }
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

### Workflow 3: Authentication Middleware
**Purpose:** Secure API routes with authentication checks

**Implementation:**
```typescript
// lib/auth-middleware.ts
import { NextRequest, NextResponse } from 'next/server'

export async function withAuth(
  handler: (req: NextRequest, context: any) => Promise<NextResponse>
) {
  return async (req: NextRequest, context: any) => {
    const token = req.headers.get('authorization')?.replace('Bearer ', '')

    if (!token) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    try {
      const user = await verifyToken(token)
      req.user = user
      return handler(req, context)
    } catch (error) {
      return NextResponse.json(
        { error: 'Invalid token' },
        { status: 401 }
      )
    }
  }
}

// app/api/protected/route.ts
export const GET = withAuth(async (request: NextRequest) => {
  const user = request.user
  return NextResponse.json({ user })
})
```

### Workflow 4: Rate Limiting
**Purpose:** Protect API from abuse

**Implementation:**
```typescript
// lib/rate-limit.ts
const rateLimitMap = new Map<string, { count: number; reset: number }>()

export function rateLimit(limit = 100, window = 60000) {
  return async (request: NextRequest) => {
    const ip = request.ip || 'anonymous'
    const now = Date.now()
    const record = rateLimitMap.get(ip)

    if (!record || now > record.reset) {
      rateLimitMap.set(ip, { count: 1, reset: now + window })
      return null
    }

    if (record.count >= limit) {
      return NextResponse.json(
        { error: 'Too many requests' },
        { status: 429 }
      )
    }

    record.count++
    return null
  }
}

// Usage in route
export async function GET(request: NextRequest) {
  const limitResponse = await rateLimit(100, 60000)(request)
  if (limitResponse) return limitResponse

  // Handle request...
}
```

### Workflow 5: Pagination Pattern
**Purpose:** Handle large datasets efficiently

**Implementation:**
```typescript
type PaginatedResponse<T> = {
  data: T[]
  pagination: {
    page: number
    limit: number
    total: number
    totalPages: number
    hasNext: boolean
    hasPrev: boolean
  }
}

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const page = parseInt(searchParams.get('page') || '1')
  const limit = parseInt(searchParams.get('limit') || '10')
  const search = searchParams.get('search') || ''

  const skip = (page - 1) * limit

  const [users, total] = await Promise.all([
    db.users.findMany({
      where: { name: { contains: search } },
      skip,
      take: limit
    }),
    db.users.count({ where: { name: { contains: search } } })
  ])

  const totalPages = Math.ceil(total / limit)

  return NextResponse.json({
    data: users,
    pagination: {
      page,
      limit,
      total,
      totalPages,
      hasNext: page < totalPages,
      hasPrev: page > 1
    }
  })
}
```

## Quick Reference

| Action | HTTP Method | URL Pattern |
|--------|-------------|-------------|
| List resources | GET | /api/resources |
| Get single | GET | /api/resources/:id |
| Create | POST | /api/resources |
| Update | PATCH/PUT | /api/resources/:id |
| Delete | DELETE | /api/resources/:id |
| Actions | POST | /api/resources/:id/action |

## HTTP Status Codes

### Success Codes
- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST (resource created)
- `204 No Content` - Successful DELETE

### Client Error Codes
- `400 Bad Request` - Invalid request body/params
- `401 Unauthorized` - Missing/invalid authentication
- `403 Forbidden` - Authenticated but not authorized
- `404 Not Found` - Resource doesn't exist
- `409 Conflict` - Resource conflict (duplicate)
- `422 Unprocessable Entity` - Validation failed
- `429 Too Many Requests` - Rate limit exceeded

### Server Error Codes
- `500 Internal Server Error` - Unexpected error
- `503 Service Unavailable` - Temporary unavailability

## Error Response Format

```typescript
type ErrorResponse = {
  error: string              // Human-readable message
  code?: string             // Machine-readable code
  details?: Record<string, any>  // Additional context
  timestamp?: string
}

// Usage
return NextResponse.json(
  {
    error: 'Validation failed',
    code: 'VALIDATION_ERROR',
    details: { field: 'email', reason: 'Invalid format' },
    timestamp: new Date().toISOString()
  },
  { status: 400 }
)
```

## CORS Configuration

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const response = NextResponse.next()

  response.headers.set('Access-Control-Allow-Origin', '*')
  response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')

  if (request.method === 'OPTIONS') {
    return new NextResponse(null, { status: 200, headers: response.headers })
  }

  return response
}

export const config = {
  matcher: '/api/:path*'
}
```

## Best Practices

- **Use HTTP Semantics:** Correct status codes (201 for create, 204 for delete)
- **Consistent Response Format:** Always return `{ data }` or `{ error, code }`
- **Validate Everything:** Use Zod for request body, query, and params
- **Handle Errors Gracefully:** Never expose internal errors to clients
- **Document APIs:** Use OpenAPI/Swagger for documentation
- **Version APIs:** Use /api/v1/ for breaking changes
- **Paginate Lists:** Always paginate list endpoints
- **Use CORS:** Configure properly for client-side requests
- **Log Requests:** Log all API requests for debugging
- **Rate Limit:** Protect against abuse

## Common Patterns

### Health Check Endpoint
```typescript
// app/api/health/route.ts
export async function GET() {
  return NextResponse.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    version: process.env.APP_VERSION
  })
}
```

### File Upload
```typescript
export async function POST(request: NextRequest) {
  const formData = await request.formData()
  const file = formData.get('file') as File

  if (!file) {
    return NextResponse.json(
      { error: 'No file provided' },
      { status: 400 }
    )
  }

  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    return NextResponse.json(
      { error: 'Invalid file type' },
      { status: 400 }
    )
  }

  const url = await uploadFile(file)
  return NextResponse.json({ url }, { status: 201 })
}
```

### Webhook Handler
```typescript
export async function POST(request: NextRequest) {
  const signature = request.headers.get('x-webhook-signature')
  const body = await request.text()

  const isValid = verifyWebhookSignature(body, signature)
  if (!isValid) {
    return NextResponse.json(
      { error: 'Invalid signature' },
      { status: 401 }
    )
  }

  const event = JSON.parse(body)
  await processWebhookEvent(event)

  return NextResponse.json({ received: true })
}
```

## Dependencies

```bash
# Validation
npm install zod

# Rate limiting
npm install @upstash/redis @upstash/ratelimit

# API documentation
npm install swagger-ui-react swagger-jsdoc
```

## Error Handling

- **400 Bad Request:** Invalid input, validation errors
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Valid auth but insufficient permissions
- **404 Not Found:** Resource doesn't exist
- **409 Conflict:** Resource already exists or state conflict
- **422 Unprocessable:** Valid syntax but semantic errors
- **429 Too Many Requests:** Rate limit exceeded
- **500 Internal Error:** Server-side failures

## Performance Tips

- Use database indexes for query fields
- Implement cursor-based pagination for large datasets
- Cache frequent reads with Redis or SWR
- Use database connection pooling
- Minimize payload size with field selection
- Compress responses with gzip

## When to Use This Skill

Invoke this skill when:
- Creating new API endpoints
- Implementing request validation
- Designing API architecture
- Adding authentication/authorization
- Handling file uploads
- Implementing webhooks
- Setting up CORS
- Adding rate limiting
- Debugging API errors
- Optimizing API performance
