---
name: "slide-narration-studio"
description: "Narrate a slide deck page by page. It writes a spoken script for every slide, records it in the teacher's own voice through a voice clone or with a chosen narrator, and delivers one audio file per slide or narrated slides as a video with subtitles. It covers course narration, PowerPoint narration, slide voiceover, and lecture voiceover for courses, training decks, and talks."
---

# Slide Narration Studio

Give every slide of a deck its spoken explanation: a script per slide in the
teacher's register, read in the teacher's own voice or a chosen voice.

## What you get

- One audio file per slide (`out/L01-audio/p001.mp3`, `p002.mp3`, …), named
  in slide order and labelled as AI-generated in its metadata.
- The spoken script for every slide, approved before any voice is made.
- On request, one narrated video of the deck (1920×1080) with its subtitles
  on screen, and its SRT subtitle file beside it.

## Ways to run it

- **Audio per slide (default).** For the teacher to place on each slide in
  PowerPoint or WPS.
- **Narrated video.** The slides play with their narration, the subtitles on
  screen, and the AI badge, with the SRT file beside the video.
- **The teacher's own voice.** Cloned once from a clean sample.
- **Lecture text without slides.** Each paragraph of the final lecture text
  becomes one audio file, in order.

## Scope and adjacent routes

Use it when the slides, or the final lecture text, exist and only the spoken
explanation is missing. For a whole course of lecture videos with an optional
on-camera teacher, Lecture Video Maker is the route; for one micro-lesson
built from a topic, Micro-Lesson Maker. When there is only lecture text and
the teacher wants a video, AI Courseware Maker builds the deck first. Point to
another Skill with the install message in
[Narration workflow](references/workflow.md#pointing-to-another-skill)
and install it only after the user asks.

## Inputs and defaults

Hard inputs: the deck (`.pptx`, PDF, or exported slide images), or the final
lecture text when there are no slides, and the spoken language. Ask for a
voice sample and the speaker's consent only when the teacher wants their own
voice, and for readings of recurring names, terms, and acronyms. Defaults: the
speaker notes as each slide's script when present, otherwise a script written
from the slide; a catalog voice that suits the subject; audio per slide. Never
add facts the slides and notes do not support; mark the gap for the teacher
instead.

## Golden path

Run every Beatra call through the bundled `scripts/mcp_client.py`. Do not
configure a host Beatra Connector. Do not use REST/OpenAPI as a fallback.
Slides are read and videos assembled on this computer with
[Deck files](references/deck-files.md) and
[Lesson video assembly](references/lesson-video.md).

1. **Read the deck** and create the course project (one lesson for the deck).
   From lecture text alone, each paragraph becomes one page.
2. **Write the scripts** for every slide and show them with the reading list.
   Nothing is submitted.
3. **Narrate the first slides.** Pick the voice (the teacher's own voice is
   cloned first, on its own card), read the live speech card, estimate only
   the first three to six slides (`--pages`), show the card for them, narrate
   them one at a time, record each, and deliver their audio. Render those
   slides as video (`plan --pages`) only when the user asks.
4. **Narrate the rest** after one card for the remaining slides, page by page.
   On `insufficient_balance` at any paid step, stop the whole run, relay that
   error's message and URL, and resume only after the user says they topped up.
5. **Deliver** the audio per slide in order, how to place it in PowerPoint or
   WPS, and, when asked, the narrated video (subtitles on screen) and its SRT
   rendered locally; report durations and the summed
   `billing.net_charged_credits`. Say that the audio files are AI-generated
   narration.

## Decisions that require confirmation

Every paid call follows the current production card in
[Narration workflow](references/workflow.md#production-cards): the first
slides, the rest of the deck, and voice cloning. Scripts and estimates are
free and are not approval. The voice is the teacher's own or used with the
speaker's permission; access to a file is not consent. A changed script or
a retake is new narration for that slide only, on its own card; a changed
reading applies to the whole deck and is new narration for every narrated
slide that contains the term, so run `estimate` first and quote how many
slides it re-opens; a new voice is new narration for every slide already
narrated.

## Recovery

Each slide's narration has one `client_request_id` from the course project;
it stays the same while the script, reading, voice, and take are unchanged.
Recover a lost response with `beatra.tasks.list` and `beatra.tasks.get` before
anything is submitted again. A narration task that ends `failed` or
`canceled` gets `retake` for that slide and a new card; its ID is never sent
again. A failed render is local and is re-run with no paid call.

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

- Read [Narration workflow](references/workflow.md) for production cards,
  payloads, placing audio in PowerPoint or WPS, cloning, and delivery.
- Read [Deck files](references/deck-files.md) when reading slides, exporting
  slide images, or installing the reader's optional helpers.
- Read [Lesson video assembly](references/lesson-video.md) for the course
  project, readings, subtitles, layouts, the AI badge, and rendering.
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
  only when the user asks to stop using it and remove its credentials.

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
