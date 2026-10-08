---
name: animaxxing
description: "Build GSAP motion without restyling, as single effects or the full treatment: for \"we're animaxxing\", every element enters from a blank page, rests, and leaves. Text: split, scramble, glitch, typewriter, and speak-in entrances, scattering headlines, letter waves, text on a path, count-ups, odometers. Scroll: reveals, scrubbing, parallax, pinned scenes, stacking cards, zoom-through, horizontal runs, waypoints, smooth scroll, paging. Pointer: magnetic, tilt, spotlights, directional fills, press ripples, shakes, cursor followers, image trails, proximity, label rolls, underlines, weight hovers. Drag: throw tracks, endless loops, card stacks, sortable lists, swipe to dismiss. Also page covers, print effects, Flip morphs, menus, dialogs, tabs, state buttons, media and SVG effects, marquees, CustomEase, sound, confetti, particles, and hover stuck on touch. Also finds a feel: premium, calm, playful. Pair with the matching GSAP framework skill. Not for visual redesign, routing, or GSAP API questions."
license: MIT
metadata:
  short-description: Reusable GSAP text, scroll, pointer, layout, SVG, and particle motion for any brand
---

# Animaxxing

Portable vanilla TypeScript and GSAP effect recipes. Keep the project's fonts, colors, layout, and component styling; no style skill, token, or font is required.

Load the matching `gsap-<framework>` skill first (`gsap-vanilla` for plain sites), installing it if missing. It owns **mount → initial state → intro → settled → outro → end state → unmount**, initialization, navigation, recovery, interruption, and cleanup timing. This skill supplies builders its controller calls; do not invent lifecycle guidance here.

## Choose the scope

