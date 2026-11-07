---
name: bascik-scripts
description: Node.js scripts inside Bascik pages and components. Use when writing <script data-bascik-build> (build-time HTML from files, Markdown, JSON, or APIs), <script data-bascik-build-once> (identical HTML shared by every use), <script data-bascik-routes> with [slug].html dynamic routes, <script data-bascik-server> or <script data-bascik-stream> for per-request rendering, early-paint footers or CSS source-order streaming layouts, API routes in src/api/, @/ import aliases, BASCIK_* environment variables, the build script cache, escaping untrusted output, or a blog or other Markdown collection with front matter, tags, drafts, and a feed. Includes a new-post script.
license: MIT
metadata:
  author: bascik
  homepage: https://bascik.dev
---

# Bascik Scripts

Bascik runs Node.js code inside special `<script>` tags. Each is a standard ESM module whose default export returns an HTML string that replaces the tag. Requires the `bascik` skill for project basics.

## Pick the right tag

| Need                                                                                      | Tag                                              | Runs                                                             |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------ | ---------------------------------------------------------------- |
| HTML that depends on the page or route (BASCIK_PAGE_PATH, BASCIK_PAGE_FILE, BASCIK_ROUTE) | `data-bascik-build`                              | Build and dev, once per use (cached by inputs)                   |
| Identical HTML shared by every use of a component or every route                          | `data-bascik-build-once`                         | Once per file (component registration or route template), cached |
| Many pages from one `[param].html` template                                               | `data-bascik-routes`                             | Build and dev startup                                            |
| Markup that depends on the request (cookies, headers, query)                              | `data-bascik-server`                             | Every request, before the response starts                        |
| A slow per-request block that should not delay the page shell                             | `data-bascik-stream`                             | Every request, streamed in document order                        |
| A JSON or HTTP endpoint                                                                   | `src/api/<name>.ts` exporting `GET`, `POST`, ... | Every request                                                    |

Prefer build-time work. Server, stream, and API code needs `bascik --server` (or a serverless target such as Cloudflare or Netlify); a plain static host cannot run it.

## Rules for every Node-side script

