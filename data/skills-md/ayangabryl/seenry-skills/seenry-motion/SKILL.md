---
name: seenry-motion
description: "Build, review or research interface motion: press feedback, menus, tooltips, dialogs, sheets, toasts, accordions, tabs, page and shared-element transitions, scroll effects, drag and gestures, number and icon changes. Decides whether something should animate at all, then picks the tool, properties, curve, duration or spring, interruption and reduced-motion behavior, with tested modern-CSS recipes and runnable assets. Also studies recorded motion from Seenry references."
license: Apache-2.0
metadata:
  author: Seenry
  version: "0.1.0"
---
# Seenry Motion

Motion exists to explain a change: where something came from, what the input did, what state the interface is in now. Build every animation through the sequence below, in order; steps 1 and 2 decide whether any code gets written at all.

Make the call and state it in one line; do not offer a menu of motion options. Extend the project's existing motion tokens and components instead of adding a parallel set.

## The build sequence

**1. Should it animate at all?** Decide by frequency.

| How often people see it | Decision |
| --- | --- |
| 100+ times a day (command menu, keyboard shortcuts, list navigation with arrows) | No animation. Instant. |
| Tens of times a day (hover, tabs, toggles) | Brief opacity/color feedback on the existing state clock, or nothing; never delay the accepted state |
| Occasionally (menus, dialogs, sheets, toasts) | Standard motion from the table below |
| Rarely (onboarding, first success, empty-to-full moments) | Room for character |

Keyboard-triggered actions never wait on animation. If the gate says no, say so and ship the instant state change.

**2. Name the purpose** in one word: feedback, orientation (where it came from or went), state, continuity (avoid a jarring jump), explanation (marketing and onboarding only), or delight (rare moments only). No purpose, no animation. Data people are reading never moves for style.

**3. Pick the cheapest tool that works.**

| Need | Tool |
| --- | --- |
| Hover, press, color, class or attribute toggle | CSS transition |
| Entrance on mount, exit before `display: none`, native `<dialog>` and `popover` | CSS transition + `@starting-style` + `allow-discrete` |
| Height to `auto` | `interpolate-size: allow-keywords`, or the grid `0fr → 1fr` track |
| Route changes, list → detail, morphing indicators | View Transitions API |
| Scroll-linked effects | `animation-timeline: view()` / `scroll()` |
| Programmatic, cancellable, no library | Web Animations (`element.animate`) |
| Springs with velocity, layout animation, gestures, presence in React | Motion (`motion.dev`) |
| A whole component (toast, drawer, command menu, select) | A maintained library, see [libraries](../seenry/references/libraries.md) |

**4. Pick the properties.** `translate`, `scale`, `rotate`, `opacity`, `clip-path`, `filter` only. Never enter from `scale(0)`: start at 0.95–0.97 with opacity 0. Popovers scale from their trigger (`transform-origin` on the trigger side); dialogs scale from center. Percent translates (`translate: 0 100%`) move by the element's own size.

**5. Pick the curve and duration, or a spring.**

| Motion | Duration | Easing |
| --- | --- | --- |
| Press feedback | 100–160ms | `--ease-out` |
| Tooltip, small popover | 120–200ms | `--ease-out` |
| Menu, dropdown, select | 150–250ms | `--ease-out` |
| Dialog | 200–250ms | `--ease-out` |
| Sheet, drawer | 350–500ms | `--ease-drawer` |
| Element moving across the screen, morphs | 250–400ms | `--ease-in-out` |
| Color, background, border on hover | Existing state token; the Transitions kit uses 180ms | Existing state curve; the kit uses `cubic-bezier(.25,0,.06,1)` |
| Progress, marquee, hold-to-confirm fill | as long as the work | `linear` |

`--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`, `--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)`, `--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1)`. Never `ease-in` on interface motion: it delays exactly the moment people are watching. Prefer product UI under 300ms; longer sheet travel needs a reason. Exits are often ~20–30% faster than entrances, unless preserving a direct manipulation or spatial relationship warrants the same clock. Use a spring for anything the user drags, flicks or can reverse mid-way: Motion `{type: "spring", duration: 0.5, bounce: 0.2}` (bounce 0 for product UI, ≤0.3 for playful), or the CSS `linear()` springs in [recipes](references/recipes.md).

