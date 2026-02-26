---
name: bulletproof-react-patterns
description: Bulletproof React architecture patterns for scalable, maintainable applications. Covers feature-based project structure, component patterns, state management boundaries, API layer design, error handling, security, and testing strategies. Use when structuring a React project, designing application architecture, organizing features, or when the user asks about React project structure or scalable patterns.
---

# Bulletproof React Patterns

Architecture patterns for building scalable, maintainable React applications. Based on [bulletproof-react](https://github.com/alan2207/bulletproof-react).

## Core References

| Topic                | Description                                                                     | Reference                                                      |
| -------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Project Structure    | Feature-based organization, unidirectional architecture, ESLint enforcement     | [project-structure](references/project-structure.md)           |
| Components & Styling | Component hierarchy, wrapping 3rd party libs, headless vs styled libraries      | [components-and-styling](references/components-and-styling.md) |
| API Layer            | API client, request declarations, query/mutation hook patterns                  | [api-layer](references/api-layer.md)                           |
| State Management     | Component, application, server cache, form, and URL state categories            | [state-management](references/state-management.md)             |
| Error Handling       | Error boundaries, API errors, error tracking with Sentry                        | [error-handling](references/error-handling.md)                 |
| Testing              | Unit, integration, e2e strategies with Vitest, Testing Library, Playwright, MSW | [testing](references/testing.md)                               |
| Project Standards    | ESLint, Prettier, TypeScript, Husky, absolute imports, file naming              | [project-standards](references/project-standards.md)           |
| Security             | Authentication, token storage, XSS prevention, RBAC/PBAC authorization          | [security](references/security.md)                             |
| Performance          | Code splitting, data prefetching, state optimization, children pattern          | [performance](references/performance.md)                       |

## Project Structure

Organize by feature, not by file type:

```
src/
├── app/                # Application shell (routes, providers, router)
├── assets/             # Static files (images, fonts)
├── components/         # Shared, reusable UI components
├── config/             # Environment variables, constants
├── features/           # Feature-based modules
├── hooks/              # Shared custom hooks
├── lib/                # Pre-configured library wrappers
├── stores/             # Global client state
├── testing/            # Test utilities, MSW handlers, factories
├── types/              # Shared TypeScript types
└── utils/              # Pure utility functions
```

### Feature Modules

```
features/users/
├── api/            # API functions and query hooks
├── components/     # Feature-specific components
├── hooks/          # Feature-specific hooks
├── types/          # Feature-specific types
└── utils/          # Feature-specific utilities
```

**Rules:**

- Features should not import from other features. Compose at the app level.
- Code flows one direction: **shared → features → app**.
- Promote to shared directories only when reused by 2+ features.
- Prefer direct imports over barrel re-exports for Vite tree-shaking.

## Component Hierarchy

```
Page Components          → route-level, compose features, handle layout
  └── Feature Components → feature-specific, business logic
        └── UI Components      → shared primitives, no business logic
```

## API Layer Pattern

```typescript
// Pure API function
function getUsers(params?: GetUsersParams): Promise<UsersResponse> {
    return api.get("/users", { params });
}

// Query hook wrapping the API function
function useUsers(params?: GetUsersParams) {
    return useQuery({
        queryKey: ["users", params],
        queryFn: () => getUsers(params),
    });
}
```

## State Management Boundaries

| State Type            | Solution                   | Examples                              |
| --------------------- | -------------------------- | ------------------------------------- |
| Server state          | TanStack Query             | User data, posts, API responses       |
| Client state (global) | Zustand / Jotai            | Theme, sidebar open, user preferences |
| Client state (local)  | useState / useReducer      | Form inputs, toggles, modal open      |
| URL state             | URL search params / router | Filters, pagination, active tab       |
| Form state            | React Hook Form            | Multi-step forms, validation          |

**Don't mix server and client state.** Never copy query data into `useState`.

## Error Hierarchy

```
App Error Boundary          → catches unrecoverable crashes
  └── Route Error Boundary     → catches route-level failures, shows retry
        └── Feature Error Boundary   → catches feature-specific errors
```

## Testing Strategy

| Layer       | Tool                  | What to Test                                    |
| ----------- | --------------------- | ----------------------------------------------- |
| Components  | Testing Library       | Render output, user interactions, a11y          |
| Hooks       | renderHook            | State changes, side effects                     |
| API         | MSW                   | Request/response handling, error states         |
| Integration | Testing Library + MSW | Full feature flows (render → interact → verify) |
| E2E         | Playwright            | Critical user journeys                          |

## Conventions

| Item        | Convention              | Example                   |
| ----------- | ----------------------- | ------------------------- |
| Components  | PascalCase              | `UserCard.tsx`            |
| Hooks       | camelCase, `use` prefix | `useUsers.ts`             |
| Utilities   | camelCase               | `formatDate.ts`           |
| Types       | PascalCase              | `User`, `CreateUserInput` |
| Constants   | UPPER_SNAKE_CASE        | `MAX_RETRIES`             |
| Directories | kebab-case              | `user-settings/`          |
| Files       | kebab-case              | `user-card.tsx`           |

### Imports

Use path aliases to avoid deep relative imports:

```typescript
import { Button } from "@/components/ui/button";
import { useUsers } from "@/features/users/api";
```

Configure `@/` as the `src/` alias in `tsconfig.json`.
