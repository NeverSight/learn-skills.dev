---
name: ugc-ad-scripts
description: "Turn a product brief and target audience into UGC-style short-form video ad scripts a creator can film - hook, body, CTA - with 3-5 hook variants per concept written as spoken line plus on-screen text plus opening visual, with delivery notes and disclosure lines. Use whenever the user asks for a UGC ad or creator script, a short-form vertical video ad script, a founder-led video, employee-generated content, or a customer testimonial video script - even if they never say 'UGC'. Covers B2C creator scripts and B2B formats. Do NOT use to score existing hooks (mbfinotti/advertising-skills@ad-hook-analyzer), to write static ad copy (mbfinotti/advertising-skills@ad-copy-variants), or to brief a designer (mbfinotti/advertising-skills@ad-creative-brief)."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.3"
---

# UGC Scripts

Turn a product brief and target audience into UGC-style short-form video ad scripts a creator can film: hook, body, CTA, 3-5 hook variants per concept, and the delivery notes needed to shoot.

The strategist writes the script; the creator performs it; the editor assembles it - "You're not paying the creator to be the creative strategist" (Savannah Sanchez, The Social Savannah). Roles stay separate; combining them is the most-cited cause of mediocre output.

## Scope

Out of scope - hand off instead of doing it here:

- Video production, casting, sourcing creators, editing, post-production. Hard out.
- Scoring or ranking existing hooks/transcripts → `mbfinotti/advertising-skills@ad-hook-analyzer`.
- Static ad copy A/B variants (headline/body/CTA text for feed and search ads) → `mbfinotti/advertising-skills@ad-copy-variants`.
- Full campaign creative brief (messaging pillars, visual guidelines, brand do/don'ts) → `mbfinotti/advertising-skills@ad-creative-brief`. This skill writes the script itself and only the delivery notes needed to shoot it.
- Deciding when an ad is worn out → `mbfinotti/advertising-skills@ad-creative-fatigue`.
- Designing the test matrix and sample sizes for the variants → `mbfinotti/advertising-skills@ad-creative-test-plan`.

## Interview

Ask one question per message. Offer multiple-choice options where possible. Skip anything the user's brief already answers.

1. Product - what is it, and what does it actually do?
2. Offer - free trial, discount code, demo, waitlist, direct purchase?
3. Audience - who, and what awareness stage: unaware / problem-aware / solution-aware / product-aware?
4. B2B or B2C?
5. Platform and placement - short-form vertical feed, stories, professional-network feed, video pre-roll?
6. Target duration - default 15-25 seconds, the strongest-cited band for paid social.
7. Performer - real customer, paid creator, founder, employee, or a concept test with nobody cast yet?
8. Evidence on hand - reviews, comments on past ads, support tickets, sales-call notes, observed winning ads?
9. Regulated category (health, finance, supplements)? Which markets does this run in?
10. Volume - how many concepts, how many hook variants each? Default: 2-3 concepts × 3-5 hooks × 2 CTAs.
11. Deadline - what date must the first ad be live?
12. One-off win or compounding asset - a single ad filling a slot now, or a script library and a repeatable format to build on?
13. Effort ceiling - hours available, who can be filmed, and what already exists: product footage, screen recordings, a documented customer result cleared for public use?

Every option menu below is ranked by a default that these last three answers override. Re-rank against them and say which answer moved what:

- A compounding mandate promotes the asset-gated hook archetypes and the customer testimonial, since the asset outlives the ad that used it.
- A shoot this week defers them to the next round - say "deferred", and keep them on the menu.
- A constraint that cannot be lifted at all (no footage, no cleared result, a category ban) deletes an option - a deleted option gets named as deleted rather than parked at the bottom of the ranking.

## Workflow

1. Run the interview.
2. Build the evidence base by review mining - the dominant input, taught as a named method by Copyhackers (Joanna Wiebe): pull the customer's own language back out of their own channels, then mirror it back. Work the sources in efficiency order - quotes returned per unit of digging:
   - Public reviews == past-ad comments: a real tie, not a shrug - both are already public, already in the customer's words, and both are read straight off a screen with nobody's permission to ask. Take whichever the product actually has.
   - Support tickets: need internal access, and a named customer's words need their consent before they reach a script.
   - Sales-call notes: cost someone's time to dig out, and pay it back with the objection language nothing else gives you.
   - Re-rank against what the user already holds: a tagged ticket export or a call-recording library drops to near-zero and outranks public reviews - as it does for most B2B products, where public reviews are too thin to carry a concept.
   - Record each quote as four columns:
     - Exact quote.
     - Source.
     - Underlying desire or problem.
     - Emotional tag.
   - If you can browse the web, pull recent public reviews of the product; otherwise ask the user to paste evidence.
   - Never invent a hook, pain point, claim, or testimonial line. Fabricated reviews and testimonials are a regulatory violation, not just weak writing.
   - No evidence at all? Say so, write from the brief alone, and label every script `UNVALIDATED - voice-of-customer not sourced`.
3. Define each concept: one audience segment × one motivation (in the customer's own words) × one format. Fix the offer. Concept, hook, and offer are three separately testable variables (Ralph Burns, Perpetual Traffic) - hold two constant, vary one.
4. Draft the body against the anatomy below, fitted to the target duration. Keep it fixed across hook variants.
5. Write 3-5 hook variants per concept, plus 2 CTA variants. One shoot then yields 6+ edit combinations against a single body - the standard way to isolate creative variables without re-filming.
   - Each hook is a triad: spoken line + on-screen text + opening visual, each carrying different information.
   - Pick distinct archetypes from [references/hook-archetypes.md](./references/hook-archetypes.md), which ranks them by persuasion bought per unit of production effort. Default: the dialogue-only archetypes lead (skeptic's turn, problem callout, POV), and an asset-gated one (proof-first, silent review, before/after contrast) earns a slot when that asset already exists. Near-identical openings re-test what is already known.
   - Say what the ratio starves. Before/after contrast and proof-first carry the strongest evidence on the list and cost the most to shoot, so an efficiency read defers them forever and the slate never shows the viewer anything checkable. Promote one when its asset already exists and is cleared, when the interview answer was a compounding mandate, or once a round of tier-1 hooks has landed within noise of itself.
   - An archetype the constraints rule out is **deleted from this concept's menu and named as deleted** in the script package:
     - A regulated category bars before/after.
     - Missing product footage kills silent review.
     - An uncleared result kills proof-first and bold claim.
   - Never rank a deleted archetype last; a ruled-out archetype at the bottom of a list gets briefed anyway next round.
6. Check every hook-to-body transition: the first body line must extend that hook's premise. Rewrite the transition line per hook when needed - never let the body pivot away from what the hook promised.
7. Lock the hook and the CTA word-for-word; leave the middle as bullet-point beats with example phrases. This is the practitioner reconciliation of authenticity versus control - see Scripting depth below.
8. Add delivery notes per script:
   - Beat timings.
   - What is on screen each beat.
   - Tone and read direction.
   - What to hold up to camera.
   - Do's/don'ts - these carry more signal than positive instruction alone.
9. Run the compliance pass with [references/compliance-checklist.md](./references/compliance-checklist.md). Disclosure lines are script lines - write them in, in the language of every market the ad runs in.
10. Run your preferred humanizer skill over every spoken line and on-screen text. Mandatory: UGC that reads machine-written destroys the authenticity the entire format depends on. Never ship raw first-draft output as final.
11. Assemble the script package (shape below) with its measurement plan. If your harness has persistent memory, store the evidence sources, chosen concepts, and winning hooks for the next iteration; otherwise put them in the package so the user can re-supply them.

## Scripting depth

Both extremes fail, and each has its own failure signature:

- Too vague ("just talk about why you love it") → the creator invents the strategy, and the footage misses the angle.
- Too scripted (every word locked) → the delivery goes stiff and the creator's own audience senses an ad and skips.

Lock the two beats that carry the test - hook and CTA - and brief the middle as beats with example phrasing. Hand the creator the actual customer-review quotes as talking points, so the lines sound real because they are real.

## Script anatomy

- Default spine: Hook → Problem → Solution → 2-3 value props → social proof → CTA. Target 15-25 seconds for paid social.
  - Under ~10 s: tends to under-communicate.
  - Past ~45 s: completion falls steeply.
- Common beat split: hook 0-3 s, value prop 3-15 s, proof or demo 15-25 s, CTA in the final ~5 s.
- Test hook lines against the Four U's: Unique, Urgent, Ultra-specific, Useful.
- Front-load the hook, but do not treat "3 seconds" as a behavioral law: it is a convention reverse-engineered from a platform counting a "view" at 3 seconds of watch time. Independent eye-tracking (Lumen Research, via WARC) puts 1.4 seconds of attention behind a 10% brand-awareness lift and 3.9 seconds behind prompted recall - the real window is likely shorter than the folklore.
  - Never cite the "8-second attention span": it traces to a 2015 report with no credible source and is debunked.
- Retention drops steeply after the first several seconds. Cut lines rather than consolidate into a longer video.

Structure the body with a general direct-response framework where one fits, in efficiency order at 15-25 seconds: PAS (Problem-Agitate-Solve) > BAB (Before-After-Bridge) > AIDA. All three cost the same to write, so the ordering is fit rather than effort:

- PAS: dialogue-only.
- BAB: needs a before state that is still filmable, plus a typicality line to clear.
- AIDA: four stages rarely land inside 25 seconds.

Default to PAS. Move to BAB when the before state is already on camera. Move to AIDA only in the longer B2B formats below.

These are classic copywriting scaffolds, not UGC-native inventions - none includes the social-proof beat paid social expects, so add it.

## Platform notes

Optional; skip when the user has not named a platform. These are placement facts, not vendor instructions.

- Short-form feeds count a "view" at different thresholds (2 s on some, 3 s on others), so hook rates are not comparable across platforms. Compare a script only against others on the same placement.
- Keep on-screen text at roughly 5-10 words per second of screen time.
- Assume sound off. On professional-network feeds especially, most video is watched muted - captions and on-screen text must carry the message alone.

## B2B adaptations

Transfers unchanged from B2C:

- Fast front-loaded hook.
- Native unpolished feel.
- Single CTA.
- Grounding in real customer language.
- On-screen text carrying the message with sound off.
- The Hook/Body/CTA spine itself.

Does not transfer:

- Haul and impulse-purchase framings.
- Discount-urgency CTAs.
- The single-decision-maker assumption.
- Purely aesthetic UGC.

B2B buying runs through a committee of roughly 6-10 people over a longer window, so one script rarely converts alone - plan scripts per awareness stage.

Lead with teaching, not pitching: "People come to LinkedIn to learn; not necessarily to watch commercials" (AJ Wilcox, B2Linked). Person-to-camera expertise outperforms polished corporate video on professional networks.

Use Challenge → Solution → Outcome as the B2B spine, and close the outcome with a quantified result and a named role. Testimonial-length formats run longer than B2C - roughly 45-90 seconds - and completion falls sharply past two minutes.

Three B2B stand-ins for the B2C creator testimonial, in efficiency order. Cost runs opposite to value here, so read every axis before casting:

- efficiency: founder-led > employee-generated > customer/practitioner testimonial
- cost: customer testimonial > employee-generated > founder-led
- value: customer testimonial > employee-generated > founder-led
- compliance cost: customer testimonial (their sign-off to be named, plus a generally-expected-result line) > employee-generated (employment disclosed in the script) > founder-led (self-evident, still labelled)

1. **Founder-led** - why we built this, the broken status quo, what changed. One person's hour and one calendar; the only rung that ships this week. Weakest proof of the three: the viewer discounts a vendor telling their own story.
2. **Employee-generated** - "how we actually do X here", practitioner voice, real workflow or screen on camera. Costs internal buy-in and someone comfortable being filmed. Buys practitioner credibility a founder cannot claim.
3. **Customer/practitioner testimonial** - real user, named role, quantified result, with a generally-expected-result line when results vary. Costs external scheduling and their approval, and it needs a documented outcome to exist first. Buys the only third-party proof on the list.

**What this order starves: the customer testimonial.**

- First on value and first on cost: the only rung carrying third-party proof, and the only one whose asset needs someone outside the company to say yes.
- A ratio picks founder-led every time, so the account ships vendor-tells-own-story video indefinitely and never once puts a customer on camera.
- Promote it when a named customer with a quantified result has already agreed to appear, when the interview answer was a compounding mandate (the cleared testimonial is reusable across every later script), or once founder-led video has stopped moving the number - that is the viewer discounting the source, which no rewrite fixes.

Move up to employee-generated when someone in-house does the job the product replaces and will show their real screen. Default to founder-led otherwise.

That order is a default, not a law. Re-rank it against the account and against the interview's deadline, durability and effort-ceiling answers: a founder with an existing audience beats a cold customer testimonial, and a signed case study already cleared for public use makes the customer testimonial the cheapest rung here rather than the dearest. Where no documented customer outcome exists and none can be obtained, **delete the customer testimonial from this account's menu and say so** - do not leave it ranked last, where the next round briefs a testimonial nobody can supply.

## Output shape

Deliver one script package per concept, using the two-column audio/video convention: one row per beat, visuals in one column, audio in the other, plus a timing column. Estimate narration time as spoken word count ÷ 150 words per minute.

- **Concept**: segment, motivation (verbatim evidence quote + source), format, offer.
- **Hook variants (3-5)**: table of spoken line / on-screen text / opening visual, with archetype label. Locked word-for-word.
- **Body**: beat-by-beat - timing, spoken beat, on-screen text, visual. Bulleted beats with example phrasing, not locked lines.
- **CTA variants (2)**: the ask, with spoken and on-screen wording. Locked word-for-word.
- **Delivery notes**: read direction, tone, setting, props, pacing, and do's/don'ts.
- **Compliance**: disclosure line(s), the markets they cover, and claim notes.
- **Validation status**: grounded (with sources) or `UNVALIDATED`.
- **Measurement plan**: which single variable this package tests, plus the baseline below.

See [references/script-examples.md](./references/script-examples.md) for a worked B2C package, a worked B2B package, and a negative example annotated with what is wrong.

## Invocation examples

- "Write 3 UGC ad concepts for our meal-planning app, busy parents, 20-second vertical video, 5 hooks each."
- "Turn these customer reviews into a founder-led video script for a professional network, 30 seconds."
- "A creator is booked Friday - script a testimonial-style ad for the discount offer, with delivery notes."

## Failure modes

- Vague direction ("just be authentic") → creator invents the strategy. Fix: lock hook and CTA, brief the middle as beats.
- Every word locked → stiff delivery that reads as an ad. Fix: same rule, from the other side.
- Hook the body never pays off → hold rate collapses. Fix: transition line extends the hook's premise (step 6).
- Generic hook → nothing to learn from the test. Test: if a competitor could say the same opening line word-for-word, rewrite it.
- Static or logo-card first frame → the most-cited cause of a low hook rate. Fix: open on motion, a face, or the money-shot.
- Problem beat that lists features instead of naming the moment the pain shows up. Fix: use the emotional tag from the evidence doc.
- Brand voice in a person's mouth ("revolutionary formula") → reads as an ad and dies. Fix: use only words found in the evidence.
- Stacked CTAs → every ask dilutes the others. Fix: one ask per script.
- Invented voice-of-customer → regulatory exposure. Fix: label `UNVALIDATED` instead.
- Everything varied at once → nothing learned. Fix: hold concept and offer fixed while testing hooks.
- Usage rights not signed before filming → unusable footage. Flag it in delivery notes; the paperwork is out of scope.

## Measurement

Set the objective against the account's own baseline, not a published number. Pull the trailing median hook rate and hold rate for comparable placements first; a new script passes when it beats that median and clears the diagnostic below. Iterate on one variable at a time until it does.

Published benchmarks conflict too much to use as a target: vendor "good" hook rates range from roughly 18% to 40% for the same metric on the same platform, and each vendor sells the analytics the number justifies. Treat any external figure as a sanity check, never a goal.

Diagnose in sequence and fix only the failing stage:

- Low hook rate (3-second plays ÷ impressions) → the opening fails. Rewrite hooks; do not touch targeting.
- Healthy hook rate, low hold rate (15-second plays ÷ 3-second plays) → the body or the hook-to-body transition fails.
- Healthy hold rate, low CTR → the CTA is weak or unclear.
- Healthy CTR, low conversion → the offer or the landing page, not the script.

Hook rate measures attention, not value - two ads at an identical hook rate can differ several-fold in return because one holds viewers to the CTA and the other does not. Never scale on hook rate alone.

## Reference

- `mbfinotti/advertising-skills@ad-hook-analyzer` - score and rank existing hooks or transcripts.
- `mbfinotti/advertising-skills@ad-copy-variants` - static headline/body/CTA text variants.
- `mbfinotti/advertising-skills@ad-creative-brief` - the full campaign creative brief.
- `mbfinotti/advertising-skills@ad-creative-fatigue` - when to replace a worn-out ad.
- `mbfinotti/advertising-skills@ad-creative-test-plan` - test matrix and sample sizes for the variants.
