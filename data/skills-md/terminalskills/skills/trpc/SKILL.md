---
name: trpc
description: >-
  Assists with building end-to-end type-safe APIs using tRPC without code generation.
  Use when creating type-safe client-server bridges, defining procedures with Zod validation,
  integrating with Next.js or React Query, or setting up WebSocket subscriptions.
  Trigger words: trpc, type-safe api, procedures, react query, end-to-end types.
license: Apache-2.0
compatibility: "Requires TypeScript and Node.js 16+"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: development
  tags: ["trpc", "typescript", "api", "type-safety", "react-query"]
---

# tRPC

## Overview

tRPC enables building fully type-safe APIs without code generation by creating seamless client-server type bridges. Changing a backend procedure instantly updates TypeScript types on the frontend, providing end-to-end type safety across the full stack.

## Instructions

- When setting up tRPC, initialize with `initTRPC.create()`, define a context factory for session/database access, and create `publicProcedure` and `protectedProcedure` bases with middleware chains.
- When defining procedures, use Zod schemas for input validation (`.input(z.object({...}))`), choose query for read operations and mutation for writes, and keep procedures thin by extracting business logic into service functions.
- When organizing routers, create one router per feature domain and merge all sub-routers in a single `appRouter`, exporting its type as `AppRouter`.
- When integrating with Next.js, use `@trpc/next` for App Router support, `createCaller` for server components, and `@trpc/react-query` for client-side cache management with optimistic updates.
- When handling errors, throw `TRPCError` with typed error codes (`NOT_FOUND`, `UNAUTHORIZED`, `BAD_REQUEST`) instead of generic errors.
- When implementing real-time features, use subscription procedures with `wsLink` and `observable()` for WebSocket-based updates.
- When testing, use `createCaller` to call procedures directly without HTTP, and inject mock context for isolated tests.

## Examples

### Example 1: Set up a type-safe API for a Next.js app

**User request:** "Add tRPC to my Next.js project with user and post routers"

**Actions:**
1. Initialize tRPC with context factory extracting session from request
2. Create `userRouter` and `postRouter` with Zod-validated procedures
3. Merge into `appRouter` and set up Next.js API route handler
4. Configure `@trpc/react-query` client with batching link

**Output:** A fully typed API where frontend components have autocomplete for all backend procedures.

### Example 2: Add authentication middleware

**User request:** "Create a protected procedure that checks user auth before allowing access"

**Actions:**
1. Create auth middleware that validates session from context
2. Define `protectedProcedure` by chaining the middleware onto `publicProcedure`
3. Use `protectedProcedure` for all routes requiring authentication
4. Return typed `UNAUTHORIZED` error when session is missing

**Output:** A reusable protected procedure base with proper error handling.

## Guidelines

- One router per feature domain: `userRouter`, `orderRouter`, `notificationRouter`.
- Merge all sub-routers in a single `appRouter` and export its type: `export type AppRouter = typeof appRouter`.
- Always validate inputs with Zod schemas; never trust raw client data.
- Use `TRPCError` with appropriate codes, not generic `throw new Error()`.
- Keep procedures thin: extract business logic into service functions.
- Co-locate input schemas with their procedures or in a shared `schemas/` package for monorepos.
- Use middleware for cross-cutting concerns instead of duplicating auth checks.
