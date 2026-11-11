---
name: scenario-game-ua-ads
description: "Use when making a finished mobile game user-acquisition (UA) video ad with Scenario at an exact length for TikTok, Reels, Stories, Meta feed, YouTube Shorts, or ad networks: from a one-line concept or the game's own screenshots, screen recording, gameplay video, characters, icon, or UI kit. Pin-pull, parking jam, match-3, swallow hole, evolution runner, stacker, draw to protect, odd one out, gacha, merge. Also hook, hand, HUD counter, end card. Not for ads from a product photo."
license: MIT
---

# Scenario Game UA Ads

## Overview

A UA ad that plays like gameplay: Scenario generates or adapts the board art and the motion, and
every piece of game UI is composited on top. The deliverable is the requested length and format at
final render quality, never a draft or a single clip. The test of every beat: a stranger who has
never heard of the game thinks "I really want to try this". For ads from a product photo, use
`scenario-video-ads`; for hook, CTA, or end-card variants of a finished ad, `scenario-ad-variants`.
Connection, discovery, and recovery follow `scenario`. If a sibling skill named here is missing from
your available skills, load it with `skill_get` (Scenario MCP) or ask the user to install it
(https://github.com/scenario-labs/skills#install); unattended, proceed from tool schemas and flag
the gap.

## Brief: ask once, then run

Ask in one round, then run without stopping:

- **Concept** or the game's core loop, and the **game name**. Invent a fictional name when none is
  given.
- **Platform and placement**. They fix the ratio, safe zones, recommended length, and sound
  ([platforms](references/platforms.md)).
- **Exact length** in seconds. Without one, use the placement's recommended UA length.
- **The game's own material**, all optional ([inputs](references/inputs.md)): screenshots, a screen
  recording or gameplay video, characters and items, the app icon, logo, or UI kit.
- Palette and **spend ceiling**.

With the game's own material, the ad must look and play like that game: boards built from its
screenshots, its characters on-model, its real icon on the end card. Invent gameplay only when the
user has none to give.

`dry_run` every paid payload before the first billed run, plus retakes; over the ceiling, cut takes
or ask. Unattended with no ceiling, stop at the plan and estimate.

## Quick reference

| Stage       | What happens                                                                      | Sibling                                  |
| ----------- | --------------------------------------------------------------------------------- | ---------------------------------------- |
| 1. Plan     | Ratio, safe zones, second-by-second timeline ([concepts](references/concepts.md)) |                                          |
| 2. Board    | One text-free still per mechanic at the delivery ratio, from the user's material  | `scenario-game-assets`, `scenario-image` |
| 3. Clips    | Final-quality takes from the still, or cuts of the user's footage                 | `scenario-video`, `scenario-seedance`    |
| 4. Logic    | Per take: timing, action crops, end frames, motion                                |                                          |
| 5. UI       | Hook, HUD, hand, bursts, effects, end card ([ui](references/ui-layers.md))        | `scenario-text-overlay`                  |
| 6. Assemble | One timeline at the exact length and canvas                                       | `scenario-video-assembly`                |
| 7. Sound    | A hit on every event, a separate music bed, mixed in assembly                     | `scenario-audio`                         |
| 8. Check    | Probe, levels, a 2 fps sheet, the reject list                                     |                                          |

## Length and format

| Length | Setup or fail              | Payoff                     | End card |
| ------ | -------------------------- | -------------------------- | -------- |
| 6 s    | none, hook over payoff     | 4.5 s                      | 1.5 s    |
| 10 s   | 3.5 s                      | 4.5 s                      | 2 s      |
| 15 s   | 5 s                        | 6 s                        | 4 s      |
| 20 s   | 5 s                        | 6 s, then a 5 s escalation | 4 s      |
| 30 s   | two rounds of fail and win | or three escalations       | 4 s      |

With footage, its own beats replace this split ([inputs](references/inputs.md)).

- Compose each ratio natively: generate the board at the delivery canvas (1080x1920 for 9:16,
  1080x1350 for 4:5, 1080x1080 for 1:1, 1920x1080 for 16:9). Never crop one ratio out of another.
- Plan the board still in the placement's bands: background only under the platform UI, the HUD and
  hook just below it, every key action in the safe middle. Overlays with text and every tap target
  (a pin ring, a lever) stay in the safe zone, clear of TikTok's right rail: measure the targets on
  the board still before any take, and regenerate a board that misses.
- Several placements: one board and one assembly run per ratio, from the same plan.

## Make the viewer want to play

A board that changes correctly sells nothing. Plan every concept around its fantasy (power,
cleverness, order, growth, rescue) and its **Fun** line in [concepts](references/concepts.md):

- The input reads within 2 s: the hand and the piece move together, and the game answers at once.
- Every input gets a satisfying reaction in the motion itself: anticipation, contact, reaction. A
  piece wobbles on an edge, tips, then drops with a spin; a stack sways and settles. Write it beat
  by beat in the clip prompt.
- Show a limit, then overcome it: a too-big object rattles across the rim until the hole grows.
- What the fantasy rides on (a ball, a car, the hole) reads at phone size: about 4% of the frame
  width or more, with a trail when it moves fast. A growing subject follows a size curve planned per
  beat, and the camera pulls back so it stays about a third of the frame.
- Escalate: each beat bigger or faster than the last, a near-fail, one clever move nobody expected,
  then the biggest moment near gameplay's end.
- Never simplify the mechanic until the model cannot break it. Build a rich one in chained stages:
  one state still per step, each edited from the last, each take pinned from one state to the next
  with one visible move. Or script it from cut pieces (below).

## Rules that carry the ad

- The first frame holds the premise: board, hook line, stakes. A sound at 0.0, motion by 0.3 s, no
  logo intro.
- Never let a board or video model draw text, numbers, gate values, buttons, or the hand into a
  still or a take: leave the slots blank and composite them.
- One mechanic, escalating. Counters only climb, in 4 or 5 visible steps, each proportional to the
  event that causes it: one pickup never jumps a level from 30 to 99.
- A fail tease is two takes from one still: the wrong move and its consequence, then the right move.
  Cut on a burst word.
- One locked camera per take, at final quality. No push-in over a busy board: pipes, gates, and
  slots warp. Ask for a longer take and keep the clean first part.
- The game logic must hold; players spot a cheat at once:
  - Video models ignore barriers: lava and coins flow through a closed pin. Design one visible move
    per path, with no pin, gate, or wall the take does not open.
  - Prefer straight drops and straight lanes. A pipe or a bend invites a shortcut outside it.
  - Every player move needs a reason on the board: a swipe reaches a collectible or dodges a hazard.
    Collectibles in one line make the swipe pointless.
  - Name every barrier's state in the prompt ("coins stay inside the glass") and what stays still.
  - A fixed end state is its own still, edited from the board with the same counts, pinned as the
    take's last frame. Pinning also locks the camera. Mask only what changes: a prop inside the mask
    can be redrawn. An edit can also change pixels outside it: paste only the masked region onto the
    source.
  - A precise move a model cannot do cleanly (a two-piece swap, a free drop) is built as layers from
    the still; the model animates only the consequence.
  - A barrier drawn locally over a generated take (a drawn line, a patch) gets a mask check inside
    it on every frame: bees sat inside a drawn dome for 74 frames.
  - A board whose every move must be exact (tile match, sort, merge, screw puzzle) is scripted
    whole: cut the pieces from the board still or the user's screenshot and animate them as layers.
    A video model adds only ambient motion behind them.
- Assembly runs on `model_scenario-compose-video`, Scenario's one deterministic compositor, so its
  id is fixed (confirm with `search`).
- Anything that moves on the UI layer is one transparent ProRes 4444 `.mov`, cropped to its motion
  box, never stepped image layers or WebM alpha ([ui](references/ui-layers.md)).
- Sound: a hit on every visible event (tap, impact, pickup, counter step) on its frame, louder than
  the music. A video-to-audio pass on the silent cut adds incidental sound but misses events.
  Generate the bed separately, banning ambient pads, and shift it so its lift lands on the payoff.
- Compose takes at most 50 layers (49 audio, so premix a dense run of hits into one stem) and has no
  limiter, so assembly runs in passes:
  - picture: clips and overlays, muted, into a silent master;
  - sound: the silent master as the one video layer under every audio layer, times to the
    millisecond;
  - loudness, only when the sound pass misses -16 to -14 LUFS or peaks above -1 dBTP:
    `model_scenario-audio-extract` with `normalizeLoudness: true`, then the silent master plus that
    one track. Scenario ships one tool for each of these jobs, so the ids are fixed.
- End on the payoff, then an end card designed in the plan, like the hook, from this game's world:
  its level-complete screen with the label where "next level" sits, the next harder board frozen
  under "CAN YOU SOLVE IT?", or the hero carrying the label. Words from the game: SAVE HIM, DIG NOW,
  TRY LEVEL 2 ([ui](references/ui-layers.md)). Social feeds ban fake buttons, so the call to action
  is a label there; a button only on clickable ad-network cards.

## Scripts

The agent runs these locally with Python 3.11+, Pillow 13, numpy 2, and ffmpeg. They render and
plan; uploads and compose runs stay MCP calls. Each takes a JSON spec; `--help` lists its fields.

- [render_tracks.py](scripts/render_tracks.py): renders the hand, counters, rewards, bursts, and
  stars as cropped ProRes 4444 tracks, plus `layers.json` with compose-exact times and safe-zone
  warnings.
- [build_passes.py](scripts/build_passes.py): `simulate` mixes the cue sheet locally and prints
  loudness, true peak, and each hit's margin; `picture` and `sound` write the two compose payloads.
- [check_master.py](scripts/check_master.py): on the downloaded master, checks canvas, length,
  loudness, true peak, dark frames, a 2 fps sheet, and each hit's onset (`--sim` reads them against
  the mix).
