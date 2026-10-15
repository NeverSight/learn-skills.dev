---
name: corporate-trust
description: |
  Genre pack: trust-first enterprise — white surfaces, one deep-blue accent, system typography, precise tables, zero decoration. For fintech, health, government, B2B platforms, and any audience whose decision rests on credibility. The identity IS the restraint: boring, on purpose, and honest. Stack on the design-taste core skill.
triggers:
  - "enterprise"
  - "corporate"
  - "fintech"
  - "b2b"
  - "trust"
  - "banking"
  - "healthcare"
  - "saas enterprise"
  - "government"
  - "professional"
---

# corporate-trust

> One identity: **an annual report with a skyline concrete building on the cover — bought because nothing surprised anyone.**

## 1. PALETTE (Fixed)

- Surfaces: pure white `#FFFFFF` for the page, `#F8FAFC` for panels, `#F1F5F9` for hover/inset.
- Ink: `#0F1722` (headings, primary), `#3B4657` (body), `#5B6777` (secondary/muted).
- Borders: `#E1E7EF` (1px). Stronger: `#C7D0DC`.
- Accent — exactly one: deep blue `#1F4FE0`. Used for: one primary button per viewport, links, active states, one emphasis mark. Nothing else.
- Success/danger exist as status colors with fixed token semantics (success green `#0E7F4B`, danger `#C0362C`) — status only, never decoration.
- NO gradients, NO hard shadows (soft `0 1px 2px rgba(15,23,34,0.06)` max — usually not needed), NO dark hero sections on marketing pages.

## 2. TYPOGRAPHY (Fixed)

- **Display:** system sans (the platform's default) at 500–600 weight, `clamp(1.8rem, 3.6vw, 2.8rem)`. Enterprise display is calm and specific — "integrations", not "transcend". NO display serifs, NO uppercase headers, NO oversized heroes (hard cap 2.8rem).
- **Body:** system stack, 15–16px, 1.6. Secondary text for descriptions.
- **Labels/metadata:** 12–13px, weight 500, `#5B6777`. Small caps optional, letterspacing ≤ 0.04em.
- NEVER: italic body, text under 12px in marketing surfaces, more than 3 weights on a page.

## 3. COMPOSITION (Fixed)

- **Conventional layouts are correct:** left-aligned hero, 12-col grid, features in 3-col or alternating 2-col rows, a comparison table, a data table, clear footers with legal links. The page should feel like the safe choice — because for this audience, it is.
- **Hero:** eyebrow (13px, accent or muted) → H1 (2.2–2.8rem) → one-line sub → one primary + one secondary button → a bordered product/metric panel. No hero theatrics, no claims without evidence nearby.
- **Evidence is the ornament:** logos (grayscale), metric callouts with source lines ("Based on 2,400 customers, 2025"), compliance chips (SOC 2, ISO 27001, GDPR — as text chips, not illustrations), customer quotes with title + company.
- **Tables are the signature component:** 1px `#E1E7EF` rules, 12px header caps left-aligned, 14px rows, zebra optional, hover row = `#F8FAFC`. Pricing as a bordered table beats pricing cards.
- Cards: 1px border, 8px radius, header + body + optional footer; hover = border darkens, no lift. Radius 6–8px everywhere; pills only for status tags.
- Footers are complete: product/company/resources/legal columns, address, copyright, compliance badges.

## 4. CONTENT TREATMENT

- Every claim gets a qualifier or source. "Best" becomes "Highest adoption in our category (G2, 2025)".
- Emoji banned. Icons: 1.5px stroke set (same family throughout), 20–24px, `#5B6777` at rest, accent at hover.
- Button language is concrete: "Start a trial", "Talk to sales", "Request a demo".
- Numbers: tabular figures, precise ("99.9% uptime SLA", "$29/month billed annually").

## 5. MOTION (Practically None)

- Hover states: background/border change only, 120–150ms, no movement.
- One entrance allowed: page-sequential section reveals (200ms, 6px, no stagger drama) — or nothing at all, which is also fine.
- No scroll animations beyond the above, no parallax, no autoplay carousels.

## 6. CHECKLIST (Fail the Page If…)

- [ ] Any decorative element that isn't earning trust (illustrations of people, gradient blobs).
- [ ] Any claim without a qualifier or source.
- [ ] Any text under 12px.
- [ ] More than one accent per viewport or any color carrying no meaning.
- [ ] Headline above ~2.8rem or any serif/uppercase display.
- [ ] Missing footer legal links or missing compliance signals on a regulated-audience page.
- [ ] Any table without proper alignment (numbers right, text left).
- [ ] A layout a procurement committee would squint at.