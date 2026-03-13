---
name: og-image-design
description: Design and generate Open Graph (OG) images for social media sharing. Use this skill whenever the user mentions OG images, social sharing images, social cards, Twitter cards, link preview images, meta images, og:image, social thumbnails, or wants to create images that appear when links are shared on Facebook, Twitter/X, LinkedIn, Discord, Slack, iMessage, or any social platform. Also use when the user asks about og:image meta tags, social preview optimization, or link unfurling visuals.
---

# OG Image Design

Design effective Open Graph images that make links stand out when shared across social platforms. This skill covers dimensions, layout, typography, color, brand tokens, HTML/CSS templates, and meta tag integration — independent of any specific image generation tool.

## Brand Token System

Before generating any OG image, establish (or locate) the project's brand tokens. If none exist, define them. Every template in this skill references these tokens — never hardcode raw color values or font sizes directly in templates.

### Token Structure

```
Brand Tokens (raw values)
  └── Semantic Tokens (purpose-driven aliases)
      └── Template Tokens (OG-image-specific bindings)
```

### Defining Brand Tokens

Store tokens as a flat object (JSON, TypeScript const, or CSS custom properties) at the project level. The agent should look for existing tokens in the codebase first (CSS variables, Tailwind theme, design-system config), then map them into the OG token format below.

```typescript
const ogBrand = {
  // ─── Colors ────────────────────────────────────────────
  color: {
    // Primitives — raw brand palette
    ink: "#0a0a0b",
    paper: "#fafaf9",
    brand: "#6d5cff",
    brandLight: "#a18aff",
    accent: "#00d4aa",
    muted: "rgba(255,255,255,0.6)",
    danger: "#ef4444",
    surface: "rgba(255,255,255,0.08)",
    border: "rgba(255,255,255,0.12)",

    // Semantic — what the color does
    bg: "#0a0a0b",
    bgGradientFrom: "#0f0a1a",
    bgGradientTo: "#1a0f2e",
    text: "#fafaf9",
    textSecondary: "rgba(255,255,255,0.7)",
    textTertiary: "rgba(255,255,255,0.45)",
    badgeBg: "#6d5cff",
    badgeText: "#ffffff",
  },

  // ─── Typography ────────────────────────────────────────
  type: {
    fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
    // Scale follows a modular ratio (1.25 — Major Third)
    title: { size: 56, weight: 800, lineHeight: 1.15, letterSpacing: "-0.02em" },
    subtitle: { size: 24, weight: 400, lineHeight: 1.4, letterSpacing: "0" },
    label: { size: 16, weight: 700, lineHeight: 1, letterSpacing: "0.08em", textTransform: "uppercase" },
    meta: { size: 18, weight: 500, lineHeight: 1, letterSpacing: "0" },
  },

  // ─── Spacing ───────────────────────────────────────────
  space: {
    pad: 60,           // outer padding (minimum 40, prefer 60)
    gapStack: 16,      // vertical gap between text elements
    gapInline: 12,     // horizontal gap (e.g. badge icon + text)
    badgePadX: 16,
    badgePadY: 8,
  },

  // ─── Radii ─────────────────────────────────────────────
  radius: {
    badge: 6,
    logo: 16,
    card: 24,
  },

  // ─── Dimensions ────────────────────────────────────────
  canvas: {
    width: 1200,
    height: 630,
  },
} as const;
```

### Using Tokens in Templates

Every inline style in a template should reference token paths, not raw values:

```tsx
// ✅ Good — references brand tokens
<div style={{
  fontSize: ogBrand.type.title.size,
  fontWeight: ogBrand.type.title.weight,
  color: ogBrand.color.text,
  lineHeight: ogBrand.type.title.lineHeight,
}}>

// ❌ Bad — hardcoded values
<div style={{ fontSize: 52, fontWeight: 800, color: "white" }}>
```

### Adapting Tokens to an Existing Brand

When the user already has a brand/design system:

1. **Scan codebase** for CSS variables (`--color-*`, `--font-*`), Tailwind `@theme` blocks, or design-token files.
2. **Map existing values** into the `ogBrand` structure above.
3. **Fill gaps** — OG images need specific sizes (48–64 px titles) that may not exist in a web design system. Derive them from the brand's type scale.
4. **Verify contrast** — check that `color.text` over `color.bg` passes WCAG AA (4.5:1 minimum). OG images must be legible at small preview sizes.

### Category Theming

For content-rich sites (blogs, docs, courses), extend the token set with per-category overrides:

```typescript
const categories = {
  engineering: { badgeBg: "#3b82f6", badgeText: "#fff", gradientFrom: "#0c1929", gradientTo: "#162744" },
  design:     { badgeBg: "#ec4899", badgeText: "#fff", gradientFrom: "#1a0a14", gradientTo: "#2e1225" },
  product:    { badgeBg: "#22c55e", badgeText: "#000", gradientFrom: "#0a1a0f", gradientTo: "#0f2e18" },
  tutorial:   { badgeBg: "#f59e0b", badgeText: "#000", gradientFrom: "#1a150a", gradientTo: "#2e2510" },
} as const;
```

The agent merges a category override into the base `ogBrand.color` before rendering, keeping typography and layout identical across all categories.

## Generation Approach

OG images are typically generated from HTML/CSS rendered to a static image. Choose whichever method fits the project:

| Method | When to use |
|---|---|
| **Next.js `ImageResponse`** (Satori + `@vercel/og`) | Next.js apps — generates at the edge, no browser needed |
| **Puppeteer / Playwright screenshot** | Any Node.js project — full browser rendering fidelity |
| **Satori standalone** | Lightweight JSX-to-SVG-to-PNG without a browser |
| **HTML-to-image CLI/API** | CI pipelines, serverless, or any language |
| **Static design tool export** | One-off images, manual workflow |
| **AI image generation** | Photographic or illustrative visuals without text layout concerns |

Regardless of method, the HTML/CSS templates and design rules below apply universally.

## Satori CSS Compatibility

Most OG image pipelines use Satori (the engine behind `@vercel/og` and `next/og`). Satori supports a **subset** of CSS. Knowing what works and what breaks prevents debugging sessions.

### Supported (safe to use)

| Category | Properties |
|---|---|
| **Layout** | `display` (flex, none), `position` (relative, absolute), `top/right/bottom/left`, `overflow` |
| **Flexbox** | `flexDirection`, `flexWrap`, `flexBasis`, `flexGrow`, `flexShrink`, `justifyContent`, `alignItems`, `alignContent`, `alignSelf`, `gap` |
| **Sizing** | `width`, `height`, `minWidth`, `minHeight`, `maxWidth`, `maxHeight` |
| **Spacing** | `margin*`, `padding*` |
| **Typography** | `fontFamily`, `fontSize`, `fontWeight`, `fontStyle`, `lineHeight`, `letterSpacing`, `textAlign`, `textDecoration`, `textTransform`, `textOverflow`, `textShadow`, `wordBreak`, `whiteSpace`, `textWrap`, `lineClamp` |
| **Color & BG** | `color`, `backgroundColor`, `backgroundImage` (linear-gradient, radial-gradient, url), `backgroundSize`, `backgroundPosition`, `backgroundRepeat`, `backgroundClip`, `opacity` |
| **Border** | `border*`, `borderRadius`, `borderColor`, `borderStyle` (solid, dashed) |
| **Effects** | `boxShadow`, `filter`, `transform` (2D only), `transformOrigin`, `clipPath`, `mask*` |

### Not supported (will break or be ignored)

| Feature | Workaround |
|---|---|
| `display: grid` | Use nested `display: flex` with `flexDirection` |
| `calc()` | Pre-compute values or use fixed sizes |
| `z-index` | Layer with DOM order and `position: absolute` |
| 3D transforms | Use 2D `transform` only |
| `@media` queries | Not needed — OG images are fixed 1200×630 |
| CSS variables (`var()`) | Inline the resolved value |
| `animation`, `transition` | Static image — no motion |
| Advanced typography (kerning, ligatures, OpenType) | Not available |
| `display: inline`, `display: block` | Use `display: flex` for everything |

**Critical rule:** Every element in Satori must use `display: flex` (this is the default). Satori does not support block or inline layout.

## Font Loading

### Satori / `@vercel/og`

Satori requires font data as an `ArrayBuffer`. Load fonts at the module level to avoid re-fetching on each request:

```typescript
// Load once at module scope
const interBold = fetch(
  new URL("./fonts/Inter-Bold.ttf", import.meta.url)
).then((res) => res.arrayBuffer());

const interRegular = fetch(
  new URL("./fonts/Inter-Regular.ttf", import.meta.url)
).then((res) => res.arrayBuffer());

export default async function OGImage() {
  return new ImageResponse(
    (<div>...</div>),
    {
      ...ogBrand.canvas,
      fonts: [
        { name: "Inter", data: await interBold, weight: 800, style: "normal" },
        { name: "Inter", data: await interRegular, weight: 400, style: "normal" },
      ],
    }
  );
}
```

