---
name: rn-reanimated
description: >
  React Native Reanimated 4.x best practices, 60fps animation patterns, bug fixing, and code
  enhancement for Android and iOS. Use when writing, reviewing, fixing, or optimizing Reanimated
  animation code, gesture-driven interactions, worklets, layout animations, or shared element
  transitions. Triggers on tasks involving react-native-reanimated, useSharedValue, useAnimatedStyle,
  withSpring, withTiming, withDecay, Gesture.Pan, layout animations, worklet debugging, animation
  performance optimization, or troubleshooting janky animations. Also use when the user wants to
  fix animation bugs, enhance animation smoothness, review gesture code, or achieve 60fps on both
  Android and iOS. Also triggers when the user asks to review, audit, check, or upgrade their
  Reanimated code to best practices, or asks "is my animation code good", "check my reanimated
  code", "update to best practices", "review my animations", or similar requests.
---

# React Native Reanimated — Best Practices & 60fps Guide

> Reanimated 4.x / Worklets 0.7.x / React Native 0.80+ (New Architecture required)

## Critical Rules

1. **Babel plugin must be LAST** in `babel.config.js` plugins array.
2. **Never use React state (`useState`) for values that drive animations.** Use `useSharedValue`.
3. **Never call `withTiming`/`withSpring` inside gesture `.onUpdate` callbacks.** Assign the event value directly for smooth tracking; use spring/timing only in `.onEnd`.
4. **Always cancel animations before starting new ones** when gestures begin: `cancelAnimation(sv)`.
5. **Always pass `velocity`** from gesture events into `withSpring` for natural feel.
6. **Always wrap the app in `<GestureHandlerRootView style={{ flex: 1 }}>`.** Gestures won't work without it.
7. **Always cancel animations on unmount** via `useEffect` cleanup.
8. **Respect reduced motion** — use `ReduceMotion.System` or `useReducedMotion()`.

## Code Review & Upgrade Action

When the user asks to review, check, audit, or upgrade their Reanimated code, follow this procedure:

1. **Scan** all files containing Reanimated imports (`react-native-reanimated`, `react-native-gesture-handler`).
2. **Check each file** against every rule below and the Anti-Patterns table. For each violation found, collect: file path, line number, what's wrong, and the fix.
3. **Report** findings to the user in a clear table format:

```
| File | Line | Issue | Severity | Fix |
|------|------|-------|----------|-----|
| src/Card.tsx | 12 | useState driving animation | HIGH | Replace with useSharedValue |
| src/Sheet.tsx | 45 | Missing cancelAnimation in onBegin | HIGH | Add cancelAnimation(sv) |
| src/List.tsx | 78 | Math.random() as key | MEDIUM | Use stable unique ID |
```

4. **Severity levels**:
   - **CRITICAL**: Will crash or break animations (missing GestureHandlerRootView, hooks in worklets, Babel plugin order wrong)
   - **HIGH**: Causes jank/dropped frames (useState for animation, withSpring in onUpdate, missing cancelAnimation, missing velocity)
   - **MEDIUM**: Sub-optimal but works (no reduced motion support, no animation cleanup on unmount, shadow on Android)
   - **LOW**: Style/convention (missing spring presets, could use better easing)

5. **Ask the user**: "I found X issues in Y files. Want me to fix all of them automatically?" — then apply all fixes if confirmed.

6. **After fixing**, re-scan to confirm zero remaining violations and report:
   - Total issues found → fixed
   - Files modified
   - Expected performance improvement (e.g., "Removed 3 JS-thread bottlenecks — gestures should now track at 60fps")

### What to Check (scan checklist)

- [ ] `useState`/`setState` used for values that drive animations → replace with `useSharedValue`
- [ ] `withTiming`/`withSpring` called inside gesture `.onUpdate` → replace with direct assignment
- [ ] `.value` read directly in JSX render → wrap in `useAnimatedStyle`
- [ ] Animation created in render return → move to handler/effect
- [ ] Missing `cancelAnimation` in gesture `.onBegin` → add it
- [ ] Missing `velocity` in `withSpring` after gesture `.onEnd` → add `{ velocity: e.velocityX }`
- [ ] Shadow properties animated on Android → switch to `elevation`
- [ ] `Math.random()` used as list item key → use stable ID
- [ ] Large staggered delays on 100+ items → cap with `Math.min()`
- [ ] Missing `GestureHandlerRootView` wrapping the app
- [ ] Missing animation cleanup in `useEffect` return
- [ ] Missing mounted guard for `runOnJS` in `useAnimatedReaction`
- [ ] `'worklet'` directive missing in custom worklet functions
- [ ] React hooks used inside worklets
- [ ] async/await inside worklets
- [ ] Large objects/arrays captured in worklet closures
- [ ] Babel plugin not last in plugins array
- [ ] Animating `borderWidth`, `shadowOffset`, `shadowRadius` on Android
- [ ] Missing `overflow: 'hidden'` for `borderRadius` animation on Android
- [ ] No reduced motion handling (`ReduceMotion.System` or `useReducedMotion()`)
- [ ] `Animated.FlatList` missing `skipEnteringExitingAnimations` for initial render

