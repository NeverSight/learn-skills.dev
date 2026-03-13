---
name: patterns
description: Reusable HTML page patterns and component blocks. Use when building common page types like FAQs, product listings, press releases, or other structured content.
allowed-tools: Read, Write, Edit
---

# HTML Patterns Skill

This skill provides reusable patterns for common page types and content blocks. Patterns combine semantic HTML with custom elements to create consistent, accessible structures.

## Philosophy

Pages are composed of **blocks** - reusable content patterns that appear across many pages. By defining custom elements for these blocks, we:

1. **Communicate intent** - `<faq-question>` is clearer than `<dt class="faq-q">`
2. **Enable styling** - Custom elements can be styled with CSS
3. **Support tooling** - Validators can enforce correct usage
4. **Document structure** - The markup is self-documenting

## Available Patterns

| Pattern | Elements | Use Case |
|---------|----------|----------|
| [FAQ](#faq-pattern) | `faq-list`, `faq-question`, `faq-answer` | Q&A pages, help sections |
| [Product Card](#product-card-pattern) | `product-card` | Product listings, catalogs |

---

## FAQ Pattern

### Elements

```
faq-list
├── faq-question
├── faq-answer
├── faq-question
├── faq-answer
└── ...
```

### Element Definitions

| Element | Content | Attributes |
|---------|---------|------------|
| `faq-list` | `faq-question`, `faq-answer` | `category` (optional) |
| `faq-question` | Phrasing content (text, links) | `id` (for anchor links) |
| `faq-answer` | Flow content (paragraphs, lists) | - |

### Usage

```html
<section id="products" aria-labelledby="products-heading">
  <h2 id="products-heading">Products</h2>
  <faq-list category="products">
    <faq-question id="faq-returns">What is your return policy?</faq-question>
    <faq-answer>We offer a 30-day hassle-free return policy.</faq-answer>

    <faq-question id="faq-shipping">How long does shipping take?</faq-question>
    <faq-answer>Standard shipping takes 5-7 business days.</faq-answer>
  </faq-list>
</section>
```

### Complete FAQ Page Structure

```html
<main id="main">
  <article>
    <h1>Frequently Asked Questions</h1>

    <!-- Table of contents -->
    <nav aria-label="FAQ sections">
      <ul>
        <li><a href="#products">Products</a></li>
        <li><a href="#shipping">Shipping</a></li>
      </ul>
    </nav>

    <!-- FAQ sections -->
    <section id="products" aria-labelledby="products-heading">
      <h2 id="products-heading">Products</h2>
      <faq-list category="products">
        <faq-question id="faq-q1">Question text?</faq-question>
        <faq-answer>Answer text.</faq-answer>
      </faq-list>
    </section>

    <!-- More sections... -->

    <!-- Call to action -->
    <aside>
      <p><strong>Still have questions?</strong></p>
      <p><a href="/contact">Contact us</a></p>
    </aside>
  </article>
</main>
```

### Accessibility Notes

- Each section has `aria-labelledby` pointing to its heading
- Questions have `id` attributes for direct linking
- Table of contents uses `<nav>` with descriptive `aria-label`
- Links within answers use proper `mailto:` and `tel:` protocols

---

## Product Card Pattern

### Element Definition

| Element | Content | Attributes |
|---------|---------|------------|
| `product-card` | Flow content | `sku`, `price` (optional) |

### Usage

```html
<product-card sku="WDG-PRO-001" price="79.99">
  <img src="widget-pro.jpg" alt="Widget Pro"/>
  <h3>Widget Pro</h3>
  <p>Our best-selling widget with enhanced durability.</p>
  <a href="/products/widget-pro">View details</a>
</product-card>
```

### Product Listing Structure

```html
<section aria-labelledby="products-heading">
  <h2 id="products-heading">Our Products</h2>
  <ul>
    <li>
      <product-card sku="WDG-001">
        <img src="widget.jpg" alt="Basic Widget"/>
        <h3>Basic Widget</h3>
        <p>Entry-level widget for beginners.</p>
      </product-card>
    </li>
    <!-- More products... -->
  </ul>
</section>
```

---

## Creating New Patterns

When you identify a repeating content structure:

1. **Define the elements** in `elements.json`
2. **Document the pattern** in this skill
3. **Create an example** in the examples directory
4. **Add to project dictionary** if needed

### Element Naming Conventions

- Use lowercase with hyphens: `pattern-element`
- Be descriptive: `faq-question` not `fq`
- Group related elements: `faq-list`, `faq-question`, `faq-answer`

---

## Page Type Patterns

Beyond component blocks, entire page types follow patterns:

| Page Type | Key Sections |
|-----------|--------------|
| Homepage | Hero, featured products, news, CTA |
| About | History, mission, values, leadership, milestones |
| Product List | Category nav, product grid, filters |
| Product Detail | Hero, specs, reviews, related |
| Contact | Info, form, map, hours |
| FAQ | TOC nav, categorized Q&A sections |
| Press Release | Headline, dateline, body, boilerplate, contacts |
| Legal | Numbered sections, definitions, effective date |

See individual examples in the `.claude/patterns/pages/` directory.

## Related Skills

- **xhtml-author** - Write valid XHTML-strict HTML5 markup
- **css-author** - Modern CSS organization with native @import, @layer casca...
- **progressive-enhancement** - HTML-first development with CSS-only interactivity patterns
- **forms** - HTML-first form patterns with CSS-only validation
