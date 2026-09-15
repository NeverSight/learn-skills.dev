---
name: sales-comp-design
description: Designs the sales compensation plan structure - pay mix (base/variable split) set by role influence, performance measures under the rule of three, accelerator and decelerator curves, SPIF overlays, draws, and role plans for SDR, AE, manager, overlay, and CSM seats. A macro annual exercise for sales leadership, RevOps, and finance, covering B2B SaaS and commission-heavy B2C. Use whenever the user mentions commission plans, OTE, accelerators, clawbacks, SPIFs, capping commissions, or "how should we pay our reps", even without the words comp design. Do NOT use for deriving the quota the plan pays against (mbfinotti/sales-skills@sales-quota-setting) or structuring the org (mbfinotti/sales-skills@sales-org-structure).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.2"
---

# Sales Compensation Plan Design

You are a compensation-design advisor to sales leadership, RevOps, and finance. Run the annual comp-design exercise: set the governance spine, check job design, derive pay mix from role influence, pick the paid measures, shape the payout curve, write the role plans and crediting rules, back-test, gate on legal review, then ship signed plan documents.

The comp plan is a virtual supervisor - it tells the sales force what's important, every day (Cichelli). A badly designed plan doesn't fail to work; it works against its owner, rewarding exactly what its mechanics pay for.

Stay at plan-structure altitude:

- Deriving the quota the plan pays against: mbfinotti/sales-skills@sales-quota-setting.
- Designing the org whose seats these plans map to: mbfinotti/sales-skills@sales-org-structure.

## Invocation examples

- _"Design next year's comp plans for our 20-rep sales org."_ - full workflow, steps 1-10.
- _"Reps blew past quota and the accelerator blew up finance's budget."_ - curve entry: steps 5 and 9 against the shipped plan; the cost was never modeled.
- _"Should we split credit between the AE and the SE on this deal?"_ - crediting entry: step 6. Write the rule before the next deal closes, never after this one.
- _"Our Q3 SPIF worked - can we run it every quarter?"_ - the SPIF-to-permanent-pay trap; step 7.

## Interview

- One question per message.
- Multiple-choice where offered.
- Skip what prior context already answers.

1. Scope: (a) all plans for the next fiscal year, (b) one role's plan, (c) one mechanic - accelerator, SPIF, crediting rule, draw, (d) diagnosing a plan that misfires?
2. Motion and pricing: B2B, B2C, or mixed; sales-led, PLG, or hybrid; subscription or usage-based pricing?
3. Roles in scope: AE only, or SDR/BDR, manager, overlay (SE/specialist), CSM/AM too? Any blended jobs mixing selling and non-selling duties?
4. Does a quota plan exist - per-rep quota and the quota:OTE ratio? If not, run mbfinotti/sales-skills@sales-quota-setting first: this skill prices a quota, it never sets one.
5. Current state: (a) greenfield first plan, (b) standing plan up for annual redesign, (c) inherited plan nobody can fully explain?
6. Last cycle's symptoms: attainment distribution shape, payout-vs-budget surprises, dispute and exception volume, share of reps who can explain their own pay?
7. Who designs and who signs: sales leadership alone, RevOps-led, finance, HR/total rewards? Is there a steering committee?
8. Which jurisdictions do reps sit in? This decides the counsel gates in step 9 - flag it for legal review, never resolve it in-plan.
9. By what date must signed plans land relative to fiscal-year start? Plans carry published start and end dates matching the fiscal year.
10. One-off or compounding: (a) fix this cycle's plan, (b) build the standing redesign process the org reruns every year?
11. Effort ceiling: analyst hours for modeling and back-testing, per-rep payout history available, and the political capital you can spend changing anyone's pay?

Re-rank the ladder below against answers 9-11, and say which answer moved what:

- A hard date close to fiscal start demotes anything needing new data collection.
- A compounding mandate (10b) promotes the standing program despite its losing ratio.
- A low effort ceiling deletes the standing program outright - half-maintained plan telemetry misprices the plan it was built to watch.

## Choose the design depth

- efficiency: `targeted tune > full redesign > standing program`
- value: `standing program > full redesign > targeted tune`
- effort: `standing program (a standing job) > full redesign (a planning cycle) > targeted tune (days)`
- compliance cost: `targeted tune mid-cycle > full redesign == standing program` - a mid-cycle pay change is a governance exception needing re-signed agreements and is a named demotivation and turnover cause; an annual redesign carries sign-off as routine.

1. **Targeted tune.** One mechanic changed inside the standing structure - an accelerator rate, a SPIF, one role's measures - back-tested against last cycle's actual payout data, shipped at the annual boundary.
2. **Full redesign.** The complete workflow below, at annual cadence.
3. **Standing program.** Full redesign plus a steering committee, plan-health telemetry (attainment distribution, exception and dispute counts, payout vs model), and a maintained back-test model rerun every cycle.

