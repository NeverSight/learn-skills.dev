---
name: viewports
description: Renders a page at every width, each breakpoint edge, a short landscape phone and 200% text, then reports what overflows, clips or hides.
---

# Viewports

This skill renders one page at a fixed set of widths and heights. It measures each render for sideways scroll, clipped text, small targets and controls that only hover reveals.

## Every width rendered, none inferred

The widths are exact: 320, 375, 768, 1024 and 1440, plus 1px either side of each project breakpoint. A width reasoned from the media queries is a finding. Run it after any layout change and whenever the user names a phone or a width.

Opening the result belongs to `verify`. Alignment inside one render belongs to `alignment`. Safe areas, hit areas and dynamic viewport units belong to `defaults`, and a failure there cites its id.

## 1. Read the breakpoints

Read the breakpoints from the CSS, the Tailwind config or the tokens. Add 1px below and 1px above each one to the fixed widths. A sweep that skips the edges of a breakpoint is `viewports-cross-each-breakpoint`.

## 2. Render each width

Set the viewport through device emulation at each width. Use 320×568, 375×812, 768×1024, 1024×768 and 1440×900. Breakpoint edges render 800px tall. Emulate touch at every width under 1024. Take a full-page screenshot of each. A layout judged from the code is `viewports-render-every-width`.

## 3. Measure each render

Run [overflow.js](overflow.js) through the browser's evaluate call at each width. Treat each result as a candidate until a crop of that width shows it.

The page never scrolls sideways, though a box may scroll inside itself. A 40px sideways scroll at 320 is `viewports-no-sideways-scroll`.

Text is never cut by its box without an ellipsis or a clamp. A button label cut in half at 375 is `viewports-no-clipped-text`. A target under 24px cites `defaults-hit-area`.

## 4. Tap at touch widths

Tap through the page with touch emulated. Row actions, copy buttons and menus that appear on hover need another way to appear. A delete button that shows only on row hover is `viewports-no-hover-only-controls`.

## 5. Shorten the height

Render 812×375, a phone held sideways. Open each dialog, sheet and menu at that size. Content scrolls inside the overlay and its actions stay reachable. A dialog whose `Save` sits below the screen with no scroll is `viewports-short-heights`.

## 6. Double the text

At 1024 wide, set the root font size to 200% and render again. Text wraps and its boxes grow, with nothing overlapping. Labels overlapping their icons at 200% is `viewports-text-zoom`. A layout that cannot grow because sizes are set in `px` gets the same id.

## 7. Report by width

Return one screenshot per width with the overlay numbers, then the findings in the same order. A finding with no width named is `viewports-name-the-width`.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `viewports-cross-each-breakpoint` | Checked at 375 and 1440 only | Also at 767 and 768, 1023 and 1024 |
| `viewports-render-every-width` | "The grid collapses at `md`, so mobile is fine" | Screenshots at 320, 375 and 768 |
| `viewports-no-sideways-scroll` | A `width: 400px` card at 320 | `max-width: 100%` on the card |
| `viewports-no-clipped-text` | `overflow: hidden` cutting a label at 375 | The label wraps, or truncates with a way back |
| `viewports-no-hover-only-controls` | Row actions behind `:hover` alone | Shown at all times under `(hover: none)` |
| `viewports-short-heights` | A dialog's `Save` below a 375px screen | `max-height: 100dvh` with the body scrolling |
| `viewports-text-zoom` | `height: 32px` on a button that clips at 200% | `min-height: 2rem` with padding |
| `viewports-name-the-width` | "The header overlaps" | "At 768, the header overlaps the search field" |

## Reporting

**Severity.** `HIGH` is sideways page scroll, a control that hover alone reveals on touch or an action unreachable at a short height. `MEDIUM` is clipped text, overlap at 200% text or a break at a breakpoint edge. `LOW` is a finding that does not name its width.

**Format.** One finding per root cause, naming the width:

```
1. file:line - [rule-id] at 375, what is wrong (measured values)
```

Cite the script's element when the source line is not found. Then a `Rule | Count | Severity` summary. `Block` when any `HIGH` remains, `Approve` otherwise. Mark any width you could not render as `Not verified`.
