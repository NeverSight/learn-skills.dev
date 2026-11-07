---
name: bascik-config
description: Configure, build, and deploy Bascik sites. Use when deciding whether a bascik.config.ts is needed, editing one (directory, components.external, scoping, minify, assets, generate, pipeline.exec, pipeline.watchPaths, scripts, http, base), setting BASCIK_SITE_URL, deploying to a static host, running bascik --server in production, building a Cloudflare or Netlify bundle with --target, placing static assets, 404, and 500 pages, or structuring a monorepo with several sites, shared components, workspaces, and CI. Includes an audit script that flags redundant or invalid config and a workspace checker for multi-site repositories.
license: MIT
metadata:
  author: bascik
  homepage: https://bascik.dev
---

# Bascik Configuration and Deployment

Bascik is zero-config. Most sites never need `bascik.config.ts`. Requires the `bascik` skill for project basics.

## Decide whether a config is needed

Create `bascik.config.ts` only after naming a concrete requirement that differs from a built-in default. Examples that justify one:

- `components.external` for third-party custom elements
- `pipeline.exec` for an existing lifecycle script (Tailwind, esbuild bundle, feed, search index)
- `pipeline.watchPaths` for helpers or content outside pages and components
- `base` for a subdirectory deployment
- `scoping.attributes.class: false` for Tailwind
- `generate.sitemapLastmod`, `generate.cspHashes`, or a custom `minify.js`
- `contentSecurityPolicy` to send a Content-Security-Policy header (see below)

If every value would equal a default, do not create the file. If one exists, keep only the non-default values. Run the audit after every edit:

```sh
node <skill-dir>/scripts/audit-config.mjs
```

It reports values that restate defaults, `siteUrl` in config, exec scripts that do not exist, `cwd` folders that do not exist outside the output directory (a warning), watched output paths, `minify` values in the default export that silently change production builds, and `build.pipeline.exec` lists that drop default scripts. Exit code 1 means an error; `--strict` also fails on redundant values.

## Shape

```ts
// bascik.config.ts (minimal example)
import { defineConfig } from "@bascik/bascik/config";

export default defineConfig({
  generate: { sitemapLastmod: true },
});

// Optional per-mode overrides, deep-merged over the default export:
export const dev = defineConfig({/* dev server only */});
export const build = defineConfig({/* bascik --build only */});
export const server = defineConfig({/* bascik --server only */});
```

- Bascik loads the first of `bascik.config.js`, `bascik.config.mjs`, and `bascik.config.ts` it finds, so a leftover `.js` wins over `.ts`. `--config <path>` selects a file explicitly.
- `"type": "module"` must be in `package.json`.
- The config is validated at startup: unknown keys fail with a "did you mean" suggestion, and referenced paths must exist. All problems are reported together.
- Objects deep-merge across `default` and the mode export. **Arrays replace.** Defining `build.pipeline.exec` replaces the whole default `exec` list, so include every script that should run in production.
- Config changes need a dev server restart.

## Built-in mode defaults

`bascik --build` and `bascik --server` already turn on `minify.html`, `minify.css`, `minify.js`, and `minify.identifiers`, and treat script and minify errors as fatal. Never write an all-`true` `minify` block. Dev defaults leave minification off.

Merge order is: built-in defaults, then the mode's defaults, then your `default` export, then your mode export. A value in the `default` export therefore applies to production too: `minify: { identifiers: false }` there keeps production names readable, which is rarely what you want. Put dev-only settings in `export const dev`.

## Rules (must follow)

1. **Never put `siteUrl` in config.** It is an error. Provide it per deployment: `--site-url` flag, then `BASCIK_SITE_URL`, then `.env` (loaded automatically; `--env-file <path>` is repeatable). Sitemap and robots generation (on by default) fail the build without it.
2. **Do not restate defaults** such as `directory.pages: 'src/pages'`, `scoping.deduplicateCss: true`, `scoping.scriptBlocks: true`, empty `pipeline.exec` or `pipeline.watchPaths`, or `base: '/'`.
3. **Do not invent `pipeline.exec` scripts.** Reference only script files that exist in the project. A relative `script` is a project-root path even when the entry sets `cwd` (the directory it starts in). `timeout` (60 s) applies to `parallel` entries too: a watcher such as `tailwindcss --watch` needs `timeout: 0` and belongs only in a dev-mode export, since a build waits for every `parallel` script. Details: `read-doc.mjs /exec-scripts`.
4. **Exec scripts write to `BASCIK_OUT_DIR` only.** Never into `src/` or any watched path, and never list generated output in `pipeline.watchPaths` or an exec entry's `watch`. There is no `outputs` option.
5. **Use `phase: 'pre'`** for output that pages depend on (bundles, copied vendor modules); `'parallel'` for independent artifacts (search index); `'post'` for steps that read or edit the compiled `dist/` (feeds, sitemap post-processing).
6. **`base` is a literal path prefix** such as `'/docs/'`: no full URL, query, fragment, percent escapes, backslashes, or dot segments. Bascik rewrites root-relative URLs in HTML, CSS, and web manifests, but not URLs built in JavaScript; expose `BASCIK_BASE` from a build script for those.
7. **Keep scoping defaults** (`deduplicateCss`, `scriptBlocks`, `inheritAttributes`) unless a specific integration requires a change, and do not write them out just to keep them.
8. **`directory.out` is a folder of its own**, such as `dist` or `build`. It is emptied at the start of every build and dev session, so a value that is the project root, holds `src/` or another source folder, or sits inside the pages, components, or API folder is a config error.

