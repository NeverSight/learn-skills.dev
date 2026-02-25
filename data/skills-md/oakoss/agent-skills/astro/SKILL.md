---
name: astro
description: |
  Astro web framework patterns for content-driven sites. Covers content collections with Zod schemas and loaders, island architecture with selective hydration directives, view transitions with ClientRouter, server-side and hybrid rendering modes, server islands, Astro DB with astro:db, middleware with onRequest, and framework integrations (React, Svelte, Vue).

  Use when building content-driven websites, configuring island hydration strategies, setting up view transitions, choosing between static and server rendering, integrating UI framework components, defining content collection schemas, or adding middleware.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://docs.astro.build'
user-invocable: false
---

# Astro

## Overview

Astro is an **all-in-one web framework** for building fast, content-focused websites. It uses an islands architecture that ships zero JavaScript by default, hydrating only interactive components on demand. Components from React, Svelte, Vue, Solid, and Preact can coexist in a single project.

**When to use:** Content-driven sites (blogs, docs, marketing), portfolios, e-commerce storefronts, any site where most pages are primarily static with isolated interactive regions.

**When NOT to use:** Highly interactive single-page applications (dashboards, real-time collaboration tools), apps requiring full client-side routing with shared global state across all components.

## Quick Reference

| Pattern                | API / Directive                                   | Key Points                                            |
| ---------------------- | ------------------------------------------------- | ----------------------------------------------------- |
| Content collection     | `defineCollection({ loader, schema })`            | Zod schemas, glob/file loaders, type-safe queries     |
| Query collection       | `getCollection('blog')`                           | Returns typed array, supports filter callback         |
| Single entry           | `getEntry('blog', 'my-post')`                     | Fetch by collection name and entry ID                 |
| Island (load)          | `<Component client:load />`                       | Hydrate immediately on page load                      |
| Island (idle)          | `<Component client:idle />`                       | Hydrate when browser is idle                          |
| Island (visible)       | `<Component client:visible />`                    | Hydrate when component enters viewport                |
| Island (media)         | `<Component client:media="(max-width: 768px)" />` | Hydrate on media query match                          |
| Island (client-only)   | `<Component client:only="react" />`               | Skip SSR, render only on client                       |
| View transitions       | `<ClientRouter />`                                | Add to `<head>`, enables SPA-like navigation          |
| Persist state          | `transition:persist`                              | Maintain island state across navigations              |
| Programmatic navigate  | `navigate(href)`                                  | Client-side navigation from scripts                   |
| Static output          | `output: 'static'`                                | Pre-render all pages at build time (default)          |
| Server output          | `output: 'server'`                                | Server-render all pages on demand                     |
| Hybrid (opt-in SSR)    | `output: 'static'` + per-page `prerender = false` | Static by default, opt individual pages into SSR      |
| Hybrid (opt-in static) | `output: 'server'` + per-page `prerender = true`  | SSR by default, opt individual pages into static      |
| Server islands         | `<Component server:defer />`                      | Defer server rendering for dynamic content in static  |
| Middleware             | `onRequest(context, next)`                        | Runs before every route, chain with `sequence()`      |
| Astro DB table         | `defineTable({ columns })`                        | Type-safe SQL with column definitions                 |
| Framework component    | Import `.jsx` / `.svelte` / `.vue`                | Auto-detected by file extension                       |
| Integration            | `astro add react`                                 | CLI to add framework adapters and tools               |
| Render content         | `const { Content } = await entry.render()`        | Compile Markdown/MDX to component                     |
| Dynamic routes         | `getStaticPaths()` + collection query             | Generate pages from collection entries                |
| API endpoint           | `export const GET: APIRoute`                      | Server-rendered REST endpoints                        |
| Shared island state    | `nanostores`                                      | Reactive state across framework boundaries            |
| Environment variables  | `import.meta.env.PUBLIC_*`                        | `PUBLIC_` prefix for client-accessible vars           |
| Transition animation   | `transition:animate="slide"`                      | `initial`, `fade`, `slide`, `none`                    |
| Prefetch links         | `data-astro-prefetch`                             | `hover`, `viewport`, `load`, or `false`               |
| Collection reference   | `reference('authors')`                            | Type-safe cross-collection relations                  |
| Script re-execution    | `data-astro-rerun`                                | Re-run `<script>` on every view transition navigation |
| Redirect               | `context.redirect(url, status)`                   | Redirect from middleware or server pages              |

## Common Mistakes

| Mistake                                           | Correct Pattern                                                           |
| ------------------------------------------------- | ------------------------------------------------------------------------- |
| Adding `client:` directive to `.astro` components | Only UI framework components (React, Svelte, Vue) accept `client:`        |
| Using `client:load` everywhere                    | Default to `client:idle` or `client:visible`; use `client:load` sparingly |
| Forgetting framework string with `client:only`    | Must specify framework: `client:only="react"`                             |
| Mixing framework components in non-Astro files    | Only `.astro` files can compose components from multiple frameworks       |
| Using `output: 'server'` for mostly static sites  | Use `output: 'static'` with per-page `prerender = false` for hybrid       |
| Omitting `<ClientRouter />` for view transitions  | Must be in `<head>` of every page (use shared layout)                     |
| Content config not at `src/content.config.ts`     | File must be named `content.config.ts` in `src/` root                     |
| Not awaiting `getCollection()` calls              | Always `await` collection queries in frontmatter                          |
| Importing from `astro:content` in client scripts  | Content APIs are server-only; pass data as props to client components     |
| Placing middleware outside `src/middleware.ts`    | Middleware must be at `src/middleware.ts` or `src/middleware/index.ts`    |
| Passing functions as props to islands             | Only serializable data crosses the server/client boundary                 |
| Using `transition:persist` without matching pages | Component must appear on both old and new page with same persist value    |
| Missing adapter for server/hybrid mode            | Install an adapter: `npx astro add vercel` (or node, netlify, etc.)       |

## Delegation

- **Pattern discovery**: Use `Explore` agent
- **Build configuration**: Use `Task` agent
- **Code review**: Delegate to `code-reviewer` agent

> If the `tailwind` skill is available, delegate styling and Tailwind CSS configuration to it.
> If the `vitest` skill is available, delegate unit testing patterns to it.
> If the `playwright` skill is available, delegate end-to-end testing patterns to it.
> If the `vite` skill is available, delegate build configuration and Vite plugin setup to it.
> If the `drizzle` skill is available, delegate advanced database query patterns to it.
> If the `sentry` skill is available, delegate error monitoring and observability setup to it.
> If the `pino-logging` skill is available, delegate server-side logging configuration to it.
> If the `tanstack-query` skill is available, delegate client-side data fetching and caching to it.

## References

- [Content collections, schemas, loaders, and querying](references/content-collections.md)
- [Island architecture and hydration directives](references/island-architecture.md)
- [View transitions and client-side navigation](references/view-transitions.md)
- [Rendering modes: static, server, and hybrid](references/rendering-modes.md)
- [Middleware patterns and request handling](references/middleware.md)
- [Framework component integration (React, Svelte, Vue)](references/framework-integration.md)
- [Astro DB schema, seeding, and queries](references/astro-db.md)
