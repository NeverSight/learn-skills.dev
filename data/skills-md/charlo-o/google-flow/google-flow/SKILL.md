---
name: google-flow
description: Automate Google Flow through a persistent browser session for authentication, recent-project discovery, local project library management, prompt-driven image or video generation, and existing-image editing. Use when Codex needs to sign into Flow, sync or manage saved Flow project URLs, open an existing Flow project, create images or videos from prompts, attach ingredient images or start/end frames, list project asset edit URLs, or edit an existing Flow image with crop, selection masks, draw masks, text overlays, or prompt-based revisions at https://labs.google/fx/tools/flow.
---

# Google Flow

Drive Google Flow from Codex with a persistent Chrome profile. This skill mirrors the NotebookLM-skill architecture: one wrapper to bootstrap the environment, one authentication manager, one local project library, and one task script that opens Flow, performs a single creation run, and exits.

## Critical Rules

- Always invoke scripts through `python scripts/run.py ...`.
- Check authentication before syncing projects or generating media.
- Prefer `project_manager.py sync` before asking the user for a project URL. Flow exposes recent projects on the signed-in home screen, so scrape that first.
- Treat generation and prompt-based image edits as credit-consuming. Confirm the prompt, model, and number of outputs before running `generate_media.py` or `edit_image.py`.
- Pass absolute local file paths for ingredient images and start/end frames.
- Default to an existing project. Do not auto-create blank projects unless the user explicitly asks for that behavior.

## Core Workflow

1. Check auth:
   `python scripts/run.py auth_manager.py status`
2. If needed, sign in:
   `python scripts/run.py auth_manager.py setup`
3. Sync recent projects from the Flow home screen:
   `python scripts/run.py project_manager.py sync`
4. Choose or activate a project:
   `python scripts/run.py project_manager.py list`
   `python scripts/run.py project_manager.py activate --id PROJECT_ID`
5. Generate media in that project:
   `python scripts/run.py generate_media.py --prompt "..." --mode image --model "Nano Banana 2"`

## Authentication

Use `auth_manager.py` to persist Google Flow login state in the skill-local `data/` directory.

```bash
python scripts/run.py auth_manager.py status
python scripts/run.py auth_manager.py setup
python scripts/run.py auth_manager.py validate
python scripts/run.py auth_manager.py reauth
python scripts/run.py auth_manager.py clear
```

`setup` opens a visible browser and waits for manual Google login. The browser state is stored locally and reused for later runs.

## Project Library

Use `project_manager.py` to maintain a local index of Flow projects.

```bash
python scripts/run.py project_manager.py sync
python scripts/run.py project_manager.py list
python scripts/run.py project_manager.py search --query storyboard
python scripts/run.py project_manager.py activate --id my-project-id
python scripts/run.py project_manager.py assets --id my-project-id --kind image
python scripts/run.py project_manager.py add --url "https://labs.google/fx/tools/flow/project/..." --name "My Project"
python scripts/run.py project_manager.py remove --id my-project-id
```

`sync` is the preferred entrypoint because it scrapes the authenticated Flow landing page and imports the visible recent projects into the local library.

Use `assets` when you need an image edit URL from a project before calling `edit_image.py`.

## Generate Images Or Videos

Create an image:

```bash
python scripts/run.py generate_media.py \
  --project-id my-project-id \
  --mode image \
  --prompt "Editorial portrait of a fox software engineer at a laptop, cinematic studio light" \
  --model "Nano Banana 2" \
  --aspect-ratio landscape \
  --outputs 2
```

Create a video from text:

```bash
python scripts/run.py generate_media.py \
  --project-id my-project-id \
  --mode video \
  --video-mode ingredients \
  --prompt "A handheld tracking shot through a neon market in heavy rain" \
  --model "Veo 3.1 - Fast" \
  --aspect-ratio landscape \
  --outputs 1
```

Create a video with start and end frames:

```bash
python scripts/run.py generate_media.py \
  --project-id my-project-id \
  --mode video \
  --video-mode frames \
  --prompt "The camera slowly pushes in as daylight turns into a moody blue-hour dusk" \
  --start-frame "C:/absolute/path/start.png" \
  --end-frame "C:/absolute/path/end.png" \
  --model "Veo 3.1 - Fast" \
  --outputs 1
```

Attach ingredient images:

```bash
python scripts/run.py generate_media.py \
  --project-id my-project-id \
  --mode video \
  --video-mode ingredients \
  --prompt "Use the uploaded robot and alley references to stage a tense reveal" \
  --ingredient-paths "C:/absolute/path/robot.png" "C:/absolute/path/alley.png" \
  --model "Veo 3.1 - Fast"
```

The script prints a JSON payload with the resolved project URL, chosen settings, and the newly detected asset URL when Flow finishes the run.

## Edit Existing Images

List image assets in the project first:

```bash
python scripts/run.py project_manager.py assets --id my-project-id --kind image
```

Edit the latest image in the active project with a full-image prompt:

```bash
python scripts/run.py edit_image.py \
  --latest-image \
  --tool full \
  --prompt "Turn this into a moody dusk scene with softer rim light" \
  --model "Nano Banana 2" \
  --aspect-ratio portrait
```

Edit a selected rectangular region:

```bash
python scripts/run.py edit_image.py \
  --asset-url "https://labs.google/fx/zh/tools/flow/project/.../edit/..." \
  --tool select-box \
  --box "0.18,0.20,0.55,0.48" \
  --prompt "Replace this window area with rainy neon city lights"
```

Mask an area with a drawn rectangle:

```bash
python scripts/run.py edit_image.py \
  --asset-url "https://labs.google/fx/zh/tools/flow/project/.../edit/..." \
  --tool draw-rect \
  --box "0.12,0.58,0.38,0.86" \
  --prompt "Remove the foreground object and restore the wooden floor"
```

Mask an irregular path with a brush stroke:

```bash
python scripts/run.py edit_image.py \
  --asset-url "https://labs.google/fx/zh/tools/flow/project/.../edit/..." \
  --tool draw-brush \
  --points "0.20,0.62;0.26,0.64;0.31,0.69;0.36,0.75" \
  --prompt "Erase this object and blend the background naturally"
```

Insert a text overlay at a specific point:

```bash
python scripts/run.py edit_image.py \
  --asset-url "https://labs.google/fx/zh/tools/flow/project/.../edit/..." \
  --tool text \
  --point "0.30,0.40" \
  --text-size 24 \
  --text "OPENING SOON"
```

Crop an existing image:

```bash
python scripts/run.py edit_image.py \
  --asset-url "https://labs.google/fx/zh/tools/flow/project/.../edit/..." \
  --tool crop \
  --crop-preset square \
  --box "0.12,0.18,0.82,0.78"
```

For `--box` and `--points`, use normalized coordinates from `0` to `1` relative to the visible image canvas.
Use `--point` the same way for `--tool text`. Text overlays are committed by pressing `Enter` inside Flow; keep `--text` single-line. `--text-size` is optional and maps to Flow's text slider in px.

## Limitations

- SceneBuilder composition is still out of scope.
- Download automation is not included. Use the returned asset URL to open the result in Flow and download it manually if needed.
- Flow UI labels can vary slightly by locale. If selectors drift, review `references/workflow.md` and update `scripts/config.py`.

## References

- UI and workflow notes: `references/workflow.md`
- Main scripts: `scripts/auth_manager.py`, `scripts/project_manager.py`, `scripts/generate_media.py`, `scripts/edit_image.py`
