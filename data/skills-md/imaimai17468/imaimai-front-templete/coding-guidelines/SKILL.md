---
name: coding-guidelines
description: Provides React/Next.js component guidelines focusing on testability, Server Components, entity/gateway pattern, and directory structure. Use when implementing components, refactoring code, organizing project structure, extracting conditional branches, or ensuring code quality standards.
---

# Coding Guidelines

Guidelines for React/Next.js development focusing on testability, Server Components, and proper architecture. Each guideline file contains principles, code examples, and anti-patterns to avoid.

---

## Quick Reference

- **Server Components & Data Fetching** → [server-components.md](server-components.md)
- **Testability & Props Control** → [testability.md](testability.md)
- **useEffect Guidelines & Dependencies** → [useeffect-guidelines.md](useeffect-guidelines.md)
- **Architecture & Patterns** → [architecture.md](architecture.md)
- **Test Guidelines (Vitest/RTL)** → [test-guidelines.md](test-guidelines.md)
- **Storybook Guidelines** → [storybook-guidelines.md](storybook-guidelines.md)

---

## When to Use What

### Server Components

**When**: Writing server-side data fetching or async components
**Read**: [server-components.md](server-components.md)

Key topics:
- Server Component Pattern (async/await, Suspense)
- Promise Handling (.then().catch() vs try-catch)
- When NOT to use "use client"

### Testability

**When**: Writing "use client" components, useEffect, or event handlers
**Read**: [testability.md](testability.md)

Key topics:
- Props Control (all states controllable via props)
- Closure Variable Dependencies (extract to pure functions)
- Conditional Branch Extraction (JSX → components, useEffect → pure functions)

### useEffect Guidelines & Dependencies

**When**: Deciding whether to use useEffect, managing dependencies, or avoiding unnecessary re-renders
**Read**: [useeffect-guidelines.md](useeffect-guidelines.md)

Key topics:
- When you DON'T need useEffect (data transformation, expensive calculations)
- When you DO need useEffect (external system synchronization)
- Event handlers vs Effects decision framework
- Data fetching patterns and race conditions
- Separating reactive and non-reactive logic
- Managing dependencies (updater functions, useEffectEvent, avoiding objects/functions)
- Reactive values and dependency array rules
- Never suppress the exhaustive-deps linter

### Architecture

**When**: Creating files, functions, or organizing code structure
**Read**: [architecture.md](architecture.md)

Key topics:
- Directory Structure (component collocation, naming)
- Entity/Gateway Pattern (data types and fetching)
- Function Extraction (action-based design)
- Presenter Pattern (conditional text)

### Test Guidelines

**When**: Creating or updating test code during Phase 2 (Testing & Stories)
**Read**: [test-guidelines.md](test-guidelines.md)

Key topics:
- AAA Pattern (Arrange-Act-Assert)
- Test Structure (describe/test descriptions in Japanese)
- Coverage Standards (branch coverage, exception paths)
- React Testing Library best practices
- Snapshot testing guidelines

### Storybook Guidelines

**When**: Creating Storybook stories for components with conditional rendering during Phase 2 (Testing & Stories)
**Read**: [storybook-guidelines.md](storybook-guidelines.md)

Key topics:
- Story Creation Rules (conditional branching focus)
- Meta Configuration (minimal setup)
- Event Handlers (fn() usage)
- Anti-patterns to avoid

---

## Core Principles

1. **Server Component First**: Default to Server Components, use "use client" only when necessary
2. **Props Control Everything**: All UI states must be controllable via props for testability
3. **Pure Functions**: Extract all conditional logic from useEffect/handlers
4. **No Closure Dependencies**: Pass all variables as function arguments
5. **Entity/Gateway Pattern**: Separate data types (entity) from fetching logic (gateway)
6. **Collocate Functions**: Place function files at same level as components, no utils/ directories

---

## Quick Decision Tree

```
Are you writing a component?
├─ Does it need interactivity? (onClick, useState, useEffect)
│  ├─ YES → "use client" required
│  │  ├─ Using useEffect?
│  │  │  └─ Read: useeffect-guidelines.md (Do you really need it? + Managing dependencies)
│  │  └─ Read: testability.md
│  └─ NO → Server Component (default)
│     └─ Read: server-components.md
│
├─ Does it fetch data?
│  └─ Read: server-components.md + architecture.md (Entity/Gateway)
│
├─ Are you organizing files/functions?
│  └─ Read: architecture.md (Directory Structure)
│
├─ Are you writing tests?
│  └─ Read: test-guidelines.md (AAA Pattern, Coverage, RTL)
│
└─ Are you creating Storybook stories?
   └─ Read: storybook-guidelines.md (Conditional Branching, Story Structure)
```
