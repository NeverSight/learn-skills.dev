---
name: ffmpeg
description: >-
  Use this skill for local FFmpeg/FFprobe media inspection, remuxing, transcoding,
  filtering, evidence-bounded video review, transcript-assisted editorial plans,
  edit decision lists, podcast/audio cleanup, rendering, and output acceptance.
  It emphasizes explicit stream selection, source preservation, build-aware commands,
  bounded evidence, and verified new outputs. Do not use it for libav API programming,
  opaque whole-video understanding, automatic publishing, rights clearance, DRM
  circumvention, professional broadcast/color certification, or HyperFrames-authored
  compositions; route those tasks to their owning capabilities.
license: MIT
compatibility: Requires ffmpeg and ffprobe for execution; exact filters, codecs, protocols, and hardware backends vary by build and version.
---

# FFmpeg Expert

Treat FFmpeg as a typed media pipeline and media editing as an evidence-driven workflow. Inspect the actual source, separate measurements from interpretations, make decisions reviewable, render to a new path, and verify at the intended boundary.

## When Not to Use

- Do not use this skill for libav API programming, opaque whole-video semantic understanding, automatic publishing, rights clearance, DRM circumvention, professional broadcast/color certification, or HyperFrames-authored compositions.
- Route online media or transcript acquisition to the owning source skill, semantic frame interpretation to a vision-capable reviewer, and platform upload/API work to the platform skill.

## Boundaries and Routing

- Use a YouTube/transcript capability to acquire online video or transcripts; return here only for local supplied media and transcript artifacts.
- Use HyperFrames for HTML-authored motion graphics or composition; use this skill to inspect and preprocess its media inputs or verify rendered outputs.
- Use the named platform skill for upload, publishing, account, or API operations.
- FFmpeg can extract bounded frames and audio segments but does not interpret their semantic content. Route visual interpretation to a vision-capable reviewer and preserve its observations as attributed evidence.
- Do not infer rights, consent, identity, intent, or whole-program meaning from technical metadata, sparse frames, silence intervals, or an unaligned transcript.

## Evidence Classes

Label consequential claims so unlike evidence is not blended:

- **Technical contract** — behavior documented by an official FFmpeg or standards source.
- **Observed artifact** — probe output, measured signal result, extracted frame, listened segment, or downstream test from this source/output.
- **Reproducible experiment** — exact version, input identity/generator, command, result, and limits.
- **Editorial heuristic** — a reversible judgment that requires human review, not a fact established by FFmpeg.
- **User requirement** — the requested output contract, preservation policy, and acceptance threshold.

## Media Editing Loop

1. **Intake.** Confirm authorization and privacy boundaries; identify every source; use a private workspace copy of `templates/media-intake.json` to record probe evidence, timing, the output contract, preservation policy, and unresolved assumptions. Keep raw probe output and media in the restricted task workspace, and minimize any shareable derivative.
2. **Inspect.** Probe streams and format. Check required local capabilities with inventories or `scripts/ffmpeg-preflight`; never assume a filter, encoder, or hardware backend exists.
3. **Collect bounded evidence.** Extract only the frames, clips, waveform/signal measurements, or transcript spans needed for the decision. Record sample timestamps, count, byte/size limits, and the statement that samples cover sampled times only.
4. **Plan before rendering.** For editorial changes, write a reviewable EDL or podcast edit plan. Every consequential cut needs a source range, reason, evidence, confidence, treatment, mapping, and verification state. Leave ambiguous decisions unresolved rather than improvising.
5. **Render safely.** Make stream mapping explicit; prefer `-n` and a new output path; avoid untrusted shell concatenation. Distinguish keyframe-limited stream copy from decoded/re-encoded precise cuts.
6. **Verify in layers.** Check exit status, decodeability, output probe, stream/timing contract, bounded frame/audio evidence, editorial review, and the actual downstream consumer as applicable. Treat probe/decode success and destination acceptance as separate gates; a local file can pass the former and fail the latter.
7. **Accept or stop.** Use a private workspace copy of `templates/media-acceptance-report.md` to record pass/fail/blocked per criterion. A valid container or successful command alone is not acceptance.

Start technical inspection with:

```sh
ffprobe -v error -show_format -show_streams -of json INPUT
```

For shipped helper workflows, run the helper from the skill root with explicit output paths and limits; treat its JSON result as a report to verify, not as acceptance by itself. When using `extract-review-frames`, pass timestamps as separate values (`--timestamps 0 5 9`), not one comma-separated value.

## Route to the Focused Reference

### Evidence-driven media work

