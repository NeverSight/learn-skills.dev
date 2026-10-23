---
name: brand-guidelines
description: "Creates comprehensive brand guidelines documents (brand books) for any brand. Guides users through a structured brand interview, collects colors, typography, logo usage rules, tone of voice, and visual style, then generates a professional self-contained HTML brand book. Use when a user asks to: \"create brand guidelines\", \"make a brand book\", \"design a style guide\", \"build brand standards\", \"create visual identity guidelines\", \"document our brand\", or wants to formalize their brand's look and feel. Also use when the user provides brand assets (colors, logos, fonts) and wants them organized into a cohesive document. Always use this skill for any brand guidelines or brand book creation task, even if the user just says \"I need a style guide\" or mentions brand colors and fonts in a design context."
license: Complete terms in LICENSE.txt
---

# Brand Guidelines Creator

Create professional brand guidelines documents (brand books) for any brand. Collect brand assets through a structured interview, then generate a self-contained HTML brand book.

**Output**: Single self-contained HTML file — no dependencies, opens in any browser, printable to PDF via Ctrl+P.

## Pipeline

```
[User Request]
      |
      v
[Detect Mode] -----> Express / Guided / Discovery
      |
      v
[Brand Interview]    6 stages, batched questions
      |
      v
[Confirmation]       Summary for user approval
      |
      v
[Generate HTML]      Self-contained brand book
      |
      v
[brand-guidelines.html]
```

---

## Modes

Determine the mode from the user's input:

**Express** — User provides brand assets upfront ("Here are my colors: #2563EB, #1E293B; font: Inter; brand name: Acme"). Validate inputs, fill gaps with smart defaults, confirm, generate.

**Guided** — User has some ideas but needs structure ("I want a brand guide for my SaaS startup"). Run the full 6-stage interview with suggestions.

**Discovery** — User starts from scratch ("Help me create a brand identity"). Start from personality/values, derive palette and typography suggestions, then proceed through all stages.

---

## Brand Interview Protocol

Present questions in batches by stage — not one at a time. Allow "skip" or "default" for any stage. After all stages, present a confirmation summary before generating.

### Stage 1: Brand Identity (required)

```
Brand name:
Tagline / slogan (optional):
Industry / domain:
Brand personality (3-5 adjectives, e.g. bold, friendly, minimal):
```

### Stage 2: Color Palette

```
Primary color (hex or describe, e.g. "deep blue"):
Secondary color:
Accent color(s):
Background light:
Background dark:
Semantic colors — success / warning / error / info (or "default"):
```

If user provides personality adjectives but no colors, generate 2-3 palette suggestions. Read `references/brand-interview-guide.md` for the personality-to-palette algorithm and industry defaults.

**Palette suggestion format:**
```
Based on "[adjectives]", here are three palette options:

Option A (name): Primary #XXXXXX, Secondary #XXXXXX, Accent #XXXXXX
Option B (name): Primary #XXXXXX, Secondary #XXXXXX, Accent #XXXXXX
Option C (name): Primary #XXXXXX, Secondary #XXXXXX, Accent #XXXXXX

Which resonates most? You can also mix and adjust.
```

### Stage 3: Typography

```
Heading font (e.g. Inter, Poppins):
Body text font:
Monospace font (optional, for code/technical content):
Font weights (e.g. 400, 600, 700):
```

If user has no font preference, recommend based on brand personality. Read `references/brand-interview-guide.md` for font pairing recommendations.

### Stage 4: Logo & Imagery

```
Logo file path(s) (if available on disk):
Logo minimum size:
Logo clear space rule:
Prohibited logo alterations:
Photography / illustration style:
Icon style (outlined, filled, duotone):
```

If user provides a logo file, read it and embed as base64 data URI in the HTML. If no logo exists, create a placeholder section with "Logo TBD" and document the usage rules for when a logo is added.

### Stage 5: Voice & Tone

```
Communication style (formal / casual / technical / friendly):
Words to use:
Words to avoid:
Example sentences for different contexts (marketing, support, technical):
```

