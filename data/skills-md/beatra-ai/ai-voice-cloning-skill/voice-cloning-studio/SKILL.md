---
name: "voice-cloning-studio"
description: "Create a reusable personal or brand voice from a clean audio sample with this AI voice cloning studio and voice cloning software. Clone my voice, build a custom AI voice, or create an AI voice clone from a short single-speaker sample; give the custom voice a memorable name and reuse it for narration, courses, product stories, customer updates, series, and brand content. Compare sample quality, review the current estimate, and hear the reusable voice in a short test reading before expanding it into longer spoken projects."
---

# AI Voice Cloning Studio

Create one named, reusable personal or brand voice from a clean, authorized
speech sample. The core outcome is the returned voice itself. A short test
reading is optional, separate paid work and never part of clone approval.

Use this Skill for authorized voice cloning, custom voices and later reuse in
narration. Route script-only text-to-speech to a voiceover Skill, and route
singing or voice-changing work to a matching workflow. Keep the useful cloning
route focused: this Skill does not add cleanup, editing, deletion,
transcription or impersonation steps.

Use the bundled `scripts/mcp_client.py` for every Beatra operation. Do not
configure, call, or use a host Beatra Connector. Do not use REST/OpenAPI as a
fallback. Pass the tool name as the command argument and its JSON request on
standard input, for example:

```bash
python3 scripts/mcp_client.py call beatra.voices.clone
```

## Confirm consent before preparing the sample

Reuse the sample, intended display name, language hint, intended reuse and any
plain consent statement already supplied. For a new clone, the user must state
that this is their own voice or that the speaker authorized this cloning use.
“Clone my voice” together with the user's current sample is sufficient; do not
turn that clear statement into repeated legal questions.

Access to a file, a public recording, a publication, a suggestive filename or
the speaker's public-figure status is not consent. For a third-party voice,
ask only for the missing explicit authorization. Until it is present, stop
before upload and before any paid call. Read [Consent and sample readiness](references/consent-and-sample-readiness.md)
for the exact sample and source checks.

## Prepare the source and current clone card

Read the live voice-clone model card with `beatra.models.list` when current
sample conditions, model selection or price are needed:

```bash
python3 scripts/mcp_client.py call beatra.models.list
```

```json
{"capability": "voice_clone"}
```

Treat that card as truth. The supported source forms are a prior `artifact_id`, a `data_uri`, or
an HTTPS `url`. A suitable sample is currently about 10 to 300 seconds, no
larger than 20 MiB, and clean natural speech from one speaker. If the host
cannot inspect or play it, say sample readiness is unverified rather than
claiming a listening check.

Only after consent, upload a local file with:

```bash
python3 scripts/mcp_client.py upload <path> --mime-type <exact MIME>
```

Record the exact filename, MIME type and byte count plus the returned
`artifact_id`. Do not teach or attempt a raw upload request. Keep the sample as
one of these discriminated JSON shapes:

```json
{"type": "artifact", "artifact_id": "artifact_..."}
{"type": "data_uri", "data": "data:audio/...;base64,..."}
{"type": "url", "url": "https://..."}
```

Require a recognizable `display_name`. `language` is an optional BCP-47 hint;
omit it rather than guessing, and never claim language coverage because the
clone card does not publish `supported_languages`. The safe current default is
`model: "auto"`. When the live auto contract says selection is not request
dependent and names a default for an omitted request, use that single resolved
model and current price. Only show a range if a future live contract makes the
selection genuinely uncertain.

For clone pricing, use the live card's `meter`, `unit`,
`successful_activated_voice` basis, quantity `1`, exact formula, unit price and
scale. Build one clone card that freezes:

- the sample source and readiness result, without exposing unnecessary
  sensitive sample detail;
- the consent attestation, display name, `model`, and optional `language`;
- the current sample constraints and exact live price for one successful
  activated voice;
- exactly one billable clone submission and its success-basis billing rule.

Planning, catalog reads, sample advice, naming, or “clone it now” do not
approve a charge. Before any `client_request_id` or `beatra.voices.clone`
call, show the clone admission card in the user's language: route
`voice_clone`, tool `beatra.voices.clone`, live `beatra.models.list` price
for one successful activated voice, the provisional estimate, the fact that
the 600-credit signup gift usually cannot start this clone, and what happens
if the balance is short. Numeric estimates come only from current model
cards; the terminal task's `billing.net_charged_credits` is final. Do not
create `client_request_id` or submit until the user confirms they have
topped up or already have enough credits for this estimate. Do not offer a
free clone or a free sample that replaces the clone.

## Submit the clone once and follow its task

After that top-up or balance confirmation, make a new opaque local
`client_request_id`. With the clone card unchanged, call `beatra.voices.clone`
once with:

```json
{
  "sample": {"type": "artifact", "artifact_id": "artifact_..."},
  "display_name": "Approved display name",
  "consent_attested": true,
  "model": "auto",
  "language": "optional-BCP-47",
  "client_request_id": "new-local-opaque-id"
}
```