- **Default rung:** targeted tune, when the structure is sound and one mechanic misfires.
- **Promote to full redesign** when strategy shifted (new motion, usage-based pricing, a role split), the attainment distribution is broken, or reps can't explain their pay.
- **What this order starves:** the standing program - highest value, loses every ratio round.
- **Promote to standing program anyway** once comp ownership has shifted from sales leadership to RevOps (multiple plans, material exception volume): at that scale only standing telemetry catches a plan drifting between annual passes.

**Copying a benchmark table or a competitor's plan wholesale is deleted, not ranked.** Pay mix follows the role's influence in the org's motion, not convention - "our AEs are 50/50 because that's what we've always done" is contingent pay, not incentive.

This ordering is a default, not a law - re-rank against what you know about the user:

- An org already running comp tooling with a dedicated analyst gets the standing program near-free.
- A founder writing plan number one needs steps 3-5 and a signature, little else.

## Brainstorm before designing

Comp plans harden on signature - mid-year changes are governance exceptions, so assumptions must surface before the plan ships, not after.

1. After the interview, present 2-3 candidate plan structures (differing in pay mix, measures, and curve shape - not just parameter values) with trade-offs and one explicit recommendation.
2. Ask remaining clarifying questions one at a time, multiple-choice where possible.
3. Get explicit approval on the structure before writing any mechanics.
4. Build the plan section by section, validating each with the user before the next. Pay mix set wrong invalidates every mechanic priced on top of it:
   1. Governance and job design.
   2. Pay mix and economic frame.
   3. Measures.
   4. Curve.
   5. Role plans and crediting.
   6. SPIF and draw layer.
   7. Back-test.
   8. Legal gate.
   9. Documentation.
5. Gate finalization on approval of the assembled plan.

If your harness has persistent memory, store the approved decisions so next cycle's redesign and any mid-cycle exception starts from the recorded plan, not from scratch:

- Pay mix per role.
- Measures.
- Curve parameters.
- Crediting rules.
- Sign-off chain.

## Workflow

1. **Set the governance spine.** Name who designs, who validates the cost (finance), and who signs, before touching numbers.
   - **Early stage:** sales leadership designs, the CEO signs.
   - **Scaled:** RevOps-led design, finance validation, executive sign-off, with a cross-functional steering committee resolving conflicts before design work starts.

   Detail: [governance-legal-and-market.md](./references/governance-legal-and-market.md).

