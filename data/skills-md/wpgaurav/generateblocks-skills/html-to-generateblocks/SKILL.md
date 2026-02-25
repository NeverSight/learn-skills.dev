---
name: html-to-generateblocks
version: 2.0.0
description: Convert HTML/CSS layouts to GenerateBlocks V2 format with inline styles
author: Gaurav Tiwari
updated: 2026-01-22
trigger:
  - HTML to GenerateBlocks
  - convert to GB
  - convert HTML to blocks
  - GenerateBlocks conversion
tags:
  - wordpress
  - generateblocks
  - conversion
  - html
---

# HTML to GenerateBlocks V2 Conversion

Convert HTML/CSS layouts to GenerateBlocks V2 format using inline styles in block attributes.

## Output Requirements

**ALWAYS output converted blocks to a file, never inline in the chat.**

- Output filename: `{original-name}-converted.html` (e.g., `hero-converted.html`)
- For large conversions: Split into multiple files by section
- Include a brief summary in chat describing what was converted

**Why file output?**
- Converted block code is often 100+ lines
- Easier to copy/paste into WordPress
- Prevents truncation and formatting issues
- Allows side-by-side comparison with original

## Core Principle

**Use both `styles` and `css` attributes:**
- `styles`: Basic properties (padding, margin, colors, display, flex, grid). Supports responsive keys like `"@media (max-width:1024px)":{...}`
- `css`: Base styles only (alphabetically sorted). Exceptions that go in `css`: pseudo-elements (::before/::after), media queries, animations, parent hover targeting children

**The `css` attribute must NOT contain hover states or transitions** - the plugin generates those from the `styles` object.

**Never use BEM or custom classes** - all styling goes in block attributes.

## When to Use Core Blocks

For HTML elements not available in GenerateBlocks, use WordPress Core Blocks:

| HTML Element | Convert To | Reason |
|--------------|------------|--------|
| `<video>` | `core/video` | Native player controls, autoplay, loop |
| `<audio>` | `core/audio` | Native audio player |
| `<iframe>` (YouTube, Vimeo) | `core/embed` | oEmbed support, responsive sizing |
| `<table>` | `core/table` | Semantic table structure |
| `<figure>` with `<figcaption>` | `core/image` | Built-in caption support |
| `<blockquote>` with cite | `core/quote` | Semantic quote with citation |
| `<pre>` / `<code>` | `core/code` | Preformatted code display |
| `<ul>` / `<ol>` (semantic lists) | `core/list` | Use with `.list` class |
| `<hr>` | `core/separator` | Horizontal rule |
| Gallery layouts | `core/gallery` | Lightbox, columns, captions |
| Background image sections | `core/cover` | Parallax, overlay, focal point |
| **Text with emojis** | `core/paragraph` | GenerateBlocks doesn't render emojis properly |

**Conversion rule:** Use GenerateBlocks for layout containers and styled text. Use Core Blocks for specialized content types that have built-in functionality (players, embeds, tables, etc.).

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

## Block Structure

### Standard Element Block

Element blocks add `"className":"gb-element"` to attributes. HTML class order: `gb-element-{id} gb-element`:

```html
<!-- wp:generateblocks/element {"uniqueId":"elem001","tagName":"div","styles":{"display":"flex","gap":"1rem","padding":"2rem"},"css":".gb-element-elem001{display:flex;gap:1rem;padding:2rem}@media(max-width:768px){.gb-element-elem001{flex-direction:column}}","className":"gb-element"} -->
<div class="gb-element-elem001 gb-element">
    <!-- Inner content -->
</div>
<!-- /wp:generateblocks/element -->
```

### Text Block (for headings, paragraphs, links)

```html
<!-- wp:generateblocks/text {"uniqueId":"text001","tagName":"h2","styles":{"fontSize":"2rem","fontWeight":"900","color":"#0a0a0a"},"css":".gb-text-text001{font-size:2rem;font-weight:900;color:#0a0a0a}"} -->
<h2 class="gb-text gb-text-text001">Heading Text</h2>
<!-- /wp:generateblocks/text -->
```

### Link as Card Wrapper

Cards with inner blocks use `generateblocks/element` (not `text`) with `tagName: "a"`:

