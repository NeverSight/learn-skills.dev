---
name: social-hook
description: >
  Generate eight scored hook options for any social post draft or topic, spanning
  proven patterns from curiosity gaps and bold claims to contrarian takes and story
  cold-opens. Use when someone says "give me hooks", "better opening",
  "improve my hook", or "8 hooks for this". Covers hook norms for LinkedIn,
  X (Twitter), and Instagram, where the first line decides whether anyone reads
  the rest. Each option
  is scored 1-10 on scroll-stopping power and 1-10 on audience fit, with a one-line
  rationale, and the top two are recommended. Reads social-context.md for brand voice
  and audience setup so the fit scores reflect who the post is actually for.
license: MIT
metadata:
  version: 0.1.0
  category: Create
  topics:
    - hooks
    - writing
  examplePrompt: "Give me hooks for this post about our pricing change"
---

Given a draft or a topic, produce eight hook options across proven patterns, score each on scroll-stopping power and audience fit, and recommend the top two.

## Context

Before writing anything, read `social-context.md` (also check `.agents/social-context.md`). You need:

- Brand voice: formal or casual, "I" or "we", banned words, humor tolerance
- Audience: who they are, what they already believe, what they scroll past daily
- The Never list, if present — a hook that breaks a red line is disqualified no matter how well it stops the scroll
- `## Platforms`, if present, for where this post will run

If the file is missing, offer to run the `social-context` skill first — but do not block on it. Ask two or three quick questions inline (Who is the audience? Which platform? Tone in one word: playful, authoritative, or plain?) and proceed with the answers.

## Workflow

1. **Extract the payload.** Read the draft or topic and isolate the single most surprising, specific, or emotionally charged element — a number, a reversal, a confession, a result. The hook sells that element, never the topic in general. "We changed our pricing" is a topic; "we doubled our price and churn went down" is a payload.
2. **Confirm the platform.** If the user has not said, ask once. Hook budgets differ (see Quality bar), and a hook shaped for X reads clipped and abrupt on LinkedIn. If the post targets multiple platforms, score against the primary one and note any hook that would need trimming elsewhere.
3. **Decide what the hook must do for this post.** A launch announcement needs reach (favor bold claim, number); a discussion post needs replies (favor question, contrarian); a story post needs read-through (favor cold-open, curiosity gap). Name the job in one line before drafting — it becomes a tiebreaker when scores are close.
4. **Write exactly eight hooks, one per pattern, no two opening with the same word:**
   - **Curiosity gap** — open a loop only the body can close ("The pricing email we almost didn't send").
   - **Bold claim** — a defensible absolute ("Most pricing pages are designed to be ignored").
   - **Specific number/result** — lead with the metric ("We raised prices 2x. Churn dropped 14%.").
   - **Contrarian take** — argue against the audience's default belief, then earn it in the body.
   - **Story cold-open** — drop into the scene mid-action, zero preamble ("The email had been live six minutes when the first cancellation arrived").
   - **Direct question** — one the reader answers "yes" or "ouch" to, never a rhetorical shrug.
   - **"How I/we" framing** — process promise with a concrete outcome ("How we repriced without a single angry email").
   - **Listicle promise** — numbered and scoped ("3 pricing mistakes we made so you don't have to").
5. **Apply hook hygiene to every option:**
   - No throat-clearing: "I've been thinking a lot about...", "So, quick story", "Excited to share" all die on sight.
   - Front-load a concrete noun or number into the first five words — that is all a skimming eye reads.
   - Cut every adjective not doing work; "huge" and "amazing" are filler, "14%" is a hook.
   - Never promise what the body cannot cash — an overpromising hook gets the post ratioed, not read.
   - Write for the fold: the hook must work even if it is the only line anyone sees.
   - Stay inside the red lines: if a hook trips the Never list or a voice rule, rewrite it within the same pattern — never ship a disqualified hook, and never drop below eight to avoid one.
6. **Score scroll-stopping power 1–10.** Judge each hook as it would appear in a feed between two other posts: does it force a second read? Anchor the scale:
   - **9–10** — physically hard to scroll past; specific, tense, or pattern-breaking.
   - **6–8** — solid; a reader interested in the topic stops, others may not.
   - **3–5** — competent but familiar; blends into the feed.
   - **1–2** — announces a topic instead of selling a payload.
7. **Score audience fit 1–10** against the voice and audience from social-context. Anchor the scale:
   - **9–10** — indistinguishable from the brand's voice and squarely aimed at this reader.
   - **6–8** — on-topic and on-audience, but the voice is generic; anyone could have written it.
   - **3–5** — off-voice or aimed at the wrong reader; needs a rewrite to fit.
   - **1–2** — breaks a voice rule, or talks down to / over the audience.
     A 10/10 stopper that sounds nothing like the brand is a liability — score honestly and let the numbers expose the tradeoff.
8. **Write a one-line why for each.** Name the mechanism ("opens a loop", "the number does the arguing", "picks a fight with the default advice"), not a compliment. If a hook scores low, the why says what is missing, so the user learns the pattern.
9. **Recommend the top two.** Prefer hooks strong on both axes over a single-axis spike. If both winners use the same pattern, swap one for the best hook of a different pattern and say why — the user deserves two genuinely different bets.
10. **Offer one revision round.** If the user picks a hook and asks for variations, produce three tighter takes on that single pattern rather than re-running all eight — depth beats breadth once a direction is chosen.

## Quality bar

| Platform  | Hook budget                      | Notes                                                             |
| --------- | -------------------------------- | ----------------------------------------------------------------- |
| LinkedIn  | ~200 chars before "...see more"  | First line must survive the fold alone; hard line break after it. |
| X         | ≤240 chars for the hook tweet    | Leave room to breathe; no hashtags or links in the hook itself.   |
| Instagram | ~125 chars visible before "more" | First caption line is the headline; emoji only if on-voice.       |

- Every hook must be true. If the draft cannot support the claim, weaken the hook, never the truth.
- No two hooks may share an opening word — eight options that all start with "How" are one option.
- Numbers beat adjectives: a real "14%" outperforms "significantly" every time.
- Questions need stakes. "Ever thought about pricing?" is a scroll-past, not a hook.
- Second person beats third: "your churn" outpulls "companies' churn".
- All eight hooks must pass the voice rules and the Never list from social-context — a banned word disqualifies the hook regardless of its score.
- If the payload is weak (no number, no tension, no story), say so before scoring — a great hook on an empty post just raises the bounce rate.

## Deliverable

Return, in order:

1. One line naming the payload and the hook's job (from steps 1 and 3).
2. A single markdown table, one row per hook, with columns: **#, Pattern, Hook, Stop (1–10), Fit (1–10), Why**.
3. A **Recommended** section naming the top two, with one sentence each on when to choose which.

Nothing else — end there.
