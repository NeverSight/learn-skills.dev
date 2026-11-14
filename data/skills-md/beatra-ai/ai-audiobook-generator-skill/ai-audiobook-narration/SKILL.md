---
name: "ai-audiobook-narration"
description: "Turn final manuscript or course text into an audiobook with one consistent narrator. This AI audiobook generator and AI audiobook narration workflow organizes chapters, settles names and specialist pronunciations, shapes long-form pacing, helps choose a suitable audiobook narrator, and creates a representative sample before the remaining book. Use it for manuscript-to-audiobook production, chapter-by-chapter audiobooks, course narration, long-text-to-speech, and sample chapters, with up-to-date price estimates, ordered audio delivery, consistent narrator voice, and focused passage refinements."
---

# AI Audiobook Narration

An audiobook is not a long TTS clip. It is a structured deliverable of many
chapterized files. Open on one of three scenes: fiction; nonfiction or course;
or sample-only. Route M4B packaging, translation, and professional mastering
out. Keep a listing cover and cloning a narrator from a supplied sample in
this package.

Turn final manuscript or course text into ordered chapter audio. Work as an
audiobook producer: preserve the manuscript's meaning, direct one
sustainable narrator performance, prove the direction with a representative
pilot, and expand only after that pilot is accepted.

## Start with the smallest complete intake

Reuse everything already supplied. Before narration, obtain only the hard
inputs that are still missing:

- final readable text for at least the pilot;
- chapter or section order and the target BCP-47 language or dialect;
- a pronunciation table extracted from the full manuscript for recurring
  names and terms, confirmed by the user before it is frozen;
- a narrator sample when the user wants their own narrator; and
- title and tone when the user wants a listing cover.

Ask for a missing hard input rather than inventing it. Create a
chapter-and-segment ledger. Preserve the intended listening order,
label every segment, and split at chapter, section, scene, paragraph, or
sentence boundaries. Never split mid-sentence, and keep each submitted `input`
at or below 50,000 characters. Remove only page-only material the user does not
want spoken. Follow [chapter production](references/chapter-production.md) for
text preparation, casting, and the pilot boundary.

## Freeze a real voice and a viable model path

When the user brought a narrator sample, present a current `beatra.voices.clone`
admission card first — route `voice_clone`, tool `beatra.voices.clone`, live
`beatra.models.list` price for one successful activated voice, the provisional
estimate, the fact that the 600-credit signup gift usually cannot start this
clone, and what happens if the balance is short. Do not create
`client_request_id` or submit until the user confirms they have topped up or
already have enough credits for this estimate. Do not offer a free clone or a
free sample that replaces the clone. Then freeze the returned `voice_id` so
every chapter uses the same performer. Without a sample, do not default to
cloning: use `beatra.voices.list` when the narrator is not already frozen. A
returned opaque `voice_id` is the only valid value for synthesis `voice`; never
substitute a display name, a prose preference, or a remembered label. Record the
selected `voice_id`, its preview, stated language information, and
`compatible_models` in the ledger. Use previews for casting without creating
paid audio.

Call `beatra.models.list` with `capability: "text_to_speech"` before deciding a
model, checking language support, or estimating cost. For an explicit model,
require an available live card that is also in the frozen voice's
`compatible_models`, then confirm that card supports the requested language.
Language is not an `auto` routing input: the service resolves `auto` from the
voice first and validates language afterward. Build the `auto` set from all live
available voice-compatible candidates. Compare a valid BCP-47 request's primary
language with every candidate's `constraints.supported_languages`, using only
documented aliases. If any potential candidate does not support the requested
language, do not use `auto`; show the viable explicit choices and ask the user
to confirm one compatible, language-supported model. Use `auto` only when all
potential candidates support the language, and price the full candidate set.

Default to `model: "auto"`, `format: "mp3"`, `speed: 1.0`, `volume: 1.0`,
`pitch: 0`, no emotion, and no explicit sample rate unless the user or
destination requires another supported value. Choose the pilot where the book
is hardest: for fiction, a passage dense with dialogue and proper names; for
nonfiction or a course, a passage dense with terms and numbers. Do not generate
a cover unless the user asked for a listing pack. See [performance, cost, and
quality](references/performance-and-quality.md) for compatible-model selection,
live price math, and review criteria.

## Golden path

Build the chapter ledger. Make the text listenable and freeze the confirmed
pronunciation table. When a narrator sample is present, present the clone
admission card, wait for top-up or balance confirmation, then freeze the
returned `voice_id`; otherwise use `beatra.voices.list`. Present the pilot
synthesis card, then wait for an ear pass. Price the remaining chapters on their own card. When the user wants a
complete listing pack, present a separate cover confirmation card for
`beatra.images.generate`. Each new paid tool has its own current production
card. Do not automatically retry a paid call. A changed argument needs a new
`client_request_id`.

## Price and confirm the pilot

Planning is free; `beatra.speech.synthesize` is paid. `beatra.voices.clone` is
a separate paid step with its own current admission card when a narrator sample
is present. That card must include the live `beatra.models.list` price, the
600-credit gift fact, and what happens if the balance is short. Do not create a
clone `client_request_id` or submit until the user confirms they have topped up
or already have enough credits for this estimate. Do not offer a free clone or
a free sample that replaces the clone. On `insufficient_balance`, relay the
returned public message, keep the URL exact, translate the rest, and retry the
same frozen clone `client_request_id` only after the user says they have topped
up. `beatra.images.generate` is a separate paid step with its own current card
when a listing cover is wanted. Count the pilot's billable quantity exactly as
the live card defines `beatra_weighted_characters`: each Han ideograph weighs 2
and every other character weighs 1. Apply the card's current
`estimate_formula`, `unit_price_credits`, and `scale`. When `auto` can resolve
to more than one applicable voice-compatible card, show the resulting range or
a clearly labeled upper bound.

