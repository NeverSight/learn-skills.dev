---
name: "audio-drama-voice-studio"
description: "Give every character in your script its own voice and get the whole scene recorded line by line, in script order, as numbered clips ready to drop into your editor. This AI multi-character voice generator covers audio drama and radio play, dramatised fiction and audiobooks with a cast, dialogue voice over, two-host and panel shows, scripted ads with two roles, and course roleplay scenes: decide who is who first — age, temperament, how far apart the voices should sit — give the narrator a voice of their own, and afterwards re-record just the one line you want to change. Also used for audio drama voice generator work, multi-character voice generator work, multi-speaker audio, dialogue text to speech, script to dialogue audio, AI audio drama, radio play voices, and full cast voiceover."
---

# Audio Drama Voice Studio

Give a script a cast. Assign one voice per character, record every line in that
character's voice, and hand back the clips in script order so the scene can be
assembled and posted.

## What you get

A finished run returns:

- One numbered audio clip per speech block, labelled with the speaking
  character, in script order
- A cast sheet: each speaker, how they sound relative to the others, and the
  voice kept for the whole piece
- The real duration, size, and format the model returned for every clip

It does not mix the clips into one episode file. Assembly stays in the user's
editor. The rendered type comes from the model and is reported on delivery.

## Ways to run it

- **Cast and record** — default. Read the script, freeze one voice per
  character, synthesize each block, deliver labelled clips.
- **Add an owned voice** — optional. Clone a sample the user owns or has
  permission to use, then put that voice on the cast sheet like any other.

Casting and script preparation are free. Synthesis is paid. Cloning is a
separate paid step with its own confirmation.

## Scope and routing

Use this Skill when a script or dialogue passage needs more than one speaker:
audio drama and radio play, dramatised fiction, audio novels with named roles, a
two-host or panel show, a dialogue-driven course or training scene, a scripted
ad with two or more roles, or an interactive story with distinct characters.

Route a single-narrator book or course to `ai-audiobook-narration`. Route a
podcast episode read by one host to `ai-podcast-voiceover`, and a short-video
voiceover to `short-form-voiceover-audio`. Route creating a reusable voice from
a sample to `voice-cloning-studio` when cloning is the whole job. If a character
on this cast needs a cloned voice, clone it in this Skill. Route general
single-voice work to `beatra-ai-voice-studio`. Route a narrated video with
pictures to `novel-promo-video-maker`.

## Inputs and defaults

The one hard input is the script text. Reuse the genre, era, tone, character
notes, language, and any voice already chosen in the conversation.

Ask only when the answer changes the paid result: who speaks each line, when the
passage is prose with no speaker attribution and the text does not settle it.

Defaults that avoid extra questions:

- One voice per named character, plus one narrator voice when the script has
  narration.
- Speaker order follows the script; nothing is reordered.
- `model` omitted so Beatra can route, unless the user names one.
- `language` omitted for automatic detection, unless the user asks for a
  specific language or the script mixes several.
- One synthesis call per speech block, so a single line can be redone without
  paying for the whole scene again.

## Golden path

1. Read the script and build a cast sheet: every speaking character, their age
   and temperament, and the narrator if there is one. Split the script into
   speech blocks, each block belonging to exactly one character. Show that
   numbered cast sheet and block list to the user. That sheet is the free
   visible result. Planning is not approval.
2. Call `beatra.voices.list` only when a voice is still needed or the user asks
   to browse or compare, then assign one voice ID per character and keep that
   assignment fixed for the whole piece.
3. Read the live `text_to_speech` card with `beatra.models.list`:

   ```bash
   python3 scripts/mcp_client.py call beatra.models.list
   ```

   ```json
   {"capability": "text_to_speech"}
   ```

   Take the rate from the returned card. Speech is charged linearly per 1,000
   weighted characters where each Han ideograph counts as two and every other
   character counts as one, and a block under 1,000 is charged for its actual
   weighted characters rather than a full block.
4. Show one current production card for the whole scene and wait. The free
   cast sheet stays usable if they stop here.
5. Synthesize each block with `beatra.speech.synthesize`, one call per block,
   submitting each exactly once and polling its own task.
6. Deliver the blocks in script order, numbered, each labelled with its
   character. Report the actual returned duration, size, MIME type, and URL or
   artifact for every block, plus the resolved model and
   `billing.net_charged_credits`.
7. Review what the host Agent can actually play. Check that each block carries
   the assigned voice, that pronunciation and pacing suit the line, and that the
   order matches the script.

