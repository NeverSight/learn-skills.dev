---
name: unlayer-custom-tools
description: Builds custom drag-and-drop tools for the Unlayer editor — registering tools, adding property editors, creating custom widgets, head CSS/JS injection, tool configuration, and the custom# prefix convention.
---

# Build Custom Tools

## Overview

Custom tools are drag-and-drop content blocks you create for the Unlayer editor. Each tool needs:
- A **renderer** (what users see in the editor)
- **Exporters** (HTML output — must be table-based for email)
- **Property editors** (the settings panel)

## Complete Example: Product Card

This is a fully working custom tool with an image, title, price, and buy button:

```javascript
unlayer.registerTool({
  name: 'product_card',
  label: 'Product Card',
  icon: 'fa-shopping-cart',
  supportedDisplayModes: ['web', 'email'],

  options: {
    content: {
      title: 'Content',
      position: 1,
      options: {
        productTitle: {
          label: 'Product Title',
          defaultValue: 'Product Name',
          widget: 'text',               // → values.productTitle = 'Product Name'
        },
        productImage: {
          label: 'Image',
          defaultValue: { url: 'https://via.placeholder.com/300x200' },
          widget: 'image',              // → values.productImage.url = 'https://...'
        },
        price: {
          label: 'Price',
          defaultValue: '$99.99',
          widget: 'text',               // → values.price = '$99.99'
        },
        buttonText: {
          label: 'Button Text',
          defaultValue: 'Buy Now',
          widget: 'text',
        },
        buttonLink: {
          label: 'Button Link',
          defaultValue: { name: 'web', values: { href: 'https://example.com', target: '_blank' } },
          widget: 'link',               // → values.buttonLink.values.href = 'https://...'
        },
      },
    },
    colors: {
      title: 'Colors',
      position: 2,
      options: {
        titleColor: {
          label: 'Title Color',
          defaultValue: '#333333',
          widget: 'color_picker',       // → values.titleColor = '#333333'
        },
        buttonBg: {
          label: 'Button Background',
          defaultValue: '#007bff',
          widget: 'color_picker',
        },
      },
    },
  },

  values: {},

  renderer: {
    Viewer: unlayer.createViewer({
      render(values) {
        return `
          <div style="text-align: center; padding: 20px;">
            <img src="${values.productImage.url}" style="max-width: 100%;" />
            <h3 style="color: ${values.titleColor};">${values.productTitle}</h3>
            <p style="font-size: 24px; font-weight: bold;">${values.price}</p>
            <a href="${values.buttonLink.values.href}"
               style="display: inline-block; background: ${values.buttonBg};
                      color: #fff; padding: 12px 24px; text-decoration: none;
                      border-radius: 4px;">
              ${values.buttonText}
            </a>
          </div>
        `;
      },
    }),

    exporters: {
      web(values) {
        return `
          <div style="text-align: center; padding: 20px;">
            <img src="${values.productImage.url}" alt="${values.productTitle}" style="max-width: 100%;" />
            <h3 style="color: ${values.titleColor};">${values.productTitle}</h3>
            <p style="font-size: 24px; font-weight: bold;">${values.price}</p>
            <a href="${values.buttonLink.values.href}" target="${values.buttonLink.values.target}"
               style="display: inline-block; background: ${values.buttonBg};
                      color: #fff; padding: 12px 24px; text-decoration: none;">
              ${values.buttonText}
            </a>
          </div>
        `;
      },
      email(values) {
        // Email MUST use tables — divs break in Outlook/Gmail
        return `
          <table width="100%" cellpadding="0" cellspacing="0" border="0">
            <tr><td align="center" style="padding: 20px;">
              <img src="${values.productImage.url}" alt="${values.productTitle}"
                   style="max-width: 100%; display: block;" />
            </td></tr>
            <tr><td align="center" style="padding: 10px;">
              <h3 style="color: ${values.titleColor}; margin: 0;">${values.productTitle}</h3>
            </td></tr>
            <tr><td align="center">
              <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">${values.price}</p>
            </td></tr>
            <tr><td align="center" style="padding: 15px;">
              <table cellpadding="0" cellspacing="0" border="0">
                <tr><td style="background: ${values.buttonBg}; border-radius: 4px;">
                  <a href="${values.buttonLink.values.href}" target="${values.buttonLink.values.target}"
                     style="display: inline-block; color: #fff; padding: 12px 24px;
                            text-decoration: none;">
                    ${values.buttonText}
                  </a>
                </td></tr>
              </table>
            </td></tr>
          </table>
        `;
      },
    },

    head: {
      css(values) {
        return `#${values._meta.htmlID} img { max-width: 100%; height: auto; }`;
      },
      js(values) { return ''; },
    },
  },

  validator(data) {
    const { values, defaultErrors } = data;
    const errors = [];
    if (!values.productTitle) {
      errors.push({
        id: 'PRODUCT_TITLE_REQUIRED',
        icon: 'fa-warning',
        severity: 'ERROR',
        title: 'Missing product title',
        description: 'Product title is required',
      });
    }
    if (!values.productImage?.url) {
      errors.push({
        id: 'PRODUCT_IMAGE_REQUIRED',
        icon: 'fa-warning',
        severity: 'ERROR',
        title: 'Missing product image',
        description: 'Product image is required',
      });
    }
    return [...errors, ...defaultErrors];
  },
});
```

### Register it at init time with the `custom#` prefix:

```javascript
unlayer.init({
  tools: {
    'custom#product_card': {          // REQUIRED: custom# prefix
      data: {
        apiEndpoint: '/api/products', // Custom data accessible in renderer
      },
      properties: {
        // Override default property values or dropdown options
      },
    },
  },
});
```