### Stage 6: Spacing & Layout

```
Base spacing unit (default: 8px):
Spacing scale (default: 4, 8, 12, 16, 24, 32, 48, 64):
Border radius (default: 4px, 8px, 12px):
Shadow / elevation style:
```

### Minimum Viable Input

The absolute minimum to generate a brand book:
- Brand name
- 1 primary color
- 1 font choice

Everything else gets smart defaults. Always inform the user what defaults were applied.

---

## Brand Data Model

Build this structure during the interview. Use it to populate the HTML template.

```json
{
  "name": "Brand Name",
  "tagline": "Optional tagline",
  "industry": "technology",
  "personality": ["innovative", "trustworthy", "bold"],
  "colors": {
    "primary": { "hex": "#2563EB", "name": "Brand Blue" },
    "secondary": { "hex": "#1E293B", "name": "Dark Slate" },
    "accent": [
      { "hex": "#F59E0B", "name": "Amber" }
    ],
    "background": { "light": "#FFFFFF", "dark": "#0F172A" },
    "semantic": {
      "success": "#22C55E",
      "warning": "#EAB308",
      "error": "#EF4444",
      "info": "#3B82F6"
    }
  },
  "typography": {
    "heading": {
      "family": "Inter",
      "fallback": "Arial, sans-serif",
      "weights": [600, 700]
    },
    "body": {
      "family": "Inter",
      "fallback": "Arial, sans-serif",
      "weights": [400, 500]
    },
    "mono": {
      "family": "JetBrains Mono",
      "fallback": "Consolas, monospace"
    },
    "scale": {
      "h1": "3rem",
      "h2": "2.25rem",
      "h3": "1.875rem",
      "h4": "1.5rem",
      "h5": "1.25rem",
      "body": "1rem",
      "small": "0.875rem",
      "caption": "0.75rem"
    }
  },
  "logo": {
    "file_base64": null,
    "file_type": "svg",
    "min_size": "32px",
    "clear_space": "1x logo height on all sides",
    "prohibited": ["stretch", "rotate", "change colors", "add effects"],
    "photography_style": "lifestyle, natural light",
    "icon_style": "outlined"
  },
  "voice": {
    "style": "professional yet approachable",
    "do": ["use active voice", "be concise", "lead with benefits"],
    "dont": ["use jargon", "be condescending", "use passive voice"],
    "examples": {
      "marketing": "Example marketing copy",
      "support": "Example support message",
      "technical": "Example technical documentation"
    }
  },
  "spacing": {
    "base": 8,
    "scale": [4, 8, 12, 16, 24, 32, 48, 64],
    "border_radius": { "sm": "4px", "md": "8px", "lg": "12px", "full": "9999px" },
    "shadows": {
      "sm": "0 1px 2px rgba(0,0,0,0.05)",
      "md": "0 4px 6px rgba(0,0,0,0.07)",
      "lg": "0 10px 15px rgba(0,0,0,0.1)"
    }
  }
}
```

---

## Smart Defaults by Industry

When user provides industry but skips color/font choices, use these as starting suggestions:

| Industry | Palette Direction | Font Pairing | Tone |
|----------|-------------------|-------------|------|
| Technology | Blue/slate tones | Inter / System UI, sans-serif | Clean, direct |
| Healthcare | Blue-green/teal | Nunito Sans / clean serif | Calm, trustworthy |
| Finance | Navy / gold | Playfair Display + Source Sans | Formal, authoritative |
| Food & Beverage | Warm earth tones | Rounded sans (Nunito, Quicksand) | Friendly, appetizing |
| Creative / Design | Bold / unexpected | Display + geometric sans | Playful, expressive |
| Education | Blue / green | Readable sans (Open Sans, Lato) | Approachable, clear |
| Luxury | Black / gold / white | Elegant serif (Cormorant, Libre Baskerville) | Refined, exclusive |
| Nonprofit | Earth tones / hopeful | Humanist sans (Source Sans, Fira Sans) | Warm, inspiring |
| E-commerce | Vibrant accent + neutral | Modern sans (Inter, DM Sans) | Persuasive, clear |
| Legal | Dark blue / charcoal | Traditional serif (Merriweather) | Formal, precise |

