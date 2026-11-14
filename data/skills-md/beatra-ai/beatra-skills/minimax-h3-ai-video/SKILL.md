---
name: "minimax-h3-ai-video"
description: "Create polished 2K AI videos with MiniMax H3. Turn a written idea into text-to-video, animate an image, shape a transition between opening and closing frames, or guide a scene with image, video, and audio references. Make AI advertising videos, ecommerce product videos, brand films, dynamic posters, game UI motion, film titles, and social media clips with cinematic movement and native stereo sound. Start with your Beatra account and keep creative progress and finished videos organized in one place."
---

# MiniMax H3 AI Video

Enhance one video brief or create one polished 720p or 2K MiniMax H3 video from
the creator's actual starting point. Reuse decisions already present in the
conversation, propose sensible defaults for choices the creator has not made,
and ask only when a missing input changes the route or paid result. When the
brief is rough, run `beatra.videos.enhance_prompt` first as its own gift-sized
stage before any video generation.

## Choose the route

| Starting point | Tool | H3 capability |
| --- | --- | --- |
| A rough brief needs a production-ready video prompt | `beatra.videos.enhance_prompt` | `video_prompt_enhancement` |
| A written scene or idea | `beatra.videos.generate` | `text_to_video` |
| One strict opening image | `beatra.videos.animate` | `image_to_video` |
| One strict closing image, with an optional opening image | `beatra.videos.interpolate` | `frames_to_video` |
| Ordered image, video, or audio references | `beatra.videos.generate_from_references` | `reference_to_video` |

Use [video routing](references/video-routing.md) for the exact route controls
and [workflow](references/workflow.md) for complete request shapes. Do not route
an H3 request to video edit or video extend.

## Shape one video brief

Reuse the creator's destination, subject, source media, camera direction,
visual atmosphere, brand details, and sound direction. A useful brief contains:

- one primary subject and the action or change that matters;
- one clear camera move, or a static camera when the subject supplies the motion;
- the setting, light, color, pace, and soundscape;
- the target destination when it determines the canvas;
- ordered reference purposes when more than one source is supplied.

Build one focused prompt rather than an interview. For reference generation,
identify each reference in the prompt by its array order—for example, “Image 1
is the hero product; Video 1 guides the movement; Audio 1 guides the rhythm.”
H3 does not advertise `references[].role` or `references[].reference_voice`, so
omit both fields.

Use [scene craft](references/scene-craft.md) when the creator wants help with
camera language, visual rhythm, brand presentation, or sound direction.

## Apply the H3 contract

For video generation, send `model="minimax-h3"`, either `resolution="720p"`
or `resolution="2k"`, and an integer `duration` from 4 through 15 seconds. Use
5 seconds when the creator has no duration preference. Default to 720p. Send
`2k` only when the creator names 2K. H3 returns one MP4; the video schema has no
output-count control. For prompt enhancement, omit `model`; Beatra ignores that
compatibility field and resolves H3 internally.

