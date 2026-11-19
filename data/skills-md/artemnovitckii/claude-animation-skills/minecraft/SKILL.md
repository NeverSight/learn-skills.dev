---
name: minecraft
description: Makes a Minecraft-style blocky voxel animation for a reel. A cottage builds itself block by block on a grassy hill, about 165 blocks dropping in with a bounce, then the chimney slams in with a puff of dust, the windows light up warm, smoke rises and a big pixel-font word lands. Procedural 16x16 pixel textures, blocky trees and flat blocky clouds, rendered with three.js. Use when the user runs /minecraft or asks for a Minecraft-style, voxel or blocky animation, or a build-it-block-by-block visual.
---

# /minecraft

```
┌──────────────────────┐
│ ▀▀▀  ▀▀▀▀   ▀▀       │  flat blocky clouds
│      home.           │  pixel-font caption (line two slams in)
│        ▄█▄  ▓        │  the chimney lands last, smoke puffs
│      ▄█████▄         │  stepped roof, plank walls, log corners
│ ▓▓   █ ▣ ▣ █   ▓▓    │  the windows light up warm
│ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   │  terraced grass hill, flowers, trees
└──────────────────────┘
```

## First use
This skill's folder is the "Base directory" Claude Code shows when it loads it.
```bash
SKILL_DIR="<base directory of this skill>"
KIT=$(python3 -c 'import os,sys;print(os.path.realpath(os.path.join(sys.argv[1],"..","..","kit")))' "$SKILL_DIR")
[ -s "$KIT/vendor/gsap.min.js" ] && [ -d "$KIT/node_modules/three" ] || bash "$KIT/setup.sh"
```
Needs ffmpeg and Node.

## Steps
1. **Words.** A short build line and a one-word payoff ("block by block" / "home."). Lowercase works best in the pixel font.
2. **Spec.** Write `<name>.minecraft.json` (below).
3. **Build.** Run `python3 "$SKILL_DIR/build.py" <spec.json>`. It takes about 1.5 minutes (WebGL in headless Chrome). Add `--snap 2.9` for a quick PNG.
4. **Check** the sheet: the house sits inside the red frame and the last frames show the lit windows and smoke.
5. **Hand over** the mp4 path.

## Spec
```json
{"lines": ["block by block", "home."]}
```
- **`lines`**: line one drops in letter by letter at 0.3 s and fades at 2.6 s. Line two slams in with the chimney at 2.7 s. Keep line one under ~17 characters and line two under ~9.
- **`hold`** (optional): extra seconds at the end. **`out`** (optional): the output path.

## Make another build
The cottage is a list of blocks with a drop time each. To build something else (a tower, a portal, a ship), copy `template.html` next to the spec, set `"template": "my-build.html"`, and change the block list: keep the order foundation, walls, roof, last block, and keep each block's position and scale a function of time only, so the video can be rendered from any frame.

## Taste
- One satisfying build with one payoff, not a whole world.
- Every texture is drawn in code on a 16x16 canvas with nearest-neighbour filtering. Don't use Mojang's textures, logos or characters.
- Named after the look of Minecraft; not affiliated with Mojang or Microsoft.
