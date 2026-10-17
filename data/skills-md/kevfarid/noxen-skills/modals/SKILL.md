---
name: modals
description: >
  Use when adding or reviewing a modal/dialog — opening it from more than
  one place, focus trapping, accessibility, or choosing a modal approach.
  Trigger on tasks like "open this as a modal", "this modal needs to be
  triggered from two places", "add a confirmation dialog", or "which modal
  library should I use". Library-agnostic — loads a
  `references/<library>.md` for the concrete approach the project uses
  (nice-modal-react, Radix Dialog, the native `<dialog>` element). On
  Next.js, see also `nextjs/screen-config` for a modal that's also
  reachable as a full route. Do NOT trigger for a component that merely
  contains a `useState('isOpen')` toggle with a single trigger — that's
  plain React, see `react-patterns`.
metadata:
  version: 1.0
  collection: noxen
---

# Noxen — Modals

Part of the **Noxen** skill set. This skill covers modal/dialog patterns
independent of which approach a project uses — load the matching
`references/*.md` for the concrete one actually installed.

## Local State vs. a Registry — Pick by Trigger Count

A modal opened from exactly one place is plain React — a local
`useState('isOpen')` next to the component that opens it, no library
needed:

```tsx
const [isOpen, setIsOpen] = useState(false);
<button onClick={() => setIsOpen(true)}>Delete</button>
{isOpen && <ConfirmDialog onClose={() => setIsOpen(false)} />}
```

Once a **second**, unrelated trigger needs to open the *same* modal — a
menu item here, a keyboard shortcut there — local state forces one of them
to own it and prop-drill or lift state up awkwardly. That's the point to
reach for a library: an imperative, globally-registered modal any component
can call without holding its open/closed state.

## Load the Right Reference

| Concern | Reference |
|---|---|
| Project uses nice-modal-react | `references/nice-modal-react.md` |
| Project uses Radix Dialog (or a design system built on it) | `references/radix-dialog.md` |
| No library — using the native `<dialog>` element | `references/native-dialog.md` |
| Starting a new project, no approach chosen yet | Read `## Choosing an Approach` below |

## Choosing an Approach (New Projects)

If the project already has a component library (shadcn/ui, Radix-based
design system), its `<Dialog>` primitive already solves focus trapping and
accessibility — use `nice-modal-react` alongside it purely for the
imperative "open this from anywhere" registry, not as a competing dialog
implementation (it's explicitly designed to wrap another library's dialog,
not replace it). Starting from scratch with no design system yet and modest
needs, the native `<dialog>` element now covers focus trapping and
top-layer stacking without a dependency — reach for it before adding a
library.

## Hard Rules

- A modal with exactly one trigger uses local `useState` — don't reach for a global registry preemptively.
- A modal reachable from more than one place is registered once and opened imperatively — never duplicated as separate local `isOpen` state per trigger.
- `nice-modal-react` wraps a dialog implementation, it isn't one — pair it with the project's existing dialog component, don't use it to skip accessibility work a real dialog primitive would give you.
