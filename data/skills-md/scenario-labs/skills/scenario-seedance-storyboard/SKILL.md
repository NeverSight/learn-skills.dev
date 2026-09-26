---
name: scenario-seedance-storyboard
description: "Use when a Seedance video must hold continuous movement across shots: dance choreography, fights, sports, or any performance where limbs teleport, feet slide, or motion resets at every cut, or when turning a storyboard and character sheet into a multi-shot sequence that plays as one take. Keywords: storyboard to video, choreography, movement control, pose chain, timecoded shot script, first and last frame chaining, character sheet, multi-shot continuity, Seedance 2.5 and 2.0."
license: MIT
---

# Scenario Seedance Storyboard

## Overview

Prompted shot by shot, generated movement falls apart: limbs teleport, feet slide, and every cut resets the performance. So storyboard instead of prompting harder. What this delivers is continuous motion through the handoffs, not editorially distinct cuts: for cuts a viewer can feel, cut the delivered clip yourself with `scenario-video-editing`. Write a timecoded shot script, draw a character sheet and a numbered panel per shot, and hold one rule: every shot ends in the pose the next one starts from. Pinned boundaries leave nothing to reset, so the cuts play as one performance.

Connection and the core loop: the `scenario` skill; the Seedance parameter contract, conditioning traps, and sound lanes: the `scenario-seedance` skill; identity across stills and a reusable character sheet: the `scenario-consistency` and `scenario-identity-library` skills; a board or comic page that is itself the deliverable: the `scenario-storyboards` skill; splitting and rejoining shots: the `scenario-video-editing` and `scenario-video-assembly` skills. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Step        | What                                                                                           | How                                                                             |
| ----------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 1. Script   | timecoded list, cast and setting agreed first                                                  | per shot: number, size, angle, lens or move, action verbs, entry and exit poses |
| 2. Plates   | one image per performer who must stay recognizable, several angles; extras generic and unnamed | image model via `recommend`; one clean still of a real performer also works     |
| 3. Briefs   | one line per panel, coverage not pictures                                                      | master first, hold the axis, climb the size ladder, punctuate                   |
| 4. Panels   | one `model_run` per panel                                                                      | plates as references, light pencil line on bare paper, each at delivery ratio   |
| 5. Gate     | two passes per panel, then repair one panel                                                    | artifacts and differences, per [board-craft](references/board-craft.md)         |
| 6. Assemble | the approved panels into the board                                                             | `model_scenario-compose-image` at explicit coordinates                          |
| 7. Approve  | script, plates, board shown to the user                                                        | reshoot by panel number; unattended, record and continue                        |
| 8. Frames   | two or three photoreal key frames                                                              | same plates, delivery ratio; they set the delivered look                        |
| 9. Video    | one scripted run, or chained runs                                                              | Seedance `model_run`, one of the two lanes below                                |
| 10. Check   | the delivery is clean and carries its track                                                    | sample every half second, not only the cuts, and match each cut to its panel    |

Label each panel as a shot list does: number, shot size, angle, lens or camera move, then three action verbs. Arrange them as coverage, not twelve pictures: open on a master that sets the geography, hold one side of the axis so screen direction never flips, climb the size ladder, and punctuate with an insert or a reaction. Adjacent shots share an edge by construction: shot 3's exit is shot 4's entry.

Draw the board light: thin pale line on bare paper, the setting in two or three quick lines, no rendered environment. A board drawn as a competing picture is treated as one, and its markings render into the delivery as objects, which no prompt clause can clean. Drawn light, the same markings transfer nothing, so numbers, captions and arrows can all stay on the board a human reviews. What carries that is prompt wording, not drawing: declare the marks as the director's planning guides rather than prohibiting them, and pass the key frames as concept art so appearance has a photographic source. Both are in [video-prompt.md](references/video-prompt.md).

Panels are generated one at a time, so one bad panel costs one panel, and gated before any video run on two passes: an AI-quality score for artifacts, and a spot-the-difference against the plate. A board-level verdict is not the bar: panels average defects away.

File as you go: one collection per sequence, created before the first generation, holding plates, panels, repairs, board and video ([board-craft](references/board-craft.md)).

Stop for approval before the first video run, with the key frames shown alongside the script, plates and board, and invite a reshoot by panel number; unattended, record the assumption and continue.

