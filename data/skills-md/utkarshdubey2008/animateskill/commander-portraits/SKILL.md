---
name: commander-portraits
description: >
  Turn a user-supplied square portrait into a circular crop and place it beside that
  commander's army. Use for kings, generals, Chandragupta, Seleucus, and other named figures.
  Coins, sculptures, or labeled reconstructions only. Never add audio.
---

# Commander portraits

## Overview

A named person is a circle with a clean border, placed on the home side of their army box. The picture comes from a square image the user supplies. The crop keeps the center of that square.

## When to use

Use when the plan names a king, a general, or another person who should be on the map.

## Steps

1. Read `docs/house-rules.md` and `docs/placement.md`.
2. Collect the user's square images. Store them at `assets/portraits/<slug>.png`.
3. Crop each one:

```bash
python3 skills/commander-portraits/scripts/circular_crop.py \
  assets/portraits/<slug>.png \
  assets/portraits/<slug>-circle.png \
  --border "#c4a46a" \
  --size 256
```

The `--border` hex is that empire's color.

4. Set the marker `role` to `person`, `image` to the cropped file, `attach` to that side's army id, and `offset` so the circle sits just outside the box on the home side.
5. Set `detail` to `coin`, `sculpture`, or `artistic reconstruction`. If the file is missing, leave `image` null and set `detail` to `portrait not supplied`. Draw initials in the circle. Do not generate a face.
6. The circle follows the army's motion because of `attach`. Do not give the person a second motion.
7. Implement circular image markers in `hde/frame.py` when the film uses an image. A plain dot is not the delivered portrait.

## Checks

- Every named commander in the script has a circle.
- The circle does not cover the unit symbols or the subtitle.
- A reconstruction is labeled. A missing file is labeled `portrait not supplied`.
- No audio is added to present the portrait.

## See also

- `skills/commander-portraits/scripts/circular_crop.py`
- `docs/scene-contract.md`
