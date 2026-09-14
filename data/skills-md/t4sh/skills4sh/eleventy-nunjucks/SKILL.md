---
name: eleventy-nunjucks
description: "Eleventy v3, Build Awesome v4 prerelease, and Nunjucks operating guide for static-site authoring, templates, build pipelines, migrations, and security review. Use when the user asks to \"create an 11ty page\", \"add a Nunjucks filter\", \"fix my layout chain\", \"review my .njk template\", \"set up Eleventy\", \"migrate to Build Awesome\", or \"audit my static site\"; when `package.json` includes `@11ty/eleventy` or `@awesome.me/buildawesome`; when paths include `.eleventy.js`, `eleventy.config.js`, `.njk`, `.11tydata.js`, `.data.js`, `.11ty.js`, or `.server.js`; or when debugging data cascades, filters, shortcodes, async Nunjucks, autoescape, or static-site security."
license: MIT
compatibility: macOS, Linux, or Windows; Eleventy v3 supports Node >=18, but supported Node 22 or 24 LTS is recommended
metadata:
  author: t4sh
  version: "0.1.8"
  tags: 11ty, eleventy, eleventy-v3, build-awesome, build-awesome-v4, nunjucks, static-site, ssg, jamstack, tailwind, markdown-it, autoescape, xss-prevention, csp, design-tokens
---

# Eleventy + Nunjucks

Operational defaults for **Eleventy v3** and **Nunjucks** static sites — directory layout, configuration surface, filter inventory, autoescape rules, stability and security checks. Load this skill when authoring templates, editing build config, or reviewing static output before merge or deploy.

> **Version boundary (verified August 6, 2026):** Eleventy `3.1.6` is the stable production baseline. Build Awesome `4.0.0-alpha.10` is a prerelease available through `@11ty/eleventy@canary` or `@awesome.me/buildawesome@alpha`. Existing Eleventy commands remain compatible, but v4 changes runtime and template behavior. Keep stable guidance as the default and load [`references/build-awesome-v4.md`](references/build-awesome-v4.md) before any v4 install or migration.

## When this skill applies

Trigger on any of:

- Paths mentioning `.eleventy.js`, `eleventy.config.{js,mjs,cjs}`, `.njk`, `.11tydata.js`, `.data.js`, `.11ty.js`, `.server.js`, `src/_includes/`, or `src/_data/`
- `package.json` lists `@11ty/eleventy` or `@awesome.me/buildawesome`
- Topics: 11ty, Eleventy, Nunjucks, SSG, JAMstack, static site, layout chain, permalink, collection, shortcode, filter, dev server, CSP, JSON-LD in templates

---

## Operating procedure

1. **Open `package.json`, its lockfile, and the active Eleventy config.** Identify the installed package/version, module type, Node engine, and the first config filename Eleventy resolves. Checked-in project behavior always wins.
2. **Choose the track.** Use the stable v3 guidance by default. If the project uses a v4 canary, the Build Awesome package, or the generic `.data.*` / `.server.*` suffixes, load `build-awesome-v4.md` and enforce its version-drift stop condition.
3. **Open the task-specific reference** from the table below. Avoid loading every reference unless the change is large.

