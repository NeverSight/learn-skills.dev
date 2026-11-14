---
name: "short-video-bgm-studio"
description: "Describe the footage and get an original instrumental track written for it, yours to keep and use commercially. This AI background music generator turns a scene, mood, and tempo feel into royalty-free BGM for short videos, vlogs, product clips, tutorials, livestream and store loops, podcast intros, and slideshow recaps, with an energy arc you choose — a calm or immediate opening, a lift at the moment that matters, a clean ending — room left for narration, and a result you can listen to before you publish."
---

# Short Video BGM Studio

Turn a description of the footage into an original instrumental track built for
it: read the scene, shape an energy curve that fits how the piece moves, and
return a result the user can hear before publishing.

## Scope and routing

Use this Skill when a video, livestream, podcast, store, or brand moment needs
background music and no vocal is wanted. It fits short-video posts, vlogs,
product and unboxing clips, tutorial and course footage, livestream and store
loops, podcast intros and outros, and slideshow or event recaps.

Scoring a finished cut to edit points is not this package; this package takes a
footage or scene description. Route a song with sung lyrics to
`beatra-ai-music-creator`. Route finished lyrics that need a melody to
`suno-lyrics-to-song`, a gift or occasion song to `personalized-song-maker`, and
a cover or re-arrangement of an existing song to `ai-song-cover-studio`. Route
a music video built around a finished track to `ai-music-video-clip-maker`, and
spoken narration to `short-form-voiceover-audio`.

## Inputs and defaults

The hard inputs are a footage or scene description plus the length in seconds.
Do not spend unless the user asked to generate. Reuse the platform, footage
description, brand tone, target length, and any reference track already present
in the conversation.

Ask only when the answer changes the paid result: the intended use, when the
request is just "make music" with no scene attached.

Defaults that avoid extra questions:

- `instrumental: true` with no lyrics, because this route is background music.
- A short, loop-friendly duration when the user did not name a length.
- A calm-to-lift energy arc with a clean resolved ending, which the full take
  keeps; a cut to a shorter exact length ends on a short fade.
- `model: "suno-6"` for ordinary generation. Never omit the model and never
  silently use `auto`; pass a different model only when the user names one.
- Room left for a voice, since most short-video BGM sits under narration.

## Golden path

Briefing and planning are free. The generation call and every cut, loop, or WAV step are paid.

1. Lock the scene and the length in seconds, then write a short music card from
   the footage: use and destination, mood, genre, tempo feel, instrumentation,
   the energy arc across the cut, the intended length, whether narration sits on
   top, and anything to avoid.
2. Turn the card into one positive prompt that carries genre, mood, tempo feel,
   instrumentation, structure, and intended use in a single coherent direction.
3. Call `beatra.models.list` with a copyable
   `{"capability":"text_to_music"}` — or
   `{"capability":"reference_audio_to_music"}` when the user supplied a
   reference recording — before the production card. Read the `pricing` of
   the chosen model's entry (`suno-6` unless the user named another eligible
   model) and show those credits on the card per slot and in total. When the
   card will list a cut or a loop, also read `{"capability":"audio_process"}`
   and count each cut or loop in that total. Never a remembered number. Read the live card rather than assuming a model, a
   control, or an input limit.
4. **Confirm before paid work.** Show the frozen prompt, `instrumental: true`,
   the title, the length fields when sent (for a target under 30 seconds, with
   the user's number: "made at 30 seconds, then cut to your 15 seconds; the
   cut ends on a short fade, the full take keeps its written ending", with the
   cut as its own line below), the model, any accepted model options, the live
   credits just read, each cut or loop as its own line with its live
   `audio_process` price and its own `client_request_id`, a
   commercial-clearance note for this original instrumental, and one opaque
   stable `client_request_id` for the generation.
5. Submit `beatra.music.generate` exactly once for one instrumental track,
   record the task ID immediately, and poll that same task.
6. Deliver every returned clip in order with its real duration, MIME type, size,
   and URL or artifact ID, plus the returned title when present, the resolved
   model, the actual usage, and `billing.net_charged_credits`.
7. Review the result against the music card. Read the actual returned duration
   rather than the requested one, and say plainly what the host Agent could not
   hear.
