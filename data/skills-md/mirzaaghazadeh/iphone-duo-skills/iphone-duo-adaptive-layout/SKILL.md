---
name: iphone-duo-adaptive-layout
description: Build layouts that adapt to the iPhone Duo fold using reserved regions, division and occlusion regions, displacement patterns, and the split and overlay ArrangementView containers. Use when content or controls land in the fold, when building a split-like or overlay layout, or when custom manually-positioned UI must avoid the hinge or the under-display camera.
---

# Adaptive layouts around the fold

When iPhone Duo is partially folded the inner display curves through the middle.
Anything sitting in that curve gets harder to read and much harder to tap. The
same thing happens to a photo printed across the spine of a book: near the gutter
it stops reading as one continuous image.

So the fold is not decoration. It is a real constraint on where content can go —
and iOS models it as a **reserved region** you can query and design around.

## Reserved regions

Reserved regions are areas of the view that hardware imposes on your layout.
Treat them exactly like the window controls you already work around on iPadOS:
not obstacles, just facts about the available space.

Two kinds, and the distinction matters:

**Division regions** split one area into several smaller usable areas. The fold
is a division region. Content does not flow *through* it — it belongs on one
side or the other.

**Occlusion regions** cover part of an area without splitting it. Think of them
as frames sitting inside your bounds. The inner FaceTime camera is an occlusion
region.

Concretely, iPhone Duo has **three** reserved regions, and it's worth knowing
which is which because they behave differently:

| Region | Kind | When it's there |
|---|---|---|
| Outer front camera | occlusion | **Always.** Sits in the corner, aligned with the side controls, and expands into the Dynamic Island for Live Activities. |
| Inner front camera | occlusion | Only while that camera is active. It's under the display and invisible otherwise; when it activates, UI moves aside to reveal it. |
| The folding region | division | Only while the device is partially folded, dividing the inner display and excluding the curved centre. |

Regions are **active or inactive**:

- The fold's division region is active only while the device is actually folded.
  Flat, it is inactive and has zero width.
- The camera's occlusion region is active only while that camera is streaming.

Note the asymmetry between the two cameras: the outer one is a permanent fact of
your layout, while the inner one appears and disappears under you. Handle the
second as a change you animate through, not a constant you read once.

By default you get only the active ones. Pass the `includeInactive` option to
also see regions that exist but aren't currently in play — which is what you want
for stable, high-level decisions. A grid, for instance, can prefer an even column
count on any device that *has* a fold, so the layout doesn't reshuffle every time
the user bends the device.

### Querying them

In SwiftUI, get a `GeometryProxy` from `GeometryReader` or `onGeometryChange`,
then ask it for `reservedRegions(kind:)`, optionally with
`options: .includeInactive`. In UIKit the same method hangs off `UIView`. Either
way you read each region's `frame` and fold it into your own layout math.

Query reserved regions for **custom, manually laid out controls**. If you are
using system containers, you already have this handled — see below.

## Displacement: the design pattern

Most interfaces can simply flow around a reserved region. Some deserve a more
deliberate response, and the pattern for that is **displacement** — adjusting an
element's frame based on the available space so that important content stays
visible, reachable and unobstructed while the device is folded.

The typical case: an element sits centered while the device is open, and once
folded it moves into whichever region actually supports its purpose.

**Choose the right scope.** Displacement scales from a single button to an
entire container. If an element can stand on its own, move it alone. If elements
work as a unit, move them together — pulling a context menu away from the photo
it belongs to breaks the relationship even though both are technically visible.

**Don't move things far.** Distance weakens the visual link between an element
and its source. Aligning both around the fold usually beats banishing one to the
far region.

**Don't displace continuously scrolling content.** Articles, feeds, documents,
lists — these already adapt by scrolling. Relocating them between regions
interrupts continuity and gains nothing. Scrollable content is also exempt from
fold avoidance generally; it's fine for it to pass under the curve.

### Where things should move

Let purpose decide, and note that purpose changes with pose:

- **Folded like a book** — send transient things such as alerts to the trailing
  side, near where they will continue to appear as the device closes onto the
  outer display.
