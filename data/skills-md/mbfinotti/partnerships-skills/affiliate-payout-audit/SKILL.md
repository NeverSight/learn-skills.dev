---
name: affiliate-payout-audit
description: Audit an affiliate or partner commission payout run for accuracy before money is disbursed - per-line rate and tier recomputation, double-counted conversions, clawback and validation windows, period cutoff, currency, rounding, and tax-form status, delivered as an audit report with severities and recommended holds. Covers B2B SaaS recurring revenue-share and B2C ecommerce order-level CPA programs. Use whenever the user mentions an affiliate payout audit, commission accuracy, payout reconciliation, overpaid or underpaid affiliates, or a pre-disbursement review, even if they never say audit. Do NOT use for spotting fraudulent affiliates - use mbfinotti/partnerships-skills@affiliate-fraud-detection instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.1.10"
---

# Affiliate Payout Audit

Audit one affiliate/partner commission payout run before release: recompute the math, verify the rules, and report findings with recommended holds and corrections. Assume the activity already passed fraud screening - this skill checks whether the payout is _correct_, not whether it is _legitimate_.

No named, affiliate-native reconciliation framework exists; platforms ship locking and dispute mechanics, not a methodology. The method here borrows openly from adjacent finance disciplines:

- **Account reconciliation** (preparer/reviewer).
- **Three-way match** - platform export vs billing/order system vs CRM, the affiliate analogue of PO/receipt/invoice.
- **Revenue assurance**.
- **Segregation of duties / four-eyes (maker-checker)**.
- **SOX ICFR / COSO** - where the program sits inside a public company.

Say this plainly to the user; never present a branded framework.

## Interview

Ask before auditing anything. One question per message; offer multiple-choice answers when possible. Skip anything the user already answered.

- B2B SaaS recurring revenue-share, B2C ecommerce order-level CPA, or both?
- Commission structure in force: rate model, tier method (marginal or retroactive), per-partner-type overrides, promo/bonus windows, new-customer gating, sub-affiliate overrides, grandfathered legacy rates?
- Payout cadence, and this run's exact period boundaries - dates and timezone?
- Which data exports exist, and what is the internal source of truth: billing system, order database, or CRM closed-won?
- Validation/locking window length? What event releases a commission from pending to approved?
- Is any line in this run already paid, or is everything still reversible?
- Minimum payout threshold, currencies involved, FX handling policy?
- Tax-form status per payee - collected, missing, expired?
- Known historical error types and past partner disputes?
- Who calculates the run, and who releases the funds? Same person or different?
- Materiality threshold? Is the program subject to external financial-controls requirements (public-company ICFR)?
- By what date must the audit result land, and is the release date itself movable?
- One-off or compounding: fix this run only, or leave standing controls behind - a reusable recompute script, a reserve policy, a longer validation window?
- Effort ceiling: review hours available, whether you can execute code over the exports, whether finance can co-sign, and how much partner-relationship capital this run can spend?

Missing period boundaries, source of truth, or commission structure block the audit - insist before recomputing anything.

The last three answers re-rank every menu below:

- A hard release date promotes the cheap gates and drops full-population recompute.
- A compounding mandate promotes both full-population recompute and the fix-it-forward rung.
- No code access deletes full-population recompute outright.
- No finance co-signer deletes direct recovery from this run.

## The Audit Sequence

Run the checks in order; each gate assumes the previous one passed. The underlying lifecycle is the same five-gate machine everywhere: pull/export → reconcile to source of truth → verify rate/tier per line → dedupe → lock → pay.

**When the release date won't fit all twelve.** The numbering is a dependency order, not a priority order. To spend a short budget well, rank the gates by errors caught per hour:

- efficiency: dedup (6) > reconcile and comparability (3-4) > lifecycle window (8) > rate/tier recompute (7) > currency, tax, thresholds (9)
- value: reconcile and comparability (3-4) > dedup (6) > rate/tier recompute (7) > lifecycle window (8) > currency, tax, thresholds (9)
- effort: rate/tier recompute (7) - an hour with code, a week by hand > reconcile (3-4) - an hour on clean exports, a week on messy ones > lifecycle window (8) == currency, tax, thresholds (9) - an hour each, date arithmetic and a checklist > dedup (6) - near-zero with code over the key set
- compliance cost: currency, tax, thresholds (9) - a payee paid without a valid tax form is a filing problem, not just a money one > maker-checker (12) - the sign-off is the evidence an external control test asks for > every other gate == none, because being wrong there costs money, not a filing

