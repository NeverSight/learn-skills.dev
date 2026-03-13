---
name: shopify-javascript-standards
description: JavaScript standards for Shopify themes - custom elements, file structure, and best practices. Use when writing JavaScript for Shopify theme sections.
---

# Shopify JavaScript Standards

JavaScript file structure, custom elements, and coding standards for Shopify theme development.

## When to Use

- Writing JavaScript for Shopify theme sections
- Creating interactive components
- Setting up JavaScript file structure
- Using custom HTML elements

## File Structure

### Separate JavaScript Files

- JavaScript must live in a **separate file** in the `assets/` directory
- Include it in the section using the `asset_url` filter

### Including JavaScript in Sections

```liquid
<script src="{{ 'section-logic.js' | asset_url }}" defer="defer"></script>
```

**Always use `defer`** to ensure scripts load after HTML parsing.

### File Naming

Match JavaScript file names to section names:

```
sections/
  └── product-quick-view.liquid

assets/
  └── product-quick-view.js
```

## JavaScript Rules

### Variable Declarations

- Use only `const` and `let`
- **Never use `var`**
- Avoid global scope pollution

### Example

```javascript
// Good
const productId = document.querySelector('[data-product-id]').dataset.productId;
let isOpen = false;

// Bad
var productId = ...; // Never use var
window.myVariable = ...; // Avoid global pollution
```

### Scope Management

Keep variables scoped to their usage:

```javascript
// Good - scoped within function
function initProductCard() {
  const card = document.querySelector('.product-card');
  const button = card.querySelector('.product-card__button');
  // ...
}

// Bad - global variables
const card = document.querySelector('.product-card'); // Global scope
```

## Custom Elements

### Use Custom HTML Elements

Use **custom HTML elements** to encapsulate JavaScript logic and create reusable components.

### Custom Element Structure

```javascript
class ProductQuickView extends HTMLElement {
  constructor() {
    super();
    this.init();
  }

  init() {
    this.button = this.querySelector('[data-trigger]');
    this.modal = this.querySelector('[data-modal]');
    this.closeButton = this.querySelector('[data-close]');
    
    this.button?.addEventListener('click', () => this.open());
    this.closeButton?.addEventListener('click', () => this.close());
  }

  open() {
    this.modal?.classList.add('is-open');
  }

  close() {
    this.modal?.classList.remove('is-open');
  }
}

customElements.define('product-quick-view', ProductQuickView);
```

### Using Custom Elements in Liquid

```liquid
<product-quick-view data-product-id="{{ product.id }}">
  <button data-trigger>Quick View</button>
  <div data-modal class="modal">
    <button data-close>Close</button>
    <!-- Modal content -->
  </div>
</product-quick-view>
```

### Custom Element Benefits

- Encapsulation - logic is self-contained
- Reusability - use anywhere in the theme
- Lifecycle hooks - `connectedCallback`, `disconnectedCallback`
- Data attributes - pass data via `data-*` attributes

### Lifecycle Hooks

```javascript
class MyComponent extends HTMLElement {
  connectedCallback() {
    // Element added to DOM
    this.init();
  }

  disconnectedCallback() {
    // Element removed from DOM
    this.cleanup();
  }

  init() {
    // Setup logic
  }

  cleanup() {
    // Cleanup logic (remove event listeners, etc.)
  }
}
```

## Data Attributes

### Passing Data to JavaScript

- Use custom HTML tags when appropriate
- Pass dynamic data via `data-*` attributes
- Access data via `dataset` property

### Example

```liquid
<product-card 
  data-product-id="{{ product.id }}"
  data-product-handle="{{ product.handle }}"
  data-variant-id="{{ product.selected_or_first_available_variant.id }}">
  <!-- Content -->
</product-card>
```

```javascript
class ProductCard extends HTMLElement {
  constructor() {
    super();
    this.productId = this.dataset.productId;
    this.productHandle = this.dataset.productHandle;
    this.variantId = this.dataset.variantId;
  }
}
```

## Observers

### Use Observers Only When Explicitly Requested

Use observers (IntersectionObserver, MutationObserver, etc.) **only if explicitly requested** by the user.

### IntersectionObserver Example

```javascript
// Only use if explicitly needed
class LazyImage extends HTMLElement {
  constructor() {
    super();
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.loadImage();
          this.observer.unobserve(this);
        }
      });
    });
  }

  connectedCallback() {
    this.observer.observe(this);
  }

  loadImage() {
    const img = this.querySelector('img');
    img.src = img.dataset.src;
  }
}
```

## Best Practices

### Event Handling

```javascript
class ProductForm extends HTMLElement {
  constructor() {
    super();
    this.form = this.querySelector('form');
    this.form?.addEventListener('submit', this.handleSubmit.bind(this));
  }

  handleSubmit(event) {
    event.preventDefault();
    // Handle form submission
  }

  disconnectedCallback() {
    // Clean up event listeners
    this.form?.removeEventListener('submit', this.handleSubmit);
  }
}
```

### Error Handling

```javascript
class ProductCard extends HTMLElement {
  init() {
    try {
      const button = this.querySelector('[data-add-to-cart]');
      if (!button) {
        console.warn('Add to cart button not found');
        return;
      }
      button.addEventListener('click', this.handleAddToCart.bind(this));
    } catch (error) {
      console.error('Error initializing product card:', error);
    }
  }
}
```

## Shopify Theme Documentation

Reference these official Shopify resources:

- [Shopify Theme JavaScript](https://shopify.dev/docs/themes/architecture/theme-assets)
- [Web Components](https://developer.mozilla.org/en-US/docs/Web/Web_Components)
- [Custom Elements](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_custom_elements)
- [Data Attributes](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/data-*)

## Complete Example

### Section File

```liquid
{{ 'product-card.css' | asset_url | stylesheet_tag }}

<product-card 
  data-product-id="{{ product.id }}"
  data-product-handle="{{ product.handle }}">
  <div class="product-card">
    {{ image | image_tag: widths: '360, 720, 1080', loading: 'lazy' }}
    <h3>{{ product.title }}</h3>
    <button data-add-to-cart>Add to Cart</button>
  </div>
</product-card>

<script src="{{ 'product-card.js' | asset_url }}" defer="defer"></script>
```

### JavaScript File

```javascript
class ProductCard extends HTMLElement {
  constructor() {
    super();
    this.productId = this.dataset.productId;
    this.init();
  }

  init() {
    const button = this.querySelector('[data-add-to-cart]');
    button?.addEventListener('click', () => this.addToCart());
  }

  async addToCart() {
    try {
      const response = await fetch('/cart/add.js', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id: this.productId,
          quantity: 1
        })
      });
      // Handle response
    } catch (error) {
      console.error('Error adding to cart:', error);
    }
  }
}

customElements.define('product-card', ProductCard);
```

## Instructions

1. **Separate JS files** - one file per section in `assets/` directory
2. **Use `defer`** when including scripts
3. **Use `const` and `let`** - never `var`
4. **Use custom elements** to encapsulate logic
5. **Pass data via `data-*` attributes**
6. **Avoid global scope pollution**
7. **Use observers only when explicitly requested**
8. **Clean up event listeners** in `disconnectedCallback`
