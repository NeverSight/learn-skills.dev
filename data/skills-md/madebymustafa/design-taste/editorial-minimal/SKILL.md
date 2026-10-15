---
name: editorial-minimal
description: |
  Genre pack: Swiss-editorial design identity. Warm paper background, ink-black type, one vermillion accent, oversized serif display with monospaced labels, hairline grids, indexed sections, strict asymmetric composition. Use when the brief asks for a calm, editorial, print-inspired, or quietly premium feel. Stack on top of the design-taste core skill.
triggers:
  - "editorial minimal"
  - "swiss design"
  - "print inspired"
  - "editorial landing page"
  - "quiet premium"
  - "newsletter aesthetic"
---

# editorial-minimal

> A single opinionated identity. When this pack is active, the entire page speaks one language: **a printed broadsheet that happens to be a website.**

## 1. PALETTE (Fixed)

- Paper background: `#F5F1EA` (warm off-white). Dark variant: `#EFEAE1`.
- Ink: `#1A1A18` (near-black, warm). Secondary ink: `#6B675E`.
- Accent: vermillion `#E34A2B` (or a deep red like `#C73E1D`). One per page.
- Hairlines: `rgba(26, 26, 24, 0.14)`.
- No other colors. No gradients anywhere. No dark-mode sections.

## 2. TYPOGRAPHY (Fixed)

- **Display:** a serif with character — Fraunces, Newsreader, or a strong system serif (Georgia, Charter). Sized `clamp(2.8rem, 7vw, 6.5rem)`, tight leading (0.98–1.08), normal weight — let the size carry the voice.
- **Labels / metadata:** monospaced (`IBM Plex Mono`, `SF Mono`, `ui-monospace`) or small caps, uppercase, letterspacing `0.10–0.15em`, 11–13px.
- **Body:** clean grotesk or the serif at 16–18px, 1.6–1.7 line-height, max-width 32–40em.
- Optional editorial flourish: italic serif pull-quotes, oversized drop figures ("01" at display size).

## 3. COMPOSITION (Fixed)

- **Asymmetric split heroes:** oversized type in a 7/12 column, a narrow index column (number + label) catching the remaining 5/12 on the right.
- **Indexed sections:** every section opens with a number ("01 — Approach") + a hairline top rule. The page should read as a table of contents.
- **Hairline everywhere:** 1px rules dividing columns, rows, and footer. Alignment must be exact — visible grid discipline.
- **Rows over cards:** features as an editorial index (numbered rows with rules between) rather than three rounded boxes. Where cards exist: square corners, paper-on-paper tonal panels (`#EFEAE1`), 1px ink hairline — never rounded-2xl, never shadow-first.
- Whitespace: hero padding ≥ 15vh, section gaps 96–160px.

## 4. CONTENT TREATMENT

- **No emoji icons.** Numbers, typographic marks (→, —, *), or a single drawn glyph if any.
- **Metrics are editorial:** present numbers as a mono typeset table with hairline rows — looks art-directed with zero assets.
- **No screenshots in browser chrome.** If a product visual is needed, use a tonal panel with type, or a clean full-bleed image with a hairline frame.
- **CTAs:** one solid vermillion square button + one text-only link in caps. Never two equal buttons.

## 5. MOTION (Almost None)

- One entrance: content fades/translates up 8–12px on scroll, 400ms, long ease.
- One micro-interaction: internal links underline on hover via background-size trick. No loops, no parallax orbs, no floating badges.

## 6. CHECKLIST (Fail the page if…)

- [ ] Any color beyond paper/ink/vermillion appears.
- [ ] Any rounded corner ≥ 6px on a major surface.
- [ ] Headline smaller than ~2.8rem or wider than ~22em.
- [ ] Body text column full-width.
- [ ] A centered, symmetrical hero.
- [ ] Emoji visible in the UI.

---

*When in doubt: what would a Swiss broadsheet do?*