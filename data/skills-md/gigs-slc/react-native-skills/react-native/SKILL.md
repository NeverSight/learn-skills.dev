---
name: react-native
description: Complete React Native and Expo optimization guide combining Callstack profiling with Vercel code patterns. Covers FPS, TTI, bundle size, memory, lists, animations, state, UI, and React Compiler. Use for any React Native performance, debugging, or best practices task.
license: MIT
metadata:
  author: Callstack + Vercel
  version: '1.0.0'
  tags: react-native, expo, performance, optimization, patterns
---

# React Native Complete Guide

The ultimate React Native optimization guide combining:
- **Callstack** - Profiling, measurement, and native optimization (27 references)
- **Vercel** - Code patterns, UI, and best practices (36 rules)

## When to Apply

Reference these guidelines when:
- Debugging slow/janky UI or animations
- Optimizing list and scroll performance
- Investigating memory leaks (JS or native)
- Optimizing app startup time (TTI)
- Reducing bundle or app size
- Implementing animations with Reanimated
- Building UI with native components
- Working with React Compiler
- Structuring monorepo projects

## Priority-Ordered Guidelines

| Priority | Category | Impact | Source |
|----------|----------|--------|--------|
| 1 | Core Rendering | CRITICAL | Vercel |
| 2 | List Performance | CRITICAL | Both |
| 3 | FPS & Re-renders | CRITICAL | Callstack |
| 4 | Bundle Size | CRITICAL | Callstack |
| 5 | Animation | HIGH | Both |
| 6 | Navigation | HIGH | Vercel |
| 7 | TTI Optimization | HIGH | Callstack |
| 8 | UI Patterns | HIGH | Vercel |
| 9 | Native Performance | HIGH | Callstack |
| 10 | State Management | MEDIUM | Vercel |
| 11 | React Compiler | MEDIUM | Both |
| 12 | Memory Management | MEDIUM | Callstack |
| 13 | Monorepo | MEDIUM | Vercel |

---

## Quick Reference: Code Patterns (Vercel)

### Core Rendering (CRITICAL)
- `rendering-no-falsy-and` - Never use && with falsy values (crashes app)
- `rendering-text-in-text-component` - Wrap strings in Text components

### List Performance (CRITICAL)
- `list-performance-virtualize` - Use FlashList/LegendList for any list
- `list-performance-item-memo` - Memoize list item components
- `list-performance-callbacks` - Stabilize callback references
- `list-performance-inline-objects` - Avoid inline style objects
- `list-performance-function-references` - Extract functions outside render
- `list-performance-images` - Use compressed, appropriately-sized images
- `list-performance-item-expensive` - Move expensive work outside items
- `list-performance-item-types` - Use item types for heterogeneous lists

### Animation (HIGH)
- `animation-gpu-properties` - Animate only transform and opacity
- `animation-derived-value` - Use useDerivedValue for computed animations
- `animation-gesture-detector-press` - Use Gesture.Tap for press animations

### Navigation (HIGH)
- `navigation-native-navigators` - Use native stack/tabs over JS navigators

### UI Patterns (HIGH)
- `ui-expo-image` - Use expo-image for all images
- `ui-image-gallery` - Use Galeria for lightboxes
- `ui-pressable` - Use Pressable over TouchableOpacity
- `ui-safe-area-scroll` - Use contentInsetAdjustmentBehavior
- `ui-scrollview-content-inset` - Use contentInset for dynamic spacing
- `ui-menus` - Use native context menus (zeego)
- `ui-native-modals` - Use native modals over JS bottom sheets
- `ui-measure-views` - Use onLayout, not measure()
- `ui-styling` - Use StyleSheet.create, gap, borderCurve

### State Management (MEDIUM)
- `react-state-minimize` - Derive values, minimize state
- `react-state-dispatcher` - Use dispatch updaters
- `react-state-fallback` - Use fallback pattern for reactive defaults
- `state-ground-truth` - State represents truth, derive visuals

