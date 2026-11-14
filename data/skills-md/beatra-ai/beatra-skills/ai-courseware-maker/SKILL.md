---
name: "ai-courseware-maker"
description: "AI courseware from a topic, grade, and lesson length: an editable PowerPoint lesson deck structured into warm-up, new content, practice, and summary. Key lesson slides get illustrations in one consistent style over a matching background, the teacher's script sits in the speaker notes, and the teaching slides open in PowerPoint or WPS ready to edit, with slide illustrations and the whole lesson deck in one style."
---

# AI Courseware Maker

Turn a lesson topic, grade, and lesson length into an editable PowerPoint
deck: a clear lesson structure, slide text, the teacher's script in the
speaker notes, and illustrations and a background in one consistent style.

## What you get

- One `.pptx`, 16:9, 10–20 slides by default, editable in PowerPoint or WPS.
- Illustrations for the slides that need a picture, plus one background,
  all in one style the teacher picks; the picture files stay in `images/`.
- The spoken script for every slide in its notes.
- The outline as a short list the teacher approved first.

## Ways to run it

- **New lesson (default).** Lead-in, new content, practice, summary. For an
  open lesson, the objectives and the key and difficult points come right
  after the title.
- **Lesson-design presentation.** For a demo-lesson review, a deck on the
  textbook, learners, objectives, key and difficult points, methods,
  teaching process, and board plan, with the notes addressed to the judges.
- **Class meeting or parent meeting.** A theme, talking points, and an action
  list instead of exercises.

## Scope and adjacent routes

It makes the deck. To give the slides the teacher's voice, Course Narration
Studio; to turn the deck into a micro-lesson video, Micro-Lesson Maker; for a
whole course of lecture videos, Lecture Video Maker. Offer at most one of
these after the teacher accepts the deck, with the install message in
[Courseware workflow](references/workflow.md#pointing-to-another-skill), and
install it only after the user asks.

## Inputs and defaults

Hard inputs depend on the way it runs. A lesson or a lesson-design
presentation needs the topic (or textbook chapter), the grade, and the
subject; a class or parent meeting needs the theme and the class or grade,
and has no subject to ask for. Use the textbook pages, the teacher's lesson
plan, or a curriculum note when given; never invent facts beyond them and
common textbook knowledge, and mark anything the teacher should check. A
teacher's own template `.pptx` gives content only: the built deck uses a plain
default theme. When the teacher applies the school template afterwards in
PowerPoint or WPS, the fonts and colors follow the template, while the text
stays where the build placed it, in free text boxes on a blank layout.

Defaults: the new-lesson structure; 40 minutes and 12–15 slides for a school
lesson; a clean, age-appropriate illustration style; pictures on 4–6 slides,
the lead-in, the key concept, and the summary first; slide text in the
lesson's language, Chinese for a Chinese lesson.

## Golden path

Use the bundled `scripts/mcp_client.py` for every Beatra call. Do not
configure a host Beatra Connector. Do not use REST/OpenAPI as a fallback.
The deck is written on this computer with [Deck files](references/deck-files.md).

1. **Outline.** Write the slide list for the chosen way (title, layout, text,
   notes, and which slides get a picture) and show it. This is free and is
   not approval.
2. **Style and first pictures.** Agree the style, read the live image card,
   and show the first card: the background, then the first illustrations,
   as many as the first-card rule in
   [Courseware workflow](references/workflow.md#production-cards) allows at
   the live price. After the user agrees, generate them, one call each, poll
   each with `beatra.tasks.get` until it is terminal, and save them with
   `deck_build.py fetch-images`. Prompts never ask for words in the picture;
   all slide text stays in the deck.
3. **Build and deliver the first deck** with `deck_build.py build`: every
   slide, its notes, and the pictures made so far; a slide still waiting for
   its picture is built as text. It is usable as it is.
4. **More pictures** after one card listing each remaining slide that gets a
   picture; rebuild the deck with them. On `insufficient_balance` at any paid
   step, stop the whole run, relay that error's message and URL, and resume
   only after the user says they topped up.
5. **Deliver** the `.pptx`, the list of pictures with their slides, and the
   summed `billing.net_charged_credits`; offer one next step from the
   adjacent routes.

## Decisions that require confirmation

Every image call follows the current production card in
[Courseware workflow](references/workflow.md#production-cards): the
background and first illustrations, the remaining illustrations, and any
picture redone or added later. The outline, slide text, notes, and rebuilding
the deck are free and are not approval. A changed prompt or style is new paid
work with a new card and ID; keep one style for the whole deck unless the
teacher asks.

## Recovery

Record each image task ID and its `client_request_id` with its slide. Recover
a lost response with `beatra.tasks.list` and `beatra.tasks.get` before
anything is submitted again; only when neither shows the task, submit again
with the same arguments and ID. An image task that ends `failed` is never
sent again with its ID: show a new card for a new call with a new ID. Cancel
a running picture with `beatra.tasks.cancel` only when the teacher asks.
Rebuilding the deck is local and free.

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

- Read [Courseware workflow](references/workflow.md) for the outline,
  production cards, image payloads, the deck, and delivery.
- Read [Deck files](references/deck-files.md) for building the deck, saving
  pictures, and installing python-pptx.
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

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
