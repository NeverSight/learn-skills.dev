---
name: hackathon-brief-design
description: Write the hackathon challenge document teams read before they build - problem statements sized to the time box, thematic challenge tracks, the published rules and eligibility text, the submission-artifact checklist, sponsor-challenge framing, and naming (never weighting) the evaluation categories. Use whenever the user mentions a hackathon brief, challenge or track prompts, hackathon rules or eligibility, submission guidelines, or turning a sponsor's API into a challenge - even if they never say "brief". Challenge tracks here are thematic categories a team enters, not parallel session streams. Do NOT use for rubric weights and judging mechanics - use samber/dev-event-organizer-skills@hackathon-judging instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Hackathon Brief Design

You write the document a hackathon hands its teams: what to build, under which rules, who may enter, what to submit, and what "good" will be called. It is the only artifact every participant reads, and every dispute at the ceremony traces back to a sentence it did or did not contain.

## What "track" means here

A **challenge track** is a thematic category a team enters its project into: an AI track, a sponsor's API track, a beginners track. It is a content and prize construct.

`samber/dev-event-organizer-skills@event-format-selection` uses "track" for parallel session streams, single-track versus multi-track programming. Same word, different concept.

Write **challenge track** wherever a reader could take the other meaning. A session-track decision settles nothing here.

## What you own, and what is already decided

You own the written brief:

- problem statements
- challenge-track content
- rules and eligibility text
- the submission checklist
- sponsor-challenge framing
- the _names_ of the evaluation categories

Three things arrive already decided. Publish them rather than re-open them.

- **The demo/judging structure** (expo table, stage pitch, video-only, or the two-stage hybrid) belongs to `samber/dev-event-organizer-skills@event-format-selection`. Translate it into the submission checklist and the deadline rather than pick it: a video-only event makes the video the deliverable, an expo event makes it optional. Deliverable format is downstream of that choice, never an independent one you make here.
- **Criteria weights, the scale, judge allocation, tie-breaks and disputes** belong to `samber/dev-event-organizer-skills@hackathon-judging`. That skill states the boundary from its own side: the evaluation categories named in the published brief are yours, and it weights them and builds the mechanics on top. Name the categories, and never print a weight, a scale or a points total.
- **Prize amounts, cash-versus-in-kind and payout handling** belong to `samber/dev-event-organizer-skills@hackathon-cash-prize`. Write "each challenge track awards a prize"; never write the figure.

Every ranking below is a default, not a law. Re-rank each menu after the interview against what you already know about this event:

- last edition's published rules
- a signed sponsorship agreement
- an organizer who has run this API before
- a beginner-heavy audience

## Interview

Ask one question at a time, multiple-choice where possible. Questions 3-5 and 8-9 decide which rung each menu defaults to; the defaults cannot be picked without those answers.

1. How long is the hacking window in hours, and is the event in person or fully digital?
2. Which demo/judging structure is already chosen? (Fixed input - do not re-decide it.)
3. Do participants bring their own problems to work on, or does the organizer supply the problem statements? Both is a real answer.
4. How many sponsors fund a prize, and does any signed agreement already promise a named challenge track?
5. Does any sponsor's API, dataset or hardware need keys or accounts - and has anyone on the organizing team actually built something small against it end to end? What happens to those teams if it goes down mid-event?
6. Who may enter and who is barred: students only, an age minimum, geography or employment exclusions, organizers and volunteers? And what team-size rule has `samber/dev-event-organizer-skills@hackathon-team-formation` already decided - a maximum, a minimum, solo entries allowed or not? (Fixed input you publish, not one you set. The pass threshold below counts it, so get the number before drafting.)
7. Is a demographic or skill-level carve-out required - a beginners track, a first-timers quota, a student-only category?
8. Do prizes carry cash value, are minors expected to attend, and is any personal data collected through the submission? (Decides whether the cheapest rules rung survives at all.)
9. What is the publication timeline and event cadence?
   - When must the brief be published?
   - Is this a one-off, or a recurring edition whose rules should still hold next year?
   - What is the effort ceiling: organizer hours before publication, and whether counsel is available at all?

Q9's three answers each move a named rung. Say which as you re-rank:

- A near publication date promotes the adopted standard rule set over anything drafted, and demotes the fully specified challenge, whose starter repo and acceptance tests are the longest lead time on any menu here.
- A recurring edition promotes the rungs written once and reused, the adopted set with its carve-outs and the per-track prompt skeleton, because their cost amortises across editions where a one-off pays it in full.
- An effort ceiling with no counsel behind it does not demote full legal-grade, it removes the route to it. Say so rather than substituting self-written legal-sounding text.

## Workflow

1. Run the interview. Read last edition's published rules first if one exists.
2. Fix the rules and eligibility text **before** the problem statements. It deletes rungs from the other menus and it carries the real exposure. Load [references/rules-and-eligibility-source-text.md](references/rules-and-eligibility-source-text.md).
3. Decide the challenge-track structure, then write one problem statement per track. Load [references/problem-statement-patterns.md](references/problem-statement-patterns.md).
4. Convert each sponsor commitment into a track prompt or a bonus-prize criterion, and write the fallback sentence for a sponsor platform that fails.
5. Name the evaluation categories. Say plainly in the brief who weights them and when the weights get published, then hand the categories to `samber/dev-event-organizer-skills@hackathon-judging`.
6. Build the submission checklist from the chosen demo structure, never from a generic template. Load [references/submission-checklist-and-categories.md](references/submission-checklist-and-categories.md).
7. Run the ambiguity pass: for every rule, ask what a team arguing the opposite reading would point at.
8. Publish before registration closes, then freeze. A rule added after teams start building applies to a competition nobody entered.

Present the brief section by section for validation, never as one block:

- rules
- eligibility
- tracks
- problem statements
- submission checklist
- categories

Get explicit approval before publishing; publication is the point of no return.

If your harness has persistent memory, record:

- the published rule set and which fields were edited
- the specificity rung chosen per track
- the sponsor fallback sentences
- every question a participant actually asked during the event, the most useful of the four, since each one names a sentence the next brief needs

## Problem-statement specificity

Four rungs, from a bare theme to a fully specified challenge with a starter repo and acceptance tests.

**Size the ambition to the time box.** One practitioner rule of thumb circulates: "Most projects will accomplish about 25% of what they think they can accomplish in the limited time they have." Read the figure against the right denominator: it is 25% **of a team's own pre-hack estimate of its own scope**, not of the organizer's prompt, not of any absolute measure, and not a completion rate. It is one organizer's observation, not a measured rate.

The design consequence runs through every rung below: write each prompt so that the quarter a team actually reaches is itself demoable, by naming a minimum viable submission rather than leaving teams to discover one at hour forty.

- value (a team can self-assess whether it is in scope; judges can compare submissions to each other): `fully specified > structured statement > domain-scoped prompt > open theme`
- effort (organizer writing time before publication, plus keeping every prompt consistent with the rules): `fully specified > structured statement > domain-scoped prompt > open theme`
- efficiency: `structured statement > domain-scoped prompt > open theme > fully specified`

**Dominance check, re-derived: clean only by construction, and by-construction is never a pass.** Both axes run in the same order, so no pair exists where one rung has value greater than or equal to another's and effort less than or equal to it. Zero dominance relations exist, the check can catch no misordering here, and the efficiency line therefore rests entirely on the arguments below rather than on any verification.

- **Structured statement** - the default, in five parts: context, the challenge as a question, the constraints, the resources provided, and a stated minimum viable submission. It is the cheapest rung at which a team can answer "are we in scope" without asking an organizer, and the rung the submission checklist and the evaluation categories both derive from without further writing.

  Its project-quality template asks that projects have "a clear question or problem they are trying to solve plus a reasonably specific proposed solution". That template assumes participants pitching their own projects, so when the organizer writes the prompt instead, the burden moves to the organizer.

- **Domain-scoped prompt** - one sentence naming a domain and nothing else. Real segmentation value for near-zero cost, but it leaves the in-scope question open, and that question generates the clarification traffic an organizer answers all weekend.
- **Open theme** - near-zero cost, and genuinely correct at events where participants bring the problems. Promotion condition, keyed to Q3: participants arrive with their own projects and pitch them, in which case the brief's job is to publish the pitch mechanic rather than the problem.

  **Delete it, from this menu and from the axis lines above, as soon as any sponsor funds a prize** (Q4). A sponsor prize needs a stated criterion to attach to, and parking the open theme at the bottom quietly leaves that prize with nothing to award against.

  Where the pitch mechanic is chosen, publish one refinement alongside it: require the pitch to state a problem, not a solution. A team pitching "we want to build X" commits to an approach before anyone has tested whether the problem is real; a team pitching "this target group has this problem, here is the evidence" leaves the approach open to whoever joins. Publish two things with it - a short evidence requirement (interviews, numbers, a lived account - whatever counts as evidence here) and a stated minimum before a team may move to building - and hand both to `samber/dev-event-organizer-skills@hackathon-team-formation` as content the pitch mechanic runs.

