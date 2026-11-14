---
name: "music-generation-studio"
description: "Create original songs, AI-generated music, lyrics-to-song tracks, instrumentals, background music, video soundtracks, jingles, multilingual songs, and reference-led arrangements from a clear creative brief. This AI music generator and AI song maker develops genre, mood, structure, singable lyrics, vocal direction, and production style, then creates reviewable audio with Suno 6 or another model you explicitly choose. Use it as an AI music studio for songwriting, an AI lyrics writer, text-to-music creation, BGM generation, brand music, podcast themes, game music, bilingual songs, or focused new versions of reference audio. Review vocals, pronunciation, duration, loop points, and arrangement fit after generation, then refine the strongest result."
---

# Music Generation Studio

Develop a theme, scene, lyric fragment, complete lyric, functional music brief,
or reference recording into one coherent musical direction and,
when the user wants audio, one intentional generation request. The deliverable
may be a song, instrumental, BGM, soundtrack, jingle, multilingual track, or
reference-led new arrangement. Treat singer identity, pronunciation, loop
points, melody carryover, and mastering as qualities to review after
generation rather than guaranteed properties. A length is a control when this
account has the music tools (see
[music editing and audio](references/music-editing-and-audio.md)).

Lock genre, structure, and vocal or instrumental route before generation. A
“surprise me” random song is not this package's default. Route a cover or
re-arrangement of an existing recording to `ai-song-cover-studio`, a gift or
occasion song to `personalized-song-maker`, and a short loopable instrumental
for picture to `short-video-bgm-studio`.

The hard inputs are a theme or lyrics plus the intended use. If purpose,
genre, or vocal route is empty, gather them first; do not fill the gap with a
default pop brief.

Use the bundled `scripts/mcp_client.py` for every Beatra operation. Do not
configure or use a host Beatra Connector. Never use REST/OpenAPI as a fallback.
For ordinary calls, run
`python3 scripts/mcp_client.py call <tool-name>` and pass one JSON object on
stdin. For local files, use only the dedicated upload command described below.
See [Bundled MCP Client diagnostics](references/mcp-connection.md) only when the
bundled path needs diagnosis.

## Shape the direction first

Reuse every settled choice in the conversation. Infer ordinary creative details
from the destination when that is safe. Ask only when a missing answer changes
the lyrics, reference direction, vocal or instrumental route, exact paid payload,
or another high-impact user choice.

Before generation, prepare one compact production card:

- destination and listener;
- title, premise, emotional arc, primary genre, tempo feel, instrumentation,
  structure, mix direction, ending or loop direction, and exclusions;
- vocal or instrumental route;
- full lyrics, language and register, and vocal direction when the track has
  vocals;
- selected model and model-specific controls;
- reference intent and the qualities that should carry over or change when a
  reference is involved; and
- the fact that the next action is one billable generation.

For instrumentals, omit lyrics and make room for dialogue or other functional
needs in the creative direction. For vocal music, finish and show material lyric
changes before generation. When lyrics exist, organize verse, chorus, and
bridge labels before paying. Do not put BPM, key, or tempo numbers into the
style caption. Lyrics writing, creative planning, model discovery,
prompt preparation, and critique do not require a paid music call. See
[intent and routing](references/intent-and-routing.md),
[creative brief and style](references/creative-brief-and-style.md),
[lyrics craft](references/lyrics-craft.md), and
[vocal, language, and tags](references/vocal-language-and-tags.md).

When a brief uses artist shorthand, translate it into actionable genre, era,
tempo, instrumentation, harmony, vocal texture, phrasing, and mix attributes.

## Choose and validate the model

Set `model: "suno-6"` for this package's ordinary generation. Never omit the
model and never silently use `auto`. Before every production card, call
`beatra.models.list` with a copyable payload:

```json
{"capability": "text_to_music"}
```

When the route uses a reference recording, also call it with:

```json
{"capability": "reference_audio_to_music"}
```

Read the `pricing` of the chosen model's entry (`suno-6` unless the user named
another eligible model) and show those credits on the card per slot and in
total. Never a remembered number. Call it again when the user requests another
model or needs a model-specific capability. Do not silently substitute a model.

Length: when this account has the music tools (the bundled client's `tools`
command lists `beatra.music.edit` and `beatra.audio.process`; see
[music editing and audio](references/music-editing-and-audio.md)), send
`duration_seconds` when the user names a length (not with a reference
recording; fit a reference-guided track afterwards with `trim` or `loop`). A song
with lyrics gets `duration_seconds` of 30 or more that the lyrics fit, without
`duration_fit`: a shorter target, or `exact`, cuts the singing at the target, so
cut afterwards with `beatra.audio.process` `trim` only when the user accepts
losing the end. An instrumental that needs exact seconds adds
`duration_fit: "exact"`, and a bed that must run longer or loop (generated
with `duration_seconds` of 30 or more and no `duration_fit`; see the shared
reference) is lengthened with `beatra.audio.process`.
[Creative brief and style](references/creative-brief-and-style.md) covers
background music. Without the tools, keep the length as direction in the prompt
and do not add a duration argument. Always report the real returned length.

Use only controls returned or documented for the selected model family. Suno
and MiniMax options are not interchangeable. Validate the exact payload using
[model routing](references/model-routing.md) and use the examples in
[music recipes](references/music-recipes.md) as patterns rather than fixed
claims.

## Use reference audio

For a local FLAC, MP3, or WAV reference, run only:

```text
python3 scripts/mcp_client.py upload <path> --mime-type <type>
```

The bundled command obtains and validates the upload grant, uploads exactly the
file bytes, and returns the artifact to use as `reference_audio`. Do not replace
it with host HTTP, a connector, REST, or a hand-written grant and PUT sequence.
The general upload limit is 100 MB; the selected music model can impose a lower
size or duration limit.

