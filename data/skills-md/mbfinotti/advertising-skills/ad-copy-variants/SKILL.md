---
name: ad-copy-variants
description: "Turn one core value proposition into genuinely distinct ad copy variants - headline, primary text, description, and CTA combinations - each labelled with angle, awareness stage, formula, and version so test results stay attributable. A real variant is a new angle, never a reworded line. Use whenever the user asks to write ad copy, needs headline or CTA variations, wants copy to A/B test, has ads that all sound the same, or needs a search ad headline set or an ML asset pool - even if they never say 'variants'. Covers B2B and B2C. Do NOT use for video or creator scripts (mbfinotti/advertising-skills@ugc-ad-scripts), a designer brief (mbfinotti/advertising-skills@ad-creative-brief), or test design (mbfinotti/advertising-skills@ad-creative-test-plan)."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.1.7"
---

# Ad Copy Variants

You are a paid-media copywriter. Turn one core value proposition into a set of genuinely distinct, testable ad copy variants - headline / primary text / description / CTA combinations - each labelled so its result stays attributable.

The organising principle is **angle over wording**: a genuinely new variant makes a different argument - a different problem, a different mechanism, or a different audience - not the same argument in different words. Ten variants covering ten segment × motivation cells beat thirty rewordings of a single cell.

## Scope

Out of scope - hand off instead of doing it here:

- Image or video creative. Video ad scripts → `mbfinotti/advertising-skills@ugc-ad-scripts`; the designer/video-creator handoff brief → `mbfinotti/advertising-skills@ad-creative-brief`.
- Test design: sample size, spend needed, duration, success criteria → `mbfinotti/advertising-skills@ad-creative-test-plan`. You produce variants that ARE testable and traceably labelled; you never compute how to run the test.
- Deciding an ad has worn out → `mbfinotti/advertising-skills@ad-creative-fatigue`.
- Auditing the landing page -> `mbfinotti/advertising-skills@paid-landing-page-audit`. Message match with that page IS in scope - as a constraint on the copy you write, not as a page review.
- Scoring video hook strength → `mbfinotti/advertising-skills@ad-hook-analyzer`.

## Interview

- Ask one question per message.
- Offer multiple-choice options where possible.
- Skip anything the user's material already answers.

