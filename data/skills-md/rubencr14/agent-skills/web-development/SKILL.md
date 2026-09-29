---
name: web-development
description: Architecture, patterns, and code organization for Next.js and React applications. Use this skill whenever the user is building a frontend feature, structuring a React/Next.js project, deciding how to organize components, creating data-fetching layers, setting up repository patterns, working with DTOs and mappers, or making any architectural decision about a web application codebase. Covers feature-first organization, clean architecture lite, ports and adapters, server/client component boundaries, state management, error handling, and TypeScript contracts. This is about code structure and maintainability — not visual design (see frontend-design) or test mechanics (see web-testing).
---

## Philosophy

This skill takes a clear stance on how to build frontend applications that last:

**Feature-first + App Router + Server Components by default + Clean Architecture lite + Ports & Adapters + Mappers + Vitest/RTL + Playwright**

Three principles drive every decision:

1. **Feature ownership.** Every feature owns its folder, its layers, its types, and its tests. The folder structure should tell you what the application does, not what framework it uses.
2. **Decouple from the backend.** The UI never consumes raw API responses. Repositories implement interfaces. Mappers translate between layers. Swap REST for GraphQL and only infrastructure/ changes.
3. **Composition over ceremony.** Factory functions, not IoC containers. Props and children, not inheritance. Local state first, global state last. Keep it lightweight.

---

## Decision Tree — Where Does This Code Go?

```
What am I building?
|
+-- New feature or major capability
|     +-- Create a feature folder in src/features/
|           +-- Use the 4-layer structure: domain/ application/ infrastructure/ components/
|           (references/deep-dive.md)
|
+-- Data-fetching or backend integration
|     +-- Repository interface in domain/, implementation in infrastructure/
|           +-- Wire with factory functions (references/deep-dive.md)
|
+-- UI component
|     +-- Server or Client?
|           +-- No interactivity needed -> Server Component (default)
|           +-- useState / onClick / forms / drag-and-drop -> Client Component
|           (references/deep-dive.md)
|
+-- Transforming API data for the UI
|     +-- DTO type in infrastructure/, ViewModel type + mapper function
|           (references/deep-dive.md)
|
+-- Handling errors
|     +-- Result types in domain/, domain-specific errors (see Error Handling below)
|
+-- Validating input or configuring types
|     +-- Validate at the boundary, trust types inside (see Validation and Types below)
|
+-- Shared utility
|     +-- Give it a contextual name (never utils.ts)
|           +-- Place in the owning feature, or shared/ if truly cross-cutting
|
+-- Writing tests
      +-- Use the web-testing skill for Vitest/RTL patterns
      +-- Use webapp-testing for Playwright E2E
```

---

## Project Structure

The canonical Next.js 15+ layout:

```
src/
  app/                          # Routing layer — thin page shells
    (marketing)/
      page.tsx
    dashboard/
      recipes/
        page.tsx                # Server Component: composes from features/
        loading.tsx
        error.tsx
        [id]/
          page.tsx

  features/                     # Business logic — each feature owns its architecture
    recipes/
      domain/
      application/
      infrastructure/
      components/
      hooks/
      tests/

    auth/
    billing/

  shared/                       # Truly cross-cutting concerns only
    components/
      ui/                       # Primitives: Button, Input, Card, etc.
    lib/
      result.ts                 # Result<T, E> utility (see Error Handling below)
      env.ts                    # Validated environment variables
      fetcher.ts                # Shared HTTP client
    types/
    test/
      builders/                 # Test data factories
      mocks/                    # Shared MSW handlers
```

**Key rules:**
- `app/` pages are **thin** — they import from `features/` and compose. No business logic in route files.
- Each `features/` folder has its own 4-layer structure (see `references/deep-dive.md`).
- `shared/` is for genuinely cross-cutting code. If only two features use it, it belongs in one of them.

For the full annotated project scaffold, see `references/deep-dive.md`.

---

## The 10 Golden Rules

