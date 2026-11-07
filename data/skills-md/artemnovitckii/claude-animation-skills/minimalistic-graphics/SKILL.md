---
name: minimalistic-graphics
description: Makes a minimal black-and-white line-art animation for a reel. Thin outlined steps rise one by one, a white dot hops up them, and at the top an orbit draws around it and a short second line swaps in. One quiet lowercase line of text on top. Use when the user runs /minimalistic-graphics or asks for simple black and white motion graphics, a calm self-improvement visual or line art with one moving dot.
---

# /minimalistic-graphics

```
┌──────────────────────┐
│ every step feels     │  one lowercase line (swaps to line two at the top)
│ small.         (•)   │  orbit + ring + sparks around the dot
│              ┌──┐    │
│         ┌──┐ │  │    │  hairline steps rise, the dot hops up them
│    ┌──┐ │  │ │  │    │
│ ┌──┐  │ │  │ │  │    │
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
1. **Words.** Split the user's idea into two short lines: a setup and a turn ("every step feels small." / "until you look back."). Each line under about 30 characters, lowercase, ending with a full stop. One line is fine too.
2. **Spec.** Write `<name>.minimal.json` (below).
3. **Build.** Run `python3 "$SKILL_DIR/build.py" <spec.json>`. It takes about 10 seconds. Add `--snap 2.4` for a quick PNG.
4. **Check** the sheet: the text sits on one line, and the last frames show the orbit around the dot.
5. **Hand over** the mp4 path.

## Spec
```json
{"lines": ["every step feels small.", "until you look back."], "steps": 5, "light": false}
```
- **`lines`**: 1 or 2 lines. Line two appears when the dot reaches the top.
- **`steps`**: 3 to 7. More steps hop faster, and the video gets a little longer (3.8 s with 5 steps).
- **`light`**: black lines on white.
- **`hold`** (optional): extra seconds at the end. **`out`** (optional): the output path.

## Taste
- Quiet and plain. Lowercase, no emojis, no bold, no exclamation marks.
- The idea should be about steady progress (habits, compounding, patience), because the picture is a dot climbing steps.
- For another motif (a maze, a line that wanders, a circle that fills), copy `template.html` and change the shapes. Keep the rules: pure black, hairline white strokes, one solid white dot, one line of text.
