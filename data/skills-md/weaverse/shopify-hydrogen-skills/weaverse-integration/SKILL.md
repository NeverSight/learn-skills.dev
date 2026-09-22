---
name: weaverse-integration
description: "Integrate Weaverse into an existing Shopify Hydrogen project — analyze codebase, convert existing components to Weaverse sections, set up SDK, configure routes, and preserve coding style. For projects not yet using Weaverse."
---

# Weaverse Integration — Existing Hydrogen Project

> **Purpose:** You are integrating Weaverse into a Hydrogen project that does NOT currently use it. This skill guides you through the full process: analysis → SDK setup → component conversion → route migration → verification.
>
> **Key principle:** Respect the existing project. Match their coding style, patterns, and conventions. Don't restructure what already works — extend it with Weaverse.

## Live Documentation

Run these from this skill's own folder. The helpers ship inside the sibling
`shopify-hydrogen` skill, so `../shopify-hydrogen/scripts/` exists whenever the
whole pack is installed.

If you installed this skill on its own, that folder is absent and the commands
below fail with `MODULE_NOT_FOUND`. Add the helpers once:

```bash
npx skills add Weaverse/shopify-hydrogen-skills --skill shopify-hydrogen
```

This skill has no `references/` directory, so the phases below are its only
offline guidance; the live-doc commands are optional enrichment.

```bash
# Always fetch latest docs before making decisions
node ../shopify-hydrogen/scripts/search_weaverse_docs.mjs "existing hydrogen integration"
node ../shopify-hydrogen/scripts/get_weaverse_page.mjs "migration-advanced/existing-hydrogen-integration"
node ../shopify-hydrogen/scripts/search_shopify_docs.mjs "createHydrogenContext"
```

---

## Phase 1: Analyze the Existing Project

Before touching any code, read and document the project's current state.

### 1.1 Detect Framework Version

```bash
# Check package.json
cat package.json | grep -E '"react-router"|"@remix-run"|"@shopify/hydrogen"|"@weaverse"'
```

| What you find | Weaverse version to install |
|---|---|
| `react-router` + `@shopify/hydrogen@2025.5.0+` | `@weaverse/hydrogen@latest` (v5, React Router v7) |
| `@remix-run/react` | `@weaverse/hydrogen@4` (v4, Remix) |

**If the project uses Remix (pre-2025.5.0):**
- Ask the user if they want to migrate to React Router v7 first, then integrate Weaverse v5
- Or integrate Weaverse v4 on their current Remix setup
- Recommend the v7 migration path — it's the future

### 1.2 Catalog the Codebase

Read these files and note their patterns:

| File | What to observe |
|---|---|
| `package.json` | Dependencies, scripts, package manager (npm/yarn/pnpm/bun) |
| `app/root.tsx` | Layout structure, providers, global styles |
| `app/entry.server.tsx` | CSP setup, rendering approach |
| `server.ts` (or `server/index.ts`) | Context creation, middleware |
| `app/routes/**` | Route structure, loader patterns, naming convention |
| `app/components/**` | Component patterns, props, styling approach |
| `app/sections/**` | If sections exist — how they're structured |
| `app/styles/**` or `tailwind.config.*` | Styling approach (Tailwind, CSS modules, styled-components, etc.) |
| `vite.config.ts` | Build plugins, aliases |
| `.env` or `.env.example` | Existing env vars (DO NOT read secrets) |
| `tsconfig.json` | Path aliases, strictness settings |

### 1.3 Document Coding Conventions

Note and **preserve** these patterns:

- **Component style:** Function declarations vs arrow functions vs `forwardRef`
- **Export style:** `export default` vs named exports vs `export let`
- **Styling:** Tailwind classes, CSS modules, styled-components, inline styles
- **State management:** Hooks, context, stores
- **Data fetching:** Loader patterns, GraphQL query structure, error handling
- **File naming:** kebab-case, PascalCase, camelCase
- **Import style:** Absolute (`~/`) vs relative, namespace imports vs default
- **TypeScript:** Strictness, interface vs type, generics usage
- **Comments:** Level of documentation, JSDoc usage

> ⚠️ **CRITICAL:** Your converted Weaverse components MUST match these conventions. If the project uses `function` declarations, don't use `const X = () =>`. If they use Tailwind, don't introduce CSS modules.

### 1.4 Identify Convertible Components

Find components that are good candidates for Weaverse sections:

**Good candidates:**
- Hero banners / sliders
- Featured collections / product grids
- Testimonials / reviews
- Newsletter signups
- Promotional banners
- Custom content sections (image + text, video, etc.)
- Footer sections (newsletter, social links)
- Navigation components with editable content

