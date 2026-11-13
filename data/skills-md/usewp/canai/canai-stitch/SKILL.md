---
name: canai-stitch
description: >
  Deploy Google Stitch screens to a CanAI WordPress site and bring the copy up to CanAI conventions,
  through the CanAI MCP server and the CanAI Stitch add-on (wpcanai-stitch-* tools). Use when the user
  wants to deploy, import, publish or update a Stitch design, screen or project on WordPress, re-deploy
  after the design changed, or clean a deployed screen up (menus instead of hard-coded nav, t() strings,
  header/footer templates). Companion to canai-mcp.
  Triggers on: "stitch", "google stitch", "stitch.withgoogle.com", "stitch screen", "stitch design",
  "stitch project", "deploy stitch", "import from stitch", "stitch to wordpress", "stitch to canai",
  "redeploy stitch", "update from stitch", "canai stitch", "canai-stitch", "wpcanai-stitch-deploy-screen".
metadata:
  author: canai
  version: "1.2.1"
allowed-tools: "Read Grep Glob"
---

# CanAI Stitch — deploy Google Stitch screens

Google Stitch (stitch.withgoogle.com) designs web and app screens. The **CanAI Stitch** add-on deploys a Stitch
screen straight to a CanAI page: the site holds the owner's Stitch API key and calls Stitch's official API itself.
You drive it with five MCP tools; you never fetch Stitch HTML yourself and never see the key once it is connected.

**This skill is a companion to [canai-mcp](../canai-mcp/SKILL.md).** Everything canai-mcp says about the transport
(CanAI MCP server only, no WP-CLI, no file edits) and about CanAI's conventions (menus, `t()`, templates, structure
comments, `wpcanai-scan`) applies here; this skill only adds the Stitch tools and the Stitch-specific workflow.

## Requirements

