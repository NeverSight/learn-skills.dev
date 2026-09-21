---
name: threejs-xr
description: "Implement Three.js VR or AR sessions, XR input, reference spaces, hit testing, and session lifecycle."
---

# WebXR

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Confirm requested VR/AR mode, target hardware/browser, secure context, and current installed XR APIs. Feature-detect session support and request sessions from a user gesture. Distinguish required and optional session features so an optional capability does not unnecessarily block entry.

Let the XR-compatible renderer loop own session frames and poses. Use XR cameras/reference spaces rather than overwriting their pose with ordinary orbit controls. Establish meters, world origin, and floor assumptions; handle reference-space reset.

Separate target-ray input from grip/controller models. Define select, squeeze, handedness, disconnect, and hand-tracking behavior as needed. For AR hit testing, handle missing hits and choose intentional placement confirmation rather than continuously teleporting content.

Provide entry, exit, unsupported, denied, and interrupted states. Restore desktop controls and scene state on session end. Keep asset and shadow/effect costs within the headset's frame requirements; test comfort, text legibility, and locomotion choices.

Release session-owned listeners and transient resources. Test on actual requested hardware for tracking, input, placement, and comfort. Emulation can exercise flows but is not evidence of headset usability. Keep an ordinary browser view available when it serves the product.

## API reference

Consult the [official documentation](https://developer.mozilla.org/en-US/docs/Web/API/WebXR_Device_API) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
