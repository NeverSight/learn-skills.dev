---
name: raw-photo-lightroom-preset
description: Use for RAW photo culling, Lightroom Classic or Camera Raw editing, reference-style matching, closed-loop Lightroom MCP adjustments, lighting-cluster preset creation, XMP fallback generation, NEF/DNG/TIFF preview workflows, or Chinese requests about matching previous edits. Prefer Lightroom-rendered before/after feedback when Lightroom MCP tools are available.
---

# RAW Photo Lightroom Preset v2

## Core rules

- Judge color only from RAW files rendered by Lightroom/Camera Raw. Use ordinary camera JPGs only for composition, focus, and expression triage.
- Preserve originals and the user's master edit. Do not move, rename, delete, overwrite, or batch-edit photos unless the user asks.
- Treat a preset as a reusable starting point, not a finished edit.
- Separate technical correction from creative style. Never guess 30-50 sliders at once.
- Prefer a closed loop: inspect Lightroom state, render, adjust a small pass, render again, compare, then continue.
- Do not claim Lightroom import, visual fidelity, or manual QA passed unless it was actually performed.

## Choose the route

1. Read `references/workflow.md` for every shoot.
2. Read `references/style-library.md` before choosing a style or reference direction.
3. If Lightroom MCP tools are available and Lightroom Classic is running, also read `references/lightroom-mcp.md` and use the closed-loop route.
4. Otherwise use Lightroom/Camera Raw neutral previews and the manual-preview route. State that Lightroom-side feedback is unavailable.
5. If provenance is missing or ambiguous, stop color work and mark the affected item `未分類`.

## Closed-loop route

Use one representative RAW per lighting cluster first.

1. Capture the current photo metadata and develop settings.
2. If the user has an approved historical look, list presets and read it with `get_develop_preset`. Use UUID or folder/scope to avoid duplicate-name ambiguity.
3. Export a baseline JPEG from Lightroom into a new empty review folder.
4. Apply one bounded pass at a time:
   - technical correction;
   - tonal shape;
   - color correction;
   - creative look;
   - detail/noise.
5. Export and inspect after each pass. Compare against the baseline and any user-approved reference image.
6. When the fork tools are available, create uniquely versioned checkpoints with `create_develop_preset` and diff them against the approved look with `compare_develop_presets`.
7. Keep a checkpoint log of settings and rendered files. Stop when the remaining difference needs masks, crop, healing, AI Denoise, or subjective user choice.
8. Ask for approval on representative before/after results before copying settings across a cluster.
9. Export an accepted custom/checkpoint preset with `export_develop_preset`; never overwrite an existing destination. Import it into Lightroom before claiming compatibility. Use Lightroom's UI for a visible canonical preset when needed. The bundled generator remains a fallback for a verified global-setting subset.

## Manual-preview route

Require Lightroom/Camera Raw exports with recorded provenance. Classify lighting clusters, choose representative files, propose style direction, and get user agreement before generating presets. Keep exposure, white balance, skin, local edits, and denoise as per-image follow-up unless the evidence supports a shared adjustment.

## Safe XMP fallback

Use `scripts/generate_xmp_preset.py` only after style direction is agreed:

```powershell
python scripts/generate_xmp_preset.py --list-styles
python scripts/generate_xmp_preset.py --list-modifiers
python scripts/generate_xmp_preset.py --style graduation-bright-natural --name "Graduation Bright Natural" --output "Graduation_Bright_Natural.xmp"
python scripts/generate_xmp_preset.py --style graduation-documentary --modifier low-light-noise-controlled --name "Graduation Documentary Low Light" --output "Graduation_Documentary_Low_Light.xmp"
```

The generator:

- accepts only `.xmp` output;
- refuses existing output unless `--force` is explicit;
- refuses paths that look like RAW/JPG sidecar XMP files, even with `--force`;
- writes atomically;
- validates known Camera Raw keys, types, and ranges;
- emits point curves as RDF sequences;
- omits Profile, White Balance, and lens settings unless explicitly requested;
- uses ASCII metadata by default; use `--allow-unicode-metadata` only when the target Lightroom setup has been tested.

Use `--unsafe-set KEY=VALUE` only for controlled research against a Lightroom-exported golden fixture. Never use it for routine delivery.

## Validation levels

Report these separately:

- `Parser-level`: XML is well formed.
- `Generator-level`: CLI, safety checks, schema validation, and tests pass.
- `Lightroom import-level`: the target Lightroom version imports the XMP and exposes the expected fields.
- `Visual fidelity-level`: Lightroom-rendered output matches the intended/reference look.

Only the last two require real Lightroom validation.
