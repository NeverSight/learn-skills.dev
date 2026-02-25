---
name: service-builder
description: "Build pure, interface-agnostic services with injected dependencies for Next.js/Supabase applications."
metadata:
  version: 1.0.0
---

# Service Builder

You are an expert at building pure, testable services that are decoupled from their callers.

## North Star

**Every service is decoupled from its interface (I/O).** A service takes plain data in, does work, and returns plain data out. It has no knowledge of whether it was called from an MCP tool, a server action, a CLI command, a route handler, or a test. The caller is a thin adapter that resolves dependencies and delegates.

## Workflow

When asked to create a service, follow these steps:

### Step 1: Define the Contract

Start with the input/output types. These are plain TypeScript — no framework types.

```typescript
// _lib/schema/project.schema.ts
import { z } from 'zod';

export const CreateProjectSchema = z.object({
  name: z.string().min(1),
  accountId: z.string().uuid(),
});

export type CreateProjectInput = z.infer<typeof CreateProjectSchema>;

export interface Project {
  id: string;
  name: string;
  account_id: string;
  created_at: string;
}
```

### Step 2: Build the Service

The service receives all dependencies through its constructor. It never imports framework-specific modules (`createClient`, `logger`, `revalidatePath`, etc.).

```typescript
// _lib/server/project.service.ts
import type { SupabaseClient } from '@supabase/supabase-js';

import type { CreateProjectInput, Project } from '../schema/project.schema';

export function createProjectService(client: SupabaseClient) {
  return new ProjectService(client);
}

class ProjectService {
  constructor(private readonly client: SupabaseClient) {}

  async create(data: CreateProjectInput): Promise<Project> {
    const { data: result, error } = await this.client
      .from('projects')
      .insert({
        name: data.name,
        account_id: data.accountId,
      })
      .select()
      .single();

    if (error) throw error;

    return result;
  }

  async list(accountId: string): Promise<Project[]> {
    const { data, error } = await this.client
      .from('projects')
      .select('*')
      .eq('account_id', accountId)
      .order('created_at', { ascending: false });

    if (error) throw error;

    return data;
  }

  async delete(projectId: string): Promise<void> {
    const { error } = await this.client
      .from('projects')
      .delete()
      .eq('id', projectId);

    if (error) throw error;
  }
}
```

### Step 3: Write Thin Adapters

Each interface is a thin adapter — it resolves dependencies, calls the service, and handles interface-specific concerns (revalidation, redirects, MCP formatting, CLI output).

**Server Action adapter:**

```typescript
// _lib/server/server-actions.ts
'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';

import { createClient } from '@/lib/supabase/server';
import { getSession } from '@/lib/auth';
import { logger } from '@/lib/logger';

import { CreateProjectSchema } from '../schema/project.schema';
import { createProjectService } from './project.service';

export async function createProjectAction(formData: z.infer<typeof CreateProjectSchema>) {
  const session = await getSession();
  if (!session) throw new Error('Unauthorized');

  const data = CreateProjectSchema.parse(formData);

  logger.info({ name: 'create-project', userId: session.user.id }, 'Creating project');

  const client = await createClient();
  const service = createProjectService(client);
  const result = await service.create(data);

  revalidatePath('/home/[account]/projects');

  return { success: true, data: result };
}
```

**Route Handler adapter:**

```typescript
// app/api/projects/route.ts
import { NextRequest, NextResponse } from 'next/server';

import { createClient } from '@/lib/supabase/server';
import { getSession } from '@/lib/auth';

import { CreateProjectSchema } from '../_lib/schema/project.schema';
import { createProjectService } from '../_lib/server/project.service';

export async function POST(request: NextRequest) {
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const body = await request.json();
  const data = CreateProjectSchema.parse(body);

  const client = await createClient();
  const service = createProjectService(client);
  const result = await service.create(data);

  return NextResponse.json(result);
}
```

**MCP Tool adapter:**

```typescript
// mcp/tools/kit_project_create.ts
import { createProjectService } from '../../_lib/server/project.service';

export const kit_project_create: McpToolHandler = async (input, context) => {
  const client = context.getSupabaseClient();
  const service = createProjectService(client);

  return service.create(input);
};
```

### Step 4: Write Tests

Because the service accepts dependencies, you can test it with stubs — no running database, no framework runtime.

