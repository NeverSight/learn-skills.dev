---
name: quiet-luxury
description: |
  Genre pack: quiet luxury for premium consumer products, private banking, fashion, high-end SaaS, and personal brands. Ivory and deep ink, one metal or oxblood accent, serif display with italic emphasis, thin rules, generous whitespace, restrained motion. The expensive look comes from calm, not decoration. Stack on the design-taste core skill.
triggers:
  - "luxury"
  - "premium consumer"
  - "high end"
  - "fashion"
  - "private banking"
  - "expensive"
  - "refined"
  - "elegant"
---

# quiet-luxury

> One identity: **a private bank's annual report — the kind you hold differently.**

## 1. PALETTE (Fixed)

- Ground: ivory `#F7F2EA`. Alternate panel: `#EFE8DC`.
- Ink: deep espresso `#17130F` (near-black with warmth). Secondary: `#6E655A`.
- Accent — exactly one: antique brass `#9A7B4F`, oxblood `#742D2C`, or deep forest `#2E4436`. Pick by brand and never change it.
- Rules: `rgba(23, 19, 15, 0.18)` hairlines.
- No pure white backgrounds (reads "template"), no gradients, no glowing shadows. Shadows allowed only on floating elements, extremely soft (`blur ≥ 40px`, opacity ≤ 0.12).

## 2. TYPOGRAPHY (Fixed)

- **Display:** high-contrast serif (Cormorant, Canela-class, Playfair Display, or Garamond fallback), sizes `clamp(2.6rem, 6.5vw, 5.5rem)`, weight 400–500, tight leading 0.95–1.05. Italics are the allowed flourish — for one word per headline.
- **Body:** neutral sans (system sans-stack at 300–400 weight) 16–17px, 1.7 line-height, or the serif at 18px for editorial sections. Body text contrast is soft — ink-soft `#6E655A` — NEVER pure black.
- **Labels:** small caps or uppercase sans, `letter-spacing: 0.18–0.28em`, 10–11px, ink-soft.
- Numbers: serif numerals. Oldstyle features (0.75em, tabular where required).

## 3. COMPOSITION (Fixed)

- **Whitespace is the product.** Hero padding ≥ 18vh. Section gaps ≥ 140px. Never fill the viewport edge-to-edge with elements.
- **Asymmetric editorial columns:** headline in a 7/12 column, thin vertical rule, a narrow 3/12 index column (label stack: small caps items, hairline separators).
- **Thin rules, not boxes:** section separators are hairlines or empty space — never heavy borders or filled cards. Where a panel exists: ivory alternate `#EFE8DC`, no border, no radius beyond 2px.
- **Marquee-free typography blocks:** headline + one-line sub + one CTA. Restraint in compounds: three sections of calm beats eight sections of noise.
- Pricing: table-like list with hairline top rules, amounts in serif; the featured tier gets a thin accent rule above its name — not a filled box.

## 4. CONTENT TREATMENT

- No emoji. No gradient buttons. No stock "people shaking hands" photography.
- Imagery: full-bleed, muted, film-grade; art-directed crops; duotone-to-neutral tints. The image is a window, not decoration — letterbox it with generous margins rather than fill the whole width.
- Write like the brand: short sentences, no exclamation marks, no "🚀". Copy IS part of the design.
- CTA: one filled accent or ink button, square-ish (≤ 4px radius), one text link in small caps with a hairline underline. Never two equal buttons.

## 5. MOTION (Barely There)

- One scene entrance per section: 10–14px rise, 500–700ms, `cubic-bezier(0.22, 1, 0.36, 1)`.
- Hover: subtle — color shift to accent, opacity 0.85, 200ms. Nothing bounces, nothing wiggles, nothing spins.

## 6. CHECKLIST (Fail the page if…)

- [ ] Pure white `#FFFFFF` background in use.
- [ ] More than one accent color appears.
- [ ] Any sans-serif used for a display headline.
- [ ] Any emoji, confetti, or gradient.
- [ ] Heading not at least ~2.6rem or body color pure black.
- [ ] Less than ~140px between major sections.
- [ ] More than one filled CTA visible per viewport.
- [ ] Any card larger than ~2px radius without good reason.