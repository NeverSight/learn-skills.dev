---
name: generateblocks-layouts
version: 2.0.0
description: Build layouts using GenerateBlocks V2 elements for WordPress
author: Gaurav Tiwari
trigger:
  - GenerateBlocks
  - GB blocks
  - GB layouts
  - HTML to GenerateBlocks
  - convert to GB
  - WordPress block layout
  - landing page section
tags:
  - wordpress
  - generateblocks
  - layouts
  - blocks
references:
  - references/block-types.md
  - references/css-patterns.md
  - references/svg-icons.md
  - references/responsive.md
  - references/troubleshooting.md
examples:
  - examples/basic/
  - examples/compound/
  - examples/layouts/
  - examples/svg/
---

# GenerateBlocks V2 Layout Builder

Build professional WordPress layouts using GenerateBlocks V2's four core blocks.

## Output Requirements

**ALWAYS output generated blocks to a file, never inline in the chat.**

- Output filename: `{section-name}.html` (e.g., `hero-section.html`, `services-grid.html`)
- For multiple sections: Create separate files or one combined file
- Include a brief summary in chat describing what was created

**Why file output?**
- Block code is often 100+ lines and breaks chat formatting
- Easier to copy/paste into WordPress
- Prevents truncation of long outputs
- Allows incremental building of complex layouts

## Quick Start

GenerateBlocks V2 uses four block types:

| Block | Class Pattern | Use For |
|-------|--------------|---------|
| `generateblocks/element` | `.gb-element-{id}` | Containers (div, section, article, header, nav, footer) |
| `generateblocks/text` | `.gb-text-{id}` | Text content (h1-h6, p, span, a, button) |
| `generateblocks/media` | `.gb-media-{id}` | Images (static only, no dynamic features) |
| `generateblocks/shape` | `.gb-shape-{id}` | SVG icons and decorative shapes |

## When to Use Core Blocks

For elements not available in GenerateBlocks or requiring advanced media features, use WordPress Core Blocks:

| Content Type | Use Core Block | Why |
|--------------|----------------|-----|
| Images with captions | `core/image` | Built-in caption support |
| Image galleries | `core/gallery` | Lightbox, columns, captions |
| Videos | `core/video` | Native video player, controls |
| Embedded media | `core/embed` | YouTube, Vimeo, Twitter, etc. |
| Audio files | `core/audio` | Native audio player |
| File downloads | `core/file` | Download links with filename |
| Tables | `core/table` | Structured data tables |
| Lists | `core/list` | Semantic ul/ol with `.list` class |
| Quotes | `core/quote` | Blockquote with citation |
| Code blocks | `core/code` | Preformatted code display |
| Separators | `core/separator` | Horizontal rules |
| Buttons (grouped) | `core/buttons` | Multiple button layouts |
| Columns (simple) | `core/columns` | Quick equal-width layouts |
| Cover images | `core/cover` | Background images with overlays |
| Dynamic post content | `core/post-*` | Post title, excerpt, featured image, etc. |
| Query loops | `core/query` | Dynamic content from posts |
| **Emojis** | `core/paragraph` | GenerateBlocks doesn't render emojis properly |

**Rule of thumb:** Use GenerateBlocks for layout structure and custom styling. Use Core Blocks for specialized content types and media with built-in functionality.

## Block Template

```html
<!-- wp:generateblocks/{type} {json_attributes} -->
<{tag} class="gb-{type} gb-{type}-{uniqueId}">
    {content}
</{tag}>
<!-- /wp:generateblocks/{type} -->
```

**Element blocks** add `"className":"gb-element"` to attributes. HTML class order: `gb-element-{id} gb-element`:
```html
<!-- wp:generateblocks/element {"uniqueId":"card001","tagName":"div","className":"gb-element",...} -->
<div class="gb-element-card001 gb-element">...</div>
<!-- /wp:generateblocks/element -->
```

## Required Attributes

