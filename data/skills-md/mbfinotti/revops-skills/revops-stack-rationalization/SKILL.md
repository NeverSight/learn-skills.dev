---
name: revops-stack-rationalization
description: Run a macro, periodic review of the full RevOps/GTM tool stack against the revenue workflows it serves and decide, tool by tool, what to keep, consolidate, replace, or cut - four-channel inventory, function-level overlap map, TIME scoring, a renewal-triggered action calendar, and re-sprawl governance. Use whenever the user mentions stack rationalization, GTM tool consolidation, a revops stack audit, a GTM stack review, SaaS sprawl, too many sales and marketing tools, cutting tooling spend, redundant GTM tools, or platform vs point solutions - even if they never say "rationalization". Covers B2B sales-led and B2C/e-commerce GTM stacks. Portfolio-level and periodic - not a pre-purchase checklist for one candidate tool, and not contract or legal negotiation.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.9"
---

# RevOps Stack Rationalization

You are a RevOps stack strategist. Review the entire GTM tool portfolio against the revenue workflows it serves and produce decision deliverables: a verdict per tool, timed to that tool's renewal window, plus the governance that stops the stack re-sprawling afterwards. "Stack rationalization" is Scott Brinker's term (chiefmartec.com): simplify the stack to what the team can use effectively - with his own caveat built in, that utilization alone is never the business case.

Stay at portfolio altitude. Evaluating one candidate tool before purchase (fit, integration burden, cost checklist) is a different, narrower job - here the unit of analysis is the whole stack and the review recurs; recommend, never execute the migrations.

## Ground Rules

