---
name: react-single-responsibility
description: |
  Strategies to simplify components, hooks, and methods: decomposition order (utilities, hooks, sub-components),
  early returns, control flow, parameter design, and code smell fixes. Use when the user says: ungodify
  this method/function/component, simplify this method/function/component, make this method/function/component
  less complex; or when refactoring a large component, hook, or function, reducing complexity, applying
  single responsibility, or asking how to simplify a component, hook, or method.
metadata:
  version: "1.0.0"
  last-updated: "2026-02-25"
  source: "Extracted from react-ts-guidelines"
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Single Responsibility — Simplify Components & Methods

Apply these strategies to keep components, hooks, and methods focused, testable, and readable. Rules are split into **component**, **hook**, and **method** simplification.

---

## Principles

| Principle                 | Rule                                                                                          |
| ------------------------- | --------------------------------------------------------------------------------------------- |
| **KISS**                  | Simplest solution that works. Avoid over-engineering.                                         |
| **Single responsibility** | One clear responsibility per component or function; extract utilities, hooks, sub-components. |
| **DRY**                   | Extract common logic; create reusable functions or components.                                |
| **YAGNI**                 | Don't build features before they're needed.                                                   |
| **Composition**           | Prefer composing small components and utilities over large, multi-purpose blocks.             |

---

## Simplifying a component

Rules that apply when reducing complexity of a **React component**.

### Decomposition (avoid God Component)

Apply in this order:

1. **Extract pure utilities first** — Logic with no React dependency → pure functions. More than one argument → object destructuring within the method signature. Reusable → `src/utils/xyz.utils.ts`; feature-specific → `component-name.utils.ts` next to the component.

2. **Form state (multiple useState)** — When multiple `useState` calls are used to manage the full state of an input form: refactor the code to use the **react-hook-form** library, which simplifies the form, its validation, its state, and its submission.

3. **Extract logic into hooks** — State, effects, derived logic → hooks (`use-xyz.ts`). Reusable → `src/hooks/`; feature-specific → feature's `hooks/` subdirectory. Prefer a **plain arrow function** over a custom hook when you don't need React primitives.

4. **Split the visual layer into sub-components** — If render/TSX exceeds roughly **40 lines**, extract sub-components with clear props and a single responsibility. **Avoid internal `renderXyz()` methods**: turn each into a **regular component** (own file, own props). Each sub-component **must live in its own file**; use **parent file name as prefix**: `parent-name-<sub-component-name>.tsx` (e.g. `market-list-item.tsx`, `market-list-filters.tsx` for parent `market-list.tsx`). Large component (~100+ lines) → split into list container, list item, filters, pure functions and hook(s) as necessary for data logic.

### Structure and readability

- **Order inside the component:** types → state → computed const → effects → handlers → render.
- **Handlers:** one arrow function per handler (e.g. `const handleClick = () => { ... }`); avoid factories that return handlers. If an arrow function handler is only depending on pure typescript it can be externalized into `component-name.utils.ts` next to the component.
- **Early returns in render** — Keep the main path flat: `if (isLoading) return <Spinner />; if (error) return <ErrorMessage />; ...` One condition per line; avoid nested ternary operators (“ternary hell”).
- **Boolean in JSX** — Use explicit computed boolean (e.g. `const hasItems = items.length > 0; { hasItems && <List /> }`) so `0` is not rendered.
- **Static data** — Constants and pure functions that don't depend on props or state → **outside the component** (relocate into `component-name.utils.ts`) to avoid new references every render.

### React-specific

- **Selected items** — Store selection by **ID** in state; **derive** the full item from the list (e.g. `selectedItem = items.find(i => i.id === selectedId)`). Avoids stale references when the list updates.
- **useMemo / useCallback — only when absolutely necessary** — Default: do not use. Re-renders are often an acceptable tradeoff to promote readability. These hooks add complexity and recent React compilers already optimize renders. Avoid for trivial cases (e.g. `useMemo(() => count * 2, [count])`, `useCallback(() => setOpen(true), [])`). Use only when: **profiling** shows a real performance problem.
- **Data fetching** — Prefer **TanStack Query** (`useQuery` / `useMutation`) instead of manual `useState` + `useEffect` — reduces boilerplate and keeps the component simpler.
- **Form state** — When multiple `useState` calls are used to manage a form, consider using **react-hook-form** to simplify the form and its state (validation, submission, and field registration in one place).

---

## Simplifying a hook

Rules that apply when reducing complexity of a **custom React hook**. Apply single responsibility by extracting pure logic into utilities and splitting broad hooks into smaller, focused ones.

### Decomposition order

1. **Extract pure JS utilities first** — Any logic that has no dependency on React (no `useState`, `useEffect`, context, etc.) → move to **pure exported arrow functions**. For more than one argument, use object destructuring in the function signature and define the parameter interface just above the function. Put extracted arrow function(s) in `<component-name>.utils.ts` next to the component or `<hook-name>.utils.ts` next to the hook, or in `src/utils/` if reusable. Examples: formatting, validation, computing derived values from plain data, building query params or request bodies. Pure functions are easier to test and reuse outside the hook.

2. **Consider enriching an existing state manager** — Before creating new specialized hooks, check if the project already uses a **state manager** (e.g. **Zustand**, **MobX**, Redux). If so, consider **adding the business logic there**: actions, derived state, and domain rules can live in the store and **slim down the hooks**. Hooks then become thin selectors or one-off bindings (e.g. `useStore(selector)`), and the store encapsulates the domain. Prefer extending the existing store over multiplying hooks that each hold their own state.

