---
name: theme-development
description: Build, customize, and deploy Shopify themes. Use this skill for creating new themes, modifying existing themes, understanding theme architecture, working with sections/blocks, and optimizing theme performance. Covers Skeleton theme, Dawn theme, layouts, templates, and the theme editor customization experience.
license: MIT
compatibility: Requires Shopify CLI, Node.js 18+, and a Shopify Partner account
metadata:
  author: shopify-agent-skills
  version: "1.0"
  shopify-api-version: "2025-01"
---

# Shopify Theme Development

## When to use this skill

Use this skill when:

- Creating a new Shopify theme from scratch
- Modifying or customizing an existing theme
- Understanding Shopify theme architecture
- Working with sections, blocks, and templates
- Setting up the development environment
- Deploying themes to a Shopify store
- Optimizing theme performance

## Theme Architecture Overview

### Directory Structure

A Shopify theme must follow this structure:

```
your-theme/
├── assets/          # CSS, JS, images, fonts
├── config/          # Theme settings (settings_schema.json, settings_data.json)
├── layout/          # Layout files (theme.liquid required)
├── locales/         # Translation files (en.default.json, etc.)
├── sections/        # Reusable section components
├── snippets/        # Reusable code snippets
└── templates/       # Page templates (JSON or Liquid)
    └── customers/   # Customer account templates
```

**Minimum Requirements:** Only `layout/theme.liquid` is required for upload.

### Component Hierarchy

```
Layout (theme.liquid)
  └── Template (product.json)
        └── Sections (product-details.liquid)
              └── Blocks (price, quantity, add-to-cart)
                    └── Snippets (icon-cart.liquid)
```

## Getting Started

### 1. Initialize a New Theme

Use the Skeleton theme as a starting point:

```bash
# Clone the Skeleton theme
shopify theme init my-theme

# Navigate to your theme
cd my-theme
```

The [Skeleton theme](https://github.com/shopify/skeleton-theme) is minimal and follows Shopify best practices.

### 2. Start Development Server

```bash
# Start local development with hot reload
shopify theme dev

# Connect to a specific store
shopify theme dev --store your-store.myshopify.com
```

This opens a local preview URL with live reloading.

### 3. Push to Shopify

```bash
# Upload as a new theme
shopify theme push --unpublished

# Push to an existing theme
shopify theme push --theme THEME_ID
```

## Key Concepts

### Layouts

Layouts wrap all pages. The main layout file is `layout/theme.liquid`:

```liquid
<!DOCTYPE html>
<html lang="{{ request.locale.iso_code }}">
<head>
  <title>{{ page_title }}</title>
  {{ content_for_header }}
</head>
<body>
  {% sections 'header-group' %}

  <main>
    {{ content_for_layout }}
  </main>

  {% sections 'footer-group' %}
</body>
</html>
```

### JSON Templates

Modern themes use JSON templates that reference sections:

```json
// templates/product.json
{
  "sections": {
    "main": {
      "type": "product-details",
      "settings": {}
    },
    "recommendations": {
      "type": "product-recommendations",
      "settings": {}
    }
  },
  "order": ["main", "recommendations"]
}
```

### Sections

Sections are reusable, customizable modules:

```liquid
<!-- sections/featured-collection.liquid -->
{% schema %}
{
  "name": "Featured Collection",
  "settings": [
    {
      "type": "collection",
      "id": "collection",
      "label": "Collection"
    },
    {
      "type": "range",
      "id": "products_to_show",
      "min": 2,
      "max": 12,
      "step": 1,
      "default": 4,
      "label": "Products to show"
    }
  ],
  "presets": [
    {
      "name": "Featured Collection"
    }
  ]
}
{% endschema %}

<section class="featured-collection">
  {% if section.settings.collection != blank %}
    {% for product in section.settings.collection.products limit: section.settings.products_to_show %}
      {% render 'product-card', product: product %}
    {% endfor %}
  {% endif %}
</section>
```

### Blocks

Blocks allow merchants to add, remove, and reorder content:

```liquid
{% schema %}
{
  "name": "Slideshow",
  "blocks": [
    {
      "type": "slide",
      "name": "Slide",
      "settings": [
        {
          "type": "image_picker",
          "id": "image",
          "label": "Image"
        },
        {
          "type": "text",
          "id": "heading",
          "label": "Heading"
        }
      ]
    }
  ]
}
{% endschema %}

{% for block in section.blocks %}
  <div class="slide" {{ block.shopify_attributes }}>
    <img src="{{ block.settings.image | image_url: width: 1920 }}">
    <h2>{{ block.settings.heading }}</h2>
  </div>
{% endfor %}
```

## Best Practices

### Performance

1. **Lazy load images** - Use `loading="lazy"` for images below the fold
2. **Optimize images** - Use `image_url` filter with appropriate widths
3. **Minimize render-blocking resources** - Defer non-critical CSS/JS
4. **Use native browser features** - Prefer CSS over JavaScript when possible

```liquid
<!-- Responsive images with lazy loading -->
{{ product.featured_image | image_url: width: 800 | image_tag:
  loading: 'lazy',
  widths: '300, 500, 800, 1200',
  sizes: '(max-width: 600px) 100vw, 50vw'
}}
```

### Accessibility

1. Use semantic HTML (`<main>`, `<nav>`, `<article>`)
2. Provide alt text for images
3. Ensure proper heading hierarchy
4. Support keyboard navigation
5. Maintain sufficient color contrast

### Theme Settings

Use `settings_schema.json` for global theme settings:

```json
[
  {
    "name": "theme_info",
    "theme_name": "My Theme",
    "theme_version": "1.0.0"
  },
  {
    "name": "Colors",
    "settings": [
      {
        "type": "color",
        "id": "primary_color",
        "label": "Primary color",
        "default": "#000000"
      }
    ]
  }
]
```

Access in Liquid: `{{ settings.primary_color }}`

## CLI Commands Reference

| Command                 | Description               |
| ----------------------- | ------------------------- |
| `shopify theme init`    | Clone Skeleton theme      |
| `shopify theme dev`     | Start development server  |
| `shopify theme push`    | Upload theme to store     |
| `shopify theme pull`    | Download theme from store |
| `shopify theme check`   | Run theme linter          |
| `shopify theme list`    | List all themes           |
| `shopify theme publish` | Publish unpublished theme |
| `shopify theme delete`  | Delete a theme            |

## Common Issues & Solutions

### Issue: Theme not syncing changes

**Solution:** Ensure `shopify theme dev` is running and check for file save errors.

### Issue: Section not appearing in editor

**Solution:** Add a `presets` array to the section schema.

### Issue: Slow page load

**Solution:** Run `shopify theme check` and address performance warnings.

## Resources

- [Dawn Theme (Reference)](https://github.com/Shopify/dawn)
- [Skeleton Theme (Starter)](https://github.com/shopify/skeleton-theme)
- [Theme Architecture Docs](https://shopify.dev/docs/storefronts/themes/architecture)
- [Theme Best Practices](https://shopify.dev/docs/storefronts/themes/best-practices)

For Liquid templating specifics, see the [liquid-templating](../liquid-templating/SKILL.md) skill.
