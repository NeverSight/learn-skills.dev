---
name: iphone-duo-games
description: Adapt a game to iPhone Duo — filling the screen across every device pose, orientation locking, aspect ratio versus letterboxing, keeping touch controls out of the fold, and consistent text and control sizing while resizing. Use when the project is a game or uses a game engine such as Unity, Unreal, Godot, SpriteKit or Metal.
---

# Games on iPhone Duo

Games get a carve-out from most of this device's UI guidance — no toolbars to
send vertical, no split views to adapt. What they don't get a carve-out from is
**resizing**. The screen changes size and shape underneath a running game every
time someone opens, closes, folds or rotates the device, and a game that assumed
a fixed viewport will letterbox, stretch, or drop controls off the edge.

## You may lock orientation. You may not stop filling the screen.

Locking to portrait or landscape is fine and supported. What is not fine is
treating that lock as permission to assume a fixed size.

Two reasons it doesn't hold here:

1. The device has **two displays with different dimensions**, and your game moves
   between them mid-session.
2. **The inner display doesn't honor supported interface orientations.** An
   orientation lock that has held on every previous iPhone stops holding on the
   inner display.

`UIRequiresFullScreen` behaves the same way — still honored, but your game still
resizes when the device opens and closes. Plan for the resize regardless.

So: pick your orientation, then make sure the game **fills the screen in every
pose**. That is the actual requirement.

## Aspect ratio beats letterboxing

When the viewport shape changes, you have three options, in order of preference:

**1. Change the aspect ratio.** Show more or less of the world. This is the
preferred answer: extend the camera frustum, widen the visible field, let the
scene breathe into the space it has been given. The game stays full-bleed and
feels native to whatever pose it's in.

**2. Letterbox or pillarbox with artwork.** If the design genuinely can't take a
variable aspect ratio — a fixed puzzle grid, a precisely tuned platformer
camera — then bars are acceptable, but fill them. Extend the background,
continue the scene's artwork, or run themed framing into the padding. The goal is
that it reads as a deliberate frame rather than a game that failed to fit.

**3. Bare black bars.** Avoid. This is what "didn't adapt" looks like.

## Keep text and controls the same size

When the viewport resizes, resist the urge to scale the whole scene uniformly.
Uniform scaling shrinks your HUD text and touch targets along with the world —
so opening the device to the *larger* display can make text harder to read and
buttons harder to hit, which is exactly backwards.

Scale the world; keep UI in its own layer sized in points. Text and controls
should stay as close to a constant physical size as you can manage across every
pose. On-screen touch controls in particular must not shrink below a comfortable
target just because the aspect ratio changed.

## The fold is a real problem for touch controls

This is the iPhone Duo-specific issue most likely to hurt a game.

When the device is partially folded, the inner display curves through the middle,
and that region is genuinely harder to see and to tap. A virtual joystick, a fire
button, or a drag target that lands in the curve becomes unreliable — not
invisible, just worse, which is harder to diagnose from a bug report.

Games rarely use the system components that get fold avoidance for free, so this
one is on you:

- Query reserved regions and keep interactive controls out of the **division
  region** (the fold). See `../iphone-duo-adaptive-layout/SKILL.md` for the API
  and the displacement patterns.
- Anchor touch controls to the **outer edges** rather than centering them. Edge
  anchoring is more robust across every pose and costs nothing when flat.
- Watch the **occlusion regions** too: the outer front camera is always present,
  and the inner camera appears whenever it activates.

Purely visual, non-interactive content can cross the fold. It's touch targets and
critical readouts that need to move.

## Poses worth designing for

You don't need a bespoke layout per pose, but two are worth a thought:

**Tabletop / laptop.** The device stands on a surface, half the display facing up
and half facing the player. This is a genuinely new play position — the lower
region is a stable touch surface and the upper region is a viewing surface. A
game with a board-and-controls split maps onto it naturally.

**Tent.** Standing on its edges, hands-free. Good for idle, spectator, ambient or
turn-based games.

Treat both as bonuses. Don't tie any functionality to a pose someone might never
use.

## Split View

Games participate in Split View multitasking like everything else — your game can
end up in half the inner display. It will be smaller and a different shape than
anything you designed for. Make sure it still renders correctly and doesn't drop
controls off the edge; you are not obliged to make it a great *play* experience
at that size, but it must not break.

## The hinge as an input

The hinge angle is available as a live, continuous value — coarse status plus an
angle — via `onHingeChange` in SwiftUI or `UIHingeInteraction` in UIKit. For a
game engine, bridge it the way you'd bridge any other native sensor.

It is a genuine novelty input, and worth considering for effects, camera
parallax, or a mechanic. Two cautions: guard for a `nil` hinge, since the same
binary runs on every non-folding iPhone, and never make it the *only* way to
perform an action. Details in `../iphone-duo-hinge-and-scenes/SKILL.md`.

## Engine notes

Most engines expose the viewport as a resize event and a safe-area inset query.
Wire both, and treat resize as a first-class event rather than a startup value:

- **Unity** — `Screen.safeArea`, and handle resolution changes at runtime rather
  than reading once in `Start()`.
- **Unreal** — safe zone / title safe values, and re-evaluate on viewport resize.
- **Godot** — the safe area API plus a stretch mode that tolerates changing
  aspect ratios.
- **SpriteKit / Metal** — you already get the resize through the view; the work
  is making the scene respond rather than assuming the initial drawable size.

Reserved regions and the hinge angle are iOS 27.1 APIs with no engine-level
equivalent, so those need a native plugin. The bridging pattern is the same one
described in `../iphone-duo-flutter/SKILL.md` and
`../iphone-duo-react-native/SKILL.md`.

## Checklist

1. Handle viewport resize as a live event — not a value read at launch.
2. Fill the screen in every pose, whatever your orientation lock.
3. Prefer changing aspect ratio; if you letterbox, fill the bars with artwork.
4. Keep HUD text and touch targets at a consistent physical size across poses.
5. Anchor interactive controls to edges, and keep them out of the fold.
6. Verify the game still renders correctly in Split View.
7. Test every pose in the iPhone Duo simulator in Device Hub — open, closed,
   folded, rotated.
