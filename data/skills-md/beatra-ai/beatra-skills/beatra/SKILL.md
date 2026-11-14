---
name: "beatra"
description: "Create AI images, videos, music, and voice, look up public social data, edit visual results, and keep generated assets easy to find and manage. Beatra Universal turns text into images, images and references into video, ideas into songs or instrumentals, and scripts into narration, while also supporting custom voice creation and public social media data lookup across YouTube, TikTok, Instagram, and X. Use it as an AI media generator and AI creative suite for text-to-image, image-to-video, AI video editing, AI music generation, text-to-speech, multilingual voice-over, voice cloning, multimodal content creation, and YouTube or TikTok data for posts, comments, accounts, and trends. Reuse source media, returned files, and public social findings across formats, follow production progress, and view actual credit use for completed creative work."
---

# Beatra Universal

**What you end up with.** Per run, one of:

- **Images** — one to four, one by default.
- **Video** — a clip, plus a separate last-frame still you can ask for on the
  models that offer one.
- **Music** — a song or instrumental, delivered as every clip the model returns.
- **Narration** — an audio file.
- **A reusable cloned voice.**
- **A rewritten production prompt**, as text.
- **Public social data**, returned as JSON.

A returned file is delivered with whichever of its real dimensions, duration,
format, and size the finished task actually reports. The exact rendered format
comes from the model that runs, and is reported on delivery rather than
promised in advance.

Turn a requested outcome into the smallest verified Beatra workflow, complete
it through the shared connection, and return only what the task actually
produced. Use the host's native text and visual understanding to analyze a
brief, source media, or returned public social content. Use Beatra to look up
public social data and to create and manage images, video, music, speech,
reusable voices, uploads, model choices, and asynchronous task results.

Reuse the destination, prompt, source media, format, language, voice, model,
public social target, important controls, and accepted results already present
in the conversation. Infer ordinary details when they do not change the paid
payload. Ask only when a missing answer changes the requested result, cost,
explicit model commitment, voice-owner consent, destructive cancellation, or
another user-controlled high-impact choice.

## Use the bundled client only

Run every Beatra operation through the bundled
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
connection; changing between image, video, music, speech, and public social
lookup does not need another grant. After installing or replacing it,
start a new agent session when the host discovers Skills only at session
startup. See [installation and authentication](references/installation-and-auth.md)
for connection recovery and
[installation registration](references/installation-registration.md) for the
automatic non-billable registration behavior.

## Before the connection is ready

When Allow is still pending at the end of a turn, finish and deliver
everything that needs no connection, in the format the user asked for.
Image: the final prompt, canvas, and count. Video: the shot list, per-shot
prompts, duration, and canvas. Music: the title, sectioned lyrics, and
style notes. Narration: the prepared reading script and voice-selection
criteria. Social lookup: the target, fields, and query plan. Say in one
line that the paid step continues on their next message after Allow;
Allow only completes the connection, and a video or clone call still waits
for its production card on that next message. Do not fill the gap with
another tool or service.

## Choose the smallest path

- For public posts, notes, videos, accounts, comments, or trends, use
  `beatra.social.tools.search`, then `beatra.social.tools.get`, then one
  `beatra.social.execute` with `operation_key`, the `schema_hash` just copied
  from that `tools.get`, `arguments`, and one `client_request_id`. Follow
  [public social data](references/social.md). If those tools are not exposed,
  say they are not available on this connection. Do not invent an
  `operation_key`, call `beatra.models.list` for social lookup, or turn a
  lookup into generation. Continue only with media the user already asked for.
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
  `beatra.images.generate` keyframe. That gift does not authorize a later video
  call. Before generate, animate, interpolate, reference, edit, or extend, call
  `beatra.models.list` with that route's exact capability (for example
  `{"capability":"text_to_video"}` or `{"capability":"image_to_video"}`), admit
  the payload, write the shortest admitted duration (audio-led and extend rules
  unchanged), and show the production card. Without a live card, do not name a
  model or a price.
  Choose with [videos](references/videos.md), then load
  [video controls](references/video-controls.md) or
  [video recipes](references/video-recipes.md) only when needed.
- For a talking presenter, spoken delivery, or digital-human clip, synthesize the
  narration first with `beatra.speech.synthesize`, then animate a portrait with
  `beatra.videos.animate`, passing that narration as `driving_audio`. The video
  card's admitted formats and durations both constrain what you synthesize, so
  read `{"capability":"image_to_video"}` and `{"capability":"text_to_speech"}`
  before the speech call. Those two free reads surface every conflict this route
  can raise before the first paid call — the audio format both cards must
  accept, the spoken length against an admitted duration, and the portrait's own
  fit. Raise all of them in a single message before the
  first paid call rather than one at a time. The returned audio's real duration
  and format still have to be re-checked against the card after synthesis.
  Follow [video recipes](references/video-recipes.md).
