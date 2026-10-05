---
name: enable-i18n
description: >
  Enable next-intl-based i18n in the shop template — locale-prefixed URLs,
  per-locale message catalogs, and a locale switcher. Use when the user wants
  "locale URLs", "multi-language", or "i18n" without Shopify Markets
  integration. For full Shopify Markets multi-region commerce (region-aware
  pricing, inventory, payments), use `enable-shopify-markets` instead — this
  skill is the routing/i18n layer only.
---

# Enable i18n (next-intl, no Markets)

Add next-intl so the storefront serves locale-prefixed URLs (`/en-US/products/foo`), loads per-locale message catalogs, and exposes a copy-language switcher. The default is one deployment with clean URLs, inline component copy with reusable functions in `lib/content/index.ts`, and `shopConfig.localization = { country: "US", language: "EN", locale: "en-US" }`. There is no next-intl dependency, message catalog, `lib/i18n/` directory, or `lib/params/server.ts` locale resolver to reuse in a fresh template.

> **Use `enable-shopify-markets` instead** for regional commerce. This skill translates storefront copy and adds routing; it must not infer a commerce country from a copy locale or mutate cart buyer country when language changes. Keep Shopify country/language configuration explicit, preserve intentional operation locale/cache inputs, and always display currency from Shopify responses.

## Inspect and preserve the installation

Read scoped `AGENTS.md`, `package.json`, `next.config.ts`, `lib/config/index.ts`, `lib/content/index.ts`, routes, components, layout, proxy, and any existing localization files. Trace copy consumers, formatting, SEO, markdown, cart, auth, and chat boundaries before editing.

Choose the migration path from evidence:

- **Fresh simplified template:** introduce next-intl, catalogs, request config, routing, and the locale resolver using the steps below.
- **Already localized or customized:** preserve its next-intl version/configuration, catalogs, translations, rich text, providers, supported locales, domains, prefixes, locale cookies, redirects, and commerce behavior. Fill only missing pieces. Do not replace existing catalogs with template English, move routes twice, or reset the locale list to these examples. If the requested routing conflicts with existing public URLs, obtain a migration decision before changing them.
- **Mixed migration:** inventory inline copy, content functions, and catalogs. Convert only unmigrated consumers and retain modules still in use. Do not delete working translations or collapse locale-sensitive commerce/cache arguments.

Confirm the default copy locale and supported copy locales with the user. In a noninteractive run, report any unresolved choice and stop rather than choosing a routing or translation policy.

## Introduce next-intl and migrate copy

1. On a fresh installation, run `pnpm add next-intl` from the storefront root. Read the installed next-intl plugin/request/routing APIs and local Next.js guides before wiring them. If next-intl already exists, preserve its compatible version rather than reinstalling blindly.
2. Create `lib/i18n/request/server.ts` as described below, then create the plugin with `createNextIntlPlugin` from `next-intl/plugin` and the explicit request-config path. In the current template, add that plugin to the list passed to `withShopConfig(nextConfig, plugins)`; preserve the conditional `withBotId` and `withEve` entries and their existing order. Do not pass the exported async config factory to a plugin that expects a config object. Preserve customized wrapper composition, rewrites, redirects, and Cache Components settings, and do not enable optional features as part of localization.
3. Inventory inline JSX text, labels in component configuration, template literals, and reusable functions in `lib/content/index.ts`. Create the default catalog from the storefront's actual customized copy, not a template snapshot. Convert functions to equivalent ICU messages with the same parameter names, zero/one/many behavior, number formatting, rich text, and accessibility labels. Do not serialize functions into JSON or build a custom `t()` parser.
4. Create catalogs and explicit loaders for each approved locale. Keep keys and interpolation arguments aligned. Do not present an English fallback as a completed translation; agree on any temporary fallback before enabling that locale publicly.
5. Replace inline server copy and content function calls with `getTranslations()` from `next-intl/server`. Pass translated primitive labels to client leaves when possible. For interactive plurals/interpolation, wrap only the relevant leaf in a Server Component's `NextIntlClientProvider` with the namespaces it uses, then use `useTranslations()` there. Never pass the full catalog from the root layout, and never pass ordinary copy functions across the server/client boundary. Keep `components/ui/` copy-agnostic.
6. Cover error boundaries, not-found screens, metadata, email/contact text, and dynamic announcements as well as visible page headings. Components outside a provider need resolved labels or an explicitly scoped provider. Keep a minimal fallback for global errors that cannot access locale context.
7. Set `<html lang>` and UI number/date formatting from the validated copy locale. Leave `shopConfig.localization.country` and `.language` as deployment commerce settings unless Shopify content translation is explicitly requested and validated. A copy locale such as `fr-FR` does not by itself mean shipping/pricing country `FR`.
8. After all consumers are migrated and checked, remove only unused content functions. Preserve custom copy and existing catalogs. Update the installation's `AGENTS.md` to require aligned locale catalogs and scoped providers now that it is localized.

