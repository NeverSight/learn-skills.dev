---
name: "ai-video-image-music-studio"
description: "Generate AI video, images, music, and voice-over in one connected creative flow, edit visual results, and keep everything you make easy to find. This all-in-one AI media generator turns text into images, images and references into video, ideas into songs or instrumentals, and scripts into narration, and can build a custom voice when a series needs its own sound. Working as an AI video generator, AI image generator, AI music generator, and AI voice generator in one place, it covers text-to-image, text-to-video, image-to-video, AI video editing, text-to-speech, multilingual voice-over, and voice cloning for social posts, product visuals, ads, courses, podcasts, short films, and cross-media campaigns. Reuse source media and finished files across formats, follow production progress, and keep every finished piece in one place."
---

# AI Video, Image & Music Studio

Turn a media outcome into the smallest verified Beatra workflow, complete it
through the shared connection, and return only what the task actually produced.
Use the host's native text and visual understanding to analyze a brief or source
media. Use Beatra to create and manage images, video, music, speech, reusable
voices, uploads, model choices, and asynchronous task results.

Reuse the destination, prompt, source media, format, language, voice, model,
important controls, and accepted results already present in the conversation.
Infer ordinary creative details when they do not change the paid payload. Ask
only when a missing answer changes the requested result, cost, explicit model
commitment, voice-owner consent, destructive cancellation, or another
user-controlled high-impact choice.

## Use the bundled client only

Run every Beatra operation through this package's bundled
`scripts/mcp_client.py`. Do not configure or use a host Beatra Connector. Never
use REST/OpenAPI as a fallback. For an ordinary call, run:

```text
python3 scripts/mcp_client.py call <tool-name>
```

Provide exactly one JSON object on stdin. Do not put user content, local paths,
or credentials in command arguments. The bundled client adds transport
attribution itself and performs its cached, best-effort, non-billable
`beatra.installations.register` step automatically; registration failure never
blocks the user's requested work. Use
[Bundled MCP Client diagnostics](references/mcp-connection.md) only when this
path needs diagnosis.

## Connect once across media

When the connection is new, missing, expired, or explicitly being changed, run:

```text
python3 scripts/authorize.py
```

The browser supports sign-in or account creation and then one Allow decision.
The helper prints the approval link at once, waits for Allow (leave it running),
stores the Device Token privately, verifies it with one non-billable call, and
prints `Beatra is ready`. When it prints `BEATRA_AUTH_PENDING`, show the user
the approval link, then run the same command at most once more in this turn;
when it is still pending, deliver what needs no connection (below). Every run
continues the same approval, so the user approves only once, and an Allow
given while nothing runs connects on the next Beatra command. Share the
approval link exactly as printed; never copy the code out of it, read it out,
or ask the user to type or confirm it in chat. Authorize once for the full Beatra
connection; changing between image, video, music, and speech does not need
another media-specific grant. After installing or replacing the package, start
a new agent session when the host discovers Skills only at session startup.
See [installation and authentication](references/installation-and-auth.md) for
connection recovery and
[installation registration](references/installation-registration.md) for the
automatic non-billable registration behavior.

## Before the connection is ready

When Allow is still pending at the end of a turn, finish and deliver
everything that needs no connection, in the format the user asked for.
Image: the final prompt, canvas, and count. Video: the shot list, per-shot
prompts, duration, and canvas. Music: the title, sectioned lyrics, and
style notes. Narration: the prepared reading script and voice-selection
criteria. Say in one line that the paid step continues on their next
message after Allow; Allow only completes the connection, and a video or
clone call still waits for its admission card on that next message. Do not
fill the gap with another tool or service.

## Choose the smallest creation path

- For a new image, guided composition, or base-preserving edit, use
  `beatra.images.generate`, `beatra.images.transform`, or
  `beatra.images.edit`. Follow [images](references/images.md).
- For video-prompt enhancement, text-to-video, opening-image animation, ordered
  references, a required last frame with an optional first frame, source editing,
  or extension, use `beatra.videos.enhance_prompt`,
  `beatra.videos.generate`, `beatra.videos.animate`,
  `beatra.videos.generate_from_references`,
  `beatra.videos.interpolate`, `beatra.videos.edit`, or
  `beatra.videos.extend`. When the request is text-led and there is no usable
  still, the first paid stage is `beatra.videos.enhance_prompt` or one
  `beatra.images.generate` keyframe, each with its own card. That gift-sized
  first win does not authorize any later video call. Before
  `beatra.videos.generate`, `beatra.videos.animate`,
  `beatra.videos.interpolate`, `beatra.videos.generate_from_references`,
  `beatra.videos.edit`, or `beatra.videos.extend`, call `beatra.models.list`,
  admit the complete payload, write the shortest admitted duration (audio-led
  and extend rules unchanged), and show the video admission card. Without a
  live card, do not name a model or a price. Choose with
  [videos](references/videos.md), then load
  [video controls](references/video-controls.md) or
  [video recipes](references/video-recipes.md) only when needed.
