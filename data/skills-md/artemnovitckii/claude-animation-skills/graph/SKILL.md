---
name: graph
description: Makes a minimal line-graph animation for a reel. A smooth black line draws itself on white (or white on black) while one big number counts up with the tip, then lands on the final value. Use when the user runs /graph or asks for a growth chart, a "0 to 100K" number animation or an animated stat.
---

# /graph

```
┌──────────────────────┐
│ Followers            │  plain label
│ 100,000              │  counts up with the tip of the line
│                  •   │
│                 /    │  smooth line draws itself
│            ___/      │
│ ______----           │
│ Jan Feb ... Sep      │
└──────────────────────┘
```

## First use
This skill's folder is the "Base directory" Claude Code shows when it loads it.
```bash
SKILL_DIR="<base directory of this skill>"
KIT=$(python3 -c 'import os,sys;print(os.path.realpath(os.path.join(sys.argv[1],"..","..","kit")))' "$SKILL_DIR")
[ -s "$KIT/vendor/gsap.min.js" ] || bash "$KIT/setup.sh"
```
Needs ffmpeg and Node.

## Steps
1. **Numbers.** Get the real numbers from the user (or their screenshot). One value per point, oldest first. Never invent data; if they only give a start and an end, ask for the points in between or say the curve is illustrative.
2. **Spec.** Write `<name>.graph.json` (below) in the user's folder.
3. **Build.** Run `python3 "$SKILL_DIR/build.py" <spec.json>`. It takes about 10 seconds. Add `--snap 3.5` for a quick PNG instead of a video.
4. **Check** `<name>.graph.sheet.jpg`: the number fits on one line and the last frame shows the final value.
5. **Hand over** the mp4 path.

## Spec
```json
{
  "label": "Followers",
  "values": [1.2, 2.1, 3.4, 5, 9, 24, 51, 78, 100],
  "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
  "final": 100000,
  "prefix": "", "suffix": "", "decimals": 0,
  "dark": false
}
```
- **`values`**: 2 or more numbers, 0 or above. The highest one touches the top gridline.
- **`labels`** (optional): one per value, shown under the axis. More than 12 shows every other one.
- **`final`** (optional): the number the count lands on. The count is the value under the tip times `final / last value`, so you can give `values` in thousands and `final` in full. Leave it out to count in the units of `values`.
- **`prefix`**, **`suffix`**, **`decimals`**: `"$"`, `"%"`, `" kg"`, and so on. The number shrinks itself if it gets long.
- **`dark`**: white line on black.
- **`hold`** (optional): extra seconds to hold the last frame. **`out`** (optional): the output path.

## Taste
- One number, one line. The label is a plain noun ("Followers", "Monthly revenue"), not a slogan.
- No callouts, no "83x growth" chips and no marketing words on the graphic.
- Values that grow late (slow, then steep) make the best curve, but show the real shape.