Maker-checker (12) is never the gate you drop: it costs one scheduling and a second reader, and its absence is what let every error in the negative example ship.

Rate/tier recompute is what this order starves - highest value of the arithmetic gates, most expensive by hand. Promote it to first when:

- a partner has disputed a tier
- the run straddles a retroactive breakpoint
- the structure changed mid-period

The order is a default, not a law, and it shifts with who executes it: a network exporting full machine-readable logs collapses (6) and (7) to near-zero and moves both up; no billing-system access puts (3-4) out of reach and makes (7) the whole audit.

1. **Freeze the run scope.** Record run ID, period start/end, timezone, date basis (transaction vs validation vs amendment date), currencies, materiality threshold, and every data source. Ambiguous scope → stop and resolve; every later check depends on it.
2. **Pull the exports on the declared date basis.** Platform/network conversion export plus the internal source-of-truth extract for the same period. If you can analyze an uploaded spreadsheet or CSV, load both; otherwise ask the user for line counts, totals, and specific lines to read out.
3. **Comparability gate.** Before comparing or summing any two numeric sources, confirm they share the same event definition, date basis, time window, timezone, currency, counting method, and dedup identity. Any mismatch → normalize first, or report the numbers side by side with their definitions and refuse to compute a total. Detail in [references/reconciliation-and-dedup.md](references/reconciliation-and-dedup.md).
4. **Reconcile totals to the source of truth.** Compare line count and money value: platform export vs billing/orders/CRM. Pass = totals match within materiality. Fail = a gap that must be explained line by line before anything is approved - never "close enough".
5. **Work the exception queue.** Records in one system but not the other, matched on stable IDs only.
   - In platform, not in billing: possible over-credit, hold and investigate.
   - In billing, not in platform: untracked sale, expect an inbound partner dispute and decide credit policy explicitly.
6. **Dedupe.** One deterministic key per conversion (order ID / transaction ID / subscription ID). Quarantine empty or malformed keys. Collapse dual tracking (platform pixel + in-house tracker) to one canonical source. Check no key appears in the prior run - period straddle pays twice.
7. **Verify rate and tier per line.** Recompute expected commission from raw inputs using the terms in force at the original transaction date: tier method and boundary operator, partner-type overrides, promo windows against start/end datetimes, new-customer gating, sub-affiliate overrides, grandfathered rates. If you can execute code, recompute every line; otherwise recompute the sampled lines by hand. Math in [references/rate-and-tier-verification.md](references/rate-and-tier-verification.md).
8. **Verify lifecycle state per line.** Every line must have cleared its validation/locking window or been explicitly released; reversals for in-window refunds/churn must already be applied; refunds that landed after lock must appear as forward-period negative adjustments, not vanish. Rules in [references/lifecycle-and-clawback.md](references/lifecycle-and-clawback.md).
9. **Verify currency, rounding, tax, and thresholds.** FX strike date matches policy, rounding to 2 decimals at the end, sub-threshold balances carried forward, tax forms on file for every payee in the run. Detail in [references/currency-tax-and-payment.md](references/currency-tax-and-payment.md).
10. **Choose the coverage method**, ranked by errors found per hour:
    - efficiency: full-population recompute > risk-based stratified > top-earner spot-check
    - value: full-population recompute > risk-based stratified > top-earner spot-check
    - effort: risk-based stratified - an hour to design, then a week by hand at volume > top-earner spot-check - an hour > full-population recompute - an hour to write the script, near-zero every run after
    - Effort inverts value here: the most thorough method is also the cheapest once the script exists, and it is the only rung that compounds. It leads only when you can execute code over a complete, machine-readable export; without that it is off the menu entirely, and risk-based stratified leads.
    - Risk-based stratified = 100% of high-value lines, high-reversal partners, and top earners (a small share of partners drives most commission dollars), plus a random sample of the remainder sized against materiality. Top-earner spot-check catches concentration errors and is blind to long-tail systematics - take it only under a hard deadline.
    - Random-only sampling is not a rung: it costs the same hours as risk-based and finds fewer dollars. Use randomness for the remainder, never for the whole run. Document the method and rationale per selection.
11. **Compile the report.** Classify every line cleared / held / corrected; every discrepancy becomes a finding with severity, value at risk, and a recommended action (see Output, then Remediation). Escalate any pattern that smells illegitimate - self-referral, coordinated bursts - to fraud review; never rule on it here.
12. **Maker-checker sign-off.** The person who calculated the run must not be the person releasing funds; the audit report is the checker's evidence. Zero blocker findings outstanding before release - otherwise hold the affected lines or the run.

