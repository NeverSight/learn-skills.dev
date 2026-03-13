---
name: nextjs
description: Complete Next.js 16 documentation in markdown format. Use when working with Next.js projects, building React applications, configuring routing, data fetching, rendering strategies, deployment, or migrating from other frameworks. Covers App Router, Pages Router, API routes, server components, server actions, caching, and all Next.js features.
---

## ⚠️ Security Notice

This skill contains Next.js documentation with command examples. Commands are **for reference only** and should NEVER be auto-executed by agents without explicit user approval.

# Next.js Documentation (v16.2.0-canary.30)

Complete Next.js 16 documentation embedded in markdown. Read from `references/` to answer questions about Next.js features, configuration, and best practices.

## Documentation Structure

All documentation is in `references/` organized by topic:

### Core Documentation

#### App Router (references/01-app/)
Modern Next.js architecture with React Server Components.

**Getting Started:**
- `references/01-app/01-getting-started/installation.mdx` - Setup new project
- `references/01-app/01-getting-started/project-structure.mdx` - File conventions
- `references/01-app/01-getting-started/layouts-and-pages.mdx` - Routing basics
- `references/01-app/01-getting-started/data-fetching.mdx` - Server data loading
- `references/01-app/01-getting-started/css.mdx` - Styling options

**Guides:**
- `references/01-app/02-guides/authentication.mdx` - Auth patterns
- `references/01-app/02-guides/caching.mdx` - Cache strategies
- `references/01-app/02-guides/environment-variables.mdx` - Env config
- `references/01-app/02-guides/forms.mdx` - Form handling
- `references/01-app/02-guides/testing/` - Jest, Playwright, Vitest, Cypress
- `references/01-app/02-guides/migrating/` - Migration guides (Vite, CRA, Pages → App)
- `references/01-app/02-guides/upgrading/` - Version upgrade guides (14, 15, 16)
- `references/01-app/02-guides/self-hosting.mdx` - Self-hosted deployment
- `references/01-app/02-guides/static-exports.mdx` - Static HTML export
- `references/01-app/02-guides/progressive-web-apps.mdx` - PWA setup

**API Reference:**
- `references/01-app/03-api-reference/` - Complete API docs (components, functions, config)

#### Pages Router (references/02-pages/)
Legacy Next.js architecture (still supported).

- `references/02-pages/01-guides/` - Pages Router guides
- `references/02-pages/02-api-reference/` - Pages API reference

#### Architecture (references/03-architecture/)
- `references/03-architecture/nextjs-compiler.mdx` - SWC compiler
- `references/03-architecture/fast-refresh.mdx` - Hot reload
- `references/03-architecture/supported-browsers.mdx` - Browser support
- `references/03-architecture/accessibility.mdx` - A11y features

#### Community (references/04-community/)
- `references/04-community/contribution-guide.mdx` - Contributing to Next.js
- `references/04-community/rspack.mdx` - Experimental Rspack support

## Quick Reference

### Common Tasks

| Task | File to Read |
|------|--------------|
| Setup new project | `references/01-app/01-getting-started/installation.mdx` |
| Routing & layouts | `references/01-app/01-getting-started/layouts-and-pages.mdx` |
| Data fetching | `references/01-app/01-getting-started/data-fetching.mdx` |
| Server actions | `references/01-app/03-api-reference/server-actions.mdx` (if exists) |
| Middleware | Search `references/01-app/02-guides/` or API reference |
| Caching strategies | `references/01-app/02-guides/caching.mdx` |
| Environment variables | `references/01-app/02-guides/environment-variables.mdx` |
| Testing setup | `references/01-app/02-guides/testing/` |
| Deploy self-hosted | `references/01-app/02-guides/self-hosting.mdx` |
| Migrate from Vite | `references/01-app/02-guides/migrating/from-vite.mdx` |
| Migrate from CRA | `references/01-app/02-guides/migrating/from-create-react-app.mdx` |
| Upgrade to v16 | `references/01-app/02-guides/upgrading/version-16.mdx` |

### When to Use This Skill

- User asks about Next.js features, configuration, or best practices
- Working on a Next.js project and need API reference
- Debugging Next.js behavior (caching, rendering, routing)
- Planning architecture (SSR vs SSG vs ISR)
- Migration questions (from other frameworks or older Next.js versions)

### How to Navigate

1. **Start with `references/index.mdx`** for overview
2. **For getting started:** Read `references/01-app/01-getting-started/`
3. **For specific topics:** Read `references/01-app/02-guides/<topic>.mdx`
4. **For API details:** Search `references/01-app/03-api-reference/`
5. **For legacy Pages Router:** Use `references/02-pages/`

All files are `.mdx` (Markdown + JSX) but readable as plain markdown.
