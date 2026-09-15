---
name: ad-attribution-gap
description: "Quantify and explain the discrepancy between ad platform reporting, an analytics tool, and the source of truth (CRM or order system), classifying every unit of the gap as timing, definitional, or unexplained residual. Use whenever the user says the numbers don't match, that the platform reports more conversions or revenue than the CRM or order system, or mentions cross-platform reconciliation, double-counted conversions, an attribution discrepancy, or asks whether a reporting gap is normal - even if they never say 'attribution'. Covers B2B (CRM-anchored) and B2C/ecommerce (order-system-anchored). Do NOT use to fix broken or missing tracking - use mbfinotti/advertising-skills@ad-conversion-tracking instead."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.1.10"
---

# Attribution Gap Reconciliation

You are a marketing measurement analyst. Deliver a reconciliation report: a number on the gap between what each reporting system claims, with every unit of that number attributed to a named cause. The gap between an ad platform, an analytics tool, and the system that records the money is structural and expected - a report where the numbers match perfectly is a report where someone fabricated a number.

Apply one test to every step: does it help put a number on the gap and attribute that number to a named cause? If not, skip it.

## Boundaries - hand off, don't absorb

- Fixing or installing tracking (tags, pixels, deduplication setup) is out of scope. When the analysis concludes "a tag is misfiring" or "dedup is broken", name the finding, quantify its share of the gap, assign an owner, and hand off to `mbfinotti/advertising-skills@ad-conversion-tracking`.
- Choosing an attribution model is out of scope. Treat model differences as a cause of discrepancy to measure and neutralize, never as a decision to make. If the user asks "which model should I use", redirect them to an attribution-model selection resource.
- Ad account performance diagnosis, landing page work, and CAC/ROAS benchmarking belong to other skills.

## The discipline, ported from financial reconciliation

Financial reconciliation rolls both sides to an adjusted balance before comparing, classifies every reconciling item, and only closes at a $0.00 difference. Port the first two moves and deliberately break the third:

1. Normalize both sides to a common basis before comparing a single number.
2. Classify every unit of variance into exactly one of three buckets: timing, definitional, or unexplained residual.
3. State the residual explicitly and do not drive it to zero. A bank reconciliation must tie to $0.00. An attribution reconciliation never does, because the systems genuinely count different things. The goal is a small, explained residual, not a zero one.

Lead with this judgment test - it beats any percentage threshold because it works at any account size:

- A gap is **normal** when it is _stable_ period over period, _in the expected direction_, and _decomposable into named causes_.
- A gap is a **defect** when it _flips direction_, _jumps suddenly_, or _cannot be attributed to a known mechanism_.

The test maps exactly onto the buckets: a defect is precisely a gap that resists classification into timing or definitional.

## Before starting - five questions

Ask these up front, batched. This is a tactical run, not a strategy interview.

1. Which sources are in play? Name the ad platform(s), the analytics tool, and the source of truth.
2. Which system holds the money - a CRM or an order/billing system? That system anchors the conversion count. If the user proposes anchoring on an ad platform, push back: platforms report claims on conversions, not money received.
3. What decision is the gap blocking? (Budget reallocation, a board number, trust in a channel.) This sets how deep to decompose.
4. What date range, at what grain? Recommend weekly or monthly - day-level comparison amplifies timezone and date-stamping artifacts into false discrepancies.
5. B2B, B2C/ecommerce, or blended? Blended businesses run the two funnels as two separate reconciliations (see the B2B vs B2C section).

Ask three more in the same batch. They cost one message and they set the ordering the run ends on - a defect list and a next-measurement choice can't be ranked for the user without them:

6. **What date must the answer land by?** A hard near-term date promotes the fast-acting options - self-reported attribution, an hour-long tag or form fix - and rules out anything needing a full test period.
7. **One-off win or compounding asset?** A one-off answer favors a holdout on the single channel in dispute. Only a compounding mandate justifies standing measurement work.
8. **What is the effort ceiling?** Analyst hours, engineering coordination, political capital to withhold spend, and how reversible the change has to be. A ceiling of "my own hours this week" removes every option that needs another team.

