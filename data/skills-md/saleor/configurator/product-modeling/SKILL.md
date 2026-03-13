---
name: product-modeling
description: "Product type design, attribute selection, and variant planning for Saleor. Use whenever user mentions products, variants, SKUs, attributes, catalogs, or product types. Not for YAML syntax (use configurator-schema) or CLI commands (use configurator-cli)."
license: MIT
metadata:
  author: saleor
  version: 2.0.0
  requires: "@saleor/configurator CLI"
---

# Saleor Domain Modeling

## Overview

This skill helps you design your product catalog structure in Saleor -- choosing the right product types, attributes, variants, categories, and collections. The key decisions are what makes a product vs. a variant, and which attribute type to use for each field.

## When to Use

- "How do I model my products?"
- "What attributes should I use?"
- "Product vs variant attributes?"
- "When to use DROPDOWN vs MULTISELECT?"
- "How to structure my product types?"
- "Categories vs Collections?"
- "When to use Models (Pages) vs Attributes?"
- When NOT looking for YAML syntax -- use `configurator-schema` instead
- When NOT looking for CLI commands -- use `configurator-cli` instead

## The Core Flow

This is the most important relationship to understand:

```
1. ATTRIBUTES (define fields)
   └── Reusable typed fields: Size (DROPDOWN), Color (SWATCH), Brand (DROPDOWN)

2. PRODUCT TYPES (define structure)
   └── Assign attributes:
       ├── productAttributes: Brand, Material (same for all variants)
       └── variantAttributes: Size, Color (create SKU combinations)

3. PRODUCTS (create items)
   └── Instance of a ProductType:
       ├── Set values: Brand="Nike", Material="Cotton"
       └── Define variants with SKU combinations

4. VARIANTS (purchasable SKUs)
   └── Each combination = 1 variant:
       ├── SKU: "TSHIRT-BLK-M" -> Size="M", Color="Black", Price=$29.99
       └── SKU: "TSHIRT-WHT-L" -> Size="L", Color="White", Price=$29.99
```

**Key insight:** Attributes are building blocks. ProductTypes assemble them into templates. Products are instances. Variants are what customers buy.

## Decision Framework: Product vs Variant Attributes

This is the most critical modeling decision.

### Use Product-Level When:

| Question | If YES, use Product Level |
|----------|--------------------------|
| Same value for all sizes/colors? | Brand, Material, Manufacturer |
| Descriptive information? | Care Instructions, Specs |
| For filtering/categorization only? | Style, Gender, Season |

### Use Variant-Level When:

| Question | If YES, use Variant Level |
|----------|--------------------------|
| Creates a separate purchasable item? | Size, Color, Storage |
| Affects price? | Size (XL costs more), quality tier |
| Needs separate inventory tracking? | Each size needs its own stock |
| Customer selects this at checkout? | Color picker, size selector |

### Quick Decision Matrix

| Attribute | Product | Variant | Why |
|-----------|:-------:|:-------:|-----|
| Brand | x | | Same for all variants |
| Size | | x | Creates separate SKUs |
| Color | | x | Creates separate SKUs |
| Material | x | | Usually same for product |
| Storage (64GB/128GB) | | x | Different prices |
| Care Instructions | x | | Same for all variants |
| Weight | | x | May differ per size |

## Attribute Type Selection

Saleor supports 12 attribute input types. Use this decision tree:

```
Is it a CHOICE from predefined options?
├── YES: Can user select MULTIPLE?
│   ├── YES -> MULTISELECT
│   └── NO: Is it a COLOR/PATTERN?
│       ├── YES -> SWATCH
│       └── NO: Is it YES/NO?
│           ├── YES -> BOOLEAN
│           └── NO -> DROPDOWN
└── NO: Is it a NUMBER with units?
    ├── YES -> NUMERIC
    └── NO: Is it a DATE?
        ├── YES -> DATE (or DATE_TIME if time needed)
        └── NO: Is it long formatted text?
            ├── YES -> RICH_TEXT
            └── NO: Is it a file/document?
                ├── YES -> FILE
                └── NO: Link to another entity?
                    ├── YES -> REFERENCE
                    └── NO -> PLAIN_TEXT
```

