---
name: event-talk-selection
description: Run the review and selection process on CFP submissions a technical event already collected - committee composition, how blind review executes (platform hiding versus a dedicated anonymizer role) and what it cannot fix, scoring rubrics, multi-round score-to-shortlist-to-program-fit cascades, conflict-of-interest recusal, diversity and first-time-speaker balancing, acceptance-rate management, and accept/decline/waitlist communication. Use whenever the user mentions a program committee, a talk rating grid, blind CFP review, choosing which submitted talks make the programme, reviewer conflicts of interest, or acceptance and rejection emails - even if they never say "selection". Do NOT use to design the call itself - use samber/dev-event-organizer-skills@event-cfp-design.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Talk Selection

You run the review process on proposals a call for papers already collected: who reviews, on what scale, in how many rounds, and what every submitter hears back.

This skill does not:

- Design the call. Its timeline, form, published criteria, and anonymization _policy_ belong to `samber/dev-event-organizer-skills@event-cfp-design`; you inherit that policy rather than re-deciding it.
- Recruit speakers outside the call. That parallel channel is `samber/dev-event-organizer-skills@event-speaker-sourcing`, and invited proposals need an explicit rule for how they enter your pipeline (see the workflow).
- Place accepted talks into the grid. That is `samber/dev-event-organizer-skills@event-schedule-design`.
- Judge projects built during a hackathon. That runs on a structurally different, same-day timeline: `samber/dev-event-organizer-skills@hackathon-judging`.

Every ranking below is a default, not a law: it shifts with context and with who executes it. After the interview, re-rank all three menus against what you already know about this organizer - any of these can overturn a default rung:

- A committee that already exists.
- A tool already paid for.
- A community small enough that reviewers recognize submitters by writing style.
- A hard program-announcement date.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 3-5 exist because the menus below diverge sharply on time-to-effect, durability of the payoff and effort - those rankings cannot be picked for the user.

1. How many submissions arrived, for how many slots? (The ratio sets the whole process: a 40-proposal pool and a 2,500-proposal pool are different problems, not the same problem at different sizes.)
2. What did the published call promise about anonymization, review criteria and notification date? Read the call before designing anything - the process must execute what was published, not what would be convenient.
3. What is the program-announcement date, and how many weeks remain? (A hard date deletes rungs rather than compressing them.)
4. Is this a one-off edition or a compounding annual asset? (A compounding mandate promotes the slow rungs: per-proposal feedback, a real committee, a documented rubric that holds year over year.)
5. What is the effort ceiling: how many people will actually read proposals, for how many hours, and who arbitrates a deadlock?
6. Who owns the event - community conference or vendor/user conference? (See the split below.)
7. Are there invited or sponsor-adjacent talks in the same program, and does the call say how they interact with the open pool?
8. Which balance goals are stated: first-time speakers, under-represented speakers, local versus out-of-town, topic and employer spread? Which were published, and which are internal?
9. What already exists that should re-rank the menus: a returning committee, last edition's rubric and its complaints, a CFP tool with a review mode, an archive of past decisions?
10. Does the submission form also carry financial-assistance or travel-grant requests?
11. Is this a multi-track program, or single-track?

## Community vs vendor conference

Who owns the event changes selection, the same replacement this collection's format and CFP skills argue:

- **Community conference** - the open pool is the program. The hard line is: "no speaker spots can be bought by sponsors: not ever - period". Everything sourced in this skill comes from this pole.
- **Vendor/user conference** - content is mostly invited and organized around the vendor's architecture; review runs over a community slice of an otherwise curated program. The mechanics below still apply to that slice, but the balance pass answers to the vendor's narrative as well as the audience's.

Say which pole a recommendation assumes when they differ.

## Workflow

