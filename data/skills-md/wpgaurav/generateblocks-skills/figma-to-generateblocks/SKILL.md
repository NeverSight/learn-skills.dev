---
name: figma-to-generateblocks
version: 1.0.0
description: Convert Figma designs to GenerateBlocks V2 format for WordPress
author: Gaurav Tiwari
updated: 2026-01-22
trigger:
  - Figma to GenerateBlocks
  - convert Figma
  - Figma design to WordPress
  - Figma to GB
  - implement Figma design
  - Figma screenshot
  - design to blocks
tags:
  - wordpress
  - generateblocks
  - figma
  - conversion
  - design
---

# Figma to GenerateBlocks Converter

Convert Figma designs to clean, semantic GenerateBlocks V2 blocks for WordPress.

## Output Requirements

**ALWAYS output converted blocks to a file, never inline in the chat.**

- Output filename: `{design-name}.html` (e.g., `homepage-hero.html`, `pricing-section.html`)
- For complex designs: Split into multiple files by section
- Include a brief summary in chat describing what was created

**Why file output?**
- Block code is often 100+ lines
- Easier to copy/paste into WordPress
- Prevents truncation and formatting issues
- Allows iterative refinement of design implementation

## Input Types

This skill handles multiple Figma input formats:

| Input Type | How to Process |
|------------|----------------|
| **Screenshot/Image** | Analyze visual layout, colors, typography, spacing |
| **Figma URL** | Extract design tokens if Dev Mode access available |
| **Copied CSS** | Parse Figma's generated CSS values |
| **Design specs** | Use provided measurements and colors |
| **Verbal description** | Infer from user's description of the design |

## Conversion Workflow

### Step 1: Analyze the Design

Extract these elements from the Figma design:

**Layout Structure:**
- Container hierarchy (sections, rows, columns)
- Grid/flex layout patterns
- Spacing between elements (gaps, padding, margins)
- Alignment (center, start, end, space-between)

**Typography:**
- Font families (map to web-safe or Google Fonts)
- Font sizes (convert to rem/clamp for responsiveness)
- Font weights (100-900)
- Line heights
- Letter spacing
- Text colors

**Colors:**
- Background colors
- Text colors
- Border colors
- Gradient definitions
- Opacity/transparency

**Spacing:**
- Padding values
- Margin values
- Gap between elements
- Section spacing

**Visual Effects:**
- Border radius
- Box shadows
- Hover states (infer from design variants)
- Transitions

### Step 2: Map to GenerateBlocks

| Figma Element | GenerateBlocks Block |
|---------------|---------------------|
| Frame/Section | `generateblocks/element` with `tagName: "section"` |
| Auto Layout (horizontal) | `generateblocks/element` with `display: flex` |
| Auto Layout (vertical) | `generateblocks/element` with `display: flex; flex-direction: column` |
| Grid | `generateblocks/element` with `display: grid` |
| Text | `generateblocks/text` with appropriate `tagName` |
| Image (simple) | `generateblocks/media` |
| Icon/Vector | `generateblocks/shape` with inline SVG |
| Button (text only) | `generateblocks/text` with `tagName: "a"` (no `htmlAttributes` for href) |
| Button (with icon) | `generateblocks/element` with `tagName: "a"` wrapping `text` + `shape` blocks |
| Card (clickable, has inner blocks) | `generateblocks/element` with `tagName: "a"` + `htmlAttributes` for href |
| Card (non-clickable) | `generateblocks/element` with `tagName: "div"` |
| Link (plain text) | `generateblocks/text` with `tagName: "a"` (no `htmlAttributes` for href) |

### Step 2b: When to Use Core Blocks

Some Figma elements should convert to WordPress Core Blocks instead:

| Figma Element | Use Core Block | Reason |
|---------------|----------------|--------|
| Image with caption | `core/image` | Built-in caption support |
| Image gallery/grid | `core/gallery` | Lightbox, columns, captions |
| Video player | `core/video` | Native video controls |
| Embedded video (YouTube/Vimeo) | `core/embed` | oEmbed support |
| Audio player | `core/audio` | Native audio controls |
| Data table | `core/table` | Semantic table structure |
| Quote with attribution | `core/quote` | Semantic blockquote |
| Code snippet | `core/code` | Preformatted code display |
| Bulleted/numbered list | `core/list` | Semantic list structure |
| Hero with background image | `core/cover` | Background image, overlay, parallax |
| Horizontal divider | `core/separator` | Semantic hr element |
| Download link/file | `core/file` | Download button with filename |
| **Text with emojis** | `core/paragraph` | GenerateBlocks doesn't render emojis properly |

