---
name: shopify-section-structure
description: Shopify theme section structure, file organization, and schema requirements. Use when creating or modifying Shopify theme sections.
---

# Shopify Section Structure

Guidelines for organizing Shopify theme sections with proper file structure, schema configuration, and padding settings.

## When to Use

- Creating new Shopify theme sections
- Modifying existing section schemas
- Setting up section file structure (Liquid, CSS, JS)
- Adding padding controls to sections

## Section File Structure

Each section must have:
- **Liquid section file** (`.liquid` in `sections/` directory)
- **Separate CSS file** (in `assets/` directory)
- **Optional separate JS file** (in `assets/` directory)

### CSS Inclusion

Each section must include its own stylesheet using:

```liquid
{{ 'section-name.css' | asset_url | stylesheet_tag }}
```

**Important**: Do NOT mix styles of multiple sections in one file. Each section has its own CSS file.

### JavaScript Inclusion

If a section needs JavaScript, include it separately:

```liquid
<script src="{{ 'section-logic.js' | asset_url }}" defer="defer"></script>
```

## Section Schema Requirements

Every section schema MUST include padding settings.

### Required Padding Settings

Add a "Paddings" heading in the schema with these settings:

```json
{
  "type": "header",
  "content": "Paddings"
},
{
  "type": "range",
  "id": "padding_top",
  "label": "Padding Top",
  "min": 0,
  "max": 100,
  "step": 1,
  "unit": "px",
  "default": 0
},
{
  "type": "range",
  "id": "padding_bottom",
  "label": "Padding Bottom",
  "min": 0,
  "max": 100,
  "step": 1,
  "unit": "px",
  "default": 0
},
{
  "type": "range",
  "id": "padding_top_mobile",
  "label": "Padding Top (Mobile)",
  "min": 0,
  "max": 100,
  "step": 1,
  "unit": "px",
  "default": 0
},
{
  "type": "range",
  "id": "padding_bottom_mobile",
  "label": "Padding Bottom (Mobile)",
  "min": 0,
  "max": 100,
  "step": 1,
  "unit": "px",
  "default": 0
}
```

### Schema Best Practices

- Add additional settings only when required
- Avoid over-configuring the schema
- Always include at least one preset
- Keep settings organized and logical

### Applying Padding in CSS

Use the schema settings in your section CSS:

```css
.section {
  padding-top: {{ section.settings.padding_top }}px;
  padding-bottom: {{ section.settings.padding_bottom }}px;
}

@media (max-width: 749px) {
  .section {
    padding-top: {{ section.settings.padding_top_mobile }}px;
    padding-bottom: {{ section.settings.padding_bottom_mobile }}px;
  }
}
```

## Shopify Theme Documentation

Reference these official Shopify resources:

- [Shopify Theme Structure](https://shopify.dev/docs/themes/architecture)
- [Section Schema](https://shopify.dev/docs/themes/architecture/sections/section-schema)
- [Section Files](https://shopify.dev/docs/themes/architecture/sections/section-files)
- [Theme Settings](https://shopify.dev/docs/themes/architecture/settings)

## Example Section Structure

```
sections/
  └── featured-collection.liquid

assets/
  ├── featured-collection.css
  └── featured-collection.js (optional)
```

## Instructions

1. **Create section file** in `sections/` directory with `.liquid` extension
2. **Create CSS file** in `assets/` directory matching section name
3. **Include CSS** in section using `stylesheet_tag` filter
4. **Add schema** with required padding settings
5. **Add at least one preset** to the schema
6. **Keep files separate** - never mix multiple sections' styles in one CSS file
