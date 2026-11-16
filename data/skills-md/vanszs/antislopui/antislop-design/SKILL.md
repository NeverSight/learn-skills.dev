---
name: antislop-design
description: "Load before writing, reviewing or fixing any web UI code (HTML, CSS, Tailwind, React) or when auditing accessibility and visual quality. A single deterministic contract: a ban filter for AI-slop defaults (purple gradients, Inter everywhere, 3-card grids, glassmorphism, emoji icons, invented proof), a positive pattern library (layouts, typography, components, charts, web dashboards, award-tier craft), and a CSV design-system generator whose output is post-filtered before use. Not for backend, API, data pipelines, docs-only work, native mobile UI, or data-viz in notebooks and BI tools."
license: MIT
compatibility: "Python 3.8+ for the CSV research tool (ui-ux-pro-max/scripts/search.py); everything else is Markdown."
metadata:
  author: "Vanszs (catalog by b4r7x)"
  version: "3.0.0"
  suite_version: "3.0.0"
  updated: "2026-11-14"
  references: "references/slop-uiux-patterns.md, references/slop-code-patterns.md, references/layouts.md, references/typography.md, references/components.md, references/animation.md, references/design-systems.md, references/charts.md, references/dashboards.md, references/awards-craft.md, references/research.md"
---

# AntiSlopUI — one skill, one contract

Produce UI that a discerning designer **cannot** instantly flag as machine-generated.
Everything this skill needs ships in this repository: the ban filter is this file,
the pattern library and the catalogues live in `references/`, and the research tool
lives in `ui-ux-pro-max/`.

> If you could swap the logo with a competitor and nobody would notice — it's slop.

## Delivery gate (read now, apply before shipping)

Before delivery, report `PASS`, `FAIL`, `N-A`, or `UNVERIFIED` plus an evidence
pointer for every audit item below. `N-A` is allowed only when the component — or
the capability it audits — does not exist on the page. `UNVERIFIED` means you could
not measure it; never mark an unmeasured item PASS, and an `UNVERIFIED` **P0** blocks delivery exactly like a
`FAIL` until you verify it.

**Any P0 failure blocks delivery, as does 3+ P0/HIGH tells. MEDIUM and LOW tells are
recorded, not blocking.** `WARN-BRAND-SWAP` is a warning, never a block.

## Deterministic terms

A **tell** is one catalogue row in `references/slop-uiux-patterns.md` sections 1–10, or one
of the code-level findings the audit lists below (five a11y/form HIGH items and seven code P0
items, the HIGH set being focus states, form labels, alt text, colour-only indicators and
validation states (F1 in the code catalogue)). Severity is exactly `P0`, `HIGH`, `MEDIUM` or `LOW`; the vocabulary is closed.

Count **per element**: when one element matches several rows (a 3-card grid with emoji icons
is both K1 and I1), count it once at the **higher** severity. Rows that describe the whole
page count **once for the page**; today that is L1, L2, L3, L4, L5, L7, L8, L10, L11, M16, M17,
M20, MO1, MO3, MO13, C10, FO1, and any other row whose tell is a property of the page rather than
of one element. N4 and H8 are
**JUDGEMENT** — record them, never count them. Absence rows do not match unless the page
claims the capability; otherwise they are `N-A`.

Banned purple, indigo or violet counts as "real brand" only when the value appears in
user-supplied brand assets — a logo file, existing CSS tokens, or a brand PDF. Otherwise
it is a violation. Record exceptions exactly as `OVERRIDE: <from> → <to> [<reason>]`,
where `<reason>` is `brand: <source>`, `craft tier §5`, `domain table`, `display table`,
`catalog <ID>`, or `prose`. A gate id is not a reason: gates are prohibitions, not
justifications.

Never invent a product name, customer name, metric, logo or testimonial. If the user
supplied a name, use it exactly; otherwise write `Your product` in the wordmark, label
it once on the page, and record `NO-BRAND: user supplied no name` — a page that records `NO-BRAND` is `N-A` on
the logo-swap item. Unknown proof is omitted and recorded `NO-PROOF: user supplied none`;
invention is P0. Placeholder content — including representative numbers — is allowed only when visibly
labelled and structurally distinct (`<figcaption>Sample data — replace before launch</figcaption>`
or `data-sample="true"`); `[placeholder]`, lorem ipsum and TODO stay banned. A labelled
sample is not an invented metric.

## Hard gates