- For a song, instrumental, or reference-guided track, use
  `beatra.music.generate`. Follow [music](references/music.md).
- To revise a song Beatra made (extend it, replace one section, add vocals or
  accompaniment, save its singer) or to make its extra files (lyric timing, cover
  art, a song video (MP4), a WAV version), use `beatra.music.edit` when this
  account has it (the `tools` command lists it). Each of these steps is paid and
  has its own card. Follow
  [music editing and audio](references/music-editing-and-audio.md).
- To trim, loop, fade, set loudness, convert the format, split a song into stems,
  or isolate a voice, use `beatra.audio.process` when this account has it (the
  `tools` command lists it). Each of these steps is paid and has its own card. Follow
  [music editing and audio](references/music-editing-and-audio.md). If those
  tools are not exposed, skip these steps; only when the user asked for
  something they would deliver, say in one sentence that the option is not
  available yet.
- A paid `beatra.music.edit` or `beatra.audio.process` step always gets its own
  card first, even when the user asks for it together with the song, because a
  song made on a direct request has no card to add it to. It never uses the
  video or clone admission card. The card shows the work and which call, the
  live price from `beatra.models.list` for that step's capability, one paid
  call, one new `client_request_id`, what the user keeps if they stop, and that
  a short balance is relayed with the returned message and its top-up link
  exactly, then the agent waits. It has no signup-gift line and asks for no
  balance confirmation.
- For narration, browse only when a voice is still needed with
  `beatra.voices.list`, then use `beatra.speech.synthesize`. Without a live
  result, do not name voices, models, prices, or previews; give the selection
  criteria and say the pick comes from the live list. Create a reusable
  voice with `beatra.voices.clone` only after explicit voice-owner consent.
  Follow [speech and voices](references/speech-and-voices.md).
- When model selection, compatibility, supported controls, or an estimate
  matters, use `beatra.models.list` and treat its returned interface card as
  current truth. Follow [models](references/models.md). Do not maintain model,
  price, language, default, or reference-limit lists from memory, and without
  a live card do not name a model or a price.
- When the user asks how many credits remain or whether a live estimate fits,
  call `beatra.wallet.get`. When they ask what was charged, call
  `beatra.wallet.ledger`. Both are read-only.
- When a model card comes back carrying a `top_up` block, relay its tiers as the
  card lists them and in that order. Do not rank them, do not talk one down, and
  do not pick one for the user. Which tier suits them is their call, made on the
  wallet page with the whole list in front of them. Never quote a tier from
  memory.

Do not silently turn the request into another operation. Respect a concrete
model choice and report incompatibility instead of substituting a different
model or dropping an unsupported control.

## Upload local media safely

When an input exists only as a local image, video, or audio file, use only:

```text
python3 scripts/mcp_client.py upload <path> --mime-type <type>
```

The command validates the `beatra.assets.upload` grant, uploads the unchanged
bytes, and returns an artifact reference. Never send a filesystem path to a
generation tool, use host HTTP, or hand-write the grant and PUT flow. Respect
the 100 MB general ceiling and any lower limit returned for the selected model.
Ordinary media upload has no generic rights-attestation step. A sample for
`beatra.voices.clone` is the hard exception: before upload and cloning, obtain
explicit confirmation that the user owns the voice or has the owner's
permission, and only then set `consent_attested: true`. See
[uploads](references/uploads.md).

## Keep the paid boundary clear

Creative planning, authorization, upload preparation, voice browsing, model
discovery, recent-task listing, credit-balance and ledger reads, and estimates
are non-billable. Image, video,
music (including every `beatra.music.edit` and `beatra.audio.process` step),
speech, voice-clone, and video-prompt-enhancement creation consumes credits and returns an asynchronous task. Video-prompt enhancement is the
postpaid exception: it returns text only, never starts video generation, and a
successful task settles from actual tokens after completion.