**Conversion rule:** Use GenerateBlocks for custom layouts and styled containers. Use Core Blocks for content types with built-in functionality (media players, embeds, tables, etc.).

### Step 3: Generate Block Code

Use this structure for each block:

```html
<!-- wp:generateblocks/{type} {"uniqueId":"{id}","tagName":"{tag}","styles":{...},"css":"..."} -->
<{tag} class="gb-{type} gb-{type}-{id}">
    {content}
</{tag}>
<!-- /wp:generateblocks/{type} -->
```

## Figma CSS to GenerateBlocks

### Typography Conversion

**Figma CSS:**
```css
font-family: Inter;
font-size: 48px;
font-weight: 700;
line-height: 120%;
letter-spacing: -0.02em;
```

**GenerateBlocks:**
```json
{
  "styles": {
    "fontFamily": "'Inter', sans-serif",
    "fontSize": "clamp(2rem, 5vw, 3rem)",
    "fontWeight": "700",
    "lineHeight": "1.2",
    "letterSpacing": "-0.02em"
  },
  "css": ".gb-text-head001{font-family:'Inter', sans-serif;font-size:clamp(2rem, 5vw, 3rem);font-weight:700;letter-spacing:-0.02em;line-height:1.2}"
}
```

### Auto Layout to Flexbox

**Figma Auto Layout:**
- Direction: Horizontal
- Gap: 24px
- Padding: 32px
- Align: Center

**GenerateBlocks:**
```json
{
  "styles": {
    "display": "flex",
    "flexDirection": "row",
    "gap": "1.5rem",
    "padding": "2rem",
    "alignItems": "center"
  },
  "css": ".gb-element-row001{align-items:center;display:flex;flex-direction:row;gap:1.5rem;padding:2rem}"
}
```

### Grid Layout

**Figma Grid (3 columns, 24px gap):**

**GenerateBlocks:**
```json
{
  "styles": {
    "display": "grid",
    "gridTemplateColumns": "repeat(3, minmax(0, 1fr))",
    "gap": "1.5rem"
  },
  "css": ".gb-element-grid001{display:grid;gap:1.5rem;grid-template-columns:repeat(3, minmax(0, 1fr))}@media(max-width:1024px){.gb-element-grid001{grid-template-columns:repeat(2, minmax(0, 1fr))}}@media(max-width:768px){.gb-element-grid001{grid-template-columns:1fr}}"
}
```

### Shadow Conversion

**Figma Shadow:**
- X: 0, Y: 20px
- Blur: 60px
- Color: rgba(0, 0, 0, 0.15)

**GenerateBlocks:**
```json
{
  "styles": {
    "boxShadow": "0 20px 60px rgba(0,0,0,0.15)"
  },
  "css": ".gb-element-card001{box-shadow:0 20px 60px rgba(0,0,0,0.15)}"
}
```

### Border Radius

**Figma:** Corner radius: 16px

**GenerateBlocks:**
```json
{
  "styles": {
    "borderRadius": "1rem"
  },
  "css": ".gb-element-card001{border-radius:1rem}"
}
```

## Responsive Conversion

Figma designs are typically at desktop width. Add responsive breakpoints:

### Breakpoint Strategy

| Figma Width | Target | Media Query |
|-------------|--------|-------------|
| 1440px | Desktop | Base styles |
| 1024px | Tablet | `@media(max-width:1024px)` |
| 768px | Mobile landscape | `@media(max-width:768px)` |
| 375px | Mobile | `@media(max-width:480px)` |

### Font Size Scaling

Convert fixed Figma sizes to fluid typography:

| Figma Size | GenerateBlocks |
|------------|----------------|
| 64px | `clamp(2.5rem, 5vw, 4rem)` |
| 48px | `clamp(2rem, 4vw, 3rem)` |
| 36px | `clamp(1.75rem, 3vw, 2.25rem)` |
| 24px | `clamp(1.25rem, 2vw, 1.5rem)` |
| 18px | `1.125rem` |
| 16px | `1rem` |
| 14px | `0.875rem` |

### Spacing Scaling

| Figma Spacing | GenerateBlocks |
|---------------|----------------|
| 80px | `4rem` (desktop), `2rem` (mobile) |
| 60px | `3rem` (desktop), `1.5rem` (mobile) |
| 40px | `2rem` (desktop), `1rem` (mobile) |
| 24px | `1.5rem` |
| 16px | `1rem` |
| 8px | `0.5rem` |

