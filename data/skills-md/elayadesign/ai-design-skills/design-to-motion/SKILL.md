---
name: design-to-motion
description: "Turns a static design (a Figma frame, dashboard, card set, app screen, or a UI on a photo background) into a pixel exact HTML replica that loads in from an empty state, then has every visual act out what it does (a chart being read, a list receiving items, a prompt being typed) in a seamless loop, and exports an MP4 for X, a website GIF, and an 800×500 GIF. Use this skill whenever the user asks to animate a design, a Figma link, a screenshot, UI cards, a dashboard, or a hero image, to make a loading or appear animation, a showcase loop, a motion mockup, or a video or GIF of a design, even when they only say \"animate this\". Also use it on landing pages and websites for bento and feature cards that pair text with a visual, and for product or dashboard mockups. Always consult it before exporting layers, choosing what moves, building the intro, writing the visual story loops, or encoding video and GIFs."
---

# Design to Motion

A showcase animation is not a redesign. The viewer must see **the exact design**, and must see that **it is alive**.

**exact frame → empty state → smooth load → every visual acts out its story → seamless repeat.**

This skill has three parts. **Part A** rebuilds the design so the finished frame is indistinguishable from the source. **Part B** is the motion system. **Part C** records and exports. Work through A before touching B, and never encode anything before the checks in A7 and B9 pass. Parts A and B apply in both contexts below; Part C is for the showcase, or for a website only when exports are asked for.

## Scope

Apply to any request to animate a static design: Figma frames, UI cards, dashboards, app screens, marketing heroes, product mockups, and designs placed on a photo background. When a rule here conflicts with a framework default, this file wins. When the user's explicit prompt conflicts with a rule, the user wins.

