---
name: scenario-playable-ads
description: "Use when a mobile game's gameplay recording, screenshots or existing art and sound should become a playable ad: an HTML5 interactive ad or interactive end card for Meta, Google Ads App campaigns, AppLovin, Unity Ads, Mintegral, Moloco, Liftoff, TikTok Pangle or any MRAID network, with a hint hand, a CTA and a mute button, packaged per network and QA-tested in headless Chromium. Keywords: playable ad, HTML5 playable, MRAID, FbPlayableAd, ExitApi, end card, CTA, hypercasual ad."
license: MIT
---

# Scenario Playable Ads

## Overview

A playable is a 35 to 45 s slice of a real game that runs inside an ad network's container. It has:

- one self-contained HTML file with no network requests;
- one verb the viewer understands within 2 s;
- a game that waits for the viewer and never plays itself;
- a mute button, always;
- the genre's signature payoff;
- a win or an honest near-fail, then an end card with an install button.

**Input:** a gameplay recording and/or screenshots of the user's game, plus a logo, store links, a
description and a genre pick when the user has them. When the studio already has art, 3D, sound or
music, the build uses those files as they are, generates only what is missing in their style, or
derives the rest from one key art ([references/existing-assets.md](references/existing-assets.md)).

**Output:** `dist/<network>/index.html` for nine networks and a local preview, the ZIP each ZIP
network takes, and a bundle of all of them. A build ships only when it passes the 19 base QA checks
plus the per-network checks.

**What was tested.** The nine-network packaging ran against fake containers in headless Chromium: 64
of 64 checks on a copy of one game. The scripts in this skill, with the first-tap guard, the Pangle
SDK placement and the input and sound holds added since, pass 67 of 67 checks on the template's
placeholder game in the same fake containers. That game also passed AppLovin's playable preview
(portrait) and Google's HTML5 validator on the App Campaigns profile (2 November 2026). Google's
Campaign Manager and Display & Video 360 policies reject the `google` ZIP, which needs a `clickTag`
there. Meta's playable preview took the `meta` ZIP, passed its spec checks and registered the CTA
tap. No other network's own tool was run. Say which tools were run when you hand a build over, and
run each network's own preview first ([references/networks.md](references/networks.md)). Each
archetype guide comes from one build that passed the 19 base checks.

Requirements: a local shell, Python 3.12 or later with Pillow, numpy, scipy, fontTools and brotli;
Playwright for Python with Chromium; ffmpeg. Install with
`pip install "pillow>=13,<14" "numpy>=2.5,<3" "scipy>=1.18,<2" "fonttools>=4.60,<5" "brotli>=1.1,<2" "playwright>=1.64,<2"`
then `playwright install chromium`; check with `ffmpeg -version`. The scripts, runtime and template
sit in this skill's `scripts/` and `assets/` folders, so the agent needs file access to the skill.