**Skip (don't convert):**
- Layout primitives (Button, Input, Modal — keep as shared components)
- Route-level wrappers
- Cart / checkout logic components
- Analytics / tracking components
- Server utilities

---

## Phase 2: Install & Configure Weaverse SDK

### 2.1 Install Package

```bash
# Use whatever package manager the project already uses
# React Router v7 (Hydrogen 2025.5.0+)
npm install @weaverse/hydrogen@latest

# Remix (legacy)
npm install @weaverse/hydrogen@4
```

### 2.2 Environment Variables

Add to `.env`:

```env
WEAVERSE_PROJECT_ID="provided-by-user"
WEAVERSE_API_KEY="provided-by-user"
```

**Also add to `.env.example`** (without real values) and update TypeScript env types:

```ts
// Add to the Env type in env.d.ts or wherever the project defines it
WEAVERSE_PROJECT_ID: string;
WEAVERSE_API_KEY: string;
WEAVERSE_HOST?: string;
```

### 2.3 Create `app/weaverse/` Directory

Create these 5 files. **Match the project's existing code style** (exports, naming, quotes, semicolons).

#### `app/weaverse/schema.server.ts` — Theme Schema

```ts
import type { HydrogenThemeSchema } from "@weaverse/hydrogen";
import pkg from "../../package.json";

export let themeSchema: HydrogenThemeSchema = {
  info: {
    version: pkg.version,
    author: "Your Store Name",
    name: "Your Theme Name",
  },
  settings: [
    // Start minimal — add more as you convert components
    {
      group: "Colors",
      inputs: [
        {
          type: "color",
          name: "colorPrimary",
          label: "Primary Color",
          defaultValue: "#000000",
        },
        {
          type: "color",
          name: "colorBackground",
          label: "Background Color",
          defaultValue: "#ffffff",
        },
        {
          type: "color",
          name: "colorText",
          label: "Text Color",
          defaultValue: "#1a1a1a",
        },
      ],
    },
    {
      group: "Typography",
      inputs: [
        {
          type: "range",
          name: "headingBaseSize",
          label: "Heading Base Size",
          configs: { min: 14, max: 32, step: 1, unit: "px" },
          defaultValue: 28,
        },
        {
          type: "range",
          name: "bodyBaseSize",
          label: "Body Base Size",
          configs: { min: 12, max: 20, step: 1, unit: "px" },
          defaultValue: 16,
        },
      ],
    },
  ],
};
```

#### `app/weaverse/style.tsx` — Global Styles

Read the project's existing global styles (CSS files, Tailwind config, root layout) and create CSS variables that integrate with their existing setup.

```tsx
import { useThemeSettings } from "@weaverse/hydrogen";

export function GlobalStyle() {
  let settings = useThemeSettings();
  if (!settings) return null;

  return (
    <style
      id="weaverse-global-style"
      key="weaverse-global-style"
      suppressHydrationWarning
      dangerouslySetInnerHTML={{
        __html: `
          :root {
            --color-primary: ${settings.colorPrimary};
            --color-bg: ${settings.colorBackground};
            --color-text: ${settings.colorText};
            --heading-base: ${settings.headingBaseSize}px;
            --body-base: ${settings.bodyBaseSize}px;
          }
        `,
      }}
    />
  );
}
```

#### `app/weaverse/components.ts` — Component Registry

```ts
import type { HydrogenComponent } from "@weaverse/hydrogen";

// Import converted sections here — start empty, add as you convert
// MUST use namespace imports: import * as X, NOT import X from
export let components: HydrogenComponent[] = [
  // Sections will be added during Phase 3
];
```

#### `app/weaverse/index.tsx` — WeaverseContent

```tsx
import { WeaverseHydrogenRoot } from "@weaverse/hydrogen";
import { components } from "./components";

export function WeaverseContent() {
  return (
    <WeaverseHydrogenRoot
      components={components}
      errorComponent={GenericError}
    />
  );
}
```

Use the project's existing error component if they have one, otherwise create a minimal `GenericError`.

#### `app/weaverse/csp.ts` — Content Security Policy

```ts
export function getWeaverseCsp(request: Request, context: any) {
  let url = new URL(request.url);
  let weaverseHost = context.env?.WEAVERSE_HOST || "https://weaverse.io";
  let isDesignMode = url.searchParams.get("weaverse_design_mode") === "true";

  let weaverseHosts = [
    new URL(weaverseHost).host,
    "weaverse.io",
    "*.weaverse.io",
    "shopify.com",
    "*.shopify.com",
    "*.myshopify.com",
  ];

  let updatedCsp: Record<string, string[] | string | boolean> = {
    frameAncestors: weaverseHosts,
    defaultSrc: ["'self'", "data:", ...weaverseHosts],
    scriptSrc: ["'self'", "'unsafe-inline'", ...weaverseHosts],
    styleSrc: ["'self'", "'unsafe-inline'", ...weaverseHosts],
    connectSrc: ["'self'", ...weaverseHosts],
  };

  if (isDesignMode) {
    updatedCsp.frameAncestors = ["*"];
  }

  return updatedCsp;
}
```

### 2.4 Update Server Context

Modify the existing context file (usually `server.ts` or `app/lib/context.ts`):

```ts
// ADD these imports
import { WeaverseClient } from "@weaverse/hydrogen";
import { themeSchema } from "~/weaverse/schema.server"; // adjust path alias
import { components } from "~/weaverse/components";

// INSIDE createAppLoadContext, after hydrogenContext is created:
return {
  ...hydrogenContext,
  weaverse: new WeaverseClient({
    ...hydrogenContext,
    request,
    cache,
    themeSchema,
    components,
  }),
};
```

**Don't restructure their context creation** — just spread the Weaverse client into their existing return object.

### 2.5 Update Root & Entry Files

#### `app/root.tsx` — Wrap with `withWeaverse`

```tsx
import { withWeaverse } from "@weaverse/hydrogen";
import { GlobalStyle } from "~/weaverse/style";

// Keep their existing Layout/App components untouched
// Only change: wrap the default export

// BEFORE:
// export default function App() { ... }

// AFTER:
function App() {
  // ... their existing App code, unchanged
}
export default withWeaverse(App);
```

Add `<GlobalStyle />` inside `<head>` in their Layout component.

#### `app/entry.server.tsx` — Add Weaverse CSP

```tsx
import { getWeaverseCsp } from "~/weaverse/csp";

// Inside handleRequest, merge Weaverse CSP with existing:
const { nonce, header, NonceProvider } = createContentSecurityPolicy({
  ...getWeaverseCsp(request, context),
  shop: {
    checkoutDomain: context.env?.PUBLIC_CHECKOUT_DOMAIN || context.env?.PUBLIC_STORE_DOMAIN,
    storeDomain: context.env?.PUBLIC_STORE_DOMAIN,
  },
});
```

Merge with their existing CSP config — don't replace it.

---

## Phase 3: Convert Existing Components to Weaverse Sections

This is the most important phase. Convert the user's existing components into Weaverse-editable sections while **preserving their exact visual output and behavior**.

### 3.1 Conversion Strategy

For each convertible component:

1. **Read the original** — understand props, state, data fetching, styling
2. **Create a Weaverse wrapper** — add schema + optional loader
3. **Keep the original rendering** — don't rewrite the JSX, just wrap it
4. **Register in components.ts** — add namespace import

### 3.2 Conversion Pattern

**Original component (before):**
```tsx
// app/components/hero-banner.tsx
interface HeroBannerProps {
  heading: string;
  subtitle: string;
  backgroundImage: string;
  alignment: "left" | "center";
}

function HeroBanner({ heading, subtitle, backgroundImage, alignment }: HeroBannerProps) {
  return (
    <section className="relative bg-cover bg-center" style={{ backgroundImage: `url(${backgroundImage})` }}>
      <div className={`flex flex-col ${alignment === 'center' ? 'items-center text-center' : 'items-start'}`}>
        <h1 className="text-4xl font-bold">{heading}</h1>
        <p className="text-xl mt-4">{subtitle}</p>
      </div>
    </section>
  );
}
export default HeroBanner;
```

**Converted component (after):**
```tsx
// app/sections/hero-banner.tsx (or keep original path, just add schema)
import type { HydrogenComponentProps } from "@weaverse/hydrogen";
import { createSchema } from "@weaverse/hydrogen";

interface HeroBannerProps extends HydrogenComponentProps {
  heading: string;
  subtitle: string;
  backgroundImage: string;
  alignment: "left" | "center";
}

function HeroBanner({ heading, subtitle, backgroundImage, alignment, children, ...rest }: HeroBannerProps) {
  return (
    <section {...rest} className="relative bg-cover bg-center" style={{ backgroundImage: `url(${backgroundImage})` }}>
      <div className={`flex flex-col ${alignment === 'center' ? 'items-center text-center' : 'items-start'}`}>
        <h1 className="text-4xl font-bold">{heading}</h1>
        <p className="text-xl mt-4">{subtitle}</p>
      </div>
      {children}
    </section>
  );
}
export default HeroBanner;

export let schema = createSchema({
  type: "hero-banner",
  title: "Hero Banner",
  settings: [
    {
      group: "Content",
      inputs: [
        { type: "text", name: "heading", label: "Heading", defaultValue: "Welcome" },
        { type: "textarea", name: "subtitle", label: "Subtitle" },
        { type: "image", name: "backgroundImage", label: "Background Image" },
        {
          type: "toggle-group",
          name: "alignment",
          label: "Alignment",
          configs: {
            options: [
              { value: "left", label: "Left" },
              { value: "center", label: "Center" },
            ],
          },
          defaultValue: "center",
        },
      ],
    },
  ],
  presets: {
    heading: "Welcome",
    alignment: "center",
  },
});
```

**Key changes:**
- Extend `HydrogenComponentProps` (adds `children`, `loaderData`, and Weaverse internals)
- Spread `{...rest}` on root element (required for Studio interaction)
- Render `{children}` if the component can accept nested sections
- Add `schema` export with `createSchema()`
- Keep the exact same JSX structure and styling

### 3.3 Schema Design Rules

When creating schemas for converted components:

| Original prop type | Schema input type |
|---|---|
| `string` (short text) | `text` |
| `string` (long text) | `textarea` or `richtext` |
| `string` (URL) | `url` |
| `string` (image path) | `image` |
| `string` (hex color) | `color` |
| `number` | `range` (with appropriate min/max/step) |
| `boolean` | `switch` |
| `string` (enum) | `select` or `toggle-group` |
| Object with Shopify data | `product`, `collection`, `blog`, etc. |

**Group settings logically** — match what makes sense for the component, typically:
- "Content" group — text, images, links
- "Design" group — colors, spacing, layout options
- "Advanced" group — visibility, custom CSS class

### 3.4 Converting Data-Fetching Components

If the original component fetches data (e.g., a featured collection), convert the data fetching to a Weaverse loader:

```tsx
import type { ComponentLoaderArgs } from "@weaverse/hydrogen";

type SectionData = {
  collectionHandle: string;
  count: number;
};

export let loader = async ({ weaverse, data }: ComponentLoaderArgs<SectionData>) => {
  if (!data?.collectionHandle) return null;
  return weaverse.storefront.query(COLLECTION_QUERY, {
    variables: { handle: data.collectionHandle, first: data.count ?? 8 },
  });
};
```

Use the project's existing GraphQL queries and fragments — don't rewrite them. If they have a `graphql/` directory with shared queries, import from there.

### 3.5 Register Converted Components

Update `app/weaverse/components.ts`:

```ts
import * as HeroBanner from "~/sections/hero-banner";
import * as FeaturedCollection from "~/sections/featured-collection";
// ... other converted components

export let components: HydrogenComponent[] = [
  HeroBanner,
  FeaturedCollection,
  // ...
];
```

**MUST use `import * as X`** — not `import X from`. This is the most common mistake.

---

## Phase 4: Update Routes

For each route that should be Weaverse-editable:

### 4.1 Route Conversion Pattern

```tsx
// BEFORE — original route
import { useLoaderData } from "react-router"; // or "@remix-run/react"
import HeroBanner from "~/components/hero-banner";
import ProductGrid from "~/components/product-grid";

export async function loader({ context, params }: LoaderFunctionArgs) {
  const productData = await context.storefront.query(PRODUCT_QUERY, { ... });
  return { product: productData.product };
}

export default function Homepage() {
  const { product } = useLoaderData<typeof loader>();
  return (
    <div>
      <HeroBanner heading="Sale" subtitle="Big deals" />
      <ProductGrid products={product} />
    </div>
  );
}
```

```tsx
// AFTER — Weaverse-enabled route
import { WeaverseContent } from "~/weaverse";

export async function loader({ context, params }: LoaderFunctionArgs) {
  // Keep existing data loading
  const productData = await context.storefront.query(PRODUCT_QUERY, { ... });

  // ADD Weaverse page loading
  const weaverseData = await context.weaverse.loadPage({ type: "INDEX" });

  return {
    product: productData.product,
    weaverseData,
  };
}

export default function Homepage() {
  // Render Weaverse content — it will use the registered components
  return <WeaverseContent />;
}
```

### 4.2 Page Types

| Route | `type` value |
|---|---|
| Homepage (`_index`) | `"INDEX"` |
| Product page | `"PRODUCT"` (with `handle: params.productHandle`) |
| Collection page | `"COLLECTION"` (with `handle: params.collectionHandle`) |
| Collections list | `"ALL_PRODUCTS"` |
| Blog | `"BLOG"` |
| Article | `"ARTICLE"` (with `handle: params.articleHandle`) |
| Custom page | `"PAGE"` (with `handle: params.pageHandle`) |
| Custom template | `"CUSTOM"` |

### 4.3 Gradual Migration (Recommended)

You don't have to convert all routes at once. Start with:

1. **Homepage** — highest impact, usually simplest
2. **Product page** — merchant value is high
3. **Collection page** — enables visual merchandising
4. **Other pages** — as needed

For routes not yet converted, keep them as-is. Weaverse doesn't interfere with non-Weaverse routes.

---

## Phase 5: Handle Edge Cases

### 5.1 Existing Layout Components

If the project has shared layout components (header, footer, nav):

- **Header/Footer** — keep them outside Weaverse for now, rendered in `root.tsx` Layout
- OR convert them to Weaverse components if the user wants them editable
- Ask the user which approach they prefer

### 5.2 Shared Components (Buttons, Inputs, etc.)

Don't convert primitive/shared components. They stay in `app/components/` and are used inside Weaverse sections.

### 5.3 Third-Party Integrations

If the project uses:
- **Analytics** (GA4, Segment, etc.) — keep in route loaders or root layout
- **A/B testing** — keep outside Weaverse page rendering
- **Custom middleware** — ensure Weaverse CSP doesn't block third-party scripts
- **CMS data** (Contentful, Sanity, etc.) — can coexist; Weaverse handles visual layout, external CMS handles structured content

### 5.4 TypeScript Types

Add to the project's type definitions:

```ts
// Wherever the project defines AppLoadContext
interface AppLoadContext {
  // ... existing properties
  weaverse: import("@weaverse/hydrogen").WeaverseClient;
}
```

---

## Phase 6: Verification Checklist

After integration, verify:

- [ ] `npm run dev` starts without errors
- [ ] Existing routes still render correctly (visual regression check)
- [ ] Weaverse Studio preview loads at the local dev URL
- [ ] Converted components appear in Weaverse Studio component picker
- [ ] Theme settings show in Studio > Theme > Customize
- [ ] Converted components render identically to their originals
- [ ] Component schemas expose the right editable settings
- [ ] Data-fetching sections load data correctly
- [ ] `npm run build` completes without errors
- [ ] TypeScript compiles without new errors
- [ ] Cart, checkout, and customer account flows still work
- [ ] No console errors related to CSP

---

## Common Mistakes to Avoid

| Mistake | Fix |
|---|---|
| `import X from` instead of `import * as X` | Always namespace import for component registration |
| Forgetting `{...rest}` on root element | Required for Weaverse Studio drag/drop interaction |
| Not rendering `{children}` in container components | Required for nested sections |
| Overriding existing CSP instead of merging | Spread Weaverse CSP into existing config |
| Rewriting component JSX "to make it better" | Preserve the exact original rendering |
| Converting ALL components at once | Convert sections first, keep primitives as shared components |
| Using `inspector` in schema | Use `settings` — `inspector` is deprecated |
| Creating `app/weaverse/` outside `app/` | Must be inside the app directory |
| Forgetting env vars in type definitions | Add WEAVERSE_* to the Env type |

---

## Quick Reference — File Changes Summary

| File | Action |
|---|---|
| `package.json` | Add `@weaverse/hydrogen` dependency |
| `.env` | Add `WEAVERSE_PROJECT_ID`, `WEAVERSE_API_KEY` |
| `app/weaverse/schema.server.ts` | **CREATE** — theme schema |
| `app/weaverse/style.tsx` | **CREATE** — global styles component |
| `app/weaverse/components.ts` | **CREATE** — component registry |
| `app/weaverse/index.tsx` | **CREATE** — WeaverseContent wrapper |
| `app/weaverse/csp.ts` | **CREATE** — CSP configuration |
| `server.ts` (or context file) | **MODIFY** — add WeaverseClient to context |
| `app/root.tsx` | **MODIFY** — wrap with `withWeaverse`, add `<GlobalStyle />` |
| `app/entry.server.tsx` | **MODIFY** — merge Weaverse CSP |
| `app/sections/*.tsx` | **CREATE/MODIFY** — converted components |
| Route files | **MODIFY** — add `weaverse.loadPage()`, render `<WeaverseContent />` |
| Type definitions | **MODIFY** — add WEAVERSE_* env vars, weaverse context |
| `.gitignore` | **VERIFY** — `.react-router/` is ignored (RRv7 projects) |
