---
name: commercetools-data
description: Production-tested patterns for commercetools product types, custom types/objects, categories, import/export, and data migration from a Platinum partner with 50+ live implementations.
---

# commercetools Data Modeling & Management

Product types are **immutable once assigned to products** -- getting the data model right is the single most consequential decision in any commercetools implementation.

**Progressive loading — only load what you need:**

- Designing product types? Load `references/product-type-design.md`
- Product type operations (CRUD, migration, versioning)? Load `references/product-type-operations.md`
- Choosing Custom Types vs Custom Objects? Load `references/custom-types-objects.md`
- Designing category hierarchies? Load `references/category-design.md`
- Setting up localization? Load `references/localization.md`
- Importing or exporting data? Load `references/import-export.md`
- Planning a migration? Load `references/migration.md`
- Auditing catalog completeness? Load `references/bulk-catalog-audit.md`
- Enriching catalog data (AI-assisted, batch updates)? Load `references/bulk-catalog-enrichment.md`
- Code review or debugging? Load `references/anti-patterns.md`

## CRITICAL Priority -- Irreversible Decisions

| Pattern | File | Impact |
|---------|------|--------|
| Product Type Design Principles | [references/product-type-design.md](references/product-type-design.md) | Cannot change product type on existing products. Cannot delete a type with products. Attribute removal is destructive. |
| Custom Types vs Custom Objects | [references/custom-types-objects.md](references/custom-types-objects.md) | Only one Custom Type per resource at a time. Field type changes silently fail. Wrong choice = data in unreachable places. |
| Category Hierarchy Design | [references/category-design.md](references/category-design.md) | Deep hierarchies degrade search. No automatic inheritance. Restructuring requires product reassignment. |

## HIGH Priority -- Significant Rework

| Pattern | File | Impact |
|---------|------|--------|
| Localization Strategy | [references/localization.md](references/localization.md) | Over-localizing bloats payloads. Missing fallbacks break storefronts. Wrong LocalizedString usage wastes storage. |
| Import & Export Patterns | [references/import-export.md](references/import-export.md) | 20-resource batch limit. Async processing with 48-hour window. Wrong import order causes unresolved references. |
| Migration Strategy | [references/migration.md](references/migration.md) | Big-bang migrations fail. No built-in environment promotion. Product type changes require delete-and-recreate. |

## MEDIUM Priority -- Quality & Maintainability

| Pattern | File | Impact |
|---------|------|--------|
| Bulk Catalog Operations | [references/bulk-catalog-audit.md](references/bulk-catalog-audit.md) | Patterns for auditing catalog completeness (missing slugs, descriptions), batch updates, and AI-assisted data enrichment. |
| Anti-Patterns Catalog | [references/anti-patterns.md](references/anti-patterns.md) | Comprehensive list of data modeling mistakes with consequences and corrections. |

## Decision Flowcharts

### "Where Should This Data Live?"

```
Is the data an attribute of a product variant? (color, size, weight)
  YES --> Product Type attribute
  NO  --> Continue

Is the data extending an existing resource? (loyalty points on Customer,
gift wrap on LineItem, metadata on Order)
  YES --> Custom Type (Custom Fields)
  NO  --> Continue

Is the data standalone reference/config? (feature flags, lookup tables,
app settings, cross-cutting data)
  YES --> Custom Object (container/key)
  NO  --> Continue

Is the data classifying products for navigation? (department, collection)
  YES --> Category
  NO  --> Continue

Is it a workflow state? (product review status, order fulfillment stage)
  YES --> State Machine
  NO  --> Consider whether commercetools is the right place for this data
```

### "Product Type or Category?"

```
Does it define WHAT the product IS? (its schema, its attributes)
  YES --> Product Type

Does it define WHERE the product APPEARS? (navigation, browsing, collections)
  YES --> Category

Rule: If you could model it as a Category, prefer Category.
Categories are flexible. Product Types are permanent.
```

### "How Many Product Types?"

```
Do products share 80%+ of their attributes?
  YES --> Same Product Type (use attributes for differentiation)
  NO  --> Different Product Types

Is data managed in Merchant Center?
  YES --> Use more specific types (better editing UX)
  NO (external PIM) --> Fewer generic types are acceptable
```

## Key Platform Limits

| Resource | Limit | Notes |
|----------|-------|-------|
| Product Types per Project | 1,000 | Hard limit |
| Attributes per Product Type | No hard limit | 50 product-level + 50 variant-level searchable attributes indexed |
| Variants per Product | 100 | Can be increased by contacting support |
| Categories per Project | 10,000 | Requires review to increase |
| Custom Objects per Project | 20,000,000 | Generous but not infinite |
| Import Containers per Project | 1,000 | Keep < 200K operations per container |
| Resources per Import Request | 20 | Hard limit, batch accordingly |
| Import Operation retention | 48 hours | Unresolved refs retry up to 5 times |
| Product Selections per Store | 100 | Plan assortment strategy carefully |
| Distribution Channels per Store | 100 | |
| Supply Channels per Store | 100 | |

## MCP Complement

Use this skill to DESIGN the data model, then use the [Developer MCP](https://docs.commercetools.com/sdk/mcp/developer-mcp) for schema details and the [Commerce MCP](https://docs.commercetools.com/sdk/mcp/commerce-mcp) to execute operations. For bulk catalog operations, see `references/bulk-catalog-audit.md` and `references/bulk-catalog-enrichment.md`.