---

## Widget Value Access Reference

How to read each widget type's value in your renderer:

| Widget | Default Value | Access in `render(values)` |
|--------|--------------|---------------------------|
| `text` | `'Hello'` | `values.myField` → `'Hello'` |
| `rich_text` | `'<p>Hello</p>'` | `values.myField` → `'<p>Hello</p>'` |
| `html` | `'<div>...</div>'` | `values.myField` → `'<div>...</div>'` |
| `color_picker` | `'#FF0000'` | `values.myField` → `'#FF0000'` |
| `alignment` | `'center'` | `values.myField` → `'center'` |
| `font_family` | `{label:'Arial', value:'arial'}` | `values.myField.value` → `'arial'` |
| `image` | `{url: 'https://...'}` | `values.myField.url` → `'https://...'` |
| `toggle` | `false` | `values.myField` → `false` |
| `link` | `{name:'web', values:{href,target}}` | `values.myField.values.href` → `'https://...'` |
| `counter` | `'10'` | `values.myField` → `'10'` (string!) |
| `dropdown` | `'option1'` | `values.myField` → `'option1'` |
| `datetime` | `'2025-01-01'` | `values.myField` → `'2025-01-01'` |
| `border` | `{borderTopWidth:'1px',...}` | `values.myField.borderTopWidth` → `'1px'` |

**Dropdown options** — pass via `unlayer.init()` under the tool's properties config:

```javascript
unlayer.init({
  tools: {
    'custom#product_card': {
      properties: {
        department: {
          editor: {
            data: {
              options: [
                { label: 'Sales', value: 'sales' },
                { label: 'Support', value: 'support' },
              ],
            },
          },
        },
      },
    },
  },
});
```

---

## Custom Property Editor (React)

For controls beyond built-in widgets:

```jsx
const RangeSlider = ({ label, value, updateValue, data }) => (
  <div>
    <label>{label}: {value}px</label>
    <input
      type="range"
      min={data.min || 0}
      max={data.max || 100}
      value={parseInt(value)}
      onChange={(e) => updateValue(e.target.value + 'px')}
    />
  </div>
);

unlayer.registerPropertyEditor({
  name: 'range_slider',
  Widget: RangeSlider,
});

// Use in your tool:
borderRadius: {
  label: 'Corner Radius',
  defaultValue: '4px',
  widget: 'range_slider',
  data: { min: 0, max: 50 },
},
```

---

## Validator Return Format

Each error must include `id`, `icon`, `severity`, `title`, and `description`:

```javascript
validator(data) {
  const { values, defaultErrors } = data;
  const errors = [];

  if (!values.productTitle) {
    errors.push({
      id: 'PRODUCT_TITLE_REQUIRED',     // Unique error ID
      icon: 'fa-warning',                // FontAwesome icon
      severity: 'ERROR',                 // 'ERROR' | 'WARNING'
      title: 'Missing product title',    // Short label
      description: 'Product title is required',  // Detailed message
    });
  }

  if (values.price && !values.price.startsWith('$')) {
    errors.push({
      id: 'PRICE_MISSING_CURRENCY',
      icon: 'fa-dollar-sign',
      severity: 'WARNING',
      title: 'Missing currency symbol',
      description: 'Price should include currency symbol',
      labelPath: 'price',               // Optional — highlights the property in the panel
    });
  }

  return [...errors, ...defaultErrors];  // Merge with built-in errors
}
```

---

## Email-Safe HTML Patterns

Email clients (Outlook, Gmail) require table-based HTML. Copy-paste these patterns:

**Button:**
```html
<table cellpadding="0" cellspacing="0" border="0">
  <tr><td style="background: #007bff; border-radius: 4px;">
    <a href="URL" style="display: inline-block; color: #fff; padding: 12px 24px; text-decoration: none;">
      Button Text
    </a>
  </td></tr>
</table>
```

**Two columns:**
```html
<table width="100%" cellpadding="0" cellspacing="0">
  <tr>
    <td width="50%" valign="top" style="padding: 10px;">Left</td>
    <td width="50%" valign="top" style="padding: 10px;">Right</td>
  </tr>
</table>
```

**Safe CSS properties:** `color`, `background-color`, `font-size`, `font-family`, `font-weight`, `text-align`, `padding`, `margin`, `border`, `width`, `max-width`, `display: block/inline-block`.

**Unsafe (avoid in email):** `flexbox`, `grid`, `position`, `float`, `box-shadow`, `border-radius` (partial support), `calc()`.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `custom#` prefix | Tools MUST use `custom#my_tool` in `tools` config at init |
| Div-based email exporter | Email exporters MUST return **table-based HTML** |
| Forgetting `_meta.htmlID` | Scope CSS: `#${values._meta.htmlID} { ... }` |
| Hardcoded values in renderer | Use `values` object — let property editors drive content |
| Wrong dropdown options format | Pass options via `unlayer.init()` under `tools['custom#name'].properties.prop.editor.data.options` |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Tool doesn't appear in editor | Check `supportedDisplayModes` includes current mode |
| Properties panel is empty | Check `options` structure — needs group → options nesting |
| Custom editor doesn't update | Ensure `updateValue()` is called with the new value |
| Exported HTML looks different | Check both `Viewer.render()` and `exporters.email/web()` |

## Resources

- [Create Custom Tool](https://docs.unlayer.com/builder/tools/custom/create)
- [Property Editors](https://docs.unlayer.com/builder/tools/custom/property-editors)
- [Advanced Options](https://docs.unlayer.com/builder/tools/custom/advanced-options)
- [Built-in Tools](https://docs.unlayer.com/builder/tools/built-in)
