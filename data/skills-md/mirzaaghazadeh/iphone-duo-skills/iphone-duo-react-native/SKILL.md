---
name: iphone-duo-react-native
description: Adapt a React Native or Expo app to iPhone Duo, Apple's first foldable iPhone — asymmetric safe area insets, resize handling, and how to expose the iOS 27.1 reserved-region and hinge APIs through a native module. Use when a React Native, Expo or JS-based iOS app needs foldable iPhone support.
---

# React Native on iPhone Duo

React Native has **no fold or hinge API**. There is no `useDisplayFeatures`, no
hinge event, nothing that tells JavaScript the device is folded. As of this
writing no React Native or Expo release has shipped iPhone Duo support.

The good news is that the two things that break most often — resizing and safe
areas — are already solvable with libraries you probably have installed. Work in
two tiers.

## Tier 1 — works today, no native code

### Safe area insets, handled per edge

This is where React Native apps break on iPhone Duo, and it is worth being blunt
about why: **the safe area is asymmetric here.** iOS moves its controls to one
side of the display, so `left` and `right` insets differ — and which side depends
on the pose and on which half of a Split View your app occupies.

Use `useSafeAreaInsets()` from
[`react-native-safe-area-context`](https://github.com/AppAndFlow/react-native-safe-area-context).
It returns `{ top, right, bottom, left }` as independent numbers, and it updates
when the insets change.

```js
const insets = useSafeAreaInsets();
// each edge, independently
paddingLeft: insets.left,
paddingRight: insets.right,
```

Three things to avoid:

- **`SafeAreaView` from `react-native` core** — deprecated, and it only ever
  handled the notch case properly. Use the context library's hook or its
  `SafeAreaView`.
- **Symmetric math** — anything shaped like `width - insets.left * 2` is wrong
  the moment the insets differ, which on this device is most of the time.
- **Reading insets once** — they change while the app is running, so read them
  through the hook on every render rather than caching.

If you're on React Native 0.81+ with edge-to-edge enabled, your content already
extends under the system UI, which makes correct inset handling load-bearing
rather than cosmetic.

### Resize on every render

The window changes size constantly on iPhone Duo: opening, closing, folding,
rotating, entering Split View.

Use `useWindowDimensions()`. It is a hook, so it re-renders on change — unlike
`Dimensions.get('window')`, which returns a snapshot that silently goes stale.
If you have `Dimensions.get(...)` at module scope or in a constant, that is a
bug on this device.

For component-level sizing, `onLayout` gives you the actual measured box, which
is more reliable than deriving from window dimensions.

### Branch on width, not on device

iOS thinks in size classes: the outer display is **compact width**, the inner is
**regular width**. React Native has no equivalent, so use width breakpoints from
`useWindowDimensions()`.

Do not branch on `Platform.OS`, a device model from `react-native-device-info`,
or orientation. The inner display does not honor supported orientations, so
orientation tells you less than you think.

### Give the inner display a real layout

A phone layout stretched to 7.6 inches looks unfinished. The cheap win is a
two-column or master-detail layout above your wide breakpoint — and if you use
React Navigation, a drawer or rail-style navigator on wide and tabs on narrow.

## Tier 2 — needs a native module

Anything genuinely iPhone Duo-specific requires bridging from Swift. Worth it in
this order:

| Native API (iOS 27.1) | Why expose it to JS |
|---|---|
| `reservedRegions(kind:)` on `UIView` | Keep touch targets out of the fold and clear of the under-display camera |
| `UIHingeInteraction` | Continuous hinge angle, for effects |
| `traitCollection` size class | The signal iOS actually uses, instead of your breakpoint guess |

### Shape of the module

Write a **TurboModule** (New Architecture) or a legacy native module, with a
`NativeEventEmitter` for anything continuous. The hinge angle is a live stream —
push it as events; do not let JS poll it.

Query the reserved regions from the view your React content is mounted in, since
those APIs hang off `UIView` and regions are reported relative to a view. Emit
regions as plain objects (`{ x, y, width, height, kind, active }`) so JS can lay
out against them directly.

Guard hard. The same JS bundle runs on every iPhone, so the module must return
"no regions, no hinge" on non-folding devices and on anything below iOS 27.1
rather than throwing. Availability-check in Swift; never assume.

If you are in **Expo**, this means a config plugin plus a local native module —
it will not work in Expo Go, so you need a development build.

### Then feed it into Tier 1

Once regions reach JS, they are just numbers in your existing layout. An absolute
`View` positioned around a division region keeps a control out of the fold; a
`marginRight` derived from an occlusion region keeps content off the camera.

## What to do, in order

1. Swap any `Dimensions.get()` for `useWindowDimensions()`.
2. Swap core `SafeAreaView` for `useSafeAreaInsets()`, and audit every inset
   expression for symmetric math.
3. Replace platform/orientation branching with width breakpoints.
4. Add a wide-layout path so the inner display earns its size.
5. Only then write the native module, and only if fold awareness genuinely
   improves the app.

Steps 1–4 are plain React Native work that pays off on tablets and foldable
Android too. Step 5 is the only iPhone Duo-specific part, and it needs the
Xcode 27.1 simulator to test.

The reasoning behind the native APIs is in
`../iphone-duo-adaptive-layout/SKILL.md` and `../iphone-duo-readiness/SKILL.md`.
The design guidance in `../iphone-duo-design-review/SKILL.md` is framework-neutral
and applies to a React Native app unchanged.
