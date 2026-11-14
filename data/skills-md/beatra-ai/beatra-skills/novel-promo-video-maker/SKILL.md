---
name: "novel-promo-video-maker"
description: "Turn a novel chapter, web-novel excerpt, or story script into narrated vertical short video scenes with illustrated shots that keep every character looking the same from beat to beat. This AI story video maker pulls the hook and the beats out of your text, draws one shot for each, records the narration in a voice you choose, and sets each clip to its own narration, so a chapter arrives as an ordered set of scenes for story channels, book trailers, web-novel promotion, chapter recaps, and faceless storytelling accounts."
---

# Novel Promo Video Maker

Turn a chapter of prose into an ordered set of narrated vertical scenes: pull
the hook and the beats out of the text, draw one shot per beat with the cast
looking the same every time, record the narration, and set each clip to the
narration that belongs to it.

## Scope and routing

Use this Skill when the user has story text — a novel chapter, a web-novel
excerpt, a short story, a synopsis, or a story script — and wants a finished
narrated video out of it. It fits web-novel promotion, story and reading
channels, book trailers, chapter recaps, faceless storytelling accounts, and
serial daily posting.

Route a shot list or storyboard with no footage to `ai-storyboard-generator`.
Route one cinematic live-action beat to `ai-short-drama-shot-maker`, and
animated comic panels to `ai-comic-drama-shot-maker`. Route whole-book audio
with no visuals to `ai-audiobook-narration`, and a multi-voice cast performance
to `beatra-ai-voice-studio`. Route a music-led montage to
`ai-music-video-clip-maker`.

## Inputs and defaults

The one hard input is the story text itself. Reuse the genre, tone, target
platform, narrator preference, character notes, and any reference art already
present in the conversation.

Ask only when the answer changes the paid result: which passage to adapt, when
the user supplied a long work and named no chapter or scene; and which character
is the point-of-view lead, when the passage carries several and the text does not
settle it.

Defaults that avoid extra questions:

- A vertical `9:16` canvas, because the destination is a short-video feed.
- Four to six beats: one hook beat, two to four development beats, and one
  cliffhanger or turn to close.
- One narrator voice for the whole piece.
- `count: 1` per shot image, so the user judges a look before the batch runs.
- An illustrated cinematic look, unless the text or the user names another.

## Golden path

Planning is free. Only image, speech, and video calls are paid.

1. Read the passage. Write a beat sheet: the hook, each beat's action and
   emotion, the visible setting, and which characters appear.
2. Build a cast sheet before any shot. For each recurring character, create one
   reference image and keep its artifact; every later shot carries that
   reference so the character stays the same person across beats.
3. Draft the narration line for each beat in the author's voice, and keep it
   short enough to sit under one shot.
4. Read the live cards with `beatra.models.list` for all four capabilities a run
   touches — `text_to_image` for cast references, `image_to_image` for shots
   carrying a cast reference, `text_to_speech`, and `image_to_video` — and take
   every price from them. For image stages, match the admitted request to the
   current `pricing.options` dimensions and use the highest eligible option as
   the approval ceiling when admission cannot identify one in advance; never
   multiply image price by reference count. Images bill per successfully persisted image, speech
   bills linearly per 1,000 weighted characters where each Han ideograph counts
   as two, and video pricing uses the returned billable basis.
5. **Confirm the plan.** Show the beat sheet, cast sheet, narration lines,
   canvas, the exact number of image, speech, and video calls, the current
   maximum charge per stage, and one opaque stable `client_request_id` per
   paid call.
6. Create the cast references and then the per-beat shot images with
   `beatra.images.generate` for a fresh composition or
   `beatra.images.transform` when a cast reference must carry through.
7. Synthesize each beat's narration with `beatra.speech.synthesize`, then read
   the actual returned duration, size, and MIME type.
