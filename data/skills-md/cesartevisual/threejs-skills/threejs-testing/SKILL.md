---
name: threejs-testing
description: "Test Three.js features with browser checks, deterministic visual fixtures, lifecycle tests, and device-specific evidence."
---

# 3D Testing and Visual QA

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Translate the requested behavior into observable checks: visible subject, correct framing, interaction outcomes, load failure/retry, resize, teardown, and any explicit performance target. Keep test scope proportional to the change.

Use unit tests for pure coordinate transforms, selection mapping, timestep policies, and reducers where these are meaningful. A mocked renderer cannot prove pixels render correctly. Run the production build and a browser fixture for GPU integration.

Make visual fixtures reproducible: seed randomness, fix camera/viewport/pixel ratio, stop or seek animation to a known time, and wait for asset readiness plus a rendered frame. Use a semantic readiness signal, not an arbitrary sleep. Capture console and network failures along with screenshots.

Use tolerant comparisons for GPU-dependent pixels; avoid treating exact image equality across unrelated drivers as a portable contract. Inspect screenshots for cropping, contrast, shadow defects, text/overlay occlusion, and loading remnants. Scope browser feature expectations to the tested backend.

Exercise repeated navigation, rapid asset changes, hidden-to-visible sizing, touch interaction, reduced motion, unsupported rendering, and the relevant real device/browser. Headless software rendering is not a mobile GPU benchmark.

Report checks as passed, failed, or not run with reasons. Do not claim performance, XR hardware support, or assistive-technology behavior from compilation alone.

## API reference

Consult the [official documentation](https://playwright.dev/docs/test-snapshots) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
