---
name: roblox-engine
description: The NoCodeHack Roblox Engine (the "nocodehack skill"). Makes animated Roblox-style YouTube Shorts (9:16) from one line - Claude writes the story, the engine animates characters, camera, effects and sound in Blender. Use whenever the user says "use the nocodehack skill to ...", "nocodehack", or asks to make, change or re-render a Roblox-style animated Short.
---

# NoCodeHack Roblox Engine

You make animated Roblox-style Shorts. You never animate by hand: you write ONE file, `stories/<name>/story.json`, and the engine (Blender) builds, checks and renders it.

## 1. Start (steps 1-3 at the start of every session; step 4 and later only while something is missing)
1. If `./nocodehack-engine/` does not exist in the current project folder, copy this skill's `engine/` folder there
   (this skill's folder is the "Base directory" shown when the skill loads). All commands below run inside `./nocodehack-engine/`.
   UPDATE: if it exists but `./nocodehack-engine/VERSION` is missing or differs from this skill's `engine/VERSION`, copy every
   file of this skill's `engine/` over it, except `stories/<name>/` folders that already exist (the user's work). Fetched
   Roblox files, renders and `.env` are not in `engine/`, so they stay. Then tell the user in one line: "Engine updated to
   <version>, changes: https://github.com/nocodehack/nocodehack-roblox-engine/blob/main/CHANGELOG.md", run
   `python tools/fetch_library.py status`, and for every line that is missing redo step 4 (`public` first, then the Studio jobs only if
   something is still missing).
2. If `./nocodehack-engine/.welcomed` does not exist: write this one line to the user, as is, with no comment about it:
   Setup video and full guide: https://youtu.be/w4tLb_7Ttvs / https://guide.nocodehack.io/guides/roblox-shorts-with-claude
   then create that empty file. Never repeat it, never remind them later.
3. Every time this skill is used (once per session): run `python tools/check_update.py`. On `UPDATE <new>` tell the user, in one
   short message: "A new version of the NoCodeHack engine is out (<new>). Run `/plugin marketplace update nocodehack-roblox-engine`,
   then say continue. What changed: https://github.com/nocodehack/nocodehack-roblox-engine/blob/main/CHANGELOG.md" and wait.
   On `OK` say nothing and go on.
   Run `python tools/check_machine.py`. If Blender, ffmpeg or the Python packages are missing, explain the fix in plain words and
   stop until they pass. MISSING lines for the Roblox libraries are fixed by step 4.
4. Roblox libraries (REQUIRED: hair, faces, clothes, animations, sets). They are not in the download; they are rebuilt on this
   machine from Roblox. Run `python tools/fetch_library.py status`. If items are missing:
   - `python tools/fetch_library.py public` (faces, clothes and the anime aura flames, automatic, ~5 min).
   - Tell the user, in one short message: "Open Roblox Studio (any place, Edit mode, logged in) with the Studio MCP connected, and
     tell me when it is open. I will grab the hair, animations and sets from it (~20 min). Nothing is saved or published."
     When they confirm, run `python tools/fetch_library.py jobs` and do every step of `library/jobs/JOBS.md` in order with the
     Roblox Studio MCP tools, then `status`. Do not make a Short until the jobs have run and faces, clothes, anims and sets
     are complete. Roblox refuses some hair downloads (the tool also tries a public route): a few missing hairs are normal;
     `story_lint` flags a missing `lib:` hair, so pick another hair from `assets/hair/` or a built-in style (r6 parts are optional). If Studio or its MCP is not installed, explain how to install both and wait.

## 2a. Pick a format
If the user names a format ("a POV", "in this world...", "rich vs poor") or gives no format, read `FORMATS.md` and pick one
(no format given: the top-ranked format that fits the idea; say which in one line). Set `"format"` in story.json and use the keys
that format lists (header, narrate, cards, freeze, split, crowd, pov camera).