The portable core targets **Eleventy 3.1.6 + Mozilla Nunjucks 3.2.4**. Version-sensitive v4 guidance is isolated in the prerelease reference. For upstream drift, prefer [11ty.dev](https://www.11ty.dev/docs/), [`11ty/buildawesome`](https://github.com/11ty/buildawesome), and the active package metadata; treat dated claims as revalidation markers.

### Completion gate

Before calling work complete, verify the project-specific result rather than only applying this skill's defaults:

1. The relevant Eleventy build, dev-server smoke check, or project test command passes.
2. Site shells that need layout frontmatter, cascade behavior, or layout chaining use Eleventy `layout:` and render `{{ content | safe }}` intentionally; any Nunjucks `extends` usage is reviewed as a separate inheritance path.
3. Every new or changed `| safe`, `{% autoescape false %}`, inline JSON/script data path, and markdown `html` setting has been reviewed against the trust boundary.
4. The task-specific reference checklist was applied when relevant (`review-shipping.md` for PR review, `security-checklist.md` for deploy/security, etc.).
5. Rendered output or generated HTML was inspected for the touched page, layout, filter, shortcode, or data cascade.

---

## Mental model (30 seconds)

| Topic | Common default |
|---|---|
| Eleventy | Stable v3.1.6 by default; Build Awesome v4 remains prerelease and version-gated |
| Node | v3 package floor `>=18`; use a supported LTS (Node 24 preferred, Node 22 supported). v4 prerelease requires `>=22.15`. |
| Config name | Search order: `.eleventy.js`, `eleventy.config.js`, `eleventy.config.mjs`, `eleventy.config.cjs`; the first match wins |
| Engines | `.njk`, `.md`, `.html` — markdown runs **through** Nunjucks when `markdownTemplateEngine` is `njk` |
| Output dir | Eleventy default `_site/`; the opinionated production profile in this skill uses `out/` |
| Input | Eleventy default project root; the production profile often uses `src/pages/` or flat `src/` |
| Layouts | Under `src/_includes/layouts/`; chain via `layout:` in frontmatter |
| Sections / macros | `src/_includes/sections/…`, `src/_includes/macros/…` |
| Data | `src/_data/*.{json,js}` plus directory and template data — see `references/data-cascade.md` |
| CSS | Project-selected; the optional profile uses Tailwind v4 CLI + `concurrently --kill-others-on-fail` |

---

## Non-negotiable rules

**Layout chain:** prefer `layout:` and `{{ content | safe }}` for site shells that require Eleventy layout frontmatter, cascade behavior, or layout chaining. Nunjucks `{% extends %}` is supported, but frontmatter in the extended parent template is not processed.

**Autoescape:** treat every `| safe` as a security boundary. Never mark user, CMS, or external HTML safe without sanitization. `dump` is for debug in `<pre>`, not inside executable `<script>`.

**Inline data in `<script>`:** use `jsonScript` or `jsonCompact` (see `references/filters.md`), not raw `JSON.stringify` or `dump | safe`.

**Flat permalinks + nginx `try_files $uri.html`:** `page.url` may end in `.html`. Ship `normalize_path` (see `references/filters.md`) for nav active state and canonical URLs.

**Passthrough copy:** prefer explicit `{ "src/path": "dest/path" }` maps — never copy `src/**/*` blindly.

**CSP:** prefer production HTTP headers. If the project uses a CSP `<meta>`, omit or adapt it during `--serve` so live reload is allowed. Deliver `frame-ancestors` via HTTP headers, never `<meta>`.

**Macros and scope:** `{% import %}` does not inherit page scope by default. If macros read `page.*` / `site.*`, use `with context` or pass arguments explicitly (see `references/nunjucks-syntax.md`).

**Markdown-it `html`:** keep `html: false` unless every markdown author is trusted; changing to `true` widens XSS risk.

**Before adding a new filter:** grep the project config for an existing filter with the same role — common 11ty projects duplicate `where` with incompatible coercion across files.

---

## Data cascade (priority order)

Highest priority wins. When a variable is missing or wrong, trace this official order before considering Eleventy-supplied values such as `page`, `collections`, or `eleventy`.

1. `eleventyComputed`
2. Template frontmatter
3. Template data files
4. Directory data files, ascending through parent directories
5. Layout frontmatter
6. `eleventyConfig.addGlobalData`
7. Global data files

Worked examples and pagination: `references/data-cascade.md`.

---

## Autoescape and the safe filter

Assume `foo` holds untrusted HTML such as a tag with an event handler.

| State | Result of `{{ foo }}` |
|---|---|
| `autoescape: true` (default) | Escaped — safe for text nodes |
| `autoescape: true` and value piped through the **safe** filter | Raw HTML — XSS if `foo` is untrusted |
| `autoescape: false` | Raw HTML — treat like global XSS risk |
| `autoescape: false` and **escape** filter applied | Escaped again |

Rules of thumb:

- Apply the `safe` filter only to trusted, sanitized HTML (or to the output of `jsonScript` / `jsonCompact` inside `<script>` as documented in `references/filters.md`).
- Avoid `{% autoescape false %}` except in tightly reviewed fragments; prefer narrowing with per-value filters.
- Markdown piped through a custom `md` filter is only as safe as `markdown-it`’s `html` flag — keep `html: false` for anything not fully trusted.

Full Nunjucks tag and macro rules: `references/nunjucks-syntax.md`.

---

## Reference files

| File | Load when |
|---|---|
| [references/eleventy-config-api.md](references/eleventy-config-api.md) | v2→v3 migration, config skeletons, `addFilter` / events / collections / server options |
| [references/build-awesome-v4.md](references/build-awesome-v4.md) | Build Awesome v4 prerelease detection, migration gates, Node/Nunjucks/data changes |
| [references/conventions.md](references/conventions.md) | Directory layout, `dir` matrix, naming, scripts shape, when to deviate |
| [references/data-cascade.md](references/data-cascade.md) | Merge order, `eleventyComputed`, pagination, worked traces |
| [references/filters.md](references/filters.md) | Canonical filter source, `normalize_path`, `jsonScript`, async filters |
| [references/nunjucks-syntax.md](references/nunjucks-syntax.md) | Tags, macros, `with context`, built-in filters, `extends` vs 11ty layouts |
| [references/build-pipeline.md](references/build-pipeline.md) | Tailwind v4 + concurrently, lint/format, clean targets |
| [references/production-patterns.md](references/production-patterns.md) | CSP, View Transitions contract, nginx, after-build hooks, OG/JSON-LD patterns |
| [references/review-shipping.md](references/review-shipping.md) | PR greps, stability checklist, anti-patterns, page recipes |
| [references/security-checklist.md](references/security-checklist.md) | Pre-deploy XSS, headers, passthrough, secrets audit |
| [references/troubleshooting.md](references/troubleshooting.md) | 404 on `--serve`, double sections, autoescape surprises, hung builds |

---

## Related skills

**Same monorepo (skills4sh):** `agent-memory` (cross-session context), `localhost-screenshots` (visual regression for static sites).

**Ground truth wins:** when a project's checked-in `.eleventy.js` / `eleventy.config.js` disagrees with this skill, the project wins. Always read the actual config and `package.json` scripts before applying conventions from here.

---

## Minimal layout reminder

```nunjucks
{# Child page #}
---
layout: layouts/page.njk
title: Example
---
<section>Page body</section>
```

```nunjucks
{# layouts/page.njk #}
---
layout: layouts/base.njk
---
<main>{{ content | safe }}</main>
```

Each parent renders the child’s compiled body through `content`, then pipes through `safe` where the child emits HTML (11ty layouts that slot HTML always use `safe` on `content`).
