---
name: saleor-domain
description: "Saleor e-commerce entity types, relationships, and identifier rules. Use before answering any question about Saleor entities, how they connect, identifier rules (slug vs name), channels, or what Configurator manages."
license: MIT
metadata:
  author: saleor
  version: 2.0.0
  requires: "@saleor/configurator CLI"
---

# Saleor Domain Knowledge

## Overview

Saleor is a headless e-commerce platform with a GraphQL API. This skill covers the core entities you'll work with in Configurator -- what they are, how they relate, and the rules that govern them.

## When to Use

- "What entities does Saleor have?"
- "How do channels, products, and variants relate?"
- "What's the difference between slug and name identifiers?"
- "What does Configurator manage vs. what's runtime only?"
- "What's a ProductType? What's a Channel?"
- When NOT designing product types -- use `product-modeling` instead
- When NOT writing YAML config -- use `configurator-schema` instead

## Core Entities

### Channel
Sales channels represent storefronts, marketplaces, or regions. Each has its own currency, country, product visibility, and pricing.

### Product Type
Defines the structure for a group of products: which attributes are shared (product-level) and which create variants (variant-level), plus shipping and tax settings.

### Product and Variant
Products are the items you sell. Each belongs to one product type and one category. Variants are the purchasable SKUs -- each with a unique SKU, specific attribute values, channel-specific pricing, and inventory tracking.

### Attribute
Typed fields attached to product types. Product-level attributes (Brand, Material) are shared across variants. Variant-level attributes (Size, Color) create separate SKUs.

### Category
Hierarchical product organization (tree structure). Each product belongs to one category. Used for navigation and filtering.

### Collection
Curated product groupings that can span categories. A product can belong to many collections. Used for promotions and merchandising.

### Warehouse
Inventory locations with stock tracking per variant. Associated with shipping zones.

### Shipping Zone
Geographic shipping regions with country-based targeting and multiple shipping methods.

## Entity Relationships

```
Channel ─────────────────────────────────────────────┐
    ├── Product Listings (visibility, pricing)       │
    ├── Variant Listings (price, availability)       │
    └── Checkout/Order settings                      │
                                                     │
ProductType ─────────────────────────────────────────┤
    ├── productAttributes ──> Attribute              │
    ├── variantAttributes ──> Attribute              │
    └── taxClass ──> TaxClass                        │
                                                     │
Product ─────────────────────────────────────────────┤
    ├── productType ──> ProductType                  │
    ├── category ──> Category                        │
    ├── collections ──> Collection[]                 │
    └── variants ──> ProductVariant[]                │
                     ├── warehouse ──> Warehouse     │
                     └── channelListings ────────────┘

Category (tree) └── subcategories ──> Category[]
ShippingZone    └── warehouses ──> Warehouse[]
```

## Identifier Rules

Each entity is identified by either its `slug` or `name`. This is how Configurator matches your local config to remote entities.

| Entity | Identifier | Mutable? |
|--------|------------|----------|
| Channel, Category, Collection, Product, Warehouse, Menu, Page | `slug` | No -- creates new |
| ProductType, PageType, Attribute, TaxClass, ShippingZone | `name` | No -- creates new |

**Important**: Changing an identifier creates a new entity and may orphan the old one. If you need to "rename" something, delete the old entity and create a new one.

## Configuration vs Runtime

Configurator manages your store's structure. Some things are runtime-only:

| Configurator Manages | Runtime Only |
|---------------------|--------------|
| Product structure and pricing | Orders |
| Categories and collections | Customers |
| Attributes and channels | Checkouts |
| Warehouses and shipping zones | Payments |
| Tax classes | Webhooks |

## Entity Relationships in config.yml

Here are practical examples showing how entities reference each other:

```yaml
# A product references its type (by name), category (by slug path),
# and channels (by slug) for pricing:
products:
  - name: "Classic T-Shirt"
    slug: "classic-t-shirt"
    productType: "T-Shirt"        # -> matches productTypes[].name
    category: "clothing/t-shirts"  # -> matches category slug path
    variants:
      - sku: "TSHIRT-S-RED"
        channelListings:
          - channel: "us-store"    # -> matches channels[].slug
            price: 29.99
        stocks:
          - warehouse: "main-wh"   # -> matches warehouses[].slug
            quantity: 100
```

```yaml
# A shipping zone references warehouses and targets countries:
shippingZones:
  - name: "US Shipping"
    countries: [US]
    warehouses:
      - "main-wh"                  # -> matches warehouses[].slug
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Confusing slug-based vs name-based entities | Check the Identifier Rules table -- some use `slug`, others use `name` |
| Changing an identifier to "rename" | This creates a duplicate. Delete old + create new instead. |
| Creating products before their product type exists | Product types must be defined first. Configurator handles deploy order, but the type must be in your config. |
| Not understanding channel scope | Products aren't visible until they have a channel listing. Each channel has independent pricing. |
| Mixing up Categories (taxonomy) vs Collections (curation) | Categories = hierarchical, 1 per product, for navigation. Collections = flat, many per product, for merchandising. |

## See Also

- For entity reference, see [references/entities.md](references/entities.md)
- For relationship diagrams, see [references/relationships.md](references/relationships.md)
- For Storefront v26 integration, see [references/storefront-v26.md](references/storefront-v26.md)

### Related Skills

- **`configurator-schema`** - Config.yml structure and validation rules
- **`product-modeling`** - Product type design and attribute selection
- **`configurator-cli`** - CLI commands for deploying configurations