3. **Split into specialized hooks** — If no store fits or the logic is purely local/UI, and the hook still handles several concerns (e.g. fetching + filtering + pagination) or states, extract **one hook per concern**: e.g. `useFetchItems`, `useItemsFilter`, `usePagination`. Compose them in the component or in a thin “orchestrator” hook that only wires the others. Each hook should have **one clear responsibility** and a name that reflects it.

### Hook design

- **Narrow return shape** — Prefer returning a small, stable object (e.g. `{ data, isLoading, error }` or `{ value, onChange }`). Avoid returning large bags of unrelated state and setters; split into separate hooks instead.
- **Plain function vs hook** — If the logic doesn’t need React primitives (state, effects, context), use a **plain function** in a `.utils.ts` file instead of a custom hook. Only introduce a hook when you need React’s lifecycle or state.
- **Dependencies** — Keep hook inputs explicit (parameters); avoid reading from context or globals inside the hook unless that’s the hook’s sole purpose. Easier to test and reason about.

### File and naming

- **One hook per file** when the hook is non-trivial; file name: `use-<name>.ts` (e.g. `use-market-filters.ts`, `use-pagination.ts`). Reusable hooks → `src/hooks/`; feature-specific → feature’s `hooks/` subdirectory.
- **Co-locate utilities** — `<hook-name>.utils.ts` next to the hook for helpers used only by that hook; `<main-component-name>.utils.ts` next to the main component for helpers used by main component and its sub-components; shared logic → `src/utils/` or domain-specific utils module.

### Quick checklist (hooks)

- [ ] Does the hook contain logic with no React dependency? → extract to pure arrow functions in `.utils.ts` using destructuring within the signature.
- [ ] Does the hook do more than one thing? → consider enriching the project’s state manager (Zustand, MobX, etc.) first; otherwise split into smaller pure JS utilities, or specialized hooks (e.g. fetch vs filter vs pagination) and compose.
- [ ] Could this be a plain function? → if it doesn’t need state/effects/context, use a utility instead of a hook.
- [ ] Is the return type a large, mixed bag? → consider splitting the hook or returning a smaller, focused API.

---

## Simplifying a method

Rules that apply when reducing complexity of a **function or method** (non-component).

### Long function (>40 lines)

- **Signal:** Scrolling to understand a single function.
- **Fix:** Extract into smaller, **named** arrow functions. Apply **single responsibility**: each new method must stay **simple and focused on one task only** (e.g. validate → fetch → persist → notify). Each step should be testable in isolation.

### Control flow

- **Early returns** — Prefer early returns over nested if/else (max ~2 levels of nesting).
- **const over let** — Prefer const; use **reduce** or pure helpers (e.g. `const isXyz({ arg1, arg2 }: MyArgs): boolean`) with early returns instead of mutable loop accumulators.
- **Clear conditionals** — Use `Array.includes(value)` for multiple value checks; `Array.some(predicate)` for existence checks. Extract **complex expressions** into named variables (destructuring, intermediate vars) for readability.

### Parameters

- **Long parameter list (>1 param)** — Use a single **params object** with destructuring; extract the interface above the function signature (e.g. `interface CreateUserArgs`). Avoids wrong order and unclear meaning at the call site. The interface name matches the method name but starts with a capital letter and ends with `Args` (e.g. for `getThisMethod`, use `interface GetThisMethodArgs`).
- **Interface used only for one method** — When an interface exists solely to type a single method’s signature, **place it immediately above that method** (colocation). This self-documents the signature that follows and keeps the type next to its only consumer.
- **Boolean flag parameter** — Avoid `fn(data, true)`. Use an **options object** with a named flag (e.g. `{ userId, includeArchived }: CreateUserArgs`) or **separate functions** when behavior diverges.
- **Conventions** — Destructuring for multiple params; extract parameters into named interfaces; optional as `param?: Type`; defaults in destructuring (e.g. `{ page = 1, size = 10 }`).

### Duplication (DRY)

- **Signal:** Copy-paste with minor variations.
- **Fix:** Extract a **parameterized arrow function** (e.g. single `getMarketsForUser({ userId, status }: GetMarketsForUserArgs)` instead of `getActiveMarketsForUser` and `getClosedMarketsForUser`).

---

## Shared (components and methods)

### Object destructuring

- Use **object destructuring** when reading or passing object attributes so that attribute names are explicit and the code stays readable. Applies to: **component props** (e.g. `const { isLoading, error, data } = props` or in the signature), **function parameters** (e.g. `const fn = ({ a, b }: FnArgs) => ...`), and **local objects** when you use several properties (e.g. `const { name, status } = item`). Prefer destructuring when it clarifies usage and improves readability; avoid when a single property is used once.

### Coupling (shotgun surgery)

- **Signal:** One feature change requires edits in many files.
- **Fix:** Co-locate related logic (e.g. feature folder with its own components, hooks, utils, types); reduce coupling and centralize domain logic where it belongs.

### File and size guidelines

- **200–400 lines** typical per file; **1000 lines** absolute maximum.
- **One responsibility per file** (high cohesion, low coupling).
- File names: **kebab-case**. Examples: `market-list-item.tsx`, `use-market-filters.ts`, `<name>.utils.ts`, (e.g. `market-list.utils.ts`).

### Quick checklist

- [ ] Does it do more than one thing? → if yes: extract pure utilities, hooks, or sub-components (component) or smaller named functions (method).
- [ ] More than 1 parameter? → use a single options object, an extracted parameter interface above the signature, and destructuring.
- [ ] Copy-pasted code? → extract and parameterize.
- [ ] Control flow deeply nested? → use early returns and intermediate variables.
- [ ] Comments explaining _what_? → rename for self-documenting code; keep comments for _why_ only.
