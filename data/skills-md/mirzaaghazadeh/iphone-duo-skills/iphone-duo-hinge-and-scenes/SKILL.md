---
name: iphone-duo-hinge-and-scenes
description: Use the iPhone Duo hinge angle for interactions and effects, support Split View multitasking and multiple app scenes, and pair UI across both displays with scene accessories including CameraCaptureAccessory. Use when building fold-driven effects, multi-window support, or dual-display experiences.
---

# Hinge, multitasking and scenes

Three capabilities that are unique to iPhone Duo, in rising order of ambition:
reacting to the hinge, participating in Split View, and putting your own UI on
both displays at once.

## The hinge

The system itself responds to the hinge — the wallpaper reacts to the angle with
a zoom effect as the device opens. Apps can read the same signal.

Use the `onHingeChange` modifier in SwiftUI, or `UIHingeInteraction` in UIKit.
Both give you:

- a coarse **status** — closed, partially open, fully open
- a **continuous angle**, updated live

`onHingeChange` hands your closure the previous and current hinge context.

Two things to check before using the value:

1. **Is there a hinge at all?** A `nil` hinge means the app is running on a
   device without one. Same binary, most devices.
2. **Is the device in a state you care about?** Usually you only want updates
   while partially open — and you need an `else` branch that resets whatever the
   angle was driving, so the effect doesn't stick at a stale value once the user
   opens the device flat.

Then map the angle to your parameter and update state.

### What the hinge is for

**Interactions and effects.** The angle is a live, continuous input stream — it
behaves like a sensor, and it suits things that respond continuously. Driving a
pitch bend from the fold angle, the way a whammy bar works, is the right shape of
idea.

**Not layout.** Do not lay out views from the hinge angle. Layout has proper
tools that are declarative, testable and correct on devices with no hinge:
arrangements and reserved regions, in
`../iphone-duo-adaptive-layout/SKILL.md`. Reaching for the angle here produces
layout that thrashes during the fold and breaks everywhere else.

## Split View multitasking

**Every app participates.** Two apps sit side by side, created with the familiar
home gesture — drag an app to one side and drop it. There's a second layout too,
stacking video and apps together when Picture-in-Picture is pinned. Your app
handles both identically.

If the app already supports resizing on iPad or under iPhone mirroring, it is
most of the way there. The system gives you size classes and scene geometry to
make layout decisions from; the general guidance in
`../iphone-duo-readiness/SKILL.md` applies unchanged.

The detail worth testing: in Split View, vertically laid out bar content can
appear on **either** side of your app, depending on which half you occupy. Drag
the app to both sides in Device Hub and check that asymmetric safe area handling
holds up.

## Multiple scenes

iPhone Duo is the first iPhone to support **multiple simultaneous instances of an
app's UI**. If the app already supports this on iPad, it works here too.

One behavior is genuinely new, though:

**New windows cannot be created on the outer display.** That is reserved for the
inner display, and the availability changes as the user opens and closes the
device. This dynamic availability doesn't exist on iPad.

Consequences:

- **Handle errors when requesting new scenes.** A request that always succeeded
  on iPad can now fail.
- **Prefer `UIWindowSceneActivation`**, which automatically hides itself when new
  windows aren't available — so users never tap an affordance that can't work.

## Scene accessories

Scene accessories pair additional content with your app's main UI on another
display. They aren't Duo-specific — the same mechanism backs using an iPhone as a
controller for a game on an external display — but iPhone Duo gives every user
two displays to work with.

The system controls availability dynamically. Accessories are enabled by default
and can be toggled at any time, so **observe availability rather than assuming
it**: use observation tracking, or the `onAvailabilityChange` modifier, and
reflect the current state in your UI (disabling a toggle button when the
accessory can't be shown, for instance).

### CameraCaptureAccessory

For camera apps, `CameraCaptureAccessory` puts UI on the **outer** display while
the app's main UI stays on the **inner** one. The person being photographed can
see something while you shoot — showing a child something entertaining, or
running a teleprompter for a subject on camera.

Two conditions gate availability: the app must be **full screen on the inner
display**, and it must have an **active camera session**.

**Register the accessory on the same view as your camera UI.** Scoping it that
way means the accessory appears and disappears with the camera view itself,
without any extra lifecycle code. In SwiftUI that's the `sceneAccessory` modifier
applied to the camera view.

Adding a toolbar control to toggle the accessory is a natural pairing — drive it
from your model, and use `onAvailabilityChange` to disable the control when the
accessory isn't available, such as when the device is closed.

Camera specifics — which physical camera is streaming, and which way it is
actually facing once two displays are involved — are in
`../iphone-duo-camera/SKILL.md`. That question gets genuinely subtle, and the
direction coordinator exists to answer it.

## Checklist

1. Support resizing first. Split View correctness follows from it.
2. Test the app on both sides of a Split View, in every pose.
3. If the app supports multiple windows, handle scene-request failure and adopt
   `UIWindowSceneActivation`.
4. Consider whether a hinge-driven effect genuinely improves the app — then guard
   for `nil` hinge and reset state when the device leaves the range you care
   about.
5. For camera apps, evaluate whether a `CameraCaptureAccessory` on the outer
   display would help the person in front of the lens.