- [put_parts.py](scripts/put_parts.py): PUTs a file to the signed S3 part URLs `upload_asset`
  returned and prints what `upload_asset_complete` needs.
- [check_take.py](scripts/check_take.py): the logic checks on each take before assembly; `motion`
  needs a locked camera.
- [make_patch.py](scripts/make_patch.py): builds a clean-plate image layer that hides a static piece
  contradicting the count, and checks every take it covers.

## Worked example: pin-pull rescue in chained stages, 15 seconds, TikTok 9:16

1. Plan: 1080x1920, TikTok safe zone, HUD from y 280. Hook over the wrong pull: gold melts in the
   lava, FAIL at 2.5 s, rewind. Water pin at 3.8 s sets the lava into a stone ramp under a punch-in;
   gold pin at 5.8 s; cell pin at 8.3 s, the miner runs up the ramp into the cart. End card 11.2 to
   15 s.
2. Board: `recommend` an image model for polished casual game art; if two rank close, run both on
   one prompt and keep the better. Glass chambers, text-free: water and gold on golden pins, lava
   below, the miner locked beside it, an empty cart. Then one state still per step, each edited from
   the last: stone ramp, gold in the cart, miner in the cart.
3. Clips: `model_schema_get`, then one run per step with `wait: false`, final tier, first and last
   frame pinned to consecutive states, one visible move each. The fail take starts from the board.
   Then `jobs_wait` every job id, retrying `pending_job_ids`; a `parallel-custom-jobs` 429 created
   no job: relaunch it after the wave (`scenario`).
