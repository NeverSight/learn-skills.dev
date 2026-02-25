---
name: backend-trpc-openapi
description: Generate OpenAPI/REST endpoints from tRPC routers. Use when you have a tRPC API but need to expose REST endpoints for third-party integrations, mobile apps, or public API documentation. Provides automatic Swagger UI and OpenAPI spec generation. Choose this when you want type-safe internal APIs (tRPC) with REST fallback for external consumers.
allowed-tools: Read, Edit, Write, Bash (*)
---

# tRPC + OpenAPI Integration

## Overview

Generate REST endpoints and OpenAPI documentation from your tRPC routers. Get the best of both worlds: type-safe internal API with tRPC, REST/Swagger for external consumers.

**Package**: `trpc-to-openapi` (active fork of archived `trpc-openapi`)  
**Requirements**: tRPC v11+, Zod

**Key Benefit**: Single source of truth — define once in tRPC, expose as both RPC and REST.

## When to Use This Skill

✅ **Use tRPC + OpenAPI when:**
- Internal apps use tRPC, but need REST for third parties
- Need Swagger/OpenAPI documentation
- Mobile apps (non-React Native) need REST endpoints
- Microservices with mixed languages need interop
- Public API requires REST standard

❌ **Skip OpenAPI layer when:**
- All clients are TypeScript (pure tRPC is better)
- Internal-only APIs
- No documentation requirements

---

## Quick Start

### Installation

```bash
# NOTE: trpc-openapi is ARCHIVED, use active fork
npm install trpc-to-openapi swagger-ui-express

npm install -D @types/swagger-ui-express
```

### Setup tRPC with OpenAPI Meta

```typescript
// src/server/trpc.ts
import { initTRPC } from '@trpc/server';
import { OpenApiMeta } from 'trpc-to-openapi';

const t = initTRPC
  .context<Context>()
  .meta<OpenApiMeta>()  // ← Enable OpenAPI metadata
  .create();

export const router = t.router;
export const publicProcedure = t.procedure;
```

---

## Define Procedures with OpenAPI Metadata

```typescript
// src/server/routers/user.ts
import { z } from 'zod';
import { router, publicProcedure, protectedProcedure } from '../trpc';

const UserSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  name: z.string(),
});

export const userRouter = router({
  // GET /api/users/{id}
  getById: publicProcedure
    .meta({
      openapi: {
        method: 'GET',
        path: '/users/{id}',
        tags: ['Users'],
        summary: 'Get user by ID',
        description: 'Retrieves a single user by their unique identifier',
      },
    })
    .input(z.object({ id: z.string() }))
    .output(UserSchema)
    .query(async ({ input, ctx }) => {
      return ctx.db.user.findUniqueOrThrow({ where: { id: input.id } });
    }),

  // GET /api/users?limit=10&cursor=xxx
  list: publicProcedure
    .meta({
      openapi: {
        method: 'GET',
        path: '/users',
        tags: ['Users'],
        summary: 'List users',
      },
    })
    .input(z.object({
      limit: z.number().min(1).max(100).default(10),
      cursor: z.string().optional(),
    }))
    .output(z.object({
      items: z.array(UserSchema),
      nextCursor: z.string().optional(),
    }))
    .query(async ({ input, ctx }) => {
      // pagination logic
    }),

  // POST /api/users (protected)
  create: protectedProcedure
    .meta({
      openapi: {
        method: 'POST',
        path: '/users',
        tags: ['Users'],
        summary: 'Create user',
        protect: true,  // ← Marks as requiring auth in docs
      },
    })
    .input(z.object({
      email: z.string().email(),
      name: z.string().min(2),
    }))
    .output(UserSchema)
    .mutation(async ({ input, ctx }) => {
      return ctx.db.user.create({ data: input });
    }),

  // PUT /api/users/{id}
  update: protectedProcedure
    .meta({
      openapi: {
        method: 'PUT',
        path: '/users/{id}',
        tags: ['Users'],
        protect: true,
      },
    })
    .input(z.object({
      id: z.string(),
      name: z.string().optional(),
      email: z.string().email().optional(),
    }))
    .output(UserSchema)
    .mutation(async ({ input, ctx }) => {
      const { id, ...data } = input;
      return ctx.db.user.update({ where: { id }, data });
    }),

  // DELETE /api/users/{id}
  delete: protectedProcedure
    .meta({
      openapi: {
        method: 'DELETE',
        path: '/users/{id}',
        tags: ['Users'],
        protect: true,
      },
    })
    .input(z.object({ id: z.string() }))
    .output(z.object({ success: z.boolean() }))
    .mutation(async ({ input, ctx }) => {
      await ctx.db.user.delete({ where: { id: input.id } });
      return { success: true };
    }),
});
```

---

## Generate OpenAPI Document