- For lecture or courseware work — slides into lecture videos, narration for
  every slide, a micro-lesson, or a new lesson deck — the dedicated Skills
  keep the course, the scripts, and the renders on this computer: Lecture
  Video Maker, Slide Narration Studio, Micro-Lesson Maker, and AI Courseware
  Maker. Offer the one that fits with the install message in
  [questions and anti-patterns](references/faq.md#pointing-to-another-skill)
  and install it only after the user asks; single clips and single
  narrations stay here.
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
  `tools` command lists it). Each of these steps is paid and has its own card,
  even when the user asks for it together with the song, because a song made on
  a direct request has no card to add it to. Follow
  [music editing and audio](references/music-editing-and-audio.md). If those
  tools are not exposed, skip these steps; only when the user asked for
  something they would deliver, say in one sentence that the option is not
  available yet.
- For narration, browse only when a voice is still needed with
  `beatra.voices.list`, then use `beatra.speech.synthesize`. Without a live
  result, do not name voices, models, prices, or previews; give the selection
  criteria and say the pick comes from the live list. Create a reusable
  voice with `beatra.voices.clone` only after explicit voice-owner consent and
  the production card. Follow
  [speech and voices](references/speech-and-voices.md).
- When model selection, compatibility, supported controls, or an estimate
  matters for image, video, music, or speech, copy an exact
  `{"capability":"..."}` payload from [models](references/models.md) and treat
  the returned interface card as current truth. Do not maintain model, price,
  language, default, or reference-limit lists from memory, and without a live
  card do not name a model or a price.
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

## Keep the user's wording

Carry the user's own subject, constraints, and negations into the prompt, and
expand it only as far as the chosen route actually needs. When you add wording
the user did not give — style, lighting, mood, instrumentation, or camera
language — say in your reply what you added. Some routes must add wording of
their own: [music](references/music.md) replaces a named artist with musical
qualities.

Send the `enhance_prompt` control only when the selected model's interface card
lists it. Sending an explicit `true` or `false` narrows which models `auto` may
choose, and an explicitly named model that does not expose it rejects the
request. `beatra.videos.enhance_prompt` is a separate paid tool that rewrites a
brief into a production prompt by design.

A returned result that does not match the prompt is a reportable outcome, not
something to hide behind a reworded retry.

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
discovery, public social tool search and inspection, recent-task listing,
credit-balance and ledger reads, and estimates are non-billable. Image, video, music (including every `beatra.music.edit` and
`beatra.audio.process` step), speech, voice-clone, video-prompt-enhancement,
and public social execute consume credits and return
an asynchronous task. Public social execute is prepaid. Video-prompt
enhancement is the postpaid exception: it
returns text only, never starts video generation, and a successful task
settles from actual tokens after completion.

A direct, well-specified request to create or look up authorizes that exact
paid request once for image, music generation (`beatra.music.generate`), speech,
social execute, or a gift-sized
video-prompt or keyframe stage. It does not authorize
`beatra.videos.generate`, `beatra.videos.animate`,
`beatra.videos.interpolate`, `beatra.videos.generate_from_references`,
`beatra.videos.edit`, `beatra.videos.extend`, or `beatra.voices.clone`. Before
those video or clone calls, show the production card and wait for the user's
answer:

1. Work — what will be made, in the user's own words, and which call makes it.
2. Credits — the provisional estimate from the live card just read, never a
   remembered number.
3. Count — how many paid calls this turn. A retry with changed arguments is
   another one.
4. Identity — one new opaque `client_request_id` per call, minted only once
   that call's payload is final.
5. If the user stops here — name what they already hold and keep, such as an
   accepted opening frame, a synthesized narration, or an enhanced prompt. When
   this is the run's first paid call, say plainly that nothing has been paid
   for yet, rather than naming an artifact that does not exist.
6. If the balance is insufficient — relay the returned message and its top-up
   URL exactly, and wait.

Show the route's live-card duration, resolution, and aspect beside the estimate,
taking the shortest admitted duration and lowest admitted resolution unless the
user named a higher tier; audio-led and extend rules are unchanged. Planning,
comparison, or “make the clip” is not approval; approving this card is. Do not
ask the user to confirm they have enough credits — the connection reports the
balance itself — and do not create `client_request_id` or submit before they
approve.

Public social lookup is never folded into a video or clone production card. When it needs
confirmation, it gets its own card. For it, copy the `schema_hash` from
`beatra.social.tools.get` into execute with
`operation_key`, `arguments`, and one `client_request_id`. Show the
`operation_key` and the credit price returned by `tools.get`. Do not show
`schema_hash` to the user and do not ask for a model. Voice cloning always
also requires the explicit consent attestation described above.

Create one stable 1..128-character `client_request_id` only after the validated
paid payload is final. It names one logical paid operation. Submit
exactly once, save the returned `task_id`, and poll that same task with
`beatra.tasks.get`. Never poll a row whose submission returned no `task_id`;
reconcile with `beatra.tasks.list` instead. An identical retry keeps the same request ID and the exact
validated paid payload; the ID itself and transport attribution are not
part of the payload identity. Any accepted paid-argument change is new
paid work with a new ID and confirmation.

