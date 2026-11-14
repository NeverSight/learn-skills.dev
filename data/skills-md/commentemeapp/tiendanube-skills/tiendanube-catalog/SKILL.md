---
name: tiendanube-catalog
description: "Apply when writing code that reads or writes the catalog of a Tiendanube / Nuvemshop store through the Admin API: products, variants and their attributes, images, categories, stock and multi-location inventory (locations and inventory_levels), price tables, kits, custom fields and metafields, and localized fields such as name per language. Use for ERP or PIM catalog sync, bulk stock and price updates, variant reconciliation by SKU, or reviewing code that calls /products, /categories, /locations or /metafields."
license: MIT
compatibility: "Tiendanube / Nuvemshop Admin API, version 2025-03. Apps and integrations built by partners."
metadata:
  author: commente.me
  version: "0.1.0"
---

# Catalog: products, variants, stock and categories

## When this skill applies

Use this skill when code calls the catalog resources of the Admin API (`https://api.tiendanube.com/2025-03/{store_id}/...`, with `Authorization: Bearer <token>` and a `User-Agent` that identifies the app).

- Creating and updating products, variants, images and categories from an ERP, PIM or marketplace connector
- Keeping stock and prices in sync, in stores with one location or with Multiple Locations enabled
- Managing locations and their priority
- Reading kits, maintaining price tables (wholesale or B2B prices) and attaching app data with custom fields or metafields
- Reviewing a sync job that loses translations, writes stock to stale variant ids or hits `422` and `429`

Do not use this skill for:

- Operating a store by conversation (listing, publishing, adjusting stock from a chat): that is the official Admin MCP, not code
- Orders, fulfillment orders and invoices (use `tiendanube-orders-fulfillment`)
- Rendering products in a theme (use `tiendanube-themes`)
- Authentication, scopes and token handling (use `tiendanube-oauth-apps`)

## Decision rules

- Treat `name`, `description`, `handle`, `seo_title` and `seo_description` as objects keyed by language (`{"es": "...", "pt": "..."}`). The ERP guide allows a plain string `name` for single-language stores; send the object whenever the store has more than one language.
- A product has at most 3 attributes, with distinct names, and at most 1,000 variants. Each variant's `values` must have the same length and order as the product's `attributes`.
- A product created without variants still has one "virtual" variant. Price, stock, weight and dimensions live on that variant, so update it with `PUT /products/{product_id}/variants/{id}`, not with `PUT /products/{id}`.
- `PUT /products/{id}` rejects `variants` and `images` with `422` and applies nothing. Use the variant and image endpoints.
- Choose the variant endpoint by intent: `POST .../variants` adds one; `PUT .../variants/{id}` edits one; `PATCH .../variants` edits many existing ones without adding or removing; `PUT .../variants` replaces the whole collection (combinations missing from the body are deleted).
- For stock changes, use `POST /products/{id}/variants/stock` with `action: "replace"` or `"variation"`. A negative variation below zero leaves stock at 0 without an error.
- For bulk price and stock, use `PATCH /products/stock-price`: up to 50 variants per call across all products.
- Unlimited stock is `"stock": ""` on a variant (or `null` as the `value` of a `replace` on `/variants/stock`). `stock_management` is set by the platform and cannot be written.
- Use `visibility` (`visible`, `unlisted`, `hidden`) instead of `published` when you need to tell unlisted from hidden. Never send both on create or update.
- Paginate every list. `GET /products` returns 30 by default and accepts `per_page` up to 200; `ids` accepts up to 150 ids. Use `fields` (including dotted `variants.sku`) to shrink responses.
- `GET /categories` reads `sinceId`, `createdAtMin`, `createdAtMax`, `updatedAtMin`, `updatedAtMax` in camelCase. The snake_case spelling is ignored silently.
- Prefer variant custom fields when the merchant needs storefront filters; product custom fields cannot be used as filters. All three custom field APIs (product, variant, category) are on the path to deprecation in favor of the unstable Custom Fields API.
- Use metafields (namespaced key and string value, owners `Product`, `Product_Variant`, `Category`, `Page`, `Order`, `Customer`) for app-owned data, including fiscal metadata the API does not expose (NCM, CEST and similar native invoice fields are not readable or writable).
- Kits are read-only (`GET /kits/{id}`); merchants build them in the admin. Only single-variant products can be components.