A revision is one block, not the scene: re-synthesize only the changed block
with a new request ID, and leave the accepted blocks untouched. Read
[the audio drama workflow](references/workflow.md) for cast-sheet shape, payload
details, per-character voice discipline, recovery, and delivery review.

## Decisions that require confirmation

Planning, the cast sheet, and live price quotes are free. They are not approval.

Before the first paid `beatra.speech.synthesize` submit, show one current
production card for the scene and wait:

1. Work — the scene in the user's words, and that this is a generate call for
   the listed blocks.
2. Credits — the live price just read from the `text_to_speech` card. Do not
   reuse a remembered number.
3. Count — one paid call per speech block. A revision of one line is another
   call.
4. Identity — one new opaque `client_request_id` per block. If script, speaker,
   voice, language, or model change, mint a new ID. Never reuse an ID across
   blocks or for different arguments.
5. If we stop here — the cast sheet and split script remain usable.
6. If the balance is insufficient — relay the official message and its top-up
   URL exactly. Translate the prose; keep the URL. Do not retry until the
   user says they have topped up.

Submit once through bundled `scripts/mcp_client.py`. Poll `beatra.tasks.get`.
Deliver actual bytes plus `billing.net_charged_credits`. Do not promise the
prepaid estimate is the final charge.

Voice cloning needs its own explicit consent confirmation and its own six-field
production card, separately from synthesis. A synthesis confirmation never
authorizes `beatra.voices.clone`.

## Using a cloned voice

Use `beatra.voices.clone` only when the user wants a reusable voice from a
sample and explicitly confirms that they own the voice or have the owner's
permission. Possession of an audio file is not consent. Obtain that confirmation
before uploading, set `consent_attested: true` only afterwards, and submit once.

Read the live `voice_clone` card before quoting anything:

```bash
python3 scripts/mcp_client.py call beatra.models.list
```

```json
{"capability": "voice_clone"}
```

Show the clone production card and wait:

1. Work — one authorized voice sample (`beatra.voices.clone`) for a named
   character on the cast sheet.
2. Credits — the live `voice_clone` price just read. Do not reuse a remembered
   number.
3. Count — one paid clone call for this sample.
4. Identity — one new opaque `client_request_id`.
5. If we stop here — the cast sheet remains usable with catalog voices.
6. If the balance is insufficient — relay the official message and its top-up
   URL exactly. Translate the prose; keep the URL. Do not retry until the
   user says they have topped up.

Do not offer a free clone or a free sample that replaces the clone. A successful
clone is already activated and returns a `voice_id` that this cast sheet can
use like any other voice. Sample limits and live-card fields live in
[the audio drama workflow](references/workflow.md).

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

## How this Skill executes

Use the bundled `scripts/mcp_client.py` for every remote Beatra operation: the
MCP tool name is the CLI argument after `call`, and one JSON object goes on
standard input. Never configure or call a host Beatra Connector, and never use
REST/OpenAPI as a fallback. Register the package with
`beatra.installations.register` on first use. Every creation is an asynchronous
task: submit once, then follow that task to a terminal state.

## Recovery

Save every task ID the moment it returns and poll with `beatra.tasks.get`;
`queued` and `running` mean wait. Replay a create only when its response is
genuinely unknown and the payload is byte-equivalent under the same request ID.
If a task ID is lost, use `beatra.tasks.list` with the capability of that call
(`text_to_speech` for synthesis, `voice_clone` for a clone), follow every
returned `next_cursor` needed to cover the submission window, confirm candidates
with `beatra.tasks.get`, and recover the original before considering new work. If a
request ID itself is lost, do not invent a new one and do not replay. Call
`beatra.tasks.cancel` only at the user's request; on `409`, keep polling the
original task and report cancellation only when its terminal status is
`canceled`.

When one block fails and the rest succeed, recover that block alone. The
delivered blocks stay valid and are not re-synthesized.

## References by task

- [Audio drama workflow](references/workflow.md): cast sheet, block splitting,
  exact payloads, per-character voice discipline, cloned voices, recovery,
  delivery review, and balance questions.
- [Installation and authentication](references/installation-and-auth.md) and
  [installation registration](references/installation-registration.md): first
  use and shared credentials.
- [Tasks and results](references/tasks-and-results.md) and
  [billing, errors, and recovery](references/billing-errors-and-recovery.md):
  task, artifact, and billing facts.
- [Bundled MCP Client diagnostics](references/mcp-connection.md): client
  operation and connection diagnostics; do not configure a host Connector.
- Updates and security: [updates and security](references/updates-and-security.md)
- [uninstall and disconnect](references/uninstall-and-disconnect.md): stopping
  use and removing shared credentials.

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