**6. Plan interruption and exit.** Prefer CSS transitions for reversible property changes because they retarget from the current value. When geometry or choreography needs WAAPI, capture the current rendered state, cancel or retarget owned animations, and guard stale completion. A second input reverses or replaces the old request rather than queuing behind it. Publish the new logical state immediately; a separate presentation state may keep an exit painted.

**Refine the interrupted change.** Use these checks where they fit the component. They are design heuristics, not a guaranteed judge score. Try repeated inputs during entry and exit, including 50–150ms apart; record actual timings when making timing claims.
- **Retain continuity and semantics.** Related tabs, filters or status states can share one grid cell (`display:grid`, `grid-area:1/1`) and transition opacity or a small translate. Keep inactive content out of the focus order and accessibility tree; mounted does not mean interactive. A quick outgoing phase (roughly 65–90ms) and incoming 120–160ms can be a starting point, not a required recipe. Unmount or hide only when the current transition permits it; a stale completion must never hide a newer state. Explicitly cancellable WAAPI and guarded native-dialog exits are valid alternatives.
- **Keep the result understandable.** Avoid accidental blank intervals or unreadable competing text. Choose overlap, a short crossfade or an instant replacement based on content; a whole-label endpoint fade may be safer than moving text through artwork. Preserve an appropriate static cue while motion is unavailable or reduced. Inspect actual readability rather than using an opacity threshold as proof.
- **One copy of a travelling thing.** When a title, avatar or cover moves to a new place, avoid visible duplicate paint. Hide the destination until the traveller lands, then retire the temporary copy. Trace the text against the artwork and moving shell; an unclipped endpoint does not prove a readable path.
- **The label agrees with its result.** A label such as “Mark paid” becoming “Paid” follows the same accepted application state as its result. Reserve its footprint when useful and prevent stale text or focusable duplicate labels. Do not delay a real success state just to finish decoration.
- **Sequences can be cancelled.** Typing demos, staged reveals and replays share an owner for pending steps. Pause, reversal and new input cancel obsolete work and retarget visible motion from its current state. A stale timeout must not resume a paused sequence or overwrite newer content.
- **Release finished animations.** Establish the settled state through CSS or committed styles, then release finite owned WAAPI animations when appropriate. `fill:forwards` must not keep overriding later state changes. Check for unexpected animations after the interaction settles, while allowing a purposeful ongoing loading indicator until its work ends.
- **Each move explains a relationship.** Menus grow from their trigger, panels from their edge, and related content moves consistently with navigation. Use the duration ranges above as starting points; keep perceived response immediate and justify longer travel. Test interruption and reduced motion rather than treating a fixed duration as proof of quality.

**Reaching 9.** On the motion judge, 7 is correct but generic, 8 is clearly premium and 9 is distinctive at the level of Apple or Linear. Rounds stall at 7–8 for the same few reasons. Handle all of them before spending a run:
- **One component at a time.** Judge each component alone with `--labels "<Row>"` until it scores 9, and keep the best version of each. A catalog's overall follows its weakest rows, so patching many rows at once never moves it, and a change that lowers a row is reverted even when the judge suggested it.
- **Apply every fix, not only the headline one.** Small items that recur (hover, press and close-control feedback) hold `states` at 7 round after round. `--prev <last motion.json>` lists the criteria that did not rise and the interactions asked to fix again; `check.mjs` passes it automatically.
- **A problem that returns after its fix is structural.** Retiming cannot fix a path that crosses. Shared elements keep their relative arrangement between states: a title below its cover stays below it in the detail view, so neither passes through the other.
- **No empty frames.** At every filmed moment (30–320ms) the changed region shows real content. A shell carries its content as it grows; a streaming answer grows from its first words. Never show a blank answer box or a skeleton that waits and then dissolves.
- **One crafted idea per component.** What persists travels and what is new is born from its cause. A fade, a 4px translate and a label swap score 7.
- **Match dismissal to the flow.** For a directly expanding card or toggle surface, preserve the source action point when the control becomes its return action. Judge confirmation dialogs by their meaningful actions, safe Cancel path, appropriate Escape behavior and focus return; do not require a redundant Close or X button or move Cancel to the launcher merely to satisfy a spatial rule. Use Back for a navigation flow when appropriate. Evaluate the actual way out and its state, not the presence of a particular icon. Menus and popovers need no close button: they dismiss on selection, outside click and Escape, and a menu that morphs from its button folds back into it. When a surface replaces a whole region (an expanded card or album), put Close at the header's top-right; never pin a control to a stale source position where it can float in leftover space or overhang its surface.
- **A single run is not a score.** One judge run (itself a median of three) moves by a point on unchanged code. Accept a 9 only when two separate runs both reach it, and compare versions on the same number of runs.

