---
name: templui
description: |
  WHEN: User is building Go/Templ web apps, using templUI components, converting sites to Templ,
  asking about templ syntax, Script() templates, HTMX/Alpine integration, JavaScript in templ,
  or working with .templ files. Also trigger when user mentions "component library", "UI components",
  "buttons/cards/modals/tables" in a Go web project, "templ generate", Alpine.js with Go,
  or asks how to build interactive UIs in Go without React/Vue. Activate whenever .templ files
  are present in the project or templUI is in dependencies.
  WHEN NOT: Non-Go projects, pure JavaScript/TypeScript frontend frameworks
---


<!-- cache:start -->

# templUI & HTMX/Alpine Best Practices
Apply templUI patterns and HTMX/Alpine.js best practices when building Go/Templ web applications.

## The Frontend Stack

The Go/Templ stack uses three complementary tools for interactivity:

| Tool | Purpose | Use For |
|------|---------|---------|
| **HTMX** | Server-driven interactions | AJAX requests, form submissions, partial page updates, live search |
| **Alpine.js** | Client-side state & reactivity | Toggles, animations, client-side filtering, transitions, local state |
| **templUI** | Pre-built UI components | Dropdowns, dialogs, tabs, sidebars (uses vanilla JS via Script() templates) |

**Note:** templUI components use vanilla JavaScript (not Alpine.js) via Script() templates. This is fine - Alpine.js is still part of the stack for your custom client-side needs.

---

## HTMX + Alpine.js Integration

HTMX and Alpine.js work great together. Use HTMX for server communication, Alpine for client-side enhancements.

### When to Use Each

```html
<!-- HTMX: Server-driven (fetches HTML from server) -->
<button hx-get="/api/users" hx-target="#user-list">Load Users</button>

<!-- Alpine: Client-side state (no server call) -->
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>
  <div x-show="open">Content</div>
</div>

<!-- Combined: HTMX loads data, Alpine filters it -->
<div x-data="{ filter: '' }">
  <input x-model="filter" placeholder="Filter...">
  <div hx-get="/users" hx-trigger="load">
    <template x-for="user in users.filter(u => u.name.includes(filter))">
      <div x-text="user.name"></div>
    </template>
  </div>
</div>
```

### Key Integration Patterns

**Alpine-Morph Extension**: Preserves Alpine state across HTMX swaps:
```html
<script src="https://unpkg.com/htmx.org/dist/ext/alpine-morph.js"></script>
<div hx-ext="alpine-morph" hx-swap="morph">...</div>
```

**htmx.process() for Alpine Conditionals**: When Alpine's `x-if` renders HTMX content:
```html
<template x-if="showForm">
  <form hx-post="/submit" x-init="htmx.process($el)">...</form>
</template>
```

**Triggering HTMX from Alpine**:
```html
<button @click="htmx.trigger($refs.form, 'submit')">Submit</button>
```

---

## templUI Components (Vanilla JS)

templUI components handle their own interactivity via Script() templates using vanilla JavaScript and Floating UI for positioning.

---

## CRITICAL: Templ Interpolation in JavaScript

**Go expressions `{ value }` do NOT interpolate inside `<script>` tags or inline event handlers.** They are treated as literal text, causing errors like:

```
GET http://localhost:8008/app/quotes/%7B%20id.String()%20%7D 400 (Bad Request)
```

The `%7B` and `%7D` are URL-encoded `{` and `}` - proof the expression wasn't evaluated.

### Pattern 1: Data Attributes (Recommended)

Use `data-*` attributes to pass Go values, then access via JavaScript:

```templ
<button
  data-quote-id={ quote.ID.String() }
  onclick="openPublishModal(this.dataset.quoteId)">
  Publish
</button>
```

For multiple values:
```templ
<div
  data-id={ item.ID.String() }
  data-name={ item.Name }
  data-status={ item.Status }
  onclick="handleClick(this.dataset)">
```

### Pattern 2: templ.JSFuncCall (for onclick handlers)

Automatically JSON-encodes arguments and prevents XSS:

```templ
<button onclick={ templ.JSFuncCall("openPublishModal", quote.ID.String()) }>
  Publish
</button>
```

