---
name: mascot-pack
description: Package a mascot master and optional pose/expression variants into social media images, sticker exports, print-ready PNGs, web responsive images, README documentation, and a zip bundle.
---

# Mascot Pack

Use this skill when the user has a mascot PNG or `mascot-creator` output directory and wants ready-to-use deliverables for social, stickers, print, or web.

## CLI

```bash
.venv/bin/python skills/mascot-pack/scripts/pack.py \
  --master output/happy-fox/master.png \
  --variants-dir output/happy-fox \
  --targets social,stickers,print,web \
  --mascot-name happy-fox
```

No OpenRouter request is made. This is local image packaging only.

## Output

The run folder contains `master/`, optional target folders, variant grids, `README.md`, `metadata.json`, and a zip unless `--no-zip` is passed.
