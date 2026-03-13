---
name: configurator-schema
description: "Config.yml schema, entity structure, and validation rules. Use whenever writing, reading, or validating any part of config.yml, or when asking about YAML format, required fields, entity identification, or config validation errors. Do NOT use for general YAML questions unrelated to Saleor Configurator."
license: MIT
metadata:
  author: saleor
  version: 2.0.0
  requires: "@saleor/configurator CLI"
---

# Configurator Schema

## Overview

Your store configuration lives in a single `config.yml` file. Each section defines a type of entity (channels, products, categories, etc.) using a declarative YAML format that Configurator syncs with your Saleor instance.

## When to Use

- "What does config.yml look like?"
- "What fields are required for a product/channel/category?"
- "Why is my config failing validation?"
- "What's the difference between slug-based and name-based entities?"
- "How do I reference one entity from another?"
- When NOT designing product types or choosing attributes -- use `product-modeling` instead

## File Structure

```yaml
# config.yml - Top-level structure
shop:               # Store-wide settings (singleton)
channels:           # Sales channels (slug-based)
productAttributes:  # Standalone product attributes
contentAttributes:  # Standalone content attributes
productTypes:       # Product type definitions (name-based)
modelTypes:         # Model type definitions (name-based) -- preferred over pageTypes
pageTypes:          # Page type definitions (name-based) -- alias for modelTypes
categories:         # Category hierarchy (slug-based)
collections:        # Product collections (slug-based)
products:           # Product definitions (slug-based)
models:             # Content models/pages (slug-based)
taxClasses:         # Tax classifications (name-based)
shippingZones:      # Shipping zone definitions (name-based)
warehouses:         # Warehouse definitions (slug-based)
menus:              # Navigation menus (slug-based)
```

## Entity Identification

Configurator matches your local config to remote entities using an identifier field. This is either `slug` or `name` depending on entity type:

| Identifier | Entity Types |
|------------|-------------|
| **slug** | channels, categories, collections, products, warehouses, menus, models |
| **name** | productTypes, modelTypes/pageTypes, taxClasses, shippingZones |

**Important**: Changing a slug or name creates a NEW entity instead of updating the existing one.

## Common Entity Examples

### Channel

```yaml
channels:
  - name: "US Store"
    slug: "us-store"
    currencyCode: USD
    defaultCountry: US
    isActive: true
```

### Product Type

```yaml
productTypes:
  - name: "T-Shirt"
    isShippingRequired: true
    productAttributes:
      - name: "Brand"
        type: DROPDOWN
    variantAttributes:
      - name: "Size"
        type: DROPDOWN
        values: [{ name: "S" }, { name: "M" }, { name: "L" }]
      - name: "Color"
        type: SWATCH
```

### Product

```yaml
products:
  - name: "Classic T-Shirt"
    slug: "classic-t-shirt"
    productType: "T-Shirt"
    category: "clothing/t-shirts"
    variants:
      - sku: "TSHIRT-S-RED"
        attributes:
          Size: "S"
          Color: "Red"
        channelListings:
          - channel: "us-store"
            price: 29.99
```

### Category (hierarchical)

```yaml
categories:
  - name: "Electronics"
    slug: "electronics"
    subcategories:
      - name: "Phones"
        slug: "phones"
```

## Attribute Types

Saleor supports these attribute input types: DROPDOWN, MULTISELECT, SWATCH, BOOLEAN, PLAIN_TEXT, RICH_TEXT, NUMERIC, DATE, DATE_TIME, FILE, REFERENCE.

For detailed guidance on choosing the right type, see the `product-modeling` skill.

## Validation Rules

1. **Required fields** -- each entity type has required fields (e.g., channels need `name`, `slug`, `currencyCode`)
2. **Unique identifiers** -- slugs/names must be unique within their entity type
3. **Valid references** -- cross-entity references must match (e.g., a product's `productType` must match a defined product type name)
4. **Currency codes** -- valid ISO 4217 (USD, EUR, GBP, etc.)
5. **Country codes** -- valid ISO 3166-1 alpha-2 (US, DE, GB, etc.)

## Entity Dependencies

Entities depend on each other and must exist in the right order:

```
Level 0 (independent):  shop, channels, productTypes, pageTypes, taxClasses, shippingZones
Level 1 (needs L0):     categories, warehouses, attributes
Level 2 (needs L1):     collections, pages
Level 3 (needs L2):     products, menus
```

Configurator handles deployment order automatically, but understanding dependencies helps when troubleshooting validation errors.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Changing a slug or name to "rename" an entity | This creates a new entity. To rename, delete the old one and create new. |
| Duplicate slugs within an entity type | Each slug must be unique. Check for copy-paste errors. |
| Product references a nonexistent productType | The `productType` field must exactly match a `name` in your `productTypes` section. |
| Missing required fields | Check the error message -- it tells you which field is missing. |
| Products defined before their productType | Not a YAML order issue (Configurator handles order), but the referenced type must exist in the file. |

## Best Practices

1. **Use meaningful slugs** -- `womens-summer-dresses` not `cat-123`
2. **Consistent naming** -- match display names to slugs when possible
3. **Comment complex sections** -- use YAML comments for documentation
4. **Version control** -- track config.yml in git

## See Also

- For complete schema documentation, see [references/schema.md](references/schema.md)
- For example configurations, see [references/examples.md](references/examples.md)

### Related Skills

- **`saleor-domain`** - Entity relationships and identifier rules
- **`configurator-cli`** - CLI commands for deploying configurations
- **`product-modeling`** - Product type design and attribute selection
