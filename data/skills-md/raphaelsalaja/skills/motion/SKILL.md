---
name: motion
description: Applies house motion for what animates, easing, durations, springs, gestures, exits and reduced motion.
---

# Motion

This skill holds how things move on every screen. It covers what animates, the curve and duration, gestures, exits and reduced motion.

## Durations and curves are exact

Use the project's motion tokens wherever they exist. Where none exists, the durations, curves and scales here are exact. Motion the user starts that runs past 300ms is a finding in any style.

Whether an animation should exist at all belongs to `restraint`. Taking an existing animation apart belongs to `deconstruct`. Whether it holds its frame rate belongs to `frames`. Surfaces, loading, hover styles and sound belong to `defaults`.

## App chrome fades

Page switches, panels and loading states fade with `opacity` and do not slide or scale. That is `motion-opacity-for-chrome`. Animate only the axis that changes. Animating width when only height changes is `motion-changing-axis-only`.

## Entrances do not replay

Switching pages does not replay entrances. Set `initial={false}` on the route-level `AnimatePresence`, and on any that wraps a state swap. That is `motion-no-replay-on-entry`. A cached view renders at once, with no fade or skeleton flash. That is `motion-no-flash-on-return`. See [recipes.md](recipes.md#route-transitions).

## Name the properties you animate

A transition lists the properties it animates, usually `opacity` and `transform`. `transition: all` is `motion-name-the-properties`.

## Toggled state transitions, keyframes run once

Interactive state changes use transitions or springs, which retarget when the user reverses. A keyframe animation on a toggled class is `motion-transitions-for-state`. Keep keyframes for sequences that run once.

## Motion starts where it comes from

A dropdown or popover scales from its trigger, with `transform-origin` set to that edge. A menu growing from its own centre is `motion-origin-from-trigger`. Modals stay centred, because no trigger anchors them.

## Nothing grows from zero

An entrance starts from `scale(0.95)` or higher, together with `opacity: 0`. `scale(0)` is `motion-no-scale-from-zero`.

## Gestures use springs

Drag, swipe and any motion the user can reverse mid-flight use a spring. On release, pass the pointer velocity into it. A drag release on a fixed `ease-out` is `motion-spring-for-gestures`. See [recipes.md](recipes.md#drag-release).

## Flicks dismiss, edges resist

A swipe dismisses on distance or on speed, so past about `0.11` px per millisecond a short flick is enough. A sheet that ignores a fast flick is `motion-flick-dismisses`.

Dragging past a boundary meets growing friction rather than a wall. A drawer that stops dead at the top is `motion-friction-at-edges`. Capture the pointer once a drag starts and ignore extra touches. See [recipes.md](recipes.md#flick-to-dismiss).

## Every gesture has a button

Each drag, swipe or pinch also works with a click and with the keyboard. A list that reorders only by dragging is `motion-gesture-alternative`.

## Easing fits the change

System changes such as a toast use easing, not a spring. Entrances and exits ease out, and a change of view eases in and out. Linear is for progress bars and clocks only. A modal entering on `ease-in` is `motion-ease-by-direction`.

The built-in `ease-out` keyword is too weak. Use `cubic-bezier(0.23, 1, 0.32, 1)` to enter and exit, and `cubic-bezier(0.77, 0, 0.175, 1)` for movement on screen. A bare `ease-out` is `motion-strong-ease-out`.

## Closes are faster than opens

A close runs shorter than its open. Nothing delays a close or a hover-out. A modal that takes as long to leave as it took to arrive is `motion-close-faster`.

## Motion stays under 300ms

Hover colour changes are instant, with no transition. A button fading its background over 200ms on hover is `motion-instant-hover-color`.

Press and hover movement take 120–180ms. Small state changes take 180–260ms. Nothing the user starts runs longer than 300ms, except a full panel or drawer at up to 400ms. A 500ms dropdown is `motion-under-300ms`.

Under `mode="wait"` the exit and the entrance play in series, so halve each. When motion feels slow, shorten it before changing the curve. Samples are in [recipes.md](recipes.md#curves-and-durations).

## Frequent actions do not animate

Typing, keyboard shortcuts, keyboard navigation and fast toggles do not animate. A command palette opened from the keyboard appears at once. A context menu appears at once and may fade out. A scale pulse on every keystroke is `motion-no-motion-on-repeat`.

## Tooltips wait once

The first tooltip in a group opens after a delay. Its neighbours open at once and without animation while one is showing, and every tooltip closes instantly. A toolbar where each tooltip waits the full delay is `motion-tooltip-delay`.

## Icons cross-fade when they swap

An icon that swaps in place, such as copy to copied, cross-fades. Scale runs `0.25` to `1`, opacity `0` to `1` and blur `4px` to `0`. A hard swap is `motion-icon-crossfade`. See [recipes.md](recipes.md#icon-swap).

## Blur bridges a cross-fade

When a cross-fade between two states still reads as two objects, add `filter: blur(2px)` while it runs. Keep blur under 20px, which gets expensive in Safari. Two labels visibly overlapping mid-swap is `motion-blur-the-crossfade`.

## Presses scale lightly

A pressed control scales to `0.98`, and squash or stretch stays within `0.95–1.05`. `whileTap={{ scale: 0.8 }}` is `motion-press-scale`. List items stagger by less than 50ms each. `staggerChildren: 0.15` on a list is `motion-short-stagger`. A staged entrance that plays once, such as a title, text and actions, staggers by 100ms. Routine interactions never stagger, and a stagger never blocks input.

## Exits need a presence boundary

A conditional element with an `exit` sits inside `AnimatePresence`, keyed by a stable id, and exits to its `initial` values. An exit that never plays because the wrapper is missing is `motion-exit-in-presence`. See [recipes.md](recipes.md#exits).

A dialog from a component library stays mounted and toggles its `open` prop. A dialog rendered behind `open &&`, which loses its close animation, is `motion-dialogs-stay-mounted`.

## Size follows content from a second element

To animate a container's width or height, measure an inner element with a `ResizeObserver` and animate the outer one. Measuring and animating the same node is `motion-measure-inner`. See [recipes.md](recipes.md#container-bounds).

While a panel collapses, its content keeps its open width, so nothing reflows mid-animation. Sidebar content set to `w-full` as the sidebar closes is `motion-hold-content-size`.

## Reduced motion removes movement

When `prefers-reduced-motion: reduce` matches, slides, scales and blurs become an opacity cross-fade. A sliding drawer that ignores the setting is `motion-reduced-motion`.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `motion-opacity-for-chrome` | `initial={{ x: 20, scale: 0.95 }}` on a page | `initial={{ opacity: 0 }}` |
| `motion-changing-axis-only` | `animate={{ width, height }}` when only height changes | `animate={{ height }}` |
| `motion-no-replay-on-entry` | `<AnimatePresence>` around routes, entrances replay | `<AnimatePresence initial={false}>` |
| `motion-no-flash-on-return` | A skeleton flash on a cached view | The cached view rendered at once |
| `motion-name-the-properties` | `transition: all 200ms` | `transition: opacity 200ms, transform 200ms` |
| `motion-transitions-for-state` | `.open { animation: slide-in 200ms }` | `transition: transform 200ms` on the toggled property |
| `motion-origin-from-trigger` | A dropdown scaling from `center` | `transform-origin: top left` under a left-aligned trigger |
| `motion-no-scale-from-zero` | `initial={{ scale: 0 }}` on a popover | `initial={{ scale: 0.95, opacity: 0 }}` |
| `motion-spring-for-gestures` | A drag release on `duration: 0.3, ease: "easeOut"` | `type: "spring"` with `velocity: info.velocity.x` |
| `motion-flick-dismisses` | Dismiss only past a fixed distance | Dismiss past the distance or above `0.11` px per ms |
| `motion-friction-at-edges` | A drawer that stops dead at its top | Movement damped the further it is dragged |
| `motion-gesture-alternative` | Rows that reorder only by drag | `Move Up` and `Move Down` in the row menu |
| `motion-ease-by-direction` | A modal entering on `ease-in` | Ease-out in and out, the exit shorter |
| `motion-strong-ease-out` | `transition: transform 200ms ease-out` | `transition: transform 200ms cubic-bezier(0.23, 1, 0.32, 1)` |
| `motion-close-faster` | A modal at `200ms` in and `200ms` out | `200ms` in, `150ms` out |
| `motion-instant-hover-color` | `transition: background-color 200ms` on a button | The hover colour applied at once |
| `motion-under-300ms` | `transition={{ duration: 0.5 }}` on a dropdown | `duration: 0.2` |
| `motion-no-motion-on-repeat` | `animate={{ scale: [1, 1.02, 1] }}` on each keystroke | No motion on the input |
| `motion-tooltip-delay` | Each toolbar tooltip waiting the full delay | The first waits, its neighbours open at once |
| `motion-icon-crossfade` | `{copied ? <CheckIcon /> : <CopyIcon />}` | Both icons cross-fading with scale and blur |
| `motion-blur-the-crossfade` | Two button labels overlapping mid-swap | `filter: blur(2px)` while the swap runs |
| `motion-press-scale` | `whileTap={{ scale: 0.8 }}` | `whileTap={{ scale: 0.98 }}` |
| `motion-short-stagger` | `staggerChildren: 0.15` | `staggerChildren: 0.03` |
| `motion-exit-in-presence` | `{open && <motion.div exit={{ opacity: 0 }} />}` | The same element inside `<AnimatePresence>` |
| `motion-dialogs-stay-mounted` | `{open && <Dialog.Root open>}` | `<Dialog.Root open={open} onOpenChange={setOpen}>` |
| `motion-measure-inner` | `ref` and `animate={{ height: bounds.height }}` on one node | The outer node animates, the inner node holds the `ref` |
| `motion-hold-content-size` | `w-full` content inside a collapsing sidebar | `w-64` content that keeps its width |
| `motion-reduced-motion` | A drawer that slides under reduced motion | An opacity cross-fade |

## Reporting

**Severity.** `HIGH` breaks use or access. That is an exit that never plays, a container that measures itself or a gesture with no button.

`MEDIUM` is a sliding page, a replayed entrance, a gesture on a fixed curve or motion over 300ms. It is also motion on typing, a wrong curve, `transition: all`, keyframes on toggled state or ignored reduced motion. It is also a conditionally rendered dialog, content reflowing as it collapses, a `scale(0)` entrance or a sheet that ignores a flick.

`LOW` is a faded hover colour, a heavy press scale or a long stagger. It is also motion from the wrong origin, a close as slow as its open, a slow tooltip or a hard icon swap. It is also a bare `ease-out`, an unblurred cross-fade or a drawer with no edge friction.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong
```

Then a `Rule | Count | Severity` summary. `Block` when any `HIGH` remains, `Approve` otherwise. Never `Approve` a file you did not read. Play the motion when a check depends on timing, and mark every check you could not run as `Not verified`.
