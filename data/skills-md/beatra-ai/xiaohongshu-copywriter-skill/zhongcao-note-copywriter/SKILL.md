---
name: "zhongcao-note-copywriter"
description: "Create Xiaohongshu or REDnote copy from a product, experience, topic, or audience brief. This AI Xiaohongshu copywriter produces title options, a structured note body, cover wording, relevant hashtags, and a natural comment starter for product discovery, local experiences, beauty, food, fashion, travel, and knowledge posts. It then renders a matching vertical 3:4 Xiaohongshu cover built around the chosen title, with a headline-safe composition. Optionally it reads Xiaohongshu itself — the notes already running for the topic, one page of a note's top comments, and an account's own recent notes — so Xiaohongshu research, competitor note analysis and comment analysis rest on the platform instead of on guesswork."
---

# Zhongcao Note Copywriter

Turn a Xiaohongshu or REDnote content brief into copy that is ready to edit and
publish: title options, a structured note body, cover wording, topic tags, and
one comment starter. When the copy is settled, render one vertical cover from
the title and cover wording it just produced.

## Scope and routing

Use this package for text-first Xiaohongshu notes: product recommendations,
experience posts, local discovery, beauty, food, OOTD, travel, and knowledge
content. It writes the customer-facing copy, then finishes with one cover
built from that approved wording.

The cover route here starts from this conversation's own note: the title and
cover phrases are already chosen, no reference image is involved, and it
produces one image. A cover that starts from a real photo, composes several
ordered references, needs several concepts compared, or refines an accepted
draft belongs to `zhongcao-cover-maker`. An ordered image set belongs to
`zhongcao-carousel-maker`. Route food-specific visual notes to
`zhongcao-food-note-maker`, OOTD lookbooks to `zhongcao-ootd-lookbook-maker`,
and non-food local-business visual notes to
`zhongcao-local-business-note-maker`. Route a beauty-specialised pack — a routine
plan, an ingredient comparison, or an efficacy-led review — to
`zhongcao-beauty-note-maker`, which holds the efficacy guardrail for those
categories. A plain text-only makeup, skincare, haircare, or body-care note
stays here and is written under the same copy screen.

## Inputs and defaults

Use the topic, product or experience facts, audience, tone, platform language,
must-keep claims, and desired action already supplied. Ask only when missing
facts would change the copy: the audience, the one recommendation or takeaway,
or a factual claim that must appear. Never invent prices, efficacy,
credentials, availability, promotions, or personal experience.

Default to five title options of at most 20 Chinese characters each, one
250–500 Chinese-character note body (or a natural equivalent in the requested
language), three cover-text options, five to ten relevant hashtags, and one
conversational comment starter. Keep one clear promise, concrete details,
readable paragraphs, and a save/share-worthy takeaway. Write the body in short
sentences and short paragraphs, and keep hashtags at the end of the note.

The cover uses a 2K vertical 3:4 canvas and `count: 1`, and omits `model`,
which resolves to `auto`. Take a different canvas only when the user names one,
and freeze whatever tier and ratio it becomes in the confirmation. Default to a text-safe area rather than promising
rendered Chinese typography; when the user wants words in the image, carry the
exact short text into the confirmation and read it back only when the result
is actually visible.

## Golden path

Steps 1 to 7 cost nothing, including reading the card and pricing the cover.
The one thing that can charge earlier is the optional Xiaohongshu lookup,
which is offered, priced and approved on its own before it runs.
The note copy is a complete deliverable on its own.

Research before writing. Prefer real experience over hype. The first two lines
carry the hook.

1. Build a brief with audience, topic, supplied facts, first-person stance,
   tone, location or product details, must-keep wording, exclusions, and the
   desired reader action.
2. Extract the post angle and separate facts from assumptions. Flag any claim
   that needs the user’s confirmation instead of filling it with plausible copy.
3. Draft five distinct titles, select a primary title, then write the note with
   a clear opening, experience or evidence, practical details, and a soft close.
4. Add cover wording, hashtags, and a comment starter that matches the actual
   note. Avoid keyword stuffing, guaranteed outcomes, fabricated reviews, and
   forced engagement bait. Then run the copy screen in
   [the workflow](references/workflow.md) over the finished titles, body, cover
   phrases, and hashtags: a hit means rewrite, not a disclaimer.
5. Review for natural Xiaohongshu rhythm, factual grounding, scannability,
   audience fit, and overlap with the selected visual package. Deliver the
   primary draft plus alternatives and clearly marked assumptions.
6. With the copy delivered, prepare the cover offer at no cost: derive the
   visual direction from the primary title, the cover phrases, and the category
   — the concrete subject, scene, and treatment the note is actually about —
   then read the live `text_to_image` card with `beatra.models.list`. Skip this step
   and the two below when the user has already said they do not want an image.
7. Offer the cover and the frozen plan together, in one message, and stop. Name
   it as paid work and show the final prompt, the 2K 3:4 canvas, `count: 1`,
   how `auto` will resolve the model, the current estimate for the frozen
   tier — or the live range with its maximum as the ceiling when `auto` still
   leaves several models eligible, and the stable `client_request_id`. A user who does not take it
   up already has everything they asked for.
