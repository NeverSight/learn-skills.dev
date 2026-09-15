---
name: lookalike-audience-seeds
description: "Select and size the seed customer list behind a lookalike, similar, or value-based audience - which customers to upload, how many, and whether the matched count (not the row count) clears the platform floor - with RFM and value-based selection, a negative-selection pass, a privacy and consent gate before any customer list upload, and a fallback ladder when the floor cannot be cleared. Use whenever the user mentions a lookalike or similar audience, a seed list, a customer list upload, match rate, an audience that is too small, or says their lookalike isn't working - even if they never say 'seed'. Covers B2B and B2C. Do NOT use to design the whole targeting tier structure - use mbfinotti/advertising-skills@ad-audience-targeting instead."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.6"
---

# Lookalike Seeds

Select, size, and validate the seed customer list that a lookalike, similar, or value-based audience will be built from. Three principles govern every step below:

- **Match count, not row count** - every uploaded list shrinks by its match rate before it reaches the platform's minimum. A 40% match on 5,000 rows is a 2,000-person seed, and the platform floor applies to that matched number - upload 2-3x the target.
- **Homogeneity and value concentration beat size** - Meta's own guidance holds that a seed's homogeneity affects audience effectiveness more than its size. Practitioner consensus (Stackmatix, Grow With Sakib - directional, not audited) is that a few hundred high-value customers outperform thousands of undifferentiated subscribers.
- **Inclusion is a suggestion, exclusion is a rule** - on Meta (Advantage+) and Google (Demand Gen, where lookalike reach tiers now function as signals rather than hard segments), the delivery algorithm may override an inclusion audience. Only exclusion/suppression audiences remain hard rules.

The seed's job is feeding the algorithm the cleanest signal, not fencing an audience - which raises the quality bar rather than removing it.

This skill ends at a specified, validated seed definition plus its export/handoff spec. It never walks through creating or uploading the audience inside any ad platform's interface.

Where each adjacent concern lives:

- Overall targeting plan (interest, behavioural, lookalike, and retargeting tier layering) - seed mechanics live here, tier architecture lives in `mbfinotti/advertising-skills@ad-audience-targeting`.
- Retargeting sequence design, audience windows per funnel stage, and frequency caps - `mbfinotti/advertising-skills@retargeting-funnel`.
- B2B buying-committee and persona mapping - `mbfinotti/advertising-skills@ad-buyer-group-mapper`.
- Root-causing broad account underperformance - `mbfinotti/advertising-skills@ad-account-diagnostic`.
- Pixel/CAPI instrumentation feeding engagement-based seed sources - `mbfinotti/advertising-skills@ad-conversion-tracking`.
- Reconciling conflicting performance reads on a seed across attribution sources - `mbfinotti/advertising-skills@ad-attribution-gap`.

## Interview

Ask before selecting anything. One question per message; offer multiple-choice answers where possible; skip anything already answered or visible in supplied data.

- B2B, B2C/ecommerce, or both?
- Which platform(s) will consume the seed? (Meta / Google / LinkedIn / TikTok / other - floors and match mechanics differ)
- What customer data exists, and where does it live? (CRM / data warehouse / email platform / pixel-and-platform events only / almost none)
- Roughly how many total customers, and which identifiers exist per row? (email / phone / name / postal address / mobile ad ID - more identifier types per row lift match rate)
- Is there a usable value column - and what does it actually measure: cumulative lifetime revenue, margin, predicted LTV, or just order count? Provenance matters more than presence.
- How recent is the data - what share of the list purchased or converted within the last 90 and 180 days?
- Does the list contain EEA/UK residents or US state-privacy-covered consumers? Is there a documented consent or lawful basis for ad-platform upload, and are opt-outs, deletions, and do-not-contact records enforced before export?
- How will the list reach the platform - manual CSV or automated warehouse/CDP sync? Who owns the refresh?
- What acquisition outcome is the lookalike meant to drive - target new-customer CPA/CAC, and any LTV or margin expectation for acquired customers?
- What does the account currently average on those same two numbers - acquired-customer CPA, and acquired-customer cohort LTV at 90 days? The pass threshold grades the seed against this baseline, so an unknown baseline means the seed cannot be graded at all: say so and set the first cohort checkpoint as the baseline-building run.
- By what date must the audience be live and spending, and is that date hard? (Seed sources span minutes to a week of coordination, and the enrichment rung runs through procurement - the orderings in steps 3 and 6 cannot be picked without this.)
- Do you want the audience that can launch soonest, or a compounding asset - an automated warehouse sync, enriched identifiers, a reusable cohort definition - that keeps paying across every future audience?
- Effort ceiling: how many hours of data-team time are available, who owns the refresh afterwards, and can you actually get privacy sign-off and a vendor DPA? (A "no" deletes rungs rather than delaying them.)