| ID | Banned | Compliant default | Severity |
|---|---|---|---|
| H2 / T2 | Gradient-text headline (one defect, two catalogue rows) | Solid, high-contrast headline | P0 |
| C1 | Purple/indigo/violet primary accent without a supplied brand asset | A non-purple brand hue from the domain table | P0 |
| C2 | Canonical purple/indigo or blue/cyan gradient combinations | Flat colour, or one intentional compliant gradient per page | P0 |
| C7 | Low-contrast body text | 4.5:1 body, 3:1 large/UI, checked | P0 |
| K6 | Purple left-border card accent | Remove; left borders only for semantic alerts | P0 |
| MO10 | Missing `prefers-reduced-motion` support | Gate animation; render static under reduced motion | P0 |
| T1 | Inter/Geist for display and body without a second face | Distinctive display face + body | HIGH |
| K1 | Identical 3-col feature grid (icon-in-rounded-square + title + blurb) | Vary size/structure, or use a list/table | HIGH |
| K3 | Any scaling hover (`hover:scale-*`) | Shadow/border/colour feedback | HIGH |
| I1 | Emoji as functional icons | One SVG icon set | HIGH |
| B3 | Pill buttons everywhere | `rounded-md`/`rounded-lg`; pills only when semantic | HIGH |
| N1 | Floating glassmorphic navbar | Fixed solid navbar with a border | HIGH |

Also enforced from the catalog: mono/technical faces as display (§3), indigo-950 or
violet-50 tints as text or background (no dedicated row: treat them as C1 for accents and
C7 for text contrast, and record the substitution from `references/research.md`), typewriter-style copy animation (MO12) and
multi-layer parallax (MO8), both in §8 MOTION. These are catalog rows, not a
second list.

For the full catalogue: `cd <skill-dir> && grep -nE '^## |^\| ?[A-Z]{1,3}[0-9]+' references/slop-uiux-patterns.md`.

## The five axes

| Axis | Banned default | Required action |
|---|---|---|
| Colour | Purple/indigo accent, purple or blue-cyan default gradients | Domain hue from the table below; document overrides |
| Type | Inter everywhere, gradient headlines, Playfair + Inter | Category display face; solid headline; 2–3 weights |
| Layout | Centred sameness, repetitive 3-col grids, one container width | Vary structure and emphasis by content |
| Copy | Hype, generic CTAs, invented proof | Specific copy; omit unknown proof, record `NO-PROOF` |
| Motion | Gratuitous motion, missing reduced-motion | Follow the motion table below |

## Motion table

| Motion class | Duration / behaviour |
|---|---|
| Hover | 100–150ms |
| Entrances and exits | 150–250ms |
| Page/route transitions | ≤300ms |
| Craft-tier exception | ≤400ms ONLY with `OVERRIDE: … [craft tier §5]` |
| Ambient | Maximum 1, pause on hover/focus, static under `prefers-reduced-motion` |

Hover examples use 150ms; entrance and exit examples use 200ms. Outside this table,
point here instead of restating durations.

## Text measure

`max-w-3xl` for prose containers, `max-w-prose` for paragraphs, `max-w-5xl` for wide
single-column blocks, `max-w-6xl` for grids. A column in a two-column hero split may use
`max-w-2xl`; the 65ch paragraph rule applies to paragraphs inside it, not to the column.
A grid section may repeat `max-w-6xl`; what is banned is every section sharing one
container, which flattens the page into a single column.

## Palette and type: who decides

Colour is decided in this order, and the first match wins:

1. **User-supplied brand assets** — logo file, existing CSS tokens, brand PDF. Use the
   value found there and record `[brand: <source>]`.
2. **This table by product domain** — every value is contrast-certified for white text:

| Product domain | Brand hue |
|---|---|
| Money, invoicing, ledger, productivity | `#0F766E` deep teal |
| Health, clinical, wellness, care | `#0E7490` cyan-teal |
| Safety, urgency, logistics, alerts | `#B45309` clay |
| Agriculture, environment, sustainability | `#3F6212` moss |
| Enterprise, legal, infrastructure, docs | `#334155` slate |
| Food, hospitality, craft, heritage | `#7F1D1D` oxblood |
| Developer tooling, data, AI infrastructure | `#4D7C0F` olive |
| Anything not listed | `#0F766E` deep teal |

If several rows match, the row earliest in the table wins. Do not derive a hue by feel.
3. **Research output** — `--design-system` colours after the post-filter. A proposal,
   never an authority: step 2 already decided the hue, so research supplies systems and
   accents only.

`references/` supplies structure, spacing, components and colour *systems* (tokens,
chart palettes, OKLCH recipes). It does not choose your brand hue.

Display face is chosen by product category, not taste:

| Product category | Display face | Body |
|---|---|---|
| Editorial, luxury, culture, portfolio, beauty | Fraunces | Inter or the palette's body face |
| Software, developer tool, data product | Bricolage Grotesque | Inter or the palette's body face |
| Neutral B2B, enterprise, docs | Bricolage Grotesque | Inter or the palette's body face |
| Playful, consumer, education, gaming, e-commerce | Cabinet Grotesk | Inter or the palette's body face |

