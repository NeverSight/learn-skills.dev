---
name: social-voice
description: >
  Analyze 3–10 writing samples the user provides — LinkedIn posts, X (Twitter) threads,
  emails, blog posts — and distill how they actually write: sentence length, rhythm,
  vocabulary, punctuation and emoji habits, openers, sign-offs, and humor register.
  The output is a set of concrete, checkable voice rules written into the "## Voice"
  section of social-context.md, the file every skill in this collection reads for brand
  voice and setup. Use when the user says "learn my voice", "write like me", "match my
  tone", or "analyze my writing style". Includes a verification round: a rewritten
  sample the user judges as "sounds like me" before the rules are saved.
license: MIT
metadata:
  version: 0.1.0
  category: Foundation
  topics:
    - foundation
    - voice
  examplePrompt: "Learn my voice from my last 10 LinkedIn posts (pasted below)"
---

Turn real writing samples into voice rules concrete enough that any future draft can be
mechanically checked against them.

## Context

Read `social-context.md` at the project root (also check `.agents/social-context.md`) —
you will be updating its `## Voice` section, and its Positioning, Audience, and Never
sections tell you which register matters. If the file doesn't exist, offer to run the
`social-context` skill first, but don't block: ask two inline questions (who is the
audience, which platform matters most) and proceed; you'll create the file with only a
`## Voice` section at the end.

## Workflow

1. Gather samples immediately. Ask the user to paste 3–10 pieces of their real writing, or
   point you at files to read. Best sources in order: published posts on their primary
   platform, emails they wrote to humans they like, blog posts. Reject samples that were
   AI-generated or heavily edited by someone else — ask "did you write these yourself,
   start to finish?" If you get fewer than 3, proceed but flag lower confidence.
2. Separate signal from context. Note each sample's medium — a LinkedIn post and a customer
   email have different formality baselines. Analyze the _invariants_: what stays the same
   across mediums is the voice; what changes is the format.
3. Measure the mechanics — actually count, don't vibe:
   - Sentence length: median words per sentence, and the range. Any one-word sentences?
   - Paragraph shape: one-sentence paragraphs? Walls of text? Where do line breaks fall?
   - Punctuation: em-dashes, semicolons, ellipses, exclamation marks, parentheses —
     count per 100 words.
   - Emoji: which ones, how often, positioned where (inline, end of line, never)?
   - Case: any lowercase-on-purpose? ALL CAPS for emphasis? Bold?
4. Extract the vocabulary fingerprint:
   - 5–10 words or phrases they reach for repeatedly.
   - Words they conspicuously avoid (corporate verbs? jargon? profanity?).
   - Whether they say "I", "we", or neither.
5. Study openers and closers separately — these carry the most identity. How do first lines
   start (a claim? a scene? a number? never a question?)? How do pieces end (a question to
   the reader, a flat statement, a sign-off phrase, nothing)?
6. Locate the humor and heat register: do they joke, and how (dry, self-deprecating,
   absurdist, never)? Do they take positions ("X is wrong") or hedge ("it depends")?
   Note the strongest opinion in the samples verbatim as a calibration example.
7. Draft the rules. Write 8–15 rules in must/never form, each one checkable by a machine or
   a stranger.
   - Good: "never opens with a question", "one-sentence paragraphs, max 2 sentences",
     "no exclamation marks", "em-dash once per post, max", "signs off with just the
     first name".
   - Bad: "conversational", "authentic", "punchy".
     Include 2–3 short verbatim quotes from the samples as calibration anchors.
8. **Verify by imitation.** Take one of the user's samples, reduce it to a 1–2 line content
   summary, then rewrite it from that summary using only your drafted rules — without
   looking back at the original. Show the rewrite next to the original and ask: "Does the
   rewrite sound like you? What's off?" Every "what's off" answer is a missing rule — add
   it, and if the user names two or more things off, run the imitation test once more on a
   different sample.
9. Before writing, confirm the draft clears every row of the Quality bar — send yourself
   back to the step that fills any gap. Then write the rules into the `## Voice` section of
   `social-context.md`. Preserve anything already there that you didn't derive this session
   (slider values, admire/avoid accounts from the `social-context` interview) — append and
   reconcile, don't replace wholesale. If a new rule contradicts an old line, show both and
   ask which wins.

## Quality bar

| Check         | Requirement                                                                              |
| ------------- | ---------------------------------------------------------------------------------------- |
| Rule count    | 8–15 rules, each in must/never form                                                      |
| Checkability  | A stranger could pass/fail a draft against every rule without asking questions           |
| Coverage      | At least one rule each for: sentence length, openers, closers, punctuation, emoji, humor |
| Evidence      | 2–3 verbatim quotes from samples included as calibration anchors                         |
| Verification  | User confirmed the imitation rewrite "sounds like me" before saving                      |
| No horoscopes | Zero rules that fit everyone ("clear", "engaging", "authentic" are banned)               |

If samples conflict (formal emails, casual posts), write platform-scoped rules
("on X: lowercase openers; in email: standard case") rather than averaging into mush.

## Deliverable

The updated `## Voice` section of `social-context.md` — rules, calibration quotes, and a
`Last calibrated:` date line (today's date; omit the line rather than guess if you can't
determine it) — plus a chat summary of the 3 most distinctive rules and anything you'd want
more samples to confirm. Nothing else changes in the file.