1. Run the interview. Read the published call first (Q2) - everything downstream must honour it.
2. Pick the committee model from its menu below, and size it against the pool (Q1) and the effort ceiling (Q5).
3. Take the rubric that goes with that model (see Scoring rubric - it follows the committee, it is not a free choice). Write it down before anyone scores. A rubric invented mid-review re-scores whatever was read first.
4. Set the anonymization execution depth from its menu, inside the policy the call published. Assign a named person to it. If the call promised blind review, decide now - in writing - at which step identity re-enters, and for whom.
5. Brief reviewers on conflict of interest before scoring opens, not after a conflict surfaces (see below). Name the fallback for a proposal that loses too many reviewers to recusal.
6. Run round one: every proposal scored on the rubric, with written comments attached to every score. Mandatory comments are established practice and are what makes rounds two and three, and any real decline feedback, possible at all.
7. Cut to a shortlist on score. State the cut as a rule before seeing the ranking - a threshold or a percentage - so the line is not drawn around a favourite.
8. Run the program-fit pass on the shortlist, not on the whole pool: topic spread, employer spread, local versus out-of-town, first-time speakers, and however invited talks were decided in Q7. This is the step where a score-rank list becomes a program. It is also the least documented step in the field (see failure modes) - write down what you traded and why, because next edition's committee will ask.
9. Fill the slots, then build the waitlist before sending anything. Keep the backup list explicitly ordered.
10. Notify, in this order:
    - Acceptances first, with a confirmation deadline.
    - Declines only once acceptances are confirmed.
    - Waitlisted submitters, told plainly that they are waitlisted, by when they will know, and that a slot may never open.
11. Hand the accepted list, with format and track tags, to `samber/dev-event-organizer-skills@event-schedule-design`. Record the acceptance ratio and the balance outcome for next edition.

Present the design section by section for validation - committee, rubric, anonymization, cut rule, communication plan - before review opens. Once scoring starts, changing the rules invalidates whatever was already read.

If your harness has persistent memory, record the rubric, the cut rule, the acceptance ratio, the balance outcome, and the specific complaint each would need to hear to change next edition.

## Review committee model

Ranking (default, not a law - Q1, Q3, Q5 and Q9 re-rank it):

- effort (reviewer headcount, coordination, rounds, calendar): `multi-tier cascade > small consensus committee > solo curation`
- value, defensibility and bias dilution: `multi-tier cascade > small consensus committee > solo curation`
- value, program coherence: `solo curation == small consensus committee > multi-tier cascade` - the tie is argued, not a dodge: both keep every decision inside one room where the whole program stays visible at once, and that is the only thing this axis measures. The cascade cannot match it at any headcount, because its later tiers only ever see what earlier tiers passed up.
- efficiency: `small consensus committee > solo curation > multi-tier cascade`

**Dominance check: 3 pairs, zero strict-dominance relations.** Clean only by construction, and by-construction is never a pass. Two mechanisms block the three:

- The cascade against each of the other two rungs is blocked by opposed value axes: it leads on defensibility and trails on coherence.
- The remaining pair, committee against solo curation, is blocked by effort alone: the committee is ahead on defensibility, tied on coherence, and still costs more.

The check catches no misordering. The efficiency line rests on the arguments below.

- **Small consensus committee** - the default and most documented at small scale: a dedicated non-voting anonymizer plus roughly four to six graders, one synchronous discussion round, a letter-grade advocate scale, and a backup list of about five talks. Fits a single-track or two-track event whose whole pool one room can read.
- **Solo curation** - one organizer, or a pair, hand-picks the lineup: near-zero coordination cost, defended by single-track organizers as editorial responsibility rather than a shortcut. Legitimate for an invitation-led or micro-scale program. **Delete it rather than demote it** when the call published open criteria and a blind-review promise: a single reader cannot run blind review on themselves and cannot be recused, so keeping the option parked at the bottom quietly reintroduces the process the call ruled out.
- **Multi-tier cascade**, the starved option: highest on both defensibility and effort, so efficiency never picks it. The established shape:
  1. Track committees score.
  2. The top-scoring 30% advance to track chairs.
  3. Track chairs pass roughly 30% of those on, with mandatory comments.
  4. Co-chairs make the final call.

  Promotion conditions:
  - A multi-track program (Q11).
  - A pool no single room can read.
  - An event whose decisions must survive public scrutiny from competing employers.