If your harness has persistent memory, memorize the run's parameters and accepted exceptions (period rules, source of truth, materiality, known one-sided records) so the next run starts from them; otherwise write them into the report header for reuse.

## Output: the Audit Report

Deliver every audit as this artifact:

```
PAYOUT AUDIT - <program>, run <id>, period <start>..<end> (<timezone>, <date basis>)
Scope     : <N> lines, proposed total <amount> <currency>; sources: <platform export> vs <source of truth>
Checks    : each numbered check above -> pass / fail / n-a, one line each
Findings  : F-<n> | severity: blocker / material / minor / informational | $ at risk | affected lines |
            action: correct before release / hold line / offset against future commission / absorb and
            document / fix it forward / direct recovery (ranked below) + escalate to fraud review if warranted
Exceptions: one-sided records with their queue (over-credit vs untracked) and resolution
Variance  : recomputed total vs proposed total; unexplained net variance vs materiality threshold
Cleared   : lines and value cleared for release (at corrected values)
Sign-off  : preparer, checker (must differ), date, release decision
```

Worked B2B SaaS and B2C ecommerce reports, plus a negative example, in [references/audit-report-examples.md](references/audit-report-examples.md).

## Remediation: the Action on Each Finding

Finding the error is the cheap half. Rank the response by value recovered per unit of effort and partner-relationship capital spent - never by how much money is nominally at stake.

1. **Correct before release.** Recompute the line, fix the run, pay the right number. Full recovery, no relationship cost - the partner never saw the wrong figure. Default whenever the line is still unpaid.
2. **Offset against future commission.** Book the correction as a forward-period negative adjustment carried against the partner's next earnings. Default once the line is paid. Full recovery, but only while the partner keeps earning.
3. **Absorb and document.** Write the line off and record it as a finding with its value. The honest rung below materiality, and the only one left for a partner who has churned out with a negative balance.
4. **Fix it forward.** Lengthen the validation window, add a reserve/holdback, install the shared idempotency key, or renegotiate that partner's rate card when the discrepancy is structural mispricing rather than an error. Recovers nothing from this run; retires the whole error class.
5. **Direct recovery.** Invoice the partner for the overpayment. Uncertain recovery, and the only rung that can end the relationship.

- efficiency: correct before release > offset > absorb and document > fix it forward > direct recovery
- value recovered: correct before release == offset > direct recovery > absorb and document == fix it forward
- effort: direct recovery - a week to a quarter of demand, finance and legal coordination > fix it forward - a week to build, then a standing job > offset - an hour, near-zero where the platform carries negative balances > correct before release == absorb - near-zero, a single edit each
- relationship capital: direct recovery > fix it forward > offset > correct before release == absorb - nothing spent, the partner is never asked for anything
- compliance cost: direct recovery - contract interpretation and legal sign-off, irreversible once sent > offset - must be authorized by the published terms, and several platforms state flatly that a paid commission can never be reclaimed > fix it forward - a terms amendment with notice to partners > correct before release == absorb - none

Justifying the ties:

- Correct-before-release and offset: both recover 100% of the line, differing only in timing.
- Absorb and fix-it-forward: both recover nothing from this run, differing only in what they buy later.
- Correct-before-release and absorb: each one edit that asks the partner for nothing.

- Delete, don't demote. If nothing in this run is paid, rungs 2, 3 and 5 are not alternatives - drop them and correct. If the terms or the platform forbid reclaiming a paid commission, delete offset and direct recovery; absorb and fix-it-forward are the whole menu.
- Fix it forward is what this order starves: high value, zero recovery this run, so it loses every round. Promote it to the top the moment the same finding class appears in two consecutive runs, or when post-lock refunds are routine rather than exceptional.
- Escalation to fraud review is not a rung. It answers a different question and runs in parallel with whichever rung is chosen.
- The order is a default, not a law, and it shifts with who executes it. Re-rank against what you already know:
  - A platform carrying negative balances natively promotes offset.
  - No finance co-signer this cycle deletes direct recovery from this run.
  - A roster small enough to re-run in full puts correct-before-release back on lines you would otherwise have to offset.

## Pass Threshold and KPIs

The run passes only when all three hold; iterate corrections and re-run the checks until they do, or recommend holding the run:

- Every line is either reconciled to the source of truth or on the exception list - no silent gaps.
- Unexplained net variance between recomputed and proposed totals sits at or below the materiality threshold.
- Zero blocker findings outstanding at release.