Every block needs:
- `uniqueId` - Unique identifier (format: `{section}{number}` like `hero001`, `card023`)
- `tagName` - HTML element type
- `styles` - CSS properties as JSON object (camelCase). Supports responsive keys like `"@media (max-width:1024px)":{...}`
- `css` - Generated CSS string (kebab-case, minified, alphabetically sorted)
- `htmlAttributes` - Array of attribute objects (for links, IDs, data attributes)

Optional:
- `className` - Additional CSS classes (e.g., `"gb-element"` for element blocks, `"gb-element alignfull"` for full-width sections)
- `globalClasses` - Array of global CSS class slugs (e.g., `["lede"]`)
- `align` - Block alignment (`"full"` for full-width)

## CRITICAL: htmlAttributes Format

**htmlAttributes MUST be an array of objects, NOT a plain object:**

```json
// ✅ CORRECT - Array of objects
"htmlAttributes": [
  {"attribute": "href", "value": "/contact/"},
  {"attribute": "target", "value": "_blank"},
  {"attribute": "id", "value": "section-id"}
]

// ❌ WRONG - Plain object (causes block editor recovery errors)
"htmlAttributes": {"href": "/contact/", "target": "_blank"}
```

**linkHtmlAttributes** (for media blocks) uses the same array format:
```json
"linkHtmlAttributes": [
  {"attribute": "href", "value": "/product/"},
  {"attribute": "target", "value": "_blank"}
]
```

### Text `<a>` vs Element `<a>` Links

| Block Type | `htmlAttributes` for href | `href` in HTML | Use Case |
|-----------|--------------------------|----------------|----------|
| `generateblocks/text` with `tagName: "a"` | **No** - plugin manages link internally | **No** | Plain text buttons/links (no inner blocks) |
| `generateblocks/element` with `tagName: "a"` | **Yes** - `[{"attribute":"href","value":"/url/"}]` | **Yes** | Containers wrapping inner blocks (cards, icon buttons) |

**Rule:** Text `<a>` blocks are leaf blocks - the link URL is managed by the editor UI. Element `<a>` blocks are containers - they need explicit `htmlAttributes` for the href.

## Styling Approach

**Always use both `styles` AND `css` attributes:**

```json
{
  "uniqueId": "card001",
  "tagName": "div",
  "styles": {
    "backgroundColor": "#ffffff",
    "display": "flex",
    "padding": "2rem"
  },
  "css": ".gb-element-card001{background-color:#ffffff;display:flex;padding:2rem}"
}
```

**CSS rules:**
- The `css` attribute contains **only base styles** - no hover states, no transitions (the plugin generates those from the `styles` object)
- CSS properties must be **alphabetically sorted**
- Exceptions that go in `css`: pseudo-elements (::before/::after), media queries, animations, parent hover targeting children

```css
/* Base styles only (alphabetically sorted) + pseudo-elements + media queries */
.gb-element-card001{background-color:#ffffff;border-radius:1rem;display:flex;padding:2rem;position:relative}.gb-element-card001::after{content:'';position:absolute;bottom:0;left:0;width:100%;height:3px;background:#c0392b;transform:scaleX(0)}@media(max-width:768px){.gb-element-card001{padding:1rem}}
```

**Parent hover targeting children** is written in the child's `css`:
```css
.gb-element-card001:hover .gb-text-title001{color:#c0392b}
```

## Responsive Design

**Desktop-first approach with standard breakpoints:**

| Breakpoint | Width | Use For |
|------------|-------|---------|
| Desktop | 1025px+ | Default styles (no media query) |
| Tablet | 768px - 1024px | `@media(max-width:1024px)` |
| Mobile | < 768px | `@media(max-width:768px)` |

**Two approaches for responsive styles:**

