---
name: iphone-duo-readiness
description: Audit and port an iOS app to iPhone Duo, Apple's first foldable iPhone. Use when asked to support, adapt, prepare, test, or review an app for iPhone Duo, foldable iPhone, the inner/outer display, device poses, or the fold. Entry point that routes to the layout, bars, hinge/scenes, camera, and design skills.
---

# Get an iOS app ready for iPhone Duo

iPhone Duo is Apple's first foldable iPhone: a 5.4-inch outer display and a
7.6-inch inner display sharing one aspect ratio, joined by a hinge the user can
leave at any angle. An existing iPhone app runs on it unchanged — but it will
look like an app that has not been thought about.

This skill is the entry point. Work the checklist, then hand off to the
specialist skill for whatever the app actually does.

## The one idea to hold onto

**iPhone Duo is not a new idiom. It is a wider continuum of sizes.**

Every mistake in this port comes from an app asserting something fixed: this
idiom, this orientation, this screen, this width, this symmetric inset. Every
fix is the same shape — replace the assertion with a question about the space
actually available right now.

If you find yourself writing a branch that means "if iPhone Duo", stop. Write a
branch on size class or available space instead, and it will be right on iPad,
in Split View, under iPhone mirroring, and on whatever ships next.

## Step 1 — Establish the baseline

Find out what the app is building against, because the SDK is the gate:

| Built against | Behavior on iPhone Duo |
|---|---|
| Pre-iOS 27 | Runs. Closed, it uses the space to the left of the status bar and camera. Open, it gets a familiar size and aspect ratio. |
| iOS 27 SDK | Extends left of the status bar area on the inner display. |
| **iOS 27.1 SDK** | Content reaches the screen edge, standard bars lay out vertically, and the reserved-region and arrangement APIs become available. |

Check the deployment target and the SDK in the project, then say plainly which
tier the app is in. Getting to the 27.1 tier is the single highest-leverage
change; almost everything else in this skill assumes it.

Then open the app in the **iPhone Duo simulator in Device Hub** (Xcode 27.1) and
drive the controls that open, close, rotate and fold it. Also try **Split View**
by dragging the app to one side with the home indicator. Bugs here are visual
and pose-dependent — you will not find them by reading code alone.

Xcode 27.1 also ships an **App Resizability** skill (renamed from the app
modernization skill, now covering SwiftUI and iPhone Duo). Run it. It mechanizes
much of Step 2.

## Step 2 — Hunt the fixed assumptions

Grep the codebase for these. Each one is a real defect on this device:

**Idiom and orientation branches.** `userInterfaceIdiom`, `isPad`, any layout
decision keyed off `interfaceOrientation`. The inner display *does not honor
supported interface orientations* — it rotates regardless of what the app
declared. Replace with size classes.

**`UIScreen.main`.** Ambiguous on a two-display device and slated for
deprecation. Prefer no screen reference at all — use the environment, the trait
collection, or the scene's bounds. For scale, `traitCollection.displayScale`.
If you genuinely need the screen, reach it from the scene:
`window?.windowScene?.screen`.

**Symmetric inset math.** This is the subtle one. On iPhone Duo the safe area
and layout margins are routinely asymmetric — vertical controls sit on one side
only, and which side depends on the pose and on Split View placement. Any
arithmetic shaped like `bounds.width - safeAreaInsets.left * 2` is wrong.
Inset by the whole set instead and let each edge speak for itself.

**Hardcoded widths and breakpoints.** Fixed point values, device-width tables,
"if width > 390" style thresholds. Target the two size classes: **compact width
on the outer display, regular width on the inner display**.

**Hand-rolled bars.** A custom `UIToolbar`, `UINavigationBar` or `UITabBar` is
invisible to the system's vertical-bar layout. Its content will not participate.

## Step 3 — Adopt the standard containers

The cheapest path to a good port is letting system containers do the adapting.
These are already fully pose-aware:

- `NavigationSplitView` / `UISplitViewController` — columns collapse to a single
  stack when closed, and appear tiled or as overlays when open.
- `TabView` / `UITabBarController` — adapt across every pose, laying out
  vertically where appropriate. On the inner display you can opt into a richer
  sidebar by setting the tab bar's preferred placement to `.sidebar`.
- `NavigationStack`, `List`, `ScrollView` — adapt to reserved regions on their
  own.
- Sheets, alerts, menus, popovers and context menus — reposition themselves
  around the fold automatically.

System components carry **fold avoidance**: they nudge interactive elements out
of the curved region so buttons never land in the fold. You get that free by
using them, and you owe yourself an implementation of it if you don't.

## Step 4 — Get safe areas right

Four rules, in priority order:

1. Use container-provided bars for anything bar-shaped. They lay out *outside*
   the safe area and dodge the status bar, the Dynamic Island and the camera on
   their own. Horizontal bars contribute top/bottom insets; vertical bars
   contribute leading/trailing insets.
2. Keep interactive and legible foreground content **inside** the safe area.
   SwiftUI does this by default; in UIKit reference `safeAreaInsets` or
   constrain to the safe area layout guide.
3. Let backgrounds bleed **past** it — `.ignoresSafeArea()` in SwiftUI,
   `view.bounds` in UIKit — so artwork runs under bars and sidebars.
4. Handle every edge independently, and test in Split View on both sides.

For custom UI that needs to live outside the safe area without colliding with
system UI, iOS 27.1 adds `ReservedRegion` (SwiftUI) and `UIViewReservedRegion`
(UIKit). Reach for those rather than guessing at insets.

To match the screen's corner radius, use the iOS 26 concentricity APIs —
`ConcentricRectangle` in SwiftUI, `UICornerConfiguration` in UIKit — which were
updated for the shapes on this device.

## Step 5 — Route to the specialist

| If the app… | Use |
|---|---|
| has toolbars, tab bars, or overflow menus | `iphone-duo-vertical-bars` |
| has custom layout, split-like views, or content that lands in the fold | `iphone-duo-adaptive-layout` |
| wants hinge-driven effects, multiple windows, or dual-display UI | `iphone-duo-hinge-and-scenes` |
| captures photo or video | `iphone-duo-camera` |
| needs a design pass rather than a code pass | `iphone-duo-design-review` |

Device numbers live in `../../reference/device-facts.md`; every API name and its
framework is in `../../reference/api-index.md`.

## Reporting back

Give the user the tier they're on, the concrete defects found with
`file:line`, and what changes tier. Be honest about what needs a running
simulator to confirm — pose-dependent layout bugs are not statically decidable,
and claiming otherwise wastes their time.

## Accuracy note

These APIs were announced in September 2026 Tech Talks while Xcode 27.1 was
still rolling out. Treat the names in this repo as the shape of the API and
confirm exact signatures against the SDK headers before promising a build works.
