---
name: event-continuous-improvement
description: Turn several editions of a recurring technical event's debrief logs into operational trends and deliberate changes  -  a signal gate separating a one-off from a reproducible pattern, themes grouping differently-worded findings, recurrence counts across editions, a learning log persisted so it survives organizer turnover, an audit so it never grows unexamined, and a route from each resulting change to the sibling that owns it. Use whenever asked what keeps going wrong every year, how to stop relearning the same lessons, how to keep institutional memory across a team that turns over, or what several editions of evidence say to change next. Do NOT use for one edition's retrospective  -  use samber/dev-event-organizer-skills@event-debrief.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event Continuous Improvement

You own everything that crosses editions of a recurring technical event:

- Detect a trend across two or more dated debrief logs.
- Separate the findings that are noise from the ones that are signal.
- Persist the aggregate learning log.
- Audit that log so it stays trustworthy.
- Close the loop back to whoever owns the change.

**One edition is not yours.** `samber/dev-event-organizer-skills@event-debrief` runs the retrospective on one finished edition and hands you its dated log. Its own upstream boundary refuses cross-edition trending, because comparing one edition to the last two duplicates a sibling's whole reason to exist. Never re-run its analysis, re-open a single edition's findings, or produce the artifact it produces.

More scope arrives already owned. Read each sibling below, route to it, and never decide for it:

| Sibling                   | Owns                                                                          | You do                                                                                                                     |
| ------------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `event-market-fit`        | Demand-signal trends: sellout speed, sales-pace, return rate, sponsor renewal | Your trends are **operational** (desk overflowing again, same vendor failing twice) - state the split out loud on handover |
| `event-growth-strategy`   | Whether and how to scale                                                      | "Bottlenecks past 300 attendees" is evidence you hand it, never a recommendation                                           |
| `event-team-structure`    | Succession, bus-factor, burnout                                               | Notice the _same_ structural finding recurs across editions - the persisted log is itself a bus-factor mitigation          |
| `event-planning-timeline` | When the work happens                                                         | You decide what changes and why                                                                                            |
| `event-vendor-sourcing`   | One vendor's own performance record                                           | Route a rebook-or-not verdict there once it recurs; it is evidence for that vendor's file, not a general theme             |

Participant feedback never reaches you directly: `event-feedback` collects it, `event-debrief` reconciles it, and you only see what came through that log.

## What organizer guides cover, and where they stop

Say this out loud to the user, because it bounds every claim below.

- **One organizer guide covers the first handover, and the gap is narrower than it looks.** MLH's `Organizer-Resources/keeping-records.md` gives a cadence, an audience, two artifacts and a worked example, all of it edition-one-to-edition-two. DevOpsDays' `organizing.md` carries only one code-of-conduct line on the subject. Neither follows a finding from edition one to edition three or four. Full quotes and the worked example: [references/log-format-and-audit.md](references/log-format-and-audit.md).
- **The one real structural proof is a git history.** DevOpsDays' `organizing.md` is a single shared guidance document that survived repeated, complete organizer turnover through small targeted edits rather than periodic rewrites. That proves a persisted, collectively-edited document survives turnover; it is _not_ a template for a trend log's format, since it carries no dated per-edition entries and no trend annotations at all.
- **Two fragments carry over from software improvement practice, labelled as borrowed wherever they appear.** The loops themselves do not: a SaaS improvement loop assumes a per-run or per-quarter cadence, while an event improves once a year with a partly-turned-over team. What survives is `printing-press-retro`'s filing gate ([references/filing-gate-and-trend-evidence.md](references/filing-gate-and-trend-evidence.md)) and `ce-compound-refresh`'s Keep/Update/Consolidate/Replace/Delete classification ([references/log-format-and-audit.md](references/log-format-and-audit.md)).
- **One conference-management report names the practice itself, not its mechanics.** Fraser and Mancl's 2023 report on the future of conferences calls a retrospective "an essential management practice for conference stakeholders to drive ongoing improvements to a conference," run as an organizer meeting after the event and paired with a post-event survey to "identify trends (year over year)," explicitly framed for "a conference series." That backs holding the practice across editions at all. It supplies no cadence beyond "after the event," no per-edition log format, and no occurrence bar.

