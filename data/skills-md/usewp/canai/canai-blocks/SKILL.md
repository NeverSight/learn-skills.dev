---
name: canai-blocks
description: >
  Opt-in CanAI companion skill for deploying PAGES as native WordPress blocks (Gutenberg)
  instead of Twig, via the CanAI MCP server: wpcanai-create-page with format:"blocks",
  wpcanai-write-page, and converting a page between the Twig and blocks formats. Attach it
  only when the user wants a page they can edit in the block editor. Requires canai-mcp for
  MCP transport, setup, blog posts (wpcanai-write-post), and every other CanAI tool
  (templates, Twig pages, settings, media, i18n, Tailwind).
  Triggers on: "/canai-blocks", "canai-blocks", "block page", "block-authored page",
  "page in blocks", "deploy as blocks", "gutenberg page", "block editor page",
  "wpcanai-write-page", "convert to blocks", "convert to twig", "page css", "block page css".
metadata:
  author: canai
  version: "1.7.4"
allowed-tools: "Read Write Edit Grep Glob"
---

# CanAI Blocks Skill

**Opt-in companion skill to `canai-mcp`.** Attaching this skill is the user's signal that they
want a **page** deployed as native WordPress blocks — editable in Gutenberg — instead of Twig.
Without it, pages are Twig; `canai-mcp` never steers toward blocks on its own. Same server, same
API key, same transport as `canai-mcp` (`{site}/wp-json/mcp/wpcanai`) — this skill only adds
the block-page tools and the page-format concept on top of it.

**Install and configure `canai-mcp` first.** It covers MCP client setup, the API key, the
"MCP only — no shell, no `curl`, no file edits" transport rule, and every other CanAI tool
(templates, Twig pages and layouts, blog posts via `wpcanai-write-post`, settings, media
sideload, i18n, Tailwind builds). This skill assumes all of that already applies and does not
repeat it. The one documented exception to "MCP only" — binary media uploads via the sideload
REST route — is `canai-mcp`'s; this skill only tells you to sideload an image *before*
referencing it by attachment id (see **Images** below).

**Blog posts are not this skill.** A blog post is block content by nature — there is no Twig
alternative — so `wpcanai-write-post` lives in `canai-mcp` and needs no opt-in. This skill is
only about *pages*, where blocks are a choice against Twig.

There is no eval escape hatch here either: the `wpcanai/eval` ability was removed in plugin
v1.59.0. Every capability is a real `wpcanai/*` ability.

---

## Page format — Twig or blocks (plugin v1.65.0)

A **page** is authored in one of two formats. The format is a mark (`_canai_format`) that only
MCP sets; the admin UI shows the owner a prompt to paste to you instead of a toggle.

| | Twig (default — `canai-mcp`) | Blocks (this skill) |
|---|---|---|
| Body lives in | `_canai_html` / `_canai_css` / `_canai_js` | `post_content` (native block markup) |
| Owner edits in | CanAI editor | Gutenberg |
| Write with | `wpcanai-write-meta` | `wpcanai-write-page` |
| Create with | `wpcanai-create-page` | `wpcanai-create-page` with `format: "blocks"` |
| Renders | Twig + layout | blocks inside the page's `_canai_layout` (`{{ page_content }}`) |
| Tailwind | compiled build or Play CDN | compiled layout build when fresh (plugin v1.67.0); Play CDN after any edit until the next `compile tailwind` |
| Page CSS | `_canai_css` (Twig-rendered) | `_canai_css` via write-page `css` — plain CSS, emitted raw after the layout's CSS |
| Snapshots / `replace-in-meta` / `grep-content` / `scan` | yes | no — WordPress revisions are the history |
| Export / import (`wpcanai-export` / `-import`) | yes | **no** — the exporter only finds pages with non-empty `_canai_html`, so a block page is never in a bundle |
| Native translation | `t()` strings in `_canai_html` (string table) | content overrides — the page's title/content/excerpt override blob (`wpcanai-i18n-set-post-overrides`, or the block editor's language mode) swaps in on `/{lang}/` renders, inside the layout; `t()` applies only to the wrapping layout's Twig, since block content is not Twig |
| Conditionals, loops over non-post data, Alpine | yes | no (an `html` block keeps raw markup but needs `unfiltered_html`) |
| Header/footer/layout wrapping | yes | **yes, too** — `_canai_layout` wraps a blocks page's rendered content the same way it wraps Twig, as long as the layout is set |

