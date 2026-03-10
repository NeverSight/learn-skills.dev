---
name: engineering-frontend-developer
description: "Build modern web applications with React, Vue, Angular, or Svelte, focusing on performance and accessibility. Use when you need component library development, TypeScript UI implementation, responsive layouts with CSS Grid and Flexbox, Core Web Vitals optimization, service worker offline support, code splitting, ARIA accessibility, Storybook integration, or frontend API client architecture."
metadata:
  version: "1.0.0"
---

# Frontend Development Guide

## Overview
This guide covers modern frontend development with React, Vue, Angular, and Svelte, including component architecture, performance optimization, accessibility, and testing. Use it when building web applications, component libraries, or optimizing frontend performance.

## Framework and Layout Decision Rules

- When choosing a framework, match it to team expertise and project constraints; default to React for broad ecosystem needs, Vue for progressive enhancement into existing pages, Svelte for bundle-size-critical apps, and Angular when the project requires an opinionated full-framework with built-in DI and routing.
- When implementing a design, use CSS Grid for two-dimensional page layouts and Flexbox for one-dimensional component alignment; avoid absolute positioning for layout purposes because it breaks responsive reflow.
- When building a component library, expose each component as a named export with TypeScript props interface, a Storybook story, and a unit test -- components without all three are not merged.
- When integrating with backend APIs, centralize fetch logic in a typed API client layer (e.g., a single `api.ts` module using `fetch` or `axios` with interceptors) so auth headers, error transforms, and retries are handled in one place.

## Performance Decision Rules

- When a page's Largest Contentful Paint exceeds 2.5 seconds in Lighthouse CI, treat it as a blocking bug -- profile with Chrome DevTools Performance tab and fix the largest bottleneck before merging.
- When adding animations, use CSS `transform` and `opacity` properties (compositor-only) rather than `width`, `height`, or `top`/`left` to avoid triggering layout recalculations that cause jank.
- When the app needs offline support, register a service worker with a cache-first strategy for static assets and a network-first strategy for API requests, falling back to cached responses when offline.
- When initial JS bundle exceeds the budget (e.g., 200 KB gzipped), add route-based code splitting with `React.lazy()` or dynamic `import()` and defer non-critical scripts below the fold.
- When supporting older browsers, define a browserslist config and let the build tool (Vite, Webpack) auto-polyfill; do not manually add polyfills or feature checks unless browserslist coverage is insufficient.
- When adding images, use `<picture>` with WebP/AVIF sources and explicit `width`/`height` attributes to prevent layout shift; for images below the fold, add `loading="lazy"`.
- When a route is not needed on initial page load, wrap it in `React.lazy()` (or framework equivalent) with a `<Suspense>` fallback so the main bundle excludes that route's code.
- When serving static assets, configure the CDN or server to set `Cache-Control: public, max-age=31536000, immutable` on content-hashed filenames and `no-cache` on `index.html`.

## Accessibility Decision Rules

- When building any interactive component, add ARIA attributes, keyboard handlers (`Enter`, `Space`, `Escape` as appropriate), and test with axe-core before marking the task complete.
- When building forms, associate every `<input>` with a `<label>` via `htmlFor`/`id`, provide visible error messages linked with `aria-describedby`, and ensure the form is fully operable with keyboard-only navigation.
- When using color to convey meaning (e.g., error states, status badges), always include a secondary indicator (icon, text, pattern) so color-blind users can distinguish states.
- When adding a modal or dropdown, trap focus inside the element while it is open and return focus to the trigger element on close; test by tabbing through the entire flow without a mouse.
- When a pull request adds a new interactive component, the PR must include an axe-core integration test that asserts zero WCAG 2.1 AA violations before it can be merged.

## CSS Debugging Decision Rules

