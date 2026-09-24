---
name: minimax-h3-comfyui
description: Prepare, validate, submit, monitor, and retrieve MiniMax H3 text-to-video, first/last-frame image-to-video, reference-to-video, and verified 32x32 audio-only workflows on a local or self-hosted ComfyUI instance. Use when a user explicitly asks to run, generate, execute, queue, preview, or fetch MiniMax H3 work through ComfyUI. Uses pinned Comfy-Org templates and bundled Turbo variants, and patches known fields deterministically; it does not adapt arbitrary custom workflows.
---

# MiniMax H3 ComfyUI

Run a finished MiniMax H3 prompt through ComfyUI using bundled T2V, I2V, R2V, or audio-only workflows. Turbo is the default variant; preserve the selected pinned graph unless the user explicitly overrides a declared field.

## Interpret control flags

Recognize these case-insensitive controls anywhere in the request:

For every `<boolean>` below, accept `true`, `on`, `yes`, or `1` as true and `false`, `off`, `no`, or `0` as false.

- `[return=<boolean>]`: wait for completion and fetch results when true; submit and return the `prompt_id` immediately when false. Default true.
- `[prompt_enhance=<boolean>]`, `[pe=<boolean>]`: improve the prompt through the matching MiniMax H3 prompt specialist when true; preserve it when false. Default false.
- `[preview=<boolean>]`: show or hide the ComfyUI browser after loading the prepared workflow. This has no effect when `load_workflow` resolves to false. Default true.
- `[load_workflow=<boolean>]`: replace the live canvas with the prepared workflow when true. When false, stay headless: do not initialize or open a browser, and do not announce preview or canvas behavior. Default false.
- `[turbo=<boolean>]`: use the 6-step MiniMax H3 Turbo LoRA workflow when true; use the original 20-step workflow when false. Default true. In particular, `[turbo=off]`, `[turbo=no]`, and `[turbo=false]` disable Turbo.

Strip control flags before sending text to MiniMax H3. Treat unambiguous natural-language name/value execution settings, such as "use seed 42" or "at 8 sampling steps," as controls and remove only those clauses from the prompt payload. Preserve ambiguous operational wording as prompt text; do not invent a setting from phrases such as "the original sampler."

Match every boolean flag name and value case-insensitively. If the same flag appears more than once, use its last occurrence. Treat any other value as invalid control syntax and stop before workflow preparation.

Without an enhancement flag, treat the prompt as finished: do not silently rewrite, expand, translate, or “improve” it. If enhancement is enabled, load and apply exactly one matching specialist:

- T2V: `../minimax-h3-text-to-video/SKILL.md`
- I2V: `../minimax-h3-frame-to-video/SKILL.md`
- R2V: `../minimax-h3-reference-to-video/SKILL.md`
- Audio only: `../minimax-h3-audio/SKILL.md`

## Select the bundled workflow

- Explicit audio-only output with no controlling media: `assets/workflows/audio-turbo.api.json` by default; `audio.api.json` when Turbo is false. Keep its disposable visual latent fixed at 32x32.
- No controlling media and video output: `assets/workflows/t2v-turbo.api.json` by default; `t2v.api.json` when Turbo is false.
- One literal first frame, or literal first and last frames: `assets/workflows/i2v-turbo.api.json` by default; `i2v.api.json` when Turbo is false.
- Media used for identity, style, motion, camera, performance, voice, music, or rhythm: `assets/workflows/r2v-turbo.api.json` by default; `r2v.api.json` when Turbo is false.

Use the `.api.json` files for validation and execution. Use each variant's matching `.ui.json` file for provenance and browser preview. The Turbo copies preserve the original mode graph while inserting `MiniMaxH3TurboLoRA` after the diffusion loader, replacing the sampler selector with `MiniMaxH3TurboSampler`, and setting `simple` scheduling with 6 steps. Reject arbitrary attached workflow JSON at runtime; custom-workflow adaptation is intentionally deferred.

## Execute the workflow

Read [references/runtime.md](references/runtime.md) before using ComfyUI. Follow it in order:

1. Parse and strip controls, resolve configuration, select the mode and variant, and validate request-derived settings without connecting or uploading. Turbo rejects sampler or scheduler overrides and steps outside 4 through 8; stop before side effects on an invalid setting.
2. Test reachability. A successful default connection check is silent.
3. Resolve installed models and, for Turbo, the custom nodes and Turbo LoRA conservatively; never install or download without explicit permission.
4. Inspect attached assets and upload them through the matching ComfyUI media tool.
5. Run `scripts/prepare_workflow.py` to patch only the manifest-declared fields, then validate the prepared API graph.
6. If explicitly requested, load or preview the matching prepared UI graph.
7. Submit once. Respect the return behavior above. For awaited runs, prefer the live sampler ETA from ComfyUI's log stream to fixed-interval polling, while binding completion and errors to the exact `prompt_id`.
8. On completion, fetch the output audio or video to a temporary or user-selected directory and return it with the `prompt_id`.

Do not submit a workflow while required media, a compatible model choice, or validation errors remain unresolved.

## Preserve selected defaults

Unless explicitly supplied by the user or non-empty configuration, preserve the selected workflow's prompt-independent defaults for resolution, seed, scheduler, steps, denoise, reference sizing, model filenames, Turbo LoRA, and output prefix. Turbo pins its custom sampler, `simple` scheduler, LoRA strength `1.0`, low-VRAM mode off, and 6 steps. A Turbo step override must remain from 4 through 8; disable Turbo to select another sampler or scheduler.

Audio mode is the exception to resolution configuration: it always patches the disposable visual latent to 32x32 and rejects any other explicit size. It accepts no first/last frame or reference media; route reference-controlled sound or voice work to R2V.

Allowed deterministic patches are:

- prompt
- uploaded media filenames and reference connections
- width and height together
- duration, converted to the H3 `17k+5` frame grid at 24 fps
- seed
- compatible model filenames
- compatible Turbo LoRA filename
- output filename prefix
- named sampler and scheduler overrides for the standard workflow
- 4–8 steps and denoise overrides for Turbo, or steps and denoise overrides for the standard workflow
- R2V reference-size overrides

Never patch fields by searching for example text or relying on UI coordinates. Use `assets/workflows/manifest.json` and the preparer script.

## Return a concise execution report

For completed jobs, return the selected mode, relevant settings, `prompt_id`, and fetched audio or video. For asynchronous jobs, return the mode and `prompt_id` plus how to request status or results later. For failures, return the failed node/error, what was checked, and the smallest next action.

Do not claim the job completed merely because it left the queue; confirm its exact history entry or fresh output file.