## Installation

```bash
npm install react-native-reanimated react-native-worklets react-native-gesture-handler
```

```js
// babel.config.js
module.exports = {
  presets: ['module:metro-react-native-babel-preset'],
  plugins: ['react-native-reanimated/plugin'], // MUST be last
};
```

After install: clear Metro cache (`npx react-native start --reset-cache`), rebuild native (`pod install` / `gradlew clean`).

## Core Pattern — The Only Pattern You Need

```tsx
const offset = useSharedValue(0);

const animatedStyle = useAnimatedStyle(() => ({
  transform: [{ translateX: offset.value }],
}));

const animate = () => {
  offset.value = withSpring(100, { damping: 15, stiffness: 150 });
};

<Animated.View style={[styles.box, animatedStyle]} />;
```

## Animation Function Selection

| Context | Use | Why |
|---------|-----|-----|
| During gesture (finger down) | Direct assignment | Follows finger at 60fps |
| Gesture release | `withSpring` + velocity | Natural physics feel |
| Fixed-duration transition | `withTiming` (200-500ms) | Predictable timing |
| Momentum/fling | `withDecay` | Natural deceleration |
| Toggle state | `withSpring` | Bouncy feedback |

## Spring Presets

```ts
const SPRING = {
  gentle:  { damping: 15, stiffness: 50 },   // Slow, smooth
  normal:  { damping: 10, stiffness: 100 },  // Balanced
  snappy:  { damping: 20, stiffness: 300 },  // Quick, snappy
  noBounce:{ damping: 30, stiffness: 200 },  // Critically damped
};
```

## Gesture Pattern (Pan with Spring Back)

```tsx
const offsetX = useSharedValue(0);
const startX = useSharedValue(0);

const pan = Gesture.Pan()
  .onBegin(() => {
    cancelAnimation(offsetX);
    startX.value = offsetX.value;
  })
  .onUpdate((e) => {
    offsetX.value = startX.value + e.translationX; // Direct assignment
  })
  .onEnd((e) => {
    offsetX.value = withSpring(0, { velocity: e.velocityX, damping: 15 });
  });
```

## Performance Targets

- **Frame budget**: 16.67ms (60fps) / 8.33ms (120fps ProMotion)
- **JS thread**: < 8ms per frame
- **UI thread**: < 10ms per frame
- **Animated properties per component**: Keep to 2-4 max

## Anti-Patterns to Fix on Sight

| Anti-Pattern | Fix |
|---|---|
| `useState` driving animation values | Replace with `useSharedValue` |
| `withTiming(event.translationX)` in `.onUpdate` | Direct assign: `sv.value = event.translationX` |
| Reading `sv.value` in JSX render | Use `useAnimatedStyle` |
| Creating `withTiming()` in render return | Move to event handler / `useEffect` |
| Missing `cancelAnimation` on gesture begin | Add `cancelAnimation(sv)` in `.onBegin` |
| Missing velocity on spring after gesture | Add `{ velocity: event.velocityX }` |
| Shadow animation on Android | Use `elevation` instead |
| `Math.random()` as list item key | Use stable unique IDs |
| 100+ items with `FadeIn.delay(i * 10)` | Cap delay: `Math.min(i * 50, 1000)` |

## Platform-Specific Rules

### Android
- Use `elevation` instead of shadow properties for animated shadows.
- Use `overflow: 'hidden'` on parent for smooth `borderRadius` animation.
- Reduce animation complexity on low-end devices (skip rotation, limit properties).
- Avoid animating `borderWidth`, `shadowOffset`, `shadowRadius` — they jank on Android.

### iOS
- Shadow properties (`shadowOpacity`, `shadowRadius`, `shadowOffset`) are animatable.
- ProMotion displays support 120fps — use spring animations to benefit from variable refresh.
- Use `enableLayoutAnimations(true)` (enabled by default).

