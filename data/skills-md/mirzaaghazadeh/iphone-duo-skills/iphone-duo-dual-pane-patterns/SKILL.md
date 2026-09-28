---
name: iphone-duo-dual-pane-patterns
description: Design and build two-pane experiences for iPhone Duo — the real pixel and point dimensions of each display and each half, the exact hinge callback types (onHingeChange / UIHingeInteraction), hinge-driven effects, pose-to-pattern mapping (companion pane, dual view, list-detail, tabletop controls), two-pane paywalls and fold-aware onboarding. Use when sizing a layout or asset for iPhone Duo, wiring a hinge callback, choosing what goes in each pane, or designing onboarding and purchase flows that span the fold.
---

# Dual-pane patterns, dimensions and hinge callbacks

The sibling skills explain the platform: reserved regions and arrangements in
`../iphone-duo-adaptive-layout/SKILL.md`, the hinge and scenes in
`../iphone-duo-hinge-and-scenes/SKILL.md`, design principles in
`../iphone-duo-design-review/SKILL.md`. This one is the **applied** layer: the
numbers you'll want when mocking up or sizing assets, the exact shapes of the
hinge callbacks, and the proven patterns for what to put in each pane — drawn
from Apple's material plus a decade of dual-screen guidance from Microsoft
(Surface Duo), Google (Android foldables) and Samsung (Flex Mode), which all
converge on the same answers.

## The numbers

From Apple's published specs. Use them for mockups, asset budgets and sanity
checks — **never** as layout constants. Layout reads size class, safe area and
reserved regions at runtime.

| | Outer display | Inner display (open) | Each half of the inner display |
|---|---|---|---|
| Diagonal | 5.4 in | 7.6 in | — |
| Points (w × h, as held) | **466 × 678** portrait | **951 × 669** landscape | **475.5 × 669** portrait |
| Pixels (w × h, as held) | **1398 × 2034** portrait | **2670 × 1878** landscape | **≈1335 × 1878** portrait |
| Density | 460 ppi | 430 ppi | 430 ppi |
| Aspect ratio | ≈1.45 : 1 (tall) | ≈1.42 : 1 (wide) | ≈1.41 : 1 (tall) |
| Size class | compact × regular (portrait), compact × compact (landscape) | regular × regular, any orientation | — |

Apple lists the inner panel as "1878-by-2670"; open, the device is wider than
tall (164.6 × 117.8 mm), so the natural open posture is **landscape**.

Three consequences worth internalising:

1. **The inner display is the outer display turned sideways**, near enough. Both
   are ≈1.4–1.45 : 1, which is why Apple describes them as sharing one aspect
   ratio.
2. **Each half of the inner display is roughly one outer display.** A phone-shaped
   UI fits one half; the other half is *additional*. That is the whole design
   thesis: one familiar pane plus one extra pane, not one stretched phone UI.
3. **The fold runs down the middle of the long edge** when open, so default
   two-pane layouts are side by side, and tabletop layouts are top/bottom.

### Points

Apple's Tech Specs list pixels only. The point sizes come from the iPhone Duo
templates in Apple's **iOS and iPadOS 27 design resource** (as reproduced in
Noah Elhadedy's community *iPhone Duo Adaptive Design Starter Kit*, aligned to
Apple's templates on 23 September 2026):

- Outer: **466 × 678 pt** — exactly the 1398 × 2034 panel at 3×.
- Inner: **951 × 669 pt** (669 × 951 in portrait). That is **not** an exact 3×
  of the 2670 × 1878 panel: the system renders at 2853 × 2007 (the App Store
  Connect screenshot size) and downsamples, like iPhone 6 Plus did. Export
  inner-display assets at 3× of the point size, not from the panel pixels.
- The fold sits at **475.5 pt** from the edge — the centre of 951 — in both
  orientations.

Still confirm in the Xcode 27.1 simulator; read `GeometryProxy.size` or scene
bounds rather than hardcoding any of this.

## Layout tokens (pt)

For mockups and for sanity-checking what the system gives you at runtime. The
**Source** column matters: only *Apple* values come from Apple's design
resource; *kit* values are design choices from the community starter kit that
you're free to change.

**Safe areas** — asymmetric by design; never mirror one side onto the other.

