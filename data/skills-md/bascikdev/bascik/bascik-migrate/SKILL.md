---
name: bascik-migrate
description: Migrate an existing website to Bascik. Use when converting a React, Next.js, Vue, Svelte, SvelteKit, Astro, Eleventy, Hugo, WordPress, or plain HTML site into Bascik pages and components; mapping props, slots, state, routing, layouts, data fetching, content collections, and template loops to Bascik equivalents; or handling existing sitemap.xml and robots.txt files during a migration.
license: MIT
metadata:
  author: bascik
  homepage: https://bascik.dev
---

# Migrating to Bascik

Requires the `bascik` skill for component rules and the `bascik-scripts` skill for build-time data.

To have coding agents refactor a live site to production parity at every breakpoint and 100 in all five Lighthouse categories, install the opt-in `bascik-refactor` skill (`npx skills add bascikdev/bascik --skill bascik-refactor`) and read `node <skills-dir>/bascik/scripts/read-doc.mjs /how-to/agent-migration`.

## Procedure

1. **Inventory.** List every URL, shared layout region (`<head>` tags, header, footer, nav), repeated widget, data source, and client behavior. Run `node <skills-dir>/bascik/scripts/list-components.mjs` if Bascik components already exist.
2. **Read the framework guide.** `node <skills-dir>/bascik/scripts/read-doc.mjs /switch/from-<framework>` (`react`, `next`, `vue`, `svelte`, `astro`, `eleventy`, `hugo`, `wordpress`). Read it before writing any code; it maps each framework feature to its Bascik equivalent.
3. **Pages first.** One `.html` per URL in `src/pages/`, each with its own `<html>`, `<head>`, and `<body>`. Parameterized URLs become dynamic route templates.
4. **Extract components.** Each page ends up as a list of tags, not a pasted block of the old site's HTML. Shared head becomes `<site-head />`; header, footer, and nav become components; each section with a nameable job (hero, pricing, reviews, signup form) becomes a component; repeated widgets become one component with props and slots. Follow the old site's component boundaries where they are sound, but do not copy wrappers that only existed for the framework (providers, layout shells, one-element components) or props threaded through layers: use a slot instead. Use `new-component.mjs` (in the `bascik` skill) for the folder layout, and the `bascik-components` skill for where to split.
   **Keep or improve the semantics.** Carry over every semantic element the old site has (`<nav>`, `<header>`, `<main>`, `<article>`, `<button>`, `<label>`, heading levels), and never turn semantic markup into `<div>`s to make a component fit. Make each component's root the element for its job (a nav component's root is the `<nav>`, not a `<div>` around it), and replace framework div soup with the right element where it is safe: a clickable `<div>` becomes a `<button type="button">`, a list of links becomes a `<ul>`. Checklist: `node <skills-dir>/bascik/scripts/read-doc.mjs /component-best-practices#use-htmls-elements`.