Sizing note: the numbers above are two documented points - roughly five reviewers at small-scale single-track conferences and a three-tier structure at large multi-track events. A third, distributed-pool model (below, under Scoring rubric) supplies the one real reviewers-per-proposal figure in this evidence base: three or more reviews before a submission stops being actively surfaced for further review. No defensible curve exists between the three points - interpolate against your own reading capacity and say that you are doing so.

## Scoring rubric

The rubric follows the committee model rather than being ranked separately; ranking options whose choice is already determined upstream would be false precision. Three established rubrics exist, each built for a different room:

- **Letter-grade advocate scale**, for a committee that will meet and discuss:
  - A: will actively advocate.
  - B: likes it, won't advocate.
  - C: neutral.
  - D: will advocate against.
  - X: abstain, the reviewer suspects they have identified the speaker.

  Grades aggregate as a best-worst pair per proposal ("AC"), never as an average, and at least one A is the practical floor for serious consideration. It measures advocacy, which is exactly what a discussion round spends.

- **Multi-criteria star scale**, for reviewers who will never meet: five stars in half-star steps across content, originality, relevance and speaker fit, with mandatory written feedback on every rating. It measures comparability, which is what an aggregated cut needs.

- **Numeric 0-3 scale**, for a distributed reviewer pool assigned through a review platform rather than a fixed committee: each score carries a written meaning (no-strong, no-indifferent, yes-indifferent, yes-strong), a comment is mandatory on every review, and a submission stops being actively resurfaced once it holds three or more reviews. It measures a straightforward accept/reject lean at platform scale, without either the letter scale's advocacy signal or the star scale's four-criteria breakdown.

Averaging the letter scale, discussing your way past the star scale, or collapsing the numeric scale's four meanings into a bare "high/low" read throws away the property each was built for. Full criteria wording, the aggregation mechanics and a worked example are in [references/committee-models-and-rubrics.md](references/committee-models-and-rubrics.md).

## Anonymization execution

The call already chose the policy. This menu is only how deeply you execute it.

Ranking (default, not a law):

- effort (per-submission handling, role separation, speaker instructions): `dedicated anonymizer > platform-level hiding > named review`
- value, leak resistance: `dedicated anonymizer > platform-level hiding > named review`
- value, information available while scoring: `named review > platform-level hiding > dedicated anonymizer` - no tie here: platform hiding withholds the author field but leaves intact whatever the submitter wrote into the title, abstract or outline, while the anonymizer rewrites those too. Reviewers genuinely see less under the anonymizer, and that loss is the rung's cost rather than a rounding difference.
- efficiency: `platform-level hiding > named review > dedicated anonymizer`

**Dominance check: 3 pairs, zero strict-dominance relations.** Clean only by construction, and that is not a pass. One mechanism blocks all three pairs: the two value axes are exact reverses, so whichever rung resists leaks better shows reviewers less, and no rung can be at least equal on both.

Effort is never reached in any pair, and no third axis is printed. The check finds nothing; the ordering is argued below, not verified.

- **Platform-level hiding** - the default where the call promised blind review: the tool withholds author information during initial review (opt-in anonymous modes ship in the common CFP platforms). Its documented limit, which must be stated to submitters before the call closes rather than discovered during review: the platform hides the author field, not what the author wrote into the title, abstract or outline.
- **Named review** - the default where the call did not promise anonymization, and the field norm in practice. Only honest when the published criteria carry the fairness load the anonymity is not carrying.
- **Dedicated anonymizer**, the starved option: one or two people see raw submissions and never score any of them. They rewrite identifying details into bracketed placeholders, deliberately preserve identity where it is the talk's own subject, and assign random IDs so submission order cannot re-identify anyone. Highest leak resistance, highest effort, so efficiency never picks it. Promotion conditions:
  - A committee small enough to recognize regulars regardless of what the tool hides.
  - **Keyed to Q10**: financial-assistance requests riding on the same form, where anonymization is the enforcement mechanism for the promise that asking for money does not hurt a proposal.
  - A community with a live fairness complaint from last edition.

**Delete, do not demote:** if the call published named review, anonymization is off the menu for this edition. Retrofitting it mid-review anonymizes nothing - reviewers have already read names - and it breaks the promise the call actually made.