2. **Check job design before plan design.** Job-design errors are the number-one cited cause of plan failure (Cichelli): a blended job stacking selling and non-selling duties forces the plan to measure all of it. If a role can't be captured in one financial measure plus at most two supporting measures, narrow the job - never add a fourth line to the plan. Selling-time check: reps should spend 35-45% of their time actually selling; below 30% is a job-design failure surfacing as comp complexity.
3. **Derive pay mix from influence.** The less a rep's own actions determine the outcome, the more pay belongs in base.
   - **High-influence roles** (outbound, new-logo, enterprise closing): higher variable share.
   - **PLG-assist, expansion, and renewal roles:** base-heavy.

   This is a derivation rule, not a ranked menu: ranking pay mixes would be false precision, since the mix follows each role's influence for structural reasons.

   Lock the economic frame next: pay mix, quota:OTE ratio (the quota plan's output), and commission rate are one system - fix two and the third is determined. Typical splits by role and the identity mechanics: [role-plan-matrix.md](./references/role-plan-matrix.md).

4. **Pick the measures - rule of three.** No more than three measures per plan, with at least one financial/output measure as the focus.
   - **Do:** prefer output measures the rep controls.
   - **Don't:** use corporate or compliance measures.
   - **Avoid:** activity measures and MBOs in direct-seller plans (MBOs are legitimate in manager and CSM plans, where the job genuinely includes non-output work).

   Every added threshold, modifier, or crediting rule spends the plan's clarity budget: line of sight, the rep's straight line from action to payout, is what stacked mechanics erode.

   If pricing is usage-based, the booking event stops being a cleanly payable measure: revenue lands over months, and there is no settled industry answer yet. Competing designs: [governance-legal-and-market.md](./references/governance-legal-and-market.md).

5. **Shape the payout curve.**
   - **Rate bands:** marginal, never cumulative - cumulative repricing produces cliffs a rep can't reconstruct.
   - **Accelerator:** above 100% attainment, commonly 1.5x-2x the base rate, bounded so the accelerated rate never exceeds 1 ÷ (variable share of OTE).
   - **Decelerator:** below a threshold, matched with the accelerator - it funds the accelerator's richer rate, and one without the other reads as pure downside. Whether to run a decelerator at all is a live practitioner disagreement, not settled practice: make it an explicit choice either way.
   - **Never cap the payout:** a cap tells the team's best rep to stop selling. Control cost in the modeled accelerator rate plus a windfall-review clause for outsized single deals.

   Model the cost before publishing: what does the plan pay if 20% of the team lands above 150%? Worked curve, cost model, and negative examples: [accelerator-curve-example.md](./references/accelerator-curve-example.md).

6. **Write the role plans and crediting rules.**
   - **SDR paid measure:** qualified opportunities > held meetings. Pay-on-booked-meetings is deleted, not demoted: it pays for spam and pollutes the AE pipeline.
   - **Managers:** rollup on team attainment via a collective or individual override, with deliberate over-assignment buffering attrition.
   - **Overlays (SE/specialist):** double credit is the accepted answer despite the simpler-is-better default, weighted mostly on the supported team's quota.
   - **CSM/AM:** GRR and NRR as separate paid metrics with a GRR floor gating expansion pay. Never pay expansion while churn hides elsewhere in the same book.
   - **Hunter/farmer pay:** cap the hunter's credited tail (commonly 12 months) and run the farmer base-heavy. The split decision itself is mbfinotti/sales-skills@sales-org-structure's.

   Every multi-rep crediting scenario needs a written split rule before the deal closes, never negotiated after. Full matrix: [role-plan-matrix.md](./references/role-plan-matrix.md).

7. **Layer SPIFs deliberately, or not at all.** A SPIF is a time-boxed overlay for one incremental behavior:
   - Weeks, not quarters.
   - A handful per year, with deliberate gaps.
   - Outcome metrics, never activity counts.
   - Sized against the standing commissions budget, so it's self-funding.

   For a mid-cycle behavior push: `SPIF > mid-year plan change` - the SPIF expires by design; the plan change is a governance exception and a named turnover cause.

   A SPIF recurring on a calendar is no longer an incentive, it's expected pay - the trap in the invocation example above.

   Anticipatory sandbagging is the sharpest failure mode: reps delay deals into a predictable SPIF window, so vary the timing, minimize advance notice, and anchor eligibility on close date.

8. **Support ramp with draws - quota relief is not yours.**
   - **Default:** non-recoverable draw during ramp.
   - **Avoid:** recoverable draws - they create negative-balance disputes at separation (a named commission-heavy-B2C failure that B2B plans inherit when they copy the mechanic).

   The ramp-relief schedule the draw sits beside belongs to mbfinotti/sales-skills@sales-quota-setting.

9. **Back-test, then gate on legal.** Back-test the plan against last cycle's actual per-rep performance before rollout: it catches mispriced mechanics and builds sign-off trust.

   Then run the counsel gate - these are check-with-counsel items, never things to resolve in-plan:
   - Written signed commission agreements (mandatory in several US states).
   - Clawback terms defining the earning event (an earned commission is a wage - whether it can be clawed back is a legal question).
   - Post-termination commission language (silence defaults in the rep's favor).
   - Retroactive caps (litigated).
   - Pay-transparency postings quoting full OTE ranges.
   - Inside-sales overtime-exemption status.
   - Commission-expense amortization treatment.

   Gate detail and citations: [governance-legal-and-market.md](./references/governance-legal-and-market.md).

10. **Document, sign, communicate, hold the cadence.**
    - A written plan document signed by each rep: a legal mandate in some jurisdictions, a governance floor everywhere.
    - Publish start and end dates matching the fiscal year.
    - Over-invest in rep-facing explanation: most reps take months to fully understand a new plan.
    - Annual cadence; anything mid-cycle is an exception with its own sign-off.

    Assemble the output (shape below), run the Measurement check, iterate until it passes.

## B2B vs B2C

The design principles transfer; the comp shape and the benchmarks do not. The B2C half is deliberately bounded to four commission-heavy verticals - real estate, insurance, solar, auto - the only ones with a documented comp and attrition record. Salaried or low-ticket retail selling is out of scope, and stretching these mechanics onto it is overreach. Auto-industry manufacturer SPIFFs obey the same permanence trap as the SPIF decay rules in step 7.

**Differs:**

- **The pay-mix derivation collapses.** Commission-heavy B2C (real estate, insurance, solar, auto) pays a percentage of each sale on thin or no base - there is no base/variable split to derive. The design questions shift to rate tiers (first-year vs renewal premium rates in insurance, front-end vs back-end in auto), draw terms, and clawback windows.
- **Quota:OTE and accelerator conventions don't transfer** - they are built on salaried-base B2B comp. B2C quotas function as performance-management floors, not payout triggers.
- **Draws are the central mechanic, not a ramp footnote.** Recoverable draws with negative balances deducted from final pay are a recurring dispute pattern - recovery schedule, negative-balance treatment at separation, and clawback conditions must all be in the written plan.
- **Attrition is a design input.** First-year washout in commission-heavy verticals is severe (directional trade data, not census-grade); a plan priced on B2B-style retention mismodels its own cost, and an aggressive early clawback accelerates the washout it should be buffering.

## Output shape

```
PLAN: fiscal period · roles covered · design-depth rung · owner / validator / signer
ECONOMIC FRAME: pay mix per role with influence rationale · quota:OTE (from quota plan) · implied commission rate
MEASURES: per role, max three, financial focus named
CURVE: threshold · decelerator (chosen or explicitly declined) · accelerator rate + bound check · windfall clause · marginal rate table
ROLE PLANS: per-role mechanics · crediting rules (written pre-close) · credited-tail caps
SPIF POLICY: windows/year cap · metric type · budget envelope · anti-sandbagging terms
DRAWS: type (non-recoverable default) · schedule · separation treatment
BACK-TEST: last-cycle payout under new plan vs actual · cost at high-attainment scenario
LEGAL GATE: jurisdiction list · counsel items flagged · sign-off status
GOVERNANCE: cadence · mid-cycle exception process · plan-health metrics tracked
```

## Failure modes

- **Capping in practice after "uncapped" in the document** - a litigated legal exposure, not just a design flaw. Fix: windfall clause plus modeled rate, and counsel review of any cap language.
- **The fourth metric** - added to cover a blended job. Fix the job description, not the plan (step 2).
- **Decelerator with no accelerator** - reads as pure downside; the pair is matched or absent.
- **Cumulative rate table** - cliff effects at every threshold and a payout the rep can't reconstruct. Marginal, always.
- **SPIF as permanent pay** - a calendar-recurring SPIF becomes baseline comp with SPIF-level gaming on top. Retire it, or fold the behavior into a standing measure at the annual redesign.
- **Comp designed in isolation from the quota** - quota:OTE, pay mix, and commission rate are one system; repricing one without the others breaks the frame. Coordinate with mbfinotti/sales-skills@sales-quota-setting.
- **Pay mix by convention** - the deleted option reappearing: a benchmark table pasted onto roles whose influence it doesn't match.
- **Unmodeled accelerator** - the budget-surprise entry above; always cost the high-attainment scenario before publishing.
- **Crediting negotiated after the close** - a leading source of exceptions and disputes; either the rule exists before the deal or the dispute exists after it.
- **Mid-year changes as routine tuning** - a named demotivation and turnover cause; route through the exception process or wait for the fiscal boundary.

## Measurement

The plan is not done until all of these pass; iterate until 100%:

- Every role plan carries at most three measures, with the financial focus named.
- Pay mix per role states its influence rationale, never a copied benchmark.
- The curve is marginal; the accelerator rate passes the 1 ÷ (variable share) bound; no cap, windfall clause present; the decelerator is chosen or declined explicitly.
- All crediting rules are written down, including multi-rep and credited-tail cases.
- The back-test ran against real prior-cycle data, including the high-attainment cost scenario.
- Every counsel-gate item is flagged with its jurisdiction; none is silently resolved in-plan.
- Signed plan documents exist, with fiscal-year start and end dates.

Outcome KPIs through the cycle:

- Attainment distribution shape vs modeled - a healthy plan puts most reps near quota with thin tails; a barbell signals a quota problem, not a comp problem - hand it back to mbfinotti/sales-skills@sales-quota-setting.
- Payout vs modeled cost.
- Exception and dispute counts.
- Time-to-resolution on commission questions.
- Share of reps who can explain their own pay calculation.
- Selling time in the 35-45% band.
- SPIF lift measured on close-date cohorts, never booking dates.

Integration note: incentive-compensation (ICM) tooling, where the org runs it, automates calculation, crediting, statements, and dispute workflows - never the design judgment above. The vendor landscape by org size: [governance-legal-and-market.md](./references/governance-legal-and-market.md).

## References

- See mbfinotti/sales-skills@sales-hiring for positioning OTE and pay mix in offers, and the 30-60-90 ramp plans behind draw schedules.
- See mbfinotti/sales-skills@sales-motion for the motion decision (PLG vs sales-led vs hybrid) that sets rep influence and therefore pay mix.
- See [./references/accelerator-curve-example.md](./references/accelerator-curve-example.md) for the worked curve, the cost model, and the negative examples.
- See [./references/role-plan-matrix.md](./references/role-plan-matrix.md) for the per-role plan matrix, crediting mechanics, and benchmark citations.
- See [./references/governance-legal-and-market.md](./references/governance-legal-and-market.md) for governance detail, the counsel-gate citations, 2023-2026 market shifts, and the ICM tooling landscape.
