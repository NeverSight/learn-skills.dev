---
name: deco-storefront-test-checklist
description: Generate a context-aware QA checklist for any Deco storefront by analyzing its sections, components, routes, and interactive patterns. Use when testing after migrations, upgrades, major refactors, or before deploying to production. Produces checklists scoped to the actual components in the site, not generic boilerplate.
---

# Deco Storefront Test Checklist Generator

Generates a **context-aware** QA checklist by reading the site's actual component inventory, registered sections, interactive patterns, and route structure. The output is scoped to what exists — no phantom items for features the site doesn't have.

## When to Use This Skill

- After a Fresh → TanStack migration
- After removing/refactoring islands
- After upgrading `@decocms/start` or `@decocms/apps`
- After changing caching configuration
- After modifying the section registry or resolution engine
- Before deploying a new version to production
- When onboarding a QA tester to a specific storefront

## Step 1 — Discover the Site Inventory

Run these commands from the site root to build context. The checklist MUST be scoped to what actually exists.

### 1.1 Registered Sections

```bash
# Find setup file and list all registered sections
rg 'registerSections' src/ -l
# Then read the registration map to get every section key
rg '"site/sections/' src/setup.ts
```

### 1.2 Routes (Page Types)

```bash
ls src/routes/
# Identify: home (index.tsx), catch-all ($.tsx), custom routes
```

### 1.3 Interactive Components

```bash
# Components with client-side state
rg 'useState|useEffect|useCart|useUI|useSignal|displayCart|displayMenu' src/components/ --glob '*.{tsx,ts}' -l

# Components with event listeners (potential hydration issues)
rg 'addEventListener|onClick|onChange|onSubmit' src/components/ --glob '*.{tsx,ts}' -l

# Vanilla JS DOM access (fragile patterns)
rg 'document\.(getElementById|querySelector|querySelectorAll)' src/components/ --glob '*.{tsx,ts}' -l
```

### 1.4 Section Loaders

```bash
rg 'registerSectionLoaders' src/setup.ts -A 20
```

### 1.5 External Integrations

```bash
# VTEX calls
rg 'vtex|VTEX' src/lib/ src/hooks/ --glob '*.{tsx,ts}' -l

# Analytics
rg 'sendEvent|dataLayer|DECO.*events' src/ --glob '*.{tsx,ts}' -l

# Third-party (Trustvox, Autodesk, etc.)
rg 'trustvox|Autodesk|forge|instagram|whatsapp' src/ --glob '*.{tsx,ts}' -i -l
```

### 1.6 UI State Signals

```bash
rg 'signal\(|useUI' src/sdk/ src/hooks/ --glob '*.{tsx,ts}'
```

This reveals which drawers, modals, and popups are managed by signals (cart, menu, search, etc.).

## Step 2 — Generate the Checklist

Using the inventory from Step 1, build the checklist below. **Only include sections that exist in the site.** Mark items with context from the actual file paths.

---

## Checklist Template

### A. Server Startup & Build

| # | Test | How to Verify | Component/File |
|---|------|--------------|----------------|
| A1 | Dev server starts without errors | `npm run dev` — no red errors in terminal | `worker-entry.ts`, `setup.ts` |
| A2 | Production build succeeds | `npm run build` — exit code 0 | `vite.config.ts` |
| A3 | All sections register without warnings | Check terminal for `[DecoSection]` warnings | `setup.ts` |
| A4 | Section loaders resolve | No `undefined` loader errors in terminal | `setup.ts` → `registerSectionLoaders` |

### B. Page Loading (per route)

For each route in `src/routes/`, verify:

| # | Test | How to Verify | Route |
|---|------|--------------|-------|
| B1 | Home page renders all sections | Visual inspection + DevTools console clean | `index.tsx` |
| B2 | PLP (category/search) renders product grid | Navigate to a category URL | `$.tsx` (catch-all) |
| B3 | PDP renders all product sections | Navigate to a product URL | `$.tsx` (catch-all) |
| B4 | Institutional pages render | Navigate to `/quem-somos` or similar | `$.tsx` (catch-all) |
| B5 | 404 page renders | Navigate to `/nonexistent-page-xyz` | `$.tsx` → `notFoundComponent` |
| B6 | House Catalog pages render | Navigate to a house catalog product | `$.tsx` (catch-all) |

