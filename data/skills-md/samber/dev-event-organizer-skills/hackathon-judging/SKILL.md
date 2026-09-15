---
name: hackathon-judging
description: Design the rubric and the scoring process for judging projects built during a hackathon - evaluation criteria and their weights, the scoring scale, judge coverage and the allocation arithmetic that fits the judging window, cross-judge score normalization, tie-breaking, sponsor and judge conflict-of-interest handling, judge recruitment and briefing, and results announcement including a contested result. Use whenever the user mentions a hackathon judging rubric, criteria weights, how many judges a team count needs, briefing a jury, a sponsor judging its own challenge track, or tie-break and dispute rules - even if they never say "judging". Do NOT use for prize amounts and payout law - use samber/dev-event-organizer-skills@hackathon-cash-prize instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Hackathon Judging

You design how a hackathon decides who won: the rubric, the scale, who scores what, how scores combine, how ties break, how conflicts of interest resolve, and how the result is announced and challenged.

Two inputs arrive already decided. Consume them, never re-open them:

- **The demo/judging structure** (Expo Table, Stage Pitch, Video Only, or the two-stage hybrid) belongs to `samber/dev-event-organizer-skills@event-format-selection`. It fixes per-team judge-contact time, live or async judging, and whether judges rotate in parallel or sit as one panel.
- **The evaluation categories** named in the published challenge document belong to `samber/dev-event-organizer-skills@hackathon-brief-design`. Weight them and build the mechanics on top.

Never set a prize amount or its legal structure. `samber/dev-event-organizer-skills@hackathon-cash-prize` turns the ranked outcome into a payout.

Judges are not mentors:

- Mentors help teams build during the hacking window (`samber/dev-event-organizer-skills@hackathon-mentoring`).
- Judges evaluate finished projects afterwards.

Small events reuse the same people for both. That is a staffing convenience, not one role.

Every ranking below is a default, not a law. Re-rank each menu after the interview. Any of these overturns a default rung:

- A returning jury.
- Last edition's rubric.
- A sponsor contract already signed.
- A ceremony start time that cannot move.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 3-6 exist because the menus below turn on them, and no default can be picked without those answers.

1. Which demo/judging structure is already chosen, and what per-team judge-contact time does it assume? (Fixed input. Do not re-decide it here.)
2. Which evaluation categories does the published brief already name? (Also fixed. Weight them, never replace them.)
3. How many teams are expected to submit, and how many minutes run between submission close and ceremony start? Minutes, not "an afternoon". The allocation menu is arithmetic and needs both numbers.
4. How many judges are confirmed, and can they all be in one room at the same time?
5. Which prizes and tracks exist, does any sponsor fund one, and does any signed sponsorship agreement require that sponsor's own representative to judge its track?
6. Will teams receive per-team feedback, and is there a window after the ceremony to write it in?
7. What did the published rules already promise about criteria, tie-breaking and disputes, and is this a one-off edition or a recurring event whose rules should still hold next year? Read the rules first. The process executes what was published, not what is convenient.
8. What is the effort ceiling: organizer hours before the ceremony, volunteers for a pre-screen round, and who holds authority to break a tie on the record?

## Workflow

1. Run the interview. Read the published rules (Q7) and the brief's categories (Q2) before designing anything.
2. Compute the allocation band from Q1, Q3 and Q4 **first**, before the rubric. It deletes rungs from every other menu, and it is the one step that can make a plan impossible rather than merely expensive. Load [references/judge-allocation-math.md](references/judge-allocation-math.md).
3. Weight the brief's categories and pick the scale. Write both down before anyone scores. A rubric changed mid-round re-scores whichever teams were seen first.
4. Fix the combination rule - raw average, per-judge normalization, or consensus - against the allocation band from step 2, never independently of it.
5. Write the tie-break ladder as a deterministic list, and publish it before submissions close.
6. Brief judges before scoring opens: criteria and weights, scale, conflict-of-interest rule, their own slice of the allocation map, and what to do if they fall behind.
7. Build the allocation map as a named list: judge, teams, order, start time. An unassigned judge wanders, and an unvisited team is a dispute.
8. Score, combine, and check the arithmetic feasibility gate before the ceremony (see Measurement).
9. Announce from a prepared list, and hold the contest path open for the window the rules stated. Load [references/coi-and-results-policy.md](references/coi-and-results-policy.md).
10. Record what happened: teams visited, recusals fired, challenges received. Hand the ranked outcome per track to `samber/dev-event-organizer-skills@hackathon-cash-prize`.