1. **Every feature owns its folder.** Domain, use cases, infrastructure, components, hooks, and tests — all co-located. No global junk drawers.

2. **The UI never consumes raw backend data.** Always map through a ViewModel. `<p>{recipe.owner.first_name}</p>` directly from a DTO is a coupling time bomb.

3. **Use cases do not import React.** Application logic is framework-agnostic. No JSX, no hooks, no `useEffect` in use cases. They call repository interfaces and return data.

4. **Repositories implement interfaces.** The interface lives in `domain/`, the implementation in `infrastructure/`. The use case depends only on the interface.

5. **Components receive simple, typed props.** Presentational components take ViewModels, not raw DTOs. They are easy to test because they have no data-fetching or business logic.

6. **Client Components only for interactivity.** Server Components are the default. Reach for `"use client"` only when you need `useState`, event handlers, forms, drag-and-drop, or browser APIs.

7. **Types as contracts at boundaries.** Every boundary (feature <-> feature, UI <-> backend, layer <-> layer) has a typed interface or type. Not decoration — contracts.

8. **Mappers between every layer boundary.** DTO -> Domain entity in infrastructure. Domain entity -> ViewModel in infrastructure or application. The mapper is the translator between worlds.

9. **No `utils.ts`, `helpers.ts`, `common.ts`, `misc.ts`.** These are architecture graveyards. Use contextual names: `recipe-title.formatter.ts`, `price-display.ts`, `auth-session.mapper.ts`.

10. **Local state first, global state last.** Escalation order: component state -> props -> context -> server state (fetch/cache) -> global store. If you think you need global state, first check if it is an architecture problem.

---

## Core Design Patterns

| Pattern | When to use | Example |
|---------|------------|---------|
| **Composition** | Always — React's fundamental model | `children` props, render props, compound components |
| **Ports & Adapters** | Decoupling from backend, storage, SDKs, external services | Repository interface in domain/, API implementation in infrastructure/ |
| **Presentational / Container** | Separating data logic from rendering | Page fetches data, passes ViewModels to presentational components |
| **Factory** | Wiring use cases with dependencies | `makeGetRecipesUseCase({ recipeRepository })` |
| **Mapper / Adapter** | Translating between layers | `toRecipeCardViewModel(dto)` |
| **Strategy** | Behavior that varies by feature flag, role, provider, or mode | Payment processor selected at runtime |
| **State Reducer** | Complex form or editor state | `useReducer` for multi-step wizard, rich text editor state |

**Do not use:** Singleton everywhere, giant service classes, inheritance hierarchies, abstract factories, global "repos of utils."

---

## Error Handling

### The Result Pattern

Use typed discriminated unions to make errors first-class return values instead of throwing exceptions:

```tsx
// shared/lib/result.ts

export type Result<T, E> =
  | { ok: true; value: T }
  | { ok: false; error: E };

export function ok<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

export function err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}

export function isOk<T, E>(result: Result<T, E>): result is { ok: true; value: T } {
  return result.ok === true;
}

export function isErr<T, E>(result: Result<T, E>): result is { ok: false; error: E } {
  return result.ok === false;
}
```

### Why Not Throw Everywhere

1. **Untyped.** The caller does not know what errors can occur. TypeScript cannot enforce handling.
2. **Hard to handle in UI.** Catching errors in components leads to try-catch spaghetti or generic error boundaries that lose context.
3. **Poor testability.** Testing that the right error is thrown for the right reason is awkward compared to asserting on a return value.

### Domain Errors

Define error types per feature in `domain/__name__.errors.ts`:

```tsx
export type RecipeNotFoundError = {
  type: 'recipe_not_found';
  recipeId: string;
};

export type RecipeValidationError = {
  type: 'recipe_validation';
  fields: Record<string, string>;
};

export type RecipeForbiddenError = {
  type: 'recipe_forbidden';
  reason: string;
};

export type RecipeError =
  | RecipeNotFoundError
  | RecipeValidationError
  | RecipeForbiddenError;
```

