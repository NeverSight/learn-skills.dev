---
name: video-edit-pipeline
description: >
  MASTER orchestration skill for producing a finished short-form video from raw
  talking-head footage. Use for ANY request to edit, produce, recut, or "make an
  ad/reel out of" talking-head footage — with or without a style reference —
  including "edit this video", "edit this like the reference reel", "turn this
  clip into a finished reel", "do the full edit", "make this look like their
  winning ads", or a revision request on a previously delivered edit. It routes
  every stage to the right specialist skill (reel-style-clone, branded-ad-edit,
  reel-recut, arcads-video-edit, recap-video, talking-head-image-overlays, hook-splitter,
  sound-design, ai-audio-sound-design,
  video-qa, video-review-canvas, edl-tighten, hook-variations, naming-convention,
  capcut-export) and
  owns the intake → style → edit → QA → deliver → revise loop end to end. Do
  NOT use for plain captions on untouched footage or single generated clips.
---

# video-edit-pipeline — master orchestration

You are running the proven end-to-end pipeline that turns raw talking-head
footage into a finished, reviewed, shipped short-form video. This skill does
not do the editing itself — it sequences the specialist skills and enforces
the working culture that made past edits ship: **verify pixels and dB, not
intentions.**

## The pipeline at a glance

```
(0) Intake ─→ (1) reel-style-clone? ─→ (2) branded-ad-edit build
                                              │
                        (3) sound-design ─────┤
                                              ▼
                    (4) QA loop (video-qa) → render → verify MP4
                                              ▼
                    (5) Deliver on video-review-canvas (URL first)
                                              ▼
                    (6) Revision rounds (notes → evidence → fix → new file)
                                              ▼
                    (7) Optional capcut-export handoff
```

Work the stages in order. Skipping a stage is allowed only when the user
explicitly says so (e.g. "no sound design", "just render, no review page").

---

## Stage 0 — Intake

For an existing media project with `project.json`, run
`python3 <pack>/tools/editor/editor.py project resume <project>` first. It reports source
changes, the next stage, the current render and outstanding review notes. Reuse those decisions
instead of repeating intake. The command is read-only unless `--run` is explicitly added.

Collect before anything else:

1. **Footage** — path(s) to the raw file(s). Expect them in the **projects
   directory** named in `MASTER_CONTEXT.md` (or `footage/` in a standalone setup) —
   never move media into this pack. Run `ffprobe` on every file immediately:
   resolution, fps, duration, audio channels. Do not assume; probe.
2. **Optional reference reel** — a file or URL of an edit whose style should
   be cloned. If present, Stage 1 is mandatory.
3. **Brand / site** — brand name, website URL, logo, palette if known. Check
   `MASTER_CONTEXT.md` at repo root first; it may already have palette, fonts,
   voice, and defaults. Ask only for what is missing and load-bearing.
4. **Target ratio** — default 9:16 unless the user or MASTER_CONTEXT.md says
   otherwise. Confirm ratio before storyboarding; a ratio change late in the
   build invalidates every crop and card position.

Create a working directory per project under the projects directory
(`<projects dir>/<project-slug>/`; default `outputs/<project-slug>/` here) and keep
every intermediate there: source copy, transcripts, spec/EDL, comp, `output-vN.mp4`
masters, `review/`, `_qa/`.

Create durable state with `editor.py project init <project> --source <file> --lane <lane>`
after choosing the lane below. Pass `--style <guide>` when an existing reference guide is
selected and `--sound` when generated sound design is part of the request. Record each
completed stage using `project checkpoint <project> <stage> --artifact <file>`; stages are
ingest, style, edit, sound, qa and review. Checkpointing records actual file hashes and
invalidates downstream work when inputs change. See
[project tools](references/project-tools.md) for commands, optional-stage handling and
the shared footage catalog. These receipts add no user approval gates.

