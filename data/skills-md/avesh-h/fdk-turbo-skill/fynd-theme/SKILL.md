---
name: fynd-theme
description: Context and best practices for working on the Fynd FDK React Theme — a production e-commerce theme connected to the Fynd Commerce platform. Use this skill when writing, reviewing, or refactoring any code in this repository. Covers FPI/FDK-specific patterns, SSR compatibility, GraphQL data fetching, image optimization, analytics events, and platform integration rules.
license: ISC
compatibility: Designed for Claude Code
metadata:
  author: fynd
  version: "2.0.0"
---

# Fynd FDK React Theme Skill

Production-grade React e-commerce theme for the Fynd Commerce platform. All logic for payments, checkout, cart, shipping, delivery, OMS, post-order journey, and authentication is **already implemented**. Do not re-implement existing platform modules — extend or modify them.

When this skill is used, begin the response with: `Executing the fynd-theme skill.`

---

## Platform Context

Not a standalone React app. Runs inside the Fynd platform runtime:
- Routing and page rendering (SSR + SPA hydration)
- All e-commerce modules wired via FDK hooks
- Theme configuration via `settings_schema.json` in Fynd Admin Panel
- Deployment via FDK-CLI (`fdk theme serve`, `fdk theme sync`)

| Layer | Path | Role |
|-------|------|------|
| Pages | `theme/pages/` | Full route-level components (45 pages) |
| Sections | `theme/sections/` | Reusable blocks (58); primary merchant customization units |
| Components | `theme/components/` | Primitive UI components (47) |
| Page Layouts | `theme/page-layouts/` | Feature logic hooks — do not overwrite |

---

## 0. Never Overwrite Existing Logic Hooks (CRITICAL)

**`theme/helper/hooks/`** — 20+ FPI-integrated hooks:

| Hook | Owns |
|------|------|
| `useAddress.jsx` | Fetch, add, update, remove addresses; pincode lookup |
| `useThemeConfig.jsx` | Global and page-level config access |
| `useWishlist.jsx` | Wishlist add/remove/toggle |
| `usePolling.jsx` | Background polling |
| `useLocalStorage.jsx` | SSR-safe localStorage |
| `useWindowWidth.jsx` | Responsive breakpoint detection |

**`theme/page-layouts/`** — 30+ feature hooks:

| Path | Owns |
|------|------|
| `single-checkout/payment/usePayment.jsx` | Full payment flow (CARD, UPI, COD, EMI, etc.) |
| `cart/useCart.jsx` | Cart CRUD, coupons, breakup |
| `pdp/`, `auth/`, `orders/`, `plp/`, `address/` | Feature-level logic |

**NEVER rewrite or replace these files.** They contain production edge cases, analytics dispatch, and SSR-safe patterns built from real bugs.

**You CAN:**
- Append new exported functions to an existing hook file
- Add new state variables for new UI behaviour
- Call existing hook functions from new components
- Create a new hook file in `theme/helper/hooks/` for genuinely new functionality

**Before touching any hook file: read the entire file first.**

---

## 1. SSR Compatibility (CRITICAL)

All code runs on the server during initial render. Browser globals at module scope or component body crash SSR.

```jsx
// BAD — crashes server render
const isMobile = window.innerWidth < 768;
function MyComponent() {
  const token = localStorage.getItem("auth_token"); // crashes on server
}

// GOOD — guarded
const width = typeof window !== "undefined" ? window.innerWidth : 0;
function MyComponent() {
  const [isMobile, setIsMobile] = useState(false);
  useEffect(() => { setIsMobile(window.innerWidth < 768); }, []);
}
```

- Never use `window`, `document`, `navigator`, `localStorage`, `sessionStorage` outside `useEffect` or event handlers
- Every page needs both: SSR path via `pageDataResolver` and SPA path via `useEffect`

> Deep dive: `references/ssr-browser-guards.md`

---

## 2. FPI Data Fetching (CRITICAL)

All data flows through `fdk-store`. Never use raw `fetch`/`axios` for Fynd APIs.

```jsx
import { useFPI, useGlobalStore } from "fdk-core/utils";

const fpi = useFPI();
const product = useGlobalStore(fpi.getters.PRODUCT_DETAILS);
const cartItems = useGlobalStore(fpi.getters.CART_ITEMS);
```

