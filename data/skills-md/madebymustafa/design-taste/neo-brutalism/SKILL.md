---
name: neo-brutalism
description: |
  Genre pack: neo-brutalism for the web — loud consumer energy with hard discipline. Bright warm paper, ink-black 2.5px borders on everything, hard offset shadows, one dominant hot accent plus one supporting accent, chunky pills and stickers, playful copy. Use for consumer apps, agencies, crypto/tech novelty brands, and anything wanting maximum personality. Stack on the design-taste core skill.
triggers:
  - "neo brutalism"
  - "neobrutalism"
  - "brutalist web"
  - "loud design"
  - "hard shadow"
  - "sticker design"
  - "web brutalism"
---

# neo-brutalism

> One identity: **a skills poster for a product that is unapologetically online — loud, honest, square.**

## 1. PALETTE (Fixed)

- Paper: `#FFF8E7` (warm bright). Alternate field: `#FFEFC2` slightly deeper.
- Ink: `#0A0A0A` — used for ALL borders (2.5px), text, and shadows.
- Accents — exactly two: one dominant hot accent `#FF3878` (fields, big elements, the hero moment) + one supporting cool accent `#7CC6FE` (secondary fields, marks, the sticker on the hot field). Two is the ceiling; one is fine.
- NO gradients, NO soft/blurred shadows (`box-shadow` must be hard: `6px 6px 0 #0A0A0A` style), NO glass, NO dark-mode hero sections.

## 2. TYPOGRAPHY (Fixed)

- **Display:** a geometric grotesk at 700 (`Space Grotesk` 700, `Archivo` 800), `clamp(2.6rem, 7vw, 5.5rem)`, leading 0.98, tracking −0.02em. Sentence case is fine; never italic, never lowercase-everything-as-a-trend.
- **Body:** same family 400/500, 16–17px, 1.5.
- **Labels:** mono caps (`IBM Plex Mono`, `Space Mono`), 11px, `letter-spacing: 0.06em` — stamps, statuses, "NEW", version notes.
- One emphasis trick set: highlight words by placing them on a translucent hot/sky swatch, or underlining with a 6px ink rule. Pick one, use ≤ 3 times.

## 3. COMPOSITION (Fixed)

- **Everything is bordered.** Every card, button, panel, sticker, input: 2.5px solid ink border, square or pill (no 6–20px soft radius unless the component is a pill). Include the hard offset shadow on 60–70% of elevated elements; flat components (bordered, no shadow) keep the page from tipping into chaos.
- **Hero:** giant display + oversized pill CTA + a hot field panel with a sky sticker on it; the panel and sticker can rotate 1–2°. Rotation budget: 3 elements per page max.
- **Color distribution:** hot fields ≤ 2 per viewport, sky fields ≤ 2, everything else paper. Never two hot fields side by side.
- **Sections:** alternate paper and ink fields (ink sections: paper text). Full-bleed allowed. Pricing: three cards — paper / hot / paper; the hot card gets the biggest shadow.
- Buttons: min 56px height, 2.5px border, `6px 6px 0 #0A0A0A` shadow, pressed state = `translate(6px, 6px)` with shadow removed.

## 4. CONTENT TREATMENT

- No emoji. Decorative marks: ✳, ★, →, ◦, •• and simple drawn SVGs (thick strokes, flat fills, only the two accents + ink).
- Copy is part of the identity: direct, a little cocky, zero corporate filler ("You probably have better things to do than learn SQL" > "Streamline your analytics workflow").
- One exclamation mark per page, max. Compliments to the reader allowed ("You're doing great.").
- Price details formatted like packaging labels: mono, bordered, stamped "MOST POPULAR".

## 5. MOTION (Snappy, Visible, Short)

- Entrances: 150–250ms snap with 2px overshoot on the shadow (`cubic-bezier(0.34, 1.56, 0.64, 1)`), or straight 120ms pops. No long cinematic reveals.
- Hover: border color flips to an accent, or shadow grows 2px. Press: shadow collapses (see §3).
- Loops: absolutely none — no marquees, no bouncing arrows, no infinite wiggle. The page is confident, not nervous.

## 6. CHECKLIST (Fail the Page If…)

- [ ] Any element without a 2.5px ink border (backgrounds and images excepted).
- [ ] Any soft shadow or gradient.
- [ ] More than two accent colors.
- [ ] More than ~3 rotated elements.
- [ ] Any emoji.
- [ ] A "corporate voice" sentence anywhere in the copy.
- [ ] Two hot accent fields side by side.
- [ ] An element that looks like it came from a Tailwind template.