5. **Which lane.** Decide from what was handed over, before Stage 1:
   - a **single talking head + a brand** → Stages 1–7 below (branded-ad-edit).
   - the creator's **own signature reel look** (banner, karaoke captions, callouts,
     silence-cut pacing) → **reel-recut**, then Stages 4–6.
   - **multi-take screen + camera + mic recordings** (a product demo read line by line)
     → **arcads-video-edit** (EDL base cut the reviewer locks, then its graphics pass).
   - **event/conference/travel recap with spoken takes and supplied B-roll** →
     **recap-video** (per-line take selection, exact base cuts, matched footage,
     split/full layouts and revision-safe timing), then Stages 4–6. Its workflow
     owns the build and sound choices; do not also run branded-ad-edit or require
     new intermediate approvals when the user requested a finished first cut.
   - **one long recording of many hooks/takes** → **hook-splitter**; an approved body
     that needs many openers → **hook-variations** (Stage 6b).
   - **AI-actor / generated footage that sounds sterile** → **ai-audio-sound-design**
     (audio-only; the picture is untouched).
   - an **uncut take carrying stacked image overlays** (nothing is cut; a title
     plate, found-footage rects above the eyeline, opaque skeleton-UI cards that
     build themselves, word-by-word karaoke, a CTA banner that lands early) →
     **talking-head-image-overlays**, then Stages 4-6. Note this lane INVERTS the
     usual base cut: it keeps ~15% of runtime as pauses instead of removing them,
     and ships no SFX or music at all.
   Check `MASTER_CONTEXT.md` § Hard rules first: it says which regime the reviewer
   holds you to (face rule, full-screen takeovers, approved-copy cuts).

## Stage 1 — Style clone (only if a reference exists)

Invoke **reel-style-clone** on the reference reel. Its job: reverse-engineer
the reference frame by frame into a `STYLE-GUIDE.md` (pacing, framing grammar,
caption treatment, card style, color, sound character) plus concrete build
directives.

- The style guide is the contract for Stage 2. The storyboard must cite it.
- If no reference exists, skip to Stage 2 and use the house defaults from
  `MASTER_CONTEXT.md` plus branded-ad-edit's own framing grammar.

## Stage 2 — The build (branded-ad-edit)

Invoke **branded-ad-edit** and run its phases in order:

1. **Ingest + crops.** Produce **two crop candidates** for the talking head:
   - a straight zoom crop, and
   - the **blur-pad band trick** when the source is framed too tight to fill
     the target ratio (scale a blurred copy of the frame to full-bleed behind
     a fitted foreground copy, so the "bands" are blurred footage, not black).
   **Lesson from production:** reviewers often prefer the plain zoom crop over
   the clever blur-pad version. Always render a frame of BOTH and show both
   before committing the composition to one. Do not silently pick the fancy
   one.
2. **Transcribe** with whisper-cli (word timestamps). The transcript drives
   captions, card-per-line timing, and the storyboard beats.
3. **Storyboard from the style guide.** Every spoken line maps to a beat:
   card, full-bleed cut, B-roll (capture real screens with `broll-capture`; GENERATE clips/overlays with `openart-broll` (MCP) or `arcads-broll` (REST)), or breather — per `STYLE-GUIDE.md` (or house
   defaults). Write the storyboard down before composing; it is the artifact
   the user approves.
   Give planned visual elements stable IDs and keep their expected output-time intervals
   in `storyboard.json`. Mirror their actual static schedules with `data-start` and
   `data-duration`/`data-end` in the composition. Run `qa:storyboard` before rendering to
   catch missing IDs or empty/mismatched schedules; run with `--video` after rendering for
   per-element contact sheets. This checks declared schedules, not JavaScript animation or
   visible pixels; inspect the rendered evidence against the storyboard.
4. **Compose.** Hand-authored composition (framing, cards, cuts, motion) +
   generated word-synced karaoke captions + SFX/bed placement markers.
   HyperFrames is the render engine (`npx hyperframes`, and make sure
   `npx hyperframes skills update talking-head-recut` has been run for
   fonts/gsap).

## Stage 3 — Sound design

Invoke **sound-design** to produce the audio kit:

- SFX for the composition's markers (whooshes, pops, hits — generated via
  ElevenLabs, `ELEVENLABS_API_KEY` from `.env`).
- A low music bed, style-matched to the reference track if Stage 1 captured
  one.
