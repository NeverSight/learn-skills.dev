---
name: "whiteboard-animation-maker"
description: "Turn a concept, a finished voiceover script, or a benchmark social video into a 1080×1920 black-and-white hand-drawn whiteboard explainer film. This whiteboard animation maker writes Chinese and English words stroke by stroke or animates flow cards and diagrams, narrates through text-to-speech or a cloned voice, and learns from benchmark Xiaohongshu, Douyin, TikTok, YouTube, Instagram, or X videos before drafting. Use it for whiteboard animation, hand-drawn explainer videos, doodle videos, concept explainers, what-is-X shorts, vertical explainers, spoken narration, TTS voiceover, and cloned narration for knowledge shorts."
---

# Whiteboard Animation Maker

One finished vertical whiteboard film per run: 1080×1920, white background,
black hand-drawn lines, spoken in one voice. The input is a concept, a
finished narration script, or a benchmark video to learn from. One film runs
one mode only. This package films locally; it does not publish.

`$SKILL` is this `SKILL.md`'s directory. Scripts, templates, and copy rules
all live here.

**Beatra MCP on this connection is the only interface for narration
synthesis, voice cloning, and benchmark social reads.** Do not switch to
another TTS or cloning service, do not ask the user to download a benchmark
video themselves, and do not scrape social platforms through REST, headless
browsers, or other skills. Invoke every remote Beatra tool only through the
bundled `scripts/mcp_client.py`. The host Agent must not configure or call a
host Beatra Connector and must not use REST/OpenAPI as a fallback.

## Scope and adjacent routes

This route is: one topic in, one hand-drawn explainer film out — concept
teardown, narration, storyboard, stroke-by-stroke drawing, optional
narration, local render. Prompt-to-video generation belongs to the AI video
studios; lecture recording belongs to the course studios; publishing to
platforms is not part of this package.

## Collect before starting (ask when missing)

At least one of: **what to explain**, **a finished script**, or **a
benchmark video link**.

- **What to explain.** A concept, a contrast, or a story to tell is enough
  to start.
- **Benchmark.** A Xiaohongshu / Douyin / TikTok / YouTube / Instagram / X
  link or "teardown this one": read it through
  [the benchmark lookup](references/benchmark-lookup.md) first, then tear
  down its structure.
- **Audience and platform.** Default to a vertical social knowledge short;
  never invent a persona.
- **What must not be said.** Company names, unreleased numbers. With no ban
  list, do not invent figures and do not claim unrun work as tested.
- **Output directory.** Default to a new `<slug>/` under the current working
  directory.
- **Voiceover and duration.** Reuse the user's choices; otherwise propose
  a narrated 1–3 minute film in the direction card. For
  voice, offer exactly two paths: a Beatra library voice, or a clone
  (own voice or attested authorization). Do not list other TTS vendors.

Choose text versus program in the direction card before creating the draft.

## Create

Follow [the workflow](references/workflow.md). Direction and storyboard are
visible planning artifacts. When the user delegates creative choices or asks
for a finished film, continue through free planning and drawing. Pause when
the user requested a review first, a hard input is missing, or a paid card
needs approval. Clear approval such as "looks good" counts; do not ask again
for a decision already made.

1. **Tear down the topic.** One takeaway, the common confusion, 3–5 steps,
   one drawable example, one boundary, the cut list. Too much? Propose a
   series. Benchmarks are read before teardown: borrow the dual text tracks
   and one-object-per-sentence, refuse color clip-art, real-hand photos,
   and follow prompts.
2. **Direction.** One card with the understanding, audience
   assumption, angle, duration, mode, voiceover decision, cut list, and an
   honesty grade. Use the user's constraints and delegated choices.
3. **Write narration and storyboard.** Per
   [script copywriting](references/script-copywriting.md): diagnose the
   opening first, hook with conflict, then evidence, then landing, then a
   closing action. Fill the storyboard's on-screen words and objects per
   [visual rules](references/visual-rules.md); one scene, one idea.
4. **Script and storyboard.** Full narration plus storyboard table
   with duration estimate. Honor a requested review before making the film;
   otherwise proceed within the user's instructions.

"You decide" delegates creative choices. It does not authorize an unpriced
paid call. Update the direction when the angle changes and the script when
narration changes; changing paid work requires its own current card.

## Choose a mode

- **text**: words written stroke by stroke — Chinese characters and
  short English words alike — then their objects drawn. Default for social
  whiteboard explainers. [text mode](references/mode-text.md).
- **program**: flow cards, relationship diagrams, labels that must be read
  precisely. [program mode](references/mode-program.md).

Latin proper nouns use Georgia in both modes. Captions and on-screen words
are two separate tracks; people stay off screen by default; see
[visual rules](references/visual-rules.md).

## Film

Follow [pipeline commands](references/pipeline-commands.md) for
prerequisites (Node 18+, npm, ffmpeg) and the full command sequence:

1. Create the draft and write the approved `script.txt` and `DESIGN.md`.
2. Draw `<outdir>/index.html` per the mode reference.
3. In text mode, Chinese characters and short English words come from
   stroke data. Program mode uses readable diagram labels as specified in
   its mode reference:

   ```bash
   python3 "$SKILL/scripts/text_svg.py" '目标' --id goalText --cx 540 --cy 280 --size 80
   ```
4. Voiceover follows [voiceover and sync](references/voiceover-and-sync.md):
   submit, poll `beatra.tasks.get`, collect. Unchanged narration never
   re-synthesizes.
5. `node "$SKILL/scripts/render.mjs" <outdir>`; check
   `renders/preview/sN.jpg` against the spoken nouns before delivering.

## Paid changes, recovery, and cancellation

Planning is free: the direction card and the script-plus-storyboard are
delivered before any charge. They are not approval. Three separate paid
calls exist. Each one gets its own six-field current production card and
one `client_request_id` per logical request. Never fold lookup into
synthesis.

Before narration synthesis, call `beatra.models.list` for `text_to_speech`:

```json
{"capability": "text_to_speech"}
```

Show the synthesis card and wait:

1. Work — this film's narration (`beatra.speech.synthesize`).
2. Credits — the live `text_to_speech` price just read. Do not reuse a
   remembered number.
3. Count — one paid synthesis call for the whole `script.txt`.
4. Identity — one new opaque `client_request_id`.
5. If we stop here — the direction and script-plus-storyboard
   remain usable.
6. If the balance is insufficient — relay the official message and its
   top-up URL exactly. Translate the prose; keep the URL. Do not retry
   until the user says they have topped up.

Before cloning, call `beatra.models.list` for `voice_clone`:

```json
{"capability": "voice_clone"}
```

Clone only after the user states it is their voice or the speaker
authorized it. Submit through the guarded `voice.mjs clone-submit
--consent` subcommand, which refuses to run without the consent
statement. Show the clone card and wait:

1. Work — one authorized voice sample (`beatra.voices.clone`).
2. Credits — the live `voice_clone` price just read. Do not reuse a
   remembered number.
3. Count — one paid clone call for this sample.
4. Identity — one new opaque `client_request_id`.
5. If we stop here — the plan remains usable; a library voice can
   still narrate.
6. If the balance is insufficient — relay the official message and its
   top-up URL exactly. Translate the prose; keep the URL. Do not retry
   until the user says they have topped up.

Benchmark lookup (`beatra.social.execute`) is a separate card. Show, then
wait:

1. Work — the link in the user's words, mapped to one `operation_key`.
2. Credits — the live price `beatra.social.tools.get` just returned.
3. Count — one paid lookup for this link.
4. Identity — one new opaque `client_request_id`.
5. If we stop here — the concept-route film still works with no lookup.
6. If the balance is insufficient — relay the official message and its
   top-up URL exactly. Translate the prose; keep the URL. Do not retry
   until the user says they have topped up.

A changed script, voice, or speed is a new card and a new id. An identical
resubmission reuses its id. On an uncertain submit, reconcile with
`beatra.tasks.list` and `beatra.tasks.get` before replaying byte-identical
arguments under the same id; never auto-retry.

Collection accepts only the task id already recorded for this draft. If the
submission response lost that id, reconcile first, then use
`voice.mjs recover <outdir>` to replay the saved request unchanged and record
the returned id. Never attach an arbitrary task to the draft.

If the tool returns insufficient credits: give the user the tool message in
full. Do not change the URL. You may translate the other words. Do not replace
it with your own top-up copy. Point the user to pay using that message.

## Account balance

When the user asks how many credits remain or whether a live estimate fits
the current balance, call `beatra.wallet.get`. When they ask what was
charged, call `beatra.wallet.ledger`. Live synthesis and clone prices come
from `beatra.models.list` with `{"capability": "text_to_speech"}` or
`{"capability": "voice_clone"}`; lookup prices from
`beatra.social.tools.get`. Never from ledger rows.

## References by task

Use [the workflow](references/workflow.md),
[script copywriting](references/script-copywriting.md),
[visual rules](references/visual-rules.md), [text mode](references/mode-text.md),
[program mode](references/mode-program.md),
[voiceover and sync](references/voiceover-and-sync.md),
[the benchmark lookup](references/benchmark-lookup.md), and
[pipeline commands](references/pipeline-commands.md). For the connection
itself, use [installation and authentication](references/installation-and-auth.md),
[Bundled MCP Client diagnostics](references/mcp-connection.md),
[tasks and results](references/tasks-and-results.md),
[billing, errors, and recovery](references/billing-errors-and-recovery.md),
and [uninstall and disconnect](references/uninstall-and-disconnect.md).

## Local rendering dependencies

The local film pipeline installs its pinned npm dependencies into this
package directory and runs the pinned renderer through npx on first use.
This is the local-rendering exception to the bundled-client update behavior
below; tell the user when those prerequisites need a network download. See
[pipeline commands](references/pipeline-commands.md) for the exact versions.

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
