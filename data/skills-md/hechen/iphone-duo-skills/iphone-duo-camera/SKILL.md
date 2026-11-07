---
name: iphone-duo-camera
description: Adapt an AVFoundation or AVKit camera app for iPhone Duo, where opening or closing the device moves the app between displays and a camera can start facing the other way. Use when choosing between the virtual front camera and the inner and outer ultra-wide cameras, adopting AVCaptureDeviceDirectionCoordinator, fixing preview mirroring or rotation after a display change, switching capture inputs safely, or verifying saved photos and video on the device.
license: MIT
---

# iPhone Duo camera

Read [camera evidence](references/camera.md). The direction coordinator and the inner and outer camera types need the iOS 27.1 SDK. Do not infer an API from a camera's marketing name.

## Choose the capture strategy

Establish the product requirement: ordinary front-camera continuity, a specific physical camera's capabilities, or a display-relative capture experience. The virtual front camera follows the active display with no extra work but exposes only what both front cameras share. Selecting the physical cameras gives their full capabilities and makes following their direction the app's job. Inspect available device formats rather than assuming a model guarantees a resolution or frame rate in the current configuration.

Document the session owner, serialization mechanism, preview owner, and actor boundaries. Keep capture logic out of presentation models where the project already has a reusable capture layer; do not undertake an unrelated architectural rewrite.

## Handle transitions deliberately

Ask a direction coordinator which cameras face the same way as the preview view instead of reading a camera's position. Create it on the main actor, keep it alive as long as its view is on screen, and use one per preview view. Pass the sendable descriptors it reports to the actor that owns the session; never call AVFoundation from its handler. Resolve a descriptor there, handle a camera that no longer exists, and replace a single input rather than running both cameras unless the product needs it.

Serialize session reconfiguration and prevent stale direction callbacks from replacing a newer selection. Check input compatibility, retain enough state to restore the previous input when replacement fails, and present a clear interruption state if recording cannot continue. Do not promise seamless recording across a device switch without measured evidence.

Keep preview mirroring, saved-media orientation, and camera selection as separate decisions. Mask stale frames while the new camera starts. Derive mirroring from direction, reapply it after every input change, and create a new rotation coordinator for each camera. Verify output with text and an asymmetric subject: a plausible preview does not prove the saved file is correctly oriented.

Preserve authorization handling, interruption recovery, and resource cleanup. Avoid synchronous camera startup or expensive session work on the main thread. Use the project's established capture actor or serial executor and satisfy actual Swift concurrency constraints rather than adding unchecked sendability.

## Verify

Test permission denial, unavailable cameras, rapid open and close, background and foreground transitions, and capture interruption. Inspect saved photos and videos, not only screenshots. Exercise reduced-capability paths and confirm the UI stays responsive. Content for the outer display during capture belongs to the scenes skill.

Return the strategy tradeoff, session and state boundary, compatibility evidence, and observed failures or untested hardware cases. Simulator has no camera, so it cannot establish camera behavior.
