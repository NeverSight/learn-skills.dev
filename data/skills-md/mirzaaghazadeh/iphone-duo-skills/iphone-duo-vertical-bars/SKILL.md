---
name: iphone-duo-vertical-bars
description: Adapt toolbars, navigation bars and tab bars for the vertical axis on iPhone Duo — item ordering, symbol vs text representations, AxisBehavior, overflow menus, visibility priority, and when to opt out. Use when toolbar items look wrong, overflow too early, or need to move to the side on the outer display.
---

# Bars on the vertical axis

iPhone Duo's displays are wider and shorter than a traditional iPhone's. Vertical
space is the scarce resource, so the system moves controls that normally sit at
the top and bottom over to the **side**, where they also land closer to the
thumb. The content area to their left stays uninterrupted and comparable to a
conventional iPhone screen.

Same components, different axis. The position stays consistent as the user opens
the device to the inner display in landscape. **The one pose that keeps
horizontal bars is the inner display in portrait**, where there is plenty of
vertical room for content.

## Opting in

Two requirements, both mandatory:

**1. Rebuild against the latest SDK.** Without this the bars stay horizontal.

**2. Use bars that come from navigation containers.** In SwiftUI, pair the
`toolbar` modifier with `NavigationStack` or `NavigationSplitView`. In UIKit,
prefer `UINavigationController` and `UITabBarController`, which manage their own
bars — set toolbar items on a view controller and put it in a navigation
controller.

If you build a bar by hand out of `UIToolbar`, `UINavigationBar` or `UITabBar`,
its content is **not considered** for vertical layout. This is the single most
common reason an app's bars stay stubbornly horizontal.

## How items are placed

Navigation, toolbar and tab bar controls all coexist in one shared vertical
region. Picture the horizontal bar rotated 90° into a vertical stack — depending
on the screen it may hold toolbar items, tab items, or both.

Two structural exceptions:

- **Split views** — only the detail column participates. Items in other columns
  stay horizontal.
- **Inspectors** — no vertical bar of their own when expanded, since the detail
  column already has one and two would be confusing.

**Sheets** vary by display. On the outer display a sheet that already has a
toolbar gets it vertically. On the inner display sheets are centered and their
items stay horizontal. When you move a sheet with the preferred-placement API, a
sheet placed on the right gets a vertical bar; one placed on the left does not.

The bar is aligned to the **hardware**, so it stays on the same physical side in
right-to-left languages. Content adapts around it; the bar itself does not move.

## Ordering items

Audit your toolbar configuration against this hierarchy, top to bottom:

1. **Primary navigation** — back, close. With a navigation controller the back
   button is added for you. For a custom back or close, use the
   `cancellationAction` placement in SwiftUI; in UIKit use a leading item and
   leave `leftItemsSupplementBackButton` at its default of `false`.
2. **Prominent actions** — done, and similar. Use the `topBarPinnedTrailing`
   placement in SwiftUI, `pinnedTrailingGroup` in UIKit.
3. **Everything else**, keeping its original grouping. A vertical spacer
   separates top and bottom placements even once they're unified into one bar.

Not every pose lays bars out vertically, so keep placement consistent. Users
should not have to relearn where an action lives each time they open the device.

## Symbol or text

This is where most polish is won or lost.

A horizontal bar gives items a fixed height and flexible width. A vertical bar
inverts that: **fixed width, flexible height**. Narrow and tall strongly favors
**symbol-only** representations.

The system already picks a representation from the icon and title you supply —
icon when visible in a bar, text when there is no icon, both once the item moves
into an overflow menu. None of that changes. What is new is that the system also
weighs whether an item suits the vertical axis: items with an icon go vertical,
text-only items stay horizontal.

So: **always provide both a title and an image**, even when you expect the image
to be used. Use a SwiftUI `Label` or the corresponding `UIBarButtonItem`
properties. The title is what the system falls back on in overflow menus and
expanded forms.

### Overriding with AxisBehavior

The inference is usually right. When it isn't, `AxisBehavior` lets you correct it:

**Force horizontal** when an item alternates between a symbol and text — an edit
button that becomes "Done", for example. Even though the symbol could sit in a
vertical bar, the text form can't, and an item that jumps axes is jarring. The
system Edit button handles this already; a custom equivalent needs the
horizontal-only behavior. Keep related items on the same axis as a rule.

**Allow vertical** when you have a custom view that the system would otherwise
keep horizontal but which does have a good vertical representation.

### Reducing text so more can go vertical