## Common Figma Patterns

### Hero Section

**Figma structure:**
```
Frame (Hero)
├── Frame (Content)
│   ├── Text (Tagline)
│   ├── Text (Headline)
│   ├── Text (Description)
│   └── Frame (Buttons)
│       ├── Button (Primary)
│       └── Button (Secondary)
└── Image (Hero Image)
```

**GenerateBlocks:**
```html
<!-- wp:generateblocks/element {"uniqueId":"hero001","tagName":"section","styles":{"paddingBottom":"4rem","paddingTop":"4rem","@media (max-width:768px)":{"paddingBottom":"2rem","paddingTop":"2rem"}},"css":".gb-element-hero001{padding-bottom:4rem;padding-top:4rem}@media(max-width:768px){.gb-element-hero001{padding-bottom:2rem;padding-top:2rem}}","className":"gb-element"} -->
<section class="gb-element-hero001 gb-element">
    <!-- wp:generateblocks/element {"uniqueId":"hero002","tagName":"div","styles":{"alignItems":"center","display":"grid","gap":"3rem","gridTemplateColumns":"minmax(0, 1fr) minmax(0, 1fr)","marginLeft":"auto","marginRight":"auto","maxWidth":"var(--gb-container-width)","paddingLeft":"1rem","paddingRight":"1rem","@media (max-width:768px)":{"gridTemplateColumns":"1fr","textAlign":"center"}},"css":".gb-element-hero002{align-items:center;display:grid;gap:3rem;grid-template-columns:minmax(0, 1fr) minmax(0, 1fr);margin-left:auto;margin-right:auto;max-width:var(--gb-container-width);padding-left:1rem;padding-right:1rem}@media(max-width:768px){.gb-element-hero002{grid-template-columns:1fr;text-align:center}}","className":"gb-element"} -->
    <div class="gb-element-hero002 gb-element">
        <!-- wp:generateblocks/element {"uniqueId":"hero003","tagName":"div","styles":{"display":"flex","flexDirection":"column","gap":"1.5rem"},"css":".gb-element-hero003{display:flex;flex-direction:column;gap:1.5rem}","className":"gb-element"} -->
        <div class="gb-element-hero003 gb-element">
            <!-- Tagline, Headline, Description, Buttons -->
        </div>
        <!-- /wp:generateblocks/element -->
        <!-- wp:generateblocks/media ... -->
    </div>
    <!-- /wp:generateblocks/element -->
</section>
<!-- /wp:generateblocks/element -->
```

### Card Component

**Figma structure:**
```
Frame (Card)
├── Image
├── Frame (Content)
│   ├── Text (Title)
│   ├── Text (Description)
│   └── Link (Read more)
```

**GenerateBlocks (clickable card):**

Cards with inner blocks use `generateblocks/element` (not `text`) with `tagName: "a"`. Hover states and transitions are managed by the `styles` object — never put them in `css`.

```html
<!-- wp:generateblocks/element {"uniqueId":"card001","tagName":"a","htmlAttributes":[{"attribute":"href","value":"/link/"}],"styles":{"backgroundColor":"white","border":"1px solid #e5e5e5","borderRadius":"1rem","display":"flex","flexDirection":"column","overflow":"hidden","textDecoration":"none"},"css":".gb-element-card001{background-color:white;border:1px solid #e5e5e5;border-radius:1rem;display:flex;flex-direction:column;overflow:hidden;text-decoration:none}","className":"gb-element"} -->
<a class="gb-element-card001 gb-element" href="/link/">
    <!-- wp:generateblocks/media {"uniqueId":"card002","mediaType":"image","htmlAttributes":[{"attribute":"src","value":"image.jpg"},{"attribute":"alt","value":"Card image"}],"styles":{"aspectRatio":"16/9","objectFit":"cover","width":"100%"},"css":".gb-media-card002{aspect-ratio:16/9;object-fit:cover;width:100%}"} -->
    <img class="gb-media gb-media-card002" src="image.jpg" alt="Card image" />
    <!-- /wp:generateblocks/media -->
    <!-- wp:generateblocks/element {"uniqueId":"card003","tagName":"div","styles":{"display":"flex","flexDirection":"column","gap":"0.75rem","padding":"1.5rem"},"css":".gb-element-card003{display:flex;flex-direction:column;gap:0.75rem;padding:1.5rem}","className":"gb-element"} -->
    <div class="gb-element-card003 gb-element">
        <!-- Title, Description -->
    </div>
    <!-- /wp:generateblocks/element -->
</a>
<!-- /wp:generateblocks/element -->
```