## Hard constraints

### Constraint: Write stock per location when Multiple Locations is enabled

When the store has more than one active location, stock lives in `variant.inventory_levels[]`, one entry per `location_id`. `variant.stock` is only the sum, kept for backward compatibility and deprecated for writes.

**Why this matters**

If only `variant.stock` is sent, the platform updates the first inventory level, so a multi-location store ends up with all the ERP stock in one place. Sending `stock` both at variant level and inside a location ignores the variant-level value. Apps that keep writing `variant.stock` fail the automatic "multi inventory ready" approval, and merchants see a warning when adding a second location or installing the app.

**Detection**

A sync that writes `{"stock": n}` to variants without first calling `GET /locations`, or that reads `variant.stock` to decide per-warehouse availability.

**Correct**

```json
PUT /products/1234/variants/144
{
  "inventory_levels": [
    { "location_id": "01HXAMPLELOCATIONMAIN0000", "stock": 12 },
    { "location_id": "01HXAMPLELOCATIONSTORE000", "stock": 3 }
  ]
}
```

**Wrong**

```json
PUT /products/1234/variants/144
{ "stock": 15 }
```

Every `inventory_levels` element must carry `stock` (otherwise `422`), and an unknown `location_id` returns `422`. With a single active location, `location_id` can be omitted.

### Constraint: Resend every i18n field on PUT /categories/{id}

On `PUT /categories/{id}`, `name`, `description`, `handle`, `seo_title` and `seo_description` are replaced as a whole. Any of them left out is cleared in every language. Other fields are partial updates.

**Why this matters**

A request that only moves a category under a new `parent` or changes `visibility` silently wipes its handle and SEO texts, breaking URLs and search snippets.

**Detection**

A category update body built from a diff that contains `parent` or `visibility` but not the five localized fields.

**Correct**

```js
const current = await api.get(`/categories/${id}`);
await api.put(`/categories/${id}`, {
	name: current.name,
	description: current.description,
	handle: current.handle,
	seo_title: current.seo_title,
	seo_description: current.seo_description,
	parent: 16366393
});
```

**Wrong**

```js
await api.put(`/categories/${id}`, { parent: 16366393 });
```

### Constraint: Reconcile variant ids after attribute changes

When a merchant edits the attributes of a product in the admin, the platform rebuilds its variants under new ids, even when SKUs stay the same. Recreated variants can start with unlimited stock.

**Why this matters**

Writing stock or price to a stored variant id that no longer exists fails, and the new variants may be selling with unlimited stock until the integration restores quantities.

**Detection**

An integration that caches `variant_id` forever and never reloads the product on `product/updated`.

**Correct**

```js
// on product/updated
const product = await api.get(`/products/${productId}`);
for (const v of product.variants) {
	const local = mapping.findBySku(v.sku); // only when the SKU is present and unique
	if (local) mapping.updateVariantId(local, v.id);
	else mapping.flagForReview(productId, v.id);
}
```

**Wrong**

```js
await api.put(`/products/${productId}/variants/${cachedVariantId}`, { price: "19.90" });
```

### Constraint: Do not send published and visibility together

On `POST /products` and `PUT /products/{id}` send either `published` or `visibility`. Sending both returns `422`. Sending `published: false` maps to `hidden`, not `unlisted`.

**Why this matters**

`published: false` hides the product and makes its URL return 404. A connector that meant "keep it off listings but reachable by link" needs `visibility: "unlisted"`.

**Detection**

A product payload builder that always sets `published` and also copies `visibility` from the source system.

**Correct**

```json
{ "visibility": "unlisted" }
```

**Wrong**

```json
{ "published": false, "visibility": "unlisted" }
```

### Constraint: Keep categories when updating a product

On `PUT /products/{id}`, an empty `categories` array removes every category from the product. Omit `categories` to keep them, or send the full list you want.

