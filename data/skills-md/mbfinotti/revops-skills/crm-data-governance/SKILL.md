---
name: crm-data-governance
description: Design and operate CRM field-level governance - who owns each CRM field, which system is authoritative for it, how often it must be refreshed, and how the rules are enforced. Produces a field dictionary, per-field ownership, a system-of-record map with write-precedence and conflict rules, freshness SLAs, an enforcement plan, a field lifecycle, and a governance cadence. Use whenever the user mentions field ownership, single source of truth, system of record per field, data dictionary, stale CRM data, custom field sprawl, "which system wins", or "our CRM fields contradict each other" - even if they never say "governance". Covers B2B and B2C. Do NOT use for org-wide, object-level source-of-truth policy - use mbfinotti/revops-skills@revenue-data-governance-strategy instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.1"
---

# CRM Data Governance

Build and run field-level governance for a CRM. The deliverable is a living rulebook plus a meeting rhythm - "governance dies from lack of a meeting, not lack of a document" (ORM Tech) - built from:

- A governed-field catalog with one named owner per field.
- A per-field system-of-record map with write-precedence and conflict rules.
- Refresh and staleness SLAs.
- An enforcement plan ranked by value per unit of effort.
- A field request-approval-deprecation lifecycle.
- The recurring cadence that keeps all of it alive.

## Ground Rules

- Govern revenue-critical fields, not every field - this is the first scoping decision. A CRM carries hundreds of fields; governing all of them is impossible and counterproductive (practitioner consensus). Start from the sourced field lists in [references/field-ownership-and-dictionary.md](references/field-ownership-and-dictionary.md) and expand only through intake.
- One named human owner per field - "Not a team. A person." (RevBlack). Assign each field to the function that consumes it, not the one that populates it.
- Designate the system of record per field, never per system or object. Every other copy is explicitly derived. Blank never overwrites populated, whatever the timestamps say.
- Reps are never the enforcement mechanism of last resort. "Sales reps cannot be responsible for data entry... their compensation, goals, and psychological incentives all push them toward selling, not data stewardship" (Jared Barol). Prefer automation, integration writes, enrichment, and defaults over required-field pressure.
- Design and operate a standing system. A cleanup without an ownership map, a lifecycle, and a scheduled cadence is not governance; decay resumes the day the cleanup ends.
- Label every threshold with its provenance: published company practice, practitioner consensus, or derived from the user's own data. Warn off the circulating statistics - "30% of CRM data decays per year" and "CRM data is only 40-60% accurate" circulate unattributed and must never be stated as fact. Cite the mechanism instead: reality changes underneath stored values (people change jobs, companies grow and rename), and multi-writer syncs without per-field authority silently overwrite each other. Never present a vendor-coined proprietary composite score as an industry standard.
- Scope boundary: record deduplication and merge mechanics are out of scope here. Recurring hygiene sweeps, stage exit criteria, forecast reliability, and routing logic belong to the sibling skills in Reference - this skill writes the field rules those jobs consume.

## B2B and B2C

**Divergent:**

- **B2B** runs on sparse, slow data: long cycles, account hierarchies, buying committees, and a rep-entry layer to treat as unreliable by default ("you should never assume that someone within your sales team is going to help you in adding data" - Stefano Mazzalai). Governance coordinates several functions writing to one account.
- **B2C** runs on high-volume, real-time behavioral data written by systems with no rep layer. Consent/preference fields and retention schedules become first-class governed fields (consent policy owned by marketing, sync reliability by platform ops; consent logic stays centralized even when page creative is federated).
- **Identity resolution** has no B2B equivalent for B2C's cross-channel matching (deterministic exact-identifier vs probabilistic). B2B resolves identity at the account level via domain matching instead.

**Identical across both:** per-field system-of-record designation, blank-never-overwrites-populated, enrichment risk tiering, and last-verified-as-distinct-from-last-modified. That equivalence is reasoned synthesis from generically-phrased sources, not a published claim - say so in the deliverable.

