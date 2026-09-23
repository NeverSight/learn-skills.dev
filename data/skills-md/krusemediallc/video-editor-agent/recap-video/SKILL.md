---
name: recap-video
description: >-
  Edit an event, conference, summit, trip, or behind-the-scenes recap from spoken
  takes and supplied B-roll. Choose the strongest take for each line, remove
  pauses and restarts, match footage to the narration, mix full-screen and split
  layouts, add captions and selective graphics, then render, verify and revise.
  Use for "recap video", "event recap", or "edit this summit like this reference";
  not for a text summary or a product screen-demo edit.
---

# Recap Video

Make the viewer understand the event and feel present: a clean spoken story,
specific visual evidence, creator cameos, and short bursts of energy. Build from
the supplied footage. Keep the original meaning and strongest complete delivery.

This is the recap lane of [video-edit-pipeline](../video-edit-pipeline/SKILL.md),
and may also be invoked directly. It owns take selection, B-roll grammar, base
assembly and timing. Reuse the pack's style, sound, QA and review tools where
needed; do not restart the branded-ad lane after selecting this one.

## Intake and working files

Read the pack's `MASTER_CONTEXT.md` for the projects directory, brand, sound and
review preferences. Collect the takes, B-roll folder, optional reference, ratio,
required talking points, and delivery destination. Use known answers; a request
for a finished first cut authorizes moving through the edit without a new
approval gate at each intermediate artifact.

Keep media in `<projects>/<slug>/`, outside the skill pack. Preserve originals;
record source IDs and download receipts privately. Useful working artifacts:

- `raw/`, `broll/`, `reference/`, `source.mp4` and a source-piece map.
- `transcript.json`, `edl-lines.json`, `_look/broll/catalog.json`.
- `storyboard.json`, `comp/`, versioned `base-cut-vN.mp4` and `output-vN.mp4`.
- `_cut_work/vN/` for EDLs, word maps and assembly evidence; `_qa/` and `review/`.

Use the available authenticated download route for supplied links. Ask only if
access or a missing source blocks the edit. Do not replace real event footage
with generated proof. Reference footage guides style; it is not automatically
cleared for inclusion in the new video.

## 1. Understand the material

Read [references/editing-workflow.md](references/editing-workflow.md) for ingest,
reference analysis, cataloging and line selection.

Probe all media, including rotation, frame rate, audio and color transfer. Analyze
the reference with [reel-style-clone](../reel-style-clone/SKILL.md) when supplied.
Separate what was measured from what the current brief requests: the user can
ask for splits, a faster montage or a better ending even when the reference has
none. Reference runtime is not permission to delete required content.

Catalog the B-roll with seek-based contact sheets and full-size checks. Record
subject, creator visibility, readable slide text, useful source intervals, crop
focus and restrictions. For a large library, delegate disjoint batches and merge
them by stable clip ID; verify every expected asset was actually covered.

## 2. Build and verify the spoken base

Transcribe each take, then choose the best complete delivery **per line**, using
mic quality, articulation, performance and semantic completeness. Record reasons
and alternate source ranges. Listen to each selected line with a transcription
pass prompted to preserve repeats, partial words and false starts. Ordinary ASR
often cleans these away.

Build one normalized mezzanine and a map back to the original takes. Use the
concat **filter**, normalize streams and reset timestamps; check a take-change
seam for sync. Read [references/assembler.md](references/assembler.md) and run
[scripts/assemble.py](scripts/assemble.py) on the selected lines. It preserves
list order, removes detected pauses, supports explicit `veto` cuts and `raw`
holds, and writes frame/sample-based cuts plus source/output word maps.

Review the base before decorative work. Check every restart, quiet word ending,
take transition and retained fragment. If the user requested a finished V1,
continue once the base passes this internal check. If they requested base-cut
approval first, deliver that stage and respect that scope.

## 3. Compose around the spoken story

Read [references/composition.md](references/composition.md) before building.
Write a shot table anchored to line IDs and source-time words, not only absolute
seconds in the current cut. Aim for an intentional visual for each sentence:

- Match a claim to the actual slide, speaker, demo or footage supporting it.
- Use full-screen B-roll over uninterrupted VO for proof and immersion.
- Use brief splits for speaker presence: B-roll top, creator bottom is the
  starting layout; change it if the brief/reference calls for another arrangement.
- Scatter lifestyle/travel/creator shots where they support self-reference,
  transitions or humor. Spend the fast montage on a relevant hook phrase.
- Use restrained phrase captions, a few emphasis stamps, a sequential takeaways
  build and a quote treatment only where the narration earns them.

Preserve the spoken audio as the continuous master; mute B-roll unless a specific
natural-sound beat is intended. Reuse cleared SFX before generating more. Follow
the user's sound preferences; a silent-bed reference and an optional music bed
are separate choices, not mandatory generation tasks. Use
[sound-design](../sound-design/SKILL.md) for asset/mix mechanics if needed.

For HyperFrames, use its installed composition contract, deterministic paused
timeline and registered media. Gate layout containers at mode changes so a
split panel cannot flash over a full-screen shot. Check HLG sources and render
mode before a full export. See the composition reference for the proven traps.

## 4. Verify, deliver and revise

Read [references/qa-and-revisions.md](references/qa-and-revisions.md). Use
[video-qa](../video-qa/SKILL.md) on the actual mastered MP4. Use the matching
version's EDL and both source/output words, including reordered/reused takes.
Use the occurrence-aware seam audit in the QA reference to adjudicate findings
and verify first/last retained edges. ASR timing alone does not prove
clipping, and an SFX attack can resemble a splice click. Preserve the engine's
raw verdict and document evidence for each adjudicated finding.

Check rendered captions, slide legibility, correct speaker identity, mode seams,
audio peaks and the final complete thought. A clean technical report does not
establish factual accuracy or permission to show restricted slides.

Use [video-review-canvas](../video-review-canvas/SKILL.md) when review hosting is
requested or a standing preference. Keep one review slug and new files per
version. For each note, capture the old frame/audio window, fix the source of
the issue, rebuild all affected timing, and record the new rendered evidence.
If the exact master is requested in a source folder, upload it and verify the
receipt, bytes and destination. Editing/review approval does not authorize social
publication, sharing changes or sending the video to a sponsor.

Deliver the requested review link or master first, then a short account of the
edit and any concrete unresolved points. Keep the reusable skill generic; retain
client names, footage, credentials, session URLs and private review details only
in the project's private records.