Read `references/brand-interview-guide.md` for expanded personality-to-palette mappings.

---

## Confirmation Summary

Before generating, present a formatted summary of all collected brand data:

```
## Brand Book Summary — [Brand Name]

**Identity**: [name] — "[tagline]"
**Personality**: [adjective1], [adjective2], [adjective3]

**Colors**:
- Primary: [swatch] #XXXXXX "[name]"
- Secondary: [swatch] #XXXXXX "[name]"
- Accent: [swatch] #XXXXXX "[name]"

**Typography**:
- Headings: [font] ([weights])
- Body: [font] ([weights])

**Logo**: [provided / placeholder]
**Voice**: [style summary]
**Spacing base**: [N]px

Defaults applied: [list any auto-filled values]

Shall I generate the brand book with these settings?
```

---

## HTML Brand Book Generation

Read `references/html-brand-book-template.md` for the complete HTML/CSS template.

### Structure of the Output File

The generated `brand-guidelines.html` file contains:

1. **Cover Page** — Brand name, tagline, generation date, personality keywords
2. **Table of Contents** — Clickable anchor links to each section
3. **Color Palette** — Visual swatches with hex / RGB / HSL values, contrast ratio badges (WCAG AA/AAA), light & dark mode palettes
4. **Typography** — Live font specimens at each scale level (H1-caption), weight demonstrations, line height and letter spacing
5. **Logo Usage** — Logo display (base64 embedded or placeholder), minimum size, clear space diagram, do's and don'ts grid
6. **Voice & Tone** — Style description, word choice guidance, example copy in 3 contexts
7. **Spacing & Layout** — Spacing scale visualization, border radius specimens, shadow elevation examples
8. **Component Examples** — Buttons (primary/secondary/ghost), cards, form inputs, alerts styled to brand
9. **Quick Reference Card** — One-page summary of all key values (copy-paste friendly hex codes, font names, spacing values)

### Technical Requirements

- **Self-contained**: All CSS inline in `<style>`, no external stylesheets
- **Fonts**: Google Fonts via `<link>` tags in `<head>`, with CSS fallback stacks for offline
- **Logo**: Embedded as base64 `data:` URI in `<img>` tag, or SVG inline
- **Colors**: Rendered as CSS background-color divs, not images
- **Contrast**: Small inline JS function (~20 lines) calculating WCAG luminance ratio, showing AA/AAA badges
- **Print**: `@media print` rules — page breaks between sections, hide interactive elements
- **Responsive**: Works on desktop and mobile viewports
- **Size**: ~800-1500 lines depending on brand complexity

Read `references/brand-book-sections.md` for detailed content standards per section.

### Output Path

- Default: `./brand-guidelines.html` in current working directory
- Multi-brand projects: `./brand-guidelines-{brandname}.html`
- After generation, report the file path to the user

---

## Logo Handling

If user provides a logo file path:
1. Read the file using the Read tool
2. For SVG: embed inline in the HTML
3. For PNG/JPG: base64 encode and embed as `data:image/png;base64,...`
4. Display in the Logo Usage section with clear space visualization

If no logo file:
1. Create a text-based placeholder using brand name + primary color
2. Document logo usage rules with placeholder area
3. Add note: "Replace placeholder with final logo"

---

## Pitfalls to Avoid

- Never generate brand colors without user confirmation — always present options and ask
- Always calculate and display contrast ratios for text-on-background combinations
- Warn if selected fonts are not available on Google Fonts (offline viewing impact)
- Never hardcode any specific company's brand values — this is a universal skill
- Do not try to generate logos, create social media templates, or design systems — output is one HTML brand book document
- When embedding logo images, verify the file exists before reading
- Always apply consistent naming to colors (give each color a semantic name)