## Interview

Ask before designing anything. One question per message; multiple-choice where possible; skip anything already answered.

- Which CRM, and which other systems write to it: marketing automation, billing, product database, enrichment providers, support desk, data warehouse?
- Can you export (or let me query) the field list for the objects in scope? Roughly how many custom fields per core object?
- Which fields feed forecasting, routing, compensation, or executive reporting today? (This seeds the governed set.)
- Symptoms driving this: fields contradicting across systems, values mysteriously reverting, stale data, field sprawl, nobody knows who owns what?
- Who does data operations today: dedicated RevOps, a CRM admin, IT, nobody?
- Does any field documentation or dictionary exist, and where does it live?
- Which enrichment providers write into the CRM, and into which fields?
- B2B, B2C, or both? Any consent/data-protection obligations in scope?
- Is there an existing governance forum? Who approves new fields right now?
- Typical sales cycle length and record volumes? (Calibrates SLAs and thresholds.)
- By what date must this be in place - an audit, a board reporting cycle, a CRM migration, or a forecast nobody trusts right now?
- Do you want a one-off correction of the fields that are wrong today, or a compounding governance system that keeps holding as fields are added?
- What is the effort ceiling: admin hours this quarter, any integration engineering capacity at all, and how much friction the sales org will absorb before it routes around you?

The last three set the option ordering in Workflow steps 4 and 6, so ask them before designing anything:

- **A hard date** promotes the config-only rungs (restricted picklists, defaults, scheduled pull, augment-only enrichment) and schedules conditional validation and real-time push for the next cycle rather than dropping them.
- **A compounding mandate** promotes per-role permissions, conditional required-at-stage, and the lifecycle and cadence themselves, and demotes default values, which patch a symptom without creating a rule.
- **No integration engineering capacity** deletes real-time push outright.
- **A sales org already hostile to required fields** deletes hard required for rep-entered fields.

Record every deletion in the spec - a ruled-out option parked at the bottom of a list reappears as scope at the next escalation.

## Workflow

1. Run the Interview; confirm the scope boundary (field rules - not dedup, not hygiene sweeps, not stage design).
2. Scope the governed set: start from the revenue-critical lists in [references/field-ownership-and-dictionary.md](references/field-ownership-and-dictionary.md), add every field feeding forecasting/routing/comp/reporting, and cap it deliberately.
3. Assign ownership per field: consumer-ownership principle, one named person, RACI-by-function as the default split (same reference).
4. Build the per-field system-of-record map: authoritative system, write precedence, replication pattern, enrichment write strategy with risk tier, and conflict-resolution tier for each governed field - [references/system-of-record-rules.md](references/system-of-record-rules.md). Two ranked choices sit inside this step, and both are made here rather than in the reference:

   - replication, efficiency: `scheduled pull > reconciliation-only > real-time push`. Default every governed field to scheduled pull on the cadence its freshness SLA demands; move a field up to real-time push only when one stale sync cycle changes an action rather than a report. Real-time push is what this order starves - best freshness, worst ratio - so name it in the spec when demoting it, and flip the order where an event bus or iPaaS is already running and the marginal field costs nothing.
   - enrichment, efficiency: `augment > append > overwrite`. Default the whole governed set to augment; move to overwrite only where the provider is definitionally authoritative and the stored value carries no verification stamp. Overwrite is starved here for the same reason, and it is the only mode that can correct a value that is already wrong.

   The reference carries the value, effort and compliance-cost axes behind both orders, the ties, and the constraints that delete an option instead of demoting it. Re-rank both against what the Interview established about this team before writing the map.

