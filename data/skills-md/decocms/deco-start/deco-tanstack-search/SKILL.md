---
name: deco-tanstack-search
description: Implement and debug search functionality in Deco storefronts on TanStack Start. Covers the full search data flow from SearchBar to VTEX Intelligent Search API, including URL parameter propagation, CMS page resolution, filter toggling, pagination, and common pitfalls.
---

# Deco TanStack Search

Complete reference for implementing search in Deco storefronts running on TanStack Start / React / Cloudflare Workers.

## When to Use This Skill

- Implementing or debugging search (`/s?q=...`) pages
- Fixing "search returns no results" or "search page shows 404"
- Adding filter support to PLP/search pages
- Debugging pagination or sort not working
- Porting search from Fresh/Deno to TanStack Start
- Understanding how URL parameters flow from the browser to VTEX Intelligent Search API

## Architecture: The Search Data Flow

The search flow spans **four layers**. Understanding each layer is critical for debugging.

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. BROWSER — SearchBar component                                 │
│    User types "telha" → form submits                             │
│    navigate({ to: "/s", search: { q: "telha" } })               │
│    URL becomes: /s?q=telha                                       │
├──────────────────────────────────────────────────────────────────┤
│ 2. TANSTACK ROUTER — cmsRouteConfig in $.tsx                     │
│    loaderDeps extracts search params: { q: "telha" }             │
│    loader builds fullPath: "/s?q=telha"                          │
│    Calls loadCmsPage({ data: "/s?q=telha" })                     │
├──────────────────────────────────────────────────────────────────┤
│ 3. @decocms/start — CMS resolution pipeline                     │
│    findPageByPath("/s") → matches CMS page with path: "/s"      │
│    matcherCtx.url = "http://localhost:5173/s?q=telha"            │
│    resolve.ts injects __pagePath="/s" and __pageUrl="...?q=telha"│
│    into commerce loader props                                    │
├──────────────────────────────────────────────────────────────────┤
│ 4. @decocms/apps — VTEX productListingPage loader                │
│    Reads query from: props.query ?? __pageUrl.searchParams("q")  │
│    Reads sort from: props.sort ?? __pageUrl.searchParams("sort") │
│    Reads page from: props.page ?? __pageUrl.searchParams("page") │
│    Reads filters from: __pageUrl filter.* params                 │
│    Calls VTEX Intelligent Search API                             │
└──────────────────────────────────────────────────────────────────┘
```

## Layer 1: SearchBar Component

### Correct Pattern (TanStack Router)

```tsx
import { useNavigate, Link } from "@tanstack/react-router";

function Searchbar({ action = "/s", name = "q" }) {
  const navigate = useNavigate();

  return (
    <form
      action={action}
      onSubmit={(e) => {
        e.preventDefault();
        const q = new FormData(e.currentTarget).get(name)?.toString();
        if (q) navigate({ to: action, search: { q } });
      }}
    >
      <input name={name} placeholder="Buscar..." />
      <button type="submit">Buscar</button>
    </form>
  );
}
```

### Suggestion Links — Correct vs Wrong

```tsx
// WRONG — query string embedded in path, TanStack Router doesn't parse it
<Link to={`/s?q=${query}`}>Buscar por "{query}"</Link>

// CORRECT — search params as separate object
<Link to="/s" search={{ q: query }}>Buscar por "{query}"</Link>
```

**Why it matters**: TanStack Router treats `to` as a path. If you embed `?q=telha` in the path, the router navigates to a path literally named `/s?q=telha` instead of `/s` with search param `q=telha`. The `loaderDeps` function receives an empty `search` object and no query reaches the API.

### Autocomplete / Suggestion Links

Category/product suggestion links should also use TanStack Router `<Link>`:

```tsx
{autocomplete.map(({ name, slug }) => (
  <Link to={`/${slug}`} preload="intent">{name}</Link>
))}
```

## Layer 2: Route Configuration ($.tsx)

The catch-all route uses `cmsRouteConfig` from `@decocms/start/routes`:

```tsx
// src/routes/$.tsx
import { createFileRoute, notFound } from "@tanstack/react-router";
import { cmsRouteConfig, loadDeferredSection } from "@decocms/start/routes";
import { DecoPageRenderer } from "@decocms/start/hooks";

