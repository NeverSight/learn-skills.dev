---
name: ui-ux-guidelines
description: "Review UI code for Web Interface Guidelines compliance. Use when asked to review UI, check accessibility, audit design, review UX, or check against best practices."
---

# Web Interface Guidelines

Dispatch hub for UI/UX rules. Load the relevant reference file for full details.

## Contents

1. [Rule Categories](#rule-categories-by-priority)
2. [Workflows](#workflows)
3. [Anti-patterns](#anti-patterns-flag-these)
4. [Output Format](#code-review-output-format)
5. [Reference Files](#reference-files)

---

## Rule Categories by Priority

| Priority | Category             | Impact   | Reference File                  |
| -------- | -------------------- | -------- | ------------------------------- |
| 1        | Accessibility        | CRITICAL | `accessibility-and-interaction` |
| 2        | Touch & Interaction  | CRITICAL | `accessibility-and-interaction` |
| 3        | Performance          | HIGH     | `layout-typography-animation`   |
| 4        | Layout & Responsive  | HIGH     | `layout-typography-animation`   |
| 5        | Typography & Color   | MEDIUM   | `layout-typography-animation`   |
| 6        | Animation            | MEDIUM   | `layout-typography-animation`   |
| 7        | Forms                | HIGH     | `forms-content-checklist`       |
| 8        | Content & Navigation | MEDIUM   | `forms-content-checklist`       |
| 9        | Charts & Data        | LOW      | `layout-typography-animation`   |

---

## Workflows

### 1. Review UI code

1. Read the target file(s).
2. Load the relevant reference file(s) from `references/` based on what the code contains.
3. Check each applicable rule. Report violations in the output format below.

### 2. Build new component

1. Load `references/accessibility-and-interaction.md` -- all components must meet CRITICAL rules.
2. Load additional references based on component type:
   - Form component -> `references/forms-content-checklist.md`
   - Layout/visual component -> `references/layout-typography-animation.md`
3. Follow rules during implementation.

### 3. Pre-delivery checklist

1. Load `references/forms-content-checklist.md` for the full checklist.
2. Load `references/accessibility-and-interaction.md` for the interaction checklist.
3. Walk through every checkbox before shipping.

---

## Anti-patterns (flag these)

- `user-scalable=no` or `maximum-scale=1` -- disables zoom
- `onPaste` with `preventDefault` -- blocks paste
- `transition: all` -- list properties explicitly
- `outline-none` without `:focus-visible` replacement
- `<div>`/`<span>` with click handlers -- use `<button>` or `<a>`
- `<img>` without `width` and `height` (causes CLS)
- Inline `onClick` navigation without `<a>` (breaks Cmd+click)
- Large `.map()` without virtualization (>50 items)
- Hardcoded date/number formats -- use `Intl.*`
- Icon-only buttons without `aria-label`

---

## Code Review Output Format

Group findings by file. Use `file:line` format (VS Code clickable). Be terse -- state issue and location. Skip explanation unless fix is non-obvious.

```text
## src/Button.tsx

src/Button.tsx:42 - icon button missing aria-label
src/Button.tsx:18 - input lacks label
src/Button.tsx:55 - animation missing prefers-reduced-motion
src/Button.tsx:67 - transition: all -> list properties explicitly

## src/Modal.tsx

src/Modal.tsx:12 - missing overscroll-behavior: contain
src/Modal.tsx:34 - "..." -> "..."

## src/Card.tsx

pass
```

---

## Reference Files

Load these as needed during reviews and implementation:

- **[Accessibility & Interaction](references/accessibility-and-interaction.md)** -- Focus, ARIA, keyboard, touch targets, cursors, drag UX
- **[Layout, Typography & Animation](references/layout-typography-animation.md)** -- Performance, responsive, fonts, color, motion, charts
- **[Forms, Content & Checklist](references/forms-content-checklist.md)** -- Forms, content handling, navigation, dark mode, locale, hydration, pre-delivery checklist