```typescript
// src/server/openapi.ts
import { generateOpenApiDocument } from 'trpc-to-openapi';
import { appRouter } from './routers/_app';

export const openApiDocument = generateOpenApiDocument(appRouter, {
  title: 'My API',
  version: '1.0.0',
  baseUrl: process.env.API_URL || 'http://localhost:3000/api',
  description: 'REST API documentation',
  securitySchemes: {
    bearerAuth: {
      type: 'http',
      scheme: 'bearer',
      bearerFormat: 'JWT',
    },
  },
});
```

---

## Serve REST Endpoints + Swagger UI

```typescript
// src/server/index.ts
import express from 'express';
import cors from 'cors';
import swaggerUi from 'swagger-ui-express';
import { createExpressMiddleware } from '@trpc/server/adapters/express';
import { createOpenApiExpressMiddleware } from 'trpc-to-openapi';
import { appRouter } from './routers/_app';
import { createContext } from './context';
import { openApiDocument } from './openapi';

const app = express();
app.use(cors());
app.use(express.json());

// tRPC endpoint (for TypeScript clients)
app.use('/trpc', createExpressMiddleware({
  router: appRouter,
  createContext,
}));

// REST/OpenAPI endpoints (for external clients)
app.use('/api', createOpenApiExpressMiddleware({
  router: appRouter,
  createContext,
}));

// Swagger UI documentation
app.use('/docs', swaggerUi.serve, swaggerUi.setup(openApiDocument));

// OpenAPI JSON spec
app.get('/openapi.json', (req, res) => {
  res.json(openApiDocument);
});

app.listen(3000, () => {
  console.log('Server: http://localhost:3000');
  console.log('tRPC: http://localhost:3000/trpc');
  console.log('REST: http://localhost:3000/api');
  console.log('Docs: http://localhost:3000/docs');
});
```

---

## URL Parameter Mapping

```typescript
// Path parameters use {param} syntax
.meta({
  openapi: {
    method: 'GET',
    path: '/users/{id}/posts/{postId}',
  },
})
.input(z.object({
  id: z.string(),       // ← Maps to {id}
  postId: z.string(),   // ← Maps to {postId}
}))

// Query parameters are auto-mapped for GET
.meta({
  openapi: {
    method: 'GET',
    path: '/users',
  },
})
.input(z.object({
  limit: z.number(),   // ← ?limit=10
  search: z.string(),  // ← &search=foo
}))
```

---

## When to Expose OpenAPI

| Scenario | Recommendation |
|----------|---------------|
| Internal TypeScript clients | Pure tRPC |
| Third-party integrations | tRPC + OpenAPI |
| Public API documentation | tRPC + OpenAPI |
| Mobile apps (non-React Native) | tRPC + OpenAPI |
| Microservices (mixed languages) | OpenAPI |

---

## Rules

### Do ✅

- Add `.output()` schema for OpenAPI response types
- Use descriptive `summary` and `description`
- Group related endpoints with `tags`
- Mark protected routes with `protect: true`
- Use path parameters for resource identifiers

### Avoid ❌

- Exposing all procedures (only add meta to public ones)
- Missing output schemas (breaks OpenAPI generation)
- Inconsistent path naming conventions
- Skipping authentication markers

---

## OpenAPI Metadata Reference

```typescript
.meta({
  openapi: {
    method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE',
    path: '/resource/{id}',
    tags: ['Category'],
    summary: 'Short description',
    description: 'Detailed description',
    protect: boolean,           // Requires auth
    deprecated: boolean,        // Mark as deprecated
    requestHeaders: z.object(), // Custom headers
    responseHeaders: z.object(),
    contentTypes: ['application/json'],
  },
})
```

---

## Troubleshooting

```yaml
"OpenAPI generation fails":
  → Ensure all procedures with meta have .output()
  → Check Zod schemas are serializable
  → Verify path parameters match input schema

"REST endpoint returns 404":
  → Check path matches exactly (case-sensitive)
  → Verify HTTP method matches
  → Ensure createOpenApiExpressMiddleware is mounted

"Auth not working on REST":
  → Check Authorization header format
  → Verify createContext extracts token
  → Match auth middleware with tRPC setup

"Swagger UI empty":
  → Check openApiDocument is generated
  → Verify /openapi.json returns valid spec
  → Check console for generation errors
```

---

## File Structure

```
src/server/
├── trpc.ts           # tRPC with OpenApiMeta
├── openapi.ts        # OpenAPI document generation
├── context.ts        # Shared context
├── index.ts          # Express server
└── routers/
    ├── _app.ts       # Root router
    └── user.ts       # Procedures with openapi meta
```

## References

- https://github.com/mcampa/trpc-to-openapi — Active fork documentation
- https://swagger.io/specification/ — OpenAPI spec
- https://swagger.io/tools/swagger-ui/ — Swagger UI
