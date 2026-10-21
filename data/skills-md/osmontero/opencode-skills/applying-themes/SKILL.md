---
name: applying-themes
description: Use when a visual artifact needs a consistent color and type system applied — slide decks, reports, HTML pages, dashboards, PDFs, docs — or when asked to "theme this", "restyle with a palette", "make these slides look consistent", "pick colors and fonts", or to build a custom theme from a brand or a description. Provides 10 contrast-verified themes with semantic tokens and a checker script.
license: Complete terms in LICENSE.txt
---

# Applying Themes

## Overview

A theme is a **complete set of semantic tokens**, not a list of nice colors. Four hex values with no defined roles produce inconsistent output, because every component has to decide for itself which one is text and which one is background.

**Core principle:** Every theme resolves to the same eight tokens. Components reference token names, never hex values. Swapping the theme then means swapping one block.

```
base  surface  line  ink  ink-2  ink-3  accent  accent-ink
```

## The Iron Law

```
NO THEME APPLIED WITHOUT ITS CONTRAST VERIFIED
```

A palette that looks good and fails 4.5:1 is unusable, and contrast is not eyeballable — mid-tone accents on mid-tone surfaces fail constantly while looking fine. Every bundled theme ships with a machine-checkable `contrast` block. Custom themes get the same treatment before use.

## Checklist

1. **Present the themes** — the table below, with what each is for
2. **Get an explicit choice** — do not assume one
3. **Read the theme file** — `themes/<name>.md` is the source of truth
4. **Verify contrast** — run the checker; for a custom theme this is mandatory
5. **Emit the token block** — once, at the top of the artifact
6. **Apply by token name** — no raw hex anywhere in components
7. **Check the render** — look at the output, especially secondary text

## The Themes

| Theme | Character | Base | Best for |
|---|---|---|---|
| `ocean-depths` | Deep maritime calm | Dark | Financial, consulting, infrastructure |
| `sunset-boulevard` | Golden-hour warmth | Light | Creative, launches, hospitality |
| `forest-canopy` | Grounded earth tones | Light | Sustainability, craft, long-form |
| `modern-minimalist` | Grayscale discipline | Light | Docs, portfolios, systems |
| `golden-hour` | Amber richness | Light | Reviews, food, retrospectives |
| `arctic-frost` | Cold clinical clarity | Light | Medical, analytics, compliance |
| `desert-rose` | Dusty sophistication | Light | Boutique, invitations, wellness |
| `tech-innovation` | Terminal high-contrast | Dark | Dev tools, AI, changelogs, status |
| `botanical-garden` | Cultivated and alive | Light | Food, agriculture, community |
| `midnight-galaxy` | Deep-space drama | Dark | Launches, entertainment, keynotes |

Each `themes/<name>.md` carries the full palette with roles, the contrast requirements, a web font pairing plus a metric-safe PDF fallback, the scale ratio, and notes on how the theme fails if misused.

> `theme-showcase.pdf` is a legacy visual from an earlier version of this skill and its colors and fonts **no longer match the theme files**. The markdown files are authoritative. Do not present the PDF as an accurate preview.

## Presenting and Choosing

Show the table, ask once, and wait. Do not apply a theme without an explicit choice — restyling an entire deck to the wrong palette wastes more time than the question costs.

If the user describes a need rather than naming a theme ("something serious for a board deck"), recommend two with one-line reasoning and let them pick.

## Verifying Contrast

```bash
source ~/.local/opencode-venv/bin/activate

python3 scripts/check_contrast.py themes/ocean-depths.md   # one theme
python3 scripts/check_contrast.py themes/*.md              # all of them
python3 scripts/check_contrast.py --pair "#8a7357" "#fbf5ea"   # ad-hoc pair
```

Exit code is non-zero on any failure, so it works as a gate. All ten bundled themes pass all six checks.

## Applying

### HTML / CSS

Emit the token block once in `:root`, then reference tokens only.

```css
:root {
  --base: #0f1c26; --surface: #16283a; --line: #2d4859;
  --ink: #eef6f8; --ink-2: #accad4; --ink-3: #8aa7b3;
  --accent: #4fd1c5; --accent-ink: #04222a;
  --font-display: "Young Serif", Georgia, serif;
  --font-text: "IBM Plex Sans", system-ui, sans-serif;
}
body   { background: var(--base); color: var(--ink); font-family: var(--font-text); }
h1, h2 { font-family: var(--font-display); }
.card  { background: var(--surface); border: 1px solid var(--line); }
.meta  { color: var(--ink-3); }
.btn   { background: var(--accent); color: var(--accent-ink); }
```

