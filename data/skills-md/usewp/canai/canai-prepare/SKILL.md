---
name: canai-prepare
description: >
  Prepares CanAI-friendly static sites as one self-contained HTML file per page: semantic HTML5,
  Tailwind utility classes, vanilla JS or Alpine.js for interactivity, Lucide icon markup.
  Use when the user asks to prepare HTML for CanAI, single-html pages, image/mockup to HTML,
  screenshot to HTML, SPA or PWA to static pages, static site export, or "canai-prepare".
  Triggers on: "canai-prepare", "prepare html", "image to html", "mockup to html", "screenshot to html",
  "spa to html", "pwa to html", "static html", "single html", "per-page html", "convert design to html".
metadata:
  author: canai
  version: "1.10.1"
allowed-tools: Bash Read Write Edit Grep Glob
---

# CanAI Prepare — single-HTML static pages

Generate **recommended static markup** for later import into **CanAI**: one **complete HTML document per page** (no React/Vue/build tools). Styling is **Tailwind CSS** utilities only; behavior is **vanilla JS** or **Alpine.js**; icons are **Lucide** (`data-lucide`).

**Assume the agent runs in the user’s own folder** (not necessarily the WordPress root). This skill focuses on **CanAI-compatible, integration-ready** single-HTML output only — no requirement for WP-CLI, `.env.wplocal`, or writing under `wp-content/`.

See [references/BOILERPLATE.md](references/BOILERPLATE.md) for the canonical skeleton, Alpine/Lucide patterns, and the `pages.json` / `menus.json` formats. See [references/STRUCTURE-NAVIGATION.md](references/STRUCTURE-NAVIGATION.md) for the shared Atomic Design navigation contract used by both `canai-prepare` and `canai-mcp`.

## Purpose

- Output goes into the **current working directory** (or a user-specified output path). Files use **relative** asset paths so the project folder is self-contained and portable — it can later be copied into WordPress uploads, served locally, or handed off to `**canai-mcp**` for import.
- Files are **CanAI-shaped**: Atomic Design navigation comments, semantic regions, and class names that map cleanly to Twig + `_canai_css` / `_canai_js` later.

## Tech stack (strict)


| Allowed        | Notes                                                                                         |
| -------------- | --------------------------------------------------------------------------------------------- |
| Semantic HTML5 | `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`                |
| Tailwind CSS   | Utility classes only; **no** `<style>` blocks in prepared HTML (CanAI stores CSS in `_canai_css`) |
| Vanilla JS     | Small IIFE or `DOMContentLoaded` handlers at end of `<body>`                                  |
| Alpine.js      | Use when stateful UI is simpler than hand-written JS (dropdowns, tabs, accordions)            |
| Lucide         | `<i data-lucide="icon-name" class="h-5 w-5"></i>`                                             |



| Disallowed                                                    |
| ------------------------------------------------------------- |
| React, Vue, Svelte, Angular, bundlers, JSX, `.vue` SFCs       |
| Tailwind CLI/build step in this skill (Play CDN classes only) |
| Heavy CSS frameworks besides Tailwind utilities               |


## Library injection — CanAI handles it on the site

CanAI outputs the same libraries through WordPress hooks when enabled in **WP Admin → CanAI → Settings** (`TailwindManager`, `LucideManager`, `AlpineManager`, `AssetManager`):


| What the static preview file simulates                                                            | Where CanAI loads it                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `<title>…</title>`                                                                                | `**wp_head()`** — WordPress outputs the document title (page/post SEO title); do not duplicate a literal `<title>` inside `_canai_html` if the theme/layout already prints it via `wp_head()` |
| `<script>` tags for Tailwind Play CDN, Alpine, Lucide UMD (inside `WPCanAI-PREVIEW-LIBS` in `<head>`) | `**wp_head()**` — enqueue/inject head scripts the theme/CanAI pipeline would print before `</head>`                                                                                           |
| `<script>lucide.createIcons();</script>` (inside `WPCanAI-PREVIEW-LIBS` before `</body>`)             | `**wp_footer()**` — footer scripts (icon init and similar)                                                                                                                                  |


