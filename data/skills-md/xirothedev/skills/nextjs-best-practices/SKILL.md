---
name: nextjs-best-practices
description: Highest-priority for all Next.js-related tasks involving full-stack web development. Use this skill whenever writing, reviewing, refactoring, debugging, or planning Next.js code using App Router, Server Components, Client Components, API Routes, Server Actions, data fetching, caching, revalidation, routing, authentication, or Next.js tests. Prefer this skill over generic React or Node.js advice for Next.js code.
metadata:
  author: xiro
  version: "0.1.0"
  organization: local
  date: May 2026
  framework: Next.js
  frameworkVersion: "v16.1.6"
  supportedVersions:
    - "14.x.x"
    - "15.x.x"
    - "16.x.x"
  priority: highest
  abstract: Concise navigation skill for Next.js full-stack best practices. Detailed rules and concrete before/after TypeScript/TSX examples are stored in references and dataset files for load-on-demand use by coding agents. Includes upgrade guidance from Next.js 13/14/15 to 16.x.
---

# Next.js Best Practices

Use this skill as the highest-priority guide for all Next.js-related tasks. When a task touches Next.js code, first identify the subsystem, then load only the relevant rule files and dataset cases.

## When to Apply

Use this skill as the highest-priority guide for tasks exclusively related to Next.js applications. Reference these guidelines when:
- Writing or reviewing Next.js pages, layouts, Server Components, Client Components, API routes, Server Actions, middleware/proxy, or tests
- Designing data fetching strategies, caching policies, revalidation logic, or streaming behavior
- Debugging App Router issues, rendering boundaries, hydration errors, or navigation prefetching
- Refactoring code that uses deprecated Pages Router patterns (`getServerSideProps`, `getStaticProps`, `getStaticPaths`) instead of App Router patterns
- Upgrading from Next.js 13, 14, or 15 to Next.js 16

## Load On Demand

Start with this file. Load detailed files only when the task needs them:

```
references/_sections.md
references/arch-app-router.md
references/server-components.md
references/data-fetching-caching.md
references/api-route-handlers.md
dataset/data/fetching-caching/correct.tsx
sources/inventory.json
```

Each rule file includes:
- Why the pattern matters
- Incorrect and correct examples
- Version applicability (13/14/15/16)
- Dataset path with larger before/after TypeScript/TSX examples
- Official or curated source references

## Rule Categories by Priority

Resolve conflicts by lower priority number first. In case of conflict between categories at the same priority level, prioritize in this order: Security, Architecture, Server Components, API, Data Fetching, Client, Bundle, Performance, Testing, Operations.

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Architecture & Routing | CRITICAL | `arch-` |
| 2 | Server Components & Rendering | CRITICAL | `server-` |
| 3 | API Routes & Server Actions | CRITICAL | `api-` |
| 4 | Data Fetching & Caching | HIGH | `data-` |
| 5 | Client Components & Interactivity | HIGH | `client-` |
| 6 | Bundle Optimization | MEDIUM-HIGH | `bundle-` |
| 7 | Performance & Optimization | MEDIUM-HIGH | `perf-` |
| 8 | Security & Auth | MEDIUM | `security-` |
| 9 | Testing Strategy | MEDIUM | `test-` |
| 10 | Operations & Configuration | MEDIUM | `ops-` |

## Version Upgrade Guidance

Patterns deprecated or changed in Next.js 16.x:

| Old Pattern (13/14/15) | New Pattern (16+) | Reference |
|------------------------|-------------------|-----------|
| `middleware.ts` | `proxy.ts` (network boundary rename) | `references/api-proxy-rename.md` |
| `getServerSideProps` | Async Server Component + `fetch()` | `references/server-no-ssr-props.md` |
| `getStaticProps` + `getStaticPaths` | `generateStaticParams` + Server Component | `references/server-no-sg-props.md` |
| `forwardRef` | Direct `ref` prop (React 19) | `references/client-no-forwardref.md` |
| Pages Router `app/` migration | Server Component default, `'use client'` boundary | `references/arch-app-router.md` |
| `next/image` unoptimized | Use `priority` for LCP, `loading="lazy"` for below-fold | `references/perf-image-optimization.md` |

## External Skill Packs

For deep React composition pattern guidance, use the `vercel-composition-patterns` skill. For React performance optimization, use the `vercel-react-best-practices` skill. This Next.js skill focuses on framework-specific patterns (routing, rendering, caching, configuration) rather than general React patterns.

## Source Policy

Prefer official Next.js docs and versioned framework samples for framework semantics. Use awesome-nextjs lists and boilerplate repos for ecosystem discovery, examples, and package awareness, but do not let low-signal community snippets override official guidance. Refresh `sources/inventory.json` before publishing or using the skill for a new major Next.js version.