**State this limit out loud, in the plan and to the committee.** No evidence exists measuring whether anonymized review changes acceptance outcomes by demographic.

What exists is stated organizer intent and mechanism design, nothing more. Blind review is defensible as a process commitment; presenting it as a proven equity outcome is a claim the evidence does not support.

## Conflict of interest

The established rule is self-administered, and it covers two distinct failures - both belong in the reviewer brief:

- Reviewers are told to skip the question - abstain from scoring rather than score and disclose - for submissions from colleagues they work closely with, or organizations they are associated with or competing against. Review "wearing your event hat" rather than an employer's.
- Abstain when you suspect you have identified an anonymized speaker.

The two cover different failures.

The honest limit: both are honour-system recusals. No declared-conflict registry, escalation path or audit mechanism exists published anywhere, so treat any escalation procedure you add as your own design, and say so. Decide two things in advance, rather than mid-dispute:

- Who arbitrates when a reviewer will not recuse.
- What happens to a proposal that loses so many reviewers to recusal that its scores are no longer comparable.

## Waitlist and declines

Build the waitlist before notifying anyone. One documented size is about five backup talks for a single-track program; scale it to your decline risk, and say that you are extrapolating. No published data exists on how often a waitlisted talk is actually promoted, so never tell a waitlisted speaker their odds - tell them the date they will know.

Ranking of decline-communication depth (default, not a law - Q4 and Q5 re-rank it):