Track run over run:

- **Payout accuracy rate**: share of lines whose recomputed value matches the proposed value.
- **Exception value** as a share of total run value.
- **Reversal/clawback rate** against planning bands - roughly 2-8% for CPA, under 3% for revenue-share (benchmark ranges, not audited data). Above band → lengthen the validation window or tighten qualification.
- **Post-payout correction rate** - corrections found after money moved.
- **Dispute rate** and dispute resolution time.

## B2B SaaS vs B2C Ecommerce

The discipline is identical: the pending → approved → locked → paid lifecycle, the comparability gate, dedup keys, the exception queue, sampling, and maker-checker apply the same way to both. Audit both with the same sequence. Only three things genuinely diverge:

- **Reversal trigger.** B2C: order return, chargeback, or cancellation inside the return window. B2B SaaS: trial-to-paid failure, refund, downgrade, or mid-period churn.
- **Recurrence.** B2C CPA pays once per order. B2B revenue-share recurs on every billing event - proration, upgrades/downgrades, seat expansion, and the 12-month-cap vs lifetime rule make each cycle a fresh line to verify.
- **Source-of-truth integration.** B2B SaaS platforms often read the billing system directly, so platform data IS billing data - check 4 collapses to a spot-check. B2C networks track independently via pixel, so the full reconciliation stays mandatory.

Do not manufacture other differences; treating the two as separate disciplines duplicates work without catching more errors.

## Failure Modes

| Failure                                       | Why it happens                                                                                                              | Fix                                                                                                |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Tier boundary off-by-one                      | Marginal computed as retroactive (or vice versa); `>=` coded as `>` at the breakpoint; retroactive cliffs magnify the error | Recompute both readings at every boundary line; match the written structure; fix the operator      |
| Duplicate order IDs across sources            | Platform pixel and in-house tracker both record the same conversion                                                         | One canonical source per conversion; shared idempotency key; pay each key once                     |
| Malformed or empty dedup keys                 | Blank transaction IDs collapse many conversions into one record - or none                                                   | Quarantine blank/malformed keys; resolve manually before totaling                                  |
| Conversion counted in two consecutive periods | Re-export overlap or period straddle at the cutoff                                                                          | Half-open period windows; diff this run's keys against the prior run                               |
| Wrong date basis on the export                | Exports offer transaction vs validation vs amendment date; the wrong pick shifts lines across runs                          | Declare the date basis in run scope; re-pull on the declared basis                                 |
| Timezone boundary error at cutoff             | Platform, billing system, and program office each keep a different clock                                                    | Fix one timezone in scope; normalize all timestamps before applying the cutoff                     |
| Clawback window ignored                       | Lines approved before the validation window elapses, so refunds never reverse                                               | Hold every line still inside its window; size the window to the reversal curve                     |
| Refund lands after the record locks           | Locked/paid lines cannot be reversed on-platform                                                                            | Book a forward-period negative adjustment; carry negative balances against future earnings         |
| Recomputed against current terms              | Rates changed since the sale; some platforms re-evaluate modified lines at today's terms                                    | Recompute against the contract terms in force at the original transaction date                     |
| Currency rounding drift                       | Per-step rounding compounds across hundreds of small lines                                                                  | Round to 2 decimals at the end, not each step; drift above materiality → audit the rounding policy |
| Sub-threshold balances silently dropped       | Minimum payout threshold applied as an exclusion instead of a carry-forward                                                 | Verify below-threshold balances roll into the next run; they must never vanish                     |
| Payout released before tax forms on file      | Payee onboarding skipped or forms expired unnoticed                                                                         | Block release for any payee with a missing/expired form; recheck every run                         |

## Invocation Examples

- "Audit this month's payout run before we release it - 840 lines, $61K proposed, platform export and billing export attached."
- "Two affiliates disputed last quarter's commissions. Re-audit that run and tell me whether the tier was applied on marginal or full volume."
- "Our network export and our order database disagree by about $3K. Reconcile them and tell me what to hold."

## Reference

- `mbfinotti/partnerships-skills@affiliate-commission-structure` - for designing the structure this audit verifies against
- `mbfinotti/partnerships-skills@affiliate-fraud-detection` - for the fraud ruleset upstream of the payout calculation
- `mbfinotti/partnerships-skills@affiliate-program-terms` - for the T&C document that codifies validation windows and clawback rights
- `mbfinotti/partnerships-skills@affiliate-performance-dashboard` - for ongoing program metrics, as opposed to a per-run audit