- Use the skill's mixing math for levels (bed well under the voice) and its
  audit pass to confirm every placed SFX actually exists and lands on its
  marker.

## Stage 4 — QA loop, then render, then verify

This is a loop, not a checklist. Order matters:

1. **hyperframes check** — must pass clean.
2. **ONE multi-timestamp snapshot** — capture a single batch of frames across
   the whole timeline (hook, each card, each cut, captions mid-word, outro).
   One batch, many timestamps; do not snapshot one frame at a time.
3. **LOOK at the snapshots with vision.** Actually inspect every frame:
   overlaps, cut-off text, wrong colors, captions colliding with cards, crop
   drift. Optional deeper pass: video-qa's Gemini-based layer
   (`GEMINI_API_KEY`) if configured.
4. **Fix → re-check → re-snapshot** until the frames are clean.
5. **Render** the MP4.
6. **Verify the rendered MP4 with video-qa** — run the engine:
   `npm --prefix tools/video-qa run qa:video -- --lane hyperframes --video <out.mp4>
   --edl <edl.json> --words <words-master.json> --words-are-output` (reel-recut lane:
   `--manifest <spec>.qa-manifest.json --words <source words>`). Read the report, open
   the inspection packets for anything HIGH, fix within the whitelist, re-render,
   re-run; max 3 rounds. The composition preview passing is NOT evidence the render is
   right — fonts, media, and audio can differ in the rendered file. Probe duration,
   spot-check frames extracted from the MP4 itself, and check audio levels in dB on the
   rendered file.

Nothing ships that hasn't been verified as rendered pixels and measured audio.

## Stage 5 — Deliver

Invoke **video-review-canvas** to publish the video to a here.now review page
(frame-accurate scrubber + timeline comments). Then reply to the user and
**LEAD with the canvas URL** — first line of the reply, before any summary of
what was done. Reviewers click the link; they do not read the recap first.

## Stage 6 — Revision rounds

When the reviewer leaves notes (or the user relays them):

1. **Read the notes back** via video-review-canvas (it can pull timeline
   comments per version). Enumerate every note; none get silently dropped.
2. **Screenshot the exact frame each note points at BEFORE fixing anything.**
   A note like "the card at 0:07 overlaps the face" gets a frame grab at 0:07
   from the current rendered file first — so you fix what the reviewer
   actually saw, not what you assume they meant.
3. Fix. For pacing notes ("tighten this", "drags here", "cut the dead air"),
   invoke **edl-tighten** — surgical silence/pacing cuts with a full timeline
   remap so captions, cards, and SFX stay synced. **Recap exception:** stay in
   **recap-video** and rebuild its line EDL/assembler and occurrence-aware time map;
   chronological removed-range helpers cannot preserve reordered or reused takes.
4. Re-run Stage 4 in full (QA → render → verify) on the new cut.
5. **Per-note QA table** — before delivering the revision, produce a table:
   one row per reviewer note, with the note, what changed, and the **evidence
   in the RENDERED file** (frame grab timestamp, measured dB, probed duration
   delta). "Fixed" without evidence is not a row.
   Canvas v2 can store replies, open/resolved state and paired before/after frame evidence
   on each stable note ID. Include prior versions in the canvas config so those links stay
   playable. Export/read back its JSON ledger and run `project import-review` to refresh
   the project snapshot; do not drop unresolved notes from older versions.
6. **New versions are NEW files** (`v2.mp4`, `v3.mp4`, …). Never overwrite a
   delivered file — the reviewer's timeline comments are anchored to it.
   Register each new file with `project render <project> <video> --version <version>` before
   checkpointing QA/review. Use `project approve` only to record an actual reviewer sign-off.
7. **Republish to the same slug** so the review URL stays stable; the canvas
   tracks versions.