### C. Header

For sites with `sections/Header/Header.tsx`:

| # | Test | How to Verify | Component |
|---|------|--------------|-----------|
| C1 | Alert bar renders and slides | Visual — top banner rotates | `header/Alert.tsx` + `ui/SliderJS.tsx` |
| C2 | Menu button opens drawer (mobile) | Click hamburger icon | `header/Buttons/Menu.tsx` → `useUI().displayMenu` |
| C3 | Menu drawer closes with Escape | Press Escape while open | `ui/Drawer.tsx` → `window.addEventListener("keydown")` |
| C4 | Menu drawer closes on overlay click | Click dark overlay | `ui/Drawer.tsx` → `<label htmlFor={id}>` |
| C5 | Search opens popup/drawer | Click search icon | `header/Searchbar.tsx` → `useUI().displaySearchPopup` |
| C6 | Search returns results | Type a product name | `search/SearchBar.tsx` or `SearchbarNew.tsx` |
| C7 | Cart icon opens cart drawer | Click cart icon | `header/Buttons/Cart/common.tsx` → `useUI().displayCart` |
| C8 | Cart badge shows item count | Add item, check badge | `header/Buttons/Cart/vtex.tsx` → `useCart()` |
| C9 | Location modal opens | Click location icon | `header/Location.tsx` → `UserLocationModal` |
| C10 | Login/user icon works | Click user icon | `header/Navbar.tsx` → Login component |
| C11 | NavItems show mega-menu on hover | Hover over top-level nav | `header/NavItem.tsx` |

### D. Sliders & Carousels

For every component that imports `SliderJS`:

| # | Test | How to Verify | Component |
|---|------|--------------|-----------|
| D1 | Previous/Next buttons work | Click arrows | `ui/SliderJS.tsx` → `prev/next addEventListener` |
| D2 | Dot indicators work | Click dots | `ui/SliderJS.tsx` → `dotHandlers[]` |
| D3 | Autoplay advances slides | Wait 3-5 seconds | `ui/SliderJS.tsx` → `setInterval(timeout)` |
| D4 | No listener memory leak | Navigate away and back, check Performance tab | `ui/SliderJS.tsx` → cleanup `return () => {}` |
| D5 | Intersection Observer triggers | Scroll to a slider, first visible slide is active | `ui/SliderJS.tsx` → `IntersectionObserver` |

**Apply to each slider instance:**
- Home banner carousel (`ui/BannerCarousel.tsx`, `ui/BannerClientSide.tsx`)
- Product shelf (`product/ProductShelf.tsx`, `ProductShelfTabbed.tsx`)
- Category list (`Category/CategoryList.tsx`)
- Testimonials, Cases de Sucesso, Client Logos
- Mini banners, Image double blocks
- Footer benefits

### E. PDP — Product Detail Page

For sites with `ProductMain/ProductMain.tsx`:

| # | Test | How to Verify | Component |
|---|------|--------------|-----------|
| E1 | Product image gallery loads | Images visible, slider works | `Gallery/ImageSlider.tsx` |
| E2 | Image zoom works | Click/hover on main image | `ProductImageZoom.tsx` |
| E3 | Variant selector changes SKU | Click color/size chips | `ProductVariantSelector.tsx`, `SkuVariation.tsx` |
| E4 | Variant selector stays on same page | URL changes path only, no redirect to external domain | `SkuVariation.tsx` → `relative(product.url)` |
| E5 | Price updates on variant change | Select different SKU, price changes | `ProductMain.tsx` → price display |
| E6 | Add to Cart button works | Click "Comprar", cart drawer opens | `AddToCartButton/common.tsx` → `useCart().addItems` + `displayCart.value = true` |
| E7 | Add to Cart button shows loading | Click and observe spinner | `AddToCartButton/common.tsx` → `loading` state |
| E8 | Shipping simulation returns options | Type CEP, click "Calcular" | `ui/ShippingSimulation.tsx` → `useCart().simulate` |
| E9 | Shipping simulation doesn't append `/p?` | Check URL bar after calculating | No `f-partial` / `f-client-nav` attributes |
| E10 | Wishlist button toggles | Click heart icon | `wishlist/WishlistButton/common.tsx` |
| E11 | Share button opens modal | Click share icon | `SociaShareTrigger.tsx` → `SocialShareModal.tsx` |
| E12 | Payment methods display | Scroll to payment section | `ProductMain/components/PaymentMethods.tsx` |
| E13 | Trustvox stars render | Check star rating area | `TrustVox/ProductStars.tsx`, `TrustVox/Trustvox.tsx` |
| E14 | "Buy Together" renders (when available) | Product with cross-selling data | `BuyTogether/BuyTogether.tsx` |
| E15 | "Buy Together" handles missing data | Product without cross-selling | Guard `!buyTogetherPricesSimulation` |
| E16 | "Also bought" shelf renders | Scroll to recommendations | `ProductMain/components/ProductShelfAlso.tsx` |
| E17 | Breadcrumb links work | Click breadcrumb items | `ui/Breadcrumb.tsx` |
| E18 | Quantity selector works | Click +/- buttons | `ui/QuantitySelector.tsx` |
| E19 | Out of Stock message shows | Visit OOS product | `OutOfStock.tsx` |
| E20 | Download options work | If product has downloads | `DownloadOptions.tsx` |

### F. Cart (Minicart)

For sites with `minicart/`:

| # | Test | How to Verify | Component |
|---|------|--------------|-----------|
| F1 | Cart drawer opens on add to cart | Add item, drawer slides in | `header/Drawers.tsx` → `CartDrawer` |
| F2 | Cart drawer closes on Escape | Press Escape | `ui/Drawer.tsx` → keydown handler |
| F3 | Cart drawer closes on overlay | Click overlay | `ui/Drawer.tsx` → label overlay |
| F4 | Cart items display correctly | Image, name, price, quantity | `minicart/common/CartItem.tsx` |
| F5 | Quantity can be changed | Click +/- in cart | `useCart().updateItems` |
| F6 | Item can be removed | Click X/trash | `useCart().removeItem` |
| F7 | Coupon can be applied | Type code, submit | `minicart/common/Coupon.tsx` → `useCart().addCouponsToCart` |
| F8 | Total updates on changes | Change quantity or remove | `minicart/common/Cart.tsx` |
| F9 | Free shipping bar progresses | Add items near threshold | `minicart/common/FreeShippingProgressBar.tsx` |
| F10 | Checkout button redirects | Click "Finalizar Compra" | Redirect to VTEX checkout |
| F11 | Cross-selling in cart shows | Products appear below items | `ProductCardCrossSelling.tsx` |

### G. Search / PLP

For sites with `search/SearchResult.tsx`:

| # | Test | How to Verify | Component |
|---|------|--------------|-----------|
| G1 | Products display in grid | Category page shows cards | `search/SearchResult.tsx` |
| G2 | Filters work | Click a filter, results update | `search/Filters.tsx` |
| G3 | Sort dropdown works | Change order, results reorder | `search/Sort.tsx` |
| G4 | Pagination works | Click page 2 | `search/PageControls.tsx` |
| G5 | Price range filter works | Drag slider or type values | `search/PriceRange.tsx` |
| G6 | Search not found shows fallback | Search for "asdqwe123xyz" | `search/NotFound.tsx` → `SectionList` |
| G7 | Product cards are clickable | Click a product card | `product/ProductCard.tsx` |
| G8 | Discount flags display | Product with discount | `product/FlagDiscount.tsx` |
| G9 | Category SEO renders | Check meta tags | `Category/CategorySeo.tsx` |

### H. Modals & Drawers (Signal-Based)

| # | Test | Signal | Component |
|---|------|--------|-----------|
| H1 | Cart drawer | `displayCart` | `ui/Drawer.tsx` |
| H2 | Menu drawer | `displayMenu` | `ui/Drawer.tsx` |
| H3 | Search popup | `displaySearchPopup` | Searchbar |
| H4 | Search drawer (mobile) | `displaySearchDrawer` | Searchbar mobile |
| H5 | Modal shelf product | `displayModalShelfProduct` | Product modal |
| H6 | Cookie consent | localStorage `store-cookie-consent` | `ui/CookieConsent.tsx` |

