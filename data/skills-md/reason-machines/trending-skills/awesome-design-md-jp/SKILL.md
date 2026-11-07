---
name: awesome-design-md-jp
description: Create accurate Japanese UI DESIGN.md files for AI agents with proper CJK typography, font stacks, line-height, kinsoku shori, and mixed typesetting rules.
triggers:
  - create a DESIGN.md for a Japanese website
  - generate Japanese UI design spec
  - add Japanese typography to DESIGN.md
  - write design spec for Japanese web app
  - CJK font stack for AI agent
  - Japanese line-height and letter-spacing spec
  - kinsoku shori design rules
  - Japanese UI design system markdown
---

# Awesome Design MD JP

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A curated collection of `DESIGN.md` files for Japanese web services, extending the Google Stitch DESIGN.md format with CJK typography, Japanese font stacks, kinsoku shori (禁則処理), and mixed typesetting (混植) rules — enabling AI agents to generate accurate Japanese UI.

---

## What This Project Does

[DESIGN.md](https://stitch.withgoogle.com/docs/design-md/overview/) is a plain-text markdown file AI coding agents read to generate consistent UI. This project extends that format for Japanese services, covering:

- **CJK font-family fallback chains** (和文 → 欧文 → generic)
- **Higher line-height** (1.5–2.0 vs Western 1.4–1.5)
- **Japanese letter-spacing** (`0.04em`–`0.1em` for body text)
- **Kinsoku shori (禁則処理)** — CJK punctuation line-break rules
- **OpenType features** (`palt`, `kern`) for proportional typesetting
- **Mixed typesetting (混植)** — combining Japanese and Latin typefaces

24 reference DESIGN.md files are included: Apple Japan, MUJI, Mercari, SmartHR, freee, note, LINE, Rakuten, Qiita, Zenn, pixiv, and more.

---

## Installation / Setup

Clone or reference the repository directly — no build step required.

```bash
git clone https://github.com/kzhrknt/awesome-design-md-jp.git
cd awesome-design-md-jp
```

Copy the template into your project:

```bash
cp template/DESIGN.md your-project/DESIGN.md
```

Or reference an existing service as a starting point:

```bash
cp design-md/muji/DESIGN.md your-project/DESIGN.md
# then edit for your brand
```

Place `DESIGN.md` at your project root alongside `AGENTS.md`:

```
your-project/
├── AGENTS.md       # how to build
├── DESIGN.md       # how it should look and feel  ← add this
├── src/
└── ...
```

---

## DESIGN.md Template Structure

The template extends the standard Google Stitch 9-section format with Japanese typography subsections.

### Full Template

```markdown
# DESIGN.md

## 1. Overview
Brief description of the product, target users, and overall visual direction.

## 2. Color Palette

| Token           | Value     | Usage            |
|-----------------|-----------|------------------|
| `--color-primary` | `#0066CC` | CTAs, links      |
| `--color-bg`     | `#FFFFFF` | Page background  |
| `--color-text`   | `#1A1A1A` | Body text        |
| `--color-muted`  | `#666666` | Secondary text   |

## 3. Typography

### 3.1 Font Families

**和文（Japanese）**
```css
font-family:
  "Noto Sans JP",       /* Google Fonts — preferred web font */
  "Hiragino Kaku Gothic ProN", /* macOS / iOS */
  "Hiragino Sans",      /* macOS newer */
  "Meiryo",             /* Windows */
  "Yu Gothic",          /* Windows 8.1+ */
  sans-serif;
```

**欧文（Latin / alphanumeric）**
```css
font-family:
  "Inter",              /* preferred web font for Latin */
  -apple-system,
  BlinkMacSystemFont,
  "Segoe UI",
  sans-serif;
```

**混植（Mixed typesetting）**
Use Japanese font as base; Latin glyphs rendered by Inter layered on top via `@font-face` unicode-range.

### 3.2 Type Scale

| Role       | Size     | Weight | Line-height | Letter-spacing |
|------------|----------|--------|-------------|----------------|
| Display    | 2.5rem   | 700    | 1.4         | -0.02em        |
| Heading 1  | 2rem     | 700    | 1.5         | -0.01em        |
| Heading 2  | 1.5rem   | 600    | 1.5         | 0              |
| Body       | 1rem     | 400    | 1.8         | 0.04em         |
| Small      | 0.875rem | 400    | 1.7         | 0.04em         |
| Caption    | 0.75rem  | 400    | 1.6         | 0.06em         |

### 3.3 Japanese Typography Rules

**Line-height:** Use 1.7–2.0 for body text (wider than Western 1.4–1.5).

**Letter-spacing:** Apply `0.04em`–`0.1em` to body Japanese text; headings may use `0` or slightly negative.

**Kinsoku shori (禁則処理):**
```css
word-break: normal;
overflow-wrap: break-word;
line-break: strict;          /* enforce JIS kinsoku rules */
```
- 行頭禁則文字 (cannot start a line): `）」』】、。・：；？！…―`
- 行末禁則文字 (cannot end a line): `（「『【`

**OpenType features:**
```css
font-feature-settings: "palt" 1, "kern" 1;
/* palt = proportional alternate widths for punctuation */
/* kern = kerning */
```

**Text rendering:**
```css
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale;
text-rendering: optimizeLegibility;
```

## 4. Spacing & Layout

Base unit: `8px`

| Token        | Value  |
|--------------|--------|
| `--space-xs` | `4px`  |
| `--space-sm` | `8px`  |
| `--space-md` | `16px` |
| `--space-lg` | `32px` |
| `--space-xl` | `64px` |

Max content width: `1200px` with `24px` horizontal padding on mobile.

## 5. Components
[Describe buttons, inputs, cards, navigation patterns]

## 6. Icons & Imagery
[Icon set, image ratios, illustration style]

## 7. Motion & Animation
[Transition durations, easing curves]

## 8. Responsive Breakpoints

| Name   | Width    |
|--------|----------|
| Mobile | < 768px  |
| Tablet | 768–1024px |
| Desktop| > 1024px |

## 9. Accessibility
- Contrast ratio: minimum 4.5:1 for body text
- Focus indicators: visible outline
- Tap targets: minimum 44×44px
```

---

## Reference DESIGN.md Examples

### MUJI Style (Minimalist Retail)

```markdown
## Color Palette
| Token              | Value     |
|--------------------|-----------|
| `--color-primary`  | `#000000` |
| `--color-bg`       | `#F5F5F0` |
| `--color-text`     | `#333333` |
| `--color-border`   | `#DDDDDD` |

## Typography

### Font Stack
```css
font-family:
  "Noto Serif JP",
  "Hiragino Mincho ProN",
  "Yu Mincho",
  "MS Mincho",
  Georgia,
  serif;
```

### Body
- font-size: 15px
- line-height: 2.0
- letter-spacing: 0.08em
- font-feature-settings: "palt" 1

### Design Principles
- 徹底した余白（generous whitespace as design element）
- 無彩色を基調（achromatic base palette）
- 装飾を排除（eliminate decoration）
```

### SmartHR Style (B2B SaaS)

```markdown
## Color Palette
| Token             | Value     |
|-------------------|-----------|
| `--color-primary` | `#0077C8` |
| `--color-success` | `#28A745` |
| `--color-warning` | `#FFC107` |
| `--color-danger`  | `#DC3545` |
| `--color-bg`      | `#F8F9FA` |
| `--color-text`    | `#212529` |

## Typography

### Font Stack
```css
font-family:
  "Hiragino Kaku Gothic ProN",
  "Hiragino Sans",
  Meiryo,
  "Yu Gothic",
  sans-serif;
```

### Type Scale
- Display: 28px / weight 700 / line-height 1.4 / ls 0
- Body: 14px / weight 400 / line-height 1.8 / ls 0.04em
- Label: 12px / weight 500 / line-height 1.6 / ls 0.06em
- Note: Dense information layout — prioritize readability at small sizes
```

### note Style (Media / Publishing)

```markdown
## Typography

### Font Stack
```css
/* Heading */
font-family: "Noto Serif JP", "Hiragino Mincho ProN", serif;

/* Body */  
font-family: "Noto Sans JP", "Hiragino Kaku Gothic ProN", sans-serif;
```

### Reading Typography
- Body: 18px / line-height 1.9 / letter-spacing 0.04em
- Max line length: 38–40 chars (約38文字で折り返し)
- Paragraph spacing: 1.5em
- Drop cap on first paragraph of long-form content
```

---

## CSS Boilerplate for Japanese UI

Use this as a starting point in any project informed by these DESIGN.md files:

```css
/* ===== Japanese Typography Base ===== */

:root {
  /* Font families */
  --font-ja-sans: "Noto Sans JP", "Hiragino Kaku Gothic ProN",
    "Hiragino Sans", "Meiryo", "Yu Gothic", sans-serif;
  --font-ja-serif: "Noto Serif JP", "Hiragino Mincho ProN",
    "Yu Mincho", "MS Mincho", Georgia, serif;
  --font-en: "Inter", -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;

  /* Type scale */
  --text-display: 2.5rem;
  --text-h1: 2rem;
  --text-h2: 1.5rem;
  --text-h3: 1.25rem;
  --text-body: 1rem;
  --text-sm: 0.875rem;
  --text-xs: 0.75rem;

  /* Line heights */
  --lh-tight: 1.4;   /* headings */
  --lh-normal: 1.8;  /* body */
  --lh-loose: 2.0;   /* long-form reading */

  /* Letter spacing */
  --ls-tight: -0.02em;
  --ls-normal: 0.04em;
  --ls-wide: 0.08em;
}

/* Base Japanese text rendering */
body {
  font-family: var(--font-ja-sans);
  font-size: var(--text-body);
  line-height: var(--lh-normal);
  letter-spacing: var(--ls-normal);
  font-feature-settings: "palt" 1, "kern" 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

/* Kinsoku shori */
p, li, td, th {
  word-break: normal;
  overflow-wrap: break-word;
  line-break: strict;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
  line-height: var(--lh-tight);
  letter-spacing: var(--ls-tight);
  font-feature-settings: "palt" 1;
}

/* Mixed typesetting — Latin numerals and ASCII via Inter */
@font-face {
  font-family: "Inter-for-JP";
  src: url("https://fonts.gstatic.com/s/inter/v13/...") format("woff2");
  unicode-range: U+0020-007E; /* Basic Latin only */
}
```

---

## Font Loading (Google Fonts)

```html
<!-- In <head> — preconnect for performance -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Noto Sans JP (recommended for most Japanese UI) -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">

<!-- Noto Serif JP (for editorial / reading-focused UI) -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap" rel="stylesheet">

<!-- Combined with Inter for mixed typesetting -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
```

---

## Common Patterns by Service Category

### Consumer App (LINE, Mercari)
```markdown
- Font: Noto Sans JP + system fallbacks
- Line-height body: 1.7
- Letter-spacing: 0.04em
- Primary color: brand-specific bold color
- Mobile-first, 375px base
- Tap targets: 48px minimum
```

### B2B SaaS (SmartHR, freee, Cybozu)
```markdown
- Font: Hiragino Kaku Gothic ProN preferred (system), Noto Sans JP web
- Line-height body: 1.8 (dense data tables may use 1.5)
- Letter-spacing: 0.04em
- Neutral palette with clear action color
- Information density: high
- Data tables with sticky headers
```

### Editorial / Media (note, WIRED.jp, Qiita, Zenn)
```markdown
- Font: Noto Serif JP or Hiragino Mincho for body; sans for UI chrome
- Line-height body: 1.9–2.0
- Letter-spacing: 0.06em
- Max line length: 38–42 characters (約40文字)
- Code blocks: monospace with JIS-compatible fallback
```

### Retail / Lifestyle (MUJI, Toyota)
```markdown
- Font: Serif for premium feel; sans for utility text
- Line-height: 2.0 (generous whitespace)
- Letter-spacing: 0.08em (airy)
- Achromatic or very restrained palette
- High-quality imagery as primary content
```

---

## Viewing Previews

Each DESIGN.md has an accompanying `preview.html` that visualizes design tokens:

```bash
# Open any preview locally
open design-md/muji/preview.html
open design-md/smarthr/preview.html

# Or view the full gallery
open design-md/gallery.html
# or visit: https://kzhrknt.github.io/awesome-design-md-jp/gallery.html
```

---

## Telling an AI Agent to Use DESIGN.md

When the file is at your project root, reference it explicitly in your prompt:

```
Read DESIGN.md and create a Japanese landing page hero section following 
the typography and color specifications defined there. Use the exact 
font-family fallback chain, line-height, and letter-spacing values specified.
Implement kinsoku shori with line-break: strict.
```

For Claude Code / Cursor, you can also reference specific sections:

```
Following DESIGN.md section 3.3 (Japanese Typography Rules), update the 
global CSS to add proper kinsoku shori, font-feature-settings, and 
-webkit-font-smoothing for all text elements.
```

---

## Troubleshooting

### AI generates wrong Japanese fonts
**Problem:** Agent uses `"MS Gothic"` or generic `sans-serif` only.  
**Fix:** Make font-family fallback chain explicit in DESIGN.md with comments explaining each fallback's platform target.

```markdown
### Font Stack (REQUIRED — do not simplify)
```css
font-family:
  "Noto Sans JP",              /* web font — always load via Google Fonts */
  "Hiragino Kaku Gothic ProN", /* macOS / iOS system */
  "Hiragino Sans",             /* macOS 10.11+ */
  "Meiryo",                    /* Windows */
  "Yu Gothic",                 /* Windows 8.1+ */
  sans-serif;                  /* absolute fallback */
```
```

### Line-height too tight on Japanese text
**Problem:** Agent uses `line-height: 1.5` from a Western design system.  
**Fix:** Specify explicitly in DESIGN.md with a note:

```markdown
**IMPORTANT:** Japanese body text requires line-height 1.7–2.0, 
NOT the Western default of 1.4–1.5. Use 1.8 for standard body copy.
```

### Punctuation appearing at line start/end incorrectly
**Problem:** `。` or `、` wraps to start of next line; `「` hangs at end.  
**Fix:** Add kinsoku rules explicitly:

```markdown
### Kinsoku Shori (禁則処理) — REQUIRED
```css
p { line-break: strict; word-break: normal; overflow-wrap: break-word; }
```
Characters that MUST NOT start a line: ）」』】、。・：；？！…―
Characters that MUST NOT end a line: （「『【
```

### Proportional punctuation not activating
**Problem:** Japanese commas and periods render full-width, looking too spaced.  
**Fix:** Ensure font-feature-settings is applied:

```markdown
font-feature-settings: "palt" 1, "kern" 1;
/* palt = proportional alternates — narrows full-width punctuation */
/* Required for Noto Sans JP, Hiragino fonts */
```

### Mixed Japanese/Latin spacing looks wrong
**Problem:** Latin letters inside Japanese text have no breathing room.  
**Fix:** Document the spacing rule in DESIGN.md:

```markdown
### Mixed Typesetting (混植)
- Insert a thin space (U+202F or 0.25em margin) between Japanese and Latin runs
- OR use CSS: `ruby { margin: 0 0.1em; }` pattern
- Preferred: use a font that handles this (Noto CJK with auto-spacing)
```

---

## Contributing a New DESIGN.md

```bash
# 1. Create directory
mkdir design-md/your-service

# 2. Copy template
cp template/DESIGN.md design-md/your-service/DESIGN.md

# 3. Fill in all 9 sections including Japanese typography subsections
# 4. Create preview.html from the preview template
cp template/preview.html design-md/your-service/preview.html

# 5. Take a screenshot at 1280×800 → preview-screenshot.png
```

Required sections for acceptance:
- ✅ Color palette with CSS custom property names
- ✅ Japanese font-family fallback chain with platform comments
- ✅ Type scale table with line-height AND letter-spacing columns
- ✅ Kinsoku shori CSS rules
- ✅ font-feature-settings specification
- ✅ Responsive breakpoints
