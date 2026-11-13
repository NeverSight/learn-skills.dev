---
name: ux-layout-spacing-grids
description: Lay out a screen with disciplined spacing, sizing, and grids — every value on one base unit (8px/4px scale), content aligned to a grid, proximity and whitespace doing the grouping, and space establishing visual hierarchy. Replaces arbitrary pixel values and ad-hoc alignment with a system. Also carries the spatial visual-hierarchy/alignment/composition fundamentals. Trigger when asked to design or critique a layout, set spacing/padding/margins, build a spacing scale or design tokens, choose or apply a grid/columns, fix inconsistent spacing or alignment, or establish visual hierarchy through space and position.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Layout, Spacing & Grids Skill

## How this skill behaves (read first)

This is a **generative** foundation skill. Layout is where an AI assistant's output is quietly amateurish: Claude reaches for **arbitrary spacing** (13px here, 27px there), pads things by eyeball, mixes alignments, drops content onto the canvas with **no grid**, and gives every element the same visual weight so nothing reads as more important. The fixes are systematic, not cosmetic — a base unit, a scale, a grid, consistent alignment, and space used deliberately to group and to rank.

So this skill gates:

1. **Establish context** — platform/density, content type, and whether the layout must be responsive (these set the base unit, the grid type, and the column model).
2. **Apply the always-true core** — one base unit and a spacing/sizing scale, align to a grid, let proximity and whitespace group, and use space to build hierarchy.
3. **Surface the context-dependent decisions** (base unit, grid type, column model, sizing approach, golden-ratio/rule-of-thirds, token layer, grid-breaking) with trade-offs; let the user choose.

Then it **hands off to `ux-aesthetics-audit`** (the composition/spacing/hierarchy review) and **`ux-accessibility-audit`** (touch targets, text scaling, reflow), plus **`ux-mobile-responsiveness-audit`** when the layout is responsive/mobile.

This skill also **owns the spatial visual-hierarchy, alignment, and composition fundamentals** (it absorbed the retired `visual-hierarchy` generative content): hierarchy created through size, position, and space; alignment and proximity; whitespace; rule-of-thirds/golden-ratio placement. It defers **type scale/readability** to `ux-typography`, **color/contrast for emphasis** to `ux-color`, and the **evaluative** composition review to `ux-aesthetics-audit`.

---

## Step 0 — Establish context before laying out

Ask if not known; state the assumption if proceeding without an answer:

- **Platform & density** — mobile vs. desktop, and how dense the UI is. Dense/compact tools may want a 4px base; most product UIs use 8px. Mobile tightens margins and must preserve touch-target spacing.
- **Content type** — uniform items (gallery, dashboard cards), long-form text, mixed media, or tabular data. This drives the grid choice (column vs. modular vs. manuscript vs. hierarchical).
- **Responsive or fixed context** — will it adapt across breakpoints, or run in a controlled environment (kiosk, signage)? Responsive needs a column model and breakpoints; fixed is the exception, not the default.

---

## The always-apply core (true for almost every layout)

### Build on one base unit and a scale

- **Pick a single base unit and make every spacing/sizing value a multiple of it.** 8px is the default (divides cleanly into halves/quarters; Material aligns to 8dp; Apple uses 8/16/32-pt increments); 4px for dense interfaces. **No arbitrary values** — 13px or 27px gaps are the tell of an unsystematic layout.
- **Express the scale as tokens, not one-offs.** Numeric scale (`spacing-01…`, e.g. 4, 8, 16, 24, 32, 48, 64) optionally with a semantic layer (`xs/sm/md/lg`). Consistency lets one change flow through; it also kills guesswork.
- **Unify spacing *and* sizing on the same base unit** so gutters, columns, and component sizes snap together and the page reads as one system.
- **Handle off-scale values as flagged exceptions.** If something genuinely needs a between-steps value, give it a functional name (`card-media-height`) or an irregular number so it's obviously not part of the scale — frequent exceptions are how a system rots.

### Use space to group and to rank (hierarchy)

- **Proximity groups.** Smaller gaps tie related elements together; larger gaps separate groups. Users read nearby items as one unit (Gestalt proximity).
  - ❌ Equal spacing between a label, its field, and the *next* field — the form reads as one undifferentiated stack. ✅ Tight label↔field, larger gap between fields.
- **External spacing ≥ internal spacing.** If the space *around* a component is smaller than the space *inside* it, unrelated elements visually merge. Keep outer ≥ inner.
- **Space creates hierarchy.** More space and prominent position (top/leading, following reading order) make an element feel important; primary content gets room to breathe, secondary content is set apart. Combine with size — but space alone already ranks.
- **Whitespace is active, not wasted.** Macro whitespace separates sections; micro whitespace aids readability and enlarges touch targets. Don't fill every gap.

### Align everything to a grid

- **Put content on a grid and keep it there.** Columns hold content; **gutters** are the gaps between; **margins** are the outer edges — content never sits in the gutter or the margin. Keep equal gutters.
- **Distinguish the three spacings:** margin (external/between), padding (internal), gutter (between columns). Mixing them up is a common source of inconsistency.
- **Align similar elements consistently on both axes** — images with images, text baselines with text baselines — so the eye scans a predictable edge. Maintain vertical rhythm.
- **Adapt the container to the grid, not the grid to the content.** A stable grid plus flexible container sizes keeps layouts predictable and easy to extend. Break the grid only deliberately (see levers).

### Make it adapt