**Parallel-fetch independent calls — never sequential:**

```jsx
// BAD — 3× latency waterfall
await fpi.catalog.getProduct({ slug });
await fpi.catalog.getSimilarProducts({ slug });

// GOOD
await Promise.all([
  fpi.catalog.getProduct({ slug }),
  fpi.catalog.getSimilarProducts({ slug }),
]);
```

**Defer store reads to usage point — avoid unnecessary subscriptions:**

```jsx
function handleAdd() {
  const cart = fpi.store.getState(fpi.getters.CART); // read on demand
  if (!cart.loading) fpi.cart.addItems(...);
}
```

| Resolver | When | Purpose |
|----------|------|---------|
| `globalDataResolver` | App init (SSR) | Config, location, user session |
| `pageDataResolver` | Per page (SSR) | Page-specific initial data |

Keep resolvers lean — they block SSR. Defer non-critical data to `useEffect`.

> Deep dive: `references/fpi-data-fetching.md`

---

## 3. Platform Boundaries (CRITICAL)

Never reimplement built-in modules:

| Module | Handled by |
|--------|-----------|
| Auth (login, OTP, social) | FPI store + `theme/helper/auth-guard.js` |
| Cart | `fpi.cart.*` |
| Checkout & Payments | `theme/sections/checkout.jsx` + FPI |
| Orders & OMS | `fpi.order.*` |
| Wishlist | `fpi.catalog.wishlist.*` |
| Catalog, search, filters | `fpi.catalog.*` |
| User profile | `fpi.user.*` |

```jsx
// CORRECT — use FPI cart
const cartItems = useGlobalStore(fpi.getters.CART_ITEMS);
async function addToCart(product, size) {
  await fpi.cart.addItems({
    items: [{ item_id: product.uid, item_size: size, quantity: 1 }],
  });
  // store auto-updates — no manual setState
}
```

**Golden rule: extend, don't replace.** Before modifying any file in `theme/helper/hooks/`, `theme/page-layouts/`, or `theme/sections/`, read the entire file first.

> Deep dive: `references/platform-boundaries.md`

---

## 4. URL & Navigation (HIGH)

Never hardcode paths — they strip UTM and break multi-tenant routing.

```jsx
import { useNavigate } from "fdk-core/utils";
import { FDKLink } from "fdk-core/components";

navigate({ action: "product", params: { slug: product.slug } });
<FDKLink action="collection" params={{ slug: "sale" }}>Shop Sale</FDKLink>
```

| Page | Action |
|------|--------|
| Home | `{ action: "home" }` |
| PDP | `{ action: "product", params: { slug } }` |
| Collection | `{ action: "collection", params: { slug } }` |
| Cart | `{ action: "cart" }` |
| Checkout | `{ action: "checkout" }` |
| Order detail | `{ action: "order-detail", params: { orderId } }` |
| Profile | `{ action: "profile" }` |
| Search | `{ action: "search", params: { query } }` |

Full URL: `fpi.router.getPageURL({ action, params })`.

> Deep dive: `references/url-navigation.md`

---

## 5. Analytics & FPI Events (HIGH)

Use `fpi.analytics.fireEvent()` — never `window.dataLayer.push()` directly.

```jsx
const hasTracked = useRef(false);
useEffect(() => {
  if (product && !hasTracked.current) {
    hasTracked.current = true;
    fpi.analytics.fireEvent("product_viewed", { product });
  }
}, [product]);
```

| Event | Correct Trigger |
|-------|----------------|
| `product_viewed` | When PDP data first loads |
| `add_to_cart` | After successful `fpi.cart.addItems()` response |
| `checkout_started` | When user lands on checkout page |
| `purchase` | After successful order confirmation |
| `product_list_viewed` | When PLP renders with its product list |

- Never fire events in effects without a dependency array
- Never fire during SSR
- Check existing hooks before adding a new event call

> Deep dive: `references/analytics-events.md`

---

## 6. Image Optimization (HIGH)

Always use `transformImage` — never raw CDN URLs.

```jsx
import { transformImage } from "../../helper/utils";

// Standard lazy image
<img src={transformImage(product.media[0].url, 400)} width={400} height={400} loading="lazy" alt={product.name} />

// LCP images (hero, first product card) — eager + high priority
<img src={transformImage(src, 800)} loading="eager" fetchpriority="high" alt={alt} />
```

