---
name: liquid-templating
description: Master Shopify Liquid templating language. Use this skill for writing Liquid code, using objects, filters, and tags, accessing product/collection/cart data, creating dynamic content, handling conditionals and loops, and working with Liquid best practices. Essential for theme customization.
license: MIT
compatibility: Works within Shopify themes and compatible Liquid environments
metadata:
  author: shopify-agent-skills
  version: "1.0"
  shopify-api-version: "2025-01"
---

# Shopify Liquid Templating

## When to use this skill

Use this skill when:

- Writing Liquid template code
- Accessing Shopify data (products, collections, cart, etc.)
- Using Liquid filters to transform output
- Creating conditional logic and loops
- Building dynamic theme content
- Debugging Liquid code issues
- Optimizing Liquid performance

## Liquid Basics

### Output Tags

Output data using double curly braces:

```liquid
{{ product.title }}
{{ shop.name }}
{{ 'hello' | upcase }}
```

### Logic Tags

Use logic with `{% %}` tags:

```liquid
{% if product.available %}
  <p>In Stock</p>
{% else %}
  <p>Sold Out</p>
{% endif %}
```

### Whitespace Control

Use `-` to strip whitespace:

```liquid
{%- if condition -%}
  content
{%- endif -%}
```

## Core Objects

### Product Object

```liquid
{{ product.title }}
{{ product.description }}
{{ product.price | money }}
{{ product.compare_at_price | money }}
{{ product.vendor }}
{{ product.type }}
{{ product.tags | join: ', ' }}
{{ product.available }}
{{ product.url }}

<!-- Featured Image -->
{{ product.featured_image | image_url: width: 500 | image_tag }}

<!-- All Images -->
{% for image in product.images %}
  {{ image | image_url: width: 300 | image_tag }}
{% endfor %}

<!-- Variants -->
{% for variant in product.variants %}
  {{ variant.title }} - {{ variant.price | money }}
{% endfor %}

<!-- Metafields -->
{{ product.metafields.custom.care_instructions }}
```

### Collection Object

```liquid
{{ collection.title }}
{{ collection.description }}
{{ collection.products_count }}
{{ collection.url }}

{% for product in collection.products %}
  {{ product.title }}
{% endfor %}

<!-- Pagination -->
{% paginate collection.products by 12 %}
  {% for product in collection.products %}
    {% render 'product-card', product: product %}
  {% endfor %}
  {{ paginate | default_pagination }}
{% endpaginate %}
```

### Cart Object

```liquid
{{ cart.item_count }}
{{ cart.total_price | money }}
{{ cart.total_weight | weight_with_unit }}

{% for item in cart.items %}
  {{ item.product.title }}
  {{ item.variant.title }}
  {{ item.quantity }}
  {{ item.line_price | money }}
{% endfor %}

<!-- Cart Attributes -->
{{ cart.attributes.gift_message }}

<!-- Cart Note -->
{{ cart.note }}
```

### Customer Object

```liquid
{% if customer %}
  Hello, {{ customer.first_name }}!
  {{ customer.email }}
  {{ customer.orders_count }} orders
  {{ customer.total_spent | money }}

  {% for address in customer.addresses %}
    {{ address.street }}
    {{ address.city }}, {{ address.province }}
  {% endfor %}
{% else %}
  <a href="/account/login">Log in</a>
{% endif %}
```

### Shop Object

```liquid
{{ shop.name }}
{{ shop.email }}
{{ shop.domain }}
{{ shop.money_format }}
{{ shop.currency }}
{{ shop.enabled_currencies }}
```

### Request Object

```liquid
{{ request.locale.iso_code }}
{{ request.page_type }}
{{ request.path }}
{{ request.host }}
```

## Essential Filters

### String Filters

```liquid
{{ 'hello world' | capitalize }}     <!-- Hello world -->
{{ 'hello world' | upcase }}         <!-- HELLO WORLD -->
{{ 'HELLO' | downcase }}             <!-- hello -->
{{ '  hello  ' | strip }}            <!-- hello -->
{{ 'hello' | append: ' world' }}     <!-- hello world -->
{{ 'hello world' | prepend: 'say ' }} <!-- say hello world -->
{{ 'hello' | replace: 'e', 'a' }}    <!-- hallo -->
{{ 'hello world' | split: ' ' }}     <!-- ['hello', 'world'] -->
{{ 'hello world' | truncate: 8 }}    <!-- hello... -->
{{ 'hello world' | truncatewords: 1 }} <!-- hello... -->
{{ 'hello' | size }}                 <!-- 5 -->
```