**Do not assume** every site has the same toggles: tell the user to enable **Load Tailwind**, **Lucide**, and **Alpine** (if templates use `x-`*) as needed.

Prepared `.html` files still include **preview-only** copies of those scripts so the file can be opened in a browser **outside** WordPress. Wrap them in:

```html
<!-- WPCanAI-PREVIEW-LIBS:START -->
...
<!-- WPCanAI-PREVIEW-LIBS:END -->
```

When importing into CanAI, **strip** the preview blocks from markup you paste into templates — CanAI will supply Tailwind/Lucide/Alpine via `**wp_head()`** / `**wp_footer()**` instead. Page-specific JS stays **outside** the preview markers (maps to `_canai_js`).

## Layout mapping — header / footer vs main content

In a **full static HTML** file, you may include `<header>` and `<footer>` for preview and for SPA splits. After import into CanAI, the usual split is:

- `**<header>...</header>`** → a **header**-type template component (site navigation shell), conventionally the **site header** component used by the main **layout** template.
- `**<footer>...</footer>`** → a **footer**-type template component, conventionally the **site footer** component used by the main layout.
- `**<main>...</main>`** (page body) → the page or type-specific template’s `**_canai_html**` (inside `{{ page_content }}` in the layout).

When generating **linked single-HTML files** (Workflow B), duplicating header/footer across files is fine for static preview; on import, extract shared regions once into `**wpcanai_template('site-header')`** / `**wpcanai_template('site-footer')**` (or the project’s actual header/footer slugs) and keep only `<main>` (and layout-specific sections) in each page template.

## Navigation — two menus, marked

> **A site has at most two menus: `primary` (the header nav) and `footer` (the footer nav).** Mark both, keep their real links, and never invent a third menu name (`topnav`, `mobile`, `main`, `social`). On import they become the site's two WordPress menus, and CanAI never renders a hardcoded nav.