## Exec scripts

```ts
// bascik.config.ts (illustrative: these script files must already exist)
import { defineConfig } from "@bascik/bascik/config";

export default defineConfig({
  pipeline: {
    watchPaths: ["src/lib/", "content/"],
    exec: [
      {
        script: "scripts/bundle-vendor.ts",
        phase: "pre",
        watch: ["scripts/vendor-entry.ts"],
      },
      {
        script: "scripts/search-index.ts",
        phase: "parallel",
        watch: ["content/"],
      },
    ],
  },
});
```

- Exec scripts receive `BASCIK_BUILD`, `BASCIK_PAGES_DIR`, `BASCIK_OUT_DIR`, `BASCIK_BASE`, and `BASCIK_SITE_URL`.
- `watch` reruns the matching script after a source edit in dev; exec-only inputs need no duplicate `pipeline.watchPaths` entry. List every input the script reads, including local modules it imports: `pipeline.watchPaths` never reruns a script.
- `pipeline.onExecError`: `'warn'` (dev default) reports and continues; `'error'` (`--build` default) stops with exit 1.
- Full semantics (cycle ordering, retries, reload behavior): `read-doc.mjs /exec-scripts`.

## Monorepos and shared components

`directory.pages`, `directory.components`, and `scripts.importRoot` are independent. `directory.components` accepts an array, and roots may live outside the project:

```ts
// sites/marketing/bascik.config.ts (illustrative paths)
export default defineConfig({
  directory: { components: ["src/components", "../../shared/components"] },
  pipeline: { watchPaths: ["../../shared/scripts/"] },
});
```

1. **One site, one project:** each site has its own config, `src/pages/`, `.env`, and `dist/`. Run Bascik from the site folder.
2. **Tag names are unique across all of a site's roots.** Roots never nest or repeat, including through symlinks.
3. **List the site's own folder first.** `bascik add` and `add-example.mjs` write into the first root.
4. **Shared components import shared helpers with relative paths** (`../../scripts/links.ts`) unless every site points `scripts.importRoot` at the same folder. `@/` resolves against the consuming site, and a broken import fails that site's build: a `data-bascik-build-once` script fails it even when no page uses the component, and a `data-bascik-build` script fails it on the first page that does.
5. **Watch shared helper and style folders** with `pipeline.watchPaths`; only component roots are watched automatically.
6. **Share tokens as a stylesheet:** `assets: { inlineStyles: ['../../shared/styles/tokens.css'] }`.
7. **One Bascik version** for every site. Task runners (Turborepo, Nx) must list `shared/**` as a build input and `BASCIK_SITE_URL` as an env input.

Check the whole repository from its root, then each site (`verify.mjs` also lints component roots outside the site):

```sh
node <skill-dir>/scripts/check-workspace.mjs
```

It lists every site with its component roots, import root, base, and Bascik version, and reports duplicate tags, nested roots, `@/` imports in shared components that do not resolve for some site, unwatched external helpers, and version drift. Exit code 1 on errors. Details: `read-doc.mjs /how-to/monorepos`.

## Assets and error pages

- Everything public lives under `directory.pages` (images, fonts, downloads, standalone CSS and JS) and is copied to `dist/` with the same structure. CSS and JS there are minified by `--build` automatically.
- Never copied: dotfiles and dot-directories (unless `security.hideDotfiles: false`), `node_modules`, `.html` (compiled instead), `.ts`, `.mjs`, `.cjs`, `.mts`, `.cts`, `.map`, `.md`, test and spec files, and inlined stylesheets. `assets.exclude` adds globs relative to `directory.pages`.
- Exception: `src/pages/.well-known/` (top level only) is published to `/.well-known/` for RFC 8615 files such as `security.txt` or `assetlinks.json`. Dotfiles inside it stay private, the deny-list still applies to its files, and files need an extension to be served as assets.
- `src/pages/404.html` becomes `dist/404.html`, which static hosts and both Bascik servers serve for unknown paths.
- `src/pages/500.html` is used only by `bascik --server`. Do not port a 500 page into a static site.
- To exclude a redirect-only page from `sitemap.xml`: `<meta name="bascik-sitemap" content="exclude">`. An authored `src/pages/robots.txt` or `sitemap.xml` takes precedence (with a warning) over generation; turn the matching `generate` flag off when you keep one deliberately.

## Content-Security-Policy (opt in)

Bascik sends no CSP by default. `contentSecurityPolicy` makes every HTML response carry one, built from the directives you list plus each route's inline script and style hashes from the build (it turns on `generate.cspHashes`). The dev server and `bascik --server` send it as a header; on Cloudflare the Worker sends it for the pages it renders and the build writes `public/_headers` rules for static pages. A static `404.html` then has its policy at `/404` only, not on a 404 for another URL (`_headers` cannot match a status; the build warns); `assets.run_worker_first: true` in the Wrangler config makes the Worker send it on every 404.