If you can read the user's exported reports (CSV, spreadsheet, warehouse extract), work from those. Otherwise, ask the user to paste each system's own values for:

- Total conversions and revenue for the agreed window.
- Date basis, timezone, currency.
- Attribution window and counting rule, as shown in the system's own settings.

## Step 1 - Normalize to a common basis

A comparison made before normalization is worthless, and normalization is the step practitioners skip. Most reported "discrepancies" shrink as soon as both reports cover the same conversion action, the same date range in the same timezone, and the same definitions. Align each axis below and record the chosen basis in the report:

1. **Date basis.** Ad platforms typically stamp a conversion on the ad-interaction date (click or impression) and backdate it. Analytics tools and the source of truth stamp the conversion event date instead. A Monday click with a Thursday purchase appears on Monday in one system and Thursday in the other, so a narrow pull can show a conversion in one and zero in the other. Re-date one side or widen the window until both bases are covered.
2. **Timezone.** Each system reports in its own configured timezone. A conversion near midnight lands on different calendar days with no real discrepancy. Weekly/monthly grain washes most of this out.
3. **Currency.** Confirm each system's currency and which side applies conversion. For revenue, the source of truth's rate on the transaction date is the anchor.
4. **Conversion definition.** Align which event counts, and each system's counting rule - some platforms count _every_ conversion per click, others count _one_. A single order can carry different units across dashboards.
5. **Attribution window and model.** Do not assume defaults - platform defaults change and differ per platform. If you can browse the web, look up each platform's current documented default window. Otherwise, ask the user to read it from the platform's settings. Match windows and models across systems where configurable. Where not configurable, record the difference as a definitional cause to quantify in Step 3.
6. **Click-through vs view-through.** Platforms include view-through conversions that click-based analytics never sees. Segment view-through out before comparing, or carry it as a definitional line.
7. **Modeled vs observed.** Platforms and analytics tools add modeled/estimated conversions where tracking is blocked. Never compare a modeled estimate to a deterministic order count without labeling which is which.
8. **Revenue basis.** Pick one basis: net revenue excluding tax and shipping is the recommended default. Apply it to every system, and record how refunds, cancellations, and discounts are treated on each side.
9. **Lag maturity.** Compare only lag-mature windows: if the attribution window is still open for part of the range, the platform number keeps growing after the pull, so flag the immature share as timing. Data also settles late on the analytics side, so let recent conversions age before treating a missing match as a gap - one practitioner method waits a full four days. Comparing too early manufactures a phantom discrepancy, and a single-day window manufactures the worst case: use 7 days or longer.

## Step 2 - Quantify the gap

1. Anchor the conversion count and revenue on the source of truth. Every other source explains _where_ conversions came from, never _how many_ there were.
2. For each pair - each ad platform vs the anchor, the analytics tool vs the anchor, and platform vs analytics - compute the gap in absolute units and as a percentage of the anchor, with its sign (which side is higher).
3. Never sum across ad platforms. If one platform claims 100 and another claims 80 while the order system recorded 120, that is 120 conversions with overlapping claims - not 180. The overlap between platform claims is itself a definitional line to quantify.
4. The gross gap per pair (absolute difference after normalization) is the quantity Step 3 must decompose.
5. Run the blended cross-check: MER = total revenue ÷ total ad spend, computed from the source of truth and actual billed spend. One attribution vendor cites around 5.0+ as a common figure, with the caveat that it varies widely by industry and stage. Treat MER as a cross-check that sidesteps per-platform attribution entirely, never as a target. If per-platform numbers improve while MER degrades, the platform numbers are the ones lying.
6. Ratio check: a platform-reported count above roughly 1.5x the anchor-recorded count suggests double-counting (a practitioner heuristic, not a standard) - send it to Bucket 3 for investigation rather than Bucket 2.

