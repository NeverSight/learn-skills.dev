---
name: nextjs-best-practices
description: "Next.js App Router best practices — file conventions, RSC boundaries, data patterns, async APIs, metadata, error handling, route handlers, image/font optimization, bundling. Use when writing, reviewing, or debugging Next.js App Router code."
---

# Next.js Best Practices

Apply these rules when writing or reviewing Next.js code.

> **Note:** Next.js 16 renamed `middleware.ts` to `proxy.ts`. Verify `proxy.ts` support in your version; `middleware.ts` remains the stable API.

## Table of Contents

- [File Conventions](#file-conventions)
- [RSC Boundaries](#rsc-boundaries)
- [Async Patterns](#async-patterns)
- [Runtime Selection](#runtime-selection)
- [Directives](#directives)
- [Functions](#functions)
- [Error Handling](#error-handling)
- [Data Patterns](#data-patterns)
- [Route Handlers](#route-handlers)
- [Metadata & OG Images](#metadata--og-images)
- [Image Optimization](#image-optimization)
- [Font Optimization](#font-optimization)
- [Bundling](#bundling)
- [Scripts](#scripts)
- [Hydration Errors](#hydration-errors)
- [Suspense Boundaries](#suspense-boundaries)
- [Parallel & Intercepting Routes](#parallel--intercepting-routes)
- [Self-Hosting](#self-hosting)
- [Debug Tricks](#debug-tricks)

## File Conventions

See [file-conventions.md](references/file-conventions.md) for:

- Project structure and special files
- Route segments (dynamic, catch-all, groups)
- Parallel and intercepting routes
- Middleware rename in v16 (middleware → proxy)

## RSC Boundaries

Detect invalid React Server Component patterns.

See [rsc-boundaries.md](references/rsc-boundaries.md) for:

- Async client component detection (invalid)
- Non-serializable props detection
- Server Action exceptions

## Async Patterns

Next.js 16.1.6+ async API changes.

See [async-patterns.md](references/async-patterns.md) for:

- Async `params` and `searchParams`
- Async `cookies()` and `headers()`
- Migration codemod

## Runtime Selection

See [runtime-selection.md](references/runtime-selection.md) for:

- Default to Node.js runtime
- When Edge runtime is appropriate

## Directives

See [directives.md](references/directives.md) for:

- `'use client'`, `'use server'` (React)
- `'use cache'` (Next.js)

## Functions

See [functions.md](references/functions.md) for:

- Navigation hooks: `useRouter`, `usePathname`, `useSearchParams`, `useParams`
- Server functions: `cookies`, `headers`, `draftMode`, `after`
- Generate functions: `generateStaticParams`, `generateMetadata`

## Error Handling

See [error-handling.md](references/error-handling.md) for:

- `error.tsx`, `global-error.tsx`, `not-found.tsx`
- `redirect`, `permanentRedirect`, `notFound`
- `forbidden`, `unauthorized` (auth errors)
- `unstable_rethrow` for catch blocks

## Data Patterns

See [data-patterns.md](references/data-patterns.md) for:

- Server Components vs Server Actions vs Route Handlers
- Avoiding data waterfalls (`Promise.all`, Suspense, preload)
- Client component data fetching

## Route Handlers

See [route-handlers.md](references/route-handlers.md) for:

- `route.ts` basics
- GET handler conflicts with `page.tsx`
- Environment behavior (no React DOM)
- When to use vs Server Actions

## Metadata & OG Images

See [metadata.md](references/metadata.md) for:

- Static and dynamic metadata
- `generateMetadata` function
- OG image generation with `next/og`
- File-based metadata conventions

## Image Optimization

See [image.md](references/image.md) for:

- Always use `next/image` over `<img>`
- Remote images configuration
- Responsive `sizes` attribute
- Blur placeholders
- Priority loading for LCP

## Font Optimization

See [font.md](references/font.md) for:

- `next/font` setup
- Google Fonts, local fonts
- Tailwind CSS integration
- Preloading subsets

## Bundling

See [bundling.md](references/bundling.md) for:

- Server-incompatible packages
- CSS imports (not link tags)
- Polyfills (already included)
- ESM/CommonJS issues
- Bundle analysis

## Scripts

See [scripts.md](references/scripts.md) for:

- `next/script` vs native script tags
- Inline scripts need `id`
- Loading strategies
- Google Analytics with `@next/third-parties`

## Hydration Errors

See [hydration-error.md](references/hydration-error.md) for:

- Common causes (browser APIs, dates, invalid HTML)
- Debugging with error overlay
- Fixes for each cause

## Suspense Boundaries

See [suspense-boundaries.md](references/suspense-boundaries.md) for:

- CSR bailout with `useSearchParams` and `usePathname`
- Which hooks require Suspense boundaries

## Parallel & Intercepting Routes

See [parallel-routes.md](references/parallel-routes.md) for:

- Modal patterns with `@slot` and `(.)` interceptors
- `default.tsx` for fallbacks
- Closing modals correctly with `router.back()`

## Self-Hosting

See [self-hosting.md](references/self-hosting.md) for:

- `output: 'standalone'` for Docker
- Cache handlers for multi-instance ISR
- What works vs needs extra setup

## Debug Tricks

See [debug-tricks.md](references/debug-tricks.md) for:

- MCP endpoint for AI-assisted debugging
- Rebuild specific routes with `--debug-build-paths`
