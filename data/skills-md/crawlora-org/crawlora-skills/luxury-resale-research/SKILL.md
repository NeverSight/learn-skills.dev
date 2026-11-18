---
name: luxury-resale-research
description: Research luxury-fashion and watch resale listings, sold evidence, condition, and seller signals across specialist marketplaces. Use for sourcing or evidence comparison, not buying or appraisal.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Luxury resale research

Research public, read-only marketplace data for luxury fashion, handbags,
watches, sneakers, and streetwear. Use this skill when the user needs current
asks, sold comparables where the source exposes them, listing-level condition,
or seller/dealer context across luxury resale sources. It complements the broad
`resale-secondhand-research` skill; use this one when specialist luxury sources
or a disciplined evidence comparison matters.

## Tool scope and data flow

The optional shell helper is the only command this skill asks to run. It makes
GET requests only to the documented, allowlisted Crawlora routes. When invoked,
it reads `CRAWLORA_API_KEY` and sends it as an `x-api-key` header over HTTPS to
`api.crawlora.net`; it does not send the key to marketplace sites. It briefly
writes a mode-600 curl config under `TMPDIR` and removes it when the command
exits. It does not inspect other environment variables, enumerate files, install
software, or run with elevated privileges. Run it only when you want to make a
Crawlora API request; successful requests can consume credits.

Do not place orders, make offers, authenticate an item, estimate an appraisal,
claim a purchase total, or imply that a platform's condition label proves
authenticity. Do not infer fees, duties, shipping, or currency conversion when
the selected public response does not state them.

## Evidence workflow

1. Define the comparability key first: brand, model/reference or style ID,
   material/color, size, condition, and region/currency where present. Search
   active and sold datasets separately; an asking price is not sale evidence.
2. Discover opaque filters before searching. Use each platform's directory,
   categories, conditions, brands, models, or facets endpoint rather than
   guessing ids, slugs, or values.
3. Pull a compact active set, then fetch detail only for credible matches.
   Keep source URL/path and the retrieval time for every record. Follow only
   the source's cursor/page limit; narrow the query instead of deep paging.
4. Report separate fields for: **active asks**; **sold evidence** (sale price
   and sale date only where the endpoint supplies both); **condition and
   authentication signals** (source-stated, never independently verified);
   **fees/shipping/duties** (stated amount or `not provided`); **currency**;
   and **source timestamp** (listing/sale date if supplied, plus retrieval
   time). Do not pool currencies or condition grades without labeling the
   normalization assumption.
5. State evidence gaps plainly. Current inventory, recommendation rails,
   seller reputation, and marketplace-wide counts are useful context, not a
   transaction record or authenticity determination.

## Source map

Use the exact routes and parameter names below. All are `GET` public-data
reads. Braces identify a path parameter; all others are query parameters.

### Core luxury sources

- **The RealReal:** discovery: `therealreal_autocomplete` (`/therealreal/autocomplete`,
  `term`), `therealreal_categories`, `therealreal_conditions`,
  `therealreal_collections`, and `therealreal_designers` (`category`). Search:
  `therealreal_search` (`/therealreal/search`, required `query`; optional
  `category_id`, `designer_id`, `condition_id`, `price_from`, `price_to`,
  `on_sale`, `available`, `after`). Browse: `therealreal_category` (`path`,
  `on_sale`, `available`, `after`), `therealreal_designer` (`slug`, `on_sale`,
  `available`, `after`), and `therealreal_collection` (`slug`, `after`). Detail:
  `therealreal_listing` (`url`) and `therealreal_similar` (`product_id`).
  Reuse `next_after` exactly as returned.
- **Fashionphile:** discovery/catalog: `fashionphile_collections` and
  `fashionphile_products` (`page`, `limit`; default 50, maximum 250), plus
  `fashionphile_sitemaps` and `fashionphile_sitemap_urls` (`type`, `limit`).
  Search: `fashionphile_search` (`/fashionphile/search`; `q`, `condition`,
  `availability`, `vendor`, `sort`, `page`, `limit`; default 20, maximum 50).
  Use `availability=sold` specifically for its sold archive; `available` is
  the default and `all` is also accepted. Details: `fashionphile_product`
  (`handle`) and `fashionphile_product_recommendations` (`handle`, `intent`,
  `limit`; default 10, maximum 20; `intent` is `related` or `complementary`).
  Collection and static-page reads use `fashionphile_collection_products`
  (`handle`, `page`, `limit`), `fashionphile_pages` (`page`, `limit`), and
  `fashionphile_page` (`handle`); suggestions use
  `fashionphile_search_suggest` (`q`, `types`, `limit`; maximum 20).
