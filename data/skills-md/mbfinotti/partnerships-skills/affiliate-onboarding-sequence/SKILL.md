---
name: affiliate-onboarding-sequence
description: Design the onboarding sequence that carries a newly approved affiliate from approval to first tracked conversion - touch plan (timing, channel, one action per touch), asset kit, time-boxed activation nudge, and never-activated follow-up branch. Covers B2B SaaS partner programs and B2C ecommerce affiliate programs. Use whenever the user mentions affiliate onboarding, an affiliate welcome email series, affiliate activation, a new-affiliate ramp, partner activation emails, or approved affiliates who never send a click or a sale, even if they never say onboarding. Starts at approval - to pitch affiliates who have not joined yet use mbfinotti/partnerships-skills@affiliate-recruitment-outreach.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.0.4"
---

# Affiliate Onboarding Sequence

Design the sequence that moves a newly approved affiliate to their first tracked conversion. Most programs activate only a small minority of approved affiliates - practitioner estimates cluster around 5-20%, a convergent range rather than a controlled measurement - so the sequence's whole job is to compress time-to-first-conversion while intent is still warm.

Two commitments run through everything below:

- **Day offsets are a starting skeleton, not a standard.** Documented practitioner consensus is 4-6 touches over 10-14 days, but every sourced practitioner favors behavior triggers - first click, first sale, no-click-by-day-N - layered on top of, and overriding, the calendar.
- **An affiliate who cannot get a working link cannot activate.** Provisioning and tracking readiness is the pre-condition of the sequence, never a touch inside it.

Two entry paths, both starting with the Interview:

- Build from scratch - "write the welcome emails for affiliates we just approved", "design our affiliate onboarding sequence", "what should new partners get in their first 30 days?" - run the full Workflow.
- Diagnose a running sequence - "our approved affiliates never send a click", "nobody activates after the welcome email" - run the Interview, then jump to Diagnosing an existing sequence before touching the plan.

## Interview

Ask one question per message; offer the multiple-choice options where given. Skip any question the user already answered.

1. B2B SaaS or B2C ecommerce? Both means the plan needs two branches.
2. What event counts as "activated": first click, first lead/trial, first paid sale, or first closed deal? Inside what window (days from approval)?
3. Program mechanics: commission model (recurring %, one-time %, flat CPA), cookie window, payout threshold, payout hold period?
4. Which archetypes does the intake actually contain: content/review site, coupon-deal, loyalty-cashback, social creator, email-list owner, sub-network - and in B2B: agency, consultant, tech partner?
5. Which assets exist today vs must be created: tracking links, banners, swipe copy, product one-sheets - and for B2B: sandbox/demo access, comparison and buyer-question material?
6. Tracking setup: are links or coupon codes auto-provisioned at approval? Is server-side (postback) conversion tracking live?
7. Tax and payout collection: which steps (tax form, payout method, terms attestation) - and do they gate payout eligibility?
8. Who sends the touches: an automated program address, or a named affiliate manager? Does capacity for calls and 1:1 exist?
9. How many new approvals arrive per month?
10. By what date must the first activation numbers land? A date inside the next cohort's window deletes every option that needs a build and promotes the near-zero fixes; no date leaves the default ordering intact.
11. A one-off win on this cohort, or a compounding asset? Compounding promotes the automated drip and the persistent asset hub; one-off promotes manual outreach to the affiliates already approved.
12. Effort ceiling: manager hours per week, whether a named AM exists at all, and whether changing a commission needs finance or legal sign-off. Zero AM hours deletes the high-touch and hybrid tiers outright rather than demoting them.

Questions 10-12 set the ordering of every menu in this skill; the answers are what the rankings below get re-sorted against.

## Workflow

