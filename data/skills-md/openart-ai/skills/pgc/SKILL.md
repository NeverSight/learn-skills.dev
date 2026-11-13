---
name: pgc
description: Generate professional presenter-led PGC footage with Seedance through OpenArt MCP. Use for camera-facing product reviews, expert explainers, educational presentations and scripted spokesperson takes with deliberate lighting and stable camera framing. Includes intake, full reference analysis, script, performance, multi-clip continuity and audiovisual QA. Deliver individual takes with native speech, without B-roll or post-production. Casual phone-native lifestyle sharing belongs to UGC.
---

# OpenArt PGC

Before interpreting any brief, script or timecoded draft, read
[intent and script development](references/intent-and-script-development.md). Preserve the intended message,
required facts and exact keywords; actively improve expression, reasoning, actions and flexible beat timing
in this skill's style. Input detail is not an instruction to execute verbatim. Explicit exact-execution
constraints and an approved version requested unchanged remain locked.

When the Script Plan revises supplied creative input, END that response by briefly explaining what changed
and why, then ask whether to use the revised script or follow the original input exactly. Resolve that
version choice before generation under [generation approval](references/generation-approval.md);
a Draft/full-quality choice alone is not acceptance of the rewrite.

Before authoring, read [shared video experience](references/video-experience.md) and
[product understanding](references/product-understanding.md). Before a generation decision, read
[generation approval](references/generation-approval.md), including native question UI and wording examples.
Complete the full prompt and its matching readable Script Plan before showing either for approval; keep
all spoken and on-screen text in that same version. Default to Seedance 2.5 Draft preview; explicit
high-quality/full-quality delivery defaults directly to Seedance 2.5. Reuse clear approval or an explicit
approval waiver. These shared rules own the experience flow across every video and variant.
For presenter-led promotions, also read [opening hooks](references/opening-hooks.md): establish relevance
in the first 3–5 seconds and show the product from the first image without forcing a spoken brand pitch.

Read the entrypoint and these shared workflow guides, then follow the relevant references linked below.
Supporting Markdown is loaded on demand, not automatically in full. Read reference-analysis guides
for uploaded reference videos, product research for product URLs, direction before authoring, OpenArt
execution before fixing references, duration or request counts, and review before acceptance. Follow nested
links when that decision requires them.

PGC here means deliberately produced, camera-facing presenter footage: a considered camera position,
controlled lighting, clear sound and purposeful explanation. A studio, desk, workshop or well-lit home setup
can all fit. The speaker can be warm and conversational; professional does not mean rigid or an announcer voice.
Use this route for reviews, explainers, tutorials and spokesperson presentations within the footage boundary.
Casual selfie-style daily sharing is a different creative mode, not a lower-quality version of PGC.

Make clean presenter footage ready for the user's later editing. Deliver one or more independent Seedance
clips with their generated speech, appropriate native background music and generation records. Music is
normally light and subordinate to the explanation; omit it for unscored formats or explicit clean-dialogue requests.
Do not concatenate, trim, composite, caption, add music in post, dub through an external pipeline, or create a
final advertising edit. OpenArt Dub Video can make a language version of an accepted take; see
[OpenArt execution](references/openart-execution.md).
This workflow does not require Hypit CLI or its project formats.
For installation and input/output expectations, see [README](README.md).

Match the user's conversation language and requested spoken language. A prompt's direction language does not
determine the language of its dialogue. Honor an explicit prompt-only request without submitting generation.

Before authoring or revising prompts, read [creative preflight](references/creative-preflight.md).
Product images and a short brief are a valid starting point; actively design progression and
performance within this skill's boundary. Audit the final prompt for unjustified restrictions before submission.

## Establish the footage brief

Read existing decisions and material before asking questions. Establish the intended message, presenter,
spoken language, aspect ratio, target speech length, requested Seedance version if any, and fixed choices.
Use [intake and script](references/intake-and-script.md) to classify references, develop missing copy, and record
what stays or changes. Do not demand personal uploads when a fictional presenter is appropriate.

For a supplied video, use [reference understanding](references/reference-understanding.md): examine the whole
source, including sound and ending, and separate its performance from its editing and graphic treatment.
Transfer the requested delivery, framing and rhetorical structure into presenter footage. A creative reference
does not automatically supply the target person's identity, voice or product claims.

If the user needs an exact edit of source footage or a finished ad with supporting visuals, explain that this
footage workflow covers the generation stage only. Do not silently promise that a new take preserves source pixels,
timing or audio, or expand the delivery into post-production.

Before developing or improving copy, read [recommendation writing](references/recommendation-writing.md) and
[latte reference script](references/recommendation-examples.md). Build specific reasons and meaningful same-shot
product use before adding performance directions. Professional presentation still needs human warmth,
audience relevance and naturally integrated commercial information.

## Direct and divide the performance

Read [performance and prompts](references/performance-and-prompts.md) for identity, voice, physical action,
reference binding and exact dialogue. Use existing references directly when supported. An optional still-image
generation through OpenArt MCP may establish a missing identity/scene anchor; it is a dependency, not B-roll.
Read [music and sound](references/music-and-sound.md) to choose a fitting music treatment or a deliberate
unscored exception, and retain that decision in each prompt and listening review.

Read [segmentation and continuity](references/segmentation-and-continuity.md) when speech needs multiple requests
or when making variants. Keep a short performance in one take if supported; split longer speech at complete
thoughts within the live model limits. Every clip remains a continuous presenter shot. Preserve full script coverage
without forcing rapid speech or silently dropping words. Deliver ordered raw clips; there is no assembly step.

## Generate through OpenArt MCP

Apply [OpenArt execution](references/openart-execution.md), read while planning, before fixing references, voice
or clip lengths. List available Seedance models/modes and inspect the exact input schema. Check native speech/audio and
reference support. Model identifiers, durations and reference limits are not constants supplied by this skill.

Resolve actual uploaded media and supported attachment labels. Submit complete authored prompts and save task IDs
and request receipts immediately. Honor authorized scope, reuse accepted takes, and recover outstanding jobs before
submitting replacements. When the selected capability cannot produce the requested speech or reference fidelity,
report that gap; do not silently switch to another model family, a silent video, or an external dubbing pipeline.

## Review and hand off footage

Use [review and delivery](references/review-and-delivery.md) for each clip and for consistency across the set.
Check complete speech, pronunciation, lip sync, identity, wardrobe, gaze, hands, framing, audio, and unwanted
cuts or graphics. A first frame, contact sheet, transcript, or successful job alone does not establish acceptance.

Regenerate only a failed passage within the authorized scope. Do not hide defects with B-roll, trim away incorrect
speech, or splice audio as a repair. Preserve successful takes and record unresolved issues precisely.

Deliver original generated clip files or accessible output links, their order and script mapping, prompts,
generation receipts, and per-clip QA status. If playback was unavailable, mark affected checks as unverified.
A multi-clip delivery is raw footage, not a continuous finished video.