## Create the locale source of truth

On a fresh installation, create `lib/i18n/index.ts` with the user's approved locales. On an existing installation, extend its current source of truth instead. Routing, sitemap, alternates, and the switcher must read the same list. This list describes copy/routing locales, not a locale-to-currency or commerce-country map.

Example only; replace with the approved list and seed the default from the deployment's formatting locale when appropriate:

```ts
import type { Locale } from "./types";

export const locales = ["en-US", "fr-FR"] as const;
export const defaultLocale: Locale = "en-US";
export const enabledLocales: readonly Locale[] = locales;

export function isEnabledLocale(value: string): value is Locale {
  return enabledLocales.some((locale) => locale === value);
}
```

Define the shared `Locale` contract in `lib/i18n/types.ts`; import it directly wherever it is needed:

```ts
import type { locales } from "./index";

export type Locale = (typeof locales)[number];
```

Use domain/context files for new modules: universal routing configuration in `lib/i18n/routing/index.ts`, client navigation in `lib/i18n/navigation/client.ts`, server request configuration in `lib/i18n/request/server.ts`, and the root-param resolver in `lib/params/server.ts`. Do not add barrels or forwarding exports. Preserve working paths in an existing customized installation rather than renaming them solely to match these examples.

Validate route params, action inputs, and request payloads against this list. Retain any existing resolver and fallback policy rather than resetting it.

## What this skill turns on

1. `lib/i18n/routing/index.ts` and `lib/i18n/navigation/client.ts` (next-intl)
2. Route segment `app/[locale]/` containing every page
3. `proxy.ts` middleware running `next-intl/middleware`
4. `lib/params/server.ts` `getLocale()` reading from `next/root-params`
5. A new next-intl plugin wrapper, catalogs, and `lib/i18n/request/server.ts` loading messages by resolved locale
6. Locale-prefixed canonicals + hreflang alternates in `lib/seo/index.ts`
7. Sitemap entries per locale
8. `next.config.ts` rewrites/redirects on `/:locale/*` sources
9. `app/(unlocalized)/page.tsx` fallback redirect to default locale
10. `generateStaticParams` on the root layout
11. Add or adapt a copy-language selector without introducing a currency selector

## Cache Components compatibility — read this first

The template runs with `cacheComponents: true` (Next.js 16). That changes a few things this skill needs to handle correctly. Skipping any of these will produce build errors that look unrelated:

### A. There must be no `app/layout.tsx` above `app/[locale]/`

For `[locale]` to be recognized as a root param, the dynamic segment must be the root layout. After Step 2, the file at `app/layout.tsx` should be gone (moved into `app/[locale]/layout.tsx`). If both exist, `rootParams.locale()` returns `undefined`.

### B. `setRequestLocale` is not used

next-intl docs sometimes show `setRequestLocale(locale)` calls in layouts/pages. **Don't add them under cacheComponents.** That helper writes to a request-scoped store and forces dynamic rendering — it defeats the cache. The rootParams + request-config pattern below makes it unnecessary because the resolved locale is already a cache key.

### C. Don't swap `next/link` to next-intl's `<Link>`

The straightforward instinct is to replace every `import Link from "next/link"` with `import { Link } from "@/lib/i18n/navigation/client"`. **Don't.** next-intl's Link reads request context (locale) on render; in a server-component tree under cacheComponents, that triggers:

```
Error: Route "/[locale]/..." accessed [...] which is not defined in the `unstable_samples` of `instant`.
```

or a generic "blocking route" prerender failure.

**Do this instead:** keep `next/link` and pass explicitly locale-prefixed hrefs from a Server Component using its validated locale. Middleware can redirect legacy unprefixed paths, but those redirects may negotiate a different locale and must not be the only mechanism keeping navigation in the selected language.

For Server Component redirects, use `next/navigation` and an explicitly prefixed path: `` `/${await getLocale()}/account/login` ``. `next/root-params` is not available in Server Actions or Route Handlers: receive and validate locale at those boundaries instead. Do not rely on middleware language detection to preserve the current URL locale; prefer explicit prefixed hrefs passed from the server for ordinary links.

### D. `instant` samples need `locale` in `params`

Any route that exports `instant` (currently: products `[handle]`, collections `[handle]`, search) needs `locale` added to every sample, or the build fails:

```
Error: Route "/[locale]/products/[handle]" accessed root param "locale"
       which is not defined in the `unstable_samples` of `instant`.
```

Fix:

```ts
export const instant = {
  unstable_samples: [
    {
      params: { locale: "en-US", handle: "__placeholder__" }, // ← add locale
      searchParams: { variant: "1" },
      cookies: [{ name: "shopify_cartId", value: null }],
    },
  ],
};
```

### E. `instant` samples need `headers` declarations if any layout-level server component reads `headers()`

This is easy to forget. If you (or a downstream skill) adds a server component to the layout that calls `headers()` — e.g. a "Shipping to {postal}" bar reading `x-vercel-ip-postal-code` — every `instant` sample in the app must declare the headers it might access:

```ts
unstable_samples: [
  {
    params: { locale: "en-US", handle: "__placeholder__" },
    searchParams: { variant: "1" },
    cookies: [{ name: "shopify_cartId", value: null }],
    headers: [["x-vercel-ip-postal-code", null]], // ← add this
  },
],
```

`null` means "header may be absent." If you forget, the build error is explicit:

```
Error: Route "..." accessed header "x-vercel-ip-postal-code" which is not
       defined in the `unstable_samples` of `instant`. Add it to the
       sample's `headers` array, or `["...", null]` if it should be absent.
```

### F. Keep server redirects outside client navigation

Do not import `lib/i18n/navigation/client.ts` into a server auth gate. Use `next/navigation`'s `redirect` (which returns `never`) and prefix the locale yourself:

```ts
import { redirect } from "next/navigation";
import { getLocale } from "@/lib/params/server";

if (!session) redirect(`/${await getLocale()}/account/login`);
return session; // OK, narrowed
```

## Step-by-step

### Step 1: Routing config

Create `lib/i18n/routing/index.ts`:

```ts
import { defineRouting } from "next-intl/routing";
import { defaultLocale, enabledLocales } from "@/lib/i18n";

export const routing = defineRouting({
  locales: enabledLocales, // pulled from lib/i18n/index.ts — never hardcode
  defaultLocale,
  localePrefix: "always",
});
```

Create `lib/i18n/navigation/client.ts`:

```ts
"use client";

import { createNavigation } from "next-intl/navigation";
import { routing } from "@/lib/i18n/routing";

export const { Link, redirect, usePathname, useRouter } = createNavigation(routing);
```

> Per "Cache Components compatibility C" above, `Link` here is mostly used by the locale switcher / programmatic routing in client components — not as a wholesale replacement for `next/link`.

### Step 2: Move routes under `app/[locale]/`

Move every route file from `app/` into `app/[locale]/`:

- `app/layout.tsx` → `app/[locale]/layout.tsx` (becomes the root layout for the locale segment). **Delete the original `app/layout.tsx` after the move** — see compatibility A above; both files cannot coexist.
- `app/page.tsx`, `app/error.tsx`, `app/not-found.tsx` → `app/[locale]/...`
- `app/account/`, `app/cart/`, `app/collections/`, `app/pages/`, `app/policies/`, `app/products/`, `app/search/` → `app/[locale]/...`

