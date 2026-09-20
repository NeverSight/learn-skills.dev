---
name: iphone-duo-camera
description: Build camera capture for iPhone Duo's two front cameras — the virtual front camera, the inner under-display and outer ultra-wide devices, AVCaptureDeviceDirectionCoordinator, preview mirroring and video gravity, and dual-display capture. Use when an app captures photo or video and must handle the device opening, closing or flipping.
---

# Camera on iPhone Duo

iPhone Duo is the first iPhone with **two front cameras**. Both are square
sensors with an ultra-wide field of view: one on the outer display, and one
beneath the inner display — the first under-display camera on iPhone.

That creates a problem no previous iPhone had. "Front" no longer means "pointing
at the user."

## Pick a strategy first

Everything downstream follows from this choice.

### The virtual front camera — automatic, limited

Discover a front camera the ordinary way — an `AVCaptureDevice.DiscoverySession`
requesting position `.front` with a Wide or Ultra Wide device type — and on
iPhone Duo you resolve to a new **virtual front camera**. It switches between the
two physical cameras by itself: inner camera when open, outer camera when closed.

It always uses the most relevant camera, and you write no switching code.

The cost is that it exposes only what **both** physical cameras can do:

- max **1080p**, **60 fps**
- **no depth**

If the app needs 4K, high frame rates, or any depth-based feature, this is not
enough.

### The individual cameras — full capability, your responsibility

Address each physically, via the built-in **outer** ultra-wide and built-in
**inner** ultra-wide device types:

| | Inner (under-display) | Outer |
|---|---|---|
| Max video | 1080p @ 60 fps | 4K @ 120 fps |
| Depth | supported | supported |

Full capabilities, but now **you** must switch cameras when the user opens or
closes the device. Which brings us to the hard part.

## Which way is a camera actually facing?

`AVCaptureDevice` has always had a fixed `position` — on iPhone, `.back` or
`.front`. Both of iPhone Duo's front cameras report `.front`. That property
describes where a camera sits **on the hardware**, and on a device whose displays
can face opposite directions it no longer tells you where the camera **points
relative to the person looking at your UI**.

Three situations make this concrete:

- The user is looking at the inner display while the app streams the outer front
  camera — a "front" camera facing *away* from them.
- The device closes while that camera is streaming, and the same camera swings
  around to face them directly.
- The device is open and flipped, so a *rear* camera is now the selfie camera.

### AVCaptureDeviceDirectionCoordinator

`AVCaptureDeviceDirectionCoordinator` (in **AVKit**) answers the real question:
which cameras are forward-facing *right now*, relative to a given view. Build one
from three things — your app's `UIView`, the device types to monitor, and a
change handler — and it keeps you current as the device moves.

Because it is anchored to a view, it reports facing **relative to the display
that view is on**. When the view is on the outer display, the outer front cameras
are forward-facing and the rear cameras are backward-facing. Open the device, the
view moves to the inner display, your handler fires, and now the inner front
camera is forward-facing while the outer front *and* rear cameras are
backward-facing.

**Driving both displays at once?** Create **one coordinator per view**. Each
reports relative to its own display, so the same rear camera is forward-facing to
the outer view's coordinator and backward-facing to the inner view's. That is
correct, not contradictory — it is the whole point. (Dual-display camera UI comes
from the scene accessories API; see
`../iphone-duo-hinge-and-scenes/SKILL.md`.)

### Concurrency

The coordinator is tied to a view, so it is **isolated to the main actor**. Your
change handler must not call AVFoundation APIs directly.

Instead of an `AVCaptureDevice`, it hands you an **`AVCaptureDeviceDescriptor`** —
a sendable, main-actor-safe stand-in carrying everything needed to construct the
real device. Pass the descriptor to your camera actor and build the
`AVCaptureDevice` there. This is the intended path; don't try to smuggle a device
across the boundary.

### What the handler should do

1. Reconfigure the `AVCaptureSession` to keep streaming from whichever camera is
   now forward-facing.
2. Re-evaluate **mirroring**. Mirroring should follow the *direction*, not the
   position: when a rear camera has become the forward-facing one, mirror the
   preview so it feels like a normal selfie view.
3. Apply any UI updates the camera change implies.

## Preview polish

**Streaming the rear camera's full field of view on the inner display** leaves
extra room around the preview. Two reasonable choices: offset the preview and
group controls in the space left over, or let the preview fill the display.
Control this with `videoGravity` on `AVCaptureVideoPreviewLayer`.

**Streaming an ultra-wide front camera**, exploit the square sensor — set
`dynamicAspectRatio` on the `AVCaptureDevice` to pick a landscape aspect ratio
that fills the inner display.

**Rotation.** Adopt `AVCaptureDeviceRotationCoordinator` so previews and captures
stay upright. On iPhone Duo it updates when the app moves between displays, which
is what keeps rotation consistent across both. Once you have adopted it, **turn
off camera-sensor-orientation compensation** — it is enabled on all of iPhone
Duo's front cameras and is redundant work once the rotation coordinator is doing
the job.

Note that direction and rotation are separate coordinators solving separate
problems. Which camera to stream is direction; which way its output is oriented
is rotation. Most camera apps on this device want both.

## Checklist

1. Build against the iOS 27.1 SDK.
2. Decide: virtual front camera (automatic, 1080p60, no depth) or individual
   cameras (full capability, manual switching).
3. If individual, adopt `AVCaptureDeviceDirectionCoordinator` — one per view.
4. In the change handler, reconfigure the session, re-decide mirroring, update UI.
   Move devices across actors as `AVCaptureDeviceDescriptor`.
5. Set `videoGravity`, and `dynamicAspectRatio` for front-camera capture.
6. Adopt `AVCaptureDeviceRotationCoordinator`, then disable sensor-orientation
   compensation.
7. Consider a `CameraCaptureAccessory` so the subject sees something on the outer
   display.
8. Test opening, closing and flipping the device mid-session in Device Hub.

Apple's related articles: *Choosing a Camera by the Direction it Faces* and
*Supporting Device Rotation in Your Camera App*. For the square sensor generally,
see *Support the Center Stage front camera in your iOS app* from WWDC26.