When a layout breaks, diagnose by symptom:
- **Flex child overflows its container**: Add `min-width: 0` (row) or `min-height: 0` (column) to the flex child. Flex items default to `min-width: auto`, which prevents shrinking below content size.
- **Grid items ignore column width**: Use `minmax(0, 1fr)` instead of `1fr`. Plain `1fr` means `minmax(auto, 1fr)`, which lets content push the column wider than intended.
- **`position: sticky` does not stick**: Check every ancestor for `overflow: hidden`, `overflow: auto`, or `overflow: scroll`. Any of these creates a new scrolling context that contains the sticky element. Also verify the element has a `top`/`bottom` value set.
- **Element centered with `margin: auto` does not center**: Verify the element has an explicit `width` (block) or the parent has `display: flex` (flex child). `margin: auto` does nothing on full-width block elements.
- **`z-index` does not work**: The element needs `position: relative/absolute/fixed/sticky` to create a stacking context. Also check if an ancestor creates a stacking context (via `transform`, `opacity < 1`, `filter`, or `will-change`) that limits the z-index scope.
- **Gap between inline-block/inline elements**: Whitespace in HTML creates gaps. Fix: use `display: flex` on the parent (preferred), or set `font-size: 0` on parent and reset on children.
- **1px gap between adjacent elements**: Sub-pixel rendering. Fix: use `outline` instead of `border` for debugging, or set `background` on the parent to mask the gap.
- **Text truncation with ellipsis not working**: Requires all three: `overflow: hidden`, `white-space: nowrap`, `text-overflow: ellipsis`. For multi-line truncation, use `-webkit-line-clamp` with `display: -webkit-box` and `-webkit-box-orient: vertical`.
- **Container queries not applying**: Verify the ancestor has `container-type: inline-size` (or `size`). The element itself cannot be its own container — the query must reference a parent.

## Build Tooling Decision Rules

- **Vite** (default): Use for all new projects. Instant dev server via native ESM, fast HMR, Rollup-based production builds. If the project uses CommonJS-only dependencies that fail with Vite, add `optimizeDeps.include` for those packages — do not switch to Webpack.
- **Webpack**: Use only for existing projects that already use it, or when a specific Webpack-only plugin has no Vite equivalent (rare). Migrate to Vite when the opportunity arises (see Migration Decision Rules).
- **Turbopack**: Use only inside Next.js 14+ (`next dev --turbo`). Not yet usable standalone. Provides faster dev builds than Webpack for Next.js projects. If builds are already fast (<5s), do not bother switching.
- **esbuild**: Use for library bundling, scripts, or CLI tools — not for full applications. No HTML entry point handling, no code splitting by route. Use `tsup` (esbuild wrapper) for publishing npm packages.
- **SWC vs Babel**: Use SWC (via Vite plugin or Next.js default). SWC is 20-70x faster for transforms. Use Babel only if a project depends on a Babel-only plugin with no SWC equivalent (increasingly rare).
- **Monorepo tooling**: <5 packages = npm/pnpm workspaces, no extra tool. 5-20 packages = Turborepo for task caching. >20 packages or polyglot = Nx. Never add monorepo tooling to a single-package project.

## SSR and Server Components Decision Rules

### When to Use SSR vs CSR vs SSG
- **SSG (Static Site Generation)**: Use for content that changes less than once per hour (marketing pages, docs, blog posts). Build at deploy time. Fastest possible TTFB.
- **SSR (Server-Side Rendering)**: Use for personalized content (dashboards, user profiles), SEO-critical pages with dynamic data, or pages where stale data is unacceptable. Adds server latency to every request — cache aggressively with `Cache-Control` or CDN.
- **CSR (Client-Side Rendering)**: Use for authenticated-only pages (admin panels, internal tools) where SEO does not matter and interactivity is the priority. Simplest to build and deploy (static hosting).
- **ISR (Incremental Static Regeneration)**: Use for pages that are mostly static but need periodic updates (product listings, pricing pages). Set `revalidate` interval based on how stale the data can be: 60s for prices, 3600s for blog posts.

### React Server Components (RSC) Decision Rules
- **Default to Server Components**: Every component is a Server Component unless it needs interactivity. If a component has `onClick`, `useState`, `useEffect`, or browser APIs — it must be a Client Component (`'use client'`).
- **Data fetching**: Fetch data in Server Components with `async/await` directly — no `useEffect`, no TanStack Query, no loading states needed. The data is resolved before the HTML is sent.
- **Auth in Server Components**: Read the session/cookie in a Server Component and pass the user object as a prop to Client Components. Never read cookies or sessions in Client Components — they execute on the client.
- **When to use Server Actions vs API routes**: Use Server Actions (`'use server'`) for form submissions and mutations that are called from the UI. Use API routes (`/api/*`) for webhooks, third-party integrations, or endpoints called by external services.
- **Sharing state between Server and Client Components**: Pass serializable data as props from Server → Client. If you need client-side state derived from server data, initialize `useState` with the server prop and manage updates on the client.
- **Large data sets**: Stream with `<Suspense>` boundaries. Wrap the slow Server Component in `<Suspense fallback={<Skeleton />}>`. The shell renders immediately; the slow component streams in when ready. Place Suspense boundaries at meaningful UI sections (sidebar, main content, comments) — not around every component.

