---
name: pro-deck-builder
description: Create polished HTML slide decks and PDF-ready documents for consulting deliverables. Uses the RRBC design system with warm light mode, dark mode cover pages, Lora/Inter/Roboto Mono typography, and data visualization palette. Trigger on 'deck', 'slides', 'presentation', 'pitch deck', 'keynote', 'report', or 'PDF'.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: reporting
  domain: presentations
  updated: 2026-02-23
  tested: 2026-03-17
  tested_with: "Claude Code v2.1"
---

# Presentation Designer

VC-backed SaaS design quality for PowerPoint. Think Linear, Attio, Vercel, Raycast — not corporate clip art.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/pro-deck-builder ~/.claude/skills/
```

## Quick Reference

| Task | Approach |
|------|----------|
| Create from scratch | Read [REFERENCE.md](REFERENCE.md), use PptxGenJS |
| Edit existing / use template | Read [editing.md](editing.md) |
| Read/extract content | `python -m markitdown presentation.pptx` |
| Visual overview | `python scripts/thumbnail.py presentation.pptx` |

---

## Before You Start (Required Steps)

### Step 1: Ask the User

Before writing any code, ask:

1. **Light or dark mode?** Dark = premium/keynote feel. Light = reports/data-heavy decks.
2. **Palette preference?** Show the palette table below, or ask if they have brand colors.
3. **Logo?** Ask if they have a logo file to include (PNG/SVG path).

### Step 2: Discover Fonts

Check what's installed — premium fonts make a massive difference:

```bash
# macOS — list all installed font families
fc-list : family | sort -u

# Search for premium fonts first
fc-list : family | grep -iE "inter|dm.sans|poppins|avenir|futura|geist|sf.pro|sf.mono|jetbrains|fira.code|montserrat|playfair|source.sans"

