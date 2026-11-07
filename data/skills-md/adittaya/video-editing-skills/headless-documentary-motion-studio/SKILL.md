---
name: headless-documentary-motion-studio
description: "A headless studio for building, editing, directing, rendering, inspecting and revising professional documentary video entirely from the terminal. Blender for 3D scenes, cinematography, animation, VFX and rendering; Remotion for 2D motion graphics, typography, charts and compositing; FFmpeg for media processing, assembly and audio; Python for orchestration; MCP where available for structured tool access; vision analysis of rendered frames for iterative quality control. Never depends on a graphical UI. Use for documentary, explainer and motion-graphics work that must be built deterministically and improved by rendering and inspecting."
---

# Headless Documentary Motion Studio

**Scope.** The pack's **headless studio** — an autonomous, terminal-only editor,
motion designer, 3D artist, cinematographer, compositor and post-production
engineer. It builds the video as a **deterministic, editable, machine-readable
project** and improves it by **rendering and visually inspecting** — never by
clicking a UI.

**When to use.** For documentary, explainer and motion-graphics builds — any job
that should be constructed deterministically from a shot list rather than
"generated blindly", and that benefits from a render → inspect → revise loop.

> **THE STUDIO LAW (mandatory).** You are not imitating a human clicking Premiere
> Pro, After Effects or Blender. You are **constructing** the video as a
> reproducible project — JSON + Python + procedural Blender scenes + Remotion
> source — and **improving it through rendering and visual inspection.**

---

## 0 · What it must work WITHOUT

No monitor · no mouse · no keyboard automation · no GUI · no screen coordinates ·
no remote desktop · no interactive Blender viewport · no interactive After Effects
· no interactive Premiere Pro.

Everything runs through: **shell commands · Python · Blender background mode ·
Remotion CLI · FFmpeg · MCP tools (where available) · project files · rendered
images/video · vision analysis.**

## 1 · Core philosophy

**1.1 — Do not generate video blindly.** Never treat text-to-video generation as
the primary solution when a shot can be **constructed deterministically**. Prefer:

```
script -> shot specification -> scene graph -> assets -> camera -> animation
       -> lighting -> render -> visual inspection -> revision -> final render
```

**Do not accept the first render automatically.**

**1.2 — Think in shots, not prompts.** Every documentary is decomposed into
**shots**. Each shot is a production unit with: narrative purpose · duration ·
visual subject · environment · camera · lens · composition · movement · lighting ·
atmosphere · animation · transitions · audio cues · narration relationship ·
visual style · quality requirements.

## 2 · Headless architecture

```
AI Agent
   +-- filesystem
   +-- Python            (orchestration)
   +-- MCP               (structured tool access, where available)
   +-- Blender headless  (3D)
   +-- Remotion          (2D motion graphics)
   +-- FFmpeg            (media)
   +-- asset generators
   +-- vision analysis   (QC of rendered frames)
   +-- audio tools
   v
Final documentary
```

### Responsibilities
- **Blender** (headless, `bpy` — see `BLENDER-ENGINE.md`) — 3D environments, asset
  placement, procedural modelling, imported AI meshes, materials, lighting,
  volumetrics, cameras, camera/object animation, particles, geometry nodes,
  physics, simulations, tracking, 3D typography, scientific visualization,
  historical reconstruction, architectural visualization, 3D compositing, final
  3D rendering.
- **Remotion** (React/CLI) — kinetic typography, captions, lower thirds, charts,
  maps, diagrams, UI animation, data visualization, 2D motion graphics, titles,
  labels, transitions, documentary overlays, procedural graphics.
- **FFmpeg** — assembly, concatenation, trimming, transcoding, audio muxing,
  normalization, frame extraction, proxy generation, thumbnails, intermediate
  formats, final encoding.
- **Python** — project orchestration, scene generation, asset management, shot
  generation, metadata, timeline generation, validation, automation, render
  orchestration, quality checks.
- **Vision analysis** — inspect rendered frames and critique them against the
  shot spec before accepting.

## 3 · Project structure (always prefer a structured project)