For each: verify opens, closes on Escape, closes on overlay/X, and **signal.value resets to false**.

### I. Footer

For sites with `sections/Footer/Footer.tsx`:

| # | Test | How to Verify | Component |
|---|------|--------------|-----------|
| I1 | Newsletter email input works | Type email, submit | `footer/Newsletter.tsx` |
| I2 | Footer links render | All sections visible | `footer/FooterItems.tsx` |
| I3 | Social icons link correctly | Click, opens new tab | `footer/Social.tsx` |
| I4 | Payment methods display | Icons visible | `footer/PaymentMethods.tsx` |
| I5 | Benefits slider works | Arrows/dots | `footer/Benefits.tsx` + `ui/SliderJS.tsx` |
| I6 | Our Stores links work | Click a store | `footer/OurStores.tsx` |
| I7 | Back to top works | Click arrow, page scrolls | `footer/BackToTop.tsx` |

### J. House Catalog (when present)

For sites with `product/HouseCatalog/`:

| # | Test | How to Verify | Component |
|---|------|--------------|-----------|
| J1 | ForgeViewer 3D loads | 3D model visible (if URN exists) | `ForgeViewer/ForgeViewer.tsx` |
| J2 | ForgeViewer fallback | "Não possui visualização 3D" message | `ForgeViewer.tsx` → `!urn` guard |
| J3 | SKU selector tabs work | Click different house types | `HouseCatalog/components/Sku/SkuSelector.tsx` |
| J4 | SKU image gallery | Slider of SKU images | `HouseCatalog/components/Sku/ImagesSku.tsx` |
| J5 | Memorial modal opens | Click memorial button | `HouseCatalog/components/Sku/ModalMemorial.tsx` |
| J6 | Comparative table opens | Click compare button | `HouseCatalog/components/ModalComparativeTable.tsx` |
| J7 | House info images | Slider works | `HouseCatalog/components/HouseInfos/ImagesHouseInfos.tsx` |
| J8 | Design section images | Slider works | `HouseCatalog/components/Design/ImagesDesign.tsx` |
| J9 | Cronograma images | Slider works | `HouseCatalog/components/CronogramaObra/ImagesCronograma.tsx` |
| J10 | Summary kit modal | Opens with correct data | `HouseCatalog/components/ModalSummaryKit.tsx` |
| J11 | Add to cart (house) | Adds full kit | `HouseCatalog/components/AddToCartButton.tsx` |

### K. Institucional

For sites with `institucional/`:

| # | Test | How to Verify | Component |
|---|------|--------------|-----------|
| K1 | Stages of the Work wizard | Steps navigate correctly | `StagesOfTheWork/index.tsx` |
| K2 | Stages navigation buttons | Next/Previous work | `StagesOfTheWork/components/NavigationButtons.tsx` |
| K3 | Stages result renders | Final result page shows | `StagesOfTheWork/components/Result/Result.tsx` |
| K4 | Financing simulator | Steps and calculation work | `FinancingSimulator/index.tsx` |
| K5 | Cases de Sucesso slider | Slider works | `institucional/CasesDeSucesso.tsx` |
| K6 | Our Stores map/list | Stores display correctly | `institucional/OurStores.tsx` |
| K7 | FAQ accordion opens/closes | Click question, answer shows | Sections: `FaqAccordion.tsx` |
| K8 | Ready Project modal | Opens with project details | `product/ReadyProject/` |

### L. Calculators

For sites with calculator sections:

| # | Test | How to Verify | Component |
|---|------|--------------|-----------|
| L1 | Shingle calculator | Input values, get result | `product/Calculators/ShingleCalculator/` |
| L2 | Forro Gesso calculator | Input values, get result | `product/Calculators/ForroGessoCalculator/` |
| L3 | Forro Modular calculator | Input values, get result | `product/Calculators/ForroModularCalculator/` |
| L4 | Calculator trigger button | Opens calculator overlay | `triggers/TriggerCalculadorasButton.tsx` |