Describe what should carry over and what should change. A reference guides a
new creative result; after generation, review melody, vocal character, energy,
instrumentation, and arrangement against that direction.

## Confirm the paid boundary once

Even a direct, well-specified request gets the production card below first.
Approval of the complete card authorizes that exact request once; do not add a
second confirmation. An estimate, comparison, lyric review, direction choice,
or “do not generate yet” is not approval.

Show one current production card and wait:

1. Work — what will be made in the user's words, a `beatra.music.generate` call,
   plus any finishing step the user asked for with it.
2. Credits — the live price of the chosen model (`suno-6` by default) just
   read from `beatra.models.list`, per slot and in total, with each finishing
   step as its own line at its live `audio_process` price; the total includes
   every line on the card. Never a remembered number.
3. Count — one paid call for this generation, plus one per finishing line on
   this card. A later revision is another slot.
4. Identity — one new opaque `client_request_id` per line listed on the card. Any changed prompt, lyrics,
   file, model, or control mints a new ID.
5. If we stop here — the production card and lyrics remain usable.
6. If the balance is insufficient — relay the official message and its top-up
   URL exactly. Translate the prose; keep the URL. Do not retry until the user
   says they have topped up.

Follow this golden path: lock structure and the dynamic arc, write an
executable caption plus labelled lyrics, then confirm one paid request that
produces a limited set of takes. After review, fix only the section that needs
it or continue a chosen song with the music tools (see Deliver and review the
music); do not automatically regenerate the whole song. Never extend
automatically or repeatedly; each revision is its own confirmed call.

Before a billable call, make model, title, lyrics or instrumental status,
reference, important controls, and the paid calls the card lists visible. Create a
stable 1..128-character `client_request_id` only after that payload is final.
Any change to prompt, lyrics, instrumental flag, title, model, reference,
model options, or any other argument accepted by the current or a future MCP
generation schema is a new paid request with a new identity and confirmation.
Fields outside the published MCP schema are ignored and do not change the
request identity or task.

Let the bundled client perform its cached, best-effort, non-billable
`beatra.installations.register` step automatically. Do not add manual
registration to the creative workflow.

Submit `beatra.music.generate` once. Retain its `task_id` and poll the same task
with `beatra.tasks.get`. Honor a returned `deadline_at`; otherwise stop active
polling after 30 minutes, report the current state and how to resume, and do not
resubmit. Cancel only when the user asks via `beatra.tasks.cancel`; if cancel
conflicts with a terminal transition, return to the same task.

For an uncertain submission or lost task ID, search recent work with
`beatra.tasks.list` using the matching music capability. List results do not
contain the complete request: call `beatra.tasks.get` for each plausible
candidate and compare its `task.input`, resolved model, reference, and options
with the saved full payload. Only an exact identical retry may reuse the same
`client_request_id`. Never create replacement paid work merely because a
response was lost or a task is slow. See
[tasks and results](references/tasks-and-results.md) and
[billing, errors, and recovery](references/billing-errors-and-recovery.md).

## Deliver and review the music

On success, present every `task.output.clips` entry in returned order. Include
the returned title and lyrics when present plus `clip.audio.url`, artifact ID,
duration, MIME type, and size. Report factual task identity and
`billing.net_charged_credits`. When the task returns `task.links.assets`, use
that exact destination for asset management; do not invent a generic URL.

Review composition, lyrics, vocal performance, pronunciation, role assignment,
arrangement, ending, and production only when the host can actually play the
audio. Otherwise label listening review incomplete while still delivering the
factual artifacts. Preserve successful qualities and turn the largest gap into
one focused, newly approved step: a new generation or, when this account has the
music tools (see Choose and validate the model), `beatra.music.edit` with
`operation: "replace_section"` to fix one part of a chosen song or
`operation: "extend"` to continue it. Each is its own paid call with its own
card, the live price for that step, and its own `client_request_id`; never extend
automatically or repeatedly. Follow
[review and iteration](references/review-and-iteration.md).

When the user asks how many credits remain, call `beatra.wallet.get`. When they
ask what was charged, call `beatra.wallet.ledger`. Both are read-only. Do not
invent an account-balance or top-up tool. Do not make `wallet.get` a required
step before every paid submit.

## References by task

- Intent, lyrics, instrumental, multilingual, and reference routes: [intent and routing](references/intent-and-routing.md)
- Brief, style, lyrics craft, vocal direction, and language: [creative brief and style](references/creative-brief-and-style.md), [lyrics craft](references/lyrics-craft.md), and [vocal, language, and tags](references/vocal-language-and-tags.md)
- Current model selection and exact payload controls: [model routing](references/model-routing.md)
- Length, loops, fixing one part of a song, extending it, and extra files: [music editing and audio](references/music-editing-and-audio.md)
- Request patterns and focused result review: [music recipes](references/music-recipes.md) and [review and iteration](references/review-and-iteration.md)
- First installation or expired authorization: [installation and authentication](references/installation-and-auth.md)
- Bundled command syntax and diagnostics: [Bundled MCP Client diagnostics](references/mcp-connection.md)
- Task recovery, billing, and returned results: [tasks and results](references/tasks-and-results.md) and [billing, errors, and recovery](references/billing-errors-and-recovery.md)
- Updates and security: [updates and security](references/updates-and-security.md)
- Package removal and shared credential handling: [uninstall and disconnect](references/uninstall-and-disconnect.md)

## Removal

For removal or credential cleanup,
follow [uninstall and disconnect](references/uninstall-and-disconnect.md).
Never directly delete `~/.beatra` or shared credentials because another Beatra
package may use the same connection.

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
