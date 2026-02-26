---
name: orpc-implementation-sops
description: 'Use when building, updating, or refactoring oRPC contracts, server handlers, clients, or React Query integration'
---

# oRPC Implementation SOPs

You are an expert TypeScript backend and frontend engineer. When implementing oRPC, you MUST strictly follow this Contract-First development pattern and the guardrails below.

## 1. Contract Definition (API First)

**CRITICAL RULE:** API paths and resource names MUST ALWAYS use **singular form** (e.g., `/api/user`, NEVER `/api/users`). Nested contract keys MUST also be singular (e.g., `user: UserContract`, NEVER `users: UserContract`).

```typescript
import { oc, type } from '@orpc/contract';
import { z } from 'zod';
import { ResourceSchema, ListQueryInputSchema, createListResponse } from 'common/contract';

// MUST define Entity Schema FIRST
export const UserSchema = ResourceSchema.extend({
  name: z.string().describe('用户名'),
  email: z.string().email().describe('邮箱'),
});

// Then define Contract
export const UserContract = {
  list: oc
    .input(ListQueryInputSchema)
    .output(createListResponse(UserSchema))
    .route({ method: 'GET', path: '/api/user' }),

  get: oc
    .input(type<{}>())
    .output(UserSchema)
    .route({ method: 'GET', path: '/api/user/:id' }),

  create: oc
    .input(z.object({ name: z.string(), email: z.string().email() }))
    .output(UserSchema)
    .route({ method: 'POST', path: '/api/user' }),
};

// Nested Contract — singular keys
export const AppContract = {
  user: UserContract,
  health: oc.output(z.object({ ok: z.boolean() })).route({ method: 'GET', path: '/health' }),
};
```

## 2. Server Implementation

Errors MUST be thrown using `ORPCError` with standard codes.

```typescript
import { implement, ORPCError } from '@orpc/server';
import { handleRPCContract } from 'common/orpc/server';

export function createUserContractImpl() {
  const os = implement(UserContract);
  return {
    list: os.list.handler(async ({ input }) => {
      const data = await db.user.findMany({ take: input.limit ?? 20 });
      return { total: data.length, data };
    }),
    get: os.get.handler(async ({ input }) => {
      const user = await db.user.findUnique({ where: { id: input.id } });
      if (!user) throw new ORPCError('NOT_FOUND', { message: 'User not found' });
      return user;
    }),
  };
}
```

## 3. Client & React Query Integration

```typescript
import { createRpcContractClient } from 'common/orpc';
import { createORPCReactQueryUtils } from '@orpc/react-query';

const client = createRpcContractClient<typeof AppContract>({
  baseUrl: 'http://localhost:3000',
  getApiKey: () => getAccessToken(),
});

export const orpc = createORPCReactQueryUtils(client);

// Usage in React Component
const { data } = useQuery(orpc.user.list.queryOptions({ input: { limit: 20 } }));
```

## 4. Schema & Error Handling Constraints

When generating or modifying Zod schemas and errors, you MUST adhere to these rules:

- **Documentation:** MUST append `.describe('...')` to string fields for frontend tooltip generation.
- **Dates:** MUST use `z.coerce.date()` to handle automatic type coercion from strings.
- **Optionality:** MUST use `.nullish()` over `.optional()` or `.nullable()` for broader compatibility unless strictly specified.
- **Bypassing Validation:** Use `oc.output(type<ComplexType>())` only when standard Zod validation is too heavy.
- **File Uploads:** MUST use `z.instanceof(File)` for Blob/File typing.
- **Type Export:** MUST export inferred types: `export type User = z.infer<typeof UserSchema>;`
- **Error Codes:** MUST use standard HTTP-mapped codes only: `NOT_FOUND`, `BAD_REQUEST`, `UNAUTHORIZED`, `FORBIDDEN`, `CONFLICT`, `INTERNAL_SERVER_ERROR`.

## 5. Protocol Selection

| Feature  | RPC (`/api/rpc`) | OpenAPI (`/api`) |
|----------|------------------|------------------|
| Routing  | Single endpoint  | RESTful          |
| Batch    | Yes              | Yes              |
| OpenAPI  | No               | Yes              |
| Perf     | Higher           | Standard         |

**Rule:** Frontend uses RPC protocol. External/third-party API uses OpenAPI protocol.

## 6. Advanced Patterns

For complex operations such as modeling external REST APIs, Hono integration, File/Blob uploads, SSE/Streaming, or AsyncIterator conversion, DO NOT guess. You MUST read the detailed reference first: [references/orpc-pattern.md](references/orpc-pattern.md)
