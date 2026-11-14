---
name: "talking-avatar-video"
description: "Create a talking avatar from one portrait and a short script or speech track. This AI presenter and digital human video workflow can prepare narration with a selected voice or use a supplied recording, then direct a stable talking-head clip with restrained expression, natural movement, clear delivery, and focused lip-sync review. Use it for AI spokesperson videos, product explainers, training, course lessons, announcements, onboarding, social talking-head content, and photo-to-talking-video messages, with narration-driven facial motion and a focused review of identity, clarity, lip sync, and motion stability."
---

# Talking Avatar Video

Talking-avatar production is an identity and voice-rights task, not only a prompt-writing task. Turn one portrait and a short script or approved speech track into one directed presenter clip. Use this Skill for explainers, product messages, training, lessons, announcements, onboarding, or social talking-head content when one stable portrait should deliver one clear spoken message. Without authorization for the likeness and the voice, stop at confirmation and do not generate.

## Scope and adjacent routes

The normal route is one portrait, one approved narration track, and one voice-led video shot. Use an existing approved speech recording directly, or prepare narration from a short script with an available voice. Route a request for a new portrait to an image workflow, voice cloning to a dedicated voice-cloning workflow, and multi-scene assembly, captions, or changes to an existing video to the appropriate video-editing workflow. Keep the presenter route focused; do not substitute silent image animation for speech-driven facial motion.

