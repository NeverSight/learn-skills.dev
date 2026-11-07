---
name: director-gate-check
description: Evaluate a motion graphics project against director quality gates before rendering or final delivery. Use when checking stage completion, verifying quality criteria, auditing director sign-offs, or preparing for client handoff.
---

# Director Gate Check

Evaluates the active project against formal Studio Director Quality Gates before advancing to subsequent production phases or delivering final renders.

## The Five Studio Director Gates

1. **Gate 1: Creative Director Gate (Concept and Storyboard)**
   - Clear hook defined within the first 2 seconds.
   - Core visual metaphor or continuous thread locked in beat sheet.
   - Script word count matched to target runtime at natural cadence.

2. **Gate 2: Technical Director Gate (Pipeline and Render Architecture)**
   - Target resolution, frame rate, and renderer chosen (HyperFrames, Blender, or OpenCV).
   - Asset manifest validated with zero missing fonts, audio stems, or cutouts.
   - Render duration and memory budget verified.

3. **Gate 3: Art Director Gate (Motion Bible and Visual Taste)**
   - Motion Bible established with locked color palette, font weights, and easing equations.
   - Contact shadows and bevelled edges confirmed for physical props.
   - Zero AI slop, zero generic floating objects, zero cheap glows.

4. **Gate 4: Audio Director Gate (Sound Design and Loudness)**
   - Frame-synchronized tactile foley mapped to every visible action.
   - Master loudness verified at -14.0 LUFS and true peak under -1.25 dBTP.
   - Hero impact allocated 60ms of clean acoustic silence.

5. **Gate 5: Platform QA Gate (Safe Zones and Multi-Aspect Delivery)**
   - 9:16 vertical text positioned between 170px and 1330px from top.
   - Zero button occlusion confirmed via safe zone test overlay frame.
   - Clean ProRes 4444 MOV and MP4 master files verified.

## Running the Gate Evaluation

```bash
bash tools/scripts/gate-check.sh
```

## Further Reading

- [references/director-gates-rubric.md](references/director-gates-rubric.md) for detailed scoring criteria.