Naming the practice this way is sourced. The log format, the occurrence bar, the menus below and every template in `references/` are this skill's own construction. Do not present any of it as established organizer practice.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 5 to 7 exist because the menus below diverge sharply on time-to-effect, durability, and effort; the default ordering cannot be picked for the user without them.

1. How many editions has this event run, and for how many of them do you hold a written record? The second number is the only one that bounds a trend claim.
2. What form do those records take today - nothing written, a chat thread, one document per edition, or a structured record with fields?
3. How much of the organizing team has turned over since the earliest record you hold - nobody, some, most, or a full rotation to a different team - and is a handover to different people planned for this cycle?
4. Are the entries in `samber/dev-event-organizer-skills@event-debrief`'s three-part form with an owner and a date, or looser? Do comparable numbers exist across editions, or only prose findings? And has any past edition changed something deliberately _because_ of a logged finding?
5. When does next edition's planning start, or when is the go/no-go decided? That date is this skill's deadline; a trend that lands after the plan is written changes nothing.
6. Is this a one-off or closing edition, or a compounding one meant to run for years - and roughly how many more?
7. What is the effort ceiling between editions: hours available, and does anyone own a between-edition job today at all?
8. Where does the log live, and who is expected to open it before planning starts? Name a person. "The team" is the answer that produces a log nobody re-reads.

## Continuity or rotation

The filing gate, recurrence counting, theme grouping, the audit classification and the routing rules are byte-for-byte identical whether the event serves enterprise buyers or weekend hobbyists.

The axis that genuinely changes the output is **how much of the team is the same team next edition**, because it decides what the log has to carry:

- **Continuous team** - the same people run consecutive editions. Memory partly substitutes for the log, and that is the trap: the log stays thin precisely because nobody needs it yet. The gap surfaces only in the year someone leaves. Write for the successor who is not in the room.
- **Partial turnover** - the common case. Some findings live in the log, some live in one person's head, and nobody can tell which is which. Theme grouping earns its cost here: a returning organizer and a new one describe the same recurring failure in different words.
- **Full rotation** - a franchise, a rotating-city model, or an incoming team inheriting the event. The log is the entire transmission mechanism, not a convenience. DjangoCon Europe bolted on a support working group of previous organizers plus a standing events-support function for exactly this case, since the written record alone could not carry it.

## Workflow

1. Run the interview. If the answer to Q1 is one edition of records, stop the trend work and say so: file this edition, start the log, and come back next year. Half of this skill is unavailable and pretending otherwise manufactures a pattern.
2. **Receive the log, do not re-run it.** Take `samber/dev-event-organizer-skills@event-debrief`'s dated log per edition as given. If an entry is thin or unclear, note the gap; never reconstruct the edition it came from.
3. **File every entry through the signal gate.** Borrowed from the `printing-press-retro` filing gate: an entry becomes a candidate only when it is reproducible in the event's own conditions and generalizes beyond one occurrence. A one-time failure that was handled and cost nothing is expected work, not a finding. De-personalise as you file: `samber/dev-event-organizer-skills@event-debrief`'s blameless frame has to survive into a document that outlives the people in it. Gate criteria, worked positive and negative filings, and the de-personalisation rule: [references/filing-gate-and-trend-evidence.md](references/filing-gate-and-trend-evidence.md).
4. **Group before you count.** Cluster differently-worded entries into themes, then count the theme's recurrence rather than the entry's. Two occurrences make a candidate; three make a pattern. Say which of the two you are holding every time you state a trend.
5. **Decide what changes, one deliberate change at a time.** Resist bundling: a plan carrying four simultaneous changes cannot attribute any outcome to any of them. Write every change in three parts:
   - What you are changing.
   - Why the evidence justifies it.
   - How you will know next edition whether it worked.
6. **Route each change to its owner.**
   - Operational change: `samber/dev-event-organizer-skills@event-planning-timeline`, as a real task on next edition's plan.
   - Anything shaped like demand: `samber/dev-event-organizer-skills@event-market-fit`.
   - Anything shaped like size: `samber/dev-event-organizer-skills@event-growth-strategy`.
   - Anything structural and recurring: `samber/dev-event-organizer-skills@event-team-structure`, carrying the recurrence count as the evidence a single debrief could not produce.
   - Anything naming one supplier's own performance, such as rebook or not, a brief to rewrite, a quantity to change: `samber/dev-event-organizer-skills@event-vendor-sourcing`, filed on that vendor's own record rather than left in the general log where next edition's buyer will not think to look for it.
