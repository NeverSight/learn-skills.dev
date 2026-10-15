---
name: taste-typography
description: |
  Typography craft for agent-built interfaces: pairing rules, fluid type scales, line lengths, baseline rhythm, weight discipline, legibility minimums, and the typography reasons most AI-generated pages read as cheap. Use whenever generating or reviewing any UI with text. Stack on the design-taste core skill.
triggers:
  - "typography"
  - "font pairing"
  - "type scale"
  - "letter spacing"
  - "type hierarchy"
---

# taste-typography

> Type is the first thing people register and the last thing they can name. This skill makes sure the type does the design's work.

## 1. PAIRING (Two Families Max, With Purpose)

Pick two families with structural contrast — never two similar ones:

| Display | Body | Works for |
|---|---|---|
| Serif with character (Fraunces, Newsreader) | Neutral sans or the serif itself | Editorial, luxury, calm |
| Heavy grotesk (Archivo, Bricolage) | Same family at 400 | Bold, playful, brutalist |
| Neutral grotesk (Space Grotesk, system) | Same family | Dark tech, developer tools |
| Mono (labels/metadata only) | Grotesk body | Technical, terminal |

- Three families = soup. One neutral sans = template.
- Mono is a label voice, not a body voice. Mono for body text is for data tables and terminals only.
- If the brand mandates a family, the pairing is built around it — the second family comes from the same species (serif + sans from the same designer is a safe pair).

## 2. THE SCALE (Two Scales, Applied Consistently)

**Display scale** (marketing, heroes): 64 / 48 / 32 / 24 / 18 / 16 — apply with `clamp()` for fluid size: `clamp(2rem, 5vw, 4rem)`.

**UI scale** (products, dashboards): 13 / 14 / 15 / 16 / 20 / 24 — never below 12px, never above 24px inside UI surfaces.

Hierarchy rules:
- One display size per section. If two headings on a page are equally large, neither is a heading.
- Weights: one weight for display (the family's natural voice: 400 for serifs, 700–900 for grotesks), 400 for body, 500–600 for emphasis. Three weights per page max.
- Small type (≤ 12px) must be accompanied by `letter-spacing` ≥ 0.02em or it renders muddy — but never below 10px without a data-table justification.

## 3. MEASURE, LEADING, RHYTHM (The Numbers)

- **Line length:** 45–75 characters for body. Hero subheads ≤ 40 chars per line, headlines ≤ 24 chars per line (break early, not by luck).
- **Leading:** headlines 0.95–1.08 (serifs need the low end), body 1.55–1.7, labels 1.2–1.4.
- **Letterspacing:** uppercase labels 0.08–0.2em; display lowercase −0.02em; body 0. NEVER apply tracking to lowercase body text above 16px except as a deliberate editorial act.
- **Vertical rhythm:** all text blocks align to the 4px baseline grid. When in doubt, `line-height` in multiples of 4: 20/24/28/32px.
- **Paragraphs:** max ~3 lines per paragraph in marketing copy. A 6-line paragraph in a card is a layout failure, not a copy failure.

## 4. TEXT PLACEMENT (The Details That Read as "Designed")

- **Never set body text full-width** — constrain to 32–40em columns, even (especially) on widescreen.
- **Break headlines deliberately:** control word breaks with manual line structure where it matters ("Know exactly / what your users do").
- **Headline + sub + paragraph:** each step should visibly shrink in size AND weight, not just one of them.
- **Justified text is banned** except for print-style editorial columns ≥ 60 chars with hyphenation. Left-aligned everywhere else.
- **Ragged edges matter:** no widows (single word on last line) in headings — fix with word breaks or sizing.
- **Faux styling:** no fake italics (use the family's real italic face), no fake bold (never `font-weight: 700` on a 400-only family).
- **Fluid type:** `clamp()` with rem, not px, for all text. Never `vw` units without a rem floor.

## 5. ACCESSIBILITY FLOOR (Non-Negotiable)

- Body ≥ 16px on marketing pages, ≥ 14px inside UI; below that, only metadata with 4.5:1 contrast.
- Contrast ≥ 4.5:1 for all body, 3:1 for large display (≥ 24px / 18.66px bold).
- `text-rendering: optimizeLegibility` on display; no `-webkit-text-stroke` (breaks at small sizes).
- Font loading: `font-display: swap`; preload the display face; never render invisible text waiting for fonts.

## 6. CHECKLIST (Fail the Page If…)

- [ ] One neutral family doing every job.
- [ ] More than two families.
- [ ] A heading below 20px with body beside it at 16px (no hierarchy).
- [ ] Body text wider than 75 characters.
- [ ] Any text under 10px.
- [ ] More than three font weights in use.
- [ ] A 6-line paragraph inside a card or sidebar.
- [ ] Justified text without hyphenation support.

*If the typography works, people will say the site "feels premium" and not know why. That's the goal.*