### Number Filters

```liquid
{{ 4.5 | ceil }}                     <!-- 5 -->
{{ 4.5 | floor }}                    <!-- 4 -->
{{ 4.567 | round: 2 }}               <!-- 4.57 -->
{{ 5 | plus: 3 }}                    <!-- 8 -->
{{ 5 | minus: 3 }}                   <!-- 2 -->
{{ 5 | times: 3 }}                   <!-- 15 -->
{{ 10 | divided_by: 3 }}             <!-- 3 -->
{{ 10 | modulo: 3 }}                 <!-- 1 -->
{{ 1234.56 | money }}                <!-- $1,234.56 -->
{{ 1234.56 | money_without_currency }} <!-- 1,234.56 -->
```

### Array Filters

```liquid
{{ array | first }}
{{ array | last }}
{{ array | size }}
{{ array | join: ', ' }}
{{ array | sort }}
{{ array | sort: 'price' }}
{{ array | reverse }}
{{ array | uniq }}
{{ array | compact }}
{{ array | concat: other_array }}
{{ array | map: 'title' }}
{{ array | where: 'available', true }}
```

### URL Filters

```liquid
{{ 'products' | url }}
{{ product.url | within: collection }}
{{ 'style.css' | asset_url }}
{{ 'image.png' | asset_url }}
{{ 'logo.png' | file_url }}
{{ product.featured_image | image_url: width: 500 }}
{{ product | product_image_url: 'master' }}
```

### Image Filters

```liquid
<!-- Modern image_url approach (recommended) -->
{{ image | image_url: width: 800 }}
{{ image | image_url: width: 800, height: 600, crop: 'center' }}
{{ image | image_url: width: 800 | image_tag }}

<!-- Responsive images -->
{{ image | image_url: width: 1200 | image_tag:
  loading: 'lazy',
  widths: '300, 600, 900, 1200',
  sizes: '(max-width: 600px) 100vw, 50vw'
}}

<!-- With alt text -->
{{ image | image_url: width: 500 | image_tag: alt: product.title }}
```

### Money Filters

```liquid
{{ product.price | money }}                    <!-- $10.00 -->
{{ product.price | money_with_currency }}      <!-- $10.00 USD -->
{{ product.price | money_without_trailing_zeros }} <!-- $10 -->
{{ product.price | money_without_currency }}   <!-- 10.00 -->
```

### Date Filters

```liquid
{{ article.created_at | date: '%B %d, %Y' }}   <!-- January 15, 2025 -->
{{ article.created_at | date: '%Y-%m-%d' }}    <!-- 2025-01-15 -->
{{ 'now' | date: '%H:%M' }}                    <!-- 14:30 -->
```

## Control Flow

### Conditionals

```liquid
{% if product.available %}
  In Stock
{% elsif product.compare_at_price %}
  Sale
{% else %}
  Sold Out
{% endif %}

<!-- Unless (opposite of if) -->
{% unless product.available %}
  Sold Out
{% endunless %}

<!-- Case/When -->
{% case product.type %}
  {% when 'Shirt' %}
    <p>It's a shirt!</p>
  {% when 'Pants' %}
    <p>It's pants!</p>
  {% else %}
    <p>Unknown type</p>
{% endcase %}
```

### Comparison Operators

```liquid
{% if product.price > 1000 %}{% endif %}
{% if product.price >= 1000 %}{% endif %}
{% if product.price < 1000 %}{% endif %}
{% if product.price <= 1000 %}{% endif %}
{% if product.title == 'Hat' %}{% endif %}
{% if product.title != 'Hat' %}{% endif %}
{% if product.tags contains 'sale' %}{% endif %}
{% if product.title %}{% endif %}              <!-- truthy check -->
{% if product.title == blank %}{% endif %}     <!-- blank check -->
```

### Logical Operators

```liquid
{% if product.available and product.price < 5000 %}
  Affordable and in stock!
{% endif %}

{% if product.type == 'Shirt' or product.type == 'Pants' %}
  It's clothing!
{% endif %}
```

## Loops

### For Loop

```liquid
{% for product in collection.products %}
  {{ forloop.index }}: {{ product.title }}
{% endfor %}

<!-- With limit and offset -->
{% for product in collection.products limit: 4 offset: 2 %}
  {{ product.title }}
{% endfor %}

<!-- Reversed -->
{% for product in collection.products reversed %}
  {{ product.title }}
{% endfor %}

<!-- Forloop variables -->
{% for item in array %}
  {{ forloop.index }}      <!-- 1, 2, 3... -->
  {{ forloop.index0 }}     <!-- 0, 1, 2... -->
  {{ forloop.first }}      <!-- true on first -->
  {{ forloop.last }}       <!-- true on last -->
  {{ forloop.length }}     <!-- total items -->
{% endfor %}

<!-- Else for empty -->
{% for product in collection.products %}
  {{ product.title }}
{% else %}
  No products found.
{% endfor %}
```

