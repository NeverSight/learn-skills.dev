---
name: scenario-image
description: "Use when generating or editing images with Scenario through MCP: text-to-image, image-to-image, instruction editing, inpainting or outpainting with a mask, background control, aspect ratio or resolution sizing, several outputs per run, or choosing between Scenario image models. Also when a run fails on prompt length, a plan-restricted model, or a reference image that was silently ignored. Keywords: txt2img, img2img, image edit, inpaint, mask, reference image, aspect ratio."
license: MIT
---

# Scenario Image Generation and Editing

## Overview

Scenario runs hundreds of image models, split across `txt2img` (generate from a prompt) and `img2img` (edit, restyle, inpaint, upscale). The loop is the one the `scenario` skill teaches. What breaks image runs is the per-model contract: sizing fields, prompt limits, and reference caps differ between two models that do the same job, so read `model_schema_get` every time. Per-family contracts (sizing families, reference caps, edit modes): `scenario-seedream`, `scenario-gpt-image`, `scenario-gemini-image`, `scenario-ideogram`, `scenario-reve`, `scenario-luma-image`, `scenario-mai-image`, `scenario-grok-imagine-image`. Upscaling, grading, effects, expand, resize and the other tool models: see `scenario-image-editing`. Holding one look across a set: see `scenario-consistency`. Sprites, icons, and tilesets: see `scenario-game-assets`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Need              | Call                                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------------------------ |
| Pick a model      | `recommend` with `capability="txt2img"` or `"img2img"`, or `search` (`target="models"`, `public=true`) |
| Read the contract | `model_schema_get`, before every `model_run`                                                           |
| Estimate cost     | `model_run` with `dry_run=true`; `cost_impact: true` marks the fields that move price                  |
| Generate or edit  | `model_run`, then `jobs_wait`                                                                          |
| Review and save   | `asset_display`, then `asset_download` (`png` default, `webp`, `jpg`)                                  |
| Land exact pixels | Generate at the nearest reachable size, then `model_scenario-resize-image` (see Landing an exact size) |

Inpainting and outpainting are `img2img`, not capabilities of their own.

## The three fields that fail runs

All three are per-model, so take them from the schema rather than from a previous run:

- **Size.** Sizing has no common shape: numeric `width` and `height` with `min`, `max`, and a `step` to land on; an enum (`aspectRatio`, a `resolution` in megapixels or K tiers, a `size` mixing tiers with pixel pairs); or an aspect ratio alone, which puts an exact pixel target out of reach entirely. Pixels sent to an enum field, or an off-step value, are rejected. When the schema cannot express the size asked for, report what it can reach rather than rounding silently.
- **Prompt length.** The prompt field's `max_length` ranges from roughly 2000 characters to 32000. A prompt that fits one model is a 400 on the next.
- **References.** Name (`referenceImages`, `image`), cap, and cardinality all come from the schema, and the name settles none of them: a field called `referenceImages` is a single scalar file on some models. Pass an array only where the schema says `array: true`, and there pass one even for a lone asset, since a bare string is dropped silently and the run then succeeds while ignoring the reference. With several references, say in the prompt which is which.

A batch-count field (`numOutputs`, `numImages`) repeats one prompt, so it yields variations, not a set. Anything with a per-item difference needs one `model_run` per item.

## Landing an exact size

