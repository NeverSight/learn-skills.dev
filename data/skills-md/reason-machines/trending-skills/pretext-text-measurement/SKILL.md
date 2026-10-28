---
name: pretext-text-measurement
description: Fast, accurate, DOM-free text measurement and layout library for JavaScript/TypeScript supporting multiline, rich-text, and variable-width layouts.
triggers:
  - measure text without DOM
  - calculate paragraph height
  - text layout without reflow
  - multiline text measurement
  - wrap text in canvas
  - pretext text library
  - layout text around image
  - shrinkwrap text width
---

# Pretext Text Measurement & Layout

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Pretext is a pure JavaScript/TypeScript library for fast, accurate, DOM-free multiline text measurement and layout. It avoids `getBoundingClientRect` and `offsetHeight` (which trigger expensive layout reflows) by implementing its own measurement logic using the browser's font engine as ground truth.

## Installation

```sh
npm install @chenglou/pretext
```

## Core Concepts

- **`prepare()` / `prepareWithSegments()`** — one-time analysis: normalize whitespace, segment text, measure via canvas. Cache and reuse this result.
- **`layout()` / `layoutWithLines()` etc.** — cheap hot path: pure arithmetic over cached widths. Call this on every resize, not `prepare()`.
- **Font string format** — same as `CanvasRenderingContext2D.font`, e.g. `'16px Inter'`, `'700 18px "Helvetica Neue"'`.

## Use Case 1: Measure Paragraph Height (No DOM)

```ts
import { prepare, layout } from '@chenglou/pretext'

// One-time per unique (text, font) combination
const prepared = prepare('AGI 春天到了. بدأت الرحلة 🚀', '16px Inter')

// Cheap — call on every resize
const { height, lineCount } = layout(prepared, containerWidth, 20)
// height: total pixel height; lineCount: number of wrapped lines
```

### With Pre-wrap (textarea-like)

```ts
const prepared = prepare(textareaValue, '16px Inter', { whiteSpace: 'pre-wrap' })
const { height } = layout(prepared, textareaWidth, 24)
```

### With CJK keep-all

```ts
const prepared = prepare(cjkText, '16px NotoSansCJK', { wordBreak: 'keep-all' })
const { height, lineCount } = layout(prepared, 300, 22)
```

## Use Case 2: Manual Line Layout

### Get All Lines at Fixed Width

```ts
import { prepareWithSegments, layoutWithLines } from '@chenglou/pretext'

const prepared = prepareWithSegments('Hello world, this is Pretext!', '18px "Helvetica Neue"')
const { lines, height, lineCount } = layoutWithLines(prepared, 320, 26)

// Render to canvas
lines.forEach((line, i) => {
  ctx.fillText(line.text, 0, i * 26)
})
// line shape: { text: string, width: number, start: LayoutCursor, end: LayoutCursor }
```

### Line Stats Without Building Strings

```ts
import { prepareWithSegments, measureLineStats, walkLineRanges } from '@chenglou/pretext'

const prepared = prepareWithSegments(article, '16px Inter')

// Just counts and widths — no string allocations
const { lineCount, maxLineWidth } = measureLineStats(prepared, 320)

// Walk line ranges for custom logic
let widest = 0
walkLineRanges(prepared, 320, line => {
  if (line.width > widest) widest = line.width
})
// widest is now the tightest container that still fits the text (shrinkwrap!)
```

### Natural Width (No Wrap Constraint)

```ts
import { prepareWithSegments, measureNaturalWidth } from '@chenglou/pretext'

const prepared = prepareWithSegments('Short label', '14px Inter')
const naturalWidth = measureNaturalWidth(prepared)
// Width if text never wraps — useful for button sizing
```

### Variable-Width Layout (Text Around Floated Image)

```ts
import {
  prepareWithSegments,
  layoutNextLineRange,
  materializeLineRange,
  type LayoutCursor
} from '@chenglou/pretext'

const prepared = prepareWithSegments(article, '16px Inter')
let cursor: LayoutCursor = { segmentIndex: 0, graphemeIndex: 0 }
let y = 0
const lineHeight = 24
const image = { bottom: 200, width: 120 }
const columnWidth = 600

while (true) {
  // Lines beside the image are narrower
  const width = y < image.bottom ? columnWidth - image.width : columnWidth
  const range = layoutNextLineRange(prepared, cursor, width)
  if (range === null) break

  const line = materializeLineRange(prepared, range)
  ctx.fillText(line.text, 0, y)
  cursor = range.end
  y += lineHeight
}
```

### Iterator API (Fixed Width, With Text Strings)

```ts
import { prepareWithSegments, layoutNextLine, type LayoutCursor } from '@chenglou/pretext'

const prepared = prepareWithSegments(text, '16px Inter')
let cursor: LayoutCursor = { segmentIndex: 0, graphemeIndex: 0 }

let line = layoutNextLine(prepared, cursor, 400)
while (line !== null) {
  console.log(line.text, line.width)
  cursor = line.end
  line = layoutNextLine(prepared, cursor, 400)
}
```

## Use Case 3: Rich Inline Text Flow

For mixed fonts, chips, @mentions, and inline code spans:

```ts
import {
  prepareRichInline,
  walkRichInlineLineRanges,
  materializeRichInlineLineRange
} from '@chenglou/pretext/rich-inline'

const prepared = prepareRichInline([
  { text: 'Ship ', font: '500 17px Inter' },
  { text: '@maya', font: '700 12px Inter', break: 'never', extraWidth: 22 },
  { text: "'s feature", font: '500 17px Inter' },
  { text: 'urgent', font: '600 12px Inter', break: 'never', extraWidth: 16 },
])

walkRichInlineLineRanges(prepared, 320, range => {
  const line = materializeRichInlineLineRange(prepared, range)
  line.fragments.forEach(frag => {
    // frag: { itemIndex, text, gapBefore, occupiedWidth, start, end }
    const item = items[frag.itemIndex]
    ctx.font = item.font
    ctx.fillText(frag.text, x + frag.gapBefore, y)
  })
})
```

### Rich Inline Stats

```ts
import { prepareRichInline, measureRichInlineStats } from '@chenglou/pretext/rich-inline'

const prepared = prepareRichInline(items)
const { lineCount, maxLineWidth } = measureRichInlineStats(prepared, containerWidth)
```

## Common Patterns

### Virtualized List Row Heights

```ts
import { prepare, layout } from '@chenglou/pretext'

// Pre-measure all items before virtualization
const rowHeights = items.map(item => {
  const prepared = prepare(item.text, '14px Inter')
  const { height } = layout(prepared, LIST_WIDTH, 20)
  return height
})
```

### Binary Search for Balanced Text Width

```ts
import { prepareWithSegments, measureLineStats } from '@chenglou/pretext'

function findBalancedWidth(text: string, font: string, maxWidth: number): number {
  const prepared = prepareWithSegments(text, font)
  const { lineCount: targetLines } = measureLineStats(prepared, maxWidth)

  let lo = 1, hi = maxWidth
  while (hi - lo > 1) {
    const mid = (lo + hi) / 2
    const { lineCount } = measureLineStats(prepared, mid)
    if (lineCount <= targetLines) hi = mid
    else lo = mid
  }
  return hi
}
```

### Resize Handler Pattern

```ts
import { prepareWithSegments, layoutWithLines } from '@chenglou/pretext'

// Prepare ONCE per text/font change
let prepared = prepareWithSegments(text, '16px Inter')

function onResize(containerWidth: number) {
  // layout() is cheap — safe to call on every resize event
  const { lines } = layoutWithLines(prepared, containerWidth, 24)
  renderLines(lines)
}

// Only re-prepare when text or font changes
function onTextChange(newText: string) {
  prepared = prepareWithSegments(newText, '16px Inter')
  onResize(currentWidth)
}
```

### Prevent Layout Shift on Dynamic Content

```ts
import { prepare, layout } from '@chenglou/pretext'

async function loadAndRender(containerId: string, width: number) {
  const container = document.getElementById(containerId)!
  const text = await fetchText()

  // Measure BEFORE inserting into DOM — no reflow needed
  const prepared = prepare(text, '16px Inter')
  const { height } = layout(prepared, width, 24)

  // Reserve space first to prevent layout shift
  container.style.height = `${height}px`
  container.textContent = text
}
```

## API Quick Reference

### Use Case 1 (Height Only)

| Function | Description |
|---|---|
| `prepare(text, font, opts?)` | One-time analysis, returns `PreparedText` |
| `layout(prepared, maxWidth, lineHeight)` | Returns `{ height, lineCount }` |

### Use Case 2 (Manual Layout)

| Function | Description |
|---|---|
| `prepareWithSegments(text, font, opts?)` | One-time analysis, returns `PreparedTextWithSegments` |
| `layoutWithLines(prepared, maxWidth, lineHeight)` | Returns `{ height, lineCount, lines[] }` |
| `walkLineRanges(prepared, maxWidth, onLine)` | Calls `onLine` per line, no string allocs |
| `measureLineStats(prepared, maxWidth)` | Returns `{ lineCount, maxLineWidth }` only |
| `measureNaturalWidth(prepared)` | Width if text never wraps |
| `layoutNextLineRange(prepared, cursor, maxWidth)` | Iterator — one range at a time, variable width |
| `layoutNextLine(prepared, cursor, maxWidth)` | Iterator — one line + text at a time |
| `materializeLineRange(prepared, range)` | Range → `LayoutLine` with text string |

### Options

```ts
{
  whiteSpace?: 'normal' | 'pre-wrap'  // default: 'normal'
  wordBreak?: 'normal' | 'keep-all'   // default: 'normal'
}
```

## Troubleshooting

**Text height is wrong / doesn't match browser rendering**
- Ensure `font` string exactly matches your CSS `font` shorthand (weight, style, size, family all matter).
- Ensure `lineHeight` matches your CSS `line-height` in pixels.
- Font must be loaded before calling `prepare()` — use `document.fonts.ready` or `FontFace.load()`.

**`prepare()` is slow on every resize**
- Only call `prepare()` when text or font changes. For resizes, only call `layout()` or equivalent.

**Canvas not available (SSR / Node)**
- Server-side support is listed as "coming soon". For now, this library requires a browser environment (canvas API).

**CJK text not wrapping correctly**
- Try `{ wordBreak: 'keep-all' }` for Korean/Chinese text that should not break mid-word.

**Rich inline items breaking when they should be atomic**
- Add `break: 'never'` to the `RichInlineItem` for chips, mentions, badges.

**Getting widest line for shrinkwrap containers**
- Use `measureLineStats(prepared, maxWidth).maxLineWidth` or walk with `walkLineRanges` and track the max `line.width`.