Two families maximum. Default body is **Inter 400/500**; any single non-display sans is
legal (the generator's body face counts), and Inter is legal only when a different display
face is present. If the category is genuinely ambiguous, use
Bricolage Grotesque and say why. If the display face is not loadable, use Bricolage
Grotesque rather than a vendor face.

## Contrast

Compute relative luminance, or use these verified pairs: `#0F172A` on `#F8FAFC` = 17.1:1 ·
`#475569` on `#F8FAFC` = 7.2:1 · `#FFFFFF` on `#0F766E` = 5.5:1 · `#FFFFFF` on `#B45309` = 5.0:1.
Ship body text at 4.5:1 or better, large text and UI at 3:1 or better. If you cannot
compute a custom pair, move the value until it matches one of these.

## Authored defaults (when research output is unavailable)

- Surfaces: `#F8FAFC` page, `#FFFFFF` card, border `#E2E8F0`, text `#0F172A`, muted `#475569`.
- Type: one display face ≠ Inter, body Inter 400/500, two families, three weights, 1.25 scale.
- Layout: prose `max-w-3xl`, grids `max-w-6xl`, section padding `py-32`/`py-16`/`py-12`.
- Radius scale: badges and avatars `rounded-full` (or `rounded-sm` for rectangular badges),
  inputs and buttons `rounded-md`, cards and tables `rounded-lg`, modals and drawers
  `rounded-xl`, sections and banners `rounded-none` or `rounded-lg` to match their card,
  accordion rows inherit the card radius, tooltips `rounded-md`. No other values.
- Interaction: `cursor-pointer` on anything clickable, visible `focus-visible` ring, hover
  feedback by colour or shadow only.
- Responsive: verify 375 / 768 / 1024 / 1440 with no horizontal scroll.

## Which reference to open

| You need | Open |
|---|---|
| Tell catalogues and code-level tells | `references/slop-uiux-patterns.md`, `references/slop-code-patterns.md` |
| Page/app skeleton, grid, responsive structure | `references/layouts.md` |
| Type scale, pairings, fluid type | `references/typography.md` |
| Cards, buttons, forms, nav, data display | `references/components.md` |
| Overlays, feedback, motion recipes | `references/animation.md` |
| Library choice, design tokens | `references/design-systems.md` |
| Charts, KPI cards, data visualisation | `references/charts.md` |
| Admin dashboard shell, tables, filters | `references/dashboards.md` |
| Award-grade craft tier (opt-in) | `references/awards-craft.md` |
| Industry evidence from the CSV tool | `references/research.md` |

Anti-monotony rules: never repeat the same section anatomy consecutively; vary container
widths by content; vary section padding (hero `py-32`, features `py-16`, CTA `py-12`);
one dominant element per section; break the rhythm every 2–3 sections; mix grid
structures; at least two deliberate asymmetric moments per page.

## Reference budget

Per task: this file plus **sections**, never whole reference files. A whole reference is
6–36 KB (2–10k tokens). Only the six smallest would fit beside this file and the catalogue;
the four largest would not. None may be read whole. A section runs from a few hundred tokens to about 1,300, with the
dashboard and code catalogues reaching roughly 2,100.

Ceiling: **70 KB of skill text per task** (≈20k real tokens; 3.5 bytes ≈ 1 token, so bytes
÷ 3.5 is the token estimate). Self-check with a shell: `wc -c` what you have loaded, add
it up, and compare with 70,000. To measure a section rather than a file:

```bash
s=$(grep -nE '^#{1,2} ' references/layouts.md | grep -i 'HERO VARIANTS' | cut -d: -f1)
e=$(grep -nE '^#{1,2} ' references/layouts.md | awk -F: -v s="$s" '$1>s{print $1; exit}')
sed -n "${s},$((e-1))p" references/layouts.md | wc -c
```

Without a shell, use the structural rule: this file plus the tell catalogue plus at most two
sections from one library file.

When a number appears here and in a reference, **this file wins**; reference values are
examples at their own scale. The `## Contents` block in a reference is a summary of its sections — `grep` returns the
same names with line numbers, so grep is the step that saves round-trips:

```bash
cd <skill-dir> && grep -nE '^#{1,2} ' references/layouts.md   # names + line numbers
sed -n 'START,ENDp' references/layouts.md                     # END = next match − 1
```

Some references carry their own checklists (`references/dashboards.md` 15 principles,
`references/charts.md` a 15-point scan, `references/research.md` a post-filter). Run them as
guidance for that artefact; they never add blocking items and never change the tell set.
Where a reference checklist disagrees with this audit, this audit wins.

## Craft tier (opt-in)

`references/awards-craft.md` is the only file that may raise the craft ceiling, and only
when the user explicitly asks for premium, award-grade, "wow", studio or launch work. It
carries a scored rubric (Design 40 · Usability 30 · Creativity 20 · Content 10), hard
performance and accessibility gates that deny the tier on failure, and a cost table for
every craft pattern. It never buys a ban. Its two relaxations are declared `OVERRIDE: … [craft tier §5]`: a 400ms hero choreography, and one viewport-wide ambient animation. Do not load it for dashboards, docs, checkout or forms.

## Research tool

`references/research.md` documents the CSV generator (commands, domains, stacks, persist
pattern, post-filter, determinism, no-shell path). The script path is
`ui-ux-pro-max/scripts/search.py` relative to this skill; it resolves its data directory
relative to itself, so an absolute or `<skill-dir>`-prefixed path works from any cwd.

If the shell is unavailable, do not read the CSVs by hand: build from the authored
defaults above, and state that the research step was unavailable.

## Pre-Delivery Audit

Report `PASS` / `FAIL` / `N-A` / `UNVERIFIED` with an evidence pointer per item.

**Colour and type**
- [ ] No banned purple/indigo without a supplied brand asset; exceptions recorded as `OVERRIDE:` with source.
- [ ] No gradient text; at most one intentional gradient element per page.
- [ ] Display face is not Inter/Geist; ≤3 weights; modular scale.
- [ ] Body text passes 4.5:1 (and 3:1 for large/UI). If the user supplies a dark palette, verify both; otherwise ship light and state that choice.

**Layout and components**
- [ ] Container widths and section padding vary by content; at least one full-bleed break.
- [ ] No identical 3-col grid repeated; one dominant element per section.
- [ ] Radius is a scale, not one value.
- [ ] No scaling hover (`hover:scale-*`); no glass except ONE surface per page over imagery at `bg-white/80`+ with `@supports`; no emoji icons.

**Copy**
- [ ] No hype, no generic CTAs, no `[placeholder]` / lorem / TODO.
- [ ] Every metric is real or visibly labelled; unknown proof omitted with `NO-PROOF`.
- [ ] Sample content visibly labelled.

**Code-level findings (7 P0)**
- [ ] (P0) Semantic landmarks: one `<main>`, `<nav>`, `<header>`, `<footer>`; page has `lang`.
- [ ] (P0) Real controls: `<button>`/`<a>`, never `<div onClick>` or `<span role="button">`.
- [ ] (P0) Overlays are `<dialog>` (or a focus-trapped equivalent) and close on Escape.
- [ ] (P0) Custom inputs follow the ARIA pattern: combobox/select exposes `role="listbox"` +
  `aria-expanded` and is keyboard operable.
- [ ] (P0) Icon-only controls carry `aria-label`.
- [ ] (P0) No secrets, keys or tokens in client code, and no unsanitized HTML injection
  (`dangerouslySetInnerHTML`, `innerHTML`, `v-html`).
- [ ] (P0) Data fetching follows the stack's idiom — server component, loader, or query cache —
  not a client-side request waterfall in an effect.

**Motion and accessibility findings (5 HIGH)**
- [ ] (HIGH) Images carry `alt`.
- [ ] (HIGH) Focus states are visible.
- [ ] (HIGH) Form controls carry labels.
- [ ] (HIGH) Forms expose validation states.
- [ ] (HIGH) Colour is never the only state indicator.

**Cross-cutting checks (counted through the catalogue rows named)**

- [ ] Motion inside the canonical table; colour/shadow hovers are 100–150ms; any spatial motion
  uses `transform`/`opacity` only; reduced-motion renders static (MO10, MO11).
- [ ] Body text and UI meet the contrast thresholds above (C7).

**Gestalt**
- [ ] Counted catalog tells per element; **any P0 tell or 3+ P0/HIGH tells = block**.
- [ ] Could a competitor swap the logo without notice? If yes, record `WARN-BRAND-SWAP` and fix it if a name exists — never a blocking FAIL.

## References

- `references/slop-uiux-patterns.md` — 126 tell rows, TELL → WHY-SLOP → FIX → SEVERITY.
- `references/slop-code-patterns.md` — React/TSX/a11y code-level tells.
- `references/layouts.md`, `typography.md`, `components.md`, `animation.md`,
  `design-systems.md`, `charts.md`, `dashboards.md` — the positive pattern library.
- `references/awards-craft.md` — opt-in craft tier with hard gates.
- `references/research.md` — CSV generator workflow, post-filter, determinism.

## Output expectations

The result must read as intentional, branded, content-aware, accessible and
production-ready. Every spacing value, colour, font, grid and animation must be
defensible with a content-specific reason. If you cannot explain why a choice was made,
it is slop — remove or replace it.