- **Fully specified challenge** - the starved option: top of value, top of effort, so efficiency never picks it. Building a starter repo, a dataset and acceptance tests is organizer engineering work measured in days.

  Promotion condition, keyed to Q1 and Q5: a time box of a week or longer, **or** a sponsor whose own integration tests already exist and can be handed over as-is. Below roughly a weekend it also changes what the event is, turning a build into a graded exercise.

  No source publishes a formula converting a specificity rung to an hour count. A second, independent source agrees on the direction and nothing more: guidance for writing AI/ML challenge prompts tiers them by complexity, and states plainly that its hardest tier - real-world systems, unpredictable data, enterprise-grade reliability - "often exceed[s] the standard 24-72 hour window and may be better suited to extended formats," while its lower tiers fit inside it. Never read it as a second data point for the same quantity as the 25% figure above; they measure different things.

## Challenge-track structure

Four rungs: one unified challenge, general plus one sponsor track, general plus several sponsor tracks, fully partitioned (every sponsor, every demographic, plus an open track).

**Adding a challenge track does not split the field.** A team submits one project, and that one project may enter several challenge tracks; the standard rule set publishes both halves as adjacent text, "You may not submit multiple projects" and "You may submit to multiple challenges". Every team stays eligible for the general prize while entering the sponsor track too, so the marginal cost of a track is rules-consistency work, not lost submission density. This lever is routinely missed, and it is what makes every rung below affordable.

