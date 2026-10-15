---
name: taste-color
description: |
  Color craft for agent-built interfaces: palette construction in OKLCH, the 60-30-10 discipline, one-accent rule, WCAG 2.2 contrast math, semantic tokens, color-blind-safe pairs, and dark mode mapping. Use whenever picking colors, building palettes, or reviewing UI color. Stack on the design-taste core skill.
triggers:
  - "color palette"
  - "brand colors"
  - "contrast"
  - "color system"
  - "dark mode"
  - "accent color"
---

# taste-color

> Color is the most emotional thing in the interface and the most abused by agents. The fix is structure: a tiny palette, used with discipline.

## 1. PALETTE ARCHITECTURE (60-30-10)

A complete interface palette has exactly:

- **60% neutrals** — the surfaces and text. Warm or cool, but one family. 2–4 surfaces (bg, panel, raised) + 3 text steps (primary/secondary/muted).
- **30% structure** — borders, hairlines, dividers: a tinted neutral, not a color.
- **10% accent** — ONE saturated color with a job: the primary CTA, links, active states, one data series. If a second accent exists, it has a distinct job (e.g., success green for status) and appears at <2% coverage.

More than three "meaningful" colors per viewport = the page has no message. The accent stops pointing at anything when it appears everywhere.

## 2. BUILDING RAMPS (OKLCH, Not RGB)

- Build all ramps in OKLCH (perceptually even lightness). Never interpolate between hex values blindly.
- Neutrals: 9–11 steps (50–950), chroma near 0. Accent: 9–11 steps, hue locked, chroma rising from low at 50 to full at 500–600, falling again at 900.
- The two most used values on a page: the 500–600 step of the accent (buttons) and the 50–100 step of the neutral (backgrounds).
- Convert to OKLCH in code where the stack allows; otherwise ship hex but compute from OKLCH.

## 3. CONTRAST (WCAG 2.2 — Exact Numbers)

| Element | Minimum ratio |
|---|---|
| Body text (normal) | 4.5:1 |
| Large text (≥24px, or ≥18.66px bold) | 3:1 |
| UI components (borders, icons, input edges) | 3:1 against adjacent |
| Focus indicator | 3:1 against adjacent, 2px minimum |

- Never eyeball it: compute with a contrast function (WCAG relative luminance formula) or a tool before shipping.
- A "premium" desaturated look is NOT an excuse for low contrast: desaturate the background, not the text.
- Text on accent buttons: white text needs accent ≤ ~4.6:1-luminance; check it. Dark text on light accent is often the right call (`#FFD100` yellow + ink text = correct; white on yellow = failure).
- Placeholder text ≤ 0.5 opacity is decorative: placeholder labels must not be the only label (floating labels, visible labels).

## 4. SEMANTIC MAPPING (Names Carry Jobs)

- `--color-surface`, `--color-surface-raised`, `--color-text`, `--color-text-muted`, `--color-border`, `--color-accent`, `--color-success`, `--color-danger`, `--color-warning` — with 3–4 steps of each where needed (e.g., `--color-danger-bg`, `--color-danger-border`, `--color-danger-text`).
- Meaning must be in the name: `--color-danger-text` not `--color-red-700`.
- Danger/success/warning exist for status ONLY — never as decoration.
- Dark mode = remap semantics (`--color-surface` flips), never a second palette of raw colors sprinkled into components.

## 5. COLOR-BLIND SAFETY (Default-Safe Pairs)

- Never encode information in red vs green alone. Add shape, position, pattern, or labels: `✓ / ✕`, ↑/↓, solid/dashed.
- Blue-violet is the safest hue (tritanopia & deuteranopia friendlier); orange is the strongest safe accent against neutrals.
- For data viz: use colorblind-safe categorical sets (e.g., Okabe-Ito) rather than rainbow defaults.

## 6. CHECKLIST (Fail the Page If…)

- [ ] Any two adjacent text/background pair under 4.5:1 for normal text.
- [ ] More than one accent color carrying meaning per viewport.
- [ ] A gradient where a flat color would do.
- [ ] Red and green as the only signal of success/failure.
- [ ] Any raw hex in a component instead of a token.
- [ ] White text on a yellow or pale accent.
- [ ] A "dark theme" that's actually just the same colors on a dark background (contrast must be recomputed).

*One accent, used twice per viewport, is a signal. The same accent everywhere is noise.*