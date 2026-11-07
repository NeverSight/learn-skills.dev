---
name: icon-creator
description: Generate a single icon, app icon, favicon, UI icon, or logo-mark from a text description.
---

# icon-creator

Use this skill when the user asks to create an icon, app icon, favicon, UI icon, or logo-mark.

## How to invoke

Prefer the top-level wrapper:

```bash
icon-skills estimate icon --variants 3
icon-skills create-icon --description "<user's description>"
```

Direct script equivalent:

```bash
python skills/icon-creator/scripts/generate.py --description "<user's description>"
```

Optional arguments:

- `--output-dir <path>`: output root, default `output`
- `--provider <provider>`: image provider override, one of `openrouter`, `openai`, or `google`
- `--model <model-id>`: provider model override; if omitted, use config, then the preset default
- `--style-preset <preset>`: one of `flat`, `gradient`, `glass-morphism`, `outline`, `3d-isometric`, `skeuomorphic`, `neumorphic`, `material`, `ios-style`
- `--colors <hex,hex>`: comma-separated palette to steer the output
- `--reference-image <path>`: PNG/JPG reference used for palette and style hints
- `--variants <n>`: number of candidates to generate and validate, default `3`, supported range `1-6`
- `--seed <n>`: optional base seed; variants use incrementing seeds when the provider supports it
- `--refine <path>`: previous `master.png` or variant to use as an image reference for iteration

The script prints the path to the selected `master.png` on the last line of stdout. Each run also writes `preview.png`, all candidate files in `variants/`, and validation results in `metadata.json`.

## Workflow

1. If the user did not specify style, choose `flat` for UI icons and `gradient` or `3d-isometric` for app icons.
2. For quick tests, use `--variants 1`; for real selection, use `--variants 3`.
3. Before live generation, use `icon-skills estimate icon`.
4. Return the selected `master.png` path and the run directory.
5. If the user asks for platform assets, run `icon-skills create-app-icon-pack --master <master.png>`.