7. **Persist the log** at the rung chosen from the first menu below, and name it to the team as the bus-factor mitigation it is.
8. **Audit the accumulated log** at the cadence chosen from the third menu. Classify every entry as Keep, Update, Consolidate, Replace or Delete, borrowed from `ce-compound-refresh` with one honest amendment: its ground truth is a codebase that can be checked at any time, while yours is next edition's own outcome, which only exists after the fact. The audit is therefore retrospective, never continuous. Format, classification rules and the handover packet: [references/log-format-and-audit.md](references/log-format-and-audit.md).
9. **Close the loop.** Before the planning cycle ends, state which of last cycle's deliberate changes shipped and what happened. An improvement loop that never checks its own output is a filing system.

If your harness has persistent memory, record the log itself: every filed entry with its theme, first-seen edition and occurrence count; every deliberate change with its justification and check; every routing hand-off. This is the one skill in the collection whose value depends entirely on the record surviving between runs a year apart, readable by someone who was not there when it was written.

Every ranking below is a default, not a law. Where a constraint deletes a rung, strike it from that menu's axis lines too: a rung left in the ordering survives in the reader's head and returns as scope. Re-rank all three menus against what you already know about this team.

- A shared version-controlled document already buys the persistence rungs cheaply.
- One person running every edition has no theme-grouping problem yet, and a worse turnover one.
- A team that never shipped a deliberate change has nothing to audit or close.

## Log persistence posture

Ranked menu - cross-edition trends that hold up and survive turnover, bought per unit of standing upkeep. The rungs and the orderings are this skill's own construction, not a published standard: organizer guides offer timeless how-to guidance, not a dated learning log to copy.

- effort (setup, per-edition upkeep, retrofitting what already exists): `structured entry record > numeric series > appended document > carry-forward only`
- value (patterns detectable at all, and readable by someone who was not there): `structured entry record > appended document > numeric series > carry-forward only`
- efficiency: `appended document > structured entry record > numeric series > carry-forward only`

Value and effort differ in the middle, which is the point of splitting them. The numeric series costs more than the appended document, because the numbers must be measured the same way every edition or someone reconstructs them. It also buys less: operational trends are prose ("the desk overflowed again"), and numbers mostly answer the demand question owned by `samber/dev-event-organizer-skills@event-market-fit`. Carry-forward sits last on efficiency despite costing almost nothing, because it buys nothing that crosses editions, and zero over zero never wins a ratio.

- **Carry-forward only** - re-read the most recent edition's debrief log when planning opens. Nothing is aggregated; recurrence lives in whoever happens to remember it.
- **Appended document** - one running dated document; each edition appends its filed findings under a dated heading. Real structural evidence backs this rung: DevOpsDays' organizing guide survived eleven years and 20+ contributors as exactly this kind of document. Borrow only its survival property, never its timeless-guidance format.
- **Numeric series** - a small table of the same handful of numbers per edition, drawn from the goals each debrief measured itself against.
- **Structured entry record** - every filed finding carries fields: theme, first-seen edition, occurrence count, status, disposition, owner. Recurrence becomes countable instead of remembered. Describe it as a record, whatever the team already uses; never prescribe a tool.

**Default rung: the appended document**, from the second edition of records onward. **Starved option: the structured entry record** - first on value, first on effort, so efficiency never picks it. Promotion conditions, and which rungs to delete outright on a thin or inconsistent record: [references/reranking-by-interview-answers.md](references/reranking-by-interview-answers.md).

## Trend-detection depth

Ranked menu - defensible patterns bought per unit of analysis time. The rungs and the orderings are this skill's own construction. The two-versus-three occurrence rule tracks a much older cross-domain convention for separating coincidence from pattern, "twice is a coincidence, three times is a pattern", rather than an event-industry-specific calibration. No organizer guide sets this number itself, and the gate it feeds is borrowed from software practice.

