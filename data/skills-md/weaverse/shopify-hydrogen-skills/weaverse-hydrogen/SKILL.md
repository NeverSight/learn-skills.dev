---
name: weaverse-hydrogen
description: "Build Shopify Hydrogen storefronts with Weaverse — components, schemas, loaders, theming, data fetching, React Router v7, deployment, and advanced features."
---

# Weaverse Hydrogen — Agent Skill

> Build Shopify Hydrogen storefronts with Weaverse visual page builder.
> Docs: https://docs.weaverse.io | GitHub: https://github.com/Weaverse

## Live Documentation

Run these from this skill's own folder. The helpers ship inside the sibling
`shopify-hydrogen` skill, so `../shopify-hydrogen/scripts/` exists whenever the
whole pack is installed.

If you installed this skill on its own, that folder is absent and the commands
below fail with `MODULE_NOT_FOUND`. Add the helpers once:

```bash
npx skills add Weaverse/shopify-hydrogen-skills --skill shopify-hydrogen
```

The `references/` files in this skill remain a usable offline fallback if you
would rather not install it.

For the most up-to-date Weaverse documentation, use these scripts:

- `node ../shopify-hydrogen/scripts/search_weaverse_docs.mjs "<query>"` — search Weaverse docs
- `node ../shopify-hydrogen/scripts/get_weaverse_page.mjs "<page-path>"` — fetch a specific page (use paths from search results)
- Weaverse docs: https://docs.weaverse.io

**Examples:**
```bash
node ../shopify-hydrogen/scripts/search_weaverse_docs.mjs "component schema"
node ../shopify-hydrogen/scripts/search_weaverse_docs.mjs "data fetching"
node ../shopify-hydrogen/scripts/get_weaverse_page.mjs "development-guide/component-schema"
node ../shopify-hydrogen/scripts/get_weaverse_page.mjs "api-reference/weaverse-client"
```

The reference files below provide offline context but may not reflect the latest changes.

---

## What is Weaverse?

Weaverse is a visual page builder for Shopify Hydrogen. It lets merchants customize storefronts via a drag-and-drop Studio while developers build type-safe React components with schemas that define the editor UI.

**Stack:** React 19 · React Router v7 · Shopify Hydrogen · TypeScript · Tailwind CSS · Vite

---

## 1. Project Structure

```
app/
├── components/        # Reusable UI components
├── graphql/           # GraphQL queries & fragments
├── hooks/             # Custom React hooks
├── routes/            # React Router v7 route files
├── sections/          # Weaverse section components ← YOUR WORK GOES HERE
├── styles/            # Global styles + Tailwind
├── weaverse/
│   ├── components.ts  # Component registry
│   ├── schema.server.ts  # Theme schema (global settings)
│   └── csp.ts         # Content Security Policy for Weaverse
├── entry.client.tsx
├── entry.server.tsx
└── root.tsx           # Wrapped with withWeaverse(App)
server.ts              # WeaverseClient initialization
vite.config.ts
react-router.config.ts
tailwind.config.js
.env
```

---

## 2. Component Anatomy

Every Weaverse component has up to 3 exports from a single file (or directory):

```tsx
// app/sections/my-section/index.tsx

// 1. Default export — React component
function MySection(props: MySectionProps) { ... }
export default MySection;

// 2. Schema export — editor configuration
export let schema = createSchema({ ... });

// 3. Loader export (optional) — server-side data fetching
export let loader = async (args: ComponentLoaderArgs<DataType>) => { ... };
```

### Minimal Example

```tsx
import { createSchema } from '@weaverse/hydrogen';
import type { HydrogenComponentProps } from '@weaverse/hydrogen';

interface BannerProps extends HydrogenComponentProps {
  heading: string;
  description: string;
}

function Banner({ heading, description, children, ...rest }: BannerProps) {
  return (
    <section {...rest} className="py-16 px-4 text-center">
      <h2 className="text-3xl font-bold">{heading}</h2>
      <p className="mt-4 text-lg text-gray-600">{description}</p>
      {children}
    </section>
  );
}

export default Banner;

export let schema = createSchema({
  type: 'banner',
  title: 'Banner',
  settings: [
    {
      group: 'Content',
      inputs: [
        { type: 'text', name: 'heading', label: 'Heading', defaultValue: 'Hello World' },
        { type: 'textarea', name: 'description', label: 'Description', defaultValue: 'Welcome to our store.' },
      ],
    },
  ],
  presets: {
    heading: 'Hello World',
    description: 'Welcome to our store.',
  },
});
```

### Key Rules

- **Spread `{...rest}`** on the root element — required for Weaverse Studio interaction.
- **Render `{children}`** if the component accepts child components (`childTypes`).
- **`forwardRef` is optional** in React 19. If using React 18, wrap with `forwardRef` and attach `ref` to root element.
- **`type` must be unique** across all components, use kebab-case (e.g., `hero-banner`).

---

## 3. Component Registration

Components must be registered in `app/weaverse/components.ts`:

```tsx
import type { HydrogenComponent } from '@weaverse/hydrogen';

// MUST use namespace imports (import * as X), NOT default imports
import * as HeroBanner from '~/sections/hero-banner';
import * as FeaturedCollection from '~/sections/featured-collection';
import * as ProductCard from '~/sections/product-card';

export let components: HydrogenComponent[] = [
  HeroBanner,
  FeaturedCollection,
  ProductCard,
];
```

**Common mistake:** Using `import HeroBanner from ...` — this won't work. Always `import * as HeroBanner from ...`.

---

## 4. Schema with `createSchema()`

```tsx
import { createSchema } from '@weaverse/hydrogen';

export let schema = createSchema({
  type: 'my-component',          // Unique kebab-case identifier
  title: 'My Component',         // Display name in Studio
  limit: 1,                      // Max instances per page (optional)
  enabled: ({ page, group }) =>  // Dynamic insertion availability (optional)
    ['PRODUCT', 'COLLECTION'].includes(page.type) && group === 'body',
  settings: [                    // Editor UI groups
    {
      group: 'Content',
      inputs: [
        { type: 'text', name: 'heading', label: 'Heading', defaultValue: 'Title' },
        { type: 'richtext', name: 'body', label: 'Body' },
        { type: 'image', name: 'image', label: 'Image' },
        {
          type: 'select', name: 'layout', label: 'Layout',
          configs: {
            options: [
              { value: 'grid', label: 'Grid' },
              { value: 'list', label: 'List' },
            ],
          },
          defaultValue: 'grid',
        },
      ],
    },
  ],
  childTypes: ['product-card', 'button'],  // Allowed child component types
  presets: {                     // Defaults when component is added to page
    heading: 'Title',
    layout: 'grid',
    children: [
      { type: 'product-card' },
      { type: 'product-card' },
    ],
  },
});
```

**`inspector` is deprecated** — always use `settings`.

**`enabledOn` is deprecated** — move page/group checks into `enabled`. The callback is synchronous, runs in the storefront preview, and receives `{ page: { id, type, handle, locale }, group }`. Errors, Promises, and non-boolean results hide the component from new insertion without affecting existing instances. Studio currently evaluates the `body` group.

**Page types for `enabled`:** `INDEX`, `PRODUCT`, `ALL_PRODUCTS`, `COLLECTION`, `COLLECTION_LIST`, `PAGE`, `BLOG`, `ARTICLE`, `CUSTOM`

---

## 5. Input Types (Quick Reference)

