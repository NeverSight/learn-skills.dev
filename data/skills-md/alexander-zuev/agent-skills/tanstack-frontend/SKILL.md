---
name: tanstack-frontend
description: "React and TanStack Start frontends with Feature-Sliced Design, Fowler's component layers, and query and mutation factories. Use for routes, pages, components, hooks, or data access."
license: Apache-2.0
---

# Frontend — React + TanStack Start

This skill owns frontend placement, React, TanStack Query, state, and UI conventions.
Use [typescript-standards](../typescript-standards/SKILL.md) for types, schemas, modules, comments, and general tests.
Use [cloudflare-backend](../cloudflare-backend/SKILL.md) when adding server functions, including stubs.

Sections marked `[detect: …]` identify evidence to read. Select reference code by the concern it demonstrates.
Do not infer compatibility from repository age. Before entity, query, or mutation work, read [data access](references/data-access.md).
Trace the target project's factory, server function, middleware registration, and error payload before editing.
State the selected layer, success/error contract, source files, and material conflicts.

## TanStack Start

- Use TanStack Start, never Next.js. Traditional SSR + hydration, no RSC, no `'use client'`.
- Server-only code: `createServerFn()` — RPC-style server functions in `src/server/entrypoints/functions/`.
- Loaders are isomorphic — they run on server and client. Secrets/DB access goes through server functions.
- Pending timing knobs when needed — native route options, never artificial delays: `pendingMs: 0` (show pending immediately; default 1000ms), `pendingMinMs: 500` (avoid flash). Most routes instead rely on loader-seeded data + `pendingComponent`.

---

## Architecture

### Mental model

FSD means Feature-Sliced Design. Entities represent business concepts such as a user, call, or balance.
Features represent user actions that coordinate those concepts. Entity slices do not own screen workflows.

```text
Route → Page → Feature → Entity → Shared
                       ↘ Shared UI
```

Imports point to lower layers. A page may compose shared UI and entities when no reusable feature is needed.
The project adapts Shared into `ui/`, `lib/`, and browser-safe workspace packages.

### Directory

Shared core under `apps/<app>/src/`:

```
src/
├── routes/            # TanStack Router files — thin, delegate to pages/
├── pages/             # orchestrators
├── entities/          # business concepts: types, factories, pure derivations
│   └── <entity>/       # <entity>-queries.ts, <entity>-mutations.ts, domain files
├── features/          # user actions and reusable workflows
│   └── <feature>/
│       ├── components/
│       ├── hooks/
│       ├── queries/   # feature-owned data, when no entity owns it
│       └── models/    # or store/, schema/ as needed
├── ui/                # app-specific presentation + stylesheets
├── lib/               # clients (rpc, auth, sentry), router, shared hooks
└── server/            # backend half (see cloudflare-backend skill)
```

[detect] Existing entity slices may be flat or use FSD segments such as `model/` and `api/`.
Follow the project's layout. Do not introduce segments or barrels merely to match an FSD diagram.
Older projects keep models under features or lib. Do not restructure unrelated code.

`[detect]` design-system location: a shared `packages/ui` workspace package (pure primitives + token stylesheets, consumed by multiple apps) and/or app-local `src/ui/components/`. App-local components may be organized by domain (`auth/`, `media/`) or by kind (`controls/`, `overlays/`, `feedback/`, …) — follow the existing folders, don't invent a taxonomy.

### Layer rules

1. Routes are thin adapters — they configure the route and render a page.
2. Pages compose features — no inline services; marketing/landing pages may own local `sections/` and `components/` subtrees.
3. Features own action workflows, components, and hooks. Entities own reusable business data and its query/mutation factories.
4. UI components are pure — no API calls, no business logic, no feature imports.
5. Place business data by entity ownership. Use reuse count to decide whether presentation code stays local or becomes shared.

```
✅ page → feature · feature → entity/model · feature → ui · entity → lib · hook → query factory
❌ ui component → feature · entity → feature · page → direct API call · circular feature pairs
```