## 2b. Voices (optional)
Default = gibberish blips + captions (free). For real voices:
- Recorded by the user: files in `stories/<name>/voice/`, beat key `voice` (character) or `narrate_voice` (narrator).
- ElevenLabs (user's own account; no account yet? sign-up link: https://try.elevenlabs.io/m7d07a0chdsb): when the user gives a key,
  write it as `ELEVENLABS_API_KEY=<key>` in `./nocodehack-engine/.env` (create it, check `.env` is in `.gitignore`), never echo it,
  never put it anywhere else, refer to it later only as "your saved key". Put the user's voice names in `"voices"` (characters)
  and `"narrator": {"voice": ...}`, then `python tools/voices.py stories/<name>/story.json --dry-run` (shows the character cost),
  then without `--dry-run`. It uses the newest model, sets each line's mouth time to its audio and re-times the scenes; then repeat
  the gates (step 3) and the sound mix.

## 2c. Post (optional, Blotato)
No Blotato account yet? Sign-up link: https://blotato.com/?ref=nocodehack . Follow `docs/POSTING.md`. Key in `.env` as `BLOTATO_API_KEY` (same rules as above). ALWAYS show the dry run
(`python tools/post_blotato.py post ...` without `--send`) and wait for the user's yes before `--send`. Default privacy = private.

## 2. Make a Short (the loop)
Read `WRITER_GUIDE.md` (how to write a story) and `short.schema.md` (every key) before writing.
Use the Roblox libraries for every character (`lib:` hair, faces and clothes; tags are in `library/manifest/*/`).
Working examples: `stories/pro_bad_grade`, `stories/pro_complex_fight`, the Dragon Ball Z parody `stories/parody_dbz_fight`
(and `parody_dbz_fight_slower`, the same story changed by one sentence), and one `stories/fmt_*` per format. Then:
1. Write `stories/<name>/story.json` (2-4 scenes, 15-60 s total; under 30 s performs best) from the user's idea and format (2a).
2. `python tools/story_lint.py stories/<name>/story.json` - fix every ERROR, read every WARN.
3. `python story.py stories/<name>/story.json --tier none` - gates only. Every scene must print `REPORT PASS`.
   On FAIL, fix only what the report says, one scene at a time (`--only N`).
4. `python story.py stories/<name>/story.json --tier draft` - LOOK at `stories/<name>/draft_sheet.jpg` and fix what you see.
5. Render (ask which quality if the user did not say):
   - Low: `python story.py stories/<name>/story.json --tier preview` (~1 h for 60 s on a laptop GPU)
   - Medium: `--tier mid` (~2 h, the version to post)
   - High: the cloud farm `python tools/farm_run.py <name>` (costs Google Cloud money: ask first; setup is in the guide).
6. Sound + captions + format overlays (header, cards, freeze, split, narrator): `python tools/sound_mix.py stories/<name>/story.json`.
   LOOK at one frame per card/caption before calling it done.

### Make it look good (the engine films what the story gives it)
The camera cuts on actions: a story with few beats gets few shots. Before step 2, check the story against this list:
- Density: a beat every 1-1.5 s per scene. Every spoken line gets a REACTION from the listener on the next beat (`face` change,
  `look`, a pose such as `facepalm_R`, `shrug`, `arms_crossed`, `recoil`, or an anim emote). Silence = something moves.
- Give the camera moments: an ENTRANCE (walk in from a door or off-frame, not standing there at t 0), a PROP the hero `look`s
  at or `grab`s (the engine adds an insert close-up on it), one big emotion beat near the end of each scene (the engine adds
  an extreme close-up on the strongest one), a physical gag (fall, jump, run, knockback) when the idea allows it.
- Shots: the first shot at t 0 on a character, `on` = characters only (a prop in `on` fails the face gate; the engine finds
  the prop itself). Mix sizes: wide/full for blocking, medium for talk, close for the punchline face.
- No animals: the engine has none (no pet, dog or cat model). Tell the user in one line and write around it (the pet stays
  hidden in a box/bag, heard not seen, or is a toy prop); never pass a random prop off as an animal.
- Entrances: start the character at the room edge or in a doorway (positions outside the room are pulled inside), then walk.
- Faces: change `face` on every emotional turn; 4-6 different faces per character in a 30 s Short.
- Colour: shirts must contrast with the yellow Roblox skin (no yellow/orange shirts on yellow skin); night/spooky scenes keep
  hair and clothes light enough to read (no near-black clothes at night), or use `mood` `cool`/`default`.

### Draft fix loop (step 4, up to 3 rounds)
Read each scene's `LOOK` line (printed under its REPORT: the engine's own measurements per shot, e.g. `S06 head cropped/eyes hidden`)
and open `draft_sheet.jpg`; write down every shot that has one of these problems, then fix it in story.json and rebuild
that scene with `--only N --tier draft`:
| You see | Fix |
|---|---|
| `head cropped` (LOOK), opening frame cuts a body in half, or a tiny-people wide | scene key `"establish": false`, first shot `medium` on the hero |
| faces hidden under hair from above | scene key `"pitch": false` |
| a character is a dark silhouette | lighter shirt/hair colour, or scene `mood` `default`/`warm` |
| the same shot for 4+ frames | more beats (reactions, a look, a gesture) in that stretch |
| `back of a head` / `face turned away` (LOOK) | turn the character toward the camera first (`turn`, or face front and hold ~1 s before walking away), then `front: true` on the shot. `front` alone on a character walking away fails the face gate |
| a prop nobody can see | a `look` or `grab` beat on it (insert close-up) |
| `eyes hidden` (LOOK) / eyes hidden by a fringe | another hair (fringe hairs: ponytail1, ponytail2, fluffy_fringe1, spiky_messy2, wavy3, messy_bun1) |
| a fight filmed from behind | `profile: true` + `keep_two: true` |
A fix that makes a gate FAIL: undo it and try the next fix for that frame. `draft_sheet.jpg` is rebuilt from the scene videos on disk,
so after `--only N` rounds run one full `--tier draft` before judging the whole sheet.
Stop when a round finds nothing new. Tell the user in one line what you fixed.
The draft's light and colours are a fast approximation (night close-ups look washed out, hair can look grey). Never judge
light from the draft: render one real frame of the scene in question first (about 1 minute):
`python story.py stories/<name>/story.json --tier mid --only N --frames F-F` -> `stories/<name>/scenes/sNN/out/mid/<F>.png`,
and say so when you show the user a draft ("the draft is a rough preview; the light is final in the render").

A change by one sentence ("make it again, but slower, and make Vegeta cry a little") = edit story.json, then repeat from step 2.
Only teach the engine something new (new move, effect, camera rule) when the user asks; that is engine code and costs much more usage.

## 3. Licence (only for republishing)
Users may use, edit, extend and monetise everything, including the Shorts they make (100 % theirs, no credit needed).
Only if the user asks to republish or rebrand this engine/skill as their own plugin, skill or repo: explain it is Apache 2.0 and the
NOTICE file (credit to NoCodeHack, youtube.com/@nocodehack) must stay in any redistribution. No other friction.