```html
<!-- wp:generateblocks/element {"uniqueId":"card001","tagName":"a","htmlAttributes":[{"attribute":"href","value":"/services/"}],"styles":{"backgroundColor":"white","borderRadius":"1rem","display":"flex","flexDirection":"column","padding":"2rem","textDecoration":"none"},"css":".gb-element-card001{background-color:white;border-radius:1rem;display:flex;flex-direction:column;padding:2rem;text-decoration:none}","className":"gb-element"} -->
<a class="gb-element-card001 gb-element" href="/services/">
    <!-- Inner blocks (text, media, shape) -->
</a>
<!-- /wp:generateblocks/element -->
```

**Plain text links** (no inner blocks) use `generateblocks/text` with `tagName: "a"` — no `htmlAttributes` for href:

```html
<!-- wp:generateblocks/text {"uniqueId":"link001","tagName":"a","styles":{"color":"#c0392b","fontSize":"0.9375rem","fontWeight":"600","textDecoration":"none"},"css":".gb-text-link001{color:#c0392b;font-size:0.9375rem;font-weight:600;text-decoration:none}"} -->
<a class="gb-text gb-text-link001">Learn more</a>
<!-- /wp:generateblocks/text -->
```

### Media/Image Block

```html
<!-- wp:generateblocks/media {"uniqueId":"img001","mediaType":"image","htmlAttributes":[{"attribute":"src","value":"https://example.com/image.jpg"},{"attribute":"alt","value":"Description"},{"attribute":"loading","value":"lazy"},{"attribute":"width","value":"600"},{"attribute":"height","value":"400"}],"styles":{"display":"block","width":"100%"},"css":".gb-media-img001{display:block;width:100%}"} -->
<img class="gb-media gb-media-img001" src="https://example.com/image.jpg" alt="Description" loading="lazy" width="600" height="400" />
<!-- /wp:generateblocks/media -->
```

## Text `<a>` vs Element `<a>` Links

| Block Type | `htmlAttributes` for href | `href` in HTML | Use Case |
|-----------|--------------------------|----------------|----------|
| `generateblocks/text` with `tagName: "a"` | **No** - plugin manages link internally | **No** | Plain text buttons/links (no inner blocks) |
| `generateblocks/element` with `tagName: "a"` | **Yes** - `[{"attribute":"href","value":"/url/"}]` | **Yes** | Containers wrapping inner blocks (cards, icon buttons) |

**Rule:** Text `<a>` blocks are leaf blocks - the link URL is managed by the editor UI. Element `<a>` blocks are containers - they need explicit `htmlAttributes` for the href.

**Buttons with icons** use `generateblocks/element` (tagName `a`) wrapping `generateblocks/text` + `generateblocks/shape` blocks. Plain text buttons use `generateblocks/text`.

## Styles vs CSS Decision Matrix

