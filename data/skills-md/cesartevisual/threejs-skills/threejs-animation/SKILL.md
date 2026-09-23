---
name: threejs-animation
description: "Implement Three.js animation clips, skeletal animation, transitions, scroll timelines, and frame-independent motion."
---

# Animation and Timelines

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Identify which system owns each animated property: imported clips, procedural motion, scroll timeline, controls, or physics. Blend or hand off explicitly when two systems would otherwise write the same transform.

Use elapsed time or delta in seconds rather than frame counts. Clamp large visual deltas after a tab resumes; physics needs its own fixed-step policy. Use frame-independent damping such as 1 - exp(-lambda * delta), with reusable scratch values.

Create a mixer for the appropriate root, select clips by inspected names, and define loop, pause, finished, and transition behavior. Reset and play the destination action as needed for crossfades; inspect root motion rather than silently translating both the root and its parent.

For scroll, map normalized section progress to a defined timeline. Recalculate ranges on layout changes and handle reverse scrolling and jumps directly. Do not accumulate scroll deltas as if all input arrived continuously. Keep text readable and content reachable without the animated camera path.

Respect reduced-motion preferences by removing nonessential motion or presenting stable states. Suspend work when the scene is inactive where practical. Stop owned actions, remove mixer listeners, and uncache roots only after their actions stop.

Verify at different frame rates, after backgrounding, during rapid state changes, on backward scroll, and with reduced motion. Confirm animation speed and final states remain consistent.

## API reference

Consult the [official documentation](https://threejs.org/docs/pages/AnimationMixer.html) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