# Check macOS Font Book directories directly
ls ~/Library/Fonts/ /Library/Fonts/ /System/Library/Fonts/Supplemental/ 2>/dev/null
```

**Priority order for font selection:**
1. **Inter** — the gold standard for SaaS UI (if installed, use it for everything)
2. **DM Sans** — geometric, startup-friendly
3. **Poppins** — rounded, approachable
4. **Avenir / Avenir Next** — ships with macOS, Apple-adjacent elegance
5. **Calibri** — safe fallback, always available

**For data/mono:** JetBrains Mono > Fira Code > SF Mono > Consolas

---

## Design Language: VC-Backed SaaS

### Aesthetic Principles

1. **Depth through layering** — Surfaces float above backgrounds. Cards and panels have subtle elevation via shadows and fine borders, not flat colored boxes.
2. **Bold typography, minimal decoration** — Let type hierarchy do the work. No accent lines, no decorative shapes, no clip art.
3. **Restrained color** — One accent color used sparingly (10%). Mostly neutrals. Color = signal, not decoration.
4. **Generous whitespace** — Empty space signals confidence. If a slide feels sparse, make the content bigger, don't add more.
5. **Every element earns its place** — Before adding anything: what does it communicate? If removing it changes nothing, remove it.

### Light vs Dark Mode

The user picks one mode for the entire deck. Never mix modes within a deck.

---

## Color System

### Dark Mode (Default — Premium/Keynote)

| Token | Value | Use |
|-------|-------|-----|
| `bg-primary` | `0A0A0C` | Slide backgrounds (deep space black) |
| `bg-surface` | `17181A` | Cards, panels (deep slate) |
| `bg-elevated` | `1E1F23` | Elevated surfaces, hover states |
| `bg-glass` | `FFFFFF` at 4% opacity | Translucent overlays |
| `text-primary` | `FFFFFF` | Headlines, key content |
| `text-secondary` | `A0A0A0` | Body text, descriptions |
| `text-muted` | `5A5A5E` | Captions, metadata, labels |
| `border-subtle` | `FFFFFF` at 8% opacity | Card borders |

### Light Mode (Reports/Data-Heavy)

| Token | Value | Use |
|-------|-------|-----|
| `bg-primary` | `FFFFFF` | Slide backgrounds |
| `bg-surface` | `F8F9FA` | Cards, panels |
| `bg-elevated` | `FFFFFF` | Elevated surfaces (use shadow) |
| `text-primary` | `111111` | Headlines, key content |
| `text-secondary` | `555555` | Body text, descriptions |
| `text-muted` | `999999` | Captions, metadata, labels |
| `border-subtle` | `E8E8E8` | Card borders |

---

## Palette System

Each palette defines one accent color (used at 10%) plus semantic status colors. The accent is the personality — everything else is neutral.

### Built-In Palettes

| Name | Accent | Hex | Best For |
|------|--------|-----|----------|
| **Electric Blue** | Intense azure | `0055FF` | SaaS, tech, product |
| **Neon Lime** | Acid green | `39FF14` | Dev tools, performance |
| **Hot Coral** | Warm energy | `FF6B6B` | Marketing, creative |
| **Indigo** | Deep purple | `6366F1` | Startups, AI/ML |
| **Teal Trust** | Cool confidence | `0D9488` | Healthcare, finance |
| **Amber Signal** | Warm authority | `F59E0B` | Consulting, strategy |
| **Rose** | Refined pink | `F43F5E` | Design, brand, luxury |
| **Emerald** | Growth green | `10B981` | Sustainability, success |
| **Cyan Edge** | Sharp blue-green | `06B6D4` | Data, analytics |
| **Violet** | Creative depth | `8B5CF6` | Education, innovation |
| **Slate** | No accent | `64748B` | Minimal, understated |
| **Gold Standard** | Financial premium | `D4AF37` | Investor, board decks |

### Custom Palette (User Brand Colors)

If the user provides brand colors, build a custom palette:

```javascript
const palette = {
  accent: "0055FF",      // primary brand color
  accentMuted: "0055FF" + " at 15% opacity", // for tinted backgrounds
  positive: "10B981",    // good, up, success
  warning: "F59E0B",     // attention, caution
  critical: "EF4444",    // bad, down, error
};
```

### Color Application: 85/10/5 Rule

- **85%** — Backgrounds + neutral text (bg + text tokens from mode)
- **10%** — Accent (key numbers, chart primary, CTAs, active states)
- **5%** — Semantic status (positive/warning/critical in KPIs and data)

---

## Typography

### Font Priority

Run font discovery (Step 2 above), then pick:

| Priority | Header | Body | Data/Mono | Vibe |
|----------|--------|------|-----------|------|
| 1st | Inter 700 | Inter 400 | JetBrains Mono | Linear/Vercel |
| 2nd | DM Sans 700 | DM Sans 400 | Fira Code | Geometric startup |
| 3rd | Avenir Next Bold | Avenir 400 | SF Mono | Apple-adjacent |
| 4th | Poppins 700 | Poppins 400 | JetBrains Mono | Friendly modern |
| Safe | Calibri Bold | Calibri | Consolas | Always available |

For editorial/financial decks:

| Header | Body | Vibe |
|--------|------|------|
| DM Serif Display | DM Sans | Sophisticated editorial |
| Playfair Display | Source Sans Pro | Luxury, financial |
| Georgia | Calibri | Classic corporate |

### Size Scale

| Role | Size | Weight | Use |
|------|------|--------|-----|
| Hero title | 54-72pt | Bold (700) | Title slide only |
| Slide title | 32-40pt | Bold (700) | Every content slide |
| Section header | 20-24pt | Semibold (600) | Within-slide sections |
| Body text | 14-16pt | Regular (400) | Paragraphs, bullets |
| Captions/meta | 10-12pt | Regular (400) | Footnotes, sources |
| Big KPI number | 48-72pt | Bold (700) | Dashboard callouts |
| KPI label | 9-10pt | Semibold, ALL CAPS, +tracking | Below KPI numbers |
| Data/numbers | 11-14pt | Mono regular | Tables, data labels |

### Typography Rules
- **Left-align** body text and lists — center ONLY titles and KPI values
- **Max 2 font families** per deck (+1 mono for data)
- **ALL CAPS + charSpacing** only for small labels (KPI labels, category tags)
- **Line height**: 1.3x for body, 1.1x for titles
- **Never underline** for emphasis — use bold or accent color

### Text Fitting (Prevents Overflow)

Big numbers and titles WILL overflow if you use a fixed font size without checking content length. Use these rules:

**Big KPI Numbers — scale font to character count:**

| Characters | Example | Max Font Size (card) | Max Font Size (standalone) |
|------------|---------|---------------------|--------------------------|
| 1–4 | `$4.2M` | 48pt | 72pt |
| 5–7 | `$5,307K` | 36pt | 54pt |
| 8–10 | `$5,307,540` | 28pt | 44pt |
| 11+ | `$12,345,678` | 22pt | 36pt |

**Rule: prefer abbreviated numbers.** `$5.3M` > `$5,307,540`. Only use full numbers in tables or footnotes where precision matters.

**Slide Titles — max characters before wrapping:**

| Font Size | Max Chars (~9" wide) | If Longer |
|-----------|---------------------|-----------|
| 54pt | ~30 | Reduce to 44pt or rewrite shorter |
| 44pt | ~38 | Reduce to 36pt or rewrite shorter |
| 36pt | ~46 | Reduce to 32pt or rewrite shorter |
| 32pt | ~52 | Use subtitle for overflow |

**Rule: count characters before setting fontSize.** Never let content slide titles wrap to 2 lines. Section dividers can wrap.

**Body Text in Narrow Containers (Insight Panels, Sidebars):**

Text overflow in narrow panels (< 4" wide) is a common problem. PptxGenJS does not auto-shrink text. Apply these rules:

| Container Width | Max fontSize | Max chars per line (~) | Max lines at 1.25x spacing |
|----------------|-------------|----------------------|---------------------------|
| 4.0"+ | 14pt | ~55 | Height ÷ 0.22" |
| 3.0-3.9" | 11pt | ~45 | Height ÷ 0.18" |
| 2.0-2.9" | 10pt | ~35 | Height ÷ 0.16" |
| < 2.0" | 9pt | ~25 | Height ÷ 0.15" |

**Rule: estimate line count before adding text.** Count characters in your text, divide by max chars per line to get line count, then verify it fits in the container height. If it doesn't fit: (1) reduce fontSize, (2) shorten the text, or (3) increase the container. Never let text silently overflow — it gets clipped or overlaps adjacent elements.

```javascript
// ✅ CORRECT: 2.8" panel → max 10pt, ~35 chars/line
// "Welcome series dominates at 62%..." = 90 chars ≈ 3 lines
// Container h: 1.6" → fits ~10 lines at 10pt. Safe.
s.addText("Short, edited copy.", {
  x: 6.55, y: 1.45, w: 2.7, h: 1.6,
  fontSize: 10, fontFace: theme.font.body,
});

