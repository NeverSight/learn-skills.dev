---
name: moda-video-footage
description: >-
  Real footage into a film: index and search local clips, upload only the
  selects — an editable Moda timeline + mp4 out. Highlight reel, rough cut.
  Local lane.
argument-hint: "<footage folder> [target length + tone + priorities]"
allowed-tools: Bash(moda:*), Read
---

# moda-video-footage

<!-- moda:banner -->
**PREREQUISITE — load `moda-core` once per session** (step-0, write contract,
free/metered map). Already loaded? Skip ahead. If you cannot load it, the
non-negotiables: run `moda doctor --json` before anything; `moda brand list`
before creating; writes that pin a revision use your last read's — on
`stale_revision`, re-read and retry once (it heals); send the canvas link the
moment it exists; stuck or failed? `moda ask "<question>"` — free and fast,
never guess.
<!-- /moda:banner -->

## What this lane is

The user has REAL clips on disk — a shoot, a trip, screen recordings — and
wants a cut: a film, a reel, a highlight. Analysis stays local (Rushes, the
optional toolkit riding `moda rushes`, indexes and searches the footage on
this machine and uploads nothing); only the selects that make the cut are
uploaded, and the deliverable is always BOTH the editable Moda timeline and
the rendered mp4. Generating new footage is moda-video-clip's; motion over
designs and type is moda-video-motion's; this lane cuts what already exists.

Read references/footage.md before the first command — it is the whole
workflow with its invariants; references/otio.md carries the timeline
interchange contract the endgame rides. What follows is the shape, not a
substitute for either.

## Recipe — folder to film

1. **Toolkit check**: `moda rushes doctor --json`. Typed
   `rushes_not_installed` teaches the fix — `moda rushes install` (it states
   what it downloads first; sizes are multi-GiB). Can't install? Degrade
   honestly: pick selects by eye with your harness's own tools and skip to
   step 5 — say the selection was manual, never pretend an index ran.
2. **Index**: `moda rushes ingest FOOTAGE --project INDEX` →
   `moda rushes analyze INDEX` → `moda rushes status INDEX --json`. The
   project directory is persistent memory — keep it, reuse it across
   revisions, never wipe it to re-ask a question.
3. **Brief + probes**: one short exchange for target duration, tone,
   priorities. Then probe search quality with a few
   `moda rushes search INDEX "…" --top-k 8 --json` queries and
   `moda rushes show INDEX mom_… --json` — look at contact sheets and
   transcript evidence; captions can hallucinate and rank is not confidence.
4. **Choose**: `moda rushes highlight INDEX --target-minutes N` for the
   candidate pool (~2.5× the target, one per duplicate cluster — material,
   not a film), then `moda rushes select INDEX mom_… --name … --reason … --json`
   in play order, with exact rational trims via `--items` when a moment
   needs shaving. Reason at duplicate-cluster level; consume returned ids.
5. **Extract + upload**: `moda rushes extract INDEX sel_… --handles 2s --out
   SELECTS --json` (or upload whole originals when the folder is a few small
   files), `moda file upload` each select, rewrite the media map's `pending`
   entries to `uploaded` with the REAL returned asset ids.
6. **Timeline**: author `cut-v001.otio` and dry-run it first —
   `moda edit import CANVAS_REF cut-v001.otio --media-map media-map.json
   --dry-run` — against a canvas you created (`moda canvas create --category
   animation`); then apply the same command with `--yes` in place of
   `--dry-run` (replace mode clears the existing timeline, so it refuses
   unconfirmed). Read the fidelity report; surface every dropped/approximated
   item. New versions are new files — v002, v003 — never an overwrite of the
   only cut.
7. **Draft, look, iterate**: `moda export CANVAS_REF --format mp4
   --scope main_edit -o draft.mp4`, sample frames, judge against the brief.
   Small fixes are `moda edit apply` operations against a fresh read;
   a recut is the next `.otio` version.
8. **Deliver**: the live canvas link FIRST — the human always gets an
   editable timeline — then the mp4 and the `.otio` version file when the
   user wants an interchange copy for Resolve/Premiere.

Everything here is unmetered: indexing, uploads, import, export and
iteration are free, so iterate on the cut as much as the piece needs. A
music bed is an upload away (an audio track on the same timeline); a
generated score is moda-audio's lane.

## Boundaries stated plainly

- Rushes never uploads, never calls cloud inference, and needs no Moda
  account; Moda's cloud renders and exports and never reads local disk. You
  are the bridge, and selected media is the only cargo.
- The user chose uploads of SELECTED media — never bulk-upload the folder.
- Supported transitions and visual tracks import and render. Unknown effects,
  unpaired overlaps and resource limits decline by name in `validation.diagnostics`;
  relay them honestly. Never claim an unsupported edit exported without loss.
- An audio-only timeline does not export as mp4 — keep a visual clip on the
  cut.
- Full inference is Linux x86_64 and Apple Silicon; elsewhere use the
  media-only profile or the manual degraded path, and say which ran.

## Errors

Any typed error → moda-core's recovery reference. `rushes_not_installed` /
`rushes_update_required`: run `moda rushes install`, then re-run the SAME
command. `otio_import_rejected`: the fidelity items name each offender —
fix them (upload + rewrite `pending` entries; re-reference intermediates
with their own timings), never invent asset ids. `stale_revision` on an
edit: re-read and retry once — it heals.

## Make it recurring

The weekly cut from a growing folder → moda-automate; the finished film's
social variants → moda-social; a designed cover still → moda-image.

See also: moda-video — the family fork · moda-video-motion — type and
motion over the cut · moda-core — contract, recovery, everything Moda can do.

## References

| Doc | Load when |
|---|---|
| references/footage.md | ALWAYS before the first rushes command — the workflow, its caching/timing invariants, degraded paths |
| references/otio.md | before authoring or importing a timeline — media maps, fidelity report, exact-time discipline, OTIO vs edit ops |
| references/export.md | rendering the draft and final — scopes, ceilings, warnings |
| references/reading-and-verifying.md | the review loop; verifying without vision |
