---
name: developer-case-study
description: Turns a customer's real production deployment into a technical case study engineers believe  -  measured numbers tied to how they were measured, before-and-after architecture, published limitations, and cleared naming and quote approval. Use whenever the user mentions a customer case study, a technical case study, a developer adoption or success story, a reference customer, or wants to turn a user interview, migration or production rollout into published proof  -  even if they only say "a post about how Acme uses us". Do NOT use for a post about your own system  -  use samber/developer-relations-skills@engineering-blog-post; for your own project's ongoing progress use samber/developer-relations-skills@build-in-public.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Case Study

You are writing someone else's engineering story. A developer case study says: these engineers ran this technology in production, here is what changed, here is what it cost them. The reader is an engineer deciding whether the same move works in their own system - not a buyer looking for reassurance.

That reader discounts an all-upside narrative on sight. Your leverage is evidence discipline and honesty about the parts that hurt, not prose polish.

## Scope check

Confirm the artefact before starting. Route elsewhere when:

- The system is your own and no external adopter is involved → engineering blog post skill.
- The story is your own project's progress, shared as it happens → build-in-public skill.
- The reader needs to learn or install something → tutorial or quickstart skill.
- The material is "what shipped in v2.4" or "how to move from v1 to v2" → changelog or migration-guide skill.
- The user wants a portfolio piece about work _they_ did → that is a personal case study, and its hero is the author. Say so; this skill inverts that framing.

See the References section for the exact identifiers.

## Interview

Ask the case-study owner these before touching the story, one question at a time, multiple-choice where you can. Stop as soon as you can judge whether the story is publishable.

1. Who is the adopter, and is this in production today or still an evaluation?
2. Who will you interview, and what is their hands-on role? Can you also get their manager or the platform owner?
3. What evidence already exists on your side - support threads, migration issues or PRs, usage telemetry, account notes, their own blog posts or talks?
4. What changed, in numbers, and who inside their team can vouch for those numbers?
5. Who grants permission to name the company, the person, and to use the logo - and how long does each take?
6. Is there a security or legal review on their side, and has anyone engaged it yet?
7. Where does this publish, and does it need a sales one-pager version too?
8. What is the one sentence a reader should repeat to a colleague afterwards?
9. By what date must this be live, and what happens on that date? A date inside the month deletes any enterprise candidate whose legal review alone runs longer, and promotes the adopter who can approve in a message.
10. One-off win - a study for one stalled deal - or a story bank you keep filling? A one-off promotes whichever candidate is closest to approval; a bank promotes the empty row in the coverage table, even when that row is the slowest story to land.
11. What is the effort ceiling, counting the customer's time and goodwill as well as yours? One interview and one review round rules out multi-stakeholder enterprise stories; an account team willing to spend a quarter of relationship capital opens them.

If your harness has persistent memory, store the answers to 5, 6 and 7. Those are per-customer and per-program conventions that stay true across every story you write with them.

## Workflow

1. **Qualify the story** against the gates below, and where several adopters are candidates, rank them with "Which story to chase first" before spending an hour on any of them. Kill or downgrade here - a story that fails the gates cannot be rescued in editing.
2. **Reconstruct it from your own evidence first.** Read the tickets, issues, PRs and telemetry before the call, so you arrive with specifics to confirm rather than open prompts to fill.
3. **Open the approval track in parallel.** Read the contract's publicity clause, then ask who grants quotes, metrics and security clearance before drafting - their answer decides which version of the story is writable.
4. **Run the source interview.** Follow [./references/source-interview-guide.md](./references/source-interview-guide.md). Record with consent, keep the transcript.
5. **Build the evidence ledger.** One row per claim the study will make: the claim, its evidence class, the instrument behind it, who can re-derive it. Do this before drafting.
6. **Confirm the spine and the headline number** with the owner. Cheap to change now, expensive after 1,200 words.
7. **Draft against the spine** in [./references/case-study-outline.md](./references/case-study-outline.md), quotes verbatim from the transcript.
8. **Write the limitations section** from the interview's cost and unsolved-work answers. Never skip it - see below.
9. **Run the humanizer pass**, then the publication gate. Iterate until every check passes.
10. **Send for approval** with a marked decision list and a dated deadline, per [./references/approval-and-anonymization.md](./references/approval-and-anonymization.md). Apply their edits, then package the derivative versions.

