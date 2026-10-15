---
name: japanese-minimal
description: |
  Genre pack: wabi-sabi minimalism — rice paper, sumi ink, one seal-red accent, a Japanese mincho serif, negative space as the design, one vertical text element allowed. Calm, deliberate, quiet-luxury's unpolished cousin. Use for studios, tea/food brands, wellness, personal sites, and any brief wanting meditative restraint. Stack on the design-taste core skill.
triggers:
  - "japanese"
  - "wabi sabi"
  - "zen"
  - "muji"
  - "minimal japanese"
  - "rice paper"
  - "sumi"
  - "east asian aesthetic"
---

# japanese-minimal

> One identity: **a room with one vase — the absence is the design.**

## 1. PALETTE (Fixed)

- Paper: `#F4F1EA` (rice paper warmth). Alternate: `#ECE8DF`.
- Ink: `#33302B` (sumi — soft, never pure black).
- Secondary: `#8A8378` (stone ash) for metadata and body-aside text.
- Seal accent — exactly one: `#B3392A` (hanko red). Used for: the seal mark, one underline, one stat, links. That's the entire accent budget.
- No pure white, no gradients, no colored fields (accent-colored fields banned — accent is a mark, not a surface).

## 2. TYPOGRAPHY (Fixed)

- **Display:** Japanese mincho serif (`Shippori Mincho`, or a serif with calligraphic rhythm), weight 400–600, `clamp(2.4rem, 6vw, 5rem)`, leading 1.15–1.3 (mincho breathes — no brutal leading).
- **Body:** a clean gothic (`Zen Kaku Gothic New` or system sans at 300–400) 15–16px, 1.8–2.0 line-height — generous.
- **Labels:** gothic caps or roman numerals, `letter-spacing: 0.18em`, 10–11px, stone ash.
- **One vertical moment:** a single `writing-mode: vertical-rl` text element (a label, a number, a name) per page — a worthwhile signature, never repeated.
- No italics (mincho has none in spirit), no fake bold, no all-caps display.

## 3. COMPOSITION (Fixed)

- **Ma (negative space) is the layout.** Hero padding ≥ 20vh. Sections ≥ 160px apart. If a section feels empty, that's correct — do not fill it.
- **Asymmetric stillness:** content in a 5/12–7/12 column, offset from center; one object per line of sight. Never center-symmetric stacks, never full-bleed busy screens.
- **Rules over boxes:** thin (1px) stone-ash rules for section dividers and index rows. Panels are paper-tone (`#ECE8DF`) with NO border — tone, not line.
- **Index as a list:** items on hairline rows: number / name / one-line note. Counts in mincho numerals.
- **The seal:** the hanko (a square or rounded-square red mark with one ideograph or monogram in white) appears exactly twice: once near the wordmark, once in the footer. It's a signature, not a logo badge.

## 4. CONTENT TREATMENT

- No emoji, no icon sets — typographic marks (・, —, ◦) or the seal itself.
- If photography: one or two images max, muted, grainy, generous margins (image smaller than the column, not filling it); `filter: saturate(0.7) contrast(0.95)`.
- Copy rhythm: short lines, imperatives in the form of observation ("The data asked quietly."), no exclamation marks, no superlatives ("best/greatest/revolutionary").
- CTA: one text link with a seal-red underline, or one solid sumi button (square). Never two equal CTAs.

## 5. MOTION (Single Acts)

- One fade/rise per section: 500–700ms, `cubic-bezier(0.22, 1, 0.36, 1)`, 8–10px.
- Hover: color shifts to seal red or opacity 0.75, 200ms. Nothing else exists. No parallax, no marquees, no loops.

## 6. CHECKLIST (Fail the Page If…)

- [ ] Any color besides paper, ink, ash, and seal red.
- [ ] Any accent-colored surface (accent is mark-only).
- [ ] Any border-radius above 2px or any box-shadow.
- [ ] Display set in a sans.
- [ ] Italic or uppercase display text.
- [ ] Center-symmetric hero or less than ~160px between sections.
- [ ] More than one vertical text element.
- [ ] Any element that doesn't appear to have been placed with a reason.