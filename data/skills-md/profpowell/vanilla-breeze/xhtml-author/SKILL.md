---
name: xhtml-author
description: Write valid XHTML-strict HTML5 markup. Use when creating HTML files, editing markup, building web pages, or writing any HTML content. Ensures semantic structure and XHTML syntax.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# XHTML Authoring Skill

## Syntax Rules (MUST follow)

1. **Self-closing void elements**: `<br/>`, `<hr/>`, `<img/>`, `<meta/>`, `<link/>`, `<input/>`
2. **Lowercase everything**: Tags and attributes must be lowercase
3. **Quote all attributes**: Always use double quotes `attr="value"`
4. **Close all tags**: No implicit closing
5. **Single h1**: One `<h1>` per page only
6. **Lowercase doctype**: Use `<!doctype html>` not `<!DOCTYPE html>`

## Semantic Structure (MUST use)

Use semantic HTML5 elements instead of `<div>`:

| Element | Purpose |
|---------|---------|
| `<header>` | Page or section header |
| `<nav>` | Navigation blocks |
| `<main>` | Primary content (one per page) |
| `<article>` | Self-contained content |
| `<section>` | Thematic grouping with heading |
| `<aside>` | Tangentially related content |
| `<footer>` | Page or section footer |
| `<figure>` | Self-contained media with caption |
| `<figcaption>` | Caption for figure |
| `<hgroup>` | Heading group |

## Div Alternatives (NEVER use `<div>`)

The `<div>` element is **blacklisted** in this project. Always use semantic alternatives:

| Instead of... | Use... |
|---------------|--------|
| `<div class="header">` | `<header>` |
| `<div class="nav">` | `<nav>` |
| `<div class="footer">` | `<footer>` |
| `<div class="sidebar">` | `<aside>` |
| `<div class="content">` | `<main>` or `<article>` |
| `<div class="section">` | `<section>` with heading |
| `<div class="card">` | `<article>` or custom element like `<product-card>` |
| `<div class="wrapper">` | Style the parent element directly |
| `<div class="container">` | Use CSS on `<body>` or parent landmark |
| `<div class="grid">` | `<ul>` or `<ol>` with CSS grid |

### Layout Wrappers

For layout constraints (centering, max-width), apply CSS directly to semantic elements:

```css
/* Instead of <div class="header-content"> inside <header> */
header {
  max-width: var(--max-width);
  margin-inline: auto;
  padding-inline: var(--space-md);
}

/* For edge-to-edge backgrounds with centered content */
header {
  background: var(--color-primary);
  /* Use padding for the content area */
  padding: var(--space-md) max(var(--space-md), calc((100% - var(--max-width)) / 2));
}
```

### When No Semantic Element Exists

If you truly need a generic container (rare), use a custom element with semantic naming:

```html
<x-layout-grid>...</x-layout-grid>
<x-card-group>...</x-card-group>
```

## Template

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Page Title</title>
</head>
<body>
  <header>
    <nav aria-label="Main navigation">
      <ul>
        <li><a href="#main">Skip to content</a></li>
      </ul>
    </nav>
    <h1>Main Heading</h1>
  </header>

  <main id="main">
    <article>
      <h2>Article Title</h2>
      <p>Content here.</p>
    </article>
  </main>

  <footer>
    <p>Footer content</p>
  </footer>
</body>
</html>
```

## Void Elements (self-closing)

These elements MUST use self-closing syntax:

```html
<area/>
<base/>
<br/>
<col/>
<embed/>
<hr/>
<img src="photo.jpg" alt="Description"/>
<input type="text" name="field"/>
<link rel="stylesheet" href="style.css"/>
<meta charset="utf-8"/>
<source src="video.mp4" type="video/mp4"/>
<track src="captions.vtt" kind="captions"/>
<wbr/>
```

## Custom Elements

- Defined elements: Check `elements.json` for available custom elements
- Ad-hoc elements: Use `x-*` prefix for one-off custom elements

See [SYNTAX.md](SYNTAX.md) for complete syntax rules.
See [ELEMENTS.md](ELEMENTS.md) for semantic element guidance.
See [EXAMPLES.md](EXAMPLES.md) for code examples.

## Skills to Consider Before Writing

When creating HTML, also invoke these skills based on content:

| Content Type | Invoke Skill | Why |
|--------------|--------------|-----|
| Any icon or visual indicator | **icons** | Use `<icon-wc>`, never inline SVG |
| Form elements | **forms** | Use `<form-field>` custom element |
| Images | **responsive-images** | Use `<picture>` with srcset |
| Page head content | **metadata** | SEO, social, performance hints |
| Dialogs, popovers, toggles | **progressive-enhancement** | Use `command`/`commandfor` attributes |
| Interactive elements | **accessibility-checker** | WCAG2AA compliance |

### Critical: Icons

**NEVER use inline SVGs.** When adding any visual indicator, icon button, or toggle with an icon:

```html
<!-- WRONG -->
<svg viewBox="0 0 24 24">...</svg>

<!-- CORRECT - invoke icons skill first -->
<icon-wc name="menu" label="Menu"></icon-wc>
```

See the **icons** skill for the full pattern.

### Critical: Interactive Elements

**Use declarative `command`/`commandfor` attributes** for dialogs and popovers—never `onclick`:

```html
<!-- WRONG - inline JavaScript -->
<button onclick="document.getElementById('modal').showModal()">
  Open
</button>

<!-- CORRECT - declarative attributes -->
<button commandfor="modal" command="show-modal">
  Open
</button>
<dialog id="modal">
  <h2>Modal Title</h2>
  <button commandfor="modal" command="close">Close</button>
</dialog>

<!-- CORRECT - popover pattern -->
<button commandfor="menu" command="toggle-popover">
  Menu
</button>
<nav popover id="menu">
  <!-- Navigation items -->
</nav>
```

| Command | Target | Effect |
|---------|--------|--------|
| `show-modal` | `<dialog>` | Opens as modal |
| `close` | `<dialog>` | Closes dialog |
| `toggle-popover` | `[popover]` | Toggles popover |
| `show-popover` | `[popover]` | Opens popover |
| `hide-popover` | `[popover]` | Closes popover |

See the **progressive-enhancement** skill for complete patterns.

## Related Skills

- **icons** - Lucide icon library with `<icon-wc>` Web Component
- **forms** - HTML-first form patterns with CSS-only validation
- **responsive-images** - Modern responsive image techniques
- **metadata** - HTML metadata and head content
- **progressive-enhancement** - Declarative dialogs/popovers with `command`/`commandfor`
- **accessibility-checker** - Ensure WCAG2AA accessibility compliance
- **css-author** - Modern CSS organization with @layer
- **javascript-author** - Vanilla JavaScript for Web Components