### Navigation Bar

**Figma structure:**
```
Frame (Nav)
├── Logo
├── Frame (Links)
│   ├── Link
│   ├── Link
│   └── Link
└── Button (CTA)
```

**GenerateBlocks:**
```html
<!-- wp:generateblocks/element {"uniqueId":"nav001","tagName":"header","styles":{"alignItems":"center","display":"flex","justifyContent":"space-between","padding":"1rem 0"},"css":".gb-element-nav001{align-items:center;display:flex;justify-content:space-between;padding:1rem 0}","className":"gb-element"} -->
<header class="gb-element-nav001 gb-element">
    <!-- Logo -->
    <!-- wp:generateblocks/element {"uniqueId":"nav002","tagName":"nav","styles":{"display":"flex","gap":"2rem","@media (max-width:768px)":{"display":"none"}},"css":".gb-element-nav002{display:flex;gap:2rem}@media(max-width:768px){.gb-element-nav002{display:none}}","className":"gb-element"} -->
    <nav class="gb-element-nav002 gb-element">
        <!-- Navigation links -->
    </nav>
    <!-- /wp:generateblocks/element -->
    <!-- CTA Button -->
</header>
<!-- /wp:generateblocks/element -->
```

## Color Extraction

### From Figma Dev Mode

If you have access to Figma Dev Mode, extract:
- Color variables/tokens
- Exact hex/rgba values
- Gradient definitions

### From Screenshot

When analyzing a screenshot:
1. Identify primary brand color (usually buttons, links, accents)
2. Identify text colors (dark for body, lighter for secondary)
3. Identify background colors (white, off-white, dark sections)
4. Note any gradients or overlays

### Default Fallbacks

When colors aren't clear, use these sensible defaults:

**Light theme:**
- Primary: `#c0392b` or `#0073e6`
- Text: `#0a0a0a`
- Muted: `#5c5c5c`
- Background: `#ffffff`
- Light background: `#f5f5f3`
- Border: `#e5e5e5`

**Dark theme:**
- Primary: `#e74c3c` or `#3498db`
- Text: `#ffffff`
- Muted: `#a0a0a0`
- Background: `#0a0a0a`
- Card background: `#1a1a1a`
- Border: `#333333`

## Hover States

Figma designs often show only the default state. The plugin generates hover CSS from the `styles` object — **never put hover states or transitions in the `css` attribute**.

The only exception is **parent hover targeting children**, which is written in the child block's `css`:

### Parent Hover Affecting Child (in child's `css`)
```css
.gb-element-card001:hover .gb-shape-icon001{background-color:#c0392b;color:white;transform:scale(1.05) rotate(-3deg)}
.gb-element-card001:hover .gb-text-title001{color:#c0392b}
.gb-element-card001:hover .gb-text-arrow001 svg{transform:translateX(4px)}
```

### Pseudo-Element Hover (in the block's `css`)
```css
.gb-element-card001::after{background:#c0392b;bottom:0;content:'';height:3px;left:0;position:absolute;transform:scaleX(0);transform-origin:left;transition:transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);width:100%}.gb-element-card001:hover::after{transform:scaleX(1)}
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
- `<!-- wp:cover {...} -->` and `<!-- /wp:cover -->`
- Any other `<!-- wp:{namespace}/{block} -->` format

**WRONG - These will break the block editor:**
```html
<!-- Hero Section -->
<!-- Card component -->
<!-- Converted from Figma -->
<!-- Navigation -->
```

**CORRECT - Only block delimiters:**
```html
<!-- wp:generateblocks/element {"uniqueId":"hero001",...} -->
<section class="gb-element gb-element-hero001">
    <!-- wp:generateblocks/text {"uniqueId":"hero002",...} -->
    <h1 class="gb-text gb-text-hero002">Heading</h1>
    <!-- /wp:generateblocks/text -->
