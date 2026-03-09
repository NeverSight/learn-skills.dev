---
name: optimising-expo-react-native-performance
description: Diagnose, improve, and prevent performance regressions in Expo-based React Native apps using release-build profiling, KPI budgets, and targeted fixes across startup, rendering, lists, images, memory, and networking.
version: 2.0.0
license: MIT
tags:
  - react-native
  - expo
  - performance
  - profiling
  - optimisation
  - hermes
  - metro
  - flashlist
  - reanimated
  - eas
---

## Summary

This skill turns “the app feels slow/janky” into a **measured**, **repeatable**, and **shippable** optimisation program for Expo-managed React Native apps.

Non‑negotiables:
- Optimise against **user-visible KPIs** (startup/TTI, scroll FPS, navigation responsiveness, memory growth, p95 network latency).
- Profile in **production-like builds** (release / profile / debugOptimized) — **not** in dev mode.
- Make **one change at a time**, re-measure, and keep a rollback path.

## When to use

Use when you need to:
- Fix **slow startup**, “white screen”, or delayed time-to-interactive.
- Fix **scroll jank**, dropped frames, sluggish taps, or slow transitions.
- Reduce **memory growth**, crashes under pressure, or image/video bloat.
- Reduce **OTA update size**, JS bundle size, or Android binary size.
- Add **regression prevention**: perf budgets + CI gates + production monitoring.

## When NOT to use

Don’t use this skill to:
- Prematurely micro-optimise already-smooth screens with no KPI regression.
- Make changes without a reproducible scenario and a baseline.
- “Optimise” by switching libraries blindly (measure first).

## Inputs

- Repo (Expo managed or CNG/prebuild), ideally with:
  - `package.json`
  - `app.json` / `app.config.*`
  - `metro.config.js` (if present)
  - `babel.config.*`
  - `eas.json` (if using EAS)
- A concrete report of the problem:
  - Device(s), OS versions, and which flow feels slow.
  - Steps to reproduce (or a screen name if using Expo Router).

If details are missing, infer as much as possible from the repo and propose a minimal repro script.

## Outputs

Deliver **both**:
1) **Perf audit report** (see template in `assets/templates/perf-audit-report-template.md`):
   - KPIs + budgets
   - Baseline measurements (device + build type)
   - Root cause hypothesis + evidence
   - Fix plan (ordered by ROI / risk)
   - Before/after measurements
2) **Code changes** (PR-ready) implementing the top fixes, plus:
   - Updated perf budgets (if needed)
   - CI gate(s) for bundle/update size at minimum

## Tooling assumptions

You can use:
- Expo CLI (`npx expo …`), EAS CLI (`eas …`) where available.
- React Native DevTools (Performance + Memory panels) for JS-level analysis.
- Native profilers (Android Studio, Xcode Instruments) for CPU/memory/UI tracing.

You should prefer:
- **Release/profile builds** for measurement.
- **Same device class** and **same scenario script** for before/after.

## The optimisation workflow (high level)

1) **Define KPIs + budgets** (3–6 metrics max). Pick what users feel.
2) **Create a repeatable scenario** (startup, list scroll, key navigation, etc.).
3) **Measure baseline in a production-like build**.
4) **Classify the bottleneck domain**:
   - Startup/bundle
   - JS thread
   - UI thread
   - Lists/images
   - Memory
   - Network/background
5) Apply **targeted fixes** (smallest change, highest ROI first).
6) **Re-measure**. Keep only changes with KPI wins.
7) Add **regression control** (budgets + CI gates + monitoring).

## Detailed playbook

### Phase 0 — Establish reality (no guesswork)

**0.1 Identify versions and architecture**
- Expo SDK version, React Native version, React version.
- New Architecture status (mandatory in newer SDKs).
- JS engine (Hermes/JSC/V8), OTA updates usage (`expo-updates`).
- Major perf-sensitive libs: navigation (Expo Router/React Navigation), lists (FlashList), animation (Reanimated), images (`expo-image`).

**0.2 Choose KPIs (pick 3–6)**
Suggested defaults:
- Cold start: **time-to-first-render** and/or **time-to-interactive**
- Scroll: dropped frames / FPS on the heaviest list
- Navigation: p95 screen transition time for a representative flow
- Memory: steady-state RSS after repeating a navigation loop 5–10×
- Network: p95 API latency on a key endpoint

Record budgets as numbers (not “fast”). See `references/00-principles-and-kpis.md`.

**0.3 Choose build type for measuring**
- Prefer store-equivalent **Release**.
- If you need debuggability, use Android “profileable” builds, iOS Instruments, or Expo’s `debugOptimized` where applicable.

### Phase 1 — Baseline measurement (release-build discipline)

