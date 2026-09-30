---
name: identity-image-pipeline-guide
description: Teach or plan reliable identity-preserving AI image generation, face swapping, face inpainting, and ComfyUI workflows using InstantID, PuLID, IP-Adapter FaceID, ReActor, InsightFace-style verification, retry/repair loops, and consent/privacy gates. Use when someone asks how to build repeatable image generation with consistent people or automated multi-face identity preservation.
---

# Identity Image Pipeline Guide

Use this skill when the user wants guidance, a build plan, or implementation help
for reliable face swapping, face inpainting, or identity-preserving AI image
generation.

The core answer:

> Do not trust the generation. Generate, detect faces again, compare identity
> embeddings, then retry, repair, reject, or export.

## Pick The Right Track

### 1. Quick Low-Code Demo

Use when the user wants the simplest practical path and does not need fully local
automation.

Recommended flow:

1. Generate the scene image.
2. Use a face-swap or character-swap tool such as Higgsfield.
3. Keep the same high-quality source face or face sheet for repeatability.
4. For multiple people, swap one person at a time when the tool allows it.
5. Manually review every output.

Position this honestly: good for prototypes and low-maintenance demos, not a
guaranteed production-grade identity pipeline.

### 2. Serious Local MVP

Use when the user wants repeatable automation.

Recommended stack:

- Python orchestration layer.
- ComfyUI as the generation engine.
- SDXL or Flux depending on model availability and desired style.
- InstantID, PuLID, or IP-Adapter FaceID for identity-conditioned generation.
- ReActor, FaceDetailer, or inpainting as optional repair/refinement.
- InsightFace-style detection, alignment, and embeddings for identity QA.
- GFPGAN or CodeFormer only as optional restoration, always followed by
  re-verification.

MVP workflow:

1. Collect 3-10 approved reference photos per person.
2. Detect, crop, align, and score each face.
3. Reject weak inputs: too small, blurry, dark, side-facing, occluded, ambiguous,
   or low-confidence.
4. Store accepted crops and identity embeddings in a profile per `person_id`.
5. Generate target images through a pinned ComfyUI workflow.
6. Verify generated faces against intended identity profiles.
7. Retry with adjusted seed/conditioning or run targeted repair.
8. Export only if face count, identity similarity, and quality thresholds pass.
9. Save a score report with the final image.

### 3. Production Pipeline

Use when the user mentions batch generation, no manual retouching, many images,
multiple people, or customer-facing use.

Add:

- versioned workflow templates and model IDs
- target-region or bounding-box hints for multi-person scenes
- deterministic retry/reject policy
- structured score reports
- live smoke tests gated behind local model/runtime configuration
- consent, retention, privacy, and external-sharing policy
- SaaS fallback review for API, cost, data retention, and batch consistency

## Explain The Tool Classes

Separate these categories clearly:

- **Identity-conditioned generation:** InstantID, PuLID, IP-Adapter FaceID. These
  try to preserve identity during generation.
- **Post-generation replacement/repair:** ReActor, FaceDetailer, inpainting,
  Higgsfield-style face swap. Useful, but not sufficient as the whole system.
- **Face analysis and verification:** InsightFace-style detection, alignment, and
  embeddings. This is the QA layer that makes automation credible.
- **Prompt helpers:** ChatGPT or Gemini can help with prompts and scene variants;
  do not position them as identity-preserving tools.

## Multi-Face Rule

Do not rely only on face index ordering such as "face 0" and "face 1." Detection
order changes with framing and scale.

Better approach:

1. Map `person_id` to identity profile and intended template slot.
2. Detect all output faces.
3. Compute embedding similarity for every output face against every intended
   person.
4. Assign identities only when the best assignment clears thresholds and is not
   ambiguous.
5. Repair or reject failed faces individually.

## Weak Reference Photos

Do not blindly "enhance" bad source photos with a generative model. That can make
the face prettier while changing identity.

Use a gate:

- reject face too small
- reject heavy blur
- reject bad lighting
- reject extreme side view
- reject occlusion
- reject multiple ambiguous faces
- reject low detector confidence

If using GFPGAN or CodeFormer, re-run identity verification afterward.

## Safety Boundaries

Always include these when real people are involved:

- Use only with consent.
- Do not commit real face images or raw embeddings.
- Keep live model downloads, SaaS APIs, paid services, and real personal data
  behind an explicit human/live gate.
- Review SaaS tools for privacy, retention, API availability, batch behavior, and
  cost before recommending them for production.

## Repo Plan Entry Point

When working in this repository, use the implementation plan:

- `implementation_plans/identity-image-pipeline/INDEX.md`
- `implementation_plans/identity-image-pipeline/TASK_QUEUE.md`
- `implementation_plans/identity-image-pipeline/OVERNIGHT_P-01_project_scaffold.md`
- `implementation_plans/identity-image-pipeline/OVERNIGHT_P-02_reference_quality.md`
- `implementation_plans/identity-image-pipeline/OVERNIGHT_P-03_identity_profiles.md`
- `implementation_plans/identity-image-pipeline/OVERNIGHT_P-04_comfyui_adapter.md`
- `implementation_plans/identity-image-pipeline/OVERNIGHT_P-05_identity_verification.md`

Check launch readiness with:

```bash
node scripts/implementation-plan-orchestrator-preflight.mjs \
  --plans-root implementation_plans \
  --plan identity-image-pipeline \
  --no-write-state
```

