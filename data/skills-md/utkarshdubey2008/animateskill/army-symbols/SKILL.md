---
name: army-symbols
description: >
  Place army boxes and unit symbols for a silent battle film: infantry, cavalry, archers,
  chariots, elephants, and banners. Both armies move forward in the clash. Use when staging
  formations or an advance. Never add audio.
---

# Army symbols

## Overview

Each army is a square box in its empire color. Inside the box, small symbols show the arms the sources actually give that force. In the clash, both boxes advance toward the gap and stop short of each other.

## When to use

Use after the map plate exists, and before commander circles are placed.

## Steps

1. Read `docs/house-rules.md` and `docs/placement.md`.
2. Choose the axis from this war's camps, not from a previous film.
3. Add one `role: army` marker per side. Set `symbol` to the arms you are allowed to show. The SVG files are:

   | Symbol | File |
   | --- | --- |
   | infantry | `skills/army-symbols/assets/infantry.svg` |
   | cavalry | `skills/army-symbols/assets/cavalry.svg` |
   | archer | `skills/army-symbols/assets/archer.svg` |
   | chariot | `skills/army-symbols/assets/chariot.svg` |
   | elephant | `skills/army-symbols/assets/elephant.svg` |
   | banner | `skills/army-symbols/assets/banner.svg` |

   Tint them with the empire color (`currentColor` in the file).
4. Put the banner on the edge that faces the enemy.
5. Leave a force that does not fight off the axis, with no motion keys.
6. In the clash scene, give both fighting armies `motions` from `docs/scene-contract.md`. Start at the camp side, end still at least 0.06 short of the other box. Confidence `illustrative`. The trail label is `Illustrative advance`.
7. Later scenes start those armies where the clash left them.
8. Implement box drawing, symbol drawing, and motions in `hde/` if the loader still rejects the fields. Dots and arrows are not a substitute for moving boxes: never use directional movement arrows on screen for advancing troops. Show movement exclusively through moving formation boxes (`motions`) with dashed advance trails.
9. Historical period flags (`assets/flags/<side>.png`) are mounted on white/silver flagstaffs above army formation boxes.

## Checks

- Both fighting armies have motion keys in the clash scene.
- The boxes do not overlap and do not sit in the subtitle band.
- Elephants, chariots, or cavalry appear only if the source note for this film includes them.
- The withheld flank never receives an advance.

## See also

- `docs/placement.md`
- `docs/scene-contract.md`
- `skills/commander-portraits/SKILL.md`
