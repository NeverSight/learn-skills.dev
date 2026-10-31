---
name: effekseer-vfx
description: Author real-time game VFX as code for the Effekseer engine and verify them in a real Godot render, and turn image-to-video clips into flipbook skills for Effekseer/Godot or Unity (URP). Use when asked to create, edit, review or iterate on Effekseer effects (.efkefc/.efk), game hit, slash, projectile, explosion, beam, charge, magic, buff or shield VFX, combos and finishers driven by a character animation, stylized hard-edged VFX, realistic or kaiju/giant-scale effects, a VFX library for a Godot game, video-model flipbooks (water columns, fire turning to smoke, looping orbs) or element skills in Unity. Covers design briefs, sequences with a blockout gate, reference steal lists, paintover concepts, texture generation prompts, Python recipe code, EffekseerCore compilation, filmstrip review, screen feedback, independent scoring and export.
license: MIT
compatibility: Build and render need macOS on Apple silicon or Windows (x64), Godot 4.x and network access for the first setup (Effekseer Core, .NET runtime, Effekseer Godot plugin). Authoring, lint and texture processing run on macOS, Linux or Windows with Python 3.11+.
metadata:
  version: "0.3.0"
---

# Effekseer VFX

Make game effects the way a VFX artist iterates, but in code: **brief → textures → recipe → EffekseerCore build → real Godot filmstrip → look → fix one thing → repeat → independent review**.

`<skill>` below is the directory that contains this file. Every command is
`sh <skill>/scripts/vfx [--project <game project>] <command> ...` and prints one JSON object
(progress goes to stderr). The project defaults to the current directory; its effect workspace is `<project>/vfx/`.
Run `sh <skill>/scripts/vfx --help` for all commands; [references/cli.md](references/cli.md) documents them.
On Windows, `sh <skill>/scripts/vfx` works from Git Bash; from cmd or PowerShell run `<skill>\scripts\vfx.cmd` instead
(same commands, same output).

## First run in a project

1. `vfx doctor` — reports `modes` (`authoring`, `build`, `render`), the workspace and the exact `next` steps. If it says a `vfx/` folder exists that `vfx init` did not create, confirm with the user that this is the game project (or pass `--project`) before initializing.
2. If setup is needed, **ask the user first** (full mode downloads about 250 MB into `~/.cache/effekseer-vfx`):
   `sh <skill>/scripts/setup.sh` on macOS ARM64, `sh <skill>/scripts/setup.sh --authoring-only` on Linux; on Windows
   `powershell -NoProfile -ExecutionPolicy Bypass -File <skill>\scripts\setup.ps1` (or `sh <skill>/scripts/setup.sh` from Git Bash, which runs it).
   `doctor`'s `next` prints the exact command for this machine.
   Setup needs Python 3.11+ or uv (macOS's built-in Python 3.9 is too old); if `doctor` reports neither, ask the user to install one. Godot 4 (Forward+) must be installed by the user; set `GODOT` if it is not on `PATH`.
3. `vfx init` creates `vfx/` (Godot Lab, materials, math textures, official Effekseer plugin). It never overwrites existing files unless `--update-templates`.
4. Optional: `vfx examples add <name>` copies a finished, independently reviewed example to learn from: pairs `fire`, `ice`, `poison`, `dark` (projectile + impact), singles `hit`, `slash`, `charge`, `shield`, `heal`, the set `kaiju` (world scale, beam, charge chain, photographic explosion), or `all`. See [references/examples.md](references/examples.md).

`vfx review`, `preview` and `showcase` open a Godot window on the user's desktop. If you run inside a sandbox (Codex's
workspace sandbox, for example), run those commands outside it with the user's approval, or give the user the exact
command to run in a terminal on their desktop if you cannot leave the sandbox; a review that stops with "rendered no
frame" most likely could not open its window (check the Godot output it includes). `render: true` from `doctor` only means Godot was found.

Without `build`/`render` mode you can still write briefs, recipes and textures and run `lint`, but you cannot judge the
look. Say so plainly: report the work as **not compiled and not render-verified**; never claim an effect improved.

## Making or changing one effect

