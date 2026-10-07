---
name: antigravity-react-best-practices
description: Best practices for building production-ready React SPAs with Vite including caching, lazy loading, and architectural patterns.
---
# Vite React Best Practices

A comprehensive guide for building production-ready React Single Page Applications (SPAs) with Vite.

### 1. Vite SPA Deployment (CRITICAL)
- **Static Rewrites**: Mandatory for client-side routing. Configure your hosting (Vercel, Netlify, Nginx) to redirect all `/*` requests to `/index.html`.
- **Caching Strategy**: Ensure that `assets/` (which contains hashed JS/CSS files) is cached aggressively (immutable, 1 year). However, the `index.html` must be configured with `Cache-Control: no-cache` so users always get the latest bundle hash map.
- **Environment Variables**: Only expose variables prefixed with `VITE_` to the client. Keep secrets out of client bundles.

### 2. React Core Performance
- **Route Splitting**: Implement code splitting at the route level using `React.lazy()` and `<Suspense>`.
- **Server State**: Do not handle complex async data fetching with naive `useEffect` loops. Use robust server-state libraries like React Query, SWR, or RTK Query.
- **Memoization**: Do not blanket everything with `useMemo` or `useCallback`. Apply memoization locally where referential equality matters for child components wrapped in `React.memo`, or for expensive mathematical computations.
- **Image Optimization**: Prevent Cumulative Layout Shift (CLS) by hardcoding image aspect ratios or utilizing modern `srcset` tools.

### 3. Architecture & Cleanup
- **Colocation**: Adopt a feature-based architecture (e.g., placing components, hooks, and tests belonging to the same feature inside a dedicated folder, rather than splitting by type).
- **Anti-Patterns**: Never import from the `dist/` or `build/` folder internally within the app source code (double bundling vulnerability).
- **Absolute Imports**: Configure `tsconfig.json` and `vite.config.ts` to support `@/` path alias mapping to the `src/` directory to avoid messy `../../../` imports.