**No raw hex outside `:root`.** Grep for `#` in your component styles before finishing — a stray hex is how themes stop being swappable.

### Both Color Schemes

If the artifact must work in light and dark, pick a light theme and a dark theme and map them to the same token names:

```css
:root { /* forest-canopy tokens */ }
@media (prefers-color-scheme: dark) { :root { /* ocean-depths tokens */ } }
:root[data-theme="dark"]  { /* ocean-depths tokens */ }
:root[data-theme="light"] { /* forest-canopy tokens */ }
```

Both the media query and the explicit attribute — a toggle that cannot override the OS preference in both directions is broken.

### PDF and Slides

Use the **PDF / slides** column from the theme's typography table. Web fonts are frequently unavailable to PDF renderers, and a missing font silently substitutes something with different metrics, which breaks every layout that assumed the original.

```python
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE, SURFACE, LINE = HexColor("#f7f6f0"), HexColor("#fffffb"), HexColor("#dcded1")
INK, INK2, INK3     = HexColor("#1a271a"), HexColor("#4a5a46"), HexColor("#79876f")
ACCENT, ACCENT_INK  = HexColor("#2f6b3c"), HexColor("#f4fbf5")

# Bundled open-licensed faces from the designing-canvas-art skill
pdfmetrics.registerFont(TTFont("Display", "../designing-canvas-art/canvas-fonts/YoungSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Text",    "../designing-canvas-art/canvas-fonts/WorkSans-Regular.ttf"))
```

`ink-3` is the token most likely to fail in print — many printers and projectors compress the light end. For slides projected in a lit room, use `ink-2` for anything the audience must read.

### React

```jsx
export const theme = {
  base: "#0f1c26", surface: "#16283a", line: "#2d4859",
  ink: "#eef6f8", ink2: "#accad4", ink3: "#8aa7b3",
  accent: "#4fd1c5", accentInk: "#04222a",
};
```

For Tailwind, map the tokens into `theme.extend.colors` so the utility classes carry the semantics: `bg-base`, `text-ink-2`, `border-line`.

## Building a Custom Theme

When no bundled theme fits, construct one rather than picking colors ad hoc.

1. **Name the direction** in two words and name a real-world reference. "Coastal Survey — 1970s nautical chart" produces a palette; "modern and clean" produces defaults.
2. **Choose a hue strategy** — monochromatic, analogous, complementary, or neutral-plus-spot. Commit to one.
3. **Build the neutrals by tinting**, never pure gray. Mix 4-8% of the accent into every neutral so the palette reads as one family.
4. **Derive `ink` from the accent's hue** at very low chroma and very low lightness — this is what makes a palette feel designed rather than assembled.
5. **Set the accent two ways** if needed: a bright value for fills, a darker value for text. One value rarely serves both.
6. **Write the file** in `themes/` using an existing one as the template, including the `contrast` block.
7. **Run the checker.** Adjust lightness until it passes. Do not ship a failing custom theme.
8. **Show the user** the palette and one rendered sample before applying it to the whole artifact.

For the underlying color theory — OKLCH construction, ramp generation, dark-mode rules — see `designing-frontend-interfaces/references/color-and-theme.md`.

## Common Mistakes

**Applying a theme without asking.** Restyling a finished deck to a palette the user did not choose is worse than not theming it.

**Raw hex in components.** The `:root` block exists, and `Card.css` still says `#16283a`. The theme is now unswappable.

**`ink-3` used for body text.** It passes 3:1, not 4.5:1. It is for captions and metadata at large sizes only.

**Accent used as both a large fill and small text.** The value bright enough to work as a fill is almost never dark enough for text. Use two steps.

**Web fonts in a PDF pipeline.** Silently substituted, breaking every layout. Use the metric-safe column.

**Second accent added "for variety".** Two saturated accents from different hue families make an artifact look assembled. If a second color is genuinely needed, take it from the ink ramp.

**Dark theme, shadows unchanged.** Shadows are invisible on dark backgrounds. Elevation on dark comes from a *lighter* surface, not a darker shadow.

**Contrast checked in one mode only.** Light passing tells you nothing about dark.
