---
name: modern-css
description: Use this skill when writing, reviewing, or refactoring CSS and HTML to replace legacy CSS, JavaScript-driven presentation, preprocessors, layout hacks, or unnecessary UI libraries with modern native web-platform features.
---

# modern css

Prefer the smallest native HTML and CSS solution that meets the project's browser targets.

Sources:

- https://modern-css.com/AGENTS.md
- https://modern-css.com/llms.txt

## workflow

1. inspect existing browser targets, conventions, and dependencies.
2. identify the behavior before changing its implementation. keep application state and business logic in JavaScript.
3. replace legacy workarounds with a stable native pattern when it is simpler.
4. check current browser support for unfamiliar or recently introduced features. add a simple fallback only when a target browser needs one.
5. test responsive layout, overflow, keyboard focus, zoom, reduced motion, and relevant color schemes.
6. run the project's formatter, linter, and tests.

## preferred patterns

| replace                                          | prefer                                                 |
| ------------------------------------------------ | ------------------------------------------------------ |
| absolute-position centering                      | grid `place-items` or flex alignment                   |
| child margin spacing hacks                       | `gap`                                                  |
| aspect-ratio padding hacks                       | `aspect-ratio`                                         |
| physical left/right properties                   | logical inline/block properties                        |
| duplicated nested grid tracks                    | `subgrid`                                              |
| component media queries                          | container queries                                      |
| JavaScript sticky positioning                    | `position: sticky`                                     |
| `100vh` on mobile                                | `svh`, `dvh`, or `lvh` according to intent             |
| JavaScript parent class toggles for visual state | `:has()`                                               |
| specificity-heavy resets                         | `:where()`                                             |
| mouse-triggered focus rings                      | `:focus-visible` with a visible outline                |
| Sass/Less nesting                                | native CSS nesting                                     |
| `!important` and specificity escalation          | cascade layers and low-specificity selectors           |
| breakpoint ladders for fluid values              | bounded `clamp()` values                               |
| hard-coded color variants                        | custom properties, `oklch()`, and `color-mix()`        |
| combined transform rewrites                      | independent `translate`, `rotate`, and `scale`         |
| simple JavaScript carousels                      | overflow and scroll snap                               |
| custom modal, popover, or accordion primitives   | `<dialog>`, popover, or `<details>` when semantics fit |
| JavaScript scroll-chain prevention               | `overscroll-behavior`                                  |
| background images used for content               | `<img>` with `object-fit`                              |

## rules

- use container queries for reusable components and media queries for viewport or user preferences.
- use custom properties for design tokens and runtime theming.
- use `text-wrap: balance` for short headings and `text-wrap: pretty` for prose.
- prefer semantic native HTML before recreating interaction with generic elements.
- preserve source order, keyboard behavior, focus management, labels, accessible names, and contrast.
- honor `prefers-reduced-motion` and avoid fixed heights that clip enlarged text.
- use `@supports` for progressive enhancement when the baseline remains usable.
- verify limited or experimental features against current MDN data and project browser targets.
- do not replace tested production behavior with an experimental feature without approval.
- do not build a complex CSS fallback merely to remove a small, clear JavaScript solution.
