---
name: generating-weaverse-project-json
description: Use when generating Weaverse project export JSON for import into the Weaverse editor. Triggers on requests to create, build, or produce a Weaverse project JSON file from a site migration, design spec, page layout description, or existing export. Also use when converting section plans into importable project and pages data.
---

# Generating Weaverse Project JSON

Generate valid, import-ready Weaverse project export JSON files.

## Overview

This skill produces JSON files that conform to the Weaverse import contract. It works independently — you can use it from a site migration, a design spec, a verbal description, or any other input that describes what pages and sections should exist.

The output is a single JSON file matching the schema in `references/project-json-schema.md`, with a real-world example in `references/demo.json`.

## Inputs

This skill accepts any of these as input:

- **Section mapping** from `cloning-websites-to-weaverse` (website migration flow)
- **Section mapping + token table** from `figma-to-weaverse` (Figma design flow)
- **Design spec** describing pages, sections, and content
- **Verbal description** of what the storefront should look like
- **Existing export** to modify or extend

The only hard requirement: you need to know which section types to use. Read `app/weaverse/components.ts` to get the list of registered sections and blocks.

## Delivery

This skill produces an **import JSON** that establishes the project structure — pages, sections, and initial content. That JSON is **imported once** into the Weaverse Studio editor to create the project.

After the structure exists, ongoing content edits (copy, images, localization, bulk updates) should go through the **`weaverse-content-api`** skill, not by re-importing. The Content API can only update items that already exist, so the import-then-update split matters: use this skill to create structure, `weaverse-content-api` to maintain it. Keep the item ids stable between the two.

## Generation Steps

1. **Read references** — load `references/project-json-schema.md` for the contract and `references/demo.json` for a complete real-world example
2. **Identify registered types** — read `app/weaverse/components.ts` to know which section and block types are available
3. **Read section source code** — for each section type you plan to use, read its source in `app/sections/` or `app/components/` to learn valid schema fields, enum values, and defaults
4. **Build the JSON** following the structure below
5. **Run the validator** — execute `python scripts/validate.py <output-file>` to catch structural errors
6. **Fix any issues** the validator reports, then re-run until clean

## JSON Structure

### Top-level

```json
{
  "version": "1.0.0",
  "exportedAt": "<ISO timestamp>",
  "project": { "name": "<name>", "config": {} },
  "pages": [],
  "pageAssignments": []
}
```

### project.config

Contains theme settings, locale, and colors. Accepted keys:

| Key | Type | Purpose |
|-----|------|---------|
| `previewHost` | string | Dev server URL, usually `http://localhost:3456` |
| `theme` | object | Storefront-wide design tokens (colors, typography, layout) |
| `defaultLocale` | object | `{ label, language, country, currency, pathPrefix }` |
| `recentColors` | string[] | Editor color picker recent colors |

For `theme`, refer to `references/demo.json` → `project.config.theme` for the full set of valid keys. Key categories:

- **Colors**: `colorPrimary`, `colorText`, `colorBackground`, `colorLine`, `colorTextSubtle`, `colorLineSubtle`, `colorTextInverse`, `colorForeground`
- **Typography**: `bodyBaseSize`, `bodyBaseLineHeight`, `bodyBaseSpacing`, `h1BaseSize`, `headingBaseLineHeight`, `headingBaseSpacing`
- **Layout**: `pageWidth`, `footerWidth`, `headerWidth`, `navHeightDesktop`, `navHeightTablet`, `navHeightMobile`
- **Header/Footer**: `headerBgColor`, `headerText`, `footerBgColor`, `footerText`, `topbarBgColor`, `topbarTextColor`, `topbarHeight`
- **Buttons**: `buttonPrimaryBg`, `buttonPrimaryColor`, `buttonSecondaryBg`, `buttonSecondaryColor`, `btnCornerRadius`
- **Product cards**: `pcardAlignment`, `pcardImageRatio`, `pcardBorderRadius`, `pcardShowVendor`, `pcardShowReviews`, `pcardShowSalePrice`, etc.
- **Badges**: `newBadgeText`, `newBadgeColor`, `saleBadgeText`, `saleBadgeColor`, `soldOutBadgeText`, `soldOutBadgeColor`, `bestSellerBadgeText`, `bestSellerBadgeColor`
- **Social**: `socialFacebook`, `socialInstagram`, `socialLinkedIn`, `socialX`
- **Newsletter**: `newsletterTitle`, `newsletterDescription`, `newsletterButtonText`, `newsletterPlaceholder`, `newsletterPopupEnabled`, etc.

Only include theme keys you understand and intend to set. Do not copy the entire demo theme blindly.

### Pages

Each page has `id`, `name`, `rootId`, and a flat `items` array:

```json
{
  "id": "b98mnnqmv3tmce7wmw3l7vw4",
  "name": "Homepage",
  "rootId": "019b917a-f48f-72d4-aee7-3b1eae6b7dca",
  "items": [
    { "id": "019b917a-f48f-72d4-aee7-3b1eae6b7dca", "type": "main", "data": {}, "children": [{ "id": "019b917a-f48f-72d4-aee7-3b1f5ca586c1" }] },
    { "id": "019b917a-f48f-72d4-aee7-3b1f5ca586c1", "type": "hero-image", "data": { "height": "small" }, "children": [{ "id": "019b917a-f48f-72d4-aee7-3b22cd55e21b" }] },
    { "id": "019b917a-f48f-72d4-aee7-3b22cd55e21b", "type": "heading", "data": { "content": "Welcome" }, "children": [] }
  ]
}
```

