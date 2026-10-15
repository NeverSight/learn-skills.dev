---
name: design-taste
description: |
  Anti-slop design skill for landing pages, portfolios, and marketing sites. The agent reads the brief, infers a deliberate design direction, and ships interfaces that do not look AI-generated. Ban the LLM defaults, set typography and color deliberately, run the pre-flight checklist before finishing.
triggers:
  - "design taste"
  - "anti slop"
  - "make it look designed"
  - "premium landing page"
  - "not generic"
  - "editorial design"
  - "portfolio redesign"
---

# design-taste

> Applies to landing pages, portfolios, marketing sites, and product UI generation.
> Every rule is contextual: first read the brief, then apply what fits. Never apply all of it blindly.

---

## 0. READ THE ROOM BEFORE ANYTHING

LLM output looks generic because the model jumps to a default aesthetic instead of reading the brief. Before writing any code, infer:

1. **Page kind** — landing (SaaS / consumer / agency / event), portfolio (designer / dev / studio), product page, redesign.
2. **Vibe words** — "minimal", "warm", "premium", "playful", "trust-first", "editorial", "dark", "agency". These pick the direction.
3. **Audience** — the audience picks the aesthetic, not your taste. A government service does not get kinetic typography.
4. **Existing brand** — logo, colors, type, photography. Redesigns start from these; they are input, not optional.

Declare a one-line **design read** before generating, so the user sees the reasoning:

- *"Reading this as: B2B SaaS landing for technical buyers, Linear-style minimal, restrained motion, monochrome + one accent."*
- *"Reading this as: solo designer portfolio for hiring managers, editorial print language, oversized serif, asymmetric grid."*

If the read is genuinely ambiguous, ask exactly one question. Otherwise proceed — do not default.

## 1. THE NEVER LIST (LLM Defaults — Banned)

These are the fingerprints of AI-generated design. Avoid them deliberately:

- Indigo-to-purple (or blue-to-purple) gradient hero backgrounds and gradient text.
- Centered hero with a badge pill + oversized bold heading + two buttons + product screenshot.
- "Three equal feature cards" layout as the default section structure.
- Emoji as feature icons (📊🚀⚡). Icons must be drawn or typographic, never emoji.
- Glassmorphism (frosted `backdrop-filter` cards) everywhere.
- `Inter` + `slate-900` as the automatic palette.
- `rounded-2xl` on everything; shadows as the only source of depth.
- Identical symmetric sections stacked in a page; every page using the same skeleton.
- "Get started free" purple button on every page regardless of context.
- 6+ nested cards — cards inside cards inside cards.

If the design read gives no reason to use any of these, do not use them.

## 2. TYPOGRAPHY (The Highest-Value Discipline)

Most "premium" verdicts come from type. Spend your quality budget here first.

- **Pair with contrast.** A serif display + clean sans, or grotesk display + mono labels. Never a single neutral sans for everything. Never default Inter unless the brand already uses it.
- **Display scale is your identity.** Make the hero headline genuinely large (`clamp(3rem, 8vw, 7rem)` range) with tight leading (0.95–1.05). Small-ish bold text reads "template".
- **Labels and metadata in mono or small caps**, letterspaced (0.08–0.15em), uppercase. Section numbers ("01", "02") in the same language.
- **Line length for body: 45–75 characters.** Body text 16–18px, generous line-height 1.55–1.7.
- **One type size hierarchy per section.** Don't show 6 font sizes in one viewport.
- Avoid 6-line paragraph wraps: ~3 lines max per paragraph, or widen the column.

## 3. COLOR (Restraint Is the Signal)

- **Start from one neutral + one accent.** Warm paper / ink, or off-black / off-white. Two neutrals + one accent is a complete palette. Three accents is a rainbow.
- **No default dark-navy backgrounds** unless the read is dark-tech. Dark ≠ premium automatically.
- **Color with intent:** the accent exists to point at one action, one stat, one highlight. Everything else stays neutral.
- **Text contrast ≥ 4.5:1** on body text. Never white-on-low-opacity-indigo.
- Use tonal depth — different tints of your neutral — instead of adding new colors.

## 4. LAYOUT & COMPOSITION (Asymmetry Reads as Designed)

- Asymmetric grids: offset the content column from center (split 7/5, 6/6 with a rule between, oversized left column with a narrow index right column).
- **Indexing:** numbers, section rules (thin hairlines top/bottom), and a visible grid structure make a page feel art-directed.
- One deliberate grid per page: everything aligns to it. Hairlines (1px `rgba(ink, 0.1–0.2)`) are the cheap way to look expensive.
- Whitespace is the tool: generous margins, breathing room around the hero, space between sections ≥ 96–160px.
- Avoid equal-height card trios everywhere; vary section rhythm (full-bleed, split, indexed list, quote, table).

## 5. DEPTH & SURFACE (Structure, Not Shadows)

- Depth from structure: hairlines, inset panels, offset blocks, tonal backgrounds. Shadows only for floating elements, and soft ones (blur ≥ 24px, low opacity).
- No gradient surfaces on buttons/CTAs. A solid, saturated accent performs better and looks better.
- No screenshot-in-browser-chrome mockups as the default hero visual — a metric table, an editorial column, an oversized pull-quote, or the type itself is often stronger.
- If the brief has no imagery, design with structure (rules, type, color blocks), not stock gradients or placeholder photos.

## 6. MOTION (Discipline Over Fireworks)

- Default: minimal. One intentional transition (nav reveal, hero entrance, scroll-triggered section fade).
- No infinite loop animations, no bounce-entrances on every element, no floating gradient orbs.
- Ease: `cubic-bezier(0.22, 1, 0.36, 1)`-style long tropical curves, 300–600ms. Snappy in, calm out.
- If the read is playful, motion is where that budget goes — not color.

## 7. PRE-FLIGHT CHECKLIST (Run Before "Done")

Read your own output as a stranger would. Fail the page if:

- [ ] It could have been made by typing "landing page" into the same agent without this skill (be honest).
- [ ] The hero is centered badge + heading + 2 buttons + screenshot.
- [ ] Any emoji icon is used as a UI element.
- [ ] Three identical cards in a row appear out of template habit.
- [ ] Font is a single neutral sans with no display contrast.
- [ ] More than ~2 colors carry meaning.
- [ ] Body text lines wrap past ~6 lines or the column is full-width.
- [ ] The accent color appears more than ~4 times per viewport (it stops pointing at anything).
- [ ] Any section could be deleted without losing the design argument.

If any box gets ticked, redo that section. One undeniably intentional page beats a polished template.

---

*Taste is a checklist you run before you ship. This is that checklist in skill form.*