- **Propped on a table** — the top region is for content that reads at a
  distance; the bottom region is the stable surface, so tappable controls belong
  there.
- **When several regions would work** — pick the contextual one. A focused search
  field should stay over the view it is searching, adapting its width and
  position as the device folds, exactly as it stays over the keyboard on iPhone.

### How things should adapt once moved

Position and size are the usual changes, but not the only ones. A split view can
keep both columns visible by rebalancing to an even 50/50 split. A grid can hold
its outer margins and simply widen the gap at the hinge, keeping every cell
whole and inside one region.

The through-line: you are **moving, resizing and reorganizing what is already
there** — never removing it. Every piece of content, every function, every layout
stays reachable no matter how the device is being held.

## Containers that adapt for free

Before writing any of this yourself, check whether a system container already
does it:

- **Navigation** — `NavigationStack`, `NavigationSplitView`, `TabView`
- **Content** — `List`, `ScrollView`
- **Presentations** — action sheets, alerts, menus, popovers all reposition
  themselves around reserved regions automatically

## Arrangements

Between navigation containers and content containers sits a third kind:
a **layout container** that arranges exactly two views by rule. That's an
arrangement, new in iOS 27.1.

The rule is a function. Inputs: horizontal and vertical size class, the view's
width-over-height aspect ratio, and whether any division region is currently
active. Outputs: whether each view is shown at all, and what frame it gets.

### Building one

In SwiftUI, put an `ArrangementView` inside your `NavigationStack` and give it a
primary and a secondary view. In UIKit, use `UIArrangementViewController` as the
root of a `UINavigationController` and assign view controllers to the `.primary`
and `.secondary` placements.

### The split style

The default. It divides the bounds between the two views — horizontally when the
view is wider than tall, vertically when taller than wide.

Constrain it when only one axis makes sense: apply `.axes(.horizontal)` to the
split style (in UIKit, configure `UISplitArrangement` the same way and pass it to
`updateArrangement(_:)`). When a split arrangement can't split along the view's
primary axis, it shows a single view rather than producing a bad layout.

The payoff on this device: when the secondary view is dismissed, the primary
doesn't recenter across the whole display the way it would on iPad. It stays
inside the region the fold defines, so its controls stay reachable and clear of
the curve.

### The overlay style

Where split prefers side-by-side, overlay prefers stacking one view above the
other — and moves them side-by-side when the device folds, which is exactly when
the stacked view would otherwise get cramped.

Because the relationship changes with the pose, you often want to change the
subordinate view's presentation to match. Read the stacking state and adapt: in
SwiftUI, the `overlayArrangementZIndex` environment value; in UIKit, `state(for:)`
on the arrangement view controller and then its `zIndex`. A list that is
collapsed while stacked can expand once it's given its own region.

### Choosing between them

Follow the pattern the app already uses. Something built from `HStack`/`VStack`
maps to **split**; something built from `ZStack` maps to **overlay**. Both
translate directly and bring iPhone Duo support with them.

With no existing pattern to follow, ask what the relationship between the two
views is:

- **Foreground over background**, where partial obscuring is acceptable —
  **overlay**. Controls floating over readable content that scrolls beneath them
  is the canonical case.
- **Main and detail**, where neither may ever be obscured — **split**. A player
  and its transcript is the canonical case.

### When not to use one

- Arrangements provide no navigation infrastructure. Don't put a
  `NavigationSplitView` or similar inside one.
- Don't nest an arrangement inside `List` or `ScrollView`.
- If you need expanding and collapsing column behavior, you want a real split
  view, not an arrangement.

## A working order

1. Audit centered layouts. Would a two-column layout be better? If not, which
   displacement pattern applies?
2. Prefer system containers and presentations — most adaptation is free.
3. Where the app has a custom horizontal split or overlay, replace it with
   `ArrangementView`. You gain iPhone Duo behavior across every supported device,
   not just this one.
4. Only then, for the highest-priority manually positioned controls, adopt the
   reserved-region APIs and implement displacement by hand.

For hinge-driven *interaction* rather than layout, see
`../iphone-duo-hinge-and-scenes/SKILL.md` — live hinge angle is the wrong tool
for laying out views, and the right one for driving effects.