**Stay at `app/`:** `api/`, `agent/`, `md/`, `sitemap.xml/`, `sitemap/`, `robots.ts`, `global-error.tsx`, `globals.css`, `favicon.ico`. Include blogs and any custom storefront pages in the localized route audit; do not limit the move to the example list.

In the moved layout, fix `import "./globals.css"` → `import "../globals.css"`.

Update every `PageProps<"/foo">` and `LayoutProps<"/foo">` generic to include the locale segment: `PageProps<"/[locale]/products/[handle]">`, `LayoutProps<"/[locale]">`, etc.

### Step 3: Create `lib/params/server.ts` for Server Component root params

This is a new module on the simplified baseline. In a customized installation, preserve unrelated helpers and extend its existing resolver. Route Handlers use their route context or validated request inputs; Server Actions receive a validated locale argument, not this getter.

```ts
import { notFound } from "next/navigation";
import { locale as rootLocale } from "next/root-params";
import { locales } from "@/lib/i18n";
import type { Locale } from "@/lib/i18n/types";

export async function getLocale(): Promise<Locale> {
  const current = await rootLocale();
  if (!current || !locales.includes(current as Locale)) notFound();
  return current as Locale;
}
```

### Step 4: `lib/i18n/request/server.ts` loads messages by resolved locale

```ts
import { hasLocale } from "next-intl";
import { getRequestConfig } from "next-intl/server";
import { getLocale } from "@/lib/params/server";
import type enMessages from "@/lib/i18n/messages/en.json";
import { routing } from "@/lib/i18n/routing";

const messageLoaders: Record<string, () => Promise<{ default: typeof enMessages }>> = {
  "en-US": () => import("@/lib/i18n/messages/en.json"),
  "fr-FR": () => import("@/lib/i18n/messages/fr.json"),
};

// We intentionally do NOT destructure `{ locale }` from the callback args.
// next-intl populates that arg from the `x-next-intl-locale` request header,
// and reading request headers from inside a cached tree forces the route
// dynamic — every `instant` sample then needs an explicit
// `headers: [["x-next-intl-locale", null]]` declaration. Going straight to
// `getLocale()` (which reads `next/root-params`) keeps the lookup cacheable.
export default getRequestConfig(async () => {
  const requested = await getLocale();
  const locale = hasLocale(routing.locales, requested) ? requested : routing.defaultLocale;
  const loader = messageLoaders[locale];
  const messages = (await loader()).default as typeof enMessages;
  return { locale, messages };
});
```

### Step 5: Extend `proxy.ts`

Compose next-intl after the existing Shopify route dispatch. `handleShopifyRoutes()` returns `null` synchronously when Hydrogen does not own the pathname, so check that result before locale routing without awaiting it:

```ts
const handleI18n = createMiddleware(routing);

// Keep the existing imports and add NextRequest as a runtime import.
export async function proxy(request: NextRequest): Promise<Response> {
  const requestContext = createCustomerRequestContext(request);
  const shopifyRoute = handleShopifyRoutes({
    // Preserve the template's handlers, session manager, and storefront client.
    request,
    requestContext,
  });
  if (shopifyRoute) return shopifyRoute;

  const i18nRequest = new NextRequest(request, {
    headers: requestContext.getForwardedRequestHeaders(),
  });
  const response = handleI18n(i18nRequest);
  requestContext.applyResponseHeaders(response.headers);
  if (!response.ok) return response;

  const rewriteHeader = response.headers.get("x-middleware-rewrite");
  if (!rewriteHeader) return response;

  const rewriteTarget = new URL(rewriteHeader, request.url);
  const [, ...segments] = rewriteTarget.pathname.split("/");
  const normalized = new URL(`/${segments.filter(Boolean).join("/")}`, request.url);
  normalized.search = rewriteTarget.search;
  return NextResponse.rewrite(normalized, { headers: response.headers });
}
```

Update the matcher. The template's single broad matcher is safe only while the proxy does nothing but Shopify dispatch; with locale negotiation, every request Hydrogen declines is localized, including app Route Handlers, webhooks, `robots.txt`, sitemaps, `llms.txt`, and static files. Replace it with Shopify's exact route families, locale-prefixed Shopify endpoints, and a catch-all that skips `/api`, Eve, Next.js and Vercel internals, and paths with a file extension:

```ts
export const config = {
  matcher: [
    "/api/cart",
    "/api/predictive-search",
    "/api/mcp",
    "/api/ucp/mcp",
    "/api/:apiVersion(unstable|2\\d{3}-\\d{2})/graphql.json",
    "/__shopify/:path*",
    "/.well-known/:path*",
    "/agent/:action(handoff|buyer-claims).:format",
    "/cart.:format(js|json)",
    "/cart/:operation(add|update|change|clear).:format(js|json)",
    "/:page(index|search).md",
    "/:resource(collections|products)/:handle.md",
    "/:locale([a-zA-Z]{2}(?:-[a-zA-Z]{2})?)/agent/:action(handoff|buyer-claims).:format",
    "/:locale([a-zA-Z]{2}(?:-[a-zA-Z]{2})?)/cart.:format(js|json)",
    "/:locale([a-zA-Z]{2}(?:-[a-zA-Z]{2})?)/cart/:operation(add|update|change|clear).:format(js|json)",
    "/((?!api|eve(?:/|$)|_eve_internal(?:/|$)|_next/static|_next/image|_next/data|_vercel|favicon.ico|.*\\..*).*)",
  ],
};
```

Downstream applications must be able to add Route Handlers such as `/api/webhooks` or `/api/custom` without sending them through Shopify dispatch or locale middleware. If a new Hydrogen feature claims another reserved route, add that exact route family.

Keep Eve's `/eve/v1/` and `/_eve_internal/` routes outside Shopify dispatch and locale negotiation. Keep `/api/agent/session` and `/agent/ucp-profile.json` unlocalized. If Shop Agent is enabled, carry and validate the copy locale explicitly for conversation context and navigation outputs without changing the deployment's Shopify country/language or allowing client context to select a cart. Keep Next.js request/cache APIs out of Eve's runtime imports.

The file is `proxy.ts` (Next.js 16 convention), not `middleware.ts`.

### Step 6: Internal hrefs — keep `next/link`

Per the cache-components note above, **leave existing `next/link` imports alone** and pass locale-prefixed hrefs from the server. Inspect product cards, menus, breadcrumbs, search, cart, and pagination so navigation retains the selected language without a negotiation redirect. Use next-intl's client navigation in the locale switcher when needed, preserving the resource and query parameters. Reuse existing localized link helpers in customized installations.

For programmatic redirects in server code, use `next/navigation`'s `redirect`:

```ts
redirect(`/${await getLocale()}/account/login`);
```

### Step 7: `lib/seo/index.ts` — locale-aware canonicals + hreflang alternates

Keep this module universal: callers resolve and validate the locale on the server, then pass it explicitly. Do not import the server root-param resolver into `index.ts`.

```ts
import { defaultLocale, enabledLocales } from "@/lib/i18n";
import type { Locale } from "@/lib/i18n/types";

function withLocalePath(locale: string, pathname: string): string {
  const normalized = normalizePath(pathname);
  return normalized === "/" ? `/${locale}` : `/${locale}${normalized}`;
}

export function buildAlternates({
  locale,
  pathname,
  searchParams,
}: {
  locale: Locale;
  pathname: string;
  searchParams?: SearchParamsInput;
}): Metadata["alternates"] {
  const canonical = buildCanonicalPath(withLocalePath(locale, pathname), searchParams);

  const languages: Record<string, string> = {};
  for (const candidate of enabledLocales) {
    languages[candidate] = buildCanonicalPath(withLocalePath(candidate, pathname), searchParams);
  }
  languages["x-default"] = buildCanonicalPath(
    withLocalePath(defaultLocale, pathname),
    searchParams,
  );

  return { canonical, languages };
}
```

Update every caller to pass its validated locale. Server Components can call `getLocale()` from `lib/params/server.ts`; Route Handlers and Server Actions must validate their own inputs.

### Step 8: Sitemap per-locale entries

Edit `app/sitemap/[shard]/route.ts`. For every resource, emit one `<url>` per enabled locale and add `<xhtml:link rel="alternate" hreflang="..." href="..." />` siblings inside each `<url>` pointing at the other locale variants. Add `xmlns:xhtml="http://www.w3.org/1999/xhtml"` to the `<urlset>` opening tag.