Load **only** the weights referenced in your brand tokens. Each font adds ~100–400 KB to the response.

### Google Fonts (remote)

```typescript
const font = fetch(
  "https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap"
).then((r) => r.text())
 .then((css) => {
   const url = css.match(/src: url\((.+?)\)/)?.[1];
   return url ? fetch(url).then((r) => r.arrayBuffer()) : null;
 });
```

### Puppeteer / Playwright

No special loading needed — install fonts on the system or use `@font-face` in the HTML. Full browser rendering gives access to all CSS features and font features.

## Platform Specifications

| Platform | Dimensions | Aspect Ratio | Max Size | Formats |
|---|---|---|---|---|
| Facebook | 1200 × 630 px | 1.91:1 | 8 MB | JPG, PNG |
| Twitter/X (`summary_large_image`) | 1200 × 628 px | 1.91:1 | 5 MB | JPG, PNG, WEBP, GIF |
| Twitter/X (`summary`) | 800 × 418 px | 1.91:1 | 5 MB | JPG, PNG |
| LinkedIn | 1200 × 627 px | 1.91:1 | 5 MB | JPG, PNG |
| Discord | 1200 × 630 px | 1.91:1 | 8 MB | JPG, PNG |
| Slack | 1200 × 630 px | 1.91:1 | — | JPG, PNG |
| iMessage | 1200 × 630 px | 1.91:1 | — | JPG, PNG |

**Universal target: 1200 × 630 px, PNG or JPG, under 1 MB (under 5 MB absolute max).**

## Template Selection

When the agent needs to generate an OG image, use this decision tree:

```
Is it a product launch or announcement?
  → Product / Launch template (centered layout)

Is it a blog post or article?
  → Blog Post template (left-aligned, category badge)

Is it a tutorial or how-to guide?
  → Tutorial template (badge + step indicator)

Is it API docs or technical reference?
  → Documentation template (icon block + version)

Does the brand require a prominent logo?
  → Branded with Logo template (text left, logo right)

None of the above?
  → Blog Post template (most versatile default)
```

## The Golden Layout

```
┌──────────────────────────────────────────────────┐
│                                                  │
│  ┌─────────────────────────────────┐  ┌───────┐  │
│  │                                 │  │       │  │
│  │  Title (max 60 chars)           │  │ Logo/ │  │
│  │  ───────────────────            │  │ Visual│  │
│  │  Subtitle (max 100 chars)       │  │       │  │
│  │                                 │  │       │  │
│  │  author · site name             │  └───────┘  │
│  └─────────────────────────────────┘             │
│                                                  │
└──────────────────────────────────────────────────┘
  1200 × 630 px
```

This is the most reliable pattern: text-heavy left side, visual accent right side. Centered single-column layouts also work well for announcements and product launches.

## Design Rules

### Typography Scale

The brand token `type` object defines the scale. Within those bounds:

| Role | Size Range | Weight | Usage |
|---|---|---|---|
| Title | 48–64 px | 700–900 | Main headline. Scale down for long titles. |
| Subtitle | 20–28 px | 400 | Supporting text, description. |
| Label | 14–18 px | 600–700 | Category badge, tag, uppercase accent. |
| Meta | 16–20 px | 400–500 | Author, date, site name, version. |

**Dynamic sizing rule:** If the title exceeds 40 characters, reduce to 48 px. If it exceeds 25 characters at 64 px, reduce to 56 px. Never go below 44 px — truncate with ellipsis instead.

```typescript
function getTitleSize(title: string): number {
  const len = title.length;
  if (len <= 25) return 64;
  if (len <= 40) return 56;
  if (len <= 55) return 48;
  return 44;
}
```

### Safe Zones

```
┌──────────────────────────────────────────────────┐
│  ┌──────────────────────────────────────────────┐│
│  │  40–60 px padding from all edges             ││
│  │                                              ││
│  │  Content lives here                          ││
│  │                                              ││
│  └──────────────────────────────────────────────┘│
└──────────────────────────────────────────────────┘
```

- 40 px minimum padding from all edges (60 px preferred).
- Some platforms crop edges or add rounded corners.
- Never place critical text in the outer 5%.

### Color & Background