const config = cmsRouteConfig({
  siteName: "My Store",
  defaultTitle: "My Store - Products",
  ignoreSearchParams: ["skuId"], // Do NOT ignore: q, sort, page, filter.*
});

export const Route = createFileRoute("/$")({
  loaderDeps: config.loaderDeps,
  loader: async (ctx) => {
    const page = await config.loader(ctx);
    if (!page) throw notFound();
    return page;
  },
  component: CmsPage,
  // ...
});
```

### Critical: ignoreSearchParams

`ignoreSearchParams` controls which URL params are excluded from `loaderDeps`. When a param is ignored, changing it does NOT trigger a server re-fetch.

**Never ignore**: `q`, `sort`, `page`, `fuzzy`, any `filter.*` param.

**Safe to ignore**: `skuId` (variant selection is client-side), `utm_*`, `gclid`.

### How loaderDeps works

```ts
loaderDeps: ({ search }) => {
  // search = { q: "telha", sort: "price:asc" }
  // After filtering ignoreSearchParams:
  return { search: { q: "telha", sort: "price:asc" } };
}
```

The loader receives `deps.search` and builds the full path:
```ts
const basePath = "/" + (params._splat || "");  // "/s"
const searchStr = "?" + new URLSearchParams(deps.search).toString(); // "?q=telha&sort=price:asc"
loadCmsPage({ data: "/s?q=telha&sort=price:asc" });
```

## Layer 3: CMS Resolution (@decocms/start)

### Page Matching

`findPageByPath("/s")` searches CMS blocks for a page with `path: "/s"`.

**Prerequisite**: The CMS must have a page block with `"path": "/s"` — typically `pages-search-*.json` in `.deco/blocks/`.

If the page block is missing from `blocks.gen.ts`, search will 404. Regenerate with:

```bash
npm run generate:blocks
# or
npx tsx node_modules/@decocms/start/scripts/generate-blocks.ts
```

### __pageUrl Injection

In `resolve.ts`, when a commerce loader is called:

```ts
if (rctx.matcherCtx.path) {
  resolvedProps.__pagePath = rctx.matcherCtx.path;  // "/s"
}
if (rctx.matcherCtx.url) {
  resolvedProps.__pageUrl = rctx.matcherCtx.url;    // "http://localhost:5173/s?q=telha"
}
```

This is how the request URL reaches the commerce loader — not via `Request` object (as in Fresh), but via injected props.

## Layer 4: Commerce Loader (VTEX)

### The productListingPage Loader

The loader must read search parameters from `__pageUrl` as fallback when `props.query` is not set by the CMS:

```ts
export interface PLPProps {
  query?: string;
  count?: number;
  sort?: string;
  fuzzy?: string;
  page?: number;
  selectedFacets?: SelectedFacet[];
  hideUnavailableItems?: boolean;
  __pagePath?: string;
  __pageUrl?: string;   // ← CRITICAL: must be declared
}