5. **Keep TypeScript.** A TypeScript source site stays TypeScript: component logic moves to a `.ts` companion or an inline `<script type="text/typescript">` and keeps its types (prop types become the `@bascik` comment and the types of what the script reads), and data loaders become typed `.ts` helpers (beside the component or page that uses them, or in `src/lib/` when several share them, step 8). A JavaScript site gets TypeScript for every new file unless the person says otherwise. Erasable syntax works with no setup; for `enum`, decorators, or npm packages in the browser, use esbuild (the `scripts.typescript` snippet in the `bascik` skill). Docs: `/scoped-javascript#typescript-in-component-scripts`, `/configuration#scriptstypescript`, `/how-to/bundling-npm-packages`.
6. **Move styles.** Delete framework scoped-style mechanisms and put the CSS in each component's companion `.css`. Class names stay the same; Bascik scopes them. Global styles go to `src/pages/css/styles.css`.
7. **Move behavior.** Replace state and effects with a TypeScript script per component, targeting elements by `id`. Prefer HTML and CSS solutions where they exist: a framework disclosure becomes `<details>`, a modal becomes `<dialog>`, a dropdown becomes `popover`. Attach click handlers to `<button>` and `<a>` elements, not to `<div>`s, and put state a screen reader needs in ARIA attributes (`aria-expanded`, `aria-pressed`).
8. **Move data.** Framework data loaders become `data-bascik-build` scripts that call typed helpers. Put each module (data, helper, types) next to its one user: in the component's folder, imported with `./faqs.ts`, or beside the one page that uses it as a `.ts` file. Content lives with the component that renders it; a page that also needs it (JSON-LD) imports it from the component's folder. Only modules several components or pages share go in `src/lib/`. Do not copy the old site's `lib/` or `data/` folder as it is: per-route data parked there moves beside its user, and `audit-components.mjs` reports a `src/lib/` module with one user. Every script and helper builds its markup with `html` from `@bascik/bascik/html` (`raw()` for trusted or sanitized HTML, `json()` for JSON-LD); never port or write an escaper of your own.
9. **Verify.** `node <skills-dir>/bascik/scripts/verify.mjs --build` and `node <skills-dir>/bascik/scripts/audit-components.mjs` (exit 0, or each kept warning explained), then compare old and new pages URL by URL. Do not copy confirmed responsive defects: test short portrait and landscape heights, measure text/header/section/CTA bounds, fix the owning constraint and add failing-before/passing-after tests across shared routes. Preserve unaffected layouts and record each intentional correction. Read `read-doc.mjs /how-to/agent-migration#finding-responsive-defects` for the investigation and parity-review procedure.

## Cross-framework mapping

| Concept                                                                           | Bascik                                                                                                                                                |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Component file (`.jsx`, `.tsx`, `.vue`, `.svelte`, `.astro`)                      | `src/components/<name>/<name>.html` with a hyphenated name (`Card.vue` becomes `info-card`), plus `<name>.ts` for its behavior                        |
| `.ts` and `.tsx` logic, prop and state types                                      | Typed `<name>.ts` companion or `<script type="text/typescript">`; types and helpers one component uses in its folder, shared ones in `src/lib/*.ts`   |
| Scoped styles (`<style scoped>`, CSS Modules, Svelte styles)                      | Companion `<name>.css`, scoped automatically                                                                                                          |
| `children`, `<slot />`, `{@render children()}`                                    | `data-bascik-slot` (no value), fallback inside                                                                                                        |
| Named slots, render props, snippets                                               | `<div data-bascik-slot="x">` in the template and as the wrapper at the usage site                                                                     |
| Props (`defineProps`, `$props()`, `props.x`)                                      | `data-bascik-prop-x`, text only                                                                                                                       |
| Prop bound to an attribute                                                        | `data-bascik-attr-<attribute>="propName"`                                                                                                             |
| Object, array, or function props                                                  | Not possible: print one component per item from a build script, or embed JSON with `` html`<script type="application/json">${json(data)}</script>` `` |
| `useState`, `ref`, `$state`                                                       | Typed variables in the component script, applied to the DOM by a function                                                                             |
| Callback props, `$emit`, `v-model`                                                | `dispatchEvent(new CustomEvent('x', { bubbles: true, detail }))`, parent listens on its root                                                          |
| `v-if`, `{#if}`, conditional JSX                                                  | Build time: a build script prints one branch. Runtime: toggle `hidden`                                                                                |
| `.map()`, `v-for`, `{#each}`                                                      | Build-time loop in a build script, or clone a `<template>` at runtime                                                                                 |
| File-system routing                                                               | One `.html` per URL in `src/pages/`                                                                                                                   |
| `[slug]`, `getStaticPaths`, `generateStaticParams`, pagination                    | `src/pages/blog/[slug].html` (or `[slug]/index.html` for trailing slashes) with `<script data-bascik-routes>`                                         |
| `getStaticProps`, `onMounted` fetch, front matter                                 | `<script data-bascik-build>` for shared data; `fetch()` in a component script for per-visitor data                                                    |
| Layouts                                                                           | Pages keep `<html>`/`<head>`/`<body>`; layout pieces become components                                                                                |
| Template includes with variables, filters, loops (Nunjucks, Liquid, Go templates) | TypeScript helpers returning `html` values, beside their one user or in `src/lib/` when shared. Only static includes become components                |
| Content collections (`getCollection`, Eleventy collections)                       | One helper (`src/lib/posts.ts` when several pages read it): `fs` read, `gray-matter`, `zod`, sort by parsed date                                      |
| API routes (`app/api/x/route.ts`)                                                 | `src/api/x.ts` exporting `GET`/`POST`; `context.params` is a plain object; needs `bascik --server`                                                    |
| `next/link`, `next/image`, `next/font`                                            | `<a>`, `<img>` with `width`/`height`, self-hosted `@font-face` plus `<link rel="preload">`                                                            |
| RSS/Atom feeds                                                                    | A `pipeline.exec` script with `phase: 'post'` writing to `BASCIK_OUT_DIR`                                                                             |
| Image optimization, syntax highlighting                                           | Not built in; add your own build step                                                                                                                 |

