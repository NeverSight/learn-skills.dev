---
name: code-review
description: "LOAD THIS SKILL when: reviewing code before PR, user mentions 'code review', 'review', 'pre-PR check', 'code quality audit'. Contains project-specific review checklist covering TRPC, TanStack, Drizzle, security, performance, and Effect patterns."
compatibility: opencode
---

# Code Review Methodology

Systematic pre-PR code review for the project codebase. Identifies critical issues with focus on TRPC patterns, TanStack Router, Drizzle ORM, and security best practices.

## Review Process

1. **Identify Scope** — Determine what code to review
2. **Scan Changes** — Analyze against project-specific patterns
3. **Verify with Exa & Context7** — Validate uncertain patterns
4. **Categorize Findings** — Organize by severity (Critical, Major, Minor)
5. **Generate Report** — Structured report with actionable feedback
6. **Run Automated Checks** — Execute `bun run check`

---

## Step 1: Identify Scope

Ask the user what to review:

1. **Recent commits** (default): `git log -5 --oneline && git diff HEAD~5..HEAD --stat`
2. **Specific files/directories**: User-provided paths
3. **Branch comparison**: `git diff main..HEAD --stat`

---

## Step 2: Vivus-Specific Review Categories

### 1. TRPC Patterns

**Check against skill:** `trpc-patterns`

**Critical patterns to verify:**

```typescript
// ✅ Correct - Using RouterOutputs/RouterInputs
type SessionData = RouterOutputs["adminAuthSessions"]["listTokens"]["sessions"][0];

// ❌ Wrong - Manual type definitions
type SessionData = { sessionId: string; ... };
```

```typescript
// ✅ Correct - Using error helpers
throw notFoundError("Project not found");

// ❌ Wrong - Manual TRPCError
throw new TRPCError({ code: "NOT_FOUND", message: "..." });
```

```typescript
// ✅ Correct - protectedMemberAccessProcedure for org-scoped
export const router = {
  getOrgData: protectedMemberAccessProcedure
    .input(z.object({ organizationId: z.string() }))
    .query(...)
}

// ❌ Wrong - Manual membership check in protectedProcedure
```

```typescript
// ✅ Correct - Inline simple schemas with common types
role: z.enum([OrganizationRoles.Owner, OrganizationRoles.Admin]);

// ❌ Wrong - Hardcoded enum values
role: z.enum(["owner", "admin"]);
```

**SQL Query Optimization:**

```typescript
// ✅ Correct - Single query with JOINs
const result = await db.select({...}).from(membersTable)
  .innerJoin(organizationsTable, eq(...))
  .leftJoin(projectsTable, eq(...))

// ❌ Wrong - Multiple separate queries (N+1)
const orgs = await db.select().from(organizationsTable);
const members = await db.select().from(membersTable);
```

---

### 2. TanStack Router & Query Patterns

**Check against skill:** `tanstack-frontend`

**Critical patterns to verify:**

```typescript
// ✅ Correct - TRPC v11 pattern with .queryOptions()
const { data } = useSuspenseQuery(trpc.organization.getById.queryOptions({ id }));

// ❌ Wrong - Old pattern (doesn't exist in v11)
const { data } = trpc.organization.getById.useQuery({ id });
```

```typescript
// ✅ Correct - Prefetch critical data with await
loader: async ({ context, params }) => {
  await context.queryClient.prefetchQuery(
    context.trpc.organization.getById.queryOptions({ id: params.id })
  );
  // Secondary data - void for optimization
  void context.queryClient.prefetchQuery(
    context.trpc.analytics.getStats.queryOptions({ id: params.id })
  );
}

// ❌ Wrong - Sequential await (slow)
await context.queryClient.prefetchQuery(...);
await context.queryClient.prefetchQuery(...);
await context.queryClient.prefetchQuery(...);

// ❌ Wrong - All void (component will suspend)
void context.queryClient.prefetchQuery(...);  // critical data!
```

```typescript
// ✅ Correct - Props type naming
type Props = { isOpen: boolean; onClose: () => void; };

// ❌ Wrong - Component-specific props naming
type DeleteMemberModalProps = { ... };
```

```typescript
// ✅ Correct - Cache invalidation
await queryClient.invalidateQueries({
  queryKey: trpc.organization.queryKey(),
});
```

---

### 3. Code Deduplication (DRY)

**Identify duplicate or near-duplicate code:**

- Same logic implemented in multiple files with different approaches
- Copy-pasted functions with minor variations
- Repeated patterns that could be extracted to shared utilities

**When to extract:**

- Same logic appears in 2+ locations
- Functions differ only in minor details (parameterize instead)
- Utility is general enough to be reused

**Where to place shared code:**

- `packages/services/src/` — Cross-service shared utilities
- `packages/common/src/` — Cross-package shared types/utilities
- Same-directory `utils.ts` — Local module utilities

---

### 4. Code Quality & Style

**Check CLAUDE.md conventions:**

- **Imports:** Always absolute (`@/path` or `@project/*`), never relative in `apps/web-app/src`
- **Nullish coalescing:** Use `??` not `||` for defaults
- **Bun APIs:** Use `Bun.file()`, `Bun.spawn()` instead of Node.js polyfills
- **File naming:** kebab-case (`contact-form.tsx`, not `ContactForm.tsx`)
- **Types:** Use `type` not `interface` unless extending
- **Logger:** Use `@project/logger` for backend, `console.log/error` is OK for frontend React components
- **No barrel files:** Don't create `index.ts` that only re-exports (causes circular imports, slow dev)

