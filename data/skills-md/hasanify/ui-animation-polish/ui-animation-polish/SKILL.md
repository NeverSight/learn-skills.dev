---
name: ui-animation-polish
description: Detailed rules for making UI animations and micro-interactions feel polished, with exact durations, easings, scales, transform origins and copy-ready CSS / Motion (Framer Motion) code. Ships a zero-dependency auditor, motion tokens, presets, references and interactive before/after examples. Use whenever the user is writing, reviewing or fixing UI motion (CSS transitions, Framer Motion / Motion, React, SwiftUI, dropdowns, popovers, modals, buttons, toggles, tabs, lists, drag interactions), or says an animation feels off, janky, slow, floaty, cheap, robotic or "not smooth", even if they never say "animation guidelines".
---

# UI Animation Polish

Twenty rules that separate "it moves" from "it feels good". Each is a concrete before → after change, so apply them as specific numbers and properties rather than vague taste.

Four principles sit underneath all of them. When a situation isn't covered by a rule, reason from these:

1. **Respond fast.** Motion that people trigger often (menus, buttons, tabs) must be quick, or it becomes a tax on every use.
2. **Start where the user acted.** Elements should grow out of, and return to, the thing that caused them.
3. **Stay physically believable.** Objects accelerate and decelerate, travel in arcs, resist at limits, and keep their mass.
4. **Never leave an empty or ambiguous frame.** One state should hand off to the next without a gap, a pop or a muddy overlap.

**Scope:** interactive UI motion on the web and native apps. Not logo stings, video editing, 3D scenes, or writing about animation.

## Bundled resources

Load only what the task needs; the rules below are enough for most fixes.

| Path | Open when |
| --- | --- |
| `references/easing-and-duration.md` | Choosing a curve, a duration, a spring, or choreographing several elements |
| `references/component-recipes.md` | Building a specific component (modal, toast, tabs, switch, drag, carousel, …) |
| `references/platforms.md` | The stack is Vue, Svelte, SwiftUI, React Native, Flutter, GSAP, WAAPI, Tailwind, or View Transitions |
| `references/accessibility-and-performance.md` | Reduced motion, vestibular safety, jank, FLIP, blur cost, frame budgets |
| `references/review-and-audit.md` | Auditing a codebase, scoring, or writing the report |
| `references/anti-patterns.md` | A motion smell needs a name and an exact replacement |
| `references/sources.md` | Verifying where a default comes from |
| `scripts/audit-motion.mjs` | You can run commands and the task is a review: `node scripts/audit-motion.mjs <path>` |
| `assets/motion-tokens.css` | Writing CSS and needs the tokens |
| `assets/motion-presets.ts` | Writing React + Motion and wants typed presets |
| `examples/before-after.html` | The user wants to see or feel the difference |
| `examples/react/` | Copy-ready React components for popover, stagger, press, icon swap, toggle, card→detail |

## How to use this skill

**Writing new motion**

1. Identify the element type (dropdown, button, list, toggle, drag handle, tab, icon swap, card expansion, success state).
2. Look it up in the Quick reference, then read the matching rules below.
3. For a specific component or unfamiliar stack, open the matching reference from the table above.
4. Use the defaults given; put durations and easings in shared tokens (see Implementation notes) or start from `assets/`.

**Reviewing or fixing existing motion**

1. Read the code and note every `transition`, `animate`, `@keyframes`, spring config, and drag handler.
2. If you can run commands, run `node scripts/audit-motion.mjs <path>` and use its rule-numbered findings as a floor. It cannot judge origin, exit direction, drag feel, or intent.
3. Compare each against the "Before" smell of each rule. Use the Review checklist at the end and `references/review-and-audit.md`.
4. Fix the violations. Report each as `rule N: old value → new value, because <one-line reason>` so the user learns why, and can push back.
5. Don't rewrite motion that already follows the rules just to make it match your taste.