Present the design for validation section by section, before judging opens:

- Allocation
- Rubric
- Combination rule
- Tie-break ladder
- Conflict rule
- Announcement plan

Once scoring starts, changing the rules invalidates whatever was already scored.

If your harness has persistent memory, record the weights, the allocation band and its inputs, the tie-break ladder, and the specific complaint each would need to hear to change next edition.

## Judge allocation depth

**Recruiting more judges does not let full coverage reach more teams.** The cap is `N ≤ W / t`, and no `J` appears in it: under full coverage each judge personally traverses all `N` teams, so the judge count cancels out of the inequality. What the cap limits is the team count, never the judge count and never the window.

This menu bends on arithmetic rather than taste. Four quantities drive it:

- `N` - teams expected to submit (Q3).
- `t` - minutes of judge time per team, fixed by the format (Q1).
- `W` - minutes of judging window (Q3).
- `J` - confirmed judges (Q4).

Timing inputs for `t`:

- **10 minutes per team** at a live multi-team demo handoff: 3 minutes demo, 1-2 minutes Q&A, 5-6 minutes setup and swap. MLH gives this figure for ceremony demo slots, not for a judging round, so what carries over is the setup and swap tax, not the audience. A judging block holds no crowd and can run tighter.
- **3-5 minutes per team** at an Expo Table.
- **2-5 minutes plus Q&A** at a Stage Pitch.
- **4 minutes per project, 3 rounds of judging per project** at MLH's own science-fair judging round: 2 minutes presentation and demo, 1 minute questions and score compilation, 1 minute judge travel. That is MLH's published judges-per-project default, close to the Expo Table figure above.

The 3-5 and 2-5 minute figures allow nothing for setup or swap, so every ceiling built on them is an optimistic upper bound rather than a capacity promise. Say so when presenting the number.

Two crossovers, computed from those inputs:

- A 120-minute window at 10 minutes per team caps full coverage at **12 teams**.
- The same window at 5 minutes per team caps it at **24 teams**.

Halving `t` doubles the teams full coverage reaches. It changes nothing about the judge count or the window.

Ranking (default, not a law - Q3, Q4 and Q8 re-rank it):

- value (comparability of the projects that actually get ranked, judge calibration, defensibility of the podium): `full coverage > sampled panel > triage-then-finals > single judge per team`
- effort (judge-hours, plus the routing and rounds an organizer has to run): `full coverage > triage-then-finals > sampled panel > single judge per team`

The two axes genuinely disagree, so efficiency is published per band rather than as one line. The order flips at an arithmetic boundary, never on preference:

- **Band 1, `N ≤ W / t`**: efficiency `full coverage > sampled panel > single judge per team > triage-then-finals`. Full coverage needs no allocation map at all and buys maximum comparability. Triage is pure overhead when everyone already fits.
- **Band 2, `W / t < N ≤ (J × W) / t`**: **full coverage is deleted here, from this menu and from the axis lines above** - it is arithmetically impossible, not merely expensive. Efficiency: `sampled panel > single judge per team > triage-then-finals`. Coverage per team is `k = floor((J × W) / (N × t))` judges.
- **Band 3, `N > (J × W) / t`**: sampled panel and single-judge are both **deleted from this menu and from the axis lines above** - even one judge per team does not fit. Triage-then-finals is the only live-window allocation left. Where the format is still open, hand back to `samber/dev-event-organizer-skills@event-format-selection` instead: async video judging is a format change, and that skill decides it.

**Dominance check, re-derived: clean by care.** One strict-dominance relation exists: sampled panel has higher value _and_ lower effort than triage-then-finals. Every band's efficiency line honours it. A wrong ordering would have failed the check, so this pass means something.

- Full coverage never dominates (top of the effort axis).
- Single-judge never dominates (bottom of the value axis).
- Triage never dominates sampled panel on either axis.

What the efficiency order starves:

- **Full coverage** - top of both axes, so efficiency abandons it the moment Band 1 ends. Promotion condition, keyed to Q3: a team count that fits `W / t`. Check the arithmetic rather than the feeling that "we're small".
- **Triage-then-finals** - cheap on nothing, and justified only in Band 3. Promote it earlier only when Q8 confirms a volunteer crew for a published pass/fail pre-screen.

Worked allocation maps, the `k` computation, and the band boundaries with numbers are in [references/judge-allocation-math.md](references/judge-allocation-math.md).

## Rubric depth and weighting

Weight the categories the brief already named (Q2). Ranking (default, not a law - Q1 and Q6 re-rank it):

- value (defensibility to teams and sponsors, dispute resistance, usable tie-break input): `weighted criteria plus written per-criterion comment > weighted criteria > named criteria unweighted > single overall score`
- effort (judge briefing, per-team time consumed inside the slot, organizer setup): `weighted criteria plus written per-criterion comment > weighted criteria > named criteria unweighted > single overall score`
- efficiency: `weighted criteria > named criteria unweighted > single overall score > weighted criteria plus written per-criterion comment`

**Dominance check, re-derived: clean only by construction, and this is not a pass.** Value and effort run in the same order, so no pair exists where one option has value >= another and effort <= it. With no dominance relation to violate, the check cannot catch a misordering here. The ordering rests on the argument below, not on the check.

- **Weighted criteria** - the default. Deciding the weights is a one-off cost paid before the event, and the scoring sheet does the arithmetic, so the marginal cost inside a 3-5 minute slot is zero. It buys the two things unweighted criteria cannot:
  - A sponsor can see its challenge is actually valued.
  - A tie has a principled first tiebreaker.
- **Named criteria, unweighted** - cheaper by one decision, and the decision does not disappear. Each judge applies private weights instead, so a technical judge and a business judge silently score different competitions. Legitimate only where the categories are genuinely equal in the organizers' minds.
- **Single overall score** - cheapest, and it buys nothing defensible, because a bare number cannot say why. **Delete it, from this menu and from the axis lines above, as soon as more than one track awards a prize** (Q5). One number cannot separate track winners, and parking it at the bottom quietly reintroduces the problem at the ceremony.
- **Weighted criteria plus mandatory written per-criterion comment** - the starved option: top of value, top of effort, so efficiency never picks it. The effort lands in the one place a hackathon has none, inside the live slot. Judges have minutes per team, not days.
  - Promotion condition, keyed to Q1 and Q6: judging is Video Only or otherwise async, **or** teams are promised per-team feedback and a post-event window exists to write it in. In both cases the comment costs no live minutes.

Scale shape is a separate decision from weighting. Two shapes:

- **A numeric 1-5 or 1-10 scale per criterion** - the default, and the one a judge can hold in their head between two tables.
- **A named capability ladder with explicit point deltas**, including a negative delta for the trivial path. Use it on a criterion that should actively discourage the cheapest route rather than merely fail to reward it: the ladder states a reward structure a plain numeric scale leaves implicit. Normalize the open-ended ladder total to the published scale with a cohort min-max pass, so the internal rubric stays expressive while judges and teams see one comparable number.

The ladder pattern, the normalization formula, scale choice, weighting worked examples, and a positive and negative scoring pair are in [references/rubric-and-scoring-mechanics.md](references/rubric-and-scoring-mechanics.md).

## Elimination criteria

A rubric scores degree. An elimination gate answers yes or no, disqualifying a submission whatever its weighted score. Keep the two as separate artifacts: a knockout condition folded into a rubric line reads as merely low-scoring instead of disqualifying.

Write elimination rules against the specific ways this event's own theme invites gaming, never a generic list copied from another event:

- A hacked or circumvented tool.
- The required technology present but not central to the project - "we could have done without it."
- A technology generation too old or too simple to meet the brief's stated ambition.
- A design file with no working build, where the brief required at least code or no-code.
- Code that never went public, where the brief's submission checklist required it.

Publish the full list alongside the category names in the brief. Write the rules here; `samber/dev-event-organizer-skills@hackathon-brief-design` prints them next to the eligibility text.

