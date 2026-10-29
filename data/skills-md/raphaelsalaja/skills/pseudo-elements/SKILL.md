---
name: pseudo-elements
description: Reviews decorative pseudo-elements, native control styling and the View Transitions API.
license: MIT
metadata:
  author: raphael-salaja
  version: "1.0.0"
  source: https://www.userinterface.wiki
---

# Pseudo-elements

This skill reviews CSS pseudo-elements and the View Transitions API. It prefers a pseudo-element over an extra node when the layer is decorative.

Every check is a pair. The broken line sits beside the line that replaces it.

`content: ""` is required or `::before` and `::after` do not render. That is exact. A second DOM node used only as a wash or a hit pad is a finding when a pseudo-element can do it. Minimum target size belongs to `laws-of-ux`. Shadow animation via a pseudo-element belongs to `visual-design`. Component exit mounting belongs to `exit-animations`.

## When to use

Use this when styling hover layers, hit areas, placeholders, selections, dialog backdrops or a shared-element page change. Use `exit-animations` for a Motion tree that mounts and unmounts in place.

## 1. Read the decorative layers

Read the files in scope. List `::before`, `::after`, `::backdrop`, `::placeholder`, `::selection`, `::marker`, `::first-line` and any `view-transition-name` or `startViewTransition` call.

## 2. Check generated boxes

`::before` and `::after` set `content`, usually `""`. That is `pseudo-content-required`. Decorative washes, underlines and hit pads use a pseudo-element instead of an empty `span`. That is `pseudo-over-dom-node`. An absolute pseudo-element has a `position: relative` parent. That is `pseudo-position-relative-parent`. If the pseudo covers the text, put the text above it, typically with `z-index: -1` on the pseudo. That is `pseudo-z-index-layering`.

Expand a hit area with a negative inset on the pseudo, as in `inset: -8px -12px`. That is `pseudo-hit-target-expansion`. The `32px` minimum target is `laws-of-ux`.

Style list markers with `::marker`, not a fake bullet element. That is `pseudo-marker-styling`. Style the first line of a passage with `::first-line`. That is `pseudo-first-line-styling`.

## 3. Check native pseudos and view transitions

A `dialog` or popover dims the page with `::backdrop`, not a sibling overlay `div`. That is `native-backdrop-styling`. Placeholder text uses `::placeholder`. That is `native-placeholder-styling`. Selection color uses `::selection`. That is `native-selection-styling`.

An element that should morph across a page sets `view-transition-name` on the single participant. That is `transition-name-required`. The name is unique while the transition runs. That is `transition-name-unique`. Clear the name from the source when the target takes it. That is `transition-name-cleanup`. Prefer `document.startViewTransition` over a Motion `layoutId` for that shared-element page change. That is `transition-over-js-library`. Custom timing goes on `::view-transition-group`, not only the default crossfade. That is `transition-style-pseudo-elements`.

## 4. Report and stop

Write findings, then the summary. Do not replace a semantic element with a pseudo-element.
## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `pseudo-content-required` | `.button::before { position: absolute }` | Add `content: ""` |
| `pseudo-over-dom-node` | `<span className={styles.background} />` inside a button | `.button::before` for that wash |
| `pseudo-position-relative-parent` | Absolute `::before` on a static parent | `.button { position: relative }` |
| `pseudo-z-index-layering` | A `::before` wash with no `z-index` over the label | `z-index: -1` on the pseudo |
| `pseudo-hit-target-expansion` | A hit box equal to the glyph | `inset: -8px -12px` on `::before` |
| `pseudo-marker-styling` | A fake bullet element | `li::marker` |
| `pseudo-first-line-styling` | A wrapped first-line span | `p::first-line` |
| `native-backdrop-styling` | A sibling overlay behind `<dialog>` | `dialog::backdrop` |
| `native-placeholder-styling` | A placeholder `<span>` toggled on empty input | `input::placeholder` |
| `native-selection-styling` | A selection color set on a wrapper | `::selection` |
| `transition-name-unique` | `.card { view-transition-name: card }` on every card | One name on the active element |
| `transition-name-cleanup` | The source keeps `viewTransitionName` after the swap | Clear it inside the callback |
| `transition-over-js-library` | `layoutId` for a cross-page shared element | `document.startViewTransition` |

## Reporting

**Severity.** `HIGH` is a pseudo-element that never renders because `content` is missing, or a view-transition name that collides. `MEDIUM` is an extra decorative node, a backdrop `div`, a name that is not cleared, or a hit area that was not expanded. `LOW` is an unstyled `::selection` or `::marker` where the rest of the UI is styled.

**Verification.** Read the declared values in the files in scope. A browser is optional. Mark any check you could not run as `Not verified`.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong
```

Then a summary:

| Rule | Count | Severity |
| --- | --- | --- |

`Block` when any `HIGH` remains. `Approve` otherwise, and leave lesser rows in the table. Never `Approve` a file you did not read. With nothing to report, say "No actionable findings" and list what was not verified.