**When to deviate.** The numbers are strong defaults, not laws. Full-screen or page-level transitions can run 300–500ms; playful or onboarding moments can bounce; a large panel needs longer than a tiny tooltip. Say so when you deviate and why. If the project has an existing motion design system, follow it and note any differences.

---

## The 20 rules

### Timing and easing

#### 1. Ease-out for entrances

- **Before:** `ease-in`, 250ms. **After:** `ease-out`, 250ms.
- **Why:** Ease-in starts slowly, so for the first ~100ms almost nothing appears to happen, right when the user is waiting for a response. Ease-out front-loads the movement, so the interface feels like it reacted instantly and then settled.
- **Use:** anything appearing or arriving: menus, toasts, modals, tooltips, list items.
- **Avoid:** `ease-in` for entrances; default `ease` is acceptable but ease-out is better. A stronger curve such as `cubic-bezier(0.23, 1, 0.32, 1)` gives a more premium settle than the built-in `ease-out`.

```css
.popover {
  transition:
    opacity 200ms cubic-bezier(0.23, 1, 0.32, 1),
    transform 200ms cubic-bezier(0.23, 1, 0.32, 1);
}
```

#### 2. Dropdowns and small popovers at 150–250ms

- **Before:** `600ms`. **After:** `200ms`.
- **Why:** People open menus dozens of times a day. At 600ms each open feels like waiting; the animation should be just long enough to be perceived as smooth, not noticed as an animation.
- **Use:** menus, selects, tooltips, context menus, small popovers: 150ms for tiny things, ~200ms default, up to 250ms for larger ones.
- **Avoid:** durations over 300ms for anything the user triggers repeatedly. Reserve longer durations for rare, large moves (page transitions, onboarding).

#### 9. Ease-in-out for moves

- **Before:** `linear`, 300ms. **After:** `ease-in-out`, 300ms.
- **Why:** Real objects don't start or stop instantly. Linear motion has constant velocity and reads as mechanical. Use ease-in-out when an element travels between two positions that are both on screen (a slider thumb, a reordered card, a moved indicator). Reserve ease-out for things _entering_ and ease-in for things _leaving_ the screen entirely.
- **Exception:** `linear` is correct for constant-speed effects such as spinners, progress shimmer and marquee text.

#### 15. Make exits about 20% shorter than entrances

- **Before:** `250ms in / 250ms out`. **After:** `250ms in / 200ms out`.
- **Why:** On entry the user is watching for what appeared; on exit they've already decided to dismiss and want to move on. A slightly faster exit feels responsive without feeling abrupt.
- **Use:** every enter/exit pair (modals, popovers, toasts, drawers). Pair with rule 12 (exit toward the trigger).

```tsx
<motion.div
  initial={{ opacity: 0, scale: 0.95 }}
  animate={{
    opacity: 1,
    scale: 1,
    transition: { duration: 0.25, ease: "easeOut" },
  }}
  exit={{
    opacity: 0,
    scale: 0.95,
    transition: { duration: 0.2, ease: "easeIn" },
  }}
/>
```

### Feedback and sequencing

#### 3. Stagger list rows by about 30ms

- **Before:** `200ms between rows`. **After:** `30ms between rows`.
- **Why:** A long gap makes a list feel like a slow wave the user must wait through. A short stagger still gives a pleasing cascade but finishes almost immediately.
- **Use:** menus, navigation lists, search results, settings rows. Keep the **total** stagger under ~300ms: for long lists, cap the number of staggered items (e.g. the first 8–10) and show the rest together.
- **Avoid:** staggering by more than ~50ms, and staggering on every re-render (only on first appearance).

```tsx
const list = { show: { transition: { staggerChildren: 0.03 } } };
const row = { hidden: { opacity: 0, y: 4 }, show: { opacity: 1, y: 0 } };
```

#### 4. Scale to 0.97 on press