**Publishing the category names and the elimination list satisfies disclosure. The numeric weight does not have to.** The failure named below is a team entering blind to what is judged at all, and named categories plus a full knockout list already prevent it. Withholding the weight itself, once those are public, is a legitimate anti-gaming choice: it stops a team optimizing to the decimal place against a figure that was never theirs to see.

## Combining scores across judges

**Normalization buys nothing under full coverage and buys back the whole ranking under a sampled panel.** The mechanism is one line of arithmetic: a uniformly harsh judge adds the same constant to every team they score.

- **Full coverage** - that judge scores every team, the constant lands on all of them equally, and the order is untouched. Normalizing is pure overhead.
- **Sampled panel** - the constant lands on that judge's slice only, so the final rank partly records which panel a team drew. Normalizing removes exactly that artifact.

Pick this menu against the allocation band, never independently of it.

Ranking (default, not a law - Q1 and Q4 re-rank it):

- value (rater-effect correction - how far the final rank reflects the projects rather than which judge happened to see them): `synchronous consensus > per-judge normalization > raw average`
- effort (setup, judge briefing, and convening every judge against a fixed ceremony start): `synchronous consensus > per-judge normalization > raw average`
- efficiency under full coverage (Band 1): `raw average > per-judge normalization > synchronous consensus`
- efficiency under a sampled panel or single-judge allocation (Bands 2-3): `per-judge normalization > raw average > synchronous consensus`

**Dominance check, re-derived: clean only by construction, and this is not a pass.** Value and effort run in the same direction, so there is no pair to check and no error the check could catch. The ordering rests on the arithmetic above.

**Synchronous consensus** is the starved option in both bands. One discussion round instead of combined independent scores needs every judge in one room at once, with no pressing schedule waiting. A hackathon jury meets against a ceremony start time that cannot move.

Promotion condition, keyed to Q4: a judge pool small enough to sit in one room, with window slack left after the visits. **Delete it, from this menu and from the axis lines above, when judging is async or when judges leave straight after their slot** (Q1, Q4) - a meeting nobody will attend parked at the bottom silently becomes a plan.

**An organizer override of the judges' combined result is not a rung on this menu; it is deleted outright.** A rejected submission was never promised a skill-based rank, and a losing team competing for a prize was. An override is the exact mechanic that makes a result contestable, and weeks after the ceremony is the wrong moment for a team to discover one was reversed.

## Conflict of interest and disclosure

**Doing nothing is not the cheap option here.** Compliance cost measures the review a rung triggers and the reversibility it costs, and on that axis "no formal process" ranks high rather than low. That is why the default is not the cheapest rung:

- **No formal process** triggers no review before the event, so it defers the whole review to the least reversible moment: after prizes are handed over, when the only moves left are re-running a judged round or living with the result.
- **Self-declared recusal** triggers one line in the judge brief. A missed conflict is quietly fixable by reassigning that judge's slice while no result exists yet.
- **A written registry** triggers a governance review every edition and is the hardest to unwind, because withdrawing a published policy next edition reads as a retreat.

Ranking (default, not a law - Q5 re-ranks it):

- value (sponsor-relationship risk avoided, credibility of the announced result): `written policy with disclosure registry and escalation path > declared recusal plus assigned replacement judge > self-declared recusal > no formal process`
- effort (judge-briefing time, organizer tracking during the window, formality): `written policy with disclosure registry and escalation path > declared recusal plus assigned replacement judge > self-declared recusal > no formal process`
- compliance cost: `written policy with disclosure registry and escalation path > no formal process > declared recusal plus assigned replacement judge > self-declared recusal`
- efficiency: `self-declared recusal > declared recusal plus assigned replacement judge > no formal process > written policy with disclosure registry and escalation path`

**Dominance check, re-derived: clean only by construction on value/effort, and this is not a pass.** Those two axes run in the same order, so no dominance relation exists there to violate. The compliance axis, not the check, is what re-orders this menu.