## Workflow

Every ranking in this skill - steps 3, 6 and 9 here, and the ones in the references - is a default, not a law. Each assumes the common case: no enrichment vendor under contract, no in-house identity graph, no analyst free this week. Who executes it changes the ordering as much as what it is.

Re-rank first against the interview's deadline, durability, and effort-ceiling answers, naming which answer moved which rung:

- A hard near-term date promotes the platform-native engagement seeds.
- A compounding-asset mandate promotes the warehouse sync and the enrichment rung despite their setup.
- No route to privacy sign-off deletes every list-based rung outright.

Then re-rank against what this user actually owns - any of these collapses a rung's effort to near-zero and moves it up:

- A signed enrichment DPA.
- Identity resolution already built in the warehouse.
- An analyst who can write the cohort SQL today.
- A data team that owns the export job anyway.

1. Run the Interview; collect every answer before selecting a single row.
2. Run the privacy and consent gate - a hard stop, before any selection work. If any item below is unconfirmed, stop and say exactly what is missing. This skill is not legal advice: lawful basis varies by jurisdiction, so route open questions to the user's counsel.
   - Documented lawful basis or consent for uploading this list to an ad platform. Under GDPR, the Bavarian DPA position upheld by the Higher Administrative Court Munich (2018, Ref. 5 CS 18.1157) holds that customer-list custom audiences require prior consent, and hashing does not change that: SHA-256 output is pseudonymous, not anonymous, so consent obligations survive it.
   - For EEA use of Google Customer Match, consent signals passed per Consent Mode v2 with both ConsentStatus fields GRANTED (mandatory since March 2024).
   - CCPA/CPRA "sharing" opt-outs and Global Privacy Control signals (honored in twelve US states) propagated before export.
   - No seed built on sensitive categories: health, sexual orientation, religion, race, political affiliation, criminal history.
   - Platform customer-list terms accepted for the specific ad account (value-based audiences need a separate terms acceptance on Meta).
   - Suppression, opt-outs, and deletions enforced once, in the warehouse, before any sync - not per-platform afterwards.