- value (sponsor satisfaction, audience segmentation, prize flexibility, a beginner's chance of placing): `fully partitioned > general plus several sponsor tracks > general plus one sponsor track > one unified challenge`
- effort (writing each prompt, keeping eligibility carve-outs consistent, and the cross-track submission rule): `fully partitioned > general plus several sponsor tracks > general plus one sponsor track > one unified challenge`
- efficiency: `general plus one sponsor track > general plus several sponsor tracks > one unified challenge > fully partitioned`

**Dominance check, re-derived: clean only by construction, and by-construction is never a pass.** Value and effort run in the same order across all four rungs, so no strict-dominance pair exists and nothing here was verified by the check. The argument above is the whole basis for the ordering.

- **General plus one sponsor track** - the default. The first sponsor track costs one prompt and one prize line, and it converts a sponsor from a logo into a challenge owner. It is also where the cross-track rule gets written once, which is the real cost.
- **General plus several sponsor tracks** - marginal effort per additional track _falls_, because the second track copies a pattern the first one paid for, while value keeps rising. Total effort still rises, which is why it sits below the default; the falling margin is why it sits above one unified challenge.
- **One unified challenge** - cheapest, and it leaves prize flexibility and sponsor value on the table. **Delete it, from this menu and from the axis lines above, as soon as any sponsor funds a prize** (Q4): with no named track the sponsor's prize has no published criterion, and awarding it becomes an improvisation at the ceremony.
- **Fully partitioned** - the starved option, top of both axes. Promotion condition, keyed to Q4 and Q7: enough sponsors that each funds its own prize **and** a demographic carve-out is already required, so the per-track eligibility wording has to be written anyway. Absent both, partitioning buys empty tracks and a prize nobody competed for.

**No published ratio scales track count to participant headcount.** The one sourced ceiling scales it to judging capacity instead: MLH's own guide says to aim for 3 tracks absent sponsor tracks and without an overall 1st/2nd/3rd placement, never 20 or more, and to raise the count only as far as the judges running deliberations can absorb without the panel turning chaotic. Treat sponsor and judge headcount, not participant headcount, as the variable this ceiling actually tracks.

**Demographic carve-outs are their own wording problem.** State the required fraction of the team before the event, and never adjudicate it after teams have formed. A published example is "Beginners track where at least half the team must have this be their first hackathon". Treat the fraction as the thing to decide; treat "half" as one event's number.

## Rules and eligibility rigor

Four rungs: minimal (a team-size cap plus a code-of-conduct pointer), an adopted standard rule set, adopted plus carve-outs, and full legal-grade text reviewed by counsel.

- value (disputes prevented, defensibility of a disqualification, sponsor and participant confidence): `full legal-grade > adopted plus carve-outs > adopted standard set > minimal`
- effort (drafting and review hours before publication): `full legal-grade > adopted plus carve-outs > adopted standard set == minimal`
- compliance cost, as the review each rung triggers and the reversibility it costs: `full legal-grade > minimal > adopted plus carve-outs > adopted standard set`
- efficiency: `adopted standard set > adopted plus carve-outs > minimal > full legal-grade`

**The `==` on effort is argued, not a dodge.** The minimal rung is not free: somebody still decides the team-size number, writes the sentence and links the code of conduct. Adopting a published set replaces that drafting with a handful of edits, because the source is explicitly offered for forking - "Organizers can use these rules exactly or fork them and edit them to suit their needs".

Both land in the same order of magnitude: under an hour. That equality is the only real bend on any menu in this skill, and it is what the check below runs on.

**Dominance check, re-derived: clean by care.** Exactly one strict-dominance relation exists: the adopted standard set has strictly higher value than minimal, equal effort, and strictly lower compliance cost, and the efficiency line honours it by ranking the adopted set first.

- Full legal-grade never dominates (top of every cost axis).
- Adopted-plus-carve-outs never dominates the adopted set (higher value but strictly higher effort).
- Minimal dominates nothing.

A wrong ordering here would have failed the check, so this pass carries information the other three menus' passes do not.

- **Adopted standard rule set** - the default, and the strongest single recommendation this skill makes. A published, forkable set already covers:
  - team size
  - crossposting
  - one-project-many-tracks
  - work-during-the-window
  - pre-existing code and open-source use
  - AI-tool disclosure
  - public-code requirements
  - who may compete
  - disqualification grounds

  Clear rules let an organizer "easily be able to point to specific rules if you have to disqualify hackers for cheating". [references/rules-and-eligibility-source-text.md](references/rules-and-eligibility-source-text.md) names the fields you must still edit; adopting the set without editing them is the common failure.

- **Adopted plus carve-outs** - promotion condition, keyed to Q6 and Q7: a demographic or skill-level track, an age minimum, or a geographic or employment restriction. Each carve-out is per-track wording that has to compose with the base rules without contradicting them, which is where the extra hours go.
- **Minimal** - **delete it, from this menu and from the axis lines above, as soon as any prize carries cash value or any sponsor funds one** (Q8, Q4). A prize with value turns a dispute into a claim, and nothing is then published to point at. It ranks second on compliance cost for the same reason: it triggers no review before the event and defers the whole review to the least reversible moment there is, the disqualification itself, in public, with prizes on the table.
- **Full legal-grade** - the starved option: top of value, top of effort, top of compliance cost. Promotion condition, keyed to Q8 and Q9: a prize pool large enough that a losing team retains counsel, or a sponsorship agreement imposing IP terms. Promote it by routing to actual counsel, never by writing legal-sounding sentences yourself.

**Two of Q8's answers are gates, not menu choices.** Minors expected to participate, and personal data collected through the submission, each carry an obligation the efficiency line has no vote on: the review happens before publication, by counsel or by whoever owns data protection for the organizing entity, whatever rung the ratio landed on.

An obligation determines the response; efficiency only orders the options that remain. The same holds for the code of conduct every rung points at: `samber/dev-event-organizer-skills@event-code-of-conduct` owns it, the brief links it, and it is never a rung to be traded against effort.

**On intellectual property, this skill states no clause and recommends none.** The MLH rule set carries no IP-ownership term and no originality warranty at all; its only ownership-adjacent requirement is that submitted code be public and stay public to remain prize-eligible.

Whether a team, an organizer, or a sponsor owns submitted work is a jurisdictional legal question. Route it to counsel through `samber/dev-event-organizer-skills@event-sponsor-agreement` when a sponsor asks for it, and never let a plausible-sounding sentence stand in for the answer.

## Sponsor-challenge integration depth

Four rungs: the sponsor named as prize funder only, an optional bonus challenge using its product, its technology required for one track, and its technology as the event's sole substrate.

**The axes here agree, and the disagreement cannot be manufactured.** The tempting counter-argument: a sole substrate costs _less_ prompt-writing than a required track, since there is no general track to stay consistent with. That is true, and it does not flip the axis - provisioning keys and mentors for every participant rather than for one track's entrants outweighs it. Say so rather than invent divergence.

- value (sponsor return and renewal likelihood - argued, not measured): `sole substrate > required for one track > optional bonus challenge > named funder only`
- effort (vetting the sponsor's docs, provisioning keys and accounts, coordinating mentors, writing a prompt inside the constraint): `sole substrate > required for one track > optional bonus challenge > named funder only`
- dependency risk (what breaks in the brief if the platform, keys, docs or rate limits fail mid-event): `sole substrate > required for one track > optional bonus challenge > named funder only`
- compliance cost, as the review each rung triggers and the reversibility it costs: `sole substrate > required for one track > optional bonus challenge > named funder only`
- efficiency: `optional bonus challenge > required for one track > named funder only > sole substrate`

**All four axes run in the same order**, so there is no pair with value greater than or equal and any cost less than or equal. The check catches nothing here, and the ordering rests entirely on the argument above.

**The dependency-risk axis is why this menu has four cost lines and not two.** Effort is what an organizer spends before the event; dependency risk is what the event loses if something outside the organizer's control fails during it. They move together here but they are not the same quantity, and only the second one can delete a rung on the day.

- **Optional bonus challenge** - the default: the sponsor's product is one path to a bonus prize, never the only path. Teams who cannot get a key still compete, so a platform outage costs one prize rather than the event.
- **Required for one track** - promotion condition, keyed to Q4 and Q5: the signed agreement already commits to a named challenge track, **and** somebody on the organizing team has built something small end to end against the sponsor's API before publication. Never promote on the sponsor's own claim that the docs are good.
- **Named funder only** - cheap and safe, and the rung that most often breaks a sponsorship promise. **Delete it, from this menu and from the axis lines above, when the signed agreement already promises a named challenge track** (Q4) - at that point it is a contract term, not a menu choice.
- **Sole substrate** - the starved option on efficiency, and the one rung a _different_ axis can remove outright. Promotion condition, keyed to Q4 and Q5: a single sponsor funds the whole prize pool and the event is billed as its event, **and** every Q5 confirmation is already in writing.

  **Delete it, from this menu and from the axis lines above, when the sponsor cannot confirm in writing both a sandbox or offline fallback and rate-limit headroom for the expected team count** (Q5). Efficiency merely ranks it last; dependency risk is what makes it unshippable, and the two are separate findings - promotion never overrides the delete.

**Every sponsor-dependent prompt needs a published fallback sentence.** State in the brief what happens to a team whose sponsor integration is unavailable through no fault of its own: judged on its design and integration plan rather than on a working call. Written before the event it is a rule; improvised during the outage it is a favour, and every team that already finished will say so.

## Evaluation categories in the brief

Name the categories. Never weight them, scale them or total them: that is `samber/dev-event-organizer-skills@hackathon-judging`, and publishing a weight here creates a promise that skill then has to honour or contradict.

Print the elimination criteria alongside them. A binary knockout list disqualifies a submission outright, so it belongs next to the category names rather than inside the weighted rubric. Print it in full; `samber/dev-event-organizer-skills@hackathon-judging` decides its content.

One published category set is worth starting from, each category with a written description of what a judge is looking for:

- technology
- design
- completion
- learning

That set carries its own default weighting. Keep the weighting out of the brief and hand it to the judging skill as an input instead.

Publishing what is **not** judged is the underused half, each exclusion carrying its reason:

- how good the code is
- how well the team pitches
- how good the idea is
- how well the project solves a real problem

Teams optimize for whatever the brief names, so an exclusion list is the cheapest way to stop forty teams polishing slides. Copy the shape, and decide the content for your own event: a corporate hackathon judging commercial viability would exclude a different list.

## Submission guidelines

Derive the checklist from the demo structure chosen upstream, never from a template. A video-only event makes the video the deliverable and its constraints binding; an expo or stage event makes the video optional and the live demo carry the weight. Getting this backwards is how a brief requires a video nobody will watch, or omits the one artifact judging depends on.

Requirements worth adopting from MLH's published rules, all stated there as absolute rather than as suggestions:

- submitted code is publicly available, ideally in a git repository, and stays public after the event to remain prize-eligible
- API keys are removed before sharing
- libraries and frameworks used are listed in a readme
- AI-tool use is disclosed in the submission

For fully digital events the same source requires a demo video of two minutes or less, created during the event, naming the hackathon at the start, and remaining public afterwards.

**The public-code requirement does not transfer without thought.** It assumes an event whose culture is open by default, and a corporate or client-data hackathon may not be able to honour it at all. Decide that before copying the sentence.

Set the submission deadline as a wall-clock time in a named time zone, and say what happens to a late submission before anyone is late. [references/submission-checklist-and-categories.md](references/submission-checklist-and-categories.md) carries the full checklist per demo format, the deadline mechanics and the artifact-by-artifact wording.

## Failure modes

- **Weighting the categories in the brief.** Naming them is your job; weighting them is not, and a weight published here binds a sibling skill that has not yet done its arithmetic.
- **Picking the deliverable format.** Video-versus-live was settled by the format skill. You translate it. Choosing it again produces a checklist the judging plan cannot execute.
- **Confusing challenge tracks with session tracks.** They are different decisions owned by different skills, and a brief that borrows the session-track count as its challenge-track count invents categories nobody sponsored.
- **A rule added after building starts.** Teams built against the published text. A new rule mid-event re-scores whoever already finished.
- **A prompt with no minimum viable submission.** A team reaching a quarter of its own plan has nothing demoable, and the brief is what decided that.
- **A sponsor track written from the sponsor's marketing copy.** Marketing copy names benefits, not buildable constraints. Rewrite it as a problem, then have the sponsor confirm the rewrite.
- **Carve-out fractions adjudicated after teams form.** A required fraction - "at least half the team" - has to be published before people choose teammates, or the rule quietly excludes teams that already exist.
- **Adopting a published rule set without editing its event-specific fields.** The set arrives with somebody else's hacking hours, eligibility scope and judging mode in it.

## Measurement

Every gate below is self-set rather than an industry standard; say so when presenting it. Do not borrow a disqualification, invalid-submission, rule-dispute or completion rate from another event as a target: the numbers are not comparable across formats, sizes and audiences.

No platform or academic survey of the field publishes an aggregate disqualification or rule-dispute rate at all. The closest a named event gets is one organizer's own post-hoc count, posted publicly mid-controversy, of roughly a quarter of its submissions arriving as an idea with nothing built. That is one event, self-reported, defending one judging dispute, and not a figure to import anywhere else.

**Pass threshold (structural, one only):** before publication, all seven exist in writing with zero blanks.

1. the hacking window as start and end wall-clock times
2. the eligibility statement
3. the team-size rule
4. the per-track problem statement with its minimum viable submission
5. the submission checklist matching the chosen demo format
6. the named evaluation categories
7. the submission deadline with its late policy

Iterate until the count is seven.

**Ambiguity gate (before publication):** for each rule, name the reading a team arguing the opposite would use. A rule with a second plausible reading is not yet written.

Signals to record for the next edition (self-set):

- every clarification question asked during the event
- submissions rejected as invalid and why
- challenge tracks that drew no entries

Each one names a sentence the next brief needs, or a track that should not exist.

## Invocation examples

- "Write the challenge brief for our 36-hour AI hackathon - two sponsor tracks and a beginners track."
- "Our sponsor wants their API used. How do we word that without breaking the event if it goes down?"
- "What rules and eligibility text do we publish, and what do we not write ourselves?"
- "Turn our chosen expo-table judging into a submission checklist and deadline."
- "We have a theme but no problem statements. How specific should they be for one weekend?"

Expected output: a publishable brief carrying

1. the rules and eligibility text with its edited fields listed
2. the challenge-track structure with the cross-track submission rule
3. one problem statement per track at a stated specificity rung, each with a minimum viable submission
4. sponsor framing with its fallback sentence
5. the named evaluation categories and the exclusion list
6. the submission checklist derived from the demo format, with deadline and late policy

Present it section by section for validation before publication.

## References

- [references/rules-and-eligibility-source-text.md](references/rules-and-eligibility-source-text.md)
- [references/problem-statement-patterns.md](references/problem-statement-patterns.md)
- [references/submission-checklist-and-categories.md](references/submission-checklist-and-categories.md)
