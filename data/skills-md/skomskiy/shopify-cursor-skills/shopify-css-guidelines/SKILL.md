---
name: shopify-css-guidelines
description: CSS naming conventions (BEM), nesting rules, and encapsulation guidelines for Shopify themes. Use when writing CSS for Shopify theme sections.
---

# Shopify CSS Guidelines

CSS naming conventions, nesting rules, and encapsulation practices for Shopify theme development.

## When to Use

- Writing CSS for Shopify theme sections
- Naming CSS classes
- Deciding when to use CSS nesting
- Encapsulating section styles

## CSS Naming - BEM Methodology

Use **BEM (Block Element Modifier)** methodology for structure inside a section:

```css
.block {}
.block__element {}
.block__element--modifier {}
```

### Naming Rules

- Class names should be **short, semantic, and intentional**
- Avoid generic or visual-based naming
- Use BEM structure: `.block__element--modifier`

### Examples

```css
/* Good - BEM structure */
.product-card {}
.product-card__image {}
.product-card__title {}
.product-card__price {}
.product-card__button {}
.product-card__button--primary {}

/* Bad - generic or visual naming */
.red-button {}
.big-text {}
.container {}
```

## CSS Scope & Encapsulation

Encapsulation is allowed:
- To avoid style leakage between sections
- To protect a section from theme-level styles
- **Only inside a section scope**

Each section should have its own scoped styles to prevent conflicts.

## CSS Nesting

Native CSS nesting is allowed, but with strict rules.

### When to Use Nesting

Use nesting **only where encapsulation is required**:
- Section-level namespacing
- Block → element structure inside a section
- Pseudo-classes and state modifiers

### Nesting Rules

- Nesting must stay **inside a section scope**
- Keep nesting depth minimal (**1–2 levels max**)
- Use nesting for BEM structure: `.block { .block__element {} }`

### Allowed Use Cases

```css
/* Section-level namespacing */
.featured-collection {
  padding: 2rem;
}

.featured-collection__grid {
  display: grid;
  gap: 1rem;
}

.featured-collection__item {
  /* Block element */
}

.featured-collection__item:hover {
  /* Pseudo-class */
}

.featured-collection__item--featured {
  /* Modifier */
}
```

### Not Allowed

- Deep nesting (more than 2 levels)
- Cross-block dependencies
- Assuming nested styles are globally reusable

```css
/* Bad - too deep */
.section {
  .block {
    .element {
      .sub-element {
        /* 3+ levels - avoid */
      }
    }
  }
}

/* Bad - cross-block dependency */
.section-a {
  .section-b__element {
    /* Don't style other sections' elements */
  }
}
```

## Section CSS Structure

Each section should have its own CSS file with scoped styles:

```css
/* featured-collection.css */
.featured-collection {
  /* Section wrapper */
}

.featured-collection__header {
  /* Section header */
}

.featured-collection__grid {
  /* Main content area */
}

.featured-collection__item {
  /* Grid item */
}

.featured-collection__item:hover {
  /* Hover state */
}

@media (max-width: 749px) {
  .featured-collection__grid {
    /* Mobile styles */
  }
}
```

## Shopify Theme Documentation

Reference these official Shopify resources:

- [Shopify Templates](https://shopify.dev/docs/themes/architecture/templates)
- [Liquid Filters](https://shopify.dev/docs/api/liquid/filters) (for CSS asset handling)

## Instructions

1. **Use BEM naming** for all classes inside sections
2. **Keep names semantic** - describe purpose, not appearance
3. **Encapsulate styles** within section scope
4. **Limit nesting** to 1–2 levels maximum
5. **One CSS file per section** - never mix multiple sections
6. **Use nesting** only for BEM structure and pseudo-classes