// ❌ WRONG: 2.8" panel with 14pt font and 200+ char paragraph
s.addText("Very long paragraph that will overflow...", {
  x: 6.55, y: 1.45, w: 2.8, h: 1.6,
  fontSize: 14, fontFace: theme.font.body,  // too large for narrow panel
});
```

### Chart Number Formatting

Always format chart numbers for readability — raw numbers like "1000000" are never acceptable on axes OR data labels.

**CRITICAL: `valAxisLabelFormatCode` only formats the AXIS. Data labels from `showValue: true` are formatted separately via `dataLabelFormatCode`.** If you set `valAxisLabelFormatCode` but not `dataLabelFormatCode`, data labels will show raw unformatted numbers like "2888000". `numFmt` is NOT a valid PptxGenJS property — always use `dataLabelFormatCode`.

**Preferred approach — OOXML conditional format with raw values:**
Use raw (unscaled) values and let OOXML conditional number formatting handle the display. This is the most reliable approach and handles mixed-magnitude data (e.g., a chart with both $2.9M and $3.6K values).

```javascript
// ✅ BEST: Raw values + OOXML conditional format
// Under 1K: whole number ($500)
// 1K-999K: X.XXK ($540.18K, $57.72K)
// 1M+: X.XM ($2.9M)
const currFmt = '[>=1000000]"$"#,##0.0,,"M";[>=1000]"$"#,##0.00,"K";"$"#,##0';

