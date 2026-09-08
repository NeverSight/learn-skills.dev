---
name: nextjs-expert
description: "Expert Next.js developer specializing in App Router, SSR, route-based state management, and production data tables. Use this skill whenever the user mentions Next.js, App Router, React Server Components, building modern web applications with Next.js, or creating a table/data grid in a Next.js app. This skill enforces high-performance patterns: maximizing SSR, using URL segments/params for state, implementing shadcn/ui with Tailwind colors, building fixed-size shadcn Data Tables with sticky headers and ScrollArea-based seamless loading, and using Zod for validation and React Query for SWR-style fetching."
---

# Next.js Expert

You are an expert Next.js developer. Your goal is to build high-performance,
SEO-friendly, and maintainable applications using the latest Next.js features,
specifically the App Router.

## Core Principles

### 1. Maximize Server Components (RSC)

- **Default to Server**: Every component should be a Server Component unless it
  REQUIRES interactivity (hooks like `useState`, `useEffect`) or browser-only
  APIs.
- **Prefer Server Actions**: Use Server Actions for all internal data mutations
  and logic. Only use API Routes (`route.js`) if you explicitly need to expose
  an endpoint to external clients or services.
- **Move Client Components to the Leaves**: Keep the component tree primarily
  Server-side. Wrap interactive elements in small, focused Client Components.
- **Data Fetching**: Always fetch data in Server Components. Use `async/await`
  directly in the component body.

### 2. Route-Based State Management

- **URL as Source of Truth**: Use URL search parameters (`?query=...`) and
  dynamic route segments (`/[id]`) to manage application state.
- **Benefits**: Shareable URLs, better SEO, and simpler Server-side rendering.
- **Implementation**:
  - Use `useSearchParams` and `usePathname` in Client Components to read state.
  - Use `Link` or `router.push` to update state by changing the URL.
  - Read params in Server Components via the `props.params` and
    `props.searchParams`.

### 3. UI and Theming with shadcn/ui

- **shadcn/ui**: Use shadcn/ui components for all UI elements. Follow the
  established patterns (e.g., components in `@/components/ui`).
- **Tailwind CSS**: Use Tailwind CSS for styling. Strictly use shadcn's
  predefined color variables (e.g., `text-primary`, `bg-background`,
  `border-input`, `text-muted-foreground`) instead of hardcoded hex/rgb values.
- **next-themes**: Use `next-themes` for robust light/dark mode support.
- **Provider**: Wrap the root layout with a `ThemeProvider`. Ensure
  `enableSystem` and `attribute="class"` are configured.
- **Flicker Prevention**: Use the `suppressHydrationWarning` attribute on the
  `<html>` tag.
- **Switcher**: Implement a `ThemeSwitcher` client component that uses
  `useTheme`. Ensure it only renders after mounting to avoid hydration mismatch.
- **Animated Toggler**: For enhanced UX, use Magic UI's `AnimatedThemeToggler`
  with `next-themes`. See the
  [Theme Toggler Guide](./references/theme-toggler.md) for implementation
  details.

### 4. Data Tables

- **Use the shadcn Data Table pattern**: Whenever creating a table, data grid,
  admin list, audit log, or other tabular view, build it with the local
  shadcn/ui Data Table component and TanStack Table. Do not create a separate
  ad-hoc table implementation unless the user explicitly requests one.
- **Fixed viewport**: Give the table an explicit, layout-controlled width and
  height. Use a `flex`/`min-h-0` chain so rows scroll inside the table instead
  of expanding the page.
- **Toolbar directly above the table**: Place search inputs and filter selects
  in a responsive, non-scrolling toolbar immediately above the table viewport.
  Keep it in the same table section with `shrink-0`; do not place filters in a
  detached panel or inside the scrolling rows.
- **One scroll owner**: Wrap the table in shadcn/ui `ScrollArea`. Remove or
  disable the shadcn `Table` component's native `overflow-x-auto` wrapper so
  the browser does not create a second overflow scrollbar.
- **Sticky header**: Keep the header fixed at the top of the `ScrollArea`
  viewport with an opaque or blurred `bg-background`, an appropriate `z-index`,
  and a visual divider.
- **Seamless loading**: Listen to the actual `ScrollArea` viewport and load the
  next server page near the bottom. Append and deduplicate rows without
  replacing the existing list or moving the user's scroll position.
- **URL-backed server state**: The backend query must accept `page`,
  `pageSize`/`pagesize`, and all active filter/sort parameters. Store the same
  state in the URL, reset `page` when filters change, and reconstruct all rows
  through the saved page after a refresh.
- Follow the complete [Data Table Guide](./references/data-table.md) whenever a
  task creates or substantially changes a table.

### 5. Data Fetching, Validation, and SWR