With multiple arguments:
```templ
<button onclick={ templ.JSFuncCall("updateItem", item.ID.String(), item.Name, item.Active) }>
```

To pass the event object, use `templ.JSExpression`:
```templ
<button onclick={ templ.JSFuncCall("handleClick", templ.JSExpression("event"), quote.ID.String()) }>
```

### Pattern 3: Double-Braces Inside Script Strings

Inside `<script>` tags, use `{{ value }}` (double braces) for interpolation:

```templ
<script>
  const quoteId = "{{ quote.ID.String() }}";
  const itemName = "{{ item.Name }}";
  openPublishModal(quoteId);
</script>
```

Outside strings (bare expressions), values are JSON-encoded:
```templ
<script>
  const config = {{ templ.JSONString(config) }};
  const isActive = {{ item.Active }};  // outputs: true or false
</script>
```

### Pattern 4: templ.JSONString for Complex Data

Pass complex structs/maps to JavaScript via attributes:

```templ
<div data-config={ templ.JSONString(config) }>

<script>
  const el = document.querySelector('[data-config]');
  const config = JSON.parse(el.dataset.config);
</script>
```

Or use `templ.JSONScript`:
```templ
@templ.JSONScript("config-data", config)

<script>
  const config = JSON.parse(document.getElementById('config-data').textContent);
</script>
```

### Pattern 5: templ.OnceHandle for Reusable Scripts

Ensures scripts are only rendered once, even when component is used multiple times:

```templ
var publishHandle = templ.NewOnceHandle()

templ QuoteRow(quote Quote) {
  @publishHandle.Once() {
    <script>
      function openPublishModal(id) {
        fetch(`/api/quotes/${id}/publish`, { method: 'POST' });
      }
    </script>
  }
  <button
    data-id={ quote.ID.String() }
    onclick="openPublishModal(this.dataset.id)">
    Publish
  </button>
}
```

### When to Use Each Pattern

| Scenario | Use |
|----------|-----|
| Simple onclick with one value | Data attribute or `templ.JSFuncCall` |
| Multiple values needed in JS | Data attributes |
| Need event object | `templ.JSFuncCall` with `templ.JSExpression("event")` |
| Inline script with Go values | `{{ value }}` double braces |
| Complex object/struct | `templ.JSONString` or `templ.JSONScript` |
| Reusable script in loop | `templ.OnceHandle` |

### Common Mistakes

```templ
// WRONG - won't interpolate, becomes literal text
onclick="doThing({ id })"

// WRONG - single braces don't work in scripts
<script>const x = { value };</script>

// WRONG - Go expression in URL string inside script
<script>
  fetch(`/api/quotes/{ id }/publish`)  // BROKEN
</script>

// CORRECT alternatives:
onclick={ templ.JSFuncCall("doThing", id) }

<script>const x = "{{ value }}";</script>

<button data-id={ id } onclick="doFetch(this.dataset.id)">
```

---

## templUI CLI Tool

**Install CLI:**
```bash
go install github.com/templui/templui/cmd/templui@latest
```

**Key Commands:**
```bash
templui init                    # Initialize project, creates .templui.json
templui add button card         # Add specific components
templui add "*"                 # Add ALL components
templui add -f dropdown         # Force update existing component
templui list                    # List available components
templui new my-app              # Create new project
templui upgrade                 # Update CLI to latest version
```

**ALWAYS use the CLI to add/update components** - it fetches the complete component including Script() templates that may be missing if copied manually.

---

## Script() Templates - REQUIRED for Interactive Components

Components with JavaScript include a `Script()` template function. **You MUST add these to your base layout's `<head>`:**

```templ
// In your base layout <head>:
@popover.Script()      // Required for: popover, dropdown, tooltip, combobox
@dropdown.Script()     // Required for: dropdown
@dialog.Script()       // Required for: dialog, sheet, alertdialog
@accordion.Script()    // Required for: accordion, collapsible
@tabs.Script()         // Required for: tabs
@carousel.Script()     // Required for: carousel
@toast.Script()        // Required for: toast/sonner
@clipboard.Script()    // Required for: copybutton
```