When the user wants lecture videos from slides — a course, several lessons,
or one micro-lesson — point to Lecture Video Maker (`lecture-video-maker`)
for a course or Micro-Lesson Maker (`micro-lesson-maker`) for one lesson,
with the install message in
[Narration-first presenter workflow](references/workflow.md#pointing-to-another-skill),
and install it only after the user asks. One presenter clip stays here.

## Inputs and defaults

The hard inputs are:

- one accessible portrait the host Agent can inspect;
- either an accessible, approved speech track or a short script plus an available voice choice;
- whether the user owns or has been granted rights to the presenter likeness and the narration voice.

Ask only for a missing hard input. Missing authorization does not enter paid `beatra.videos.animate` or `beatra.speech.synthesize`. Reuse the known language, pronunciation, destination, framing, energy, background, and delivery intent. For a local image or audio file the host Agent can access, use the bundled upload helper only after inspection:

```text
python3 scripts/mcp_client.py upload ./presenter-portrait.png --mime-type image/png
python3 scripts/mcp_client.py upload ./approved-speech.mp3 --mime-type audio/mpeg
```

Upload is transport, not visual or audio review. Retain each returned artifact reference and never pass a local path to a remote tool.

Default to one presenter clip, `model: "auto"`, the portrait as the strict first frame, and a source-derived aspect ratio. Omit resolution and other optional controls unless the destination or an explicit user choice requires them. For synthesized narration, default an unspecified format to `mp3` only when a live speech card supports it and a live video card accepts its expected `audio/mpeg` output. Direct one clear message with restrained eye line, expression, posture, head movement, camera, and background. Treat identity, clothing, product details, logos, framing, and background as must-keeps and review the result for drift rather than promising exact preservation or perfect lip sync.

## Golden path

1. Inspect the portrait. Record its actual MIME type, width, height, aspect ratio, byte size, and whether it has an alpha channel. Identify the message, destination, spoken language, pronunciation needs, framing, performance direction, and must-keeps. If the user supplied approved audio, review what is actually accessible and record its real MIME type, duration, and byte size; otherwise make the short script speakable without changing its meaning.
2. For a script route, call `beatra.voices.list` only when a voice still needs to be selected. Call `beatra.models.list` with `{"capability":"text_to_speech"}` when selecting the language, output format, named model, optional control, or numeric estimate. Keep the speech model at `auto` unless the user chose a concrete compatible model. Numeric estimates are provisional and require live catalog facts.
3. Before any paid synthesis, call `beatra.models.list` with `{"capability":"image_to_video"}`. Confirm that a current card admits `[image, driving_audio]`. Compare the portrait's actual MIME type, width and height, aspect ratio, byte size, and alpha-channel presence with every advertised image constraint; compare supplied audio's actual MIME type, duration, and byte size with every advertised driving-audio constraint. Also confirm that planned speech can fit a video duration the route can fully contain. If any required media fact is unavailable or incompatible, stop before TTS and request the smallest compatible source change. For a script route, use `mp3` only when the live speech card supports it and the live video card accepts the corresponding `audio/mpeg`. If the user requested `flac`, `opus`, or `pcm` and the video route does not accept the resulting format, explain the incompatibility before any paid call and obtain the user's choice of a compatible format. Do not silently change it or hard-code a model.
4. Show the exact narration arguments and paid boundary. A clear instruction to synthesize that prepared narration can count as approval; planning, auditioning, comparison, or an unresolved voice or format choice does not. Freeze the script, voice, language, model, format, optional controls, and one opaque stable `client_request_id`; then submit one `beatra.speech.synthesize` call exactly once.
5. Poll the narration task with `beatra.tasks.get` until terminal. On success, read the returned artifact plus the actual `task.output.audio.mime_type`, `task.output.audio.duration_seconds`, and `task.output.audio.size_bytes` when present. Present or play the real audio when the host can do so, and ask the user to approve it before the dependent video stage. Never treat a script preview, expected duration, requested format, or task metadata as an audio review.
6. Refresh or re-read the current `image_to_video` cards and admit the actual portrait plus approved speech again. Recheck every image fact and compare the audio's actual MIME, duration, and byte size with the current driving-audio constraints. If terminal audio size is absent, obtain it from trusted artifact metadata; if it remains unavailable, stop before video submission. The audio duration must be at least the live minimum (currently 2 seconds) and must not exceed either the live audio maximum or the longest eligible video duration that can contain the complete speech. Use the smallest supported integer video duration at or above the actual speech length so words are not truncated; do not add silence. A fractional narration may leave the shortest unavoidable tail pause or held frame, so disclose it and inspect the ending. If any media fact is unavailable or incompatible, stop before video submission and propose the smallest narration, recording, or portrait change. Replacing synthesized narration is new paid work with a new ID and approval.
7. Keep `model: "auto"` unless the user chose a concrete eligible video model. Preserve the portrait-derived aspect ratio by omitting `aspect_ratio`. If the destination needs another frame, ask for a first-frame image already composed for that target or explicitly route through a suitable preprocessing workflow before returning with the new image; `beatra.videos.animate` is not a crop or canvas-override step. Never crop, stretch, or change the canvas silently.
8. Show an admission card before any video `client_request_id` or `beatra.videos.animate` call: route `image_to_video`, tool `beatra.videos.animate`, approved portrait and speech, prompt, audio-led duration, resolution if set, output count, provisional live estimate, the fact that the 600-credit signup gift usually cannot start this video, and what happens if the balance is short. Planning, comparison, or “make the clip” is not approval. Approved narration does not authorize the video call. Do not submit until the user confirms they have topped up or already have enough credits for this estimate. Freeze them with a new opaque stable `client_request_id`. Invoke only the bundled `scripts/mcp_client.py`: the MCP tool name is the CLI argument and its arguments are JSON on standard input. For example:

   ```text
   printf '%s' '{"image":{"type":"artifact","artifact_id":"art_portrait"},"driving_audio":{"type":"artifact","artifact_id":"art_speech"},"prompt":"A restrained presenter delivery with steady eye line, subtle expression, and a stable camera.","duration":8,"client_request_id":"opaque-video-id"}' | python3 scripts/mcp_client.py call beatra.videos.animate
   ```

   Do not configure, call, or use a host Beatra Connector. Do not use REST/OpenAPI fallback. Submit `beatra.videos.animate` exactly once.
9. Record the returned task ID immediately and poll the same task with `beatra.tasks.get` until terminal. Deliver every returned video artifact or link. Report only actual returned task status, resolved model, dimensions, duration, usage, and `billing.net_charged_credits`. Review accessible output for identity, speech clarity, mouth timing, restrained motion, camera and background stability, ending quality, destination fit, and must-keep drift. State what the host Agent could and could not inspect.

## Paid changes, recovery, and cancellation

Narration and video are separate paid stages. Each has its own frozen payload, stable request ID, approval, create response, and task ID. A changed script, voice, language, speech control, image, audio, prompt, model, duration, aspect ratio, resolution, or video control is new logical paid work with a new ID and fresh approval. A video-stage change also needs a new admission card and fresh top-up or balance confirmation. A revised narration also invalidates any unsubmitted dependent video plan that named the old audio. On `insufficient_balance`, relay the returned message, keep the top-up URL inside the balance error exact, and retry the same frozen `client_request_id` only after the user says they have topped up.

If a create response is lost, retry only the identical frozen payload with the same stage ID. If a task ID is lost, call `beatra.tasks.list` for the relevant capability, inspect plausible candidates with `beatra.tasks.get`, and match them against that stage's private ledger before considering an identical retry. Queued and running are progress states, not failures. Recover the original stage before planning changed work; never duplicate a paid submission or guess its charge or refund.

Call `beatra.tasks.cancel` only when the user asks to cancel. Call it once and confirm the resulting terminal state with `beatra.tasks.get`. A 409 means cancellation is not confirmed, so continue polling that same task without creating replacement work.

## Account balance

When the user asks how many credits remain or whether a live estimate fits,
call `beatra.wallet.get`. When they ask what was charged, call
`beatra.wallet.ledger`. Both are read-only. Do not invent an account-balance or
top-up tool. Do not make `wallet.get` a required step before every paid submit.

When a model card comes back carrying a `top_up` block, relay its tiers as the
card lists them and in that order. Do not rank them, do not talk one down, and
do not pick one for the user. Which tier suits them is their call, made on
the wallet page with the whole list in front of them. Never quote a tier from
memory.

## References by task

- Read [Narration-first presenter workflow](references/workflow.md) when preparing or uploading speech, selecting a voice, checking duration and live model facts, constructing exact payloads, polling, recovering, cancelling, or reviewing delivery.
- Read [Installation and authentication](references/installation-and-auth.md) only when authorization or shared credentials need attention.
- Read [Installation registration](references/installation-registration.md) for the non-billable best-effort package registration step.
- Read [Tasks and results](references/tasks-and-results.md) for shared terminal task and artifact semantics, and [Billing, errors, and recovery](references/billing-errors-and-recovery.md) for returned billing or error details.
- Read [Bundled MCP Client diagnostics](references/mcp-connection.md) when the bundled client cannot connect. Do not configure a host Connector.
- Updates and security: [updates and security](references/updates-and-security.md)
- Read [Uninstall and disconnect](references/uninstall-and-disconnect.md) only when the user asks to remove the package or shared credentials.

Use or invoke the bundled `scripts/mcp_client.py` for every Beatra operation.

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