**7. Ship reduced motion and input gating with it.** Under `prefers-reduced-motion: reduce`, remove movement, parallax, blur and loops; keep short opacity changes that aid understanding. Keep ordinary control hover still: change its tint or ring, not its position, scale or layout. Gate hover feedback with `@media (hover: hover) and (pointer: fine)`; a deliberately requested pointer-tracking material demo is a separate interaction, not the default hover treatment. Every animated state change also leaves a static cue (label, icon, color) for when motion does not run.

## Recipes

Start from [recipes](references/recipes.md) for press feedback, menus and popovers, tooltips, dialogs, sheets, toasts, accordions, staggered entrances, tab indicators, page and shared-element transitions, scroll reveals, icon swaps, number changes, hold-to-confirm, drag-to-dismiss (with velocity projection and rubber banding), crossfade masking, theme switching and first-render suppression. The native-CSS recipes are exercised in Chromium by the package tests.

## Runnable assets

| Requested change | Focused route |
| --- | --- |
| Action menu or short status label | Original [action menu](assets/action-menu/README.md), [status switch](assets/status-switch/README.md) and [product transitions](references/product-transitions.md). If the menu is asked to animate open and closed, preserve its surface through the closing phase; conditional unmount on close skips that phase. For a status transition, move the text in a reserved slot; a plain text replacement or dot-color change alone is incomplete. The application owns the real action. |
| In-flow disclosure or changing geometry | Original [expanding card](assets/expanding-card/README.md), [geometry helper](references/adapters.md) and [surface patterns](references/patterns/surfaces.md). Preserve focus and retarget from current geometry. |
| Focused modal task | Original [modal surface](assets/modal-surface/README.md) and [surface patterns](references/patterns/surfaces.md). Use a native dialog for top-layer and focus behavior; allow the exit to finish before closing, and make reversal cancel the pending close. |
| Changing number or icon | [Number transitions](references/number-transitions.md) and [adapters](references/adapters.md). For a small integer count, prefer the original count-pop helper over rebuilding digit semantics. Keep one real accessible value; do not hide every digit and put `aria-label` on a plain `<strong>`. A digit transition needs per-place motion; keep units anchored. |
| Live voice input or output | Original [voice presence](assets/voice-presence/README.md) accepts application-owned state and a normalized audio level. Keep controls and announcements in the DOM; a generated demo signal is not microphone activity. |
| Loading or process presence | Original [signal field](assets/signal-field/README.md), [boundary trace](assets/boundary-trace/README.md) and [loading patterns](references/patterns/loading.md). Animation time is not progress. |
| Decoded image or expressive material | Original [image reveal](assets/image-reveal/README.md), [reflective solid and rim surfaces](assets/reflective-surface/README.md), [pointer tilt](assets/pointer-tilt/README.md), [surface effects](references/surface-effects.md) and [expressive effects](references/expressive-effects.md). Keep useful content while a replacement loads; use reflection and tilt only where the material has a purpose. |
| Designing any new interactive component (brief, state graph, motion score, input contract, checklist) | [Interaction craft](references/interaction-craft.md) |
| Toast or banner stack | [Feedback patterns](references/patterns/feedback.md) and original [notification reducer](assets/notification-state.mjs). Remove overflow from active state before its exit; test the fourth event in a three-item stack. |
| Occasional completed milestone | Original [confirmation burst](assets/confirmation-burst/README.md). Record success in application state first, then play the finite decoration; the settled result must remain visible after it clears. |
| Selected tabs or ordered page change | Original [selection surface](assets/selection-surface-demo.html) for a shared highlight and [directional stage](assets/directional-stage/README.md) for related views; the application owns selection, panels, route and history. Use [navigation patterns](references/patterns/navigation.md) for other structures. |
| Scroll or a coordinated system | [Scroll choreography](references/scroll-choreography.md), [worked scores](references/worked-scores.md), [system choreography](references/system-choreography.md) and the [motion index](references/patterns.md). |