- **Before:** no press feedback. **After:** `scale(0.97)` over ~150ms while pressed, release to 1.
- **Why:** An element that doesn't react to a press feels dead or broken. A slight shrink confirms the interface received the input, mimicking physical depression. It must be subtle: 0.95 is the floor for small buttons; large cards should use closer to 0.98–0.99.
- **Use:** buttons, cards that are clickable, list rows, chips, icon buttons.

```css
.btn {
  transition: transform 150ms ease-out;
}
.btn:active {
  transform: scale(0.97);
}
```

```tsx
<motion.button whileTap={{ scale: 0.97 }} transition={{ duration: 0.15 }} />
```

- **Avoid:** scaling disabled buttons; letting the scale change layout (use `transform`, never width/height).

#### 6. Stagger as details settle

- **Before:** a main element and its secondary details (badge, counter, label) stop at exactly the same moment, rigid and synchronized. **After:** the detail trails by ~50ms.
- **Why:** Real objects with attached parts don't stop in lockstep; the smaller or lighter part lags slightly and arrives after. It gives the interface a sense of mass and polish.
- **Use:** notification badges on icons, counters beside labels, avatars with status dots, a subtitle under a title.

```tsx
<motion.span animate={{ x: 0 }} transition={{ duration: 0.2, delay: 0.05 }} />
```

- **Avoid:** delays above ~80ms (the detail then looks detached), and applying this to every element on the page.

#### 8. Pulse to confirm success

- **Before:** only the label changes ("Save → Saved"). **After:** label change plus a single pulse.
- **Why:** A text change alone is easy to miss, especially in peripheral vision. One pulse draws the eye to the confirmation without needing a toast or dialog.
- **Use:** save, copy, send, add-to-cart, toggled-on confirmations.
- **Avoid:** looping pulses (they read as "still loading" or demand attention); large amplitudes. Keep the peak around `scale(1.04–1.08)` and under ~400ms total.

```tsx
<motion.button
  animate={saved ? { scale: [1, 1.06, 1] } : {}}
  transition={{ duration: 0.35, ease: "easeOut" }}
/>
```

### Physicality and origin

#### 5. Stretch moving knobs about 12%

- **Before:** rigid circle slides across the track. **After:** knob stretches along its travel direction by ~12% while moving, with the other axis squashing to preserve area.
- **Why:** A rigid shape feels like a sticker sliding on a rail. A stretch with preserved area suggests a soft, living object and makes the motion feel faster and more fluid.
- **Use:** toggle switches, slider thumbs, segmented-control indicators, pill-shaped selection highlights.
- **How:** during the move, `scaleX ≈ 1.12` and `scaleY ≈ 1/1.12 ≈ 0.89` (area preserved), returning to 1 as it settles. The stretch must be transient, not left on at rest.

```tsx
<motion.div
  animate={{ x: on ? 20 : 0, scaleX: [1, 1.12, 1], scaleY: [1, 0.89, 1] }}
  transition={{ duration: 0.25 }}
/>
```

- **Avoid:** stretching more than ~15% (looks like jelly), and non-uniform stretch that changes the apparent area.

#### 7. Arcs for object movement

- **Before:** straight line. **After:** about a `32px` arc.
- **Why:** Natural movement of a thrown or carried object follows a curve. Straight lines look robotic, especially over longer distances.
- **Use:** an item flying into a cart, folder, or tray; a card moving between columns; any object that visibly travels across the screen (not small indicator slides).
- **How:** animate x and y with _different_ easings or durations so the path bows, or follow an offset path.

```tsx
<motion.div
  animate={{ x: 240, y: 0 }}
  transition={{
    x: { duration: 0.35, ease: "easeInOut" },
    y: { duration: 0.35, ease: [0.3, 0, 0.7, 1] },
  }}
/>
```

- **Avoid:** huge arcs that exaggerate a short move; arcs on tiny UI nudges.

#### 10. Start popovers at scale 0.95