8. **Fit and finish the chosen take.** With the music tools and a length from the
   user, cut the chosen take to that length with `beatra.audio.process`
   `operation: "trim"`
   (`target_duration_ms`, a short `fade_out_ms`; a paid call at the live `audio_process` price (`beatra.models.list` with `{"capability": "audio_process"}`), listed on the track's card as its own line with its own `client_request_id`) and deliver it beside the uncut take: the cut is exact and ends on a
   short fade; the uncut take keeps its written ending. A take that already falls
   short of the length keeps its real length: say the difference. Then offer a
   WAV version made from the uncut take (`beatra.music.edit` `deliverable`
   `kind: "wav"`, own card, live `music_wav` price, own `client_request_id`), and
   cut the WAV the same way afterwards (one more paid cut, listed on the WAV's card; a WAV stays WAV). See
   [music editing and audio](references/music-editing-and-audio.md).

Length: when this account has the music tools (the bundled client's `tools`
command lists `beatra.music.edit` and `beatra.audio.process`; see
[music editing and audio](references/music-editing-and-audio.md)), send
`duration_seconds` for the length the user gave (at most 360; for a longer run,
make a shorter piece and `loop` it), or 30 when they gave no length or less than 30 seconds (not
with a reference recording; fit a reference-guided track afterwards with `trim`
or `loop`), and leave out `duration_fit`. The take then lands within about 10% of
that length. The uncut take keeps its written ending and can still get a WAV
version; step 8 cuts the chosen take to the user's length and delivers the cut
beside it. Without the tools, keep the length as direction in the prompt, as
before. Always report the real returned length.

Loops: a bed that must run clearly longer than one generation (more than about
10% over the take), or loop under a long scene, is generated once, then
lengthened with `beatra.audio.process` `operation: "loop"` to the target length (a paid call at the live `audio_process` price with its own `client_request_id`, listed on the track's card as its own line when the user asked for that length together with the track, otherwise on its own card). When a
player repeats the file itself (a store or livestream loop), send `loop_count`
with `end_with_fade: false` instead, as the shared reference says. A bed within
about 10% of its target keeps its real length: report the difference. Report the
real length and the loop's seam in plain words ("how smoothly it joins where it
repeats: 0.91 out of 1, higher is smoother"); never promise an inaudible seam.
Without the music tools, ask for a loop-friendly arrangement and do not promise
a seamless loop. Space for narration is arrangement direction in the prompt.

Read [the BGM workflow](references/workflow.md) for the music card, prompt
shape, payloads, model options, reference-guided tracks, recovery, and delivery
review.

## How this Skill executes

Use the bundled `scripts/mcp_client.py` for every remote Beatra operation: the
MCP tool name is the CLI argument after `call`, and one JSON object goes on
standard input. Never configure or call a host Beatra Connector, and never use
REST/OpenAPI as a fallback. Register the package with
`beatra.installations.register` on first use. Every creation is an asynchronous
task: submit once, then follow that task to a terminal state.

## Decisions that require confirmation

Confirm before submitting. Show one current production card and wait:

1. Work — the instrumental bed in the user's words, a `beatra.music.generate` call, and with the music tools and a length from the user, the cut or loop of the chosen take as its own `beatra.audio.process` line.
2. Credits — the live price of the chosen model (`suno-6` by default) just read from `beatra.models.list`, and the live `audio_process` price of a cut or loop listed, per line and in total. Never a remembered
   number.
3. Count — one paid call for this track, plus its cut or loop when listed. A later revision is another slot.
4. Identity — one new opaque `client_request_id` per line listed on the card (the track, and its cut or loop when listed). A changed prompt, title,
   length, model, option, reference track, or instrumental setting mints a new
   ID.
5. If we stop here — the music card remains usable.
6. If the balance is insufficient — relay the official message and its top-up
   URL exactly. Translate the prose; keep the URL. Do not retry until the user
   says they have topped up.

Also freeze the prompt, the instrumental setting, the title, the length, the
model and any model options. A changed prompt, title, length, model, option,
reference track, or instrumental setting is new paid work with a new request ID.
The WAV version is a later paid step: its own call on its own card with its own
ID.

When the user asks how many credits remain, call `beatra.wallet.get`. When they
ask what was charged, call `beatra.wallet.ledger`. Both are read-only. Do not
invent an account-balance or top-up tool. Do not make `wallet.get` a required
step before every paid submit.

When the user supplies a reference recording, upload it once through the bundled
client, state what should carry over and what should change, and keep that as
musical direction rather than a promise about melody or arrangement.

## Recovery

Save the task ID the moment it returns and poll with `beatra.tasks.get`;
`queued` and `running` mean wait. Replay a create only when its response is
genuinely unknown and every validated argument is byte-equivalent under the same
request ID. If the task ID is lost, use `beatra.tasks.list`, confirm candidates
with `beatra.tasks.get`, and recover the original before considering new work.
If the request ID itself is lost, do not invent a new one and do not replay.
Call `beatra.tasks.cancel` only at the user's request; on `409`, keep polling the
original task and report cancellation only when its terminal status is
`canceled`.

## References by task

- [BGM workflow](references/workflow.md): music card, prompt construction,
  payloads, model options, reference-guided tracks, recovery, and delivery
  review.
- [Installation and authentication](references/installation-and-auth.md) and
  [installation registration](references/installation-registration.md): first
  use and shared credentials.
- [Music editing and audio](references/music-editing-and-audio.md): the
  length, loop, and WAV steps, their prices, limits, and errors.
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