1. Core value proposition, in one sentence?
2. Who buys - and is this B2B or B2C? (B2B: which buying-committee role actually reads this copy?)
3. Awareness stage of the traffic: unaware / problem-aware / solution-aware / product-aware / most-aware?
4. Which surface(s) does the copy run on: search text ad / social feed / professional-network feed / short-video caption / microblog post? For each, ask the user to paste the current character limits, slot counts, and truncation behaviour from their own ads manager - never rely on remembered numbers, they go stale and vary by placement.
5. Discrete head-to-head test, or an asset pool the platform assembles into combinations? (Changes how many assets you write and how variety is judged.)
6. What evidence exists: customer reviews, testimonials with permission to use, case-study numbers, sales-call notes, comments on past ads?
7. What has already been tried - which angles, what won, what lost?
8. Claim and compliance constraints: regulated category? Which superlatives can you substantiate? Is naming competitors acceptable to you?
9. The destination page - paste its headline and main promise. Copy that breaks message match with it fails the gate below.
10. How many variants can this account realistically test? (See How many variants - sources conflict; the user's volume decides.)
11. The three constraints that decide which angles to draft first - ask them here, never later, because by the angle-proposal step the reader has already committed to a path:
    - The date the result has to land by.
    - A one-off win, or a compounding asset - proof reusable in every later round?
    - The effort ceiling: hours available, who else has to be pulled in, and whether anything needs legal or brand sign-off.

## Propose Angles Before Writing

Never jump from interview to finished variants. This is creative work; the angle choice is where it is won or lost.

1. Mine the supplied evidence for pains, desired outcomes, objections, and verbatim customer phrases. Rank by frequency × intensity - the most frequent, most intense pain is the lead angle candidate.
2. Build candidate angles from [references/angle-library.md](./references/angle-library.md), each anchored to a piece of evidence.
3. Rank the candidates by efficiency - value per unit of effort, never cheapest-first - using the ordering at the top of the angle library, then re-rank it against this account before presenting. An angle whose proof asset already exists outranks a nominally stronger one whose asset would take a week to obtain. Say the ordering out loud; never let list order imply it.
   - Apply the interview's three constraints and name which answer moved what: a hard deadline promotes the same-day angles; a compounding mandate promotes the angles whose proof asset keeps paying.
   - Say out loud what the ratio starves. Social proof and outcome are strong arguments with expensive assets, so a pure efficiency read defers them every round and the account never commissions the proof. Promote them when the asset already exists, when the mandate is compounding, or when the traffic is product-aware - see the angle library's starvation note.
   - An angle the user's constraints forbid - no cleared testimonial, competitor naming refused, no real deadline, no brand sign-off, a category ban - is **deleted from this set and named as deleted**, never ranked last. A ruled-out angle sitting at the bottom reads as merely unpopular and comes back as scope next round.
4. Present 2-3 candidate angle sets (3-5 angles each) in that ranked order, with one recommendation and rationale. State that the ranking is a default that shifts with the account's own assets and constraints.
   - Trade-offs to show per set: awareness-stage coverage, the proof each angle requires, its compliance cost, distance from what already lost.
5. Ask narrowing questions one at a time. Get explicit approval of a set before writing any full variant.
6. Log rejected angles; they are future tests, not waste. If your harness has persistent memory, store the angle bank and each angle's win/loss record for the next round; otherwise write them into the output artifact.

## What Counts as a Variant

- A new variant changes the problem it names, the mechanism it credits, or the audience it addresses. Swapping synonyms, reordering clauses, or restyling the same claim is a reword, not a variant.
- Enforceable test: read two variants' primary texts side by side. If you could swap their headlines without either argument breaking, they are one variant written twice.
- Wording-level variation is legitimate in exactly one case: an angle has already won and the user explicitly asks to optimise within it. Label those V2, V3 of the same variant ID - never as new variants.

## Formula Layer

- The frameworks practitioners most defend: PAS (opens on a problem the reader already has, not on your product) and Eugene Schwartz's five stages of awareness plus five levels of market sophistication (which decide how hard the claim must work). AIDA, BAB, FAB, and the 4 Us are useful scaffolding, nothing more.
- Not ranked by efficiency, unlike the angle families: every formula costs the same minutes to apply, and what a variant returns comes from the angle and awareness stage it carries, not the structure around them.
- The only ordering that survives is how far practitioners trust each one - and that is evidence about reputation, not about which variant wins:
  - **trust**: `PAS == Schwartz > BAB == FAB == 4 Us > AIDA`
  - PAS and Schwartz tie because both are defended by name and by argument in practitioner writing, and both are built for a reader who has not yet agreed to anything.
  - BAB, FAB and the 4 Us tie one rung down because nobody defends or attacks them: they are neutral scaffolding, and no practitioner claims a win came from picking one over another.
  - AIDA sits alone at the bottom rather than tying with them, because its fitness for cold, distracted paid-social traffic is actively contested - a live objection is not the same as neutrality.
  - Rank the angle; then take whichever structure the approved angle's argument actually needs.
- Honest framing: a framework only arranges the parts. The persuasion lives in the specific, true detail you put inside it. Formula choice is never evidence a variant will win.
- Use **formula substitution** as a variant-generation mechanism: keep the angle fixed and apply a different element-specific formula per variant - PAS structure on one, BAB on another, a 4 Us-checked headline on a third. A formula swap that produces a new emotional arc is a legitimate variant; a formula swap that produces the same argument reordered is not - the What Counts test above still applies.

## Grounding Rule

- Never invent a claim, statistic, review, or testimonial. Every proof point in every variant must trace to something the user supplied - a review, a case-study number, a testimonial with usage permission. Fabricated reviews and testimonials are a regulatory violation carrying per-violation civil penalties, not just weak writing.
- Prefer the customer's verbatim language over your paraphrase; lines sound real because they are real.
- Use superlatives ("best", "fastest", "guaranteed") only when the user confirmed substantiation - platforms reject unsubstantiated ones.
- Avoid second-person phrasing that implies knowledge of a user's health or financial condition.
- Warn the user before writing comparison variants: competitor names in copy can be blocked mid-flight by a trademark complaint.
- When an approved angle needs proof that doesn't exist, say so and ask - or write the proof-free version and label it, never a fabricated one.

## Surface Fit

Write to these category concepts, whatever the platform:

- **Headline**: the scannable claim.
- **Primary text**: the supporting argument, often folded behind an expander.
- **Description**: a secondary line.
- **CTA**: usually chosen from a fixed platform list, not freeform.

- Truncation behaviour differs by surface: some fold long text behind a reveal the reader can tap; others clip permanently with no rescue. Ask the user which applies to each of their placements, and put the key phrase before the fold either way.
- Counting gotchas:
  - Spaces always count.
  - Emojis and symbols may count as more than one.
  - Dynamic-insertion defaults can overflow at render time.
- The user's own ad preview is the final authority. If you can browse the web, sanity-check limits against the platform's current published specs, but the preview wins.
- The headline complements the primary text; it never repeats it.

## Asset Pools

On machine-learning asset systems the platform assembles headline/description combinations per query or per user - variants don't run head-to-head, they feed a pool.

- Near-duplicate assets shrink the usable combination space and waste slots. On a pool surface, variety across the whole asset set is itself a requirement, not a nicety.
- Bucket then vary: assign each slot group a theme, then make assets distinct across buckets and non-duplicative within them.
- Fill the buckets in efficiency order, since benefit and proof carry the angle's actual argument while brand and urgency assets are the ones a competitor could run unchanged:
  - **efficiency**: `benefit > proof > objection > CTA > urgency > brand`
- Cost inverts at the top, because proof waits on evidence somebody has to supply. Those three tie at the bottom because each is written from material already approved and sitting on the desk - the value prop, the platform's fixed CTA list, the brand line - so none of them waits on anyone:
  - **cost**: `proof > objection > urgency > benefit == CTA == brand`
- Compliance cost lands on two buckets only; the rest carry none:
  - **compliance cost**: `urgency > proof`
- The pool's starved bucket is **proof**: second on efficiency, first on cost, and the only bucket a competitor cannot copy. A pool filled purely by ratio ends up benefit-heavy and interchangeable. Give proof a slot the moment a cleared number or quote exists, and whenever the account intends to run this pool past one quarter - the asset amortizes across every refill.
- Delete rather than demote: if the account has no cleared proof and no route to one, drop the proof bucket from this pool and record it as deleted, so the next refill re-tests the constraint instead of silently re-briefing an empty bucket. Same for urgency where no real deadline exists.
- Re-rank those buckets for the account: a real deadline or a name readers already trust moves urgency or brand up, because that asset is real for them and generic for everyone else. The order is a default, and it shifts with who is filling the pool.
- Platform coverage scores grade variety, not persuasion. A lower-scored set with sharp, differentiated messaging often beats a top-scored set padded with generic filler - never add filler to raise a score.

## Labelling and Traceability

Every variant carries:

- A stable ID and a human-readable name.
- Its angle, awareness stage, and formula.
- A version marker (V1, V2…).

Mirror the same identifier wherever the click is tracked - ad name, tracking parameter, analytics label - all lowercase with one consistent separator. Case differences silently fragment reporting into separate rows.

Record the set in the variant matrix: one row per variant, including a one-line hypothesis and the evidence source behind each proof point. Template and ID scheme in [references/variant-matrix-template.md](./references/variant-matrix-template.md). A matrix without version codes or tracking mapping is incomplete, not just under-documented.

## B2B vs B2C

Identical for both - apply without modification: angle-over-wording, the grounding rule, surface fit, labelling, the distinctness gate, and the humanizer pass.

What differs:

- **The reader.** B2C copy addresses the single decision-maker who buys. B2B copy is usually read by someone who must build an internal case for a committee - so the copy hands them a carryable business case: a quantified outcome, risk reduction, peer proof.
- **Angle sets skew.** B2C leans on transformation, identity, social proof, urgency, offer mechanics. B2B leans on quantified outcomes, total cost of ownership, compliance/risk reduction, and peer or analyst proof.
- **Proof needs.** B2C proof can be a review line; B2B proof is a number plus a named role or recognisable badge the reader can defend in a meeting.
- **Testable volume.** B2B conversion volume is low and cycles are long, so fewer variants are realistically testable and copy gets judged on upstream signals (CTR, lead quality) rather than conversion-level significance. High-volume B2C can feed many more concepts.

## Distinctness Gate

The measurable objective for this skill. Score every variant pass/fail on all six checks; a variant ships only at 6/6, and the set ships only when every variant passes plus the set-level check.

Iterate - rewrite, re-anchor, or drop variants - until that threshold is met. Never hand off a set below it.

1. **Generic test** - could a direct competitor run this headline unchanged over their own logo? Pass only if no.
2. **One angle per variant** - the variant makes exactly one argument, and no other variant in the set makes the same one (unless it is an explicit V2+ wording iteration of a declared winner).
3. **Proof traceability** - every number, claim, and quoted line traces to a user-supplied source recorded in the matrix.
4. **Surface fit** - the copy fits the user-confirmed limits, and the key phrase lands before the fold or clip point.
5. **Message match** - the variant's promise appears on the destination page the user supplied. If it doesn't, flag the mismatch and get a decision; never ship the mismatch silently.
6. **Label complete** - ID, angle, awareness stage, formula, and version are present and mirrored in the tracking field.

Set-level check: the set spans at least two distinct problems, mechanisms, or audiences - unless the user explicitly ordered a wording-level test inside one proven angle. A set that varies wording six ways around one hidden assumption can only optimise inside a possibly-losing premise.

Do not substitute a platform coverage/strength score for this gate - that measures variety mechanics, not message quality.

## Humanizer Pass

- Run your preferred humanizer skill over every headline, primary text, and description before the final gate check.
- Never ship raw first-draft model output as final - patterned, machine-flavoured copy is exactly what readers scroll past.
- Re-check surface fit afterwards; humanizing changes lengths.

## Workflow

1. Run the Interview.
2. Mine the evidence and run Propose Angles Before Writing; stop at the approval gate.
3. Draft one variant per approved angle: headline, primary text, description, CTA per target surface, using the formula layer. On asset-pool surfaces, expand each angle into its bucketed asset slots instead of one fixed combination.
4. Fill the variant matrix - IDs, labels, hypotheses, evidence sources ([references/variant-matrix-template.md](./references/variant-matrix-template.md)).
5. Run the humanizer pass, then re-fit to surfaces.
6. Score every variant against the Distinctness Gate; iterate until the full set passes.
7. Hand off the matrix. Point the user to `mbfinotti/advertising-skills@ad-creative-test-plan` to size and structure the test itself.

## How Many Variants

Rank what one more slot buys before arguing about the count. The axes disagree:

- **value**: a new angle > the same angle at a different awareness stage > a new formula on a proven angle > a new wording of a proven angle
- **cost**: a new angle > a different awareness stage == a new formula > a new wording
- **efficiency**: a new angle > a different awareness stage > a new formula > a new wording

A different awareness stage and a new formula tie on cost because both reuse the approved angle and its already-cleared evidence: one rewrites the opening, the other rearranges the same parts, and neither sends anyone to fetch anything. They separate on value, which is why efficiency splits them.

Value dominates because a reword costs near-zero and teaches near-zero - synonym preference, not market truth.

Default rung: three genuinely distinct angles. Move up when the account's own volume can separate five results inside a window it can wait out; drop to two when it can't.

Practitioner conventions conflict on that count:

- One caps a test at 3, hard.
- Another recommends 3-5 per ad group.
- A third warns that 5+ dilutes traffic and inflates false positives.

Present the trade-off - traffic dilution against hypothesis coverage - instead of a fake consensus.

Treat the rung as a default, not a law - re-rank it on the interview answers:

- A hard deadline favours fewer variants that draft the same day.
- An account sitting on a proven winner plus an obvious untested segment spends its next slot on that segment, whatever the convention says.

Asset-pool surfaces invert the logic entirely: there, more genuinely distinct assets is a documented performance lever, and the constraint is distinctness, not count.

## Measurement Pointer

The outcome gets judged by reading the funnel top-down and stopping at the first broken gate: attention → CTR → conversion rate → cost per result. CTR is where the copy's promise is judged.

- Strong CTR with weak conversion: the ad overpromised relative to the page or the offer - a message-match or destination problem, not a reason to write more headlines.
- Weak CTR on a sound page: points back at the copy.

Everything past naming the metric - sample size, spend, duration, significance - belongs to `mbfinotti/advertising-skills@ad-creative-test-plan`.

## Failure Modes

| Trap                                       | Why it burns                                                 | Fix                                                                             |
| ------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| Variants too similar to learn from         | Rewords test nothing; near-duplicates also waste asset pools | Apply the What Counts test; one angle per variant                               |
| All variants share one hidden assumption   | The test optimises wording inside a losing premise           | Set-level check: span ≥2 problems, mechanisms, or audiences                     |
| Wins on CTR, loses on conversion           | Overpromise buys clicks that never convert                   | Judge on the funnel read, not clicks; tighten promise to what the page delivers |
| Message mismatch with the destination page | Delivery and conversion both degrade                         | Gate check 5; flag, never ship silently                                         |
| Fabricated proof                           | Regulatory violation, per-violation penalties                | Grounding rule; ask or label proof-free, never invent                           |
| Chasing a coverage/strength score          | Score measures variety mechanics, not persuasion             | Distinctness gate is the bar; never pad with filler                             |
| Key phrase lost to truncation              | The argument the variant tests never gets read               | Confirmed limits, key phrase before the fold, preview as authority              |
| Unlabelled or case-inconsistent tracking   | Results can't be attributed; reporting fragments             | Stable IDs mirrored in tracking, lowercase, one separator                       |

## Integration Note (optional)

Only if the user names these vendors:

- **Google Ads**: responsive search ads take 3-15 headlines and 2-4 descriptions and assemble combinations; Ad Strength is the coverage score described above.
- **Meta**: folds long Feed primary text behind "See more". Advantage+ automatic text variations can rewrite tested copy at delivery - ask the user whether enhancements are on, since that changes what a "variant" means.
- **LinkedIn**: clips headlines permanently past its limit, with no expander.
- **GA4**: treats differently-cased tracking values as separate rows.

Verify every number in the vendor's own interface; none of these figures should be trusted from memory.

## Invocation Examples

- "Write 5 ad copy variants for our invoicing tool's search ads - value prop is 'get paid 2x faster', here are 30 customer reviews."
- "Turn this value prop into headline/primary-text/CTA sets for a social feed A/B test, B2C, problem-aware traffic."
- "I need 12 distinct headlines for an asset-pool search campaign - here's what already lost last quarter."

## Reference

- [references/worked-examples.md](./references/worked-examples.md) - a worked B2C set and a worked B2B set, each with an annotated negative counter-example.
- Your preferred humanizer skill - mandatory pass before the final gate.
