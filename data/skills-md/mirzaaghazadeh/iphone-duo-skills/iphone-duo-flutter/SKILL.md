---
name: iphone-duo-flutter
description: Adapt a Flutter app to iPhone Duo, Apple's first foldable iPhone — what MediaQuery gives you today, why displayFeatures does not work here, and how to bridge the iOS 27.1 reserved-region, hinge and arrangement APIs through platform channels. Use when a Flutter or Dart app needs foldable iPhone support.
---

# Flutter on iPhone Duo

Start here, because it is the thing that will waste your afternoon otherwise:

> **`MediaQuery.displayFeatures` is documented as "populated only on Android."**

Flutter's foldable abstraction was built for Android hinges. On iPhone Duo it
returns an **empty list**, no matter how folded the device is. The same goes for
the `dual_screen` package (`TwoPane`, `hingeAngleEvents`) — Android-only in
practice, and last published around three years ago.

So Flutter gives you no fold awareness on this device out of the box. What it
*does* give you is most of what actually matters. Work in two tiers.

## Tier 1 — works today, no native code

This is the bulk of a good port, and it is all pure Dart.

### Resize correctly

iPhone Duo changes your app's size constantly: opening, closing, folding,
rotating, and entering Split View. Flutter handles the mechanics, but only if
your layout is driven by constraints rather than constants.

- Use `LayoutBuilder` and its `BoxConstraints` for layout decisions.
- Use `MediaQuery.sizeOf(context)` when you need the window, not
  `MediaQuery.of(context)` — the `sizeOf`/`paddingOf` accessors rebuild only on
  the property you read, which matters when the size changes this often.
- Never cache a size in `initState` or a field. It will be stale within seconds.

### Handle asymmetric safe areas

This is the one that produces real bugs. On iPhone Duo the system puts its
controls **on one side**, so insets are routinely asymmetric — and which side
depends on the pose and on which half of a Split View you occupy.

`MediaQuery.paddingOf(context)` returns `EdgeInsets` with independent `left`,
`top`, `right`, `bottom`. Use each one. Any expression of the form
`width - padding.left * 2` is a defect on this device.

The `SafeArea` widget handles all four edges independently already, so prefer it
over hand-rolled padding. Where you need artwork to bleed underneath, put the
background outside the `SafeArea` and only the interactive foreground inside it.

### Replace breakpoints with size-class thinking

iOS reasons about this device in size classes: the outer display is **compact
width**, the inner display is **regular width**. Flutter has no size classes, so
map to width breakpoints — the Material 3 window size classes are a reasonable
proxy (compact `< 600`, medium `600–840`, expanded `≥ 840` logical pixels).

Two rules:

- Branch on the **constraints you were handed**, not on `Platform.isIOS`, a
  device model string, or `MediaQuery.orientationOf`. The inner display does not
  honor supported orientations, so orientation is not a reliable signal.
- Pick breakpoints from where *your content* stops working, then sanity-check
  that a compact/regular split falls out of it.

### Prefer adaptive containers

`NavigationRail` for wide layouts and `NavigationBar` for narrow ones is the
Flutter analogue of what iOS does natively when it moves controls to the side.
A rail on the inner display and a bar on the outer display will feel close to
right, and costs one breakpoint.

## Tier 2 — needs a platform channel

Everything genuinely iPhone Duo-specific is unavailable to Dart until you bridge
it. As of this writing no Flutter release has shipped iPhone Duo support, so
plan on writing this yourself, and check whether it has landed before you do.

What is worth bridging, in priority order:

| Native API (iOS 27.1) | Why you'd want it in Dart |
|---|---|
| `reservedRegions(kind:)` on `UIView` | Keep controls out of the fold and out of the under-display camera |
| `UIHingeInteraction` | Continuous hinge angle for effects |
| Size class from `traitCollection` | The real signal iOS uses, rather than your breakpoint guess |

### How to shape the bridge

Use a **`MethodChannel`** for one-shot queries (current reserved regions, current
size class) and an **`EventChannel`** for anything continuous — the hinge angle
is a live stream and will spam a `MethodChannel`.

On the iOS side, in the `Runner` target, register a `FlutterMethodChannel` and a
`FlutterEventChannel` on the `FlutterViewController`, then read the native APIs
from that view. The reserved-region APIs hang off `UIView`, and the
`FlutterViewController`'s view is the right one to query — that is the view your
Dart layout actually occupies.

Serialize regions as plain maps (`{left, top, width, height, kind, active}`) so
Dart gets something it can rebuild `Rect`s from. Send the region list on change
rather than polling.

Guard everything: the hinge is `nil` on every non-folding device, and these APIs
do not exist below iOS 27.1. Your bridge must degrade to "no regions, no hinge"
rather than throw, because the same Flutter binary runs on every iPhone.

### Then use it like Tier 1

Once regions arrive in Dart, feed them into the same constraint-driven layout you
already built. A division region (the fold) tells you where to *not* put
interactive widgets; an occlusion region (the camera) tells you what to avoid
covering. `Stack` with `Positioned`, or a custom `MultiChildLayoutDelegate`, is
usually the cleanest way to displace a specific control around a region.

## What to do, in order

1. Make the app resize cleanly under `LayoutBuilder`. Most bugs die here.
2. Audit every use of `MediaQuery.padding` for symmetric-inset math.
3. Replace orientation and platform checks with constraint-based branching.
4. Add a rail/bar split so the inner display isn't just a stretched phone layout.
5. Only then, if the app genuinely needs fold awareness, write the channel.

Steps 1–4 get a Flutter app most of the way to feeling right on iPhone Duo, and
they improve it on tablets and desktop at the same time. Step 5 is the only part
that is iPhone Duo-specific, and it is the only part that can't be tested without
the Xcode 27.1 simulator.

For what the native APIs actually do and why, read
`../iphone-duo-adaptive-layout/SKILL.md` and
`../iphone-duo-readiness/SKILL.md` — the design reasoning transfers directly even
though the code doesn't.