values: [2888000, 717734, 425467, 3655],  // raw dollar values
dataLabelFormatCode: currFmt,              // conditional brackets OK here
valAxisLabelFormatCode: '"$"#,##0.0,,"M"', // simple format only (no brackets)
```

```javascript
// ✅ ALSO OK: Pre-scale when all values are same magnitude
values: [2888, 718, 425],  // raw values divided by 1000
dataLabelFormatCode: '"$"#,##0"K"',
valAxisLabelFormatCode: '"$"#,##0"K"',
```

```javascript
// ❌ WRONG: Raw values with axis-only format
values: [2888000, 718000, 425000],
valAxisLabelFormatCode: "$#,##0,K",  // axis may format but data labels show 2888000
// ❌ WRONG: numFmt (not a valid PptxGenJS property)
```

**OOXML conditional format reference (use with RAW values):**

| Data Range | Format Code | Renders As |
|------------|-------------|------------|
| Currency (auto-scale) | `'[>=1000000]"$"#,##0.0,,"M";[>=1000]"$"#,##0.00,"K";"$"#,##0'` | $2.9M, $540.18K, $500 |
| Plain number (auto-scale) | `'[>=1000000]#,##0.0,,"M";[>=1000]#,##0.00,"K";#,##0'` | 2.9M, 540.18K, 500 |
| Percentage | `'0%'` | 50%, 85% |

**Format code syntax:** OOXML supports up to 2 conditions in brackets + a default: `[condition1]format1;[condition2]format2;defaultFormat`. Each trailing `,` divides by 1,000 (so `,,` divides by 1M).

**IMPORTANT: `valAxisLabelFormatCode` does NOT support OOXML conditional brackets `[>=1000]`.** Use a simple format for the axis based on the data range:

| Axis Range | `valAxisLabelFormatCode` | Renders As |
|------------|----------------|------------|
| Up to ~999K | `'"$"#,##0,"K"'` | $0K, $100K, $500K |
| Up to ~10M+ | `'"$"#,##0.0,,"M"'` | $0.0M, $0.5M, $1.0M |
| Up to ~999 | `'"$"#,##0'` | $0, $100, $500 |

Use the conditional `currFmt` for `dataLabelFormatCode` (which supports brackets), but a simple format for `valAxisLabelFormatCode`. Always set `showValue: true` with `dataLabelPosition: "outEnd"` on bar charts so readers can see exact values without tracing to the axis.

---

## Spacing

| Token | Value | Use |
|-------|-------|-----|
| `xs` | 0.125" | Within grouped elements |
| `sm` | 0.25" | Label to value, icon to text |
| `md` | 0.375" | Between sections within a card |
| `lg` | 0.5" | Between cards, major sections |
| `xl` | 0.75" | Between content zones |

### Layout Grid (10" × 5.625")

```
Margins:       0.5" from all edges
Content area:  9.0" wide × ~4.5" tall
Title zone:    y = 0.3"
Content zone:  y = 1.0" to y = 5.0"
Footer zone:   y = 5.2"
Card gap:      0.25" - 0.3"
```

---

## Logo Placement

### Finding Logos

```bash
find ~/Desktop ~/Downloads ~/Documents -maxdepth 3 -iname "*logo*" \( -name "*.png" -o -name "*.svg" -o -name "*.jpg" \) 2>/dev/null
```

### Placement Patterns

| Slide Type | Position | Size | Notes |
|------------|----------|------|-------|
| Title slide (top-left) | `x:0.5, y:0.4` | `w:1.5, h:0.5` | Subtle brand mark |
| Title slide (centered) | `x:4.0, y:0.8` | `w:2.0, h:0.7` | Above title text |
| Content slides | `x:8.5, y:0.2` | `w:1.0, h:0.35` | Top-right corner, every slide |
| Closing slide | `x:3.5, y:1.5` | `w:3.0, h:1.0` | Centered, hero size |

### Logo Rules
- Always use `sizing: { type: "contain", w, h }` to preserve aspect ratio
- **Content slides**: max 1" wide, don't compete with content
- **Title/closing**: up to 3" wide for brand moment
- **Dark mode**: use white/light logo variant if available (ask user)
- **Slide master**: if logo goes on every slide, add it to a master definition

---

## Icons

### Pipeline: react-icons → sharp → PNG → PptxGenJS

```bash
npm install -g react-icons react react-dom sharp
```

**Prefer Lucide (`react-icons/lu`) or Feather (`react-icons/fi`)** — they match the Linear/Vercel icon language.

| Package | Import | Style |
|---------|--------|-------|
| `react-icons/lu` | Lucide | Linear-style, clean |
| `react-icons/fi` | Feather | Thin, modern |
| `react-icons/hi2` | Heroicons v2 | Apple-ish |
| `react-icons/tb` | Tabler | Consistent strokes |

### Icon Sizes

| Context | Display Size | Color |
|---------|-------------|-------|
| KPI card icon | 0.35" × 0.35" | Accent on dark, muted on light |
| Feature row icon | 0.4" × 0.4" | White inside accent circle |
| Section divider | 0.5" × 0.5" | Accent color |
| Inline bullet | 0.25" × 0.25" | text-secondary |

---

## Reusable Components

### Bottom Callout Box (Standardized)

Many slides end with a highlighted callout box (recommendation, key insight, total impact). **These must be visually identical across all slides:**

| Property | Value | Notes |
|----------|-------|-------|
| Box height | 0.6" | Always 0.6" — never 0.5", 0.7", 0.9" |
| Text height | 0.5" | Fits inside 0.6" box with padding |
| Font size | 11pt | Always 11pt bold — never 12pt or 13pt |
| Font | `theme.font.body` | Bold, left-aligned, valign: "middle" |
| Box x/w | `x: 0.5, w: 9.0` | Full content width |
| Text x/w | `x: 0.7, w: 8.6` | Inset 0.2" from box edges |
| Text y offset | box y + 0.05" | Centers text vertically in box |
| Corner radius | 0.06" | Consistent across all callouts |

```javascript
// Standard bottom callout — copy this pattern exactly
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: calloutY, w: 9.0, h: 0.6,
  fill: { color: "DCFCE7" },  // or theme.accentMuted, "FEF3C7", etc.
  line: { color: theme.status.positive, width: 0.75 },
  rectRadius: 0.06,
});