- **Rebag:** use the same public storefront pattern with only Rebag routes:
  `rebag_search` (`/rebag/search`; `q`, `sort`, `page`, `limit`),
  `rebag_product` (`handle`), `rebag_product_recommendations` (`handle`,
  `intent`, `limit`), `rebag_products` and `rebag_collections` (`page`,
  `limit`; default 50, maximum 250), `rebag_collection_products` (`handle`,
  `page`, `limit`), `rebag_search_suggest` (`q`, `types`, `limit`; maximum
  20), `rebag_sitemaps`, `rebag_sitemap_urls` (`type`, `limit`), `rebag_pages`
  (`page`, `limit`), `rebag_page` (`handle`), and `rebag_store`.
- **Vestiaire Collective:** discovery: `vestiaire_brands`,
  `vestiaire_categories`, and `vestiaire_conditions`. Search:
  `vestiaire_search` (`/vestiaire/search`; `q`, `brand_id`, `category_id`,
  `condition_id`, `sort`, `page`, `per_page`). `per_page` is at most 60 and
  `page * per_page` must not exceed 1000; use the returned directory IDs.
  Detail/context: `vestiaire_product` (`path`), `vestiaire_search_sellers`
  (`q`), `vestiaire_seller` (`id`), and `vestiaire_suggest` (`q`).
- **Grailed:** discover filters with `grailed_categories` and designers with
  `grailed_designers` (`q`, `page`, `limit`); curated browse is
  `grailed_collections` then `grailed_collection` (`id`). Use
  `grailed_search` for active asks and `grailed_sold_listings` for sold
  evidence. Both accept `q`, `designer`, `department`, `category`, `size`,
  `color`, `condition`, `min_price`, `max_price`, `sort`, `page`, and `limit`;
  price filters mean final sold price on the sold route. Detail/context:
  `grailed_listing` (`id`), `grailed_similar_listings` (`id`, `limit`),
  `grailed_seller` (`username`, `page`, `limit`), `grailed_seller_reviews`
  (`username`, `page`), and `grailed_suggest` (`q`).
- **Chrono24:** discover `chrono24_brands`, then `chrono24_models` (`brand`),
  and `chrono24_facets` (`group`) before advanced filters. Search with
  `chrono24_search` (`/chrono24/search`; at least `query` or `brand`; optional
  `model`, `sort`, `page`, `page_size`, `condition`, `used_or_new`,
  `case_material`, `dial_color`, `bracelet_material`, `movement_type`,
  `gender`, `watch_type`, `stock_info`). The UI page sizes are 30, 60, or 120.
  Use `chrono24_listing` (`path`) for the reference number, specifications,
  price/currency, condition, seller type, and location; dealer context is
  `chrono24_dealer` (`slug`) and `chrono24_dealer_reviews` (`slug`, `page`,
  `page_size` 1–50, `min_stars` 0–5, `sort`). Suggestions:
  `chrono24_autocomplete` (`query`).

### Adjacent resale benchmarks

Use these only when they improve the requested comparison; do not substitute a
streetwear marketplace for a luxury-listing comparable without saying so.

- **Depop:** `depop_search` (`query` plus `brand_ids`, `category`,
  `subcategory`, `condition`, `colours`, `sizes`, `gender`, `is_kids`,
  `on_sale`, `price_min`, `price_max`, `sort`, `after`); discover with
  `depop_brands`, `depop_categories`, `depop_sizes`, and
  `depop_search_facets` (`query`). Detail/shop: `/depop/item/{slug}`,
  `/depop/item/{slug}/similar` (`after`, `limit`, up to 150),
  `depop_search_sellers` (`query`), and `/depop/shop/{username}` with the
  compatible filters. Suggestions: `depop_suggest` (`query`).
- **Poshmark:** use `poshmark_brands` and `poshmark_categories` for discovery;
  active browse/search is `poshmark_search` (`query`, `department`, `max_id`),
  `/poshmark/brand/{name}` (`max_id`), or `/poshmark/category/{path}`
  (`max_id`). Details are `/poshmark/listing/{id}`; seller context is
  `/poshmark/closet/{username}` (`max_id`). Reuse `next_max_id` exactly.
- **GOAT and StockX:** use product detail for market context, not a confirmed
  sale comp unless the response explicitly provides a last-sale field.
  `goat_search` supports `query`, facets, `page`, and `limit`; discover with
  `goat_search_facets`, `goat_countries`, and `goat_curated`; detail is
  `/goat/product/{slug}` (`country_code`). `stockx_search` supports `category`,
  `query`, facet filters, `page`, and `limit`; discover `stockx_categories` and
  `stockx_brands`; detail is `/stockx/product/{slug}`. `stockx_releases`
  (`from`, `page`, `limit`) is a release calendar, not resale history.

## Reporting shape

For a comparison, return a compact table or JSON list with one row per source
listing and include `source`, `listing_url_or_path`, `status` (`active`,
`sold`, or `market_context`), `price`, `currency`, `condition_text`,
`authentication_signal`, `seller_or_dealer_signal`, `sale_date`,
`fees_shipping_duties`, `source_timestamp`, and `retrieved_at`. Leave an
unsupported field null or label it `not provided`; never fill it with an
estimate. Keep active asks and sold evidence in separate summaries before any
user-requested comparison.