### Hydration Error Decision Tree
- **Error: "Text content does not match"**: A value differs between server and client render. Common causes:
  1. `Date.now()`, `Math.random()`, or `new Date().toLocaleString()` in render → move to `useEffect` + `useState`.
  2. `typeof window !== 'undefined'` conditional rendering → use `useEffect` to set a `hasMounted` flag.
  3. Browser extensions injecting DOM nodes → not your bug, but test in incognito to confirm.
- **Error: "Hydration failed because the server rendered HTML didn't match"**: A structural difference (different elements). Common causes:
  1. `<p>` nested inside `<p>`, or `<div>` inside `<p>` → fix the nesting, HTML spec does not allow it.
  2. A third-party component renders differently on server vs client → wrap in `dynamic(() => import(...), { ssr: false })`.
  3. Missing closing tags or self-closing tags where HTML requires explicit close.

## Performance Debugging Workflow

When a page is slow, follow this sequence — do not skip steps:

### Step 1: Identify the bottleneck type
- Run Lighthouse. Check which metric is failing:
  - **LCP >2.5s**: The largest visible element loads too slowly. Go to Step 2.
  - **FID/INP >200ms**: User interaction is blocked by JavaScript. Go to Step 3.
  - **CLS >0.1**: Layout shifts after initial paint. Go to Step 4.

### Step 2: Fix LCP
1. **Check what the LCP element is** (Lighthouse shows it). Usually: hero image, heading text, or video.
2. If **image**: Add `priority` (Next.js) or `fetchpriority="high"`. Add explicit `width`/`height`. Serve in WebP/AVIF. If served from a CDN, verify cache headers.
3. If **text**: Check for render-blocking fonts. Use `font-display: swap` or `font-display: optional`. Preload the critical font file with `<link rel="preload" as="font" crossorigin>`.
4. If **blocked by JS**: The bundle is too large. Check Step 3. The LCP element cannot render until the JS that creates it is loaded and executed.
5. Check the **server response time** (TTFB). If TTFB >600ms, the bottleneck is backend or CDN — not frontend.

### Step 3: Fix INP (Interaction to Next Paint)
1. Open Chrome DevTools → Performance → record a click/type interaction.
2. Find the **Long Task** (>50ms yellow bar). Click it to see the call stack.
3. If the long task is **your code**: Break the work into smaller chunks with `requestIdleCallback`, `scheduler.yield()` (Chrome 115+), or `setTimeout(fn, 0)` to yield to the browser between frames.
4. If the long task is **React re-rendering**: Open React DevTools Profiler. Find the component that re-renders. Common fixes: `React.memo` (expensive children), `useMemo` (derived values), or move state closer to where it is used. If >500 components re-render on a single state change, the state is too high in the tree.
5. If the long task is **third-party script** (analytics, ads): Defer with `async` or `defer` attribute, or load after `requestIdleCallback`.

### Step 4: Fix CLS
1. Check which element shifts (Lighthouse shows it, or use DevTools → "Layout Shift Regions").
2. **Image/video without dimensions**: Add `width` and `height` attributes (or `aspect-ratio` CSS). The browser reserves space before the asset loads.
3. **Font swap**: The fallback font has different metrics than the web font. Use `size-adjust` in `@font-face` to match metrics, or use `font-display: optional` to eliminate the swap entirely.
4. **Dynamic content injected above the fold**: Ads, banners, cookie notices. Reserve space with `min-height` on the container. If the content height varies, use `contain: layout` to prevent shifts from propagating.
5. **Late-loading CSS**: If a stylesheet loads after first paint and changes visible layout, inline the critical CSS or preload the stylesheet.

## Code Quality Decision Rules

