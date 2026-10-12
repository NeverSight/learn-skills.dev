---
name: scenario-ad-variants
description: "Use when making multiple independent ad or campaign edits from existing footage with Scenario: hook, CTA, copy, end-card, placement, or targeted visual variants. Also for revising one variant or resuming a partially completed batch. Not for a new commercial from a still image, ordinary single-clip grading, or automatic Cartesian combinations."
license: MIT
---

# Scenario Ad Variants

## Overview

One supplied source becomes an ordered set of independently specified edits. Preserve what the brief does not change, and keep every output traceable to the same source. A new storyboard from a product still belongs to `scenario-video-ads`; single-clip utilities to `scenario-video-editing`. Connection, discovery, submission and recovery follow `scenario`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

Resolve only missing decisions: source, requested variants, exact copy, destination, runtime, audio policy and spend ceiling. Reuse answers already supplied. Distinguish a controlled comparison, where only the agreed variable changes, from creative exploration. Never multiply options into a Cartesian batch unless requested.

## Quick reference

| Requested change                           | Route                                                   | What stays fixed                                       |
| ------------------------------------------ | ------------------------------------------------------- | ------------------------------------------------------ |
| Hook copy, CTA or end card                 | `scenario-text-overlay`, then `scenario-video-assembly` | Underlying footage, source audio and all other copy    |
| Cutdown, grade or placement                | `scenario-video-editing`, `scenario-formats`            | Agreed source intervals, sequence and focal subject    |
| Background, clothing or object replacement | `scenario-video` with a discovered video-edit member    | Unchanged identities, actions, timing and source audio |
| New shots or concept                       | `scenario-video-ads`                                    | This is new creative, not a source-preserving edit     |

Use deterministic operations when they satisfy the brief. In gameplay capture, replacing a background generatively can also change geometry, UI or mechanic behavior. Do not silently treat such output as faithful gameplay. If preserving those pixels is mandatory and the available route cannot isolate the edit, report the limitation before spending. A generative preservation prompt is a request to verify, not a guarantee.

## Source and variant records

Read `asset_get` for source dimensions, duration and frame rate; inspect the footage, its existing text, cuts and audio. Reference images have explicit roles: identity, product, style or replacement. Assign each variant a stable label and record its source asset, intended delta, invariants, exact copy, output specification and audio policy. Every independent variant starts from the source, never the last generated variant. A requested revision starts from the chosen variant when that is the user's intent.

Keep a compact local record of each variant's state: blocked, planned, submitted, pending, failed or verified; submitted job id; output ids; measured properties; QA outcome. Save the actual submitted payload, not just a prose prompt. A rendered output awaiting review is not verified. Retain completed variants and wait on pending jobs after interruption; a transport failure is reconciled through `scenario` before any resubmission. Retry only the affected failed variant within the remaining ceiling, keeping its original label. Changing the intended delta creates a revision, not an invisible retry.

For a generative edit, construct the prompt from the requested change, named reference roles, preserved identities/text/actions and the source timing. Use `recommend` with the need in the user's own words, then `model_schema_get` to establish supported video inputs, references, durations and audio controls. Never import another provider's duration or prompt-length limits. If the requested precision or media is unsupported, offer the nearest feasible route without promising equivalence.

## Worked example: three hook variants from gameplay

The brief supplies a 15-second gameplay clip with audio and requests exactly three 9:16 exports. The hook copy occupies seconds 0 to 2: "Hold the line", "One hit left", and "Can you survive?". The gameplay, audio, runtime and final end card must not change. The source already has a clear hook area.

1. `asset_get` the source, then inspect it. Check that its measured shape, runtime and hook area support the brief. If existing hook text must be removed from flattened footage, ask for a clean source or agree a covering panel. Unattended, use a panel only if already authorized and it preserves all required visible content; otherwise mark affected variants blocked on a clean source and continue any independent feasible variants. Do not spend on blocked variants or generate new gameplay to erase text.
2. Record variants A, B and C with the same source and invariants. Render three exact text cards through `scenario-text-overlay`, with matching geometry and styling so copy is the only changed variable. Upload the rendered cards through `scenario`.
3. Follow `scenario-video-assembly`: `model_schema_get` on `model_scenario-compose-video`, Scenario's single deterministic compositor. Each payload uses the same source video layer and its audio, plus its own card as an image layer at the agreed time. Set `canvasMode: "custom"` with numeric `canvasWidth`/`canvasHeight`, and `durationMode: "custom"` with `duration: 15`. Give the source layer string `width`/`height` matching the canvas and `fit: "contain"` to preserve the whole picture without stretching; different source ratios leave bars, and cropping requires authorization. Set the card's string `width`/`height`, explicit placement and `fit: "contain"`. Set `fps` from the measured source rate within the schema's whole-number range; disclose any required rounding. This compositor uses seconds in 0.1 increments; do not promise frame-exact timing beyond that contract.
4. Price each exact payload with `model_run` and `dry_run: true`. Fit submissions and any planned repairs inside the authorized ceiling. A quote is not payload or visual validation. Submit with `wait: false`, save each job id and use `jobs_wait`; pending jobs keep their ids.
5. Inspect every exported variant at the hook boundaries, throughout the gameplay and on the end card. Check the frames immediately before, at and after the requested endpoint: a timeline field does not establish whether the rendered endpoint is inclusive. Compare measured runtime and shape with the source. Check that audio stays synchronized and that the tail is intact. A succeeded job with a missing overlay fails. Report an endpoint mismatch instead of silently shortening the hook to hide it.
6. Deliver A, B and C in the requested order via `asset_display` and `asset_download`. Include the variant map and measured properties. Preserve the payloads and source references for revisions; these are a reconstruction recipe, not a native editable-editor project.

## Verification and common mistakes

For generative edits, inspect a contact-sheet sweep plus frames around important changes, not just the first and last frames. Check identities, original and requested text, objects outside the requested edit, action continuity and audio. When generated audio differs, use the supported assembly route to restore the source track only if the picture still aligns; attaching original audio to retimed action does not fix synchronization. Silent sources remain silent unless the brief asks for sound.

- Rebuilding every variant after one failed job discards successful work and repeats spend.
- Changing music, grade and hook together invalidates a copy-only comparison.
- Requested dimensions and duration are not measured output properties.
- A new visual treatment is not evidence of a better-performing ad; performance needs a separate campaign experiment.
- Source reconstruction is not byte identity after re-encoding. Check preserved content and measured synchronization; promise lossless delivery only when the route supports it.
