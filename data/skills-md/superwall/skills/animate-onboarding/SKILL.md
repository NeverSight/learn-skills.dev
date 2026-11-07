---
name: animate-onboarding
description: "Animate a tap-through onboarding or web funnel (quiz, survey, web2app flow) so the motion tells the flow's story — each page-to-page hand-off gets its own choreography tied to what the two pages say, the chosen answer physically becomes the progress it earns or the next page's hero, and everything stays fluid, physical and smooth on real phones. Built for flows shipped as Superwall surfaces (the superwall framework: pages, router transitions, layout chrome), with the engine mapped onto the router; the same direction applies to any tap-through web flow. Motion only; no new screens. Use when the user asks to \"animate the onboarding\", \"make the funnel feel premium\", \"add transitions between onboarding pages\", or when a flow's page transitions feel flat, generic, choppy, or cheap."
user-invocable: true
---

# Animate Onboarding

Make an onboarding flow move like it means something. The pages, answer
capsules, progress bar and buttons already exist; this skill changes only how
they move — so the reader feels the story the questions tell, and the tap on an
answer is visibly what moves them forward.

## Where the flow lives: a Superwall surface

An onboarding is a screen the team will want to change after shipping —
reorder a question, cut a step, try a new statement — without an app release.
That is what the **superwall framework** is for: the flow is one surface in
`superwall/` (`config.ts` plus one page per screen in `app/`, shared chrome in
`layout.tsx`), previewed on every device in `superwall dev`, pushed as an
immutable version and switched live from the dashboard. Everything in this
skill assumes that shape, and the engine below is mapped onto its router:

- **A page is a route and the router owns every page change**
  (`router.push`, `router.back`, `useRouter()` from `superwall/navigation`).
  Never build a page swapper, a custom router or a cloned outgoing page:
  the leaving page stays mounted while it animates away, so there is
  nothing to clone. The only script in a hand-off is the shared-element
  flight that rides on top of the router's transition (a thin wrapper
  around `useRouter`, `references/framework/useStoryRouter.ts`, that
  measures, calls `router.push`, and measures again).
- **A hand-off is a custom transition name** on the page being entered
  (`export const transition = "story-picture"`), styled through the router's
  four phases (`enter`, `recede`, `leave`, `return`) on `[data-sw-route]`.
- **The progress bar, back button and primary button live in `layout.tsx`**,
  so the chosen answer has something persistent to fly into.
