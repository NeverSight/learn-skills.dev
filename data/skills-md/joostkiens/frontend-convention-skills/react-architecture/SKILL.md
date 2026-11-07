---
name: react-architecture
description: >
  React architecture conventions: component layers (foundation vs domain),
  global state, co-location, and module boundaries. Use when working on
  folder structure, component layering, or module organisation.
user-invocable: false
model: claude-haiku-4-5
---

# Frontend Architecture Conventions

> **Before applying these conventions, invoke the `frontend-conventions:general`
> and `frontend-conventions:react` skills** to load the conventions these build on.
>
> Project-specific rules always override these defaults.

## Component Layers

Organise components into two layers based on domain knowledge, not reusability
alone. The names below are defaults; the principle matters more than the naming.

### Foundation layer

- Contains pure UI components with no domain knowledge
- A foundation component knows nothing about users, orders, products, or any
  business concept specific to this application
- Reusable in any project without modification: buttons, inputs, modals, cards,
  tooltips, layout primitives
- Foundation components may only import from other foundation components,
  never from domain

### Domain layer

- Contains components coupled to a specific business concept
- A domain component may use foundation components internally, but carries
  domain meaning: `UserCard`, `OrderSummary`, `ProductGrid`
- Not expected to be reusable across projects
- Domain components may import from foundation and from other domain components

### The one-way dependency rule

Foundation must never import from domain. Domain may import from foundation.
This boundary is absolute. Violating it collapses the layers and makes
foundation components impossible to extract or reuse.

```
pages / features   (composes domain)
      |
   domain          (composes foundation + domain)
      |
  foundation       (no imports from above layers)
```

### Pages and features (optional third layer)

For larger applications, a pages or features layer above domain is a natural
extension. This layer owns route-level composition, data fetching, and
combining multiple domain components into full views. It may import from both
domain and foundation but should not contain reusable UI logic of its own.

## Global State

- State that is genuinely global (auth, current user, theme, session) belongs
  at the top of the component tree or in a dedicated store — not threaded
  through props or duplicated across sibling components
- Distinguish between state that crosses component boundaries and state that is
  local to a subtree; only promote state when it is genuinely shared
- Use Context for low-frequency updates (theme, auth, locale); it is simple and
  requires no extra dependency
- Use an external store for high-frequency updates or complex state with many
  transitions; Context re-renders every consumer on every update, which becomes
  a performance problem at scale
- Keep store slices focused on a single domain concept; a single global store
  object that holds all application state is hard to reason about and test
- Co-locate store definitions with the domain they belong to, not in a central
  `store/` folder

## Co-location

- Tests, styles, and component-specific hooks live next to the component
  they belong to, not in a parallel folder tree
- A component's folder contains everything needed to understand and modify it:
  ```
  UserCard/
    UserCard.tsx
    UserCard.test.tsx
    UserCard.module.css   (or equivalent)
    useUserCard.ts        (if the hook is only used here)
    index.ts
  ```
- Only promote a file to a higher scope when it is genuinely used in more
  than one place; don't preemptively centralise

## Barrel Files

- Use a barrel (`index.ts`) at layer boundaries to define the public API of
  a layer; consumers import from the layer, not from internal paths:
  ```ts
  // ✅
  import { UserCard } from '@/domain';

  // ❌ reaches into internals
  import { UserCard } from '@/domain/UserCard/UserCard';
  ```
- Avoid barrels inside a layer; they obscure the real module graph, slow
  down bundlers, and make tree-shaking less effective
- A barrel should re-export only what is intentionally public; if something
  is not in the barrel, it is private to that layer

## Naming

- Name layers by what they are, not where they live
- Avoid `common`, `shared`, `misc`, or `utils` as top-level folder names;
  they describe location, not purpose, and become catch-all dumping grounds
- If a component or function resists being named after a domain concept or a
  UI primitive, that is a signal it needs to be split or reconsidered
