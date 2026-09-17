---
name: composition-patterns
description: React composition patterns that scale. Use when refactoring boolean-prop APIs, building reusable component libraries, or reviewing compound components, render props, and context. Includes React 19 API changes.
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# React Composition Patterns

Composition patterns for building flexible, maintainable React components. Avoid boolean prop proliferation by using compound components, lifting state, and composing internals. Upstream: `composition-patterns` in [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills).

## Scope

- Applies to: reusable component APIs, compound components, explicit variants, React 19 ref/`use()` changes
- Does NOT cover: visual direction ([frontend-design](../frontend-design/SKILL.md)); Next.js caching or RSC data fetching ([next-v16](../next-v16/SKILL.md), [vercel-react](../vercel-react/SKILL.md))

## Assumptions

- React 19+ in typical Basilic apps; skip the React 19 rule section on React 18
- Server/client boundaries already exist; composition must not move server data into client-only providers

## Principles

- Prefer composition over boolean configuration for reused components
- Lift client UI state only when siblings need it; keep server data on the server
- Extract shared primitives after a second call site, not for one-off route UI

## Constraints

### MUST

- Extract compound components only for a shared UI package or 2+ call sites, not a single route leaf
- Keep React Server Components fetching their own data; pass server-rendered children into client leaves instead of lifting that data into a client provider
- Leave URL-shareable state, async server state, and grouped local UI state on the libraries the project already uses (query-string parsers, TanStack Query, grouped-state hooks)—do not replace them with a generic context DI layer

### SHOULD

- Skip `forwardRef` unless a parent must attach a ref
- Use explicit variant components instead of `isX` boolean modes on reused APIs
- Prefer `children` over `renderX` props

### AVOID

- Premature abstractions around a one-off screen
- Client providers whose only job is to re-export RSC-fetched props
- Breaking existing `'use client'` placement to “compose” everything

## Interactions

- App Router / RSC: [next-v16](../next-v16/SKILL.md)
- React performance: [vercel-react](../vercel-react/SKILL.md)
- shadcn primitives: [shadcn-v3](../shadcn-v3/SKILL.md)
- URL state: [nuqs-v2](../nuqs-v2/SKILL.md)
- Client async: [tanstack-query-v5](../tanstack-query-v5/SKILL.md)
- Grouped local state: [ahooks-v3](../ahooks-v3/SKILL.md)

## When to apply

- Refactoring components with many boolean props
- Building reusable component libraries
- Designing flexible component APIs
- Reviewing component architecture
- Working with compound components or context providers

## Rule categories by priority

| Priority | Category | Impact | Prefix |
| --- | --- | --- | --- |
| 1 | Component Architecture | HIGH | `architecture-` |
| 2 | State Management | MEDIUM | `state-` |
| 3 | Implementation Patterns | MEDIUM | `patterns-` |
| 4 | React 19 APIs | MEDIUM | `react19-` |

## Quick reference

### 1. Component Architecture (HIGH)

- `architecture-avoid-boolean-props` — Don't add boolean props to customize behavior; use composition
- `architecture-compound-components` — Structure complex components with shared context

### 2. State Management (MEDIUM)

- `state-decouple-implementation` — Provider is the only place that knows how state is managed
- `state-context-interface` — Define generic interface with state, actions, meta for dependency injection
- `state-lift-state` — Move state into provider components for sibling access

Apply these only where the Constraints above allow. Do not lift server-owned data.

### 3. Implementation Patterns (MEDIUM)

- `patterns-explicit-variants` — Create explicit variant components instead of boolean modes
- `patterns-children-over-render-props` — Use children for composition instead of renderX props

### 4. React 19 APIs (MEDIUM)

React 19+ only. Skip this section on React 18 or earlier.

- `react19-no-forwardref` — Don't use `forwardRef` for new components. `use()` is optional for conditional context reads; `useContext()` remains supported.

## How to use

Read individual rule files for detailed explanations and code examples:

```
rules/architecture-avoid-boolean-props.md
rules/state-context-interface.md
```

Each rule file contains why it matters, incorrect and correct examples, and extra context.

Full compiled guide (do not name this `AGENTS.md`; Cursor always-loads that filename): [references/compiled.md](references/compiled.md)