1. Run the Interview.
2. Fix the activation definition and its measurement window before designing anything. Touch count, nudge deadline, and every KPI depend on it; a plan without it cannot be judged.
3. Verify day-0 readiness: link/code provisioning at approval, tracking that records the activation event, and payout/tax collection wired as a payout gate - checklist in [references/asset-kit-and-provisioning.md](references/asset-kit-and-provisioning.md). Stop and fix gaps before mapping a single touch.
4. Segment the intake twice: by archetype (question 4) and by touch tier. Archetype is a lookup, not a ranking: route the archetypes the intake actually contains. Tier is a ranking, and it decides where the manager's hours go:

   - efficiency (activation bought per manager hour): `self-serve > hybrid > high-touch`
   - value (activation rate per affiliate): `high-touch > hybrid > self-serve`
   - recurring effort (manager hours per affiliate): `high-touch > hybrid > self-serve`
   - one-off build before the first send: `self-serve == hybrid > high-touch`

   Self-serve leads because its marginal cost per affiliate is near-zero once built, not because it converts best - it converts worst. Build it as the floor for everyone, then buy activation upward for the segment that repays it. The build tie is real: hybrid _is_ the self-serve drip plus one calendar slot, so it costs the same week to stand up; high-touch needs almost no build and instead becomes a standing job.

   High-touch is what this order starves. It tops the value line and tops the recurring-effort line at once, so the ratio buries it every round and a program that only computes efficiency ends up serving its largest partners the same automated drip as its long tail. Promote it explicitly - never wait for it to win - when a single partner's expected revenue exceeds the hours the calls consume, or when the roster is small enough that the drip's build never pays back.

   Default: self-serve for the whole intake, hybrid layered on the archetypes whose expected volume repays a check-in.

   Delete high-touch from the menu, do not demote it, when no named AM exists or approvals run past roughly a hundred a month. A tier nobody can staff is absent, not slow, and one parked at the bottom quietly reappears as scope the plan cannot execute.

   This ordering is a default, not a law, and it shifts with who executes it. Re-rank it against what the Interview already told you:

   - An affiliate platform with milestone automation already live collapses the self-serve build to near-zero and widens its lead.
   - A manager with no capacity (question 12) deletes hybrid and high-touch both.
   - A roster of a dozen partners each worth a large deal inverts the order outright, because near-zero volume makes the per-affiliate hour cheap and the self-serve build never pays back.

   Tier detail in [references/touch-plan-patterns.md](references/touch-plan-patterns.md).

5. Map the touch plan per segment: day-offset skeleton plus behavior-trigger layer, patterns in [references/touch-plan-patterns.md](references/touch-plan-patterns.md). Every touch asks exactly one action.
6. Place terms/disclosure attestation in the approval touch, and tax/payout collection before the first payout is possible - never after the first commission is earned. Decide placement only; drafting the clauses belongs to the terms skill.
7. Attach a time-boxed activation nudge inside the first window, when intent peaks. Decide its slot, deadline, and framing here; its rate economics belong to the commission skill.
8. Design the never-activated branch: diagnostic checkpoint at the window's end, re-engagement touches, one final-notice email, then archive. Never use termination threats as the lever - motivation research documents threats as counterproductive.
9. Draft copy for every touch - one action, one CTA, link or code in the first lines of touch 1 - and set the exit, suppression, and re-entry rules, using [references/copy-and-sequence-logic.md](references/copy-and-sequence-logic.md).
10. Run every drafted email through your preferred humanizer skill; reject raw first-draft model output as final copy. The pass rewrites tone only - the one-action structure and money mechanics stay verbatim.
11. Validate the plan with the user section by section - activation definition, routing, touch plan, nudge, never-activated branch, copy - revising on pushback before moving to the next section.
12. Emit the Sequence Plan artifact below and set the KPI review cadence. If your harness has persistent memory, memorize the activation definition and routing decisions so a later diagnosis run starts from them.

## The Sequence Plan

Deliver every engagement as this artifact - it is the deliverable contract, not an example:

```
SEQUENCE PLAN - <program>, <date>
Activation       : event + window (e.g. first paid sale within 30 days of approval)
Routing          : archetype -> tier (high-touch | self-serve | hybrid), volume note
Touches          : one block per touch
  T<n> Trigger : day offset OR behavior event (behavior overrides calendar)
       Channel : email | call | in-portal | chat
       Sender  : automated program address | named AM
       Action  : the ONE action asked
       Content : one-line summary
       Asset   : asset attached or linked
Activation nudge : incentive + deadline + which touch carries it
Never-activated  : entry condition, touches, final-notice rule, archive rule
Exits            : on activation | on branch entry | suppression + re-entry rules
KPIs             : activation rate @ window | time-to-first-conversion |
                   never-activated share at cutoff | per-touch engagement
```

Every touch line carries a reason the reader can review - "T3 fires on no-click-by-day-7 because the calendar alone can't tell stuck from gone" is reviewable; a bare day number is not. Two fully worked plans (one B2C, one B2B) live in [references/sequence-plan-examples.md](references/sequence-plan-examples.md).

## B2B SaaS vs B2C ecommerce

Where the two diverge, the plan must branch:

| Dimension          | B2C ecommerce                                   | B2B SaaS                                                            |
| ------------------ | ----------------------------------------------- | ------------------------------------------------------------------- |
| First conversion   | Tracked sale                                    | Lead, trial, demo, or closed deal - fix which                       |
| Time horizon       | Days to weeks; 30-day window fits               | 30-180 days; 90-day window fits                                     |
| Touch model        | Automated self-serve for nearly all             | Hybrid/high-touch; kickoff call for strategic partners              |
| Asset kit          | Links, codes, banners, swipe copy, product feed | Adds sandbox/demo, comparison pages, buyer-question material        |
| Day-0 provisioning | Link + coupon code                              | Adds deal registration and sandbox/NFR access                       |
| Payout risk        | Clawback ends with the return window            | Clawback rides every recurring invoice; longer holds                |
| Sequence span      | 10-14 day skeleton, then triggers               | Same skeleton, but trigger layer stretches across the 90-day window |

Identical for both - stated so it is not left implicit:

- The activation-definition-first rule.
- The provisioning pre-condition.
- One action per touch.
- Tax/payout gating at onboarding.
- The never-activated branch structure.
- The humanizer pass.
- The Sequence Plan format itself.

## Failure modes

Fix in this order when several of these are true at once - activation bought per hour of fixing: `link placement > welcome dump > approval-as-finish-line > threat framing > activation nudge > archetype routing == never-activated branch`. The tie is argued: routing and the branch each cost about a week to build, but routing pays inside the window you are already in while the branch only pays on the next cohort - equal ratio, different clock.

| Failure                                                                | Fix                                                                                                  | Fix effort                                       |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| Tracking link buried, or not yet provisioned at send time              | Link/code in the first lines of touch 1; provisioning verified before the sequence launches          | near-zero                                        |
| The welcome dump - everything crammed into email one, no single action | One action per touch; move the rest to later touches or a persistent asset hub                       | an hour                                          |
| Approval treated as the finish line                                    | Set the concrete activation plan and expectations in touch 1                                         | an hour                                          |
| Termination threats used to force activation                           | Replace with opportunity-framed incentives; motivation research finds threats counterproductive      | near-zero, when threats are present at all       |
| No activation nudge, no time-boxed first-window incentive              | Deadline-bound bonus inside the first window, carried by a named touch                               | a week - the rate needs sign-off before it ships |
| One-size-fits-all sequence across archetypes and tiers                 | Route by archetype and tier before drafting anything                                                 | a week - one leading asset per archetype present |
| No branch for the never-activated                                      | Diagnostic at window end, re-engagement, final notice, archive - designed upfront                    | a week to design, then a standing job            |
| Payout/tax collection deferred until after the first commission        | Gate payout eligibility at onboarding; unclaimed-setup commissions have documented expiry precedents | a week plus finance coordination                 |

The payout/tax row sits outside that ordering deliberately. It buys avoided payout disputes and reduced legal exposure, not activation, so it cannot be ranked on the same ratio as the rows above it - fix it on the compliance clock, before the first commission is earned, whatever the activation work is doing.

## Diagnosing an existing sequence

When the user arrives with a running program ("our affiliates never send a click"), run checks in this order instead of redesigning from scratch. The order is information bought per unit of effort - not cheapest-first, which would put the conversion trace last and let you redesign a sequence that was working all along:

- information bought per hour spent: `conversion trace > approval-email check > per-touch engagement > cohort split > nudge and branch audit > rewriting touch 1`
- effort: `rewriting touch 1 > conversion trace == cohort split > approval-email check == per-touch engagement == nudge and branch audit`

Both ties are real, not hedges: the trace and the cohort split each cost about an hour of query and click work, and the last three each cost near-zero because they only read what already exists.

| #   | Check                                                                                                            | Effort        | What it settles                                                                                                            | Symptom pointing here                                                                       |
| --- | ---------------------------------------------------------------------------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 1   | Trace one conversion end to end: click → recorded conversion → pending commission → reversal state               | an hour, once | Whether the reported activation number is real. A dark hop makes every row below measure fiction                           | Activity visible in-platform but activation reported low; clicks tracked, conversions never |
| 2   | Open the approval email as a newly approved affiliate: is a working link or code in it, provisioned at approval? | near-zero     | Whether the fault is the pre-condition rather than the sequence at all                                                     | Approved affiliates never click                                                             |
| 3   | Read the per-touch open and click rates the platform already records                                             | near-zero     | Where the sequence loses people - localizes the fault, never names it                                                      | Opens collapse after touch 1                                                                |
| 4   | Split activation by archetype and by tier                                                                        | an hour       | Whether one sequence is being sent to archetypes that need different first actions                                         | One archetype activates, the rest never                                                     |
| 5   | Audit the plan for a deadline-bound nudge inside the window and a designed never-activated branch                | near-zero     | Why the cohort stalls at the deadline - explains a late-window stall only, nothing earlier                                 | Cohort stalls before the window closes; long tail piles up untouched                        |
| 6   | Rewrite touch 1 or the asset kit                                                                                 | a week        | Nothing, until 1-5 have run - it is a change, not a check, and it destroys the baseline that would have told you it worked | (none - never the first move)                                                               |