1. **Export a default function that returns markup:** a string or an `html` value. A server or stream script may also return an array of them, joined with no separator (``return items.map((p) => html`...`)``). Never return data, a `Response` (that is an API route), a caught `Error` (throw it) or an async `.map` (use `await Promise.all(...)`): a server or stream script that does is refused, a located error in dev and an empty slot with one warning in production (`read-doc.mjs /scripts/server`). `console.log()` output goes to the terminal only; it never becomes markup.
2. **One directive per tag.** Combining `data-bascik-build`, `data-bascik-build-once`, `-routes`, `-server`, or `-stream` is a hard error.
3. **Imports, and where modules live:** top-level `import` and `await` work. A module (data, helper, types) one component uses lives in that component's folder with its tests and is imported with `./` (`import { faqs } from "./faqs.ts"`), which resolves against the file containing the script, inline or `src=`. A module one page uses sits beside the page as a `.ts` file (the pages folder publishes `.json` and `.js` files). Content lives with the component that renders it: a page that also needs it (JSON-LD) imports `@/components/faq-list/faqs.ts`. Only modules several components or pages share, or that config, exec scripts, or API routes import, go in `src/lib/`, imported with `@/` (`import { renderMd } from '@/lib/md.ts'`, resolved against `scripts.importRoot`, default `src`, from any depth). `audit-components.mjs` in the `bascik` skill reports a `src/lib/` module with one user. Bare npm packages work.
4. **Never import with a bare leading `/`.** `import x from '/lib/x.ts'` and `src="/lib/x.ts"` are hard errors. Use `@/lib/x.ts` or `./lib/x.ts`. A `data-bascik-*` tag with `src=` has an empty body: a tag with both is rejected, and a `src=` file that cannot be read is the reported error.
5. **Helpers import helpers with relative paths.** `@/` is rewritten only inside script tags; a `.ts` helper that imports another helper uses `./other.ts` (with the extension) and `import type` for type-only imports. tsconfig `paths` do not apply.
6. **Data paths are relative to the project root.** `readFile('./content/post.md')` resolves from `process.cwd()`, not from the page.
7. **Watch helpers.** Add `src/lib/` and data folders such as `content/` to `pipeline.watchPaths` so edits rebuild dependent pages in dev. Modules in a component's folder or beside a page need no entry: those folders are watched already, and an edit rebuilds every page whose scripts import the module.
8. **Build all markup with `html` from `@bascik/bascik/html`.** This covers every build, build-once, routes, server and stream script, API route, and every `.ts` helper that returns markup (`src/lib/` or a component's companion). Plain template strings do not escape, and a hand-written escaper (`escapeHtml`, a `.replace(/&/g, "&amp;")` chain, an entity map) misses URLs and script contexts: never write one, and replace one you find with `html`. A feed or sitemap is XML, not HTML: build it as a string and escape each value with `esc()`. `html` escapes each value for where it lands (text, quoted attribute, URL) and throws on places escaping cannot make safe (`on*`, `<script>`, `style`, unquoted attributes). Nest `html` values and arrays of them (`.map` with no `.join`). Use `raw(value)` only for HTML a sanitizer with an allowlist (for example `sanitize-html`) already cleaned, `json(value)` for `<script type="application/json">`, and `safeUrl(value, { origins })` when a script or stylesheet URL comes from data. Build scripts return `html` values like server scripts do. An `html` value is an object, not a string: `String(output)` in tests of a helper, `serverScriptOutput(output).text` from `@bascik/bascik/runtime` for a handler's whole return (an array included), `SafeHtml` as a helper's return type. Never `.join("")` fragments (the joined string is escaped and shows `&lt;li&gt;`). One hole per URL attribute: build the URL in code first (`` const href = `${siteUrl}${path}` ``, then `href="${href}"`). `html` throws `url-scheme-split` on two holes before the URL's first `/`, `?` or `#`, because together two values could spell a scheme such as `javascript:`; a hole after a written `/` (`href="/blog/${slug}"`) is fine. A hole cannot add an attribute: for `selected`, `checked` or `disabled`, write the tag twice and choose in code (`checked="${false}"` is still checked). An `html` error shows a plain 500 in the browser; the located message is in the terminal. Details: `read-doc.mjs /scripts/security`, `/html-helpers`.
9. **TypeScript by default.** Helpers and data modules (in a component's folder, beside a page, or in `src/lib/`), API routes (`src/api/*.ts`), `pipeline.exec` scripts (`scripts/*.ts`), and `bascik.config.ts` are TypeScript; Node strips their types, so there is no build step. Keep to erasable syntax (no `enum`, namespaces with code, or parameter properties), or pass Node flags such as `--experimental-transform-types` through `NODE_OPTIONS`. A `data-bascik-*` script is TypeScript when its `src=` names a `.ts` file (`<script data-bascik-build src="./nav.ts">`) or its tag is marked `type="text/typescript"`; Bascik strips its types before it runs, on Node and in the Cloudflare Worker, and errors keep the source's lines; a syntax error or `enum` fails `bascik --build` (and the page in dev) with file:line:column, never only at request time. An unmarked block is JavaScript, so mark it. Keep each block to a few lines that import typed helpers. Helpers import each other with the `.ts` extension. Use JavaScript only when the person asks for it; when refactoring TypeScript, keep the types. Browser TypeScript and esbuild: the `bascik` skill, and `read-doc.mjs /scoped-javascript`, `/configuration`, `/how-to/bundling-npm-packages`.
10. **Directives in output never run.** If a build script prints another `data-bascik-*` script, it is removed with a warning; in server and stream output it is sent as written and never runs on the server. Printed component tags do expand, in build, server, and stream output.

## Build scripts

```ts
// src/lib/markdown.ts
import { readFile } from "node:fs/promises";
import { html, raw, type SafeHtml } from "@bascik/bascik/html";
import { marked } from "marked";

/** Your own Markdown is trusted, so raw() inserts the rendered HTML as it is. */
export async function renderMarkdown(path: string): Promise<SafeHtml> {
  const md = await readFile(path, "utf8");
  return raw(marked.parse(md, { async: false }) as string);
}

/** A card from data: html escapes each value for where it lands. */
export const postCard = (post: { slug: string; title: string }): SafeHtml =>
  html`<a href="/blog/${post.slug}/">${post.title}</a>`;
```

```html
<!-- src/pages/about.html: the path stays in the script, where the cache can see it. -->
<script data-bascik-build>
  import { renderMarkdown } from "@/lib/markdown.ts";
  export default () => renderMarkdown("./content/intro.md");
</script>
```

- Runs before component resolution, so the returned HTML may contain component tags and is scoped like the surrounding template.
- Each uncached script runs in its own child process (about 50 to 150 ms). Output is cached on disk in `node_modules/.cache/bascik/script-cache/`.
- **Cache gotcha:** the cache key covers the script (and whether it runs as TypeScript), its statically referenced local files, installed package versions, the page path, site URL, base, and whether it is a dev or build run (so the first run in a mode with no cache entries re-runs every script). It cannot see network responses, `readdir` results, or computed paths. Exclude scripts that read remote or directory data with `scripts.cache.exclude`, and declare environment variables a script reads in `scripts.cache.environment`.
- **Fetch once:** read data once per page in one script, then feed it to the parts that need it, instead of fetching per component instance.
- **Component context:** `data-bascik-build` runs for each use with that page's context. Use `data-bascik-build-once` for identical output with no page or route context: in a component every use shares one run, and in a dynamic route template every route shares one run. Its output is cached like any build script. Use a build-wide `pre` exec script when work should be shared across different files.
- Errors follow `scripts.onBuildScriptError` (`'error'` by default): dev shows the error on that page and keeps serving; `--build` fails.

Per-page values come from environment variables: `BASCIK_PAGE_PATH` (`/about`), `BASCIK_PAGE_FILE`, `BASCIK_SOURCE_FILE`, `BASCIK_PAGES_DIR`, `BASCIK_BUILD` (`"1"` in `--build`), `BASCIK_SITE_URL` (absent when unset), `BASCIK_BASE`, and `BASCIK_ROUTE` (dynamic routes). Details: `read-doc.mjs /scripts/build`, `/environment-variables`, `/how-to/page-aware-scripts`.

Server and stream scripts read the server's own `process.env` (`.env` values, secrets, `BASCIK_SERVER`, `BASCIK_SITE_URL`) and get no page variables: read the page from `request.url`. On Cloudflare Workers, read secrets and bindings from `context.platform.env`. Never print a secret from a build script; it ships in the page. Details: `read-doc.mjs /scripts#environment-variables`.

## Dynamic routes

```html
<!-- src/pages/blog/[slug].html -->
<script data-bascik-routes>
  import { listPosts } from "@/lib/posts.ts";
  export default async function () {
    const posts = await listPosts();
    return posts.map((post) => ({ params: { slug: post.slug }, data: post }));
  }
</script>
<script data-bascik-build>
  import { html } from "@bascik/bascik/html";
  export default function () {
    const { data } = JSON.parse(process.env.BASCIK_ROUTE || "{}");
    return html`<h1>${data.title}</h1>`;
  }
</script>
```

Every bracket name needs a matching `params` key; a param cannot contain `/` (use one template per depth). Use `src/pages/blog/[slug]/index.html` for trailing-slash URLs. Never generate page files into `src/pages/`. Details: `read-doc.mjs /scripts/dynamic-routes`.

## Server and stream scripts

```html
<script data-bascik-server>
  import { html } from "@bascik/bascik/html";
  export default function (request, context, { signal }) {
    const name = request.headers.get("x-display-name") ?? "Guest";
    return html`<p>Welcome, ${name}!</p>`;
  }
</script>
```

- `request` is a standard WHATWG `Request`; `context` is `{ remoteIp }`; `signal` aborts on timeout or disconnect.
- All `server` scripts resolve before any byte is sent. Swap to `data-bascik-stream` when the shell should paint first; a stream failure renders an empty slot instead of a 500.
- Source is moved to `.bascik/dist/server-scripts.json`; static `dist/` keeps an inert placeholder. They never run during `--build`.
- Never block the event loop with synchronous work; timeouts cannot interrupt it.

### Optional early-paint layout

- **Default to logical source order.** Bascik flushes static markup only up to the first stream tag; static content after a slow stream waits too, even when later jobs finish first.
- **Consider the early-paint footer technique** when independent help, a sidebar, footer, or other shell content should arrive before slow streamed content but appear below it. Put that markup before the first stream tag, then use Flexbox `order` or Grid areas on their shared layout container to restore visual placement. This needs no client relocation or Bascik runtime; all `server` scripts still finish before the initial flush.
- **Use only when the reordered source still makes sense for reading and keyboard navigation.** CSS does not change screen-reader or tab order. Keep logical source order for sequential forms, instructions, or controls whose order matters. Reserve space for expected streamed output when layout stability matters; reordering alone does not prevent layout shift.
- Early HTML is not necessarily interactive: deferred/module scripts can still wait for parsing to finish. Keep authentication/authorization gates before streaming and do not move protected markup into an unconditional shell.
- Verify with a deliberately stalled stream that the intended shell bytes arrive first, then check visual placement on desktop/mobile with JavaScript disabled, keyboard order, and success/empty/error results.

Recipe and examples: `read-doc.mjs /scripts/stream#recipe-c-priority-source-order-with-css-positioning-the-early-paint-footer-trick`, especially `/scripts/stream#option-3-flexbox-column-order` (the homepage and Cloudflare adapter demo use this pattern).

### Server and stream scripts may return component tags

```html
<script data-bascik-server>
  import { html } from "@bascik/bascik/html";
  import { searchBooks } from "@/lib/books.ts";
  export default async function (request) {
    const q = new URL(request.url).searchParams.get("q") ?? "";
    const books = await searchBooks(q);
    return html`${books.map(
      (b) => html`<book-card data-bascik-prop-title="${b.title}"></book-card>`,
    )}`;
  }
</script>
```

- Each returned tag renders per request with the component's markup, props, slots, and scoped CSS, as at build time. No import, attribute, or config.
- **Output is HTML with the same power as your markup.** Build it with `html` so every value in a prop or slot is escaped; sanitize HTML from a CMS or an API, then insert it with `raw()`.
- Bound URLs (`data-bascik-attr-href` and the like) lose script URLs such as `javascript:` and non-image `data:` URLs (`about:invalid`); any http(s) URL, third-party included, is kept, so restrict script and stylesheet URLs from data with CSP or `safeUrl(value, { origins })`.
- Scripts inside a returned component run once per instance with the same request and the parent's remaining `scripts.timeout`, and get no props from the usage tag. A nested `stream` script resolves with its parent.
- Budgets (defaults; change them with `scripts.renderLimits`): 1000 component instances and 4 MiB of rendered HTML per script output; 64 nested component scripts per response, 4 levels deep. Over budget, or when an instance fails to render (`failed during <stage>`), `onServerScriptError` decides as for a throw: `'error'` is a 500 for a server script and a logged empty slot for a stream script; `'warn'` logs it and gives an empty slot; `'ignore'` gives an empty slot without a log.
- The component's CSS is a `<style>` in the body before the first instance in document order, once per response (once more if the page uses the component in its own markup). Unscoped `body`/`*` rules in it restyle the page.
- Component client scripts stay inside the rendered instance (end of the outermost one with `minify.html`), never at the end of the document.
- With a non-root `base`, URLs inside rendered components are rewritten; the rest of the output is sent as written.
- Tags in `components.external` with no component file, misspelled tags, and escaped tags are sent as written. The dev server logs typos and unsupported components once per route (when any component is renderable); `bascik --check` cannot see typos.
- **Unsupported, left unexpanded** (listed by `bascik --check` after a build): `attr-binding-to-scoped-attribute` (a `data-bascik-attr-*` binding onto `id`, `class`, `style`, an SVG reference attribute, or `name`/`usemap` when `scoping.attributes.name` is on; bind a `data-*` attribute instead), `instance-scoped-server-script` (the component's server or stream script names its scoped ids or field names, or the component has such a script and its stylesheet uses `url(#id)` or `scoping.deduplicateCss: false`; a `url(#id)` component with no script renders, with one style block per instance), `build-script-reads-page-context` (a `data-bascik-build` script reads `BASCIK_PAGE_PATH`, `BASCIK_PAGE_FILE`, or `BASCIK_ROUTE`; use `data-bascik-build-once`), `attr-src-on-directive-script`, and `scoping-template-unavailable` (the `--check` detail says why).
- With `generate.cspHashes`, server and stream routes list every renderable component's hashes, except components with per-instance CSS or client scripts that use scoped ids.

Details: `read-doc.mjs /scripts` (Returning component tags), `/compatibility` (Request-Time Component Rendering).

## API routes

```ts
// src/api/contact.ts  ->  POST /api/contact
export const POST = async (request: Request): Promise<Response> => {
  const data = await request.json();
  if (!data.name)
    return Response.json({ error: "name is required" }, { status: 400 });
  return Response.json({ ok: true }, { status: 201 });
};
```

Every script file in `src/api/` is a route except `*.d.ts` and tests beside a route (`*.test.ts`, `*.spec.ts`), so keep shared helpers in `src/lib/` and import them as `@/lib/<name>.ts`. Unexported methods, and any method other than `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS` and `HEAD` (an exported `PURGE` is never called), return 405 with an `Allow` header; `HEAD` derives from `GET`; `OPTIONS` is automatic. Handlers receive `(request, { params, remoteIp, platform }, { signal })`. Details: `read-doc.mjs /api-routes`, `/scripts/server`, `/scripts/stream`. A handler that accepts both JSON and a no-JavaScript form post: `add-example.mjs starter-site/src/api/contact.ts`.

## Blogs and Markdown collections

There is no content API. A collection is a folder such as `content/posts/`, one helper that reads, validates, and sorts it, and pages that call the helper. The helper goes in `src/lib/` when several pages, or a page and the feed, call it (a blog's index, post, and tag pages do); a collection only one component lists keeps its helper in that component's folder. Copy a working blog instead of writing one: `add-example.mjs starter-site/src/lib/posts.ts starter-site/src/pages/blog starter-site/scripts/feed.ts`, then merge the starter's `bascik.config.ts` settings.

1. **One reader.** Every page, the feed, and a home page "latest posts" list call the same helper.
2. **Fail loudly.** Validate front matter in the helper and throw with the file name, so a bad post fails `bascik --build`.
3. **Exclude every page that lists the folder from the cache** (`scripts.cache.exclude`), because the cache cannot see `readdir`; otherwise new posts do not appear. Add `content/` and `src/lib/` to `pipeline.watchPaths`.
4. **Dates stay `YYYY-MM-DD` strings** in route data, formatted with `timeZone: 'UTC'`.
5. **Drafts** are skipped when `process.env.BASCIK_BUILD === '1'`.
6. **Print front matter values with `html`; sanitize Markdown from a CMS or users before `raw()`.** Your own repository's Markdown is trusted, so `raw(post.html)` inserts it. The starter's `posts.ts` and blog pages show the pattern.
7. **Style rendered Markdown from a global stylesheet** (`.prose h2`). In a component, element selectors never match generated or slotted HTML.
8. **Feeds and other files are `post` exec scripts** that write to `BASCIK_OUT_DIR` and need `BASCIK_SITE_URL` for absolute URLs.

```sh
node <skills-dir>/bascik-scripts/scripts/new-post.mjs "Launching the new site" --tags news,release --description "What changed and why."
```

Details: `read-doc.mjs /how-to/markdown`, and the working blog in `add-example.mjs starter-site/src/pages/blog`.

## Look it up

| How do I...                                                | Read                                                |
| ---------------------------------------------------------- | --------------------------------------------------- |
| Choose between build, routes, server, and stream scripts   | `/scripts`                                          |
| Import helpers, use `@/`, or load TypeScript               | `/scripts/imports`                                  |
| Read the page's own path or source, set per-page head tags | `/how-to/page-aware-scripts`                        |
| Render Markdown, front matter, a collection                | `/how-to/markdown`                                  |
| Bundle npm packages for the browser                        | `/how-to/bundling-npm-packages`                     |
| Run scripts before or after the build                      | `/exec-scripts`                                     |
| Rebuild on changes outside pages and components            | `/watch-paths`                                      |
| Test build and server scripts                              | `/testing/build-scripts`, `/testing/server-scripts` |

`node <skills-dir>/bascik/scripts/read-doc.mjs <path>` prints any of these; `search-docs.mjs "server script timeout"` searches them.
