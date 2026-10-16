---
name: swift-performance
description: Keep a macOS Swift app fast. Use when designing, writing or reviewing a SwiftUI or AppKit view, list, model or data flow that must scale, or when an app is slow, laggy, janky, hot or busy while idle.
---

# Swift performance

A cost is the work per run, times how often it runs. Build mode keeps costly work off hot paths while you write code. Diagnosis mode finds the work that got there, and its fix goes back through build mode.

Write your own fixtures, scenarios and counters for each app, since every app needs different ones.

## Build mode

Run all steps for a new feature. For a review, run steps 4 to 6 on the diff.

1. **Workload model.** Name each view's item count today, at ×10 and at ×100. The largest view is usually one that merges others.
2. **Hot path analysis.** Tag each computation by how often it runs: per frame, per input event, per action, per data change, or once.
3. **Performance budgets.** A frame has 8 ms of main-thread time at 120 Hz and 16 ms at 60 Hz. An action takes under 100 ms. An untouched window uses about 0% CPU.
   - Done when each hot path's cost at ×10 fits its budget, or is flagged.
4. **Work bounding.**
   - Draw growing collections lazily, with `LazyVStack`, `List` or `Table`. A `VStack` builds every item.
   - Run animations, symbol effects, `TimelineView`s, timers and polls only while visible and changing. A repeating effect keeps the window rendering every frame.
   - Keep a large subtree's `.id` stable, since a new one rebuilds the subtree.
5. **Reuse and invalidation.**
   - Compute derived collections when their source changes, and read the stored result in `body`.
   - Keep fast-changing state, such as hover and selection, in the smallest view that needs it. State at a list's root redraws every row.
   - Build per-item extras, such as tooltip text, only when shown.
   - Read item geometry on demand, or in a coordinate space that doesn't scroll.
6. **Concurrency and I/O.** Keep the main thread for drawing and input. In Swift 6.2 with approachable concurrency, mark CPU-heavy async functions `@concurrent`, since a plain `nonisolated async` function runs on its caller's actor.
7. **Measurement.** Measure each flagged path at each volume, before and after the change.

## Diagnosis mode

1. **Symptom.** Note what is slow, where, how slow, and at what volume.
2. **Reproduction.** Repeat it at the user's volume in a copy of the app with its own data, so the user's app and data stay unchanged.
3. **Measurement.** Measure idle, the slow interaction, and a fast comparison case, on the path the user takes.
   - Done when the slow and fast cases differ in a number.
4. **Isolation.** Switch parts off one at a time until the cost goes away. Do this whenever the profile shows only framework code, since profilers show where time goes but not why.
5. **Root cause.** Name the mechanism, its frequency, its file and line, and the build rule it breaks.
   - Done when removing it removes the cost.
6. **Verification.** Measure the fix beside an unchanged baseline.

Report a table of each scenario's main-thread share, worst stall and slowest action, then the root causes.

## Measuring you can trust

- Measure main-thread CPU share and stall length. Total CPU and frame rate hide where time goes.
- Count how often bodies and handlers run, since frequency explains most costs.
- Confirm the state while you measure: the window open, the data loaded, nothing else drawing on that main thread.
- Check that your tools don't cause the cost. Automation and screenshots can change what the app draws.
- Compare release builds with release builds, and repeat each case at least twice, changing one thing per run.

## Scripts

- `scripts/MainThreadMeter.swift`: main-thread CPU share and stalls, inside an app you can build. Its 8 ms ping wakes the main thread, so measure idle with `sample`.
- `scripts/sample-busy.py`: main-thread busy share from `sample <pid> <seconds> -mayDie -file <path>` output, for any running app. `--frames <binary>` lists that binary's heaviest frames.