s.addText("Callout text here.", {
  x: 0.7, y: calloutY + 0.05, w: 8.6, h: 0.5,
  fontSize: 11, fontFace: theme.font.body, bold: true,
  color: "166534", align: "left", valign: "middle",
});
```

### Table + Callout Layout (Prevents Overlap)

**Always calculate the table bottom position before placing a callout below it.** PptxGenJS tables don't auto-report their height, so you must compute it:

```
tableBottom = tableY + (rowCount × rowH)
calloutY = tableBottom + 0.15"  // minimum 0.15" gap
```

**Verify calloutY + 0.6" (callout height) < 5.2" (footer zone).** If it doesn't fit, reduce `rowH` or table font sizes — never let the callout overlap the footer.

| Rows (incl header) | rowH: 0.32" | rowH: 0.36" | rowH: 0.42" | rowH: 0.48" | rowH: 0.55" |
|---------------------|-------------|-------------|-------------|-------------|-------------|
| 6 rows | 1.92" | 2.16" | 2.52" | 2.88" | 3.30" |
| 7 rows | 2.24" | 2.52" | 2.94" | 3.36" | 3.85" |
| 8 rows | 2.56" | 2.88" | 3.36" | 3.84" | 4.40" |
| 11 rows | 3.52" | 3.96" | 4.62" | — | — |

With table starting at y: 1.0" and callout needing 0.75" (0.15" gap + 0.6" box), the table height limit is **3.45"** to stay above footer. Choose `rowH` accordingly.

### Cross-Slide Consistency Rules

Repeated elements MUST use identical dimensions across all slides:

1. **Bottom callout boxes** — same h, fontSize, padding on every slide (see standard above)
2. **Chart font sizes** — if multiple slides have bar/line charts, use identical `dataLabelFontSize`, `catAxisLabelFontSize`, and `valAxisLabelFontSize` across all of them
3. **Table styling** — header row style (`hdr()`) and cell style (`cell()`) should be defined once as helpers and reused
4. **Card dimensions** — if using stat cards on multiple slides, keep card width/height/corner radius consistent
5. **Section badge positions** — impact badges (e.g., "$400K-$800K") should use the same x, y, w, h, fontSize

**Rule: define reusable constants at the top of the script** for any dimension that appears on more than one slide.

---

## Slide Compositions

### Vary Layouts — The #1 Rule

Never repeat the same layout more than twice consecutively. Rotate through:

| Type | When | Elements |
|------|------|----------|
| **Title Slide** | Opening/closing | Hero text, subtitle, logo, date |
| **KPI Dashboard** | Executive summary | 3-5 cards, big numbers |
| **Chart + Insight** | Data with context | 60/40 split |
| **Full-Width Chart** | Chart IS the story | Full span, callout overlay |
| **Icon Feature Grid** | Features, pillars | 3-4 icon+text rows |
| **Data Table** | Financials, comparisons | Styled rows, mono numbers |
| **Section Divider** | Between sections | Bold title on dark/accent bg |
| **Quote** | Testimonials | Large italic, attribution |
| **Big Number** | Single key stat | Huge centered metric |
| **Comparison** | Before/after, vs. | Side-by-side columns |
| **Image + Text** | Products, case studies | Half-bleed image |
| **Closing** | End | Logo, CTA, contact |

---

## Anti-Patterns (Never Do These)

1. **NEVER add horizontal accent lines/bars under titles, subtitles, or headings** — This is the #1 AI tell. No thin rectangles (h: 0.03-0.05) placed under text as decorative separators. Not on title slides, not on section dividers, not on closing slides, not anywhere. If you feel a slide needs visual separation, use whitespace or a tinted panel instead.
2. **No gradient fills on shapes** — use solid colors + subtle borders
3. **No heavy shadows** — max opacity 0.1, blur 6
4. **Don't repeat layouts** on consecutive slides
5. **Don't center body text** — left-align everything except titles/KPIs
6. **No more than 2 fonts** (+1 mono)
7. **No walls of text** — max 6 lines body per slide
8. **No decorative shapes** — no random circles, triangles, swooshes
9. **No clip art** — use Lucide/Feather icons
10. **No colored card backgrounds** — cards = `bg-surface` + subtle border
11. **No unicode bullets** — use `bullet: true`
12. **No mixing light/dark** within a deck
13. **No unformatted chart data labels** — if you use `showValue: true`, you MUST also set `dataLabelFormatCode`. `valAxisLabelFormatCode` alone does NOT format data labels. Use OOXML conditional formats with raw values for best results.
14. **No long text in narrow panels without size checks** — before adding body text to any container < 4" wide, estimate line count (chars ÷ chars-per-line) and verify it fits the container height. Reduce font size or shorten text if it won't fit.
15. **No inconsistent callout boxes** — all full-width bottom callout boxes must use identical height (0.6"), text fontSize (11pt), and padding across every slide. Define the callout pattern once and copy it exactly.
16. **No callout-over-table overlap** — always calculate `tableBottom = tableY + (rows × rowH)` and place the callout at `tableBottom + 0.15"` minimum. Never hardcode callout y-positions without verifying they clear the table.
17. **No inconsistent chart font sizes** — if multiple slides contain charts, use identical `dataLabelFontSize`, `catAxisLabelFontSize`, and `valAxisLabelFontSize` values. Define these as constants and reuse them.