- **Self-declared recusal** - the default. Tell judges to abstain from scoring a team they are close to rather than score it and disclose. The honour-system convention works only with fast reassignment: a CFP reassigns a reviewer over days, a hackathon reassigns inside the window. Name the fallback in advance, for a team that loses so many judges to recusal that its scores stop being comparable.
- **Declared recusal plus assigned replacement.** Promotion condition, keyed to Q5: any sponsor funds a track and any judge is tied to that sponsor. Track judge-sponsor ties and rebalance the allocation map live.
- **No formal process.** **Delete it, from this menu and from the axis lines above, as soon as any sponsor funds a track prize** (Q5). A party then holds a financial interest in the outcome with no stated rule about it.
- **Written policy with registry and escalation** - the starved option, top of value, effort and compliance cost. Promotion condition, keyed to Q5 and Q7: a multi-edition event whose published rules already promise a dispute process, or a prize pool large enough that a losing team will ask who decided and on what basis.

**The hard case the ladder cannot rank away.** A signed sponsorship agreement can _require_ the sponsor's own representative to judge its own challenge track. That conflict was accepted at contract time, so it overrides this whole menu.

- Confine the sponsor judge to that track and keep them off the overall prize.
- Pair them with at least one neutral judge.
- Check whether the track rank survives dropping their scores.
- Disclose the composition in the published rules before submissions close.

Full handling, including what to do when the rank does not survive, is in [references/coi-and-results-policy.md](references/coi-and-results-policy.md). Where the clause is not signed yet, the wording belongs to `samber/dev-event-organizer-skills@event-sponsor-agreement`, not here.

## Tie-breaking

Publish the tie-break ladder in the brief before submissions close, rather than inventing one at the podium. Walk it in order and stop at the first rung that separates the teams.

1. Highest score on the highest-weighted criterion. The weights already state what the event values most; weights that cannot break the tie were the wrong weights.
2. Highest count of judges who placed the project first among the teams they personally saw.
3. A named tie-break judge decides, on the record, in one sentence.
4. A co-award, only where the prize is divisible and the published rules said so in advance.

Published rules converge on the same shape: a deterministic score cascade, then a follow-up tally or panel vote, then a named decider, with a divisible-prize co-award reserved for the rare case the rules promised it.

- Devpost's rules template, reused across dozens of Devpost-hosted hackathons, cascades through the listed judging criteria before falling back to a judges' vote.
- MLH's own contest terms give the judge sole and final discretion, with no criterion cascade at all.
- HackMIT sidesteps numeric ties structurally: it ranks projects by pairwise comparison instead of scoring them independently, so there is no tie to break.
- Salesforce is the one documented case of abandoning score-based resolution outright. After a 2013 judging controversy it declared co-champions and split its Salesforce1 Hackathon grand prize. That was crisis management after the fact, not a published rule.

Full precedent, including the WildHacks three-tier scoring fallback, is in [references/coi-and-results-policy.md](references/coi-and-results-policy.md).

Two moves to refuse, for unrelated reasons:

- **Re-scoring.** The demos are over, so a second pass scores a memory rather than a project.
- **A coin flip or any random draw.** Some jurisdictions treat a prize contest differently depending on whether the outcome is demonstrably skill-based. Confirm that with `samber/dev-event-organizer-skills@hackathon-cash-prize` before relying on any legal constraint.

## Results announcement and a contested result

- Collect the winner list, sponsor tracks included, before the ceremony rather than live. Announce from slides rather than narration.
- Do not schedule live demos at the closing ceremony while judging is still concluding. Demo slots and the judging window draw on the same minutes.
- Call judges into the room a full hour before the ceremony for the briefing. Attach the scoring grid to their calendar invite as soon as it exists rather than handing it out cold at check-in.
- Stage the deliberation room in advance - seating, something to drink, something to write on - rather than assembling it once judges are already inside.
- Where the combination rule above lands on synchronous consensus, run the deliberation as two timed passes rather than one open discussion:
  - A short fixed slot per team first, then a longer pass on the shortlist only.
  - A timekeeper named before the round starts.
  - Every networked device in the room taken off the network for the duration. A result that leaks before the announcement is a result nobody trusts.
- Announce the rank and the criteria. Withhold per-judge and per-team raw scores, and the numeric weights unless the event already published them before submissions closed: publishing either turns a decision into a leaderboard teams audit at a precision the rubric was never built for, and raw scores additionally expose individual judges by name.
- State one contest path in the published rules before submissions close:
  - Who receives a challenge.
  - The window, closing before prizes change hands, since reversal after payout is `samber/dev-event-organizer-skills@hackathon-cash-prize`'s problem.
  - What can actually change. An arithmetic or eligibility error can change a result; a judge's opinion cannot.
