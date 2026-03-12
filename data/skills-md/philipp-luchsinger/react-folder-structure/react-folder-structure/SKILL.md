---
name: react-folder-structure
description: >
  Opinionated React + Vite + TypeScript + shadcn/ui project structure, conventions,
  and setup guide. Use this skill when bootstrapping a new project, creating a new
  feature, wiring up API calls with TanStack Query + Axios, or managing state with
  Zustand. Enforces self-contained features, a typed API layer, and theme-aware
  Tailwind v4 styling via CSS variables.
license: MIT
metadata:
  author: philipp-luchsinger
  version: "1.0.0"
---

# React Folder Structure & Conventions

Opinionated setup guide and coding conventions for React + Vite + TypeScript + shadcn/ui projects.

## When to Apply

Reference these guidelines when:
- Bootstrapping a **new project from scratch**
- Creating a **new feature** inside `components/features/`
- Adding a **new API domain** (TanStack Query + Axios)
- Creating or scoping a **Zustand store**
- Adding a **shadcn/ui component**
- Deciding where a file or hook belongs in the project

## Rule Categories

| Category | Area | Prefix |
|----------|------|--------|
| Project Setup | Bootstrapping Vite + Tailwind + shadcn | `setup-` |
| Folder Structure | Top-level `src/` layout | `structure-` |
| Features | Self-contained feature architecture | `feature-` |
| API Layer | Axios + TanStack Query conventions | `api-` |
| State Management | Zustand (global & scoped) | `store-` |
| Styling | Tailwind v4 + CSS design tokens | `style-` |
| Naming | File, component & hook naming conventions | `naming-` |

## Quick Reference

### Setup
- `setup-vite` — Scaffold Vite + React + TypeScript + Tailwind v4 + path aliases
- `setup-shadcn` — Initialize shadcn/ui and never edit generated ui components

### Features
- `feature-structure` — Self-contained feature directory layout
- `feature-components` — What goes in `components/` vs `shared/`
- `feature-boundaries` — Features may only import each other's root export

### API
- `api-client` — Single Axios instance in `api/client.ts`
- `api-endpoints` — Centralized endpoint constants, never hardcode URLs
- `api-query-hooks` — Query key factories + TanStack Query hook patterns
- `api-domain-folder` — One folder per domain with `use<Domain>Api.ts` + `types.ts`

### State
- `store-global` — `src/stores/` for app-wide state only
- `store-scoped` — Context-scoped `createStore()` pattern for feature-local state

### Styling
- `style-tokens` — Always use CSS variable tokens, never raw Tailwind color utilities
- `style-dark-mode` — Dark mode via `.dark` class + `@custom-variant`

## Full Reference

For detailed explanations and Incorrect/Correct code examples for every rule: `AGENTS.md`

Individual rule files are in `rules/`.