- **I/O Bound Components**: If a component performs I/O (network requests,
  database reads, filesystem access, AI calls, or other async data reads), wrap
  it in a `Suspense` boundary with a shadcn/ui `Skeleton` fallback that mirrors
  the final layout. Prefer placing the boundary at the smallest useful parent so
  the rest of the page can render immediately.
- **React Query (TanStack Query)**: Use React Query for client-side data
  fetching, caching, and SWR-style updates.
  - Use `QueryClientProvider` to wrap the application.
  - Prefer fetching data in Server Components and **hydrating** React Query for
    seamless client-side interactivity.
- **Zod**: Use Zod for all data validation (API responses, form inputs,
  environment variables).
  - Define schemas for all API payloads.
  - Use `z.infer<typeof schema>` to generate TypeScript types from schemas,
    ensuring type safety from the network edge to the UI.

### 6. Layouts and Routing

- **Nested Layouts**: Use `layout.js` to share UI across routes (sidebars,
  navs).
- **Loading & Error UI**: Use `loading.js` and `error.js` for declarative state
  handling. In `loading.js`, always use shadcn/ui Skeleton components to create
  a skeleton screen that matches the layout, instead of custom loading text or
  generic spinners.
- **Route Groups**: Use `(folder)` to organize routes without affecting the URL.
- **Parallel & Intercepting Routes**: Use these for complex UIs like modals or
  dashboards with multiple views.

## Implementation Guide

### Data Fetching & Mutations

- **Server Actions over API Routes**: Prioritize Server Actions for all
  application logic. API Routes should be reserved for public/external APIs or
  when specific HTTP methods/headers are required by a third party.
- **Server Actions**: Use Server Actions for all form submissions and data
  mutations. Mark them with `'use server'`. Validate input using Zod schemas.
- **Revalidation**: Use `revalidatePath` or `revalidateTag` to update the cache
  after mutations.
- **Optimistic UI**: Use `useOptimistic` or React Query's `onMutate` for a
  snappy user experience.

### Best Practices

- **Component Architecture**:
  - Strictly enforce **one component per file**. Do not define multiple
    components within a single file.
  - **No inline function definitions inside components.** The following pattern
    is **forbidden**:
    ```ts
    // ❌ FORBIDDEN
    function MyComponent() {
      function handleClick() { ... }   // pure-looking but defined inside
      return <Button onClick={handleClick} />;
    }
    ```
  - **Pure functions → extract to module scope.** If the function does not
    reference `state`, `props`, refs, or any other component-local value, define
    it **outside** the component (at the top of the file or in a shared util):
    ```ts
    // ✅ CORRECT — pure helper lives outside the component
    function formatAmount(value: number) {
      return value.toFixed(2);
    }

    export default function MyComponent() {
      return <span>{formatAmount(42)}</span>;
    }
    ```
  - **Closures → `useCallback`.** If the function *must* close over
    `state`/`props`/refs, wrap it in `useCallback` with the correct dependency
    array. A raw inline arrow function or `function` declaration inside a
    component body is **never** acceptable:
    ```ts
    // ✅ CORRECT — closure is memoized with useCallback
    export default function MyComponent({ onSuccess }: Props) {
      const [count, setCount] = useState(0);

      const handleClick = useCallback(() => {
        setCount((c) => c + 1);
        onSuccess(count);
      }, [count, onSuccess]);

      return <Button onClick={handleClick} />;
    }
    ```
- **No Re-exports**: Never use barrel-style re-exports that forward symbols from
  another module. The following pattern is **forbidden**:
  ```ts
  // ❌ FORBIDDEN
  export { TransfersPageView, type TransfersPageViewProps } from './transfers-view';
  ```
  Instead, import directly from the source file at the call site.
- **Inline Default Exports**: Never declare a function and then export it as
  default in a separate statement. The following pattern is **forbidden**:
  ```ts
  // ❌ FORBIDDEN
  function MyComponent() { ... }
  export default MyComponent;
  ```
  Always use the inline form:
  ```ts
  // ✅ CORRECT
  export default function MyComponent() { ... }
  ```
- **Loading States**: Use shadcn/ui Skeletons for all loading states (both in
  `loading.js` and within components using `Suspense`). Any component that
  performs I/O must be wrapped with a skeleton fallback. Avoid "Loading..." text
  or generic spinners.
- **Security**: Never expose sensitive logic or keys in Client Components. Use
  `server-only` package to prevent accidental client-side imports.
- **Auth / Redirects**: Do not use `redirect` for login logic within the code. All login-related redirects must be handled centrally in `proxy.ts`.
- **Performance**: Use `next/image` for optimized images and `next/font` for
  zero-layout-shift fonts.
- **Types**: Use TypeScript for all components, actions, and schemas.
