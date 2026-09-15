---
name: deal-red-flags
description: Reviews one deal's free-text notes - call notes, opportunity fields, CRM activity log, email threads - for qualification red flags such as single-threaded deal, no champion, no compelling event, unverified budget, no agreed next step, or fading engagement, each graded on severity and confidence with the quoted note fragment behind it. Covers B2B and B2C. Use whenever the user mentions deal risk, a stalled or slipping deal, ghosting, forecast inspection, or "is this deal real", even without the words red flag. Reviews one deal, not a pipeline export. Do NOT use for structured qualification scoring (mbfinotti/sales-skills@meddpicc-scorecard) or stakeholder mapping (mbfinotti/sales-skills@deal-champion-mapping).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.3"
---

# Deal Red Flags

Review the written record of a single deal - call notes, opportunity-record text fields, CRM activity log entries, email threads - and surface qualification red flags with the evidence behind each one. Free-text notes are lossy, so silence in the notes is not the same as a confirmed problem.

Grade every flag on two independent axes, never collapsed into a single score:

- Severity: how much damage the risk does to this deal if it is real.
- Confidence: how the notes evidence it.

A high-severity but poorly evidenced gap is escalated differently from a low-severity but certain one. The most common and most useful verdict is Unknown - the notes say nothing either way - because it converts a note gap into a question for the next call. A structured scorecard cannot produce Unknown honestly, since its input is already structured; that asymmetry is this skill's whole reason to exist.

Hard rules, not suggestions:

- Every finding graded Verified or Assumed must quote the exact fragment of the notes it came from. A finding with no quotable evidence is by definition Unknown.
- Every flag has a specific piece of disconfirming evidence that clears it. Check for it before recording a risk, so the review is not a one-way ratchet where every deal looks doomed.

## Use this, or use a sibling

Use this skill when the user has the written notes of one deal and wants its risks surfaced from the prose. Use something else when:

- The user wants a structured score against MEDDPICC criteria, criterion by criterion - `mbfinotti/sales-skills@meddpicc-scorecard`. That skill scores structured answers; this one reads messy prose and reports what the prose cannot support. This skill never outputs a methodology score.
- The user wants the stakeholder map built (who is the champion, economic buyer, blocker) - `mbfinotti/sales-skills@deal-champion-mapping`. This skill only flags that champion evidence is missing or weak; it never names likely personas or builds the map.
- The user wants a full discovery question set - `mbfinotti/sales-skills@sales-discovery-questions`. This skill emits exactly one diagnostic question per gap.
- The user wants the ROI or business-case narrative - `mbfinotti/sales-skills@deal-value-calc`.
- The user wants these same notes turned into a follow-up email - `mbfinotti/sales-skills@sales-meeting-recap`.
- The user has a pipeline export of many deals. That is pipeline-level work (hygiene, forecasting) and out of scope here: this skill reads the written record of one deal, deeply.

## Interview

Ask before reviewing - one question per message, multiple-choice where possible. Skip anything the notes already answer.

