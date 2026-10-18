---
name: explain-with-storytelling
description: Use when asked to explain visually with storytelling.
---

# Explain with Storytelling

A scroll-driven story: short text steps on the left scroll past one sticky graphic on the right. As each step
reaches the middle, the graphic changes to show it. On phones the kit pins the graphic at the top and the steps
scroll under it. Best for the big picture before the details.

## Use this skill when

- The user asks for a visual explanation of changes with storytelling.
- Used by an orchestrator to explain changes visually with storytelling.

## Story

- 5–7 steps, 1–2 short sentences each, one idea per step. Gloss each tool or term the first time it appears, in a
  few words in the same sentence ("tsgolint, Oxc's type-checking helper,").
- An arc: the situation today → what it costs → the change → the result → the catch → what to do first.
- **One graphic** (one SVG) that evolves through all steps, and **every step changes something visible** on it
  (a bar appears, a value turns red, the counter moves, and the caption line always says what this step shows).
  Not a dashboard of every fact at once, and not a different picture per step.
- **Don't redraw the hero.** The overview already shows the headline numbers; the story shows the thing they are
  about, and draws the catch on it: e.g. one bar per option split into carried over / lost / to fix, or the
  toolchain as boxes that get swapped one by one, with the broken part turning red or struck through.
- It **fills its panel from step 1**: draw the whole frame (labels, empty tracks, axis) at rest and fill it in as the
  story goes, so there is never a small drawing in a large empty panel.
- To scale and honest: bars on one scale share a unit and a base (seconds with seconds; counts out of different
  totals become each one's % of its own total, labelled "263 of 276"). Label things on the graphic itself.
- Don't repeat the overview's numbers in every step, and don't append a details block; it ends when the story ends.

## Build it from this template (no script, no layout CSS)

Copy it and change the labels, values and steps. It is a counter, to-scale rows whose empty tracks show from
step 1, and a caption line that changes every step. Bar width = value ÷ largest × 240 (the track is 240 wide; values sit right of it).

```html
<section class="ev-tab-content" data-tab="story" data-label="Story" data-hint="6 steps" data-part-title="…">
<div class="ev-side ev-side--pin" data-ev-story>
  <div>
    <div class="ev-step" id="story-today" data-toc="Today"><b>Today:</b> one or two sentences.</div>
    <div class="ev-step">…</div>  <!-- one per step; first step of each scene gets id + data-toc -->
  </div>
  <div class="ev-stick"><figure class="ev-visual"><svg class="ev-svg" viewBox="0 0 440 320" role="img" aria-label="…">
    <text x="20" y="62" class="ev-t-num" data-say="38 s||6 s|4 s||6 s">38 s</text>
    <text x="20" y="92" class="ev-t-muted" data-say="Build today (Webpack)|step 2 caption|…|…|…|…">Build today (Webpack)</text>  <!-- one caption per step -->
    <!-- row: label, empty track (always shown), bar (shown from its step), value right-aligned -->
    <text x="20" y="139">Webpack</text>
    <rect x="100" y="122" width="240" height="24" rx="4" class="ev-f-sunken"/>
    <rect x="100" y="122" width="240" height="24" rx="4" class="ev-f-line" data-hl="1,2"/>
    <text x="420" y="139" text-anchor="end" class="ev-t-b">38 s</text>
    <text x="20" y="183">Vite</text>
    <rect x="100" y="166" width="240" height="24" rx="4" class="ev-f-sunken"/>
    <rect x="100" y="166" width="38" height="24" rx="4" class="ev-f-acc" data-on="3-" data-hl="3"/>
    <text x="420" y="183" text-anchor="end" class="ev-t-b" data-on="3-">6 s</text>
    <!-- … one row per thing compared, 44 px apart … -->
    <line x1="20" y1="252" x2="420" y2="252" class="ev-wire"/>
    <text x="20" y="284" class="ev-t-risk" data-on="5">! the catch, in a few words</text>
    <text x="20" y="284" class="ev-t-new" data-on="6">✓ the first step to take</text>
  </svg></figure></div>
</div>
</section>
```

- The kit wires `data-ev-story`: for step n it sets `data-step="n"` on the panel and, inside it, shows
  `data-on` elements only on their steps (`2-4`, `3-` = from 3 on, `2,5`), adds `.is-hl` on `data-hl` steps and
  sets `data-say` text to the n-th item (`a|b||d`; an empty item keeps the previous text). Step 1's state is what
  the page shows at rest; scrolling back restores states exactly. Add a scoped `<style>` keyed on
  `[data-step="3"]` only for what the attributes can't express.
- Fills: `ev-f-acc` the point, `ev-f-new` good, `ev-f-risk` bad, `ev-f-line` neutral, `ev-f-sunken` empty track.
  For a flow instead of numbers, use boxes (`<rect class="ev-node">` + `is-acc|is-new|is-risk`) joined by
  `ev-wire` lines, in the same frame-first way.
- Text: `ev-t-num` only for the one counter; labels at the default size (15) or `ev-t-sm`; nothing below `ev-t-xs`.
  Keep `viewBox` about 440 × 320 so it stays legible when pinned on a phone.
- `ev-side--pin` spaces the steps and pins the graphic on phones; don't add padding, spacers or media queries.