## Gotchas that apply everywhere

- **Build every template with `html`** in scripts and helpers; JSX and Vue templates escaped for you, and `html` does the same for each value (and blocks `javascript:` URLs). Delete a project `escapeHtml` instead of porting it; `audit-components.mjs` reports one.
- **Component tag names need a hyphen.**
- **Named-slot wrappers are removed**, so wrap headings and links in a `<div data-bascik-slot="x">`.
- **Elements created with `document.createElement` get no element-selector styles.** Clone a `<template>` in the component instead.
- **Production moves component scripts to the end of the document.** Look up elements inside handlers or after `DOMContentLoaded`; keep pre-paint scripts (theme) in `<head>`.
- **Re-sync form state on `pageshow`** after Back/Forward or reload.
- **`bascik --check` reports components printed only by build scripts as unused.** That is expected.
- **Add `"html.validate.scripts": false` to `.vscode/settings.json`** (or run `bascik init`, which merges it in). Otherwise VS Code joins a page's `<script>` blocks into one file and reports false errors such as "A module cannot have multiple default exports".
- **Adapt existing editor linters; do not introduce new ones by default.** Once the head moves into a component and a build script, webhint and axe report a missing charset, viewport, and `<title>` on source pages. `bascik init` leaves third-party linter configs alone. If the person uses one, preserve its settings and adapt the source exceptions in `read-doc.mjs /testing/linting#editor-linters-read-source`. Never add head tags back to source pages to quiet them.
- **Do not generate page files into `src/pages/`.** Use dynamic routes.
- **Exclude data-reading build scripts from the cache** (`scripts.cache.exclude`) and watch `content/` (`pipeline.watchPaths`).
- **Tailwind:** run it as a `pre` exec script with `scoping.attributes.class: false`; see `read-doc.mjs /libraries`.
- **Start from the examples** for layout, SEO tags, a blog, and interactive widgets: `add-example.mjs --list` in the `bascik` skill.

## Existing `sitemap.xml` and `robots.txt`

1. Read both files.
2. If they contain nothing Bascik would not generate (no hand-curated URLs, live `Disallow` rules, external sitemap index pointer, or bot-specific directives), delete them. Bascik generates fresh ones at build time. Do not copy them into `src/pages/` and do not disable `generate.sitemap` or `generate.robots`.
3. If they contain custom directives, keep the authored file in `src/pages/`, set the matching `generate` flag to `false`, and add a config comment explaining why.
4. Exclude redirect-only pages from the generated sitemap with `<meta name="bascik-sitemap" content="exclude">`.

Copying old files while disabling generation looks correct but freezes the sitemap at the old URL list forever.

For Astro, Eleventy, and Hugo, read the live guide with `read-doc.mjs /switch/from-astro` (or `from-eleventy`, `from-hugo`).
