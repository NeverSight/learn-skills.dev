---
name: blender
description: "Automate Blender scenes with the bpy Python API, build Geometry Nodes workflows, configure Cycles or EEVEE renders, and troubleshoot headless batch jobs."
category: 3d
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["blender", "bpy", "python-api", "cycles", "eevee", "geometry-nodes", "headless", "batch-render"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Blender 4.x 3D Creation Suite AI Skill Guide (Claude)

## Overview & Engine Architecture

Blender 4.2 LTS / 4.3+ / 5.x is an open-source DCC suite. Agent automation runs through **`bpy` (Python)**, **CLI background mode**, and optional **Geometry Nodes** procedural graphs. Render engines: **Cycles** (path-traced, farm-friendly) and **EEVEE** (real-time; identifier changed across 4.2→5.0 — resolve at runtime, do not hardcode `BLENDER_EEVEE_NEXT`).

Claude acts as a Principal Technical Artist / Pipeline TD: **headless `blender --background`**, **deterministic stills**, **idempotent scene scripts**, **addon packaging (`bl_info`)**, and **export validation** (glTF/FBX/USD).

```
┌─────────────────────────────────────────────────────────────┐
│                 Blender automation stack                    │
│  bpy.data / RNA  →  depsgraph  →  Cycles|EEVEE  →  files  │
│  CLI: -b blend -P script.py  |  -E CYCLES -f N -a (last!)   │
│  Determinism: cycles.seed, fixed samples, no animated seed  │
└─────────────────────────────────────────────────────────────┘
```

**Version pins (document in every pipeline README):** pin Blender **minor** (e.g. 4.2.11 LTS). GPU backends: CUDA / OPTIX / HIP / ONEAPI / METAL after `--` (see [CLI render docs](https://docs.blender.org/manual/en/latest/advanced/command_line/render.html)).

---

## When to use / when not to

**Use when**

- Batch stills/animations, asset conversion, procedural scene generation, CI smoke renders.
- Geometry Nodes or modifier stacks must be evaluated headlessly.
- You need reproducible Cycles output (golden frames, A/B materials).

**Do not use when**

- Real-time game runtime (use Unity/Godot/Unreal skills).
- Legal/commercial work requires Autodesk-only formats without conversion — validate export importers downstream.
- Host has no GPU and Cycles GPU is mandatory without CPU fallback plan.

---

## Operational Capabilities & Agent Directives

1. **Data API first**: Mutate `bpy.data`, `scene`, object properties; use `bpy.ops` only with explicit context overrides in `--background`.
2. **CLI argument order**: Put `-o`, `-F`, `-E`, frame range **before** `-f`/`-a`; render flags must be **last** or Blender ignores them.
3. **Deterministic Cycles**: Set `scene.cycles.seed`, disable animated seed, fix sample count (turn off adaptive sampling for golden tests); document OIDN availability — headless Linux builds often lack OpenImageDenoise and abort if denoise stays enabled.
4. **Color management**: Set `scene.view_settings.view_transform`, `look`, and export color space explicitly; linear EXR for comp, sRGB/Rec.709 for web stills — never assume default OCIO matches farm workers.
5. **Engine resolution**: `scene.render.engine = bpy.context.preferences.addons['cycles'].preferences...` or iterate `bpy.types.RenderEngine` — EEVEE enum names differ by version.
6. **Exit codes**: Wrap `main()`; on failure `sys.exit(1)` so CI fails; log `blender --version` at job start.

---

## Headless batch: deterministic Cycles still

`render_still.py` — run: `blender -b scene.blend --python render_still.py -- --cycles-device OPTIX`

```python
import bpy
import sys

def main():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "GPU"  # or CPU-only farm
    scene.cycles.samples = 128
    scene.cycles.use_adaptive_sampling = False
    scene.cycles.seed = 42
    scene.cycles.use_animated_seed = False
    # Disable denoise if OIDN missing on worker
    scene.cycles.use_denoising = False
    scene.render.image_settings.file_format = "OPEN_EXR"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.filepath = "//out/frame_####"
    bpy.ops.render.render(write_still=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("BLENDER_PIPELINE_FAIL", e, file=sys.stderr)
        sys.exit(1)
```

**Animation farm split**: render frame ranges per worker (`-s` / `-e`), merge with `bpy.ops.cycles.merge_images` or FFmpeg concat of EXR/PNG sequences.

---

## Export pipelines

| Target | Operator / notes | Pitfalls |
| :--- | :--- | :--- |
| **glTF 2.0** | `bpy.ops.export_scene.gltf` | Apply scale; Draco optional; check NLA vs active action |
| **FBX** | `export_scene.fbx` | Unit scale 0.01 vs 1.0; bone roll |
| **USD** | Blender USD exporter | Instance paths, material binding |
| **Alembic** | Cache transforms/deforms | Frame range, subframe sampling |

Always **apply scale** (or document non-uniform scale) before export; validate in target engine (Unity/Unreal importers).

---

## Failure taxonomy

| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| Black render | No camera/lights/world | Assert `scene.camera`; add key light |
| `context is incorrect` | `bpy.ops` in wrong mode | Data API or `temp_override` |
| `Failed to denoise` | OIDN absent on server | `use_denoising = False` or install OIDN build |
| EEVEE enum not found | Version drift | Query available engines at runtime |
| Non-deterministic noise | Animated seed / adaptive sampling | Fixed seed + fixed samples |
| Washed stills vs viewport | Wrong view transform / display device | Match `view_settings` + file format color space |

Practitioner pattern (r/blenderhelp): background jobs fail silently when `-a` precedes `-o` — reorder CLI.

---

## Essential CLI

```bash
blender --version
blender -b file.blend -E CYCLES -o //renders/frame_#### -F PNG -f 1 -- --cycles-device CPU
blender --factory-startup -b --python tests/smoke_bpy.py
blender -b file.blend -P pipeline/export_gltf.py
```

**Paths (Windows):** `%APPDATA%\Blender Foundation\Blender\<ver>\scripts\addons`

---

## Agent Operational Directive

> **MANDATORY**: Pin Blender version in CI. Set Cycles seed + fixed samples for deterministic output. Put `-f`/`-a` last on CLI. Prefer EXR + documented OCIO for color-critical pipelines. Exit non-zero on pipeline failure.