| Type | Returns | Use For |
|------|---------|---------|
| `text` | `string` | Single-line text |
| `textarea` | `string` | Multi-line text |
| `richtext` | `string` (HTML) | Rich text with formatting |
| `url` | `string` | URLs/links |
| `image` | `WeaverseImage` object | Image picker from Shopify Files |
| `video` | `WeaverseVideo` object | Video picker from Shopify Files |
| `color` | `string` (#hex) | Color picker |
| `range` | `number` | Slider (requires `configs: { min, max, step }`) |
| `switch` | `boolean` | Toggle on/off |
| `select` | `string` | Dropdown (requires `configs: { options }`) |
| `toggle-group` | `string` | Button group (requires `configs: { options }`) |
| `heading` | — | Section header in settings panel (no data) |
| `datepicker` | `number` (timestamp) | Date/time picker |
| `product` | Shopify product | Product picker |
| `collection` | Shopify collection | Collection picker |
| `blog` | Shopify blog | Blog picker |
| `article` | Shopify article | Article picker |
| `metaobject` | Shopify metaobject | Metaobject picker |
| `product-list` | Shopify products[] | Multi-product picker |
| `collection-list` | Shopify collections[] | Multi-collection picker |

→ Full details: [references/04-input-settings.md](references/04-input-settings.md)

---

## 6. Data Fetching

```tsx
import type { ComponentLoaderArgs, HydrogenComponentProps } from '@weaverse/hydrogen';

type MyData = { collectionHandle: string };

export let loader = async ({ weaverse, data }: ComponentLoaderArgs<MyData>) => {
  let { storefront } = weaverse;
  return await storefront.query(COLLECTION_QUERY, {
    variables: { handle: data.collectionHandle },
  });
};

// Derive props type from loader return
type Props = HydrogenComponentProps<Awaited<ReturnType<typeof loader>>> & MyData;

function MyComponent({ loaderData, ...rest }: Props) {
  let collection = loaderData?.collection;
  return <section {...rest}>{collection?.title}</section>;
}
export default MyComponent;
```

**Key patterns:**
- `weaverse.storefront.query()` — Shopify Storefront API
- `weaverse.fetchWithCache(url, options)` — External APIs with caching
- `Promise.all([...])` — Parallel fetching
- `shouldRevalidate: true` on schema inputs that affect the loader

→ Full details: [references/05-data-fetching.md](references/05-data-fetching.md)

---

## 7. Styling & Theming

**Tailwind CSS** is the primary styling approach.

**Global theme settings** are defined in `app/weaverse/schema.server.ts` and applied via CSS variables:

```tsx
// app/components/GlobalStyle.tsx
import { useThemeSettings } from '@weaverse/hydrogen';

export function GlobalStyle() {
  let settings = useThemeSettings();
  if (!settings) return null;
  return (
    <style dangerouslySetInnerHTML={{ __html: `
      :root {
        --color-primary: ${settings.colorPrimary};
        --body-base-size: ${settings.bodyBaseSize}px;
        --heading-base-size: ${settings.headingBaseSize}px;
      }
    `}} />
  );
}
```

**CVA (Class Variance Authority)** for component variants:

```tsx
import { cva } from 'class-variance-authority';
let buttonVariants = cva('inline-flex items-center rounded font-medium', {
  variants: {
    variant: { primary: 'bg-blue-600 text-white', secondary: 'bg-gray-200' },
    size: { sm: 'h-8 px-3 text-sm', md: 'h-10 px-4', lg: 'h-12 px-6' },
  },
  defaultVariants: { variant: 'primary', size: 'md' },
});
```

→ Full details: [references/06-styling-theming.md](references/06-styling-theming.md)

---

## 8. Weaverse API (Key Hooks & Utilities)

| API | Purpose |
|-----|---------|
| `createSchema()` | Define component schema with Zod validation |
| `WeaverseClient` | Server-side client (initialized in `server.ts`) |
| `weaverse.loadPage({ type, handle })` | Load page data in route loaders |
| `weaverse.loadThemeSettings()` | Load global theme settings |
| `weaverse.fetchWithCache(url)` | Cached external API fetching |
| `withWeaverse(App)` | HOC wrapping root `App` in `root.tsx` |
| `useWeaverse()` | Access global Weaverse instance |
| `useThemeSettings()` | Access global theme settings |
| `useItemInstance()` | Access a specific component instance |
| `useParentInstance()` | Access parent component instance |
| `useChildInstances()` | Access child component instances |

→ Full details: [references/10-weaverse-api.md](references/10-weaverse-api.md)

---

## 9. Server Setup (server.ts)

```tsx
import { WeaverseClient } from '@weaverse/hydrogen';
import { components } from '~/weaverse/components';
import { themeSchema } from '~/weaverse/schema.server';

export async function createAppLoadContext(request, env, executionContext) {
  let hydrogenContext = createHydrogenContext({ env, request, cache, waitUntil, session, /* ... */ });
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
}
```

---

## 10. Route Integration

```tsx
// app/routes/($locale)._index.tsx
import { WeaverseHydrogenRoot } from '@weaverse/hydrogen';

export async function loader({ context }: LoaderFunctionArgs) {
  let weaverseData = await context.weaverse.loadPage({ type: 'INDEX' });
  return { weaverseData };
}

export default function Homepage() {
  return <WeaverseHydrogenRoot />;
}
```

For product pages:

```tsx
export async function loader({ context, params }: LoaderFunctionArgs) {
  let weaverseData = await context.weaverse.loadPage({
    type: 'PRODUCT',
    handle: params.productHandle,
  });
  return { weaverseData, /* other data */ };
}
```

---

## Reference Index

For detailed information on specific topics, read these reference files:

| # | File | Topic |
|---|------|-------|
| 01 | [references/01-project-structure.md](references/01-project-structure.md) | Project structure & file anatomy |
| 02 | [references/02-creating-components.md](references/02-creating-components.md) | Component creation & registration |
| 03 | [references/03-component-schema.md](references/03-component-schema.md) | createSchema(), settings, childTypes, presets, enabled |
| 04 | [references/04-input-settings.md](references/04-input-settings.md) | All input types & configurations |
| 05 | [references/05-data-fetching.md](references/05-data-fetching.md) | Loaders, Storefront API, caching |
| 06 | [references/06-styling-theming.md](references/06-styling-theming.md) | Tailwind, theme settings, CVA, CSS variables |
| 07 | [references/07-react-router-7.md](references/07-react-router-7.md) | React Router v7 conventions |
| 08 | [references/08-hydrogen-fundamentals.md](references/08-hydrogen-fundamentals.md) | Hydrogen framework essentials |
| 09 | [references/09-deployment.md](references/09-deployment.md) | Oxygen, Docker, env vars |
| 10 | [references/10-weaverse-api.md](references/10-weaverse-api.md) | All hooks & WeaverseClient API |
| 11 | [references/11-advanced-features.md](references/11-advanced-features.md) | Localization, data connectors, CSP |
| 12 | [references/12-pilot-theme.md](references/12-pilot-theme.md) | Pilot theme patterns & conventions |
| 13 | [references/13-migration-v5.md](references/13-migration-v5.md) | Remix → React Router v7 migration |
| 14 | [references/14-sdk-caching-and-diagnostics.md](references/14-sdk-caching-and-diagnostics.md) | SDK 5.15.x caching, Builder diagnostics headers, nested multi-instance pages, client upgrades |

## Examples

| File | Shows |
|------|-------|
| [examples/hero-banner.tsx](examples/hero-banner.tsx) | Complete section with schema, settings groups, childTypes, presets |
| [examples/featured-collection.tsx](examples/featured-collection.tsx) | Section with loader, Storefront API query |
| [examples/product-card.tsx](examples/product-card.tsx) | Child component example |
| [examples/components-registry.ts](examples/components-registry.ts) | Registration pattern |
