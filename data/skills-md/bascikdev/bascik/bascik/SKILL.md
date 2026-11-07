---
name: bascik
description: Build websites with Bascik, the zero-runtime HTML component build tool. Use whenever a project depends on @bascik/bascik, has a bascik.config.ts, or keeps components in src/components/*.html, or when the user mentions Bascik. Covers pages, components, slots, props, attribute inheritance, the bascik CLI (dev, --build, --server, --check, add), project layout, verifying compiled dist/ output, building a new site, and copying tested example components. Start here; companion skills cover components, compatibility, scripts, SEO, config, testing, and migration.
license: MIT
metadata:
  author: bascik
  homepage: https://bascik.dev
---

# Bascik

Bascik is a build tool for HTML components. It expands custom tags such as `<site-nav />` into the matching component file, scopes the component's CSS, IDs, classes, and scripts, and writes plain HTML pages to `dist/`. It adds zero JavaScript: every script in the output is one you wrote.

It is not a framework. There is no virtual DOM, reactive state, client router, template language, Shadow DOM, or runtime. Write HTML, CSS, and TypeScript (stripped to plain JavaScript), and let Bascik do the isolation at build time.

## Pages read like a list of tags

Write pages as a list of component tags, not big blocks of HTML:

```html
<body>
  <site-header />
  <main id="main">
    <home-hero />
    <pricing-section>
      <plan-card data-bascik-prop-name="Home" data-bascik-prop-price="$49" />
      <plan-card data-bascik-prop-name="Cafe" data-bascik-prop-price="$129" />
    </pricing-section>
    <faq-list />
  </main>
  <site-footer />
</body>
```

- **Split** a section into a component when it has a job you can name (pricing, reviews, signup form), when its markup repeats, or when the page is no longer readable at a glance.
- **Do not split** a piece that only makes sense inside its parent, that would need a prop passed through a component that does not use it, or that is a tiny wrapper used once. Use a slot, or keep the parent whole.
- **Write each fact once.** An address, opening hours, a price, or a phone number lives in one component or one data file, never typed into several. A fact several components show goes in `src/lib/site.ts`; data only one component renders (its FAQ entries, its plans) lives in that component's folder (rule 17). A value that is the same on every page, such as the brand name, belongs inside the component, not passed as a prop on every page. A heading group (eyebrow, heading, intro) that repeats across sections is a `<section-head>` component with props.

Small named files are easier for people and agents to read and change, and each is a boundary for its CSS, IDs, and script. It is a balance: the `bascik-components` skill has the detailed guidance with good and bad examples, and [`scripts/audit-components.mjs`](scripts/audit-components.mjs) checks it.

## TypeScript by default

Write all new code in TypeScript. Use JavaScript only when the person asks for it. When refactoring TypeScript, keep it TypeScript and carry the types across.

- **Browser code** goes in a component's companion `name.ts` (`<script src="name.ts">`) or an inline `<script type="text/typescript">`. Bascik strips the types with Node's strip-only mode, so it works with no setup. Use erasable syntax only: annotations, interfaces, `as`, `!`, and `import type`. `enum`, namespaces with code, and parameter properties fail the build. A plain `<script>` is JavaScript. A page's own `<script src="x.ts">` is compiled and inlined too; a classic one with `defer` or `async` fails the build (inline scripts ignore them), so drop the attribute or mark it `type="module"`. A `type="module"` `.ts` script is inlined, not bundled: importing `./util.ts` (or any relative, `@/` or `.ts` path) fails the build, so bundle it with esbuild or import a published `/js/*.js` URL.
- **Build, routes, server, and stream scripts** are TypeScript with a `.ts` `src=` or a tag marked `type="text/typescript"` (`<script data-bascik-server type="text/typescript">`). Bascik strips them the same way before they run, and compiles them when the page builds, so a syntax error or `enum` fails the build with file:line:column; an unmarked block is JavaScript.
- **`type="text/typescript"` blocks are type checked** in the editor (the VS Code extension or `@bascik/language-server`, with hover, definition and completion for imports) and, opted in, by `bascik --check --typescript`.
- **Node code** is `.ts` too: helpers and data modules, `src/api/` routes, `pipeline.exec` scripts, and `bascik.config.ts`. Node strips their types. Keep each `data-bascik-*` block to a few lines that import typed helpers: `./faqs.ts` for a module in the component's own folder, `@/lib/posts.ts` for one several pages share (rule 17). A helper that returns markup builds it with `html` from `@bascik/bascik/html` and declares `SafeHtml` as its return type (rule 15).
- **esbuild** is the option for full TypeScript (`enum`, decorators, an older browser target): `npm install -D esbuild`, then set `scripts.typescript` to an esbuild transform. Browser code that imports npm packages needs esbuild too, as a `pipeline.exec` step that bundles it into `dist/`.

```ts
// bascik.config.ts (illustrative: esbuild as the browser TypeScript compiler)
import { defineConfig } from "@bascik/bascik/config";
import { transform } from "esbuild";

export default defineConfig({
  scripts: {
    typescript: async (code, { sourcePath }) => {
      const result = await transform(code, {
        loader: "ts",
        target: "es2020",
        sourcefile: sourcePath,
      });
      return result.code;
    },
  },
});
```

Read `/scoped-javascript#typescript-in-component-scripts`, `/configuration#scriptstypescript`, and `/how-to/bundling-npm-packages` before going beyond erasable syntax.

Code in this skill is illustrative. Adapt tag names, paths, and values to the project instead of copying example names literally.

## Recognize a Bascik project

- `package.json` depends on `@bascik/bascik`, or the root has `bascik.config.ts` / `bascik.config.js`, or there are `.html` files under `src/components/`.
- Node.js 22.22 or newer (24 LTS recommended). Node runs `.ts` files natively and Bascik strips browser TypeScript, so no TypeScript build step exists.
- Standard scripts: `npm run dev` (`bascik`), `npm run build` (`bascik --build`), `npm run lint` (`bascik --check`).

## Project layout

```text
src/
  components/            component templates; the file name is the tag name
    site-nav/
      site-nav.html      <site-nav>
      site-nav.css       optional companion stylesheet, scoped to site-nav
      site-nav.ts        optional companion script, loaded with <script src="site-nav.ts">
      links.ts           data or a helper only site-nav uses, imported with ./links.ts
  pages/                 one .html file per URL, plus public assets
    index.html           /
    about.html           /about
    blog/post.html       /blog/post
    404.html             served for unknown routes
    css/styles.css       copied to dist/css/styles.css (global, unscoped)
  lib/                   modules several components or pages share (import with @/lib/...)
  api/                   optional API route handlers in .ts (bascik --server only)
dist/                    compiled output, never edited by hand, never committed
```

## Write a component

Default pattern: `<style>` above the markup, markup in the middle, a TypeScript `<script>` below. Give every element a script must control an `id` and find it with `getElementById`, and put a `data-testid` on the root and on each control (rule 16).

```html
<!-- src/components/like-button/like-button.html -->
<style>
  .like {
    padding: 0.5rem 1rem;
    border-radius: 6px;
  }
  .like.active {
    background: #d3ff8d;
  }
</style>
<button class="like" id="btn" type="button" data-testid="like-button">
  <span data-bascik-prop-label>Like</span>
</button>
<script type="text/typescript">
  const btn = document.getElementById("btn") as HTMLButtonElement;
  btn.addEventListener("click", () => btn.classList.toggle("active"));
</script>
```

```html
<!-- src/pages/index.html -->
<like-button data-bascik-prop-label="Like this post" />
<like-button data-bascik-prop-label="Like this comment" />
```

Bascik strips the types, rewrites `.like` to `.bascik__like-button__like`, gives each instance its own `id` (`bascik__like-button__<instance>__btn`), rewrites the `getElementById` string and the `classList` class to match, and wraps the script in an IIFE. For a longer script, move it to `like-button.ts` beside the template and load it with `<script src="like-button.ts"></script>`. Both buttons work independently. To see the exact output, run [`scripts/preview.mjs`](scripts/preview.mjs).

New components are picked up by the running dev server automatically; no restart is needed.

## Rules (must follow)

1. **Hyphenated, lowercase file names.** `feature-card.html` becomes `<feature-card>`. Never name a component after a native element (`header.html`, `dialog.html`): it replaces every such element on the page. Names must be unique across every component root.
2. **Per-instance targeting uses `id`.** Use `getElementById` (or `getElementsByName`) for elements a script controls. `querySelector('.cls')` returns the first instance on the page, so the other instances look broken.
3. **Order:** `<style>` above the markup, `<script>` below it.
4. **Props carry text only.** `data-bascik-prop-*` values are HTML-escaped strings. Pass markup or nested components through slots (`data-bascik-slot`).
5. **Self-close** components that take no slot content: `<site-head />`, `<site-footer />`.
6. **HTML and CSS first.** Reach for JavaScript only when HTML and CSS cannot do the job cleanly (`<details>`, `<dialog>`, `:has()`, `popover` cover a lot).
7. **Semantic HTML.** Pick the element the HTML standard defines for the job, because Bascik ships exactly the markup you write: a component's root is the semantic element itself (`<site-nav>` renders a `<nav>`, a review an `<article>`, a form a `<form>`), not a wrapper `<div>`; `<button type="button">` for actions and `<a href>` for navigation, never a clickable `<div>` or `<span>`; one `<main>` and one `<h1>` per page with no skipped heading levels; a `<label>` for every control; `alt` on every image; native `<details>`, `<dialog>`, and `popover` before ARIA or JavaScript. The checklist with spec links: `read-doc.mjs /component-best-practices#use-htmls-elements`.
8. **Runtime state in `data-` attributes.** Toggle `data-state="open"` and style `.panel[data-state="open"]`; anchor attribute selectors on a scoped class.
9. **Zero config.** Do not create `bascik.config.ts` unless a requirement differs from a default, and never put `siteUrl` in it. See the `bascik-config` skill.
10. **Never write generated files into `src/`.** Generated output goes to `dist/` (`BASCIK_OUT_DIR`) from an existing `pipeline.exec` script.
11. **Client scripts are not bundled.** Bare imports such as `import x from 'pkg'` fail in the browser. They work only in Node-side scripts (`data-bascik-build`, `data-bascik-server`). Bundle browser packages with esbuild (`read-doc.mjs /how-to/bundling-npm-packages`).
12. **Pages are lists of tags.** Shared `<head>` tags, the header, the footer, and every section with a nameable job become components (`<site-head />`, `<site-header />`, `<pricing-section />`, `<site-footer />`). Pages keep their own `<html>`, `<head>`, and `<body>`. Balance it: no tiny single-use wrappers and no props passed through components that do not use them.
13. **Script directives are exclusive.** One `<script>` tag takes at most one of `data-bascik-build`, `data-bascik-build-once`, `data-bascik-routes`, `data-bascik-server`, `data-bascik-stream`. `data-bascik-build-once` runs once per file with no page context.
14. **TypeScript by default.** New browser and Node code is TypeScript (see "TypeScript by default" above). Use JavaScript only when the person asks for it.
15. **Every script and helper builds markup with `html`.** Any build, build-once, routes, server or stream script, API route, and any `.ts` helper that returns markup (in `src/lib/` or beside a component) does `import { html } from "@bascik/bascik/html"` and returns `` html`<p>${value}</p>` ``: it escapes each value for where it lands, turns `javascript:` URLs into `about:invalid`, and throws where escaping cannot help. Use `raw()` only for markup the project wrote and trusts or sanitized CMS HTML, `json()` for JSON-LD, and `esc()` or `safeUrl()` where a string is built without `html`. Never write your own escaper (`escapeHtml`, an `&amp;` replace chain) and never interpolate data into a plain template string. Give a URL attribute one hole: build the URL in code first (`` const href = `${siteUrl}${path}` ``, then `href="${href}"`), because `html` refuses two holes before the URL's first `/` (`url-scheme-split`) so that two values cannot spell `javascript:` together. A browser script cannot import it: set `textContent` there. See the `bascik-scripts` skill.
16. **A `data-testid` on what a test needs.** Every component root gets `data-testid="<component-name>"`, and every interactive part (a button, an input, select, or textarea, a `<summary>`, a link a script handles, an element with an ARIA widget role or `tabindex="0"`) gets `data-testid="<component-name>-<part>"`. Forms, dialogs, and landmarks (`<main>`, `<nav>`, the page's `<header>` and `<footer>`) get one too. Bascik never scopes or hashes `data-testid`, so `getByTestId(...)` matches in a production build where classes and ids are hashed. Instances share their ids: a test picks one with `.filter({ hasText })`, or the page names one with `data-testid` on the usage tag, which replaces the root's. Never put request or random data in a test id, and keep existing hooks (`data-test`, `data-cy`, `data-qa`) when migrating. `scripts/new-component.mjs` adds the root's, and `scripts/verify.mjs` lists the gaps. See `read-doc.mjs /testing/e2e-testing`.
17. **Colocate what one component or page uses.** A module (data, helper, types) that one component uses lives in that component's folder, with its tests, and is imported with `./` (`import { faqs } from "./faqs.ts"`). Content lives with the component that renders it: a page that also needs it, for JSON-LD say, imports it from there (`@/components/faq-list/faqs.ts`). A module only one page uses sits beside that page as a `.ts` file (the pages folder publishes a `.json` or `.js` file as a public asset, never a `.ts` one). Only modules several components or pages share, or that config, exec scripts, or API routes also import, go in `src/lib/`. Files in component and page folders are watched already; `src/lib/` needs `pipeline.watchPaths`. `scripts/audit-components.mjs` reports a `src/lib/` module with one user (`single-use-module`).

## Slots, props, and attributes

| Need                     | Component template                                              | Usage site                                                                    |
| ------------------------ | --------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Default slot (rich HTML) | `<div data-bascik-slot>fallback</div>`                          | `<my-card><h2>Title</h2></my-card>`                                           |
| Named slot               | `<div data-bascik-slot="header"></div>`                         | `<div data-bascik-slot="header"><h1>Hi</h1></div>` inside the tag             |
| Text prop                | `<p data-bascik-prop-title></p>`                                | `<my-card data-bascik-prop-title="Hello" />`                                  |
| Prop into an attribute   | `<img data-bascik-attr-src="image" data-bascik-attr-alt="alt">` | `<my-card data-bascik-prop-image="/a.png" data-bascik-prop-alt="A" />`        |
| Forward attributes       | (nothing)                                                       | `<my-card class="wide" aria-label="Promo" />` lands on the first root element |

Pass props as `data-bascik-prop-<name>="..."` on the usage tag. A plain attribute such as `label="..."` is not a prop: it is forwarded to the root element and the prop keeps its default. A forwarded attribute the root already has keeps the root's value, except `data-testid`: the usage tag's replaces it, so a page can name one instance. The slot element itself is replaced by the content, so named-slot wrappers disappear: wrap headings and links in a `<div data-bascik-slot="x">` rather than putting the attribute on the `<h1>` or `<a>`. Details: `read-doc.mjs /slots`, `/props`, `/attribute-inheritance`.

## Script tags at a glance

| Tag                               | Runs                        | Use for                                                                |
| --------------------------------- | --------------------------- | ---------------------------------------------------------------------- |
| `<script>`                        | Browser                     | Component and page behavior (scoped, IIFE-wrapped)                     |
| `<script data-bascik-build>`      | Node, at build time         | Markup from files, Markdown, APIs; output replaces the tag             |
| `<script data-bascik-build-once>` | Node, once per file         | Markup shared by every use of a component or every route of a template |
| `<script data-bascik-routes>`     | Node, at build time         | Expanding `[slug].html` templates into many pages                      |
| `<script data-bascik-server>`     | Node, per request           | Personalized markup (needs `bascik --server` or a serverless target)   |
| `<script data-bascik-stream>`     | Node, per request, streamed | Slow per-request blocks that should not delay the page shell           |

Node-side scripts export a default function that returns an HTML string. Component tags in that HTML render, at build time and, from server and stream scripts, per request. Details are in the `bascik-scripts` skill.

## CLI

```sh
bascik                      # dev server at http://localhost:8080 with live reload and watch
bascik --build              # production build to dist/ (HTML, CSS, JS, and identifier minification on)
bascik --build --only "blog/**"   # rebuild matching pages without cleaning dist/
bascik --server             # serve a built dist/ (needed for server/stream scripts and API routes)
bascik --check              # project checks, plus the per-file checks when @bascik/language-server is installed
bascik --check --fix        # also rewrite fixable findings (needs @bascik/language-server)
bascik add <package>        # copy components from an installed npm package into src/components/
bascik init                 # add Bascik to an existing project
npx @bascik/language-server --check   # the per-file checks on their own (bascik --check already runs them)
```

`bascik --check` and the linter are not two overlapping tools. `bascik --check` answers project questions (duplicate routes, unused components, config), and the linter answers per-file questions (attribute typos, CSS that cannot be scoped). `bascik --check` runs the linter too, so use it, and reach for the linter alone only on a folder outside the project.

New project: `npm create bascik@rc my-site -y`. It and `bascik init` both write `.vscode/settings.json` with `"html.validate.scripts": false` and recommend the Bascik extension in `.vscode/extensions.json`, merging into files the folder already has. Third-party linters such as Webhint are opt-in: neither command installs them or creates or modifies their configs. A project set up any other way (a migration, or files copied in with `add-example.mjs`) needs that VS Code setting added by hand, or VS Code joins a page's `<script>` blocks into one file and reports false errors such as "A module cannot have multiple default exports". The setting turns off only VS Code's own check of inline scripts, not Bascik's checks. Production builds need a site URL for `sitemap.xml` and `robots.txt`: `BASCIK_SITE_URL=https://example.com bascik --build` (or `--site-url`, or `.env`). Full CLI and error output: `read-doc.mjs /cli`.

## Verify every change

Do not stop at "the file looks right". Run these from the project root:

1. `node <skill-dir>/scripts/verify.mjs` runs `bascik --check` (project and per-file checks) and, for component folders outside the project, the linter, then summarizes each step. Add `--build` to also run a production build.
2. `node <skill-dir>/scripts/audit-components.mjs` reports oversized pages and components, inline sections that should be components, repeated blocks and heading groups, the same fact typed into several files, props every page passes with the same value, tiny single-use components, props passed through layers, JavaScript where TypeScript is expected, a hand-written HTML escaper or code that strips `<`, `>` and `&` from a value (build the markup with `html` instead), a `src/lib/` module that only one component or page uses (move it beside that user), and a component build script that should be `data-bascik-build-once` (or a build-once script that reads the page). It also warns about semantic HTML: a clickable `<div>` or `<span>`, a component root that is a `<div>` where `<nav>`, `<header>`, `<footer>`, `<form>`, `<article>`, or `<section>` fits, a skipped heading level in a page's output, an `<img>` with no `alt`, a form control with no label, and a page with no `<main>`. Each finding has `file:line` and what to do. Pass `--allow-js` only when the person asked for JavaScript.
3. `node <skill-dir>/scripts/preview.mjs '<my-card data-bascik-prop-title="Hi" />' --count 2` compiles a snippet with the project's real components and config and prints the unminified output, so you can confirm scoped names, slot placement, and script rewrites.
4. Read the relevant file in `dist/` after a build. A hyphenated tag still present in `dist/` means no component matched it.

A page is not done until `verify.mjs` passes and `audit-components.mjs` exits 0. Fix each warning, or tell the person which one you kept and why (for example, a long legal page that is all prose). "The content differs" is not a reason to keep a repeated block: different text is what props and slots are for. Neither is "the fields belong to their form" when two forms repeat them.

`<skill-dir>` is the directory containing this file, for example `.agents/skills/bascik`.

## Editor linters read source; Bascik writes `dist/`

webhint, axe, html-validate, HTMLHint, and VS Code's HTML checker read `src/`. Bascik overrules some of what they report, because the answer is only in the built page:

- **Composed at build time:** a missing charset or viewport `<meta>` (a head component adds them), an `apple-touch-icon` link "should be specified in the `<head>`" (a head component is a fragment with no `<head>`), a missing `<title>` (a build script writes it), an `<img>` with no `alt` or `src` and an empty heading whose value comes from a `data-bascik-attr-*` or `data-bascik-prop-*` prop.
- **Bascik syntax:** self-closed component tags, component files with no doctype, and several `<script>` blocks in one file (`"html.validate.scripts": false`).

Rules:

- **Never "fix" one of these by adding the tag to a source page.** Open the built page in `dist/` first. If the tag is there, the warning is false and a second copy would ship twice; if it is missing there too, fix the head component or build script.
- **Everything else is real:** a `<button>` with no `type`, `<html>` with no `lang`, a literal `<img>` with no `alt`. The optional documented `.hintrc` turns `image-alt` off in the editor, so a literal missing `alt` shows only in `audit-components.mjs` and the built-site check: run them. The documented `src/.htmlvalidate.json` makes `<img>` `src` optional, so a literal `<img>` with no `src` shows only when html-validate checks `dist/`; never turn `element-required-attributes` off for all of `src/`, which also hides a missing `lang`.
- **Do not add third-party linter configs or dependencies by default.** If the person uses Webhint or another linter, read `/testing/linting#editor-linters-read-source` and adapt its copyable configs to the project's folders. Preserve existing settings. Keep Webhint configs as plain JSON, because its extension's quick fixes use `JSON.parse`. Keep the built-site config independent of the source config so source exceptions do not leak into `dist/`. Other linters get a `src/` config; HTMLHint's must list its default rules too, or unnamed checks are disabled.
- **The checks that decide run on built output:** `bascik --check` for Bascik syntax and WHATWG parsing, then `bascik --build`. If the person opts into Webhint, copy the documented `.hintrc.dist.json` first, then run `npx hint -c .hintrc.dist.json $(find dist -name '*.html')` (files, not the folder; use `directory.out` if it is not `dist`). Lighthouse on `bascik --server` is another built-site audit. Webhint does not check local links: run `check-links.mjs`.
- **cSpell `Unknown word` on a brand or product name is real:** add the name to the project's `cspell.json` `"words"`, not to a user setting.

Every warning, its setting, and the config files: `read-doc.mjs /testing/linting#editor-linters-read-source`.

## Bundled scripts

All scripts are dependency-free Node.js (22.22+) and run from the project root. Each prints `--help`.

| Script                                                         | Purpose                                                                                                                                                                                                                                                                                     |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`scripts/verify.mjs`](scripts/verify.mjs)                     | `bascik --check`, plus the linter on component folders outside the project, with an optional `--build`                                                                                                                                                                                      |
| [`scripts/audit-components.mjs`](scripts/audit-components.mjs) | Page and component structure (too big, inline sections, repeats, tiny wrappers, prop drilling), semantic HTML (clickable divs, wrapper roots, heading order, alt, labels, `<main>`), JS where TS is expected, hand-written escapers, single-use `src/lib/` modules, and build vs build-once |
| [`scripts/preview.mjs`](scripts/preview.mjs)                   | Compile a snippet, file, or existing page in a temporary build and print the result                                                                                                                                                                                                         |
| [`scripts/list-components.mjs`](scripts/list-components.mjs)   | Inventory components with their props, slots, companion files, and `@bascik` descriptions                                                                                                                                                                                                   |
| [`scripts/new-component.mjs`](scripts/new-component.mjs)       | Create a component folder that follows the naming and ordering rules                                                                                                                                                                                                                        |
| [`scripts/search-docs.mjs`](scripts/search-docs.mjs)           | Search the live docs at bascik.dev for a topic                                                                                                                                                                                                                                              |
| [`scripts/read-doc.mjs`](scripts/read-doc.mjs)                 | Print the current text of a docs page, such as `/scoped-javascript`                                                                                                                                                                                                                         |
| [`scripts/add-example.mjs`](scripts/add-example.mjs)           | Copy a tested example component or part of the starter site from bascik.dev into the project (`--list` shows them)                                                                                                                                                                          |
| [`scripts/check-links.mjs`](scripts/check-links.mjs)           | Find broken internal links, missing assets, and dead `#fragments` in the built `dist/`, honoring `base`                                                                                                                                                                                     |

Run `list-components.mjs` before creating a component so you reuse what exists instead of duplicating it.

## Look it up in the docs

The docs at https://bascik.dev are the reference; this skill only holds the rules. Read the page for any task below before writing code, instead of guessing:

```sh
node <skill-dir>/scripts/read-doc.mjs /scripts/dynamic-routes
node <skill-dir>/scripts/search-docs.mjs "dynamic routes trailing slash"
```

| How do I...                                           | Read                                                          |
| ----------------------------------------------------- | ------------------------------------------------------------- |
| Write components, slots, props, attributes            | `/components`, `/slots`, `/props`, `/attribute-inheritance`   |
| Pick semantic elements, landmarks, headings, labels   | `/component-best-practices#use-htmls-elements`                |
| Pass shared `<head>` tags                             | `/how-to/templating`                                          |
| Use a library (petite-vue, Alpine.js, HTMX, Tailwind) | `/libraries`                                                  |
| Use a third-party web component                       | `/how-to/third-party-web-components`                          |
| Share components between projects                     | `/how-to/sharing-components`, `/how-to/publishing-components` |
| Find answers to edge cases, fix a known problem       | `/faq`, `/testing/troubleshooting`                            |
| Use the CLI and the dev server                        | `/cli`, `/development-server`                                 |

The full page index is at https://bascik.dev/llms.txt.

## Start from an example

https://bascik.dev/example-components has tested components (tabs, dialog, popover menu, copy button, filter list, contact form, theme toggle). `add-example.mjs` also offers `starter-site`, a complete site (layout components, SEO helper, Markdown blog, feed, `llms.txt`, contact page) whose README is at https://github.com/bascikdev/bascik/tree/main/examples/starter-site. Copy instead of writing from scratch, then adapt:

```sh
node <skill-dir>/scripts/add-example.mjs --list
node <skill-dir>/scripts/add-example.mjs tab-group
node <skill-dir>/scripts/add-example.mjs starter-site/src/lib/seo.ts
```

The script downloads from bascik.dev, maps files to the project's configured folders, also copies example components a file uses, and writes nothing if any file would overwrite a different one. It prints `bascik.config.ts` and `package.json` instead of copying them.

## Build a new site

1. `npm create bascik@rc my-site -y`, or read the existing project first with `list-components.mjs`. Add `BASCIK_SITE_URL=https://example.com` to `.env`.
2. Plan the pages and URLs (one purpose and one `<h1>` each), then the components each page is made of: the shared layout (head, header, footer), one component per section with a job, and one per repeated block. Plan repeated content (a collection in `content/`) and anything that needs a server (API routes, per-request markup). Ask when the plan is unclear.
3. Copy the foundation: `add-example.mjs starter-site`, or only the parts you need. Then replace the example name, navigation (`src/components/site-header/links.ts`), colors (tokens in `src/pages/css/styles.css`), and every page's `seo({ title, description })`.
4. Add components (`new-component.mjs --script inline` or `--script ts`), then pages as lists of their tags, and interactive examples. Load the companion skill for each area.
5. Before launch: `npx bascik --build`, then `verify.mjs`, `audit-components.mjs`, `check-links.mjs`, the `bascik-seo` audit, and the `bascik-components` token check. The starter site README's "Build and Check It" section has the manual checklist.

## Companion skills

| Skill                  | Load it when                                                                                                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `bascik-components`    | Deciding what becomes a component, writing component CSS or TypeScript, interactivity, theming, scoped names, optimizing images with local tools and native srcset |
| `bascik-compatibility` | Deciding whether an HTML, CSS, or JavaScript feature works in browsers and inside a component                                                                      |
| `bascik-scripts`       | Using `data-bascik-build`, `-routes`, `-server`, `-stream`, API routes, Markdown, or a blog                                                                        |
| `bascik-seo`           | Titles, descriptions, canonical URLs, social cards, JSON-LD, sitemap, `llms.txt`                                                                                   |
| `bascik-config`        | Creating or editing `bascik.config.ts`, monorepos, deploying, or running `bascik --server`                                                                         |
| `bascik-testing`       | Writing tests, debugging, validating output, or tuning Lighthouse scores                                                                                           |
| `bascik-migrate`       | Moving a site from React, Next.js, Vue, Svelte, Astro, Eleventy, Hugo, or WordPress                                                                                |
| `bascik-refactor`      | Opt-in: having coding agents refactor a live site to production parity and 100 in all five Lighthouse categories                                                   |

New projects do not include `bascik-refactor`. Install it with `npx skills add bascikdev/bascik --skill bascik-refactor`.

If the companions or this skill's `scripts/` folder are missing, the skill was installed as a single file. Reinstall the full set:

```sh
npx skills add bascikdev/bascik
# or, without npx skills:
mkdir -p .agents/skills && curl -fsSL https://bascik.dev/assets/skills.tar.gz | tar -xz -C .agents/skills
```
