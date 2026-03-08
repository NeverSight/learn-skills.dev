---
name: wix-stores-versioning
description: "Handle Wix Stores Catalog V1 and V3 SDK compatibility. Use when building any integration that interacts with Wix Stores products, inventory, orders, or collections. Triggers include Wix Stores, products API, inventory API, catalog version, productsV3, V1 vs V3, store products, queryProducts, getProduct."
compatibility: Requires Wix CLI development environment.
---

# Wix Stores Catalog Versioning

Wix Stores has two catalog versions that are **NOT backwards compatible**:

| Version | Status |
|---------|--------|
| **V1_CATALOG** | Legacy (e.g., `products`, `inventory`) |
| **V3_CATALOG** | Current (e.g., `productsV3`, `inventoryItemsV3`) |

V3 modules typically have a `V3` suffix. Use Wix MCP to search for the specific module you need.

## Core Pattern

Always check catalog version before any Stores operation:

```typescript
import { catalogVersioning, products, productsV3 } from '@wix/stores';

async function getProducts() {
  const { catalogVersion } = await catalogVersioning.getCatalogVersion();

  if (catalogVersion === 'STORES_NOT_INSTALLED') {
    return [];
  }

  if (catalogVersion === 'V3_CATALOG') {
    // Use V3 module
    const result = await productsV3.queryProducts().limit(10).find();
    return result.items;
  }

  // Use V1 module
  const result = await products.queryProducts().limit(10).find();
  return result.items;
}
```

## Required Permissions

**Always look up permissions for each API method you use:**

1. Search for the method using `SearchWixRESTDocumentation`
2. Read the full docs with `ReadFullDocsArticle` to get the required permissions
3. Return the required permissions to the user

## Key Rules

- Call `getCatalogVersion()` at the start of each flow
- Catalog version is permanent per site (won't downgrade from V3 to V1)
- V1 and V3 have different payload structures — field names, nesting, and types differ
- Subscribe to both V1 and V3 webhooks to handle all sites

## Finding SDK Details

**Use MCP tools to search for version-specific documentation:**

- `SearchWixRESTDocumentation` - Search for methods and permissions
- `ReadFullDocsArticle` - Read full documentation when needed

**Search queries** (results show both V1 and V3 namespaces):
- `"getCatalogVersion"` → permissions and usage
- `"createProduct"` → `productsV3` (V3) and `products` (V1)
- `"queryProducts"` → `productsV3` (V3) and `products` (V1)
- `"getInventoryItem"` → `inventoryItemsV3` (V3) and `inventory` (V1)

**Important:** After finding the method, use `ReadFullDocsArticle` to get the full documentation including required permissions. Return them to the user.

## API Differences Reference

V1 and V3 have different field structures. For field mapping, see:
[Catalog V1 to V3 Migration Guide](https://dev.wix.com/docs/api-reference/business-solutions/stores/catalog-v3/catalog-v1-to-v3-migration-guide?apiView=SDK)