**Why this matters**

A partial update that serializes an empty array by default unassigns the product from every category and it disappears from category pages.

**Detection**

`categories: []` in a product update body when the source record has no category data.

**Correct**

```json
{ "id": 5123, "categories": [4567, 4568] }
```

**Wrong**

```json
{ "id": 5123, "brand": "Acme", "categories": [] }
```

## Preferred pattern

A catalog sync for an ERP, keyed by SKU:

```text
1. GET /locations                      -> location ids and priorities
2. GET /products?updated_at_min=...&per_page=200&fields=id,name,variants.id,variants.sku
3. For each ERP item:
   - not in store  -> POST /products with name per language, attributes, variants, up to 9 images
   - in store      -> PUT /products/{id} for product fields only
                     PATCH /products/{id}/variants for many variants
                     POST /products/{id}/images for more images (max 250 per product)
4. Stock and price -> PATCH /products/stock-price in chunks of 50 variants,
                      with inventory_levels[].location_id when locations > 1
5. Webhooks product/updated, category/deleted -> reload and reconcile
6. Periodic full sync to catch missed events
```

Chunking bulk stock and price:

```js
const chunks = splitVariants(updates, 50); // the endpoint accepts at most 50 variants per call
for (const chunk of chunks) {
	const res = await api.patch("/products/stock-price", chunk);
	if (res.status === 429) await backoff(); // weighted token bucket: smaller payloads cost fewer tokens
}
```

Images: each must be under 20 MB and 100 megapixels, in gif, jpg, png or webp. Send exactly one of `src`, `attachment` (Base64), `image_id` (from `POST /products/images`, useful to reuse one upload) or `store_media_uuid`. Set alt text with `seo: {"es": {"alt": "..."}}` only once per language; sending it again for a language that already has alt text returns `500`. Images may be served as WebP; check `Content-Type` before forwarding them.

Locations: `PATCH /locations/priorities` sets the order used to pick stock at checkout (priority 0 becomes default) and affects shipping origin and cost. A location can be deleted only if it has no inventory levels and is not the default. Scopes are `read_locations` and `write_locations`.

Price tables: resolution goes variant exception (fixed `price` wins over `discount`), then category exception, then `default_discount`. IDs are strings in bodies. Adding customers is append-only, up to 10,000 per request, and a customer already linked to any table makes the whole batch fail with `409`.

Extra preparation days per variant: a metafield with `namespace: "shipping_rules"`, `key: "additional_days"`, `owner_resource: "Product_Variant"`.

## Common failure modes

- Sending `PUT /products/{id}/variants` with only the variants that changed: every combination not in the body is deleted.
- Sending repeated value combinations: `422` "Variants cannot be repeated" (the `PATCH` error lists `duplicate_variant_ids`).
- Expecting `POST /products/custom-fields` to fail when a list value is duplicated: it returns `201` and marks that value `created: false` with an `error`. Check each value.
- `PUT /products/{id}/custom-fields/values` overwrites the associations; send `value: null` to remove one. Only fields created by your app can be deleted.
- Using `created_at_min` filters on `GET /products/{id}/images`: they return `400`.
- Reading `parent` as `null` for top-level categories: the category resource returns `0`.
- A `hidden` category cannot contain `visible` subcategories; `soft-hidden` is inherited and cannot be set.
- Creating more than the plan allows: `402 Payment Required` (product limit of plan) or `422` (store limit of 100,000 products, 1,000 categories).
- Variant `cost`, when sent, must be greater than 0; `age_group` and `gender` only accept the documented values.
- Large variant payloads with many translations and inventory levels consume more rate-limit tokens and trigger `429`; split them.

## Review checklist

- [ ] Localized fields are sent as language-keyed objects matching the store's languages
- [ ] Attributes are at most 3, unique by name, and every variant has matching `values`
- [ ] Stock writes use `inventory_levels` with `location_id` when the store has several locations
- [ ] Category updates resend the five i18n fields; product updates never send empty `categories` by accident
- [ ] `published` and `visibility` are never sent together
- [ ] Variant ids are reconciled after `product/updated`, matching by SKU only when unique
- [ ] Bulk updates are chunked (50 variants for stock-price) and back off on `429`
- [ ] Lists are paginated, filters use camelCase on `/categories`
- [ ] Custom field responses are checked per value; app data that has no native field uses metafields

