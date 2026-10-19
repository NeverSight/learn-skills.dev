---
name: scenario-seedance-drafts
description: "Use when exploring several Seedance video takes before paying for a final: cheap 480p previews, variations of one shot to compare, reviewing and ranking takes before a pick, or finalizing a chosen preview to 1080p without regenerating it, including within its 7-day window. Keywords: Seedance draft, draft mode, draft complete, finalize, 480p preview, variations, takes, review, rank, pick, Seedance 2.5."
license: MIT
---

# Scenario Seedance Drafts

## Overview

A Seedance draft is a 480p preview of a take that can later be finalized to 1080p without
regenerating it: the completion is the same take at full resolution. Seedance has no seed, so a
draft is the only way to approve a take cheaply and then ship that exact take. Re-running the
payload at 1080p performs it again differently, and a generic upscaler returns a softer copy, not
the 1080p render.

The economics decide when to draft. A draft prices like a plain 480p render, and a draft plus its
completion costs at least a direct 1080p render: at authoring time 2,040 against 2,024 CU for a 15
second edit (366 plus 1,674), and 544 against 456 for a 4 second reference shot (84 plus 460).
Drafting pays only through the takes that get discarded: five 15 second takes and one finalist came
to about 3,500 CU, against about 10,100 for five 1080p renders. A single take costs more drafted
than rendered.

Seedance modes, conditioning and sound: `scenario-seedance`. Connection and the core loop:
`scenario`. Music over the finals: `scenario-video-assembly`. If a sibling skill named here is
missing from your available skills, ask the user to install it
(`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and
flag the gap.

## Quick reference

| Step     | Call                                                                          | What to know                                                                                                                                                      |
| -------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Discover | `search`, `target="models"`, `query="seedance"`, `public=true`                | `model_schema_get` the newest member: `draft` is a boolean there (2.5 at authoring time), and `resolution` is ignored while it is on                              |
| Draft    | `model_run` with `"draft": true`, `wait=false`                                | One call per take: no seed and no batch-count field, so repeat the identical payload. Set `duration` to the shot (Auto priced the 30 s cap); edit mode takes `-1` |
| Wait     | `jobs_wait` with every job id                                                 | 15 s edit-mode drafts took 7 to 8 minutes; re-call with the returned `pending_job_ids`                                                                            |
| Review   | `asset_download`, then local contact sheets and close-ups                     | See Reviewing takes                                                                                                                                               |
| Finisher | `search`, `target="models"`, `query="seedance draft complete"`, `public=true` | Its one input is `draftVideo`, a scalar file                                                                                                                      |
| Complete | `model_run` with `draftVideo` set to the draft job's asset id                 | `dry_run` first; took 1 to 3 minutes. `asset_get` reports an H.264 MP4, but `asset_download` returns the original MOV (HEVC in one run): compose by asset id      |
| Verify   | `asset_get`                                                                   | 1080 wide, the draft's frame rate and duration                                                                                                                    |

A draft stays completable for 7 days from its creation. Record each take's asset id straight off its
`jobs_wait` row. Review copies made from a draft (a music version, a trim) are fine, but each is a
new asset: only that recorded id resolves to the draft task the finisher completes.

## Reviewing takes

Takes of one payload diverge exactly where shots fail, so review every one, never just the first.
Download each draft (inspecting a download is not editing it) and check, in this order:

1. **Sweep**: a contact sheet over the whole clip (`ffmpeg -vf "fps=2,scale=150:-1,tile=10x3"` fills
   it for a 15 s clip; raise `fps` on shorter ones), one per take, stacked per variant. It catches
   identity swaps, wrong wardrobe, broken backgrounds, extra or missing props.
2. **Close-ups where generators fail**: hands in fast moves (gloved fingertips turned glowing red in
   two of three takes of one batch), long hair through turns, the face at four moments, and every
   prop the brief fixes, counted against its reference (one take stacked a second jack-o'-lantern on
   a one-lantern plate).
3. **Timing**: when a source clip exists, frames at four matched timestamps side by side.

Sheets at this size cannot rule out a fault, only find one: crop before judging fingers or faces.
Pixel counting is a weak substitute: a red-pixel test for the glove fault also fired on warm candle
light in an empty plate, so it ranked nothing. Sampled frames also miss motion faults: a ponytail
problem visible at speed passed every sheet. So rank per variant, give each defect a timestamp, say
what each take was and was not checked for, and have the user watch the finalists at speed before
paying for completion. Unattended, complete the top-ranked take that meets the brief's acceptance
criteria and report the checks it did not get.

## Worked example: five takes, one 1080p final with licensed music

1. Discover and read the schema as above. `dry_run` the exact payload twice: with `"draft": true`,
   and at the delivery `resolution` without it. Quote both with the arithmetic (N drafts plus one
   completion, against N finals).
2. The music is laid afterwards, so `generateAudio: false`. Launch five identical `model_run` calls
   with `"draft": true`, the shot's `duration` (in edit mode `-1`, which follows the source clip)
   and `wait=false`. A 429 `parallel-custom-jobs` creates no job: keep the launched ids, and launch
   the refused takes as earlier ones finish, within `actionLimit` per the `scenario` skill.
3. `jobs_wait` with every launched job id; record each row's asset id as that take's draft id.
4. Review as above. Present the ranked takes with their links and the defects found, then wait for
   the pick (unattended: the brief's acceptance criteria pick).
5. Find the finisher, `model_schema_get` it, then `model_run` with `{"draftVideo": "<draft id>"}`
   and `dry_run=true`. Run it and `jobs_wait`.
6. `asset_get` the completion: 1080 wide, frame rate and duration equal to the draft's. Sweep it
   once more: the completion matched its draft on every sampled frame at authoring time, and that
   match is the proof it finalized rather than regenerated.
7. Lay the track on the completion with `model_scenario-compose-video` (a fixed id: Scenario's
   single timeline compositor): a video layer and an audio layer, both at `startTime: 0`,
   `durationMode: "custom"` at the clip's length rounded down to the field's 0.1 s step (a 4.04 s
   clip loses its last frame at 4.0), `canvasMode: "custom"` with numeric `canvasWidth` and
   `canvasHeight` set to the completion's size, and `fps` at its frame rate (the field defaults to
   30). Check the sync per `scenario-video-assembly`, then `asset_download`.

## Common mistakes

- Rendering the variations at the delivery resolution: every discarded take costs its full 1080p
  price.
- Re-running the chosen payload at 1080p, or upscaling the 480p draft: the first is a new take, the
  second a soft copy of the right one.
- Passing a music version, trim or re-encode as `draftVideo`: only the draft job's own asset is the
  draft.
- Letting the 7-day window lapse: an expired draft can only be regenerated, as a new take.
- Laying music on the drafts and completing those: the completion carries only what the draft
  generated. Review copies with music are fine; lay the delivery audio once, on the completion.
- Ranking from one look at the first take, or from contact sheets alone.
