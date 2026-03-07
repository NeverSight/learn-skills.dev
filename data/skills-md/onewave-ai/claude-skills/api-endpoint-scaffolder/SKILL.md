---
name: api-endpoint-scaffolder
description: Generate REST API endpoints with proper structure, validation, error handling, and types. Use when creating new API routes, endpoints, or backend services.
---

# API Endpoint Scaffolder

## Instructions

When creating a new API endpoint:

1. **Identify the framework** (Express, Next.js, FastAPI, etc.)
2. **Determine HTTP method** (GET, POST, PUT, PATCH, DELETE)
3. **Define request/response types**
4. **Implement with best practices**

## Templates

### Next.js App Router (TypeScript)

```typescript
// app/api/[resource]/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

const RequestSchema = z.object({
  // Define your schema
});

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    // Implementation
    return NextResponse.json({ data }, { status: 200 });
  } catch (error) {
    console.error('[API] Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validated = RequestSchema.parse(body);
    // Implementation
    return NextResponse.json({ data }, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      );
    }
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

### Express (TypeScript)

```typescript
import { Router, Request, Response, NextFunction } from 'express';
import { z } from 'zod';

const router = Router();

const CreateSchema = z.object({
  // Define schema
});

router.post('/', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const data = CreateSchema.parse(req.body);
    // Implementation
    res.status(201).json({ success: true, data });
  } catch (error) {
    next(error);
  }
});

export default router;
```

## Best Practices

1. **Always validate input** using Zod, Yup, or similar
2. **Use proper HTTP status codes**:
   - 200: Success
   - 201: Created
   - 400: Bad Request
   - 401: Unauthorized
   - 403: Forbidden
   - 404: Not Found
   - 500: Server Error
3. **Log errors** but don't expose internals to clients
4. **Use consistent response format**
5. **Add rate limiting** for public endpoints
6. **Document with OpenAPI/Swagger** when possible