In-game placements need exact pixels (a 210x600 banner, a 256x256 icon), which a generative model may not support directly. Numeric sizing fields snap to a grid (a `step` of 16 is common, with `min` and `max` bounding the range), enum fields offer fixed tiers, and some members silently replace a request below their floor: 512x128 came back as 1408x480 on one member, with no error. When the target is unsupported, generate at the nearest reachable size at or above it, matching the ratio where possible and respecting every schema limit (1024x1024 for a 256x256 icon on a member with a 1K floor; 224x640 for a 210x600 banner only if both dimensions meet that member's limits), then finish with `model_scenario-resize-image`, a fixed id since it is Scenario's single deterministic exact-dimension resize tool and discovery would only re-derive it: `images` as an array even for one asset, `width` and `height`, and `fit` `cover` to fill the box and center-crop the overflow or `stretch` for exact dimensions at the cost of distortion (`contain`, the default, can return a smaller image than the box). Choose a larger source only for an explicit quality requirement or documented model guidance, not an assumed family sweet spot. Confirm with `asset_get`. Downscaling can make softness less visible; resizing upward cannot recover missing detail.

Blur has the same discipline: several members default to a 1K tier with a higher one in the schema, so set the resolution or `quality` tier explicitly for a new generation. To preserve an approved frame, upscale the exact keeper (`scenario-image-editing`); re-running its recipe can change the image. On a custom-trained member, check guidance and step count against its schema and model guidance before increasing them. When outputs feel literal, split the prompt into what is fixed and what the model may invent and say so. Invented details must obey the fixed constraints too (no decorative runes in a text-free brief); `prompt_spark` expands a thin brief into an on-model one before the run.

## Prompt wording

In-image text: quote each string exactly and say where it sits ("the label reads 'NORTH', top center"), keep to a few short strings, and spell a word that keeps mangling letter by letter (NORTH: N, O, R, T, H); unquoted copy gets reworded. Copy that must be letter-perfect (prices, legal lines) is composited with `scenario-text-overlay`, never prompted. A film-still or cinematic prompt, or a ratio written in prose (2.39:1), can bake letterbox bars into the pixels, and an `asset_get` dimension check reads them as picture: ask for full frame edge to edge, no letterboxing, no black bars, and carry the ratio in the sizing field alone. Where skin shows, name its texture (visible pores, fine hairs, a faint highlight) or it tends to come back retouched smooth.

An instruction edit names the change and pins the rest: "put the chair on a sunlit terrace; keep its shape, fabric and shadow exactly", or for text, "change only the headline to 'NORTH', same typeface, size and position". Anything unnamed is open to change.

## Worked example: replacing a label on a product shot

1. `recommend` with `capability="img2img"` and the user's own words as `prompt`. Handle `next_step` as the `scenario` skill directs, and never run a `requires_plan_upgrade` entry.
2. `upload_asset` the product photo, then `upload_asset_complete`, which returns the `asset_id`. Only the inline path under ~100KB skips the second call.
3. `model_schema_get` on the pick: the reference field's name and cap, which sizing family it uses, the prompt `max_length`, and whether a `mask` field exists.
4. For a masked edit, read the `mask` field's own description before building anything. Masks are not interchangeable: one model wants an alpha channel at the source's exact dimensions, another wants a black and white image it resizes itself, and which pixels get painted differs too. With no mask in hand, `recommend` with `capability="img2img"` and the masking need in the user's own words finds segmentation models that take a short noun phrase or a box and return one mask per object; most segmentation models in the catalog segment 3D meshes instead, so check `capabilities` on the pick. Where no convention fits, an instruction editor scopes the edit in prose instead.
5. `model_run` with the schema's own field names: the prompt, the reference (wrapped in an array only where the schema says `array: true`), plus the mask and sizing fields it named. Use `dry_run=true` first when cost matters.
6. `jobs_wait`; its ~180s timeout is not an error, so re-call it with the returned `pending_job_ids` as `job_ids`. Then `asset_display` to review and `asset_download` to save.

## Common mistakes

- Passing a bare string where the schema marks the reference field `array: true`: it is dropped without an error, and the output quietly ignores it.
- Reusing one model's parameter block on another: `aspectRatio` and `width`/`height` rarely coexist, and unknown fields are rejected.
- Retrying a 403 `ModelAccessRestrictedError`: it names `modelId` and `requiredPlan`, so surface the upgrade or pick another model.
- Prompting "transparent background": diffusion outputs are opaque. Use a `background` field when the schema has one, otherwise run a background-removal model afterwards.
- Re-running an approved frame at a higher size tier and expecting it back sharper: many models expose no `seed`, and where one exists it reproduces a run only with every other field unchanged, so the re-run is a new image; draft at the cheapest tier, then upscale the exact keeper (`scenario-image-editing`).
- Assuming a model can hit a requested pixel size: some expose an aspect ratio and nothing else, and others silently substitute a size for one below their floor. Generate near, then resize (Landing an exact size), and confirm what landed with `asset_get`, which reports `properties.width` and `properties.height`; `jobs_wait` returns asset ids only.