| Feature | Use `styles` | Use `css` |
|---------|-------------|-----------|
| Layout (display, flex, grid) | ✅ | Also in CSS (base styles) |
| Spacing (padding, margin, gap) | ✅ | Also in CSS (base styles) |
| Colors (background, text) | ✅ | Also in CSS (base styles) |
| Typography (font-size, weight) | ✅ | Also in CSS (base styles) |
| Basic borders, border-radius | ✅ | Also in CSS (base styles) |
| Responsive overrides | ✅ `"@media (max-width:1024px)":{...}` | Also in CSS |
| Hover states | ✅ via `styles` object | ❌ **Never in `css`** (plugin generates) |
| Transitions | ✅ via `styles` object | ❌ **Never in `css`** (plugin generates) |
| Pseudo-elements (::before/::after) | ❌ | ✅ Only CSS |
| Media queries | ✅ (simple overrides) | ✅ (complex rules) |
| Animations (@keyframes) | ❌ | ✅ Only CSS |
| Parent hover targeting children | ❌ | ✅ Only CSS (in child's `css`) |

**Pattern**: Put base properties in both `styles` and `css` (alphabetically sorted). The `css` attribute contains base styles plus exceptions (pseudo-elements, media queries, animations, parent-hover-child selectors). **Never put hover states or transitions in `css`.**

## Common Patterns

### Card with Animated Underline

Cards with inner blocks use `generateblocks/element`. Pseudo-elements (::after) and parent-hover-pseudo go in `css`. Hover states and transitions do NOT go in `css`.

```html
<!-- wp:generateblocks/element {"uniqueId":"card001","tagName":"a","htmlAttributes":[{"attribute":"href","value":"/link/"}],"styles":{"backgroundColor":"white","border":"1px solid transparent","borderRadius":"1rem","display":"flex","flexDirection":"column","padding":"2rem","position":"relative","textDecoration":"none"},"css":".gb-element-card001{background-color:white;border:1px solid transparent;border-radius:1rem;display:flex;flex-direction:column;padding:2rem;position:relative;text-decoration:none}.gb-element-card001::after{background:#c0392b;bottom:0;content:'';height:3px;left:0;position:absolute;transform:scaleX(0);transform-origin:left;transition:transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);width:100%}.gb-element-card001:hover::after{transform:scaleX(1)}","className":"gb-element"} -->
<a class="gb-element-card001 gb-element" href="/link/">
    <!-- Inner blocks -->
</a>
<!-- /wp:generateblocks/element -->
```

### Grid Layout (Responsive)

```html
<!-- wp:generateblocks/element {"uniqueId":"grid001","tagName":"div","styles":{"display":"grid","gridTemplateColumns":"repeat(4, minmax(0, 1fr))","gap":"1rem"},"css":".gb-element-grid001{display:grid;grid-template-columns:repeat(4, minmax(0, 1fr));gap:1rem}@media(max-width:1024px){.gb-element-grid001{grid-template-columns:repeat(2, minmax(0, 1fr))!important}}@media(max-width:768px){.gb-element-grid001{grid-template-columns:1fr!important}}"} -->
<div class="gb-element gb-element-grid001">
    <!-- Grid items -->
</div>
<!-- /wp:generateblocks/element -->
```

### Icon (Shape Block with SVG)

SVG icons use `generateblocks/shape`. Two valid approaches:

**Approach 1: `styles.svg` object** (plugin generates `.gb-shape-{id} svg{...}` CSS):
```html
<!-- wp:generateblocks/shape {"uniqueId":"icon001","styles":{"alignItems":"center","backgroundColor":"#f5f5f3","borderRadius":"1rem","color":"#c0392b","display":"flex","height":"3.5rem","justifyContent":"center","width":"3.5rem","svg":{"fill":"none","height":"1.5rem","stroke":"currentColor","width":"1.5rem"}},"css":".gb-shape-icon001{align-items:center;background-color:#f5f5f3;border-radius:1rem;color:#c0392b;display:flex;height:3.5rem;justify-content:center;width:3.5rem}.gb-shape-icon001 svg{fill:none;height:1.5rem;stroke:currentColor;width:1.5rem}.gb-element-card001:hover .gb-shape-icon001{background-color:#c0392b;color:white;transform:scale(1.05) rotate(-3deg)}"} -->
<span class="gb-shape gb-shape-icon001"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg></span>
<!-- /wp:generateblocks/shape -->
```

**Approach 2: Simple styles** (for quick inline icons):
```html
<!-- wp:generateblocks/shape {"uniqueId":"check001","styles":{"color":"#10b981","height":"20px","width":"20px"},"css":".gb-shape-check001{color:#10b981;height:20px;width:20px}"} -->
<span class="gb-shape gb-shape-check001"><svg stroke-linejoin="round" stroke-linecap="round" stroke-width="3" stroke="currentColor" fill="none" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></span>
<!-- /wp:generateblocks/shape -->
```

**Parent hover targeting icons** is written in the shape block's `css` (as shown in Approach 1).

### Featured Card (Dark, Span Multiple Columns)

```html
<!-- wp:generateblocks/element {"uniqueId":"feat001","tagName":"div","styles":{"background":"linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)","borderRadius":"1rem","display":"flex","flexDirection":"column","gap":"1rem","gridColumn":"span 2","gridRow":"span 2","minHeight":"26rem","padding":"2rem","position":"relative"},"css":".gb-element-feat001{background:linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);border-radius:1rem;display:flex;flex-direction:column;gap:1rem;grid-column:span 2;grid-row:span 2;min-height:26rem;padding:2rem;position:relative}.gb-element-feat001::before{background:radial-gradient(circle at 100% 0%, rgba(192, 57, 43, 0.2) 0%, transparent 60%);content:'';height:100%;pointer-events:none;position:absolute;right:0;top:0;width:60%}.gb-element-feat001>*{position:relative;z-index:1}@media(max-width:1024px){.gb-element-feat001{grid-column:span 2;grid-row:span 1;min-height:auto}}@media(max-width:768px){.gb-element-feat001{grid-column:span 1}}","className":"gb-element"} -->
<div class="gb-element-feat001 gb-element">
    <!-- Featured card content -->
</div>
<!-- /wp:generateblocks/element -->
```

### Badge (Absolute Position)

```html
<!-- wp:generateblocks/text {"uniqueId":"badge001","tagName":"span","styles":{"backgroundColor":"#c0392b","borderRadius":"2rem","color":"white","fontSize":"0.75rem","fontWeight":"600","letterSpacing":"0.05em","padding":"0.25rem 0.625rem","position":"absolute","right":"1rem","textTransform":"uppercase","top":"1rem"},"css":".gb-text-badge001{background-color:#c0392b;border-radius:2rem;color:white;font-size:0.75rem;font-weight:600;letter-spacing:0.05em;padding:0.25rem 0.625rem;position:absolute;right:1rem;text-transform:uppercase;top:1rem}"} -->
<span class="gb-text gb-text-badge001">Recommended</span>
<!-- /wp:generateblocks/text -->
```

## Dynamic Content with Query Blocks

For sections with dynamic WordPress posts, use native query blocks with GenerateBlocks for styling:

```html
<!-- wp:query {"queryId":1,"query":{"perPage":12,"postType":"post","order":"desc","orderBy":"date","taxQuery":{"category":{"terms":[],"operator":"NOT IN"}}}} -->
<div class="wp-block-query">
    <!-- wp:post-template {"style":{"spacing":{"blockGap":"1rem"}}} -->

        <!-- wp:generateblocks/element {"uniqueId":"post001","tagName":"a","styles":{"backgroundColor":"white","border":"1px solid #e5e5e5","borderRadius":"1rem","display":"flex","flexDirection":"column","overflow":"hidden","textDecoration":"none"},"css":".gb-element-post001{background-color:white;border:1px solid #e5e5e5;border-radius:1rem;display:flex;flex-direction:column;overflow:hidden;text-decoration:none}","className":"gb-element"} -->
        <a class="gb-element-post001 gb-element">
            <!-- wp:post-featured-image {"isLink":false,"aspectRatio":"12/5"} /-->

            <!-- wp:generateblocks/element {"uniqueId":"post002","tagName":"div","styles":{"display":"flex","flex":"1","flexDirection":"column","padding":"1rem"},"css":".gb-element-post002{display:flex;flex:1;flex-direction:column;padding:1rem}","className":"gb-element"} -->
            <div class="gb-element-post002 gb-element">
                <!-- wp:post-title {"isLink":false,"style":{"typography":{"fontSize":"1.125rem","fontWeight":"700"}}} /-->
                <!-- wp:post-excerpt {"excerptLength":14} /-->
            </div>
            <!-- /wp:generateblocks/element -->
        </a>
        <!-- /wp:generateblocks/element -->

    <!-- /wp:post-template -->
</div>
<!-- /wp:query -->
```

## Unique ID Convention

- Format: `{section}{number}{letter}` (e.g., `hero001a`, `serv023`, `tool014`)
- Section prefix: 3-4 characters (hero, serv, tool, blog, feat)
- Number: Sequential 001-999
- Optional letter: For nested elements (a, b, c)

## Conversion Workflow

1. **Read original HTML/CSS** - Understand structure and styles
2. **Identify sections** - Break into logical components
3. **Map BEM classes to blocks** - Each `.block__element` becomes a GenerateBlocks element
4. **Extract base styles** - Put in `styles` attribute
5. **Extract complex styles** - Put in `css` attribute (pseudo-elements, media queries, parent-hover-child). Never put hover states or transitions in `css`
6. **Create unique IDs** - Follow convention
7. **Test responsive behavior** - Ensure media queries work
8. **Handle dynamic content** - Use WordPress query blocks

## CSS Syntax Rules

### In `styles` attribute (JavaScript object):
```json
{
  "display": "flex",
  "flexDirection": "column",
  "backgroundColor": "#ffffff",
  "borderRadius": "1rem",
  "marginBottom": "2rem"
}
```

### In `css` attribute (CSS string):
```css
.gb-element-id{background-color:#ffffff;border-radius:1rem;display:flex;flex-direction:column;margin-bottom:2rem}@media(max-width:768px){.gb-element-id{flex-direction:row}}
```

**Rules:**
- CSS must be minified (no line breaks, minimal spaces)
- Properties must be **alphabetically sorted**
- Contains **base styles only** — no hover states, no transitions
- Exceptions: pseudo-elements (::before/::after), media queries, animations, parent hover targeting children

## Responsive Patterns

### Mobile-First Grid
```css
.gb-element-grid{display:grid;grid-template-columns:1fr}@media(min-width:768px){.gb-element-grid{grid-template-columns:repeat(2, minmax(0, 1fr))}}@media(min-width:1024px){.gb-element-grid{grid-template-columns:repeat(4, minmax(0, 1fr))}}
```

### Desktop-First Grid (Match Original)
```css
.gb-element-grid{display:grid;grid-template-columns:repeat(4, minmax(0, 1fr));gap:1rem}@media(max-width:1024px){.gb-element-grid{grid-template-columns:repeat(2, minmax(0, 1fr))!important}}@media(max-width:768px){.gb-element-grid{grid-template-columns:1fr!important}}
```

### Sticky Sidebar
```css
.gb-element-sidebar{position:sticky;top:calc(var(--header-height, 80px) + 1rem)}@media(max-width:1024px){.gb-element-sidebar{position:static}}
```

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
<!-- This is a card -->
<!-- Section header -->
<!-- Hero content goes here -->
<!-- Button wrapper -->
```

**CORRECT - Only block delimiters:**
```html
<!-- wp:generateblocks/element {"uniqueId":"card001",...} -->
<div class="gb-element gb-element-card001">
    <!-- wp:image {"id":123} -->
    <figure class="wp-block-image"><img src="image.jpg" alt=""/></figure>
    <!-- /wp:image -->
</div>
<!-- /wp:generateblocks/element -->
```

Any extra HTML comments will **break the WordPress block editor** and cause parsing errors. This is non-negotiable. Do NOT add descriptive comments, section labels, or any other HTML comments.

### Design Inference (When CSS Not Provided)

When converting HTML without explicit CSS values, infer styles based on context:

**GeneratePress Defaults:**
- Primary: `#0073e6`
- Text: `#222222`, Muted: `#757575`
- Body: `17px`, line-height `1.7`
- H1: `42px`, H2: `35px`, H3: `29px`
- Section padding: `60px`
- Container max-width: `var(--gb-container-width)`

**gauravtiwari.org Design System:**
- Primary: `#c0392b`
- Text: `#0a0a0a`, Muted: `#5c5c5c`
- Background: `#ffffff`, Light: `#f5f5f3`
- Headings: font-weight `900`, letter-spacing `-0.03em`
- Section padding: `4rem`
- Card radius: `1rem`, Button radius: `2rem`
- Hover lift: `translateY(-6px)`
- Shadow: `0 20px 60px rgba(0,0,0,0.15)`

## Common Gotchas

1. **No HTML comments except block markers** - Breaks WordPress block editor
2. **Always escape quotes in CSS strings** - Use single quotes for content, attr values
3. **Duplicate properties** - Put in both `styles` and `css` for consistency
4. **CSS alphabetically sorted** - Properties in the `css` string must be sorted alphabetically
5. **No hover/transitions in `css`** - The plugin generates hover states and transitions from the `styles` object. Never put these in the `css` attribute
6. **Cards with inner blocks = element block** - Use `generateblocks/element` (not `text`) for cards containing other blocks. Text blocks are leaf blocks (no inner blocks)
7. **Text `<a>` = no htmlAttributes for href** - Link URL managed by editor UI. Element `<a>` = use `htmlAttributes` for href
8. **SVG icons = shape blocks** - Use `generateblocks/shape` for SVGs, not `generateblocks/element` with raw SVG inside
9. **Pseudo-elements need content** - `content:''` for ::before/::after (these go in `css`)
10. **Parent hover targeting children** - Written in the child's `css`: `.gb-element-card001:hover .gb-text-title001{color:#c0392b}`
11. **Gradients only in CSS** - Can't use in `styles` attribute
12. **CSS variables work** - Use `var(--custom-property)` freely. Use `\u002d\u002d` for `--` in JSON
13. **Element blocks need className** - Add `"className":"gb-element"` to element block attributes
14. **Use !important sparingly** - Only for overriding at breakpoints
15. **Lists use `core/list` with `.list` class** - Convert `<ul>`/`<ol>` to native WordPress list block with `className: "list"`
16. **Use `--gb-container-width` for inner containers** - Set inner container width using the CSS variable; add `align: "full"` to parent section
17. **Buttons with icons** - Use `generateblocks/element` (tagName `a`) wrapping `generateblocks/text` + `generateblocks/shape` blocks. Plain text buttons use `generateblocks/text`

## Performance Notes

- Inline styles are fast (no external CSS file)
- Each block's CSS is scoped to its unique ID
- GenerateBlocks automatically deduplicates common styles
- Media queries only load when needed
- Use `content-visibility: auto` for off-screen sections

## Example: Complete Hero Section

See `to-convert/home-hero-v2.html` for a complete real-world example with:
- Complex grid layout
- Multiple nested components
- Responsive breakpoints
- Hover effects
- Icon fonts
- Images with overlays
