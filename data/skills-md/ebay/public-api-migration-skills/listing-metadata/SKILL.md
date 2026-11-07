---
name: listing-metadata
description: |
  Migration guidance for traditional listing metadata and product discovery to Taxonomy API, Sell Metadata APIs, Catalog API, Charity API, and compatibility or product metadata surfaces.

  Trigger when user mentions: GeteBayDetails/GetCategories/GetCategoryFeatures/GetCategoryMappings/GetSuggestedCategories; ProductDetails/findProducts/getProductDetails/addProducts; compatibility search or compatibility value operations; GetCharities; or asks "how do I migrate category metadata before listing".

  Covers 22 traditional operations including marketplace metadata, taxonomy, category policies, compatibility and catalog lookup, charity discovery, and many decommissioned metadata rows.
  Do NOT use for listing create, revise, or end flows or for order/account workflows.
---

# Listing Metadata Migration

Use this skill for pre-listing metadata and discovery work that happens before a seller creates or revises a listing.

It covers:
- site-level metadata formerly returned by GeteBayDetails
- category taxonomy and leaf-category discovery formerly handled by GetCategories
- category policy and feature lookups formerly handled by GetCategoryFeatures
- motors compatibility metadata and catalog-assisted product lookup flows
- charity discovery
- decommissioned or no-replacement product metadata operations

## When To Apply

Use this package when you need to:
- split one traditional metadata call into several REST lookups
- decide whether a traditional metadata capability has a usable replacement or only a fallback workflow
- confirm the required sequence for marketplace ID, category tree ID, and leaf-category dependent calls
- migrate motors compatibility lookups from Product Metadata Service calls to Sell Metadata or Taxonomy flows
- document decommissioned metadata calls without inventing replacements

## Key Migration Patterns

- `GeteBayDetails` is no longer a single broad metadata payload. Pull only the specific marketplace or shipping metadata you need from Sell Metadata and Taxonomy.
- `GeteBayDetails` should stay precise around `SiteDetails`: current source inventory and migration-guide evidence both keep `getDefaultCategoryTreeId` in scope, but the answer should frame it as the taxonomy bootstrap call for marketplace/category-tree identity, not as field-for-field parity for the full historical `SiteDetails` container.
- `GetCategories` becomes a taxonomy workflow: resolve the marketplace tree ID first, then retrieve the whole tree, a subtree, or suggestions as needed.
- `GetCategoryFeatures` splits across multiple Sell Metadata and Taxonomy endpoints. The modern flow is category-policy oriented instead of one monolithic feature blob.
- Compatibility and product metadata are split between Sell Metadata, Taxonomy, Catalog, and documented no-replacement outcomes.
- Many modern metadata methods depend on marketplace path parameters, category tree IDs, and leaf-category validation instead of SOAP headers and broad response containers.

## Recommended Workflow

1. Start in `INDEX.md` to identify the traditional operation status and target modern API family.
2. Use `INTENTS.md` when the task is workflow-oriented rather than operation-oriented.
3. Use `references/operation-mapping.md` for the canonical migration narrative and payload examples.
4. Check `rules/` before implementing category-policy, taxonomy, compatibility, or refresh logic.
5. Open `references/operations/` when you need source-backed traditional extracts, modern doc notes, or concrete request examples.

## Navigation

- `INDEX.md`: fast lookup table for every traditional operation in this domain
- `INTENTS.md`: task-oriented navigation for common migration jobs
- `references/operation-mapping.md`: full traditional-to-modern mapping reference
- `rules/category-taxonomy-sequencing.md`: marketplace and category-tree workflow rules
- `rules/category-policy-split-and-filters.md`: GetCategoryFeatures split rules and category filter constraints
- `rules/marketplace-metadata-refresh.md`: GeteBayDetails replacement and refresh guidance
- `rules/compatibility-catalog-charity.md`: compatibility, catalog, charity, and decommission fallback patterns

## Evidence Limits

- Public documentation coverage is incomplete for many Taxonomy and Sell Metadata operations in this domain.
- Where public documentation coverage is limited, the supporting modern `_doc.md` files in `references/operations/` intentionally stay limited to validated notes derived from the migration mapping and the reference material included in this package.
- Decommissioned and no-replacement operations remain visible in this package so migration planning does not silently drop them.

## Field-Level Details

Field-level request and response details and field-by-field mapping are not provided in this skill, even if explicitly requested. For field definitions, refer to the official eBay developer documentation page.