- **Full treatment.** "We're animaxxing", "animax this", or "full treatment" means every element on every screen animates, keeping the brand. Each element starts from a blank first paint, enters (intro), rests static or ambient (settled), and leaves (outro) on every requested navigation. Content below the fold enters when it is scrolled or tabbed to. Mark every element as a page item ([route letters](references/recipes/route-letters.md)) or give it a pair from [the shelf](references/motion-vocabulary.md#the-shelf-paired-entrances-and-exits); the framework skill keeps the first paint blank. Record the decision in the project's plan or notes so later sessions keep it.
- **Single effects.** A named effect gets only that effect. A particle button does not imply a page transition, font change, or hero sequence.
- **A feel, or no effect named.** "Make it feel premium", "add some animation": read [Finding the vibe](references/finding-the-vibe.md) before choosing any effect. Read the feel from the project, then say the plan in a line or two before building.
- **Unclear.** When the project's own cues settle the feel and how much motion it wants, say the plan in a line or two and build. Ask only when they don't, and then once: "Full treatment on every element, or only <effect>?", folding in the feel if that is open too.
- The full treatment still follows reduced motion, no-script readability, and the framework skill's initialization and lifecycle.

## Setup and adaptation

- Read the installed GSAP version and types. Every plugin used is free since 3.13; SplitText recipes need 3.13+ (`SplitText.create`, `smartWrap`, `mask`, `aria`); `easeReverse` needs 3.15+. Each recipe lists its dependencies; register only those used. Use the official GSAP skills for API details.
- Recipes register plugins at module scope, which is server-safe, but import them only from client code. Drop a copy's registration when the project registers plugins centrally.
- Add only requested effects unless the full treatment applies; see [Choose the scope](#choose-the-scope).
- Recipe constants are editable defaults, not brand rules. Tune timing, stagger, spread, and intensity to the surface; expose more constants only if the app needs runtime configuration.
- Weight effects need a loaded variable weight axis, not a specific font. Match endpoints and resting weight to the face (examples use 400–800), or use transform-only effects.
- Particle canvases take their CSS `color`; use an existing brand color with enough contrast. Keep control geometry and focus styling.
- Use `style-animaxxing` only when its look is requested; it selects and configures these recipes.

## Read only what you need

| Task | Reference |
|---|---|
| The feel isn't settled: a full treatment, a new project, or a user describing a mood | [Finding the vibe](references/finding-the-vibe.md) |
| Choose in/out effects, configure defaults, coordinate with the controller | [Motion vocabulary](references/motion-vocabulary.md) |
| A brand's signature curve for every `ease` option | [Signature curves](references/motion-vocabulary.md#signature-curves) |
| Loading flashes, auth-dependent content, or layout shifts | Matching installed framework skill's `references/initialization.md`, **Data readiness and layout stability** |
| Character animation: font readiness, kerning, masks, stable split/revert; weight or width moves inside a line of text | [Text stability](references/text-stability.md) |
| Character, word, line, scramble, or glitch entrances/exits, implode and explode, ellipse line reveals, highlighter line sweeps | [Split entrances](references/recipes/split-entrances.md) |
| Page items, including scattering headlines | [Route letters](references/recipes/route-letters.md) |
| Short display copy arriving at speaking pace | [Speak-in](references/recipes/speak-in.md) |
| Text typed behind a caret, deleted, or a word that retypes through a list | [Typewriter](references/recipes/typewriter.md) |
| Ambient headline ripple | [Wave](references/recipes/wave.md) |
| Scroll reveals and pop-ins, scrubbed statements, parallax and footer reveals, pinned scenes, stacking cards, zoom-through to the next scene, horizontal runs and drift inside them, an element traveling between section waypoints, progress, velocity skew, header theme per section, hide-on-scroll headers | [Scroll effects](references/recipes/scroll-effects.md) |
| Magnetic buttons, tilt cards, spotlight reveals, cursor follower and its scrolling label, momentum hover, proximity scaling and dock effects, image trails, drag-and-throw tracks, swipe to dismiss | [Pointer effects](references/recipes/pointer-effects.md) |
| Endless drag galleries: a wrapping loop with snap, wheel, and drift; a 2D grid that wraps on both axes; a fanned card stack dealt by drag or flick | [Endless drag](references/recipes/endless-drag.md) |
| Lists reordered by dragging a handle or with the keyboard | [Sortable](references/recipes/sortable.md) |
| Full-screen sections changing on a wheel flick, swipe, or key | [Section pager](references/recipes/section-pager.md) |
| Opt-in sound on interactions and timelines, ambient beds | [Sound cues](references/recipes/sound-cues.md) |
| Line drawing, icon morphs, a shape flowing through a sequence of shapes, a mark following a path, a section edge that morphs with scroll, text riding a path or turning around a badge | [SVG effects](references/recipes/svg-effects.md) |
| Printmaking: an image or block painted on with a dry brush, text that inks in through grain or is written on by a brush, a second impression slipping into register, a corner pulled back and peeled off | [Print effects](references/recipes/print-effects.md) |
| Thresholds and arches: a picture opening out of an arch to fill its frame, a scrolled passage through a doorway into the next picture, a picture flying from a card into an arch and taking its shape | [Doorways](references/recipes/doorways.md) |
| A beat that draws the eye then rests (a ring from a live dot, a heartbeat, a badge bump), and ambient loops that float, drift, breathe, or orbit while on screen, with a pause | [Pulse and ambient](references/recipes/ambient.md) |
| Count-up figures, odometer digits rolling to new values, looping marquees, logo walls that cycle | [Counters and marquees](references/recipes/counters-and-marquees.md) |
| Eased page scrolling with Lenis or ScrollSmoother | [Smooth scroll](references/recipes/smooth-scroll.md) |
| Curtain page transitions, tilted, titled, clip-path wipe, or drifting covers, curved SVG swipe covers, first-visit preloaders | [Page covers](references/recipes/page-covers.md) |
| Filter, reorder, and expand layouts; shared-element morphs across pages | [Layout Flip](references/recipes/layout-flip.md) |
| Image wipe reveals, a liquid pour reveal, hover image previews, scroll-scrubbed video, canvas frame sequences | [Media effects](references/recipes/media-effects.md) |
| Label rolls, underline sweeps, direction-aware fills, weight or width hovers in running text, image zoom on hover and focus, liquid hovers (a bead underline, a poured round fill, a jelly button) | [Hover effects](references/recipes/hover-effects.md) |
| A control that squashes and ripples when pressed, by any input | [Press feedback](references/recipes/press-feedback.md) |
| A shake for an error or refused action | [Accents](references/motion-vocabulary.md#accents) |
| Menu overlays, interruptible enter/exit with reverse easing, dialog enter and exit, accordion height, sliding tab indicators, buttons that show loading, success, and failure | [Component motion](references/recipes/component-motion.md) |
| Dispersal on a call to action | [Blast-off](references/recipes/blast-off.md) |
| Confetti bursts and emoji rain thrown under gravity | [Physics effects](references/recipes/physics-effects.md) |
| Particle buttons, cards, links, or command fields | [Particle effects](references/recipes/particle-effects.md) plus [field/attach helpers](references/recipes/particle-field.md) |
| Touch, focus, stuck hover, mobile particle budgets | [Input and devices](references/motion-vocabulary.md#input-and-devices) |
| Roll back partial setup and restore modified content | [Effect restoration](references/effect-restoration.md) |
| Verify effects and reuse on another brand | [Verification](references/verification.md), then the framework's relevant checks |

## Recipe contract

Copy only the selected recipe and its named local helpers. Return shapes differ per recipe (timelines, `{ timeline, revert }`, stop functions, particle controls); assume no universal interface.

| Framework phase | Effect responsibility |
|---|---|
| initial state | Targets prepared under the framework's pre-paint/no-script mechanism |
| intro | Entrance builder or `enter(delay)` |
| settled | Clear temporary styles; optional `idle()` or wave |
| outro | Exit builder, `exit()`, or `blastOff(...)` |
| end state | Notify completion; controller decides the next action |
| unmount | Controller calls the recipe's stop, `destroy`, or `revert` handle |

- Apply [effect restoration](references/effect-restoration.md) when copying a recipe, including failure before a handle returns.
- Builders never navigate, mount, subscribe to page lifecycle, or decide when they run. The controller calls them and owns phase state.
- An invisible start does not make incomplete data ready. The controller supplies resolved targets or reserved regions; never use an entrance to disguise guest or empty content.
- Keep split markup only while an effect needs it (speak-in finishes and an active wave persist). Revert at the controller's cleanup boundary; preserve accessible text and nested controls.
- Use `overwrite: "auto"`; clear temporary styles and `will-change` when their phase ends.
- Park a start position with `gsap.set` or `fromTo`, never with a CSS transform the tween also moves: GSAP reads CSS `translateY(100%)` as pixel `y` and adds `yPercent` on top, so a cover lands a full height short. A CSS transform is fine as a resting pose that a `from` tween lands on.
- Reduced motion reaches the documented settled or exit state and still fires completion callbacks; no ambient motion. Use the project's preference helper, including any app override. Builders read it when they build; on a change, the controller tears down and rebuilds.
- Killing a parent timeline never reaches a nested builder's interrupt callback. Kill the parent, then call each builder's revert, such as `revertText` for split runners.
- One effect per target: two owners must never write one element's transform. Stop pointer and ambient effects before an outro moves their target.
- Ambient effects expose controls so the owner can pause them off screen and stop them on exit. Loops past five seconds need a user-facing pause ([WCAG 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide)).
- Particle input and density follow the [field contract](references/recipes/particle-field.md#input-and-density). Controls work without hover.
- Text keeps its line breaks from first paint to rest. Wait for the faces before measuring or splitting, keep text hidden until they load (briefly at most), never tween letter-spacing, width, or weight on text that wraps, and animate a paragraph as one block unless its split lines match the resting breaks. [Verification](references/verification.md) has the check.
- Width changes can invalidate split measurements ([resize](references/motion-vocabulary.md#resize)). The controller decides whether to rebuild; recipes never remount pages.
