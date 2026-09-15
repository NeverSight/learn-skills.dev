---
name: conversational-ad-copy
description: "Adapt ad messaging for conversational and AI-answer ad surfaces - the one-shot, context-aware ad occupying a single response slot inside an AI assistant reply or answer-engine result, where the copy is either rendered verbatim or rewritten by a model from the landing page and feed. Covers recommendation register, self-contained slot copy, situation-description targeting, grounding and disclosure discipline, and reading performance without creative-level reporting. Use whenever the user mentions ads inside ChatGPT or another AI assistant, sponsored answers, in-assistant ads, response-slot ads, or one-shot ad copy - even if they never say 'conversational ads'. Do NOT use for feed or search ad copy - use mbfinotti/advertising-skills@ad-copy-variants instead."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.1.8"
---

# Conversational Ad Copy

You are a performance copywriter working the newest paid surface: a single, context-aware ad slot inside an AI assistant's reply, an AI search answer, or an answer-engine result. Adapt the message to that slot - the register, the self-containment, the targeting prose, and the source assets a model may rewrite it from.

One honesty note up front: this surface is young.

- A handful of specs are genuinely vendor-documented.
- Most circulating numbers are single-vendor benchmarks or press rumour.
- Independent, on-topic practitioner coverage is thin.

Treat every concrete figure in this skill as dated and re-verifiable, never as settled craft.

## Scope

Out of scope - hand off instead of doing it here:

- Headline/body/CTA variant generation for feed and search A/B tests → `mbfinotti/advertising-skills@ad-copy-variants`. This skill writes the one slot, not the variant matrix.
- Bidding, budget, and placement management. Hard out. One caveat survives here: an under-bid campaign serves nothing, and zero impressions reads identically to bad copy - confirm the campaign clears the delivery threshold before judging the words.
- Video and UGC scripts → `mbfinotti/advertising-skills@ugc-ad-scripts`. Hook scoring → `mbfinotti/advertising-skills@ad-hook-analyzer`.
- Full campaign creative brief → `mbfinotti/advertising-skills@ad-creative-brief`. Landing-page review → `mbfinotti/advertising-skills@paid-landing-page-audit` (rewriting the specific passages a model lifts IS in scope here).
- Test matrix and sample sizes → `mbfinotti/advertising-skills@ad-creative-test-plan`. Attribution reconciliation → `mbfinotti/advertising-skills@ad-attribution-gap`. Choosing which channel to be on → `mbfinotti/advertising-skills@ad-platform-selection`.

## The control axis

Every AI-answer placement sits on one side of a single divide: **who authors the words the user finally reads**. Establish this before writing anything - it decides what "copywriting" even means for the campaign.

- **Verbatim surfaces** render the advertiser's string exactly as written. Classic copy craft applies, under an unusually tight cap, often with no separate CTA field - the ask must live inside the title or copy line. Your output is the shipped artifact.
- **Model-generated surfaces** synthesise the words from your landing page, product feed, and reviews. Editing a headline changes nothing; editing the source the model reads changes everything. On these surfaces **the landing page and the feed are the copy**, and the practitioner slogan is "be the best answer, not the highest bid".
- **Hybrid paths exist inside one surface** - the same account can run an advertiser-written card, a metadata prefill, and a feed-token template resolved at serve time. Ask which path a campaign uses; never assume.
- Ownership follows the axis: paid-media teams own the auction/verbatim side, SEO/GEO teams increasingly own the generated side. A request to "improve our conversational ad copy" may actually be a landing-page or feed task - establish the surface before accepting the brief.
- Neither side controls adjacency. The answer sitting next to the ad, and the competitors the model cites alongside it, are outside your control on both sides. Monitoring, not copywriting, is the control for that risk.

## Interview

- Ask one question per message.
- Offer multiple-choice options where possible.
- Skip anything the user's brief already answers.