| State | Top | Bottom | Leading | Trailing | Safe content size | Source |
|---|---|---|---|---|---|---|
| Outer portrait | 0 | 0 | 0 | **84** (vertical bar) | 382 × 678 | Apple |
| Outer landscape | 0 | 0 | 0 | **84**, on the camera edge | 594 × 466 | Apple |
| Inner landscape (flat or book) | 0 | 0 | 0 | **84** (vertical bar) | 867 × 669 | Apple |
| Inner portrait (flat or tabletop) | **84** (status + top bar) | **95** (tab bar) | 0 | 0 | 669 × 772 | Apple |

Horizontal bars return **only** on the inner display in portrait. Everywhere
else, navigation, toolbar and tab bar share one 84 pt vertical bar in the order
back → prominent action → toolbar groups → tab bar, top to bottom.

**Bars and controls**

| Element | Size | Source |
|---|---|---|
| Vertical bar width | 84 pt | Apple |
| Horizontal navigation bar / toolbar (inner portrait) | 48 pt tall | Apple |
| Horizontal tab bar (inner portrait) | 95 pt tall inset | Apple |
| Bar button / prominent bar button | 36 pt / 48 pt | Apple |
| Touch target | 44 × 44 pt default, 28 × 28 pt minimum | Apple HIG |

**Margins, gaps, fold**

| Token | Value | Source |
|---|---|---|
| Layout margin, both displays | 20 pt | Apple |
| Division region width when flat | 0 pt | Apple |
| Division region width when folded | not published — read `ReservedRegion.frame` | — |
| Fold avoidance band (mockups) | 27 pt, centred on 475.5 pt | kit |
| Gap between panes | 16 pt outer, 24 pt inner | kit |
| Max width for running text | 600 pt | kit |

**Columns** — Apple asks for an even count; the counts themselves are kit values.

| State | Columns | Gutter |
|---|---|---|
| Outer portrait | 4 | 16 |
| Outer landscape | 6 | 16 |
| Inner portrait | 6 | 24 |
| Inner landscape | 8 | 24 |
| Inner, book-folded | 4 + 4, meeting at the fold, none on it | 24 |

**Typical pane widths** inside the 867 pt inner-landscape safe area (kit):
list 300–320 + detail 546–566; sidebar 280; player/primary ≈462 (one half) +
context ≈404. Keep a pane's content close to its outer-display size rather than
stretching it.

### Physical

| | Open | Closed |
|---|---|---|
| Width × height | 164.6 × 117.8 mm | 84.1 × 117.8 mm |
| Thickness | 5.2 mm | 11.3 mm |
| Weight | 254 g | 254 g |

Biometrics are **Touch ID in the side button** — no Face ID. Any flow that says
"Face ID" or uses a face glyph needs to branch on `LAContext.biometryType`.
**No LiDAR** is listed: features built on RoomPlan or scene depth need a
fallback on this device.

## Hinge callbacks — exact shapes

All iOS 27.1 (beta at time of writing), verified against Apple's symbol docs.

### SwiftUI

```swift
nonisolated func onHingeChange(
    isEnabled: Bool = true,
    _ action: @escaping (DeviceHingeContext, DeviceHingeContext) -> Void
) -> some View
```

| Type | Member | Type of member | Notes |
|---|---|---|---|
| `DeviceHingeContext` | `hinge` | `DeviceHinge?` | `nil` → the device has no hinge |
| `DeviceHinge` | `angle` | `Angle` | use `.degrees` / `.radians` |
| `DeviceHinge` | `status` | `DeviceHinge.Status` | |
| `DeviceHinge.Status` | `.closed`, `.partiallyOpen`, `.fullyOpen` | **struct** with static members | Equatable, so `switch` works, but you need a `default` |

The closure receives `(old, new)`. Use `isEnabled:` to stop updates when an
effect is off-screen instead of ignoring them in the closure.

### UIKit

```swift
init(updateHandler: (UIHingeInteraction, UIHingeInteraction.Update) -> Void)
var isEnabled: Bool
```

