---
name: dxe-semantic-html-first
description: "Choose HTML semantics and accessible behavior for controls, forms, and custom interaction primitives."
license: MIT
---

# Semantic HTML First

Semantic HTML is interface infrastructure. Native elements carry keyboard support, form participation, disabled behaviour, and accessibility semantics without a second implementation.

## Defaults

1. Start with the native element that matches the interaction.
2. Use ARIA to refine native semantics, not to rebuild them on `div`/`span`.
3. Prefer explicit composition over magic `asChild` polymorphism when it obscures the real element.
4. Style states with native pseudo-classes (`:disabled`, `:checked`, `:open`, `:invalid`) before parallel `data-*` state systems.
5. If a library primitive exists, verify it still renders a real semantic element in the DOM.

## Prefer / Reject

| Prefer | Reject |
| --- | --- |
| `<button type="button">` | `<div onClick>` / `<span role="button">` without need |
| `<a href>` for navigation | Button-styled divs that only route in JS |
| `<details>` / `<summary>` | Custom disclosure with ad-hoc keyboard code |
| `<dialog>` / Popover API | Modal divs fighting focus and top-layer behaviour |
| Native `<form>` controls | Clickable rows that ignore Enter/Space/disabled |

## Decision guide

- **Performs an action:** `button`
- **Goes somewhere:** `a[href]`
- **Toggles visibility of related content:** `details` or disclosure button + controlled region
- **Requires a temporary overlay task:** `dialog` or `popover`
- **Collects input:** native form controls inside `form`

## Review checklist

- [ ] Can this be a native element?
- [ ] Tab focus works without extra code?
- [ ] Enter/Space activate buttons?
- [ ] Disabled state blocks interaction and exposure correctly?
- [ ] Screen reader role matches the visual control?
- [ ] Form controls submit/reset with the form?
- [ ] Custom ARIA is additive, not a rewrite of the platform?

## Source essays

- On the semantic web
- Why I built a semantic-HTML first library