## Related skills

- `tiendanube-rest-api`: base URL, headers, pagination and rate limits shared by every resource
- `tiendanube-oauth-apps`: scopes such as `write_products` and `read_locations`
- `tiendanube-webhooks`: `product/*`, `category/*` and `location/*` events that trigger re-syncs
- `tiendanube-orders-fulfillment`: stock reserved and returned by orders and fulfillment orders
- `tiendanube-erp-integration`: end-to-end ERP flows that combine catalog, inventory and orders
- `tiendanube-themes`: how products, kits and custom fields reach the storefront

## Reference

- [Product](https://nuvemshop.dev/en-US/api/resources/2025-03/product.md): properties, visibility, list filters and limits, sparse fieldsets, rejected fields on PUT, stock-price bulk endpoint, attribute and variant limits, unlimited stock, variant id recreation
- [Product Variant](https://nuvemshop.dev/en-US/api/resources/2025-03/product-variant.md): variant fields, single, batch PUT and PATCH semantics, stock endpoint actions, additional_days metafield, weighted rate limiting
- [Product Image](https://nuvemshop.dev/en-US/api/resources/2025-03/product-image.md): image restrictions, upload sources, alt text via seo, temporary image ids
- [Category](https://nuvemshop.dev/en-US/api/resources/2025-03/category.md): camelCase filters, i18n fields cleared on PUT, parent and visibility rules
- [Location](https://nuvemshop.dev/en-US/api/resources/2025-03/location.md): scopes, priorities, default location, deletion rules, location webhooks
- [Kit](https://nuvemshop.dev/en-US/api/resources/2025-03/kit.md): read-only kits, price and stock calculation, components
- [Metafields](https://nuvemshop.dev/en-US/api/resources/2025-03/metafields.md): owner resources, namespace and key format, endpoints
- [Product Custom Fields](https://nuvemshop.dev/en-US/api/resources/2025-03/products/custom-fields.md): value types, partial 201 responses, association overwrite, deprecation notice, no filters
- [Product Variant Custom Fields](https://nuvemshop.dev/en-US/api/resources/2025-03/products/variants/custom-fields.md): variant fields usable as storefront filters
- [Category Custom Fields](https://nuvemshop.dev/en-US/api/resources/2025-03/categories/custom-fields.md): category custom field endpoints
- [Product Price Tables](https://nuvemshop.dev/en-US/api/resources/2025-03/products/price-tables/price-tables.md): price resolution order, exceptions, customer association limits and 409
- [Multi inventory: products](https://nuvemshop.dev/en-US/api/guides/multi-inventory/products.md): inventory_levels per endpoint, fallback to the first location, 422 cases
- [Multi inventory overview](https://nuvemshop.dev/en-US/api/guides/multi-inventory/multi-inventory.md): deprecated stock parameter, automatic read_locations scope, multi inventory ready approval
- [ERP guide: catalog overview](https://nuvemshop.dev/en-US/apps/erp-guide/catalog/overview.md): plain string name for single-language stores
- [ERP guide: products](https://nuvemshop.dev/en-US/apps/erp-guide/catalog/products.md): products with and without variation, attributes and values
- [ERP guide: categories](https://nuvemshop.dev/en-US/apps/erp-guide/catalog/categories.md): sync with updatedAtMin, category/deleted webhook and periodic full sync
- [ERP guide: custom fields](https://nuvemshop.dev/en-US/apps/erp-guide/catalog/custom-fields.md): variant custom field operations for ERPs
- [ERP guide: inventory](https://nuvemshop.dev/en-US/apps/erp-guide/inventory.md): locations as stock points and the effect of priority on shipping
- [Admin MCP](https://nuvemshop.dev/en-US/ai-agents/admin-mcp.md): conversational store operation, out of scope for code
