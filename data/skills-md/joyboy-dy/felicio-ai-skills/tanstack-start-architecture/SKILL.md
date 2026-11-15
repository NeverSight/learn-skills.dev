---
name: tanstack-start-architecture
description: "Use when creating, structuring, reviewing, or refactoring a TanStack Start application (React or Solid): project layout, file-based routes, server functions, middleware, server routes, the server/client execution boundary, loaders with TanStack Query, search-param and input validation (Zod/Standard Schema), auth guards, SSR/SPA/prerender modes, environment variables, hosting, or an Elysia/Hono API mounted inside Start with Eden. Also for migrating to TanStack Start from Next.js or from a pre-1.169 release."
---

# TanStack Start Architecture

Structure TanStack Start apps so that **each piece of code runs where it is meant to run**, routes stay thin, and data has one owner. Apply it to the **installed version** and to the repository's existing conventions.

## Use when

Activate for TanStack Start project setup or layout, route trees, `createServerFn`, `createMiddleware`, `src/start.ts`, server routes (`server.handlers`), loaders/`beforeLoad`, Router + Query integration, `validateSearch`, auth guards, selective SSR, SPA/prerender, env handling, hosting adapters, an API framework (Elysia, Hono) mounted inside Start, or a Next.js → Start migration.

Do not use for a plain TanStack Router SPA without Start (no `@tanstack/*-start` dependency), for Next.js projects (`nextjs-architecture-pattern`), or for a backend deployed as a separate service; for the internals of an embedded Elysia app, prefer the official Elysia skill. Generic implementation quality belongs to `senior-frontend-engineering`; form behavior/UX to `form-ux-validation`.

## Detect first

```bash
python scripts/scan_tanstack_start.py <project-root> --json
```

Then read `package.json`, `vite.config.*` (or `rsbuild.config.*`), `src/router.tsx`, `src/routes/__root.tsx`, `src/start.ts` if present, `tsconfig.json`, and two or three representative routes and server-function files. Record:

- `@tanstack/react-start` (or `solid-start`) version, bundler (Vite 8 or Rsbuild), hosting target;
- route style (flat dot files, directories, or mixed) and where non-route code lives;
- server-code convention (`*.server.ts`, `server/` folder, marker imports);
- data layer: loaders only, or TanStack Query via `@tanstack/react-router-ssr-query`;
- validation library (Zod v4/v3, Valibot, ArkType) and form library;
- auth provider/session library, if any;
- an embedded API (Elysia/Hono mounted on `/api/$`, Eden client), runtime (Node or Bun) and workspace layout (single package or monorepo).

**Version gate.** Start became stable in **1.169** (Oct 2026). Several APIs agents learned earlier changed then. Before writing code, read `references/version-notes.md` and use the APIs the installed version supports. When unsure of an API, check the current docs (`https://tanstack.com/start/latest/llms.txt`) instead of memory.

## The rule that drives every decision: code is isomorphic by default

Route files, components, **loaders and `beforeLoad` run on the server for the first request and in the browser on client navigation.** Only these are server-only:

- `createServerFn(...).handler(...)` bodies (the client gets an RPC stub);
- `server.handlers` of server routes, and request/function middleware `.server()` callbacks;
- `createServerOnlyFn(...)`, and files the import protection denies to the client (`*.server.*` by default).

So a secret, a DB client or a `process.env` read placed directly in a loader leaks or breaks. Put it behind a server function. Read `references/server-boundaries.md` for server functions, middleware, server routes, import protection, CSRF, env and serialization.

## Layering

Keep four responsibilities apart, whatever folder names the repo uses:

| Layer             | Holds                                                                                         | May import                 |
| ----------------- | --------------------------------------------------------------------------------------------- | -------------------------- |
| Route file        | path, `validateSearch`, `loaderDeps`, `beforeLoad`, `loader`, `head`, boundaries, composition | everything below           |
| `*.functions.ts`  | `createServerFn` wrappers: validate input, check authorization, call server code, return data | `*.server.ts`, schemas     |
| `*.server.ts`     | DB/SDK clients, secrets, queries, internal business logic                                     | other server code, schemas |
| client-safe `.ts` | schemas, inferred types, constants, `queryOptions` factories, pure helpers                    | nothing server-only        |

Static imports of `*.functions.ts` are safe anywhere; the compiler strips the handler and its server-only imports from the client build. Avoid dynamic `import()` of server-function modules.

For a new project, or when the repo has no convention yet, use the feature layout in `references/project-structure.md`. In an existing repo, extend its structure; do not reorganize folders unless asked.

## Routes