- effort (organizer time per decline, multiplied by a pool that is mostly declines): `per-proposal feedback > decline plus criteria recap > form decline`
- value (submitters who return next edition, and the reputation that fills next year's pool): `per-proposal feedback > decline plus criteria recap > form decline`
- efficiency: `decline plus criteria recap > form decline > per-proposal feedback`

**Dominance check: 3 pairs, zero strict-dominance relations.** Clean only by construction, and that is never a pass.

Value and effort share one ordering, so a single mechanism blocks every pair: the rung that brings more submitters back costs strictly more organizer time per decline. Nothing else is printed that could block or rescue a pair. The efficiency line rests entirely on the arguments below.

- **Decline plus criteria recap** - the default: one warm template, plus the criteria the call published and the acceptance ratio. The ratio is doing real work - it reframes a no as arithmetic rather than a verdict, at no extra cost per submitter.
- **Form decline** - a short, kind, identical note. Cheap and honest; it just buys nothing beyond not being silent.
- **Per-proposal written feedback**, the starved option: the reviewer comments, edited for tone. Promotion conditions:
  - A pool small enough to write them all.
  - A first-time-heavy pool where growing the speaker base is the point.
  - A rubric that already mandates written comments, where the text exists at near-zero marginal cost and only editing remains.

  At least one common CFP platform can attach individual feedback to decline notifications, so the constraint is editorial time, not mechanism.

One structural detail worth copying from a blind process: accepted speakers are de-anonymized because someone must coordinate logistics, while declined submitters are notified without the review team ever learning who they were. Decide which of your own people ever sees a declined submitter's name. Templates and sequencing are in [references/decision-communication.md](references/decision-communication.md).

## Failure modes

- **Anonymization theater.** Blind review announced, then identity re-entering with no published phase boundary, or free-text leaks left unmanaged because the tool "handles it". Publish where identity enters, or run named review honestly.
- **Rubric-free consensus.** A committee that meets and talks without a written scale converges on whoever argues hardest and cannot explain a decline six months later. Write the scale down before scoring opens.
- **Conflict of interest by omission.** No brief, no recusal rule, and a reviewer scoring a colleague's proposal because nobody said not to. The rule costs one paragraph and only works before scoring, not after.
- **Waitlist promises.** "You're first in line" and "we'll definitely have room" are commitments nobody can keep. Promise a date, never a probability.
- **Silent balance.** A program-fit pass that trades a higher-scored talk for spread and writes nothing down. Next edition's committee re-litigates it blind, and the submitter who asks gets an answer nobody can give.
- **Reading oversubscription as a track shortage.** A high submission-to-slot ratio is a demand signal, not a live cue to add a track mid-cycle. The track count was fixed upstream by `samber/dev-event-organizer-skills@event-format-selection`; the demand read belongs to `samber/dev-event-organizer-skills@event-market-fit`.
- **Reviewing invited talks in the same pool.** An invited speaker's identity is the reason they were invited, so they cannot be blind-reviewed alongside the open pool without corrupting both. Decide their lane in advance (Q7).

## Measurement

Sourced figures are labeled; everything else is a gate you set yourself and should mark as such when you present it.

- **Acceptance ratio** (calibration reference, not a target):
  - PyCon US 2025 selected 15% of 938 proposals.
  - KubeCon EU 2024 accepted 9% of 2,541.
  - Academic venues run higher - CHI 2024 at 26.4% - on a different selection logic that does not transfer.

  Record yours; a ratio that swings hard between editions usually means the call changed, not the pool.

- **Balance outcome against stated goals** (mixed): count first-time speakers, employer spread and local/out-of-town share in the accepted set and compare to what was promised. One documented quantified target exists at event level - "at least 50% of speakers who are new speakers if possible" plus at least 25% from end-user companies - and notably it is not a line item in the rubric reviewers actually see. If you set a target, decide before review whether it is a goal or a gate.
- **Reviewer coverage** (self-set): proposals per reviewer, and how many lost reviewers to recusal. A committee that cannot read the pool inside the calendar is a process failure discovered too late.
- **Declined-submitter return rate** (self-set): how many declined submitters submit again next edition. It is the only real test of whether the decline communication rung was worth its cost.

Pick two or three, write down the revision each would trigger, and record them before the event rather than after.

## Invocation examples

- "We got 180 proposals for 24 slots and five organizers who can review - how do we run this?"
- "Set up the review committee and rating grid for our two-track conference CFP."
- "Our CFP promised blind review. How do we actually run it, and what does it not fix?"
- "One of our reviewers works with a submitter. What's the rule?"
- "Write the acceptance, decline and waitlist emails, and tell me what order to send them in."

Expected output: a selection plan with:

1. The committee model and size, with named roles.
2. The rubric, written out.
3. The anonymization execution depth, and the exact step identity re-enters.
4. The conflict-of-interest brief and its arbitration fallback.
5. The round structure and the cut rule, stated before ranking.
6. The program-fit pass, with its trade-offs recorded.
7. The waitlist and the notification sequence, with draft copy.
8. The metrics to record for next edition.

Present it section by section for validation before review opens.

## References

- [references/committee-models-and-rubrics.md](references/committee-models-and-rubrics.md) - both established rubrics verbatim with their criteria wording, the cascade's percentage stages, the letter-scale aggregation mechanic, committee roles, and a worked positive/negative scoring example.
- [references/decision-communication.md](references/decision-communication.md) - accept, decline and waitlist templates, the notification sequence and de-anonymization asymmetry, per-speaker duplicate-acceptance handling, and the tooling capabilities the flow needs.
- [references/selection-evidence-and-gaps.md](references/selection-evidence-and-gaps.md) - acceptance-rate and oversubscription benchmarks, diversity rules and targets, the panel composition rule, and an explicit list of what this domain does not document.

See also, same collection:

- `samber/dev-event-organizer-skills@event-cfp-design` - designs the call whose policy this skill executes: timeline, form, published criteria, anonymization policy.
- `samber/dev-event-organizer-skills@event-speaker-sourcing` - the invited-speaker channel that merges into this program; decide its lane before review opens.
- `samber/dev-event-organizer-skills@event-speaker-experience` - picks up at the acceptance email's "what we need next" line: collects those materials and runs everything after. It never touches decline or waitlist messaging, which stays here.
- `samber/dev-event-organizer-skills@event-schedule-design` - places the accepted list into the track structure downstream.
- `samber/dev-event-organizer-skills@hackathon-judging` - judges projects built during an event, on different criteria and a same-day timeline; distinct from reviewing a talk proposal.
- `samber/dev-event-organizer-skills@workshop-program-design` - owns the format-specific questions a hands-on proposal raises that a talk proposal does not: whether the instructor can run it at the capacity offered, and whether the exercise scales to the room.