### M. Analytics & Tracking

| # | Test | How to Verify | Component |
|---|------|--------------|-----------|
| M1 | Page view fires | Check `dataLayer` or `DECO.events` on load | `Analytics.tsx` → `SendEventOnView` |
| M2 | Product click fires | Click product card, check events | `Analytics.tsx` → `SendEventOnClick` |
| M3 | Add to cart event fires | Add item, check `add_to_cart` event | `AddToCartButton/common.tsx` → `sendEvent` |
| M4 | View item event fires | PDP load, check `view_item` | Route loader analytics |

### N. Console Health

| # | Test | What to Check |
|---|------|--------------|
| N1 | No `Element type is invalid` errors | Means a section failed to resolve |
| N2 | No `Invalid tag: site/sections/...` | Means nested section rendered as HTML tag |
| N3 | No `Cannot read properties of undefined` | Means loader data is missing guards |
| N4 | No hydration mismatch warnings | `Prop did not match. Server: ... Client: ...` |
| N5 | No `addEventListener` errors | Missing `window.` prefix or SSR execution |
| N6 | No `[DecoSection]` warnings | Section key not in registry |
| N7 | No CORS errors from admin | `/live/_meta`, `/.decofile` working |

### O. Performance Sanity

| # | Test | How to Verify |
|---|------|--------------|
| O1 | No memory growth on SPA navigation | DevTools → Performance → Memory (navigate 10 pages) |
| O2 | Slider listeners clean up | Navigate away from page with slider, back, check listener count |
| O3 | No duplicate event listeners | Use `getEventListeners(element)` in DevTools |
| O4 | Cache working in production | Check `Cache-Control` headers, `CF-Cache-Status: HIT` |
| O5 | Lazy sections load on demand | Network tab shows chunk load when section enters viewport |

---

## Step 3 — Adapt to the Specific Site

After generating the base checklist:

1. **Remove sections the site doesn't have** — If no HouseCatalog, remove section J entirely
2. **Add site-specific sections** — Custom sections from `setup.ts` that aren't covered above
3. **Check integrations** — If the site uses Shopify instead of VTEX, adapt cart/checkout tests
4. **Note known issues** — Add items for bugs found in previous test rounds
5. **Prioritize** — Mark critical path items (home → PLP → PDP → cart → checkout) as P0

## Discovery Commands for Custom Sections

To find sections not covered by the template:

```bash
# All registered sections
rg '"site/sections/' src/setup.ts | sed 's/.*"site\/sections\///' | sed 's/".*//' | sort

# Sections with loaders (higher risk)
rg 'export const loader' src/sections/ --glob '*.tsx' -l

# Sections with client state (interactive)
rg 'useState|useEffect' src/sections/ --glob '*.tsx' -l

# Sections importing SliderJS (slider tests needed)
rg 'SliderJS' src/sections/ src/components/ --glob '*.tsx' -l
```

## Automation Hooks

For sites with CI/CD, these checks can be automated:

```bash
# Build check
npm run build && echo "PASS: Build" || echo "FAIL: Build"

# Console error check (requires headless browser)
# Use with deco-e2e-testing skill for full automation

# Section registry completeness
node -e "
  const setup = require('./src/setup.ts');
  // Compare registered sections vs section files on disk
"
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `deco-to-tanstack-migration` | Full migration playbook (imports, signals, architecture) |
| `deco-tanstack-navigation` | SPA navigation patterns (`<a>` → `<Link>`, `useNavigate`, `loaderDeps`, forms) |
| `deco-tanstack-storefront-patterns` | Runtime fixes post-migration (nested sections, caching, SliderJS, async_hooks, cart, server functions) |
| `deco-islands-migration` | Islands removal guide with its own verification checklist |
| `deco-e2e-testing` | Automated e2e performance tests with lazy section tracking |
| `deco-full-analysis` | Full site analysis with 9 optimization checklists |
| `deco-startup-analysis` | Analyze startup logs for issues before testing |