- effort (reading, clustering, assembling evidence): `written trend review > paired numeric read > theme grouping == recurrence count`
- value (deliberate changes that survive contact with the plan): `written trend review > theme grouping > recurrence count > paired numeric read`
- efficiency: `theme grouping > recurrence count > written trend review > paired numeric read`

The effort tie is argued, not indecision: counting happens _during_ clustering, since you cannot group a theme without counting its members. The marginal cost of grouping over counting is one judgment call, not extra hours, and value then breaks the tie cleanly.

- **Recurrence count** - count how many editions each filed entry appears in, as written.
- **Theme grouping** - cluster entries describing one underlying cause (badge printing, desk queue, and lanyard sorting are one check-in theme), then count the theme. It beats raw counting on value because the same failure is described in different words each edition and by each organizer. Counting entries under-detects exactly the recurring problems you are looking for.
- **Paired numeric read** - put a theme's recurrence beside the numbers from the same editions to see whether it tracks anything measurable. Lowest on value here: a number rarely arbitrates whether the check-in desk failed again, and where it does move, the reading usually belongs to `samber/dev-event-organizer-skills@event-market-fit`.
- **Written trend review** - a short document per planning cycle: each candidate trend, its evidence per edition, its disposition, circulated before the planning kickoff.

**Default rung: theme grouping**, with recurrence counted on themes rather than raw entries. **Starved option: the written trend review** - first on value, first on effort, so efficiency never picks it. Promotion conditions, and which rungs to delete outright: [references/reranking-by-interview-answers.md](references/reranking-by-interview-answers.md).

## Log-audit cadence

Ranked menu - a log the team still trusts at edition five, bought per unit of standing overhead. The classification is borrowed from `ce-compound-refresh`. The cadences, the rungs and the orderings are this skill's own construction.

- effort (calendar, ownership, per-pass hours): `standing audit owner > kickoff pass plus closure pass > kickoff pass > audit on read`
- value (entries that are still true, and a log short enough to be re-read): `kickoff pass plus closure pass > standing audit owner > kickoff pass > audit on read`
- efficiency: `kickoff pass > kickoff pass plus closure pass > audit on read > standing audit owner`

Value and effort disagree at the top for a domain-specific reason: the only ground truth here is next edition's own outcome, so an audit _timed to that outcome_ verifies something a calendar-interval audit cannot, at less cost than owning the log year-round. That puts the closure pass above the standing owner on value while below it on effort, and is why efficiency still leads with the plain kickoff pass.

- **Audit on read** - classify only the entries you happen to touch during a trend pass. Everything else accumulates unexamined.
- **Kickoff pass** - one pass over the whole log before planning opens, classifying every entry as Keep, Update, Consolidate, Replace or Delete.
- **Kickoff pass plus closure pass** - the same pass, plus a second one after the edition ships, classifying the entries behind each deliberate change against what actually happened. Its cheapest form reopens the same change record and appends two columns rather than drafting a separate report: **did this actually improve, yes or no**, and **why**. The record then becomes its own verification instrument instead of a second document nobody reads.
- **Standing audit owner** - a named person owns the log year-round on a fixed interval, independent of the planning calendar.

**Default rung: the kickoff pass.** **Starved option: the standing audit owner** - first on effort, second on value, last on efficiency, so the ratio never picks it. Promotion conditions, and which rungs to delete outright: [references/reranking-by-interview-answers.md](references/reranking-by-interview-answers.md).

## Re-ranking against the interview answers

Re-rank all three menus above against Q1, Q3, and Q5 to Q8, and say out loud which answer moved which option rather than silently reordering. Full breakdown, menu by menu and answer by answer: [references/reranking-by-interview-answers.md](references/reranking-by-interview-answers.md).

## Failure modes

