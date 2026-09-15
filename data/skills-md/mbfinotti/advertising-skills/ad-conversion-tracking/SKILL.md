---
name: ad-conversion-tracking
description: "Verify that conversion events are correctly configured, firing once, and deduplicated before a paid campaign launches, then turn the evidence into a GO / NO-GO decision. Covers tag debugging, test conversion tracing, browser/server event deduplication (including Conversions API setups), value and currency checks, conversion action status, consent handling, and test-data exclusion. Use whenever the user asks if their tracking works, mentions a pixel or tag check, conversions not showing up, duplicate conversions, or a pre-launch checklist - even if they never say 'conversion tracking'. Covers B2B lead gen and B2C ecommerce on any ad platform. Do NOT use to reconcile platform vs CRM numbers after launch - use mbfinotti/advertising-skills@ad-attribution-gap instead."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.6"
---

# Conversion Tracking

Verify that conversion tracking actually measures reality before a single dollar of campaign budget spends.

- **The anti-pattern this skill exists to prevent:** teams treat tracking as a launch-checklist checkbox, tick it off from a settings screenshot, and discover it was broken only once the spend report stops making sense. 70-80% of B2B SaaS search accounts audited by GrowthSpree carry at least one significant conversion tracking issue.
- **The governing principle:** bad conversion data does not merely misreport, it actively trains the bidding algorithm to find the wrong people - "if your tracking is inaccurate, every optimisation decision made by the platform will be based on incorrect data" (PPC Hero).

The output is a verification report with per-check evidence, ending in an explicit GO / NO-GO decision with a named approver.

## Scope and handoffs

This skill verifies; it never implements. It produces the checklist, walks the evidence, and issues the verdict - writing or installing tracking code belongs to whoever owns implementation (identified in the Interview). Adjacent ground goes to siblings:

- Reconciling cross-platform numbers after launch → `mbfinotti/advertising-skills@ad-attribution-gap`.
- Account-level performance root-cause diagnosis → `mbfinotti/advertising-skills@ad-account-diagnostic` (it hands tracking FAILs back here).
- Landing-page conversion-rate review → `mbfinotti/advertising-skills@paid-landing-page-audit`.
- Ongoing creative decay monitoring → `mbfinotti/advertising-skills@ad-creative-fatigue`.

## Interview

Ask one question at a time; skip anything already known or visible in the setup. This is a tactical pass, not an interview - keep it brief.

1. Which platform(s) will the campaign run on?
2. Funnel type: B2B lead gen, B2C ecommerce, or both?
3. Do server-side events run alongside the browser pixel/tag, or browser only?
4. Who owns implementation - you, a dev team, an agency? (Fixes get addressed to them.)
5. Is a consent banner live, and does traffic include a consent-regulated region?
6. Budget behind this launch? (Sets how much is at risk behind the gate.)
7. Is the launch date hard or movable? A hard date promotes the near-zero-effort settings and trigger fixes and pushes the click-identifier chain past launch as a risk-accepted item; a movable date lets the whole defect batch ship in one release and relearn once.
8. One-off clearance for this campaign, or a tracking setup you intend to trust for quarters? Compounding intent promotes the click-identifier chain and the shared event ID - they pay every future campaign; one-off intent promotes only the checks that clear this launch.
9. Effort ceiling before launch: your own hours in a tag manager, dev and CRM coordination, or a legal sign-off too? No dev access caps the fix list at settings and tag-manager work, and everything below that line is deleted from the list by name in the report, with the measurement it costs and who accepted the loss - never silently dropped and never left ranked last.

Answers 7-9 re-rank the fix ordering in the Defect checklist. Record them - the report has to say which defects were deferred and on whose authority.

## Evidence gate

Never issue a GO verdict from configuration screenshots alone - a settings page that looks right, or even a tag firing green in a debugger, is not proof of accurate measurement. A GO requires at least one real test conversion traced end to end:

1. Action performed.
2. Payload inspected.
3. Event received in the platform UI with correct value and currency.
4. Deduplicated.
5. Test data excluded.

One named exception: a brand-new property with no traffic yet cannot show a platform-UI conversion within the verification session (events can take hours to appear, and a fresh conversion action starts in a waiting status). It may receive a **provisional PASS, labelled as such**, on the strength of debug-mode evidence plus a correct payload - with a mandatory re-verification the moment the first live conversions land.

## The verification sequence

Nine steps, fixed order. Each step's evidence is only readable once the steps before it hold:

- The platform UI cannot be judged until what the tag actually sent is known.
- You cannot judge deduplication until events arrive from both sources.
- Test-data exclusion must exist before the soak period generates data - exclusion filters are not retroactive.

Do not rank these steps by efficiency, and do not reorder them to front-load the cheap ones: the sequence is a dependency chain, so a value-per-effort ordering here would be false precision. Efficiency ordering belongs to the fix list this sequence produces (Defect checklist), not to the sequence itself.

Record per-step evidence as you go.

1. **Settings and conversion-action configuration.** Confirm the primary conversion designation matches the business goal - revenue-relevant actions primary, page views and micro-actions secondary and excluded from bidding. Rawsoft found an account with 13 primary conversion actions of which only 4 were business outcomes, so smart bidding optimized against 1.5M+ monthly noise conversions. For lead gen, confirm count-once (not count-every) per click. _Evidence: list of primary actions, each mapped to a business outcome; counting method per action._
2. **Enter tag debug / preview mode.** Use the tag manager's preview mode and the platform's test-event or tag-inspection tool. _Evidence: the conversion tag visible and armed on the conversion page, firing on the intended trigger only._
3. **Perform a real test conversion end to end.** Walk the exact user journey a paid click takes - land with the click identifier in the URL, accept (and separately reject) the consent banner, complete the action. B2C: place a real low-value test order (near-zero discount code, or refund it later). B2B: submit a test lead with a unique QA value and confirm it lands in the CRM record. _Evidence: the test order/lead ID, and the identifier it carries._
4. **Inspect the event payload.** In the browser's network inspector or the tag debug tool, read the actual request: correct event name, value, currency, a per-conversion event ID, the click identifier, and hashed identifiers where used. _Evidence: the payload fields, copied into the report._
5. **Confirm the event in the platform UI.** The test event appears in the platform's event manager, marked browser or server, and the conversion action shows a healthy recording status. Any primary action in a misconfigured or no-recent-conversions status is an automatic NO-GO. Allow a few hours of reporting lag before concluding an event is missing. _Evidence: status per primary action; the test event visible with correct value and currency._
6. **Verify deduplication** (section below) whenever browser and server events both run. _Evidence: one counted conversion for the test action; dedup rate._
7. **Exclude and clean the test data** (section below). _Evidence: filter state active, test conversion retracted, test order refunded/removed._
8. **Soak.** Let real signals accumulate for a few days before scaling judgment - practitioners confirm the conversion has been reporting signals for a few days so the platform understands the goal (Pearmill); reconciliation against backend or CRM should wait roughly 4 days for data to settle (Enalitica). _Evidence: daily counts trending, gaps within thresholds (Objective section)._
9. **Document and sign off.** Fill the output-shape report, name the approver, date it, and issue GO / NO-GO. Launch checklists that skip an explicit approval field get skipped under launch pressure (Marketing Machine's template carries a GO/NO-GO block with approver and date). _Evidence: the completed report itself._

## Deduplication check

When a conversion is sent from both the browser tag and a server-side endpoint, the platform needs a shared key to count it once. Three conditions must hold (Analyzify):

- A **shared, per-conversion event ID** (an order ID works well) sent identically by both sources.
- **Matching event names** (exact, including casing).
- **Timestamps within the platform's matching window** - ideally seconds apart.

Failure modes to check for:

- The server generates a different event ID, or omits it entirely - the platform cannot match, and every conversion counts twice.
- A new event ID generated per page load instead of per conversion - a refresh mints a "new" conversion.
- Event-name casing or naming mismatch between the two sources.
- Timestamp drift pushing the pair outside the matching window.

Name the wrong fix explicitly, because it is the tempting one: **deleting the server event to stop double-counting is exactly backwards** - it silently discards the more resilient signal source. The fix is always the shared event ID.

Three confirmations exist, and they are not worth equal time:

```
efficiency (do first) : dedup rate > browser-vs-server count comparison > match-quality score
effort                : browser-vs-server count comparison > dedup rate == match-quality score
value for this goal   : dedup rate > browser-vs-server count comparison > match-quality score
```

Effort and value disagree on the match-quality score. It ties the dedup rate at the bottom of the effort axis: both are a single number the event manager has already computed and shows on one screen, nothing to pull, nothing to align. That is also why it ranks last on efficiency despite costing nothing: it is the least useful of the three here.

1. **Dedup rate**, in the platform's event manager - one screen, near-zero effort, and it answers the question directly. Healthy setups show ~90%+ of browser events deduplicated (TAGGRS shows a monitored setup at 95.35% browser / 100% server). Start here every time.
2. **Browser vs server event counts** for the same action - roughly an hour of pulling and aligning two reports. Run it when the dedup rate looks wrong, is unavailable, or when the test action counted twice; when the rate is healthy and the test action counted once, this is confirmation rather than discovery, so it can wait for the soak.
3. **Match-quality score** - read it as a **completeness** signal, never an accuracy signal. It rates how well-formed and matchable the event data is, not whether the conversions are real (AnyTrack), so it never confirms deduplication on its own. Record it; do not spend the launch window improving it.

Re-rank this against the account: where the platform's event manager hides the dedup rate, or where an analyst already maintains a browser-vs-server count report, step 2 moves to the front.

## Defect checklist

The defects that waste spend, with the check that catches each.

Impact says how badly the defect corrupts measurement:

- **Critical** blocks launch.
- **High** blocks unless explicitly risk-accepted in the report.
- **Medium** goes on the fix list.

Fix effort says what clearing it costs the reader in hours, coordination and reversibility.

**Rows are ordered by efficiency - impact bought per unit of fix effort - so the top row is the one to fix first, not the cheapest one and not the most critical one.**

| Defect                                                                           | Check that catches it                                                            | Impact                           | Fix effort                                                                             |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------- | -------------------------------------------------------------------------------------- |
| Noise actions designated primary                                                 | Settings review (step 1)                                                         | Critical                         | Near-zero - a designation toggle, reversible in a click                                |
| Container works in preview but was never published                               | Test the live site outside preview mode                                          | Critical                         | Near-zero - publish the container                                                      |
| Count-every set on a lead form                                                   | Settings review (step 1)                                                         | High                             | Near-zero - one counting setting per action                                            |
| Internal/QA traffic counted as conversions                                       | Filter state check (Test-data exclusion section)                                 | Medium                           | Near-zero - flip the filter from testing to active                                     |
| Tag fires on page load / all-pages trigger, not the completed action             | In debug mode, load the page without converting                                  | Critical                         | An hour - retrigger in the tag manager, no dev                                         |
| Fires on button click, not confirmed success                                     | Abandon a submit mid-way; check nothing fired                                    | High                             | An hour - same, plus a success signal to bind to                                       |
| Bot/spam form fills counted - and taught to the algorithm                        | Spam protection on forms; inspect lead quality in the soak                       | Medium                           | An hour - form-level protection, self-service                                          |
| Confirmation page refires on refresh/back (no unique transaction ID)             | Refresh the confirmation page after the test conversion; look for a second event | Critical                         | An hour if the order ID already reaches the tag; a week of dev if it does not          |
| Single-page-app route change refires the tag                                     | Navigate between virtual pages in debug mode                                     | High                             | An hour if a tag-manager rule fixes it; a week if the app must emit its own event      |
| Missing/hard-coded value, wrong or missing currency                              | Payload inspection (step 4)                                                      | Critical for value-based bidding | An hour if the value sits in the data layer; a week of dev if it must be exposed first |
| Browser + server both counted (no shared event ID)                               | Deduplication check                                                              | Critical                         | A week - dev coordination across both senders, and a redeploy to reverse               |
| Consent banner blocks the tag entirely, or consent state never reaches it        | Run the test conversion on both the accept and the reject path                   | High                             | A week, plus a legal sign-off - see compliance cost below                              |
| Click identifier stripped by redirect chain, or truncated by browser cookie caps | Inspect the landing URL and the persisted identifier at conversion time          | High                             | A week to a quarter - touches redirects, storage and every funnel step                 |
| Cross-domain checkout drops identity mid-journey                                 | Walk the full cross-domain journey in debug mode                                 | High                             | A week to a quarter - coordination across two domain owners                            |

Two axes disagree with that order, so state them separately:

```
efficiency (fix first) : settings-class toggles > trigger corrections > refire guard
                         > value & currency > bot protection > shared event ID > consent path
                         > click-identifier chain
compliance cost        : consent path > click-identifier persistence
                         > server-side sender (shared event ID) > every other row: none
```

Impact alone would put the shared event ID near the top; it lands sixth because a week of dev coordination buys the same critical fix that a designation toggle buys in a click. The internal-traffic filter is only Medium and still ranks near the top for the same reason, inverted.

The refire guard, the value-and-currency fix and bot protection are not tied: all three cost the same hour of tag-manager work when the data they need already reaches the tag, so impact alone separates them.

- A missing refire guard miscounts every conversion on the account.
- A wrong value miscounts only accounts bidding on value.
- Bot fills are Medium.

Compliance cost is the review a fix triggers and the reversibility it spends, never a fine.

- **Consent path** (heaviest): changing what fires on the reject path is a decision about lawful basis, so it needs privacy or legal sign-off before it ships and is awkward to quietly roll back once documented.
- **Click-identifier persistence:** extends a storage and retention decision across domains and into the CRM record, which usually reopens the privacy notice.
- **Server-side sender:** relocates event data to infrastructure the team chooses, which raises data-residency and processor questions the browser tag never raised.
- **Every other row:** a configuration change with no external reviewer.

**Default rung:** clear everything down to and including the shared event ID before launch, and risk-accept the consent path and the click-identifier chain in writing. Move one rung further - fixing the consent path pre-launch too - when consent-regulated traffic is a majority of the audience rather than a slice, because the risk-accepted signal loss then swamps the campaign rather than trimming it.

**What the efficiency order starves:** the server-side rebuild - the shared event ID, and the click-identifier chain behind it. Both sit at the top of the value axis and the effort axis, so a settings toggle outranks them every single round. An account that only ever fixes what is cheap this week runs for years on a browser tag whose signal loss nobody is still measuring.

Promote them above the default rung on any of these conditions:

- Interview question 8 comes back as a setup meant to be trusted for quarters.
- The funnel is B2B, where the identifier landing on the CRM record is what makes offline outcome import possible at all, rather than an improvement to it.
- The journey crosses domains, where the identifier is lost by construction and no downstream fix recovers it.

**Delete, don't demote.** Where a constraint rules a row out instead of lowering it, strike the row from this account's fix list and record it on the report's `deleted` line with the measurement it costs. No engineering resource before launch deletes the shared event ID, the consent-path rebuild and the click-identifier chain - the report then names what the campaign is knowingly launching without, and who accepted that.

Traffic that touches no consent-regulated region deletes the consent-path row outright as not applicable. A ruled-out row parked at the bottom of the order still reads as work someone intends to do, and comes back as scope the launch never budgeted.

This ordering is a default, not a law. It shifts with context and with who executes it, so re-rank it against what you already know about the user before presenting it:

- An in-house engineer on the team collapses every "a week of dev" row toward an hour and promotes the shared event ID.
- A tag manager already deployed with a built data layer collapses the value-and-currency and refire-guard rows.

Answers 7-9 in the Interview move it too: a hard launch date demotes the click-identifier chain, and a compounding mandate promotes it and the shared event ID above rows that only clear this one launch.

The ranking orders which defects make the cut - it does not order shipping. Everything that makes the cut still ships in one batch and relearns once (Learning-phase stakes); the ranking decides what is in that batch when the effort ceiling cannot hold all of it.

**The click-identifier chain.** Signal-loss defects share one root: the click identifier must be captured on the first hit - before any redirect - then persisted, carried across every funnel step including cross-domain hops, and attached to the order or lead record.

Redirect chains that strip query strings and browser storage caps that expire cookies within days are what silently destroy attribution; a single tracking redirect that drops the identifier breaks measurement for the whole campaign. For B2B, the identifier stored on the CRM record is what makes offline outcome import possible at all.

## B2B vs B2C

The verification spine is shared; value handling and timing diverge.

| Dimension             | B2C ecommerce                                       | B2B lead gen                                                                                                       |
| --------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Core conversion       | Purchase, immediate                                 | Form fill/lead, then offline stages                                                                                |
| Value                 | Dynamic value + currency per order                  | Value per pipeline stage; verify click-ID capture into CRM                                                         |
| Post-event correction | Refunds via conversion adjustment (restate/retract) | Lead disqualification via CRM outcome import                                                                       |
| Click-to-revenue lag  | Minutes to days                                     | Weeks to months - "B2B attribution is messy, fragmented, and impossible to make fully black and white" (AJ Wilcox) |
| Volume                | Usually clears platform learning minimums           | Often starves them; verify the optimized event has volume                                                          |

Identical for both - say so and don't re-derive: tag debug/preview, the shared-event-ID dedup mechanism, the platform-UI status check, consent handling, and the test conversion with payload inspection.

Two B2B-specific checks:

- Confirm the attribution window covers the sales cycle: a conversion landing 40 days after the click is simply not counted under a 30-day click window (Tucker Evans, B2Linked).
- Confirm the primary conversion is the deepest stage that still has enough volume: roughly 30 conversions in 30 days before optimizing to it (Jyll Saskin Gales's 30-in-30 rule); otherwise, optimize to a higher-volume upstream event and import downstream outcomes.

## Test-data exclusion

The verification itself pollutes the data; clean up before the soak period, not after.

- **The two-part filter trap.** Internal-traffic exclusion needs both a definition (which IPs/markers count as internal) and an activated filter. Many analytics setups default the filter to a testing state, where internal traffic is tagged but **not** excluded - the single most missed step (NiceLookingData). Verify the filter reads active, not testing.
- **Filters are not retroactive.** Exclusion must be in place before launch; data already recorded stays polluted.
- **Retract the test conversion** via the platform's conversion adjustment (value to zero / removal), and refund or delete the test order in the backend so backend-vs-analytics reconciliation stays honest. For B2B, delete the QA lead from the CRM.

## Learning-phase stakes

Why severity runs high on counting defects: platforms exit their learning phase on a minimum volume of optimization events.

- **Over-counting** (duplicates, bots, refires) exits learning on false signal - the algorithm then optimizes toward whoever triggers the phantom events (EasyInsights).
- **Under-counting** (consent loss, broken tags) traps the campaign below the threshold indefinitely (Niblin).

One audited account showed only 31 conversions on its primary metric while hundreds of real actions sat uncounted in secondary reporting - artificially stuck under the learning threshold (Jyll Saskin Gales).

Fix all discovered defects in **one batch**, then let the platform relearn once: smart bidding starts relearning from better data within roughly 24 hours of the fix (GrowthSpree). Serial one-at-a-time fixes trigger serial learning resets.

## Output shape

Deliver the verification as one report: a header (campaign, date, platform(s), funnel type, server-side flag, launch date, budget at risk), a per-check table across all nine steps (result, impact, fix effort, evidence), the dedup rate and gap summary, and a decision block (GO / NO-GO, fix order, blockers, deferred, deleted, re-verify, approver, date). See [./references/output-report-example.md](./references/output-report-example.md) for a full worked NO-GO example.

Every check reports one of pass / fail / unknown / not applicable - `unknown` is not `pass`. A brand-new property clears as `PROVISIONAL GO (new property - no traffic yet)` per the Evidence gate, never as a plain GO.

## Failure modes

- **Screenshot verification** - settings reviewed, nothing traced. The Evidence gate exists for this.
- **Deleting the server event to fix double-counting** - backwards; restore it and fix the shared event ID.
- **Testing only the consent-accept path** - the reject path is where signal silently dies; test both.
- **Filter left in testing state** - tagged is not excluded; verify the state reads active.
- **Launching on a waiting/misconfigured conversion status** - automatic NO-GO until the status is healthy.
- **Verifying in preview only** - the container was never published; test the live site.
- **Serial fixes** - each fix resets learning; batch every defect into one release, one relearn.
- **Reading match quality as accuracy** - it measures payload completeness; duplicates can score beautifully.
- **Chasing a zero gap** - a 10-20% platform-vs-analytics discrepancy is structural and normal (Ruler Analytics); spending the pre-launch window eliminating it delays launch for nothing.

## Objective and measurement

The gate clears - and only then does GO issue - when all of the following hold. Iterate on fixes and re-verify until they do:

- One real test conversion traced end to end, appearing in the platform UI with correct value and currency.
- Every primary conversion action in a healthy recording status; any primary action misconfigured or showing no recent conversions is an automatic NO-GO.
- Browser/server dedup rate at or above ~90%, with exactly one counted conversion per test action.
- Platform-vs-analytics gap inside the normal 10-20% band (Ruler Analytics).
- Ecommerce analytics-vs-backend gap under 25%; above 35% deserves investigation before launch (Enalitica).
- Server-vs-browser gap up to 10% is normal; a 30% gap combined with a match rate below 50% is a launch blocker - scaling on it is "spending more money to optimize a broken model faster" (Journify).
- Test data excluded with the filter active, the test conversion retracted, and the test order refunded.

Post-launch, track the platform-vs-backend ratio weekly: a stable ratio is healthy even if nonzero; a ratio swinging week to week means the pipeline is dropping events - hand off to `mbfinotti/advertising-skills@ad-attribution-gap`.

## Platform note (optional)

Load only when the user names their platform; the core checklist above stays vendor-neutral.

**Dedup keys and windows:**

- Meta deduplicates on `event_id` + event name within a 48-hour window.
- TikTok deduplicates on `event_id` + event name, merging events arriving after 5 minutes and within 48 hours of the first, keeping the first received.
- LinkedIn deduplicates on a shared `eventId` per conversion rule, keeping the Insight Tag event and discarding the Conversions API duplicate (the reverse of Meta's model).
- Google Ads deduplicates on `transaction_id`, with `gclid` for click matching.

**Click identifiers by vendor:** `gclid` (Google, plus `wbraid`/`gbraid`), `fbclid` (Meta), `li_fat_id` (LinkedIn), `ttclid` (TikTok), `msclkid` (Microsoft).

**Learning-phase minimums:**

- Meta ad sets need roughly 50 optimization events per 7 days to exit learning.
- Google Target CPA documents a 15-conversions-per-30-days minimum, with 30 recommended for evaluation.

Treat exact numbers as directional - platforms revise them.
