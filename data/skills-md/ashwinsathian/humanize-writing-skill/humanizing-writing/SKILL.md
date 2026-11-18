---
name: humanizing-writing
description: Use when drafting prose of a paragraph or more for a human reader (docs, READMEs, reports, emails, blog posts, cover letters, release notes, PR descriptions, commit bodies, long explanations in chat), or when asked to humanize text or make it sound less AI-generated, robotic, or like slop. Not for proofreading a person's own writing or for evading AI detectors.
---

# Humanize Writing

## Overview

Text reads as machine-written when every choice in it would suit any
reader and any subject. The fix is to write for this reader about this
subject, and the rules below apply that to the choices where the default
shows most.

The reader is a person. This skill does not change AI-detector scores; if
asked to get text past a detector, say so.

## Write this way

- Make claims specific and checkable. Replace "plays a significant role"
  or "experts say" with the fact and who said it. In technical writing
  the specific detail is the number, the command, the file, the error
  text. If you don't know, say so in plain words.
- Never invent to sound specific. No made-up incidents, figures, quotes,
  or sources, including a plausible "last quarter we..." in a piece for
  a team. With no real example, give the mechanism only if you know it,
  mark a made-up case as hypothetical ("suppose a deploy breaks
  checkout"), or cut the claim. Given a set of facts or a text to
  rewrite, add no claim that was not in it.
- Say each thing once. Don't follow a sentence with the same point in
  other words, and don't add a section that repeats a list above it.
- Use the plain verb and the common word: "is" and "has", not "serves
  as" or "boasts"; "use", not "utilize"; "we analyzed", not "we conducted
  an analysis". A precise term stays ("idempotent", "mutex").
- Replace a figure of speech with the fact it stands for: "removing this
  check lets empty orders through", not "this check is load-bearing".
  Established terms that began as metaphors (bottleneck, memory leak) are
  literal. An analogy that explains how something works is doing a job;
  keep it.
- Let sentence length follow the content. Split a sentence that chains
  clause after clause with "and", and break a paragraph where the subject
  changes. Write a short sentence when it has something new to say, not
  for emphasis.
- Stop when the content stops. Delete a final line that only repeats the
  paragraph as a saying. Don't announce a point before making it ("Here's
  the thing", "The result?", "The cost is real."). Deny X only when this
  reader is likely to believe X (a common misconception, the ticket's own
  diagnosis). Otherwise skip "it's not X, it's Y" and state Y.
- Put asides in commas or parentheses. Use an em dash only for a break
  that a comma would hide.
- Hedge each uncertain claim once, at the claim. Don't stack hedges ("may
  potentially") or hedge what you know. Cut fillers and candor markers
  ("it's worth noting", "honestly").
- Let structure follow the content. Use a list for items a reader will
  scan or follow in order, a header for a section a reader will jump to,
  and three items when there are three things. Otherwise write
  paragraphs, and don't open every bullet with a bold phrase.
- Match the voice already there: a codebase's commit conventions, a
  document's tone, a user's writing sample.

## Scope

Never fabricating is the one rule that does not yield. The others are
defaults for expository prose and follow the context:

- An explicit user request overrides them. Asked for buzzwords, a
  mandated template, or a required stock phrase? Comply, and don't change
  it back afterward.
- When editing someone else's text, fix what was asked and leave their
  voice, hedges, fragments, and rhythm alone.
- When drafting in a person's own voice from their writing sample or a
  voice profile, their habits outrank the rules above. If they use
  dashes, rhetorical questions, stock idioms, or "not X but Y", the
  draft does too, at about their rate, and the checklist below does not
  undo it. Take rhythm and connectives from the sample, not content or
  opinions. Example profile, to be read only when writing for that
  author: `voices/ashwin-sathian.md`.
- API and reference docs, schemas, and repeated list entries are meant to
  be uniform. Keep the parallel structure.
- A summary (an abstract, a TL;DR, the conclusion of a long report)
  exists to restate.
- In fiction, speeches, poetry, and brand voice, metaphor, fragments, and
  a closing line written for effect belong to the form, and a story's
  invented detail is not fabrication.
- In legal, compliance, and other fixed-register text, enumerations,
  terms of art, and standard hedges ("to the maximum extent permitted by
  law") are functional.
- In persuasive or marketing copy, the emotional close or call to action
  is what the piece is for. Cut the generic lines and keep it.
- In non-English text, the English word examples don't map across. The
  rules on claims, structure, and endings still apply.
- In text shorter than a paragraph, only the rules on claims and plain
  words have anything to act on.

## Other tells

Patterns that no rule above names. A single one proves little. Several
together are the signal.

| Tell | Why it reads as artificial |
|---|---|
| Trailing "-ing" clause ("..., underscoring its importance") | Attaches significance to a fact without evidence. Measured at 2–5x the human rate (Reinhart et al. 2025) |
| Significance inflation ("pivotal", "testament to", "plays a crucial role") | Grand and vague is safer than specific |
| Noun-built phrases ("the implementation of", "utilization") | Reads as bureaucratic. Measured at 1.5–2x the human rate (same study) |
| "Not only X but also Y" | Inflates one point into two |
| Rule-of-three padding | Suggests thoroughness the content lacks |
| "Moreover", "Furthermore", "In conclusion" plus recap | Connectors and endings that fit any text |

Sources: `reference/research/2026-update.md`. Habits reported for
specific Claude versions, with evidence grades:
`reference/claude-tics.md`.

## Before finalizing

Reread the draft:
1. Is every claim supported by the request or by what you know? Cut or
   flag any that is not. Can a vague claim be made specific without
   inventing anything? Do that.
2. Does a sentence or section repeat another, or a paragraph end on a
   line that only repeats it? Delete the repeat. A conclusion drawn from
   the paragraph, an instruction, or a request is not a repeat.
3. Does a sentence keep going on "and"? Split it. Does a fragment exist
   only for effect? Join it to its neighbor or delete it.
4. Did a fix swap one pattern for another (a triad for a negated
   contrast, a long sentence for a string of fragments)? Fix that too.

Explain changes if asked. Worked passages: `examples/`.