| Type | Member | Type of member | Notes |
|---|---|---|---|
| `UIHingeInteraction.Update` | `hinge` | `UIHinge?` | `nil` when the view leaves a hierarchy that provides hinge updates |
| `UIHinge` | `angle` | `CGFloat` | **radians**, not degrees |
| `UIHinge` | `status` | `UIHinge.Status` | |
| `UIHinge.Status` | `.closed`, `.partiallyOpen`, `.fullyOpen`, **`.unknown`** | `enum` (`Int` raw value) | UIKit has a fourth case SwiftUI doesn't |

The UIKit handler is **not** an `(old, new)` pair. It fires when the hinge
changes *and* when the interaction moves between hierarchies. Keep your own
previous value if you need a delta.

### Rules Apple states in the reference

- **Status is decided by the system from angle *and* device orientation.** Don't
  re-derive it from angle thresholds — there is no documented "closed below N°".
- **Update rate and precision are system policy** and can change with system
  state. Don't assume a frequency; interpolate or animate towards the latest
  value rather than treating each callback as a frame.
- **If you only need closed / partial / open, use `status`, not `angle`.**
- The **angle range isn't documented.** Don't assume flat is exactly 180° — treat
  `.fullyOpen` as your upper bound and normalise against it.

### A reusable normaliser

```swift
/// 0 = closed, 1 = fully open. Effects read this; nothing lays out from it.
@Observable final class HingeProgress {
    var value: Double = 1          // no hinge → behave as if flat
    var isPartial = false
    private var maxSeen: Double = .pi

    func update(_ hinge: DeviceHinge?) {
        guard let hinge else { value = 1; isPartial = false; return }
        let radians = hinge.angle.radians
        switch hinge.status {
        case .closed:
            value = 0; isPartial = false
        case .fullyOpen:
            maxSeen = max(maxSeen, radians)
            value = 1; isPartial = false
        default: // .partiallyOpen
            value = min(max(radians / maxSeen, 0), 1); isPartial = true
        }
    }
}

// usage
.onHingeChange(isEnabled: effectVisible) { _, new in progress.update(new.hinge) }
```

The UIKit equivalent reads `update.hinge?.angle` (already radians) and must add a
`case .unknown:` that leaves the last value untouched.

## Pose → pattern

There is no "laptop" or "tent" status. Poses are what the user does; your code
sees **size class, reserved regions and hinge status**. Map them like this:

| Pose | What your code observes | Pattern |
|---|---|---|
| Closed | outer display, compact width | The phone app you already have. Secondary pane collapses to a sheet or a push. |
| Open flat | regular × regular, division region inactive (zero width) | Two panes side by side, media may cross the centre. |
| Book (partly folded, inner landscape) | division region **active and taller than wide** | Two panes, left/right. Nothing interactive in the curve. |
| Tabletop / laptop (partly folded, inner portrait) | division region **active and wider than tall** | Content in the raised half, controls in the flat half. |
| Tent | partially open, often flipped | Hands-free viewing; don't rely on touch. |

Detect orientation of the fold from the region, not the hinge:

```swift
GeometryReader { proxy in
    let fold = proxy.reservedRegions(kind: .division).first { $0.isActive }
    let isTabletop = fold.map { $0.frame.width > $0.frame.height } ?? false
    // …
}
```

Better still, let `ArrangementView` with `.split` choose the axis for you — it
splits horizontally when wider than tall and vertically when taller than wide,
which *is* the book-vs-tabletop decision.

### The five patterns that work

Microsoft's dual-screen taxonomy, reconciled with Apple's containers:

| Pattern | Left / top pane | Right / bottom pane | Apple container | Good for |
|---|---|---|---|---|
| **Companion pane** | Canvas (photo, room, document) | Tools, library, properties, prompt | `ArrangementView(.split)` | Editors, creative tools |
| **Dual view** | Version A (original) | Version B (result) | Two columns on regular width | Before/after, diffs, compare variants |
| **List-detail** | List | Detail, updates on tap | `NavigationSplitView` | Browsing catalogs, styles, messages |
| **Extended canvas** | One image spanning both panes | — | full-bleed + reserved regions for overlays | Maps, panoramas, video |
| **Tabletop controls** | Media, no buttons | Joystick, sliders, actions | `ArrangementView(.split)` / `.overlay` | Hands-free viewing, showroom, playback |

Pick by content relationship, not by pose: companion = one thing + its tools;
dual view = two versions of one thing; list-detail = many things + one.

### Six rules that come from all four vendors