| Background type | When to use |
|---|---|
| Solid brand color | Consistent series, corporate identity |
| Gradient | Modern feel, eye-catching |
| Photo with dark overlay | Blog posts, editorial content |
| Dark background | Better contrast, stands out in feeds |

Dark backgrounds outperform light ones in social feeds — most feeds have a light background, so dark OG images create contrast and draw the eye.

### Background Pattern Library

These patterns work in Satori and add visual depth without external images.

**Diagonal gradient (default):**
```css
background: linear-gradient(135deg, var(--bg-from), var(--bg-to));
```

**Radial spotlight:**
```css
background: radial-gradient(ellipse 80% 60% at 30% 50%, rgba(109,92,255,0.25), transparent), linear-gradient(135deg, #0f0a1a, #1a0f2e);
```

**Dual radial glow:**
```css
background: radial-gradient(circle at 20% 40%, rgba(109,92,255,0.3), transparent 50%), radial-gradient(circle at 80% 60%, rgba(0,212,170,0.2), transparent 50%), #0a0a0b;
```

**Mesh gradient (3-point):**
```css
background: radial-gradient(at 0% 0%, rgba(109,92,255,0.4) 0%, transparent 50%), radial-gradient(at 100% 0%, rgba(0,212,170,0.3) 0%, transparent 50%), radial-gradient(at 50% 100%, rgba(239,68,68,0.2) 0%, transparent 50%), #0a0a0b;
```

**Subtle noise (via SVG data URI — works in Satori):**
```tsx
<div style={{
  position: "absolute", top: 0, left: 0, width: "100%", height: "100%",
  backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`,
  opacity: 0.04,
}} />
```

> **Note:** SVG filter noise may not render in all Satori versions. Test first; fall back to a solid or gradient background.

## HTML/CSS Templates

All templates use `display: flex` for Satori compatibility. The outer `div` is always exactly 1200 × 630 px. Templates reference brand token values — replace the literal values with your project's tokens.

### Blog Post

```html
<div style="width:1200px;height:630px;background:linear-gradient(135deg,#0f0a1a,#1a0f2e);display:flex;align-items:center;padding:60px;font-family:'Inter',system-ui,sans-serif;color:#fafaf9">
  <div style="display:flex;flex-direction:column;flex:1">
    <div style="display:flex;align-items:center;margin-bottom:20px">
      <span style="font-size:16px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;background:#6d5cff;color:#fff;padding:8px 16px;border-radius:6px">Engineering</span>
    </div>
    <h1 style="font-size:56px;margin:0;line-height:1.15;font-weight:800;letter-spacing:-0.02em">How We Reduced Build Times by 80%</h1>
    <p style="font-size:24px;color:rgba(255,255,255,0.7);margin:16px 0 0;line-height:1.4">A deep dive into CI/CD optimization</p>
    <p style="font-size:18px;color:rgba(255,255,255,0.45);margin-top:24px">yoursite.com</p>
  </div>
</div>
```

### Product / Launch Announcement

```html
<div style="width:1200px;height:630px;background:radial-gradient(ellipse 80% 60% at 50% 40%,rgba(109,92,255,0.3),transparent),#0a0a0b;display:flex;align-items:center;justify-content:center;font-family:'Inter',system-ui,sans-serif;color:#fafaf9;text-align:center">
  <div style="display:flex;flex-direction:column;align-items:center">
    <p style="font-size:16px;color:#00d4aa;text-transform:uppercase;letter-spacing:0.12em;font-weight:700;margin:0">Now Available</p>
    <h1 style="font-size:64px;margin:12px 0;font-weight:900;letter-spacing:-0.02em">ProductName 2.0</h1>
    <p style="font-size:24px;color:rgba(255,255,255,0.6);margin:0">Tagline goes here. Zero configuration.</p>
  </div>
</div>
```

### Tutorial / How-To

```html
<div style="width:1200px;height:630px;background:linear-gradient(135deg,#0c1929,#162744);display:flex;align-items:center;padding:60px;font-family:'Inter',system-ui,sans-serif;color:#fafaf9">
  <div style="display:flex;flex-direction:column">
    <div style="display:flex;align-items:center;margin-bottom:16px">
      <span style="background:#f59e0b;color:#000;padding:8px 16px;border-radius:6px;font-size:16px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase">Tutorial</span>
    </div>
    <h1 style="font-size:48px;margin:0;line-height:1.15;font-weight:800;letter-spacing:-0.02em">Build a REST API in 10 Minutes with Node.js</h1>
    <p style="font-size:22px;color:rgba(255,255,255,0.65);margin-top:16px">Step-by-step guide with code examples</p>
  </div>
