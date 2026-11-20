---
name: dan-koe
description: Makes Dan Koe style minimal black-and-white line art for a reel. One white dot on pure black grows into a hairline tree that splits in two at every step, the tips light up, a pulse ring and sparks go off, and one quiet lowercase line swaps to a second. Use when the user runs /dan-koe or asks for Dan Koe style visuals, calm black and white motion graphics about choices, habits or compounding, or line art with one moving dot.
---

# /dan-koe

```
┌──────────────────────┐
│     one choice.      │  one lowercase line (swaps to line two at the payoff)
│    . :.:.:.:.:. .    │  the tips light up, sparks drift off the crown
│   \/\/\/\/\/\/\/   │
│      \/ \/ \/       │  hairlines that split in two at every step
│        \  /         │
│         |   (  )     │  one dot at the root, a pulse ring at the end
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
1. **Words.** Split the idea into a setup and a turn ("one choice." / "then the next."). Each line under about 30 characters, lowercase, ending with a full stop. One line is fine too.
2. **Spec.** Write `<name>.dankoe.json` (below).
3. **Build.** Run `python3 "$SKILL_DIR/build.py" <spec.json>`. It takes about 10 seconds. Add `--snap 2.6` for a quick PNG.
4. **Check** the sheet: the text sits on one line, the tree stays inside the red frame, and the last frames show the lit tips.
5. **Hand over** the mp4 path.

## Spec
```json
{"lines": ["one choice.", "then the next."], "depth": 9, "seed": 5, "light": false}
```
- **`lines`**: 1 or 2 lines. Line two appears when the last tips land.
- **`depth`**: 6 to 10 levels of branching. 9 makes 256 tips and a 4 s video; each level adds or removes 0.25 s.
- **`seed`**: any whole number. It changes the tree's shape, not its size.
- **`light`**: black lines on white.
- **`hold`** (optional): extra seconds at the end. **`out`** (optional): the output path.

## Taste
- Quiet and plain. Lowercase, no emojis, no bold, no exclamation marks.
- The idea should be about one thing turning into many (choices, habits, compounding), because the picture is one dot becoming a tree.
- For another motif, copy `template.html` and change the shapes, or use `/minimalistic-graphics` for the steps. Keep the rules: pure black, hairline white strokes, solid white dots, one line of text.
- Named after the style of Dan Koe's videos; not affiliated with him.
