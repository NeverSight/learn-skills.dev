---
name: iphone-duo-design-review
description: Review or design an iOS interface for iPhone Duo's poses — closed, open, book-folded, tabletop and tent — covering side-mounted controls, asymmetric layouts, fold avoidance, sheets, and how to use the inner display well. Use for design critique, mockup review, or deciding what a screen should look like on a foldable iPhone rather than how to code it.
---

# Designing for iPhone Duo

A design skill, not an implementation one. For APIs, see the sibling skills.

Closed, iPhone Duo is compact, familiar and pocketable. Open, it is the largest
canvas ever on an iPhone. It gets held and set down in many ways: partially
folded like a book, seated on a table like a laptop with the inner display
facing the user, or standing on its edges.

## The governing principle

**One app that adapts — not several designs stitched together.**

Users open and close this device constantly, often mid-task. If the hierarchy or
the available functions change between inside and outside, they have to
re-orient every time. So:

- Never tie functionality to a pose. Everything reachable in one pose is
  reachable in all of them.
- Keep the hierarchy identical across displays.
- If you do build a pose-specific layout, it keeps the same controls and the same
  general hierarchy as the others.

## Design to two size classes, not to poses

The temptation is a custom layout per pose. Resist it. Design to:

- **Compact width** — the outer display
- **Regular width** — the inner display

Avoid fixed widths, breakpoints, or any metric tied to a specific screen. Build
with layout margins and horizontal safe area insets and the adaptation mostly
happens on its own. The honest summary: **design the app to be freely resizable**
and iPhone Duo is largely handled.

The one optional layout worth considering is the **tabletop pose** — media up
top, tappable controls on the stable base below. It suits hands-free use. It is
optional, and it still owes users the same controls as every other pose.

## Controls on the side

Closed, the display is wider and shorter than a traditional iPhone. Controls that
would sit at the top and bottom move to the **right side**, freeing vertical
space and landing within easy reach of the thumb. To their left is an
uninterrupted content area comparable to a conventional iPhone screen.

That side region is shared. It holds the tab bar, app toolbars, navigation
controls like back, the redesigned status bar, and the Dynamic Island — which now
expands *vertically* as Live Activities arrive. When room runs short, app
controls collapse into an overflow menu automatically.

Mapping an existing iPhone app across is mostly mechanical:

- Toolbar buttons from the top → top of the vertical region
- Toolbar buttons from the bottom → bottom of the vertical region
- Tab bar → stays bottom-aligned

**Exception:** items too wide for that side region — a text button, a segmented
control — should stay in the navigation bar. Don't force them.

**The one pose that keeps horizontal bars is the inner display in portrait**,
where vertical space is plentiful.

In **Split View**, controls sit along the *outer* edge: an app on the left gets
its controls on the left edge, keeping them thumb-reachable and away from the
center.

## Asymmetry

Side-mounted controls make most layouts asymmetric. Three approaches, chosen by
content type:

**Offset content.** The default. Most content needs offsetting so it isn't hidden
behind the controls — and if the design aligns to horizontal safe area insets,
this happens automatically.

**Center on the full display.** No offset. Right for immersive, highly visual,
non-scrolling interfaces — but only when you are certain no interactive element
lands under the controls.

**Mix them.** A full-width background image or header behind inset, scrollable
foreground content. The rule that makes this safe: **every interactive element
lives inside the scrollable inset area**, so nothing tappable can be covered.

## The fold

Partially folded, the inner display curves through the center. Content
automatically moves away from that region — text and images shift aside to stay
readable, and interactive elements move to the sides where they're easier to hit.
The curve becomes a natural divider for the layout.

In portrait, folded, interactive elements move to the **bottom half**, easier to
reach while the device rests on a surface.

**Buttons are genuinely hard to tap in the fold.** The system nudges interactive
elements aside whenever the device is partially folded, and this behavior is
built into sheets, alerts, menus, toolbar buttons and more. Use system components
and you inherit it.

**Scrollable content is exempt.** It does not need to avoid the fold region.

The design goal is simple: keep interactive elements out of the curve as much as
possible.

Two refinements when you do adapt to the fold:

**Prefer containers that adapt themselves.** A split view that rebalances its
pane widths handles the fold better than anything you position by hand. In grids,
prefer an **even number of columns** so content divides cleanly either side of
the centre.

**Move as little as possible.** Controls that vanish or jump across the screen as
someone bends the device are hard to find and harder to track. Favour small
adjustments that keep things visible and tappable over rearranging the layout.

## Using the inner display well

A stretched-out iPhone app is the failure mode. Three approaches that work:

**Split views.** Surface multiple levels of hierarchy at once. The nuance worth
getting right: your information hierarchy must stay the same across displays, but
you may reveal *one more level of it* on the larger display. A mail app showing
either the message list or a single message when closed, and both side by side
when open, is the same hierarchy with more of it visible — not a different app.
That is the distinction between adapting and reinventing.

Standard split views also adapt to reserved regions on their own, rebalancing
column widths and margins so both panes stay visible as the device folds.

**Reflow to columns.** A vertically stacked layout that becomes a two-column
layout when horizontal space allows.

**Tab bar as sidebar.** For apps with tab bars, present the tab bar as a sidebar
on the inner display. Not for every app — it suits information-dense ones best.

## Sheets

Sheets behave differently by display, and it's worth knowing all four cases:

- **Outer display, default** — sheet controls move to the side like everything
  else.
- **Outer display, vertical bar disabled** — controls stay put. Good for a sheet
  with a single toolbar button, where a vertical bar costs more width than it
  earns. The sheet then stops just short of the front camera, and the status bar
  repositions itself.
- **Inner display** — standard horizontal bars, in both orientations.
- **Partially folded** — the sheet slides over to avoid resting in the fold.

## Multitasking and PiP

Split View is a **50/50 split** created with the home gesture — drag an app to
one side. The two halves work independently. Picture-in-Picture can be pinned to
the top of the screen; the app below resizes vertically to fit, and if the device
is partially folded the video expands to fill half the screen. Apps adjust
vertically to these video sizes in real time, so vertical flexibility is not
optional.

## Review checklist

Ask these of any iPhone Duo design:

1. Does anything interactive land in the fold, or under the side controls?
2. Is any function or hierarchy available in one pose but not another?
3. Are there fixed widths or breakpoints instead of size-class thinking?
4. Do toolbar items map cleanly to the side region — and are the wide ones left
   in the nav bar?
5. Is the inner display doing something better than stretching?
6. Does content offset from the safe area, center deliberately, or mix the two
   with every control inside the scrollable area?
7. Does the layout hold up in Split View on both sides, and with PiP pinned?
8. Are custom components reimplementing fold avoidance that system components
   would have provided?
9. Do controls sit near the content they act on, rather than being swept into the
   side bar away from the pane they belong to?
10. Does anything change *state* between displays, rather than just layout? State
    should survive opening and closing the device.

If the project is a game, most of this doesn't apply — see
`../iphone-duo-games/SKILL.md` instead, which covers filling the screen across
poses, aspect ratio versus letterboxing, and keeping touch controls out of the
fold.
