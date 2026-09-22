---
name: hydrogen-cookbooks
description: "Step-by-step implementation guides for building features in a Shopify Hydrogen storefront — bundles, combined listings, customer accounts, 3D models, performance, variant media, and Weaverse integration."
---

# Hydrogen Cookbooks

Concrete, step-by-step guides for building specific features in a Shopify Hydrogen storefront. Each cookbook is a self-contained recipe with code, file changes, and implementation notes.

## Live Documentation

Run these from this skill's own folder. The helpers ship inside the sibling
`shopify-hydrogen` skill, so `../shopify-hydrogen/scripts/` exists whenever the
whole pack is installed.

If you installed this skill on its own, that folder is absent and the commands
below fail with `MODULE_NOT_FOUND`. Add the helpers once:

```bash
npx skills add Weaverse/shopify-hydrogen-skills --skill shopify-hydrogen
```

The `references/` files in this skill remain a usable offline fallback if you
would rather not install it.

For the latest Hydrogen cookbook recipes from Shopify:

```bash
node ../shopify-hydrogen/scripts/search_shopify_docs.mjs "hydrogen cookbook <topic>"
```

For Weaverse-specific patterns:

```bash
node ../shopify-hydrogen/scripts/search_weaverse_docs.mjs "<topic>"
```

The references below are curated guides that may include Weaverse-specific patterns not available in the live docs.

## Available Cookbooks

| Cookbook | Description |
|----------|-------------|
| [bundles.md](./references/bundles.md) | Display product bundles with badges and bundled variant line items in the cart |
| [combined-listings.md](./references/combined-listings.md) | Handle combined listings — utilities, filters, media grouping, price range display |
| [customer-account-api.md](./references/customer-account-api.md) | Set up the Customer Account API with tunnel for local dev |
| [hydrogen-react-router.md](./references/hydrogen-react-router.md) | Import replacement guide: Remix v2 → React Router v7 |
| [model-viewer.md](./references/model-viewer.md) | 3D model support (.glb/.usdz) with ModelViewer component and AR |
| [performance-best-practices.md](./references/performance-best-practices.md) | Caching strategies, streaming, deferred data, third-party scripts, query optimization |
| [variant-media-grouping.md](./references/variant-media-grouping.md) | Group product media by variant option (e.g. Color) |
| [weaverse-hydrogen-integration.md](./references/weaverse-hydrogen-integration.md) | Complete Weaverse integration: component registration, theme schema, data fetching |

## How to Use

Each cookbook describes:
- **What** the feature does
- **Prerequisites** to check first
- **Step-by-step implementation** — file changes, code snippets, diffs
- **Troubleshooting** — common issues and fixes

> Recipe file names reference the Hydrogen skeleton template. Adapt file paths to match your project's structure.