- **Header nav:** `<!-- Navigation / Primary -->` immediately before `<nav data-canai-menu="primary" aria-label="Primary">`.
- **Footer nav:** `<!-- Navigation / Footer -->` immediately before `<nav data-canai-menu="footer" aria-label="Footer">`. When the footer links sit in several columns, wrap all the columns in that one `<nav>`.
- **Keep real `<a href>` links inside both** (`href="about.html"`), so the file previews in a browser. Do not write Twig or menu loops here: `canai-mcp` swaps the links for a `get_menu()` loop on import.
- **A mobile drawer repeats the primary links**, so it is marked `data-canai-menu="primary"` too. Breadcrumbs and pagination are `Navigation` landmarks, not menus, and carry no `data-canai-menu`.
- **Write `menus.json` next to `pages.json`**, listing each marked nav's links in order: `{ "primary": [ … ], "footer": [ … ] }`. An item is `{ "title", "page" }` for a link to a generated page (`page` is that page's `slug` from `pages.json`) or `{ "title", "url" }` for any other link, with optional `"target": "_blank"` and `"children": [ … ]` (at most 3 levels). That is exactly the `items` shape of `wpcanai-write-menu`. Example in [references/BOILERPLATE.md](references/BOILERPLATE.md#menusjson-manifest-site-navigation).
- **Mega menus are menu data too.** A column heading or dropdown trigger that is not a link is an item with `children` and neither `page` nor `url`; a link's one-line blurb goes in `"description"` and its Lucide icon name in `"icon"` (the same name as its `data-lucide`). Keep the panel's real markup in the HTML (headings, icons, blurbs, links), and list the same structure in `menus.json`. A thumbnail stays a relative `<img>` in the HTML and `"image"` is left out: `canai-mcp` sideloads it and adds the attachment id on import.

## Output paths

Default: write under `**./<project-slug>/**` in the **current working directory** (or a path the user specifies). No WordPress root or uploads folder is required.

```
<project-slug>/
  index.html
  about.html
  ...
  assets/
    hero.webp
    ...
  pages.json          # optional; multi-page / SPA decomposition
  menus.json          # the primary / footer nav links (see Navigation)
```

- `**project-slug`:** kebab-case, short (e.g. `landing-q2`, `shop-redesign`).
- `**assets/`:** binary media copied from designs or exported from SPAs; reference with **relative** paths (`src="assets/photo.jpg"`).
- **Cross-page links:** relative (`href="about.html"`), not absolute domain.

## Workflow A — Image / mockup → HTML

1. Accept screenshot, Figma export, or other reference image(s).
2. Infer layout: header, hero, sections, footer; typography scale; spacing; color **roles** (map to Tailwind palette + optional `tailwind.config` extend in a small inline script **only if needed** — prefer standard utilities).
3. Run the **Image framing preflight** below before choosing image-container classes.
4. Emit **one `.html` file per distinct full-page design** the user asked for.
5. Label navigable elements with the exact HTML form `<!-- Type / Short Label -->`, such as `<!-- Section / Hero -->`, `<!-- Card / Feature -->`, and `<!-- Button / Get Started -->`. Follow the controlled vocabulary in [references/STRUCTURE-NAVIGATION.md](references/STRUCTURE-NAVIGATION.md).
6. Save extracted raster assets into `assets/`; reference them relatively. Use stable filenames; optionally list them in a short `README.txt` in the project folder.

## Image framing preflight

Run this for every meaningful raster image before writing its container markup. Logos, icons, decorative textures, and images rendered with `object-contain` do not need subject-crop analysis.

1. **Inspect the asset, not only the reference page.** Read its intrinsic width and height with an available local image-info tool and inspect the pixels with the host's image viewer. Record the aspect (`width / height`) and the important region: faces, full bodies, co-subjects, hands, products, awards, or text baked into the image. If the asset cannot be inspected, preserve it with `object-contain` or a close-to-source aspect ratio rather than guessing a destructive crop.
2. **Choose the container from the source shape and design role.** Prefer responsive `aspect-*` utilities over shallow fixed `h-*` crops: portrait originals → `aspect-[4/5]`, `aspect-[3/4]`, or `aspect-square`; square → `aspect-square` or `aspect-[4/3]`; landscape → `aspect-[16/9]`, `aspect-[3/2]`, or `aspect-[4/3]`. A portrait may use a landscape crop only when the inspected safe region demonstrably fits at every target breakpoint.
3. **Set an optical focal point when using `object-cover`.** Start from these baselines, then adjust from the actual image: headshot/single portrait `object-[center_30%]` (roughly 25–35% Y); seated pair `object-[center_58%]` (55–60% Y); standing group `object-[center_20%]`; subject holding an item `object-[center_80%]` (75–85% Y) with at least `aspect-[3/4]` or comparable height. Off-centre subjects need both coordinates, for example `object-[80%_25%]`. These are starting points, never a substitute for inspection.
4. **Verify responsive crops.** Preview at narrow mobile and wide desktop sizes. Faces, heads, co-subjects, and task-relevant objects must remain visible without pressing against an edge. Use breakpoint-specific aspect/focal classes when the composition genuinely needs them; if no crop works robustly, use a taller/source-matched container or `object-contain`.

Example:

```html
<div class="aspect-[4/5] overflow-hidden rounded-2xl sm:aspect-[3/4]">
  <img src="assets/founder.webp" alt="Founder holding the product" class="h-full w-full object-cover object-[center_80%]" width="1200" height="1600" loading="lazy">
</div>
```

## Workflow B — SPA / PWA → linked static HTML pages

1. Discover routes: router config (`react-router`, Vue Router, Next.js `app/`, etc.), `sitemap`, nav links, or user-provided list.
2. For **each route**, generate **one self-contained HTML file** (duplicate header/footer/nav per file — no partials in this skill).
3. Replace client-side navigation with normal `**<a href="...">`** links between generated files.
4. Downgrade framework components to semantic HTML + Tailwind + Alpine/vanilla behavior.
5. Write `**pages.json**` — array of `{ "slug", "title", "file" }` for traceability.
6. Write `**menus.json**` from the marked header and footer navs (see **Navigation — two menus, marked**).

## CanAI compatibility checklist

- Navigation comments use the exact `<!-- Type / Short Label -->` grammar and controlled vocabulary.
- Every `<main>`, `<section>`, `<header>`, `<footer>`, `<nav>`, and `<aside>` has its required matching type immediately before the opening tag.
- Header nav is `<!-- Navigation / Primary -->` + `<nav data-canai-menu="primary">`, footer nav is `<!-- Navigation / Footer -->` + `<nav data-canai-menu="footer">`; no other `data-canai-menu` value; `menus.json` lists their links.
- No `<style>` in body content; no inline `style=""` unless unavoidable (prefer utilities).
- Scripts: preview libs inside `WPCanAI-PREVIEW-LIBS`; page logic below, outside those markers.
- Images: framing preflight completed; descriptive `alt`, intrinsic `width`/`height`, responsive aspect container, and `loading="lazy"` below the fold.
- Lucide: decorative icons `aria-hidden="true"`; controls have `aria-label`.
- Links: readable link text; avoid `href="#"` for real navigation.

## Handoff to CanAI

1. **Settings:** Enable Tailwind, Lucide, and Alpine (if used) in **CanAI → Settings** so scripts load via `**wp_head()`** / `**wp_footer()**` as above.
2. **Document title:** Set the WordPress page/post title (and SEO plugin fields if used); `**wp_head()`** outputs `<title>` on the live site — omit a duplicate `<title>` from imported template fragments when the layout already includes `{{ wp_head() }}`.
3. **Layout:** Move header markup into the **site header** component template; footer into the **site footer** component; wire them from the main **layout** template (`{{ wpcanai_template('site-header') }}`, `{{ wpcanai_template('site-footer') }}` — use the project’s actual slugs).
4. **Import:** Use `**canai-mcp**` (convert HTML → Twig, write `_canai_html` / `_canai_css` / `_canai_js`) — follow that skill for storage rules (e.g. no `post_content` for CanAI bodies).
5. **Strip** `WPCanAI-PREVIEW-LIBS` blocks when pasting into templates (avoid duplicating what CanAI already injects).
6. **Images become ID-based helpers at import, not here.** Prepared `.html` keeps **relative** `src="assets/…"` so the folder previews in a plain browser. On import, `canai-mcp` sideloads each asset and rewrites `<img>` → `{{ image_attrs(id, 'src,alt') }}` (and other surfaces → `{{ media_url(id, size) }}`) by media **id** — so keep the prepared markup clean and swappable: one `<img>` per asset, a descriptive `alt`, `width`/`height` when known, and no inline `style` that would fight the helper output.
7. **Navigation comments map 1:1 on import:** `<!-- Type / Short Label -->` becomes `{# Type / Short Label #}`. Preserve the type and label exactly; only replace the delimiters. Follow [references/STRUCTURE-NAVIGATION.md](references/STRUCTURE-NAVIGATION.md), including the required landmark mappings, so `wpcanai-scan` passes and the editor's Structure metabox stays useful.
8. **Keep copy translation-ready.** On native-i18n target sites, downstream import turns each user-facing sentence into one `{{ t('…') }}` translation source. Write each sentence as one unit inside its block element: inline tags inside the sentence are fine (`<p>Get <strong>free shipping</strong> today.</p>` becomes one source), and no block element ever sits inside a sentence. This mirrors the image → `image_attrs()` and section-comment handoffs.
9. **WooCommerce pages** — for shop / cart / checkout pages, emit the cart/checkout region as one navigable placeholder such as `<!-- Section / Cart -->`, with any implementation instruction in a separate `<!-- @dev Replace with wc_cart_block() on import -->` comment. Downstream (`canai-mcp`) swaps in the `wc_*` Twig helpers; do not wire helper markup here.
10. **Navigation becomes WordPress menus on import.** `canai-mcp` writes `menus.json` with `wpcanai-write-menu` (one call per key, after the pages exist) and replaces each marked `<nav data-canai-menu>`'s links with the `get_menu('primary')` / `get_menu('footer')` loop. The prepared file keeps its real links; the site owner edits the menus in WordPress afterwards.

## Related skills

- `**canai-mcp**` — MCP tools for `_canai_*` on the configured server.
