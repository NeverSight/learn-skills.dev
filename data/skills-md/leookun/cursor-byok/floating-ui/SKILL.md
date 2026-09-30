---
name: floating-ui
description: Implement or review floating desktop UI such as dropdowns, popovers, tooltips, menus, comboboxes, and nested overlays under apps/desktop.
---

# Floating UI

Use `@floating-ui/dom` for every interactive element positioned relative to a trigger. Do not calculate coordinates manually or rely on CSS absolute offsets for dropdowns, popovers, menus, combobox lists, or tooltips.

## Required structure

- Render overlays through `createPortal(..., document.body)` so layout and stacking contexts do not clip them.
- Position with `computePosition` inside `autoUpdate`; clean up the function returned by `autoUpdate` when the overlay closes or unmounts.
- Start from the closest existing control in `apps/desktop/src/components/ui`. Match its `placement`, `offset`, `flip`, `shift`, and `size` middleware unless the interaction requires a deliberate difference.
- Store computed `left`, `top`, width, and available height in React state. Apply the state to the portal root; do not mutate element styles directly.
- Use `size` when reference width or viewport height constrains the overlay. Lists that can grow must use `components/virtual/VirtualList.tsx`; keep fixed headers and footers outside the virtual viewport.

## Interaction invariants

- Keep the trigger's open/focus border visible while focus is inside a portaled overlay.
- Close on outside pointer interaction and Escape, then return focus to the trigger.
- Outside-click checks must include both trigger and overlay. A nested portaled overlay must stop its pointer event from reaching the parent's outside-click listener, so interacting with a child menu never closes its parent.
- Expose trigger state with `aria-expanded`, `aria-controls`, and the appropriate `aria-haspopup`; give the overlay the matching menu, listbox, dialog, or tooltip semantics.
- Verify placement near all viewport edges, nested-overlay clicks, keyboard dismissal, virtual scrolling, and fixed footer behavior.