- **Plan responsiveness around the grid.** Resize containers and reflow columns at breakpoints rather than rebuilding the structure; standard column counts are 12 desktop / 8 tablet / 4 mobile.
- **Scale spacing with text (dynamic type).** When users enlarge text, margins/padding/gaps and row heights should scale too, so hierarchy and touch targets survive. Respect safe areas and platform margins.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0; let the user choose. **Applying every grid type and proportion system at once is the failure mode.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Base unit (8px vs 4px)** | 8px for most product UIs; 4px for dense/data-heavy interfaces needing finer control | Mixing both, or going off-grid for convenience | 8px base; drop to 4px only where density truly demands it |
| **Grid type** | *Column* for general layouts; *modular* (columns × rows) for galleries/tables/e-commerce; *manuscript* for long text; *hierarchical* for content-led/editorial; *integrated* (two grids) for media + type | Forcing a modular grid on simple content (false rigor) or a manuscript grid on a dashboard | Column grid by default; modular for uniform card/data layouts |
| **Symmetric vs asymmetric** | Symmetric for uniform, equal-priority content (calm, classic); asymmetric to emphasize and add movement | Asymmetry that breaks the reading pattern into chaos | Symmetric unless you need emphasis/contrast; keep consistent proportions |
| **Column model (fixed/fluid/responsive)** | Responsive (resize + breakpoints) for cross-device; fluid (%) for smooth scaling; fixed only in controlled environments | Fixed-pixel layouts on the open web (horizontal scroll on small, dead space on large) | Responsive by default; plan breakpoints up front |
| **Sizing approach** | *Element-first* (fixed dimensions) for buttons/inputs/icons that need uniformity; *content-first* (fixed padding, size grows) for text blocks, table rows, unpredictable content | Fixing heights on content that varies (clipping/overflow) | Element-first for interactive primitives; content-first for content containers |
| **Golden ratio / rule of thirds** | Placing focal elements (hero, CTA) at active-zone intersections; deriving harmonious proportions | Treating it as a mandate that overrides content needs or the base-unit scale | Use to *place* focal points; keep spacing on the unit scale |
| **Semantic token layer** | Larger teams/design systems that benefit from `xs/sm/md` aliases over raw numbers | Tiny projects where the alias layer is overhead | Numeric scale always; add semantic aliases for systems |
| **Breaking the grid** | A deliberate hero/element breaking out to grab attention | Breaking it by accident or so often the grid stops meaning anything | Break intentionally and rarely; everything else stays aligned |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After laying out or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **none are Tier A; `aesthetics` and `accessibility` are Tier B (offered), and `mobile-responsiveness` is Tier B (offered, mobile only)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — the composition review this skill generates *toward*: is spacing consistent and on-scale, is there a clear hierarchy, is alignment clean, is whitespace balanced (not cramped, not cavernous)? Aesthetics owns the *evaluative* side of composition/hierarchy.
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — do spacing and sizing preserve adequate touch targets, does the layout reflow without loss at higher zoom/text sizes, does spatial grouping still make sense to assistive tech?
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer; applies only on mobile)* (when responsive/mobile) — do margins, gutters, and column counts adapt cleanly across breakpoints, and does spacing scale with dynamic type?

Scope & composition (per `docs/orchestration-policy.md` §9): **inherit under a design system (only build from scratch)** — `ux-typography` owns **type scale and readability** and `ux-color` owns **color-based emphasis/contrast**; take both from the system's tokens when one exists. Hierarchy is built from space *and* type *and* color together. If the audits surface a conflict, resolve toward the purpose: **layout exists to make content scannable and ranked — if spacing is arbitrary, nothing's on a grid, or everything has equal weight, the structure isn't done.**

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Use arbitrary values (13px, 27px) | Put every value on one base unit (8px/4px) and a token scale |
| Pad and space by eyeball | Define spacing/sizing tokens and reuse them |
| Space related and unrelated items equally | Proximity: tight within a group, larger between groups |
| Let outer space be smaller than inner space | Keep external spacing ≥ internal spacing so groups don't merge |
| Drop content on the canvas with no grid | Align content to columns; keep it out of gutters and margins |
| Mix alignments / ragged edges | Align similar elements consistently on both axes |
| Give every element equal weight | Use space + position (and size) to rank importance |
| Fill every gap | Treat whitespace as active — grouping, breathing room, touch targets |
| Rebuild the grid per breakpoint | Adapt container sizes to a stable grid; reflow columns at breakpoints |
| Force one grid/proportion system everywhere | Pick the grid type that fits the content; reach for golden-ratio only to place focal points |
| Ship the layout unchecked | Hand off to aesthetics + accessibility (+ mobile-responsiveness) |

---

## Source lessons (Uxcel)

- [Layout Fundamentals & Spacing](https://uxcel.com/lessons/layout-fundamentals-spacing-482)
- [Spacing & Sizing in Design Systems](https://uxcel.com/lessons/spacing-sizing-803)
- [Intro to Design Grids](https://uxcel.com/lessons/grid-i-044)
- [Best Practices for Designing Grids](https://uxcel.com/lessons/grid-best-practices-485)
- [Composition Grids in Design](https://uxcel.com/lessons/dc--lesson-050)
- [Applying Composition Grids in Design](https://uxcel.com/lessons/dc--lesson-679)
- [Typographic Grid](https://uxcel.com/lessons/typographic-grid-077)
- [Basics of Design Composition](https://uxcel.com/lessons/design-composition-182)
- [Intro to Design Layouts](https://uxcel.com/lessons/basics-139)
- [Design Format Properties](https://uxcel.com/lessons/dc--lesson-177)
