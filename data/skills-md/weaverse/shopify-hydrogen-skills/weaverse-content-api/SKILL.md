---
name: weaverse-content-api
description: Use when reading or updating live Weaverse content programmatically — pulling projects/pages/theme settings, bulk-editing page content, pushing AI-generated copy, deleting pages, or uploading media to Shopify for use in Weaverse. Triggers on requests to update a Weaverse project via API, push content to a live project, run bulk content edits, or upload images/assets to Shopify from automation.
---

# Weaverse Content API

Read and edit live Weaverse content (projects, pages, theme settings, languages) outside the Studio editor, over an authenticated REST API. Use it for bulk edits, AI/automation content pipelines, and pushing updates into a project that already exists.

- **Base URL:** `https://studio.weaverse.io/api/v1/content`
- **Machine spec:** `GET https://studio.weaverse.io/api/v1/content/openapi.json` (OpenAPI 3.1, no auth) — the authoritative contract
- Full endpoint details: `references/endpoints.md`. Rich-text/Portable Text details: `references/portable-text.md`.
- Helper script: `scripts/weaverse_content_api.mjs` (zero-dependency, Node 18+).

## The one thing you must understand first

**The Content API edits live content — and it can also create pages.**

Two write paths exist:

- `PATCH .../pages/:type/*handle` shallow-merges `data` into items **on the page**. Existing ids are updated; an unknown id is **created** when its entry also supplies a `type` (the component type). `children` may be supplied to relink an item's children in the same request — each entry needs an `id` that already belongs to the page or is created in the same request.
- `POST /projects/:projectId/pages` **creates a page** — a `CUSTOM` page (bespoke merchant page, blank root) or a resource-backed template page (`PRODUCT`/`COLLECTION`/`PAGE`/`BLOG`/`ARTICLE`, a per-resource override that clones the project's shared default template or a `basedOn` source page).

So the lifecycle is:

```
Create initial structure  →  import a project JSON into Studio (generating-weaverse-project-json)
                              OR create pages one by one via POST /projects/:projectId/pages
Update content afterwards  →  Content API (PATCH page content, incl. new typed items)
```

There is no "create project" endpoint — a project must already exist (from Weaverse Builder) before the API can touch it.

## When to Use

- Push AI-generated or translated copy into an existing live project
- Bulk-edit content across many pages/items
- Read current page content/items to diff or round-trip
- Add a new typed item to a page (via `PATCH` with a `type` on the new id) or relink `children`
- Create a `CUSTOM` page or a resource-backed template page (`POST /projects/:projectId/pages`)
- Delete pages in bulk
- Upload an image/video to Shopify and reference its CDN URL in a Weaverse item

Do not use it to create *projects* — a project must already exist in Weaverse Builder.

## Authentication

Every endpoint except `openapi.json` needs a bearer token:

```
Authorization: Bearer <WEAVERSE_API_KEY>
```

- Get the key from **Weaverse Studio → Dashboard → Account/Settings → API Keys**.
- A token is scoped to one shop. Requests for a project owned by another shop return `403 FORBIDDEN`.
- The same token also authorizes the Shopify proxy (see "Upload resources to Shopify").
- Store it in an env var (`WEAVERSE_API_KEY`). Never hardcode it, never pass it as a `?apiKey=` query param outside local testing — query params leak into server/CDN logs.

## Core update workflow

**Read before you edit.** To change existing content you must target real item ids, so read the page first — you cannot patch blindly. New items are the one exception: they use a fresh id plus a `type`, and must fit the page tree (a `children` reference has to point at an id already on the page or created in the same request).

1. **Find the project** — `GET /projects`, match by name, keep its `id`.
2. **Pick a locale** — `GET /projects/:projectId/languages`. Keep the `isDefault: true` code (e.g. `en-us`). You need it for the next steps.
3. **Read the page** — `GET /projects/:projectId/pages/:type/*handle?locale=<code>`. **Always pass `locale`.** With no `locale` the resolver only tries the empty locale and the legacy default `en-us`, so a market-first project or any project whose default locale isn't `en-us` returns `PAGE_NOT_FOUND` even though the page exists. The default `weaverse` format already returns **every item with its `id`** — that id is exactly what the patch needs, so **`?meta=true` is not required** (it only matters for `portable-text` reads).
4. **Build the patch** — for each item you want to change, send only the fields that change inside `data` (it shallow-merges, so untouched fields stay). To **create** a new item, give it a fresh `id` and supply its `type` (component type). To **relink children**, add `children` with the child ids (each must already belong to the page or be created in the same request). Include the **same `locale`** you read with:
   ```json
   {
     "locale": "en-us",
     "items": [
       { "id": "itm1", "data": { "heading": "New heading" } },
       { "id": "itm-new", "type": "Hero", "data": { "heading": "Fresh section" }, "children": [{ "id": "itm1" }] }
     ]
   }
   ```
5. **Patch** — `PATCH /projects/:projectId/pages/:type/*handle` (use `POST` if your client/proxy can't send a `PATCH` body). The page is resolved with the **same locale rules as the read** — a missing/wrong `locale` can hit `PAGE_NOT_FOUND` or patch the wrong locale's page. Max **100 items per request** — chunk larger edits.
6. **Check the response** — `{ object: "page_update", updated, notFound, updatedIds, notFoundIds }`. A non-empty `notFoundIds` means those ids couldn't be resolved on the page (wrong page, wrong locale, stale ids, or a new id sent **without** a `type`) — re-read the page with the right `locale`, don't retry the same ids.

A successful patch invalidates caches and goes live through `api.weaverse.io` — the same path a Studio save takes.

### Page addressing

Pages are addressed by Prisma page type + handle:

```
INDEX, PRODUCT, ALL_PRODUCTS, COLLECTION, COLLECTION_LIST, PAGE, BLOG,
ARTICLE, CART, CUSTOMER, NOT_FOUND, PASSWORD, SEARCH, CUSTOM
```

- **Singletons** (`INDEX`, `ALL_PRODUCTS`, `COLLECTION_LIST`, `CART`, `CUSTOMER`, `NOT_FOUND`, `PASSWORD`, `SEARCH`) — one page per project, **omit the handle**.
- **CUSTOM** — addressed by its path (the splat may contain slashes, e.g. `blogs/news`).
- **Templated** (`PRODUCT`, `COLLECTION`, `PAGE`, `BLOG`, `ARTICLE`) — keep a shared default template at the empty handle, so a **missing handle is rejected** (it won't silently edit the template). Pass the real handle.

**Locale always matters.** On reads/updates, always pass a real `locale` code (from List languages). In list-pages responses, a row's `locale` may be `null` for market-first projects (rows are keyed by market, not locale) — don't echo `null` back; pass a real code and let resolution map it to the market (e.g. `locale=en-us` resolves market `us`).

See `references/endpoints.md` for the full endpoint list, query params, and response shapes.

## Upload resources to Shopify

The Content API itself has no upload endpoint. To get media into a Weaverse item, upload it to Shopify first, then reference the returned CDN URL.

Upload goes through the **Weaverse Shopify proxy**, which accepts the same Weaverse token:

```
POST https://studio.weaverse.io/api/admin-graphql
Authorization: Bearer <WEAVERSE_API_KEY>
Content-Type: application/json
```

The body is a normal Shopify Admin GraphQL request (`{ "query": "...", "variables": {...} }`). Upload is the standard two-step Shopify flow:

1. `stagedUploadsCreate` → get a `url` + `parameters` (a presigned target) and a `resourceUrl`.
2. Upload the file bytes to that staged `url` with the returned `parameters` (multipart POST, not through the proxy).
3. `fileCreate` with `originalSource: <resourceUrl>` → Shopify ingests it and returns the permanent CDN file.
4. Read back the file's `image.url` / `sources` and put that CDN URL into the Weaverse item `data` via the update workflow above.

Reference implementation in the builder repo: `app/backend/admin/file.server.ts` (`generateStagedUploadLinks` → `stagedUploadsCreate`, then `fileCreate`). When in doubt, mirror its mutations and field selections.

> Alternatively, when a connected Shopify MCP is available, its image-upload / `graphql_mutation` tools do the same job without the proxy. Use whichever is connected.

## Helper script

`scripts/weaverse_content_api.mjs` wraps auth and the common calls. It reads `WEAVERSE_API_KEY` from the environment.

```bash
export WEAVERSE_API_KEY=...

node scripts/weaverse_content_api.mjs projects
node scripts/weaverse_content_api.mjs languages <projectId>
node scripts/weaverse_content_api.mjs theme <projectId>
node scripts/weaverse_content_api.mjs pages <projectId> [type]
node scripts/weaverse_content_api.mjs page <projectId> <type> [handle] [locale]   # reads with ?locale
node scripts/weaverse_content_api.mjs update <projectId> <type> <handle> <patch.json>
node scripts/weaverse_content_api.mjs delete <projectId> <type> <handle...>
```

Use it to inspect a project quickly and to apply patch files. For anything the script doesn't cover, call the REST endpoints directly or read `openapi.json`.

## Red Flags

- **Trying to create a *project* via the API** — there is no create-project endpoint. Projects are created in Weaverse Builder; the API edits them.
- **Sending a new item id without a `type` in a PATCH** — unknown ids are created only when `type` is supplied; otherwise they land in `notFoundIds`. For `children` entries, each id must already be on the page or be created in the same request.
- **Patching an existing item without reading its id first** — you must target a real item id. Read the page first (with the right `locale`); the default `weaverse` read already includes every item `id`, so you do **not** need `?meta=true`. (Creating a *new* item is different: fresh id + `type`.)
- **Omitting `locale` on a page read/update** — with no `locale` the resolver only tries the empty locale and legacy `en-us`, so non-`en-us` or market-first projects return `PAGE_NOT_FOUND` even when the page exists. Always pass a real `locale` from List languages.
- **"My published edit is missing from the API" — silent wrong-locale page (not a 404).** Content is stored per locale (`PageAssignment` keyed by `projectId, locale, type, handle`). When a merchant edits/publishes with a market locale selected (e.g. `en-us`), the change saves to the `en-us` assignment, **not** the base locale `""`. Because `locale` defaults to `""`, a request like `…/pages/PRODUCT/default` (no `?locale`) can **succeed (200)** but return the base-locale assignment — a *different, often empty/stale* page — so the edit looks "missing" even though it published fine. This is distinct from `PAGE_NOT_FOUND`: the request works, it just returns the wrong locale's page. Fix: always pass `?locale=<market>` (e.g. `en-us`). To find which locale a product/page uses: Studio top-bar template dropdown (shows active template + "Assigned to N products") with the market/locale selector beside it; or `GET /pages` (locale per row); or read `data-weaverse-template-id` from the live storefront HTML. Verified live on a market-first project: the edit lived on `locale=en-us` (active, freshly published) while base `locale=""` was the stale page the no-locale call returned.
- **Echoing back `locale: null`** — list-pages rows can be `null` for market-first projects. Don't send `null`; pass a real code and let resolution map it to the market.
- **Adding `?meta=true` for normal edits** — it only affects `portable-text` reads (where it restores `_weaverse.id`). On a `weaverse`-format read it changes nothing.
- **Ignoring `notFoundIds` in the response** — it means your ids aren't on the resolved page (wrong page, wrong locale, or stale ids). Re-read with the right locale, don't retry.
- **Sending more than 100 items in one update** (or 500 targets in one delete) — chunk the request.
- **Editing a templated type with an empty handle** — rejected by design. Pass the real handle.
- **Hardcoding the token or using `?apiKey=`** — use `Authorization: Bearer` from an env var.
- **Replacing whole `data` objects** — updates shallow-merge. Send only changed fields; don't resend the entire `data` and risk wiping nested values you didn't read.
- **Putting a non-Shopify URL into a media field after "upload"** — finish the `fileCreate` step and use the returned Shopify CDN URL, not the staged/temporary `resourceUrl`.

## Related skills

- `generating-weaverse-project-json` — creates the import JSON that establishes the structure this API then updates. The item ids you patch here come from that JSON (or from a page read back with the right `locale`).
- `cloning-websites-to-weaverse` / `figma-to-weaverse` — produce the section plan that feeds the JSON generator.