## Two lanes

**One scripted run.** When the sequence fits one job's duration cap (30 seconds on 2.5 at authoring time), pass the plates, board and key frames as `referenceImages` and build the prompt to the seven-section shape in [video-prompt.md](references/video-prompt.md). One generation carries the internal cuts: the plates hold identity, the pose chain holds continuity. Name `aspectRatio`; it defaults to `adaptive` here, so a portrait board hands back a portrait video. Reference mode anchors frame one to the base state of the reference world (see `scenario-seedance`), so a sequence that must open on an exact pose belongs in the chained lane.

**Chained per-shot runs.** Past the duration cap, when each shot needs its own control, or when the sequence must open on an exact pose: render each boundary pose as a still, then run shot N with `image` = still N-1 and `lastFrameImage` = still N, so adjacent shots share a frame both sides agree on. This excludes `referenceImages`, so the stills are a shot's only identity, and N shots cost N+1 stills and N runs. Each run also has a duration floor (4 whole seconds on 2.5 at authoring time), so N shots cannot total less than N times it, and more cuts than that means fewer shots or more seconds. The disciplines and the repair path are in [references/chained-lane.md](references/chained-lane.md).

## Worked example: a 12-shot dance in one run

1. Write the script: 12 shots over 24 seconds, edge poses named, every exit matching the next entry. Show it to the user first; it is the cheapest place to be wrong; unattended, write it down and continue.
2. Generate one plate per character, then the 12 panels, then two or three photoreal key frames from the same plates. Upload anything local with `upload_asset` (see the `scenario` skill). Show the board and the key frames to the user before going further.
3. `search` with `target="models"`, `query="seedance"`, `public=true`. Hits rank by relevance, not generation, so scan them all for the newest non-deprecated member rather than the first: at authoring time `model_bytedance-seedance-2-5` (re-discover each session), which takes the most references and holds identity best. Then `model_schema_get` for caps.
4. `model_run` with `dry_run=true` and `parameters={"prompt": "<the timecoded script>", "referenceImages": ["asset_dancer", "asset_board", "asset_key1", "asset_key2"], "duration": 24, "resolution": "1080p", "aspectRatio": "16:9"}`; re-estimate after any change.
5. Re-run with `wait=false`, then `jobs_wait`, re-called with `pending_job_ids` on timeout. A timeout is not a failure and never justifies a second `model_run`.
6. Step through the cuts: both sides must agree in pose and match the panel. Then sweep the whole clip at two frames a second, because a leaked board marking can fade in part-way through a shot, so one sample per shot reports a false clean. `asset_display` returns a link for video, not frames, so pull them locally or with `model_scenario-video-to-image-seq` (a fixed id: Scenario's single deterministic frame-extraction tool, so discovery would only re-derive it). Expect fewer cuts than scripted: most handoffs render as camera moves, so cut the delivered take at the twelve scripted points.

## Common mistakes

- Prompting choreography as adjectives ("dances energetically"): timecoded verbs and edge poses survive generation; mood words do not.
- Naming the pose but not the position: in a two-character scene a mirrored boundary still breaks the cut as hard as a wrong limb.
- Scripting a character who leaves frame and returns, or a change made off camera, inside one run: whatever leaves frame is gone for the rest of that run, and no boundary check can catch what happened out of shot. Land departures, returns and state changes on a chained boundary still ([chained-lane](references/chained-lane.md)).
- Expecting a scripted run to open on a prompt-described pose: reference mode anchors frame one to the base state; exact openings are the chained lane's job.
- Delivering silence by default: ask for diegetic sound and rule out music, but name no instrument or genre, which is what triggers an audio refusal. `generateAudio: false` is the fallback, not the default.
- A script past the prompt's `max_length`, or timecodes past the duration cap: read both off `model_schema_get` before writing the script, since step 1 comes before discovery; an overrun is a 400, never a trim. Then send the run's scripted length as `duration`: its default is Auto (-1), which the schema defines only against a reference clip, so a timecoded script sent without it runs for an unstated length.
- Getting the ratios wrong: each panel must carry the delivery ratio, since a reframe moves the poses the chain depends on, and the composed board must land inside a 0.4 to 2.5 aspect ratio or Seedance rejects it as a reference and the run fails.