5. Set refresh SLAs per field category and design last-verified tracking with trigger-based re-verification - [references/freshness-slas.md](references/freshness-slas.md). Tag each SLA's provenance.
6. Pick enforcement per field from [references/enforcement-menu.md](references/enforcement-menu.md), ranked by value per unit of effort rather than by how light it is:

   - efficiency: `picklist > conditional-required > defaults > permissions > layout > hard-required`. Default to restricted picklists plus defaults in the first pass; climb to conditional required-at-stage for any field a decision reads at a known transition.
   - Per-role permissions and hard required are what this order starves: both carry real value the cheap rungs cannot buy, and both lose every efficiency round. Promote permissions the moment a governed field has two writers ignoring its system-of-record designation, and hard required only where a record without the value is undecidable.
   - Never default to hard-required - a program that only ever picks the cheap rung ends up with a dictionary full of fields nobody trusts.

7. Stand up the lifecycle and cadence: intake question set, approval/rejection criteria, deprecation process, council membership, meeting rhythm, decision rights - [references/field-lifecycle.md](references/field-lifecycle.md).
8. Compile the dictionary using the working-default column set (ownership reference). When the live CRM is directly queryable, generate initial rows from its metadata; otherwise build from the user's export and mark unverified rows as such.
9. Emit the deliverable (Output Shape) one section at a time for user validation, grounded in the matching example from [references/worked-examples.md](references/worked-examples.md).
10. Check the Pass Threshold; iterate until it holds. If your harness has persistent memory, store the governed-field list, ownership map, and system-of-record decisions so cadence reviews and dispute resolutions start from them; otherwise the dictionary itself is the durable artifact - tell the user to treat it that way.

## Output Shape

Every threshold line carries a provenance tag.

```
CRM FIELD GOVERNANCE SPEC - <company>, <date>
Scope            : objects in scope; governed-field count vs total field count;
                   motion (B2B / B2C / both); options deleted by the user's
                   constraints, and which constraint deleted each
Ownership map    : field -> named owner (a person) + owning function
System of record : field -> authoritative system, write precedence, replication
                   pattern, enrichment strategy + risk tier, conflict rule
Freshness SLAs   : field/category -> refresh cadence, re-verification triggers,
                   last-verified tracking plan
Enforcement      : field -> mechanism + why it beat the rung below it +
                   rollout note
Dictionary       : column set, initial rows, dictionary-vs-live-CRM
                   reconciliation plan
Lifecycle        : intake form, approval/rejection criteria, deprecation
                   process, utilization-review threshold
Cadence          : council membership, weekly/monthly/quarterly rhythm,
                   decision rights, escalation path
Metrics          : baseline values captured, KPI targets, first review date
```

## Pass Threshold

- Every governed field has:
  - One named individual owner (never a team name).
  - Exactly one system of record.
  - A declared write-precedence and conflict rule for every sync touching it.
  - A refresh SLA, or an explicit event-driven designation.
  - At least one enforcement mechanism.
  - A dictionary row.
- No governed field has two writers without a declared winner, and enrichment never auto-applies to identity or downstream-trigger fields.
- Dictionary spot-check: sample 10-15 governed fields against the live CRM (type, picklist values, required-ness, description present) - at least 95% agreement, a working bar to tighten from the user's own drift data, not a published standard.
- The cadence exists on a calendar with named attendees and documented decision rights - a policy document alone fails this threshold by definition.

Iterate until all four hold. If live-CRM verification is impossible in this run, mark the spot-check pending and schedule it as the first council agenda item.

## Common Failure Modes