Entity slices must not import sibling entity slices. Feature slices must not import sibling feature slices.
Coordinate relationships in the consuming feature or page. Put shared contracts in the browser-safe core package when appropriate.
Use FSD's explicit `@x` entity API only when the project already adopts it and a domain relationship requires it.
Read the official [FSD layers](https://feature-sliced.design/docs/reference/layers) guidance before adding or changing entity boundaries.

Pages stay within 100 lines for app pages. Marketing pages may run longer; do not restructure them without scope.

---

## Component Architecture (Fowler layers)

- **Components** — thin JSX, props/handlers only. <100 lines (aim 50).
- **Hooks** — state/effects, two+ queries merged into a domain object, or a **presentation model** (see below). Do not wrap a single `queryOptions` in `useX()` *just to pass it through*: call `useSuspenseQuery` / `useQuery` on the factory or the bound route-context object, and put extra options (`select`, `staleTime`) at that call site. Do not accept `UseQueryOptions` as a hook argument — type inference breaks.

```typescript
// ✅ extra options at the call site
const { data } = useQuery({
  ...productQueries.detail({ productId: id }),
  select: (product) => product.title,
  staleTime: 20_000,
})

// ❌ do not wrap the factory and forward UseQueryOptions
function useProduct(id: ProductId, options?: UseQueryOptions<Product>) {
  return useQuery({
    ...productQueries.detail({ productId: id }),
    ...options,
  })
}
```

- **Models** — framework-agnostic business logic. Zero React deps.
- **Services/queries** — data fetching, API ↔ domain conversion. *Domain* mapping lives in the `queryFn`. *View* mapping is a different job — see Presentation model.

### Presentation model

A route reads a hook and passes the result down. **Mapping query state into props is not wiring** — it belongs in the hook that owns the screen's view model: `pages/<page>/use-<thing>.ts` when one screen reads it, `features/<feature>/hooks/` when two or more do. `entities/` holds types, query factories, and pure derivations, and never imports React.

```typescript
// ❌ mapping in the route — 20 lines, still wrong
const { data, error, hasNextPage, fetchNextPage, refetch } = useInfiniteQuery(conversationQueries.list())
const conversationList = data
  ? { status: 'ready', conversations: data.pages.flatMap((p) => p.conversations), hasMore: hasNextPage, … }
  : { status: 'failed', error, onRetry: () => void refetch() }
```

```typescript
// ✅ pages/conversations/use-conversation-list.ts returns the view-ready shape
export function useConversationList(): ConversationList {
  const query = useInfiniteQuery(conversationQueries.list())

  if (query.status === 'pending') return { status: 'pending' }
  if (query.status === 'error') {
    return { status: 'failed', error: query.error, onRetry: () => void query.refetch() }
  }
  return { status: 'ready', conversations: query.data.pages.flatMap((p) => p.conversations), … }
}
```

Two concrete reasons, not style:

1. **Branching on `data`/`error` instead of `status` swallows `pending`.** The ❌ version renders "failed" during a legitimate loading state. Only `status` distinguishes all three.
2. **The page stays renderable from a fixture.** Every state becomes a value a story can pass — including "failed", which otherwise has to be *induced* by mocking a rejecting fetch.

The returned shape is one discriminated union, with per-arm fields so no arm carries something it cannot use:

```typescript
export type ConversationList =
  | { readonly status: 'pending' }
  | { readonly status: 'ready'; conversations: readonly ConversationSummary[]; hasMore: boolean; isLoadingMore: boolean; onLoadMore: () => void }
  | { readonly status: 'failed'; error: unknown; onRetry: () => void }
```

Place a reusable entity state type in the entity slice. Keep a screen-specific presentation type beside its page hook.
Never import page types into an entity. This project keeps entity modules free of React imports; FSD itself permits entity UI.

### Page props

- **Group handlers into one `actions` object** rather than a spray of `onX` props — adding one then touches one call site, not every story and harness.
- **Pass data, not `ReactNode` slots**, when the page already has what the slot needs. A `header: ReactNode` prop that only ever wraps `<Header host={host} relay={relay} />` should be `host` + the page rendering its own header.
- **Navigation is a `Link`, never an action callback.** `onOpenThing: (id) => navigate(...)` loses cmd/middle-click, "open in new tab", right-click → copy address, and the URL on hover. `useNavigate` is for imperative cases — after a mutation, not for going somewhere.

| Metric | Limit | Action |
|---|---|---|
| Lines | <100 (aim 50) | Extract component/hook |
| Hooks used | ≤5 | Extract custom hook |
| Props | ≤7 | Composition or context |
| Ternary depth | 1 | Early returns |

Refactoring moves: Extract Hook (state/effects out), Extract Model (calculations to pure TS), Extract Service (API calls out). Anti-patterns: fat components, god hooks, logic in JSX, framework coupling, store-as-service.

---

## Data Layer — Query and Mutation Factories

Each entity exposes reusable `queryOptions`, `infiniteQueryOptions`, and `mutationOptions` builders.
Factories own keys, typed requests, domain conversion, and cache effects. Consumer hooks own screen state and action sequencing.
Read [data access](references/data-access.md) for examples, reference files, API checks, and validation.

Return bare server-function values in the current transport pattern.
Use an existing unwrap helper only when the inspected server function returns an envelope.
The backend skill owns serialization and error conversion.

For route-prefetched queries, the route binds URL inputs once.
The loader and page consume the same returned query options.

### Query keys

- The key includes every input the `queryFn` reads. Change the key to refetch. Do not call `refetch({ newId })`.
- Hierarchy: `['products']` → `['products', 'list']` → `['products', 'list', filters]` → `['products', 'detail', input]`.
- Invalidate with a prefix: `invalidateQueries({ queryKey: ['products', 'list'] })`.
- Never share a key between `useQuery` and `useInfiniteQuery`.
- Use `productQueries.detail({ productId: id }).queryKey` for typed `getQueryData` / `setQueryData`.

### Transforms (`select`)

| Where | What |
|---|---|
| `queryFn` | Transport value → domain when conversion is needed. The cache stores this value. |
| `select` at the call site | One field or a derived value. Do not put `select` in the factory. |
| Render | Cheap derive only. |

Do not use `select` by default. Use it when a large payload would re-render a small widget.

### Mutations

Mutations live in `<entity>-mutations.ts`.

- After success, `invalidateQueries` is the default.
- Return that promise if the button must stay pending until the list refreshes.
- Prefer `mutate`. Use `mutateAsync` when the caller must compose or await the returned promise.
- Factory `onSuccess` = cache work. Call-site `mutate(variables, { onSuccess })` = toast / redirect.
- One variables object: `mutate({ title, body })`.
- Do not write optimistic cache updates for forms, dialogs, or redirects. Use them only for an instant toggle. Prefer invalidate after the mutation.
- `setQueryData` is the exception: instant toggle, or the mutation returns the exact cached row.

### Infinite queries

Use `infiniteQueryOptions`. Give it a key that is not the normal list key. Set `initialPageParam`.

### Router + Query ownership

- Entity: owns query factories, query keys, requests, and domain conversion. It does not import Router APIs.
- Route: validates URL state and binds all query inputs for the current route match.
- Loader: starts cache work with the bound query options. **Throw vs swallow is a UX decision, not a preference.** Await `queryClient.query(options)` (or `query({ ...options, staleTime: 'static' })` when cached data must win even if stale). A throw replaces the whole route via `errorComponent`. Swallow with `.catch(noop)` so the failure stays in the page layout — the component then owns `pending` too, because suspense no longer covers it. Pick swallow when the shell (header, nav, actions) should survive a failed read. `ensureQueryData` / `prefetchQuery` / `fetchQuery` are deprecated aliases and go away in Query v6.
- Page: observes the bound query with `useQuery` or `useSuspenseQuery`.
- Feature: consumes domain data and owns user actions.

Router and React use the same `QueryClient`. Set `defaultPreloadStaleTime: 0` when Query owns freshness.

Create a new `QueryClient` for each SSR request. Configure `setupRouterSsrQueryIntegration` for dehydration, hydration, and streaming.

Read Query-owned data through a Query hook. Do not read it through `useLoaderData`.

For binding, loader timing, boundaries, subscriptions, examples, and sources, read [TanStack Router + Query](references/tanstack-router-query.md).

### Route params/context in pages

Parse path params at the route definition with `params.parse` when the route requires validation, refinement, or conversion. Return parsed values so child routes inherit them. Keep the parser deterministic and side-effect-free.

Pages read params and loader-seeded context via `getRouteApi('/_authed/products/$productId')` — no prop drilling from route files. Search params are validated with Zod via `validateSearch` (+ `@tanstack/zod-adapter`).

---

## State Management

| State type | Solution | When |
|---|---|---|
| Server data | TanStack Query | Always. No exceptions. |
| Local UI | useState | Single component |
| Global client state | Zustand | Criteria below |
| Derived | Compute inline | Never store what you can compute |

### Server state

All server data goes through Query — no `useEffect`+fetch, no copying query results into stores. Client-cache writes (`queryClient.setQueryData`) are for the mutation exceptions above, not for local UI state.

**No waterfalling:** design the server function to return what the page needs (join server-side, no N+1); when multiple requests are unavoidable, `Promise.all`. Raise `staleTime` to cut repeat fetches. Keep focus refetching as the default. Change it only for documented product behavior. A stale query refetches on mount when `refetchOnMount` permits it. The defaults are `staleTime: 0` and `refetchOnMount: true`.

### Zustand

Use ONLY when: (1) multiple components need the same client state, (2) persistence required, (3) access outside the React tree. Otherwise `useState` or lift. Real apps need very few stores (current repos: 0–2) — treat a new store as a design decision, not a default.

**Rules:**
- Atomic selectors (no fresh `{}` per render without `useShallow`)
- O(1) lookups — lookup map, not `.find()` in selectors
- Separate `actions` sub-object from data
- Never store server data

```typescript
// ❌ new object every render → re-renders on ANY change
const { x, y } = useStore((s) => ({ x: s.x, y: s.y }))

// ✅ atomic
const x = useStore((s) => s.x)
const y = useStore((s) => s.y)

// ❌ O(n) per render          // ✅ O(1)
useStore((s) => s.nodes.find((n) => n.id === id))
useStore((s) => s.nodeLookup[id])
```

**Vanilla-store variant** — when non-React code needs the store (upload engines, background tasks): `createStore` (vanilla) + `useStore` from `zustand/react` + `useShallow`, `devtools` middleware, `actions` sub-object; non-reactive handles (e.g. engine instances) live in a module-level Map beside the store, not in state.

### Effects

Effects must remain correct under setup → cleanup → setup.
Never suppress Strict Mode replay with refs or flags. Read [React's replay guidance](https://react.dev/learn/synchronizing-with-effects#how-to-handle-the-effect-firing-twice-in-development).
User actions, including purchases, belong to their originating event handler.
For automatic continuation after authentication or an external redirect, persist a stable attempt ID before redirect.
Enforce idempotency at the server or external boundary so replay remains safe.

Lint enforces this: `react/set-state-in-effect`, `react/no-deriving-state-in-effects`, and the nine `react-you-might-not-need-an-effect/*` rules are `error`. Each row is a section of [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect); the middle column quotes its recap.

| Effect does this | react.dev says | Use |
|---|---|---|
| [computes from props/state](https://react.dev/learn/you-might-not-need-an-effect#updating-state-based-on-props-or-state) | "If you can calculate something during render, you don't need an Effect." | derive during render |
| [caches a costly value](https://react.dev/learn/you-might-not-need-an-effect#caching-expensive-calculations) | "To cache expensive calculations, add `useMemo` instead of `useEffect`." | `useMemo` |
| [resets all state on a prop](https://react.dev/learn/you-might-not-need-an-effect#resetting-all-state-when-a-prop-changes) | "To reset the state of an entire component tree, pass a different `key` to it." | `key` |
| [adjusts some state on a prop](https://react.dev/learn/you-might-not-need-an-effect#adjusting-some-state-when-a-prop-changes) | "To reset a particular bit of state in response to a prop change, set it during rendering." | `if (prev !== next) setState(...)` in render |
| [reacts to a user action](https://react.dev/learn/you-might-not-need-an-effect#sharing-logic-between-event-handlers) | "Code that runs because a component was *displayed* should be in Effects, the rest should be in events." | the event handler |
| [chains setState after setState](https://react.dev/learn/you-might-not-need-an-effect#chains-of-computations) | "If you need to update the state of several components, it's better to do it during a single event." | one handler or reducer event |
| [runs app setup once](https://react.dev/learn/you-might-not-need-an-effect#initializing-the-application) | run it at module level, not per component | module scope |
| [reports state to the parent](https://react.dev/learn/you-might-not-need-an-effect#notifying-parent-components-about-state-changes) | "Whenever you try to synchronize state variables in different components, consider lifting state up." | lift state; call `onChange` in the handler |
| [subscribes to a store or browser API](https://react.dev/learn/you-might-not-need-an-effect#subscribing-to-an-external-store) | built-in hook for exactly this | `useSyncExternalStore` |
| [fetches server data](https://react.dev/learn/you-might-not-need-an-effect#fetching-data) | "You can fetch data with Effects, but you need to implement cleanup to avoid race conditions." | TanStack Query (see Server state) |
| [measures a DOM node](https://react.dev/learn/manipulating-the-dom-with-refs#how-can-i-measure-a-dom-node) | callback ref runs on attach, cleanup on detach | `ref={useCallback((node) => {...; return cleanup}, [])}` |
| syncs with an external system, with cleanup | this is what Effects are for | `useEffect`, and `setState` only from its async callbacks |

```typescript
// ❌ redundant state + sync effect
const [filtered, setFiltered] = useState([])
useEffect(() => { setFiltered(items.filter((i) => i.active)) }, [items])

// ✅ derive inline
const filtered = items.filter((i) => i.active)
```

---

## Async State Rendering

Mutually exclusive states = separate branches. Never nested ternaries.

| Data source | Pattern |
|---|---|
| Route loader (critical) | `pendingComponent` / `errorComponent` config |
| `useQuery` in component | Early returns |
| Multiple async sources | Suspense + ErrorBoundary composition |

```typescript
function Component() {
  const { data, isPending, isError } = useQuery(...)
  if (isPending) return <Layout><Skeleton /></Layout>
  if (isError) return <Layout><Error /></Layout>
  return <Layout><Content data={data} /></Layout>
}
```

### Query rendering and boundaries

An awaited loader query blocks the route for critical data. An unawaited query can stream with Suspense or remain non-blocking with `useQuery`.

Route queries use Router pending and error boundaries. Standalone widgets can own local Suspense and error boundaries.

Use `getRouteApi` or a strict `from` route. Use `select` to subscribe to the smallest required Router state.

Read [TanStack Router + Query](references/tanstack-router-query.md) before changing route prefetching or Query SSR behavior.

### Polling

Use TanStack Query's `refetchInterval`; do not add a separate interval loop.
For a finite job, stop at terminal state. Use the project's timeout policy when the job has a completion deadline.
For live data, such as balance during a call, the consuming feature controls when polling is active.
Continuous reads have no terminal state and need no invented stuck-job timeout.
Choose polling intervals from product requirements. Preserve Query's background and focus behavior unless the product requires a change.

---

## Pending / Loading States in Buttons

Keep button dimensions and label position stable across states. Use one of three patterns:

- Show only a spinner, preserving the label’s space and accessible name
- Keep the text unchanged and show a spinner in reserved space on its left
- Keep the text unchanged and only disable the button

Never let a spinner move the label or resize the button.

---

## List & Repeated Element Performance

React Compiler (`babel-plugin-react-compiler`) is enabled in newer apps `[detect vite.config.ts]` — it handles memoization, so don't hand-write `useMemo`/`useCallback` for compiler-covered cases. Structural costs still compound; when rendering 10+ repeated items:

- **Minimize per-item weight** — 1-2 components per row, audit DOM nodes, remove wrapper `<div>`s.
- **Event delegation** at 100+ items or 3+ handlers per item: one handler on the container reading `data-item-id`, not a closure per row.
- **Defer complexity to interaction** — one menu/tooltip rendered on demand for the active row, not mounted per row:

```typescript
const [menuTarget, setMenuTarget] = useState<string | null>(null)
{items.map((item) => (
  <Row key={item.id} onContextMenu={() => setMenuTarget(item.id)} />
))}
{menuTarget && <ContextMenu itemId={menuTarget} />}
```

- **No `useEffect` inside list items** — effects multiply with count; lift to the container.
- **Virtualize at 200+ items** (TanStack Virtual). Not below.
- **CSS**: flat class-based selectors on repeated elements; avoid `:has()` (per-parent child evaluation).

---

## Design System

Stack: **Tailwind CSS v4** (`@theme`) + **`@radix-ui/colors`** scales + **shadcn-style components** (cva variants, `tailwind-merge`) on **Base UI / Radix primitives**.

- Tokens are centralized stylesheets: `ui/stylesheets/{colors,typography,radius,shadows,utilities}.css` (in `packages/ui` when shared across apps). `colors.css` imports Radix color scales and maps them to shadcn-compatible variable names — components depend on those names.
- `[detect imports in ui components]` primitive library mix: newer components use `@base-ui/react`, older use `@radix-ui/react-*`. Match the file you're in; for new components follow the repo's majority.
- **No component styles in CSS files** — components are TSX using tokens.
- **Missing token?** Check the stylesheets first, then extend the design system — no one-off values or classes.
- **Never reinvent** an existing design-system component, icon, or pattern.

### UI copy and icons

UI copy has no final period: labels, buttons, hints, validation errors, toasts, leads, and empty states.
Join two clauses with a comma or use one clause. Emails, legal pages, articles, and SEO descriptions use sentence punctuation.
Follow the project's localization system.
Import Phosphor icons with the `Icon` suffix, such as `PlusIcon` and `MagnifyingGlassIcon`.

Do not use `||` to hide missing data or error states. Refine the type or parse the input.
Legitimate product defaults remain allowed.

### Phone surfaces

For phone products, PWAs, and phone flows, read [phone surfaces](references/phone-surfaces.md).
These rules do not apply automatically to desktop or mixed surfaces.

### Browser support

The baseline is the last 3 years of browsers and OS releases, counted from today. Use current platform APIs as they are (`URL.parse`, `Array.prototype.at`, `:has()`, `structuredClone`, …). No polyfills, no feature detection, no older forms for older devices, and reject review findings that argue for them. Older support only when the user asks for it explicitly.

### Visual design

For typography, spacing, surfaces, and interaction rules, read [visual design](references/visual-design.md).

### Storybook

- Framework package: `@storybook/tanstack-react` — `Meta`/`StoryObj` imported from it; typed meta: `const meta: Meta<typeof Component> = {...}`.
- **Stories are centralized under `.storybook/`** (`design-system/`, `components/`, `features/`, `pages/`), discovered relative to `.storybook/`, with shared title constants in `.storybook/story-paths.ts`. MSW via `msw-storybook-addon` for data-touching stories.
- Storybook-first UI workflow: spike new UI in a story before app code; stories are the UI spec — update them with every UI change and give the story URL when done.
- Stories never use the localization system. Story files and story data use plain text for all copy. Do not import message functions in a story, and do not add a message for a story. The production components that a story renders keep their own messages. The one exception is a story that shows internationalization itself, such as a locale switch.

### Query tests

Use a new `QueryClient` per test. Set `retry: false` in test defaults.
Use MSW when testing the network boundary. Test factory behavior through the cache where practical.
Read [data access](references/data-access.md#validation) for checks matched to the changed behavior.

### Performance targets

For performance work, read [performance targets](references/performance.md).

---

## Forms

`[detect package.json]`:
- **TanStack Form** (newer apps) with design-system `field.tsx` primitives.
- **react-hook-form + `@hookform/resolvers`** (older apps) with the shadcn `form.tsx` wrapper.

Either way: Zod schema as the single validation source (shared with the server function's `.validator`), field primitives from the design system, no ad-hoc form state.

Copy server data into form state on purpose, then pick one:

- Solo edit: `staleTime: Infinity` on the query. Snapshot, no background overwrite.
- Shared edit: keep Query live. Show `field.value ?? serverValue` so untouched fields still update.

Render the form only after data exists (`defaultValues` must be defined). After save, await invalidation and get the authoritative saved values.

- TanStack Form: `form.reset(savedValues)` resets the form and updates its default values.
- React Hook Form: `reset(savedValues)` resets the form from the supplied values. Supply the complete values when practical.

### TanStack Form rules

Sources: [shadcn TanStack Form](https://ui.shadcn.com/docs/forms/tanstack-form), [submission handling](https://tanstack.com/form/latest/docs/framework/react/guides/submission-handling), [form composition](https://tanstack.com/form/latest/docs/framework/react/guides/form-composition).

1. Validate with one schema at form level: `validationLogic: revalidateLogic({ mode, modeAfterSubmission })` and `validators: { onDynamic: Schema }`. Choose the timing per form and state why in a comment. Do not add field validators or hand-written checks in `onSubmit`. The `tanstack` lint plugin enforces these rules.
2. Type `defaultValues` as `z.input<typeof Schema>`. `onSubmit` receives input values. When input and output types differ, call `Schema.parse(value)`; otherwise use `value`.
3. Compute a time or random default once, with `useState(() => …)` or a module constant. TanStack Form resets an untouched form when `defaultValues` change between renders.
4. Wire each field with `id={field.name}`, `name={field.name}`, and `onBlur={field.handleBlur}`. `isInvalid = field.state.meta.isTouched && !field.state.meta.isValid` controls `data-invalid`, `aria-invalid`, and the error.
5. The form element uses `noValidate` and calls `event.preventDefault()`, then `form.handleSubmit()`.
6. A form component receives `pending` and `onSubmit(output)`. The consumer owns the mutation, toast, and dialog close.
7. Async validators use `onChangeAsync` or `onSubmitAsync`. The sync slots do not wait for a promise.
8. Server functions receive files only as `FormData`. Build it in the mutation factory.

## Auth (client side)

better-auth client in `lib/clients/auth-client`; a `lib/auth/` layer (hooks, models, services) wraps it — components consume `useSession`-style hooks, never the raw client. Route protection via route groups (`_auth`/`_authed` layouts) whose `beforeLoad` redirects unauthenticated users.