Using union types for errors gives you:
- Exhaustive switch statements (TypeScript warns if you miss a case)
- Clear documentation of what can go wrong
- Specific error handling in the UI per error type

### Using Result in a Use Case

```tsx
export function makeSaveRecipeUseCase({ recipeRepository }: Dependencies) {
  return {
    async execute(input: SaveRecipeInput): Promise<Result<Recipe, SaveRecipeError>> {
      const validation = validateRecipeInput(input);
      if (!validation.ok) {
        return err({ type: 'validation', fields: validation.errors });
      }

      try {
        const recipe = await recipeRepository.save(toRecipe(input));
        return ok(recipe);
      } catch (error) {
        return err({ type: 'network', message: 'Failed to save recipe' });
      }
    },
  };
}
```

### Handling Result in the UI

```tsx
'use client';

export function RecipeEditorClient() {
  const [error, setError] = useState<SaveRecipeError | null>(null);

  async function handleSubmit(data: SaveRecipeInput) {
    const result = await saveRecipe.execute(data);

    if (result.ok) {
      router.push(`/recipes/${result.value.id}`);
      return;
    }

    // TypeScript knows result.error is SaveRecipeError
    switch (result.error.type) {
      case 'validation':
        setFieldErrors(result.error.fields);
        break;
      case 'forbidden':
        setError(result.error);
        break;
      case 'network':
        setError(result.error);
        break;
    }
  }

  if (error?.type === 'forbidden') {
    return <Alert variant="error">{error.message}</Alert>;
  }

  return <RecipeForm onSubmit={handleSubmit} errors={fieldErrors} />;
}
```

### Error Boundaries

For unrecoverable errors (bugs, unexpected crashes), use Next.js error boundaries:

```tsx
// app/dashboard/recipes/error.tsx
'use client';

export default function RecipesError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

**Use Result types for expected errors** (validation, forbidden, not found).
**Use error boundaries for unexpected errors** (crashes, bugs, unhandled exceptions).

| Error type | Strategy | Where |
|-----------|----------|-------|
| Validation failure | Result type with field errors | Use case -> component |
| Business rule violation | Result type with domain error | Use case -> component |
| Not found | Result type returning null or error | Repository -> use case |
| Network failure | Result type or error boundary | Infrastructure -> use case |
| Unexpected crash | Error boundary (`error.tsx`) | Anywhere -> Next.js catches it |

---

## Validation and Types

### Edge Validation

Every piece of data that enters your system from the outside world must be validated at the boundary. Inside the boundary, trust the types.

| Boundary | Data source | Risk |
|----------|------------|------|
| API responses | Backend server | Shape may change, may be malformed |
| Form inputs | User | May be empty, invalid, malicious |
| URL parameters | Browser/user | May be missing, wrong type |
| Environment variables | Build/deploy config | May be undefined, wrong format |
| LocalStorage/cookies | Browser | May be corrupted, missing, tampered |
| Third-party SDK responses | External service | May change without warning |

**Validate at the boundary. Trust types inside.**

```
[External World] -> validation -> [Typed Internal World]
     untrusted       boundary        trusted
```

### Zod for Runtime Validation

Zod is the recommended library for runtime validation at boundaries.

```tsx
// infrastructure/recipe-dto.ts — validating API responses
import { z } from 'zod';

export const RecipeDtoSchema = z.object({
  id: z.string(),
  title: z.string(),
  owner: z.object({
    first_name: z.string(),
    last_name: z.string(),
  }),
  main_image_url: z.string().url().nullable(),
  created_at: z.string().datetime(),
  status: z.enum(['draft', 'published', 'archived']),
});

export type RecipeDto = z.infer<typeof RecipeDtoSchema>;
```

```tsx
// domain/recipe.ts — validating form inputs
export const SaveRecipeInputSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200, 'Title too long'),
  description: z.string().max(2000).optional(),
  ingredients: z.array(z.string().min(1)).min(1, 'At least one ingredient'),
  cookingTimeMinutes: z.number().int().min(1).max(1440),
});

