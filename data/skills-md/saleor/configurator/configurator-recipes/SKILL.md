---
name: configurator-recipes
description: "Pre-built store configuration templates for common business types. Use whenever user asks for templates, examples, starting points, or mentions fashion/electronics/subscription store setup. Not for custom product type design (use product-modeling)."
license: MIT
metadata:
  author: saleor
  version: 2.0.0
  requires: "@saleor/configurator CLI"
---

# Configurator Recipes

## Overview

Recipes are ready-to-use `config.yml` templates for common store types. Pick one that matches your business, customize it, and deploy. They save you from building your store configuration from scratch.

## When to Use

- "How do I set up a fashion store?"
- "Is there a template for electronics?"
- "Can I see an example config.yml?"
- "What's a good starting point for my store?"
- "How do I set up a subscription service?"
- When NOT looking for CLI commands -- use `configurator-cli` instead
- When NOT designing custom product types -- use `product-modeling` instead

## Available Recipes

| Recipe | Best For | Key Features |
|--------|----------|--------------|
| **Fashion Store** | Apparel, shoes, accessories | Size/color variants, seasonal collections, multi-currency |
| **Electronics Store** | Tech products, gadgets | Specs attributes, storage/RAM variants, warranty info |
| **Subscription Service** | Recurring products, SaaS | Plan tiers, billing cycles, add-on services |

For a blank starting point (correct structure, no business content), use the skeleton template.

## Quick Start

```bash
# Copy a template directly
cp skills/configurator-recipes/templates/fashion-store.yml config.yml

# Customize and deploy
pnpm dlx @saleor/configurator deploy --url=$SALEOR_URL --token=$SALEOR_TOKEN
```

## Recipe Details: Fashion Store

A complete configuration for apparel and fashion retail with two channels (US/EU), five product types, a full category tree, and curated collections.

**Channels**: US Store (USD), EU Store (EUR)

**Product Types**: T-Shirt, Pants, Dress, Shoes, Accessory -- each with appropriate size/color/material variants.

**Categories**:
```
Clothing -> Men's (T-Shirts, Pants, Shoes) / Women's (Dresses, Tops, Shoes) / Accessories (Bags, Jewelry)
```

**Collections**: New Arrivals, Best Sellers, Sale Items, Seasonal Collection

**Attributes**: Size (XS-XXL), Color (swatches), Material, Brand, Care Instructions

See [templates/fashion-store.yml](templates/fashion-store.yml) for the complete configuration.

## Other Recipes

**Electronics Store** -- Single channel (USD), product types for Smartphones, Laptops, Tablets, Accessories, and Software. Attributes include Brand, Storage, RAM, Screen Size, and Warranty. See [templates/electronics-store.yml](templates/electronics-store.yml).

**Subscription Service** -- Subscription portal channel, product types for Monthly/Annual subscriptions, One-Time Purchases, and Add-Ons. Attributes include Plan Tier, Billing Cycle, User Limit, and Storage Limit. See [templates/subscription-service.yml](templates/subscription-service.yml).

## Customization Tips

After copying a recipe:

1. **Rename channels** to match your brand and regions
2. **Adjust currency and country codes** for your markets
3. **Modify categories** for your actual product catalog
4. **Add or remove product types** you don't need
5. **Test on staging first** before deploying to production

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using a recipe without customizing identifiers | Update all slugs and names to match your brand before deploying |
| Not adjusting currency/country codes | Change `currencyCode` and `defaultCountry` to your actual markets |
| Deploying a recipe straight to production | Always test on a staging instance first |
| Keeping entity types you don't need | Remove unused product types, categories, etc. to keep your config clean |
| Forgetting to update channel references | Products reference channels by slug -- make sure they match after renaming |

## Creating Your Own Recipe

### Template Structure

A recipe template should follow this structure:

```yaml
# Recipe: [Business Type] Store
# Description: [What this recipe sets up]
# Customize: [List key things users should change]

channels:
  - name: "Main Store"          # <- User should rename
    slug: "main"                # <- User should update
    currencyCode: USD           # <- User should set region
    defaultCountry: US
    isActive: true

productTypes:
  # Each type should have a comment explaining its purpose
  - name: "[Type Name]"
    isShippingRequired: true
    productAttributes: [...]
    variantAttributes: [...]

categories:
  # Keep hierarchy to 3 levels max
  - name: "[Root Category]"
    slug: "[root-slug]"
    subcategories: [...]
```

### Required Sections

Every recipe must include:
1. **Header comment** -- recipe name, description, customization checklist
2. **At least one channel** -- with valid currency and country codes
3. **Product types** -- with product and variant attributes defined
4. **Categories** -- at least a basic hierarchy
5. **Comments** -- explaining what each section does and what to customize

### Testing Your Recipe

```bash
# 1. Deploy to a fresh Saleor instance
pnpm dlx @saleor/configurator deploy --url=$STAGING_URL --token=$STAGING_TOKEN

# 2. Verify idempotency (second deploy should show no changes)
pnpm dlx @saleor/configurator deploy --url=$STAGING_URL --token=$STAGING_TOKEN

# 3. Introspect and diff to confirm round-trip fidelity
pnpm dlx @saleor/configurator introspect --url=$STAGING_URL --token=$STAGING_TOKEN --config=introspected.yml
pnpm dlx @saleor/configurator diff --url=$STAGING_URL --token=$STAGING_TOKEN
```

### Documentation Checklist

- [ ] Every section has comments explaining purpose
- [ ] All placeholder values are clearly marked for customization
- [ ] Currency/country codes use valid ISO standards
- [ ] Slugs are descriptive and follow lowercase-hyphen convention
- [ ] README or header documents what the recipe creates

## See Also

### Related Skills

- **`configurator-schema`** - Config.yml structure and validation rules
- **`product-modeling`** - Product type design and attribute selection
- **`saleor-domain`** - Entity relationships and Saleor concepts