1. **Mask media, split controls.** Photos and video may run across the fold.
   Buttons, text and inputs never sit on it. The only exception is a drag in
   progress — a dragged card may cross the fold while the finger is down.
2. **Don't stretch.** Each half is phone-shaped. Doubling font size or button
   width across 2670 px is the canonical failure. Use an even column count so
   nothing straddles the centre.
3. **Tabletop: content up, controls down.** The raised half is for looking, the
   flat half is for touching. Nothing interactive near the fold.
4. **Tools go right** (or bottom) of the canvas — thumb side for most users, and
   where iOS 27.1 already puts the vertical bar.
5. **Two screens = compare.** If the app has any before/after or variant choice,
   the fold is the natural divider; a single-screen slider is no longer needed.
6. **State survives the fold.** Opening and closing resizes the scene; it isn't
   torn down. Scroll position, in-progress text and the current step live in
   the model, not in view `@State` that a layout swap discards. Dialogs stay
   within one half.

## Hinge-driven effects

The hinge is for **effects and interactions**, never layout. Effects that earn
their place:

- **Hinge as a handle.** Map normalised progress to a reveal — a door swinging
  open onto a scene, a cover lifting, a camera pushing in. The user's hand *is*
  the animation. Keep it an overlay under a second long, never blocking input,
  and on `.fullyOpen` finish the transition and remove the overlay.
- **Close to save.** On `.closed`, persist and show a short confirmation on the
  outer display. Pairs naturally with the reveal running in reverse.
- **Parallax pitch.** Combine CoreMotion tilt (yaw/roll) with hinge progress
  (pitch) to move 2.5D layers — a depth map split into 3–4 layers is enough.
  Clamp amplitude to avoid motion sickness.
- **Continuous controls.** Anything a lever or whammy bar could drive.

Always:

- Guard `nil` hinge (most devices) and give those users the end state.
- Reset in the `else` branch when leaving `.partiallyOpen`, so effects don't
  stick at a stale angle.
- Honour **Reduce Motion** — swap the reveal for a crossfade.
- Pass `isEnabled: false` when the effect isn't on screen.

## Purchase and paywall screens

- **Sheets avoid the fold** on their own, so a sheet paywall lands in one half.
  To span both panes, present a **full-screen cover** with your own two-column
  layout: value proposition (ideally the user's *own* result, animated) in the
  left pane, plans and the purchase button entirely in the right pane.
- **Price, button and legal copy stay together in one pane.** Never split the
  price from the button across the fold, and never run the button through it.
- On the **outer display**, fall back to one column; `SubscriptionStoreView`
  handles trial badges and renewal wording for you there.
- App Review 3.1.2 still governs: the billed amount is the most prominent
  element, trial wording is secondary, the renewal period is explicit, restore
  purchases is reachable, and the close button is visible immediately.
- **Folding is not a dismissal.** Don't treat a close/open during a paywall as
  "user declined" for exit-offer logic; the scene was only resized.
- Tabletop-triggered paywalls should keep the tabletop shape: preview up top,
  plans on the flat half.

## Fold-aware onboarding

1. **Never require opening the device.** Invite it — "open to step inside" —
   and continue on the outer display after a few seconds if the user doesn't.
   People hold Duo closed a lot.
2. **Opening at any step expands that step** into two panes. It never restarts
   the flow. This is the state-survives-the-fold rule applied to onboarding.
3. Reach the "aha" before asking for permissions or money. Permission priming
   screens go directly before the system prompt, at the moment of need, with a
   "not now".
4. Ask for notifications *after* the paywall, attached to a concrete promise
   (for example, "we'll remind you before your trial ends").

## Test matrix

Run every two-pane screen through this in the Xcode 27.1 Device Hub simulator,
dragging the hinge slider slowly through each transition:

| | Closed | Book (slider mid-way) | Open flat | Tabletop | Split View, left | Split View, right |
|---|---|---|---|---|---|---|
| No letterboxing | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Nothing tappable in the fold | — | ☐ | — | ☐ | — | — |
| State kept across the transition | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Hinge effect resets / no-hinge path works | ☐ | ☐ | ☐ | ☐ | — | — |
| Paywall price + button in one pane | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

Also run once on a non-foldable simulator to exercise the `nil`-hinge path.