```
project/
├── project.json
├── script/        master.md · narration.md · research.json
├── shots/         001.json · 002.json · …
├── scenes/        001_factory/ scene.blend · scene.py
├── assets/        models/ textures/ materials/ references/ maps/ generated/
├── audio/         narration/ music/ ambience/ sfx/
├── remotion/      src/ compositions/ components/
├── renders/       previews/ frames/ shots/ final/
├── qc/            reports/ critiques/
└── final/         master.mp4 · master_prores.mov
```

**Never destroy the source assets or procedural scene files.**

## 4 · Source of truth (reproducibility)

Prefer **JSON + Python + procedural Blender scenes + Remotion source** over
manually edited binary files with no deterministic source. Every generated shot
must be **reproducible from source**. Store: prompts · random seeds (where
supported) · asset identifiers · camera parameters · render settings · animation
settings · version information · style parameters.

## 5 · Shot specification (machine-readable)

Every shot carries a spec. Example:

```json
{
  "id": "shot_014",
  "duration": 6.5,
  "fps": 24,
  "purpose": "Establish the scale of the factory",
  "environment": { "type": "industrial_factory", "era": "1930s", "style": "documentary_realism" },
  "camera": { "lens_mm": 35, "sensor": "full_frame", "movement": "slow_dolly",
              "start": [2.4, -8.1, 2.1], "end": [4.8, -2.0, 3.5], "look_at": "furnace" },
  "lighting": { "style": "industrial", "volumetric": true, "contrast": "medium" },
  "atmosphere": { "smoke": "subtle", "dust": "subtle" },
  "subjects": ["furnace", "workers", "conveyor"],
  "animation": { "workers": "slow_walk", "machinery": "active", "steam": true },
  "audio": { "ambience": "factory_low",
             "events": [ { "time": 4.2, "sound": "metal_impact" } ] }
}
```

## 6 · The loop (run it per shot, then per film)

1. **Specify** — write the shot spec (Section 5) from the script/beats.
2. **Build** — generate the scene (Blender scene.py / Remotion composition) from
   the spec.
3. **Render** — a **preview** first (low-res, few samples), then inspect.
4. **Inspect** — run **vision analysis** on the rendered frames; check the spec
   (framing, lens, movement, lighting, atmosphere, subjects).
5. **Revise** — fix what failed; re-render the preview. **Never accept the first
   render.**
6. **Commit** — once the shot passes, render at final quality; record the seed and
   settings for reproducibility.
7. **Assemble** — FFmpeg concatenates, muxes audio, normalizes, and encodes the
   master (+ ProRes).

## 7 · Quality control

- **Per shot:** spec match, no artifacts, correct camera/lens/movement, lighting
  and atmosphere as specified, audio cues on their times.
- **Per film:** the beat map holds; the narration relationship is right; loudness
  is normalized; colour is consistent; the cut rhythm reads.
- Write **`qc/reports/`** and **`qc/critiques/`**; run the pack's QA gate
  (`edit-qa-validator`, `tools/qa_check.py`) and write `EDIT-QA.md`.

## 8 · Where it sits

- **Blender** — the 3D engine (`BLENDER-ENGINE.md`, `skills/blender-engine`).
- **Remotion** — the 2D motion-graphics engine (`TOOLCHAIN.md`).
- **FFmpeg** — media assembly and encoding.
- **Remote workspace** (`REMOTE-WORKSPACE.md`) — run the heavy work on the GPU.
- **`THINKING-SYSTEM.md`** — how to think; **`ADVANCED-FEATURE-USE-CASES.md`** —
  the feature pass; **`MOTION-UI-STYLE-LIBRARY.md`** / **`UI-STYLE-ENCYCLOPEDIA.md`**
  — the look.

---

## QA GATE
Run `skills/edit-qa-validator` and `tools/qa_check.py` before delivery. Audit the
render against the shot specs, AI-re-think anything weak, revalidate, write
`EDIT-QA.md`.

## HARD LIMITS
- **Terminal only.** No GUI, no monitor, no mouse, no interactive viewport.
- **Construct, don't blindly generate** — prefer a deterministic shot over a
  text-to-video guess.
- **Never accept the first render** — always inspect and revise.
- **Keep the project reproducible** — JSON + Python + procedural scenes + source.
- **Never destroy** the source assets or procedural scene files.
- **Never invent** facts, quotes or history; label every reconstruction.