A clone approval never authorizes the pilot, a pilot approval never authorizes
remaining chapters or a cover, and a cover approval never authorizes speech or
clone. Before paid narration, present one production card containing:

- the pilot scope, ordered segment count, and weighted-character total;
- frozen `voice_id`, model choice or applicable `auto` range, BCP-47 language,
  format, sample rate if set, speed, volume, pitch, and emotion if set;
- the live pricing basis, formula, unit price or range, and estimated credits;
  and
- a clear statement that approval creates exactly the listed paid requests.

Wait for explicit approval of that current card. Do not add a second
confirmation when the user has already approved the exact current card. Every
newly proposed paid execution must be covered by an explicit current-card
confirmation; never automatically retry a paid call. A pilot approval covers
only the pilot. After review, price the remaining chapters as an incremental
batch, show its own segment count and estimate or range, and obtain a separate
approval before continuing.

## Execute each approved segment once

Use only the bundled `scripts/mcp_client.py` for remote Beatra operations. The
tool name is the CLI argument and its JSON arguments are sent on stdin. Do not
configure, call, or use a host Beatra Connector, and do not use REST/OpenAPI as
a fallback. For exact client commands and troubleshooting, use
[Bundled MCP Client diagnostics](references/mcp-connection.md).

The bundled client performs best-effort non-billable installation registration.
When a clone admission card was approved after top-up or balance confirmation,
submit `beatra.voices.clone` once under that card's identifier and freeze the
returned `voice_id` before any synthesis.
When a cover card was approved, submit `beatra.images.generate` once under
that card's identifier. For each newly approved segment, create a new opaque
`client_request_id` and
submit `beatra.speech.synthesize` once. The JSON must explicitly include the
frozen voice, exact segment text, and request identity, followed by the frozen
optional controls:

```json
{
  "voice": "<opaque voice_id>",
  "input": "<exact approved segment text>",
  "client_request_id": "<new opaque id>",
  "model": "auto",
  "language": "<BCP-47 tag>",
  "format": "mp3",
  "speed": 1.0,
  "volume": 1.0,
  "pitch": 0
}
```

Call it as `python3 scripts/mcp_client.py call beatra.speech.synthesize`, with
that JSON on stdin. Immediately record the
returned `task_id` beside the segment and request identity, then poll only that
task with `beatra.tasks.get` until it is terminal.

## Recover without duplicating paid work

If a known task exists, read it with `beatra.tasks.get`. If the `task_id` is
lost, call `beatra.tasks.list` with `capability: "text_to_speech"`, follow every
returned `next_cursor` needed to search the relevant time window, and verify a
candidate with `beatra.tasks.get`. `tasks.list` does not filter by
`client_request_id`, and the remote list/get task envelope does not return
`client_request_id`; keep it in the local ledger only. Match remote candidates
by capability, relevant time window, returned input and settings, and task
facts. Never claim to reconcile the local request identity from a remote task.

Only when transport or task creation left the original result genuinely
unknown may the same request identity be replayed, and then only with JSON that
is field-for-field identical. Any change to text, voice, model, language,
format, or another control is a new paid execution with a new ID and new
approval. Slow polling, authorization trouble, update failure, or a terminal
failure never authorizes an automatic replacement request. Follow [delivery and
recovery](references/delivery-and-recovery.md) for task pagination, terminal
errors, cancellation, and billing facts.

## Review and deliver what actually returned

For each succeeded segment, deliver every returned fact that exists: `task_id`,
audio URL, `artifact_id`, `duration_seconds`, actual `mime_type`, actual sample
rate, `task.links.assets`, resolved model, usage, and billing. Keep chapters in
listening order and identify anything still awaiting review. If the host can
play or inspect the audio, review pronunciation, pauses, pace, voice fit, and
cross-chapter consistency. If it cannot, say that the audio was not auditioned
and ask the user to review it; never invent listening observations.

Correct only the smallest affected segment. A correction is new paid work and
uses the same production-card and confirmation boundary.

When the user requests an exact duration, preserve that target as a review
goal. Use supported speed and delivery controls, generate the smallest useful
segment after confirmation, compare its returned `duration_seconds` with the
target, and report the drift. Then propose only the smallest useful adjustment
for a new confirmation. Never guarantee an exact hit before hearing the result.

When the user requests multi-cast narration, first clarify whether a single
narrator performing dialogue with one frozen voice, supported controls, and
careful pacing is acceptable. If it is, keep that requirement in the direction
and use the normal pilot route. If the user truly needs mixed multi-cast voices,
voice-by-voice production, or editing, preserve the requirement and route it to
another suitable workflow that can mix and edit multiple voices; do not weaken
the request or claim this single-voice workflow completed it. Start from final
readable text. If the project also needs source-file import, translation,
multi-cast mixing, M4B assembly, mastering, or publishing support, preserve
those requirements and route those preparation or finishing steps to a
suitable workflow.

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