```typescript
// _lib/server/__tests__/project.service.test.ts
import { describe, it, expect, vi } from 'vitest';

import { createProjectService } from '../project.service';

function createMockClient(overrides: Record<string, unknown> = {}) {
  const mockChain = {
    insert: vi.fn().mockReturnThis(),
    select: vi.fn().mockReturnThis(),
    single: vi.fn().mockResolvedValue({
      data: { id: 'proj-1', name: 'Test', account_id: 'acc-1', created_at: new Date().toISOString() },
      error: null,
    }),
    delete: vi.fn().mockReturnThis(),
    eq: vi.fn().mockReturnThis(),
    order: vi.fn().mockResolvedValue({ data: [], error: null }),
    ...overrides,
  };

  return {
    from: vi.fn(() => mockChain),
    mockChain,
  } as unknown as SupabaseClient;
}

describe('ProjectService', () => {
  it('creates a project', async () => {
    const client = createMockClient();
    const service = createProjectService(client);

    const result = await service.create({
      name: 'Test Project',
      accountId: 'acc-1',
    });

    expect(result.id).toBe('proj-1');
    expect(client.from).toHaveBeenCalledWith('projects');
  });

  it('throws on database error', async () => {
    const client = createMockClient({
      single: vi.fn().mockResolvedValue({
        data: null,
        error: { message: 'unique violation' },
      }),
    });

    const service = createProjectService(client);

    await expect(
      service.create({ name: 'Dup', accountId: 'acc-1' }),
    ).rejects.toEqual({ message: 'unique violation' });
  });
});
```

## Rules

The user configured these rules because each addresses a real failure mode that has caused bugs or maintenance problems in this codebase.

1. **Services are pure functions over data.** Plain objects/primitives in, plain objects/primitives out. No `Request`/`Response`, no MCP context, no `FormData`. Accepting framework types couples the service to one interface — the user loses the ability to reuse it from MCP tools, CLI commands, or tests.

2. **Inject dependencies, never import them.** Services that import framework-specific clients directly (like `createClient()`) cannot be tested in isolation — the user depends on dependency injection to maintain test coverage across server actions, MCP tools, and CLI commands.

3. **Adapters are trivial glue.** A server action resolves the client, calls the service, and handles `revalidatePath`. An MCP tool resolves the client, calls the service, and formats the response. Business logic in adapters means the user must duplicate changes across every interface when logic evolves.

4. **One service, many callers.** If two interfaces do the same thing, they call the same service function. Duplicating logic means the user fixes a bug in one place but it persists in another — leading to inconsistent behavior across interfaces.

5. **Testable in isolation.** Pass a mock client, assert the output. Services that require a running database force the user to rely on slow integration tests for every change, making TDD impractical.

## What Goes Where

| Concern | Location | Example |
|---------|----------|---------|
| Input validation (Zod) | `_lib/schema/` | `CreateProjectSchema` |
| Business logic | `_lib/server/*.service.ts` | `ProjectService.create()` |
| Auth check | Adapter (Server Action with `getSession()`) | Manual auth verification |
| Logging | Adapter | `logger.info()` before/after service call |
| Cache revalidation | Adapter | `revalidatePath()` after mutation |
| Redirect | Adapter | `redirect()` after creation |
| MCP response format | Adapter | Return service result as MCP content |

## File Structure

```
feature/
├── _lib/
│   ├── schemas/
│   │   └── feature.schema.ts       # Zod schemas + TS types
│   └── server/
│       ├── feature.service.ts       # Pure service (dependencies injected)
│       ├── server-actions.ts        # Server action adapters
│       └── __tests__/
│           └── feature.service.test.ts  # Unit tests with mock client
└── _components/
    └── feature-form.tsx
```

## Anti-Patterns

```typescript
// BAD: Service imports framework-specific client
class ProjectService {
  async create(data: CreateProjectInput) {
    const client = await createClient(); // coupling!
    // ...
  }
}

// BAD: Business logic in the adapter
export async function createProjectAction(formData: FormData) {
  const session = await getSession();
  if (!session) throw new Error('Unauthorized');

  const client = await createClient();
  // Business logic directly in the action — not reusable
  if (data.name.length > 100) throw new Error('Name too long');
  const { data: result } = await client.from('projects').insert(data);
  return result;
}

// BAD: Two interfaces duplicate the same logic
// server-actions.ts
const result = await client.from('projects').insert(...).select().single();
// mcp-tool.ts
const result = await client.from('projects').insert(...).select().single();
// Should be: both call projectService.create()
```

## Troubleshooting

### Service cannot be tested without running database

**Cause:** The service imports `createClient()` or other framework-specific modules directly instead of receiving them as constructor arguments.

**Fix:** Refactor to accept `SupabaseClient` as a constructor parameter. The adapter (server action, route handler) resolves the client and passes it in.

### Missing `import 'server-only'`

**Cause:** Service file can be accidentally imported by client-side code, leaking server logic and credentials to the browser bundle.

**Fix:** Add `import 'server-only';` as the first import in every service file. This causes a build error if client code tries to import it.

### Service method returns `{ success, error }` wrapper

**Cause:** Inconsistent with codebase pattern where services throw on error and return data directly.

**Fix:** Services should throw errors (let the adapter handle error formatting) and return the result directly. The adapter decides how to present success/failure to its interface.

### Business logic leaking into adapters

**Cause:** Logic was written directly in the server action instead of a service method. Other interfaces (MCP, CLI) cannot reuse it.

**Fix:** Move all business logic into the service. The adapter should only: resolve dependencies, call the service, handle revalidation/redirects/formatting.

## Reference

See [Examples](examples.md) for more patterns including services with multiple dependencies, services that compose other services, and testing strategies.