4. Logic, with `check_take.py` on each take, never frame by frame: `sheet` for timing;
   `action --at 4.5 --box 270 600 540 540` tiles crops of the water hitting the lava; `ends` for
   counts; `motion --allow` the chamber boxes flags anything else moving. Nothing passes a closed
   pin or the glass, steam included.
5. UI with `scenario-text-overlay`: hook, level badge, counter values, FAIL, RESCUED!. The end card:
   the full cart rolls in with the icon on its side, the next miner locked behind, under a "FREE HIM
   NEXT" label. `render_tracks.py` renders the hand on each ring, coins flying to the counter, and
   the stars.
6. Picture pass: `build_passes.py picture` lays the takes at their frame times, muted, overlays
   above, 15 s long.
7. Sound pass on the silent master: hits on each pull, the melt, the steam, the coins, each counter
   step, the leap, and the end card; the bed with its lift on the payoff. Run `simulate` first and
   trim until the peak sits near -1.8 dBTP.
8. Check: `check_master.py --sim`, then the reject list on one tiled crop sheet per action.

## Reject list

- A beat where the board changes with no readable player input, or an input with no satisfying
  reaction.
- Anything passing through a closed pin, gate, wall, glass, or floor, or leaving its container,
  judged on tiled native-resolution crops of the action, never a downscaled sheet.
- Anything moving that the beat does not move: a crowd reacting in unison, a second copy of the
  hero, a piece shifting elsewhere (`check_take.py motion`).
- A hand gesture with no matching action, an action with no gesture, or a count that contradicts the
  screen.
- A win that leaves a piece on the board ("cleared" with one car still parked), even half under the
  HUD.
- A timer or meter faster than real seconds.
- A character or item off-model against the user's assets, or a board that no longer matches their
  screenshots.
- UI outside the placement's safe zone, overlapping elements, or HUD digits under 72 px on 1080
  wide.
- A black frame at a cut: the end card starts exactly when the last clip ends, with no fade.
- An end card another game could carry: the same layout and "PLAY NOW" from ad to ad.
- The board shifting between takes, or pieces warping near a take's end: trim earlier, and prompt
  pinned takes to settle a second early (steam gone, pieces still).
- An event with no hit, a hit more than 0.1 s off its frame, a quiet first second, or a peak above
  -1 dBTP.
- A counter step, reward, burst, or star with no event on screen to cause it.

## Common mistakes

- A label fixed to a moving object slides off it. Keep it to the static second or use the HUD.
- Scaling a full-canvas overlay in the compose run: it scales from the corner and can leave the
  frame. Render it at final size.
- Naming a real game, studio, or character in invented gameplay, or letting an archetype drift into
  one: an angry driver came back in a red cap, mustache, and blue shirt. Name an original look and
  check the still before animating. A take flagged for IP: reword it generically and rerun; flagged
  again, build that beat as layers from the stills.