3. Choose the seed source: purchase data first, always. If purchase data is too thin, pick among the eight sourced alternatives - but never down the value ranking alone, because effort and compliance cost both run backwards to it. The axes disagree, so read all four:
   - value: `purchasers > checkout/add-to-cart initiators > high-intent page viewers > lead-form submitters > email clickers > video viewers > page engagers > all visitors`
   - effort: `video viewers == page engagers == all visitors > high-intent page viewers == lead-form submitters > checkout initiators > email clickers > purchasers` - the platform-native engagement audiences build inside the ad account in minutes off a rule the pixel already fires, and skip the customer-list upload and its step-2 consent gate entirely. A purchaser or CRM seed needs a warehouse export, an identity-resolution join, and the full gate. Both ties are real equalities: the first three are one blanket rule over an event already firing, and the next two are that same single rule pointed at a named URL set or a named form - minutes either way, by the same person.
   - compliance cost: `purchasers == checkout initiators == email clickers > lead-form submitters > high-intent page viewers == video viewers == page engagers == all visitors` - anything reaching the platform as a customer list runs the full step-2 gate (lawful basis, Consent Mode v2 in the EEA, opt-out propagation, a separate terms acceptance for value-based audiences), while a platform-native engagement audience never leaves the ad account and triggers none of it. Both ties are exact rather than approximate: the three list-based sources run the identical gate item for item, and the four native ones run none of it - this gate has no partial version to separate them by. The axis can decide the pick on its own: where consent for upload is unconfirmed, every list-based rung is unavailable, not merely expensive.
   - efficiency: `purchasers > high-intent page viewers > lead-form submitters > checkout initiators > email clickers > video viewers (75%+) > page engagers > all visitors`. Purchasers lead **when the customer export already exists**, the common case - a large value gap for one query. Where it doesn't, high-intent page viewers and lead-form submitters are the best ratio on the board: near-zero setup, no upload, no new exposure, still top-half on value. Those two are ordered rather than tied - their setup is the same single rule, so the value axis breaks it - except in B2B lead gen, where the form submission _is_ the conversion and submitters move ahead. Never let effort pull the choice below them: past that point per-row quality falls off faster than effort does. Per-source breakdown and the conditions that move this order: [references/seed-selection.md](references/seed-selection.md).

   What this efficiency order starves is the customer-identity asset itself: the purchaser or CRM seed, and the identity enrichment that makes it usable (fallback rung 1). It tops the value axis and sits last on both effort and compliance cost, so wherever the export does not already exist it loses every round to a pixel rule that ships in minutes - and the account still has no export the next time it asks.

   Promote it against the ratio when:
   - The interview answered "compounding asset" rather than "live soonest".
   - The seed is B2B and the native match rate cannot reach any floor without enrichment.
   - This same account has now lost the round twice.

   Delete it instead - by name, out of the menu - where there is no route to privacy sign-off or no vendor DPA available. A list-based source with no lawful basis is not a slow option, it is not an option, and one left ranked at the bottom reappears as scope after the audience is already live.

   Use email clickers, never openers - Apple Mail Privacy Protection (2021) inflated opens into noise. In B2B, seed from closed-won CRM opportunities, not all-MQL exports. SQL-only beats all-MQL.

4. Select the rows. [references/seed-selection.md](references/seed-selection.md) has the full cohort definitions, window guidance, and exclusion list.
   - Default selection: RFM Champions + Loyal cohorts, or the top 10-25% by predicted LTV or margin - never by cumulative lifetime revenue, which tracks tenure, not worth.
   - Recency window: 30-90 days as the starting point, up to 180 for pixel/CAPI-tracked buyers. Contact data older than 12-18 months materially degrades both match rate and performance.
   - Negative-selection pass (most teams forget this): strip refunders, chargebacks, serial returners, discount-only buyers, employees, and wholesale accounts. Keep existing customers in the seed, but suppress them from the acquisition campaign at delivery level.
