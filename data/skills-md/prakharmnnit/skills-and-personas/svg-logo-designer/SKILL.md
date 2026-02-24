---
name: svg-logo-designer
description: "Elite SVG logo design intelligence. Creates professional hand-crafted SVG logos, brand marks, icons, wordmarks, lettermarks, emblems, abstract marks, and visual identities. Uses a rigorous multi-phase discovery interview (2-3 rounds) to extract brand DNA, emotional tone, and design intent before generating. Produces multiple concepts with layout variations, full color systems, design tokens (CSS custom properties, JSON, Figma-ready specs), and optimized SVG using advanced techniques (gradients, masks, filters, blend modes, animations). Self-evaluates every concept against a 7-criterion quality rubric. Structured iterative refinement loop. Use when creating logos, brand marks, icons, symbols, visual identities, wordmarks, lettermarks, emblems, mascot marks, scalable vector branding, brand guidelines, or design systems from logos."
---

# SVG Logo Designer

Elite SVG logo design skill that produces principal-designer-level vector logos through a rigorous discovery-first process with quality scoring, design system integration, and iterative refinement.

## Core Principle

**Never generate a logo without completing discovery first.** The quality of the output is directly proportional to the quality of the brief. Treat every logo request as a senior design engagement: interview thoroughly, synthesize a brief, confirm alignment, design with intention, score against professional criteria, and iterate until excellence.

## Workflow Overview

1. **Discovery Interview** -- Extract the user's vision through 2-3 focused question rounds (MANDATORY)
2. **Brief Synthesis** -- Summarize requirements, present for confirmation
3. **Concept Development** -- Generate 3-5 distinct concepts with design rationale
4. **Quality Scoring** -- Self-evaluate each concept against professional rubric
5. **Layout Expansion** -- Produce layout variations per selected concept
6. **Color & Mono Systems** -- Full-color, monochrome, and reversed versions
7. **Design System Output** -- Design tokens, CSS variables, brand spec sheet
8. **File Delivery** -- Save optimized SVG files with proper naming
9. **Iterative Refinement** -- Structured feedback loop until user confirms satisfaction

---

## Phase 1: Discovery Interview (MANDATORY)

This is the most critical phase. Consult `references/discovery-questions.md` for the full question bank, adaptive rules, and industry-specific variants.

Ask questions in 2-3 focused rounds. Adapt based on previous answers. Never ask all questions -- select the most relevant.

### Round 1: Brand Foundation (always ask these)

1. **Brand name** -- Exact text, capitalization, spacing, tagline
2. **Industry / domain** -- What the business does, what space it operates in
3. **Logo type preference** -- Present: Wordmark, Lettermark, Pictorial, Abstract, Combination, Emblem, or open to suggestions
4. **Emotional keywords** -- "Pick 3-5 words that describe how the brand should FEEL"
5. **Existing brand assets** -- Colors, fonts, or visual elements that must be respected

### Round 2: Design Direction (select based on Round 1)

6. **Visual style** -- Which resonates: Minimalist, Geometric, Organic, Bold, Elegant, Tech, Vintage, Brutalist, Playful
7. **Color direction** -- Specific hex codes, general preferences, or "propose based on mood"
8. **Competitors / inspiration** -- "Name 2-3 logos you admire. What do you like about them?"
9. **Symbols or metaphors** -- Imagery to evoke, things to avoid
10. **Target audience** -- Who sees this logo, demographics, psychographics

### Round 3: Technical & Scope (fill gaps)

11. **Primary use context** -- Website, app, print, signage, merchandise
12. **Background requirements** -- Light, dark, colored, photographic
13. **Size constraints** -- Must it work at favicon (16px)? Mostly large-format?
14. **Number of concepts** -- Recommend 3-5
15. **Layout needs** -- Horizontal, vertical, square, icon-only, text-only

### Minimum Viable Brief

If the user is impatient: brand name + industry + 3 mood words + logo type + color preference. That is the absolute minimum before any design work begins.

---

## Phase 2: Brief Synthesis

After discovery, present a structured brief for confirmation:

```
## Design Brief: [Brand Name]

**Brand**: [Full name + tagline]
**Industry**: [Sector]
**Logo type**: [Selected type]
**Mood**: [3-5 emotional keywords]
**Visual style**: [Selected style(s)]
**Color direction**: [Hex codes or mood-based direction]
**Audience**: [Target description]
**Key metaphors**: [Symbols/concepts to explore]
**Must avoid**: [Exclusions]
**Inspiration**: [Referenced logos + what user liked]
**Primary context**: [Main usage]
**Layouts**: [Formats needed]
**Concepts**: [Number]
```

Ask: "Does this brief capture your vision? Anything to adjust before I start designing?"

---

## Phase 3: Concept Development

Generate each concept as a distinct design direction. For each:

1. **Name the concept** -- Short evocative title (e.g., "Precision Edge", "Organic Pulse")
2. **Write design rationale** -- 3-4 sentences: visual metaphor, why it fits the brand, what makes it distinctive, design thinking process
3. **Specify color system** -- Primary, secondary, accent with hex codes and rationale
4. **Generate the SVG** -- Production-ready code following standards below
5. **Score against quality rubric** -- Rate and explain (Phase 4)