8. **Patch a generated composition by unique block markers, then prove every block is
   still there.** On one round a range replace between two section comments (`// ---- TK5`
   … `// ---- TK4`) also deleted a third block that sat between them; `hyperframes check`
   passed, the render was clean, and a whole overlay (tiles + counter) was simply absent
   until the frame sheet showed the speaker alone. The checker cannot know what should
   exist. After any patch, grep the generated page for every element id the storyboard
   names (`grep -c '"#tk3g"' index.html`) and read the frame sheet against the storyboard,
   not just for defects. Same round, same lesson: two overlay windows 150 ms apart let the
   first one's banner re-show land inside the second; key an exit/re-show off the NEXT
   window's start, not a fixed offset after the current one's end. That covers every element
   two windows share (banner, backdrop field, PIP ring): one round shipped the second window
   on plain black because the first window's field fade-out outran the second's fade-in.

Repeat until sign-off. Production edits have taken 4+ rounds; that is normal,
not failure.

## Stage 6b — Variant batches (only when one cut spawns many)

If the approved cut is a **body** that now needs a set of alternate openers — "add all
these hooks to it", a hook A/B test, opener variants — hand off to **hook-variations**.
It joins losslessly (the approved body stays bit-identical), matches each hook's loudness
to the body, and verifies with AVFoundation rather than ffmpeg, because an ffmpeg-only
check cannot see the parameter-set mismatch that makes such a join play fine in ffmpeg and
freeze in QuickTime.

Any time a stage produces **more than two files a human has to choose between**, run
**naming-convention** before delivering. A folder of `render-final-v3.mp4` forces the
reviewer to open everything; the filename should carry the axes that vary. That skill also
covers verifying a subject label before baking it into 40 filenames — inherited labels from
an upstream cut list are evidence, not truth.

## Stage 7 — Optional CapCut handoff

If a human editor wants a final manual pass, invoke **capcut-export** to
export the layered composition into a CapCut draft (pyJianYingDraft venv).
Note honestly: this exporter is documented as work-in-progress — verify the
draft opens before telling the user it is ready.

---

## Routing table

| Need | Skill |
|---|---|
| Reverse-engineer a reference reel | reel-style-clone |
| The main build (crops, storyboard, cards, captions) | branded-ad-edit |
| SFX kit + music bed + mix levels | sound-design |
| 4-layer QA on comps and rendered MP4s | video-qa |
| Publish for review, read notes back | video-review-canvas |
| Silence/pacing cuts with timeline remap | edl-tighten |
| One body + many hooks → one video per hook (hook A/B batch) | hook-variations |
| Naming a batch of deliverables so the files say what they are | naming-convention |
| Spec-driven short-form recut style (the creator's own look, or a graphics-free raw cut) | reel-recut |
| Multi-take screen + camera + mic demo → EDL base cut → motion-graphics pass | arcads-video-edit |
| Event recap from spoken takes + supplied B-roll, split/full layouts and line-anchored revisions | recap-video |
| One long recording of many hooks → one tightened video per hook (+ gallery canvas) | hook-splitter |
| AI-actor footage: ambience, room reverb, bleeps, watermark whine, loudness master | ai-audio-sound-design |
| Uncut take + hard-cut image overlays on content nouns (title plate, inserts above the eyeline, skeleton-UI cards, early CTA banner) | talking-head-image-overlays |
| Layered export to a CapCut draft | capcut-export |

## Culture rules (apply at every stage)

- **Verify pixels and dB, not intentions.** A change is done when the rendered
  file shows it, not when the code contains it.
- Probe media with ffprobe before reasoning about it.
- One batched snapshot beats twenty single-frame grabs.
- **Many concurrent `<video>` players break caption gating.** With ~30 small clips playing at
  once (a "wall of my videos"), the rendered file showed every past caption stacked wherever the
  players were active, while plain sections were clean; five players rendered correctly. When a
  beat needs many clips playing together, pre-composite them into ONE video with ffmpeg `xstack`
  and keep the count labels as DOM text. Frame-tile the RENDER at the dense beats; the check pass
  does not see this.
- **Sorting a list of timed blocks invalidates every index into it.** A takeover list sorted by
  time left two blocks reading `TK[2]`/`TK[3]` — the wrong windows. Look blocks up by id.
- Show competing options (crops especially) as images, not descriptions.
- Every reviewer note gets evidence, every version gets a new file, every
  delivery leads with the review URL.
