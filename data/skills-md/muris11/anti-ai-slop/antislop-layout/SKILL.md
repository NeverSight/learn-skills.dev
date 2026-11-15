---
name: antislop-layout
description: "Layout and composition rules: hero, sections, symmetry, grids, spacing rhythm. Map to antislop-master section C. Use when building or auditing page structure and layout."
allowed-tools: Read Write Edit Glob Grep
---
# antislop-layout

> Layout and composition rules for anti-ai-slop. Catalog codes are **C-1 … C-12** in `antislop-master`.
>
> The job is not "make it symmetrical" — it is *make the page tell the reader where to look and what matters.*

---

## The one rule that beats all others

**Layout must express content hierarchy.** If the layout would look identical with the real content swapped for lorem ipsum — and still be "fine" — the layout is a template, not a composition.

Run the **swap test** on any page that feels generic: replace every heading with a different, real one and re-read. If nothing pushes back, rebuild.

---

## Hero patterns

- **Avoid** the trapped formula: centered headline → subtitle → **two** CTAs → **three** cards. (C-1)
- **Prefer** a hero built around the single primary action — one CTA that matters, or a layout that shows the product working (a real screenshot, an interaction, the tool mid-use) instead of a headline + "Learn more".
- **Alternatives** to the centered stack:
  - **Asymmetric hero** — a bold headline left, the product live right.
  - **Command center** — the interface itself IS the hero.
  - **Editorial split** — a strong image/sidebar with the message beside it.
  - **Product storyboard** — a strip that walks through how it's used.
- A **demo without a product** (fake terminal, floating UI mock in a blob) is the loudest tell. (see C-1, A-11)

## Section rhythm

- **Avoid** every section being the same (title → 3 bullets → CTA), repeated 4×. (C-2)
- **Vary** width, alignment, background, and column count so sections change pace — but keep the change purposeful, not random.
- **Break symmetry deliberately.** If the whole page is left-of-center or centered, add one asymmetric moment to anchor attention. (C-3)

## Grids & cards

- **Avoid** card grid as the universal content box. (C-5)
- **Bento grid only when** content genuinely has mixed sizes — never "because it's current". (C-4)
- **Vary card weight**: a primary card can be larger than a secondary one if the content is more important. Identical width for unequal content is a tell. (C-7)

## Spacing rhythm

- Use one scale (e.g. 4/8/12/16/24/32/48/64). **No ad-hoc values.** (I-2)
- Intentional whitespace is **structural** (it groups, separates, directs). Leftover whitespace is *surplus*. (C-11)
- If two unrelated elements share the same gap as two related ones, the rhythm is broken.

## Section hand-offs

- A CTA at the end is not mandatory. Put a clear **next step** where the reader is ready for it, not always at the bottom. (C-8)
- **FAQ only if there are real questions** — product-specific, not template filler. (C-9)

---

## Audit checklist (Quick / Full / Deep)

- [ ] Swap test passes (content changes compose layout). (C-1, C-2)
- [ ] One clear focal point per screen. (C-3)
- [ ] Grids follow content, not convenience. (C-4, C-5, C-7)
- [ ] Spacing uses a real scale. (I-2)
- [ ] Sections vary in rhythm for a reason. (C-2)
- [ ] Whitespace is structural, not surplus. (C-11)

If any is **no**, it is a finding. Cite the code from `antislop-master` and one honest reason.
