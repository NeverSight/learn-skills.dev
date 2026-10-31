---
name: vfx-review
description: Independently score one rendered game VFX filmstrip against a fixed rubric and return a JSON verdict. Use when asked to review, score or judge an effect's strip images (for example from the effekseer-vfx skill's `vfx review`) as a reviewer who did not author it.
license: MIT
metadata:
  version: "0.2.0"
---

# Independent VFX review

You are the reviewer, not the author. Judge only what is visible in the images you are given. Do not open, read or
ask for the recipe code, the brief's intentions or the author's notes; a design sentence from the manifest is context,
not evidence.

## Inputs you should receive

Usually one brief file written by `vfx review-handoff` (`vfx/work/handoff/<evidence_id>.md`) that lists everything
below and the `report_file` path to write your JSON to. Otherwise:

- the whole-timeline strip `vfx/previews/strips/<ID>.png` and the key-frame sheet (paths from `vfx review`);
  optionally `<ID>_compare.png` (previous round above, current below) and a `--bright` strip;
- the effect's manifest entry: `id`, `category`, `element`, `duration`, `peak`, `impact`, `delivery`, `design`;
- its review `flags`;
- the evidence ID of the capture.

Open every image with your image-viewing tool. Tiles are labelled with absolute frame numbers at 60 FPS from the
effect's own start. If you need full-size frames, ask the author to run `vfx frames <evidence_id> <frames...>` and
give you the paths (or run it yourself if you have the skill installed). If an image is missing, say so — do not score
from flags.

## Rubric

Score each criterion 0–3: **0** missing or wrong · **1** present but weak, a player would not notice it · **2** clearly
works · **3** reads instantly and has a distinct identity.

| id | Question | Look at |
|---|---|---|
| `read` | From the first lit tile alone, can you tell what the effect is (hit, slash, element, buff...)? | first 2–3 lit tiles |
| `timing` | Anticipation → contact → body → secondary → dissipation (or the slow fade-in / inward build for heals, buffs and charges)? Is the contact the brightest moment and only 2–5 frames? | tile labels against manifest `peak` |
| `layering` | At the strongest tile: a white-hot core, a saturated body and a darker rim or residue, not one flat colour? | peak tile; bright strip if provided |
| `shape_change` | Does the main shape erode, sweep or distort over time, or only scale and fade like a sticker? | the main shape across consecutive tiles |
| `motion` | Do secondary particles burst fast then slow, and move as the element should (fire up, ice falls, dark draws in, holy descends or rises)? | secondary particles across tiles |
| `placement` | Do arcs, columns and ground decals sit on or under the dummy rather than beside it or floating? | all tiles |
| `tail` | Does the last third still show deliberate dissipation, or is it empty or cut off? | last third of the strip |
| `identity` | Would it be distinguishable from other effects of the same category if recoloured grey? | whole strip |
| `coherence` | Do all layers speak one visual language (one palette family, one shape language, one motion vocabulary), with no layer that looks borrowed from another effect? | whole strip |

The authoritative copy is `vfx rubric` (from `assets/review_rubric.json` of the effekseer-vfx skill); if it differs
from this table, follow it.

Purpose exceptions: heals, shields and buffs need no attack-style white flash; charges build inward before one
release; a projectile strip ends at arrival and does not include its impact.

## Output

Return exactly one JSON object and save it where the author asks (for example `report.json`):

```json
{"id": "VFX_Fire_Explosion",
 "scores": {"read": 2, "timing": 3, "layering": 3, "shape_change": 2, "motion": 3, "placement": 3, "tail": 2, "identity": 3, "coherence": 3},
 "worst": "shape_change",
 "fix": "From f18 to f30 let the main fire layer burn a large gap open on one side so the round outline breaks up.",
 "verdict": "ship",
 "observed_frames": [1, 4, 9, 10, 12, 18, 30, 42, 54, 72]}
```

Rules:
- Every criterion gets an integer 0–3. `worst` names a lowest-scoring criterion.
- `verdict` is `iterate` if any score is below 2, otherwise `ship`.
- `fix` is **one** concrete change for the worst criterion in recipe terms (which layer, timing, texture or motion),
  naming frames. One fix only: each iteration round changes one class of problem.
- `observed_frames` lists the frame labels you actually looked at.

Save it to the `report_file` named in the brief (or where the author asks), then reply with your scores, verdict and
fix. The author then runs `vfx review-submit <evidence_id> <report_file> --reviewer <your reviewer id>`.
Your reviewer id is whatever the host uses to identify you (subagent name or session id); never `author` or `self`.
