---
name: zereight-react-native-optimizer
description: React Native performance review checklist for code reviews. Use when reviewing RN code to detect rendering, animation, and native performance regressions. Complements zereight-review — run both together on RN PRs.
---

# zereight-react-native-optimizer

Focused on **performance correctness** during code review.
The goal is not to teach optimization — it is to catch regressions before they ship.

## When to use

Use alongside `zereight-review` when:
- Reviewing React Native or Expo PRs
- Auditing list, animation, or native module changes
- Checking screen transitions or gesture interactions

Not a replacement for `react-native-best-practices` or `vercel-react-native-skills` — those explain *how* to optimize. This skill detects *what went wrong* in a diff.

## Prerequisites

The following skills provide the full optimization context this skill references:
- `react-native-best-practices` (callstackincubator)
- `vercel-react-native-skills` (vercel-labs)
- `react-native-animations` (pluginagentmarketplace)
- `react-native-best-practices` (callstackincubator)
- `agent-device` (callstackincubator)

## Priority order

1. Animation on JS thread (causes visible jank — always 🟠 Major or higher)
2. List rendering with FlatList instead of FlashList for large datasets
3. Unnecessary re-renders in hot paths (list items, animated components)
4. Memory leaks (listeners, subscriptions not cleaned up)
5. Bridge overuse (synchronous calls, large payloads)
6. Bundle size regressions
7. Image loading / caching issues

## Rendering checks

Run on every component change. See `references/rendering.md` for detail.

| Pattern | Severity |
|---|---|
| FlatList used for list with 50+ items | 🛠️ 🟠 Major |
| `keyExtractor` returns index | ⚠️ 🟡 Minor |
| Inline function/object passed as prop to memoized child | 🛠️ 🟡 Minor |
| `React.memo` wrapping component that receives new object ref each render | ⚠️ 🟡 Minor |
| Context provider too high — causes full subtree re-render | ⚠️ 🟠 Major |
| `useSelector` selecting large slice of store | 🛠️ 🔵 Trivial |
| Missing `useCallback` on event handler passed to child | 🛠️ 🔵 Trivial |
| `StyleSheet` defined inside component body | 🛠️ 🟡 Minor |

## Animation checks

Run when animation, gesture, or transition code is changed. See `references/animation.md` for detail.

| Pattern | Severity |
|---|---|
| `Animated.Value` (legacy API) used instead of Reanimated shared value | 🛠️ 🟠 Major |
| Animation drives style via `setState` (runs on JS thread) | ⚠️ 🟠 Major |
| Worklet function accesses JS-side state directly (no `runOnJS`) | ⚠️ 🟠 Major |
| `useAnimatedStyle` depends on non-shared-value reactive data | ⚠️ 🟡 Minor |
| Touch handled with `TouchableOpacity` instead of `GestureDetector` in animated context | 🛠️ 🟡 Minor |
| `LayoutAnimation` used instead of Reanimated layout animations | 🛠️ 🔵 Trivial |
| Animation not cancelled on unmount | ⚠️ 🟡 Minor |

## Native / bridge checks

Run when native modules, images, or bundle changes are involved. See `references/native.md` for detail.

| Pattern | Severity |
|---|---|
| Event listener / subscription not removed in cleanup | ⚠️ 🟠 Major |
| `NativeModules` called synchronously in render path | ⚠️ 🟠 Major |
| Large object passed over bridge (>10KB) | ⚠️ 🟡 Minor |
| Image loaded without `resizeMode` or explicit `width`/`height` | 🛠️ 🟡 Minor |
| Image source is remote URL without caching strategy | 🛠️ 🟡 Minor |
| New dependency added without checking bundle size impact | ⚪ Info |
| `console.log` left in production code path | 🧹 🔵 Trivial |

## Findings format

Use the same format as `zereight-review`:

```
### [type] [severity] Title

**Condition:** <what triggers this>
**Impact:** <FPS drop / memory leak / jank / crash>
**Evidence:** `file:line` — short snippet
**Minimal fix:** <smallest safe change>
```

## Output template

When running as standalone review:

1. `Performance Summary` (2-3 lines: what changed, overall signal)
2. `⚠️ Performance Findings` (ordered 🟠→🟡→🔵)
3. `🎯 Verdict` (`No regressions` | `Minor regressions` | `Block — performance regression`)

When integrated with `zereight-review`, append findings to the existing `⚠️ Findings` section under a `--- Performance ---` subheader.

## Quick heuristics

- If it touches a list → check FlashList, keyExtractor, and item memoization
- If it touches animation → verify UI thread execution (Reanimated, not setState)
- If it mounts/unmounts → verify all listeners/subscriptions have cleanup
- If it adds a native module call → verify async, not in render, not in hot loop
- If it adds a new package → note bundle size concern as ⚪ Info