Connection, uploads and the core loop: the `scenario` skill. Image edits: `scenario-image`. Sheets
and cut-outs: `scenario-game-assets`. SFX and music: `scenario-audio`. Image-to-3D: `scenario-3d`.
If a sibling skill named here is missing from your available skills, load it with `skill_get`
(Scenario MCP) or ask the user to install it (https://github.com/scenario-labs/skills#install);
unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Step        | What happens                                                                                |
| ----------- | ------------------------------------------------------------------------------------------- |
| 1. Intake   | `intake/`: recording and/or screenshots, logo, `intake.json` (store links, networks, genre) |
| 2. Analysis | contact sheet, key frames, `analysis/brief.md` and `analysis/design.md` (beats, asset map)  |
| 3. Assets   | plate, transparent sheets, HUD crops, logo, SFX, music in `assets/raw/`, or studio files    |
| 4. Build    | `src/game.js` on the runtime; `assets/manifest.json`, then `prep_assets.py`                 |
| 5. Package  | `build.py --networks all` (the default is `meta,google`)                                    |
| 6. QA       | `qa.py --speed 2`, then look at every frame it writes                                       |
| 7. Report   | `notes.md`: job ids, the source frame of every asset, tuning, open questions                |

```bash
SKILL=<path to this skill>; P=<project dir>
cp -Rn "$SKILL/assets/template/." "$P/" && mkdir -p "$P/runtime" && cp "$SKILL/assets/runtime/runtime.js" "$P/runtime/"
python3 "$P/make_placeholders.py" "$P" --font "$SKILL/assets/fonts/fredoka/Fredoka-Bold.woff2"  # optional
python3 "$SKILL/scripts/asset_inventory.py" "$P"    # only with the studio's own files: analysis/assets_inventory.md
python3 "$SKILL/scripts/prep_assets.py" "$P"        # assets/raw and intake/ to assets/web/
python3 "$SKILL/scripts/build.py" "$P" --networks all
python3 "$SKILL/scripts/qa.py" "$P" --speed 2       # qa/report.json and qa/*.png
```

- `cp -Rn` never overwrites what the project already has, such as `intake/`.
- Never edit the runtime or the scripts per game. Work around a gap in the game's own code and write
  it in `notes.md`.
- Replace the template's game section with your genre. Keep its structure: config, reset, wait,
  play, result, input on pointerdown, draw, `qa()` with `progress`, boot.
- The hint hand is a vector drawing unless the project adds `assets/web/hand.webp`.

## Start here

When the user has not yet said what they have (for example "how do I make a playable ad?"), ask
once, in one message, for everything the build needs, then wait. Do not generate anything yet.

1. A gameplay recording of 30 s to 2 min and/or store screenshots. With neither, stop: the skill
   rebuilds what it sees and never invents a mechanic.
2. The game name, the logo file, the App Store and Google Play links, and one line on what the
   player does.
3. The ad networks they run, or "not sure" (the build covers nine).
4. Whether the game is 3D with a free camera (see the decision points below).
5. Any art, 3D, sound or music they already have for the game, and whether they own it for ads
   ([references/existing-assets.md](references/existing-assets.md)).

Say in two lines what they will get: the game's core loop rebuilt as code from the recording, with
their own art and sound where they sent some and generated art and sound for the rest, never the
recording itself, so side features are simplified. Then watch the recording and ask the genre
question below; when they sent files, ask in the same message how to use each kind (as supplied,
complement or derive). Those are the only two rounds of questions the user needs to answer; the
Scenario team and project, when the `scenario` skill asks for them, go in the first round.

## Two questions before generating anything

Answer both in `analysis/brief.md`.

1. **Which genre is it?** Watch the recording first (contact sheet and key frames). Then ask the
   user one question with these options:
   - the two genres from [references/genres.md](references/genres.md) that fit best, each with a
     one-line reason from the recording (what the finger does, the most satisfying moment);
   - "I don't know, you choose": pick the best fit and say why in one line;
   - "Other": ask what the player does and what makes it fun, and store it as `game_description`.

   Record the answer in `intake.json`. Classify from the recording, not the label, and state your
   confidence. No guide, a hybrid, or a game too big for one verb: follow
   [references/unknown-genre.md](references/unknown-genre.md). Never invent a mechanic the recording
   does not show.

2. **Why would someone install after playing?** Plan the levers from
   [references/make-them-install.md](references/make-them-install.md): a first touch that pays off
   at once, visible growth, one real choice, a tease from the recording, a cliffhanger ending with
   the player's own state on the end card.

## Decision points

1. **Genre and product model** (hypercasual, hybrid-casual, casual, midcore) go into `intake.json`.
   The genre's row names its guide or the nearest one.
2. **Hook:** one opening pattern while the game waits: a power spike, a near-win, a satisfying
   motion, or a clear promise. One short line on a backing plate. Fail-bait is allowed only as the
   player's own choice.
3. **Signature payoff:** the moment that makes the genre (a screen wipe, a crowd clash, a legendary
   merge), at 10 to 25 s of play, the biggest and loudest thing in the ad.
4. **Ending:** a good player wins, a careless one ends one step short, an untouched viewer gets the
   end card after 10 s. Cap play at 35 to 45 s after the first touch.
5. **Original IP:** when the genre has a famous leader, list what the game must not share with it
   (characters, piece shape, board and track silhouette, how ammo is shown, the name). Have a human
   compare with the leader's store page. See
   [references/archetype-paint-train.md](references/archetype-paint-train.md).
6. **Networks:** ask which ones the user runs. Per-network contracts, confirmed facts and the
   unconfirmed list: [references/networks.md](references/networks.md).
7. **3D games:** ask before generating. A fixed or side camera means 2.5D from frames; a free 3D
   camera means considering three.js with an image-to-3D model. Unattended, build 2.5D and say so.
   See [references/3d-games.md](references/3d-games.md).
8. **Orientation:** portrait first. Re-slice a landscape level along the portrait axis instead of
   letterboxing it, and collapse an on-screen pad to one finger (say it is drift and ask the user;
   unattended, ship the one-finger verb and record the drift in `notes.md`).

## Archetype index

| Archetype                       | Ad verb                                 | Guide                                                  |
| ------------------------------- | --------------------------------------- | ------------------------------------------------------ |
| Survivor shooter                | tap to move, auto-fire, tap a card      | [survivor](references/archetype-survivor.md)           |
| Crowd runner with math gates    | drag left and right                     | [crowd runner](references/archetype-crowd-runner.md)   |
| Lane shooter with gates         | drag left and right, auto-fire          | [lane shooter](references/archetype-lane-shooter.md)   |
| Merge-2                         | drag an item onto its twin              | [merge](references/archetype-merge.md)                 |
| Sort puzzle                     | tap source, tap target                  | [sort](references/archetype-sort.md)                   |
| Conveyor color puzzle           | tap to dispatch a shooter               | [paint train](references/archetype-paint-train.md)     |
| Pin pull                        | tap or swipe a pin                      | [pin pull](references/archetype-pin-pull.md)           |
| Idle arcade                     | tap to move                             | [idle arcade](references/archetype-idle-arcade.md)     |
| Tower defense                   | tap a pad to build or upgrade           | [tower defense](references/archetype-tower-defense.md) |
| Platformer, as a portrait climb | tap where to land, tap again in the air | [platformer](references/archetype-platformer.md)       |
| Racing, real 3D                 | drag to steer, tap to boost             | [racing](references/archetype-racing.md)               |

A new archetype gets `references/archetype-<name>.md` with these sections: Controls, Beat sheet,
Tuning, QA bot pattern, Asset map with source frames, Mistakes seen. Then add its row here and mark
it built in `genres.md`.

## Rules every playable follows

- **Never autoplay.** The game never makes a move for the player: no demo, no rescue autopilot, no
  auto-picked card. The world may run where that is the genre (a crowd runs forward), but every
  choice is the player's.
- **Wait, alive, for the first touch.** The gameplay clock is held, the target glows, and the hand
  loops the exact gesture on a real good move. `qa()` exposes `progress`, which stays 0 until the
  first touch.
- **Three endings:** the goal, a time cap of 35 to 45 s of play, and a 10 s idle timeout. After a
  start, an honest line shows for at most 1.5 s before the end card.
- **Hint, never a move.** The hand returns after 2.5 s idle and only points.
- **Mute button, always.** The runtime draws it and it cannot be turned off; `cfg.mute` only moves
  it. It never counts as the first touch.
- **The first tap never opens the store** on `applovin`, `unity` and `mraid`. The runtime enforces
  it.
- **Calm sounds.** Nothing repeats faster than about 3 times a second (`cfg.soundGap`). Duck the
  music around each payoff (`PA.audio.duck`) and boost quiet takes with `boost_db`, never plain
  gain.
- **Honest result text,** computed from the real state: "SO CLOSE! 1 left!" only when one move
  remains.
- **A near-fail for bad play.** Scripted luck rewards the player's own good moves, so careless play
  ends just short.
- **Replay** calls `PA.clearTweens()` before `reset()`, and the game waits again.

Asset sourcing, prompts and model discovery:
[references/scenario-assets.md](references/scenario-assets.md). Starting from the studio's own
files: [references/existing-assets.md](references/existing-assets.md). Lessons and known runtime
gaps: [references/build-lessons.md](references/build-lessons.md). Every QA check, build refusal and
the game contract: [references/qa-checks.md](references/qa-checks.md).

## Worked example: a sort puzzle from a 40 s recording

1. The user drops `gameplay.mp4`, a logo and store links in `intake/`. A 4 fps contact sheet shows
   taps that pour liquid between jars, and a jar that pops when full. Ask the genre question with
   `sort-puzzle` and `match-tile`; the user picks `sort-puzzle`.
2. `analysis/design.md`: the hook "Can you sort them all in one go?", a jar pop at about 12 s, a
   near-fail with one jar left, and a tease of a locked level 25 on the end card.
3. Upload three frames. Generate the plate (an image edit that removes jars, liquids and HUD), one
   transparent sheet of jars and the mascot, five SFX and a 30 s music loop, each via `recommend`,
   `model_schema_get`, `dry_run`, `model_run` with `wait=false`, and `jobs_wait`. Key the user's
   logo with `"key": true`.
4. Write the solver and the game from [references/archetype-sort.md](references/archetype-sort.md).
   Run `prep_assets.py`, then `build.py --networks all`.
5. `qa.py --speed 2` fails `idle_never_autoplays`: a demo pour moved `progress` before the first
   touch. Remove it, let the hand loop the pour gesture instead, and rebuild.
6. Open every `qa/story_*.png`: a banner covers the jar it describes. Move it to the top band.
7. Hand over the bundle ZIP with `notes.md`, and say which networks' own tools were run
   ([references/networks.md](references/networks.md)) and that the rest were tested only in fake
   containers.

## Common mistakes

- **An ad that plays itself.** A demo takes the move away from the viewer.
- **A dead waiting screen,** which fails `hook_moves_without_input` and looks broken.
- **A hint on the wrong spot.** The hand must point at a real good move from the solver or the level
  script.
- **Chattering sounds:** a tick per coin at 10 to 25 a second. One sound per event group.
- **Hard-coded near-fail text,** which lies to players who lost by a lot.
- **Copying recording glitches or platform UI,** or baked HUD numbers. Redraw numbers live.
- **Cutting a sheet by grid math.** Sprites cross the cells: use `"blob": n` and check `--blobs`.
- **Decorative buttons that look live.** Make them work, or make them a CTA.
- **Units or zeros the game never shows** on the end card.
- **An asset with no source frame** in the asset map.
- **Editing the studio's files in place,** or generating a piece they supplied.
- **Claiming a network passed** when only `qa.py` ran.

## Files

- Scripts, run by the agent: [scripts/asset_inventory.py](scripts/asset_inventory.py) (catalog the
  studio's own files), [scripts/prep_assets.py](scripts/prep_assets.py) (crop, cut out, key,
  compress, subset fonts), [scripts/build.py](scripts/build.py) (inline and package per network),
  [scripts/qa.py](scripts/qa.py) (Playwright QA in fake containers),
  [scripts/pack_glb.py](scripts/pack_glb.py) (a GLB into a JS include for three.js).
- Runtime, copied into each project: [assets/runtime/runtime.js](assets/runtime/runtime.js)
  (`window.PA`).
- Template game: [index.src.html](assets/template/src/index.src.html),
  [game.js](assets/template/src/game.js), [manifest.json](assets/template/assets/manifest.json),
  [intake.json](assets/template/intake/intake.json), [qa_bot.py](assets/template/qa_bot.py),
  [make_placeholders.py](assets/template/make_placeholders.py).
- OFL fonts with their licenses: [Fredoka](assets/fonts/fredoka/Fredoka-Bold.woff2)
  ([OFL](assets/fonts/fredoka/OFL.txt)), [Rajdhani](assets/fonts/rajdhani/Rajdhani-Bold.woff2)
  ([OFL](assets/fonts/rajdhani/OFL.txt)),
  [Lilita One](assets/fonts/lilita-one/LilitaOne-Regular.woff2)
  ([OFL](assets/fonts/lilita-one/OFL.txt)),
  [Orbitron](assets/fonts/orbitron/Orbitron-ExtraBold.woff2) ([OFL](assets/fonts/orbitron/OFL.txt)).