8. After the shot image and narration exist, show a video admission card
   before any video `client_request_id` or `beatra.videos.animate` call: route
   `image_to_video`, tool `beatra.videos.animate`, that beat's image and
   narration, audio-led duration, resolution if set, provisional live
   estimate, the fact that the 600-credit signup gift usually cannot start
   this video, and what happens if the balance is short. Planning, comparison,
   or “make the clip” is not approval. Approved stills or narration do not
   authorize the video. Do not submit until the user confirms they have topped
   up or already have enough credits for this estimate. Then animate each beat
   with `beatra.videos.animate`, passing that beat's shot image and its
   narration as the driving audio. Select the video model explicitly rather
   than leaving it to `auto`: keep only models whose card admits
   `[image, driving_audio]`, because most on this capability do not and the
   advertised `auto` default is a model that refuses driving audio. Omit
   `aspect_ratio` — the 9:16 shot image governs the frame. Re-check the real
   returned narration length against that card and use the smallest admitted
   whole second at or above it; if the card admits none, stop before the video
   call rather than truncating the line. An approved `beatra.videos.extend`
   also needs its own admission card; its `duration` is the final returned
   length and must exceed that clip's own duration.
9. Deliver the beats in order as the finished scene set. Report only the actual
   returned task status, resolved model, dimensions, duration, usage, and
   `billing.net_charged_credits` for each. Review only media the host Agent can
   actually play or view, and say what it could not inspect.

To make one beat run longer, continue that single clip with
`beatra.videos.extend` after the user approves the extra paid step. Extension
generates new footage immediately before or after exactly one source clip; its
integer `duration` is the final returned duration and must exceed that clip's
own duration. Read
[the novel promo workflow](references/workflow.md) for beat-sheet shape, cast
consistency, payloads, narration timing, extension, recovery, and delivery
review.

## How this Skill executes

Use the bundled `scripts/mcp_client.py` for every remote Beatra operation: the
MCP tool name is the CLI argument after `call`, and one JSON object goes on
standard input. Never configure or call a host Beatra Connector, and never use
REST/OpenAPI as a fallback. Register the package with
`beatra.installations.register` on first use. Every creation is an asynchronous
task: submit once, then follow that task to a terminal state.

## Decisions that require confirmation

Confirm before the first paid call, and again whenever the plan changes: the
frozen beat sheet, the cast references, each narration line, the canvas, the
explicit video model, the total number of paid calls in each stage, and the
current maximum charge. Each video generate, animate, or extend call still
needs its own admission card and top-up or balance confirmation. A changed
passage, beat, cast reference, narration line, canvas, model, or control is
new paid work with a new request ID and, for a video stage, a new admission
card. On `insufficient_balance`, relay the returned message, keep the top-up
URL inside the balance error exact, and retry the same frozen
`client_request_id` only after the user says they have topped up.

Because one beat spans an image, a speech, and a video call, keep a separate
stable request ID per call and never reuse one across stages.

## Recovery

Save every task ID the moment it returns and poll with `beatra.tasks.get`;
`queued` and `running` mean wait. Replay a create only when its response is
genuinely unknown and the payload is byte-equivalent under the same request ID.
If a task ID is lost, use `beatra.tasks.list` for that capability, confirm
candidates with `beatra.tasks.get`, and recover the original before considering
new work. If a request ID itself is lost, do not invent a new one and do not
replay. Call `beatra.tasks.cancel` only at the user's request; on `409`, keep
polling the original task and report cancellation only when its terminal status
is `canceled`.

When one beat fails and the others succeed, recover that beat alone. The
approved beats already delivered stay valid and are not regenerated.

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

- [Novel promo workflow](references/workflow.md): beat sheet, live price cards,
  cast consistency, exact payloads, narration duration matching, extending one
  clip, recovery, and delivery review.
- [Installation and authentication](references/installation-and-auth.md) and
  [installation registration](references/installation-registration.md): first
  use and shared credentials.
- [Tasks and results](references/tasks-and-results.md) and
  [billing, errors, and recovery](references/billing-errors-and-recovery.md):
  task, artifact, and billing facts.
- [Bundled MCP Client diagnostics](references/mcp-connection.md): client
  operation and connection diagnostics; do not configure a host Connector.
- Updates and security: [updates and security](references/updates-and-security.md)
- [uninstall and disconnect](references/uninstall-and-disconnect.md): package
  removal and shared credential cleanup.

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
