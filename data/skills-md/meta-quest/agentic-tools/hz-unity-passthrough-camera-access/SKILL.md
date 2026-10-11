---
name: hz-unity-passthrough-camera-access
license: Apache-2.0
description: Meta Quest Passthrough Camera Access (PCA) for Unity — access the forward-facing RGB cameras on Quest 3 / Quest 3S to feed Computer Vision and Machine Learning pipelines. Use when capturing the passthrough camera image/texture, reading the camera pose and intrinsics, projecting camera pixels into world space via `PassthroughCameraAccess.ViewportPointToRay`, wiring camera frames into ML/CV models, or reasoning about resolution, permissions, vendor tags, and the pinhole/principal-point model. For projecting the image onto a flat world-space surface (frustum-slice quad / image-plane overlay) see references/principal-point-offset.md; for placing 2D ML detections as world-space 3D bounding boxes see references/detection-bounding-boxes.md. Skip if the user only wants to cast the user's POV (use the Media Projection API instead) or is doing screen-space-only overlays.
---

# Meta Quest Passthrough Camera Access (PCA)

Building on top of the [Android Camera2 API](https://developer.android.com/media/camera/camera2),
Passthrough Camera Access provides access to the forward-facing RGB cameras on
Quest 3 and Quest 3S for the purpose of supporting Computer Vision and Machine
Learning. This API is distinct from the
[Media Projection API](https://developers.meta.com/horizon/documentation/native/native-media-projection/),
which supports casting from the user's POV (including the UI) and should be used
if your purpose is to represent what the user is seeing. Use the Passthrough
Camera API to add application-specific computer-vision capabilities that extend
the understanding of the user's environment and actions beyond what is provided
by the Scene API.

## Use Cases

This API provides an unobstructed view using the forward-facing RGB cameras and
can be integrated with ML/CV pipelines. Common use cases:

1. Specially-trained ML/CV models that identify specific objects the
   application can interact with (e.g. fitness equipment like dumbbells,
   industrial equipment like audio mixers).
2. ML/CV assistants or guides for experiences. For instance, a museum tour
   where looking at a painting surfaces information about its history, artist,
   and style using off-device LLMs.
3. Feedback for training or special-interest applications — after asking the
   user to perform a task, the app can detect whether it was done correctly by
   interpreting changes to the environment (e.g. writing on a whiteboard).
4. Design improvements. By interpreting the lighting or using the camera image
   to modify a texture, much more realistic design effects can be achieved.

## General Prerequisites

1. Horizon OS v74 or later.
2. Quest 3 or Quest 3S (Quest Pro and earlier are not supported).
3. Either permission `android.permission.CAMERA` or
   `horizonos.permission.HEADSET_CAMERA`. `CAMERA` grants access to both the
   passthrough and avatar cameras; `HEADSET_CAMERA` grants access only to the
   passthrough camera.
4. The **Passthrough feature** must be **enabled** to access the Passthrough
   Camera API.

## Passthrough Camera Using Android Camera2

Camera Access on Meta VR devices is implemented on top of
[Android's Camera2 API](https://developer.android.com/reference/android/hardware/camera2/package-summary)
within Horizon OS. Starting from Horizon OS v74, Camera2 and its Unity
extension are available on Meta VR headsets (Horizon OS v83 added an Unreal
extension). On Quest 3 and Quest 3S developers have access to the left and right
cameras on the face of the HMD.

The Android Camera2 API provides:

- **Image capture:** capture camera data for advanced processing.
- **Camera metadata:** query the API for hardware capabilities and
  configuration information.
- **Multi-camera support:** access and control multiple cameras.

## Known Issues

1. After the first install of an app using the Camera API in v74 after flashing
   a new OS, the RGB channels might flip causing color distortion (e.g. flesh
   tones appear bluish). Reboot the device to fix.
2. Passthrough Camera API is **not supported in XR Simulator**.
3. The passthrough camera texture captures a rectangular area (1280×960)
   smaller than what the user sees. The 1280×1280 resolution added in v83
   expands the vertical field of view, but still does not cover the entire
   passthrough view.
4. Restrictions applied by a parent to restrict Teen and Youth accounts (e.g.
   accessing the Passthrough Camera API) are not applied if the application is
   installed through the Meta Quest Developer Hub.

## Best Practices

1. **Ensure user privacy.** Camera image data is considered Device User Data and
   is covered by the Developer Data Use Policy. Adhere to this policy fully.
2. **Avoid costly processing on device.** On-device processing of camera images
   can enable compelling use cases, but keep experiences comfortable by
   maintaining a high framerate.
3. **Validate the feed on device.** After deploying, stream
   `metavr adb logcat --follow --tag Unity` while the pipeline runs to confirm
   frames flow, and check PCA API changes
   with `metavr docs search "passthrough camera access Unity"` before
   integrating — this surface moves fast.

## References

Detailed, task-specific guidance for projecting and placing PCA imagery in world
space lives under [references/](references/):

- **[references/principal-point-offset.md](references/principal-point-offset.md)** —
  Correctly project the camera image onto a flat world-space surface
  (frustum-slice quad, FOV visualizer, image-plane overlay) using the optical
  axis as the plane normal. Read this when corner rays from `ViewportPointToRay`
  produce a non-rectangular quad, a camera-aligned quad drifts off-center, or
  `2 * d * tan(fov / 2)` gives the wrong size on a device whose camera principal
  point is offset even though it worked on Quest 3.
- **[references/detection-bounding-boxes.md](references/detection-bounding-boxes.md)** —
  Draw precise 3D bounding boxes around real-world objects detected by an ML
  model. Read this when placing 2D ML detections (YOLO, SSD, DETR, custom CNN)
  into world space, building a camera-facing billboard quad from a 2D detection,
  or wiring `PassthroughCameraAccess` + `EnvironmentRaycastManager` for object
  localization.
