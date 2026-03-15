---
name: trpc-tanstack-integration
description: "Use when adding tRPC and TanStack Query integration to a TypeScript project, especially Next.js App Router projects. Triggers: setup trpc, integrate tanstack query, create trpc router/context/provider, add api client server client hydration."
---

# tRPC + TanStack Query Integration

## Goal
Set up end-to-end type-safe API integration using:
- `@trpc/server`
- `@trpc/client`
- `@trpc/tanstack-react-query`
- `@tanstack/react-query`
- optional transformer (`devalue` or `superjson`)

This skill should perform implementation, not just planning.

## Bundled Reusable Templates

Use the prebuilt templates in this skill as the default implementation source.

- `templates/next-app-router/server/trpc.ts`
- `templates/next-app-router/server/app-router.ts`
- `templates/next-app-router/app/api/trpc/[trpc]/route.ts`
- `templates/next-app-router/client/query-client.ts`
- `templates/next-app-router/client/trpc-react.tsx`
- `templates/next-app-router/server/trpc-rsc.tsx`
- `templates/next-app-router/README.md`

When integrating, copy these files into the target project and adapt import paths and auth session typing.

## Workflow

1. Detect project shape before editing.
- Check framework (`next`, `vite`, `react`, `node`) from `package.json`.
- Detect package manager from lockfiles (`pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `bun.lockb`).
- Detect routing/runtime style (Next.js App Router vs Pages Router vs SPA).

2. Install required dependencies.
- Runtime deps:
  - `@trpc/server`
  - `@trpc/client`
  - `@trpc/tanstack-react-query`
  - `@tanstack/react-query`
  - `zod`
  - `devalue`
- Add framework-specific deps only if needed by detected architecture.

3. Copy templates first.
- For Next.js App Router, copy files from `templates/next-app-router/`.
- Follow `templates/next-app-router/README.md` for destination mapping.
- After copying, update imports and aliases to match the target project.

4. Create server foundation.
- Add `trpc` initializer with:
  - context typing
  - `router`, `publicProcedure`, optional `protectedProcedure`
  - consistent error formatting for Zod validation issues
  - transformer serialize/deserialize setup
- Add root router (`appRouter`) and exported `AppRouter` type.

5. Expose server endpoint.
- For Next.js App Router: create `app/api/trpc/[trpc]/route.ts` using `fetchRequestHandler`.
- Build context per request (auth/session if available).
- Add structured logging for non-auth errors.

6. Create TanStack Query client factory.
- Add a reusable `makeQueryClient()` with sane defaults:
  - non-zero `staleTime`
  - hydration/dehydration serializer support
  - query/mutation error handling hooks
- Export inferred API input/output types from `AppRouter` if helpful.

7. Create client provider.
- Implement a `TRPCReactProvider` as a client component.
- Wrap app tree with:
  - `QueryClientProvider`
  - `TRPCProvider` from `createTRPCContext<AppRouter>()`
- Use browser singleton query client to avoid recreation on suspense.

8. Add server-side helper (when SSR/RSC exists).
- Provide RSC helper utilities for:
  - prefetching query options
  - creating server-side caller
  - hydration boundary wrapper
- Use request-aware context/session where auth exists.

9. Wire providers into app layout.
- Ensure root layout or app provider tree includes the TRPC/TanStack provider.
- Preserve existing provider order and do not break existing context dependencies.

10. Validate integration.
- Run type-check/lint/build commands available in repo.
- Confirm one read query and one mutation compile and run.
- If tests exist for API layer, run relevant subset.

## Implementation Rules
- Prefer adapting existing project conventions (logger, auth, folder layout) over introducing new patterns.
- Reuse existing serialization approach if project already uses one.
- Avoid replacing unrelated files; keep edits minimal and additive.
- If authentication exists, include `protectedProcedure`; otherwise keep public-only setup.
- If project already has partial integration, complete missing pieces instead of duplicating files.

## Next.js App Router Reference Layout

Use this structure when no established convention exists:

- `src/server/trpc.ts` 
- `src/server/routers/_app.ts`
- `app/api/trpc/[trpc]/route.ts`
- `src/lib/trpc-client.tsx` 
- `src/lib/query-client.ts`
- `src/lib/trpc-rsc.tsx`

## Completion Checklist
- Template files copied from this skill and adjusted for target project paths.
- Dependencies installed.
- `AppRouter` exported.
- API route handler wired.
- React Query and TRPC provider mounted in app tree.
- Client can call at least one procedure with inferred types.
- Type-check passes.
- No duplicate provider/query-client instances introduced.