**Component Dependencies:**
| Component | Requires Script() from |
|-----------|----------------------|
| dropdown | dropdown, popover |
| tooltip | popover |
| combobox | popover |
| sheet | dialog |
| alertdialog | dialog |
| collapsible | accordion |

**If a component doesn't work (no click events, no positioning), check that:**
1. The Script() template is called in the layout
2. The component was installed via CLI (not manually copied)
3. All dependency scripts are included

---

## Converting Sites to Templ/templUI

When converting HTML/React/Vue to Go/Templ:

**Conversion Process:**
1. Analyze existing UI patterns
2. Map to templUI base components
3. Convert syntax:
   - `class` stays as `class` in templ
   - `className` (React) → `class`
   - React/Vue event handlers → vanilla JS via Script() or HTMX
   - Dynamic content → templ expressions `{ variable }` or `@component()`
4. **Add required Script() templates to layout**
5. Set up proper Go package structure

**Templ Syntax Quick Reference:**
```templ
package components

type ButtonProps struct {
    Text    string
    Variant string
}

templ Button(props ButtonProps) {
    <button class={ "btn", props.Variant }>
        { props.Text }
    </button>
}

// Conditional
if condition {
    <span>Shown</span>
}

// Loops
for _, item := range items {
    <li>{ item.Name }</li>
}

// Composition
@Header()
@Content() {
    // Children
}
```

---

## Auditing for Better Component Usage

**Audit Checklist:**
1. **Script() Templates**: Are all required Script() calls in the base layout?
2. **CLI Installation**: Were components added via `templui add` or manually copied?
3. **Component Consistency**: Same patterns using same components?
4. **Base Component Usage**: Custom code that could use templUI?
5. **Dark Mode**: Tailwind dark: variants used?
6. **Responsive**: Mobile breakpoints applied?

**Common Issues to Check:**
- Missing `@popover.Script()` → dropdowns/tooltips don't open
- Missing `@dialog.Script()` → dialogs/sheets don't work
- Manually copied components missing Script() template files

---

## Import Pattern

```go
import "github.com/templui/templui/components/button"
import "github.com/templui/templui/components/dropdown"
import "github.com/templui/templui/components/dialog"
```

---

## Troubleshooting

**JavaScript URL contains literal `{` or `%7B` (URL-encoded brace):**
Go expressions don't interpolate in `<script>` tags. Use data attributes:
```templ
// WRONG: <script>fetch(`/api/{ id }`)</script>
// RIGHT:
<button data-id={ id } onclick="doFetch(this.dataset.id)">
```
See "CRITICAL: Templ Interpolation in JavaScript" section above.

**Component not responding to clicks:**
1. Check Script() is in layout: `@dropdown.Script()`, `@popover.Script()`
2. Reinstall: `templui add -f dropdown popover`
3. Check browser console for JS errors

**Dropdown/Tooltip not positioning correctly:**
1. Ensure `@popover.Script()` is in layout (uses Floating UI)
2. Reinstall popover: `templui add -f popover`

**Dialog/Sheet not opening:**
1. Add `@dialog.Script()` to layout
2. Reinstall: `templui add -f dialog`

---

## Resources

**templUI:**
- Documentation: https://templui.io/docs
- GitHub: https://github.com/templui/templui

**HTMX + Alpine.js:**
- [HTMX and Alpine.js: How to combine two great, lean front ends](https://www.infoworld.com/article/3856520/htmx-and-alpine-js-how-to-combine-two-great-lean-front-ends.html)
- [Full-Stack Go App with HTMX and Alpine.js](https://ntorga.com/full-stack-go-app-with-htmx-and-alpinejs/)
- [When to Add Alpine.js to htmx](https://dev.to/alex_aslam/when-to-add-alpinejs-to-htmx-9bj)
- [HTMX Alpine-Morph Extension](https://htmx.org/extensions/alpine-morph/)

**Templ:**
- Templ Docs: https://templ.guide

---

*This skill provides templUI and HTMX/Alpine.js best practices for Go/Templ web development.*

<!-- cache:end -->
