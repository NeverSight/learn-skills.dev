---
name: "ai-multilingual-dubbing"
description: "Create multilingual voice-over audio from prepared scripts for videos, product launches, e-learning, training libraries, creator content, and international campaigns. This AI multilingual dubbing workflow organizes every market and segment, helps choose a locale-ready voice, pilots pronunciation and timing, and delivers reviewable narration by language. Use it for AI video dubbing audio, AI video translation audio, video localization voice-over, training video localization, global marketing narration, text to speech in multiple languages, or Chinese, English, and Japanese dubbing. Receive narration tracks organized by language, market, and segment, ready for localization editing, lip-sync production, training libraries, and campaign assembly."
---

# AI Multilingual Dubbing

Create organized narration audio for every target market from scripts the user
provides or approves. Reuse the message, destination, languages, voice direction,
segment boundaries, and timing targets already visible in the conversation. Move
by the shortest route to a representative pilot, then produce the rest of the
approved audio scope.

## Start from the spoken scripts

Build a `segment × locale` production matrix. Each cell records the locale and
BCP-47 tag, approved text, protected terms, pronunciation notes, voice, delivery
direction, format, timing target, and status. Use natural segments such as a
scene, lesson, chapter, ad, or publishable message—never a mid-sentence split.

If the source exists only as video or audio, use an actually available host
capability to obtain a transcript or ask the user for one. Keep that transcript
as draft text until the user approves what will be spoken. The speech operation
accepts text, not source media. When localization is requested, help draft the
target-language wording in the conversation, preserve product names, claims,
numbers, units, URLs, and calls to action, and obtain content approval. Do not
claim professional or native-language review unless the user supplies that fact.

Use [matrix design](references/matrix-design.md) and [locale readiness and
quality](references/locale-readiness-and-quality.md) for the complete preparation
and review gates.

## Choose a voice and a useful pilot

Reuse an accepted voice when its returned card supports the target language.
Otherwise call `beatra.voices.list`, filter by language and expressed preferences,
and recommend two or three suitable candidates from their live cards. Use the
available preview URLs for an unpaid audition; do not synthesize paid audio only
to discover a voice.

Default to `model: "auto"`, speed `1.0`, `mp3` for direct delivery, no emotion,
and unchanged pitch, volume, and sample rate. Use `wav` or `flac` for downstream
editing when that destination is known. Call `beatra.models.list` with
`capability: "text_to_speech"` only when the user asks about current models or
cost, selects a model, or language compatibility needs live confirmation.
Every speech request uses the approved cell text as `input`, the selected
returned voice ID as `voice`, and the cell's target BCP-47 tag as `language`.

For a multi-cell release, choose one representative high-risk segment per locale
as the pilot. Prefer names, numbers, technical terms, offers, or calls to action.
For timing-sensitive work, record the target duration, compare it with the
returned pilot duration, and adjust the smallest useful script or speed decision
after approval. Treat timing as a design constraint, not a promise of exact
synchronization.

## Confirm the paid scope once

Planning, copy drafting, voice discovery, and previews do not use the paid speech
operation. Before any `beatra.speech.synthesize` call, present the complete paid
scope in one readable matrix: every included pilot or production cell, its locale,
approved text, voice, format, delivery direction, and timing target. State that
each listed cell is one paid render. Clear approval of the complete matrix
authorizes every listed cell once; do not ask for a second confirmation. A changed
or newly added cell is new paid work and needs a revised scope and approval.

Create one stable opaque `client_request_id` for each approved locale/segment
render. Submit every approved cell once, retain its `task_id`, and poll that same
task with `beatra.tasks.get`. Honor `deadline_at` when it is returned by the
task; when none is present, stop active polling after 30 minutes, report the
current task state, and resume later instead of waiting indefinitely or creating
a replacement. The
bundled client handles its own cached, best-effort, non-billable installation
registration; do not add a manual registration step to this creative workflow.

## Use the bundled MCP Client

Use only this Skill's bundled `scripts/mcp_client.py` for every remote MCP
operation. Pass the MCP tool name as the CLI argument and send one JSON object on
stdin. Do not configure or call a host Beatra Connector, and do not use
REST/OpenAPI as a fallback. For exact commands and troubleshooting, use
[Bundled MCP Client diagnostics](references/mcp-connection.md).

## Recover the task and deliver the audio

A queued or running task is work in progress, not a reason to submit again. If a
response is uncertain but every generation argument is identical, retry with the
same `client_request_id`. Any change to text, voice, language, model, speed,
format, pitch, volume, sample rate, or emotion creates a new request identity and
new paid work. If the task ID is lost, use `beatra.tasks.list` with the
`text_to_speech` capability, call `beatra.tasks.get` for every plausible
candidate, and compare its complete `task.input`, resolved model, and timing to
the saved matrix cell before creating anything. A list item alone is not enough
to identify the original request. Cancel only when the user asks; if
`beatra.tasks.cancel` conflicts, continue polling the same task.

On success, deliver the actual `task.output.audio.url`, artifact ID, MIME type,
size, sample rate when returned, and `task.output.audio.duration_seconds`, grouped
by locale and segment. Include the actual task identity and billing result. Review
pronunciation, register, pauses, voice fit, pace, tone, and timing only when the
host can actually play the audio; otherwise say listening review is incomplete
and deliver the factual result. Revise only the affected cell after a new paid
confirmation. Keep accepted cells untouched and do not claim translation,
captions, lip sync, voice preservation, audio/video editing, or exact timing.

Use [recovery and delivery](references/recovery-and-delivery.md) for the detailed
task and acceptance path.

## References by task

- Matrix, segmentation, casting, defaults, and pilots: [matrix design](references/matrix-design.md)
- Locale-copy readiness and listening review: [locale readiness and quality](references/locale-readiness-and-quality.md)
- Exact retry, cancellation, terminal results, and delivery: [recovery and delivery](references/recovery-and-delivery.md)
- First installation or expired authorization: [installation and authentication](references/installation-and-auth.md)
- Bundled MCP Client commands and diagnostics: [Bundled MCP Client diagnostics](references/mcp-connection.md)
- Installation registration behavior: [installation registration](references/installation-registration.md)
- Task lookup and result fields: [tasks and results](references/tasks-and-results.md)
- Balance, uncertain submissions, billing, and errors: [billing, errors, and recovery](references/billing-errors-and-recovery.md)
- Disconnecting the installation: [uninstall and disconnect](references/uninstall-and-disconnect.md)
- Updates and security: [updates and security](references/updates-and-security.md)

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