Honor a returned `deadline_at`. Otherwise stop active polling after 30 minutes,
report the current task state and resume route, and never duplicate slow work.
Cancel with `beatra.tasks.cancel` only when requested. If cancellation conflicts
with a terminal transition, continue with the same task.

Public social validation or a failed lookup is not a `beatra.models.list`
event. Keep `error.code`, read `error.message` or `error.data.message`, and
do not change a model. Follow [tasks and results](references/tasks-and-results.md)
for task identity and polling. For media generation validation or model
incompatibility only, follow
[billing, errors, and recovery](references/billing-errors-and-recovery.md).

## Recover without duplicating work

If a task ID is lost, use `beatra.tasks.list` with a plausible capability, then
call `beatra.tasks.get` for every plausible candidate. List items omit the full
input, so compare each detailed `task.input` with the saved payload before
deciding that it is the same work. For media generation, also compare resolved
model, media, and options. For public social lookup, compare `operation_key`,
arguments, and `schema_hash`. Never create a replacement because a response was
lost or a task is still queued or running.

On `insufficient_balance`, relay the returned public message, keep its top-up
URL exact, translate the rest, and retry the same
frozen `client_request_id` only after the user says they have topped up. State
that nothing was charged only when the error says so. Do not invent a top-up
operation or an account mutation. Use the `topup_url` from `beatra.wallet.get`
or the URL inside the 402 message. When the user asks which top-up amount to
buy, read [questions and anti-patterns](references/faq.md). Connection
revocation belongs in the Beatra Console.

On a failed public social lookup, keep `error.code` and read the platform
wording in `error.message` or `error.data.message`. Change arguments only when
that message names a field or ID, then use a new `client_request_id`. Otherwise
keep the same ID and the same payload. Do not suggest changing a model.

## Deliver returned truth

Lead the reply with the result and format the user asked for; the production
card, route choice, and cost notes follow it and never replace it.

While a task is still queued or running, report the `stage` that
`task.progress` actually returns instead of narrating an invented pace. Treat
its `percent` as a phase marker rather than a completion fraction: it moves on
fixed server steps, holds one value for the whole generation wait, and must never
be handed to the user as a share of the work finished. An unchanged stage or
percent is not evidence that the task is stuck. When a response carries no
progress at all, say the task is still running and leave it there.

On completion, report the `task_id`, terminal status, every returned result,
and actual usage. For media generation, also report the resolved model. For
artifacts, include every returned link or ID plus dimensions, duration, MIME
type or format, and size when present. For public social lookup, deliver the
inline JSON or JSON artifact; do not look for a resolved model or a generated
media file. Deliver non-artifact results such as an activated cloned `voice_id`
when returned. Report `billing.net_charged_credits`; include gross charge and
refund only when present. Use the exact returned `task.links.assets`
destination for asset management.

Never infer completion, file URLs, quality, usage, refunds, or credit totals.
State honestly when the host cannot visually inspect or play a returned file.
Preserve structured errors and give the smallest recovery step.

## References by task

Three tiers. Read the first on a first run, the second once a route is chosen,
and the third only when something needs diagnosis or recovery.

### Getting started

- On a first run, or when one job spans more than one medium, read [planning a multi-medium run](references/worked-example.md) for the order of decisions and where each paid boundary falls
- First connection and automatic registration: [installation and authentication](references/installation-and-auth.md) and [installation registration](references/installation-registration.md)

### Building the request, one medium at a time

- Public social posts, accounts, comments, and trends: [public social data](references/social.md)
- Image generation, transformation, and editing: [images](references/images.md)
- Video route selection, controls, and request patterns: [videos](references/videos.md), [video controls](references/video-controls.md), and [video recipes](references/video-recipes.md)
- Songs, instrumentals, references, and music delivery: [music](references/music.md); revising, finishing, or splitting a song: [music editing and audio](references/music-editing-and-audio.md)
- Narration, voice discovery, and consent-gated voice cloning: [speech and voices](references/speech-and-voices.md)
- Local image, video, or audio preparation: [uploads](references/uploads.md)
- Current model compatibility, controls, and estimates: [models](references/models.md)

### Diagnosing and recovering

- When a user reports a result that misses the brief, a refused model, a stuck or lost task, or an unexpected charge, read [questions and anti-patterns](references/faq.md)
- Bundled commands and connection diagnosis: [Bundled MCP Client diagnostics](references/mcp-connection.md)
- Task progress, recovery, results, balance, and errors: [tasks and results](references/tasks-and-results.md) and [billing, errors, and recovery](references/billing-errors-and-recovery.md)
- Updates and security: [updates and security](references/updates-and-security.md)
- When the user wants to stop: [stopping use and removing shared credentials](references/uninstall-and-disconnect.md)

## Removal

For removal or credential cleanup,
follow [stopping use and removing shared credentials](references/uninstall-and-disconnect.md).
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
