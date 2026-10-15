---
name: taste-brand-identity
description: |
  Brand identity generation for agents: logo mark concepting, wordmark typography, lockups, clear space and minimum sizes, color application, favicon and og-image construction, and the one-page brand sheet. Use when asked to create a logo, identity, or brand assets for a product or site. Stack on the design-taste core skill.
triggers:
  - "logo"
  - "brand identity"
  - "wordmark"
  - "branding"
  - "favicon"
  - "brand sheet"
  - "logo design"
---

# taste-brand-identity

> A logo is a memory aid, not a drawing. This skill makes sure the identity survives a favicon and a billboard.

## 1. THE CONCEPT (Before Any Drawing)

1. **One idea, two words:** the mark reduces to a single association ("north + needle", "record + flower"). If you can't say it in two words, the concept isn't there yet.
2. **Literal is the last resort:** a generic icon of the product category (spark, rocket, chat bubble, gear) is what every other mark does. Reach for the abstract idea behind the product.
3. **Test at 16px before loving it:** the mark must read as a favicon first. If the concept needs 3 colors or fine detail to live, it fails the test.
4. **Two colors, hard ceiling:** one ink + one accent (or monochrome). A mark that needs its gradient to exist is not a mark.

## 2. WORDMARK TYPOGRAPHY (The Half Nobody Checks)

- Prefer modifying a strong existing face over inventing a font: letterspacing (`−0.03em`), case, a punctuation detail (`.` in "skittie.dev"), or one cutout/glyph swap.
- One typographic move per wordmark: track tight OR case change OR a single altered glyph. Two moves = a novelty logo.
- Test the wordmark in: caps, sentence case, and at 12px. If it doesn't survive small, tighten or accept a secondary lockup.
- Never letterspace lowercase (it breaks the word shape). Never stretch type (use the real condensed family).

## 3. THE LOCKUP (Mark + Wordmark, Formalized)

- Build on a construction grid: mark and wordmark on shared optical centers, clear space = height of the mark's smallest element (or 1/4 the mark width) on all sides.
- Three lockups, defined once: horizontal (mark + wordmark), stacked (mark above wordmark), compact (mark + short wordmark, for small spaces).
- Minimum sizes: mark ≥ 16px (favicon), ≥ 24px (in-app), ≥ 12px wordmark in compact lockups only.
- Banned lockup crimes: shadowed marks, gradient marks, outlined marks at small sizes, mark alone without the brand name on the first view.

## 4. COLOR APPLICATION

- The identity lives in ink + one accent (from the palette the page uses). A reversed (light-on-dark) variant is required — define both.
- Accent distribution: the accent is a signal (links, one button, active states, the logo's accent detail) — never a background fill.
- Provide a "monochrome only" fallback: every brand asset exists in 100% ink as a default.
- If the logo is a wordmark, its color rule is: same ink as headings — never a rainbow of per-section colors.

## 5. THE DELIVERABLE SET (Ship All of These)

1. **Primary lockup** — SVG, currentColor-compatible.
2. **Favicon** — 32px and 180px (apple-touch): the mark alone, centered, its own square tile.
3. **og-image** — 1200×630 canvas: mark or wordmark top-left or centered, one accent detail, clear space ≥ 80px margins; this is the most-viewed brand asset on the internet — never let it be a screenshot of the site.
4. **One-page brand sheet** — mark, wordmark, clear space diagram, min sizes, palette (with tokens), type pair, do/don't rows. This becomes the agent's own brand guideline file.

## 6. DO / DON'T (The Fast Filter)

| Do | Don't |
|---|---|
| Simplify until one element remains | Add a stroke, shadow, and gradient "for depth" |
| Test at 16px, 48px, 400px | Design only at 400px and pray |
| One typographic move | Custom-draw letters that fight the font |
| Provide the reversed variant | Ship only the version that works on white |
| Make the og-image deliberately | Let socials crop a screenshot |

## 7. CHECKLIST (Fail the Identity If…)

- [ ] The concept can't be stated in two words.
- [ ] More than two colors (plus neutrals).
- [ ] Any gradient, shadow, or outline needed for legibility.
- [ ] The mark at 16px is ambiguous with the competition's.
- [ ] No reversed variant exists.
- [ ] No clear-space/min-size rule defined.
- [ ] The og-image is missing or is a page screenshot.