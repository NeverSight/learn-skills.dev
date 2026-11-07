---
name: hz-unity-device-readiness
license: Apache-2.0
description: "Audits a Unity project for Meta VR Glasses readiness across input and field of view — finds controller-dependent interactions such as OVRInput usage, recommends hand-tracking and ISDK controller-to-hands migrations, produces a prioritized migration plan, and detects head-locked UI that a narrower FoV would clip."
---

# Device Readiness

## Context

This skill prepares a Unity project for Meta VR Glasses device requirements across two dimensions: **input** (hand tracking as the primary input, not a fallback) and **field of view** (a device with a narrower FoV than current Quest headsets). The input workflow is immediately below; the field-of-view workflow is its own section further down.

The target device treats hand tracking as the primary input method, not a fallback. Most existing Quest projects were built controller-first, so the work isn't just "replace button presses with gestures" — it's rethinking interaction design so hands feel natural instead of like a worse controller. A systematic scan matters: find every controller dependency, understand the gameplay intent behind it, and map it to the right ISDK pattern.

When a Meta VR Glasses or Meta Quest device is connected, ground the audit in real device data first — `metavr device list` shows what's attached, and `metavr device info <id>` reports the device's input and display capabilities the audit should target.

## Analysis Workflow

### Step 1: Scan the Project

Build a complete picture of how the project handles input today. Controller dependencies hide in surprising places — not just obvious `OVRInput.Get()` calls, but also XR Interaction Toolkit components, Unity's legacy Input system, and custom grab systems. Cast a wide net:

```bash
# Find controller input usage
grep -r "OVRInput\.\(Get\|GetDown\|GetUp\)" --include="*.cs" .
grep -r "OVRInput\.Button\|OVRInput\.Axis" --include="*.cs" .

# Find XR Interaction Toolkit usage
grep -r "XRGrabInteractable\|XRRayInteractor\|XRDirectInteractor" --include="*.cs" .

# Find legacy Input system usage
grep -r "Input\.GetButton\|Input\.GetAxis\|Input\.GetKey" --include="*.cs" .

# Find interaction patterns
grep -r "Grabbable\|IGrabbable\|OnGrab\|OnRelease" --include="*.cs" .
grep -r "Raycast\|RaycastHit\|Physics\.Raycast" --include="*.cs" .
```

### Step 2: Categorize Findings

For each finding, categorize it:

| Category | What to Look For | Impact |
|----------|------------------|--------|
| **Controller Input** | `OVRInput.Get()`, button/axis references | Must replace with hand gestures or ISDK components |
| **Grab Systems** | Trigger-based grab, distance grab | Convert to `HandGrabInteractable` with pinch detection |
| **UI Interaction** | Ray-based UI, pointer clicks | Convert to poke interactions (`PokeInteractable`) |
| **Movement** | Thumbstick locomotion, snap turn | Redesign for hand-based or gaze-based navigation |
| **Object Manipulation** | Thumbstick rotation, button-based scaling | Use direct hand rotation/scaling with two-hand support |

### Step 3: Suggest Adaptations

For each controller-dependent system, suggest a specific ISDK-based replacement. Reference the hand-tracking patterns in `references/hand-tracking-patterns.md` for implementation details.

### Step 4: Prioritize

Rank suggestions by impact and effort:

- **High Priority** — core gameplay interactions that use controller APIs and must be replaced (e.g. OVRInput-based grab, trigger-based shooting).
- **Medium Priority** — secondary interactions on controller APIs (e.g. thumbstick scrolling, ray-based UI navigation).
- **Low Priority** — enhancements for code that already uses hand tracking but could be improved (hover feedback, audio cues, two-hand support). Nice-to-haves, not required to be hand-ready.

**Important.** If the project already uses ISDK hand tracking (`HandGrabInteractable`, `PokeInteractable`, etc.) and has no controller-dependent code, report that it is already hand-ready. Surface enhancements only as Low-priority items — don't treat them as required changes. A project that already works with hands should not receive a long list of improvement suggestions.

## Output Format

Provide your analysis as a structured report:

1. **Project Summary** — what type of project this is and its core mechanics.
2. **Readiness Score** — rough percentage of interactions that already work with hands.
3. **Required Changes** — prioritized list with:
   - what was found (specific files / classes),
   - what needs to change,
   - which ISDK pattern to use (reference `hand-tracking-patterns.md`),
   - estimated complexity (Low / Medium / High).
