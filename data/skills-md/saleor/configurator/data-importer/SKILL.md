---
name: data-importer
description: "Transforms external product data into Saleor config.yml format. Use whenever importing, migrating, or converting data from CSV, Excel, Shopify, or any external source. Not for manual config editing (use configurator-schema)."
license: MIT
metadata:
  author: saleor
  version: 2.0.0
  requires: "@saleor/configurator CLI"
---

# Data Importer

## Overview

This skill helps you convert product data from external sources (CSV files, spreadsheets, Shopify exports) into Saleor's `config.yml` format. It walks through format detection, column mapping, and validation before generating output.

## When to Use

- "I need to import products from a CSV"
- "How do I convert my spreadsheet to config.yml?"
- "I'm migrating from Shopify"
- "I have product data in Excel"
- "How do I bulk import products?"
- When NOT writing config.yml from scratch -- use `configurator-schema` instead
- When NOT designing product types -- use `product-modeling` first

## Core Workflow

1. **Detect format** -- CSV, Excel, JSON, or unknown
2. **Extract columns** -- read headers and sample data
3. **Map interactively** -- you confirm field mappings
4. **Transform** -- convert to Saleor schema
5. **Validate** -- check for issues before output

## File Handling

### Excel (.xlsx)
Excel files need conversion. Export as CSV from Excel/Sheets, or:
```bash
python3 -c "import pandas as pd; pd.read_excel('$FILE').to_csv('${FILE%.xlsx}.csv', index=False)"
```

### CSV
Read directly to inspect headers and sample rows.

## Field Mapping

**Don't assume column names.** The importer will:
1. Show you all columns with sample values
2. Ask which column maps to each Saleor field
3. Mark unmapped columns as potential attributes

### Required Fields

| Saleor Field | Typical Source Columns |
|--------------|----------------------|
| `product.name` | "name", "title", or any descriptive column |
| `product.slug` | Generated from name, or "handle"/"ID" column |
| `variant.sku` | "SKU", "External ID", "Code" |
| `productType` | "type" column or you specify it |

### Optional Fields

| Field | Notes |
|-------|-------|
| `price` | If missing, imports as catalog-only |
| `quantity` | If missing, skips stock tracking |
| `category` | From category/region column |
| `description` | If present in source data |
| Other columns | Become product attributes |

## Output Structure

```yaml
productTypes:
  - name: "[from type column or your input]"
    productAttributes: [unmapped columns become attributes]

categories:
  - name: "[from category column]"
    slug: "[generated]"

products:
  - name: "[from name column]"
    slug: "[generated or from ID]"
    productType: "[reference]"
    variants:
      - sku: "[from SKU column]"
        channelListings: [if price exists]
        stocks: [if quantity exists]
```

## Special Cases

- **No price column** -- imports as catalog-only; add pricing later
- **No SKU column** -- generates from name or uses any unique ID column
- **Unknown columns** -- presented to you as potential attributes
- **Multiple rows with same product** -- grouped as variants of one product

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Assuming column names without checking | Always inspect headers first -- column names vary wildly between sources |
| Not handling missing SKUs | Generate SKUs from product name + variant attributes, or use a unique ID column |
| Importing without validating first | Review the generated YAML before deploying -- check for duplicates and missing fields |
| Duplicate products from multi-row variants | Ensure rows sharing a product name are grouped as variants, not separate products |
| Forgetting to create product types first | Design your product types before importing -- use `product-modeling` skill |

## Validation Checklist

Before generating output, verify:
- All products have names
- All variants have unique SKUs
- Product type references are valid
- No duplicate slugs

## Reference Files

- **`references/csv-patterns.md`** -- CSV/Excel parsing techniques
- **`references/field-mapping.md`** -- Mapping strategies for various data shapes
- **`references/shopify-format.md`** -- Shopify-specific handling
- **`references/transformations.md`** -- Data transformation rules

## See Also

### Related Skills

- **`configurator-schema`** - Config.yml structure and field requirements
- **`product-modeling`** - Product type design before importing
- **`saleor-domain`** - Entity relationships and identifier rules