**Choose blocks** when the owner wants to edit copy and layout themselves in Gutenberg
(marketing pages, landing pages, about/contact). **Keep Twig** for anything with logic, loops
over Woo/term/menu data, or Alpine — use `canai-mcp` for those. Layouts, headers, footers, shop,
product, cart, checkout and archive templates are always Twig (`canai-mcp`'s territory, not this
skill's).

`wpcanai-read-meta` returns `format` by default; `wpcanai-list-pages` rows carry `format`.
Reading `blocks` on a Twig page, writing `html` or `js` on a blocks page, or `write-page` on a Twig page
with html all fail with `format_mismatch` and change nothing. Both of those tools are
`canai-mcp`'s — see that skill for their full argument/return reference; this skill only adds
the block-authoring side. Writing `css` on a blocks page is allowed through either tool — it is
the page's CSS slot.

**Convert to blocks** (owner pastes `Convert post id 123 to blocks. /canai-blocks`):
1. `wpcanai-read-meta` `{ post_id: 123 }` — read `html`, `css`, `js`, `layout`.
2. Rewrite the body as a block list. Static markup maps to
   `group`/`columns`/`heading`/`paragraph`/`image`/`buttons`/`cover`/`media_text`. Anything with
   `{% %}` logic, loops over non-post data, or Alpine **cannot** be carried over: tell the user
   what you left out, or keep it verbatim in an `html` block if the owner accepts raw HTML
   there.
3. `wpcanai-write-page` `{ post_id: 123, blocks: [...], convert: true, css: "..." }`. The Twig
   meta is snapshotted, then cleared, then `css` is written; the response says
   `converted: true`. Rewrite the old `_canai_css` against block class names
   (`.wp-block-button__link`, `.wp-block-list li`) or drop it — Twig-specific selectors will not
   match block markup.
4. Look at the rendered page yourself: `wpcanai-preview-link { "post_id": 123 }`, then open its `url` in a browser
   tool (drafts and maintenance mode included). Then tell the owner to open the page in the block editor and check
   it.

**Convert to Twig** (owner pastes `Convert post id 123 to twig. /canai-blocks`):
1. `wpcanai-read-meta` `{ post_id: 123, fields: ["blocks", "css", "layout"] }` — read the CSS slot
   too; step 3 has to rewrite or clear it.
2. Rewrite the block markup as Twig HTML (drop the `<!-- wp:… -->` delimiters, keep the elements
   and classes).
3. Deal with the CSS slot; it goes into the same write as the body (step 4). A Twig page's
   `_canai_css` is rendered **through Twig**, so plain CSS left over from the blocks build is
   parsed as a Twig template — and `@media (min-width:640px){#hero{...}}` contains `{#`, which
   Twig reads as a comment opener. The render throws, the error is swallowed, and the page
   silently loses **all** of its CSS.
   So rewrite the plain CSS into the Twig CSS body (Twig-safe: no bare `{#`, `{{` or `{%`;
   rewrite `{#id` selectors, e.g. as `[id="hero"]`, or put a space after the brace) — or clear
   it with `css: ""`, adding `confirm_truncate: true` in the same call if the existing CSS is
   non-trivial. Never leave it untouched.
4. `wpcanai-write-meta` `{ post_id: 123, html: "...", css: "...", convert: true }` — this call is
   `canai-mcp`'s tool, but the `convert` flow on a blocks page is documented here since it's the
   reverse of the workflow above. The mark is removed; `post_content` is left in place but no
   longer rendered.

---

## Workflow — brief to a deployed block page

1. **Gate first.** Run [references/feasibility.md](references/feasibility.md) on the brief before
   preparing anything. A fail names the reason and the Twig path (`canai-mcp`); say so to the user
   up front instead of discovering it after the mapping.
2. **Prepare HTML under the block constraints.** Use `canai-prepare` for the browser-previewable
   HTML, applying [references/prepare-for-blocks.md](references/prepare-for-blocks.md) so every
   element maps to a block.
3. **Map and deploy.** Follow [references/html-to-blocks.md](references/html-to-blocks.md): produce
   `pages/<slug>.blocks.json` and `pages/<slug>.css`, sideload images, then `create-page` /
   `write-page`, set the layout, and run `compile tailwind` (`canai-mcp`) if the site uses
   compiled builds.

---

## MCP tool reference (inline)

Ability IDs use slashes; MCP tool names use **hyphens** (`wpcanai/write-page` →
`wpcanai-write-page`). See `canai-mcp` for how to invoke MCP tools from any client — that isn't
repeated here.

### `wpcanai-create-page` (the `format: "blocks"` path)

This is the same `wpcanai-create-page` tool `canai-mcp` documents for Twig pages
(`{ "title", "slug"?, "status"?, "html"?, "css"?, "js"?, "layout"?, "parent"?, "menu_order"? }`)
— this section only covers its block-authoring arguments.

- **Additional args:** `"format"?: "twig"|"blocks"`, `"blocks"?: object[]`.
- **(v1.65.0) `format: "blocks"`.** `blocks` is then required and `html`/`css`/`js` are
  rejected; the page is created with a block body and marked blocks. The block builder's
  warnings come only on this path. The reverse is also refused: sending `blocks` without
  `format: "blocks"` errors `invalid_input` rather than silently publishing an empty page.
- **(v1.96.0) `parent` / `menu_order`** work on the blocks path too: `parent` (an existing
  page's id; `0` = top level) nests the page at `/<parent path>/<slug>/` with `slug` as the last
  segment only, and `menu_order` is Page Attributes → Order. Non-integers are refused by the
  tool's input schema, and a bad parent with `invalid_parent`, both before anything is written.
  Rules and warnings are `canai-mcp`'s
  (`wpcanai-create-page`, **Nested pages**). To move or re-slug an existing blocks page,
  or rename or publish it without re-sending its blocks, use `canai-mcp`'s
  `wpcanai-update-page` — `write-page` takes no `slug` or `parent`.
- **Returns:** `{ "post_id": int, "slug": string, "format": string,
  "warnings": string[], "status": string, "parent": int, "path": string, "url": string }`.

### `wpcanai-write-page`

- **Args:** `{ "post_id": int, "blocks": object[], "title"?: string, "status"?: string,
  "layout"?: int, "css"?: string, "convert"?: bool }` — `post_id` must be a
  `page`. `blocks` replaces the whole body (WordPress revisions are the undo path). Block types
  are listed below; the `html` block is available here (and in `create-page` with
  `format: "blocks"`), and nowhere else.
- **`css`.** Plain CSS stored in `_canai_css` and emitted raw in the head after the layout's
  CSS — never Twig-rendered, no `@apply`. Use it only for the markup WordPress owns inside a
  block (`.wp-block-button__link`, `.wp-block-list li`, `.wp-block-table td`, the cover overlay);
  everything on a block's root element stays a Tailwind `className`. `""` deletes it; omit to
  leave it. Written after the body and after a conversion's cleanup, so a failed body write never
  touches it.
- **Returns:** `{ "post_id", "slug", "status", "url", "edit_url", "format": "blocks",
  "converted": bool, "block_count", "warnings": string[] }`.
- **Format guard.** On a Twig page whose `_canai_html` is non-empty the call fails with
  `format_mismatch` (the error carries the prompt to show the owner) unless `convert: true`:
  then the body is written first, and only once that lands is the CanAI meta snapshotted and
  `_canai_html`/`_canai_css`/`_canai_js` deleted and the page marked blocks — in that order, so a
  failed body write destroys nothing. A Twig page with empty html is simply written and marked.
  A `css` field in the same call is written after the cleanup.
- **Layout still applies.** Set `layout` to a `canai-mcp` layout template's id the same way you
  would on a Twig page. `_canai_layout` wraps a blocks page's rendered content in that layout's
  Twig shell (header/footer included) exactly as it wraps Twig content — the plugin checks
  `_canai_layout` independently of the format mark, so the same layout mechanism serves both.
- **Errors:** `invalid_input`, `invalid_status`, `not_a_page`, `invalid_blocks`
  (with `path` like `"2.blocks.0"` for nested blocks), `invalid_attachment`, `format_mismatch`,
  `forbidden` (writing `css` without the `unfiltered_html` capability; an authenticated MCP
  API-key request runs as an administrator and bypasses this check). Fatal problems write
  nothing.

## Block types (v1)

Each item in `blocks` is `{ "type": …, …fields }` — accepted by `write-page` and by
`create-page` with `format: "blocks"`. (`canai-mcp`'s `wpcanai-write-post` takes the same list
minus `html`.)

| `type` | Fields |
|---|---|
| `paragraph` | `text` (required), `align` (`left`/`center`/`right`) |
| `heading` | `text` (required), `level` 2–6 (default 2; **level 1 is rejected** — the post title is the h1) |
| `list` | `items` string[] (required), `ordered` bool. Flat lists only |
| `quote` | `text` **or** `paragraphs` string[] (one required), `cite` |
| `image` | `id` int (required — an attachment id), `alt`, `caption`, `size` (default `large`), `link` (`none`/`media`/`attachment`) |
| `code` | `code` (required). Escaped as literal text; no inline HTML |
| `separator` | — |
| `embed` | `url` (required, http/https) |
| `table` | `rows` string[][] (required, rectangular), `header` string[] |
| `group` | `blocks` (required, child blocks), `tag` (`div`/`section`/`header`/`footer`/`aside`/`main`), `className` |
| `columns` | `columns` (required, 1–6 of `{ width?, className?, blocks }`), `className` |
| `buttons` | `buttons` (required, `{ text, url, style?: fill/outline, target?: _blank, rel?, className? }`), `className` |
| `cover` | `image` (required, attachment id), `overlay_opacity` (10–100 step 10, default 50), `blocks` (required), `className` |
| `media_text` | `image` (required, attachment id), `side` (`left`/`right`), `blocks` (required), `className` |
| `spacer` | `height` px (1–1000, default 100), `className` |
| `html` | `html` (required, raw markup kept verbatim). Requires `unfiltered_html` on the user the write runs as; refused otherwise |

Every type except `embed` and `html` accepts `className` (Tailwind classes on the block's root
element). `core/html` declares `supports.className: false`, so a class set there is dropped and
reported as a warning — put it on your own markup instead; `embed` rewrites its own class list
on first save. Nesting is capped at 4 levels. Nested errors report a dotted `path`.

**Images: sideload first, then pass the id.** `write-page` accepts attachment ids only — no
URLs, no binaries (`cover` and `media_text` take the same id and return `invalid_attachment` if
it doesn't resolve). Call `wpcanai-sideload-url` (`canai-mcp` tool — or find an existing one
with `wpcanai-list-media`) and pass the returned `id`.

**Inline HTML inside text fields** is limited to `<a href|title|rel|target>`, `<strong>`,
`<em>`, `<b>`, `<i>`, `<code>`, `<br>`, `<s>`, `<sub>`, `<sup>`, `<kbd>`, `<mark>`. Anything else
is stripped silently, not rejected — a `<script>` or `<iframe>` in a paragraph would be invalid
block content anyway. Markdown is **not** accepted; there is no raw-HTML escape hatch inside
text fields — raw markup goes in an `html` block.

---

## Undo (snapshots)

Block-page writes go through the same CanAI snapshot system `canai-mcp` documents in its
**History / undo (snapshots)** section — `wpcanai-write-page`'s convert-to-blocks path
snapshots the CanAI meta before clearing it (operation `mcp-write-page-convert`), and the whole
`wpcanai-list-snapshots` / `wpcanai-get-snapshot` / `wpcanai-restore-snapshot` /
`wpcanai-restore-operation` toolset applies. This skill doesn't repeat that reference — see
`canai-mcp` for it. One caveat worth restating here: a snapshot taken while a page was marked
`blocks` but still carried a non-empty `_canai_html` (a stale Twig body left behind by an
interrupted conversion) restores both values together — the page still opens in the block
editor, but the stale Twig renders instead of the blocks, because the frontend only falls back
to `post_content` when `_canai_html` is empty. `post_content` itself has **no** snapshot/undo
path of its own — WordPress's own post revisions are the only history for block content.