export default async function vtexProductListingPage(props: PLPProps) {
  const pageUrl = props.__pageUrl
    ? new URL(props.__pageUrl, "https://localhost")
    : null;

  // Read from props first (CMS override), then URL (runtime), then default
  const query = props.query ?? pageUrl?.searchParams.get("q") ?? "";
  const count = Number(pageUrl?.searchParams.get("PS") ?? props.count ?? 12);
  const sort = props.sort || pageUrl?.searchParams.get("sort") || "";
  const fuzzy = props.fuzzy ?? pageUrl?.searchParams.get("fuzzy") ?? undefined;
  const pageFromUrl = pageUrl?.searchParams.get("page");
  const page = props.page ?? (pageFromUrl ? Number(pageFromUrl) - 1 : 0);
  // ...
}
```

### Filter Extraction from URL

Users apply filters via URL params like `?filter.category-1=telhas&filter.brand=saint-gobain`. The loader must parse these:

```ts
if (pageUrl) {
  for (const [name, value] of pageUrl.searchParams.entries()) {
    const dotIndex = name.indexOf(".");
    if (dotIndex > 0 && name.slice(0, dotIndex) === "filter") {
      const key = name.slice(dotIndex + 1);
      if (key && !facets.some((f) => f.key === key && f.value === value)) {
        facets.push({ key, value });
      }
    }
  }
}
```

### Pagination Links Must Preserve URL Params

When building `nextPage`/`previousPage` URLs, persist all current URL params (q, sort, filter.*) and only change the page number:

```ts
const paramsToPersist = new URLSearchParams();
if (pageUrl) {
  for (const [k, v] of pageUrl.searchParams.entries()) {
    if (k !== "page" && k !== "PS" && !k.startsWith("filter.")) {
      paramsToPersist.append(k, v);
    }
  }
} else {
  if (query) paramsToPersist.set("q", query);
  if (sort) paramsToPersist.set("sort", sort);
}

// Filter toggle URLs also need paramsToPersist
const filters = visibleFacets.map(toFilter(facets, paramsToPersist));
```

## Key Difference: Fresh/Deno vs TanStack Start

| Aspect | Fresh/Deno (original) | TanStack Start |
|--------|----------------------|----------------|
| **Request access** | Loader receives `Request` directly | Loader receives CMS-resolved props |
| **URL reading** | `url.searchParams.get("q")` | `props.__pageUrl` → parse URL |
| **Navigation** | `<a href="/s?q=...">` (full reload) | `navigate({ to: "/s", search: { q } })` (SPA) |
| **Route matching** | Deco runtime matches `/s` | TanStack catch-all `/$` + `cmsRouteConfig` |
| **Param flow** | Direct from Request | URL → loaderDeps → loadCmsPage → matcherCtx → resolve.ts → __pageUrl |

## CMS Page Block Structure

The search page block (`.deco/blocks/pages-search-*.json`) should look like:

```json
{
  "name": "Search",
  "path": "/s",
  "sections": [
    {
      "page": {
        "sort": "",
        "count": 12,
        "fuzzy": "automatic",
        "__resolveType": "vtex/loaders/intelligentSearch/productListingPage.ts",
        "selectedFacets": []
      },
      "__resolveType": "site/sections/Product/SearchResult.tsx"
    }
  ],
  "__resolveType": "website/pages/Page.tsx"
}
```

**Important**: The `page.query` field is intentionally empty/absent. The query comes from the URL at runtime via `__pageUrl`.

## Debugging Checklist

When search is broken, check each layer:

### 1. Is the URL correct?
```
Expected: /s?q=telha
Check: Browser address bar after search submit
```

### 2. Are search params reaching loaderDeps?
Add a temporary log in `$.tsx`:
```ts
loader: async (ctx) => {
  console.log("[CMS Route] deps:", ctx.deps);
  // Should show: { search: { q: "telha" } }
}
```

### 3. Does the CMS page exist?
```bash
# Check blocks.gen.ts has the search page
grep '"path": "/s"' src/server/cms/blocks.gen.ts
# If missing, regenerate:
npm run generate:blocks
```

### 4. Is __pageUrl being injected?
Add a temporary log in the commerce loader:
```ts
console.log("[PLP] __pageUrl:", props.__pageUrl);
// Should show: "http://localhost:5173/s?q=telha"
```

### 5. Is the query reaching VTEX API?
Check terminal output for the Intelligent Search API call:
```
[vtex] GET .../api/io/_v/api/intelligent-search/product_search/?query=telha&...
```

### 6. Is the loader returning null?
The loader returns `null` when both `facets` and `query` are empty:
```ts
if (!facets.length && !query) {
  return null;  // ← This triggers "no results" / NotFound
}
```

## Common Pitfalls

### 1. Query string in Link `to` prop
```tsx
// BUG: TanStack Router doesn't parse ?q= from `to`
<Link to={`/s?q=${query}`}>
// FIX: Use search prop
<Link to="/s" search={{ q: query }}>
```

### 2. Missing __pageUrl in loader interface
If `PLPProps` doesn't declare `__pageUrl`, TypeScript won't complain (it's injected dynamically), but the loader won't read it.

### 3. blocks.gen.ts out of date
After adding/editing CMS blocks locally, `blocks.gen.ts` must be regenerated. Automate in `package.json`:
```json
"dev": "npm run generate:blocks && vite dev"
```

### 4. ignoreSearchParams filtering out q
If `ignoreSearchParams` includes `"q"`, search will never work. Only ignore client-side-only params.

### 5. Shopify vs VTEX patterns
Shopify loader already reads `__pageUrl` correctly:
```ts
const query = props.query || pageUrl.searchParams.get("q") || "";
```
VTEX initially didn't — this was the root cause of the espacosmart search bug.

### 6. Duplicate search param keys (filters)

VTEX filter URLs use duplicate keys: `?filter.category-1=telhas&filter.category-1=pisos`.
TanStack Router's `search` is a plain `Record<string, string>` — it **cannot represent duplicate keys**.

**Consequences**:
- `navigate({ search: Object.fromEntries(params) })` loses all but the last value per key
- `loaderDeps` receives a flat object, so the `loader` builds a URL with collapsed params

**Solution**: Use plain `<a href={url}>` for filter and pagination links. This triggers a server round-trip (like the original Fresh site), but the **real** request URL preserves all params. The `cmsRoute.ts` `loadCmsPageInternal` prefers `getRequestUrl()` over the `loaderDeps`-built path, so the commerce loader receives the full URL via `__pageUrl`.

```tsx
// WRONG — navigate({search}) collapses duplicate keys
<Link to="." search={parsedParams}>Filter</Link>