### React Compiler (MEDIUM)
- `react-compiler-destructure-functions` - Destructure functions early
- `react-compiler-reanimated-shared-values` - Use .get()/.set() not .value

### Monorepo (MEDIUM)
- `monorepo-native-deps-in-app` - Install native deps in app package
- `monorepo-single-dependency-versions` - Single versions across packages

### Configuration (LOW)
- `fonts-config-plugin` - Load fonts at build time
- `imports-design-system-folder` - Re-export from design system
- `js-hoist-intl` - Hoist Intl formatter creation

---

## Quick Reference: Profiling & Measurement (Callstack)

### FPS & Re-renders (CRITICAL)
```bash
# Open React Native DevTools
# Press 'j' in Metro, or shake device → "Open DevTools"
```
- `js-profile-react.md` - React DevTools profiling
- `js-measure-fps.md` - FPS monitoring
- `js-react-compiler.md` - Automatic memoization
- `js-atomic-state.md` - Jotai/Zustand patterns
- `js-concurrent-react.md` - useDeferredValue, useTransition

### Bundle Size (CRITICAL)
```bash
npx react-native bundle \
  --entry-file index.js \
  --bundle-output output.js \
  --platform ios \
  --sourcemap-output output.js.map \
  --dev false --minify true

npx source-map-explorer output.js --no-border-checks
```
- `bundle-barrel-exports.md` - Avoid barrel imports
- `bundle-analyze-js.md` - JS bundle visualization
- `bundle-tree-shaking.md` - Dead code elimination
- `bundle-r8-android.md` - Android code shrinking
- `bundle-hermes-mmap.md` - Disable bundle compression

### TTI Optimization (HIGH)
- `native-measure-tti.md` - TTI measurement setup
- `bundle-hermes-mmap.md` - Enable Hermes mmap
- Defer non-critical work with `InteractionManager`

### Native Performance (HIGH)
- iOS: Xcode Instruments → Time Profiler
- Android: Android Studio → CPU Profiler
- `native-turbo-modules.md` - Building fast native modules
- `native-threading-model.md` - Turbo Module threads
- `native-profiling.md` - Platform profiling guides

### Memory Management (MEDIUM)
- `js-memory-leaks.md` - JS memory leak hunting
- `native-memory-leaks.md` - Native memory leaks
- `native-memory-patterns.md` - C++/Swift/Kotlin memory

### Animations (MEDIUM)
- `js-animations-reanimated.md` - Reanimated worklets

---

## Problem → Solution Mapping

| Problem | Vercel Rules | Callstack References |
|---------|--------------|---------------------|
| App crashes | `rendering-no-falsy-and`, `rendering-text-in-text-component` | - |
| List scroll jank | `list-performance-*` | `js-lists-flatlist-flashlist.md` |
| Animation drops frames | `animation-gpu-properties` | `js-animations-reanimated.md` |
| Too many re-renders | `react-state-minimize` | `js-profile-react.md`, `js-react-compiler.md` |
| Slow startup (TTI) | - | `native-measure-tti.md`, `bundle-hermes-mmap.md` |
| Large app size | - | `bundle-analyze-app.md`, `bundle-r8-android.md` |
| Memory growing | - | `js-memory-leaks.md`, `native-memory-leaks.md` |
| TextInput lag | - | `js-uncontrolled-components.md` |
| Native module slow | - | `native-turbo-modules.md` |

---

## File Structure

```
react-native/
├── SKILL.md          # This file
├── AGENTS.md         # Full 74KB compiled Vercel guide
├── rules/            # 36 individual Vercel rule files
│   ├── list-performance-*.md
│   ├── animation-*.md
│   ├── ui-*.md
│   └── ...
└── references/       # 27 Callstack reference files
    ├── js-*.md
    ├── native-*.md
    ├── bundle-*.md
    └── images/
```

## Attribution

Combined from:
- "The Ultimate Guide to React Native Optimization" by Callstack
- React Native Skills by Vercel