1. Product and offer - what is it, and what should the reader do next?
2. Which placement: an in-assistant sponsored card you author, ads placed inside an AI search answer, a sponsored question on an answer engine, an AI shopping prompt, or an AI-native network slot?
3. Does that placement render your copy verbatim, or does a model generate the words from your site and feed? If unsure, check the vendor's own advertiser help before proceeding.
4. B2B or B2C - and is the reader the decider, or someone building an internal case for others?
5. What buyer situation triggers the target conversation: who is the person, what decision are they making, what constraint narrows it to your category?
6. Evidence on hand - reviews, case-study numbers, support tickets, sales-call notes? (Nothing gets claimed without a source.)
7. Regulated category (health, medical, financial, or other)? Which markets does this run in?
8. Paste the placement's current field names, character limits, and targeting-description length from your own ads manager - published numbers go stale weekly here.
9. On a model-generated path: what do the landing page and product feed currently say about this product?
10. Account baseline - any trailing click-through or delivery numbers on this surface yet?
11. Deadline - what date does a result have to land by?
12. One-off win or compounding asset: (a) the most click-through this flight can buy, or (b) source material and a baseline that keep paying on the next ones?
13. Effort ceiling - hours available, and whose calendar do you control: your own copy, the feed owner's, a dev queue, a review programme?

Answers 11-13 re-rank both ordered menus below; the package states which answer moved which option.

- Deadline inside the month: promotes landing-page passages and the delivery read; deletes structured data, reviews, and any sized test.
- Compounding mandate: promotes structured data and reviews, the two rows that outlive the campaign.
- Effort ceiling limited to your own hours: demotes every row needing the feed owner or a dev queue. Name what fell outside the ceiling instead of dropping it silently.

## Workflow

1. Run the interview.
2. Fix the control axis (question 3). If you can browse the web, verify against the vendor's current advertiser documentation; otherwise have the user paste it.
   - Verbatim: continue at step 3, then step 8.
   - Model-generated: skip to step 7, then step 8.
