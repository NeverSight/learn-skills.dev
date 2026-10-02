---
name: iphone-duo-capacitor
description: Adapt a Capacitor or Ionic app to iPhone Duo, Apple's first foldable iPhone — why the standard Device Posture and Viewport Segments CSS does not reach a web view, what CSS gives you today, and how to get fold state, hinge angle and bar placement from the native side. Use when a Capacitor, Ionic, Angular, React or Vue app needs foldable iPhone support.
---

# Capacitor on iPhone Duo

Start here, because it is the thing that will waste your afternoon otherwise:

> **WebKit 27.1 implements Device Posture and Viewport Segments, but both sit
> behind an experimental flag that only Safari can set.**

A Capacitor app runs in a `WKWebView` it does not control the flags of, so
`navigator.devicePosture`, the `device-posture` media query and the
`env(viewport-segment-*)` variables are all absent there, while the same page in
Safari on the same device can see them. Feature-detect rather than assume, and
plan for both to be missing.

So the web platform gives you no fold awareness on this device out of the box.
What it *does* give you is most of what matters. Work in two tiers.

## Tier 1 — works today, no native code

### Trust safe areas, and never assume symmetry

This is the one that produces real bugs. iOS moves its bars to **one side** of
the display, and that side depends on the pose and the reading direction.

The bar arrives as a genuine safe-area inset: measured on the 27.1 simulator it
is `env(safe-area-inset-right)` of **84px**, and it moves to
`env(safe-area-inset-top)` of **82px** if the app opts out of vertical bars,
live and without a reload. So most layouts need nothing more than honest
`env(safe-area-inset-*)` padding on all four edges.

Any expression of the form `width - env(safe-area-inset-left) * 2` is a defect
on this device.

### Resize correctly

The window changes size constantly: opening, closing, folding, rotating, Split
View. Read sizes when you need them rather than caching, and prefer container
queries and `%`/`fr` layout over stored pixel values. Anything measured in a
`useEffect` or `ngOnInit` and kept will be stale within seconds.

### Think in size classes, not device checks

iOS reasons about this device in size classes: the outer display is **compact
width**, the inner display is **regular width**. Branch on the size you were
given, never on a user-agent string or an orientation, since the inner display
does not honour supported orientations.

Measured on the simulator: inner display **951×669** in landscape, outer display
**466×678**.

### Move navigation to the side on the wide display

When iOS moves its own tab bars and toolbars to a vertical rail, an HTML tab bar
pinned to the bottom looks unconverted next to every native app. A side rail on
the inner display and a bottom bar on the outer one is the web analogue, and it
costs one breakpoint.

## Tier 2 — needs the native side

Everything genuinely iPhone Duo-specific is invisible to the web view until
something native hands it over.

| Native API (iOS 27.1) | Why you want it in the web view |
|---|---|
| `reservedRegions(kind:options:)` on `UIView` | Where the fold and the camera are, so layout can avoid them |
| `UIHingeInteraction` | Continuous hinge angle, for effects and posture |
| `verticalBarEdge` on the trait collection | Which edge iOS moved the bars to, so your own chrome matches |
| Size class from `traitCollection` | The signal iOS actually uses, rather than your breakpoint guess |

Two details worth knowing before you write any of this yourself. A flat phone's
fold region is reported **inactive**, so reading it needs
`options: .includeInactive` or you will conclude the device has no hinge. And
`UIHinge.status` updates lazily, so it disagrees with the angle mid-fold; treat
the angle as the truth when both are available.

### Use the existing bridge

[`@erkamyaman/capacitor-foldable`](https://github.com/erkamyaman/capacitor-foldable)
is an MIT plugin that already does this, and also fills in Device Posture and
Viewport Segments so the standard CSS works in an app today:

```bash
npm install @erkamyaman/capacitor-foldable
npx cap sync
```

```typescript
import { Foldable, installFoldablePolyfill } from '@erkamyaman/capacitor-foldable';

await installFoldablePolyfill();

const fold = await Foldable.getFoldState();
await Foldable.addListener('foldStateChange', (state) => layout(state));
```

The polyfill sets `--fold-left`, `--fold-width` and friends on `<html>`, so a
grid can put its gutter exactly on the crease rather than guessing. The same
build covers Android foldables through `androidx.window`.

Deeper material lives in
[iphone-duo-capacitor-skills](https://github.com/erkamyaman/iphone-duo-capacitor-skills):
the CSS patterns, the full API, Ionic specifics, and how to test on the
simulator and on an Android emulator.

### Ionic apps

Ionic's `ion-tabs` is HTML, so it stays at the bottom while native bars move.
Two routes: a stylesheet that turns the tab bar into a side pill on the edge iOS
chose, or [`@rdlabo/ionic-theme-ios27`](https://github.com/rdlabo-dev/ionic-theme-ios27),
which repositions existing `ion-buttons`, `ion-button`, `ion-back-button` and
`ion-tab-bar` controls and projects them into native UI. The theme takes device
state as input, so the two compose rather than compete.

## What to do, in order

1. Audit every safe-area expression for assumed symmetry. Most bugs die here.
2. Stop caching sizes, and branch on the size you were handed.
3. Give the wide display a real layout rather than a stretched phone one.
4. Add the plugin, and feature-detect the standard APIs so the same build still
   works in a browser that has them.
5. Only then reach for hinge angle effects, which are the smallest part of a
   good port.

Steps 1 to 3 need no native code and improve the app on tablets at the same
time. Step 4 is the only iPhone Duo-specific part, and it cannot be tested
without the Xcode 27.1 simulator.

For what the native APIs do and why, read `../iphone-duo-adaptive-layout/SKILL.md`
and `../iphone-duo-vertical-bars/SKILL.md` — the design reasoning transfers
directly even though the code does not.
