---
name: video-director
license: MIT
description: Direct and produce finished videos using AI artwork with editable SVG foregrounds, real product UI, or procedural 3D. Use for explainers, product demos, launch films, Shorts and before/after studies needing readable visuals, timed annotations, smooth capture and a local review MP4. Not for an isolated image or ordinary website animation without a video deliverable.
---

# Video Director

Make the subject understandable, not merely animated. Choose the least complicated medium that shows the important action truthfully. This is a skill with bundled helpers, not a separate application or Python library.

## Brief and recipe

Establish subject, audience, duration, aspect, key action and delivery boundary from the request. Preserve approved voices, footage and current product positioning. Make minor reversible choices; ask about consequential missing choices, rights or costs. Creation does not authorize publication.

Show the interesting result early. Write short specific sentences: “See which page gets clicks,” not “Bring your workflow together.” Hold actual UI long enough to read. Establish the whole mechanism before explaining its parts.

Read only the relevant recipe:

- First run or dependency setup: [first-video.md](references/first-video.md), a self-contained SVG example with a locked runtime and export commands.
- Generated artwork + editable foreground: [hybrid-scenes.md](references/hybrid-scenes.md).
- Actual product UI: [real-ui.md](references/real-ui.md).
- Mechanisms and 3D: [3d-explainers.md](references/3d-explainers.md).
- Narration, pauses and music: [audio.md](references/audio.md).
- Runtime, capture and verification: [production.md](references/production.md).
- Matched comparison and runnable starter: [before-after.md](references/before-after.md).
- Optional MoneyPrinterTurbo CLI: [moneyprinterturbo.md](references/moneyprinterturbo.md), when automated footage/script/audio assembly fits.

Choose a fresh researched composition/palette when requested. Do not impose one channel's style on every film. Complementary colours can separate subjects, but labels and contrast must also work without colour cues.

## Production decisions

1. **Keep controllable things controllable.** Text, arrows, highlights, UI framing and factual geometry belong in SVG/HTML/canvas or 3D. Generated pixels are useful art, not exact UI or mechanical truth.
2. **Show the action.** Real clicks need a visible pointer and lead-in; real operations need their actual state/footage. Do not animate a screenshot as if a backend operation occurred. Name a part as its highlight appears; track its moving anchor.
3. **Stage attention.** One teaching action at a time. Ease camera moves, settle, then hold. Derive positions from absolute time, not accumulated frame deltas. Secondary motion must support the explanation. Linear rotation is correct for a constant-speed shaft.
4. **Compose for output.** A vertical version needs readable framing/label placement of its own, not an automatic landscape crop. Keep annotations clear of parts, other labels and platform overlays.
5. **Separate generation from assembly.** Save approved art and raw speech. Log prompts, sources, rights, settings and hashes. A timed-out generation may still have created a billed job; check before retrying. Resolve separately billed scope/cost before spending.
6. **Preserve review boundaries.** Use a new output folder, preserve masters/recovery files and refuse accidental overwrites. Stop before upload/publication unless separately authorized.

## Working helpers

These adapt the explicit-time capture, safe local serving, clip assembly and encoded-output checks used in the Pip productions. Resolve `<skill>` from this file's location. Run from the **video project**, not the skill folder. Read [production.md](references/production.md) first.

| Helper | Purpose |
| --- | --- |
| `scripts/create-example.mjs` | Copy a self-contained first project into a new folder; never overwrite. |
| `scripts/doctor.mjs` | Check dependencies and actually launch Chromium; no automatic installs. |
| `scripts/capture.mjs` | Local page → exact-frame silent H.264; retries at the same time; source hashes/error receipt. |
| `scripts/serve.mjs` | Loopback-only static server with ranges and path containment. |
| `scripts/compare.mjs` | Labelled side-by-side; reject duration/fps mismatch. |
| `scripts/audio.mjs` | Existing speech clips + explicit pauses → WAV and measured timing manifest. |
| `scripts/verify.mjs` | Probe/full decode/hash, all adjacent-frame statistics and encoded contact sheet. |
| `scripts/self-test.mjs` | Regression tests for helpers and overwrite protection. |
| `scripts/boundary-test.mjs` | Local browser-network and damaged-audio regressions. |

Requires Node, FFmpeg/FFprobe and project-accessible Playwright/Chromium; Three.js only for 3D. Helpers do not install packages/models, call providers, read credentials or publish. `assets/first-video/` is code-only and needs no external media. The comparison starter at `assets/comparison-study/` contains code and an asset manifest, **not** private screenshots, generated media, fonts or vendored Three.js.

## Delivery

Make a low-fps timing pass before final capture. Check the **encoded** duration, dimensions, fps, full decode, colour, readable keyframes and transition boundaries. Metrics support inspection; a large frame difference can be an intentional edit, while low differences can hide frozen animation. Look at the film and listen to speech. ASR and clean WAVs do not prove a natural voice.

Deliver a playable local MP4 and source path, with checks and omissions. Do not claim real-time 60 fps from offline capture, a historical result from a constructed baseline, or an independent agent test from the author's own run.

See [lineage.md](references/lineage.md) for inspirations and licence boundaries. Specialised installed skills may supplement this one; the workflow does not require loading all skills or copying upstream repositories.
