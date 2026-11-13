---
name: ux-iconography
description: Choose and design UI icons that are understood, not just decorative — universal metaphors, one consistent style, text/accessible labels where meaning isn't obvious, legible at small sizes, and adequate touch targets. Replaces ambiguous icon-only buttons and mixed icon styles with a system. Trigger when asked to add or pick icons, design an icon set, decide filled vs outlined, label icons, fix inconsistent/ambiguous iconography, or choose between a system library (SF Symbols/Material) and custom icons.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Iconography Skill

## How this skill behaves (read first)

This is a **generative** foundation skill. Icons are where an AI assistant ships ambiguity: Claude adds **icon-only buttons with no labels**, reaches for **novel or decorative** glyphs instead of the metaphor users already know, **mixes styles** (some outlined, some filled, different stroke weights), and uses **different icons for the same action** across a screen. An icon that makes the user stop and decode it has failed — its whole job is faster recognition.

So this skill gates:

1. **Establish context** — platform/library, whether icons earn their place here, and the design-system maturity (these set the style, the label policy, and the source).
2. **Apply the always-true core** — universal metaphors, one consistent style, labels where meaning isn't obvious, legibility at size, and accessible labels.
3. **Surface the context-dependent decisions** (icon style, system library vs custom, labels, state variants, rendering mode, containers) with trade-offs; let the user choose.

Then it **hands off to `ux-accessibility-audit`** (labels, contrast, touch targets), **`ux-aesthetics-audit`** (style consistency, overdesign), and **`ux-microcopy-audit`** (the icon labels themselves), plus **`ux-mobile-responsiveness-audit`** when touch targets matter.

Scope & composition (per `docs/orchestration-policy.md` §9): this skill owns **icon choice, style, and usage**. **Peers that own a sub-part (defer — each handles its sub-part if reached):** `ux-buttons` owns **button label wording and button anatomy**. **Inherit under a design system (only build from scratch):** `ux-typography` owns the **type scale** and `ux-layout-spacing-grids` owns the **spacing/grid the icons sit on** — take both from the system's tokens when one exists. The **full evaluative review** defers to the audits above.

---

## Step 0 — Establish context before choosing icons

Ask if not known; state the assumption if proceeding without an answer:

- **Platform & library** — iOS/macOS lean on SF Symbols; Android on Material symbols; web may use an open set or a custom library. The platform sets default metaphors, rendering, and weights.
- **Do icons earn their place here?** Icons help with frequent or quick-access actions and scanning. If an icon doesn't simplify the journey, omit it — clutter dilutes the icons that matter. One icon, one action.
- **Design-system maturity** — a one-off screen needs the right glyphs and labels; a system needs naming, tagging, component structure, and tokens so the set stays consistent and findable.

---

## The always-apply core (true for almost every icon)

### Make it understood

- **Use universal, recognized metaphors — clarity over novelty.** Magnifying glass for search, arrows for navigation, gear for settings. A clever substitute (binoculars for search) just makes users stop and think.
  - ❌ A bespoke glyph for "search." ✅ The magnifying glass everyone already reads as search.
- **Label when meaning isn't obvious.** Unique/ambiguous icons need a short text label (1–3 words, action words like "Search," "Share"). Universal icons can sometimes stand alone — but pairing icon + label is the safe default in dense or first-use contexts.
- **Always provide an *accessible* label for icon-only controls.** If there's no visible text, the control needs an accessible name so screen readers can announce its purpose. (If a visible label exists, that serves as the accessible text — don't double up.)
- **One action, one icon — and don't conflict.** Use the same icon for the same action everywhere; never two icons for one concept. Be aware metaphors carry different meanings across products (heart vs. star vs. thumbs-up; heart = "like" vs. "love" vs. "save") and keep your usage unambiguous.

### Make it legible and consistent

- **Keep icons simple.** Reduce to the essential shape; fine detail blurs or disappears at small sizes. Add detail only where the display size genuinely supports it.
- **One consistent style across the set.** Match stroke weight, corner radius, geometry, and color treatment. Mixing outlined and filled (or sharp and rounded) at random breaks the visual language. Pick a single primary style.
- **Balance optically, not just mathematically.** Equal frame size ≠ equal visual weight; a dense glyph looks heavier than a sparse one at the same dimensions. Adjust within the frame (and use consistent containers/padding) so icons *feel* equal.
- **Design per size; don't mechanically scale.** Stroke scales with the frame (e.g. 16px→~1px, 24px→~1.5px); small sizes need simpler geometry. Use SVG so icons stay crisp across densities.

