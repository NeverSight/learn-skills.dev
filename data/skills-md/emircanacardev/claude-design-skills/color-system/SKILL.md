---
name: color-system
description: Builds complete UI color systems with brand ramps from 50 to 950 generated in OKLCH for even lightness steps, a tinted neutral ramp, semantic success, warning, danger and info colors, usage roles, contrast-verified text and background pairs, and light and dark mappings with 60-30-10 guidance. Use when asked to create a palette, generate shades from a brand color, pick UI colors or fix inconsistent colors. Not for token file structure; use design-tokens.
---

# Color System

Produces a palette that works in a product, not just in a swatch: ramps with predictable lightness, roles that say where each color goes, and a pair table proving that every text and UI combination passes contrast in light and dark.

## When to use
- "Generate a palette from this brand color" or "give me shades 50–950"
- The codebase has a dozen near-identical grays and blues
- Adding success, warning, error and info states
- A brand color fails contrast as text or as a button background
- Preparing colors for a dark theme (then continue with dark-mode)

## Workflow
1. Gather the seed: brand hex, or industry and adjectives if none exists, plus any existing scale (Tailwind or custom). Convert the seed to OKLCH and find the step whose target lightness is closest; the seed keeps its exact value at that step.
2. Build the brand ramp: 11 steps, constant hue, lightness from the target table, chroma peaking at 500–600 and tapering toward 50 and 950. Clamp every step into the sRGB gamut.
3. Build the neutral ramp on the same lightness targets, tinted toward the brand hue at chroma 0.005–0.015.
4. Build semantic ramps on the same targets: success hue ≈ 145–150, warning ≈ 70–85, danger ≈ 25–30, info ≈ 240–260 (OKLCH degrees). Shift any that collide with the brand hue.
5. Assign roles for light and dark: background, surface, text (primary, secondary, disabled), border (subtle, strong), accent (action, link, focus) and semantic (subtle bg, border, solid, text).
6. Compute WCAG 2 contrast for every pair that is actually used; fix failures by moving steps, not by inventing new colors.
7. Hand the result to design-tokens for export.

## Rules
**Ramps**
- Starting lightness targets (OKLCH L): 50 0.97 · 100 0.93 · 200 0.88 · 300 0.81 · 400 0.71 · 500 0.62 · 600 0.55 · 700 0.48 · 800 0.41 · 900 0.34 · 950 0.26. Neutral 950 may drop to 0.17–0.20 (about #0f0f0f–#141414) to serve as the dark background.
- Lightness strictly decreases; no two adjacent steps closer than 0.03 L.
- Keep hue within ±3° across the ramp, except yellows and oranges, which may drift about 10° toward orange in dark steps to avoid olive.
- Generate in OKLCH, not HSL: HSL 50% yellow and 50% blue differ wildly in perceived lightness.
- Do not build ramps by mixing with white or black in sRGB; it dulls chroma and spaces steps unevenly.

**Contrast**
- Text 4.5:1 minimum; large text (≥24px regular or ≥18.66px bold) 3:1; aim for ≥7:1 on primary body text.
- UI boundaries needed to identify a control (input borders, focus rings, icon-only buttons) and meaningful graphics: 3:1 against adjacent colors.
- On white, text usually needs OKLCH L ≤ ~0.56, so 600 and darker for text; always verify with the WCAG formula because hue shifts the result.
- Text on a solid accent: choose white or the 950 step by measured contrast. White on 500 fails for most greens, yellows, ambers and cyans.
- Color is never the only signal (WCAG 1.4.1): pair semantic color with an icon or text.

**Roles and proportion**
- 60-30-10: about 60% background and surfaces, 30% secondary neutrals and text, 10% accent. The accent marks actions and emphasis, not decoration.
- One accent hue for interaction. Semantic colors are reserved for status and never reused decoratively.
- Semantic set per status: subtle bg (50/100), border (200/300), solid (600), text on subtle bg (700/800).
- Dark mapping is not an inversion: background 950, surfaces 900/800, text 50–300, accents moved to 300–400 with 10–30% less chroma. Details in dark-mode.

## Output
- Ramp table per hue: step, oklch() value, hex fallback.
- CSS custom properties, e.g. --color-brand-600: oklch(0.55 0.2 260). OKLCH works in all evergreen browsers since 2023; add hex fallbacks only for legacy targets.
- Role table: role → light step → dark step.
- Contrast table: foreground, background, ratio, result (AA text, AA large, 3:1 UI).
- A short usage note showing where the 10% accent appears on a typical screen.

## Avoid
- Ramps built from sRGB tints and shades or equal HSL lightness steps
- Pure gray neutrals beside a saturated brand color
- Two accent hues competing for clicks
- Red or green used decoratively where they read as error or success
- Contrast reported for pairs that never occur while real pairs go unchecked
- Out-of-gamut OKLCH values with no clamping or fallback

## Final check
- [ ] Every ramp has 11 strictly descending lightness steps and the seed is preserved
- [ ] All values inside sRGB, or P3 with an sRGB fallback
- [ ] Every used text pair ≥4.5:1 (large text ≥3:1); UI boundaries ≥3:1
- [ ] Semantic states have a non-color cue
- [ ] Light and dark mappings both verified
- [ ] Accent coverage near 10% of the screen