</div>
```

### Documentation / Technical

```html
<div style="width:1200px;height:630px;background:linear-gradient(135deg,#0c0c0c,#1c1c1c);display:flex;align-items:center;padding:60px;font-family:'Inter',system-ui,sans-serif;color:#fafaf9">
  <div style="display:flex;flex-direction:column;flex:1">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:24px">
      <div style="width:48px;height:48px;background:#3b82f6;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:900">D</div>
      <span style="font-size:20px;font-weight:600;color:rgba(255,255,255,0.7)">Docs</span>
    </div>
    <h1 style="font-size:52px;margin:0;line-height:1.15;font-weight:800;letter-spacing:-0.02em">Authentication API Reference</h1>
    <p style="font-size:22px;color:rgba(255,255,255,0.45);margin-top:16px">v2.0 — Updated March 2026</p>
  </div>
</div>
```

### Branded with Logo (right side)

```html
<div style="width:1200px;height:630px;background:linear-gradient(135deg,#0f172a,#1e293b);display:flex;align-items:center;padding:60px;font-family:'Inter',system-ui,sans-serif;color:#fafaf9">
  <div style="flex:1;display:flex;flex-direction:column;padding-right:40px">
    <h1 style="font-size:52px;margin:0;line-height:1.15;font-weight:800;letter-spacing:-0.02em">Your Title Goes Here</h1>
    <p style="font-size:22px;color:rgba(255,255,255,0.7);margin-top:16px">Supporting description text</p>
    <p style="font-size:18px;color:rgba(255,255,255,0.4);margin-top:24px">yoursite.com</p>
  </div>
  <div style="width:200px;height:200px;background:rgba(255,255,255,0.08);border-radius:24px;display:flex;align-items:center;justify-content:center;flex-shrink:0">
    <span style="font-size:64px;font-weight:900">☐</span>
  </div>
</div>
```

Replace the placeholder square with an `<img>` tag pointing to the actual logo when the renderer supports it.

## Adapting Templates

When customizing these templates:

1. **Replace placeholder text** with actual title, subtitle, and branding.
2. **Swap gradient colors** to match `ogBrand.color.bgGradientFrom` and `bgGradientTo`.
3. **Apply dynamic title sizing** using the `getTitleSize()` function. Longer titles need smaller sizes.
4. **Match badge color** to the content category using the category theming map.
5. **Truncate long text** rather than shrinking the font below minimum sizes. An ellipsis at 60 chars is better than 36 px text.
6. **Verify all `display: flex`** — if targeting Satori, every container element must be a flex container.

## Next.js Integration (with Brand Tokens)

```tsx
// lib/og-brand.ts — export tokens for use in OG routes
export const ogBrand = { /* ...token object from above... */ };

// app/blog/[slug]/opengraph-image.tsx
import { ImageResponse } from "next/og";
import { ogBrand } from "@/lib/og-brand";

export const runtime = "edge";
export const alt = "Blog post";
export const size = ogBrand.canvas;
export const contentType = "image/png";

export default async function Image({ params }: { params: { slug: string } }) {
  const [interBold, interRegular] = await Promise.all([
    fetch(new URL("../../../fonts/Inter-Bold.ttf", import.meta.url)).then((r) => r.arrayBuffer()),
    fetch(new URL("../../../fonts/Inter-Regular.ttf", import.meta.url)).then((r) => r.arrayBuffer()),
  ]);

  const { color, type, space } = ogBrand;

  return new ImageResponse(
    (
      <div style={{
        width: "100%", height: "100%", display: "flex", alignItems: "center",
        padding: space.pad,
        background: `linear-gradient(135deg, ${color.bgGradientFrom}, ${color.bgGradientTo})`,
        fontFamily: type.fontFamily, color: color.text,
      }}>
        <div style={{ display: "flex", flexDirection: "column", flex: 1 }}>
          <span style={{
            fontSize: type.label.size, fontWeight: type.label.weight,
            letterSpacing: type.label.letterSpacing, textTransform: type.label.textTransform,
            background: color.badgeBg, color: color.badgeText,
            padding: `${space.badgePadY}px ${space.badgePadX}px`,
            borderRadius: ogBrand.radius.badge,
          }}>
            Category
          </span>
          <span style={{
            fontSize: type.title.size, fontWeight: type.title.weight,
            lineHeight: type.title.lineHeight, letterSpacing: type.title.letterSpacing,
            marginTop: space.gapStack,
          }}>
            Post Title Here
          </span>
          <span style={{
            fontSize: type.subtitle.size, fontWeight: type.subtitle.weight,
            color: color.textSecondary, marginTop: space.gapStack,
            lineHeight: type.subtitle.lineHeight,
          }}>
            Subtitle or description
          </span>
        </div>
      </div>
    ),
    {
      ...size,
      fonts: [
        { name: "Inter", data: interBold, weight: 800, style: "normal" },
        { name: "Inter", data: interRegular, weight: 400, style: "normal" },
      ],
    }
  );
}
```

## OG Meta Tags Reference

```html
<!-- Essential (Facebook, LinkedIn, Discord, Slack, iMessage) -->
<meta property="og:title" content="Title here (60 chars max)" />
<meta property="og:description" content="Description (155 chars max)" />
<meta property="og:image" content="https://yoursite.com/og-image.png" />
<meta property="og:url" content="https://yoursite.com/page" />
<meta property="og:type" content="article" />