5. Compute the effective seed: `effective seed = uploaded rows x expected match rate`. Pull the expected match rate from the platform's documented range in [references/platform-floors.md](references/platform-floors.md), adjusted for the list's identifier density and age - for example:
   - Google Customer Match: 29-62% for most advertisers (per Google's own docs).
   - Meta: 50-80% on good lists.
   - LinkedIn: ~30-40% on work-email contact lists.
   - Reddit: ~2% native CSV.

   Compare the result to the platform's matched-count floor and size the upload at 2-3x the target. If your harness can read the customer export, compute the counts directly. Otherwise, emit the exact filter definitions (source table, filter conditions, recency bounds, value threshold) for the user's data team to run, and wait for the counts before proceeding.

6. If the effective seed cannot clear the floor, walk the fallback ladder - never by loosening selection quality first. Rung numbers are stable IDs used by the spec block and the worked examples; each rung carries its own value, effort, and compliance cost:
   - **Rung 1, enrich identifiers** - identity resolution appending personal emails/phones. Value: the only rung that adds matched people without changing what the model learns, and on a B2B work-email list against a consumer platform the only rung that reaches any floor at all from a ~5% native match. Effort: the outlier the ladder's numbering hides - vendor selection, security review, budget sign-off, then a match test, so a week or more of coordination before a single row moves. Compliance: a new processor in the chain - DPA, counsel sign-off, and a lawful-basis re-check covering enrichment and not just upload; the hardest rung to reverse once contracted.
   - **Rung 2, widen the recency window one notch** (90 to 180, 180 to 365). Value: moderate, paid for in signal freshness. Effort: near-zero - a query edit, minutes, fully reversible. Compliance: none new.
   - **Rung 3, stack an adjacent segment of the same homogeneity** - add Loyal to Champions, or a second product line's buyers if behaviour is genuinely similar. Value: moderate, and homogeneity is what's at risk. Effort: about an hour, plus the judgment call that is the actual work. Compliance: none new.
   - **Rung 4, switch to the next non-purchase seed source down the step-3 ranking.** Value: lowest - the only rung that changes what the model learns. Effort: about an hour if the event source is already instrumented. Compliance: **lower**, not higher - a platform-native source needs no upload and no consent gate.
     Efficiency by default: `rung 1 > rung 2 > rung 3 > rung 4`. Stop at the first rung that clears, and record it in the spec.

     One documented flip: `rung 2 > rung 1`, when no enrichment vendor is contracted **and** there is recency left to widen - an afternoon may end the problem before procurement starts, and rung 1 stays available if it doesn't. The flip does not apply on the standard B2B case, where the cheap rungs are structurally empty: an all-time closed-won list has no recency left, no adjacent segment that isn't lost deals, and a native match too low for rungs 2-4 to reach any floor.

     Rung 1 is also the rung to delete rather than demote. No procurement route, no DPA, or no owner for a vendor budget takes it off the ladder entirely - say it is deleted and run rungs 2-4. A rung nobody can execute, left sitting at the top of an efficiency order, is how the spec ends up assuming it.

     On the standard B2B case that leaves no ladder at all: report that as the finding instead of filling it with a looser seed.
7. If the seed is value-based:
   - Feed margin or predicted LTV.
   - Positive values only.
   - Values must not be all identical.
   - One currency per list.
   - Cap or winsorize whale outliers so a few large accounts don't skew the model.
   - Confirm the value column is mapped at upload. An unmapped value column makes the platform silently build a standard, not value-based, lookalike - if the value-based option doesn't appear at audience-build time, the column didn't map.
8. Specify identifier preparation:
   - Multiple identifiers per row beat email alone.
   - Phone in E.164-style digits with country code, no plus sign, no leading zero.
   - Emails lowercased and trimmed.
   - Never pre-hash a file destined for a UI upload - the platform hashes on ingest, and a salted or double hash will never match.

   On Meta, target an Event Match Quality score of 6.0+ as the practitioner benchmark.

9. Decide splits, refresh, and overlap.

   **Splits.** Split in this order - `country > product line > high-AOV vs. all` - and stop when the named refresh owner runs out of capacity. Effort per split is identical (one WHERE clause), but each adds a permanent one: an audience to refresh, monitor for overlap, and keep above its floor forever.

   Country is not a choice: Meta lookalikes are country-scoped by construction, so multi-country coverage needs one seed-and-lookalike pair per country. Check every split's own effective seed against the floor before committing to it.

   **Refresh.** Set the refresh cadence with a named owner. Static CSV uploads do not auto-refresh (LinkedIn lists, manual Meta customer lists), so schedule weekly-to-monthly refreshes or move to an automated warehouse sync.

   Between those two, `automated sync > manual CSV` on efficiency and on compliance cost, despite losing on effort. A week of engineering once retires the whole decay failure mode and propagates opt-outs and deletions continuously. The CSV is near-zero to start but becomes a standing job forever, re-uploading yesterday's opt-outs every cycle.

   Recommend the CSV only as a bridge, with a named owner and a date the sync lands. Google Customer Match drops members not refreshed within 540 days.

   **Overlap.** Check overlap between this seed's audience and existing ones. Practitioner concern threshold is roughly 20-30%. Consolidate or exclude above it.

10. Fill the Seed Specification block (shape below; worked B2C and B2B versions in [references/examples.md](references/examples.md)) and hand the seed's tier placement to `mbfinotti/advertising-skills@ad-audience-targeting`.
11. Attach the measurement plan and a re-check date one cohort window out. If your harness has persistent memory, memorize the seed version, its definition, counts, and the re-check date so the next run compares against history instead of re-deriving it.

## The Seed Specification

Deliver one block per seed:

```
SEED SPECIFICATION - <seed name/version>, <date>
platform        : <destination platform(s)> | audience type: <lookalike | similar | value-based | predictive>
definition      : <source records> filtered by <selection rule> within <recency window>
value column    : <none | column, what it measures, currency> | mapping confirmed: <yes | at upload>
row count       : <n rows> | identifiers/row: <email, phone, ...>
expected match  : <x%> (basis: <platform range + list quality adjustment>)
effective seed  : <rows x match = n matched> vs floor <platform floor> -> <clears | fails>
fallback used   : <none | ladder rung + what changed>
exclusions      : <negative-selection list applied; suppression audiences delivered separately>
consent basis   : <basis + suppression enforced in warehouse date | BLOCKED - missing item>
refresh         : <cadence + owner + mechanism (manual CSV | automated sync)>
measurement     : <new-customer CPA target, cohort LTV checkpoints by seed version>
re-check        : <date - first cohort checkpoint>
```

## Evidence Gate

Refuse to emit a Seed Specification built on any of the following; state what is missing instead:

- **Unknown match rate basis** - no platform range consulted and no prior upload to calibrate against. Estimate only from the documented ranges plus list age/identifier density, and label it an estimate.
- **Unconfirmed consent basis** - the privacy gate (workflow step 2) did not pass. No selection quality justifies an upload the user has no lawful basis to make.
- **Value column of unknown provenance** - "we have an LTV field" is not evidence. If nobody can say whether it is revenue, margin, or a model output, the seed is not value-based until someone can.

Never invent a customer list, a segment definition, or a threshold the user's data does not support - request the missing evidence rather than substituting a generic list.

## Seed Diagnosis Ladder

When an existing lookalike underperforms and the seed is suspected, use this table as a symptom lookup, not a ranked menu: each symptom has one cause and one action, so ranking them against each other would be false precision.

What does need an order is which to fix when several symptoms fire at once. Fix anything that stops the audience serving or matching before anything about its quality - a floor failure, a broken mapping, or a match rate under the platform's band makes every quality read downstream of it meaningless. Then fix overlap and refresh, then the value/expansion causes.

| Symptom                                                    | Likely cause                                                                                     | Action                                                                                                  |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| Match rate far below the platform's documented range       | Stale list, single identifier per row, or unnormalized formats                                   | Normalize (E.164, lowercase email), add identifier columns, drop rows older than 18 months, then enrich |
| List uploaded but audience won't build or serve            | Matched count under the floor - row count misread as seed size                                   | Recompute effective seed; run the fallback ladder                                                       |
| Value-based option absent at audience build                | Value column not mapped during upload                                                            | Re-upload with mapping confirmed; the platform silently built a standard lookalike                      |
| CPA fine, 90-day cohort LTV of acquired customers weak     | Seed scaled low-margin converters (the documented Churney pitfall)                               | Re-seed on margin or predicted LTV; retire the seed version                                             |
| Lookalike performs near random / no better than broad      | Expansion percentage too wide, or heterogeneous seed mixing unlike buyers                        | Tighten the percentage; split seed by product line, segment, or country                                 |
| Plan cites Google Similar Audiences or LinkedIn Lookalikes | Stale playbook - Similar Audiences removed August 2023; LinkedIn Lookalikes sunset February 2024 | Rebuild on Customer Match as signal / LinkedIn Predictive Audiences (300 matched min)                   |
| Two seeded audiences cannibalizing each other              | Audience overlap above the ~20-30% concern band                                                  | Consolidate seeds or add mutual exclusions                                                              |
| Performance decays over weeks with no change made          | Static CSV never refreshed; members aging out                                                    | Set cadence and owner; automate the sync; respect the 540-day Customer Match cutoff                     |

## Platform Floors

Floors apply to the **matched** count. Compact view - full table with recommended sizes, expansion tiers, documented internal inconsistencies, deprecations, match-rate and refresh behavior in [references/platform-floors.md](references/platform-floors.md). Platform floors move over time: if your harness can browse the web, verify against the platform's live documentation before finalizing a spec; otherwise instruct the user to verify.

| Platform                      | Matched floor                                                             | Recommended seed                                                  |
| ----------------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Meta                          | 100                                                                       | 1,000-5,000 (Meta docs)                                           |
| Google Customer Match         | 100 (cut from 1,000 in 2025)                                              | 1,000+ (practitioner)                                             |
| Google Demand Gen lookalike   | 1,000 active matched (API docs; Help Center says 100 - take the stricter) | -                                                                 |
| LinkedIn (Matched/Predictive) | 300 matched                                                               | contact list: upload 10,000+ rows; company list: 1,000+ companies |
| TikTok                        | 1,000 (Help Center; FAQ says 100 - take the stricter)                     | 10,000 (practitioner)                                             |
| Pinterest                     | 100                                                                       | 1,000+ (practitioner)                                             |
| Reddit                        | 1,000 matched                                                             | -                                                                 |
| X                             | 100 matched                                                               | -                                                                 |
| Amazon AMC lookalike          | 500 user IDs                                                              | 10,000+ (practitioner)                                            |
| Snapchat                      | 1,000 to serve                                                            | -                                                                 |

## B2B vs B2C

**Identical in both:** hashing and normalization mechanics (SHA-256, E.164, lowercase email), match-rate arithmetic, the effective-seed computation, negative selection, warehouse-first suppression, and the measurement windows - they run on the same ad systems. What differs is list size and identity.

**B2B** lives with the small-list problem: 400 high-ACV customers cannot feed a consumer-platform lookalike natively, because work emails match poorly on Meta and TikTok while personal emails match poorly on LinkedIn. Identity enrichment before upload is the documented workaround, and the reason it is fallback rung 1.

B2B seeds are account-level or contact-level: expand a company list into contacts via title/seniority/function before upload. On LinkedIn, a company list wants 1,000+ companies, while a contact list needs roughly 10,000+ emails uploaded to reliably clear the 300-match floor. Seed from closed-won, not from MQLs.

The long sales cycle means the conversion read on a B2B seed lags by weeks: judge early on match quality and engagement, judge the seed itself only at cohort maturity.

**B2C** gets the opposite trade: lists large enough that selection discipline, not floor-clearing, is the binding constraint.

## Measuring Whether This Worked

Match rate is a data-quality leading indicator only - per Google's own wording, a high match rate suggests correct data but does not guarantee list performance. Never grade a seed on it.

Judge a seed version on new-customer CPA/CAC, new-to-brand rate, AOV of acquired customers, and the skill's own KPI: **cohort LTV at 90/180/365 days by seed version**. The named trap (Churney): low-CPA lookalikes that underperform on LTV at maturity because the seed scaled low-margin converters. The fix is re-seeding on margin or predicted LTV and retiring the version.

Compare seed variants with a user-level split test or a geo holdout, never a naive ad-set comparison - audience overlap contaminates it. Between the two valid methods:

- `split test > geo holdout` on effort - a platform setting versus withholding a market's traffic for the whole test window, which needs sign-off from whoever owns that market's number.
- `geo holdout > split test` on evidence strength - it survives cross-device identity loss and measures incremental sales, not platform-attributed ones.

Default to the split test where the platform offers a true user-level one. Escalate to the geo holdout when the seed decision is expensive to reverse - a re-platformed value column, a retired seed version, a country split - or when the split test's own read is what's in dispute.

Respect the learning phase before reading anything: roughly 50 optimization events per ad set per week (widely attributed to Meta's guidance) or 2-4 weeks at low volume.

Pass threshold: the seed version's 90-day acquired-customer cohort LTV meets or beats the account's average acquired-customer LTV at equal-or-better CPA. Below that, iterate: re-seed on value, tighten recency, or split. Re-check one cohort window later - a seed is a versioned artifact, not a one-time upload.

## Common Failure Modes

Deliberately unranked: these are trap/fix pairs, not competing options for one goal, and every fix here is cheap enough that ordering them by efficiency would imply a triage choice that does not exist - do all of them.

| Trap                                                    | Why it burns                                                                             | Fix                                                                                           |
| ------------------------------------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Sizing to the row count                                 | The floor applies to matched people; a 5,000-row list at 40% match is a 2,000 seed       | Compute effective seed; upload 2-3x the target                                                |
| Padding the seed with everyone to "hit the minimum"     | Dilutes the signal cluster; homogeneity outweighs size                                   | Run the fallback ladder instead - quality is never the first thing traded                     |
| Feeding cumulative lifetime revenue as the value column | It tracks tenure, and high-revenue low-margin customers poison the model                 | Use margin or predicted LTV                                                                   |
| Skipping the negative-selection pass                    | Refunders, discount-only buyers, employees, wholesale teach the model the wrong customer | Strip them before export, every time                                                          |
| Pre-hashing a file for UI upload                        | The platform hashes on ingest; a salted hash matches nothing                             | Upload normalized plaintext via the UI; hash only in API/warehouse syncs that require it      |
| Uploading before consent is confirmed                   | Hashed lists are still personal data under GDPR; enforcement is real                     | Privacy gate first; suppression enforced once, in the warehouse                               |
| Grading the seed on match rate                          | Match rate measures data hygiene, not audience quality                                   | Grade on cohort LTV by seed version                                                           |
| Judging a seed inside the learning phase                | Early CPA is noise until optimization volume accumulates                                 | Wait for learning exit or 2-4 weeks; then read                                                |
| One global seed for a multi-country lookalike           | Lookalikes are country-scoped; the model averages across markets                         | One seed-lookalike pair per country                                                           |
| Treating the upload as done forever                     | Static lists decay; members age out (540-day rule on Customer Match)                     | Refresh cadence with an owner, or automated sync                                              |
| Mixing work and personal identity per platform          | Work emails barely match on consumer platforms; personal emails barely match on LinkedIn | Match identifier type to platform; enrich when they diverge                                   |
| Copying 2022-era playbooks                              | Similar Audiences and LinkedIn Lookalikes no longer exist; inclusions became suggestions | Verify features against live docs; treat the seed as signal, exclusions as the only hard rule |

## Reference

- Read [references/platform-floors.md](references/platform-floors.md) when sizing against a floor - full per-platform table with dates, inconsistencies, deprecations, match-rate ranges, and refresh behavior.
- Read [references/seed-selection.md](references/seed-selection.md) when selecting rows - RFM cohorts, recency windows, the negative-selection list, value-based rules, and the non-purchase source ranking.
- Read [references/examples.md](references/examples.md) when writing the spec - a worked B2C value-based seed and a worked B2B closed-won seed that fails the floor and takes the fallback ladder.
