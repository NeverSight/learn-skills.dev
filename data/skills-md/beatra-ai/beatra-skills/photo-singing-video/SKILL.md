---
name: "photo-singing-video"
description: "Make a photo sing by animating one clear portrait with a short singing audio excerpt. This photo singing video and AI singing portrait workflow turns a single face into an expressive singing clip from one portrait and a chosen song excerpt, and reviews identity, mouth and facial movement, performance energy, audio presence, and synchronization. Use it for old photo singing, birthday greetings, character art, playful posts, song promos, and memorable messages, with one portrait and one singing audio excerpt per run and honest post-result review."
---

# Photo Singing Video

Make one clear portrait sing a short song excerpt. Use this Skill for making a photo sing, portrait singing, old photo singing, character illustration singing, a greeting song video, a meme singing clip, or a digital-character song performance.

## Scope and adjacent routes

The normal route is one portrait, one approved singing-audio excerpt, and one singing-photo clip. Route a spoken presenter message (no singing) to the talking-avatar-video workflow; a pet photo plus speech to the talking-pet-video workflow; a portrait plus non-audio motion to an image-to-motion workflow; and a finished song that needs broader music-led visuals to the music-video-clip workflow. If the user needs a new song first, route that separate stage to personalized-song-maker or ai-song-cover-studio before this workflow resumes with the finished excerpt. Keep this route focused on one portrait plus singing audio. Lyrics alone are not driving audio; only an audio file can drive the singing motion.

## Inputs and defaults

The hard inputs are:

- one accessible portrait the host Agent can inspect;
- a short singing-audio excerpt.

Ask only for a missing hard input. Reuse the known occasion, framing, crop, background, and destination. For a local image or audio file the host Agent can access, use the bundled upload helper only after inspection:

```text
python3 scripts/mcp_client.py upload ./singing-portrait.png --mime-type image/png
python3 scripts/mcp_client.py upload ./song-excerpt.mp3 --mime-type audio/mpeg
```

Upload is transport, not visual or audio review. Retain each returned artifact reference and never pass a local path to a remote tool.

Default to one singing clip, `model: "auto"`, the portrait as the strict first frame, and a source-derived aspect ratio. Omit resolution and other optional controls unless the destination or an explicit user choice requires them. Treat identity, clothing, framing, and background as must-keeps and review the result for drift rather than promising exact preservation or perfect lip sync. If a new portrait canvas or cleanup is needed, route that to a suitable image workflow and return with an approved first frame.

## Golden path

1. Inspect the portrait. Record its actual MIME type, width, height, aspect ratio, byte size, and whether it has an alpha channel. Identify the face visibility, identity, framing, background, desired crop, and the singing excerpt. If the user supplied the singing audio, review what is actually accessible and record its real MIME type, duration, and byte size.
2. If the user needs a new song first, route that separate stage to personalized-song-maker or ai-song-cover-studio. Before paying for that upstream music, call `beatra.models.list` with `{"capability":"image_to_video"}` and prove that a current card admits the portrait plus the planned audio format and a duration envelope the route can fully contain. Resume this workflow once the user supplies a singing excerpt whose real duration fits a supported video duration and the current maximum; then repeat live admission with the actual file.
3. For the singing-photo video, call `beatra.models.list` with `{"capability":"image_to_video"}`. Require a current card whose `input_combinations` admits `[image, driving_audio]`. Compare the portrait's actual MIME type, width and height, aspect ratio, byte size, and alpha-channel presence with every advertised image constraint; compare the singing audio's actual MIME type, duration, and byte size with every advertised driving-audio constraint. Confirm the audio duration is at least the live minimum and within the longest eligible video duration that can contain it. If any media fact is unavailable or incompatible, stop before the video call and request the smallest compatible source change.
4. Show an admission card before any `client_request_id` or `beatra.videos.animate` call: route `image_to_video`, tool `beatra.videos.animate`, portrait, singing audio, prompt, audio-led duration, resolution if set, output count, provisional live estimate, the fact that the 600-credit signup gift usually cannot start this video, and what happens if the balance is short. Planning, comparison, or “make the clip” is not approval. Do not submit until the user confirms they have topped up or already have enough credits for this estimate. The audio duration determines the duration: use the smallest supported integer video duration at or above the actual audio length so the singing is not clipped; do not truncate or add silence. Freeze them with one opaque stable `client_request_id`. Invoke only the bundled `scripts/mcp_client.py`: the MCP tool name is the CLI argument and its arguments are JSON on standard input. For example:

   ```text
   printf '%s' '{"image":{"type":"artifact","artifact_id":"art_portrait"},"driving_audio":{"type":"artifact","artifact_id":"art_song"},"prompt":"An expressive singing performance with natural mouth movement and engaged facial energy, keeping the portrait identity and background stable.","duration":10,"client_request_id":"opaque-singing-video-id"}' | python3 scripts/mcp_client.py call beatra.videos.animate
   ```

   Do not configure, call, or use a host Beatra Connector. Do not use REST/OpenAPI fallback. Submit `beatra.videos.animate` exactly once.
5. Record the returned task ID immediately and poll the same task with `beatra.tasks.get` until terminal. Deliver every returned video artifact or link. Report only actual returned task status, resolved model, dimensions, duration, usage, and `billing.net_charged_credits`. Review accessible output for identity, mouth and facial movement, singing performance energy, audio presence and synchronization, background and wardrobe stability, ending quality, ratio, and actual duration. State what the host Agent could and could not inspect.

## Paid changes, recovery, and cancellation

A new song and the singing-photo video are separate paid stages when both run here; each has its own frozen payload, stable request ID, approval, create response, and task ID. A changed portrait, singing audio, song, prompt, model, duration, aspect ratio, resolution, or video control is new logical paid work with a new ID, a new admission card for a video stage, and fresh top-up or balance confirmation. On `insufficient_balance`, relay the returned message, keep the top-up URL inside the balance error exact, and retry the same frozen `client_request_id` only after the user says they have topped up.

If a create response is lost, retry only the identical frozen payload with the same stage ID. If a task ID is lost, call `beatra.tasks.list` for the relevant capability, inspect plausible candidates with `beatra.tasks.get`, and match them against that stage's private ledger before considering an identical retry. Queued and running are progress states, not failures. Recover the original stage before planning changed work; never duplicate a paid submission or guess its charge or refund.

Call `beatra.tasks.cancel` only when the user asks to cancel. Call it once and confirm the resulting terminal state with `beatra.tasks.get`. A 409 means cancellation is not confirmed, so continue polling that same task without creating replacement work.

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

- Read [Singing-photo workflow](references/workflow.md) when inspecting a portrait, admitting or preparing singing audio, checking live model facts, constructing exact payloads, polling, recovering, cancelling, or reviewing singing motion.
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
