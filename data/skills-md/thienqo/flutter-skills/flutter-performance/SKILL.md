---
name: flutter-performance
description: Profile and improve Flutter runtime performance using profile-mode evidence, DevTools, frame analysis, rebuild inspection, memory, and app-size tools. Use for jank, slow startup, excessive work, leaks, or size regressions; route production logs, errors, and traces to flutter-observability.
---

# Flutter Performance

Measure a reproducible flow before changing code. Debug-mode timing is not release-performance evidence. A cause or fix named in the request is a hypothesis: confirm it with a measurement first.

## Establish evidence

Record the target device, Flutter version, build mode, flow, dataset, and metric. Reproduce in profile mode on representative hardware when the issue is user-facing.

## Diagnose by symptom

- Frame jank: inspect UI/raster timing, expensive build/layout/paint, shader or image work.
- Excess rebuilds: inspect state subscription scope and widget identity before adding `const` mechanically.
- Slow startup: trace initialization and defer work not required for first useful frame.
- Memory growth: compare repeated-flow snapshots and find retained ownership, listeners, controllers, or caches.
- Large binaries: use Flutter's app-size analysis and compare like-for-like release artifacts.
- CPU-heavy Dart: use timeline/CPU profiling and consider isolates only after locating the work.

Prefer removing or moving work over caching everything. Bound caches and preserve correctness.

Load [profile and frame analysis](references/profile-and-frame-analysis.md) for frame, CPU, image, rebuild, or web-rendering investigations. Load [memory, startup, and size](references/memory-startup-and-size.md) for retention, first-useful-frame, or artifact-size work.

## Verification

Repeat the same scenario after the change and report before/after evidence with variance. Run correctness tests because performance changes often alter lifecycle or caching behavior.

## Sources

- [Flutter performance](https://docs.flutter.dev/perf)
- [DevTools performance view](https://docs.flutter.dev/tools/devtools/performance)