<!-- Recommended dimensions hint -->
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />

<!-- Twitter/X specific -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Title here" />
<meta name="twitter:description" content="Description" />
<meta name="twitter:image" content="https://yoursite.com/og-image.png" />
```

### Twitter Card Types

| Card type | Image size | Use when |
|---|---|---|
| `summary` | 800 × 418 (small thumbnail) | Short updates, links |
| `summary_large_image` | 1200 × 628 (full width) | Blog posts, articles, announcements |

Always prefer `summary_large_image` — the large image gets significantly more engagement.

## Testing & Debugging

Validate OG images after deployment with these tools:

| Tool | URL |
|---|---|
| Facebook Sharing Debugger | `developers.facebook.com/tools/debug/` |
| Twitter/X Card Validator | `cards-dev.twitter.com/validator` |
| LinkedIn Post Inspector | `linkedin.com/post-inspector/` |
| OpenGraph.xyz | `opengraph.xyz` |

## Quality Checklist

Before delivering an OG image, verify every item:

- [ ] **Canvas is 1200 × 630 px** — exact dimensions, no rounding
- [ ] **File size under 1 MB** — under 5 MB absolute max
- [ ] **Title is ≤ 60 characters** — truncated with ellipsis if longer
- [ ] **Title font ≥ 44 px** — never smaller, even for long titles
- [ ] **Safe zone padding ≥ 40 px** — 60 px preferred on all sides
- [ ] **Text contrast ≥ 4.5:1** — WCAG AA against background
- [ ] **Brand tokens used** — no hardcoded colors or font sizes outside the token system
- [ ] **Category badge matches** — correct color for the content category
- [ ] **Font loaded** — custom font data provided to Satori or installed for Puppeteer
- [ ] **All elements use `display: flex`** — if targeting Satori
- [ ] **No unsupported CSS** — no `calc()`, `z-index`, grid, CSS variables in Satori
- [ ] **Image serves over HTTPS** — absolute URL with protocol
- [ ] **`og:image:width` and `og:image:height` meta tags set** — for fast unfurling
- [ ] **Tested on at least one validator** — Facebook Debugger or OpenGraph.xyz

## Common Mistakes

| Mistake | Problem | Fix |
|---|---|---|
| No `og:image` at all | Platform shows random page element or blank | Always set `og:image` |
| Text too small | Unreadable on mobile previews | Title minimum 48 px at 1200 px width |
| Light background | Gets lost in white/light feeds | Use dark or saturated backgrounds |
| Too much text | Cluttered, overwhelming | Stick to title + subtitle + brand |
| Image too large (> 5 MB) | Some platforms won't load it | Optimize to under 1 MB ideally |
| No safe zone padding | Text gets cropped on some platforms | 40–60 px padding from all edges |
| HTTP image URL | Many platforms require HTTPS | Always serve OG images over HTTPS |
| Relative image path | Won't resolve when shared externally | Use full absolute URL with protocol |
| Missing `og:image:width` / `height` | Slower unfurling on some platforms | Always include dimension hints |
| Caching stale image | Updated image not reflected | Append version query param or use Facebook debugger to scrape again |
| Hardcoded colors per template | Brand drift across pages | Use the brand token system |
| Different fonts per page | Inconsistent visual identity | Lock `fontFamily` in brand tokens |
| No dynamic title sizing | Long titles overflow or become unreadable | Use `getTitleSize()` function |