**DO NOT REPORT these as issues (they are acceptable):**

- `packages/*/src/index.ts` using `export *` — Package entry points are allowed exceptions
- Relative imports (`../`) inside `packages/` directories — Only apps/web-app requires absolute imports
- `console.log/error` in React components (frontend) — Only backend code requires `@project/logger`

---

### 5. Security

**Critical checks:**

- Hardcoded secrets/API keys: `grep -iE "api[_-]?key|password|secret|token"`
- SQL injection: String interpolation in queries
- Missing auth: Endpoints without `protectedProcedure` or `protectedMemberAccessProcedure`
- Sensitive data in logs
- Missing input validation

**Use error helpers from `@/infrastructure/errors`:**

- `badRequestError()`, `unauthorizedError()`, `forbiddenError()`, `notFoundError()`

---

### 6. Performance

**Database:**

- N+1 queries (multiple queries that could be JOINs)
- Missing indexes on frequently queried columns
- Sequential API calls instead of `Promise.all()`

**Frontend:**

- Missing prefetch in loaders
- Sequential `await` instead of `Promise.all()` in loaders
- `fetchQuery` when `prefetchQuery` would suffice

---

### 7. Testing

**Check for:**

- New TRPC endpoints without tests in `packages/services/src/__tests__/`
- New components without tests
- Missing E2E tests for critical flows

---

### 8. Effect Patterns (if changes include Effect code)

**Check against skill:** `effect-ts`

**Applies to:** `packages/services/`, `effect-runtime.ts`, files with `Effect.gen`, `Context.Tag`

```typescript
// ✅ Correct - Service with @project namespace
export class MyService extends Context.Tag("@project/MyService")<...>() {}

// ❌ Wrong - Missing namespace
export class MyService extends Context.Tag("MyService")<...>() {}
```

```typescript
// ✅ Correct - Effect.fn for tracing
const doSomething = Effect.fn("MyService.doSomething")(
  function* (params) { ... }
);

// ❌ Wrong - No tracing
const doSomething = (params) => Effect.gen(function* () { ... });
```

```typescript
// ✅ Correct - Schema.TaggedError
export class MyError extends Schema.TaggedError<MyError>()("MyError", {...}) {}

// ❌ Wrong - Data.TaggedError (less Schema interop)
export class MyError extends Data.TaggedError("MyError")<{...}> {}
```

```typescript
// ✅ Correct - ManagedRuntime for TRPC
import { runtime } from "@/infrastructure/effect-runtime";
await runtime.runPromise(Effect.gen(function* () { ... }));

// ❌ Wrong - Inline provide per request
await Effect.runPromise(effect.pipe(Effect.provide(ServiceLive)));
```

**For comprehensive Effect analysis, run:** `/scan-effect-solutions`

---

## Verify Uncertain Patterns

**Use Exa Search** for real-world patterns:

```
Query: "React useEffect cleanup best practices"
Query: "TRPC v11 queryOptions pattern"
```

**Use Context7** for official docs:

```
1. context7-resolve-library-id(libraryName: "tanstack-query")
2. context7-get-library-docs(context7CompatibleLibraryID: "...", topic: "prefetchQuery")
```

---

## Finding Severity Classification

### CRITICAL (Must Fix Before Merge)

- Security vulnerabilities
- SQL injection, hardcoded secrets
- Missing authentication on protected endpoints
- Breaking changes to public APIs

### MAJOR (Should Fix)

- Wrong TRPC v11 patterns (`.useQuery` instead of `.queryOptions`)
- N+1 database queries
- Missing prefetch causing slow page loads
- Manual types instead of `RouterInputs`/`RouterOutputs`
- Code duplication — same logic in multiple files (DRY violation)

### MINOR (Consider Fixing)

- Style inconsistencies
- Missing documentation
- Non-critical refactoring

---

## Report Template

```markdown
# Code Review Report

**Scope:** [What was reviewed]
**Date:** [Current date]

---

## CRITICAL ISSUES

[List with file:line, description, fix]

---

## MAJOR ISSUES

[List with file:line, description, fix]

---

## MINOR ISSUES

[List with file:line, brief description]

---

## POSITIVE OBSERVATIONS

- [Good patterns found]

---

## SUMMARY

**Assessment:** [APPROVE / NEEDS_WORK / REJECT]
**Next steps:** [Specific actions]

## Quick Stats

- Files reviewed: [N]
- Issues: Critical: [N], Major: [N], Minor: [N]
```

---

## Assessment Criteria

**APPROVE**

- No critical issues
- TRPC and TanStack patterns correct
- `bun run check` passes

**NEEDS_WORK**

- Major pattern violations
- Missing tests for new functionality
- Performance issues

**REJECT**

- Security vulnerabilities
- Breaking changes without migration
- Fundamental design flaws

---

## Related Skills

- `trpc-patterns` — TRPC router patterns, procedures, error handling
- `tanstack-frontend` — Router, Query, Form patterns
- `effect-ts` — Effect services, layers, ManagedRuntime, error handling
- `scan-effect-solutions` — Deep Effect compliance scan
- `production-troubleshooting` — Performance investigation
