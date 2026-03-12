---
name: offensive-typesafety
description: >
  Invoke this skill when setting up new tech stacks, configuring project architecture, or replacing 
  untyped boundaries with strict, compiler-enforced constraints. Treat types as a development 
  accelerator. Prefer tools like TanStack Router, Zod, and Drizzle to build end-to-end type safety.
---

# Offensive Typesafety

**When to invoke this skill:**
- When setting up or evaluating a new tech stack.
- When designing API, URL state, or database boundaries.
- When refactoring untyped string-based logic into strict, compiler-checked contracts.

**Offensive Typesafety** is the practice of using strong, compiler-enforced types to accelerate development. Instead of using types defensively (just to catch bugs before production), use them offensively to establish strict boundaries that allow you—and AI code generators—to move blazingly fast without breaking things.

## Core Philosophy: Compilers over Conventions

- **Constraints over "looks right"**: Code should not just look plausible; it should fail at the compiler level if it is structurally or conceptually wrong.
- **Explicit over Magic**: Prefer explicit, traversable data structures over string-based assumptions or untyped framework magic.
- **Fail Early**: The compiler is the first line of defense. The faster it fails, the faster you can iterate.
- **AI Viability**: When AI writes code, types act as a contract, a feedback loop, and a way to self-correct. If an AI generates a typo in a string route, it fails silently at runtime. If it messes up a strongly typed route, the compiler catches it instantly.

## Architecture Patterns for Moving Fast

Default to tools that enforce correctness at every layer.

### 1. Type-Safe Routing (e.g., TanStack Router, Expo Router)

A surprising amount of app complexity lives in routes, path parameters, and navigation. String-based routing and filesystem-only navigation often silently fail at runtime when links break or params change.

**Avoid:** String-based routing where broken links aren't caught until clicked.  
**Prefer:** Explicit, structurally-typed routes.

```tsx
// BAD: String soup routing. Easy to break on refactoring.
<Link to={`/users/${userId}?tab=settings`}>Settings</Link>

// GOOD: Type-checked routing. The compiler ensures the target route, path params, and search params exist and are valid.
<Link 
  to="/users/$userId" 
  params={{ userId }} 
  search={{ tab: 'settings' }}
>
  Settings
</Link>
```

### 2. Validated External Inputs (e.g., Zod, Valibot, ArkType)

URL state and API responses are real application state. They must be strictly typed and validated, not treated as untyped "string soup."

**Avoid:** Parsing `window.location.search` manually or using unbound search param hooks.  
**Prefer:** Defining schemas (e.g., via Zod) to validate and type search parameters before they enter the application logic.

```tsx
import { z } from 'zod';

// Define the contract for the URL
const userSearchSchema = z.object({
  tab: z.enum(['profile', 'settings']).default('profile'),
  page: z.number().catch(1),
});

// The router enforces this contract
export const Route = createFileRoute('/users/$userId')({
  validateSearch: userSearchSchema,
});

// The component instantly benefits from typed, parsed, and safe search params
function UserPage() {
  const { tab, page } = Route.useSearch(); // tab is automatically 'profile' | 'settings'
  // ...
}
```

### 3. Unified Server/Client Boundaries (e.g., TanStack Start, tRPC, Hono RPC)

Your frontend and backend must speak the same type language. Manual API endpoints and manual type casting introduce dangerous gaps where the client expects one shape and the server returns another. This is especially true for E2E testing, where type-safe clients (like `hc` from Hono) prevent test queries from becoming outdated.

**Avoid:** Fetching data from manually constructed `fetch` endpoints and casting with `as MyType`.  
**Prefer:** Server functions or RPC procedures that automatically infer their inputs and outputs across the network boundary, ensuring both app requests and test suites stay synced.

```tsx
import { createServerFn } from '@tanstack/start';

// Server Function: Defines the exact input and output types naturally
export const getUserStats = createServerFn("GET", async (userId: string) => {
  const dbUser = await db.query.users.findFirst({ userId });
  return { active: dbUser.isActive, score: dbUser.score }; // Inferred output type
});

// Route Loader: Consumes the server function directly. Type logic is preserved over the network.
export const Route = createFileRoute('/users/$userId')({
  loader: async ({ params }) => {
    // The compiler enforces that params.userId is a string, and 'stats' is { active: boolean, score: number }
    const stats = await getUserStats(params.userId);
    return { stats };
  },
});
```

### 4. End-to-End Database Types (e.g., Drizzle ORM, Prisma, Kysely)

Your database schema should drive the types for the rest of your application.

**Avoid:** Writing SQL strings and manually declaring a TypeScript interface to match the expected results.  
**Prefer:** A TypeScript ORM where the schema definition dictates the types exactly.

```tsx
// schema.ts
export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull(),
  isActive: boolean('is_active').default(true),
});

// Re-use inferred types everywhere
export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;
```

---

## Summary Checklist

- [ ] Does your chosen tech stack rely on **compiler errors** rather than runtime checks to catch broken links and payloads?
- [ ] Are external inputs (like **search parameters** and API requests) validated through a strict schema before they hit application logic?
- [ ] Are **routes and paths** treated as explicit data structures rather than strings?
- [ ] Is there a **single source of truth** for types crossing from the database, through the server, and into the client boundary?