Select only the guide and helper needed for this change. The bundled original assets are reusable starting points, not automatic substitutes for a named source component or proof of fidelity to it. Keep licenses with any copied third-party runtime; the original Seenry assets use the repository's Apache-2.0 license.

## Never ship

| Never | Instead |
| --- | --- |
| Animation on a 100+/day or keyboard-driven action | Instant change |
| `transition: all` | Name the properties |
| Entrance from `scale(0)` | `scale: 0.96` + `opacity: 0` |
| `ease-in` on UI | `--ease-out` |
| Default `ease`/`ease-out` on a deliberate entrance | The custom curves above |
| Product UI motion over 300ms without a reason | 150–250ms |
| Popover scaling from its center | `transform-origin` at the trigger |
| Uncontrolled keyframes on re-triggered interactions | Retargetable transitions or explicitly cancellable WAAPI |
| Animating `width`, `height`, `top`, `left`, `margin` | Transforms; grid-track or `interpolate-size` for height |
| Moving or scaling an ordinary control on hover | A still tint or ring change, gated to a fine hover pointer; reserve scale feedback for press |
| No reduced-motion variant | Opacity-only or instant |
| A long list entering item by item | 30–50ms stagger capped at ~300ms total, or none |
| Motion as the only sign of a state change | A static cue as well |
| A token that holds `duration easing` inside `transition-duration` (the whole declaration is dropped and every state change becomes instant) | Plain durations in duration lists; confirm in computed style that `transitionDuration` is not `0s` |
| A `display` rule on a filterable item that beats the `[hidden]` attribute | `:not([hidden])` on the layout rule; check that hidden items are neither painted nor tabbable |
| A colour change crossfading a second shape over a morphing surface | One surface whose own fill changes while it unfolds |

## Output

Write the code, then report in a few lines: the gate result (frequency and purpose, or why nothing animates), the ingredients (tool, properties, duration, curve or spring), and what was checked (normal speed, 10% speed in DevTools Animations, rapid repeat, reversal, keyboard, reduced motion, phone).

## Research the observed behavior

When matching a supplied reference, inspect playback at normal speed and useful intermediate frames, not only endpoints. [Motion research](references/research-route.md) explains recordings, Seenry MCP, creator studies and source limits; load it only when research is needed. A static image cannot establish timing, interruption or keyboard behavior. Without playback, implement a proposed treatment and test it locally.

**Recorded phase check:** Match source checkpoints to the running browser animation. State jumps verify endpoints, not timing. See [motion reconstruction](references/replication.md).

## Verify

Start with the static scan, which needs no browser and finishes in well under a second: `node ../seenry/scripts/motion_scan.mjs <project>`. It flags off-token durations, delays and curves, browser-default and linear easing, `transition: all`, layout-property transitions, stagger steps above 20ms and a missing reduced-motion branch, with the nearest token for each. Fix its violations and the warnings you cannot justify, then verify the behaviors you changed using the [interaction verification checklist](references/verification.md). A small fix needs its affected states and a regression check, not a new whole-site benchmark. Inspect normal-speed playback and useful slow-motion frames; check internal text/control fit as well as document overflow. During reversal, assert the final logical and accessible state and inspect the actual moving layers, not just their fixed container.

When the sibling `seenry` skill runtime and authorized model access are available, resolve `../seenry/scripts/motion_judge.mjs` from this skill's installed directory and run it with Node against the page. Do not assume the caller's working directory is the skill directory. If the runtime is absent, report that check unavailable. For web evidence, its acceptance floor is 9 in every declared motion criterion and every reviewed interaction row, with no violations and a row for each captured interaction label. Missing criteria or label coverage are unverified; high overall cannot average away a weaker row. The report names its captured scope and does not certify untested components. Native-video legacy judging remains a separate contract. Use the findings to inspect the relevant interaction. Keep that judgment separate from functional and rendered checks; an unavailable judge or missing recording is unverified, never a pass. Try relevant keyboard, narrow-width and reduced-motion states. For gestures, use touch emulation and a real phone when available, and report which you actually tested.

For deeper mechanics read [motion craft](references/motion-craft.md), [interaction anatomy](references/interaction-anatomy.md), [product transitions](references/product-transitions.md), [scroll choreography](references/scroll-choreography.md), [surface effects](references/surface-effects.md) and [number transitions](references/number-transitions.md). Use **seenry** for overall interface direction and material.