Key rules:
- **Flat items** — all items live in the `items` array, hierarchy is expressed through `children` id-references
- **One root `main` item** per page — its id must match `rootId`
- **`children`** is REQUIRED on every item — use `[]` for leaf items, `[{ "id": "<item-id>" }]` for parents
- **`data`** is REQUIRED on every item — use `{}` when no non-default values are needed
- **`type`** must be a registered section or block type from `app/weaverse/components.ts`

**CRITICAL:** The Weaverse importer expects both `data` and `children` to be present on EVERY item. Omitting them causes silent import failures (empty page renders). Always include `"data": {}` and `"children": []` even when empty.

### Page Assignments

Maps pages to routes:

```json
{ "pageId": "b98mnnqmv3tmce7wmw3l7vw4", "type": "INDEX", "handle": "", "locale": "en-us" }
```

Common types: `INDEX`, `PRODUCT`, `COLLECTION`, `ALL_PRODUCTS`, `COLLECTION_LIST`, `PAGE`, `BLOG`, `ARTICLE`, `CUSTOM`.

For `CUSTOM` pages, set `handle` to the route slug (e.g., `"reseller"`). For standard template pages, `handle` is usually empty `""`.

### Template page stubs

Standard pages (product, collection, blog, article) that aren't being customized should be empty stubs:

```json
{
  "id": "qa8xa47ou35atbo1ik4w7v6y",
  "name": "Default product",
  "rootId": "019b917a-f490-794d-95d0-82a578d7cdfc",
  "items": [{ "id": "019b917a-f490-794d-95d0-82a578d7cdfc", "type": "main", "data": {}, "children": [] }]
}
```

## Data Value Rules

### Only use verified enum values

Before writing any `select`, `toggle-group`, or `position` value, read the section source code. Common mistakes:

| Wrong | Correct | Field |
|-------|---------|-------|
| `"custom"` | `"small"`, `"medium"`, `"large"`, `"full"` | height |
| `"stretch"` | `"full"`, `"fixed"` | width |
| `"right"` / `"left"` | `"start"`, `"end"` | desktopMediaPosition |
| `"white"` / `"black"` | `"light"`, `"dark"` | arrowsColor |

### Only include non-default values

If a field matches the schema default, omit it. The Weaverse editor strips defaults on save. Including them creates noise.

### Shopify entity references

Collections and products use object format, not bare strings:

```json
// Collections
"collections": [{ "id": 456905851102, "handle": "covers" }]

// Products
"product": { "id": 123456789, "handle": "my-product" }
```

If real Shopify IDs are unknown, omit the field or use `[]`. Do not invent fake IDs.

### Image fields

External images use a bare URL string. Shopify-hosted images use the media object:

```json
// External
"backgroundImage": "https://example.com/image.jpg"

// Shopify media
"backgroundImage": {
  "id": "gid://shopify/MediaImage/12345",
  "url": "https://cdn.shopify.com/...",
  "width": 1920, "height": 1080, "altText": "Description"
}
```

## ID Format Rules

Page IDs and item IDs use different formats:

| Entity | Format | Example |
|--------|--------|---------|
| **Page `id`** | CUID (25-char alphanumeric) | `b98mnnqmv3tmce7wmw3l7vw4` |
| **Item `id`** (and `rootId`) | UUID v7 (hyphenated) | `019b917a-f48f-72d4-aee7-3b1eae6b7dca` |

Integrity rules:
- Every page `id` must be unique across the export
- Every item `id` must be unique across the export
- `rootId` must match the root `main` item's `id` exactly
- Every child reference must point to an existing item in the same page
- Page IDs are CUIDs — use a CUID generator or produce 25-char lowercase alphanumeric strings
- Item IDs are UUIDs — use UUID v7 format (timestamp-sortable, hyphenated)

## Validation

After generating the JSON, run the bundled validator:

```bash
python scripts/validate.py <path-to-output.json>
```

The validator checks:
- Valid JSON structure
- Required top-level fields present
- Every page has `id`, `name`, `rootId`, `items`
- Every `rootId` resolves to an item with `type: "main"`
- Every item has `data` and `children` fields (both required)
- No duplicate item IDs
- All child references resolve to existing items within the same page
- All `pageAssignment.pageId` values resolve to existing pages

Fix any reported errors and re-run until clean. Do not deliver JSON that fails validation.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `data` or `children` on items | Both are REQUIRED on every item — use `"data": {}` and `"children": []` even when empty |
| Nesting full items inside `children` | Use `{ "id": "..." }` references only |
| `rootId` doesn't match any item | Ensure root `main` item's id equals `rootId` |
| Using unregistered section types | Read `app/weaverse/components.ts` first |
| Duplicate IDs | Page IDs = CUIDs, item IDs = UUIDs — every id must be unique |
| Including default values in `data` | Omit fields that match schema defaults |
| Guessing enum values | Read the section source for valid options |
| Copying entire demo theme blindly | Only include keys you understand and intend |
| Missing `pageAssignments` | Every page needs a route assignment |
| Fake Shopify IDs | Omit unknown IDs, let user select in editor |
