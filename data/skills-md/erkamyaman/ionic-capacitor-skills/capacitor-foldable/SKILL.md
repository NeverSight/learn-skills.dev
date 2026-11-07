---
name: capacitor-foldable
description: Build Capacitor apps that adapt to foldable devices, iPhone Duo and Android foldables, with @erkamyaman/capacitor-foldable. Trigger when laying out around the crease or fold, reading the hinge angle or posture, using window size classes, polyfilling the Device Posture and Viewport Segments APIs, telling the outer display from the inner one, using rear display or dual screen on an Android foldable, moving an Ionic tab bar where iPhone Duo puts native bars, or testing on the iPhone Duo simulator or a foldable emulator.
license: MIT
metadata:
  author: erkamyaman
  version: '0.1'
  status: beta
  checked: 2026-09, against Xcode 27.1, Capacitor 8.5, Play target API 36
---

# Capacitor Foldable

Guidance for [`@erkamyaman/capacitor-foldable`](https://github.com/erkamyaman/capacitor-foldable), which reports the fold to a Capacitor web view: where the crease is, the hinge angle, the posture, and which display the app is on.

This skill is new. Everything in it was checked against the plugin source and measured on the iPhone Duo simulator, but it has not been through much real use yet, so [report anything that misleads you](https://github.com/erkamyaman/capacitor-foldable/issues).

## Install

```bash
npm install @erkamyaman/capacitor-foldable
npx cap sync
```

Capacitor 8 uses the current major. **If you are on Capacitor 7 and building with Xcode 27, upgrade to 8.5 or later before anything else**: those apps crash at launch, because iOS 27 needs the scene lifecycle that only 8.5 adopted, and a crash on launch is an automatic App Review rejection. Capacitor 7 apps can install `@erkamyaman/capacitor-foldable@7` and build with Xcode 26, which reports the fold on Android and size classes everywhere but has no iPhone Duo support. That route closes when Apple requires the iOS 27 SDK in April 2027. The 7.x line also predates the `--fold-*` variables (8.1.0) and the Ionic tab stylesheets, so the CSS below needs Capacitor 8.

## Start here: CSS before JavaScript

Install the polyfill once at startup, then lay out with CSS. Most foldable work needs no JavaScript at all.

```typescript
import { Foldable, installFoldablePolyfill } from '@erkamyaman/capacitor-foldable';

await installFoldablePolyfill();
```

Whenever the device reports a fold, that sets `--fold-left`, `--fold-top`, `--fold-width`, `--fold-height` and `--fold-margin-*` on `<html>`, and adds `fold-vertical` or `fold-horizontal`. It also sets the `vertical-bars-*` classes the Ionic stylesheet needs, and fills in the standard Viewport Segments and Device Posture APIs. Android's WebView turns both off, and Safari 27.1 has them behind an off-by-default flag that only Safari can set, so a Capacitor web view gets neither. The polyfill stands aside if it ever finds them already there.

Prefer the `--fold-*` variables over the polyfilled segment variables for layout: the segments only split when the fold actually separates the window, which on iPhone Duo means half open, while the fold variables are there when it is open flat too.

```css
.fold-vertical .reader { position: fixed; inset: 0; }

.fold-vertical .reader .page {
  position: absolute;
  top: 0;
  bottom: 0;
  padding: 14px;
  box-sizing: border-box;
}

.fold-vertical .reader .page:first-child { left: 0; width: var(--fold-left); }
.fold-vertical .reader .page:last-child { left: calc(var(--fold-left) + var(--fold-width)); right: 0; }
```

On a phone with no fold there are no `--fold-*` variables and no `fold-*` class, so write the flat layout first and let these rules refine it. The install is also a no-op off native, so nothing appears in a desktop browser: iterate in the simulator or on a device.

Handle both orientations. On iPhone Duo the crease is vertical in landscape and horizontal in portrait, so a layout that only styles `.fold-vertical` flattens when the phone is turned.

Reach for the plugin's methods when CSS cannot answer the question: the hinge angle, the posture, which display you are on, or where the system put its bars.

## When to consult these references

- **Laying out around the crease** (variables, classes, worked layouts): [css-layout.md](references/css-layout.md)
- **The API** (methods, events, and what is platform specific): [api.md](references/api.md)
- **Ionic apps** (`ion-tabs` on the side, the keyboard event a fold fires, Angular's CSS rule): [ionic.md](references/ionic.md)
- **iPhone Duo specifics** (reserved regions, vertical bars, safe areas, what the hinge status gets wrong): [iphone-duo.md](references/iphone-duo.md)
- **Android foldables** (postures, rear display, dual screen): [android.md](references/android.md)
- **Testing** (iPhone Duo simulator, foldable emulator, driving the hinge from the terminal): [testing.md](references/testing.md)

## Hard rules

- ✅ **Split on `var(--fold-left)`, never on 50%.** The variables give the band's leading edge, not its centre, and the coordinates are measured against the web view, so any inset moves them off the viewport midpoint. On iPhone Duo the fold is a 40 point band, so a halfway split also lands inside the part the system wants kept clear.
- ✅ **Treat `--fold-width` as the keep-clear band.** The margins are *inside* it, so `--fold-margin-*` tells you how much of the band is margin rather than physical crease. Do not add them on top of it. They are iOS only and read `0px` on Android, where a seamless fold also reports zero width, so keep your own minimum clearance: `max(12px, var(--fold-width, 0px))`, with the fallback because the variable does not exist at all on a phone with no fold.
- ✅ **Expect the fold when the device is fully open, not just half.** The position is reported flat as well as folded, so a layout can line up with the crease before anyone bends anything. A *closed* device reports `state: 'flat'` and no `hingeBounds`, because the plugin drops the fold below 20 degrees.
- ✅ **Let the layout expand; do not design a screen per pose.** Apple: "Don't reinvent your app when it resizes; allow the existing layout to expand based on the available space instead", and "Avoid extreme layout changes as people fold the device." Google's equivalent is to adapt to window size classes rather than device type, and to consider whether controls and text should avoid the hinge space.
- ❌ **Do not use `setVerticalBarBehavior({ behavior: 'disabled' })` to avoid adapting.** Apple's HIG asks you not to override bar placement. UIKit's own reference gives the exception: disable it only for interfaces better served by horizontal bars, "such as a fullscreen video player with toolbar controls or a non-scrolling layout like a calculator". It returns the bars to horizontal; it does not hand you the full display.
- ❌ **Do not poll `getFoldState()` on a timer** when `foldStateChange` will tell you. The exception is the moment the app moves between displays, where iOS pauses the web view: see [iphone-duo.md](references/iphone-duo.md).
- ❌ **Do not confuse "this device folds" with "there is a fold on this screen".** `isDeviceFoldable()` answers the first, though it can answer `false` on an Android foldable that advertises no tabletop posture and no hinge sensor. The presence of `hingeBounds`, or `--fold-left` in CSS, answers the second, and is what layout should key on. For the *outer screen*, neither is the gate: use `getDisplayModes()` and `displayModeChange`, since rear display and dual screen are Android only and read `unsupported` on iPhone Duo even though it folds. Every *read* method answers safely on any device; `startRearDisplay()` and `startDualScreen()` reject when the mode is unavailable.

## Before reporting done

```bash
npm run build      # or the app's build
npx cap sync
```

Then run it open flat, half open and closed, and fold it shut and open again, which suspends and resumes the web view on iOS. Do one pass at the largest system text size and one with VoiceOver or TalkBack on, since a layout that splits at the crease is exactly where reading order and target sizes go wrong. On iPhone Duo the posture picks the display, so that covers both screens; on Android the outer display needs rear display mode. [testing.md](references/testing.md) has the commands.