8. Only after the user approves that frozen plan, call `beatra.images.generate`
   exactly once. Poll with `beatra.tasks.get` until terminal and deliver the
   result.

## Revisions

A changed product fact, audience, claim, tone, or call to action is a new copy
brief. Revise only the affected section when possible and preserve accepted
wording elsewhere. Rewriting copy stays free; a cover already rendered against
a title that changed is new paid work.

Read [the workflow](references/workflow.md) for the brief card, claim handling,
the copy screen, title and body formats, revision rules, the cover payload, and
routing boundaries.

## Decisions that require confirmation

There are two paid gates and they are never folded into one approval: the optional Xiaohongshu lookup, priced and approved on its own before it runs, and the cover. Both the in-image string and the derived prompt
must clear the copy screen before either can be frozen into that plan: a
superlative or a regulated-category efficacy claim is no more acceptable rendered
as artwork — or depicted as a before-and-after panel — than written in the note.
The cover is offered together with the frozen
plan, so the user sees the price in the same message that asks for the go-ahead;
nothing is submitted on a yes given before that plan existed. A clear instruction
to proceed against the shown plan is approval. Comparing options, an unresolved
title, or an unanswered price question is not.

Every additional `beatra.images.generate` is new paid work needing its own
identifier and its own confirmation showing the current price — including an
identical re-roll after an unsatisfying result, where nothing about the request
changed. Rewriting the copy stays free.

Do not pay a second time for the cover already delivered: re-rendering that same
delivered picture in `zhongcao-cover-maker` would be a second charge for one picture. An actual
edit of the delivered cover is different work: it changes the picture rather than
repeating it, so hand it to `zhongcao-cover-maker`, which prices and confirms its own call. A
standalone cover request — one that does not follow copy written in this
conversation — also routes to `zhongcao-cover-maker`, even when the user has no photo to start
from.

## Execution

Invoke every remote Beatra tool through this package's bundled
`scripts/mcp_client.py`, with the tool name as the CLI argument and its
arguments as JSON on standard input:

```text
printf '%s' '{"capability":"text_to_image"}' | python3 scripts/mcp_client.py call beatra.models.list
```

Do not configure or call a host Beatra Connector, and do not use REST/OpenAPI
as a fallback. The bundled client registers the installation itself on its first
invocation, so there is no register subcommand. Give the cover one stable
opaque `client_request_id` containing no user content and submit it exactly
once.

## Delivery and review

Deliver the titles, note body, cover wording, hashtags, comment starter,
marked assumptions, and — when a cover was rendered — its artifact link, the
returned dimensions, the task ID, the resolved model, and
`billing.net_charged_credits`. Report only what the task actually returned.

When the cover is visible, check focal clarity in a feed-sized thumbnail,
whether the reserved text area stays clear, whether the 3:4 ratio is correct,
and whether any requested in-image text matches the approved wording character
for character. When it cannot be viewed, say which parts were not inspected
instead of describing them as verified.

## Recovery

Record the task ID immediately and poll only that task; `queued` and `running`
mean wait. If a create response is lost, resubmit the identical frozen payload
under the same `client_request_id`. If the task ID is lost, list tasks for that
capability and match candidates against your own record before any retry.
`insufficient_balance` means nothing started and nothing was charged, so the
identical request can be resubmitted after a top-up. A cover that fails or is
redone leaves the delivered copy untouched.

## Reading Xiaohongshu before you write

Optional, and paid. When the connection exposes Beatra's public social lookup, this Skill
can read Xiaohongshu directly instead of working from what the user remembers: one page of
notes matching a keyword, one specific note the user pastes, one page of that note's top comments, and an
account's profile or recent notes. Six operations, Xiaohongshu only.

**Every one of them costs 60 credits**, and there is no cheap operation on this platform to
fall back on. The same reads cost 6 on TikTok. They cost 6 on Douyin too — except Douyin's
own keyword search, which is also 60, so do not say "ten times Douyin" without naming the
read. A three-step read — the field, one note, that note's top comments — is 180 credits, and
every further page is another 60. Say the number before offering anything, confirm each lookup on
its own before it runs, and say plainly that this Skill's own deliverable arrives either
way at no cost. Offer one read, not a plan of four.

The rule is the whitelist, not a list of exceptions: a platform with no operation on it
cannot be looked up from here, and another platform's notes are never presented as
Xiaohongshu's. A returned image URL is not a viewed image — state a visual finding only
about an image the host can actually open. Every figure that reaches the work is labelled
as looked up with the time it was read, or as supplied by the user, or as missing. Nothing
is estimated, and nothing is carried in from what notes in this category usually do.

See [reading Xiaohongshu](references/note-lookup.md) for the operations, the argument
routes, the confirmation wording, and how a result is reported and recovered.

## References by task

Use [the workflow](references/workflow.md) for normal writing, the copy screen,
and the cover step, [tasks and results](references/tasks-and-results.md) for
polling and result fields, and
[billing, errors, and recovery](references/billing-errors-and-recovery.md) for
balance and structured errors. Read
[installation and authentication](references/installation-and-auth.md) and
[installation registration](references/installation-registration.md) on first
use, [Bundled MCP Client diagnostics](references/mcp-connection.md) when the
client cannot connect, and
[uninstall and disconnect](references/uninstall-and-disconnect.md) when
removing the package.

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
