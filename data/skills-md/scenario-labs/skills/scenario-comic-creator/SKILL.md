---
name: scenario-comic-creator
description: "Use when a user wants to make their own comic, manga, BD, graphic novel or illustrated book with Scenario: a short personalized story from a photo or an idea, a branded or training comic, an album, or a book of hundreds of pages adapted from a text. Keywords: comic book, manga, webtoon, graphic novel, personalized comic, book adaptation, comic pages, speech balloons."
license: MIT
---

# Scenario Comic Creator

## Overview

A comic fails when a late decision breaks early work: a style change after the cast sheets, a
character invented on page 20, lettering proofread only at the end. Lock decisions in order: story,
direction, style, cast, script, pages, review, delivery. The size of the book changes how much is
locked and recorded, never the order. A comic can pass every check and still be stock: slop that
nothing ties to this story or this hand. Taste is a phase here, with a gate:
[art-direction.md](references/art-direction.md). Taste serves the reader: a comic that employees or
customers must understand puts clarity first ([clear-first.md](references/clear-first.md)). A short
comic is also under an hour of work, held there by gates:
[budget-and-gates.md](references/budget-and-gates.md).

Three lanes cover a three-page gift and a nine-hundred-page adaptation. Connection and the core
loop: `scenario` skill. Identity across pages: `scenario-consistency`. Reference roles:
`scenario-multi-reference`. Exact text: `scenario-text-overlay`. Iteration: `scenario-refine-loop`.
Storyboards and animatics for film, games or ads stay in `scenario-storyboards`. If a sibling skill
named here is missing from your available skills, load it with `skill_get` (Scenario MCP) or ask the
user to install it (https://github.com/scenario-labs/skills#install); unattended, proceed from tool
schemas and flag the gap.

## Pick the lane

- **Quick**: 1 to 12 pages, one hero, one tale. Gift comics, strips, explainers, a branded story.
  Phases 1 to 8, kept lean.
- **Album**: 13 to 120 pages, recurring cast, chapters, places. Adds a written bible, the cast gate,
  full three-tier review, a manifest and a cover.
- **Book**: over 120 pages, adapted from a text, several sessions. Adds a coverage plan and project
  files.

Start in the smallest lane that fits. Move up when the recurring cast passes four characters or the
work will outlive one session.

## Pick the mode

- **Showpiece**: the reader chose a comic, as with a gift, a fan book or an art book. The art can
  lead.
- **Clear-first**: the reader must understand a message, as with employees, customers, students or a
  board. Plain words and a light page come first, and the art serves them.

Ask who reads it and what they do afterwards. Training, onboarding, safety, compliance, sales,
internal and explainer comics are clear-first. Write the mode in the brief card.

## Intake: one round

Ask every question in one message, each with a default, then run without asking again: story,
reader, length, format, look, cast, language, deliverable, budget and time. A number the user gave
beats every default: a title and a dedication fit inside the pages they asked for. Unattended, take
the defaults, pick where the user would pick (style, likeness) and choose the bolder option, then
log each choice with two reasons in the brief card. Spend is the exception: proceed past the
estimate only when the user gave a ceiling it fits or said to spend; otherwise stop at the brief
card with the number. If the user has no story or no look, propose options instead of asking an open
question.

## Quick reference

| Phase        | Do                                                                | Gate                        |
| ------------ | ----------------------------------------------------------------- | --------------------------- |
| 1. Brief     | Brief card: mode, reader, takeaways, lane, pages, estimate, clock | Mode and reader written     |
| 2. Story     | Five loglines cut to one, beats, one script per page              | Script check, cover-the-art |
| 3. Direction | Look bible: two named influences, hard rules, FORBIDDEN list      | Rules are facts about pages |
| 4. Style     | Two or three directions, each staged differently, run at once     | Lettering readable at 100%  |
| 5. Cast      | One sheet per character, all at once: its face is on every page   | Faces differ, not generic   |
| 6. Pages     | Proofs at a low-cost quality, then finals, each batch at once     | Proofs read, finals drawn   |
| 7. Review    | One pass: defects in tiers, the cold read, the taste review       | Cold reader follows it      |
| 8. Fix       | Redraw only flagged pages, fresh from the originals, one round    | Residuals listed            |
| 9. Deliver   | Manifest, PDF, collection, clock log                              | PDF read in order           |

## Rules that carry the quality

- Never edit in a chain. Editing an edit melts faces and costumes. Every page and every redraw
  starts from the original sheets and the original prompt.
- Reference by role: style anchor, identity, costume state, prop, place. The prompt says what each
  image sets and what it never sets. The style anchor sets line, color, paper and lettering, never
  characters or compositions.
- Ask for the whole page, not panels, unless the comic scrolls vertically or will be animated.
- Decide the lettering mode by test, never by assumption (next section).
- State is per panel: costume, injuries, held objects, time of day. Write it into each panel.
- Fix through the prompt. A defect traces to one clause: replace that clause, never append a history
  of corrections.
- Direct before drawing. Name two influences, a material, three hard rules and a FORBIDDEN list. A
  mood or a bare genre label returns stock.
- Name one light source per scene and where its shadows fall. Even light is stock.
- Make every page readable cold. Write plain full sentences, add caption rectangles only where they
  carry what the picture and balloons cannot (usually one or two a page, almost never one per
  panel), label each character at first appearance, and keep pages mostly light
  ([clear-first.md](references/clear-first.md)). Cover the art and read the words alone: the story
  must survive. This matters most in clear-first mode and still applies to a gift.
- Run the taste review. In showpiece mode aim to ship only distinctive pages, anchor first. In
  clear-first mode a competent page ships when it reads. When the attempt cap runs out below the
  bar, show the best try and ask, or unattended ship the strongest and record the gap.
- Keep a clock. Quick lane: about 50 minutes for six to eight pages. Run independent work at once,
  give each reviewer an evidence pack, check each gate, and take the cuts when one runs late. Never
  answer a late gate with a longer run ([budget-and-gates.md](references/budget-and-gates.md)).
- Use the top-ranked model at the highest quality value its schema offers for the style round,
  sheets and final pages, even when `recommend` suggests a lower tier. Prompts run 600 to 1,000
  words once a template exists.
- Proof before the final. Draw every page once at a middle quality value, read words, beats and
  layout, fix the prompt text, then submit the same prompt and references at the top value. A final
  is a fresh generation: never edit a proof or attach it as a reference
  ([page-production.md](references/page-production.md)).
- Cap attempts by lane. Quick: one proof, the final plus one fresh alternative per page, at most
  four top-quality generations per page across the job. Album and Book: up to four fresh tries per
  page until pages pass on the first try, then the first plus one alternative. Later rounds hold
  only pages with a confirmed defect.
- Settle style before sheets, and sheets before pages. A late style change reaches everything.
- Keep the model validated on the first pages. Switching mid-book shifts the look.

## Lettering mode

Run the two pages with the most printed words, every word in the prompt, and proofread each balloon
at 100%.

- Every word exact: **integrated** lettering for the whole book, one language.
- Any word breaks, several languages ship, or text will be edited later: **overlay**. Generate art
  with empty balloons, then add exact text with `scenario-text-overlay`.

Record the mode in the brief card. Never switch silently.

## Worked example: a six-page personalized comic from one photo

1. Intake. The user answers: "Ines turns 8, she rides her grandfather's old yellow bicycle every
   Sunday, French, ink and gouache, PDF", and attaches Ines's photo.
2. `recommend` with capability `img2img` and the user's own words: one complete comic page, several
   panels, readable dialogue, several reference sheets. Read `next_step.type`. On `ask_user`, show
   the options (unattended: apply the `proceed` rule and log the options). On `no_match`, stop and
   report `unmet_requirements`, and do not generate. On `proceed`, take `specialty` unless its
   `caveats` or `when_general_better` name this task, else the first ranked entry not marked
   deprecated in its `caveats`, `tradeoff` or `explanation`. Never run an entry flagged
   `requires_plan_upgrade`. `model_schema_get` on the pick for the reference field, its cap and
   array rule, and page sizes. A pick whose schema has no image reference field cannot carry the
   photo or the sheets: take the next entry.
3. Resize the photo to about 2,000 px on its long side and upload it with `upload_asset`.
4. Price a representative page payload with `dry_run: true`, using the uploaded asset id as the
   reference: the real size, a prompt of realistic length. Write the brief card with the estimate:
   pages, sheets, style round and a redraw margin.
5. Script: five loglines cut to one that keeps every fact given (the bicycle, her grandfather,
   Sundays), six beats, six page scripts in her grandfather's voice with the exact French words,
   accents included. Cover the art and read the words alone. Write the look bible: one light source
   per scene, a four-color palette, a refuse list, a camera plan.
6. Style round on the page with the most words. Draw the hero from a written description, not the
   photo. Three directions from the style library, each with two named influences and hard rules and
   its own staging of the same beat, run at once with a plain-prompt stock twin of the same page.
   Show them side by side and run the taste review. The user picks one (unattended: pick and log two
   reasons). Record its asset IDs as the style anchor.
7. Cast: settle outfit details first (coat, scarf, helmet, the bicycle's colors). Draw Ines's sheet
   from the photo in the chosen style, then her grandfather's. The user approves the likeness
   (unattended: compare it with the photo at crop size and log the check). From here pages use the
   sheet, not the photo. With no photo, draw the sheet from the written description.
8. Proof the two densest pages together at a middle quality value and apply the lettering test. Then
   submit all the other proofs at once with `wait: false` and collect them with `jobs_wait`. A
   return of `in_progress` is not a failure: call it again with the returned `pending_job_ids`, and
   never relaunch or cancel. Read the proofs, fix the prompt text, then submit every final at once
   at the top quality value from the same prompts and references.
9. One review pass over all pages: three tiers plus the taste review, with crops of hands, faces and
   balloons and counts of repeated objects, then a cold read of the pages in order. Redraw each
   flagged page once by replacing the guilty clause, and `jobs_wait` on each redraw before comparing
   it with the old page.
10. Build the manifest, then the lossless PDF, a light PDF to send and a contact sheet with
    `scripts/build_book.py`. Read the contact sheet in order. Report where the PDF, the page files
    and the collection are.

## Read next

- [intake.md](references/intake.md): the questions, photos, formats, estimate, brief card.
- [clear-first.md](references/clear-first.md): comics for readers who must understand a message:
  lettering kit, plain dialogue, light pages, the cold read.
- [budget-and-gates.md](references/budget-and-gates.md): the clock, attempt budget, gates, cuts.
- [story-and-script.md](references/story-and-script.md): beats, page craft, dialogue, page script
  format, adapting a text.
- [art-direction.md](references/art-direction.md): the direction formula, finding the specific
  story, the look bible, camera, acting, the taste review.
- [style-library.md](references/style-library.md): paste-ready directions that name artists.
- [transformations.md](references/transformations.md): plain versus directed prompts on the same
  stories.
- [style-and-cast.md](references/style-and-cast.md): style round, sheets, cast gate, places, props,
  state ledger.
- [page-production.md](references/page-production.md): lettering test, prompt anatomy,
  defect-to-clause table, running pages.
- [review-and-fix.md](references/review-and-fix.md): tiers, mechanism checks, redraws, fix rounds.
- [assembly-and-delivery.md](references/assembly-and-delivery.md): manifest, covers, trim, PDF,
  languages, filing. The PDF builder is [scripts/build_book.py](scripts/build_book.py), run by an
  agent.
- [book-scale.md](references/book-scale.md): the Book lane: coverage plan, project files, ledger,
  sessions.
- [personalized-and-branded.md](references/personalized-and-branded.md): gift comics and company
  comics.

## Common mistakes

- Writing "same character as before": runs have no memory. Attach the sheet every time.
- Feeding the raw photo into every page: pages drift toward photographic rendering.
- Judging by score: crop and compare against the sheet.
- Naming a genre as the style ("watercolor", "manga"): it returns the average of the genre. Name
  influences and write hard rules.
- Describing a mood and leaving the rendering free: it returns the dark cinematic painting every
  moody prompt ends in.
- Adding a sheet to fix one page: the style drifts everywhere. Fix the clause.
- Skipping the cast gate: unnamed recurring figures get treated as extras and change page to page.
- Reviewing a page alone: check the previous and next page for state and place.
- Keeping printable words only in the prompt: keep them in the script file and paste them unchanged
  into every redraw.
- Calling a finished PDF proof: open it and read pages in order.
- Letting art ambition cost the reader: clipped lines, no caption rectangles, near-black pages. A
  reader who cannot follow the page never sees the art.
- Treating the first run as a place to chase one more verdict: a late gate triggers the cuts.