### Cycle

```liquid
{% for product in collection.products %}
  <div class="{% cycle 'odd', 'even' %}">
    {{ product.title }}
  </div>
{% endfor %}
```

### Tablerow

```liquid
<table>
  {% tablerow product in collection.products cols: 3 %}
    {{ product.title }}
  {% endtablerow %}
</table>
```

## Variables

### Assign

```liquid
{% assign my_variable = 'Hello' %}
{% assign price_in_dollars = product.price | divided_by: 100.0 %}
```

### Capture

```liquid
{% capture full_name %}
  {{ customer.first_name }} {{ customer.last_name }}
{% endcapture %}

<p>Hello, {{ full_name }}!</p>
```

### Increment/Decrement

```liquid
{% increment counter %}  <!-- 0 -->
{% increment counter %}  <!-- 1 -->
{% decrement counter %}  <!-- -1 -->
```

## Snippets and Sections

### Render Snippets

```liquid
<!-- Basic render -->
{% render 'product-card' %}

<!-- With variables -->
{% render 'product-card', product: product %}

<!-- With multiple variables -->
{% render 'product-card', product: product, show_price: true %}

<!-- For loop with render -->
{% render 'product-card' for collection.products as product %}
```

### Section Tags

```liquid
<!-- In layout file -->
{% section 'header' %}
{% sections 'footer-group' %}

<!-- Content placeholder -->
{{ content_for_layout }}
{{ content_for_header }}
```

## Forms

### Product Form

```liquid
{% form 'product', product %}
  <select name="id">
    {% for variant in product.variants %}
      <option value="{{ variant.id }}">{{ variant.title }}</option>
    {% endfor %}
  </select>
  <input type="number" name="quantity" value="1" min="1">
  <button type="submit">Add to Cart</button>
{% endform %}
```

### Contact Form

```liquid
{% form 'contact' %}
  <input type="email" name="contact[email]" required>
  <textarea name="contact[body]"></textarea>
  <button type="submit">Send</button>
{% endform %}
```

### Customer Forms

```liquid
<!-- Login -->
{% form 'customer_login' %}
  <input type="email" name="customer[email]">
  <input type="password" name="customer[password]">
  <button type="submit">Log In</button>
{% endform %}

<!-- Register -->
{% form 'create_customer' %}
  <input type="text" name="customer[first_name]">
  <input type="text" name="customer[last_name]">
  <input type="email" name="customer[email]">
  <input type="password" name="customer[password]">
  <button type="submit">Create Account</button>
{% endform %}
```

## Best Practices

1. **Use `render` not `include`** - `render` is faster and scopes variables
2. **Avoid complex logic in Liquid** - Move to JavaScript when possible
3. **Use descriptive variable names** - `{% assign product_price = ... %}`
4. **Leverage caching** - Use Liquid responsibly within sections
5. **Handle blank states** - Always check for `blank` or empty arrays
6. **Use schema defaults** - Provide sensible defaults in section schemas

## Common Patterns

### Sale Badge

```liquid
{% if product.compare_at_price > product.price %}
  {% assign savings = product.compare_at_price | minus: product.price %}
  {% assign percent_off = savings | times: 100.0 | divided_by: product.compare_at_price | round %}
  <span class="sale-badge">{{ percent_off }}% OFF</span>
{% endif %}
```

### Variant Selector

```liquid
{% unless product.has_only_default_variant %}
  {% for option in product.options_with_values %}
    <label>{{ option.name }}</label>
    <select name="options[{{ option.name }}]">
      {% for value in option.values %}
        <option value="{{ value }}">{{ value }}</option>
      {% endfor %}
    </select>
  {% endfor %}
{% endunless %}
```

## Resources

- [Liquid Reference](https://shopify.dev/docs/api/liquid)
- [Liquid Cheat Sheet](https://www.shopify.com/partners/shopify-cheat-sheet)
- [Objects Reference](https://shopify.dev/docs/api/liquid/objects)
- [Filters Reference](https://shopify.dev/docs/api/liquid/filters)
- [Tags Reference](https://shopify.dev/docs/api/liquid/tags)