1. **Read before writing.** Always read [craft](references/craft.md), [design](references/design.md), [layering](references/layering.md), [timing](references/timing.md) and [skeletons](references/skeletons.md); then the topic files from the routing table below, and `vfx examples show <name>` for the matching example's layer plan (names: `hit`, `slash`, `charge`, `shield`, `heal`, the pairs `fire`, `ice`, `poison`, `dark` for projectiles and impacts such as explosions, or `kaiju` for large-scale, beam and realistic effects; an effect ID also works). For an existing effect run `vfx effect-context <ID>` and read its history so you do not repeat a failed change.
2. **Brief.** Write `vfx/briefs/<ID>.json` (three key frames, palette roles, beats, layer plan, acceptance, avoid). Format in [design.md](references/design.md).
3. **Textures.** Math shapes (glows, rings, noise, trails, distortion maps) and a starter set of painted smoke, explosion, wisp, crack and ice textures already exist after `init`. Complex painted shapes (flame, slash, smoke, crack, ice, rune) come from an image generation model — follow [textures.md](references/textures.md). Measure every texture with `vfx texture-info` before using its angle.
4. **Recipe.** Write `vfx/src/<ID>.py` defining `recipe()` with the primitives in [primitives.md](references/primitives.md). Follow the verified engine rules in [engine-conventions.md](references/engine-conventions.md) instead of guessing axes, units or blend behaviour.
5. `vfx brief-validate <ID>` and `vfx lint --ids <ID>`. Lint errors must be fixed; warnings are craft hints the render decides.
6. `vfx build --ids <ID>`, then `vfx review --ids <ID> --note "<what this round changed>"`.
7. **Look at the images.** Open every path the review returns (`sheets`, `compare`, `details.*.sheet`) with your image-viewing tool. Flags only point at likely problems; never judge from flags alone. Procedure and flag meanings: [review.md](references/review.md).
8. Fix **one class of problem per round**, 3–5 rounds per effect.
9. **Independent review.** The author never scores its own effect. Run `vfx review-handoff <ID>`: it writes a complete reviewer brief (images, captured frames, manifest context, rubric, where to save the report, and the path of the `vfx-review` skill installed next to this one) and returns `prompt_file`, `report_file` and the exact submit command. Give that brief, unchanged, to a separate agent that has not seen the recipe: start a subagent with it if your host can, telling it nothing else about the effect; otherwise ask the user to open a new session and paste it. When `report_file` exists, run the returned `vfx review-submit <evidence_id> <report_file> --reviewer <that agent's identifier>` (its subagent ID or name, or the session ID; never `author` or `self`; frames default to the report's `observed_frames`). Never write the report yourself.
10. `vfx overview` (no `--ids`: the library baseline), then `vfx effect-verify <ID>`. Only `verified: true` may be reported as done; otherwise list what is missing. If the round limit is reached without a ship verdict, report the unresolved items.

## Three ways to make an effect

Pick per effect; none is required. **Procedural** (everything above): layered primitives in a recipe, Effekseer →
Godot. **Video flipbook**: an image-to-video clip on black becomes a graded sheet (`vfx video-first-frame`,
`video-timeline`, `video-flipbook`, `video-grade`) — the way to get a continuous change of shape that primitives cannot
draw (a column that rises and collapses, fire that boils into smoke, a looping orb). **Combined**: the sheet is the
body layer of a recipe (`video_body(...)`) and primitives add the flash, sparks, rings, cracks and decals. Sheets play in
Effekseer/Godot or, through `vfx unity-install` / `unity-export`, in Unity (URP) as data-driven element skills. Read
[video-flipbook](references/video-flipbook.md) before any of it.

## Making a combo or a skill with several beats

When several effects fire on the beats of one animation (a laser chain ending on a finisher), work on them as a
**sequence** ([sequence](references/sequence.md)): measure the event times in the game, write
`vfx/sequences/<SEQ_ID>.json`, and go **blockout → detail → polish**. The blockout uses basic shapes and solid colours
only (`effect(..., stage='blockout')`) and must get an independent `ship` (`vfx sequence-review`, preferably with
`--frames` captured in the game, then `sequence-handoff` / `sequence-submit`) before any texture work. Detail adds
references with steal lists; polish adds a paintover concept (`vfx paintover`, an image-edit model, `vfx
concept-compare`) and the finisher's screen feedback (`screen=`). Cut any element that does not carry the theme and
record it in `cut`. Each effect in the sequence still has its own brief, recipe and single-effect review.

## Hard rules

- Every effect has a time structure (anticipation → contact → body → secondary → dissipation) and value layering (white-hot core, saturated body, darker rim or residue). Heals, shields and charges have their own documented exceptions.
- The body changes shape (dissolve, sweep, UV distortion, flipbook, re-struck shapes); it never only scales and fades. Particles ease out (fast, then slow).
- Elements differ in at least three of shape, motion, rhythm, material and secondary motion — never a recolour.
- Do not draw complex painted shapes with Python. If no image generation tool is available, write the prompt into `vfx/texture_prompts.json` and ask the user for the image.
- Keep generated originals in `vfx/textures/generated/` and write processed copies to `vfx/textures/processed/`; record every prompt (`vfx video-flipbook --prompt-file` records clips in `vfx/video_prompts.json`).
- A video clip is a body, never a finished effect: the engine adds the contact flash, secondary motion and ground. Generate it with a first and a last frame on pure black, skip opening white flashes, grade every sheet of one element with the same ramp, and no hit-stop while it plays (hit-stop freezes the flipbook).
- Units: recipe timing in 60 FPS frames, F-curves in percent of life, manifest duration/peak in seconds, Godot API rotation in radians.
- Write recipes at the Lab's character scale; for a larger world declare `scale` instead of hand-scaling numbers ([scale](references/scale.md)). Frames in briefs and reviews are the built, scaled timeline.
- Every effect declares `delivery`; a projectile needs a paired impact effect that points back to it.
- Screen feedback (shake, impact frame, hit-stop) is manifest data (`screen=`), reviewed with the effect; the game
  plays it from `Vfx.screen_cue`, never as a separate hand-tuned guess.
- Use only layer fields the compiler knows (`vfx layer-schema`); extend the compiler instead of writing raw property paths into recipes.
- A full `vfx build` (no `--ids`) prunes the outputs of effects this skill built whose source left `vfx/src/`; it never deletes effects it did not build and refuses to run on an empty library. Use `--ids` for partial work (a broken source elsewhere is reported in `unloaded` instead of blocking it).
- Never claim export, playback, device performance or recording success without actually running and checking it.

## Routing table

| Task | Also read |
|---|---|
| new painted texture, flipbook, texture problem | [textures.md](references/textures.md) |
| image-to-video clip → flipbook, `video_body`, combined effects, Unity (URP) skills | [video-flipbook.md](references/video-flipbook.md) |
| slash, projectile, charge, aura, anything that travels | [motion.md](references/motion.md) |
| shield, pillar, boss, status, volumes, occlusion | [shapes.md](references/shapes.md) |
| matching a reference video | [reference.md](references/reference.md) |
| giants, kaiju, warships: anything far larger than a character | [scale.md](references/scale.md) |
| combo, finisher, several effects on one animation, blockout, paintover, camera shake / flash frame / hit-stop | [sequence.md](references/sequence.md) |
| stylized hard-edged look, only when the brief's `style` asks for it: toon shapes, spiral ribbons, spiky dark bases, star glints, greyscale masks | [stylized.md](references/stylized.md) |
| beam, laser, breath weapon, charge chain, values the game drives at runtime | [primitives.md](references/primitives.md) (`beam`, `charge_chain`, `bind`), [godot.md](references/godot.md#beams) |
| realistic / photographic explosion, fire, smoke, steam | [realism.md](references/realism.md) |
| a specific visual failure (white blob, empty tail, no break-up) | [cases.md](references/cases.md) |
| adding an engine feature to the compiler | [engine-conventions.md](references/engine-conventions.md#extending-the-compiler), `vfx discover`, `vfx core property-list/get/set` |
| using the effects in a game | [godot.md](references/godot.md) |

## Recipe skeleton

```python
# vfx/src/VFX_Hit_Spark.py
from vfxkit.primitives import *

def recipe():
    hot = (255, 240, 200, 255)
    return effect('Hit_Spark', 'Spark Hit', 'hit', 'physical', .4, [
        flash('Contact flash', WHITE, 2.2, life=4, delay=1),
        glow('Bloom', (255, 170, 70, 170), 1.6, life=9, delay=1),
        radial_sparks('Sparks', 10, hot, color_end=(255, 120, 30, 255), distance=(.8, 1.7), life=(12, 16), delay=1, gravity=.0018),
        smoke('Dust', (185, 160, 135, 200), count=2, size=(.5, .7), life=(13, 14), delay=4),
    ], peak=.03, impact=.3, delivery=MELEE, design='One-line description of what the player sees.')
```

`effect('Hit_Spark', ...)` produces the ID `VFX_Hit_Spark`, which must match the file name. Files starting with `_` in
`vfx/src/` are shared helpers that recipes may import.
