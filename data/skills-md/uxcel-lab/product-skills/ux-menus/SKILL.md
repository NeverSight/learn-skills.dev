---
name: ux-menus
description: Design or critique UI menus — pick the right menu type (dropdown, cascading, contextual, single/multi-select, search, inline) for the action set, and apply item ordering, grouping, labeling, and state best practices. Trigger when the user asks to design or review a menu, dropdown, context/right-click menu, overflow (⋮) menu, or asks how to organize actions into a menu.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Menus Skill

## How this skill behaves (read first)

This is a **generative** skill. The default failure modes: **catch-all dropdowns** (unrelated actions dumped into one menu), **deep ambiguous nesting** (cascading levels users get lost in), and **unordered item lists** (no prioritization, no grouping, jargon labels). A menu is a *curated, ordered set of related actions* — when it stops being that, the fix is changing the flow, not adding levels. This skill gates:

1. **Establish the action set** — what actions, how related, how many, selection or command?
2. **Apply the always-true core** — type from structure, priority ordering, grouping, labels, states.
3. **Surface the context-dependent decisions** (cascading, contextual, search-in-menu, shortcuts) with trade-offs.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, and `ux-microcopy-audit`** for validation.

> Scope & composition (per `docs/orchestration-policy.md` §9): this skill owns menu *structure and anatomy*. **Peers that own a sub-part (defer — each handles its sub-part if reached):** `ux-navigation` owns where menus live in the overall navigation system (hamburger placement, mega menus, top bar vs. sidebar), and `ux-selection-controls` owns the choice between menus vs. radio/checkboxes for form selection.

---

## Step 0 — Establish the action set

Ask if not known; state the assumption if proceeding without an answer:

- **Commands or selection?** Triggering actions (Copy, Delete) vs. choosing values (filter options) — selection menus need selection indicators and single/multi-select decisions; command menus need verbs and possibly shortcuts.
- **How many items, how related?** A menu only earns its place if the items belong together. Unrelated actions → split or rethink the flow. Very long lists → search menu or a different control.
- **Is there sub-structure?** Real parent-child categories may justify cascading — but if children multiply, change the user flow instead.
- **Platform** — contextual (right-click) menus are desktop-native; multiselect menus are hard on mobile; hover states need touch equivalents.

---

## The always-apply core (correct for almost every case)

### Pick the type from the structure of the choice

- **Basic dropdown** — one pick from a simple list; closes on selection.
- **Single-select** — mutually exclusive options with a clear selection indicator (checkmark, bold, overlay). Don't use it to launch modals or dynamic controls.
- **Multiselect** — checkboxes/tags for combinable options; selected items always visible and removable *in the menu input* — never force backtracking to deselect.
- **Search menu** — long lists (countries, languages): auto-suggest filtering as users type.
- **Contextual menu** — frequent actions for the clicked element (right-click/long-press), appearing at the pointer, options varying by target.
- **Inline / overflow (⋮) menu** — per-row actions in tables and lists (Edit, Delete, Download) without leaving the view.
- **Cascading menu** — only for genuinely categorized actions (New → document types); see the gated table.

### Order and group — this is where menus are won

- **Most-used items at the top.** Don't hide critical options behind extra levels when space exists; working memory holds ~5–9 items, so the primary list carries the important actions, the rest go a level down or out.
- **Dividers cluster related items** — pale lines, not separate menus; grouping makes the list scannable without clutter.
- **Scrolling is a smell:** a scroll bar is mandatory if you scroll, but beyond a couple of wheel-turns of options, add search or change the flow.

### Labels and icons

- **Labels say what happens** — short, conventional ("Paste," not "Insert"), no jargon or wordplay; truncate unavoidable long labels with tooltip access; a wrapped label is a label that needs rewriting. Test labels (card sorting) — what's clear to you confuses users.
- **Leading icons before labels** (LTR) — familiar, universal icons only (scissors = Cut); unfamiliar icons slow users down more than no icon.
- **Familiar selection marks** — checkmark or ×; nothing inventive.

### States and behavior

- **Hover/focus feedback on every item** (subtle overlay, elevation, or border) and visible states for selected/disabled.
- **Predictable open/close:** opens on tap/click, closes on outside click. No surprises.
- **Items ≥48×48px** with comfortable padding — legibility and motor-impairment access.
- **Elevation (~8dp) separates the menu from the page** — it should read as a floating, actionable surface.

---

## The context-dependent decisions (surface, don't auto-apply)

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Cascading menu** | True parent-child action categories; desktop, with room to unfold | Many/deep children (cumbersome, overwhelming); mobile; tight layouts — check unfold space with mockups | One child level max; if it grows, restructure the flow |
| **Contextual (right-click) menu** | Desktop power workflows; element-specific frequent actions | As the *only* access to a function (undiscoverable); touch-first products | Context menu as accelerator; every action also reachable visibly |
| **Search inside the menu** | Long lists where scrolling is tedious | Short lists (overhead) | Add when the list exceeds a couple of scroll-turns |
| **Keyboard shortcuts shown in the menu** | Productivity tools with repeat actions (copy/cut/paste) | Inventing non-standard shortcuts; shortcut-only access | Standard shortcuts on the most common commands, displayed in the menu |
| **Multiselect pattern** | Hotkey+click, checkboxes, or tag collection — pick by audience and platform | Hotkey-based multiselect on mobile or for casual audiences | Checkboxes/tags; selections visible and removable in place |
| **Icon-only inline menus (⋮)** | Dense tables needing per-row actions | Burying the row's single most important action in the overflow | Primary row action visible; secondary actions in ⋮ |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics` and `microcopy` are Tier A (auto-run); `accessibility`, `aesthetics`, `information-architecture`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — recognition over recall (visible critical options), consistency of behavior, user control (easy deselection, predictable dismissal).
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — keyboard navigation through items, 48px targets, contrast of labels and dividers, non-hover access to everything.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — spacing, elevation, grouping rhythm; whether the menu reads as one clean surface.
- **`ux-microcopy-audit`** *(Tier A)* — label clarity, conventional verbs, truncation choices.
- **`ux-information-architecture-audit`** *(Tier B — offer)* — whether the menu's grouping, depth, and label system match user mental models and carry information scent; this skill structures the menu surface, IA owns the category model behind it.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer; applies only on mobile)* — when the context is mobile: touch targets, no hover-dependence, multiselect pattern fit.

If the audits surface a conflict (e.g., completeness vs. scannability), resolve back toward the primary task: the user opens a menu to act fast — every item competes for the same scan.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| One dropdown holding every miscellaneous action | Related actions only; restructure when it stops being a set |
| Three levels of cascading children | One child level; if it grows, change the flow |
| Alphabetical order regardless of use | Most-used first; secondary items a level down |
| Flat list of 14 ungrouped items | Dividers clustering related actions |
| "Insert" when everyone says "Paste" | Conventional, tested labels |
| Decorative or clever icons per item | Universal icons only — or no icon |
| Right-click as the only way to delete | Contextual menu as accelerator, visible path exists |
| Deselecting requires reopening and hunting | Selected items shown and removable in place |
| Menu stays open on outside click | Standard open/close behavior |
| 32px cramped rows | ≥48px items with breathing room |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy |

---

## Source lessons (Uxcel)

- [Types of UI Menus](https://uxcel.com/lessons/types-i-358)
- [Best Practices for Designing UI Menus](https://uxcel.com/lessons/anatomy-ii-502)