**1.1 Baseline checklist (must pass)**
- Dev mode off.
- No remote JS debugging.
- Same device, same OS version, same network conditions.
- Warm vs cold start explicitly noted.

**1.2 Capture traces and numbers**
- React Native DevTools:
  - Performance trace (JS execution + React tracks + network events)
  - Heap snapshot (if memory suspected)
- Native tools:
  - Android Studio System Trace for jank attribution
  - Xcode Instruments (Time Profiler / Allocations / Leaks)

Store raw artefacts (trace files, screenshots) alongside your report.

### Phase 2 — Decide the bottleneck domain

Use this decision rubric:
- **Startup slow**: long splash, white screen, slow first render → startup/bundle.
- **Taps lag / transitions slow** but scrolling OK → JS thread or navigation.
- **Scroll stutters** even with little JS work → UI thread or list/render cost.
- **Memory climbs over time** → leak / image/video pressure.
- **Everything waits on API** → network/caching.

### Phase 3 — Apply high-ROI fixes by domain

#### A) Startup & bundle
Do in this order:
1) **Stop doing work before first paint**
   - Gate only critical assets (fonts, tiny config) and hide splash ASAP.
2) **Confirm Hermes**
   - Make it explicit in app config if necessary.
   - If you use OTA updates, ensure runtime compatibility when engine/bytecode changes.
3) **Shrink JS evaluation**
   - Prefer ESM imports, avoid breaking tree shaking.
   - Consider Metro `inlineRequires` (validate side effects!).
4) **Control OTA payloads**
   - Configure update asset inclusion/exclusion and verify assets.
5) **Android size knobs (measure trade-offs)**
   - Enable R8 minify + resource shrinking.
   - Treat bundle compression as a measured toggle (smaller APK vs slower startup).

See `references/02-startup-bundle-ota.md`.

#### B) JS thread stalls (renders + computation)
High ROI:
1) Remove production `console.*`.
2) Defer heavy work with `InteractionManager` / `requestAnimationFrame`.
3) Reduce re-renders:
   - Stabilise props, split context, memoise hot rows.
   - Consider **React Compiler** (branch rollout + profiling + easy rollback).

See `references/03-rendering-js-ui.md`.

#### C) UI thread / rendering / animations
High ROI:
1) Prefer native-driven transitions (native stack / `react-native-screens`).
2) Avoid expensive UI operations on animated frames:
   - Alpha compositing, heavy shadows, animating image size.
3) Use native-driver animations where possible; for complex gestures prefer Reanimated worklets.

See `references/03-rendering-js-ui.md`.

#### D) Lists, images, and media
High ROI:
1) Fix list fundamentals:
   - Stable keys, avoid re-render storms, tune render window.
   - Add `getItemLayout` when item heights are known.
2) If still janky: evaluate FlashList for large/complex feeds.
3) Move image-heavy UIs to `expo-image` with caching + placeholders.
4) For replay-heavy video: use `expo-video` caching with a storage policy.

See `references/04-lists-images-media.md`.

#### E) Memory leaks / pressure
High ROI:
1) Reproduce with a navigation stress loop.
2) Take JS heap snapshots (before/after) to spot retained graphs.
3) If JS heap stable but RSS grows: switch to native allocation tools.

See `references/01-profiling-toolchain.md`.

#### F) Network & background work
High ROI:
1) Prevent refetch storms: cache + dedupe + prefetch.
2) Use platform-appropriate background scheduling (best effort) for sync.

See `references/05-network-background.md`.

### Phase 4 — Regression control (the “next level”)

Minimum viable regression control:
- **Budget file** committed (bundle size + a few KPI thresholds).
- **CI gate** that fails on obvious regressions (bundle/update size growth).
- **Production monitoring** (crash + perf traces) with symbolication.

See `references/06-ci-regression.md`.

## Common pitfalls (things this skill forbids)

- Benchmarking in dev mode and trusting the results.
- Making 5 optimisations at once, then not knowing which mattered.
- “Fixing” a symptom (e.g. bigger splash delay) instead of root cause (slow JS eval).
- Turning on size flags (bundle compression, aggressive shrinking) without measuring startup and runtime.

## Fast checklist

- [ ] KPIs chosen (3–6) + budgets written down
- [ ] Baseline measured in production-like build
- [ ] Bottleneck domain identified with evidence
- [ ] One fix at a time + before/after numbers
- [ ] At least one regression gate added (bundle/update size)
- [ ] Monitoring configured (crash + perf)

## References

Start here:
- `references/00-principles-and-kpis.md`
- `references/01-profiling-toolchain.md`
- `references/02-startup-bundle-ota.md`
- `references/03-rendering-js-ui.md`
- `references/04-lists-images-media.md`
- `references/06-ci-regression.md`

External links: see `references/resources.md`.