- CanAI **1.98.0+** with its MCP server connected (canai-mcp's prerequisites).
- The **CanAI Stitch** add-on (`canai-stitch` **1.1.0+**) active on the site.
- **No `wpcanai-stitch-*` tools in your list?** The add-on is not installed or not active. Ask the owner to install it
  (https://github.com/usewp/canai-stitch). If they can't, a screen's HTML exported from Stitch is just an HTML file: prepare it with [canai-prepare](../canai-prepare/SKILL.md) and deploy it with canai-mcp like any other.
- **The key.** The owner creates it in **Stitch → Settings → API Keys** and pastes it in **CanAI → Tools → Import
  from Stitch** — preferred, the key stays out of the chat. Use `wpcanai-stitch-connect { "api_key" }` only when the
  owner hands you the key for that purpose. Never write a key into a template, a file or a message.
- **Who can deploy:** a deploy writes raw `_canai_html` / `_canai_css`, so it follows `wpcanai-write-meta`'s rule — a
  request made with a CanAI API key, or a user with `unfiltered_html` (`forbidden` otherwise).

## Pick the mode first

A deployed page is a **faithful copy** of the design: its nav is hard-coded `<a>` links, its text is literal, it has
no structure comments. Bringing it up to CanAI conventions means editing it in CanAI — and **an edited page is no
longer something a re-deploy can update without throwing those edits away.** So decide with the owner which way round
it is, before cleaning anything:

| Mode | When | What you do |
|---|---|---|
| **Stitch stays the source** | The design is still changing; the owner iterates in Stitch | Deploy, review, re-deploy as often as the design changes. Don't edit the deployed page or layout in CanAI (every edit makes the next deploy stop). The copy stays a copy: fine for previews, landing pages, campaign pages. |
| **Hand over to CanAI** | The design is final | Deploy once, then run **Cleanup** below. From then on CanAI is the source: a later Stitch change either goes in by hand, or with `overwrite: true` (the cleanup is lost — the snapshot keeps it restorable). |

**A new page for the same screen.** A re-deploy always targets the page an earlier deploy made for that screen;
only a page in the trash is ignored. To deploy the design to a fresh page while keeping the cleaned-up one, the owner
duplicates the screen in Stitch and you deploy the duplicate (a new screen id, so a new page and layout).

## Deploy

1. **Connected?** `wpcanai-stitch-connect` with no arguments → `{ connected, key_hint }`. Not connected → the key
   step under **Requirements**.
2. **Find the project.** A Stitch account can hold dozens of projects; the site works with the ones its owner
   **chose** (CanAI → Tools → Import from Stitch → Add projects). `wpcanai-stitch-list-projects` with no arguments
   lists exactly those. If the project the owner means is there, use it. If it is not (or nothing is chosen yet), look
   in the whole account — `wpcanai-stitch-list-projects { "view": "owned" }`, or `"shared"` for projects shared with
   the owner (each row has `added`) — **ask the owner which project is for this site**, then
   `wpcanai-stitch-set-projects { "add": ["<id>"] }`. Never add projects the owner did not name.
   `unavailable` in the site list means a chosen project the key can no longer see (deleted, unshared, another
   account's key): tell the owner; `wpcanai-stitch-set-projects { "remove": [...] }` clears it.
3. **Find the screen.** `wpcanai-stitch-list-screens { "project_id" }` → the screen. `deployed_page_id > 0` means
   an earlier deploy made a page for it (re-deploy rules below). `hidden` counts items that are not designs
   (no device, size or preview, such as Stitch's "Extracted text from…" notes): leave them alone — there is no HTML
   to deploy — and pass `include_other: true` only to look at them.
4. **Deploy.** `wpcanai-stitch-deploy-screen { "project_id", "screen_id" }` → a **draft** page plus a layout of its
   own. Pass `status: "publish"` only when the owner asked for it.
5. **Read the result.**
   - `images.remote` > 0 → the 25-second image budget ran out: deploy again (already-copied images are reused) to
     copy the rest.
   - `images.failed` > 0 → read the warning. Stitch sometimes generates image URLs Google itself answers with 400
     (their ids end in repeated patterns); those are broken in Stitch too and stay remote on every deploy — tell the
     owner, who can regenerate the image in Stitch or give you a replacement to sideload.
   - `site_changes` → what `prepare_site` turned on (Tailwind, the Tailwind plugins the screen uses). Mention it.
6. **Check it.** Call `wpcanai-preview-link { "post_id": <page_id> }` and open its `url` in your browser tool at phone
   and desktop widths. It shows the draft, without the admin bar, even during maintenance mode (canai-mcp: **Check
   your work in a browser**). Compare with the screen in Stitch. A `fixed top-0` bar at the very top is hidden behind
   WordPress's admin bar for a logged-in owner; visitors and the preview link see it.

## What a deploy writes

- **Layout** `Stitch: <screen title>` (`template_type` `layout`, published): CanAI's document shell with
  `{{ wp_head() }}`, the screen's Google Fonts links (Material Symbols included), its `tailwind.config` in a
  `<script id="tailwind-config">` after `wp_head()`, and its `<html>` / `<body>` classes and attributes. The screen's
  head `<style>` goes to the layout's `_canai_css`. Stitch's Tailwind CDN script is dropped: CanAI serves its own
  Tailwind v3.
- **Page**: `_canai_html` is the screen's `<body>` after a one-line `{# Stitch: … #}` note; `_canai_layout` points at
  the layout. Any `{{`, `{%` or `{#` in the design (layout CSS included) is printed literally (`{{ '{{' }}`), so a
  design can never run Twig. Images that carried only `data-alt` get a real `alt`.
- **Images** are copied to the media library, attached to the page and named after the screen
  (`<screen-slug>-1`, `-2`, … with the image's own extension), and the markup points at the copies; a re-deploy reuses them.
- One **snapshot operation** covers the page and the layout: `wpcanai-restore-operation { "operation_id",
  "confirm": true }` undoes the deploy.

## Re-deploy

Deploying the same screen again updates **that** page and its layout in place and keeps the page's title, slug,
status and parent; `status` changes only when you pass it.

If, since the last deploy, the page's `_canai_html`, the layout's code, or the page's layout choice was changed in
CanAI, the deploy stops with **`stitch_page_edited`** (409) and writes nothing. The error data names what changed:
`edited` ⊆ `page`, `layout`, `layout_choice`. Content a snapshot restore put back is not a change. Then:

- the owner wants the new design over those edits → deploy again with `overwrite: true` (the snapshot keeps the
  edited version restorable);
- the edits are your cleanup and the owner wants to keep them → don't overwrite; port the design change by hand
  (read the new screen in Stitch, edit with `wpcanai-replace-in-meta`).

Never pass `overwrite: true` on your own initiative.

## Cleanup — hand over to CanAI

Run this only in **Hand over** mode, on the deployed page (`page_id`) and its layout (`layout_id`). It is canai-mcp's
"Implement HTML → CanAI" applied to a page that is already on the site; read that section and **Menus** there for the
detail of each rule.

1. **Look.** `wpcanai-read-meta` on the page and the layout, then `wpcanai-scan { "post_id": <page_id> }`. Expect
   `hardcoded_nav`, missing structure comments and literal strings; clear them in the steps below.
2. **Pages first.** Stitch's nav links are mostly `href="#"` placeholders. Ask the owner which page each nav item
   should open; create missing pages with `wpcanai-create-page` (or deploy their Stitch screens) **before** writing
   the menu. Never invent URLs.
3. **Header and footer → templates** (when they belong on other pages too). Create them with
   `wpcanai-create-template` — `type` `header` / `footer`, a **title that slugs to exactly `header` / `footer`** unless
   the site already has those (then reuse or merge; check `wpcanai-list-templates`). Move the screen's `<header>` /
   `<footer>` markup into them, then, with `wpcanai-replace-in-meta`, put `{{ wpcanai_template('header') }}` before and
   `{{ wpcanai_template('footer') }}` after `{{ page_content }}` in the **Stitch layout**, and remove the markup from
   the **page**. A screen-specific header can stay in the page.
4. **Navigation → menus.** Write each nav list once with `wpcanai-write-menu` (`primary` for the header, `footer` for
   the footer — never another location), then replace the list with the `get_menu()` loop, keeping the screen's
   classes on the `<nav>` and the `<a>`. A mobile drawer loops `get_menu('primary')` again.
5. **Internal links.** Other links to site pages → `{{ turl(id_url(<id>)) }}` (or `slug_url()`); in-page `#section`
   anchors stay.
6. **Strings → `t()`.** Wrap user-facing copy one whole sentence per `t()`, inline tags inside, block elements
   outside, dynamic values as `{placeholders}` (canai-mcp **Native string translation**).
7. **Structure comments.** Label the sections with `{# Type / Short Label #}` comments (canai-mcp's "Implement HTML" step 7 and
   [STRUCTURE-NAVIGATION.md](../canai-mcp/references/STRUCTURE-NAVIGATION.md)), replacing the HTML comments Stitch left.
8. **Images (optional).** The markup points at the copies by URL. To follow CanAI's helper rule, swap each for
   `{{ media_url(<id>, 'full') }}` / `{{ image_attrs(<id>, 'src,alt') }}` — find the ids with `wpcanai-list-media`
   (`search` by the screen slug). Ask the owner about images left on Google.
9. **Icons.** Material Symbols keep working (the layout loads the font). Convert to Lucide only when the site uses
   Lucide elsewhere and the owner wants one icon set.
10. **Scan again** until clean, open the page, and tell the owner the page is now CanAI's: a re-deploy from Stitch
    will stop with `stitch_page_edited` and only `overwrite: true` would replace the cleanup.

## Tools

### `wpcanai-stitch-connect`

- **Args:** `{ "api_key"?: string, "disconnect"?: boolean }`. With `api_key`, Stitch checks the key before it is
  stored; a key Stitch rejects is not stored and an existing one is kept. `disconnect: true` removes the stored key.
  Neither → the current status.
- **Returns:** `{ "connected": bool, "key_hint": "…ab12", "projects"?: int }` — never the key. `wpcanai-get-option`
  refuses the key's option.

### `wpcanai-stitch-list-projects`

- **Args:** `{ "view"?: "owned"|"shared" }`. Omitted → **this site's projects** (the ones its owner chose).
  `owned` / `shared` → every project in the connected account, to choose from.
- **Returns:** `{ "projects": [{ "id", "title", "updated", "device", "thumbnail", "added" }], "unavailable"?: string[] }`
  — `added`: the project is on this site's list; `unavailable` (site list only): chosen ids the key cannot see.

### `wpcanai-stitch-set-projects`

- **Args:** `{ "add"?: string[], "remove"?: string[] }` — project ids. Neither → the ids chosen so far, without
  calling Stitch.
- **Adding** checks every id against the account (owned or shared) first; if one is not found, **nothing** is added
  (`stitch_project_not_found`). **Removing** only edits the site's list: the project in Stitch and pages already
  deployed from it are untouched. Disconnecting the key keeps the list.
- **Returns:** `{ "added": string[], "removed": string[], "projects": string[] }` — the ids now chosen, in the order
  they were added.
- The add-on does not stop `wpcanai-stitch-list-screens` / `-deploy-screen` for a project that is not on the list;
  put the project on the list first so the owner sees it in wp-admin.

### `wpcanai-stitch-list-screens`

- **Args:** `{ "project_id": string, "include_other"?: bool (default false) }`.
- **Returns:** `{ "project_id", "screens": [{ "id", "title", "device", "width", "height", "thumbnail", "design": bool,
  "deployed_page_id", "deployed_at", "page_status", "edit_url" }], "hidden": int }`. Items that are not designs
  are left out and counted in `hidden`; a screen with a deployed page is never left out.

### `wpcanai-stitch-deploy-screen`

- **Args:** `{ "project_id": string, "screen_id": string, "status"?: "draft"|"publish"|"pending"|"private",
  "rehost_images"?: bool (default true), "prepare_site"?: bool (default true), "overwrite"?: bool (default false) }`.
- **Returns:** `{ "page_id", "layout_id", "created": bool, "status", "url", "edit_url", "images": { "rehosted",
  "reused", "remote", "failed" }, "site_changes": string[], "warnings": string[], "operation_id", "purged" }`.

## Errors (nothing is written)

| Code | Meaning / what to do |
|---|---|
| `stitch_not_connected` | Connect first (**Requirements**). |
| `stitch_invalid_key` | Not shaped like a Stitch key — have the owner copy it again. |
| `stitch_unauthorized` | Stitch rejected the key (deleted or revoked) — the owner makes a new one and connects it. |
| `stitch_not_found` | Wrong id, or a project of another account (try `view: "shared"`). |
| `stitch_project_not_found` | `wpcanai-stitch-set-projects` `add`: an id is not in the connected account (owned or shared); nothing was added. List the account with `view` and use an id from it. |
| `stitch_rate_limited` | Wait a minute, then retry. |
| `stitch_unavailable` / `stitch_bad_response` | Stitch is unreachable or answered oddly — retry later. |
| `stitch_link_expired` | The download link expired twice in a row — retry. |
| `stitch_html_too_large` | The screen's HTML is over 5 MB. |
| `stitch_parse_failed` | The screen's HTML could not be read; tell the owner which screen. |
| `stitch_page_edited` | See **Re-deploy**. |
| `forbidden` | The caller lacks `unfiltered_html` (and the request has no CanAI API key). |
| `invalid_input` | A missing or malformed id, or an unknown `status`. |
