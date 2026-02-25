---
name: server-action-builder
description: "Create Next.js Server Actions with Zod validation, auth, and service layer integration. Generates schema + service + action files."
metadata:
  version: 1.0.0
---

# Server Action Builder

You are an expert at creating type-safe server actions for a Next.js/Supabase application.

## Why This Skill Exists

The user's codebase has established patterns for server actions using manual authentication, Zod validation, and service layers. Deviating from these patterns causes real problems:

| Deviation | Harm to User |
|-----------|--------------|
| Raw async functions without auth check | No authentication — unauthenticated data reaches the database, creating security vulnerabilities |
| Missing Zod schema | Invalid data reaches database, causing crashes or data corruption that is expensive to debug |
| Business logic in action (no service layer) | Untestable code that cannot be reused from MCP tools, CLI, or other interfaces — the user must duplicate logic |
| Missing logging | No visibility when things go wrong in production — the user cannot diagnose issues without structured logs |
| Missing `revalidatePath` | UI shows stale data after mutations, confusing users who think their action failed |
| Using admin client unnecessarily | Bypasses RLS, creating potential data leakage between tenant accounts |

Following the patterns below prevents these failures.

## Workflow

When asked to create a server action, follow these steps:

### Step 1: Create Zod Schema

Create validation schema in `_lib/schema/`:

```typescript
// _lib/schema/feature.schema.ts
import { z } from 'zod';

export const CreateFeatureSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  accountId: z.string().uuid('Invalid account ID'),
});

export type CreateFeatureInput = z.infer<typeof CreateFeatureSchema>;
```

### Step 2: Create Service Layer

**North star: services are decoupled from their interface.** The service is pure logic — it receives a database client as a dependency, never imports one. This means the same service works whether called from a server action, an MCP tool, a CLI command, or a plain unit test.

Create service in `_lib/server/`:

```typescript
// _lib/server/feature.service.ts
import 'server-only';

import type { SupabaseClient } from '@supabase/supabase-js';

import type { Database } from '@/types/database';
import type { CreateFeatureInput } from '../schema/feature.schema';

export function createFeatureService(client: SupabaseClient<Database>) {
  return new FeatureService(client);
}

class FeatureService {
  constructor(private readonly client: SupabaseClient<Database>) {}

  async create(data: CreateFeatureInput) {
    const { data: result, error } = await this.client
      .from('features')
      .insert({
        name: data.name,
        account_id: data.accountId,
      })
      .select()
      .single();

    if (error) throw error;

    return result;
  }
}
```

The service never calls `createClient()` — the caller provides the client. This keeps the service testable (pass a mock client) and reusable (any interface can supply its own client).

### Step 3: Create Server Action (Thin Adapter)

The action is a **thin adapter** — it resolves dependencies (client, logger) and delegates to the service. Business logic in the adapter means the user must duplicate changes across every interface when logic evolves.

Create action in `_lib/server/server-actions.ts`:

```typescript
'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';

import { createClient } from '@/lib/supabase/server';
import { getSession } from '@/lib/auth';
import { logger } from '@/lib/logger';

import { CreateFeatureSchema } from '../schema/feature.schema';
import { createFeatureService } from './feature.service';

export async function createFeatureAction(input: z.infer<typeof CreateFeatureSchema>) {
  const session = await getSession();
  if (!session) throw new Error('Unauthorized');

  const data = CreateFeatureSchema.parse(input);

  const ctx = { name: 'create-feature', userId: session.user.id };
  logger.info(ctx, 'Creating feature');

  const client = await createClient();
  const service = createFeatureService(client);
  const result = await service.create(data);

  logger.info({ ...ctx, featureId: result.id }, 'Feature created');

  revalidatePath('/home/[account]/features');

  return { success: true, data: result };
}
```

## Key Patterns

The user configured these patterns because each prevents a specific failure mode that has caused real issues:

1. **Services are pure, interfaces are thin adapters.** The service contains all business logic. The server action is glue code that resolves dependencies and calls the service. If an MCP tool and a server action do the same thing, they call the same service function — otherwise the user fixes bugs in one place while they persist in another.
2. **Inject dependencies, don't import them in services.** Services that import framework clients directly cannot be tested in isolation — the user depends on dependency injection to maintain test coverage.
3. **Schema in separate file** — Reusable between client forms and server actions; a single source of truth for validation prevents client and server from drifting apart.
4. **Logging** — Without structured logs, the user cannot diagnose production issues. Always log before and after operations with a context object.
5. **Revalidation** — Missing `revalidatePath` after mutations causes stale UI that makes users think their action failed.
6. **Trust RLS** — Manual auth checks are error-prone and duplicate logic that RLS already handles. Use the standard Supabase client, not the admin client.
7. **Testable in isolation** — Because services accept their dependencies, you can test them with a mock client and no running infrastructure.

## File Structure

```
feature/
├── _lib/
│   ├── schema/
│   │   └── feature.schema.ts
│   └── server/
│       ├── feature.service.ts
│       └── server-actions.ts
└── _components/
    └── feature-form.tsx
```

## Troubleshooting

### Server action callback receives wrong parameters

**Cause:** The server action function signature doesn't match the expected input. Ensure the function accepts the validated input type and performs its own auth check with `getSession()`.

**Fix:** Always use `async function myAction(input: z.infer<typeof Schema>)` and call `getSession()` at the top of the function body.

### Missing `'use server'` directive

**Cause:** Without the directive, Next.js treats the file as a regular module. Server actions silently become client-side functions, breaking auth and validation.

**Fix:** Add `'use server';` as the very first line of the server actions file.

### Stale UI after mutation

**Cause:** Missing `revalidatePath` call after the mutation. Next.js caches server component data, and without revalidation the user sees outdated data.

**Fix:** Add `revalidatePath('/home/[account]/feature-path')` after every successful mutation.

### Missing auth check in server action

**Cause:** The server action doesn't verify the user is authenticated before processing. Without auth verification, unauthenticated requests can reach the database.

**Fix:** Always call `getSession()` at the top of every server action and throw an error if no session exists.

### Server action re-exported from barrel file

**Cause:** Re-exporting server actions from `_lib/server/index.ts` breaks Next.js server action detection. The framework cannot identify re-exported functions as server actions.

**Fix:** Import server actions directly from `_lib/server/server-actions.ts`, never through a barrel file.

## Reference Files

See examples in:
- [Examples](examples.md)
- [Reference](reference.md)
