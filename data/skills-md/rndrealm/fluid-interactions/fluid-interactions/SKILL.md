---
name: fluid-interactions
description: "Build gesture-driven web interfaces that feel native: drags, flicks, sheets, swipe-back, swipe actions, pull to refresh, scrubbers, card-to-detail morphs and app-switcher style gestures. Use when adding or fixing anything the user drags, flicks or swipes, when an animation needs to start from the finger's speed, when something should rubber band at an edge, or when a gesture feels stuck, jumpy or janky on touch."
---

# Fluid interactions

Interfaces where motion behaves like physical objects instead of playing back a timeline. That covers:

- **Gestures:** things follow the finger, carry its speed when released, land where a flick was heading, resist at their edges, and can be caught mid-animation.
- **Transitions:** sheets, navigation, and views that grow out of the thing you tapped and can be dragged back.
- **Gesture modes:** one gesture doing different things depending on how it moves.
- **Getting it right everywhere:** touch quirks, performance, and reduced motion.

## Use motion

Always build these interactions with [motion](https://motion.dev). Its springs start from a velocity, its motion values update without re-rendering, and it follows reduced motion, which is everything this skill relies on. Don't use GSAP, anime.js or CSS transitions for them; the code here and in the references assumes motion. (The one hand-written loop, coasting in a custom scroller, still writes to a motion value and hands off to a motion spring.)

**Install it before writing any code** if it isn't in `package.json`, using the project's package manager (check the lockfile):

```sh
npm install motion     # package-lock.json
pnpm add motion        # pnpm-lock.yaml
yarn add motion        # yarn.lock
bun add motion         # bun.lock / bun.lockb
```

- **React:** import from `motion/react` (`motion`, `animate`, `useMotionValue`, `useTransform`, `MotionConfig`, `useReducedMotion`).
- **Already has `framer-motion`:** that's motion under its old name. Use it as it is, importing from `framer-motion`; don't install both.
- **Already uses another animation library:** keep it for whatever it already does, and add motion alongside it for these interactions. Don't rebuild these patterns in the other library.

Never fake a spring with a duration and an easing curve (`elastic`, `back`, cubic-bezier overshoot). They can't start from the finger's speed.

## The rules

1. **Animate with springs, not durations.** A spring only needs a target and a starting velocity, so it can pick up from wherever the finger left off. Describe springs by response (seconds) and damping ratio with `springFromResponse`, not raw stiffness and damping. See [springs](references/springs.md).
2. **Hand the release velocity to the spring.** Track the pointer with `VelocityTracker` (last 100ms only) and pass `velocity` into the animation. Without it, the element stops dead for a frame before setting off.
3. **Everything is interruptible.** On pointer down, `stop()` the animation and read the current value as the new origin. Never block input while something is animating. Decide state (open or closed, which page is current) from where an animation is **heading**, not from the value or `onComplete`: a spring looks done long before it finishes. See [drag and momentum](references/drag-and-momentum.md) and [decide from the target](references/springs.md#decide-from-the-target-not-the-value).
4. **Decide where it lands from where it was going.** On release, `project(velocity)` gives where a flick would coast to; snap to the nearest target from that point, not from the release point. That is what lets a short, fast flick skip a detent.
5. **Rubber band past the edges** instead of hard-stopping: `applyRubberBand(value, min, max, d)`. The further you pull, the less it moves.
6. **Directions that lead nowhere resist.** If only one direction does something (down dismisses, right goes back), the others still move, but under a rubber band, then spring back on release. Don't freeze them and don't let them move freely: free movement suggests an action that isn't there. This is only for something the user is holding that moves freely. If the other axis belongs to something else (page scroll, a parent list), hand it off with a direction lock instead of rubber banding. See [drag and momentum](references/drag-and-momentum.md#directions-with-no-action).
7. **Lock the direction before acting.** Wait about 10px, then commit to an axis. Only capture the pointer after the lock, so taps and the other axis (usually native scroll) still work. See [direction lock](references/direction-lock.md).
8. **Per-frame work never touches React state.** Use refs and motion values (or direct DOM writes). Only set state on release or on a discrete change.
9. **Move with transforms, not layout.** `x`, `y`, `scale`, `opacity`. Read layout (`getBoundingClientRect`, `clientWidth`) once at the start or end of a gesture, never every frame.
10. **Always end the gesture.** Handle `pointerup`, `pointercancel` and `lostpointercapture`. A gesture that misses its end leaves the UI stuck. See [pointer events](references/pointer-events.md).
11. **Respect reduced motion** by softening what moves by itself, never what the finger drives. See [reduced motion](references/reduced-motion.md).
12. **One gesture can mean several things.** How it moves (where it started, distance, speed, a pause, a second axis) can pick between related outcomes, like swiping up to go home or pausing to open the app switcher, or moving away from a scrubber to scrub more finely. The plain version must always work, and the mode must show before release. See [gesture modes](references/gesture-modes.md).

## Code

Copy these into the project and adapt them. `physics.ts` has no dependencies; the hooks need React, and `use-motion-preference.ts` needs motion.

- [code/physics.ts](code/physics.ts): `springFromResponse`, `noBounce`, `VelocityTracker`, `rubberBand`, `applyRubberBand`, `rubberBandInverse`, `project`, `DECELERATION`, `nearest`, `nearestPoint`, `clamp`, `FADE`.
- [code/use-drag.ts](code/use-drag.ts): a pointer-events drag hook that reports the offset from the start and the release velocity, and always calls `onEnd`.
- [code/use-motion-preference.ts](code/use-motion-preference.ts): `{ reduceMotion, spring }`, where `spring()` drops the bounce when reduced motion is on.

## The basic shape of every gesture

```tsx
const x = useMotionValue(0);
const origin = useRef(0);

const drag = useDrag({
  onStart: () => {
    x.stop(); // catch it mid-flight
    origin.current = x.get(); // continue from where it is on screen
  },
  onMove: (delta) => {
    x.set(applyRubberBand(origin.current + delta.x, min, max, width));
  },
  onEnd: (velocity) => {
    const landing = x.get() + project(velocity.x);
    animate(x, nearest(landing, targets), {
      ...spring(SNAP),
      velocity: velocity.x,
    });
  },
});

return (
  <motion.div {...drag} style={{ x }} className="touch-none select-none" />
);
```

## Patterns

Read the reference for the pattern you are building:

| Building                                                                                                | Read                                                 |
| ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| Any spring, picking response and damping                                                                | [springs](references/springs.md)                     |
| Draggable or flickable element, snapping to corners or points, custom scroller with momentum and paging | [drag and momentum](references/drag-and-momentum.md) |
| Horizontal swipe inside a vertical list, swipe actions, pull to refresh                                 | [direction lock](references/direction-lock.md)       |
| Bottom sheet with detents                                                                               | [sheets](references/sheets.md)                       |
| Video or audio scrubber with fine scrubbing                                                             | [scrubbing](references/scrubbing.md)                 |
| Thumbnail that grows into a detail view and drags back down to close                                    | [morphing](references/morphing.md)                   |
| Edge swipe to go back in a navigation stack                                                             | [swipe back](references/swipe-back.md)               |
| One gesture with several outcomes or modes (home bar, fine scrubbing, stretching swipe actions)         | [gesture modes](references/gesture-modes.md)         |
| Reduced motion                                                                                          | [reduced motion](references/reduced-motion.md)       |
| A gesture that freezes, gets stuck, or breaks taps on touch                                             | [pointer events](references/pointer-events.md)       |

## Defaults that feel right

| Thing                                                 | Value                                               |
| ----------------------------------------------------- | --------------------------------------------------- |
| Most UI springs                                       | `springFromResponse(0.35–0.45, 0.85–0.9)`           |
| Navigation, paging, anything that shouldn't overshoot | damping ratio `1`                                   |
| Velocity window                                       | last 100ms                                          |
| Direction lock threshold                              | 10px                                                |
| Lock ratio for a strict axis                          | the winning axis is 2× the other                    |
| Rubber band constant                                  | `c = 0.55`, `d` = the container's size on that axis |
| Projection deceleration                               | `0.998` (normal), `0.99` (fast, stops sooner)       |
| Edge-swipe zone                                       | 24px from the edge                                  |
| Reduced-motion fade                                   | 200ms ease-out                                      |

Two choices have their own guidance, so don't guess them: how much a spring should bounce ([springs](references/springs.md#how-much-bounce)) and whether a scroller coasts normally, stops fast or pages ([drag and momentum](references/drag-and-momentum.md#normal-fast-or-paging)). When unsure, no bounce and normal deceleration.

## Checklist before calling it done

- [ ] Grab it mid-animation: it stops exactly where it is, no jump.
- [ ] Act again the moment an animation looks finished (open another row, tap the revealed page, swipe the other way): it responds straight away, no dead quarter-second.
- [ ] Flick it: it leaves at the finger's speed, no hitch on release.
- [ ] Drag past the edge: it resists and springs back.
- [ ] Drop something that can rest anywhere inside its bounds: it stays exactly there, no wobble.
- [ ] Drag in a direction that does nothing: it resists (not frozen, not free) and springs back.
- [ ] On a phone: drag slowly; it tracks the finger and doesn't scroll the page (`touch-action`).
- [ ] Taps on buttons and rows inside the draggable still work.
- [ ] Put a second finger down mid-drag: nothing breaks.
- [ ] Switch apps or open the context menu mid-drag: it settles, it doesn't stay stuck.
- [ ] Turn on reduced motion: no overshoot, big automatic movements fade, dragging is unchanged.