Omit the optional `language` when unknown. On first use, allow the bundled
client's best-effort non-billable `beatra.installations.register`; a
registration failure must not block the requested operation.

Poll the returned `task_id` with `beatra.tasks.get`. A queued or running task
is not a reason to submit again. Use `beatra.tasks.cancel` only when the user
asks to cancel; if cancellation is not confirmed, continue following the same
task. Read [Clone execution and recovery](references/clone-and-proof-workflow.md)
before any uncertain-response recovery.

On success, report the actual task status and returned output type,
`voice_id`, display name, resolved model, usage, billing and links when present.
Lead with the named voice being ready. Preserve and hand off the exact opaque
`voice_id`; a display name is neither a substitute nor proof of uniqueness.
Do not promise resemblance, activation, persistence or retention beyond the
returned result.

Later, `beatra.voices.list` with `category: "cloned"` can locate saved clones.
Match the exact returned `voice_id`, and use its `compatible_models` when
planning later speech. Do not re-clone merely because conversation context was
lost.

## Offer a test reading only when requested

The user may stop after a successful clone. If they ask to hear it, prepare a
short final text and delivery direction first. The clone confirmation does not
approve this second paid operation. Read live `beatra.voices.list` and
`beatra.models.list` with `{"capability":"text_to_speech"}` and inspect every
live candidate compatible with the returned voice. Read language support from
each text-to-speech model card's `constraints.supported_languages`. Keep
`model: "auto"` only when every such
candidate supports the target BCP-47 language there. Otherwise freeze one
live, voice-compatible, language-supported explicit model in the separate
card. If no candidate meets both requirements, stop before submission and
offer a feasible saved voice, supported language, or no-proof route. The card
also freezes the exact voice,
text, controls, one synthesis call and current weighted-character price. Get
explicit approval, make a new `client_request_id`, call
`beatra.speech.synthesize` once, and recover it through the same task rules.

A test reading proves only what is present in the returned clip; it does not
establish universal similarity or language coverage. Any changed text or
delivery is a newly priced proof requiring a new approval and request ID, not
a reason to clone again. Read [Test-reading review and voice reuse](references/review-recovery-and-voice-reuse.md)
for pricing, delivery and focused revision.

## Recover and deliver factual results

For a known task, continue with `beatra.tasks.get`. If a clone task ID was
lost, paginate `beatra.tasks.list` with the voice-clone capability and every
returned `next_cursor`, then verify candidates with `beatra.tasks.get` using
the time window, capability and returned facts. `client_request_id` is a local
ledger value; task list and task output do not expose a remote request-ID
filter or field.

Only when transport or task creation remains genuinely uncertain may the
identical clone JSON be replayed with the same local request ID. A changed
sample, name, model or language is new paid work: create a new card, a new
admission card, top-up or balance confirmation, and ID. Never automatically
retry a terminal failed or canceled task. On `insufficient_balance`, relay the
returned public message, keep the top-up URL inside the balance error exact,
translate the rest, and retry the same frozen `client_request_id` only after
the user says they have topped up.

For clone and proof delivery, preserve actual task, output, model, usage,
billing, asset and error fields. Missing billing values are unknown, not zero.
Use provider-neutral `TaskError` facts and report charged, refunded and net
values only when returned. If the host cannot play returned audio, say it was
not auditioned rather than fabricating a review.

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

- Before upload or consent attestation, read [Consent and sample readiness](references/consent-and-sample-readiness.md).
- For clone request JSON, live pricing, polling and lost-response recovery,
  read [Clone execution and recovery](references/clone-and-proof-workflow.md).
- For saved-voice reuse, optional test-reading pricing, delivery and review,
  read [Test-reading review and voice reuse](references/review-recovery-and-voice-reuse.md).
- For account setup, read [Installation and authentication](references/installation-and-auth.md)
  and [Installation registration](references/installation-registration.md).
- For request transport problems, read [Bundled MCP Client diagnostics](references/mcp-connection.md).
- For task envelopes and billing facts, read [Tasks and results](references/tasks-and-results.md)
  and [Billing, errors, and recovery](references/billing-errors-and-recovery.md).
- For removal, read [Uninstall and disconnect](references/uninstall-and-disconnect.md).

## Automatic updates and safety

Silent automatic update checks are enabled by default and occur at most once
every 24 hours. When a newer version is found, it installs without separate
confirmation. Discovery comes only from the fixed official discovery source
and immutable CDN objects. The updater verifies discovery, manifest, archive,
and every file before replacing only package-owned files. It rejects unsafe
redirects, downgrades, and different channel or locale content.

Update trouble fails open: the original command continues and the current
installation remains usable. The user's choice persists across commands. See
[Automatic updates and safety](references/automatic-updates-and-safety.md), or
use these explicit controls:

```bash
python3 scripts/mcp_client.py update --auto off
python3 scripts/mcp_client.py update --auto on
python3 scripts/mcp_client.py update --check
```