```ts
export default defineConfig({
  contentSecurityPolicy: {
    directives: {
      "default-src": ["'self'"],
      "script-src": ["'self'", "https://cdn.example.com"],
      "img-src": ["'self'", "data:"],
    },
    // hashes: true (default) appends each route's hashes to script-src and style-src.
    // reportOnly: true sends Content-Security-Policy-Report-Only while you try a policy.
  },
});
```

Quote keywords (`'self'`, `'none'`); the validator names a misspelled directive with a did-you-mean and warns about `'unsafe-inline'` next to hashes and `*` or `https:` in `script-src`. Details: `read-doc.mjs /how-to/content-security-policy`.

## Security settings

Bascik changes the author's output only to protect it, and each change has a switch in one `security` object. The default rule: a protection is on by default when it cannot break a correct site and needs no setup; it is off by default when the right setting depends on the site and needs setup (`contentSecurityPolicy`, `http.trustProxy`, `generate.cspHashes`). All seven keys default to `true`; there is no master switch (`security: false` is an error).

| Key                     | On (default)                                                                                                                       |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `blockScriptUrls`       | Script URLs such as `javascript:` in bound URL attributes and inherited `<object data>` become `about:invalid`                     |
| `blockCodeBindings`     | Props are never bound to `on*`, `srcdoc`, `<meta http-equiv>`, SVG animation targets, unsafe `style`, or `<script>`/`<style>` text |
| `headers`               | Five security headers; `{ "x-frame-options": "DENY" }` changes one, `false` as a value removes one                                 |
| `hsts`                  | `max-age=31536000` over HTTPS; `{ maxAge, includeSubDomains, preload }`                                                            |
| `privateDynamicPages`   | `cache-control: private, no-store` on pages with server or stream scripts                                                          |
| `stripDirectiveScripts` | Directive scripts printed by build scripts are removed                                                                             |
| `hideDotfiles`          | Dot paths 404 (except `/.well-known/`) and dotfiles in `src/pages` are not published                                               |

- HSTS no longer sends `includeSubDomains` by default; opt in with `hsts: { includeSubDomains: true }` only when every subdomain serves HTTPS. `hsts: { maxAge: 0 }` makes browsers forget an earlier policy.
- Turn one off only for a named reason, and never the binding ones for visitor data: `blockCodeBindings: false` lets a prop become code.
- The binding keys and `stripDirectiveScripts` apply at build time (default or `build` export; Bascik warns in `server`). The Cloudflare Worker uses the build's values for all of them.
- Limits are their own settings, not `security`: `scripts.renderLimits` (request-time rendering, `maxInstances: 1000` and five more) and `components.expansionLimits` (build guard, `maxInstances: 10000`, `maxPageLength`). `scripts.stripAnsi: false` keeps terminal color codes in script output.

Details: `read-doc.mjs /configuration` (section `security`) and `read-doc.mjs /scripts/security`.

## Deploy

For watched platform development, use `bascik --target cloudflare` (HTTP port 8787) or `bascik --target netlify` (HTTP port 8888), bound to `127.0.0.1` by default, with `--port`/`--host` overrides. These run the real platform runtime, rebuild the full adapter bundle on source edits, and inject browser live reload only through a local HTTP proxy. Rebuilding or failed builds may return 503; the watcher retries after the next edit. Bare `bascik` remains Node development. Keep `--build --target ...` and direct platform previews for production output without live reload. Read `/deployment/cloudflare#develop-locally` or `/deployment/netlify#develop-locally`.

| Site uses                                                 | Deploy                                                                                                                                                                                       |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Only static pages, build scripts, and dynamic routes      | `BASCIK_SITE_URL=https://example.com bascik --build`, upload `dist/` to any static host                                                                                                      |
| `data-bascik-server`, `data-bascik-stream`, or `src/api/` | `bascik --build && bascik --server` on Node, `bascik --build --target cloudflare` for a Worker bundle, or `bascik --build --target netlify && bascik-netlify-install` for a Netlify Function |

## Look it up

| How do I...                                                                            | Read                                              |
| -------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Find an option and its default                                                         | `/configuration`                                  |
| Choose a host, deploy static output                                                    | `/deployment`, `/deployment/static-hosting`       |
| Run `bascik --server` (TLS, caching, compression, rate limits, proxies, health checks) | `/production-server`                              |
| Deploy to Cloudflare Workers or Pages                                                  | `/deployment/cloudflare`                          |
| Deploy to Netlify Functions                                                            | `/deployment/netlify`                             |
| Write exec scripts and pick a phase                                                    | `/exec-scripts`                                   |
| Control the sitemap and robots.txt                                                     | `/sitemap`                                        |
| Set per-environment values                                                             | `/environment-variables`                          |
| Share components across sites or repositories                                          | `/how-to/monorepos`, `/how-to/sharing-components` |

`node <skills-dir>/bascik/scripts/read-doc.mjs <path>` prints any of these.