Re-rank against the program in front of you:

- A program already running server-side tracking has bought row 1's information in advance: start at row 2.
- A program with a single archetype in its intake drops row 4 from the list entirely, rather than ranking it last.

Copy-level vs structure-level separation lives in [references/copy-and-sequence-logic.md](references/copy-and-sequence-logic.md).

## KPIs and pass threshold

- Activation rate at the defined window - the sequence's primary score.
- Time-to-first-referral / time-to-first-conversion, tracked as a cohort median.
- Never-activated share of each monthly cohort at the cutoff.
- Per-touch engagement (open/click) to locate where the sequence loses people.

Measure by monthly approval cohort: each month's approvals form one cohort, judged only when its window closes. A blended all-time rate hides whether the sequence is improving.

Pass gates come in two parts, because the sequence ships before any activation number exists to measure.

**Design-time**, check before emitting the artifact, and iterate until every line holds:

- The activation definition and its window are fixed (step 2).
- Day-0 provisioning is verified, not assumed (step 3).
- Every touch asks exactly one action.
- The tracked link or code appears in the first lines of touch 1.
- A time-boxed nudge sits inside the activation window.
- The never-activated branch ends in archive, with no termination threat.
- Every drafted email has been through the humanizer.

**Post-launch**, scheduled as the first review gate: do not report a verdict you cannot compute.

- 30-day activation at or above ~18% for B2C, the TrackRev _median_, not its ~31% top quartile; 90-day at or above ~20% for B2B.
- Track360's "below 30% signals onboarding problems" is a diagnostic trigger for investigating, not a ship gate; used as one, it demands top-quartile performance on day one, above the entire 5-20% range this skill opens by citing.
- These are vendor and practitioner numbers, not audited studies: thresholds for iteration, never facts to quote.
- Below the gate, diagnose the sequence (provisioning, first touch, nudge), not recruitment.
- If the program has no data yet, say so in the deliverable and set the measurement date; the user may also document why their economics justify a different gate.
- Reliability framing for every number lives in [references/benchmarks-and-frameworks.md](references/benchmarks-and-frameworks.md) - read it before quoting any benchmark to the user.

## Invocation Examples

- "We approve about 40 affiliates a month and almost none ever send traffic. Design the onboarding sequence."
- "Map the first 30 days for a newly approved B2B SaaS affiliate - links auto-provision at approval, tax forms gate payout, one affiliate manager for the whole program."
- "Design the never-activated branch: what we send at day 30, how many times, and when we archive."

## Reference

- See [references/touch-plan-patterns.md](references/touch-plan-patterns.md) for the touch skeleton, trigger layer, tier and archetype routing, kickoff-call agenda, and the never-activated branch.
- See [references/asset-kit-and-provisioning.md](references/asset-kit-and-provisioning.md) for the day-0 checklist, tracking-readiness checks, kit contents per side, and payout/tax gating.
- See [references/copy-and-sequence-logic.md](references/copy-and-sequence-logic.md) for per-touch copy rules, subject lines, the humanizer pass, and exit/suppression/re-entry logic.
- See [references/sequence-plan-examples.md](references/sequence-plan-examples.md) for one fully worked B2C plan, one B2B plan, and a negative example.
- See [references/benchmarks-and-frameworks.md](references/benchmarks-and-frameworks.md) for every benchmark with its reliability flag, and the honest verdict on named frameworks.
- See `mbfinotti/partnerships-skills@affiliate-recruitment-outreach` for everything before approval.
- See `mbfinotti/partnerships-skills@affiliate-program-terms` for drafting the terms surfaced in touch 1.
- See `mbfinotti/partnerships-skills@affiliate-commission-structure` for the economics of the activation bonus and the commission ladder.
- See `mbfinotti/partnerships-skills@partner-enablement` for the training/certification curriculum a B2B touch may point to.
- See `mbfinotti/partnerships-skills@affiliate-performance-dashboard` for building the reporting behind the KPIs named here.