- Keep route files thin: declare behavior and compose feature components. No DB calls, no business rules.
- Use the router's conventions (`__root`, `index`, `$param`, `{-$param}`, `$` splat, `_pathless` layouts, `(group)` folders, `-ignored` colocated files, `route.tsx`). Cheat sheet in `references/project-structure.md`.
- Put auth gates in a pathless layout (`_authed.tsx`) with `beforeLoad` + `throw redirect(...)`. A guard is UX, not security: every server function and server route still authorizes.
- Give each route the states the user needs: `pendingComponent`, `errorComponent`, `notFoundComponent`, `throw notFound()` for missing resources.
- Use server routes (`createFileRoute(path)({ server: { handlers } })`) for external HTTP callers: webhooks, OAuth callbacks, public APIs, files, `sitemap[.]xml`. Inside the app, call server functions (or the embedded API's typed client).

## Data, mutations, validation

- Reads: the loader calls server functions (or `queryClient.query(options)` when Query is used). Await what determines content, title, redirects or existence; stream the rest.
- One owner per piece of data. With Query, create the `QueryClient` **inside `getRouter()`**, never at module scope, and share `queryOptions` between loader and component.
- Writes: POST server function with `.validator(schema)`, called through `useServerFn`, then invalidate the real owner (`queryClient.invalidateQueries` or `router.invalidate()`).
- Validate at every boundary: `validateSearch` and `params.parse` for URLs, `.validator()` for server-function input, `sendContext` and server-route bodies by hand. Shape validation is not authorization.

Read `references/data-and-validation.md` for loader/Query patterns, search params, forms with TanStack Form, auth and sessions.

## Embedded API (Elysia, Hono)

When an API framework is mounted inside Start, it becomes the app's API surface: features read and write through it (Eden client for Elysia), and server functions shrink to SSR glue. Never implement one operation both ways. The SSR side must call the app in memory **and forward the request's cookies**; the browser side calls the page origin. Elysia routes are outside Start's automatic CSRF protection and need their own. Read `references/embedded-api-elysia.md` for the mount, the isomorphic Eden client and its traps, contracts, auth and the Bun production entry.

## Rendering and hosting

SSR is the default. Pick per route: `ssr: false` for browser-only widgets, `'data-only'` when only the data needs the server, SPA mode or prerendering for static sites. Personalized responses send `Cache-Control: private, no-store`; only public pages get CDN caching. Read `references/rendering-and-deployment.md` for selective SSR, SPA, prerender, ISR headers, adapters (Nitro, Cloudflare, Netlify, Bun, Node) and the Next.js mapping.

## Validation before claiming done

Run the repo's real scripts (typecheck, lint, tests, `vite build`). Then, when you changed boundaries or data flow:

- build with a dummy secret and search the client output (`.output/public` or `dist/client`) for it;
- compare a direct page load with a client-side navigation to the same route;
- call changed server functions and server routes while signed out and as another user;
- check the response `Cache-Control` of personalized pages;
- watch the console for hydration mismatches and import-protection warnings.

Static review alone does not prove a boundary is safe.

## Common failure modes

- Treating loaders or `beforeLoad` as server-only (secrets, DB clients, `process.env` in them).
- `createServerOnlyFn` called from a loader: it throws on client navigation; use `createServerFn`.
- A module-scope `QueryClient`, DB session or user cache shared across SSR requests.
- Reading env at module scope (empty on edge runtimes; leaks if bundled for the client).
- Creating `src/start.ts` and forgetting to re-add `createCsrfMiddleware` for server functions.
- Using pre-1.169 APIs (`.inputValidator`, `useSession`, `registerGlobalMiddleware`, `app.config.ts`/Vinxi) on a current install.
- Business logic in route files, or the same rule duplicated in a loader, a server route and a hook.
- Calling the app's own server routes with `fetch` instead of server functions (or, with an embedded Elysia app, instead of Eden).
- An Eden client with a hard-coded `localhost` origin, or SSR calls that drop the user's cookies.
- `setResponseHeader('set-cookie', ...)`, which replaces all cookies; use `setCookie`.
- Public caching of HTML that depends on a cookie or the user.

## Optional companions

TanStack publishes official, version-pinned skills inside its npm packages (TanStack Intent): `npx @tanstack/intent@latest install`, or `npx skills add tanstack/router --skill start-core` (also `react-start`, `router-core`). They cover API detail; this skill owns architecture and boundaries. See `docs/COMPANION_SKILLS.md` at the repository root.

## Output

State the detected version, bundler and hosting target; the execution boundary of each file touched; the architectural decision and where code was placed; version-sensitive assumptions; validations run; and anything still unverified at runtime.