---

## QA (Required)

**Assume there are problems. First render is never correct.**

### Content Check
```bash
python -m markitdown output.pptx
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|placeholder|click to"
```

### Visual QA (Use Subagents)
```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

Subagent prompt:
```
Inspect these slides. Assume issues exist — find them.
Look for:
- TEXT OVERFLOW: Numbers or titles that wrap to a second line inside their container. Also check body text in narrow panels (<4" wide) — long paragraphs at font sizes >11pt will overflow.
- ACCENT LINES: Any thin horizontal bars/lines under titles or headings (must be removed)
- CHART DATA LABELS: Raw unformatted numbers on data labels (e.g., "2888000" instead of "$2,889K"). This is the #1 chart bug — valAxisLabelFormatCode does NOT format data labels.
- CHART AXES: Raw unformatted numbers on axes (should be $500K not 500000)
- Overlapping elements, cramped spacing (<0.3"), insufficient margins (<0.5")
- Low contrast, text-only slides, repeated layouts, placeholder text
- Mode inconsistency (light elements on dark or vice versa)
- Big numbers that should be abbreviated ($5.3M not $5,307,540)
- CALLOUT INCONSISTENCY: Bottom callout boxes with different heights, font sizes, or padding across slides (all must be h:0.6", fontSize:11)
- TABLE-CALLOUT OVERLAP: Callout boxes overlapping tables — calculate tableY + (rows × rowH) and verify callout clears it
- CHART FONT INCONSISTENCY: Different dataLabelFontSize, catAxisLabelFontSize, or valAxisLabelFontSize between charts on different slides
```

Fix → re-render → inspect → repeat until clean. **Complete at least one fix cycle.**

---

## Dependencies

```bash
npm install -g pptxgenjs                          # Creation
npm install -g react-icons react react-dom sharp  # Icons
pip install "markitdown[pptx]" Pillow             # Reading + QA
# Also: LibreOffice (soffice) + Poppler (pdftoppm) for visual QA
```

## Implementation

Read [REFERENCE.md](REFERENCE.md) for PptxGenJS API patterns and complete slide composition code for both light and dark modes.

## Brand Context (Optional)

If `brand-profile.json` exists in the working directory, read it before building decks. Override the default RRBC palette with the brand's colors (primary, secondary, background), use brand fonts when available (fall back to system fonts), and include the brand name on title slides and headers. This profile is produced by the `brand-dna` skill.