Minimize title-only items and custom views that pair text with an image. Most are
better as symbols. A count rendered inline next to an icon, for instance, becomes
a **badge** on the symbol — the iOS 26 badge API gives you the standard
appearance on every device — turning a mixed item into a symbol-only one.

The test: *is the text reinforcing the symbol, or carrying information the symbol
can't?* Supplementary text can go. A cart button showing a running total cannot —
keep that one horizontal.

Keyboard accessory bars stay attached to the keyboard. They never move to the
vertical axis.

### Custom views

Opted-in custom views must either fit the bar's fixed width or lay out vertically
on their own. Revisit their metrics — a control panel might hide its labels and
shrink slightly when vertical to free up room.

To branch on this, read `toolbarVerticalEdge` (environment value in SwiftUI,
trait in UIKit). It's readable from the content view or from inside the item's
own view, and it is populated only when items can be on the vertical axis — `nil`
or unspecified otherwise.

Two behavioral details worth knowing: a vertical bar has no scroll edge effect by
default, but it *does* get a background when Reduce Transparency is on, so keep
custom content legible either way. And flexible spacers collapse to zero on the
vertical axis while fixed spacers keep their minimum — though your app shouldn't
be adding bar spacing manually on either axis.

**Group instead of spacing.** Rather than inserting spacers by hand, express the
relationship: `ToolbarItemGroup` in SwiftUI, `UIBarButtonItemGroup` in UIKit.
Groups space themselves against neighbouring groups and re-space as the available
room changes — which on this device happens constantly. Manual spacing is fixed
at exactly the moment it needs to be fluid.

**Keep controls near what they act on.** When a control belongs to a content area
that isn't the trailing one, leave it with that area instead of sending it to the
side bar. Proximity is what tells someone the control applies to *that* pane. In a
mail-style layout, controls acting on the message list belong above the list, not
in the shared vertical bar where they'd read as applying to the open message.

## Overflow

Items overflow more readily here — the outer display in landscape has little
vertical room, and competing UI such as the keyboard or pinned Picture-in-Picture
squeezes it further.

**First decide what survives longest: toolbar items, or the tab bar.**

- Navigation-driven screens should let the **toolbar compress first**, keeping
  primary destinations reachable. This is the default.
- Task-driven screens should let the **tab bar compress first**, preserving
  frequently used actions.

Configure this per view with the toolbar compression behavior API.

**Consolidate into the system overflow.** If the app has its own overflow menu,
fold its actions into the system-managed one — `ToolbarOverflowMenu` in SwiftUI,
`UINavigationItem.additionalOverflowItems` in UIKit. Reserve the ellipsis symbol
for overflow specifically; give other menus their own distinct symbols rather
than importing conventions from other platforms.

**Then set priorities.** By default items overflow bottom to top. Assign a
visibility priority — `ToolbarItemVisibilityPriority` in SwiftUI,
`UIBarButtonItemVisibilityPriority` in UIKit — to control the collapse order.
Prioritize by group first, then within a group if you need finer control.

Two things deserve high priority: actions people reach for constantly (compose,
new note), and controls conveying status such as badged items, which are useless
once hidden.

## When to turn it off

**Default answer: don't.** Side-mounted controls are a defining pattern of this
device, and Apple's guidance is explicit that you generally shouldn't override the
placement. Familiar control positions are what let someone pick up your app and
already know it, and every app that opts out erodes that a little.

The legitimate exceptions are narrow:

- **Interfaces that don't need bars at all** — a calculator-style layout that
  spans the full display width. This works for visual, immersive, non-scrolling
  interfaces, provided nothing collides with the Dynamic Island or status bar. You
  can also mix: a full-width background or header with the scrollable content
  inset.
- **Control-light sheets**, where one close button doesn't justify surrendering
  the width.

Use `toolbarVerticalBehavior` (SwiftUI) or `preferredVerticalBarBehavior` (UIKit)
to opt out. When a sheet opts out on the outer display, it stops just short of
the front camera and the status bar repositions itself.

## Checklist

1. Rebuild against the latest SDK.
2. Replace hand-rolled bars with container-provided ones.
3. Give every item both a title and an image.
4. Order items: navigation, then prominent actions, then the rest.
5. Convert text+symbol items to symbols with badges where the text is
   supplementary.
6. Apply `AxisBehavior` to items that alternate between symbol and text.
7. Choose toolbar-first or tab-bar-first compression per view.
8. Consolidate custom overflow into the system menu, and assign
   `visibilityPriority`.
9. Verify in every pose in Device Hub, including Split View on both sides.