- **Before:** `scale(0) → 1`. **After:** `scale(0.95) → 1` plus opacity.
- **Why:** Nothing in the real world appears from zero size. Scaling from 0 makes the popover zoom out of nowhere and look gimmicky. Starting close to full size reads as a subtle lift, and is much easier to look at repeatedly.
- **Use:** popovers, dropdowns, tooltips, context menus, command palettes, modals (modals can use 0.95–0.98).
- **Avoid:** `scale(0)` for any UI that isn't deliberately playful.

#### 11. Enter from the trigger

- **Before:** `transform-origin: center`. **After:** `transform-origin: top right` (or wherever the trigger is).
- **Why:** If a popover scales from its own centre, it looks detached from the button that opened it. Scaling from the corner or edge nearest the trigger shows a clear cause → effect relationship.
- **How:** set the origin to the point on the popover closest to the trigger. A menu below a left button → `top left`; below a right button → `top right`; above → `bottom ...`. Most positioning libraries expose this (e.g. Radix exposes `--radix-popover-content-transform-origin`).

```css
.popover {
  transform-origin: var(--radix-popover-content-transform-origin, top right);
}
```

- **Avoid:** leaving the default `center` origin on anything anchored to a trigger.

#### 12. Exit toward the trigger

- **Before:** centre-origin fade. **After:** exits toward the trigger.
- **Why:** The element came from the trigger, so returning there completes the loop and tells the user where it went. Use the same `transform-origin` as the entrance so the exit is its mirror, 20% faster (rule 15).

#### 13. No bounce on everyday UI

- **Before:** underdamped spring with wobble. **After:** no overshoot.
- **Why:** Bounce draws attention to the animation itself. In menus, buttons, forms, tabs and toggles that are used constantly, it becomes distracting and makes the product feel toylike rather than precise.
- **Use:** critically damped or ease-out curves. In Motion springs, raise `damping` until the overshoot disappears (e.g. `{ type: 'spring', stiffness: 400, damping: 40 }`) or use `bounce: 0`.
- **Exception:** celebratory moments (confetti, achievement, onboarding, playful consumer brands) can use bounce, once and rarely.

```tsx
<motion.div transition={{ type: "spring", stiffness: 400, damping: 40 }} /> // settles without overshoot
```

### Direct manipulation

#### 14. Don't tween while held

- **Before:** an easing tween (or spring) is applied to the position while the user holds and drags, so the element lags behind the finger or cursor. **After:** direct, 1:1 pointer tracking while held.
- **Why:** During a drag the user's hand _is_ the animation. Any smoothing delay breaks the feeling that they are holding the object. Animate only once the pointer is released (snap to position, settle, momentum).
- **How:** update position directly from pointer events during the drag (no `transition` on the moving property, or `transition: none` while dragging). On release, apply the spring or ease to the resting position.

```css
.thumb {
  transition: transform 200ms ease-out;
}
.thumb.dragging {
  transition: none;
}
```

- **Avoid:** CSS `transition` on `left` / `transform` that is still active while dragging; smoothing filters on pointer position.

#### 19. Rubber band past bounds

- **Before:** hard stop at the edge. **After:** diminishing resistance past the limit, then spring back on release.
- **Why:** A hard stop feels like hitting a wall and gives no sense of how far past the limit the user pushed. Diminishing resistance communicates "this is the edge" while keeping the motion alive.
- **How:** the further past the bound, the less the element moves per pixel of input. A common formula (iOS-style):

```ts
// x = distance dragged past the limit, d = max visible stretch (e.g. 100), c = 0.55
const rubberBand = (x: number, d: number, c = 0.55) =>
  (1 - 1 / ((x * c) / d + 1)) * d;
```

In Motion, `drag` with `dragElastic` (e.g. `0.2`) and `dragConstraints` gives this behaviour for free; on release it springs back.

- **Use:** sheets, sliders, carousels, pull-to-refresh, scroll edges, draggable panels.

### Transitions between states

#### 16. Overlap old and new states

