---
name: code-style
description: "Personal TypeScript/React code style preferences including naming conventions, formatting rules, and review severity labels. Use this skill when: (1) Writing new TypeScript/React code, (2) Reviewing code or PRs, (3) Refactoring existing code, (4) Setting up linting/formatting configuration."
---

# Code Style Guide

Personal code style preferences for TypeScript/React development.

## Core Principles

- Prefer the simplest viable solution; readability > cleverness
- Add complexity only when clearly warranted (scale, correctness, security)
- When uncertain, state assumptions and open questions instead of guessing

## Output Format

- Lead with the answer, then brief explanation
- Match depth to complexity - don't over-explain simple things
- For larger designs/refactors: summary → trade-offs → next steps

## Code Style

### Formatting (Prettier)
- 2-space indent
- Single quotes (including JSX)
- No semicolons
- Named exports (not default exports)
- Auto-organized imports (prettier-plugin-organize-imports)
- Auto-sorted Tailwind classes (prettier-plugin-tailwindcss)

### Naming Conventions
- **PascalCase**: Components, Types, Interfaces
- **camelCase**: Functions, variables, hooks
- **UPPER_SNAKE_CASE**: Constants

### TypeScript
- Precise TS types; avoid `any` unless necessary (explain why)
- Prefer `??` over `||` for nullish coalescing
- Prefer explicit null checks over loose truthiness
- Use strict mode
- Consistent type imports: `import { type Foo }` (inline-type-imports)
- Exhaustive switch statements (`@typescript-eslint/switch-exhaustiveness-check`)
- Unused vars with underscore prefix allowed (`_unused`)

### ESLint Rules (Enforced)
- `eqeqeq: smart` - Use strict equality (except null checks)
- `no-console` - Only `console.warn` and `console.error` allowed
- `consistent-type-imports` - Inline type imports
- `switch-exhaustiveness-check` - All switch cases must be handled
- `no-unused-vars` - Underscore prefix (`_`) ignores args/vars
- `no-misused-promises` - Except void return in JSX attributes

### Code Organization
- Inline until a pattern repeats 3+ times
- For new components/hooks/APIs: include a usage example
- Co-locate related code

## React Patterns

- Functional components only
- Composition over configuration
- Co-location of related code

### State Management
- Prefer derived/declarative state
- Avoid useEffect unless truly needed for side effects or external sync
- State progression: useState → Context → Zustand (when needed)

### Hooks
- Custom hooks start with `use`
- Exhaustive deps (understand when to override)

## Code Review

### Severity Labels
- **critical**: Must fix - security, data loss, crashes
- **major**: Should fix - bugs, significant issues
- **minor**: Nice to fix - style, minor improvements

### Review Approach
- Prefer minimal diffs
- Flag unnecessary complexity with simpler alternative
- Proactively flag security issues with brief explanation and fix
- Note accessibility and SEO concerns when relevant

## Stack-Specific

### Next.js
- App Router patterns
- Proper server/client boundaries
- Optimize for both SSR and CSR contexts

### tRPC
- Input validation with Zod
- Proper error handling
- Type-safe returns

### TanStack Query
- Meaningful query keys
- Appropriate staleTime
- Proper cache invalidation

### AG Grid
- Type-safe column definitions
- Performance-conscious cell renderers
- Proper SSRM implementation for large datasets
