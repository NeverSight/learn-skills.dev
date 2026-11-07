---
name: xbox-research
description: Research Xbox game listings, regional prices, compatibility, accessibility features, curated collections, subscription inclusion, and review samples through Crawlora. Use to shortlist Xbox or PC games or compare editions and Game Pass catalog evidence without purchases.
---

# Xbox game research

## Access and contract

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the named Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact tool names, methods,
and parameters. Check application `code` as well as HTTP status; payloads are
inside `data`. Stop on authentication errors, back off on `429`, and retry a
transient upstream failure once. Bound pages and calls by the requested scope
and credit budget. Preserve source URLs, identifiers, and collection times.

Build a game shortlist from Xbox's public catalog, detail, and review surfaces.

## Match the requested platform and edition

1. Establish locale, device/platform, genre, accessibility needs, and whether the
   user wants purchase offers or subscription inclusion. Use `xbox_search` or
   `xbox_browse`, then resolve the returned 12-character alphanumeric `product_id`.
2. Fetch `xbox_game` for selected candidates. Keep base games, bundles, add-ons,
   preorder editions, and subscriptions separate. Xbox and Microsoft Store share
   StoreId format, but a shared format alone does not prove two records are the
   same edition; verify returned title and product kind.
3. Use only documented browse filters. Repeat array query keys for multiple
   values (for example `genre=Shooter genre=Strategy`), and copy opaque pagination
   cursors from responses. Curated `xbox_collection` IDs are a closed documented
   set, not arbitrary genres or guessed subscription identifiers.
4. Preserve `available_on`, accessibility evidence, currencies, locale, price
   basis, and `included_with_subscription_ids` when returned. An inclusion ID is
   evidence from the current catalog, not proof the user owns that subscription
   or that every edition is included in every region.
5. Sample reviews only for the chosen product. Preserve review date/rating where
   available and distinguish the sample from the aggregate rating.

```sh
scripts/crawlora.sh /xbox/search query="Forza" locale=en-US
scripts/crawlora.sh /xbox/collection id=XboxPlayAnywhere locale=en-US
# Use a returned StoreId, for example:
# scripts/crawlora.sh /xbox/game product_id="$PRODUCT_ID" locale=en-US
# scripts/crawlora.sh /xbox/reviews product_id="$PRODUCT_ID"
```

## Deliver a usable shortlist

Show edition/product ID, compatible devices, price/currency, subscription
inclusion evidence, accessibility attributes, review sample size, source URL,
and collection time. Missing attributes are unknown rather than unsupported.
A listed feature or store availability is not a guarantee of performance on the
user's hardware. Trailers may be HLS manifests; link only usable returned media
rather than inventing downloadable files. No purchase, installation, sign-in,
or subscription change is part of this workflow.
