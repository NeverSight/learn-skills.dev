---
name: threejs-audio
description: "Add Three.js spatial audio, user-controlled playback, listener movement, and audio lifecycle handling."
---

# Spatial Audio

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Establish whether audio communicates information or provides optional ambience. Expose mute/volume and any required textual equivalent in HTML. Start or resume audio from a user interaction and handle autoplay rejection without breaking the scene.

Attach the listener to the active viewpoint and handle camera changes without duplicating listeners or output paths. For positional sources, choose distance/rolloff and directional cones in the scene's units. A positional source does not automatically simulate wall occlusion.

Load and decode asynchronously with explicit failure and stale-result handling. Bound concurrent sources and reuse buffers where appropriate. Avoid replaying a sound on every frame of a collision; trigger from meaningful state transitions.

Coordinate pause, visibility changes, route transitions, and XR session transitions with playback. Stop/disconnect owned sources and release listeners. Do not close an AudioContext shared with another part of the application.

Verify blocked autoplay, first interaction, mute persistence, moving-camera attenuation, rapid retriggers, and repeated mount/unmount. Measure perceived volume on actual output devices when spatial audio matters.

## API reference

Consult the [official documentation](https://threejs.org/docs/pages/PositionalAudio.html) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