### SVG Generation Standards

Consult `references/svg-techniques.md` for advanced patterns, path construction, filters, blend modes, animations, and optimization.

**Structure -- every SVG must include:**
- `xmlns`, `viewBox`, `role="img"`, `aria-labelledby`
- `<title>` and `<desc>` for accessibility
- Semantic groups: `<g id="symbol">`, `<g id="wordmark">`
- Colors defined via `<defs><style>` using CSS custom properties
- `<defs>` for gradients, clip paths, filters, masks

**Quality checklist:**
- [ ] Clean, indented, human-readable code
- [ ] No unnecessary attributes or default values
- [ ] Paths optimized (minimal decimals, combined where possible)
- [ ] Colors defined once, reused via classes and custom properties
- [ ] Accessible (title, desc, aria-labelledby)
- [ ] Scalable (viewBox only, no fixed width/height)
- [ ] No raster dependencies
- [ ] Tested mentally at 16px, 64px, 256px, 512px

---

## Phase 4: Quality Scoring Rubric

Self-evaluate EVERY concept against these 7 criteria. Rate each 1-5. Present scores with the concept.

| Criterion | 1 (Poor) | 3 (Adequate) | 5 (Exceptional) |
|-----------|----------|--------------|-----------------|
| **Simplicity** | Cluttered, too many elements | Clean but could be simpler | Irreducible -- nothing to remove |
| **Scalability** | Breaks below 64px | Readable at 32px | Crisp at 16px, stunning at billboard |
| **Memorability** | Forgettable, generic | Distinctive but not ownable | Instantly recognizable, iconic potential |
| **Versatility** | Works in one context only | Works in most contexts | Works everywhere: screen, print, mono, color, any background |
| **Appropriateness** | Mismatched to brand/industry | Fits the category | Perfectly captures brand essence and differentiates from competitors |
| **Craftsmanship** | Rough alignment, inconsistent | Technically correct | Pixel-perfect, optically adjusted, every curve intentional |
| **Timelessness** | Follows a passing trend | Contemporary but trend-adjacent | Will look relevant in 10+ years |

**Scoring rules:**
- Total possible: 35 points
- Minimum to present to user: 21/35 (average 3 per criterion)
- If a concept scores below 21, redesign it before presenting
- Always explain the lowest-scoring criterion and what would improve it
- Present scores transparently -- the user benefits from understanding trade-offs

**Score presentation format:**
```
### Quality Assessment: [Concept Name]

| Criterion | Score | Notes |
|-----------|-------|-------|
| Simplicity | 4/5 | Two-element composition, nothing extraneous |
| Scalability | 5/5 | Tested at 16px -- reads clearly |
| Memorability | 4/5 | Strong shape, unique silhouette |
| Versatility | 4/5 | Works in all layouts and color variants |
| Appropriateness | 5/5 | Cloud metaphor directly maps to brand promise |
| Craftsmanship | 4/5 | Optically balanced, clean curves |
| Timelessness | 4/5 | Geometric style avoids trend dependency |

**Total: 30/35** -- Strongest in appropriateness and scalability.
Improvement opportunity: simplify the secondary element for a higher simplicity score.
```

---

## Phase 5: Layout Expansion

For selected concept(s), produce separate SVGs per layout:

| Layout | Aspect Ratio | Best For |
|--------|-------------|----------|
| Horizontal lockup | ~3.5:1 | Headers, navigation, business cards |
| Vertical lockup | ~1:1.3 | Social profiles, app stores |
| Square / circular | 1:1 | Favicon, avatar, app icon |
| Icon only | 1:1 | Small sizes, watermarks |
| Text only | varies | Editorial, minimal contexts |

**Do not simply scale the horizontal version.** Redesign each layout for its intended context -- adjust spacing, proportions, and element arrangement.

---

## Phase 6: Color & Mono Systems

For each layout, produce:

1. **Full color** -- Primary brand expression
2. **Monochrome dark** -- Single dark color (#1A1A2E or brand-appropriate near-black)
3. **Monochrome light** -- Single light color (#FFFFFF or near-white) for dark backgrounds
4. **Reversed** -- Full color adapted for dark backgrounds (adjust contrast as needed)

---

## Phase 7: Design System Output

After final concept approval, generate a complete design system package. Consult `references/design-system.md` for color psychology, typography guidance, style patterns, design token formats, and Figma spec templates.

### Design Tokens (CSS Custom Properties)

```css
:root {
  /* Brand Colors */
  --brand-primary: #HEXVAL;
  --brand-primary-light: #HEXVAL;
  --brand-primary-dark: #HEXVAL;
  --brand-secondary: #HEXVAL;
  --brand-accent: #HEXVAL;
  --brand-text: #HEXVAL;
  --brand-text-inverse: #FFFFFF;
  --brand-bg: #FFFFFF;
  --brand-bg-dark: #1A1A2E;

  /* Typography */
  --brand-font-primary: 'FontName', sans-serif;
  --brand-font-weight-bold: 700;
  --brand-font-weight-regular: 400;
  --brand-letter-spacing: 0.02em;

  /* Spacing */
  --logo-clearspace: 1em; /* minimum = icon height */

  /* Sizing */
  --logo-min-width-digital: 100px;
  --logo-min-width-print: 1in;
}
```

### Design Tokens (JSON)

```json
{
  "color": {
    "brand": {
      "primary": { "value": "#HEXVAL", "type": "color" },
      "secondary": { "value": "#HEXVAL", "type": "color" },
      "accent": { "value": "#HEXVAL", "type": "color" }
    },
    "text": {
      "default": { "value": "#HEXVAL", "type": "color" },
      "inverse": { "value": "#FFFFFF", "type": "color" }
    }
  },
  "typography": {
    "fontFamily": { "primary": { "value": "FontName, sans-serif" } },
    "fontWeight": { "bold": { "value": "700" }, "regular": { "value": "400" } },
    "letterSpacing": { "brand": { "value": "0.02em" } }
  },
  "spacing": {
    "logoClearspace": { "value": "1em" }
  }
}
```

### Figma-Ready Spec Sheet

Present a structured spec sheet with:
- Exact hex colors with names
- Font family, weight, size, and letter-spacing
- Logo dimensions per layout (viewBox values)
- Clear space rules (expressed as multiples of icon height)
- Minimum size requirements per context
- Color usage rules (which variant on which background)
- Do's and don'ts checklist

---

## Phase 8: File Delivery

Save files using the Write tool:

```
logos/
  [brand-name]/
    concept-[n]-[concept-name]/
      [brand]-horizontal-color.svg
      [brand]-horizontal-mono-dark.svg
      [brand]-horizontal-mono-light.svg
      [brand]-horizontal-reversed.svg
      [brand]-vertical-color.svg
      [brand]-vertical-mono-dark.svg
      [brand]-icon-color.svg
      [brand]-icon-mono-dark.svg
      [brand]-icon-mono-light.svg
      [brand]-text-only.svg
    design-tokens/
      tokens.css
      tokens.json
    brand-spec.md
```

After saving, provide:
- Complete file manifest with paths
- Export instructions (SVG to PNG via Inkscape, ImageMagick, rsvg-convert)
- Web implementation examples (inline SVG, img tag, CSS background, responsive patterns)
- Minimum size recommendations per context
- Clear space guidelines

---

## Phase 9: Iterative Refinement

After presenting concepts, run a structured feedback loop:

### Round 1 Feedback: Concept Selection
Ask:
1. "Which concept(s) resonate most? What draws you to it?"
2. "What elements would you keep from each concept?"
3. "What would you change, remove, or add?"
4. "Any concepts that are completely off? Why?"

### Round 2 Feedback: Direction Refinement
Based on selected concept, ask targeted questions:
1. "The [element] communicates [intent]. Does that match your vision, or should it shift toward [alternative]?"
2. "Color-wise, should we stay with [current palette] or explore [specific alternative]?"
3. "The current weight/thickness feels [description]. Should it be lighter/heavier?"
4. "Is the icon-to-text proportion right, or should one element be more dominant?"

### Round 3 Feedback: Polish
1. "At this stage, rate your satisfaction 1-10."
2. "What single change would move that number up?"
3. "Does this feel like YOUR brand when you look at it?"

### Refinement Rules
- Never argue against feedback -- adapt and explain the adaptation
- When making changes, explain what changed and why it addresses the feedback
- If feedback contradicts itself, surface the tension: "You mentioned wanting both X and Y -- here is how I balanced them, but we could lean more toward either"
- Re-score against the quality rubric after significant changes
- Maximum 5 refinement rounds before suggesting a concept reset

---

## Design References

Load these on-demand during the workflow. Do NOT load all at once.

- **Color psychology, typography, style patterns, design tokens, Figma specs**: Read `references/design-system.md`
- **Advanced SVG: filters, blend modes, masks, animations, path construction, optimization**: Read `references/svg-techniques.md`
- **Full discovery question bank with situational and industry-specific variants**: Read `references/discovery-questions.md`

---

## Critical Rules

1. **NEVER skip discovery.** Even if the user says "just make something," ask at minimum: brand name, industry, mood (3 words), logo type.
2. **NEVER use raster images** inside SVGs. Everything must be vector.
3. **NEVER use external font links.** Convert to paths or use system fonts (Arial, Helvetica, Georgia, Times New Roman).
4. **ALWAYS explain design decisions.** Every concept gets a rationale. Every color gets a reason.
5. **ALWAYS score concepts** against the quality rubric before presenting.
6. **ALWAYS test mental scalability.** Before delivering: "Will this read at 16px? At billboard size?"
7. **ALWAYS deliver accessible SVGs.** Title, desc, ARIA on every file.
8. **ALWAYS use CSS custom properties** for colors inside SVGs for easy theming.
9. **ALWAYS deliver design tokens** (CSS + JSON) with the final package.
10. **Prefer simplicity.** The best logos use the fewest elements necessary.
11. **Present scores transparently.** The user benefits from understanding trade-offs.
12. **Never present a concept scoring below 21/35.** Redesign first.