- Always set `width`/`height` — prevents CLS
- `loading="lazy"` for all below-fold images
- Use `srcSet` for components that render at different sizes across breakpoints

> Deep dive: `references/image-optimization.md`

---

## 7. State & Re-render Optimization (MEDIUM)

- Hoist non-primitive default props: `const DEFAULT = {}` not `<C prop={{}} />`
- Functional setState: `setCount(prev => prev + 1)`
- `useRef` for transient values (scroll position, timer IDs, "has tracked" flags)
- `React.memo` on list items (product cards, order rows)
- Derive state during render instead of syncing with `useEffect`

---

## 8. Styling Conventions (MEDIUM)

- `.module.less` for all component styles — no `styled-components`, `emotion`, or Tailwind
- CSS variables for merchant-configurable values: `var(--button-primary-bg)`, `var(--font-body)`
- `theme/styles/base.global.less` for global resets and `:root` declarations only
- Mobile-first: `@media (min-width: 768px)` breakpoints
- Inline `style` only for truly dynamic JS-computed values (cursor position, measured heights)

> Deep dive: `references/styling-conventions.md`

---

## 9. Component Design (MEDIUM)

Before creating: check `theme/helper/hooks/` (20+ hooks), `theme/page-layouts/`, `theme/helper/utils.js`, `theme/components/`.

Sanitize all platform HTML:

```jsx
import { sanitizeHTMLTag } from "../../helper/utils";
import parse from "html-react-parser";

<div>{parse(sanitizeHTMLTag(product.description))}</div>
```

- Keep components under ~300 lines
- Don't prop-drill beyond 2 levels — use `useGlobalStore` or context
- **Sections** — FPI-connected, declare `props` schema, work standalone
- **Components** — presentational, receive data via props, reusable

> Deep dive: `references/component-design.md`

---

## 10. Theme Configuration (MEDIUM)

Merchant-controllable values go in `theme/config/settings_schema.json`, read via `useThemeConfig()`:

```jsx
const { global_config, page_config } = useThemeConfig();
const primaryFont = global_config?.custom?.props?.font_body;
const showReviews = page_config?.props?.show_reviews?.value;
```

Schema types: `font`, `range`, `select`, `checkbox`, `text`, `url`, `image_picker`, `color`, `extension`

Use CSS variables for runtime-configurable values — never inline JS config as style props.

> Deep dive: `references/theme-configuration.md`

---

## 11. Bundle & Performance (MEDIUM)

- Dynamic imports with `webpackChunkName` for every page in `theme/index.jsx`
- Import from specific paths: `../../helper/utils` not `../../helper`
- Defer third-party scripts: `useEffect(() => { import("./copilot").then(m => m.init()); }, [])`

---

## Key Files

| File | Purpose |
|------|---------|
| `theme/index.jsx` | Entry point — initializes FPI, exports all page/section/component references |
| `theme/providers/global-provider.jsx` | ThemeProvider — SEO meta, Copilot.live init |
| `theme/helper/utils.js` | `transformImage`, `sanitizeHTMLTag`, color utils |
| `theme/helper/hooks/` | 20+ custom hooks (`useThemeConfig`, `useAddress`, `useWishlist`, etc.) |
| `theme/page-layouts/` | Feature logic hooks — do not overwrite |
| `theme/helper/lib.js` | `globalDataResolver`, `pageDataResolver` |
| `theme/helper/auth-guard.js` | Auth guard utilities |
| `theme/config/settings_schema.json` | All merchant-configurable theme props |
| `webpack.config.js` | Build config — Less modules, code splitting |

---

## References

| File | Topic |
|------|-------|
| `references/ssr-browser-guards.md` | SSR safety patterns |
| `references/fpi-data-fetching.md` | FPI GraphQL patterns |
| `references/platform-boundaries.md` | Module ownership boundaries |
| `references/url-navigation.md` | Action-based navigation |
| `references/analytics-events.md` | Event dispatch safety |
| `references/image-optimization.md` | transformImage usage |
| `references/theme-configuration.md` | settings_schema patterns |
| `references/styling-conventions.md` | Less modules + CSS variables |
| `references/component-design.md` | Component patterns |
