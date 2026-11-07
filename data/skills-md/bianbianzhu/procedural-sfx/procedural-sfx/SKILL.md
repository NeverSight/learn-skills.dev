---
name: procedural-sfx
description: Synthesize sound effects from code (numpy/scipy, no sample libraries), check them by numbers, and mix them frame-accurately under a video or animation with voice ducking and masking checks, then master it with a single linear gain to a loudness target for audio-only or video delivery. Use whenever someone needs sound effects or foley for a code-rendered video, animation, explainer, motion graphic or game prototype; wants to generate a specific sound from code (枪声, 爆炸, 脚步, 音效, 拟音, a laser, a door slam); needs SFX with no third-party sample licences; or needs audio synced to animation events, even if they never say "procedural". Not for composing music or finding recorded samples.
---

# Procedural SFX

Make every sound effect from noise, sine waves, filters and envelopes, then place each one on the exact frame where it happens. You get sounds with no third-party sample licences that render identically on every run and stay in sync with the picture automatically.

This works best for stylised work: animation, explainers, UI, motion graphics, game prototypes. For photoreal film foley (a specific real gun, real footsteps on real gravel) a recorded sample is still better. The mixer accepts audio files too (`"type": "file"`), so hybrids are fine.

## Setup

```bash
pip install -r scripts/requirements.txt   # numpy, scipy, soundfile
python scripts/check_env.py               # verifies them; ffmpeg >= 4.2 is optional (only for master.sh / mux.sh)
```

All scripts live in `scripts/` and run from anywhere. Paths below are relative to this skill's directory. On a mistake they exit 1 with `error: …` and a `fix: …` line; act on the fix line and rerun.

## Workflow

1. **Spot the sounds.** List every moment that needs a sound: time, what happens, what material is involved (plastic, wood, metal, air, electricity). Material decides the recipe, not the action's name: "a coin landing" and "a key dropping" are both small metal impacts. Plan the silences as well. A beat of quiet before a big hit makes it land harder than extra volume does.

2. **Pick or design each sound.** Run `python scripts/render_sfx.py --list` to see the built-in recipes. If one fits, render it with arguments and audition it. If none fits, write a new recipe in a project file based on `assets/recipe_template.py`.
   - Read `references/design-method.md` before writing a new recipe. It explains the attack/body/tail layering and which number changes what you hear.
   - Read `references/recipes.md` for what each built-in does, its parameters, and variations such as gun types, surfaces and distances.

3. **Check each sound by numbers.** You cannot hear the output, so measure it: `python scripts/analyze.py sound.wav --bands`. Compare attack, ring time, spectral centroid and band balance against what the sound should be. `references/design-method.md` has rough targets. For sounds that repeat, `render_sfx.py <recipe> --variants 4` prints metrics per take and flags takes that are identical or barely differ.

4. **Write the event list.** `events.json` is one entry per sound with time, type, args, gain and pan. `assets/events.example.json` is a runnable example; voice lines and recorded audio go in as `"type": "file"` events. Take the times from the same constants that drive the animation rather than retyping them. See `references/event-sync.md` for the schema, exporting from different animation stacks, and anticipation offsets such as a whoosh that starts before its impact.

5. **Mix.** Run `python scripts/mix.py events.json -o mix.wav [--recipes my_recipes.py] [--music score.wav] [--bed rumble] [--stems stems/] [--audition audition/]`. It validates the whole events file first, then prints levels per bus, a masking report that flags events buried under louder sounds, and the true peak before and after its limiter (ceiling −1 dBTP). Investigate every `CHECK` line: fix it, or accept it knowingly and say why. See `references/mixing.md` for gain staging, ducking and fixes for masking.

6. **Master for delivery.** Both scripts measure the mix, apply one linear gain to reach the loudness target (−14 LUFS for web/social; others in `references/mixing.md` §5) and print the re-measured result. They never compress; if the target would push the true peak over the limit they stop and name the loudest reachable target.
   - With a video: `sh scripts/mux.sh video.mp4 mix.wav out.mp4 [LUFS=-14] [dBTP=-1]`. The mix **replaces** the video's own audio. If the video already has music or dialogue that must stay, extract it (`ffmpeg -i video.mp4 -vn -c:a pcm_s24le original.wav`) and pass it to `mix.py --music original.wav` before muxing; `mux.sh` warns when the video has audio. Every video frame is kept, and the mix is fitted to the video's length before it is mastered (set `"dur"` to the video length and nothing needs fitting). Output `.mp4`, `.m4v`, `.mov` or `.mkv`.
   - Audio only: `sh scripts/master.sh mix.wav final.wav [LUFS=-14] [dBTP=-1]`.

7. **Hand off for listening.** Numbers catch broken sounds but not ugly ones. The mix report ends with a "not ear-tuned yet" table: every placed sound whose recipe status is `starting point` or `new`, one row per recipe and argument set. Run `mix.py` with `--audition DIR` and it renders each of those on its own (same args and take as in the mix) and fills in the file column; give events a `"name"` ("angry cat") and it fills in the sound column. Paste that table into the hand-off as it is: sound · recipe · args · status · times · file to audition. Ask the user to listen to every row that isn't `tuned`. If something is off, `references/troubleshooting.md` maps complaints like "too thin", "clicks at the end" or "sounds robotic" to fixes, and has the final QA checklist.

## Scripts

| Script | Purpose |
| --- | --- |
| `scripts/sfxkit.py` | Library: noise, envelopes, filters, sweeps, saturation, echo, radio FX, true-peak meter and limiter, `add()` for placing sounds, wav I/O |
| `scripts/recipes.py` | 18 built-in recipes + `load()` that merges your project recipe files |
| `scripts/render_sfx.py` | Render one recipe, variants, or all recipes to wav for audition |
| `scripts/analyze.py` | Metrics per file: peak, RMS, attack, ring time, spectral centroid, band energy |
| `scripts/mix.py` | events.json → stereo mix with buses, ducking, limiter, stems, masking report |
| `scripts/master.sh` | Audio-only delivery: measure, one linear gain to the LUFS target, true-peak check (ffmpeg) |
| `scripts/mux.sh` | `master.sh`, then mux under a video as AAC (ffmpeg) |
| `scripts/check_env.py` | Check dependencies |

## Built-in recipes

Impacts: `click`, `clack`, `crash`, `thump`, `step` (hard/wood/soft), `creak` · Motion: `whoosh` · UI: `ding`, `pop`, `beep` · Weapons & sci-fi: `gunshot` (pistol/rifle/shotgun), `burst`, `explosion`, `laser` · Ambience & drama: `rumble`, `ignite`, `roar`, `heartbeat`. Each has a status, shown by `render_sfx.py --list`: `tuned` (ear-tuned in finished work) or `starting point` (measured, never ear-tuned: `gunshot`, `burst`, `explosion`, `laser`, and `step` on wood/soft). Recipes from your own `--recipes` files are `new`. Details in `references/recipes.md`.

## Principles

- **One recipe = one normalised sound; gain lives in the event list.** Recipes end with `norm(x) * v`, and loudness is set only by `gain` in events.json. Mixing is then a matter of editing one table.
- **Randomness only through `noise()`, `rand()`, `uniform()`.** `mix.py` seeds each event from its type, time and args, so adding an event never changes how other events sound, and every render is byte-identical.
- **Vary repeated sounds.** Identical repeats (footsteps, gunfire, typing) sound fake. Randomise pitch by ±5–10%, level by ±20% and pan slightly.
- **Timing comes from the animation, not from your ears.** When sync is off, the fix is almost always in how the event times were produced, not a nudge in the mix.