</section>
<!-- /wp:generateblocks/element -->
```

Any extra HTML comments will **break the WordPress block editor** and cause parsing errors. This is non-negotiable.

## Other Critical Rules

### 1. htmlAttributes MUST Use Array Format

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

**linkHtmlAttributes** (for media blocks) uses the same array format.

### 2. Both styles AND css Required

Always include both attributes:
```json
{
  "styles": {"padding": "2rem"},
  "css": ".gb-element-id{padding:2rem}"
}
```

- `styles`: camelCase properties. Supports responsive keys like `"@media (max-width:1024px)":{...}`
- `css`: minified, **alphabetically sorted**, base styles only
- The `css` attribute must **NOT** contain hover states or transitions (plugin generates those from `styles`)
- Exceptions that go in `css`: pseudo-elements, media queries, animations, parent hover targeting children

### 3. Minified CSS (Alphabetically Sorted)

```css
.gb-element-id{background:#fff;padding:2rem}
```

### 4. Unique IDs

Format: `{section}{number}{letter}`
- `hero001`, `hero001a`, `hero001b`
- `card023`, `card023a`

### 5. Element Blocks Need className

Add `"className":"gb-element"` to all element block attributes. HTML class order: `gb-element-{id} gb-element`:
```html
<!-- wp:generateblocks/element {"uniqueId":"card001",...,"className":"gb-element"} -->
<div class="gb-element-card001 gb-element">...</div>
<!-- /wp:generateblocks/element -->
```

### 6. Text `<a>` vs Element `<a>` Links

| Block Type | `htmlAttributes` for href | Use Case |
|-----------|--------------------------|----------|
| `generateblocks/text` with `tagName: "a"` | **No** - plugin manages link internally | Plain text buttons/links (no inner blocks) |
| `generateblocks/element` with `tagName: "a"` | **Yes** - `[{"attribute":"href","value":"/url/"}]` | Containers wrapping inner blocks (cards, icon buttons) |

### 7. SVG Icons Use Shape Blocks

Convert Figma icon/vector layers to `generateblocks/shape` (not `generateblocks/element` with raw SVG):
```html
<!-- wp:generateblocks/shape {"uniqueId":"icon001","styles":{"alignItems":"center","backgroundColor":"#f5f5f3","borderRadius":"0.75rem","color":"#c0392b","display":"flex","height":"3rem","justifyContent":"center","width":"3rem","svg":{"fill":"currentColor","height":"1.5rem","width":"1.5rem"}},"css":".gb-shape-icon001{align-items:center;background-color:#f5f5f3;border-radius:0.75rem;color:#c0392b;display:flex;height:3rem;justify-content:center;width:3rem}.gb-shape-icon001 svg{fill:currentColor;height:1.5rem;width:1.5rem}"} -->
<span class="gb-shape gb-shape-icon001"><svg viewBox="0 0 24 24" fill="currentColor"><path d="..."/></svg></span>
<!-- /wp:generateblocks/shape -->
```

### 8. Test Responsive

Always add media queries for:
- Tablet: `@media(max-width:1024px)`
- Mobile: `@media(max-width:768px)`

### 9. Lists Use `core/list` with `.list` Class

Convert Figma list designs to native WordPress list block:
```html
<!-- wp:list {"className":"list"} -->
<ul class="wp-block-list list">...</ul>
<!-- /wp:list -->
```

### 10. Container Width with CSS Variable

Use `--gb-container-width` for inner container width and `align: "full"` on parent section:
```json
{"align": "full", "styles": {"maxWidth": "var(\u002d\u002dgb-container-width)"}}
```

## Image Handling

### Placeholder Images

When Figma shows placeholder images, use:
```json
{
  "htmlAttributes": [
    {"attribute": "src", "value": "https://placehold.co/800x600/f5f5f3/5c5c5c?text=Image"},
    {"attribute": "alt", "value": "Descriptive alt text"},
    {"attribute": "width", "value": "800"},
    {"attribute": "height", "value": "600"},
    {"attribute": "loading", "value": "lazy"}
  ]
}
```

### Aspect Ratios

Common Figma image ratios:
| Ratio | Use Case | CSS |
|-------|----------|-----|
| 16:9 | Hero, video thumbnails | `aspect-ratio:16/9` |
| 4:3 | Blog cards, features | `aspect-ratio:4/3` |
| 1:1 | Avatars, icons | `aspect-ratio:1/1` |
| 3:2 | Product images | `aspect-ratio:3/2` |

## Output Format

When converting, provide:

1. **Complete block code** - Ready to paste into WordPress
2. **Section-by-section** - For complex designs, break into chunks
3. **Mobile considerations** - Note any responsive adjustments made
4. **Image placeholders** - Indicate where user should replace images
5. **Content placeholders** - Mark text that needs customization