## Memory Management

```tsx
useEffect(() => {
  return () => {
    cancelAnimation(offset);
    cancelAnimation(scale);
  };
}, []);
```

For reactions that call `runOnJS`, guard with a mounted flag:

```tsx
const isMounted = useSharedValue(true);
useEffect(() => () => { isMounted.value = false; }, []);

useAnimatedReaction(
  () => progress.value,
  (val) => {
    if (val >= 1 && isMounted.value) runOnJS(onComplete)();
  }
);
```

## Worklet Rules

- `'worklet'` directive must be the **first statement** in the function body.
- Auto-workletized contexts (no manual directive needed): `useAnimatedStyle`, `useAnimatedProps`, `useDerivedValue`, `useAnimatedReaction`, `useAnimatedScrollHandler`, gesture callbacks.
- **Never** use React hooks, async/await, DOM APIs, or `localStorage` inside worklets.
- **Never** close over large arrays/objects — they get copied to the UI thread.
- Use `runOnJS(fn)(args)` to call JS from worklets; use `runOnUI(fn)(args)` to call worklets from JS.

## Layout Animations Quick Reference

```tsx
<Animated.View
  entering={FadeInUp.delay(index * 50).springify().damping(12)}
  exiting={FadeOut.duration(200)}
  layout={Layout.springify()}
/>
```

- Use staggered delays for lists: `delay(index * 50)`.
- Use stable unique keys — never `Math.random()`.
- Use `skipEnteringExitingAnimations` on `Animated.FlatList` for initial render.
- Handle reduced motion: `entering={reducedMotion ? undefined : FadeIn}`.

## Debugging Checklist

1. Babel plugin is last in plugins array
2. Metro cache cleared (`--reset-cache`)
3. Native code rebuilt (`pod install` / `gradlew clean`)
4. `'worklet'` directive present in custom worklet functions
5. Hooks only at component top level (never in worklets)
6. Shared values used for animation state
7. `GestureHandlerRootView` wraps the app
8. Animation functions assigned to `.value` (not called standalone)
9. Previous animations cancelled before new ones

## Reference Files

For detailed API docs, examples, and patterns, read these files as needed:

- **[Fundamentals & Getting Started](references/fundamentals.md)**: Installation, prerequisites, New Architecture setup, core concepts (Shared Values, Animated Styles, Animated Components), first animation walkthrough, architecture overview.
- **[Animation Functions](references/animation-functions.md)**: `withTiming`, `withSpring`, `withDecay`, modifiers (`withDelay`, `withRepeat`, `withSequence`, `withClamp`), easing functions, spring physics, callbacks.
- **[Hooks & Utilities](references/hooks-utilities.md)**: All hooks (`useSharedValue`, `useAnimatedStyle`, `useAnimatedProps`, `useDerivedValue`, `useAnimatedReaction`, `useAnimatedRef`, `useAnimatedScrollHandler`, `useScrollViewOffset`, `useAnimatedKeyboard`, `useAnimatedSensor`, `useFrameCallback`), utility functions (`runOnJS`, `runOnUI`, `cancelAnimation`, `interpolate`, `interpolateColor`, `clamp`).
- **[Worklets Deep Dive](references/worklets.md)**: Threading model, `'worklet'` directive rules, closure capture, custom runtimes, thread communication (`runOnUI`, `runOnJS`, `runOnUISync`), scheduling, debugging worklets.
- **[Layout Animations](references/layout-animations.md)**: Entering/exiting animations (Fade, Slide, Zoom, Bounce, Flip, Rotate, etc.), layout transitions, keyframe animations, list animations, shared element transitions.
- **[Gestures Integration](references/gestures.md)**: All gesture types (Tap, Pan, Pinch, Rotation, Fling, LongPress), gesture configuration, composition (`Simultaneous`, `Exclusive`, `Race`), common patterns (swipeable item, bottom sheet, pull-to-refresh, carousel, photo viewer).
- **[Best Practices & Performance](references/best-practices.md)**: 60fps performance principles, animation optimization patterns, anti-patterns to avoid, debugging strategies, platform-specific guidelines (Android/iOS), memory management, complex animation patterns.
- **[Troubleshooting](references/troubleshooting.md)**: Installation issues, build errors, runtime errors, animation issues, gesture issues, performance issues, platform-specific issues, error message reference.