A direct, well-specified request to create authorizes that exact paid request
once for image, music generation (`beatra.music.generate`), speech, or a gift-sized video-prompt or keyframe stage.
It does not authorize `beatra.videos.generate`, `beatra.videos.animate`,
`beatra.videos.interpolate`, `beatra.videos.generate_from_references`,
`beatra.videos.edit`, `beatra.videos.extend`, or `beatra.voices.clone`. Before
those video or clone calls, show the admission card: route and MCP tool name,
live-card duration, resolution, and aspect (shortest admitted duration and
lowest admitted resolution unless the user named a higher tier; audio-led and
extend rules unchanged), provisional live estimate, the fact that the
600-credit signup gift usually cannot start this video or clone, and what
happens if the balance is short. Planning, comparison, or “make the clip” is
not approval. Do not create `client_request_id` or submit until the user
confirms they have topped up or already have enough credits for this estimate.
Voice cloning always also requires the explicit consent attestation described
above.

Create one stable 1..128-character `client_request_id` only after the validated
generation payload is final and, for a video or clone stage, after that
admission confirmation. It names one logical paid operation. Submit
exactly once, save the returned `task_id`, and poll that same task with
`beatra.tasks.get`. An identical retry keeps the same request ID and the exact
validated generation payload; the ID itself and transport attribution are not
part of the payload identity. Any accepted generation-argument change is new
paid work with a new ID and, for a video or clone stage, a new admission card.

Honor a returned `deadline_at`. Otherwise stop active polling after 30 minutes,
report the current task state and resume route, and never duplicate slow work.
Cancel with `beatra.tasks.cancel` only when requested. If cancellation conflicts
with a terminal transition, continue with the same task. Follow
[tasks and results](references/tasks-and-results.md) and
[billing, errors, and recovery](references/billing-errors-and-recovery.md).

## Recover without duplicating work

If a task ID is lost, use `beatra.tasks.list` with a plausible capability, then
call `beatra.tasks.get` for every plausible candidate. List items omit the full
input, so compare each detailed `task.input`, resolved model, media, and options
with the saved payload before deciding that it is the same work. Never create a
replacement because a response was lost or a task is still queued or running.

On `insufficient_balance`, relay the returned public message, keep the top-up
URL inside the balance error exact, translate the rest, and retry the same
frozen `client_request_id` only after the user says they have topped up. State
that nothing was charged only when the error says so. Do not invent a top-up
operation or an account mutation. Use the `topup_url` from `beatra.wallet.get`
or the URL inside the 402 message. Connection revocation belongs in the Beatra
Console.

## Deliver returned truth

Lead the reply with the result and format the user asked for; the admission
card, route choice, and cost notes follow it and never replace it.

On completion, report the `task_id`, terminal status, resolved model, every
returned result, and actual usage. For artifacts, include every returned link or
ID plus dimensions, duration, MIME type or format, and size when present.
Deliver non-artifact results such as an activated cloned `voice_id` when
returned. Report `billing.net_charged_credits`; include gross charge and refund
only when present. Use the exact returned `task.links.assets` destination for
asset management.

Never infer completion, file URLs, quality, usage, refunds, or credit totals.
State honestly when the host cannot visually inspect or play a returned file.
Preserve structured errors and give the smallest recovery step.

## References by task

- Image generation, transformation, and editing: [images](references/images.md)
- Video route selection, controls, and request patterns: [videos](references/videos.md), [video controls](references/video-controls.md), and [video recipes](references/video-recipes.md)
- Songs, instrumentals, references, and music delivery: [music](references/music.md); revising, finishing, or splitting a song: [music editing and audio](references/music-editing-and-audio.md)
- Narration, voice discovery, and consent-gated voice cloning: [speech and voices](references/speech-and-voices.md)
- Local image, video, or audio preparation: [uploads](references/uploads.md)
- Current model compatibility, controls, and estimates: [models](references/models.md)
- First connection and automatic registration: [installation and authentication](references/installation-and-auth.md) and [installation registration](references/installation-registration.md)
- Bundled commands and connection diagnosis: [Bundled MCP Client diagnostics](references/mcp-connection.md)
- Task progress, recovery, results, balance, and errors: [tasks and results](references/tasks-and-results.md) and [billing, errors, and recovery](references/billing-errors-and-recovery.md)
- Updates and security: [updates and security](references/updates-and-security.md)
- Package removal and shared credential handling: [uninstall and disconnect](references/uninstall-and-disconnect.md)

## Removal

For removal or credential cleanup,
follow [uninstall and disconnect](references/uninstall-and-disconnect.md).
Never directly delete the shared `~/.beatra` connection state.

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