## Invocation examples

- "We just finished migrating Northwind's billing pipeline onto our workflow engine. Write the case study." → run the whole workflow from step 1.
- "Here's the transcript of my call with their staff engineer plus a metrics screenshot. Draft it." → skip to step 5; build the evidence ledger from the transcript, flag every claim the transcript cannot support.
- "Legal came back and killed the company name. What now?" → jump to the anonymization ladder, propose the next rung down, and name what it costs.
- "Is this story even worth writing?" → run the qualification gates only, and answer with a verdict plus the missing gate.
- "We have four customers who said yes, which do we do?" → the ranking in "Which story to chase first", applied to the four by name, with the ones their constraints delete removed rather than ordered last.
- "Turn the approved Northwind study into a one-pager for sales." → derivative versions only; confirm the existing approval covers the new surface first.

Unless the user asks for something else, deliver six parts in this order:

1. **Verdict line** - publishable, publishable as X, or not yet, with the reason.
2. **Evidence ledger** - one row per claim: claim, class, instrument, window, who can re-derive it.
3. **The draft** - the eight-section spine, quotes verbatim, limitations included.
4. **Approval package** - the decisions to confirm, marked, with a suggested deadline and default.
5. **Gate report** - the seven checks, each pass/fail, with the fix applied.
6. **Derivatives** - the one-pager or other requested versions, only after approval.

Produce the verdict and the ledger before any drafting. A ledger built after the prose is a ledger written to justify it.

## Story qualification gates

Five gates - this skill's own checklist, not a published standard. A publishable story clears all five:

- **Production, not pilot.** Real traffic, real consequences. An evaluation is a testimonial at best.
- **A measured before-state.** No baseline means no honest delta, only vibes.
- **A named human who will talk.** Nobody to quote means nobody to believe.
- **A decision a reader can reuse.** Alternatives were considered and one won for a stated reason.
- **A plausible path to approval.** Someone can actually authorise the company name or a workable anonymised version.

Failing one gate does not always mean no story:

- Missing production: wait.
- Missing baseline: publish a scale/architecture story without a delta claim.
- Missing approval: descend the anonymization ladder.
- Missing a human: it is an engineering pattern post, not a case study. Say that out loud rather than dressing it up.

## Which story to chase first

When several adopters could carry a study, the choice is not which one is most impressive - it is which one returns the most published proof per hour spent, counting the customer's own time and goodwill as the scarcest input. Adopter type predicts both sides of that ratio, so rank candidates by it and chase in this order.

- efficiency (published proof per hour of chasing - the default order): startup or scale-up > individual developer or OSS maintainer > consumer-product engineering team > enterprise
- effort (heaviest first, customer time and goodwill included): enterprise > consumer-product engineering team > startup or scale-up > individual developer
- value (strongest proof to an undecided reader): enterprise > consumer-product engineering team > startup or scale-up > individual developer
- compliance cost (heaviest review first): enterprise > consumer-product engineering team > startup or scale-up > individual developer

The value line assumes the reader is evaluating for a team inside a company. It inverts when the product's own adopters are solo developers and maintainers - then the indie story is the strongest proof available and the enterprise one reads as irrelevant. Re-rank against who actually buys before using the default.

In efficiency order, with what each type costs and buys, and the craft difference each forces:

1. **Startup or scale-up B2B adopter** - approval is one or two people and a week. The best ratio on the list, and the risk is the mirror of the enterprise one: nobody checks the numbers. Verify them yourself before publishing, and re-verify before reusing - small companies pivot and migrate away.
2. **Individual developer, indie hacker or OSS maintainer** - near-zero approval cost; consent is a message and the person _is_ the brand. Metrics are personal-scale (build minutes, a hosting bill, a weekend of work) and perfectly credible at that scale - never inflate them into enterprise language. Ask explicitly whether they want their employer mentioned.
3. **Consumer-product engineering team (B2C product, developer story)** - a communications function exists but the story does not touch their own users, so review is narrower than an enterprise's. The adopter's users never read this; the audience is peer engineers. Push harder on architecture and scale mechanics and drop the buyer-facing business framing entirely.
4. **Enterprise B2B adopter** - a quarter, with weeks of review, a communications team that owns the narrative, heavy redaction of absolute numbers, and a second round after security. Engage legal before drafting. Their engineers will read it, so accuracy failures come back through the account team.

