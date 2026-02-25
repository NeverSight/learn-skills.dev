---
name: shopify-liquid-templates
description: Liquid template best practices for Shopify themes - snippets, logic, image handling, and SVG usage. Use when writing or modifying Liquid templates in Shopify themes.
---

# Shopify Liquid Templates

Best practices for Liquid templates, snippets, logic flow, image handling, and SVG usage in Shopify themes.

## When to Use

- Creating or modifying Liquid templates
- Working with snippets
- Handling images and media
- Writing Liquid logic
- Using SVG icons

## Snippets

### Usage

- Use `{% render %}` only (never `include`)
- Inside each snippet, add a **Usage** block at the top

### Snippet Structure

```liquid
{%- comment -%}
Usage:
{% render 'snippet-name', param: value, another_param: value %}
{%- endcomment -%}

<div class="snippet-name">
  {{ param }}
</div>
```

### Snippet Parameters

Pass data to snippets via parameters:

```liquid
{% render 'product-card', 
  product: product, 
  show_price: true, 
  image_size: 'large' %}
```

### Why `render` Instead of `include`

- `render` is more performant
- Better variable scoping
- Recommended by Shopify

## Liquid Logic

### Use `{% liquid %}` Tag

For long or complex logic, use the `{% liquid %}` tag:

```liquid
{% liquid
  assign discount = product.compare_at_price | minus: product.price
  assign discount_percent = discount | times: 100 | divided_by: product.compare_at_price
  if discount_percent > 20
    assign is_big_discount = true
  endif
%}
```

### Logic Best Practices

- Avoid deeply nested conditionals
- Prefer readable, linear logic
- Break complex logic into multiple `liquid` blocks if needed
- Use meaningful variable names

### Example: Clean Logic Flow

```liquid
{% liquid
  if product.available
    assign button_text = 'Add to Cart'
    assign button_class = 'btn--primary'
  else
    assign button_text = 'Sold Out'
    assign button_class = 'btn--disabled'
  endif
%}

<button class="{{ button_class }}">
  {{ button_text }}
</button>
```

## Images

### Always Use `image_tag`

- Always use `image_tag` filter
- Use responsive `srcset` and sizes
- Do NOT hardcode `<img>` tags

### Image Tag Syntax

```liquid
{{ image | image_tag: widths: '360, 720, 1080', loading: 'lazy' }}
```

### Responsive Images

```liquid
{% assign image_widths = '360, 540, 720, 900, 1080, 1296, 1512, 1728, 1944, 2160' %}

{{ product.featured_image | image_tag: 
  widths: image_widths,
  sizes: '(min-width: 1200px) 50vw, 100vw',
  loading: 'lazy',
  alt: product.featured_image.alt | escape }}
```

### Image Settings

Common `image_tag` parameters:
- `widths`: Comma-separated list of widths for srcset
- `sizes`: Sizes attribute for responsive images
- `loading`: 'lazy' or 'eager'
- `alt`: Alt text (use `| escape` filter)

## SVG Files

### Inline SVGs

Inline SVGs using the `inline_asset_content` filter:

```liquid
{{ 'icon-arrow.svg' | inline_asset_content }}
```

### Do NOT Paste Raw SVG

- Do NOT paste raw SVG markup into templates
- Store SVG files in `assets/` directory
- Use `inline_asset_content` filter to include them

### SVG Example

```liquid
<button class="icon-button">
  {{ 'icon-close.svg' | inline_asset_content }}
  <span class="visually-hidden">Close</span>
</button>
```

### SVG Styling

SVGs can be styled with CSS when inlined:

```css
.icon-button svg {
  width: 24px;
  height: 24px;
  fill: currentColor;
}
```

## Shopify Theme Documentation

Reference these official Shopify resources:

- [Liquid Documentation](https://shopify.dev/docs/api/liquid)
- [Liquid Objects](https://shopify.dev/docs/api/liquid/objects)
- [Liquid Filters](https://shopify.dev/docs/api/liquid/filters)
- [Liquid Tags](https://shopify.dev/docs/api/liquid/tags)
- [Theme Templates](https://shopify.dev/docs/themes/architecture/templates)
- [Snippets](https://shopify.dev/docs/themes/architecture/snippets)
- [Image Filters](https://shopify.dev/docs/api/liquid/filters/media-filters#image_tag)

## Common Liquid Patterns

### Product Card Snippet

```liquid
{%- comment -%}
Usage:
{% render 'product-card', product: product, show_vendor: false %}
{%- endcomment -%}

<div class="product-card">
  <a href="{{ product.url }}">
    {{ product.featured_image | image_tag: widths: '360, 720', loading: 'lazy' }}
    <h3>{{ product.title }}</h3>
    <p>{{ product.price | money }}</p>
  </a>
</div>
```

### Conditional Rendering

```liquid
{% liquid
  if section.settings.show_title
    assign title_visible = true
  else
    assign title_visible = false
  endif
%}

{% if title_visible %}
  <h2>{{ section.settings.title }}</h2>
{% endif %}
```

## Instructions

1. **Use `render`** for snippets, never `include`
2. **Add Usage comments** to all snippets
3. **Use `liquid` tag** for complex logic
4. **Always use `image_tag`** - never hardcode `<img>`
5. **Inline SVGs** using `inline_asset_content` filter
6. **Keep logic linear** - avoid deep nesting
7. **Use responsive images** with proper srcset and sizes