```ts
import { enabledLocales } from "@/lib/i18n";

function localizePath(locale: string, pathname: string): string {
  if (pathname === "/") return `/${locale}`;
  return `/${locale}${pathname.startsWith("/") ? pathname : `/${pathname}`}`;
}

// Inside renderShard(): for each item, for each locale, emit a <url> with
// a <loc> at the localized path and an <xhtml:link> per other locale.
```

`app/sitemap.xml/route.ts` (the index) doesn't need locale handling — it only lists shard URLs, which stay locale-agnostic.

### Step 9: `next.config.ts` rewrites/redirects on `/:locale/*`

Existing markdown content-negotiation rewrites must move their `source` from `/products/:handle` to `/:locale/products/:handle`, etc. Destinations stay at `/md/products/:handle`, `/md/collections/:handle`, and `/md/search`. Inspect the existing handlers before forwarding locale; introduce and validate a copy-locale input where needed rather than assuming they already read it. Keep their deployment commerce context unchanged. Adapt existing redirects to locale-prefixed sources without restoring obsolete rules from an older template.

### Step 10: `app/(unlocalized)/page.tsx` fallback

```ts
import { permanentRedirect } from "next/navigation";
import { defaultLocale } from "@/lib/i18n";

export default function UnlocalizedRoot(): never {
  permanentRedirect(`/${defaultLocale}`);
}
```

This is a defensive fallback; with `localePrefix: "always"` middleware should already redirect `/`.

### Step 11: `generateStaticParams` on the locale layout

```ts
import { locales } from "@/lib/i18n";

export const generateStaticParams = async () => {
  return locales.map((locale) => ({ locale }));
};
```

### Step 12: Patch `instant` samples

Walk every route file that exports `instant` and add `locale` to each sample's `params`:

```ts
params: { locale: "en-US", handle: "__placeholder__" }
```

If any layout-level server component (e.g. a shipping/postal banner, geo-aware nav) reads `headers()`, also add a `headers` array to every sample:

```ts
headers: [["x-vercel-ip-postal-code", null]];
```

(See "Cache Components compatibility D/E" at the top.)

### Step 13: Add or adapt the language selector

Inspect the current navigation, including any Shopify-menu customization. The simplified template does not ship a dormant `LocaleCurrencySelector` to re-enable. Add a leaf language selector, or preserve and extend an existing one. Keep the current resource and query parameters when switching. A copy-language switch must not change cart country or invent a currency choice.

## Verifying

After applying:

```bash
pnpm lint
pnpm build
pnpm dev
# In another terminal, replace locale/handle with actual supported values:
curl -I http://localhost:3000/
curl -I http://localhost:3000/products/actual-handle
curl http://localhost:3000/sitemap.xml
curl http://localhost:3000/sitemap/products-1.xml
curl http://localhost:3000/en-US
```

Smoke-test checklist:

- [ ] Lint and build pass; restart dev after route moves so route types regenerate
- [ ] Default copy matches the pre-migration storefront, including custom text
- [ ] Every enabled catalog has matching keys and arguments; zero/one/many, interpolation, errors, and accessibility labels render correctly
- [ ] Client leaves receive only needed namespaces or primitive labels; no copy functions cross the RSC boundary
- [ ] Copy-language switching preserves Shopify country, cart identity, and currency behavior
- [ ] Existing localized installations retain translations, public URLs, providers, and custom commerce behavior
- [ ] API, OAuth, markdown, cart, and chat boundaries do not call the Server Component root-param getter
- [ ] Report which fresh and existing-installation migration paths were actually exercised; lint/build alone do not prove migration parity
- [ ] Bare `/` redirects to default locale
- [ ] Each enabled locale serves 200 at its prefix
- [ ] `<html lang>` matches the URL's locale segment
- [ ] Sitemap emits one entry per locale per page
- [ ] Canonical + hreflang alternates appear in page metadata
- [ ] Internal `next/link` hrefs preserve the selected locale; legacy unprefixed public URLs still redirect correctly
