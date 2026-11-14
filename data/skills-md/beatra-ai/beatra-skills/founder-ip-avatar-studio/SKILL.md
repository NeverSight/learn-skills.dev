---
name: "founder-ip-avatar-studio"
description: "Turn one authorized founder or expert portrait and a weekly script into a talking-head IP video in that person's likeness and voice. This founder avatar and digital avatar studio can clone that person's voice and produce a stable founder talking head clip for founder updates, expert explainers, and brand announcements. Use it for a digital human spokesperson, talking head founder series, expert avatar video, brand digital human, AI presenter, AI spokesperson video, and recurring presenter video."
---

# Founder IP Avatar Studio

Turn one authorized likeness and voice into a recurring talking-head update.
The first run may create the voice. Later weeks reuse it.

## Scope and adjacent routes

Use this Skill when a founder, expert, or brand wants a weekly or campaign
talking-head clip from one stable portrait plus a short script.

Route a one-off presenter clip with no series plan to
`talking-avatar-video`. Route audio-only series work to
`voice-clone-series-studio`. Route a lecture series with many lessons to
`course-video-studio`. Without authorization for the likeness and the
voice, stop at confirmation and do not generate.

## Inputs and defaults

The hard inputs are:

- one accessible portrait the host Agent can inspect;
- either an approved speech track or a short script plus a voice path;
- whether the user owns or has been granted rights to the likeness and the
  voice.

Reuse language, destination, framing, and the frozen `voice_id` from
earlier weeks. Default to one presenter clip, `model: "auto"` for video,
the portrait as the strict first frame, and a source-derived aspect ratio.

## Golden path

1. Inspect the portrait. Record MIME type, width, height, aspect ratio, byte
   size, and whether it has an alpha channel. Confirm likeness rights. For a
   local portrait or sample, upload only through the bundled client after
   inspection. Never pass a local path to a remote tool.
2. If the series still needs a cloned voice, confirm consent first. Access
   to a file is not consent. A suitable sample is currently about 10 to
   300 seconds, no larger than 20 MiB, and clean single-speaker speech.
   Call `beatra.models.list` with `{"capability":"voice_clone"}` and show
   the clone admission card before any clone `client_request_id` or
   `beatra.voices.clone` call: route `voice_clone`, tool
   `beatra.voices.clone`, live price for one successful activated voice,
   the provisional estimate, the 600-credit signup gift usually cannot
   start this clone, and what happens if the balance is short. Do not
   create `client_request_id` or submit until the user confirms they have
   topped up or already have enough credits. Do not offer a free clone.
   Submit `beatra.voices.clone` exactly once:

   ```json
   {
     "sample": {"type": "artifact", "artifact_id": "artifact_..."},
     "display_name": "Founder Voice",
     "consent_attested": true,
     "model": "auto",
     "client_request_id": "opaque-founder-clone"
   }
   ```

   Poll with `beatra.tasks.get` until terminal, then freeze the returned
   `voice_id`. Otherwise call `beatra.voices.list` when a catalog voice
   still needs to be selected. Never put a display name in `voice`.
3. If the user already supplied an approved speech track, skip synthesis
   and admit that audio for video. For a script route, call
   `beatra.models.list` with
   `{"capability":"text_to_speech"}` and `{"capability":"image_to_video"}`.
   Confirm that a current video card admits `[image, driving_audio]`. Compare
   the portrait's actual MIME, dimensions, byte size, and alpha-channel
   presence with every advertised image constraint. Confirm planned speech
   can fit a video duration the route can fully contain. If the weekly
   script is longer than the longest containable clip, split it into
   sequential containable segments. Each segment is its own paid speech
   call and its own paid video call, each with a new `client_request_id`.
   Do not shorten words to cheapen a clip. Use `mp3` only when
   the live speech card supports it and the live video card accepts
   `audio/mpeg`. If the user requested `flac`, `opus`, or `pcm` and the
   video route does not accept the resulting format, explain the
   incompatibility before any paid call and obtain the user's choice. Do
   not silently change the format. If any required media fact is
   unavailable or incompatible, stop before TTS.
4. On the script route only, show the narration arguments and paid
   boundary. Freeze the script, voice, format, and one speech
   `client_request_id` per segment. Submit `beatra.speech.synthesize`
   exactly once per segment through the bundled client. Skip this step
   when approved speech already exists.
5. For each speech segment, or for the supplied approved track, poll
   until terminal audio facts exist. On the script route, poll each
   narration task with `beatra.tasks.get`. Read the returned artifact
   plus actual `task.output.audio.mime_type`, `duration_seconds`, and
   `size_bytes` when present. Approve the real audio before that
   segment's video. Never treat a script preview, expected duration, or
   task metadata as an audio review.
6. For each approved audio segment, refresh the `image_to_video` cards
   and admit the actual portrait plus that audio. Recheck every image
   fact and compare the audio's actual MIME, duration, and byte size
   with the current driving-audio constraints. If terminal audio size
   is absent, obtain it from trusted artifact metadata; if it remains
   unavailable, stop before video. Use the smallest supported integer
   video duration at or above the actual speech length. Show the video
   admission card before any video `client_request_id` or
   `beatra.videos.animate` call: route `image_to_video`, tool
   `beatra.videos.animate`, approved portrait and speech artifacts,
   prompt, audio-led duration, resolution if set, output count,
   provisional live estimate, the fact that the 600-credit signup gift
   usually cannot start this video, and what happens if the balance is
   short. Do not submit until the user confirms they have topped up or
   already have enough credits. Approved narration does not authorize
   the video call.
7. Submit `beatra.videos.animate` exactly once per approved audio
   segment. Do not configure a host Beatra Connector. Do not use
   REST/OpenAPI as a fallback. Poll each video task with
   `beatra.tasks.get` until terminal.
8. Deliver the returned clips in script order with actual dimensions,
   duration, usage, and `billing.net_charged_credits`. Review identity,
   clarity, lip timing, and must-keep drift.

## Decisions that require confirmation

Likeness and voice rights, clone admission, narration, and the video
admission card each require their own confirmation.

## Recovery

Each paid stage has its own frozen payload and ID. Recover a lost create
response only with that stage's identical payload. Recover a lost task
ID through `beatra.tasks.list` and `beatra.tasks.get`. Call
`beatra.tasks.cancel` only when the user asks to cancel that stage. On
`insufficient_balance`, keep the top-up URL inside the balance error
exact and retry the same frozen ID only after the user says they have
topped up. If a create returns no `task_id`, do not poll; reconcile
before minting a new ID.

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

- Read [Founder avatar workflow](references/workflow.md) for clone,
  narration, admission cards, payloads, and review.
- Read [Installation and authentication](references/installation-and-auth.md)
  only when authorization needs attention.
- Read [Installation registration](references/installation-registration.md)
  for first-use registration.
- Read [Tasks and results](references/tasks-and-results.md) and
  [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
  for task and billing facts.
- Read [Bundled MCP Client diagnostics](references/mcp-connection.md) when
  the bundled client cannot connect.
- Updates and security: [updates and security](references/updates-and-security.md)
- Read [Uninstall and disconnect](references/uninstall-and-disconnect.md)
  only when the user asks to remove the package.

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
