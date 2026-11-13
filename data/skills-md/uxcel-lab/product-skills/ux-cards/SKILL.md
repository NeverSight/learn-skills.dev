---
name: ux-cards
description: Design or critique UI cards — one-topic, scannable cards with clear hierarchy, the right container style (elevated, outlined, flat), and restrained shadows. Trigger when the user asks to design or review cards, card layouts, card grids, content tiles, user/profile cards, or a browse view built from cards.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Cards Skill

## How this skill behaves (read first)

This is a **generative** skill. The default failure modes: **card stuffing** (multiple topics, long text, every detail crammed into one card), **shadow soup** (shadows on the card *and* its image *and* its buttons), and **cards-for-everything** (card grids where users need ranked, comparable results). A card is *one digestible topic in one container, inviting exploration* — and card layouts fit browsing, not searching. This skill gates:

1. **Establish what's being carded and how users consume it** — browsing vs. searching decides whether cards are even right.
2. **Apply the always-true core** — one topic per card, internal hierarchy, progressive disclosure, restraint.
3. **Surface the container-style and interaction decisions** (elevated/outlined/flat, full-card click, media) with trade-offs.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, and `ux-microcopy-audit`** for validation.

---

## Step 0 — Establish context before designing

Ask if not known; state the assumption if proceeding without an answer:

- **Browsing or searching?** Cards are flat — every card carries equal rank. That's perfect for exploratory browsing (feeds, galleries, dashboards) and wrong for ranked search results or spec-by-spec comparison (use lists/tables). If users hunt for a specific item, reconsider cards entirely.
- **Content per item** — text-only (metrics, notes) → text cards; media + summary + actions → rich cards; people → user cards (avatar, name, status, one CTA). Heterogeneous items with varying detail are cards' home turf.
- **One action or several?** A single action argues for a fully clickable card; multiple actions need an internal button hierarchy.
- **Platform/density** — mobile truncates harder, needs bigger touch areas, and responsive card grids reflow.

---

## The always-apply core (correct for almost every case)

### One card = one topic

- **Split distinct topics into separate cards.** The container's whole job is signaling "everything in here is related; everything outside isn't." Mixed-topic cards make users parse what belongs together.
- **The card is a teaser, not the article — progressive disclosure.** Short supporting text, truncated with an ellipsis that invites opening. Don't answer every question on the card face.
  - ❌ A card with full description, specs, three links, and two buttons ✅ Image, title, two-line teaser…, one clear action

### Hierarchy inside the card

- **Decide what users should see first** and enforce it with size, weight, color, and placement — title over preview, primary action over secondary.
- **Color hierarchy:** when everything is highlighted, nothing is. One emphasized element ("Learn more") — auxiliary actions (save, favorite) stay quiet.
- **Primary vs. secondary actions visibly differentiated**; overflow (kebab ⋮) menu in the top-right corner where users expect it.

### Restraint is the style

- **Simplicity first:** typography and negative space over horizontal dividers — dividers are rarely helpful inside a card.
- **One shadow per card, maximum.** Never shadow media, buttons, or icons inside an already-elevated card. Shadow visible on all four edges (soft ambient, not just a sharp key light).
- **Consistent padding and margins** — elements breathe, related items cluster, content never touches edges.
- **Concise labels:** no redundant words or punctuation; microcopy-grade brevity.
- **Quality media only** — blurry or grainy images break trust; text over images keeps ≥4.5:1 contrast (use a translucent dark overlay).

---

## The context-dependent decisions (surface, don't auto-apply)

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Elevated (shadowed) card** | Clickable cards needing affordance; mimics physical cards; intensify shadow on hover | Dense dashboards where dozens of shadows add noise | Default for interactive cards — with the one-shadow rule |
| **Outlined card** | Grouping without depth; cleaner, quieter surfaces | When interaction needs stronger affordance | Use for non-interactive or low-emphasis grouping |
| **Flat card** | Minimal aesthetics with a distinct background color separating it | Without any visual cue (users miss it entirely) | Only with a contrasting background + hover microinteraction |
| **Fully clickable card** | One primary action; bigger target, less cognition | Multiple competing actions inside (nested click traps) | Whole card clickable + hover cue when there's a single action |
| **Rich media card** | Browsing experiences where the visual is the content (products, articles, video) | Media as decoration that crowds the message | Media earns its space or gets cut |
| **User card** | Social/people contexts: avatar + name + status + one CTA | Cramming full profiles into the card | Identity + one action; the rest on the profile |
| **Card grid vs. list/table** | Heterogeneous, visual, browsable content | Ranked results, spec comparison, scanning for a known item | Cards for discovery; lists/tables for lookup (→ `ux-tables` for data) |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics` and `microcopy` are Tier A (auto-run); `accessibility`, `aesthetics`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — recognition (does the card read as one unit?), consistency across the card set, affordance of clickability.
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — text-over-image contrast (≥4.5:1), touch targets for in-card actions, focus states for clickable cards.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — this is the shadow-overload and clutter check: hierarchy, padding rhythm, one-emphasis rule.
- **`ux-microcopy-audit`** *(Tier A)* — title and label brevity, teaser text quality.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer; applies only on mobile)* — when the context is mobile: grid reflow, truncation, touch areas.

If the audits surface a conflict (e.g., marketing wants more on the card vs. scannability), resolve back toward the primary task: a card's job is to be grasped in a glance and invite the click — not to be the destination.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Three topics in one container | One topic per card; split into logical groups |
| Full article text on the card face | Teaser + truncation… — progressive disclosure |
| Shadows on card + image + buttons | One shadow per card; nothing inside gets its own |
| Horizontal dividers slicing the card | Negative space and typography do the separating |
| Every element bold and colorful | One emphasized element; color hierarchy |
| Flat card indistinguishable from the page | Distinct background + hover cue, or use outlined/elevated |
| Card with one action but only a tiny link is clickable | Entire card clickable, pointer cursor, hover effect |
| White text straight over a busy image | Dark translucent overlay, ≥4.5:1 contrast |
| Card grid for ranked search results | Lists/tables for lookup; cards for browsing |
| Kebab menu floating in a novel corner | Top-right, where users expect it |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy |

---

## Source lessons (Uxcel)

- [UI Cards Types & When to Use Them](https://uxcel.com/lessons/cards-310)
- [Best Practices for Designing UI Cards](https://uxcel.com/lessons/cards-best-practices-038)