### Make it usable

- **Adequate touch targets.** The tappable area should exceed the glyph — at least 44×44pt (iOS) / 48×48dp (Android) — with padding so neighboring icons aren't mis-tapped.
- **Consistent, purposeful color.** A limited palette: one standout color for active/important icons, a muted/neutral for the rest; semantic colors where they carry meaning (red = destructive, etc.). Don't let colored icons distract from content.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0; let the user choose. **Mixing styles, or labeling everything / nothing by reflex, is the failure mode.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Icon style** | *Outlined* for clean, text-heavy UIs; *filled* for stronger contrast in compact spaces; *colored/duotone* for playful brands | Mixing styles freely; colored icons that distract or fail at small/accessibility sizes | Pick one primary style (outlined or filled) and apply it across the set |
| **System library vs custom** | SF Symbols/Material for platform-native consistency, auto weight/scale/alignment; custom only for unique concepts | Reinventing universal glyphs; custom icons that don't match the system's stroke/grid | Use the platform library first; add custom icons that match its characteristics |
| **Label or icon-only** | Label unique/ambiguous icons and first-use contexts; icon-only acceptable for truly universal glyphs with an accessible name | Icon-only for unique actions (users guess); over-labeling universal toolbar icons in tight space | Pair icon + label when in doubt; always keep an accessible name |
| **Filled vs outlined for state** | Use the variant to signal *state* — outlined = default, filled = selected/active (favorite, bookmark, visibility) | Switching variants for decoration rather than meaning | Reserve the filled/outlined switch for state; keep structure identical across variants |
| **Rendering mode** (Apple) | Monochrome for flexibility; hierarchical for depth; palette/multicolor for semantic meaning | Multicolor where it muddies an interface control | Monochrome for interface elements; richer modes only for semantic/feature icons |
| **Container & grid** | Containers/keylines for uniform alignment, touch-target size, and optical balance across a set | Letting every icon fill its frame edge-to-edge (uneven weight) | Use consistent frames + trim/padding; align to an icon grid |
| **Library structure** (systems) | Naming (`category/object/modifier`), tags, flattened single-layer components, color tokens | Ad-hoc names and inconsistent layer structure (breaks swaps/overrides, spawns duplicates) | Group by purpose, name + tag consistently, keep identical component structure |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After choosing or designing icons, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`microcopy` is Tier A (auto-run); `accessibility`, `aesthetics`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — do icon-only controls have accessible names, do icons meet contrast against their background, are touch targets large enough, is meaning ever carried by color/icon alone?
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — is the set one consistent style (stroke, geometry, color), optically balanced, and free of decorative overload?
- **`ux-microcopy-audit`** *(Tier A)* — are the icon labels short, clear, action-oriented, and consistent with the product's voice?
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer; applies only on mobile)* (when targeting touch) — do touch targets and spacing hold up on small screens?

This skill defers **button label copy and button anatomy** to `ux-buttons`, and the **spacing/grid** icons sit within to `ux-layout-spacing-grids`. If the audits surface a conflict, resolve toward the purpose: **an icon exists to make an action faster to recognize — if it's ambiguous, inconsistent, or unreadable, add a label, unify the style, or drop it.**

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Ship icon-only buttons for non-obvious actions | Pair with a label; always give an accessible name |
| Invent a clever/novel metaphor | Use the universal glyph users already know |
| Mix outlined + filled + different stroke weights | One consistent style across the whole set |
| Use different icons for the same action | One action, one icon, everywhere |
| Pack in fine detail | Keep it simple so it reads at small sizes |
| Trust equal frame size for equal weight | Balance optically with containers/padding |
| Mechanically scale one icon to all sizes | Design per size; scale stroke; use SVG |
| Shrink the tap area to the glyph | ≥44pt / 48dp touch target with padding |
| Switch filled/outlined for decoration | Use the variant to signal state (default vs active) |
| Reinvent platform-standard icons | Start from SF Symbols / Material; match them for custom |
| Ship icons unchecked | Hand off to accessibility + aesthetics + microcopy (+ mobile) |

---

## Source lessons (Uxcel)

- [How to Use Icons in UI Design](https://uxcel.com/lessons/icons-in-ui-616)
- [Icons & Symbols Guidelines](https://uxcel.com/lessons/icons-symbols-guidelines-647)
- [Iconography in Design Systems](https://uxcel.com/lessons/iconography-standards-997)
- [Icon Terminology](https://uxcel.com/lessons/basics-457)
