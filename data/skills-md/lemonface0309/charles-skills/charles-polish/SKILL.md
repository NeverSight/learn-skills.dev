---
name: charles-polish
description: "Push a working interface from fine to exceptional: hill-climb it through levels, fix the invisible details, and make motion correct frame by frame. Use when a screen or component works but feels off or unfinished, when asked to polish, refine, take it further, or make it feel great, when adding or reviewing animation, or when reviewing UI against a high craft bar. Triggers on polish, feels off, make it better, level up, hover and press states, focus rings, tabular numbers, layout shift, hit areas, optical alignment, easing, springs, duration, transitions, choreography, reveal, morph, flash, jank, stutter, sound and haptic feedback. If the screen still looks AI-generated, run charles-unslop first."
---

# Polish

Built from Emil Kowalski's UI polish and animation skills, Josh Puckett's Interface Craft, and feedback from Charles Liu's "Removing AI Slop" series.

Most work stops at level 3 of 10, because it works and it's easy to stop. The difference between fine and great is rarely the idea; it's how far the idea gets pushed. Most "something feels off" problems are one wrong note, so look, measure and name it before changing anything.

## Run it

1. **Render it,** at its real size and at the smallest size it will be seen. Capture each state and each motion as frames. Measure in the pixels people see: on a scaled stage, a 42 px button may be 37 px on screen.
2. **Score it** against the anchors below and name the weakest thing on screen in one sentence.
3. **Structure:** fix hierarchy and containers before details. Polishing the wrong structure is wasted work.
4. **States:** map every state, including empty, loading, error and success, and design the unhappy ones.
5. **Details:** run the details table.
6. **Motion:** walk the three decision trees, then storyboard.
7. **Verify** frame by frame (below). Nothing is done until you've looked at the frames.
8. **Climb:** run the loop until two passes in a row find nothing that changes the score.

If you were asked to review and not to change anything, stop before step 8 and report each finding as severity, what's wrong, the evidence (frame, number or file and line) and the fix. High means a state is broken or a promise the screen makes isn't kept. Medium means people notice. Low means only a designer does.

### Score anchors

| Score | It means |
| --- | --- |
| 3 | It works, and looks like everything else |
| 5 | Designed at rest, but unhappy states or motion are default |
| 7 | Every state is designed and motion is correct; nothing is memorable yet |
| 8 | One thing people would screenshot, no visible defect at the viewing size |
| 9 | That thing holds up in every state and input path, and a rival would copy it |
| 10 | Don't award this to your own work |

## The climb

Think in levels. Early levels fix what's broken, and you can see what to do. Later levels are invention, and you can't, so use a move:

| Stuck because | Move |
| --- | --- |
| You don't know what better is | **Zoom in.** Take one element at 3×. What if this were the only thing on screen? |
| It's busy | **Remove something.** Did you actually need it? |
| It feels off | **Name it** in one sentence, even before you know the fix |
| It's fine but plain | **Reference the best.** Find the world-class version and list what it does that yours doesn't |
| You keep tweaking one idea | **Generate more.** Make three genuinely different versions, compare at real size, keep one |
| You can't see it anymore | **Critique.** Get a fresh reader with no context, or re-read your own work as a rival would |

Rules for climbing:

- **Each level is one nameable move with a reason.** "Add a spring" isn't a reason; "it can be redirected mid-flight, so it never blocks you" is. If you can't say why in a sentence, the change isn't honest.
- **Make the first leap the biggest.** Going from default to designed must be obvious in a still. If before and after look alike, the default wasn't default enough or the change wasn't structural.
- **Each level is strictly better than the last.** Never ship a deliberately broken step; a demonstrated bug looks like a bug.
- **Name the thing people would screenshot.** If there isn't one, that's the next job.
- **Push the concept into the material,** not effects on top of it. If the idea is a pressure gauge, the needle is the loading state, not a spinner beside it.
- **Undo your own decisions** when they stop holding up. Restraint counts as a level.
- **Land success as the peak.** The end of a flow is what people remember. If success is only a label swap, push the concept into it: the thing the screen has been holding back happens now.
- **Every input path reaches the same ending.** Pointer, keyboard, a slow gesture and reduced motion may travel differently, but all of them end with the same state and the same best detail.

## Details

Absence is what gets noticed, so run all of these. If you're short on time, start with form behavior, hit area, contrast and layout shift, because those are the ones people feel. Express them in the project's own styling system.