- When writing tests, require every component to have at least one unit test covering its primary render path and one interaction test (click, keyboard) -- enforce via a CI coverage gate of 80% line coverage minimum.
- When starting a project, enable `strict: true` in `tsconfig.json` on day one; retrofitting strict mode later is exponentially harder as the codebase grows.
- When an API call or async operation fails, display a user-facing error message with a retry action -- never swallow errors silently or show raw exception text.
- When a component file exceeds 300 lines, split it into smaller sub-components with a shared barrel export; large files signal mixed responsibilities.
- When setting up CI, include lint (ESLint), type-check (`tsc --noEmit`), test (Vitest/Jest), and bundle-size check as required gates -- all four must pass before merge.

## Workflow

### Step 1: Project Setup and Architecture
- Set up modern development environment with proper tooling.
- Configure build optimization and performance monitoring.
- Establish testing framework and CI/CD integration.
- Create component architecture and design system foundation.

### Step 2: Component Development
- Create reusable component library with proper TypeScript types.
- Implement responsive design with mobile-first approach.
- Build accessibility into components from the start.
- Create comprehensive unit tests for all components.

### Step 3: Performance Optimization
- Implement code splitting and lazy loading strategies.
- Optimize images and assets for web delivery.
- Monitor Core Web Vitals and optimize accordingly.
- Set up performance budgets and monitoring.

### Step 4: Testing and Quality Assurance
- Write comprehensive unit and integration tests.
- Perform accessibility testing with real assistive technologies.
- Test cross-browser compatibility and responsive behavior.
- Implement end-to-end testing for critical user flows.

## Reference

### Lighthouse CI Targets
- Performance score: 90+
- All interactive elements keyboard-navigable with visible focus indicators
- axe-core: zero violations at WCAG 2.1 AA level
- Bundle size: < 200 KB gzipped for initial JS (enforce with `bundlesize` or equivalent)
- Zero TypeScript `any` casts in production code; `strict: true` enabled in tsconfig

## Migration Decision Rules
- **CRA to Vite**: Migrate when CRA's build time exceeds 30s or eject pressure mounts. Steps: replace `react-scripts` with `vite` + `@vitejs/plugin-react`, move `index.html` to root, update `process.env` → `import.meta.env`, fix any CommonJS imports. Budget: 2-4 hours for small apps, 1-2 days for large apps with custom Webpack config.
- **Pages Router to App Router (Next.js)**: Migrate incrementally. Move one route at a time to `app/` directory. Start with static/simple pages, leave complex pages (with getServerSideProps + complex state) for last. Do not migrate the entire app at once. Budget: 1 route per day for complex apps.
- **JavaScript to TypeScript**: Enable `allowJs: true` in tsconfig and rename files one at a time from `.js` → `.tsx`. Start with leaf components (no dependencies), work inward. Enforce `strict: true` on new files from day one; create a `tsconfig.strict.json` that extends base if needed. Budget: ~10 files per day.
- **CSS Modules to Tailwind**: Do not rewrite all styles at once. Install Tailwind alongside CSS Modules. New components use Tailwind; migrate old components only when you touch them for other reasons. Budget: per-component during normal development.
- **Class components to hooks**: Migrate only when you need to modify the component for a feature change. Do not migrate stable, untouched class components — they work fine. When migrating: `componentDidMount` → `useEffect(..., [])`, `componentDidUpdate` → `useEffect` with deps, `this.state` → `useState`.

## State Management Decision Matrix
- **<5 components sharing state**: Lift state up with props. No library needed. If prop drilling goes >3 levels, add React Context for that specific slice.
- **5-15 components with shared state**: Use React Context + `useReducer` for structured state, or Zustand for simpler API. If the state is server data, use TanStack Query instead — not Context.
- **>15 components or complex derived state**: Zustand (simple, small bundle) or Jotai (atomic, bottom-up). Use Redux Toolkit only if the team already knows Redux. Never introduce Redux to a new project.
- **Server state (API data, caching, sync)**: TanStack Query (React), SWR (simpler needs), or Apollo Client (GraphQL). Never store server data in a client state manager (Zustand, Redux) — it causes stale data and duplicate cache management.
- **Form state**: react-hook-form for complex forms (>5 fields, validation, dynamic fields). Native `useState` for simple forms (<5 fields, no complex validation). Never use a global state manager for form state.
- **URL state (filters, pagination, search)**: Use URL search params (`useSearchParams`) as the source of truth. Sync to component state only for derived values. This makes the state shareable, bookmarkable, and back-button friendly.