export type SaveRecipeInput = z.infer<typeof SaveRecipeInputSchema>;
```

```tsx
// shared/lib/env.ts — validating environment variables
const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  API_BASE_URL: z.string().url(),
  NEXT_PUBLIC_APP_URL: z.string().url(),
  AUTH_SECRET: z.string().min(32),
  NODE_ENV: z.enum(['development', 'production', 'test']),
});

export const env = envSchema.parse(process.env);
```

### TypeScript Contracts

| Use | `interface` | `type` |
|-----|------------|--------|
| Repository ports | Yes | -- |
| Service contracts | Yes | -- |
| Component props | Either | Either |
| Union types | -- | Yes |
| View Models | -- | Yes |
| Mapped / conditional types | -- | Yes |

**Rule of thumb:**
- `interface` for contracts and ports — things that declare a capability and represent a boundary between systems
- `type` for data shapes, unions, and composition — things that describe what data looks like

```tsx
// Interface: declares a capability (port)
export interface RecipeRepository {
  list(): Promise<Recipe[]>;
  getById(id: string): Promise<Recipe | null>;
  save(recipe: Recipe): Promise<void>;
}

// Type: describes a data shape
export type RecipeCardViewModel = {
  id: string;
  title: string;
  authorName: string;
  imageUrl: string;
};
```

### Presentational Component Example

A component that receives a ViewModel and renders it -- no data fetching, no business logic:

```tsx
// components/RecipeCard.tsx
import type { RecipeCardViewModel } from '../infrastructure/recipe-mappers';

export function RecipeCard({ recipe }: { recipe: RecipeCardViewModel }) {
  return (
    <article aria-label={recipe.title}>
      <img src={recipe.imageUrl} alt={recipe.title} loading="lazy" />
      <h3>{recipe.title}</h3>
      <p>by {recipe.authorName}</p>
    </article>
  );
}
```

### No Decorative Types

Every type should represent a **boundary** or an **intention**:

```tsx
// Bad: type adds no value
type Count = number;
type IsVisible = boolean;

// Good: type constrains valid values
type RecipeStatus = 'draft' | 'published' | 'archived';
```

### Branded Types (Advanced)

For IDs that should not be accidentally mixed:

```tsx
type Brand<T, B extends string> = T & { __brand: B };

type RecipeId = Brand<string, 'RecipeId'>;
type UserId = Brand<string, 'UserId'>;

function getRecipe(id: RecipeId): Promise<Recipe> { ... }

const userId = 'abc' as UserId;
getRecipe(userId); // TypeScript error
```

Use branded types when mixing up IDs would cause subtle bugs. Do not use them everywhere.

| Boundary | Validation tool | Output |
|----------|----------------|--------|
| API response | `RecipeDtoSchema.parse(json)` | Typed DTO |
| Form input | `SaveRecipeInputSchema.safeParse(data)` | Typed input or validation errors |
| URL params | `z.string().uuid().parse(params.id)` | Typed param |
| Environment | `envSchema.parse(process.env)` | Typed env object |
| LocalStorage | `JSON.parse` + schema validation | Typed data or fallback |

Inside the validated boundary, trust the types. Do not re-validate.

---

## Related Skills

| Need | Skill | When to use |
|------|-------|-------------|
| Visual design, UI aesthetics, styling | **frontend-design** | Building UI that needs to look polished and distinctive |
| Unit / component / integration tests | **web-testing** | Writing Vitest + Testing Library tests for any layer |
| E2E browser automation | **webapp-testing** | Writing Playwright tests for critical user flows |

---

## Reference Files

| File | Description |
|------|-------------|
| `references/deep-dive.md` | 4-layer structure, ports & adapters code walkthrough, server/client component rules, state hierarchy, ViewModels & mappers, composition patterns, naming conventions |
