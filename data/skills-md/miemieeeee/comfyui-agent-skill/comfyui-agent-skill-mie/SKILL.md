---
name: comfyui-agent-skill-mie
description: >
  Agent skill for running registered ComfyUI workflows through a stable CLI.
  Supports image, video, music, and speech generation on a local or trusted self-hosted
  ComfyUI server (default http://127.0.0.1:8188). Registered workflows only.
---

# comfyui-agent-skill-mie

## Purpose

Run registered ComfyUI workflows through a stable Agent-facing CLI, with prompt enhancement, fail-fast errors, and structured JSON results.


Use this skill when the user asks to:

- Generate an image from text.
- Generate a new image inspired by a reference image.
- Edit an input image while preserving some structure or subject details.
- Generate text-to-video or image-to-video MP4 output.
- Generate music / instrumental / song-style MP3 output.
- Synthesize spoken voice audio with Qwen3-TTS.
- Check whether a ComfyUI server is available.

Do not use this skill when the user only wants prompt writing, brainstorming, or discussion without actual generation. Do not use it when the ComfyUI server is unavailable.

## Hard Rules

- Source mode: run CLI commands from the skill root (the directory containing `SKILL.md` and `scripts/`).
- Tool-install mode: `comfyui-agent-skill-mie` / `comfyui-skill` can be run from any directory.
- Source mode: use `uv run --no-sync python -m comfyui` (or `uv run --no-sync comfyui-skill`) for runtime calls.
- Tool-install mode: use `comfyui-skill` (or `comfyui-agent-skill-mie`) directly; do not wrap with `uv run`.
- Use registered workflows only. Do not run arbitrary unreviewed ComfyUI workflow JSON.
- If server health fails, stop generation and return/handle `SERVER_UNAVAILABLE`; do not search disk for ComfyUI installs or guess ports.
- Do not create or edit `config.local.json` unless the user explicitly wants a persistent server URL. For one-off runs, use `--server` or `COMFYUI_URL`.
- For `reference_to_image`, inspect the reference image with Agent vision and create a prompt. Do not upload that reference image to ComfyUI.
- For `image_to_image` and `image_to_video`, upload the provided local image with `--image`.
- Analyzer-generated workflow configs require human review before activation.

## Workflow Selection Policy

- Built-in defaults are fallback choices, not hard requirements.
- If another registered workflow is a stronger semantic match for the request, prefer the stronger match.
- Use workflow capability metadata and workflow selection guidance to choose among registered workflows.
- Any automatic workflow selection in the CLI is only a low-risk fallback when no explicit workflow has been chosen.
- If multiple workflows appear suitable and the user’s preference is ambiguous, ask a brief clarifying question.

## User-Added Workflows

- Users may add custom workflows that were first validated in ComfyUI, then imported into the skill as reviewed registered capabilities.
- Do not execute arbitrary raw workflow JSON directly.
- Import the workflow, generate/review the config template, and activate it only after a reviewed `workflow.config.json` exists.
- User-added workflows must be stored in the per-user workflow registry so skill upgrades do not overwrite them.
- Once activated, user-added workflows may be selected like other registered workflows when they are a stronger semantic match and required inputs are available.
- `import-workflow` only accepts **API format** (ComfyUI's *Save (API)* button, requires *Settings → Enable Dev mode options*). A plain *Save* product (UI/Save format, `{nodes, links}`) is refused with `WORKFLOW_NOT_API_FORMAT`. To convert existing UI/Save workflows in place, run `convert-ui` (needs a running ComfyUI + Playwright).

## Setup

Recommended install (tool-install mode):

```bash
pipx install comfyui-agent-skill-mie
```

- Install package: `comfyui-agent-skill-mie`
- Main command: `comfyui-agent-skill-mie`
- Short alias: `comfyui-skill`

Prerequisites:

- ComfyUI server with `GET /system_stats` available.
- Python 3.10+.
- Source mode only: `uv`.
- Required ComfyUI models/custom nodes for the selected workflow.

Networking note:

- Default local examples use `http://127.0.0.1:8188` for same-environment setups.
- If the agent runs inside WSL/container/sandbox while ComfyUI runs on the host OS, `127.0.0.1` may refer to the runtime itself. Try `--server http://localhost:8188` or the host machine IP (and optionally persist it via `save-server`).

Initial setup from the skill root:

```bash
uv sync
uv run --no-sync python -m comfyui --help
```

Tool-install mode:

```bash
comfyui-agent-skill-mie --help
comfyui-agent-skill-mie check
comfyui-skill --help
comfyui-skill check
```

## Quick Workflow Choice

Minimal decision tree:

- User gives text only → start from general T2I (`z_image_turbo` fallback), but prefer a stronger registered match when workflow guidance indicates one (e.g. posters / anime / artistic styles).
- Poster / text-in-image requests → prefer `qwen_image_2512_4step`
- Anime / manga / illustration style → prefer `anima_turbo`
- Artistic / painterly realism / concept art / product → prefer `krea2_turbo`
- User gives a reference image and wants a new similar image → vision → `reference_to_image` prompt → run `z_image_turbo`
- User gives an input image and wants edits → `generate --workflow klein_edit --image input_image=... -p "..."`
- User wants to mask / cut out an object by describing it → `sam3_mat_image`
- User wants face/expression transfer (face photo + driving video) → `liveportrait`
- User wants TTS / voice audio → `generate --workflow qwen3_tts --speech-text "..." --instruct "..."`
- User wants to clone a specific voice from a sample → `qwen3_tts_clone`
- User wants video → `ltx_23_t2v_distill` (text→video) or `ltx_23_i2v_distilled` (image→video)

| User intent | Workflow / mode | Required command shape |
|-------------|-----------------|------------------------|
| Text to image (general fallback) | `z_image_turbo` | `generate -p "prompt"` |
| Poster / embedded text (preferred) | `qwen_image_2512_4step` | `generate --workflow qwen_image_2512_4step -p "prompt"` |
| Anime / manga / illustration | `anima_turbo` | `generate --workflow anima_turbo -p "prompt"` |
| Artistic / painterly / concept art | `krea2_turbo` | `generate --workflow krea2_turbo -p "prompt"` |
| Similar image from reference | Agent vision + T2I | Read reference image, create English prompt, then T2I |
| Edit image | `klein_edit` | `generate --workflow klein_edit --image input_image=photo.png -p "edit prompt"` |
| Mask / cut out an object (text-driven) | `sam3_mat_image` | `generate --workflow sam3_mat_image --image photo.png -p "the cat"` |
| Face/expression transfer (photo + video) | `liveportrait` | `generate --workflow liveportrait --image face.png --video drive.mp4` |
| Text to video | `ltx_23_t2v_distill` | `generate --workflow ltx_23_t2v_distill -p "shot prompt"` |
| Image to video | `ltx_23_i2v_distilled` | `generate --workflow ltx_23_i2v_distilled --image input_image=photo.png -p "motion prompt"` |
| Text to music | `ace_step_15_music` | `generate --workflow ace_step_15_music -p "music tags"` |
| Text to speech | `qwen3_tts` | `generate --workflow qwen3_tts --speech-text "..." --instruct "..."` |
| Voice cloning (from a sample) | `qwen3_tts_clone` | `generate --workflow qwen3_tts_clone -p "new text" --text-input "ref_text=..." --audio sample.mp3` |

For workflow-specific size rules, capability boundaries, and examples, read [references/workflows.md](references/workflows.md).

## Core Commands

Environment doctor (check server + preflight registered workflows):

Tool-install mode:

```bash
comfyui-skill doctor
```

Source mode:

```bash
uv run --no-sync python -m comfyui doctor
```

If it exits with code 0, the environment is ready for all checked workflows. Exit code 1 means missing nodes/models or server is unreachable (see JSON payload).

Health check:

```bash
uv run --no-sync python -m comfyui check
```

Tool-install mode:

```bash
comfyui-skill check
```

Generate an image:

```bash
uv run --no-sync python -m comfyui generate -p "a cute cat sitting on a windowsill at golden hour"
```

Tool-install mode:

```bash
comfyui-skill generate -p "a cute cat sitting on a windowsill at golden hour"
```

Generate with a specific workflow and server:

```bash
uv run --no-sync python -m comfyui generate --workflow z_image_turbo --server http://192.168.1.100:8188 -p "a landscape"
```

Save a persistent server URL only when the user asks for it:

```bash
uv run --no-sync python -m comfyui save-server http://192.168.1.100:8188
```

Preflight a workflow before a long run:

```bash
uv run --no-sync python -m comfyui generate --workflow qwen_image_2512_4step --preflight
```

Show progress for long jobs:

```bash
uv run --no-sync python -m comfyui generate --workflow ltx_23_t2v_distill -p "cinematic waves at sunset, slow pan" --progress
```

Convert UI/Save workflows to API format (opt-in; needs a running ComfyUI + Playwright, does not run inference):

```bash
uv run --no-sync python -m comfyui convert-ui path/to/ui_workflow.json --server http://127.0.0.1:8188
uv run --no-sync python -m comfyui convert-ui path/to/workflows_dir -o api_workflows/
```

Full CLI options, output path behavior, async submit/poll, and error code details are in [references/cli.md](references/cli.md).

## Prompt Enhancement

Before generation, convert the user's intent into the right workflow inputs.

| Type | Read this file | Use when |
|------|----------------|----------|
| `character` | [references/prompt_enhancement/character.md](references/prompt_enhancement/character.md) | Portrait, person, character, figure photo |
| `reference_to_image` | [references/prompt_enhancement/reference_to_image.md](references/prompt_enhancement/reference_to_image.md) | User provides a reference image and wants a new similar image |
| `image_to_image` | [references/prompt_enhancement/image_to_image.md](references/prompt_enhancement/image_to_image.md) | User provides an input image and wants to edit it |
| `text_to_speech` | [references/prompt_enhancement/text_to_speech.md](references/prompt_enhancement/text_to_speech.md) | User gives a short voice description and needs full Qwen3-TTS instruction |

Reference-to-image flow:

1. Ensure a usable reference image exists; otherwise return Agent error `NO_REFERENCE_IMAGE`.
2. Ensure this runtime can inspect images; otherwise return Agent error `VISION_UNAVAILABLE`.
3. Read the reference prompt enhancement file and create one English prompt.
4. Call T2I generation with that prompt. Do not pass the reference image to ComfyUI.

Image-to-image flow:

1. Ensure a local image path is available.
2. Read the image edit prompt enhancement file.
3. Call `klein_edit` with `--image input_image=path`.

Text-to-speech flow:

1. Split user intent into spoken content and voice/style instruction.
2. Read the TTS prompt enhancement file.
3. Call `qwen3_tts` with `--speech-text` and `--instruct`; do not use positional prompt.

## Fail-Fast and Recovery

CLI failures are structured JSON on stdout. Agent-only pre-check failures for reference images should also be JSON.

Agent-only error shape:

```json
{
  "source": "agent",
  "success": false,
  "error": {"code": "VISION_UNAVAILABLE", "message": "Cannot read reference image in this runtime."}
}
```

Required fail-fast behavior:

- Missing prompt: return/handle `EMPTY_PROMPT`.
- Unregistered workflow: return/handle `WORKFLOW_NOT_REGISTERED`.
- Server unavailable: return/handle `SERVER_UNAVAILABLE` and ask whether ComfyUI is running locally or on another machine.
- Missing reference image before `reference_to_image`: return Agent error `NO_REFERENCE_IMAGE`; do not call CLI.
- No vision for `reference_to_image`: return Agent error `VISION_UNAVAILABLE`; do not call CLI.
- Missing image for image workflows: return/handle `NO_INPUT_IMAGE` or `INPUT_IMAGE_NOT_FOUND`.
- Missing custom nodes/models during preflight: return/handle `PREFLIGHT_MISSING_NODES` or `PREFLIGHT_MISSING_MODELS`.

When the user provides a remote ComfyUI address, save it only if they want persistence:

```bash
uv run --no-sync python -m comfyui save-server http://<address>:<port>
```

Otherwise retry the original command with `--server http://<address>:<port>`.

## Output Handling

After successful generation, present the result to the user. Do not silently parse JSON and stop.

- For images, display the file when the runtime supports local image display; otherwise provide the absolute/local path from `outputs[].path`.
- For MP3/MP4, provide the path or use the runtime's media display/playback capability when available.
- Prefer omitting `--output`; the CLI writes to a per-job directory under `results/` and returns exact paths in JSON.
- For `--count > 1`, parse the wrapper object and present each result.

See [references/cli.md](references/cli.md) for JSON schemas and output directory rules.

## References

- [references/workflows.md](references/workflows.md) — workflow selection, capabilities, size rules, examples.
- [references/cli.md](references/cli.md) — CLI contract, async jobs, output paths, JSON schemas, error codes.
- `references/prompt_enhancement/` — prompt enhancement instructions.
