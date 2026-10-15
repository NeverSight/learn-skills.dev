---
name: retro-print
description: |
  Genre pack: Risograph / 70s–80s print revival. Warm paper, pigment inks (one red + one blue maximum), halftone dot textures, misregistered ink offsets, rubber-stamp details, poster typography. Use for zines, events, agencies, food/drink brands, music, and anything wanting a warm analog voice. Stack on the design-taste core skill.
triggers:
  - "retro"
  - "risograph"
  - "riso"
  - "print"
  - "zine"
  - "70s"
  - "80s"
  - "vintage print"
  - "analog"
  - "poster"
---

# retro-print

> One identity: **a risograph poster that just came off the drum — straight print, honest misregistration.**

## 1. PALETTE (Fixed)

- Paper: `#F4EDDE` (warm print stock). Alternate panel: `#EBE2CF` (slightly pulled).
- Ink: `#21201C` (print black).
- Inks — exactly two, at most: riso red `#E4572E` and riso blue `#355E8C`. If the brief needs one, use red. If two, red + blue. Never a third.
- NO gradients, NO antialiased-looking shadows (no `box-shadow` blurs), NO pure white backgrounds, NO screenshots-in-browser.

## 2. TYPOGRAPHY (Fixed)

- **Display:** a single-weight condensed/display poster face (Anton, Archivo Narrow 800, or the system's heaviest), uppercase, `clamp(2.8rem, 8vw, 7rem)`, tight leading 0.95–1.0. Poster volume, not editorial whisper.
- **Body:** a quiet serif (`Newsreader`, Georgia) at 16–18px, 1.6–1.7 — the print contrast to the shouting display.
- **Labels/metadata:** monospaced caps (`IBM Plex Mono`), `letter-spacing: 0.1em`, 10–12px, ink or red.
- **The signature:** misregistration offsets — display text with `text-shadow: 2px 2px 0 var(--riso-red)` (or blue). Apply to 2–3 headings max, never body. One offset direction per page.

## 3. TEXTURE & DETAIL (The Craft That Sells It)

- **Halftone:** dot fields via `repeating-radial-gradient` (`radial-gradient(var(--ink) 1.2px, transparent 1.3px)` at 8–12px grid), capped at ~2 panels per page. Inverse (paper dots on ink field) counts as one.
- **Rough edges:** elements may sit flush to viewport edges, section separators can be full-bleed ink rules — print bleed, not web padding.
- **Stamps:** mono caps in a circle or pill with a dashed ink border, rotated 1–3°, **max two per page** (e.g., one in the nav, one in an attribution). Stamp = dashed, always.
- **Halftone numbers:** big display numerals (01, 02) in red with blue offset.
- No emoji. No linear icons — typographic markers (✳, →, ◆) or drawn dot-grid marks only.

## 4. COMPOSITION (Fixed)

- **Poster grid:** asymmetric columns (5/7 or 4/8), one giant element per viewport, rules (1–2px ink) doing the separation instead of cards.
- **Hero:** kicker stamp → giant display headline (offset applied) → body serif block right-aligned in 4/12 → two-line mono colophon under ("SKITTIE VOL. 02 — PRINTED IN FIVE COLORS").
- **Features:** numbered print index — big figure + serif name + body description on hairline-divided rows.
- **Pricing:** three poster cards — paper / ink field (paper type) / paper + red; 2px ink borders, square corners. The ink card is the featured.
- Photographs (if any): duotone — grayscale → `sepia` → `hue-rotate` toward ink, contrast 1.15, with a 1.5px ink frame. Grain via faint noise if available.

## 5. MOTION (Almost None — Prints Don't Move)

- One entrance: sections reveal with a 200ms snap-up (6px), like paper landing.
- Hover: link color flips to red, 100ms. Nothing drifts, nothing rolls, no parallax — the illusion is physical print.
- QR/archive jokes allowed in copy, not in motion.

## 6. CHECKLIST (Fail the Page If…)

- [ ] More than two ink colors (red + blue max) in use.
- [ ] Any gradient or blurred shadow.
- [ ] Any pure white background.
- [ ] Any emoji.
- [ ] Display type not uppercase or smaller than ~2.8rem.
- [ ] Body text set in a sans.
- [ ] No texture anywhere (no halftone, no misregistration, no stamp) — that's the identity.
- [ ] Misregistration offset applied to body text.