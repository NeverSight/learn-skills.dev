---
name: cycle-review
description: Run the fortnightly-ish cycle-review meeting round trip on the CLHbid Delivery board — publish the meeting notes discussion, process the returned notes back into cycles and statuses, or adjust a cycle's membership.
disable-model-invocation: true
---

# Cycle Review

The cycle review is a **round trip through a GitHub Discussion**. Branch A publishes the meeting
notes as a Discussion, the meeting works through them, the project manager posts their decisions as
a comment, and branch B turns those decisions into tracker writes.

**The Discussion is the record**, and the baseline the next cycle's notes are diffed against. See
[Editing Discussions](#editing-discussions) for where they live and how to read and write one.

**The notes are not edited during the meeting.** The project manager posts a comment using the same
headers, and branch B integrates it afterwards.

A cycle is an iteration of the `Cycle` field; work state is the `Status` field. Both live on the
CLHbid Delivery project. **Read the field mechanics, the `Status` values, the reference convention
and every board query from the `issue-tracker` skill** — this skill names the recipes it needs and
never restates them, so the two cannot drift.

**Everything branch A reports is the business view.** Every section of the notes, every number
quoted beside one, and anything said in conversation about them filters to **business work** with
the `business` filter — see **Business and delivery** in `issue-tracker`: top-level issues and the
children of epics. Every issue table opens with an **Epic** column naming the epic a row belongs
to, blank for ordinary work; an epic's rows sit together, ordered by `Result`. An epic itself
appears only in [Epics](#the-notes). The one thing that must not be lost to the filter is a **question**: when the issue
blocking on business input is a sub-issue of an ordinary parent, list the parent as the item and
name the child, so branch B knows which issue the answer lands on.

**The notes are a business document**, written with `writing-lean`. No agent commentary — tooling
state, recipe caveats and process notes go to the project manager in conversation or into your own
TODO list.

## Cycle roles

Roles are resolved from the `Cycle` field's `configuration` by date, never by array order or by
reading a title:

| Role    | Where it comes from                                                          |
| ------- | ---------------------------------------------------------------------------- |
| closing | the most recent entry in `completedIterations` — the cycle the meeting closes |
| current | the entry in `iterations` whose `startDate + duration` brackets today         |
| future  | the two entries in `iterations` starting after current                        |

An iteration **ends the day before the meeting that closes it**. **If the roles cannot be resolved,
stop and say so** — never invent an assignment.

Every membership change is `gh project item-edit` against the `Cycle` field, on **committed units
only** — a top-level issue or a child of an epic; descendants inherit, and an epic's own `Cycle` is
never set. Every state change is a `Status` value from the `issue-tracker` role map. The
milestones API plays no part in this skill.

**Confirm before every mutating step.** Show the proposed cycle and status values, closures, issue
body edits, notes body and iteration-configuration diff, get an explicit go-ahead, then read the
write back. A read-back that disagrees straight after a write is unconfirmed, not failed — re-check
after a moment rather than re-issuing it.

## Invocation

- **A. Prepare** — `/cycle-review prepare for the 2026-08-28 meeting, next one is 2026-09-11`
- **B. Process notes** — `/cycle-review process the notes from discussion 2323`
- **C. Adjust** — `/cycle-review move clhbid/clhbid.com#2325 into the current cycle; defer
  clhbid/CLHbid-LiveAuction#922 to the next one`

## Branch A — Prepare the notes

Branch A publishes the notes discussion and writes to the tracker only in the bookkeeping steps
below. **They run first**, before a line of the draft is written, because they change what the
tables say. _Automatic_ means no meeting decides them — they still show their list and take a
go-ahead, like every other mutation.

1. **Open the next cycle.** Three iterations must be live: current plus two future. If only two
   are, add one. **This is a destructive configuration write** — follow the procedure in
   `issue-tracker`, and fold every other pending change into the same write, because a second one
   costs a second restore of the whole board.
2. **Housekeeping.** Run the `issue-tracker` **stale closed items** recipe and flag what it
   returns, along with any issue that should be on the board and is not. **Both are healthy empty**,
   so a result is a signal that the sweep behind them is failing. Report it to the project manager
   in conversation and archive by hand with `archiveProjectV2Item` only if the meeting cannot wait.
   Then run the **Epic candidates** recipe, read each result, and put the ones that slipped or
   whose open children plainly exceed a cycle to the project manager — work committed "this cycle
   and the next few" is the signature. **Converting is the project manager's call, made before
   the meeting**, never a `Decision` line: for each agreed one, PATCH its type, clear its `Cycle`,
   set `Cycle` on the children being committed and move its `Status` along the ladder — see
   **Epics** in `issue-tracker`. **All of this stays out of the notes.**
3. **Merged, still open.** Run the `issue-tracker` **merged pull request, open issue** recipe.
   GitHub closed nothing for these — the recipe says why — so each is finished work that no cycle
   report has ever credited. Every row ends one of two ways: closed as `completed` naming the pull
   request, or judged still live because the pull request was a deliberate partial. Report the
   closures to the project manager in conversation. **This stays out of the notes** for the same
   reason step 2 does.
4. **Worked-off-cycle backfill.** Run the `issue-tracker` **worked off-cycle** recipe against the
   closing cycle's window and keep the business results — top-level issues and epic children. A
   sub-issue of an ordinary parent needs no write and no row — it inherits its parent's cycle. This
   is bookkeeping, not triage: no meeting decision, no `Decision` line.
   - **Closed** work is credited to the cycle it was completed in — set `Cycle` — and appears as an
     extra `➕ Added mid-cycle, done` row in **Last Cycle**.
   - **`In progress`** work touched during the closing cycle was picked up without ever being
     committed to it. Credit it to the cycle now opening — unfinished work belongs to the cycle
     that will finish it — and record it in **both** places: an `➕ Added mid-cycle, not done` row
     in **Last Cycle** whose reason says it carries forward, and an entry in **Committed This
     Cycle**.
   - **Dormant** work — the **dormant** variant of the same recipe, untouched since before the
     closing cycle began — gets **no write**. List it as its own decision with its status flagged
     **suspect**. Never auto-credit it, and never reset it to `Backlog`.
5. **Read the board.** Project items, the `Cycle` configuration, and the previous cycle's notes
   discussion.
6. **Draft Last Cycle.** Restate the closing cycle's goal, then table every committed unit in it.
   **`Result` is filled in** — closed is `✅ Done`, open is `❌ Slipped`. **`Reason` is blank**
   unless the row slipped or was added mid-cycle, and it is filled **only from direct evidence**: a
   closing pull request, a comment, sub-issue state. Leave it blank rather than inferring one. Diff
   the membership against the previous cycle's notes so slippage and mid-cycle additions are
   visible rather than silently absorbed.
7. **Draft Epics.** One row per open epic, from the `issue-tracker` **Epics** recipe: its
   `Status`, progress as `completed of total`, and the children committed to the current cycle. An
   epic closed during the window gets a final row, `🏁 Completed`. Below the table, a **Ready to
   close** line with its own `Decision` for every epic the **Epics ready to close** recipe
   returns. Closing is the meeting's call, and a decision to keep one open names what remains to
   be done.
8. **Draft Next Cycle Review** — date, time and location together, from the invocation or empty. It
   comes **before** Current Cycle because it sets when the cycle ends, and therefore how much fits
   in it.
9. **Draft Current Cycle**, sections in this order, because each one feeds the next: **New Issue
   Triage** (every issue opened since the closing cycle started, `Decision` blank), **Stale
   Issues** (next step), **Waiting on Input** (every `Status = Waiting on input` issue, listed
   **one at a time** with its own `Decision`, never summarised as a count), **Significant Dates** (a
   blank prompt), then **Committed This Cycle**, carrying anything the backfill already credited.

   Report the count of items already `In progress` alongside Committed This Cycle. **We finish what
   we start**: started work takes precedence, and new work should not be accepted into the cycle
   while it is outstanding.

   Each **Waiting on Input** row states the question and its decision. **The question must already
   exist as a comment on the issue** — a plain comment stating it is enough; the _Triage Notes_
   heading is a convention, not the test. If no comment asks it, that is an **error**: the question
   has never been put to anyone, so say so rather than reconstructing one from the title.
10. **Draft Stale Issues.** Run the `issue-tracker` **stale issues** recipe and report two numbers:
   the total stale, and how many went **newly stale** during the cycle just closing. Then do the
   reading:
   - **Close candidates** — a handful, judged on _old_, _underspecified_ or _duplicate_. This means
     reading each candidate's body and cross-checking the board for duplicates. Sorting by age is
     not the job.
   - **Needs a cycle, not a close** — stale work that plainly still needs doing, flagged for
     pulling into this cycle's triage instead.
   - **Newly stale, worth a look** — anything that went stale this cycle and looks important on its
     own evidence: comment volume, a prior assignee, other issues referencing it. A judgement call,
     not a threshold.
11. **Draft Future Work** — one sub-section per future cycle, headed by the iteration name, each
   with its own table, so the load committed to each is visible at a glance.
12. **Draft the closing sections.** **Out of Office** is a blank prompt for the team. **Next
    Actions** is present but empty, showing the owner-first shape.
13. **Reconcile against the live board.** Every cycle section must agree with what the board
    actually says, item for item.
14. **Publish.** Create the Discussion, or update it if this cycle's notes already exist. **Branch A
    is re-runnable**: run it again whenever the board changes and it revises the same discussion.

**Every section is worked one decision at a time.** Each triage line, each `Waiting on input`
question and each stale candidate carries its own `Decision`, never a shared verdict at the end of
a table.

See [The notes](#the-notes) for the shape, with every `Decision`, `Reason` and **Next Actions** line
blank in the draft and filled in on the way back.

## Branch B — Process the returned notes

Read the published body and the project manager's comment from the API by discussion number.

**Accept both reference forms.** A qualified `<org>/<repo>#<number>` resolves as written; a bare
`#<number>` resolves against `clhbid/clhbid.com`, the repo hosting the discussion. **Say which issue
you resolved a bare reference to** before acting on it.

1. **Last Cycle** — the discussion is the record and the backfill already set every `Cycle` in
   branch A. Nothing to write.
2. **Sweep.** **No open item may still carry the closing cycle** (`cycle:@previous is:open` on the
   board). Reassign every straggler with `gh project item-edit` — usually to current, or clear the
   field if the work was dropped. An orphan left behind is invisible to every cycle-scoped view
   from then on.
3. **New Issue Triage** — apply each line: set `Cycle` and `Status` with `gh project item-edit`, or
   close the issue with `--reason "not planned"`.
4. **Stale Issues** — apply each line: close candidates are closed `--reason "not planned"`; work
   pulled into a cycle gets its `Cycle` set like anything else triaged at this meeting; items
   merely flagged as worth watching get **no write at all** — they are informational, and they
   resurface in next cycle's stale report on their own.
5. **Waiting on Input** — for each answered question, record it on the issue in two places: reply
   to the comment that asked it, prefixed `> *Recorded from the <date> planning meeting.*`, and
   **fold the answer into the issue body** so someone picking the work up cold has the whole spec.
   The comment is the audit trail; the body is the spec. Never delete what was there. An item the
   meeting could not resolve is **left untouched**, `Waiting on input` and all.

   Then route it off `Waiting on input`, and only when **every** question on the issue is answered:
   `Ready for Agent` **only if the updated body now reads as a complete brief an agent could work
   from cold**; `Ready for Human` if it needs judgement, external access, a design decision or
   manual testing; `Backlog` if it is answered but still underspecified. An answer that raises a
   **new** question has not unblocked anything: post the new question as a comment in the same
   shape and leave the issue on `Waiting on input`.
6. **Significant Dates** and **Out of Office** — informational; no tracker write.
7. **Committed This Cycle** and each **Future Work** section — set `Cycle` on each committed unit,
   skipping anything the branch A backfill already credited. The first child of an epic committed
   to any cycle moves the epic to `In progress` if it is not there already.
8. **Epics** — the table is informational; the **Ready to close** lines are writes. An agreed
   close is `gh issue close --reason completed`; an epic kept open has what remains filed as a new
   child, so its progress stops reading complete.
9. **Next Actions** — decide by **what the line describes, not who owns it**: the owner tells you
   nothing, since the project manager's own lines cover both delegated tracker work and follow-ups
   they handle themselves. Execute the tracker actions — cycle and status changes, closures, the
   new-issue draft. Leave person-to-person follow-ups alone.
10. **Apply any agreed cycle date change** to the `Cycle` field's configuration. **The write is
   destructive** — follow the procedure in `issue-tracker`. Branch A has usually already made this
   cycle's one write, so an agreed date should have gone in with it.
11. **Draft an issue** for work in the notes that matches nothing on the board — category label
    only, no state, body drawn from the notes. It is new input, so it lands in `Backlog` like
    anything filed from a template.
12. **Update the discussion** with the decisions integrated, then **re-check for issues closed
    since the notes were published** — meeting-morning merges land after the cut and would
    otherwise be credited to the wrong cycle.

## Branch C — Adjust

Move membership with `gh project item-edit` on `Cycle`, or clear it when work is dropped, then note
the change in the next notes discussion.

## The notes

Below is a **completed** set of notes — the input branch B receives, every `Decision`, `Reason` and
**Next Actions** line filled in. It is also the target branch A drafts toward: the same headings,
the same order, the same prompts, with those fields blank instead. Reproduce this shape.

Notice the **Next Actions** register: outcomes in business language, owner first. Field names and
`gh` syntax never appear there — the team reads this, and branch B recognises a tracker action by
what it describes.

_Illustrative example. The organisation, repositories, issue numbers and titles are invented, chosen
to cover the range of states the skill has to handle. Nothing here is real work._

````markdown
# Cycle Review — 18 Mar 2026 meeting

## Last Cycle: Checkout reliability & vendor migration (4 Mar → 17 Mar 2026)

**Goal:** Stop checkout failing under load, and finish moving off the old payments vendor.

| Epic | Issue | Title | Result | Reason |
| ---- | ----- | ----- | ------ | ------ |
| acme/site#421 | acme/site#423 | Export stored payment methods from the old vendor | ✅ Done | — |
| acme/site#421 | acme/site#424 | Import stored payment methods into the new vendor | ❌ Slipped → current cycle | The vendor's import API rate-limits at a rate that makes a single-pass import impossible; needs a batched approach. |
| | acme/site#412 | Retry failed payment captures instead of dropping them | ✅ Done | — |
| | acme/site#418 | Checkout times out when the vendor is slow to respond | ✅ Done | — |
| | acme/api#207 | Remove the legacy payments client | ✅ Done | — |
| | acme/infra#88 | Alert on checkout error rate rather than raw 5xx count | ✅ Done | — |
| | acme/api#215 | Retire the vendor webhook shim | ❌ Slipped → current cycle | Blocked on acme/site#424 — the shim cannot go until stored methods have moved. |
| | acme/site#430 | Fix the currency rounding error on partial refunds | ➕ Added mid-cycle, done | Reported by finance mid-cycle and treated as urgent; nothing was displaced to fit it. |
| | acme/infra#91 | Rotate the credentials the old vendor had access to | ➕ Added mid-cycle, done | Closed during the cycle without ever being committed to it. |
| | acme/api#219 | Split the checkout handler so failures are isolated | ➕ Added mid-cycle, not done | Picked up mid-cycle without being committed; carries into the current cycle, where it is listed under Committed This Cycle. |

**Decision:** Both slipped items carry into the current cycle as-is. The batching approach for
acme/site#424 is agreed in principle — no rework of what has already migrated.

## Epics

_Work too large for one cycle, delivered a child at a time. Progress counts children._

| Epic | Status | Progress | Committed this cycle |
| ---- | ------ | -------- | -------------------- |
| acme/site#421 · Migrate stored payment methods to the new vendor | `In progress` | 3 of 8 | 2 · acme/site#424, acme/site#425 |
| acme/api#198 · Schema consolidation | `Ready for Human` | 0 of 6 | — |
| acme/site#390 · Review and close the never-triaged backlog | `Ready for Human` | 0 of 4 | 1 · acme/site#450 |
| acme/site#380 · Retire the legacy admin | `In progress` | 5 of 5 | — |

**Ready to close**

- **acme/site#380** — every child is closed. **Decision:** Kept open — the old admin's DNS entry
  still points at the retired host; filed as a new child, and the epic closes with it.

## Next Cycle Review

_Agreed first, because it sets when the current cycle ends and therefore how much fits in it._

**Date:** 1 Apr 2026
**Time:** 10:00 AM MT
**Location:** Video call — link in the calendar invite

## Current Cycle: Search relevance (18 Mar → 31 Mar 2026)

### New Issue Triage

_Every issue opened since the last cycle, and where it landed._

| Epic | Issue | Title | Status | Decision |
| ---- | ----- | ----- | ------ | -------- |
| acme/site#421 | acme/site#425 | Cut over checkout to the new vendor's stored methods | `Ready for Agent` | ➡️ This cycle — the last step of the migration |
| | acme/site#437 | Search returns nothing for hyphenated terms | `Backlog` | ➡️ This cycle — reported by three customers this week |
| | acme/site#441 | Add a "recently viewed" row to the listings page | `Backlog` | ⏸ Reporting refresh — no urgency, and it fits that theme better |
| | acme/api#224 | Document the search ranking fields | `Ready for Agent` | ➡️ This cycle — small, and unblocks acme/site#437 |
| | acme/infra#96 | Evaluate a managed search service | `Waiting on input` | ⏸ Apr 15 – Apr 28 — see Waiting on Input below |
| | acme/site#444 | Dark mode for the account pages | `Backlog` | 🚫 Closed, not planned — nobody has asked for it; reopen if that changes |

### Stale Issues

**58 stale business issues** across `Backlog` and `Ready for *`, untouched 8+ weeks; **7 newly
stale** since this cycle opened. 54 of the 58 are `Backlog`.

> Triage at this scale will not be fixed one issue at a time — acme/site#390 is the lever worth
> pulling, and its first child is committed this cycle.

**Close candidates**

| Epic | Issue | Title | Why it's a candidate | Decision |
| ---- | ----- | ----- | -------------------- | -------- |
| | acme/site#102 | Investigate an idea for the landing page | Open 14 months. The issue template was never filled in — every section is still an empty comment. | ✅ Closed, not planned |
| | acme/api#61 | Consider caching the catalogue response | Open 9 months, empty body, no comments. The title is the entire specification. | ✅ Closed, not planned |
| | acme/api#77 | Cache catalogue responses at the edge | Duplicates acme/api#61, filed later with more detail. | ✅ Closed as duplicate of acme/api#61 |

**Needs a cycle, not a close**

| Epic | Issue | Title | Why | Decision |
| ---- | ----- | ----- | --- | -------- |
| | acme/api#230 | Add retries to the nightly settlement export | `Ready for Agent`. Fully briefed and genuinely needed — finance re-runs it by hand every time it fails — but nine weeks without a cycle. | ➡️ This cycle |

**Newly stale, worth a look**

| Epic | Issue | Title | Why it's worth a look | Decision |
| ---- | ----- | ----- | --------------------- | -------- |
| | acme/infra#84 | Remove the old vendor's IAM roles | Went stale during the very cycle themed on the vendor migration. | ✅ Closed — the work was done and the issue was left open by accident |
| | acme/api#198 | Schema consolidation | An epic with six children and nothing committed. Real design discussion in the comments, and it looked close to agreement before it went quiet. | ➡️ Reporting refresh — commit its first child |

### Waiting on Input

| Epic | Issue | Question | Decision |
| ---- | ----- | -------- | -------- |
| | acme/infra#96 | Is moving search to a managed service worth the cost, or do we keep running it ourselves? | Worth doing eventually, but not now — revisit once search relevance work has settled and we know the real query load. Deferred to Apr 15 – Apr 28. |
| | acme/site#433 | Which customer segments should see the new pricing display? | Not resolved — nobody on the call had the definitive answer. Left as `Waiting on input`; it will reappear in next cycle's notes on its own. |

### Significant Dates

_Upcoming events to plan releases around._

| Date | Event | Note |
| ---- | ----- | ---- |
| Thu 26 Mar | Quarterly catalogue refresh | Highest-traffic day of the quarter. No deploys that day; the release goes out the following morning. |
| Mon 6 Apr | Finance close for Q1 | Refund and rounding behaviour must not change during that week. |

### Committed This Cycle

| Epic | Issue | Title | Status |
| ---- | ----- | ----- | ------ |
| acme/site#421 | acme/site#424 | Import stored payment methods into the new vendor | `In progress` |
| acme/site#421 | acme/site#425 | Cut over checkout to the new vendor's stored methods | `Ready for Agent` |
| acme/site#390 | acme/site#450 | Close the never-triaged issues older than a year | `Ready for Human` |
| | acme/api#219 | Split the checkout handler so failures are isolated | `In progress` |
| | acme/api#215 | Retire the vendor webhook shim | `Ready for Human` |
| | acme/api#224 | Document the search ranking fields | `Ready for Agent` |
| | acme/site#437 | Search returns nothing for hyphenated terms | `Backlog` |

## Future Work

_The two cycles after the current one. Committing work here now means it has a home when the current
cycle closes, rather than being re-argued every fortnight._

### Reporting refresh (1 Apr → 14 Apr 2026)

| Epic | Issue | Title | Status |
| ---- | ----- | ----- | ------ |
| acme/api#198 | acme/api#226 | Merge the two customer tables | `Ready for Human` |
| | acme/site#441 | Add a "recently viewed" row to the listings page | `Backlog` |

The listings redesign is already designed and underway in a pull request. It sits beneath
acme/site#441, along with acme/site#446 — "Sort recently viewed by last visit" — which was folded in
as part of that work.

### Apr 15 – Apr 28 2026

_No theme agreed yet, so the cycle carries its dates as a placeholder until one is._

| Epic | Issue | Title | Status |
| ---- | ----- | ----- | ------ |
| | acme/infra#96 | Evaluate a managed search service | `Waiting on input` |

## Out of Office

- **ALEX:** Out 24–26 Mar.
- No other absences reported for the current or upcoming cycles.

## Next Actions

_Each follow-up as **OWNER:** action, stated as the outcome rather than the mechanics. Tracker
writes default to the project manager, delegated to the agent as needed; name the person when it is
someone else's job._

- **SAM:** Email the team proposing that Apr 15 – Apr 28 be spent clearing work that was already in
  progress before cycles were introduced.
- **SAM:** Create an issue for the 26 Mar catalogue refresh — nothing on the board covers it.
- **ALEX:** Get a definitive answer on the pricing-display segments in acme/site#433 before the next
  meeting, and record it on the issue.
````

## Editing Discussions

Notes go in the
[**Meetings** category](https://github.com/orgs/clhbid/discussions/categories/meetings).

**Every org-wide discussion is hosted by the `clhbid/clhbid.com` repository**, whatever
`github.com/orgs/clhbid/discussions` implies. That is the repo the API addresses them through, and
it is why a bare `#<number>` in the notes resolves against `clhbid.com`.

`gh` has no discussion command, so use `gh api graphql`: `createDiscussion` and `updateDiscussion`
to write, `repository { discussion(number:) }` to read a body and its comments back.

## Iterating on the skill

**Fix the skill, not the output.** Whenever a draft needs hand-editing, that edit is a bug report.
Change the skill and re-run rather than patching the notes by hand.