For the complete attribute type reference, see [references/attribute-types-deep-dive.md](references/attribute-types-deep-dive.md).

## Variant Matrix Planning

Before creating variants, calculate the SKU explosion:

```
SKU Count = Value1 x Value2 x Value3 x ...

Example: T-Shirt
- Sizes: XS, S, M, L, XL, XXL (6)
- Colors: Black, White, Navy, Gray, Red (5)
- SKUs: 6 x 5 = 30 variants per product
```

| SKU Count | Assessment | Recommendation |
|-----------|------------|----------------|
| 1-10 | Manageable | Good for most products |
| 11-50 | Moderate | Fine for fashion, needs inventory planning |
| 51-100 | High | Consider splitting into multiple products |
| 100+ | Too many | Simplify -- move some attributes to product level |

**Tips for high counts:** Split by product line, reduce dimensions, move non-purchasable attributes to product level.

## Industry Patterns

Quick reference for common store types:

| Pattern | Product-Level Attrs | Variant-Level Attrs | Typical SKUs |
|---------|-------------------|-------------------|-------------|
| **Apparel** | Brand, Material, Care | Size, Color | 30/product |
| **Electronics** | Brand, Screen, Processor, Features | Storage, Color | 20/product |
| **Furniture** | Brand, Style, Capacity, Dimensions | Fabric, Color | 16/product |
| **Food & Beverage** | Origin, Roast, Flavor, Certifications | Size, Grind | 12/product |
| **Digital Products** | Publisher, Platform, Features | License Type, Duration | 9/product |

For complete YAML examples of each pattern, see [references/industry-patterns.md](references/industry-patterns.md).

## Categories vs Collections

Both organize products, but they serve different purposes:

| Aspect | Category | Collection |
|--------|----------|------------|
| **Structure** | Hierarchical (tree) | Flat (list) |
| **Assignment** | 1 product = 1 category | 1 product = many collections |
| **Purpose** | Taxonomy, navigation | Merchandising, promotions |
| **Examples** | Electronics > Phones > Smartphones | "Summer Sale", "New Arrivals" |

**Use Categories** for main site navigation, browse/filter structure, SEO URLs.
**Use Collections** for curated groups, promotions, campaigns, temporary groupings.

Keep category trees to 3 levels deep. If you need a 4th level, consider using Collections instead.

## Models and Structures

**Models** (Pages/PageTypes) let you create custom entities beyond products -- like Brands, Ingredients, or Scent Profiles. Use them when data is shared across many products, has its own attributes, and needs its own page.

**Structures** (Menus) assemble Categories, Collections, Models, and URLs into navigation hierarchies.

For complete guidance and examples, see [references/models-and-structures.md](references/models-and-structures.md).

## Workflow: Designing a New Product Type

1. **List all product characteristics** -- write down every field/attribute
2. **Categorize each** -- apply the decision framework (product vs variant)
3. **Select types** -- use the attribute type decision tree
4. **Calculate SKU count** -- ensure the variant matrix is manageable
5. **Write the YAML** -- create the ProductType configuration
6. **Validate** -- deploy with `--plan` to check structure

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Over-dimensioning variants (6 sizes x 10 colors x 4 materials = 240 SKUs) | Move non-purchasable attributes to product level. Aim for under 50 SKUs. |
| Using variant attributes for non-inventory fields | If it doesn't create a separate SKU (like Care Instructions), it's a product attribute |
| Product attributes that should vary | If value differs by size (e.g., Weight), move to variant level |
| Too many product types | Reuse types when products share the same attribute structure |
| Skipping variant planning | Always calculate SKU count before creating product types |

## Additional Resources

### Reference Files

- **[references/attribute-types-deep-dive.md](references/attribute-types-deep-dive.md)** -- complete attribute type reference
- **[references/industry-patterns.md](references/industry-patterns.md)** -- detailed YAML for 5+ industries
- **[references/models-and-structures.md](references/models-and-structures.md)** -- Models and Structures guide

### Related Skills

- **`configurator-schema`** - Complete YAML schema reference
- **`saleor-domain`** - Entity relationships and Saleor concepts
- **`configurator-recipes`** - Complete store templates
