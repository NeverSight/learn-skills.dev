---
name: minimax-h3-frame-to-video
description: Create, enhance, or diagnose MiniMax H3 first-frame and first/last-frame animation prompts when supplied images are literal opening or closing frames. Use for animating posters, key art, portraits, UI mockups, product stills, or controlled transitions that must begin from one exact image or travel between two exact images while preserving composition, identity, geometry, and continuity.
---

# MiniMax H3 Frame to Video

Direct motion from an exact first frame, optionally landing on an exact last frame. Stay prompt-only and never submit a generation job.

## Confirm this workflow

Use this skill when the image is the actual first frame, not merely a style or identity reference. With two images, require the first to be the opening frame and the second to be the closing frame. Otherwise route to `../minimax-h3-reference-to-video/SKILL.md`.

Recommend a 5–15 second clip, `768P` for iteration or `2K` for a final pass when the active workflow and hardware support it, and note that output aspect ratio should follow the first-frame image.

## Build the motion bridge

1. State whether there is one first frame or a first/last pair.
2. Inventory visual invariants visible in the supplied frame: identity, object design, layout, lighting direction, text, and geometry.
3. Describe what begins moving, in what order, and how strongly.
4. Direct camera movement without contradicting the fixed starting composition.
5. With a last frame, describe a continuous causal path that naturally reaches it.
6. Add sound events and timing when useful.
7. Prohibit abrupt morphing, unmotivated cuts, duplicated elements, identity redesign, or geometry drift when those are likely risks.

Do not spend the prompt redescribing every pixel in supplied frames. Spend words on motion, continuity, timing, and controlled change. Do not introduce an intermediate event that makes the final frame physically or spatially impossible.

## Enhance or diagnose

When enhancing, preserve explicit transition ideas and exact on-screen text. Clarify motion order, camera path, how typography or UI appears, and the final settle.

When diagnosing, test for:

- treating the two frames as unrelated scene descriptions;
- a camera path that cannot land on the last composition;
- no preservation instructions for identity, layout, or text;
- too many simultaneous transformations;
- a requested cut in what should be a seamless transition;
- input frames with incompatible geometry that require an acknowledged bridge.

## Use the template and examples

Read [references/template-and-examples.md](references/template-and-examples.md) for the canonical fill-in template and two representative examples. Adapt their motion logic, not their visual subject matter.

## Return

Provide:

- input-frame roles and suggested duration, resolution, and workflow route;
- material assumptions, if any;
- one copy-ready prompt;
- 2–4 continuity checks.

Do not return an API payload or submit a job.