- **Before:** old content fades out → blank beat → new content fades in. **After:** enter and exit overlap in time.
- **Why:** The empty frame between the two reads as a flicker or lag. Overlapping keeps something on screen at all times and makes the change feel like one continuous event.
- **How:** run exit and enter at the same time (e.g. `AnimatePresence mode="popLayout"` or the default sync mode) instead of `mode="wait"`, and absolutely position so the two don't stack layout.
- **Avoid:** `mode="wait"` for small content swaps; sequencing that doubles the total duration.

#### 17. Masks for reveals and colour

- **Before:** fade the content, or crossfade the text. **After:** clip the content, or mask the text.
- **Why:** A crossfade between two pieces of text briefly shows both overlapped, which looks muddy and unreadable. A clip (`clip-path`) or mask reveals the new content while hiding the old in a controlled edge, so the change reads as clean and intentional. The same applies to colour changes on tabs or toggles: reveal the new colour through a moving mask rather than cross-fading colours.
- **Use:** tab content switching, label changes, progress/colour fills, text swaps, indicators.

```css
.reveal {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 250ms cubic-bezier(0.23, 1, 0.32, 1);
}
.reveal.on {
  clip-path: inset(0 0 0 0);
}
```

#### 18. Crossfade icons with scale + opacity + blur

- **Before:** hard replacement of one icon with another. **After:** scale + opacity + blur animate together.
- **Why:** An instant swap pops. A pure opacity crossfade shows two icons overlapped at 50%. Adding a small scale change and a touch of blur hides the overlap and reads as one icon morphing into another.
- **Use:** copy → check, play → pause, menu → close, like toggle, theme toggle.
- **How:** outgoing icon goes to `scale 0.5–0.8`, `opacity 0`, `blur(4px)`; incoming comes from the same values to `scale 1`, `opacity 1`, `blur(0)`, in ~150–200ms, overlapping (rule 16).

```tsx
<motion.span
  key={copied ? "check" : "copy"}
  initial={{ opacity: 0, scale: 0.6, filter: "blur(4px)" }}
  animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
  exit={{ opacity: 0, scale: 0.6, filter: "blur(4px)" }}
  transition={{ duration: 0.18 }}
/>
```

- **Avoid:** blur above ~6px or on large areas (expensive and looks smeared).

#### 20. Reuse the same layoutId

- **Before:** a disconnected replacement: one element vanishes and an unrelated one appears. **After:** the same object expands or moves.
- **Why:** When a card becomes a detail view, or a selected indicator moves between tabs, the user's brain tracks it as a single object. Treating it as two unrelated elements breaks that continuity and forces them to re-orient.
- **How:** give both states the same `layoutId` in Motion so it animates the shared position and size.

```tsx
// list
<motion.div layoutId={`card-${id}`} onClick={() => setOpen(id)}>...</motion.div>
// detail
<motion.div layoutId={`card-${id}`}>...</motion.div>
```

- **Use:** card → detail, thumbnail → lightbox, active tab underline / pill, selected item highlight.
- **Avoid:** reusing the same `layoutId` for two elements that are visible at once; animating children inside a shared layout without `layout="position"` when they distort.

---

## Quick reference

| Situation                          | Do this                                                       |
| ---------------------------------- | ------------------------------------------------------------- |
| Menu / dropdown / popover opens    | `ease-out`, 150–250ms, start `scale(0.95)`, origin at trigger |
| Same element closes                | ~20% shorter, exits toward trigger                            |
| Button pressed                     | `scale(0.97)`, ~150ms                                         |
| List appears                       | `ease-out`, 30ms stagger, capped total                        |
| Element moves on screen            | `ease-in-out`, ~300ms, 32px arc if it travels a distance      |
| Toggle / knob                      | ~12% area-preserving stretch, no overshoot                    |
| Badge / detail on a moving element | settles ~50ms after its parent                                |
| Dragging                           | 1:1 pointer tracking, rubber band at limits                   |
| Text / tab swap                    | overlap, mask or clip, never blank gap or muddy crossfade     |
| Icon swap                          | scale + opacity + blur, overlapping                           |
| Card → detail, moving indicator    | shared `layoutId`                                             |
| Success                            | label change + one pulse                                      |
| Spring                             | critically damped, no bounce, unless the moment is playful    |