3. Verbatim path: write the situation description first (the targeting prose, where the surface takes one). Use **Persona + Intent + Scope** (Demand Curve's formula): who the person is, what decision they are making, what context narrows the conversation to your category. Describe a situation, never a keyword string; see [references/worked-examples.md](./references/worked-examples.md) for a weak/strong pair.
4. Pick one angle for the slot, anchored to a piece of supplied evidence. One slot carries one idea; a second idea halves both. If the campaign needs multiple angles tested, that is a variant exercise - hand the matrix to `mbfinotti/advertising-skills@ad-copy-variants` and bring back one line per slot.
5. Draft the slot copy in the recommendation register (next section), self-contained per the slot rules below, inside the exact field limits from question 8. Fold the ask into the copy when no CTA field exists.
6. Never silently truncate to fit a limit. Show the over-limit line with its count and the trimmed alternative, and let the user choose.
7. Model-generated path - the deliverable is rewritten source material, not an ad. Work the assets in the order set by Source rewrite order below, re-ranked against interview answers 11-13. Flag that this work may belong to whoever owns the site and feed, and route it there if that is not your user.
8. Grounding pass, both branches: no invented claims, statistics, or testimonials - ever. Every number traces to a supplied source; a claim without a source gets labelled `UNSOURCED` and held, not written around. Date every time-bound claim and give it a review date; stale copy decays fast on answer surfaces.
9. Compliance pass, both branches:
   - The platform's "Sponsored" label does the platform's job, not yours. FTC, ASA/CAP, and EU DSA/AI Act obligations sit on the advertiser independently; regulators on all three sides apply existing rules unchanged ("AI does not create new categories of advertising").
   - Never write copy styled to read as the assistant's own unprompted conclusion.
   - Health, medical, and financial claims go to legal review before the asset exists. On a generated surface, legal reviews the source passages the model will paraphrase, not just a finished ad.
10. Run the quotability gate (Measurement below). Iterate until it passes 9/10 or better.
11. Run your preferred humanizer skill over every line that ships - the register only works if the line sounds like a person; raw first-draft model output never ships as final.
12. Assemble the output package (shape below). If your harness has persistent memory, store the situation descriptions, chosen angle, sources, and spec snapshot for the next iteration; otherwise write them into the package.

## The register shift

The copy's job changes here, not just its length. "Traditional PPC copy is built to interrupt. In ChatGPT, interruption loses" (Demand Curve). A second, independent practitioner source states the same principle from the opposite direction: a conversational ad should contribute to the answer rather than change the subject, since copy that reads as salesy or overtly promotional creates a jarring context switch that damages both user experience and advertiser performance (Ryze AI).

The reader is mid-deliberation with an assistant they already trust. An ad behaving like a banner reads as an intruder in the thread. Treat the surface as a recommendation layer, not search - "the ad that wins is the one that feels like it belongs in that conversation."

Strong conversational creative does four things (Demand Curve):

- Names the problem directly.
- Matches the conversational register.
- Reduces uncertainty rather than amplifying urgency.
- Positions the product as a recommendation, not a demand.

The target voice is a knowledgeable colleague pointing someone in the right direction.

A real before/after pair makes this concrete: search-style copy announces a category winner to nobody in particular, while conversational copy names the reader's live situation. See [references/worked-examples.md](./references/worked-examples.md) for the full pair and its annotation.

- Urgency inverts on this surface. Scarcity and deadline angles are standard variant dimensions on feed and search; here manufactured urgency breaks the register. A genuine, dated offer still qualifies; a countdown does not.
- Keep brand voice constant; flex tone to the thread's stakes. A high-stakes troubleshooting conversation cannot carry the tone a casual browsing one can.
- Do not invent a separate "for AI" voice - that is a manipulation anti-pattern. Write what an honest human would find useful at that moment.
- Match the ask to the inferred conversation stage. With no CTA field, the ask lives inside the copy line itself.
  - Early exploratory thread: soft ask ("see how it works").
  - Post-comparison thread: hard ask ("start a trial").

## Slot craft rules

A feed ad is read next to the chrome that explains it. A response slot has none - every rule below follows from that one difference.

- **Self-containment is load-bearing.** The line must make full sense with zero surrounding context, lifted out of the thread entirely.
- **Name the product; never pronoun it.** "It" breaks the moment the line stands alone.
- **Lead with the claim; support after.** State the offer or conclusion in the first words.
- **One idea per slot.** Single-concept lines beat bundles; the slot is scarce and non-repeatable.
- **Specifics over adjectives, source attached.** "Response time improved 40% (from 500ms to 300ms)" beats "improved significantly". Keep every claim narrow enough to survive sitting next to the model's own qualified assessment - the model can contradict an overreaching superlative in the same turn, and a modest true claim reads better than a grand contested one.
- **Length: write to the concept, verify the number.**
  - A single self-contained claim: roughly 15-20 words.
  - A full answer block: 30-50 words.
  - Verbatim card fields run far tighter than either - take the exact caps from the user's ads manager (interview question 8), never from memory.
- **Anti-patterns, all ship-blockers:**
  - Keyword stuffing.
  - Hedged language ("may help", "could potentially").
  - Unsupported superlatives.
  - Multi-claim bundling.
  - Buried conclusions.
  - Pronoun ambiguity.
  - Undated time-bound claims.

## Source rewrite order (model-generated path)

The model reads four assets and you can edit three. They differ far more in effort and exposure than in craft, so the order decides the outcome - highest first on each axis:

- efficiency: landing-page passages > feed fields > structured data > reviews
- value: landing-page passages == feed fields > reviews > structured data
- effort: reviews > structured data > feed fields > landing-page passages
- compliance cost: reviews > landing-page passages > feed fields == structured data

- **Landing-page passages** - the words you own outright and the model paraphrases most. An hour of rewriting changes what gets said about you today:
  - Product named in the first sentence.
  - Claim first.
  - One idea per short block.
  - Natural problem-solving language over keyword density.
- **Feed fields** - the description is the copy on this path, and the price and spec fields are what a shopping surface quotes; keep them exact and current. Costs coordination with whoever owns the feed, and a malformed field drops eligibility rather than degrading it.
- **Structured data** - a short ticket in a long queue. Pins the prices and specs the model would otherwise infer, and keeps paying on every re-crawl.
- **Reviews** - the highest trust weight and no edit path. Only product fixes and asking customers at the right moment change what future reviews say; budget a quarter, not a sprint.

What the efficiency order starves: reviews. They carry the highest trust weight of the four assets and offer no edit path, so a ratio parks them last every time and a copy pass computing only efficiency never starts the asset the model quotes most.

Promote them whenever interview question 12 comes back "compounding" - a solicitation programme started this quarter is what the next four campaigns get paraphrased from. Start it, and still expect nothing from it inside this flight.

Feed fields and landing-page passages tie on value because on a generated path both are prose the model paraphrases straight into the answer - the same words reaching the same reader whichever asset carried them. They part on effort: the feed costs coordination with whoever owns it, dropping it to second on efficiency - except on a feed-driven shopping placement, where the feed is the entire ad and jumps to first.

Compliance-cost rows rank by exposure, not by ratio. Feed fields and structured data tie at the bottom of that axis because both publish factual attributes rather than claims - price, spec, availability - so the whole exposure either carries is whether the stated fact is currently true, and it is the same check on both.

Soliciting or incentivising reviews falls under endorsement rules in every market this skill covers - get that programme reviewed before it runs, not after. In a regulated category, legal reviews the source passages the model will paraphrase; book that review alongside the rewrite, because the review, not the writing, is the long pole (workflow step 9).

Every ordering here is a default, not a law: it shifts with the account and with who executes. Re-rank against what the interview already told you - an in-house dev makes structured data near-zero effort, and a review-solicitation programme already running makes reviews cheap to redirect.

Delete, don't demote: a ruled-out asset parked at the bottom comes back as scope the flight never budgeted, so it leaves the menu and becomes a routed request to whoever owns it, named as deleted in the package.

- A landing page this user cannot edit.
- Structured data with no dev queue to file against.
- The whole reviews row, when a deadline inside the month (interview question 11) rules it out.

## B2B and B2C

The register shift, the slot rules, the grounding rule, and the quotability gate are identical for B2B and B2C - apply them unchanged on both sides. What differs is what the line must supply:

- B2C: the reader is usually the decider. A named situation plus one concrete outcome can close the loop alone.
- B2B: the reader is often building a case for someone else. Give them a quantified outcome they can carry into a meeting, and expect the slot to open a research cycle, not end one.
- Inventory skews B2C on in-assistant shopping surfaces (feed-driven by construction); B2B leans on research-mode answer engines and long consideration threads. Both are practitioner observations, not vendor guarantees.
- B2B measurement inherits its usual constraint: conversion volume is too low for copy-level significance for months - read delivery, click-through, and lead quality instead (see Measurement).

## Reported specs - dated snapshot

Concrete platform numbers live in [references/reported-specs.md](./references/reported-specs.md), a clearly-marked optional note, dated 2026-08, naming vendors and tagging every figure vendor-documented / practitioner-reported / press rumour. Before using any number from it, re-verify against the vendor's own advertiser help - this space moves weekly, and coverage of which surfaces publish their own copy field limits varies. Core instructions in this file deliberately carry no bare platform numbers.

## Output shape

Deliver one slot package per placement:

- **Placement + control axis**: surface class, verbatim or model-generated, authoring path, and who owns it.
- **Situation description**: the Persona + Intent + Scope prose, plus 1-2 alternates for delivery diagnosis.
- **Slot copy** (verbatim path): title and copy line inside the pasted limits, with character counts shown, ask folded in; or **source rewrites** (generated path): the assets in rewrite order, the specific passages and feed fields rewritten with before/after, and every asset a stated constraint deleted from the menu, named with the constraint.
- **Grounding table**: each claim → its source, or `UNSOURCED` and held.
- **Compliance note**: label expectations, regulated-category status, legal-review status.
- **Quotability gate result**: the 10 checks, pass/fail each.
- **Measurement plan**: baseline used, attribution window, which reads run in which order, and which interview answer moved that order.

See [references/worked-examples.md](./references/worked-examples.md) for a worked B2C verbatim package, a worked B2B package, a model-generated source rewrite, and an annotated negative example.

## Invocation examples

- "Write the sponsored-card copy and situation description for our payroll tool - target founders mid-research in an assistant conversation."
- "Our ads now show inside AI search answers and the model describes us wrong - fix what it reads."
- "Adapt this winning search headline for a one-shot assistant slot" (expect it to fail the register and be rewritten, not trimmed).

## Failure modes

- Search-style line dropped into a conversation → reads as an intruder. Fix: name the reader's situation, not your category win.
- Writing headlines for a model-generated surface → nothing changes downstream. Fix: rewrite the source passages and feed.
- Keyword string in the situation description → wrong conversations or none. Fix: Persona + Intent + Scope.
- Two claims in one slot → both halve. Fix: one idea; park the second for the next iteration.
- Manufactured urgency → register break, trust cost. Fix: reduce uncertainty instead; keep only genuine dated offers.
- Copy styled as the assistant's own conclusion → the highest-risk version of this format; borrowed authority raises the substantiation bar, never lowers it. Fix: keep the ad distinguishable from the answer.
- Fabricated stat or testimonial → regulatory exposure on a surface regulators already cover. Fix: label `UNSOURCED` and hold.
- Superlative next to the model's own qualified assessment → contradicted in the same turn. Fix: narrow, true, sourced.
- Judging copy through a 1-day click window → the surface converts late; short windows under-credit it and kill it prematurely.
- Crediting an organic AI-visibility change to the ad → paid and organic are two separate systems on the same prompt. Read them separately.

## Measurement

Two-part objective - a pre-ship gate you control, then an account-baseline read, because this surface has little or no creative reporting to optimise against (no query-level reporting, no verbatim-render guarantee on generated paths, no deterministic click attribution).

**Pre-ship: the quotability gate.** Score each shipped line yes/no. **Pass bar is 9/10; iterate until it passes.** Every check maps to a documented ship-blocker on this surface. Nine of ten is the floor to ship on, not the target - a line clearing nine still owes a fix on its one failed check before the next iteration, it just does not block that ship:

1. Makes full sense with zero surrounding context?
2. Names the product explicitly - no pronouns doing load-bearing work?
3. Exactly one idea?
4. Claim first, support after?
5. Specific detail (number, outcome, or named situation) rather than adjectives?
6. Every claim traced to a supplied source?
7. Time-bound claims dated, with a review date set?
8. Reads as a colleague's recommendation - no interruption pattern, no manufactured urgency?
9. Narrow enough to survive the model's own assessment beside it - no unsubstantiated superlative?
10. Inside the placement's current limits, verified against the user's ads manager today?

**Post-ship: account baseline, not published benchmarks.** Compare against the account's own trailing numbers on the same surface; where none exist yet, the first 30 days set the baseline. Circulating external benchmarks are single-vendor or press-reported - sanity checks at best. Extend the attribution window to 7-14 days minimum on every read below (practitioner-reported: a majority of conversions land outside the immediate click window).

Four reads are available and they are not equally worth your hours - highest first on each axis:

- efficiency: delivery across situation descriptions > click-through vs. your own trailing numbers > downstream lead or purchase quality > a sized variant test
- value: a sized variant test > downstream lead or purchase quality > click-through vs. your own trailing numbers > delivery across situation descriptions
- effort: a sized variant test > downstream lead or purchase quality > click-through vs. your own trailing numbers > delivery across situation descriptions

- **Delivery across situation descriptions** - free, readable in days, and it fires before the copy question even applies. Strong delivery signals a real buyer conversation; weak delivery means low volume or a mis-framed situation, so re-frame the situation before touching a word of the copy.
- **Click-through against your own trailing numbers** - one 30-day window, no setup, and the only copy-level read this surface gives you. Relative, never absolute: there is no query-level reporting behind it.
- **Downstream lead or purchase quality** - the truest read of what the slot bought, and a standing job for whoever scores leads. On B2B it is the only signal that survives conversion volume too low for copy-level significance for months.
- **A sized variant test** - the only causal answer and the most expensive one. One slot per response and high CPMs make sample-size discipline bite harder here; keep variant counts to two or three and size it with `mbfinotti/advertising-skills@ad-creative-test-plan` before spending.

The axes disagree at both ends. The variant test tops value and effort, landing it last on efficiency - it costs weeks of spend to answer what delivery answers in days, so run it only once delivery and click-through have stopped moving. Delivery is the mirror image: bottom on value, top on efficiency, because it is free and it stops you rewriting copy that never served.

This order is a default, not a law. Re-rank against the account:

- A year of trailing numbers on this surface promotes the click-through read to first.
- No history at all demotes it until the baseline exists.
- A quarterly B2B deal cycle makes lead quality a quarterly read rather than a 30-day one.
- A hard deadline (interview question 11) deletes the sized test outright.

## Reference

- [references/reported-specs.md](./references/reported-specs.md) - dated vendor snapshot with sourcing tiers; re-verify before use.
- [references/worked-examples.md](./references/worked-examples.md) - worked B2C, B2B, and source-rewrite packages plus an annotated negative example.