1. **In `styles` object** (preferred for simple overrides):
```json
{
  "styles": {
    "display": "grid",
    "gridTemplateColumns": "minmax(0, 1fr) minmax(0, 1fr)",
    "gap": "4rem",
    "@media (max-width:1024px)": {
      "gridTemplateColumns": "minmax(0, 1fr)"
    }
  }
}
```

2. **In `css` string** (for complex responsive rules):
```css
.gb-element-hero001{display:grid;gap:4rem;grid-template-columns:minmax(0,1fr) minmax(0,1fr)}@media (max-width:1024px){.gb-element-hero001{grid-template-columns:minmax(0,1fr)}}
```

**Common responsive patterns:**
- Grid to single column: `grid-template-columns:minmax(0,1fr) minmax(0,1fr)` → `grid-template-columns:minmax(0,1fr)`
- Reduce padding: `padding:6rem 0` → `padding:4rem 0` → `padding:3rem 0`
- Reduce font sizes: Use `clamp()` for fluid typography
- Stack flex items: `flex-direction:row` → `flex-direction:column`
- Adjust gaps: `gap:4rem` → `gap:2rem`
- Center text on mobile: `text-align:left` → `text-align:center`

## Full-Width Section Pattern

For full-width sections with contained inner content:

```html
<!-- wp:generateblocks/element {"uniqueId":"hero001","tagName":"section","styles":{...},"css":"...","align":"full","className":"gb-element alignfull"} -->
<section class="gb-element-hero001 gb-element alignfull">
    <!-- wp:generateblocks/element {"uniqueId":"hero002","tagName":"div","styles":{"maxWidth":"var(\u002d\u002dgb-container-width)","marginLeft":"auto","marginRight":"auto"},"css":".gb-element-hero002{margin-left:auto;margin-right:auto;max-width:var(\u002d\u002dgb-container-width)}","className":"gb-element"} -->
    <div class="gb-element-hero002 gb-element">
        <!-- Inner content -->
    </div>
    <!-- /wp:generateblocks/element -->
</section>
<!-- /wp:generateblocks/element -->
```

**Key:**
- Outer section: `"align":"full"` + `"className":"gb-element alignfull"`
- Inner container: `maxWidth: "var(\u002d\u002dgb-container-width)"` (unicode-escaped `--gb-container-width`)

## Unique ID Convention

Format: `{section}{number}{letter}`

- **Section prefix**: 3-4 chars (`hero`, `serv`, `card`, `feat`, `blog`)
- **Number**: 001-999 sequential
- **Letter**: Optional for nested elements (`a`, `b`, `c`)

Examples: `hero001`, `serv023a`, `card014`, `feat007b`

## References

For detailed documentation, see:

- **[Block Types](references/block-types.md)** - Complete attribute specs for all four blocks
- **[CSS Patterns](references/css-patterns.md)** - Hover effects, transitions, gradients, pseudo-elements
- **[SVG Icons](references/svg-icons.md)** - Shape block usage and inline SVG patterns
- **[Responsive](references/responsive.md)** - Media queries and breakpoint patterns
- **[Troubleshooting](references/troubleshooting.md)** - Complex layout handling, chunking, error recovery

## Examples

See `/examples/` folder for copy-paste ready blocks:

- **basic/** - Single blocks (text, buttons, images)
- **compound/** - Combined blocks (cards, features, stats)
- **layouts/** - Full sections (hero, services, grid)
- **svg/** - Icons and decorative shapes

## CRITICAL: No Extra HTML Comments

**⛔ NEVER add HTML comments other than WordPress block markers.**

The ONLY allowed comments are WordPress block delimiters:
- `<!-- wp:generateblocks/element {...} -->` and `<!-- /wp:generateblocks/element -->`
- `<!-- wp:generateblocks/text {...} -->` and `<!-- /wp:generateblocks/text -->`
- `<!-- wp:generateblocks/media {...} -->` and `<!-- /wp:generateblocks/media -->`
- `<!-- wp:generateblocks/shape {...} -->` and `<!-- /wp:generateblocks/shape -->`
- `<!-- wp:image {...} -->` and `<!-- /wp:image -->`
- `<!-- wp:video {...} -->` and `<!-- /wp:video -->`
- `<!-- wp:embed {...} -->` and `<!-- /wp:embed -->`
- Any other `<!-- wp:{namespace}/{block} -->` format

**WRONG - These will break the block editor:**
```html
<!-- Hero Section -->
<!-- Card container -->
<!-- Button wrapper -->
<!-- This is a heading -->
<!-- Content goes here -->
```

**CORRECT - Only block delimiters:**
```html
<!-- wp:generateblocks/element {"uniqueId":"hero001",...,"className":"gb-element"} -->
<section class="gb-element-hero001 gb-element">
    <!-- wp:generateblocks/text {"uniqueId":"hero002",...} -->
    <h1 class="gb-text gb-text-hero002">Heading</h1>
    <!-- /wp:generateblocks/text -->
</section>
<!-- /wp:generateblocks/element -->
```

Any extra HTML comments will **break the WordPress block editor** and cause parsing errors. This is non-negotiable.

## Key Rules

1. **No custom CSS classes** - All styling in block attributes
2. **Minify CSS** - No line breaks in `css` attribute
3. **CSS = base styles only** - No hover states or transitions in `css` (the plugin generates those from the `styles` object). Exceptions: pseudo-elements, media queries, animations, parent hover targeting children
4. **Alphabetically sort CSS** - Properties in the `css` string must be alphabetically sorted
5. **Duplicate styles** - Put in both `styles` object AND `css` string
6. **Test responsive** - Add media queries for tablet (1024px) and mobile (768px)
7. **Text `<a>` = no htmlAttributes for href** - The link URL is managed by the editor UI internally
8. **Element `<a>` = use htmlAttributes for href** - Container links need explicit `[{"attribute":"href","value":"/url/"}]`
9. **Buttons with icons** - Use `generateblocks/element` (tagName `a`) wrapping `generateblocks/text` + `generateblocks/shape` blocks. Plain text buttons use `generateblocks/text`
10. **Shape blocks** - Use `styles.svg` for SVG-specific properties (fill, stroke, width, height) OR simple `styles` with width/height/color and inline SVG attributes. Both patterns work
11. **Lists use `core/list` with `.list` class** - Always use the native WordPress list block with `className: "list"` and customize styling as needed
12. **Use `--gb-container-width` for inner containers** - Set inner container width using the CSS variable; add `align: "full"` to parent section for full-width layouts
13. **htmlAttributes as array** - ALWAYS use array format: `[{"attribute":"href","value":"/link/"}]` NOT object format

## Design Inference (When CSS Not Provided)

When no CSS values are specified, infer styles based on context:

### GeneratePress Defaults
- Primary: `#0073e6`
- Text: `#222222`
- Body font: `17px`, line-height `1.7`
- H1: `42px`, H2: `35px`, H3: `29px`
- Section padding: `60px`
- Container max-width: `var(--gb-container-width)`
- Button padding: `15px 30px`

### gauravtiwari.org Design System
- Primary: `#c0392b`
- Text: `#0a0a0a`, Muted: `#5c5c5c`
- Background: `#ffffff`, Light: `#f5f5f3`
- Headings: font-weight `900`, tight letter-spacing
- Section padding: `4rem`
- Card radius: `1rem`, Button radius: `2rem`
- Hover lift: `translateY(-6px)`
- Shadow: `0 20px 60px rgba(0,0,0,0.15)`

## Complex Layout Strategy

For large sections (50+ blocks), break into chunks:

1. **Plan structure first** - Map components before coding
2. **Build bottom-up** - Start with innermost elements
3. **Test incrementally** - Verify each component works
4. **Use consistent IDs** - Same prefix for related elements

See [Troubleshooting](references/troubleshooting.md) for detailed guidance on complex layouts.