// WRONG — TanStack Router treats `to` as a path, not a relative URL  
<Link to="?filter.category-1=telhas&q=telha">Filter</Link>

// CORRECT — plain <a href> preserves full query string
<a href="?filter.category-1=telhas&q=telha">Filter</a>
```

**Sort** (single key) can safely use `navigate({ search })` since there are no duplicate keys.

## Related Skills

- `deco-tanstack-storefront-patterns` — General runtime patterns for TanStack storefronts
- `deco-apps-vtex-porting` — Full guide for porting VTEX loaders to apps-start
- `deco-tanstack-navigation` — Navigation patterns including Link, prefetch, search params
- `deco-tanstack-hydration-fixes` — Fixing hydration and flash-of-white issues
- `deco-cms-route-config` — Deep dive into cmsRouteConfig and route helpers

## Files Reference

| File | Layer | Purpose |
|------|-------|---------|
| `src/components/search/SearchBar.tsx` | Browser | Search input, form submit, suggestion links |
| `src/routes/$.tsx` | Router | Catch-all route with `cmsRouteConfig` |
| `deco-start/src/routes/cmsRoute.ts` | Framework | `loaderDeps`, `loadCmsPage`, URL construction |
| `deco-start/src/cms/resolve.ts` | Framework | `__pageUrl`/`__pagePath` injection into loaders |
| `apps-start/vtex/inline-loaders/productListingPage.ts` | Commerce | VTEX IS API call, URL param reading |
| `.deco/blocks/pages-search-*.json` | CMS | Page definition for `/s` route |
| `src/server/cms/blocks.gen.ts` | Build | Compiled CMS blocks (must include search page) |