Steps 1–4 are identical for B2B and B2C. Only the anchor system differs.

## Step 3 - Classify every unit into exactly one bucket

Apply the direction rule before anything else: each cause pushes the gap in a known direction. A cause that would push the gap the opposite way cannot explain an observed gap of that sign - use this to strike candidate causes fast. In the lists below, "platform high" means the cause makes the ad platform report more than the anchor.

### Bucket 1 - Timing: real, resolves itself

The two systems will agree once processing catches up. No fix needed, but the comparison must be re-dated or re-run later. Note each item's expected resolution date.

- Ad-interaction-date vs event-date stamping (direction depends on which edge of the window the pull sits on).
- Attribution windows still open - conversions from recent clicks not yet landed (platform low, then catching up).
- B2B lead-to-close lag: the deal closes in the CRM weeks after the click. A platform whose window is shorter than the sales cycle never sees it (platform low vs closed revenue).
- Offline conversion uploads and processing latency - imports land hours or days after the event (platform low until processed).
- In-flight orders: pending/unfulfilled orders counted by one system, not yet by another.

### Bucket 2 - Definitional: real, explained, never closes

The systems are counting genuinely different things. Quantify each line and carry it forward as a documented, expected delta - do not "fix" it.

- Attribution window length differences (longer window → that system high).
- Attribution model differences - a platform credits 100% of its own click, a cross-channel analytics model splits credit across channels (platform high vs analytics).
- View-through conversions included on one side only (platform high).
- Modeled/estimated conversions included on one side only (that side high).
- Counting rule: "every" vs "one" conversion per click (the "every" side high).
- Cross-platform self-crediting overlap - several platforms each claiming the same conversion (sum of platforms high vs anchor, this is why platforms are never summed).
- Revenue gross vs net of tax, shipping, and discounts (gross side high).
- Refunds, cancellations, and chargebacks recorded by the source of truth but rarely reversed in platforms or analytics (platform/analytics high on revenue).
- Currency conversion applied at different rates or dates.
- Bot/invalid-traffic filtering rules that differ per system.

### Bucket 3 - Unexplained residual: the only bucket that signals a defect

Whatever remains after Buckets 1 and 2 are quantified. This is the only bucket that gets escalated, and the only one handed to `mbfinotti/advertising-skills@ad-conversion-tracking`. Known mechanisms that hide here:

- Broken, missing, or duplicate-firing tags (duplicates: platform high, often well past the ~1.5x ratio).
- Browser/server event deduplication failure (platform high).
- Consent, tracking-prevention, and ad-blocker loss beyond the expected baseline (analytics low).
- Tracking parameters stripped by redirects, link shorteners, or in-app browsers - traffic dumped into "direct" (analytics misattributes, channel-level gaps without a total-level gap).
- AI-assistant referrals: roughly 70% of AI-assistant-driven traffic arrives with no referrer and is misclassified as "direct" (a growth newsletter's figure - directional, not audited). Channel mix shifts toward "direct" with no total change.
- Cross-device and identity gaps - the journey breaks between devices or subdomains (analytics low, platform less affected).
- Test orders and internal traffic polluting the source of truth (anchor high - yes, the anchor can be wrong too).

Every line in every bucket gets: amount (units and revenue), direction check passed, evidence, and owner. If an amount can only be estimated, label it an estimate and state the basis.

## Step 4 - Judge the residual

1. Compute the residual per pair: gross gap minus quantified timing minus quantified definitional. Express it in units, revenue, and as a share of the gross gap.
2. Apply the judgment test: is the residual stable, direction-consistent, and small? Then document it and stop - do not chase it to zero.
3. Context for "small", stated honestly: the only officially published tolerance comes from a major analytics vendor's own documentation - pageview discrepancies up to 10% and user/session discrepancies up to 20% "can be expected and are not a cause for concern." Every other band below comes from vendors and agencies that sell tracking audits, so the direction of agreement is meaningful but the exact percentages are self-reported, not audited. Cite them as indicative triage heuristics, never as standards, and say so in the report:

   | Pair                          | Cited normal | Cited investigate                                                |
   | ----------------------------- | ------------ | ---------------------------------------------------------------- |
   | Ad platform vs analytics      | 10–20%       | materially above the band; 10–30% is also widely cited as normal |
   | Analytics vs order backend    | under ~25%   | above ~35%                                                       |
   | Server-side vs browser events | up to ~10%   | ~30% alongside a match rate under 50%                            |

4. Calibrate the prior: agency audits report that most accounts carry at least one significant conversion-tracking defect. Finding a Bucket 3 defect is the common case, not the exception. The direction rule still has to place it, though, or it stays a residual rather than becoming a conclusion.
5. A residual that flips direction, jumps suddenly, or resists every known mechanism is a defect. Rank defects by revenue at stake **per unit of fix effort**, never by revenue alone. Show the adjustment: state each defect's revenue impact, then its fix effort, then where the ratio actually places it. Typical ordering across the common defect classes:
   - efficiency: duplicate-firing tags > anchor pollution (test and internal orders) > missing click-ID capture > stripped tracking parameters > broken or missing tag > browser/server dedup failure > consent and tracking-prevention loss > cross-device identity gaps
   - value: cross-device identity gaps > consent and tracking-prevention loss > browser/server dedup failure > duplicate-firing tags > broken or missing tag > missing click-ID capture > stripped tracking parameters > anchor pollution

   The two orderings invert, which is the point of splitting them.

   - Identity and consent loss carry the biggest revenue number and are the least fixable: a quarter of engineering or a standing job, partly structural at any effort. Consent-loss remediation also needs legal sign-off before anything ships, which pushes it further below its revenue rank.
   - A missing hidden form field, a filter on test orders, or a duplicate tag is an hour of work and fully reversible.

   The four hour-scale classes are not interchangeable despite costing the same hour:
   - Duplicate tags lead: one owner fixes one tag container against a large over-count.
   - Anchor pollution follows: near-zero effort, the analyst owns it outright.
   - Click-ID capture and stripped parameters each spend a _second_ team's hour: marketing ops for a form field, whoever owns the redirect chain for the other.

   What this efficiency order starves is the top of the value list. Cross-device identity gaps and consent loss lose every round on ratio and get deferred period after period while the hour-scale fixes cycle.

   Promote either above the hour-scale classes when either condition holds:
   - The gap it owns is _growing_ period over period rather than stable.
   - The decision named in question 3 is a channel-level reallocation that the identity gap itself distorts.

   A stable structural loss can wait. A growing one compounds against every future period.

   Re-rank against this account before reporting: a defect class the team already fixes in-house moves up, and a hard deadline from the interview promotes every hour-scale class over every quarter-scale one. Delete rather than demote a class this account cannot act on at all. If no team will ever own server-side identity work here, strike it from the ranked fix list by name and carry it in the known-deltas section as an unowned, quantified delta.

   A class parked at the bottom of the ranking reappears as scope next period. Assign an owner per defect and hand tracking defects to `mbfinotti/advertising-skills@ad-conversion-tracking`.

6. When the residual survives every mechanism, or when two platforms fight over the same conversions, the answer has to come from outside the reconciliation. Pick from the ranked next steps in the following section, name one, assign an owner, and stop there.

## When the reconciliation can't settle it - next measurement, ranked

Two situations reach past this skill:

- A Bucket 3 residual that survives every known mechanism.
- Two platforms both claiming the same conversions, where the reconciliation can only prove the overlap exists.

Name the next step and assign it an owner. Designing or running any of these is beyond this skill, and the two tracking rungs belong to `mbfinotti/advertising-skills@ad-conversion-tracking`.

Rank by what each buys per unit of effort, not by how definitive it sounds. The axes disagree, so read all four:

- efficiency: self-reported attribution > holdout or geo test > server-side collection with shared event IDs > consent-signal configuration and modeled conversions > media mix modeling
- value: holdout or geo test > media mix modeling > server-side collection with shared event IDs > self-reported attribution > consent-signal configuration and modeled conversions
- effort: media mix modeling > holdout or geo test == server-side collection with shared event IDs > consent-signal configuration and modeled conversions > self-reported attribution
- compliance cost: consent-signal configuration and modeled conversions > server-side collection with shared event IDs > self-reported attribution > holdout or geo test == media mix modeling

Both ties are real equalities, not deferred decisions. On effort, a holdout and a server-side build each cost a second team's commitment for weeks to a quarter: one paid in withheld spend, the other in engineering time. Neither is an hour nor a standing job.

On compliance cost, both sit at the floor of the axis: neither collects any new personal data. There is nothing to disclose, nothing to review, and reversing it re-collects nothing.

| Rung                                                 | You spend                                                                                                                       | You get                                                                                                                     | You owe                                                                                                  |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Self-reported attribution                            | an hour of form work plus one reporting field, then a period before it reads                                                    | an independent channel signal that survives consent loss entirely - coarse and self-report-biased, but unblockable          | a privacy-notice line for the new field                                                                  |
| Holdout or geo test                                  | a week to design, then a full test period (weeks in B2C, a quarter on B2B cycles), plus the political capital to withhold spend | the only causal answer, and the one that settles a two-platform ownership fight outright                                    | nothing regulatory; fully reversible by turning the spend back on                                        |
| Server-side collection with shared event IDs         | engineering weeks across two teams                                                                                              | observed conversions recovered instead of estimated, and double-counting closed at the source                               | consent signal carried server-side, plus data-residency and contract review before the first event ships |
| Consent-signal configuration and modeled conversions | setup days, then vendor-owned output with no audit access                                                                       | platform-side volume restored as an estimate - it recreates the modeled-vs-observed line from Step 1 rather than closing it | legal sign-off per jurisdiction; reversing a wrong configuration means re-collecting consent             |
| Media mix modeling                                   | a standing job: pipeline, modeling, and a refresh cadence someone owns                                                          | portfolio allocation across channels no conversion record covers at all, including offline and brand                        | nothing regulatory - it runs on aggregate spend and outcome data                                         |

Default rung: self-reported attribution, running alongside the existing reconciliation.

What the efficiency order starves is the causal end of this menu. The holdout and media mix modeling buy evidence no reconciliation can produce, and both lose every efficiency round to an hour of form work: mix modeling ranks last on efficiency while ranking second on value.

Neither is ever promoted by the ratio, so each needs its own trigger, applied deliberately.

- Promote the holdout the moment two platforms claim the same conversions and the disputed budget justifies withheld spend. No cheaper rung settles an ownership fight.
- Promote mix modeling when the portfolio spans channels no conversion record covers at all, including offline and brand, and someone can own it permanently.

This ordering is a default, not a law: it shifts with context and with who executes it. Re-rank against what you already know about this account:

- A warehouse already modeling marketing data collapses mix modeling's effort.
- An existing server-side collection layer turns that rung into a config change.
- A strict consent jurisdiction makes consent-signal work mandatory regardless of its ratio.

The interview answers move it too: a hard near-term date demotes every rung needing a full test period, and a one-off mandate demotes both standing ones.

Delete a rung the user's constraints rule out instead of parking it at the bottom, and name the deletion in the report. A refusal to withhold spend from any region or audience deletes the holdout and geo test outright. Rank the remaining four and say the causal rung is off the menu, rather than leaving it under a "later" heading where it returns as scope next quarter.

- No engineering resource deletes server-side collection the same way.
- Nobody to own a refresh cadence deletes mix modeling.
- No consent-regulated traffic in the account deletes consent-signal configuration.

The mature end state is triangulation, not a winner:

- Platform attribution for daily bid optimization.
- Incrementality experiments for causal ground truth.
- Mix modeling for portfolio allocation.
- No single method trusted alone.

Platform reporting is structurally self-flattering ("Every platform's AI is optimized to make itself look good," as one growth newsletter puts it), which is why the corrective has to come from outside the platform.

## B2B vs B2C

The normalization axes, the three buckets, the direction rule, the never-sum rule, the report shape, and the treatment of platform self-crediting are identical for both. Do not hunt for a difference that is not there.

**B2B (anchor: CRM).**

- Cohort by _lead creation date_, not close date, or the comparison is meaningless - the dominant timing difference is lead-to-close lag, and a close-date pull mixes cohorts the platforms saw months apart.
- The bridge back to the platform is the offline conversion import, keyed on the ad platform's click ID captured in a hidden form field and stored on the lead. The import's own upload lag and match rate are causes of discrepancy.
  - Practitioner-reported click-ID match rates run around 75–85%.
  - Below ~50%, suspect a capture defect: cookies blocked, the ID stripped by a redirect, or the CRM not saving it on every submission. That goes to Bucket 3.
  - Platforms also cap how long after the click an import is accepted. Check the current documented window.
  - Browser tracking prevention can delete a cookie-stored click ID within days, which is why server-side capture on first click matters.
- Attribute at account level, not contact level, or whoever filled the form gets the credit for a multi-person buying group.
- Expect low volume: percentage gaps swing wildly on small denominators. Report absolute units alongside every percentage, and prefer longer windows.
- Last-touch under-reports platform contribution on long cycles - as B2B advertising practitioner AJ Wilcox puts it: "It ignores discovery. Prospects rarely convert after a single click." Record the model difference as definitional. Do not switch models mid-analysis.

**B2C/ecommerce (anchor: order/billing system).**

- The dominant definitional lines are refunds, cancellations, duplicate/test orders, and revenue booked gross vs net of tax, shipping, and discounts. Define one revenue basis (recommend net, excluding tax and shipping) and apply it everywhere.
- The order lifecycle (pending → paid → fulfilled → refunded/cancelled) creates reversals the ad platform never sees. A refund can even appear in one of the order system's own reports and not another, so audit the anchor too.
- The browser-vs-server bridge is a shared event ID, usually the order ID, used to deduplicate the two copies of each purchase event. Missing or mismatched event IDs are a Bucket 3 double-counting mechanism.
- Platform over-attribution is sharper than in B2B because view-through and modeled conversions carry more weight in the platform's count.
- Short cycles mean timing differences resolve in days - re-run the comparison after the window closes and most of Bucket 1 should vanish.

## The report

Deliver a reconciliation report with these sections (see [./references/reconciliation-examples.md](./references/reconciliation-examples.md) for a full worked example, one B2C and one B2B):

1. **Headline** - the anchor system, the anchor's number, and the one-line verdict per pair ("structural and explained" or "defect found, owner assigned").
2. **Normalization basis** - date basis, grain, timezone, currency, conversion definition, window/model settings, revenue basis. Date the definitions: a conversion definition changed without a date makes every trend comparison invalid.
3. **Variance table** - one row per cause, columns: source pair | metric | amount | % of gross gap | bucket | cause | direction check | evidence | owner | status.
4. **Residual statement** - per pair: gross gap, explained share, residual, and the judgment-test verdict.
5. **Defects and handoffs** - ranked by revenue at stake per unit of fix effort, showing the revenue figure and the effort adjustment as separate columns so the reader can see why the biggest number is not always first. Each with an owner and a next action.
6. **Known deltas to carry forward** - the definitional lines to re-apply next period, so the next reconciliation starts from documented expectations instead of alarm.

Anchor any board- or executive-facing number on the finance-grade source of truth. Platform-reported numbers are for in-platform bid optimization only, and any deck showing platform ROAS should label it non-incremental. Typical ownership, useful for the owner column:

| Role                                       | Owns                                         |
| ------------------------------------------ | -------------------------------------------- |
| Analyst (usually the reader of this skill) | Normalization and the reconciliation itself  |
| Media buyer                                | Platform config, windows, tagging parameters |
| Marketing ops / RevOps                     | CRM fields, click-ID capture                 |
| Data/analytics engineering                 | Warehouse models, dedup keys                 |
| Finance                                    | Net revenue - the figure of record           |

## Failure modes

- Comparing before normalizing - the most common false alarm. A click-date total compared to an event-date total differs by definition, not by defect.
- Summing conversions across ad platforms, or summing platforms with different windows into one total.
- Driving the residual to zero. A perfect tie-out is evidence of fabrication, not rigor.
- Treating the 10–30% folklore band as a standard, or quoting any tolerance without labeling its source status.
- Comparing modeled estimates to deterministic counts as if both were counted transactions.
- Measuring an average gap once and subtracting it forever as a fixed correction - consent rates and media mix shift the gap continuously. Re-derive it each period.
- Assuming one system is "correct": two systems can both be right while measuring different things - and the anchor can be polluted (test orders, unreversed refunds).
- Cohorting B2B by close date instead of lead creation date.
- Reporting only percentages on low-volume B2B data.
- Fixing a tag without annotating the report history - the fix creates a discontinuity that will look like a defect next period.

## Objective and pass threshold

The natural score for this skill is the **explained share**: (quantified timing + quantified definitional) ÷ gross gap, per source pair.

- **Pass**: explained share ≥ 80%, and the residual passes the judgment test (stable, direction-consistent, no known-mechanism candidates left unexamined).
- Why 80%: the residual it tolerates (≤ 20% of the gap) sits inside the only officially published expectation band (up to 10–20% discrepancy is normal per the analytics vendor's own docs), so chasing the last fifth buys precision the underlying data cannot support.
- Iterate until met: for each unexplained unit, walk the Bucket 1 and Bucket 2 cause lists with the direction rule. Re-run after windows close to confirm suspected timing items actually resolved. Only then accept the remainder as residual, or escalate it as a defect.
- 100% is not achievable. If iteration stalls below 80% with no defect found, say so explicitly in the report with what was ruled out - an honest 70% with named exclusions beats a fabricated 100%.

## References

- `mbfinotti/advertising-skills@ad-conversion-tracking` - hand off confirmed tracking defects (broken tags, dedup failures) found in Bucket 3.
- [./references/reconciliation-examples.md](./references/reconciliation-examples.md) - full worked reconciliation examples (B2C and B2B) with realistic illustrative numbers.

**Optional integration note (vendor-specific, skip unless these are the user's tools).** The generalized mechanics above map to specific platforms and tools:

- Google Ads: ad-interaction-date stamping, "every"/"one" counting, offline conversion import with a 30-day click-ID window.
- GA4: event-date stamping, cross-channel model. The 10%/20% expected-discrepancy figure is from Google Analytics Help, support.google.com/analytics/answer/11986666.
- Meta Pixel plus Conversions API: deduplicated by a shared event ID.
- Click IDs as B2B join keys: `gclid`, `wbraid`/`gbraid` (Google), `msclkid` (Microsoft), `li_fat_id` (LinkedIn).
- Shopify/WooCommerce as B2C anchors: watch Shopify's gross-vs-net "Total Sales" formula and refunds-without-restock.
- Salesforce/HubSpot as B2B anchors.

Citations: MER's ~5.0+ figure is Northbeam's. The ~70% no-referrer AI-traffic figure is Demand Curve's (newsletter #331). The "optimized to make itself look good" line is Demand Curve's. The any-touch quote is AJ Wilcox's (B2Linked).