- Anchor every verdict on business value, never on utilization alone. Low-frequency tools can cover critical edge cases; a 3-seat data-hygiene service protecting forecast integrity is not comparable to a 40-seat unused sequencer (Brinker's explicit caveat - see [references/benchmarks-and-figure-grading.md](references/benchmarks-and-figure-grading.md)).
- Target redundancy, not raw tool count. The goal is stopping duplicate spend on the same function, not hitting a smaller number (Lauren Nickels, Blackline).
- Treat shadow IT as evidence of unmet need before treating it as waste: self-selected tools measure higher engagement than IT-issued ones (Productiv: 54% vs 40%). A cut list that equates "bought outside procurement" with "cut candidate" argues against its own usage data.
- Never present suite-vs-point-solution as settled. Suite preference is rising, but best-of-breed utilization sits at parity (Gartner: 57% suite vs 59% point) - and full consolidation transfers pricing power to the suite vendor. Every consolidation verdict must name the alternative vendor kept under evaluation to preserve negotiating leverage.
- The renewal calendar is the binding constraint. A correct verdict landing after the notice window closes is a wasted verdict; time every action to a window.
- "Do nothing" is a valid verdict for a low-utilization flag - e.g. secondary users meant to touch a tool rarely. Enablement is the most underused remedy for genuine underutilization; cutting is not the only response.
- Name the source and edition behind every cited figure. Never cite the circulating unsourced statistics - "70% of CRM implementations fail", "the average B2B team uses tools from 23 vendors", or any hyper-specific number with no locatable original source. The blocklist and the sourced replacements live in [references/benchmarks-and-figure-grading.md](references/benchmarks-and-figure-grading.md).
- Rankings below are defaults, not laws. Re-rank against the user's known context - an in-house engineering team, a SaaS-management platform already deployed, a board deadline - and say which answer moved which option.

## B2B and B2C / E-commerce

- **B2B sales-led:** the stack centers on the CRM as system of record (42% of B2B orgs name it the stack center - MarTech.org/MartechTribe). Sales-engagement, conversation-intelligence, enrichment, and forecast tooling are all in scope alongside martech.
- **B2C / e-commerce:** martech-heavy, with no SDR/sales-engagement layer at all. The stack likely centers on the data/warehouse or engagement layer rather than a CRM - state this as a reasonable inference, not a benchmarked finding, whenever it appears in output. Duplicates cluster in analytics, attribution, and messaging categories.
- Warn B2C readers that this domain's published benchmarks are B2B-SaaS-centric - flag it rather than implying parity.
- **Identical in both, apply without modification:** the four-channel inventory union, the renewal-triggered cadence, the value-over-utilization rule, TIME scoring itself, and the intake gate.

## Interview

Ask before proposing anything. One question per message; multiple-choice where possible; skip anything already answered.

- What triggered this review: cost pressure, a board efficiency push, a merger/acquisition, new leadership, a renewal-price shock, or a routine cycle?
- Scope: the full GTM stack, or one function's slice (marketing, sales, CS/post-sale)?
- Motion: B2B sales-led, PLG/hybrid, or B2C/e-commerce?
- Scale and stage: is RevOps one person wearing every hat, or is there formal IT, procurement, and FinOps? (This sizes the review's rigor - see Ground Rules on re-ranking.)
- Who holds the final call on stack decisions - RevOps, shared with IT, a finance gate? Is the FinOps/IT/procurement split defined at all? (Only ~31% of orgs have a clear one - Zylo 2026.)
- Can SaaS cost be allocated per business unit today? (Without allocation, chargeback-style governance is off the table - don't design for it.)
- Which inventory sources exist: a contract repository, AP/expense exports, SSO logs, network/CASB telemetry, a SaaS-management platform?
- Does a renewal calendar with notice windows exist, or must this review build one?
- What usage evidence is available: feature-depth telemetry, per-vendor admin reports, or nothing beyond login counts?
- By what date must decisions land - a budget cycle, a board date, no fixed date? (A hard date promotes tools with imminent notice windows to the front and deletes long migrations from this cycle.)
- One-off savings, or a compounding operating model? (One-off promotes downgrades and cuts; compounding promotes the intake gate, renewal-triggered cadence, and governance.)
- Effort ceiling: analyst hours only, admin/IT capacity, engineering capacity, or a cross-functional mandate? (Analyst-only deletes consolidation migrations and internal build from the register; a mandate is what makes consolidation rankable at all.)

## Brainstorming the Review Design

Enter explicit brainstorming after the Interview, before any inventory or scoring work. Do not jump to a deliverable.

1. Map the workflows first, tools second: list the revenue workflows the stack must serve (capture, routing, qualification, deal management, quote/sign, billing, onboarding, renewal, expansion - trimmed to the user's motion). A tool serving no workflow on the map is already a finding.
2. Propose 2-3 candidate review designs with trade-offs. Efficiency, measured as decisions produced per review hour: one-time portfolio sweep with renewal overlay > renewal-window rolling review > practice-level benchmark first.
   - **One-time portfolio sweep with renewal overlay** - full scoring pass now, every action queued to its window; fastest complete picture, some verdicts wait months for a lever.
   - **Renewal-window rolling review** - verdicts produced as each notice window approaches; lowest wasted work, slowest full-portfolio picture.
   - **Practice-level benchmark first** - score how the stack is run (Do More / Do Less / Start / Stop, Frans Riemersma's instrument) before scoring tools; answers a different question than the other two, which is why it ranks last on tool decisions.
3. Recommend one design and say which Interview answer drove it. Default to the sweep with overlay for a first cycle; promote the rolling review once a full renewal calendar exists and the mandate is standing rather than one-off. The order starves the practice-level benchmark - promote it to first when the mandate covers how the stack is run, not only what it costs.
4. Validate the deliverable plan section by section (inventory → calendar → overlap map → verdicts → governance) and get approval before building anything.

## Workflow

1. Run the Interview; fix scope, motion, decision rights, and the three efficiency answers (deadline, one-off vs compounding, effort ceiling).
2. Run Brainstorming the Review Design; get the design approved.
3. Build the inventory (see Inventory below); flag every shadow-discovered tool and run the dedicated AI-tool discovery pass.
4. Build or verify the renewal calendar - renewal date, notice window, auto-renew flag, action deadline per tool. Method and worked example in [references/renewal-calendar-audit-example.md](references/renewal-calendar-audit-example.md).
5. Map functional overlap at the function level, never the vendor level; tag each tool system-of-record vs system-of-engagement - tools that write to the record system are held to a stricter standard than tools that only read.
6. Gather usage evidence per the Usage Evidence ranking - as a diagnostic input, never as the verdict.
7. Score every tool with TIME (Tolerate / Invest / Migrate / Eliminate - Gartner); overlay the renewal calendar on every verdict. Worked pass in [references/time-scoring-worked-example.md](references/time-scoring-worked-example.md). TIME's known blind spot is exactly SaaS contract timing, which is why the overlay is mandatory.
8. At any category served by a thin, commoditized, or integration-hostile point solution, run a buy-vs-build checkpoint: internal GTM-engineering build capacity is re-entering this calculation (GTM-engineering postings grew ~205% YoY - Bloomberry; Brinker calls the custom-app long tail the "hypertail"). State the trend; never invent a capability threshold.
9. Build the verdict register ranked by the Verdict Execution Order below, re-ranked against the Interview's deadline, one-off-vs-compounding, and effort-ceiling answers. Delete an option the constraints rule out and say which constraint deleted it - never park it at the bottom.
10. Run the consolidation risk pass: a named risk owner per failure mode in the table below, and a preserved-alternative vendor per consolidation verdict.
11. Attach governance: intake gate (required fields: business justification, intended users, data types, expected duration; automated duplicate-check against the tool registry; 3-5 business day approval SLA - a slow gate creates the shadow IT it exists to prevent) and renewal-to-recertification linkage (recertify access, ownership, and need before each auto-renewal fires).
12. Emit the deliverable one section at a time for user validation, per the approved design.
13. Store the verdict register, renewal calendar, and governance decisions in persistent memory when the harness offers it, so the next cycle starts from them; otherwise put all three in the report's final section for the user to carry forward.

## Inventory

The working inventory is the union of four discovery channels - each one alone undercounts.

- Value (tools surfaced that no other channel sees): network/CASB telemetry > AP/expense export > SSO logs > contract repository - the repository, by construction, only holds what already cleared procurement.
- Efficiency: AP/expense export > contract repository > SSO logs > network/CASB telemetry.
- Effort: contract repository == AP/expense export (finance already holds both) < SSO log pull < network telemetry.
- Default rung: run the first three; the order starves network telemetry - the only channel that sees unsanctioned AI tools, the largest blind spot in most stacks (60% of IT leaders lack visibility into generative-AI tools in use; 77% found AI running without IT's awareness - Zylo 2026). Promote it whenever AI shadow usage is suspected or at enterprise scale.
- Interview finance about expense-channel purchases specifically: expense-based SaaS buying is growing fast while fewer people do it - the buyers to interview are concentrated, not spread thin.

## Usage Evidence

Usage is a diagnostic input to the value conversation, never the cutoff itself.

- Value as cut evidence: feature-depth telemetry > proxy signals (records written per user, API call volume, workflows terminating in the tool) > login counts.
- Effort: login counts (near-zero) < proxy signals (hours per tool) < feature-depth telemetry (needs a management platform or per-vendor admin work).
- Efficiency: proxy signals > login counts > feature-depth telemetry.
- Default rung: screen with login counts, decide with proxy signals. The order starves feature-depth telemetry - the only tier that catches a nightly automated sync masquerading as adoption; promote it when a SaaS-management platform is already deployed, or whenever a high-spend verdict hangs on usage.
- No tier justifies a cut alone: every usage-based flag still needs the per-tool business-value check from Ground Rules.

## Scoring

- Efficiency: function-overlap map > TIME scoring > practice-level benchmark.
- These answer different questions:
  - Overlap map: "where are the duplicates"
  - TIME scoring: "what do we do with each tool"
  - Practice-level benchmark: "are we running the stack well"
- Default: overlap map plus TIME. Add the practice-level benchmark when the mandate covers process maturity, not only spend.
- TIME's track record is real (Gartner documents a US Air Force application across a mission IT portfolio, with governance and a dry run) - cite it as the credible named framework, and always pair it with the renewal overlay it lacks.

## Verdict Execution Order

- Value (spend plus integration surface removed): platform consolidation > duplicate elimination > point-for-point replacement == seat/tier downgrade.
- Effort: seat/tier downgrade < duplicate elimination < point-for-point replacement < platform consolidation < internal build (a standing engineering commitment, not a project).
- Efficiency: seat/tier downgrade > duplicate elimination > point-for-point replacement > platform consolidation > internal build.
- The == tie: a replacement swaps like for like and a downgrade trims spend only - both leave the stack's shape and integration surface intact, which is what the value axis measures.
- Default rung: first cycle executes downgrades and duplicate eliminations, timed to notice windows. The order starves platform consolidation - the highest long-run value option loses every efficiency round; promote it when integration failures are a measured defect source, an alternative vendor stays live, and the suite capability being consolidated onto ships today. A consolidation premised on the suite's AI roadmap is a bet on a roadmap, not a purchase (Gartner, mid-2025, n=413 martech leaders: 45% of those running AI agents say vendor agent capabilities miss promised performance).
- Internal build enters only through the buy-vs-build checkpoint in the Workflow, and only where engineering capacity exists.

## Cadence

- Value: renewal-triggered per-tool review > annual portfolio synthesis > fixed calendar sweep.
- Effort: fixed calendar sweep (one block of hours) < annual synthesis < renewal-triggered review (a standing trigger per contract, not a project).
- Renewal-triggered wins mechanically: the average org manages ~211 SaaS renewals a year and renewals carry ~87% of software spend (Zylo 2026) - a calendar review landing after a notice window closes produces analysis with no lever attached.
- Default rung: renewal-triggered per tool, plus one annual portfolio synthesis, since per-renewal reviews never show portfolio-level patterns (category creep, spend-per-workflow drift). The order starves that synthesis - every individual renewal feels more urgent than it does - so protect it with a fixed date. Delete the fixed calendar sweep once every contract has a window; it survives only as the bridge used while the calendar is still being built.
- Name an accountable owner per tool - decentralized committee buying means no one's job is on the line for a bad purchase (Jeremey Donovan).

## Output Shape

```
STACK RATIONALIZATION REVIEW - <scope>, <date>
Workflow map      : revenue workflows served; tools mapped to each; orphan tools flagged
Inventory         : tool | function | owner | annual cost | seats | discovery channel | shadow flag
Renewal calendar  : tool | renewal date | notice window | auto-renew | action deadline
Overlap map       : function-level duplicates; system-of-record vs system-of-engagement tags
Verdict register  : rank | tool | TIME verdict | value evidence | usage (diagnostic) |
                    action + window | risk owner
                    (ranking basis and any deleted option stated above the register)
Consolidation risk: named owner per failure mode; preserved alternative per consolidation
Governance        : intake gate fields + SLA; renewal-recertification link; re-sprawl metric
Next cycle        : upcoming notice windows; re-review triggers; decisions stored/carried
```

## Pass Threshold

- Every in-scope tool carries an owner, a function, a TIME verdict, and a renewal date with notice window; unknowns are marked "unconfirmed", never left blank.
- No Eliminate or downgrade verdict rests on utilization alone; each carries a one-line business-value justification.
- Every consolidation verdict names the preserved alternative vendor and a risk owner per failure mode.
- Every verdict has an action deadline inside a live notice window, or is explicitly queued to the next one.

Iterate until all four hold. A verdict queued to a future window with a date attached is a passing outcome; a verdict with no window is not.

## Common Failure Modes

| Defect                                      | Consequence                                                                                                                                                                                                                                                                                                 | Fix                                                                                                                                                                            |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Cutting by utilization percentage alone     | Kills low-seat tools covering critical edge cases                                                                                                                                                                                                                                                           | Business-value check per tool; "do nothing" and enablement stay on the verdict menu                                                                                            |
| Renewal-window blindness                    | Auto-renew locks in another term at a higher rate                                                                                                                                                                                                                                                           | Action deadline = notice-window open, on every verdict; start negotiations well before the window                                                                              |
| Full consolidation with no live alternative | Pricing power transfers to the suite vendor permanently                                                                                                                                                                                                                                                     | Name and keep evaluating an alternative per consolidation verdict                                                                                                              |
| Adoption collapse post-consolidation        | The project fails on behavior, not data (the direction is consistent across sources; the circulating failure percentages are unverifiable)                                                                                                                                                                  | Adoption owner, enablement plan, and champion transition named before migration                                                                                                |
| Feature-parity gap surfaces post-migration  | An undocumented workflow breaks after cutover                                                                                                                                                                                                                                                               | Workflow-level parity walkthrough with the tool's heaviest users before the verdict finalizes                                                                                  |
| Reporting discontinuity                     | Year-over-year comparison breaks while leadership scrutinizes the project's own ROI                                                                                                                                                                                                                         | Migrate the measurement model with the records; see mbfinotti/revops-skills@revenue-reporting                                                                                  |
| Champion loss                               | The person who made the cut tool work leaves the workflow orphaned                                                                                                                                                                                                                                          | Name a transition owner for every Eliminate/Migrate verdict                                                                                                                    |
| Re-sprawl between cycles                    | The next review starts from scratch                                                                                                                                                                                                                                                                         | Intake gate with automated duplicate-check + renewal-recertification link, installed as part of this deliverable                                                               |
| Single-platform mandate over-reaches        | Mandating everything live inside one suite and ripping out specialized tools reads clean on paper; when a capability like conversation intelligence or forecasting quality visibly drops, reps route around the mandate and rebuild a shadow stack, so the org pays for the suite and the shadow stack both | Scope the mandate to what the suite genuinely covers at parity; keep a named specialized tool where the suite's version is materially worse                                    |
| Logic and platform change on the same day   | Changing scoring or routing logic at the same moment as the platform migration forces reps to relearn judgment while learning a new tool, and adoption rarely survives both at once                                                                                                                         | Freeze process logic during the cutover window; if the schema looks the same after migration, the org changed tools, not operations - change logic separately, before or after |

## KPIs

- Track per cycle: spend per workflow served (trend), redundant-function count (trend), share of renewals reviewed before their notice window opened (target near-100%), and net new tools entering outside the intake gate (re-sprawl rate, target near-zero).
- Honesty checks: realized savings vs the register's projections, and surviving-tool adoption after each consolidation - if adoption drops, the consolidation failed regardless of the spend line.
- Never report "tools cut" as the success metric - it rewards cutting count instead of redundancy, the exact inversion of the goal.

## Invocation Examples

- "We're at something like 40 GTM tools and finance wants a rationalization plan before budget season."
- "Our CRO thinks half the sales stack overlaps - run a stack review and tell us what to consolidate or cut."
- "Renewals keep auto-firing before anyone looks at the tool - set up a stack review that runs on the renewal calendar."

## Reference

- Read [references/benchmarks-and-figure-grading.md](references/benchmarks-and-figure-grading.md) before citing any figure - the sourced benchmark set with editions, the ranked source list, and the fabricated-statistic blocklist.
- Read [references/time-scoring-worked-example.md](references/time-scoring-worked-example.md) when scoring - a worked TIME pass over a sample GTM stack, with the renewal overlay and a negative example (a utilization-only cut done wrong).
- Read [references/renewal-calendar-audit-example.md](references/renewal-calendar-audit-example.md) when building the calendar - schema, action-deadline arithmetic, worked mini-calendar, and the wasted-verdict failure case.
- See `mbfinotti/revops-skills@crm-data-governance` for field ownership and source-of-truth policy inside the systems this review keeps.
- See `mbfinotti/revops-skills@revenue-data-governance-strategy` for the cross-system ownership map that any consolidation redraw must respect.
- See `mbfinotti/revops-skills@revenue-leakage` when records or dollars vanish in one funnel - a leak traced to a tool defect feeds this review; this review does not trace leaks.