## Review checklist

Work through this when auditing existing motion. Flag each hit with its rule number.

- [ ] Any entrance using `ease-in` or `linear`? (1, 9)
- [ ] Any menu, dropdown or tooltip over ~250ms? (2)
- [ ] Exit as long as or longer than entrance? (15)
- [ ] Popover using `scale(0)` or `transform-origin: center`? (10, 11)
- [ ] Exit that doesn't return to the trigger? (12)
- [ ] Clickable element with no `:active` / `whileTap` feedback? (4)
- [ ] List stagger over ~50ms per item, or unbounded total? (3)
- [ ] Spring with visible overshoot on routine UI? (13)
- [ ] A `transition` still active on a property during drag? (14)
- [ ] Hard stop at drag or scroll limits? (19)
- [ ] `mode="wait"` or fade-out-then-fade-in gaps? (16)
- [ ] Text or tab content crossfading? (17)
- [ ] Icon swapped with no animation, or opacity-only? (18)
- [ ] A thing that becomes a bigger version of itself but is re-mounted? (20)
- [ ] Success shown only by a label change? (8)
- [ ] Rigid toggle knob, straight-line travel for a thrown object? (5, 7)

## Implementation notes

- **Performance:** animate `transform` and `opacity` (compositor friendly). Avoid animating `width`, `height`, `top`, `left`, `margin`. Use blur sparingly and check on low-end devices.
- **Reduced motion:** respect `prefers-reduced-motion`. Keep opacity changes; drop travel, scale, stagger, arcs, stretch and pulse. In Motion use `useReducedMotion()` or `<MotionConfig reducedMotion="user">`. Reduced motion is not the same as no feedback; see `references/accessibility-and-performance.md`.

```css
@media (prefers-reduced-motion: reduce) {
  * {
    transition-duration: 1ms !important;
    animation-duration: 1ms !important;
  }
}
```

- **Tokens:** define shared values so the product stays consistent. Ready-made: `assets/motion-tokens.css` (CSS) and `assets/motion-presets.ts` (typed Motion presets).

```css
:root {
  --dur-fast: 150ms;
  --dur-base: 200ms;
  --dur-slow: 300ms;
  --dur-exit: 160ms;
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
}
```

- **Interruptibility:** users can re-trigger things mid-animation. Prefer transitions/springs that retarget from the current value over keyframes that restart from zero.
- **Don't over-apply:** not every element needs motion. Animate to explain cause and effect, confirm actions, and preserve continuity, not to decorate.
- **Existing systems:** when a rule conflicts with a project's motion tokens or platform conventions (SwiftUI, Material), follow the system and mention the difference.
- **Reporting:** when you change motion, summarise as a short list of `rule N: before → after`, and offer to show the alternative if the user prefers a different feel.
- **Tooling:** `scripts/audit-motion.mjs` scans CSS/JSX/TSX/Vue/Svelte/HTML for the mechanical violations; `examples/` shows the numbers running. Neither replaces reading the interaction.

## Reference map

| Need | File |
| --- | --- |
| Curve, duration, spring, choreography | `references/easing-and-duration.md` |
| Component-by-component code | `references/component-recipes.md` |
| CSS, Tailwind, React, Vue, Svelte, SwiftUI, RN, Flutter, GSAP | `references/platforms.md` |
| Reduced motion, vestibular safety, jank, FLIP | `references/accessibility-and-performance.md` |
| Audit workflow, scoring rubric, report template | `references/review-and-audit.md` |
| Smell → exact fix | `references/anti-patterns.md` |
| Citations | `references/sources.md` |