- That contest path is this skill's own design. Code-of-conduct sanction appeals are a different subject that some events do publish; judging appeals are not.

## Failure modes

- **Re-deciding the demo format here.** Expo versus Stage versus Video was settled upstream, and it arrives as the `t` input rather than as a choice. Reopening it invalidates the allocation already computed.
- **Recruiting judges before computing the window.** Judge count is the last input the arithmetic needs, not the first. Ask for `N`, `t` and `W` first.
- **Adding judges to rescue full coverage.** The cap `N ≤ W / t` has no `J` in it. More judges buy a sampled panel, never a longer full-coverage reach.
- **Averaging raw scores across a sampled panel.** The harsh-judge constant only cancels when every judge scored every team. Under sampling it lands on one slice and moves the rank.
- **A sponsor judge discovered at the ceremony.** Same fact, opposite outcome, on timing alone:
  - Disclosed in the rules in advance, it is a rule.
  - Disclosed after the announcement, it is a scandal.
- **Inventing a tie-break at the podium.** Two teams tied with no published ladder means whoever speaks first decides, live, in front of both.
- **Categories that never reach the brief that teams read.** Teams optimize for what they were told counts. Undisclosed categories score a competition nobody entered. The numeric weight behind each category is a separate, legitimate anti-gaming withhold (see § Elimination criteria) - do not confuse the two.
- **Judges also competing.** Organizers, volunteers, judges and sponsors are barred from competing as hackers. Check the entrant list against the judge list before scoring, not after.

## Measurement

Everything below is a self-set gate; say so when presenting it.

**Pass threshold (structural, one only): before scoring opens, all six of these exist in writing, with zero blanks.**

- Criteria with weights.
- The scoring scale.
- The allocation map naming which judge sees which team.
- The conflict-of-interest rule and its recusal fallback.
- The tie-break ladder.
- The contest path.

Iterate until the count is six.

**Feasibility gate (arithmetic, checked before the day):** compute `k = floor((J × W) / (N × t))`.

- `k ≥ 1`: the confirmed judges reach every team at the format's contact time, and the plan is feasible as it stands.
- `k < 1`: they do not. That is Band 3, not a failed plan. Recompute the gate against the triage round the allocation menu prescribes there. The pre-screen is a pass/fail check that consumes part of `W`, so the finals slate must satisfy `k ≥ 1` on the surviving finalist count `N₂` and the remaining window `W₂`. If it fails again there, the only legitimate responses left are a longer window or a format change, both decided before the event.

Never absorb `k < 1` by shortening `t` on the day. That re-scores whichever teams were seen first.

Signals to record for next edition:

- Judges who finished their slice inside the window.
- Teams that got fewer judges than the map promised.
- Recusals that fired.
- Challenges received.

Pick two or three, write down the revision each would trigger, and record them before the ceremony rather than after.

## Invocation examples

- "We expect 60 teams, 12 judges, and 2 hours between submission close and the ceremony. How do we judge this?"
- "Build the scoring rubric and weights for our AI hackathon's three tracks."
- "A sponsor's contract says their VP judges their own challenge. What do we do?"
- "Two teams tied for first. What's the rule, and what should it have been?"
- "Write the judge brief and the results announcement plan."

Expected output: a judging plan with:

1. The allocation band with its arithmetic shown and the resulting judges-per-team.
2. The weighted rubric and scale written out.
3. The combination rule tied to that band.
4. The conflict-of-interest rule with its recusal fallback.
5. The published tie-break ladder.
6. The judge brief.
7. The announcement plan and contest path.
8. The signals to record.
9. Elimination criteria, where the event uses them, published separately from the weighted rubric.

Presented section by section for validation before judging opens.

## References

- `samber/dev-event-organizer-skills@event-run-of-show` - schedules the judging window and the ceremony this skill's arithmetic depends on.
- `samber/dev-event-organizer-skills@event-feedback` - collects participants' own read on judging fairness after the event.