| Defect                                        | Consequence                                                         | Fix                                                                                                          |
| --------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Field owned by a team ("RevOps owns it")      | Everyone-owns-nothing; issues ignored or multiply across systems    | One named person per field, name visible in the dictionary                                                   |
| Governing every field                         | Effort diluted; governance abandoned as unworkable                  | Govern the revenue-critical set; expand only via intake                                                      |
| Make-it-required reflex                       | "n/a" and junk entries pass the gate; adoption collapses            | Work the efficiency order: picklists and defaults first, conditional validation before hard-required         |
| Enrichment clobbering verified values         | Trusted data silently destroyed                                     | Augment/append by default; overwrite only where enrichment is the designated authority; risk-tier all writes |
| Bidirectional sync, no per-field authority    | Flapping values, silent overwrites, "the data is wrong" escalations | Per-field system of record plus last-synced conflict detection                                               |
| One-time cleanup mistaken for governance      | Decay resumes immediately                                           | Lifecycle + cadence; cleanup is an output of the system, not the system                                      |
| Council that never meets                      | Policy rots; requests bypass intake                                 | Scheduled weekly triage with decision rights; the meeting is the mechanism                                   |
| Governance assigned to IT                     | Business stops trusting definitions                                 | RevOps owns it; stewardship is a business role                                                               |
| Orphaned one-off fields                       | Sprawl, duplicate fields, tribal knowledge                          | Intake with duplicate check; utilization review; deprecation queue                                           |
| Success measured as "reps filled more fields" | Fill rate up, accuracy down                                         | Measure conflict rate, staleness, and verified coverage instead                                              |

## KPIs

- Track:
  - Field fill rate on governed fields, not all fields.
  - Field utilization: consumed in reports/automation, not merely populated.
  - Staleness distribution: time since last verified, per field.
  - Cross-system conflict rate per sync run.
  - Validation-failure rate. A spike means friction - check for junk-value workarounds before celebrating enforcement.
  - Time-to-approve a field request. Practitioner target: under one week from request to published.
  - Custom-field count trend, which should flatten once intake stands up.
- Never report "reps filled more fields" as success - fill rises while accuracy falls when gates force garbage entries.
- Re-run the dictionary spot-check quarterly; rising drift means the reconciliation loop is broken.

## Invocation Examples

- "Our CRM says one employee count, billing says another, and marketing automation a third. Decide which system wins, field by field."
- "Anyone can add a custom field and we're at 400 on the account object. Set up a field request process and an ownership model."
- "Build a data dictionary and refresh SLAs for the fields our forecast depends on - half are stale and nobody owns them."

## Reference

- Read [references/field-ownership-and-dictionary.md](references/field-ownership-and-dictionary.md) when scoping the governed set, assigning owners, or building the dictionary - ownership models, revenue-critical field lists, working-default column set, drift control.
- Read [references/system-of-record-rules.md](references/system-of-record-rules.md) when mapping authority across systems - per-field designation, write precedence, the ranked replication and enrichment menus with their value/effort/compliance axes, enrichment risk tiers, flapping detection.
- Read [references/freshness-slas.md](references/freshness-slas.md) when setting refresh cadences - the sourced cadence table, last-verified vs last-modified, re-verification triggers.
- Read [references/enforcement-menu.md](references/enforcement-menu.md) when choosing enforcement - the six mechanisms ranked on efficiency, value, effort and compliance cost, picklist governance, when required backfires, optional vendor note.
- Read [references/field-lifecycle.md](references/field-lifecycle.md) when standing up intake, deprecation, and the council - question sets, approval criteria, cadence, decision rights.
- Read [references/worked-examples.md](references/worked-examples.md) when shaping the deliverable - a five-field governance spec done right and one done wrong.
- See `mbfinotti/revops-skills@sales-pipeline-hygiene` for recurring stale-deal sweeps and completeness audits - it enforces weekly what this skill defines once.
- See `mbfinotti/revops-skills@pipeline-stage-definition-audit` for stage exit criteria design - stage fields appear here only as governed picklists.
- See `mbfinotti/revops-skills@sales-forecast-diagnostic` for forecast reliability built on top of governed fields.
- See `mbfinotti/revops-skills@lead-routing` for the routing logic that consumes governed routing fields.
- See `mbfinotti/revops-skills@revenue-data-governance-strategy` for company-level data governance and cross-team data contracts - this skill stays at the CRM field level.
