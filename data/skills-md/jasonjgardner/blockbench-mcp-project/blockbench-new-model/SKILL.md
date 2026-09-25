---
name: blockbench-new-model
description: "Start a new Blockbench model or scene from a short intake form and deliver a render-ready Blender scene. Asks for quality, texture style (PBR 2K/HD/standard, vanilla Minecraft, classic Blockbench), animation (keyframed or Havok physics), scene type (scene, vignette, isometric room), subject, output folder and render preset; builds .bbmodel files with the headless Blockbench MCP server and parallel agents; imports them into Blender; and writes a render.cmd that renders stills on every GPU and assembles them into a video with FFmpeg. Use when the user runs /blockbench-new-model or asks for a new Blockbench model delivered as a rendered Blender scene or video."
argument-hint: "[subject]"
---

# Blockbench New Model

Build a new subject end to end: headless `.bbmodel` authoring, a Blender scene ready to render, and a `render.cmd` that renders PNG stills on every GPU and encodes them with FFmpeg.

Load [blockbench-use](../blockbench-use/SKILL.md) before the first model edit and follow its routing to the domain skills. The form answers settle its appearance-versus-performance question; do not ask it again.

## 1. Intake form

Ask before any building. Use the client's structured question tool (`AskUserQuestion` in Claude Code); without one, send the same questions as one numbered list. Present options in the order shown, without marking a recommendation.

**Round 1: what to build.** Ask all four questions in one call.

| Header | Question | Options (label: description) |
|---|---|---|
| Quality | What quality level? | **High-quality**: detailed silhouette, smooth rounded parts, detail in textures · **Low-poly**: faceted, bold shapes, flat color regions |
| Textures | Which texture style? | **PBR textured**: albedo + normal + MER, resolution asked next · **Vanilla Minecraft**: Minecraft's own 16× textures · **Classic Blockbench**: hand-painted pixel art, no PBR |
| Animation | How should it move? | **Animated**: keyframed clips · **Havok physics**: physics-based motion baked with the Havok plugin in Blockbench desktop |
| Scene | What kind of scene? | **Simple 3D scene**: subject with a few context props · **Complete 3D scene**: full environment with foreground to background · **Simple 3D vignette**: subject on a small diorama base · **3D isometric room**: cutaway room seen from an isometric camera |

**Round 2: details.** Ask only the questions that apply, in one call.

| Header | When | Question | Options |
|---|---|---|---|
| Subject | No argument was given | What is the subject? | Two or three example subjects suited to the round 1 answers; the user types their own through Other |
| Resolution | Textures = PBR | Which PBR resolution? | **2K PBR**: 2048² maps, ~32 px per unit · **HD PBR**: 512–1024² maps, 128–256 px per block · **PBR (standard)**: 16×–32× pixel art with PBR channels |
| Output | Always | Where should the project folder go? | A parent folder the user chose before, if you know one · **Current directory**: `./<slug>/` · anything else through Other |
| Render | Always | Which render preset? | **1080p**: 1920×1080, 30 fps, 10 s · **4K UHD**: 3840×2160, 30 fps, 10 s · **Square loop**: 1080×1080, 30 fps, 6 s seamless loop · **Quick preview**: 1280×720, 24 fps, 5 s |

An argument after the command (`/blockbench-new-model a lighthouse on a sea stack`) is the subject. Derive `<slug>` from it (lowercase, hyphens, ≤ 40 characters). Create `<output>/<slug>/` and refuse to overwrite a folder that already holds a project; offer a numbered slug instead.

Echo the full brief back in one sentence ("A high-quality, 2K PBR textured, animated simple 3D vignette of a lighthouse on a sea stack, 1080p 30 fps 10 s, in …") and continue without waiting for confirmation.

## 2. Preflight

Check everything the answers need before modeling; report all gaps at once.

- **Headless server**: `bbmodel_*` tools are connected. If not, see [setup](references/headless-build.md#setup), give the user the command with their folder filled in, and stop.
- **Preview renders**: `bbmodel_render` needs Node 23.6+ with npm and a GPU; its packages install on first use ([rendering](references/headless-build.md#rendering)). Warn the user about the one-time install, and about `$BB_RENDER_HOME` if C: is short on space.
- **Blender, FFmpeg, GPUs**: locate and probe them as in [find the tools](references/blender-handoff.md#find-the-tools).
- **Havok physics**: Blockbench desktop with the MCP plugin and the Havok Physics Animations plugin (`havok_*` tools after `blockbench_launch`). If unavailable, ask whether to switch to keyframed animation.
- **AI textures (PBR)**: `FAL_KEY` for generated albedo. If missing, note it and paint procedurally.
- **glTF route**: when Blender has no `.bbmodel` importer, Blockbench desktop is needed for glTF export.

## 3. Plan

Write `plan.md` in the project folder: the brief, each answer translated with [option specs](references/option-specs.md) (geometry budget, texel density, texture size, filtering, channels, scene contents, camera and lights, frame range), the part list with real-world sizes, the animation beats per second of the render, and the shot list. Keep it current; subagents read it.

## 4. Build the models

Follow [headless build](references/headless-build.md): layout, build order, verification after each pass, and parallel subagents for complete scenes and rooms. Textures and animation follow the rows in [option specs](references/option-specs.md) for the chosen answers. Share each write tool's `web_app` link with the user as models land.

Gate before Blender: every asset validates, its contact sheet and a posed render look right, and the plan's budgets hold. Havok scenes are baked and saved first.

## 5. Build the Blender scene

Follow [Blender handoff](references/blender-handoff.md): import, run the fix pass, assemble, light and stage cameras for the scene type, apply the render preset, and save `blender/<slug>.blend` from scripts kept in `blender/scripts/`.

## 6. Render deliverable

Copy [render_worker.py](assets/render_worker.py) and [render.cmd](assets/render.cmd) into `render/`, fill the placeholders, and confirm none remain. Render the verification stills, look at them, fix what they show, and time one full-quality frame. Do not start the full render unless the user asks.

## 7. Report

Reply with:

- the project folder, the `.blend`, `render/render.cmd` and the video path it will write;
- the verification stills (send or link them);
- the `web_app` links of the final models;
- GPUs found, seconds per frame, frame count and estimated total render time;
- what was substituted or skipped (no `FAL_KEY`, no Havok, glTF route) and anything unverified.