- **The first page's entrance gates on presentation** (`useSuperwallSnapshot
  ().paywall !== undefined`), never mount: the SDK preloads surfaces hidden.

Read the `superwall-framework` skill before touching the flow (install it if
it isn't there: `npx skills add https://github.com/superwall/skills
--skill superwall-framework --global --yes --agent claude-code universal
--full-depth`); its `references/mobile-design.md` carries the touch, motion
and type rules this skill builds on. A flow that is not a surface yet (a
native onboarding, a hand-rolled web funnel) is worth proposing as one first
(`superwall create`, or `superwall migrate --screen <path>` for a native
screen); the user decides. Only if they keep their own web runtime does
`references/web-runtime/` apply, and never on a surface.

The direction comes from Emil Kowalski's design engineering and Apple's
fluid interfaces (both folded into `mobile-design.md`), the idea that every
hand-off is tied to the copy of the two pages it joins, and a long round of
direct feedback on a shipped funnel (Reflective's discovery flow). **The
direction below is that feedback. It outranks general taste.**

## The one rule: Frame A → Frame B share one geometry, at every moment

> **When element A transforms into element B, A and B must have exactly the
> same geometry — size, position, corner radius, blur — on every frame of the
> transition. Not "close". Not "driven by the same numbers". The same.**

Two separate animated copies (A's and B's), each with its own clip, transform
and blur, *will* drift apart: A's own rounded ends, a border, a margin, a
different blur, a rounding difference. The eye catches a 1px mismatch
instantly, and the whole morph reads as broken.

So build every A → B as **one frame with two faces** (`references/morphFrame.ts`):
a single element owns all of the geometry (the clip is the only outline, one
transform, one blur), and A and B are *faces* that fill it and only crossfade.
They cannot differ in geometry, because there is only one.

```ts
const answer = fillFace(answerEl, answerRect);      // capture A before the page swaps
// …swap the page…
morph({
  from: { rect: answerRect, radius: answerRect.height / 2 },
  to:   { rect: photoRect,  radius: 20 },
  faces: { from: answer, to: photoFace(photoEl) },
  duration: 504,
});
```

Faces: `photoFace(img)`, `fillFace(el, rect)` (answers, buttons: its colour
fills the frame, its content sits where it rests), `colorFace(color)`
(backgrounds). Recipes for every case are in `references/handoffs.md`. Never
hand-roll an A → B morph as two layers.

Check it: the frame must start exactly on A's rect and radius and end exactly
on B's, so the handover to the live elements is pixel-exact.

References — read when you reach that part:

- `references/framework/` — **the engine on the superwall framework, as
  shipped** in the `animated-onboarding` example (`superwall create --example
  animated-onboarding` gives the whole project): `handoffs.ts` (every
  hand-off, both directions, cleanup), `useStoryRouter.ts` (`router.push` /
  `back` inside the hand-off), `motion.css` (exits and entrances on the
  router's phases), `layout.tsx` (chrome and the motion layer),
  `Question.tsx`, `flow.ts`. Start from these on a surface.
- `references/engine.md` — the hand-off engine on the framework's router:
  the hold on the layer, `flushSync` around `router.push`, the motion
  layer, chrome in the layout, the focus trap, the flag, roles declared up
  front, loaded destinations, interruption, traps.
- `references/handoffs.md` — how the transforms are built (answer → progress
  bar, answer ↔ photo, bar → answer), the clock, and the hand-off catalog.
- `references/performance.md` — what to animate, what never to, and how to
  diagnose "it's choppy".
- `references/morphFrame.ts` — **the A → B morph**: one frame, two faces, the
  glide clock, the shape. Use it for every element-into-element transform.
- `references/imageReady.ts` — image readiness incl. Safari.
- `references/web-runtime/` — the same engine for a flow the user keeps in
  a hand-rolled web runtime (it clones the outgoing page because that
  runtime has no router). Never the starting point on a surface.

## Direction (from the feedback)

### 1. Map every element before choreographing

Before writing any motion, build a **map of every element on every page, for
each hand-off in both directions**, and give each exactly one role. Elements
are the same when they're **optically equivalent** — they look like the same
thing in the same place — not when they're literally the same component.
Always read between the lines.

| From → to | Motion |
|---|---|
| **A → A**, same position, same size | **No animation.** No transition out or in for either. Animating it only draws attention to something that didn't change (e.g. a pinned "Continue" on consecutive pages). |
| **A → A**, different position, size or text | Transition gracefully out and in. |
| **A → B** (a different element) | **The transform *is* the transition.** No exit on A, no entrance on B; nothing else may compete with it. |
| **A → nothing** | Scale, fade and blur out. Cascade it so the elements feel like they move *because the others did* — subtle, like dominoes. Sneak in physics wherever possible: falling back with a skew or perspective. |
| **nothing → B** | Usually the reverse idea of the above. |

**Choosing A (the source)** — the element the user interacted with last has
top priority: the option they picked in a single select. A continue button has
the lowest. For multiple choice, animate **all** the chosen options into the
progress bar.

**Choosing B (the destination)** — in order:

1. **The most visually demanding element on the next screen that ties to the
   story.** If option A in a selection is purple and the next screen has a
   purple background, the background is a great destination.
2. **A hero image.** It's always nice to morph a chosen option, or the
   continue button, into the next screen's hero.
3. When in doubt, **the progress bar**: it gamifies selection and increases
   completion.
4. Or **the next continue button**: it makes them want to press it again.

**Back reverses roles.** If three answers collapsed into a photo going
forward, all three come *out of* it going back — not just the chosen one while
the others do a standard rise.

**Verify the map in code.** Every element gets the standard entrance by
default, so an element marked "transformed from" whose exemption is missing
runs its entrance *and* the transform — two animations fighting. For every
hand-off in both directions, confirm each destination's standard entrance is
off (declare it up front: `engine.md`, "Roles, declared up front").

### 2. How an A → B transform moves

It should feel fluid and physical, as one continuous thing.

- **One clock for every stacked phase.** A transform is several phases
  stacked (lift, travel, open, land). Drive every channel — position, size,
  corners, crossfade, blur — from **one** clock, so phase 1 eases in, each next
  phase starts with the velocity and acceleration the last one left, and the
  final phase eases out. Giving each phase its own eased span makes it stall
  at every boundary. The move leads and the opening follows on the same curve
  (e.g. size on `p^1.5`), never restarting from rest.
- **The clock is a critically damped spring** (damping 1.0, Apple's default
  for UI), in every dimension it drives (position *and* size): a barely-there
  pull-back (~1%), a quick rise to top speed early (~27% of the duration),
  then a **long, continuously slowing tail** into the target — **no constant-
  speed middle and no overshoot or bounce at the end**. At rest at both ends
  (a final taper lands it exactly on the last frame). Check it numerically:
  near top speed ≤ ~15% of the time, overshoot 0, soft braking in the last
  quarter.
- **Keep the path gentle.** Arrive at a normal slope and grow size linearly
  near the destination; a steep final curve or a multiplicative grow rushes
  the end and magnifies any change in speed.
- **Size floor: never more than 20% smaller than the smaller end.** 80 → 100
  may dip to 64 on the way, never to 20. No pinching an answer down to a
  thumbnail. (Exception: an answer becoming a stretch of a 4px progress bar
  has to shrink to be it.)
- **Bubbly:** a dimension that's about the same at both ends (e.g. both
  348px wide) **dips up to 20%** mid-flight (sin-shaped) and swells back —
  squeezing through like a bubble. None once the ends differ by half or more.
- **One geometry** (the rule above): the frame's clip is the only outline.
  Never scale a rounded shape non-uniformly (it squashes round ends into
  ovals); the frame clips (`inset(... round r)`) and only ever scales *up*.
- **Corners are proportional.** Interpolate the corner radius as a *fraction
  of the shape's shorter side* (its roundness: 0.5 = fully round ends), not in
  pixels, starting from the source's own roundness and ending at the
  destination's. A fully round answer opening into a square full-screen
  background stays visibly rounded while it's big and only goes square at the
  very end; interpolated in pixels, a big frame has tiny, sharp-looking
  corners almost at once.
- **Blur is motion blur.** It **starts and ends crisp**, and is blurred only
  while the frame is moving fastest: **from 25% to 75% of the duration**
  (easing in over 25–35%, a full 5px on screen over 35–65%, easing out over
  65–75%). One blur for both faces, on the frame's outer wrapper (no
  transform), so it softens the silhouette in screen pixels. **The swap
  (handover) happens inside that window**, so A becomes B under the blur.
  A single colour going into the bar (or back out) has nothing to smear:
  `blur: 0`. Keep one switch for all motion blur (`MOTION_BLUR_ENABLED` in
  `morphFrame.ts`) so it can be turned off in one place to isolate a problem.
- **Back is never a rewind.** Going back is its own move on the same clock,
  landing on the same long gentle tail, with no direction flip mid-motion. E.g. back from
  the progress bar: the pill takes its stretch of bar with it (the bar gives
  it up at once, under the pill), slides out, and drops and grows into the
  answer.
- **One duration for every A → B transform** — 504ms in the reference. They
  drifted to 720–820ms and felt slow; keep them equal and brisk.

### 3. Handovers: no doubles, no flashes, no missing targets

- **A destination never fades in while something transforms into it.** Keep
  the live element hidden; the transforming copy carries it the whole way.
- **Hand over on the last frame, already painted.** Keep the live element at
  `opacity: 0.001` for the whole transform (painted, but invisible), let it
  return to 1 as the transform ends, and remove the copy in that same frame.
  A browser doesn't paint a fully transparent element, so one kept at 0 and
  revealed only on the last frame shows a frame of nothing: a flash.
- **The destination must be loaded.** An unloaded `<img>` has no height, so
  the morph measures a zero target and animates a blank. Decode every image
  up front and keep it; before a hand-off into a page with an image, wait for
  it (up to ~400ms, a newer tap cancels the wait); if it still isn't there,
  skip the morph and fade the image in on load.
- **Safari (every iPhone) loads even a cached image asynchronously** when a
  new `<img>` is created: right after the page swaps, the new image reports
  "not loaded" with zero height. So:
  - never require the *new* `<img>` to be loaded to run the morph — require
    the flow's own decoded copy to be ready (a morph gated on the live element
    simply never runs on an iPhone);
  - render images with `width`/`height` from their known natural size, so the
    box is right before it paints;
  - build copies from the already-decoded `Image` object, not `cloneNode()`
    of an `<img>` (a clone reloads and paints blank);
  - keep the copy on top until the live image has actually loaded;
  - mark an image ready on its `load` event; older Safari rejects `decode()`
    for images outside the document.
  Test on a real iPhone: none of this reproduces in desktop Chrome.

- **Remove each copy when its own transform ends.** The copies' removal waits
  only on the copies' animations and the destinations' 0.001 holds (which end
  on the same frame), plus a live photo's load. Never on the new page's
  entrances: a copy that waits for them sits over them for their whole
  duration. Under a full-screen colour that hid the statement's words for
  ~1s, then they just appeared. Keep two lists (`engine.md`): everything, for
  a fast second tap to finish, and the handovers, for cleanup.
- **Nothing enters under a covering copy.** A morph frame is above the live
  page until it hands over. Anything whose entrance starts before then (words
  on a full-screen colour, a header switching onto it) fades in unseen and pops
  in mid-fade when the frame goes. Start those after `TRANSFORM_MS`.

### 3b. Full-screen colour moments (statement screens)

A "Did you know…" statement on a full-screen field of the answer colour is a
strong beat between questions. Its background is by far the most visually
demanding element on the screen, and it's the answer's own colour, so by the
destination rules:

- **Question → statement: the chosen answer opens into the background.** One
  frame, answer face → colour face, the corners going from the pill's full
  roundness to square only at the end. The answer doesn't fly into the
  progress bar here: the background is the better destination (the bar steps
  normally).
- **The colour is its own full-screen layer**, rendered by the runtime behind
  the page (not the page's or body's background), so it can be a morph
  destination and source as one element, and stays out of sight (0.001) until
  the morph hands over.
- **The words arrive after the colour** (entrance delayed ~540ms: just after
  the 504ms frame hands over, never under it), and the header and button
  invert onto it, switching only once the colour has arrived.
- **Statement → next question: the colour goes into the progress bar exactly
  like an answer pill** (see 4): its right edge flies to where the bar ends as
  it shrinks to a bar-height pill, joins, grows together with the bar to the
  new length, and bounces. The statement becomes progress. Its words leave
  first, one after another, above the colour.
- **Back** is the pill's return: the stretch of bar slides out along it, then
  drops and grows into the full-screen colour; and the colour closes back into
  the answer that opened it.

### 3c. The browser's own chrome (iOS 26 toolbar tint) — web funnels only

A surface in the SDK's webview has no browser chrome; skip this section
there, and never add a `position: fixed` element to a native surface (the
framework's insets rule). On a web funnel in Safari it matters: iOS 26
Safari ignores `<meta name="theme-color">`. It tints its toolbars from
a `position: fixed` element touching the top edge (within ~4px, 80%+ of the
width, 3px+ tall, with its own background colour), otherwise from the page
background. A full-screen colour sweeping in makes it retint mid-transition,
which looks janky. So:

- **Pin the tint with a sentinel**: one permanent fixed element at the very
  top, 4px tall, full width, in the page colour, topmost. Safari always tints
  from it. Keep `theme-color` for Chrome and older Safari.
- **Never animate with `position: fixed`.** Every copy, frame and flying pill
  is `position: absolute` at the same screen coordinates (the page itself
  doesn't scroll). A full-screen fixed morph frame is exactly what Safari tints
  from: it flashed the statement colour into the toolbar. The sentinel must be
  the only fixed element.
- To verify on a phone, turn the sentinel red for a test: the toolbar should
  go red and hold through every transition.

### 4. The signature move: the answer becomes the progress

- **Every chosen answer flies into the progress bar** — on every question
  page, unless it's morphing into something better (the next page's hero).
- **The selection is what grows the bar, not a timer.** The bar holds still
  until the answer arrives, then they move as one, driven by **one sampled
  timeline**. A CSS transition with a guessed delay is not good enough.
- **Right edge to right edge.** The answer shrinks around its *right* edge,
  and that edge flies to where the bar *currently ends*; they join, then
  **grow together** to the new length. Not "dropping into the gap like a
  brick".
- **Path: rise and drift together, rise leading**; it reaches the bar's height
  ~87% of the way across and slides the last short stretch level.
- **A bounce after growing** (~13%, ease-out-back).
- **Nothing about the bar changes except its length** — no colour or opacity
  animation (the pill reaches the bar's colour *before* it joins and is
  removed without a fade), and **no height change** (a swell reads as a flash,
  since the pill on top doesn't swell with it).
- The fill slides with `translateX` inside the clipping track, never `scaleX`,
  so its round end stays round.
- **Anything that goes into the bar goes the same way** — a full-screen
  statement colour included: right edge to the bar's end, shrinking to a
  bar-height pill, join, grow together, bounce. Build it through the
  one-geometry frame with a custom path (`morph({ path })`), never by
  stretching the shape (a full-screen rectangle scaled to 4px squashes its
  corners). The progress bar is the one exception to the size floor.
- **Back:** see "Back is never a rewind" above.

### 5. What landed well

- "Gone within a day": the old page fades to nothing, a beat of emptiness
  (~120ms), then the photo settles in from `scale(1.03)`; its exit lifts the
  photo first, then the words.
- The welcome page's exit — **the example of physics in an A → nothing**: it
  leans back in perspective as it floats up
  (`perspective(900px) translateY(-20px) rotateX(22deg) scale(.97)` about its
  bottom edge, fading), like a card tipping away.
- Hand-offs chosen per pair from the copy (forgetting pages drift away,
  "re-explaining" arrives from above, agitation gets faster cuts, the last
  answer completes the bar and hands over to "You're all set").

### 6. What was tried and rejected — don't reach for these

| Tried | Why it failed |
|---|---|
| View Transitions API snapshots for exits and morphs | Snapshot artefacts (smeared edges, stretched morphs), a full-page snapshot re-composited every frame |
| `filter: blur()` on every entering line, answer and image | ~15fps on software raster; blurred text halos |
| `backdrop-filter` on answer capsules while they move | Re-computed every frame they move |
| Genie / mesh "sucked into the bar" (sliced strips) | Didn't read as premium; too clever |
| Rotating the pill to face its velocity | Didn't feel right; a straight path with the right timing did |
| A decorative background pattern reacting to transitions | Decoration competing with the story |
| Answer filling the bar's gap like a brick (left edge to bar end) | Reads as placement, not propulsion |
| A height swell on the bar when the answer joins | Flash: the pill on top doesn't swell with it |
| Fading the flying pill out over the bar | Visible as a colour change in the bar |
| A photo fading in from a large source rect | Ghosting |
| Squeezing the answer to a thumbnail to swap with the photo | Too small; squashed corners; not fluid |
| Stock `easeInOutBack` | 10% pull-back and overshoot, rushed middle: abrupt |
| A stiff simulated spring | ~6% overshoot that swells and snaps back in ~75ms |
| A smooth-step ease to a 1.5% overshoot at 82%, settling back in ~90ms | Too linear in the middle, too bouncy/snappy at the end |
| A separately eased span per phase | Stalls at every phase boundary |
| The destination fading in as the transform arrives | The element appears twice |
| Playing the forward move in reverse for back | Direction flips mid-motion; no physical landing |
| Revealing the destination on the last frame | A one-frame flash before it's painted |
| A and B as two separate animated layers, each with its own clip, transform and blur, "driven by the same numbers" | Geometry drift: A's own rounded ends, different blur, rounding; visibly different sizes mid-morph |
| Gating the morph on the new `<img>` being loaded | Never ran on iOS Safari (it loads cached images asynchronously) |
| Corner radius interpolated in pixels | A big frame gets tiny, sharp-looking corners almost at once |
| A statement colour shrinking into the bar as a plain morph to the new segment | Should move like a pill: right edge to the bar's end, join, grow together |
| `position: fixed` animated copies and morph frames | iOS 26 Safari tints its toolbar from a fixed element at the top: the statement colour flashed into the browser chrome |
| Blur tied to the swap, rising into it and fading out to the last frame | Blurred only for the first half. Blur is motion blur: crisp at both ends, blurred from 25% to 75% |
| Removing the copies once *every* animation had finished, the new page's entrances included | The full-screen colour frame sat over the statement's words for their whole entrance: a long red pause, then the words just appeared |
| Words entering on a statement at ~420ms, under a 504ms frame | Their first ~84ms happened unseen, so they popped in mid-fade when the frame went |

When the user rejects an approach, **revert it completely** to the last
approved state (confirm with the build output), then try the next idea. Don't
stack a fix on top of a rejected idea.

## Principles

**Restraint first.** Onboarding is a
first-time, rare surface — it has the delight budget — but every motion still
needs a named purpose: explanation, spatial consistency, state indication,
feedback. Keyboard navigation (Enter/Esc) and browser back/forward get a
**plain** 200ms fade: repeated or system-animated, they must not be
choreographed.

**The router owns navigation.** Every hand-off is a custom transition the
router runs (`export const transition = "story-…"`, CSS on
`data-sw-transition` and `data-sw-phase`); the script only adds the
shared-element flights, inside a wrapper around `useRouter`. A custom
router, a page swapper, a cloned page or a `position: fixed` copy is a
rejected approach on a surface, whatever it would make easier.

**Each hand-off is tied to the pair.** Read the copy of page A
and page B, and pick motion that says what B says. Name the idea for each pair
in a code comment. In a long quiz, a family of related question → question
hand-offs is fine; make the act boundaries the distinct moments. Change pacing
by act: calm, soft, faster under tension, settled at the resolution.

**Fluid, not scripted.** Respond on pointer-down. Every
navigation first settles the previous hand-off instantly, so a fast second tap
never waits. Motion hints at its destination (it starts moving before it
opens).

**Craft (`mobile-design.md`, Motion).**
- Curves: `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`,
  `--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)`. Never `ease-in` on UI.
- Exits quicker than entries: exits 120–380ms, entries 240–720ms; A → B
  transforms one shared, brisk duration.
- Entrances: title, then subtitle, then answers 40ms apart (30–80ms); answers
  are tappable from the first frame.
- Never from `scale(0)`; from 0.9+ with opacity.
- Only `transform` and `opacity` move, with two sanctioned exceptions on a
  single element at a time: the morph's `clip-path` and its 5px blur.
- Reduced motion: opacity only, nothing moves.
- Self-check against the never-ship list in `mobile-design.md` (`transition:
  all`, `scale(0)`, `ease-in`, width/height animation, ungated hover, no
  reduced motion, everything entering at once).

## Workflow

1. **Recon.** Find the surface (`config.ts`, one route per page in `app/`,
   `layout.tsx` with the progress bar and back button), the answer
   component, the page-title component, every image, and existing
   easing/duration tokens. Read every page's copy and name the story arc
   (acts). If a page change happens anywhere but `router.push` /
   `router.back`, fix that first.
2. **Plan as a table, then stop.** One row per hand-off: from → to, what
   moves, why it fits that pair — choosing A and B by the priorities above.
   Under it, the **element map** for each hand-off in both directions (every
   element's role). Plus the whole-flow rules. Ask at most one decision
   question with a recommendation. Build only after approval.
3. **Build the engine** (`engine.md`, starting from `references/framework/`):
   an opt-in flag, a `story-…` transition name per page, the hold on the
   route layer, `router.push` / `router.back` wrapped so the swap happens
   inside the hand-off (and waits for the destination's image), the motion
   layer in the layout, destinations declared up front.
4. **Build the transforms and hand-offs** (`handoffs.md`): the answer → bar
   flight first, then the A → B morphs, then each pair's exit, then entrances
   as CSS variable overrides.
5. **Map check, geometry check, timeline check and performance pass** before
   showing anyone: every "transformed from" element has its entrance off;
   every A → B goes through `morph()` (one frame) and starts and ends exactly
   on the real rects; no destination is visible before the last frame or faded
   in over its copy; nothing animated is `position: fixed`. **Timeline:** for
   each hand-off, list every copy's lifetime on screen next to every entrance
   beneath it. No entrance may run under a copy that covers it (a full-screen
   colour frame covers the whole page), and each copy is removed when its own
   transform ends, not when the entrances do. Then `performance.md`. Then test
   on a real iPhone.
6. **Run it for the user.** `superwall dev`, then the studio's **Preview**
   button for a QR code that opens the flow on their phone; a production
   build (`superwall push`, then the studio's pushed version) is what to judge
   smoothness on. Don't claim it feels right without the user's eyes on it.
7. **Iterate on feel, one change per round, with numbers.** Compute a table
   from the actual keyframes (t, ms, size, corners, position, opacity, blur)
   and verify the invariants (size floor, no overshoot, speed continuity, at rest
   at both ends) before reporting. For your own checks, play it at 2–5× or step
   it frame by frame.
8. **Ship behind the flag** so the old motion stays reachable (a `motion`
   query key on a web funnel; a constant or a placement param natively) for
   comparing funnel drop-off. `superwall push` only when asked; the user
   promotes.