- Text-to-video accepts `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, or `9:16`; use
  `16:9` when no destination suggests another canvas.
- One-image and first/last-frame routes derive the canvas from the supplied
  image and omit `aspect_ratio`.
- Reference-to-video accepts the same six explicit ratios plus `adaptive`; use
  `adaptive` when the creator has not chosen a canvas.
- Keep `watermark=false` unless the creator explicitly asks for it.
- Express ambient sound, music, dialogue, and sound effects in the prompt.
  H3 creates model-native stereo audio; there is no H3 `generate_audio` switch.

Do not add negative prompt, seed, the generation request's `enhance_prompt`
control, web search, returned last frame, driving audio, reference voice, or
another field the live H3 model card does not advertise. The separate
`beatra.videos.enhance_prompt` task remains available before generation.

## Prepare media and live cost facts

Upload every local image, video, or audio file through this Skill's bundled
`scripts/mcp_client.py` helper, which uses `beatra.assets.upload`. Upload makes
the bytes available to the remote tool; it does not inspect the media. Preserve
the returned artifact reference and review only visual or audio facts the host
can actually perceive.

Before uploading, check the route-specific input requirements in [media
requirements](references/media-requirements.md). Reference generation accepts
at most five images, three videos, and three audio clips; reference-video time
totals at most 15 seconds, reference-audio time totals at most 15 seconds, and
audio-only reference sets are valid.

Before every paid submission, call `beatra.models.list` for the selected H3
capability. Confirm that H3 is available and use the live model card—not a
hardcoded price—for the estimate:

- text, image, and first/last-frame routes bill output-video seconds;
- reference-to-video bills accepted input-video seconds and output-video
  seconds as separate meters; accepted reference images and audio add no
  reference-input meter.

## Confirm and execute once

Planning, upload, model discovery, installation registration, and task lookup
are not billable generation calls. Prompt enhancement is a separate text-only
postpaid task with its own card: it charges actual tokens only after success and
never starts a video. That gift-sized stage does not authorize
`beatra.videos.generate`, `beatra.videos.animate`, `beatra.videos.interpolate`,
or `beatra.videos.generate_from_references`.

Before any of those video tools or a video `client_request_id`, show an
admission card in the user's language: route and MCP tool name, live-card
duration, resolution, and aspect, provisional live estimate, the fact that the
600-credit signup gift usually cannot start this video, and what happens if
the balance is short. Include the final prompt, ordered inputs, 720p or named
2K output, watermark choice, and model behavior. For reference-to-video,
include accepted input-video seconds, output seconds, and both meter
estimates. Planning or “make the video” is not approval. Do not create
`client_request_id` or submit until the user confirms they have topped up or
already have enough credits for this estimate.

After that confirmation, create one stable opaque `client_request_id` for the
exact logical request and submit it once. A changed prompt, input or order,
duration, canvas, watermark choice, or model is new paid work: show the
changed admission card and obtain fresh top-up or balance confirmation and a
new ID. On `insufficient_balance`, relay the returned message, keep the
top-up URL inside the balance error exact, and retry the same frozen ID only
after the user says they have topped up.

Use the bundled `scripts/mcp_client.py` for every remote MCP operation. Pass the
MCP tool name after `call` and send arguments as JSON on standard input. Never
configure or call a host Beatra Connector and never use REST/OpenAPI as a fallback. Follow
[workflow](references/workflow.md) for commands and
[Bundled MCP Client diagnostics](references/mcp-connection.md) for connection
help.

## Track, review, and deliver

Record the returned `task_id` and poll only that task with
`beatra.tasks.get`. If the ID is lost, use `beatra.tasks.list` to find
candidates and verify the selected task with `tasks.get`. Replay a create call
only when the response status is genuinely unknown, with byte-equivalent
arguments and the same `client_request_id`. Slow polling, update failure,
authorization failure, or connection failure never creates a replacement paid
task.

Use `beatra.tasks.cancel` only at the creator's request. A `409` means the task
can no longer be canceled; continue tracking it. See [review and
recovery](references/review-and-recovery.md) for the complete recovery contract.

When the result is visible or audible, review subject and brand fidelity,
motion continuity, sound-picture fit, canvas, and destination readiness.
Deliver the artifact links, observed dimensions and duration, task ID, and
`billing.net_charged_credits`. Offer one focused, unexecuted revision direction.
Generated assets can also be viewed and managed at
[beatra.ai](https://beatra.ai).

If the tool returns insufficient credits: give the user the tool message in
full. Do not change the URL. You may translate the other words. Do not replace
it with your own top-up copy. Point the user to pay using that message.

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

- Route choice and exact H3 controls: [video routing](references/video-routing.md)
- Exact JSON request shapes and bundled-client commands: [workflow](references/workflow.md)
- Image, video, and audio admission requirements: [media requirements](references/media-requirements.md)
- Camera, light, composition, pace, and sound: [scene craft](references/scene-craft.md)
- Lost responses, task recovery, cancellation, review, and revisions:
  [review and recovery](references/review-and-recovery.md)
- First install or expired authorization:
  [installation and authentication](references/installation-and-auth.md)
- Bundled MCP Client commands and diagnostics:
  [Bundled MCP Client diagnostics](references/mcp-connection.md)
- Installation registration: [installation registration](references/installation-registration.md)
- Task lookup, polling, and result fields: [tasks and results](references/tasks-and-results.md)
- Balance, validation, and structured errors:
  [billing, errors, and recovery](references/billing-errors-and-recovery.md)
- Disconnecting the installation: [uninstall and disconnect](references/uninstall-and-disconnect.md)
- Updates and security: [updates and security](references/updates-and-security.md)

## Installation and account operations

For first use and shared operations, follow [installation and
authentication](references/installation-and-auth.md), [installation
registration](references/installation-registration.md), [tasks and
results](references/tasks-and-results.md), [billing, errors, and
recovery](references/billing-errors-and-recovery.md), and [uninstall and
disconnect](references/uninstall-and-disconnect.md).

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