## Self-Verification Protocol
After completing a frontend implementation, verify:
- Run Lighthouse CI and confirm: Performance >=90, Accessibility >=90, Best Practices >=90. If any score drops below 90, fix before merge.
- Run `npx axe-core` or `axe-playwright` on every new page/component. Zero WCAG 2.1 AA violations.
- Test keyboard navigation: Tab through the entire page. Every interactive element must be reachable and operable. Focus indicators must be visible.
- Open the browser DevTools Performance tab, record a user interaction, and check for: layout thrashing (forced reflows), long tasks >50ms, excessive re-renders.
- Check bundle size: run `npx bundlesize` or check the build output. If initial JS exceeds 200KB gzipped, investigate what is in the bundle (use `npx source-map-explorer`).
- Test responsive layout at 320px, 768px, and 1280px. No horizontal scroll, no overlapping elements, no unreadable text.
- Test with browser devtools network throttling set to "Slow 3G." If the page is unusable, add loading states and optimize critical rendering path.

## Failure Recovery
- **Component re-renders excessively**: Use React DevTools Profiler to identify the cause. Common fixes: memoize with `React.memo` (for expensive children), `useMemo`/`useCallback` (for derived values/callbacks passed as props), or move state closer to where it is used.
- **Bundle size suddenly increased**: Run `source-map-explorer` to find the culprit. Common causes: importing an entire library (`import _ from 'lodash'` → `import groupBy from 'lodash/groupBy'`), accidentally bundling a dev dependency, or a heavy polyfill.
- **Hydration mismatch (SSR/SSG)**: The server-rendered HTML differs from client render. Common causes: using `Date.now()` or `Math.random()` in render, accessing `window`/`document` during SSR, or conditional rendering based on client-only state. Fix: use `useEffect` for client-only values, or `suppressHydrationWarning` as last resort.
- **CSS layout breaks at specific viewport**: Check for: hardcoded pixel widths, missing `min-width: 0` on flex children, `overflow: hidden` clipping content, or `position: absolute` elements escaping their container. Use CSS Grid with `minmax()` instead of fixed widths.
- **API calls fire too many times**: Check for missing or incorrect `useEffect` dependency arrays. If using TanStack Query, set `staleTime` to avoid refetching on every mount. If using `useEffect` for data fetching, consider switching to a data fetching library entirely.

## Existing Codebase Orientation
When joining an existing frontend project:
1. **Run `npm start` / `npm run dev`** (5 min) — If it fails, fix the dev environment first.
2. **Check the tech stack** (5 min) — Framework (React/Vue/Angular/Svelte), bundler (Vite/Webpack/Turbopack), CSS approach (Tailwind/CSS Modules/styled-components), state management, testing library.
3. **Run the test suite** (5 min) — `npm test`. Note coverage, test types, and which flows are untested.
4. **Open the browser DevTools** (10 min) — Check bundle size (Network tab), console errors, Lighthouse score. These are your baseline numbers.
5. **Read the component tree** (10 min) — Start from the app root. Map the top-level routes and their key components. Identify shared components (design system, layout).
6. **Check for tech debt signals** (5 min) — Any `any` casts? `eslint-disable` comments? Files >500 lines? Inline styles? These indicate areas of fragility.
7. **Identify the data flow** (10 min) — How does data get from the API to the UI? Is there a centralized API client? Are there loading/error states? Is server state managed with a library or manually?

## Scripts

- `scripts/check_bundle.sh` -- Analyze a build output directory for JS and CSS bundle sizes, with gzip estimates and configurable warning/error thresholds. Run with `--help` for options.

See [DataTable Component](references/data-table.md) for a full virtualized DataTable implementation in React + TypeScript.
See [React Component Patterns](references/react-patterns.md) for compound components, custom hooks, error boundaries, optimistic UI, and form validation patterns.
See [TypeScript Patterns](references/typescript-patterns.md) for discriminated unions, polymorphic components, branded types, and type-safe API clients.
See [CSS Patterns](references/css-patterns.md) for modern CSS Grid layouts, container queries, theming, view transitions, and :has() selectors.