- B2B or B2C? (B2C here means considered purchases with a real sales conversation - remodeling, financial products, high-ticket coaching - not impulse retail.)
- Rough deal size and expected cycle length? (Calibrates severity: a missing mutual action plan is severe on a six-month enterprise deal, irrelevant on a two-week transactional one.)
- What stage does the seller believe the deal is in; is it on a forecast or commit list, and by what date must the answers land - the forecast call, the stage gate, or the buyer's own event? (A committed deal raises the stakes of every gap; a gap that resolves after that date is not worth chasing at any price.)
- What period do the notes cover, and are they complete? (One call's notes cannot evidence trends; see failure modes.)
- Is the goal this deal, or the habit behind it? (Saving this cycle ranks buyer-facing asks first; fixing qualification or note hygiene promotes the record work that pays across every later deal.)
- What is the effort ceiling before the next gate - how many asks the relationship can carry, and whether a manager or exec sponsor is available? (Decides which chase and response rungs are open at all.)
- Anything the user already suspects? (Becomes a hypothesis to test against the evidence - never a conclusion to confirm.)

## Intake

Accept any prose about the deal:

- Raw call notes.
- A pasted activity log.
- Opportunity-record free-text fields.
- Email or chat threads.
- Recap emails.
- Transcript excerpts.

Notes exported from any CRM or conversation-recording tool work as input - nothing in the workflow depends on which tool produced them. If your environment can read files, accept a file path or export; otherwise ask the user to paste the text.

Partial, messy, or thin notes are fine - saying what is missing is half of this skill's job. Be explicit with the user about what the review can and cannot see: it grades the notes, not the deal, so thin notes produce many Unknowns, and that is itself a finding about deal hygiene.

## Workflow

1. Run the Interview; then confirm the input covers everything the user has (a stray email thread often holds the only first-hand buyer quote).
2. Normalize the notes into a dated timeline of events: meetings held, who attended, commitments made, dates moved. Note where the record thins out - that is evidence too.
3. Extract candidate evidence: verbatim fragments that assert or disconfirm anything in the catalog. Distinguish first-hand buyer statements from the rep's own inferences and from second-hand relays - "I have it in writing from the economic buyer" outranks "my champion told me".
4. Run every group of [references/red-flag-catalog.md](references/red-flag-catalog.md) against the timeline and the evidence. Resolve every flag in every group to a state - never skip a group.
5. Check each flag's disconfirming evidence before recording a risk. A flag whose clearing evidence is quoted in the notes is Cleared, not Red.
6. Assign severity to every non-Cleared flag, calibrated to the deal size, cycle length, and motion from the Interview - not to a fixed table.
7. Separate what is evidenced from what is merely absent. Write exactly one diagnostic question per Unknown flag (the catalog supplies one per flag), then order the Gaps by the chase order below - the rep gets one next touch, not twelve.
8. Write the report in the output shape below, attaching one remediation play per Red and Amber flag from the catalog and naming the response rung that play belongs to.
9. Run the Quality gate; iterate - re-grade and rewrite - until every item passes.
10. If your harness has persistent memory, record the flags raised, their states, and their evidence, so the next review of the same deal can check which gaps closed. Otherwise end the report with a short carry-forward list for the user to keep.

## Grading rubric

Confidence states - how the notes evidence the flag:

| State    | Meaning                                                                | Evidence requirement                     |
| -------- | ---------------------------------------------------------------------- | ---------------------------------------- |
| Cleared  | The notes contain the flag's disconfirming evidence                    | Verbatim quote of what cleared it        |
| Verified | A first-hand, quotable buyer statement evidences the risk              | Verbatim quote from the notes            |
| Assumed  | Only the rep's inference, hearsay, or a second-hand relay evidences it | Verbatim quote of the inference or relay |
| Unknown  | The notes are silent on this flag                                      | None - silence is the finding            |

Severity - High, Medium, or Low: the damage to this deal if the risk is real, judged against deal size and cycle length, not a fixed table. Grading a flag red/amber/green with a verified-versus-assumed confidence test is standard practice in deal inspection (documented across MEDDPICC-lineage sources); the state names above extend that vocabulary with Unknown for note review.

Deliberately left unranked: severity and confidence are a risk rubric, not a menu of competing options. Never order the two axes against each other, and never collapse them into one score - the rubric grades what the notes say, and the two rankings below then choose the work on top of its output. A later pass should leave the rubric alone.

Report grade - a presentation grouping only; both axes stay visible on every finding:

- Red: Verified risk, High severity.
- Amber: Verified risk at Medium/Low severity, or Assumed risk at High severity.
- Watch: Assumed risk at Medium/Low severity - name what would confirm or clear it.
- Gap: any Unknown - carries one diagnostic question, never a remediation play (there is nothing confirmed to remediate).
- Cleared: listed briefly with its clearing quote, so the next reviewer does not re-raise it.

## Chase order: which gap earns the next touch

Grading resolves every flag in every group; chasing is the separate, smaller choice. The rep has one next touch, so a gap is only worth chasing when the answer changes what they do next - a flag that cannot move the plan is not worth chasing however severe it looks. Rank the instrument, not the flag: the same gap is cheap or expensive depending on how the rep closes it.

Effort here is rep hours, buyer goodwill spent on the ask, and calendar latency before the answer lands - never a price.

- efficiency (the default order): `desk check > one question > access ask > second data point > record repair`
- value: `access ask > one question > desk check > record repair > second data point`
- effort, most to least: `record repair > access ask > second data point > one question > desk check`

| Rung                                                                                                                          | What it closes                                                                                                 | Effort                                                                   | What the answer changes                                                                                                 |
| ----------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| Desk check - close it from records the rep already holds: calendar, sent mail, CRM field history, attendee lists              | Thread coverage, close-date pushes, seller-owned timeline, latency and attendance trends, notes thinning       | Near-zero; no goodwill; the answer already sits in the rep's own records | Re-grades the evidence base itself - a thin or wrong record corrupts every other finding, so this one gates the rest    |
| One question in the thread - a single diagnostic question answered by email or in the already-booked call                     | Decision process, budget owner's own words, the blocker's actual objection, next dated step, quantified impact | An hour of prep, one ask of goodwill, days of latency                    | Usually flips the forecast category and names the next meeting                                                          |
| Access ask - ask the buyer to spend their own capital: an introduction, the co-decider, the missing function, a co-owned plan | Economic buyer never met, co-decider unconsulted, champion's reach to power, requirements from one function    | A week or more of latency, real goodwill, and refusable                  | The most of any rung - the ask is both the confirmation and the remediation, and a refusal is itself a Verified finding |
| Second data point - wait for the next reply gap, push, or attendee list                                                       | Trend flags that a two-point record cannot grade at all                                                        | Near-zero hours, but a quarter of calendar latency                       | Little now - the answer usually lands after the forecast call it was meant to inform                                    |
| Record repair - backfill this deal's log, then hold notes to a gradable standard                                              | Nothing on this deal today                                                                                     | A standing job                                                           | Nothing for the next call; compounds across every later review of every deal                                            |

Deleted, not demoted: a full re-discovery call closing several gaps at once. This skill emits one question per gap, and five questions in one call reads as an interrogation - it burns exactly the goodwill the access ask needs. Route a genuine full question set to `mbfinotti/sales-skills@sales-discovery-questions`.

What this order starves:

- The access ask: highest value, highest effort, so it loses every efficiency round. That is the failure mode of ratio thinking here, because unmet power is what kills late-stage deals while the cheap rungs report progress. Promote it to first whenever the deal is on commit, or the next stage gate is the decision meeting: no desk check clears a veto.
- Record repair, too. Promote it when Unknowns dominate two consecutive reviews of the same deal.

Re-rank against what you already know about this deal and this rep, and say in the report which fact moved which rung:

- A forecast call inside the week promotes the access ask and makes the second data point worthless.
- A champion who replies same-day collapses the one-question rung's latency, promoting it above the desk check.
- A rep carrying thirty deals stays on the first two rungs; a rep with three can afford an access ask on each.
- An answer of "fix the habit" in the Interview promotes record repair from last to first.
- Notes covering a single call make the desk check return nothing but Unknowns - start at the one-question rung.

## Response order: what to do with a confirmed flag

Applies only to Red and Amber. An Unknown has nothing confirmed to respond to; it goes back to the chase order above.

- efficiency (the default order): `trade it > work it > re-forecast it > escalate it > disqualify`
- value, as deals unblocked or cycle hours returned: `escalate it > trade it > work it > disqualify > re-forecast it`
- effort, most to least: `escalate it > work it > trade it > re-forecast it == disqualify`

The tie is real: re-forecasting and disqualifying both cost near-zero rep hours, zero buyer goodwill, and one internal update. They are genuinely equal in what the rep spends and differ only in reversibility, which the value axis carries - so effort alone must not pick between them.

| Rung           | What it is                                                                                                        | Effort                                                                     | What it buys                                                                                         |
| -------------- | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Trade it       | Make the fix the price of the next thing the buyer already wants - the proposal, the scoping session, the pricing | An hour to structure; no new goodwill, since the buyer's own ask funds it  | The flag closes inside a step that was happening anyway                                              |
| Work it        | Run the catalog play as its own touch                                                                             | An hour of prep, one touch of goodwill, days of latency                    | One flag closed; the default when nothing is on the table to trade                                   |
| Re-forecast it | Move the deal out of the committed period and name the flag that moved it                                         | Near-zero hours, no buyer goodwill, some internal capital                  | Forecast truth, not deal progress - the honest answer to an urgency or budget flag nothing can clear |
| Escalate it    | Bring a manager or exec sponsor to open a door the rep cannot                                                     | Political capital, a week of coordination, spendable roughly once per deal | Everything where the blocker is access; nothing where it is information                              |
| Disqualify     | Return the remaining cycle's hours to the rest of the pipeline                                                    | Near-zero                                                                  | The whole remaining cycle - and it is irreversible, so it is wrong on any recoverable flag           |

Deleted, not demoted: raising the flag to the buyer as a concern with no ask attached. It spends goodwill and returns no evidence; every catalog play carries an ask for exactly that reason.

What this order starves:

- Escalation: it reads as expensive and political, so efficiency never picks it, and the flags it alone fixes (economic buyer never met, blocker unaddressed) are the ones that kill deals late. Promote it above trade and work when the blocker is access rather than information, the champion has been asked at least twice, and the stage gate lands inside the current period.
- Disqualifying, for the same reason. Promote it on one named unrecoverable flag, never on a flag count.

Neither order is a law. Both shift with the deal, the quarter, and who executes: a rep with an engaged exec sponsor escalates cheaply, a rep without one should not plan around it, and quarter end promotes trading and re-forecasting over anything with a week of latency in it.

## Invocation and output shape

Typical invocations:

- "Here are six weeks of notes on my top deal - what red flags am I missing?" (pasted notes follow)
- "Review this opportunity's activity log before I commit it - is this deal real?"
- "Single-threaded check: everything I have on the deal is in this email thread."

Deliver one report (worked example, including a negative example, in [references/example-review.md](references/example-review.md)):

```
DEAL RED-FLAG REVIEW - <deal>, reviewed <date>, notes covering <period>
Snapshot   : size, stage, cycle age, motion (B2B/B2C) - as stated, or "not in notes"
Timeline   : dated events reconstructed from the notes; where the record thins
Red        : flag - severity - verbatim evidence quote - one remediation play -
             its response rung, and the fact that promoted or demoted it
Amber      : same shape as Red
Watch      : flag - verbatim evidence quote - what would confirm or clear it
Gaps       : flag - one diagnostic question - its chase rung; listed in chase
             order, highest value per unit of effort first
Cleared    : flag - the quote that cleared it
Risk check : the two pipeline-review questions (Armand Farrokh, 30MPC): is there
             risk in HOW the deal cleared its past stage criteria, and is there
             risk in the PLAN for the next ones - answered from the findings
Verdict    : what is evidenced vs what is merely absent; the single next action,
             which is the top of the chase order after re-ranking against the
             Interview answers. Never a win-probability or methodology score.
```

## B2B and B2C

Identical in both, stated explicitly rather than left implied:

- The evidence rule: quote it, or it is Unknown.
- The two-axis grading.
- The disconfirming-evidence check.
- The whole Pain and value, Engagement, and Urgency-quality logic: happy ears, unquantified impact, seller-owned timelines, repeated pushes, and growing response latency read the same way in both motions.

Genuinely different in B2C and high-velocity transactional deals - do not just relabel the B2B list:

- Single-threading is not a flag: these deals are single-stakeholder by design. The equivalent stakeholder risks are an unconsulted co-decider (partner or spouse whose approval is assumed but never evidenced) and unverified ability to pay (financing or credit never confirmed).
- Compelling events are more often personal or seasonal (a move, a life event, a deadline the household set) than fiscal; a real dated trigger still beats "they seemed eager".
- Procurement, security, and legal review usually do not exist; the Process group collapses to one question - is there an agreed, dated next step? Cart or trial abandonment and lengthening reply gaps take over as the dominant engagement flags.
- Applying enterprise heuristics to a transactional deal is itself a false positive (see below), and the reverse holds too: judging a long-cycle enterprise deal by transactional response-speed standards manufactures ghosting flags that are not real.

## Failure modes and false positives

| Over-reaction                                                   | Fix                                                                                                                                         |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Treating Unknown as Red                                         | Unknown means the notes are silent, not that the deal is broken; it earns a question, not an escalation                                     |
| Flagging a small transactional deal against enterprise criteria | Calibrate with the Interview; multithreading and mutual-action-plan flags switch off below the motion they fit                              |
| Calling a deal single-threaded when the notes cover one call    | One call's notes evidence one call; state Unknown for coverage and ask who else is involved                                                 |
| Inferring champion departure from a single unanswered email     | A widening pattern of gaps is evidence; one silence is not - grade Assumed at most, with the quote                                          |
| Qualifying out on a flag count                                  | Counts collapse the two axes and a count is not a decision rule; the response order names what does justify disqualifying                   |
| One-way ratchet - recording risks without checking clears       | Run step 5 for every flag; a review that cannot output Cleared will always find a doomed deal                                               |
| Reading slow, consensus-driven buying as disengagement          | Some buying cultures and regulated processes are legitimately slow and quiet; weigh cadence against the segment's norm, not a universal one |
| Grading the deal instead of the notes                           | The verdict must distinguish "evidenced risk" from "thin record"; recommend better note hygiene when Unknowns dominate                      |

## Quality gate

Score the finished report against all six. Pass threshold: 6/6 - iterate until nothing fails.

1. 100% of Red and Amber findings carry a verbatim evidence quote from the notes.
2. Every catalog group resolves every one of its flags to a state - none skipped, including Cleared and Unknown.
3. No Unknown appears as Red, Amber, or Watch; every Unknown carries exactly one diagnostic question.
4. Every Red and Amber finding carries exactly one remediation play.
5. Every severity is justified against this deal's size, cycle, and motion - no fixed-table severities.
6. Gaps are listed in chase order and Red/Amber plays name a response rung, both re-ranked against the Interview answers, with the fact that moved a rung stated.

## KPIs and measurement

The review worked if, on reviewed deals over time:

- The slip rate (close dates pushed past the committed period) falls.
- A growing share of flagged deals close the flag before the next stage.
- Forecast accuracy on reviewed deals improves against unreviewed ones.
- Unknowns from one review convert to Verified or Cleared by the next.

A rising Unknown count across reviews of the same deal means note hygiene, not deal quality, is the problem to fix first.
