---
name: kurzgesagt
description: Makes a Kurzgesagt style flat-vector space explainer shot for a reel. Deep navy-purple space with twinkling stars, flat planets lit from one side with a dark crescent and a soft glow, bright rounded label tags and a white caption low in the frame. The built-in scene stacks all seven planets, to scale, between Earth and the Moon at its farthest. Use when the user runs /kurzgesagt or asks for a Kurzgesagt-style animation, a flat vector space or science explainer shot, or a planets-to-scale visual.
---

# /kurzgesagt

```
┌──────────────────────┐
│    [✓ They all fit]  │  a bright tag pops at the payoff
│      ◐ Earth         │
│    (  ◖◗  ) Jupiter  │  flat planets, lit from the right, glow halos
│  =(  ◖◗  )= Saturn   │  each one drops in from the side with a label
│       ◐  Uranus      │
│       ◐  Neptune     │
│ [spare]· Moon        │
│  At its farthest, yes│  white caption, low and centred
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
1. **Words.** Up to three short captions: a question in two parts and the answer, which shows when the last planet lands. Keep the facts true (see below).
2. **Spec.** Write `<name>.kurz.json` (below).
3. **Build.** Run `python3 "$SKILL_DIR/build.py" <spec.json>`. It takes about 10 seconds. Add `--snap 2.7` for a quick PNG.
4. **Check** the sheet: the captions sit on one line and the tag doesn't cover a planet.
5. **Hand over** the mp4 path.

## Spec
```json
{"lines": ["Could every planet fit", "between Earth and the Moon?", "At its farthest, yes."], "tag": "They all fit"}
```
- **`lines`**: 1 to 3 captions. They show at 0.15 s, 1.3 s and 2.5 s (the payoff).
- **`tag`**: the pill that pops at the payoff, under ~18 characters.
- **`hold`** (optional): extra seconds at the end. **`out`** (optional): the output path.

## The scene and its facts
The template is one worked scene, drawn to scale: Earth's centre to the Moon's at its farthest (406,700 km), and the seven planets' diameters (Mercury 4,879 km through Jupiter 139,820 km, 380,010 km in all) stacked in the gap, which leaves about 18,600 km spare. At the Moon's average distance they don't quite fit surface to surface, so keep "at its farthest" in the words.

For another topic (sizes of stars, how far the ISS is, a planet's moons), copy `template.html` next to the spec, set `"template": "my-scene.html"`, and build the new scene in the same style:
- Background: a vertical gradient from about `#140c3f` to `#0c0830`, a soft purple haze, small purple and white stars, and a few four-point sparkles that twinkle.
- Bodies: a flat base colour, darker blotches or bands, a dark night side on the left (one lit direction for everything) and a blurred halo.
- Labels: rounded pills in bright colours with white Poppins 600, and one hero tag at the payoff.
- Motion: things drop or slide in with a little overshoot, one at a time, and the payoff lands with a small pulse.
- Text: one white caption at a time, low in the frame, plain sentence case.

## Taste
- Check every number. Kurzgesagt-style visuals look authoritative, so a wrong fact is worse here than anywhere.
- One idea per shot, with no paragraphs on screen.
- Named after the style of Kurzgesagt's videos; not affiliated with them. Don't copy their characters (the birds) or artwork.