- Read `references/media-intake-and-manifest.md` before handling supplied/generated media, sensitive material, multiple sources, or a defined delivery contract.
- Read `references/video-inspection-and-visual-evidence.md` when extracting or reviewing frames/clips, choosing samples, or making visual claims.
- Read `references/editorial-video-editing.md` for transcript-assisted selection, sequencing, pacing, transitions, overlays, and reviewable editorial decisions.
- Read `references/audio-and-podcast-editing.md` for podcast cuts, signal cleanup, silence/noise analysis, loudness measurement, and listening gates.
- Read `references/ffmpeg-edit-decision-lists.md` before creating, validating, or turning an EDL into a command plan.
- Read `references/media-verification-and-acceptance.md` before declaring an output complete or compatible.
- Read `references/media-failure-modes.md` when evidence is contradictory, a cut drifts, a filter is missing, review samples are sparse, or a workflow repeatedly fails.
- Read `references/media-research-source-index.md` when supporting claims, refreshing version-sensitive guidance, or recording a technical experiment.
- Read `references/editorial-workflow-example.md` when proving that intake, evidence, EDL, rendering, and acceptance artifacts compose end to end on a synthetic fixture.
- Read `references/synthetic-media-fixtures.md` when a change needs bounded real-media fixtures for cuts, cadence, concat, audio, subtitles, or visual-boundary sampling.

### Core FFmpeg work

- Read `references/core-model-and-command-anatomy.md` for containers, streams, codecs, option scope, mapping, copy/transcode, and timestamps.
- Read `references/filters-and-transformations.md` for filtergraphs, labels, audio/video processing, and incremental graph debugging.
- Read `references/intermediate-workflows.md` for seeking, trimming, concat, metadata, subtitles, batching, pipes, and streaming.
- Read `references/advanced-operations-and-safety.md` for hardware acceleration, synchronization, reproducibility, network safety, and failure boundaries.
- Read `references/command-cookbook.md` only after inspection and capability checks; every recipe is conditional.
- Read `references/learning-summary.md` for the newcomer-first mental model.
- Read `references/source-inventory.md` for the original FFmpeg source survey and `references/local-verification.md` only for its explicitly host-specific FFmpeg 8.1.2 observations.

## Templates

- `templates/media-intake.json` — source identities, probes, contract, privacy, preservation, assumptions
- `templates/edit-decision-list.json` — reviewable source ranges and treatments
- `templates/video-inspection-report.md` — technical inspection and bounded evidence ledger
- `templates/visual-review-packet.md` — attributed frame/clip observations and coverage limits
- `templates/vision-review-observations.json` — parseable attributed observation block for a prepared packet
- `templates/podcast-edit-plan.md` — mechanical, signal, and editorial audio decisions
- `templates/media-acceptance-report.md` — layered verification and criterion verdicts
- `templates/media-acceptance-contract.json` — machine-readable stream, format, evidence, loudness, and downstream requirements
- `templates/target-compatibility-manifest.json` — one named target, sourced requirements, technical constraints, and downstream lane
- `templates/research-experiment-record.md` — reproducible version/command/result record

Run `scripts/editorial-workflow-example` in a new or empty task-local directory when a reproducible synthetic integration proof is required. Its `PASS_WITH_UNVERIFIED_BOUNDARIES` result is deliberately narrower than editorial or destination acceptance.

Run `scripts/generate-media-fixtures` when tests need deterministic non-personal media. Keep its generated binaries and manifest in the task workspace; commit the generator and assertions, not the outputs.

Use `scripts/render-edl` for a non-executing single- or multi-source plan. Default to decoded concat-filter assembly; select concat-demuxer stream copy only with matching probe-derived signatures and verified packet/keyframe boundaries. Unsupported transitions must remain explicit errors.

Use `scripts/audio-inspect` for bounded silence, EBU R128, peak/clipping, and transcript-alignment evidence. Request each measurement explicitly, preserve unavailable filters as `UNAVAILABLE`, and treat every interval or transcript range as a listening-review candidate. Its optional report output refuses overwrite.

Use `scripts/media-verify` with a declared acceptance contract, output FFprobe JSON, and optional evidence JSON. It reports every criterion independently as `PASS`, `FAIL`, `BLOCKED`, `UNVERIFIED`, or `NOT_APPLICABLE`; only a report with no failed or missing required evidence is an overall pass.

Use `scripts/target-compatibility` when acceptance names a real player, editor, host, archive, or service. Keep sourced technical requirements and local probe results separate from evidence produced by that exact consumer; a pass applies only to the named target/version.

Use `scripts/vision-review-handoff` to prepare bounded, privacy-safe frame packets for an authorized human or vision reviewer. Import only attributed reviewed observations with `scripts/import-vision-review`; treat proposed editorial consequences as evidence for review, never automatic decisions.

Copy a template into the task workspace and replace its placeholder/example values. Do not put private paths, media, transcripts, or review evidence in the public skill repository.

## Non-Negotiable Checks

- Make stream selection explicit whenever multiple inputs/tracks or a complex graph are involved.
- Treat option order as significant: options generally apply to the next input or output.
- Do not call silence useless; `silencedetect` reports threshold crossings, not editorial value.
- Claim loudness, clipping, timing, or keyframe status only from an available measurement method and retain its output.
- A transcript is evidence only for its text and supplied timing quality; spot-check alignment against media before frame-accurate edits.
- Stop for review when evidence is sparse, ambiguity could remove meaningful content, an optional tool/filter is absent, privacy/authorization is unclear, or two materially different approaches fail.

## Completion

Finish only when the requested artifact exists at a new path, required probes and bounded reviews are recorded, the output has been exercised at the relevant downstream boundary, and every acceptance criterion is passed or explicitly blocked. Report untested claims and remaining assumptions instead of filling gaps with plausible output.