4. **Quick Wins** — changes that are easy and high-impact.
5. **Migration Risks** — potential issues to watch for.

## Key References

For detailed implementation patterns, read:
- `references/hand-tracking-patterns.md` — 7 ISDK interaction patterns with component references.
- `references/migration-guide.md` — step-by-step controller-to-hands migration checklist.

## Important Notes

- Always maintain controller support as a fallback during migration.
- Consider accessibility — some users may prefer or need controller input.
- Performance matters — hand tracking adds CPU overhead; suggest efficient implementations.
- Test with both left and right hands; don't assume right-hand dominance.
- Hand tracking works best with interactions within arm's reach.

## Field-of-View Readiness (Head-Locked UI)

Run this when preparing the project for a device with a **narrower field of view** than the developer's current target. It finds **head-locked** (HUD) UI that fits a wider FoV but would be clipped at the edges of the narrower device — reticles, health/ammo counters, minimaps, tutorial pins, vignette/letterbox overlays — and reports each with a migration fix. This is a distinct pass from the input workflow above.

### What "FoV bleed" means

In VR nothing is permanently off-screen — the user can turn their head. The genuinely-clipped case is **head-locked** content: UI attached to the camera at a fixed angular offset. If that offset fit the wider FoV but exceeds the narrower device's frustum, it is clipped every frame and can never be brought into view. That is the only class this pass claims to find completely.

### Reliability rule

Compute the geometry; never estimate it. Do not read scene/prefab YAML and do trigonometry on nested transforms in your head. Get **resolved** transforms from the running project — enter Play mode (or a build) and read the live objects — then apply the deterministic frustum test below. The math decides; you classify and suggest.

To reach the game's HUD states and automate this instead of clicking through by hand, drive the running build with **Meta XR Operator** — it can play the project and exercise gameplay states for you, then you inspect the resolved objects at each state. If you can't run and inspect the project live, this pass isn't reliable from static files alone — say so rather than guessing.

### FoV spec source

The frustum test needs both view frusta as tangent half-angles:

- `{ leftTan, rightTan, upTan, downTan }` — target (narrower) device
- `{ leftTan, rightTan, upTan, downTan }` — current device (for the "fit before, not now" delta)

Use the target device's published FoV spec for these values. If you don't have both sets, **skip the FoV pass and say so** — never guess numbers you don't have.

### Procedure

1. Confirm you can run and inspect the project live (for example with Meta XR Operator driving a build) and that you have both frustum param sets. If either is missing, stop and report why.
2. Enumerate head-locked UI candidates: `Canvas` with `renderMode` ScreenSpaceOverlay/ScreenSpaceCamera; any `Canvas`/`RectTransform`/`Renderer` whose transform ancestry passes through the tracked camera / `CenterEyeAnchor` / `OVRCameraRig` center eye; full-screen vignette/letterbox overlays. Exclude world-locked content not parented to the head.
3. For each candidate, get resolved corner world positions and the center-eye camera world transform from the running project — not from YAML.
4. Frustum test (per corner, transformed into eye space, for `z > 0`): `tanX = x/z`, `tanY = y/z`; a corner is inside a device when `-leftTan <= tanX <= rightTan` and `-downTan <= tanY <= upTan`. **Bleed** = at least one corner inside the current device but outside the target device.
5. Report each bleed ordered by severity, noting per-corner margins (degrees past the target edge).

### Severity

- **Critical** — always-visible HUD the player relies on (reticle, health, ammo, objective marker) clipped.
- **Warning** — secondary HUD partially clipped, or a comfort overlay mis-sized for the narrower FoV.
- **Advice** — decorative head-locked element near the edge.

### Migration guidance

- Pull the HUD inward within the target's angular budget; prefer the primary 0–30° zone for must-see HUD.
- Reduce HUD radius / reference distance so the cluster subtends a smaller angle.
- Convert edge HUD to an off-screen indicator (arrow / edge glow) when it must live at the periphery.
- Re-tune vignette / letterbox to the narrower FoV rather than the wider one.
- Avoid simply hiding clipped HUD — relocate it; the information is usually needed.

### Limits (state these in the report)

- Completeness is guaranteed only for head-locked UI — not world-locked content expected to be seen peripherally, nor anything reached only in specific gameplay states.
- First-order model: mono central frustum. Stereo (an element visible to one eye only) and lens-distortion are refinements, not covered.
- If the frustum config was unavailable, say the pass was skipped — never report "no issues found" when it did not run.