- **Trending on two data points.** Two occurrences are a candidate; a trend claimed from them is a coincidence with a plan attached. Say "candidate" and hold it for one more edition unless the cost of being wrong is trivial.
- **Re-doing the debrief's work.** Re-analysing a single edition, re-scoring its risks, re-writing its entries - all of it belongs to `samber/dev-event-organizer-skills@event-debrief` and produces a second version of the same document nobody adopts. Take the log as given.
- **Treating a demand trend as operational.** "Fewer people came back" is a demand signal for `samber/dev-event-organizer-skills@event-market-fit`. "Check-in took ninety minutes for the third year running" is yours. Getting this backwards produces an operational fix for a demand problem - the event runs beautifully for an audience that has stopped coming.
- **A log nobody re-reads before planning.** The most likely failure of all, because it looks like success: the record exists, it is well-formed, and the planning meeting runs entirely on the loudest memory in the room anyway. Name the person who opens it, and the moment they open it.
- **A log that only grows.** This is the failure above reached by a second route. Without the audit, a superseded entry from three editions ago still reads as live, and the log gets too long for anyone to re-read. Audit it so no entry sits unexamined.
- **Bundling four changes into one edition.** Nothing can then be attributed, and next cycle's closure pass has no verdict to give. One deliberate change at a time is what makes the loop measurable at all.
- **Naming people in a persisted log.** A performance criticism that was uncomfortable in the room becomes indefensible in a document read by people who never met the person. File the structural finding, route it to `samber/dev-event-organizer-skills@event-team-structure`, and keep the name out of the record.
- **Borrowing a cadence from software.** Quarterly reviews, per-sprint retros and per-run gates all assume a cycle far shorter than one edition. Take the filing discipline; leave the calendar.
- **An artifact kept for appearances after nobody uses it as designed.** A scoring sheet, a checklist or a process step the team quietly stopped following in full is a finding about the artifact, not about the team. Audit it the same pass, and fix it one of two ways, never a third: make the design's own output visible enough that skipping it is no longer possible, or simplify the design down to what people actually do. Keeping the unused version because rewriting it feels like admitting failure is the failure.

## Measurement

Start with what the guidance reaches, because it decides which numbers this skill is entitled to set. MLH's organizer guide covers the first handover: its cadence, its artifacts and its worked example are all edition-one-to-edition-two. **Everything past that handover is a threshold you set**, and importing a target from software continuous-improvement tooling would present a borrowed number as organizer practice.

That leaves one number worth fixing. This skill sets **exactly one pass threshold**, on the only thing fully inside the team's control:

- **Zero unclassified entries after an audit pass** (self-set, binary). Every entry in the persisted log carries Keep, Update, Consolidate, Replace or Delete, and a live entry carries its theme and occurrence count. Iterate until it holds. A log failing this is an archive, and an archive is what nobody re-reads.

The rest are signals to record, not targets to hit:

- **Editions of records held** (self-set). Every trend claim is bounded by this number; record it beside the claim.
- **Share of deliberate changes traceable to a filed pattern** (self-set), rather than to an opinion in the planning room. A low share means the log is decoration.
- **Closure rate on last cycle's changes** (self-set): how many shipped, and how many had their outcome checked. `samber/dev-event-organizer-skills@event-debrief` records per-edition carry-through; the trend across editions is yours.
- **Whether the log was opened before planning, and by whom** (self-set, binary per cycle). Blunt, and the single best predictor of whether any of this worked.

## Invocation examples

- "This is our fourth edition and I swear registration has broken every single year. How do we actually fix it instead of rediscovering it?"
- "We have three years of retrospective notes in a shared doc nobody opens. What do we do with them before planning starts?"
- "Half the organizing team is new this year. How do we stop them from relearning everything the hard way?"
- "We changed the schedule last edition because of feedback. How do we tell whether it worked?"
- "Our learning log is forty entries long and I don't think half of it is still true."
- "Attendance dropped for the second year. Is that something this skill handles?"

Expected output:

- A filed set of entries grouped into themes, each with an occurrence count and a candidate-or-pattern label.
- A short list of deliberate changes with the evidence behind each and the check that will confirm it.
- Routing hand-offs to the siblings that own the demand, size, structural, vendor and scheduling consequences.
- A persistence rung and an audit cadence chosen with their reasons.
- Every claim marked as either published organizer practice or this skill's own judgment.

## See also, same collection

Sibling skills referenced throughout: see the sibling table at the top of this file. One more sits outside it: `samber/dev-event-organizer-skills@event-budget` plans and tracks one edition's money, and a cost line creeping edition over edition is this skill's trend to read, never that skill's to re-model.
