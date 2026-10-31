---
name: frames
description: Records a performance trace of one interaction on a throttled CPU, names what drops frames or delays input, then proves the fix with a second trace.
disable-model-invocation: true
---

# Frames

This skill measures whether an interaction stays smooth. It records the interaction on a throttled CPU, traces each slow frame to its cause and proves the fix with a second recording.

## A trace, never a feeling

The budgets are exact. Every frame lands within one refresh interval, 16.7ms at 60Hz, and no animation frame runs past 50ms while something moves. Every interaction paints its response within 200ms. "Feels smooth" with no numbers is a finding.

What a motion's values should be belongs to `motion`. Taking a motion apart frame by frame belongs to `deconstruct`. Opening the running result belongs to `verify`.

## 1. Name the interaction

Write the route, the steps and the moment that matters, such as "open the command palette and type three letters". Throttle the CPU 4× through the browser's emulation call, which stands in for a mid-range phone. A trace on an unthrottled laptop is `frames-throttle-the-cpu`.

## 2. Record it

Run [observe.js](observe.js) through the browser's evaluate call. Call `window.__frames.start()`, perform the interaction three times, then call `window.__frames.stop()`. When a long frame has no named script, record a full performance profile too. Reporting smoothness without a recording is `frames-trace-not-feel`.

## 3. Read the budget

Compare the recording against the budgets. Dropped frames or a long animation frame while something moves is `frames-hold-the-budget`. An interaction whose `duration` passes 200ms is `frames-answer-in-200ms`. Name whether the time went to input delay, processing or presentation.

## 4. Find the cause

Read each long frame's scripts and their forced layout time, then the code they point to.

A layout property animated across a large subtree reflows every frame. `top` or `width` animated on a full-page panel is `frames-compositor-properties`. Move it to `transform` and `opacity`.

Reading layout after writing a style forces the browser to lay out mid-frame. `offsetHeight` read inside a loop that sets `style.height` is `frames-no-forced-layout`. Read every value first, then write.

A state update on every frame re-renders the component tree each frame. `setState` inside a `requestAnimationFrame` loop or a scroll handler is `frames-animate-outside-render`. Drive the value through a motion value, a CSS variable or a ref.

A large surface repainted each frame costs more than the motion is worth. `backdrop-filter` on a full-screen layer that moves is `frames-small-paint`. Shrink the painted area or fade a static copy.

## 5. Trace the fix

Record again with the same steps and the same throttle. Report both recordings side by side. "Should be faster now" is `frames-before-and-after`. Clear the CPU throttle when done.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `frames-throttle-the-cpu` | Traced on an unthrottled laptop | Traced at 4× CPU throttle |
| `frames-trace-not-feel` | "The drawer feels smooth" | "Drawer open: 0 dropped frames, worst gap 17ms at 4×" |
| `frames-hold-the-budget` | 14 dropped frames while the sheet opens | 0 dropped, no animation frame over 50ms |
| `frames-answer-in-200ms` | A keystroke painting after 340ms, 280ms of it processing | 90ms, with the filter moved off the keystroke |
| `frames-compositor-properties` | `animate={{ width: 320 }}` on the full-page sidebar | `animate={{ x: 0 }}` with the width fixed |
| `frames-no-forced-layout` | `el.style.height = el.scrollHeight + "px"` in a loop over rows | All heights read first, then all written |
| `frames-animate-outside-render` | `setProgress(p)` on every frame | `progress.set(p)` on a motion value |
| `frames-small-paint` | `backdrop-filter: blur(20px)` on a moving full-screen layer | Blur on the static backdrop, the panel moving above it |
| `frames-before-and-after` | "Should be faster now" | Before 14 dropped, after 0, same steps at 4× |

## Reporting

**Severity.** `HIGH` is an interaction over 200ms at the throttle, or a report of smoothness with no recording. `MEDIUM` is dropped frames during motion, a layout property animated on a large subtree, forced layout or a state update per frame. It is also a trace taken without a throttle. `LOW` is a large repaint that still holds the budget, or a fix reported without a second recording.

**Format.** One finding per root cause, with the measured numbers:

```
1. file:line - [rule-id] what is wrong (dropped, worst gap, duration)
```

Then a `Rule | Count | Severity` summary. `Block` when any `HIGH` remains, `Approve` otherwise. Mark a browser without long animation frame support as `Not verified` for script attribution.