| Check | Rule | Why |
| --- | --- | --- |
| Fonts | `-webkit-font-smoothing: antialiased`; subset files | Crisper text, nothing unused shipped |
| Field and button | A resting button and a field never share one fill. The field stays the brightest; a waiting button sits one tone down | Two identical white slabs hide which one you type in |
| Cast light | Window shadows and light patterns stop at an object's edge | Bars running unbroken from the table across paper read as seeing through the paper |
| Dynamic numbers | `tabular-nums` | Digits that change width make neighbors jiggle |
| Weight | Never change `font-weight` on hover or selection; use color | It reflows text |
| Layout shift | Fixed dimensions or `aspect-ratio` for skeletons, images, async content; reserve space for messages | Jumping content reads as broken |
| Typography | `…` `’` `“ ”`; `text-wrap: balance` on headings, `pretty` on body; 45–75ch measure; body leading 1.4–1.6, display ~1.1 | Punctuation and rag are where care shows |
| Tracking | Caps at any size +0.08em. Other text: none below 28px, −0.01em at 28–47px, −0.022em from 48px | Large type wants tighter, caps want air |
| Sizes | At most 5 type sizes, one vertical grid | Fewer things |
| Alignment | At most 2–3 dominant vertical lines; icons on a center spine, text on a left edge | Stray lines are what "off" usually is |
| Optical | Icon side of a button −2 to −3 px padding; play triangles 2 px toward the point; fix asymmetric icons in the SVG | Equal numbers often look unequal, so eyes win |
| Radius | Inner = outer − padding; one radius family | Mismatched nesting is visible |
| Borders | Transparent rings: `box-shadow: 0 0 0 1px rgb(0 0 0/.08)` | They adapt to any surface |
| Style | One icon style, one material, one neutral temperature | The odd one out reads as a bug |
| Color fit | Success and error marks are hues from the page's palette, or adjusted toward it. Real-world meanings stay (a delayed flight may be amber) | A stock green check on an ink page reads as borrowed |
| Contrast | Body and labels ≥4.5:1, large text and icons ≥3:1, measured over the real background. Nothing people must read under 12 px at the viewing size | "Legible" isn't a judgment call |
| Press | `scale(0.96)`, never below 0.95 | Tactile without exaggeration |
| Hover | Named properties, ~150ms; gate to `(hover: hover)`; no layout change | `transition: all` animates things you didn't choose |
| Focus | Keep it; neutral color only | Brand-colored rings clash |
| Hit area | ≥44×44 touch, ≥40×40 desktop, via a pseudo-element; never overlapping; make whole surfaces the target | Small targets miss (Fitts's law) |
| Stacking | `isolation: isolate` or a fixed z-index scale | `9999` means nobody knows |
| Decoration | `pointer-events: none`, `user-select: none` | It can't steal clicks |
| First paint | Resolve state before render: never default-then-correct | Prevents flashes |
| Forms | 16px inputs, real labels, `autocomplete`, Enter submits, errors keep what was typed | Don't punish; prevent |
| Overlap | When one element grows into another, fade the neighbor out and back | Collisions look like bugs |

Shadows, on light surfaces, are layered and tinted toward the light. On dark surfaces depth comes from lighter raised surfaces, softer text and calmer accents; pure black with neon is inversion, not design.

## Motion

### Should it animate?

```
How often will this be triggered?
├── 100+ times a day, or an action fired from a keyboard shortcut → no animation. Speed beats smoothness.
│   (Feedback while typing is allowed if it never delays a character.)
├── Occasionally (modal, menu, drawer)     → standard: under 300ms.
└── Rare or once (success, reveal, onboarding) → may be choreographed, up to ~2.5s.
Then: does it answer a question (where did this come from? did that register? what caused this?)
├── No  → cut it.
└── Yes → continue.
```

### Which curve?

```
Follows a finger, or could be interrupted?  → spring. Default: duration 0.5, bounce 0.
                                              Bounce 0.1–0.3 only for physical, playful things.
Entering or exiting the screen?             → ease-out, e.g. cubic-bezier(0.32, 0.72, 0, 1).
                                              The fast start reads as an instant response.
Already on screen, moving or resizing?      → ease-in-out.
Hover or color change?                      → ease, ~150ms.
Constant (spinner, marquee)?                → linear.
ease-in alone                               → never for an entrance; the slow start reads as lag.
```

### How long?

| What | Duration |
| --- | --- |
| Hover, press, color | 100–150ms |
| Tooltip, dropdown, popover | 150–250ms |
| Modal, drawer, toast | 200–300ms |
| Page transition | 300–400ms |
| Choreographed one-off | up to ~2.5s of motion, with no stretch standing still |
| Holding on words to be read | 250ms per word, at least 1.5s; never counts as dead time |

Exits run 20–30% faster and quieter than enters. If it feels slow, cut duration before anything else.

### Rules

- Animate `transform` and `opacity`. Keep blur under 20px, and never animate layout properties.
- Interactive state uses transitions or springs, which retarget mid-flight. Keyframes restart, so use them for one-shots.
- **Interruptible by default:** never lock input during motion, and start the next motion from where it is on screen. Check where it ends too: a reversal aims at what's selected now, and has no long tail. An action that can't physically undo (a tear, a takeoff) may run to its end, as long as it's short and says so.
- Clicks assist (snap, spring); drags are direct (no easing under the finger). If a level promises something follows the finger, plot the value against drag position: it should change across the whole travel, not jump at the end. At bounds, rubber-band with a dead zone.
- Enter at `scale(0.95)` and `opacity: 0`, never at `scale(0)`, because real objects always have a shape.
- Cap how fast a thrown object can spin when it carries words.
- Scale from the trigger. Paired elements share duration and easing.
- Disable color transitions during theme swaps, so each part doesn't fade at its own speed.
- If a value's effective state doesn't change, nothing repaints. Switching between two settings that resolve to the same look never repaints.
- Animate only the delta: change one digit, not the whole number.
- **No hand-offs between elements mid-morph.** Swapping a pill for a separate element mid-slide twitches. One shape continuously becomes the next (a button's fill narrows to a dot, the dot draws the check).
- Icon morphs interpolate real paths on a spring, and must land on a readable icon.
- Loading is worth watching or invisible: no bouncing dots or generic waves. Use a calm shimmer, timed steps, or optimistic state.
- Respect `prefers-reduced-motion`: same information, no movement.
- Don't play entrances on things already at rest at page load.

### Physical motion and choreography

Honor the metaphor: if it's paper, it doesn't fade and doesn't pass through things. Then layer:

- **Anticipation:** a small counter-move before the big one.
- **Arcs:** travel curves, because nothing real moves in a straight line.
- **Squash and stretch, follow-through, overlapping action:** parts arrive at different times, and small parts react to big ones.
- **Clear before coming forward:** an object leaves its container before it scales past it.
- **Compound motion:** a small loop on top of the main motion.
- **A target at all times:** the eye always has somewhere to go. Empty sky between two beats is a dead stretch; cut it or give it a destination.

Write multi-stage motion as a storyboard with named timing constants at the top of the file:

```js
/* 0ms lifts · 120ms flips on an arc · 460ms lands, squashes · 570ms flap opens */
const TIMING = { lift: 0, flip: 120, land: 460, flap: 570 };
```

Tune live, then hard-code. Layer simple parts rather than one clever effect: a value mapped to a range and eased, a wave with a phase offset, a gradient + noise + mask.

### Sound and haptics

Add them only to rare or physical moments. Every sound has a visible cause on that same frame (multimodal feedback only works in sync). Nothing on resets or passive state changes, and no key clicks by default; soft, short and consistent beats clever.

Choose each sound from the product's own world by naming the real object that makes it: a travel app has a cabin's switch, chime and air; a pottery shop has paper and a ceramic tink. If it could be a game's pickup sound, replace it, because bright UI-kit tones make a premium screen feel like a toy.

## Verify frame by frame

Drag every scrubbed control slowly out and back, and read each frame on the way back. A value going to zero must get there continuously: scale a feather, blur or stroke with the shape it belongs to, because at a fixed width it stays on screen as a soft dot until the shape pops off. When two layers hand over, close the inner one fully before fading the outer one.

Motion you haven't looked at frame by frame isn't verified. Drive it from a controllable clock and capture at 60 fps. Don't try to eyeball hundreds of frames: plot the pixel difference between neighboring frames first, because a pop is a spike and a dead stretch is a flat line. Then look at the frames around each one in a labeled strip. Screenshots time out on a busy machine, so run one capture at a time. Check:

- [ ] **First frame:** the response starts at once. A simulated network wait, a press being held or a scripted hand reaching isn't a dead frame, but the wait still shows something happening.
- [ ] **Origin:** if something emanates from a trigger, measure it. The start point equals the trigger's center in screen space, including under any camera or scale transform. Print the numbers. Motion that reads in order, like a chart filling left to right, is exempt.
- [ ] **Last frame:** it settles with no pop, snap or re-layout.
- [ ] **No flash:** no frame shows a wrong state. Test every state pair, e.g. all six transitions among three themes, under both OS schemes, with pixel probes where the risk is real.
- [ ] **Readable:** hold words long enough to read before the camera or the next beat moves on.
- [ ] **No twitch:** no backward jump or element swap mid-move.
- [ ] **No collisions:** nothing overlaps or clips by accident.
- [ ] **Text survives:** where text passes through refraction or a transform, glyphs bend without shattering or fringing.
- [ ] **Reversal:** where it can be undone, interrupt it halfway. It returns smoothly, to the right place.
- [ ] **Same ending:** pointer, keyboard and reduced motion finish on the same state.
- [ ] **Empty submit and stopped states** say something in words.
- [ ] **Reduced motion,** keyboard path, and no console errors.

Then check at the final viewing size: the smallest important text is legible, and the change you're proud of is visible there. If it's only visible at full size, move the camera or redesign it.

Final read: what's the weakest thing on screen now? If fixing it would change the score, you aren't done. If it wouldn't, stop.