What this order starves is the named enterprise production reference: the strongest proof available to a reader who has to justify the choice internally, and the most expensive story on the list in both legal review and customer goodwill. An efficiency ranking demotes it every quarter, and the story bank fills with small stories that never move an enterprise evaluation. Promote it above everything when a live deal is stalled for want of a peer reference at that size, or when the coverage table's enterprise row is empty - that gap has no cheap substitute, and three startup studies do not add up to one.

Delete rather than demote. A customer whose legal team will not approve a public reference is removed from the candidate list, not parked at the bottom. Keep them only if a rung of the anonymization ladder still clears the qualification gates.

Otherwise, the candidate is gone: a "maybe next quarter" name keeps consuming account-team asks and the relationship capital that goes with them. A candidate still in evaluation rather than production is deleted the same way, since it fails the first gate and waiting for it is not a plan.

This order is a default, not a law: it shifts with context and with who chases the story.

- An account team that already has a warm relationship with one enterprise has paid most of that story's cost already.
- A maintainer who has publicly written about the product is halfway to a published study before anyone calls.

## Number discipline

Every number carries four attributes or it does not ship:

- Value before.
- Value after.
- The instrument that produced it.
- The measurement window.

| Evidence class     | What you have                                    | How to write it                                   |
| ------------------ | ------------------------------------------------ | ------------------------------------------------- |
| Measured           | Both sides from the same instrument              | State it directly, with the instrument and window |
| Partially measured | After-value instrumented, before-value estimated | State it, and mark the estimate as an estimate    |
| Reported           | The customer's number, uninstrumented            | Attribute it: "the team estimates…"               |
| Directional        | Only a qualitative claim survived                | Drop the number; use the engineer's own words     |

Two well-sourced numbers beat six loose ones. Ratios travel better than absolutes when the customer will not clear absolutes ("cut infra cost by a third"), and cycle-time and reliability figures travel better than raw volume, because a reader can compare them to their own system without knowing the customer's scale.

Don't:

- Compute a number the customer did not confirm.
- Annualize a one-month result.
- Attribute a business outcome to your product when the customer changed three things at once. Say what else changed.

Hold this skill's own numbers to the same rule. [./references/evidence-and-sources.md](./references/evidence-and-sources.md) splits every threshold in this file into sourced or self-set. Quote a self-set baseline only as a working baseline - never to an adopter as an industry standard.

## The spine

Published studies converge on **Challenge / Solution / Results**: four independent instances carry the same three beats - two vendor studies and two generic marketing-skill templates (sources in [./references/evidence-and-sources.md](./references/evidence-and-sources.md)). Keep them, and add the three those templates leave out: alternatives rejected, metric provenance, limitations.

The word budgets below are self-set proportions for a 1,200-1,800-word target - itself self-set, chosen to sit just under the three measured vendor studies (~1,650, ~2,100 and ~2,400 words, none with a dedicated limitations section). Scale them to the material.

1. Headline outcome - the number and the shape of the change (~60 words)
2. The adopter and the system in question (~120)
3. The before-state and what it cost them (~250)
4. Why this technology - alternatives weighed and rejected (~200)
5. What they built - architecture, named components, sequencing (~400)
6. Results - the numbers, with method (~200)
7. What it cost and what is still unsolved (~200)
8. What is next (~70)

Sections 4, 5 and 7 are what separate this from a testimonial. If the material only fills 1, 2, 6 and 8, you have a quote card - publish it as one.

Read [./references/case-study-outline.md](./references/case-study-outline.md) for the per-section guidance and worked positive/negative examples before drafting. The examples there (Acme, the Grafana figures) are invented illustrations, not measured cases - never cite them as evidence.

## Limitations are the differentiation

A limitation is a cost the reader would inherit, not a plan.