**Not for** interaction motion inside a shipping product (hovers, menus, toasts). For that, use a product motion skill such as [emilkowalski/skills](https://github.com/emilkowalski/skills). **Companion skill:** `landing-page-design` in this repo, when the animation will live on a landing page.

## Two contexts

Decide the context before anything else. It changes what you animate, how the motion starts and ends, and what you deliver.

| | **Showcase** | **Website** |
|---|---|---|
| Typical request | "Animate this design for me", a Figma link and nothing else | Building or editing a landing page or site, or the request names one |
| What gets animated | The whole frame | Only the sections that qualify (table below) |
| Start | Page load, from the empty state | When the section scrolls into view, once |
| After the intro | Stories run, then the frame dissolves and the cycle repeats (B5) | Stories run forever. No dissolve, no cycle |
| Text | Exported layers, so the frame is pixel exact | Live HTML text in the site's font, for SEO and accessibility. Only the visual parts are exported images or SVG |
| Deliverables | The page plus MP4 for X, website GIF, 800×500 GIF (Part C) | The animated sections inside the site's code. Exports only when asked |

If the request does not say which, look at where you are working: inside a site's codebase, assume website. With only a design and no site, assume showcase. If it is still unclear, ask once.

### Website: which sections get which motion

Scan the page section by section. Apply this skill only where a section has a visual part. Never animate a text section with it.

| Section | Apply |
|---|---|
| Bento and feature sections: cards with text plus a visual (a chart, list, flow, calendar, prompt, player) | Card intro on scroll (B2, `card` kind, text included), then a story loop on each card's visual (B4). This is the main use on a landing page |
| Product or dashboard mockup (a hero shot of the app, a product screenshot) | The loading intro on scroll: surfaces stay, contents load (A5). Then **ask the user** whether they also want stories after loading. Do not add them unasked |
| Logo rows, integrations | A marquee or a gentle light up story |
| Text only sections: headline blocks, testimonials, FAQ, pricing, CTA, footer | Not this skill. Use the page's normal scroll reveal (for example `landing-page-design` B7) |

Website rules:

- **Trigger with `IntersectionObserver`.** Start the intro when about 30% of the section is visible. Play it once. Never use a scroll listener.
- **Pause stories off screen.** Stop the clock when the section leaves the viewport and resume it on return.
- **Stagger by reading order inside the section**, never across the whole page.
- **Respect the site's system.** Use its components, tokens, radii, and fonts. Fidelity to the design still applies (A7), compared section by section.
- `prefers-reduced-motion: reduce` shows each section in its final state with no stories.

---

# PART A — Fidelity

## A1. Intake

Gather these before building. Ask only for what is missing, and ask in one batch.

- **Context.** Showcase or website (see "Two contexts"). Decide this first.
- **Source.** A Figma link with a node id is best. A flat image works, but its layers cannot be separated perfectly (see A2).
- **Layout.** Decide it yourself from the tree (A5): an **app frame** (a dashboard or app screen built from joined surfaces, such as a sidebar and a body) or **separate cards** (a bento grid, a card set, widgets). The two load differently.
- **Background.** Is there a photo or texture behind the UI? Assume it must stay exactly as designed.
- **Visuals.** Which parts are visuals that should act out a story after load (B4)? Assume every chart, list, stack, calendar, flow, prompt, photo, media control, and status indicator.
- **Deliverables.** Showcase: default to all three, MP4 for X, website GIF, 800×500 GIF. Website: the animated sections in the site's code, with exports only when asked.
- **Camera.** Assume no zoom and no pan (B7).

If the user cannot answer, make a reasonable assumption, state it in one line, and continue. On the first design of a session, show the live page before recording exports, so the direction can be corrected cheaply.

## A2. Source of truth

**Figma.** Use the REST API with a personal access token.

- Read the token from a secure store (an environment variable or the OS keychain). Never print it, echo it, paste it into chat, or commit it.
- `GET /v1/files/:key/nodes?ids=:node&geometry=paths` gives the tree, bounds, fills, effects, and radii.
- `GET /v1/images/:key?ids=:node&format=png&scale=2` renders the **reference frame**. The finished still must match this image (A7).
- Note the frame's absolute origin. Every layer position is `absolute bounds − origin`.
- The image URLs the API returns point at a CDN that sometimes resets connections. Retry every download, and check each PNG's size before using it.

**Flat image only.** The image is the reference. Rebuild what you can isolate, and tell the user plainly which parts cannot be separated before you animate them. Never fake fidelity by animating a screenshot as one block.

## A3. Layer export

Export every element that will move as its own PNG at **3x** through `/v1/images`, batched 20 to 25 ids per call.

| Case | Placement |
|---|---|
| PNG size equals `absoluteRenderBounds` (text layers always do) | Place at the render bounds |
| PNG larger than the render bounds (a parent clipped it), effects that overhang evenly | `x = bbox.x − (pngW − bbox.w) / 2`. Use `renderBounds.y` when the top was not clipped, otherwise derive it from the effect radius and offset |
| Overhang that is not even (a line with an arrowhead, a stroke with one square cap) | Take the bounds of `strokeGeometry` or `fillGeometry` from the `geometry=paths` response instead of the formula |
| Rotated vectors with a large layer blur (soft colour blobs) | Export with `use_absolute_bounds=true` and place at the bounding box. Run a PSNR offset search against the reference only if that region scores below about 45 dB. Blobs can be stored at 1x; the loss is invisible |
| Zero height or zero width stroked vectors | `use_absolute_bounds=true` returns null for them. Export without it |
| Mask group with blurred content | Anchor on the edge that was not clipped (usually the bottom of the mask plus its stroke) |
| Arcs, donuts, partial ellipses | Export with `use_absolute_bounds=true` |
| Patterns or overlays far larger than their surface | Export with `use_absolute_bounds=true`, then crop to the surface rectangle |
| Instance children (ids like `I12:34;56:78`) | They often return null. Export the parent instance |
| Lines that should draw on, dashed or not | Figma outlines strokes into filled shapes, so there is no centerline to animate. Write the centerline yourself and use it as a mask over the exported PNG (example below) |
| A photo baked inside a larger exported layer | Export the photo node on its own as well. Cover the baked photo with a skeleton, and put the separate photo layer on top for the `photo` resolve. At rest it must equal the reference |

Rules that keep the frame exact:

- **Text stays an exported layer in a showcase.** Never retype it in HTML there: fonts, kerning, and line metrics will not match. On a website, text is live HTML (see "Two contexts").
- **Keep Figma's z order.** Static layers can sit between animated ones in the same order the tree has them.
- **Frame strokes usually draw above children.** Render a card's stroke as a separate overlay above its clipped content, then confirm against the reference: a glow inside the card can tint the stroke in Figma's render.
- **Containers whose children move on their own.** The API always exports a frame together with its children, so exporting a card or panel bakes in everything inside it. When its children must load or act separately, rebuild the container in CSS from the node data: fills, corner radii, inside strokes (including `individualStrokeWeights`), and effects. Then export each child separately.
- **Shadow mapping.** A Figma drop shadow with blur `R` is a CSS `box-shadow` with blur `R` on a single element, or `filter: drop-shadow()` with blur about `R / 2` on a group. Both give the same Gaussian. Verify against the reference.
- **A group shadow is the shadow of the union.** When a drop shadow sits on a group of joined surfaces (an app frame), put all surface shapes in one static container with `filter: drop-shadow()`. Per element `box-shadow` would darken neighbours where surfaces overlap. Separate cards each carry their own shadow inside their `card` unit, so the shadow moves with the card.
- **Skip hidden layers** (`visible: false`) and stray layers buried under opaque shapes.

**Drawing a line on.** Read the corner points and arc radii from the outline in `strokeGeometry`: the centerline sits halfway across the stroke width, and a rounded corner's centerline radius is the outline's inner radius plus half the stroke. Most UI connectors are straight runs and arcs, so the path is short:

```html
<svg class="ly" viewBox="0 0 1440 990" style="left:0;top:0;width:1440px;height:990px">
  <mask id="draw1">
    <path d="M193 832 V700 A45 45 0 0 1 238 655 H380" fill="none" stroke="#fff" stroke-width="8"
          pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
  </mask>
  <image href="data:image/png;base64,..." x="192" y="653" width="190" height="181" mask="url(#draw1)"/>
</svg>
```

Animate `stroke-dashoffset` from 1 to 0 on the JS clock. `pathLength="1"` means no length measuring, and the wide mask stroke covers the line's antialiasing. For pulses that travel along it, read positions with `getPointAtLength` on the same path.

## A4. Background (sacred)

When the design sits on a photo or texture, the background is part of the design, not decoration. Often the whole canvas outside the app frame is background.

- **It never changes.** Not in the intro, not in the loop, not in the dissolve, not in any zoom. It never moves, blurs, scales, fades, or recolours.
- **Every version keeps it.** A "loading only" or "no zoom" variant is still the same design on the same background. Never drop the photo to make a variant simpler.
- **Export the original image, not a render.** `GET /v1/files/:key/images` returns the raw image fills. Apply the fill's scale mode and `imageTransform` as CSS: for a stretch fill with a transform, `background-size` is the frame size divided by the transform scale, and `background-position` is the negative offset.
- **Verify it.** Compare the background region of your still against the reference. Aim above 45 dB PSNR. A crop or offset error shows up instantly.
- **Frosted panels must see the photo.** A surface with `backdrop-filter: blur()` is its own element, a sibling above the background, never inside an ancestor that has `filter` or `opacity` below 1. Headless Chrome only renders it with `transform: translateZ(0)` and a `z-index` on that element.
- **If you cannot reproduce it, say so before building.** No image access, a generated texture, a missing fill: tell the user and ask. Never swap in a flat colour silently.
- Store photos as high quality JPEG or WebP, not PNG.

## A5. Layout: app frame or separate cards

Decide which of the two layouts the design is. It changes what the empty state contains and what moves.

**App frame (joined surfaces).** A dashboard or app screen whose frame is built from two or more surfaces joined into one unit: a sidebar and a body, often overlapping by a few pixels. Only this layout gets static surfaces.

- **The surfaces exist in the empty state.** The sidebar and body are in place, fully opaque, and still from the first frame. They never fade, slide, scale, or blur in. Only the elements inside them load.
- **Keep Figma's stacking where they meet.** The body sits above the sidebar's content clip, so sidebar content can never draw over the body, and the body never slides over the sidebar.
- Cards inside the body are content: they load like any other element.

**Separate cards (bento, card sets, widgets).** Cards that stand apart from each other with gaps between them. These are **not** joined surfaces.

- **The cards themselves load in.** Each card rises in with blur (the `card` kind in B2), staggered in reading order, and its contents follow inside it.
- The empty state is the background alone.

**Both layouts:**

- **Each container clips its own contents** to its exact shape, including per corner radii. Nothing may overflow onto a neighbour or the background.
- **Image shaped surfaces.** When a container's silhouette is a photo (a cover header, a full bleed card image), give it a placeholder in the image's average colour. The photo then loads into it.
- **Nested content is content.** Trays, toolbars, and inner panels load like any other element.

Clip pattern, which keeps stage coordinates valid inside the clip. For separate cards, the card's unit wraps its clip, so the card and its contents move together:

```html
<div class="clip" style="left:113px;top:138px;width:305px;height:907px;border-radius:16px 0 0 16px">
  <div class="cin" style="left:-113px;top:-138px"><!-- units in stage coordinates --></div>
</div>
```

```css
.clip { position: absolute; overflow: hidden; isolation: isolate; }
.cin  { position: absolute; width: var(--stage-w); height: var(--stage-h); }
```

## A6. Page architecture (showcase)

On a website, build inside the site's code instead, following the website rules in "Two contexts". The clock, units, and modes below still apply per section.


- One self contained HTML file: a fixed size stage at the frame's exact size, scaled to fit the viewport. Images inline as base64, deduplicated when the same image repeats. Wait for decode on `<img>` elements only; CSS gradients are not images.
- **Modes:** `?still` renders the exact Figma frame with no motion (also used for reduced motion). `?loop` repeats the cycle like the exports. `?capture` turns off `requestAnimationFrame` and exposes `window.__start()`, `window.__tick(dt)`, and the loop time `window.__lt`, so the recorder drives the clock (C1).
- **Units.** Every animated element is wrapped in a full stage layer `.u` carrying its delay `--d`. The intro is CSS transitions keyed on `.stage.in`. Because a unit covers the whole stage, any percentage in `clip-path` or `transform-origin` on it refers to the stage, not the element. Use pixel values computed from the element's rectangle.
- **Static layers stay composited.** Give clips and stroke overlays `transform: translateZ(0)`, so their antialiasing does not change when nearby transitions start. Otherwise a 1px edge flickers at every cycle start.
- **One JS clock** (`requestAnimationFrame`) drives everything time based: masks, sweeps, stories, accents. Drive it from loop time, never from wall clock, so capture is deterministic. In `?capture` the clock advances only through `__tick`.
- Default page behaviour: wait for image decode, play the intro once (when the frame scrolls into view, if it sits on a longer page), then keep the stories running.

## A7. Verify the still

Render `?still` at 2x and compare it with the reference before any motion work.

- PSNR for the whole frame and for each container, after a light blur (`gblur sigma≈1.2`) so sub pixel antialiasing does not dominate. Aim above 35 dB overall and above 30 dB per container. Text heavy containers sit near 30 dB because 3x layers are resampled to 2x; if one is lower, retest it at `sigma≈2.5`, where text edges stop counting and only structure remains.
- Look at a blurred, amplified difference image. It reveals structural errors: a glow placed too high, wrong stacking, a missing stroke, a shifted shadow.
- **Do not chase sub pixel offsets.** Measuring at 2x cannot resolve errors under half a pixel, and "corrections" overshoot. Fix structure, not antialiasing.

---

# PART B — Motion system

Every timing, distance, and curve below comes from the values in **Make it yours**. Never invent ad hoc values.

## B1. Start empty

The first frame of every page load and every export is the **empty state**. Empty becomes loaded. Never open on the finished frame.

- **App frame:** background plus the static joined surfaces, nothing else.
- **Separate cards:** the background alone.

## B2. Loading choreography

The appear animation is smooth, slow, and soft: elements **rise from below and resolve from blur to sharp**, staggered.

| Kind | Use for | From |
|---|---|---|
| `card` | Separate cards (bento, card sets) as a whole, with their shadow | `translateY(24px)`, `scale(0.985)`, `blur(6px)`, opacity 0 |
| `up` | Text, headers, values, rows | `translateY(10px)`, `blur(4px)`, opacity 0 |
| `down` | Top toolbars, top bars | `translateY(-8px)`, `blur(4px)` |
| `left` | Sidebar items, list rows, labels | `translateX(-10px)`, `blur(4px)` |
| `pop` | Icons, badges, avatars, buttons, dots | `scale(0.82–0.88)` from the element's own center, `blur(4px)` |
| `photo` | Images | skeleton shimmer first, then `blur(14px) saturate(0.6)` to sharp. For a photo baked into a bigger layer, see A3 |
| `wipe` | Bars, fills, highlights | A left to right `clip-path` reveal in pixels on the full stage unit (A6). The right inset starts at `stageW − x` (zero width, so no sliver shows) and ends at `stageW − (x + w)` (the element fully shown). Top and bottom insets stay at `y` and `stageH − (y + h)` |
| `line` / `grow` | Rules, ticks, timelines | `scaleX(0)` / `scaleY(0)` from their start edge |
| `donut` | Rings, gauges | conic mask sweeping clockwise from 12 o'clock |
| `tray` / `rise` | Sheets, trays, folders | slide up 40px from inside the container's bottom edge, clipped by it |
| `fade` | Layers that sit under another layer | opacity only |

- **Order.** Containers load in reading order, 80 to 90ms apart: for an app frame, the regions inside its static surfaces; for separate cards, the cards themselves, each starting about 0.15s before its own contents. Inside a container: header, then labels, then values, then visuals. Items in a group stagger 30 to 80ms.
- **Never `scale(0)` on an object.** Only lines and bars grow from zero, because they draw.
- **Covered layers arrive last and leave first.** Anything hidden under another layer in the final frame (calendar weeks under a meeting tray) appears after its cover lands and exits faster in the dissolve, so it never ghosts through.
- **Skeletons match the real shape** and sit 1px inside it, so no halo shows around the loaded image.
- Total intro: about 2 to 2.5 seconds for a full frame.

## B3. Bars fill like progress

- **Data bars, meters, and highlights fill like progress bars**: a left to right `clip-path` wipe with the in out curve, 0.7 to 1.1s.
- **Never add loading lines.** No progress line along a card's or surface's top edge, and no other bar or rule that is not in the design. Only shapes that exist in the design animate.

## B4. Story loops (the main act)

The intro is only the opening. The main act is every visual **acting out what it does**, on a loop: a lead list receives new leads, a chart is being read, a calendar finds an open slot, a prompt gets typed. When a user says "animate the visuals", this is what they mean. A frame that only loads in and then sits there with a few pulses is not finished.

**Write the story first.** For each visual, name its story in one sentence before building, for example "a new lead lands on top and the older ones settle back". Pick from this table, or invent one in the same spirit.

| Visual | Story |
|---|---|
| Stack of items (leads, notifications, files) | A new item lands on top with a blur, the others step back one slot, the last one leaves |
| Line or area chart | A scrubber glides across, dots ride the curves, the tooltip value counts. Or: the line redraws, a marker pops, the numbers count up with it |
| Bar chart, equalizer, grid of cells | Bars breathe like a live feed and settle back to the design heights. A dot and tooltip ride the active bar |
| Donut, gauge | Segments ease outward one at a time and back. Or: the ring sweeps again clockwise |
| Table, list | A cursor inspects rows one by one, the row highlights, and a preview loads for it. Or: a soft highlight steps down the rows |
| Calendar, scheduler | A highlight searches for an open slot, the event glides into it, then back |
| Flow, connectors, pipeline | Pulses travel along the connectors in the flow direction, and nodes or avatars light up as a pulse passes. Dashed lines march |
| AI, prompt, form | The prompt deletes and retypes, chips evaluate one by one, then the result appears with a blur |
| Counters, KPIs | Numbers count up together with the chart that drives them |
| Profile, long content | The content scrolls slowly inside its clip, then returns |
| Logo row | A continuous marquee that moves exactly one full set per loop, so it repeats seamlessly |
| Media player | The playback handle and progress advance while the play button pulses |

**Rules for stories**

- **Start and end on the exact design.** Each story leaves the Figma frame, acts, and comes back to it. At rest, the frame equals `?still`.
- **Use the design's own elements.** Cards, rows, bars, dots, chips, and tooltips from the design. Helpers the story needs (a cursor, duplicate stack items, extra pulses) must match the design's style, and are hidden in `?still`.
- **Changing text only when it is the point.** Counters, typing, and tooltip values. All other text stays still.
  - **Typing** reveals the exported text layer glyph by glyph, never as a smooth wipe. Find the glyph boundaries from the empty alpha columns of the text PNG, step the reveal one glyph every 45 to 70ms, and show a caret at the edge that blinks once a second while idle. Deleting runs the same steps backwards, a little faster.
  - **Counters** need live text in the design's font at the exact size and weight, landing on the design's exact text at rest.
- **Obvious, not busy.** Every card with a story shows a clear action every one to two seconds. A story is made of beats (a pulse leaves, a node lights, the arrow fires), and its beats provide that rhythm. If a viewer cannot tell the frame is animated within two seconds, the stories are too timid ("make more movement"). Calm screens, such as a document dashboard, may rest after load if the user prefers. Ask once.
- **Text only cards get no story** in a showcase. They rise in with their card and rest. Not every card needs to move; every visual does.
- **Readable at the smallest export.** A story must still be visible in the 800×500 GIF. If a moving element is smaller than about 4px there (a pulse dot, a thin line), enlarge it within the design's style, add a halo, or pick a bigger story.
- **Offset the cards.** Cards never act in unison. Shift each card's story so attention travels around the frame in reading order.
- **One story per card, three to eight seconds long. A short story may repeat** within one cycle (twice in the 8.6s story phase is common), and a second run can vary a beat. Every run still ends at rest before the dissolve.
- Stories are built from eased keyframe tracks on the JS clock (A6), so capture stays deterministic:

```js
// [[time, value], ...] eased per segment; values may be numbers or arrays
function track(keys, t, ease = easeInOut) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) {
    const [t1, v1] = keys[i], [t0, v0] = keys[i - 1];
    if (t <= t1) {
      const k = ease(Math.min(1, (t - t0) / (t1 - t0 || 1)));
      return Array.isArray(v0) ? v0.map((v, j) => v + (v1[j] - v) * k) : v0 + (v1 - v0) * k;
    }
  }
  return keys[keys.length - 1][1];
}
// a slot that scrubs along a curve and returns to its design position
slot.style.transform = `translate(${track([[0, [0, 0]], [1.2, [46, -18]], [2.6, [46, -18]], [3.8, [0, 0]]], t).join('px,')}px)`;
```

**Accents** sit on top of stories, never instead of them:

| Accent | Use for | Values |
|---|---|---|
| Pulse ring | Status dots, live indicators, play buttons | 1.8–2.2s period, ring scale 1 → 2.6, opacity 0.55 → 0 |
| Heartbeat | Hearts, likes, sparkles | +20% over 0.35s, every 3s |
| Gentle bob | Floating objects (folders, devices, cards inside cards) | ±2.6px, 2.8s sine |
| Sheen sweep | Photos, bars, buttons | A band 38% of the element's width, peaking at 34% white, 1.5s pass every 3.4s. On light grey shapes it disappears; use a refill story instead |
| Skeleton glimmer | Placeholder lines inside the design | 2.4s shimmer |

- Stories and accents start when the intro has landed (about 2.4s). Stories begin from the exact design, so they need no fade. Accents and added helpers fade in over 0.6s.

## B5. The loop cycle (showcase)

On a website there is no cycle: the intro plays once on scroll and the stories run until the section leaves the viewport.


| Phase | Default timing |
|---|---|
| Build in | 0 → 2.4s |
| Stories | 2.4 → 11.0s |
| Dissolve | 11.0 → 11.6s (opacity 0.5s) |
| Empty beat | 11.6 → 12.0s |

- **The story phase holds at least one full story of every card.** Lengthen the cycle rather than cutting a story short. Time the stories so every card is back at rest when the dissolve starts.
- **The live page keeps telling stories forever** after its intro. Only `?loop` and the exports dissolve and restart.
- **Dissolve back to the empty state (B1).** For an app frame, only the contents dissolve and the joined surfaces stay. For separate cards, the cards dissolve too. The background never dissolves.
- **Reset everything.** A class that disables transitions for one frame resets the CSS, but every JS driven value (masks, tracks, helpers, typed text, pulses) must be set back to its empty state too, or it ghosts through the empty beat. The frame at the end of a cycle must equal the frame at its start.

## B6. Easing and duration

Never use default `ease` or `linear` for entrances.

| Token | Curve | Use |
|---|---|---|
| `--e` | `cubic-bezier(0.16, 1, 0.3, 1)` | Transforms on entrance (1.05s) |
| `--e2` | `cubic-bezier(0.33, 1, 0.68, 1)` | Opacity and blur (0.7–0.8s) |
| `--io` | `cubic-bezier(0.65, 0, 0.35, 1)` | Wipes, fills, sweeps, camera moves |
| linear | `linear` | Constant motion only (shimmer, playback) |

Showcase timing is slower than product UI timing on purpose. Product rules like "under 300ms" do not apply here; slow and smooth is the brief.

## B7. Camera

- **No zoom and no pan** by default. The user has to ask for it.
- When asked: only the app frame scales toward the items, the background never moves (A4), moves use `--io`, and the frame returns to its resting position before the dissolve.

## B8. Performance and accessibility

- Animate `transform`, `opacity`, `filter`, and `clip-path` only. Never `top`, `left`, `width`, or `height`.
- Keep animated blur at 14px or less. Static `backdrop-filter` is fine.
- `prefers-reduced-motion: reduce` renders the still frame.
- CSS transitions for the intro, the JS clock only for time based effects.

## B9. Motion checks

Run these on the recorded frames (C1) before encoding.

- **Overflow check.** Test with the containers' real shapes, rounded corners included, not rectangles: render a mask from the page itself (every container as a solid white shape with its exact radii on black, plus its shadow area if it has one), grow it by 2px to skip antialiasing, and compare only the black pixels. Any `?still` used for comparison here is rendered at the capture's device scale factor, not at the 2x of A7.
  - **App frame:** every pixel outside the joined surfaces must be identical to the empty first frame in every frame of the cycle (PSNR `inf`).
  - **Separate cards:** during the story phase, every pixel outside the cards (and their shadows, when they have any) must be identical to the `?still` frame, so no story, helper, or content escapes its card. The intro frames are excluded, because the cards' own rise moves pixels there; the contact sheet must show contents moving with their card, never ahead of it or outside it.
- **Seam check.** The first frame of the export window equals the frame one cycle later.
- **Empty beat check.** Every frame of the empty beat equals the frame before `__start`. The seam check cannot catch JS state that failed to reset, because both its frames are at loop time 0; this one can.
- **Rest check.** The last frame before the dissolve equals `?still` at the capture scale, proving every story came back to the design.
- **Contact sheet.** Tile frames at key moments (empty, mid intro, landed, several points through the stories, mid dissolve, end) and look for overflow, ghosting, pops, and stories too timid to notice.

---

# PART C — Recording and export

## C1. Deterministic capture

Never screen record in real time. Step a fake clock and screenshot every frame. Three details decide whether the loop is smooth and the seam is clean; all three are in the snippet.

```js
await page.clock.install({ time: 0 });
await page.goto(url + '?capture', { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
await page.clock.pauseAt(10000);
const loopTime = [];
for (let i = 0; i < frames; i++) {
  // 1. whole milliseconds that average exactly 1000/60 (17, 17, 16, ...); runFor(1000 / 60) drifts
  const dt = Math.round((i + 1) * 1000 / 60) - Math.round(i * 1000 / 60);
  await page.clock.runFor(dt);
  loopTime.push(await page.evaluate(([i, PRE, dt]) => {
    if (i === PRE) window.__start();          // 2. start inside the same evaluate as the seek
    if (i >= PRE) window.__tick(dt / 1000);   // 3. the page clock advances here, never through rAF
    const now = performance.now();
    for (const a of document.getAnimations()) {  // CSS transitions follow the fake clock
      a.__m ??= window.__mark;                    // each one keeps the mark it was created under
      a.pause(); a.currentTime = Math.max(0, now - a.__m);
    }
    return i >= PRE ? window.__lt : 0;
  }, [i, PRE, dt]));
  await page.screenshot({ path: `${out}/${String(i).padStart(5, '0')}.png` });
}
```

On the page side, in `?capture`:

- `__start()` adds the `in` class. Every change of the stage's state classes (`in`, `out`, the reset) sets `window.__mark = performance.now()`, so each transition is seeked from the moment it was created. Transition delays (`--d`) are counted inside `currentTime`.
- `__tick(dt)` advances the loop time, runs the cycle phases (B5), draws every story and accent, and sets `window.__lt`.
- Loops that never end (shimmer, marquee) are driven by the JS clock, not by infinite CSS keyframes, which the seek would restart.

`PRE` is a few frames (about 15) recorded before the start, so the page has settled. Save `loopTime` beside the frames.

- Viewport is the frame size. `deviceScaleFactor = min(1920 / W, 1200 / H)` so the long side hits the X limit. Screenshots round to whole pixels and can come out one pixel odd (1745×1200 for a 1440×990 frame); the MP4 crop to even dimensions takes care of it, so expect 1744×1200.
- **The export window** starts at frame `PRE − 1` (loop time 0, the empty state) and spans exactly `cycle × 60` frames. Record at least 10 frames past it for the seam check.

## C2. Formats

| File | Spec |
|---|---|
| `<name>-x.mp4` | H.264, `yuv420p`, 60fps, CRF 14–15, preset slow, `+faststart`, max 1920×1200, even dimensions |
| `<name>-loop.gif` | 960px wide, 15–20fps, about 2 to 3MB, for the website |
| `<name>-800x500.gif` | Always delivered. When the frame has wide empty borders (most card and bento frames), crop to the content with about 40px of margin at exactly 1.6:1. When the content fills the frame, fit it and pad with the page background colour. On a photo background, always crop, so no flat band sits beside the photo. 20fps, 12fps if heavy |

```bash
ffmpeg -start_number $A -framerate 60 -i frames/%05d.png -frames:v $N \
  -vf "crop=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -preset slow -crf 15 \
  -pix_fmt yuv420p -movflags +faststart name-x.mp4

ffmpeg -start_number $A -framerate 60 -i frames/%05d.png -filter_complex \
  "trim=end_frame=$N,fps=20,scale=960:-2:flags=lanczos,split[a][b];\
   [a]palettegen=max_colors=192:stats_mode=diff[p];\
   [b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle" -loop 0 name-loop.gif
```

For the 800×500 GIF, add `scale=800:500:force_original_aspect_ratio=decrease,pad=800:500:(ow-iw)/2:(oh-ih)/2:color=<page bg>` before `split`.

- Keep bayer dithering whenever a photo is in frame; without it photos band.
- If a GIF is too heavy, lower the frame rate or colours before lowering the size.

---

# Output format

Before building, state in a few lines:

1. **Context** — showcase or website. For a website, list each section and what it gets (intro and stories, intro only, or nothing)
2. **Layout** — app frame (which joined surfaces stay static) or separate cards (which cards rise in), and the clip shapes
3. **Background** — kept exactly, or what cannot be reproduced
4. **Choreography** — load order and the kind per element group
5. **Stories** — one sentence per visual saying what it acts out, plus any accents
6. **Cycle** — total length and phases

After building, report:

- Still frame fidelity (overall and worst surface PSNR)
- Overflow check and seam check results
- The three files with size, dimensions, frame rate, and duration
- Anything not reproduced exactly, named plainly

---

# Make it yours

Every motion and export value lives here. Edit this section and the rest of the skill follows.

| Value | Default |
|---|---|
| Rise distance | 10px (`up`), 8px (`down`), 10px (`left`) |
| Entrance blur | 4px, photos 14px |
| Pop start scale | 0.82–0.88 |
| Transform duration | 1.05s with `--e` |
| Opacity and blur duration | 0.7–0.8s with `--e2` |
| Wipe duration | 0.7s, slow bars 1.1s, with `--io` |
| Card rise | 24px, `scale(0.985)`, `blur(6px)`, 0.9s transform with `--e`, 0.6s opacity |
| Container stagger | 80–90ms |
| Tray and folder rise | 40px |
| Typing | one glyph every 45–70ms, caret blink 1s |
| Item stagger | 30–80ms |
| Story start | 2.4s |
| Story length | 3–8s per card, offset between cards |
| Cycle | 12s (dissolve at 11.0s, reset at 11.6s), longer if a story needs it |
| MP4 | 60fps, CRF 15, max 1920×1200 |
| Website GIF | 960px wide, 20fps |
| Small GIF | 800×500, 20fps |

---

# Quick checklist

**Fidelity**
- [ ] Reference frame rendered from the source
- [ ] Every moving element exported as its own layer, text included
- [ ] Figma z order kept, strokes above children, group shadow on the union
- [ ] Background is the original image, positioned by its transform, verified by PSNR
- [ ] Every variant keeps the background, frosted panels blur the photo behind them
- [ ] Still frame matches the reference (no structural differences)

**Context and layout**
- [ ] Context decided: showcase, or website with each section mapped (text only sections untouched)
- [ ] Website mockups: asked the user before adding stories after the loading intro
- [ ] Layout identified: app frame with joined surfaces, or separate cards
- [ ] App frame: joined surfaces present, opaque, and still in the empty state, Figma stacking kept where they meet
- [ ] Separate cards: cards rise in themselves, empty state is the background alone
- [ ] Each container clips its own contents with its exact radii
- [ ] Overflow check passes for the layout type

**Motion**
- [ ] Exports and page load start on the empty state
- [ ] Rise plus blur to sharp intro, staggered in reading order
- [ ] Bars fill like progress bars, no added loading lines or shapes that are not in the design
- [ ] Every visual acts out a story after load, starting and ending on the exact design; text only cards rest
- [ ] Stories stay visible in the 800×500 GIF
- [ ] Stories are obvious, offset between cards, and only counters or typing change text
- [ ] Covered layers arrive last and leave first
- [ ] No zoom or pan unless asked, background never moves
- [ ] Dissolves back to the empty state, background untouched
- [ ] Seam, empty beat, and rest checks pass

**Export**
- [ ] Deterministic frame capture: whole millisecond steps averaging 1000/60, start and tick inside the seek, no real time recording
- [ ] `<name>-x.mp4`, `<name>-loop.gif`, `<name>-800x500.gif` delivered
- [ ] Token never printed or committed

---

# Credits

Part of [ai-design-skills](https://github.com/elayadesign/ai-design-skills) by Elaya, MIT licensed.

A few general motion rules were adapted, not copied, from these MIT licensed skill collections:

- [emilkowalski/skills](https://github.com/emilkowalski/skills) — animating only cheap properties, keeping blur small, never growing objects from zero, reduced motion handling
- [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills) — skeletons shaped like the real content, staggered entrances
- [dylantarre/animation-principles](https://github.com/dylantarre/animation-principles) — offsetting sibling loops, loops whose last frame flows into the first
