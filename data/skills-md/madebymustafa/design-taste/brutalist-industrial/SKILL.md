---
name: brutalist-industrial
description: |
  Genre pack: raw mechanical interface — Swiss typographic print fused with military/industrial terminal aesthetics. Rigid visible grids, extreme type-scale contrast, utilitarian color (paper, ink, one signal color), hard edges, zero decoration. Use for data-heavy platforms, developer tools, portfolios, studios, or any brief wanting to feel like a declassified blueprint. Stack on the design-taste core skill.
triggers:
  - "brutalist"
  - "industrial"
  - "blueprint"
  - "terminal aesthetic"
  - "developer tool landing page"
  - "raw design"
  - "technical design"
---

# brutalist-industrial

> One identity: **a declassified blueprint for a machine you haven't been cleared to see.**

## 1. PALETTE (Fixed)

- Ground: `#F2F1EC` (aged paper). Dark ground variant: `#1B1B18`.
- Ink: `#141414` (near-black, neutral).
- Signal color — exactly one: safety orange `#E8540B`, industrial yellow `#E3B23C`, or technical blue `#2B5FA8`. Pick by brief; then it never changes.
- Secondary ink for metadata: `#6E6C64`.
- Rules/borders: `#141414` full opacity — visible, 1px, everywhere.
- No gradients, no shadows, no glows. Depth comes from offset solid blocks and rules.

## 2. TYPOGRAPHY (Fixed)

- **Display:** heavy grotesk (Archivo, Archivo Black, or Arial Black fallback), weight 700–900, uppercase, tight tracking (−0.01em), huge scale `clamp(2.6rem, 7vw, 6rem)`.
- **Body:** same family at 400, 15–17px, 1.5–1.6.
- **Labels/metadata:** monospaced (`IBM Plex Mono`, `ui-monospace`), uppercase, `letter-spacing: 0.08–0.12em`, 10–12px. Section coordinates ("01 / 04"), spec numbers ("GS-114"), and status tags all use mono.
- NEVER italic, never serif, never lowercase-as-brand (except deliberate design-read exception).

## 3. COMPOSITION (Fixed)

- **Visible grid discipline:** hairline rules (1px solid ink) everywhere — section separators, column dividers, table rows. The grid IS the design.
- **Header block:** left-aligned wordmark + mono coordinates right ("N-01 / REV 3"); top and bottom 1px rules closing the masthead.
- **Hero:** giant condensed uppercase headline spanning full width, kicker line in mono with a signal-color marker (▪ or ▸), body right-blocked in a 5/12 column, exit line at the bottom: mono small print + signal CTA box.
- **Data as structure:** features/pricing rendered as indexed tables or ledger rows with rules — never rounded cards. If cards: square, 1px ink border, no shadow. Selected/featured row gets a signal-color fill (`#E8540B` with ink text).
- Buttons: rectangles, 1–2px ink borders, hard offset shadow `4px 4px 0 ink` (or signal), press = offset removed.

## 4. CONTENT TREATMENT

- No emoji. No icons beyond typographic markers (▪, ▸, ■, →) and drawn square/cross glyphs.
- Numbers are the decoration: every section gets a mono index number; metrics typeset in mono columns like an instrument panel.
- Photography: none by default. Full-bleed halftone/greyscale image with a 1px ink frame only if the read demands it.
- CTAs: one solid CTA (signal fill or ink), plus a plain mono text link. Never two equal buttons.

## 5. MOTION (Mechanical, Not Pretty)

- Instant or 80–150ms snaps — machine response, not choreography.
- Hover: invert (ink→ground), 1px border flip to signal. No float, no wobble, no parallax.
- One allowed entrance: sections reveal via clip/translate up 8px, 150ms.

## 6. CHECKLIST (Fail the page if…)

- [ ] Any border-radius above 2px on a major surface.
- [ ] Any gradient, glow, drop-shadow, or blur.
- [ ] More than one signal color in use.
- [ ] Any emoji or whimsical iconography.
- [ ] Display type not uppercase or not heavy.
- [ ] Any italic or serif in a label position.
- [ ] The grid is invisible (no rules, no alignment evidence).
- [ ] A standard rounded-card row of three appears.