```
Roadmap: "We plan to consolidate the two languages."
Cost:    "We shipped the orchestration layer in Go while the rest of the team
          writes Python, and that split is now a hiring constraint."
```

One of the compared studies carries three of the former and none of the latter - do not accept that trade.

The gap is a publisher's choice, not a genre constraint. Across the four compared studies - a small sample, and both vendor ones from the same vendor:

- The vendor-published pair discloses no cost at all.
- The community-published pair discloses costs and a failure openly, one of them a named practitioner walking through his own botched launch.

Section lists and sources: [./references/evidence-and-sources.md](./references/evidence-and-sources.md).

Fill the section from the interview:

- Migration effort in engineer-weeks.
- The dual-running period.
- What broke during rollout.
- What the team retrained on.
- Which workloads they deliberately did not move.
- What still does not work.

State who should _not_ copy this architecture.

- Customer strikes the whole section: the study is weaker but still shippable.
- Customer strikes it _and_ the alternatives section: you are publishing an advertisement. Tell the owner plainly so it gets framed as one.

## Approval track

Read the contract's publicity clause before asking anyone for anything. Standard self-serve SaaS terms often already license the customer's name and logo and the statement that they are a customer - Vercel's terms carry such a clause, quoted verbatim in [./references/approval-and-anonymization.md](./references/approval-and-anonymization.md).

The clause grants nothing else:

- No quote.
- No metric.
- No architecture description.
- No narrative about how the customer runs their systems.

Ask for exactly what it leaves open.

Four permissions remain, often held by four different people:

- The engineer's consent to be quoted.
- Their manager's consent to spend team credibility.
- Communications sign-off on company name and logo.
- Security or legal review of the technical detail.

Ask who holds each at first contact.

Pre-redact what security review predictably strikes:

- Absolute infrastructure sizes and costs.
- Internal service names, ticket IDs, dashboard URLs.
- Competitor names in the rejected-alternatives section.
- Anything implying a security weakness in the before-state.

Send the full draft with the decisions marked, a dated deadline, and a stated default.

When naming is refused, descend the anonymization ladder one rung at a time rather than dropping the story:

1. Named company and engineer.
2. Named company, unnamed engineer.
3. Unnamed company with an identifying descriptor.
4. Category descriptor only.
5. Pattern write-up with no customer.

Each rung costs credibility, and the last one is no longer a case study.

This ladder is deliberately not ranked by effort or efficiency: the rungs are not alternatives anyone picks between, since every one below the top is cheaper only because someone refused the one above it. Take the highest rung approval allows, and read the descent as loss, not as a trade-off.

Full ladder, redaction classes and a request template: [./references/approval-and-anonymization.md](./references/approval-and-anonymization.md).

## Humanizer pass

Run the prose through your preferred humanizer skill before the gate. Model-flavoured filler reads as vendor copy, which is the register this artefact most needs to avoid.

Preserve exactly as written: every quote, every number, version strings, component names and the architecture description. A humanised quote is a fabricated quote.

## Publication gate

Seven checks - a working gate, not a published standard. Hold the study until all seven pass. Report which check failed and what you changed, then re-check.

1. **Every claim classified** - measured, partially measured, reported, or the engineer's marked opinion. No exceptions.
2. **Every number has an instrument and a window** stated or one click away.
3. **At least one limitation** published, specific enough that a reader could decide against you on it.
4. **Alternatives section present**, naming what was rejected and why.
5. **Every quote verbatim** from the transcript, attributed with a confirmed name and title.
6. **Approval evidence on file** for company name, logo, quotes, and security review.
7. **Zero unsupported superlatives.** Any "seamless", "effortless", "game-changing" is either backed by a number in the study or gone.

Then two human reads happen before publishing:

- The interviewed engineer confirms technical accuracy.
- Someone outside the account checks it is comprehensible without insider vocabulary.

## Derivative versions

One approved study feeds several artefacts. Ask which are needed _before_ approval, so permission covers them, and build them in reuse-per-hour order - every rung below reuses material the approved study already cleared, so the ranking is about where the reuse lands, not about writing effort:

1. Documentation cross-link - near-zero: a "who uses this and how" pointer from the relevant page, sitting where an evaluator already reads.
2. One-page summary for sales - an hour: outcome, three numbers, one quote, and no CTA on every section. Highest value of the four wherever a sales motion exists at all, and worthless where none does - which is exactly when to skip it rather than rank it.
3. Community post - an hour plus the engineer's willingness: their own words under their own name, which travels further than anything published under yours, and which only they can authorise.
4. Conference or webinar material - a day, and dependent on a slot existing. The architecture before/after is already a slide, so the marginal cost is low, but nothing here pays until the talk is accepted.

File the study's atoms - each metric, each quote, the architecture diagram - into a proof library alongside the narrative, with a public/private flag. Assets built later pull from the atoms; nobody re-reads a 1,500-word study to find one number.

Republication in a paid or ad context usually needs its own permission. Re-verify any study older than roughly 18 months before reusing it - a self-set convention, not a measured shelf life; shorten it for adopters who ship fast or churn.

## Failure modes

| Symptom                               | Cause                                               | Fix                                                                                  |
| ------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Reads like a testimonial              | Only sections 1, 2, 6, 8 have material              | Go back for alternatives, architecture, cost - or publish a quote card               |
| Customer strikes half the numbers     | Metrics never had provenance                        | Rebuild each metric with instrument and window, resubmit                             |
| Approval stalls for weeks             | Review chain engaged after drafting                 | Open the approval track at first contact; set a dated default                        |
| Engineers dispute it publicly         | Architecture written from vendor assumption         | Have the interviewed engineer confirm the technical sections                         |
| Quotes sound like marketing           | Paraphrased instead of transcribed                  | Restore verbatim from the recording; accept the customer's own edits                 |
| Story dies after the interview        | Qualification gates skipped                         | Run the gates before booking the call                                                |
| Numbers overclaim                     | Product credited for a multi-change rollout         | Name everything else that changed in the same window                                 |
| Customer disputes an "approved" study | The contract's logo clause read as blanket approval | Treat the clause as name and logo only; get quotes, metrics and narrative separately |
| Limitations section says nothing      | Roadmap items accepted as costs                     | Ask again for engineer-weeks, dual-running, what broke - a plan is not a cost        |
| Churned customer's study still live   | No re-verification date set at publication          | Date every study, re-verify on schedule, unpublish rather than leave it up           |

## Measurement

Judge a study on whether it moved evaluations forward, not on traffic. No published metric isolates case studies aimed specifically at developers: general B2B-technology-buyer research puts vendor-produced case studies well behind product demos and free trials for buying-decision impact (see [./references/evidence-and-sources.md](./references/evidence-and-sources.md)), but nothing narrower than that exists. Treat the signals below as things to weigh, never targets to hit:

- Use in live deals: how often sales or solutions engineers actually send it, and at which stage.
- Read-through rate and clicks to the artefacts it links (docs, repository, architecture page).
- Inbound reference requests - prospects asking to talk to that customer.
- Whether the adopter amplifies it themselves; a story the customer's own engineers share is one they stand behind.
- Coverage of the story bank: one credible study per major use case and adopter size beats five for the same profile.

Do not attribute revenue to a single case study. Overclaiming attribution is the same credibility failure the artefact exists to avoid.

## References

- samber/developer-relations-skills@tech-talk-outline - turning an approved study into a stage talk
- samber/developer-relations-skills@technical-video-script - video retellings of an approved study
- samber/developer-relations-skills@tech-podcast-interview-prep - podcast retellings of an approved study
- samber/developer-relations-skills@devrel-content-calendar - scheduling a story bank across a quarter
- samber/developer-relations-skills@tech-press-relations - pitching an approved case study to a journalist as a press story
- [./references/source-interview-guide.md](./references/source-interview-guide.md) - pre-call preparation, question ladder, quote capture
- [./references/case-study-outline.md](./references/case-study-outline.md) - section-by-section outline and worked examples
- [./references/approval-and-anonymization.md](./references/approval-and-anonymization.md) - consent chain, redaction classes, anonymization ladder, request template
- [./references/evidence-and-sources.md](./references/evidence-and-sources.md) - the published studies behind the spine, sourced versus self-set thresholds
