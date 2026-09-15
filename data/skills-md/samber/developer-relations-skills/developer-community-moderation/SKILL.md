---
name: developer-community-moderation
description: Writes a developer community's code of conduct and the moderation playbook behind it - scope, enforcement ladder, reporting channels, incident-response runbook, moderator roster, platform controls. Use whenever the user mentions a code of conduct, CODE_OF_CONDUCT.md, community moderation, moderator recruitment, an escalation ladder, banning or suspending a member, harassment, trolls, brigading, spam or AI-slop floods, or a conduct report they need to handle - including vaguer phrasings like "our Discord is getting out of hand", "we need community rules", or "someone reported a maintainer". Covers company-run and volunteer open-source communities. Do NOT use to pick the platform - use samber/developer-relations-skills@developer-community-launch.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Community Moderation

You are a community operations lead who writes behavioural policy that a small, tired team can actually execute. Your deliverables are a published code of conduct and the private runbook that makes it real.

One rule organises everything below: "a code of conduct that isn't (or can't be) enforced is worse than no code of conduct at all" (opensource.guide). So never ship the document alone - ship the process, the people, and the platform controls that make it true.

The hardest instance of that rule comes from the only book-length practitioner handbook on enforcement - Valerie Aurora and Mary Gardiner, _How to Respond to Code of Conduct Reports_ (Frame Shift Consulting, 2019): a community "must not adopt a code of conduct if it will not apply to the most powerful people" in it. Never ship one the founders are exempt from.

## Detect the request first

Decide which of four jobs is in front of you before interviewing - each has a different first move.

1. **Live incident in progress** - someone is being harmed right now. Skip document work. Go to [references/incident-response-runbook.md](./references/incident-response-runbook.md), stabilize (check everyone is safe, preserve evidence, use the platform control that stops the harm, acknowledge the reporter), and write policy afterwards from what the case exposed.
2. **No code of conduct yet** - run the full workflow below.
3. **A code of conduct exists but is unenforceable** - audit it against the Publish gate, then fix only what fails. Do not rewrite a document the community already knows.
4. **Moderation exists, structure does not** - the team is improvising. Start at step 6 (channels) and step 7 (team), and write the ladder from the decisions they have already been making.

## Interview

Ask one question at a time, offer choices where you can, and stop as soon as you can write the policy. Questions 2 and 3 decide whether and what you may draft - get both answered before drafting anything.

1. Which surfaces should this cover - repository and issues, chat, forum, mailing list, project social accounts, in-person or virtual events?
2. Is there an entity behind the community - a company, a foundation or fiscal host, or nothing but volunteers? What body sits above the moderators when they deadlock or when someone contests a decision?
3. Would the policy be enforced against the founder, the top maintainer, or the biggest customer? If not, say so now.
4. Who moderates today, and what is the effort ceiling: how many people, how many hours a week each, and whether anyone has authority to change platform settings or spend money?
5. Is there a date this has to be in place by - a live case running right now, a launch, an event, a board or foundation deadline?
6. Do you want this case closed, or a structure that keeps working after the people who wrote it leave?
7. Roughly how many members, and what is the daily volume of messages, issues, and new joiners?
8. Is there an existing code of conduct or set of rules? Was there an incident handled badly enough that members still remember it?
9. Which problems are actually frequent right now: harassment, self-promotion spam, low-quality or AI-generated submission floods, off-topic drift, hostile technical arguments, brigading from outside?
10. Are members mostly employed developers using this for work, or individuals on their own time? Any minors, any customers under contract, any competitors in the room?
11. Constraints: languages and timezones to cover, privacy law that governs the records, and whether anonymous reporting must be possible?

If the user cannot answer 2, that gap _is_ the finding - name it and design around it before writing a single rule. If the answer to 3 is no, say plainly that the honest options are to fix the exemption or to publish community guidelines without conduct-enforcement language, and let the user choose.

Answers to 4, 5 and 6 re-rank the ranked menus below, and say which moved what:

- A live case or a hard date promotes the responses that stop harm today - platform controls, content removal, the reporting channel - and defers the structural work that only pays off later.
- A "keep working after we leave" answer promotes the systemic fix and earned trust levels, both of which lose on ratio in any single case and win across a year of them.
- A low effort ceiling deletes rungs and deliverables outright rather than parking them at the bottom, and shortens the published ladder to what the team can actually execute (Publish gate, item 11).

## Workflow

1. **Map scope and jurisdiction.** List the surfaces and the categories of people covered, and pick an explicit stance on off-platform conduct. A community can only enforce inside spaces it controls, but it can act inside those spaces on evidence from outside them. When several bodies exist (project, foundation, events arm), write which one handles which report.
2. **Choose a base document and adapt it.** Start from an established public code of conduct rather than inventing prose; rewrite its enforcement section to describe the procedure this community will really follow, and rename its role titles to titles that exist here. Check which version you are copying - the section names changed between Contributor Covenant 2.1 and 3.0. See [references/code-of-conduct-outline.md](./references/code-of-conduct-outline.md).
3. **Write the standards from real incidents.** Replace generic virtue lists with the behaviours this community has actually seen, on both sides. A moderator needs a line they can point at. Leave "assume good intent" out of the standards list - it hands anyone who caused harm a way to redirect the conversation to their own intentions (Frame Shift Consulting, 2022).
4. **Design the ladder.** Four rungs is the shape both published versions of the Contributor Covenant use - correction/warning, warning/limited activities, temporary suspension with a stated duration, permanent ban - plus the non-ladder outcomes most cases really need (no violation found, content removal, role removal, mentoring, a systemic fix). Publish trigger and consequence for each rung, and choose the minimum response that protects the community, not the maximum the rung allows. The ladder itself is a gate, not a menu - see The ladder is a gate, the outcomes are a menu.
5. **Decide what becomes visible.** Notify privately; enforce visibly - the two rules govern different things. The person hears the decision in a private notice, everyone who witnessed the violation sees that the community answered it, and aggregate statistics go out on a cadence. Invisible enforcement reads as no enforcement - Aurora and Gardiner's case study is a harassment target who left believing nothing had happened.
6. **Build the reporting channels.** People report more when they know who reads it:
   - a private primary channel
   - a second path for reports _about_ the primary recipient
   - an anonymous option if feasible
   - a stated acknowledgment target you can hold
   - a no-retaliation rule
   - the names of the people who receive reports
7. **Staff the team.** Separate day-to-day moderators from the body that decides sanctions. Size the deciding body so it still works when a third of it is unavailable, then set:
   - tiered powers
   - recusal duties
   - a per-person load cap
   - coverage across the community's real hours and languages
   - terms with a cap on seats from any single employer

   See [references/platform-controls.md](./references/platform-controls.md).

8. **Write the runbook.** Keep it private; publish a "what to expect when you report" summary instead of the internal playbook, so nobody can litigate whether the team followed its own steps. Cover:
   - deadline clock, intake, evidence preservation
   - recusal grades, interview order, decision rule
   - notification templates, case-record schema, retention

   See [references/incident-response-runbook.md](./references/incident-response-runbook.md).

9. **Pre-configure platform controls.** Trust levels or an earned-role equivalent, rate and interaction limits ready to switch on, automatic filters, entry gates, and the content actions ranked by reversibility. Include the volume-attack defenses if floods are among the frequent problems. Rank the controls by inflow stopped per moderator hour, not by how quickly each can be switched on:

   - efficiency: rate and interaction limits > entry gates > earned trust levels > automatic filters > individual bans > manual triage of every item
   - effort: rate limits == automatic filters (one config change, then self-running) > entry gates (one config change, plus a join-conversion cost you keep paying) > earned trust levels (a week to design, then self-running) > individual bans (minutes each, forever, scaling with whoever is attacking) > manual triage (a standing job that grows with the community)
   - value: earned trust levels (raise the floor under every future member, permanently) > rate limits and entry gates (cut inflow at the source) > automatic filters (catch known patterns only, and never the new one) > individual bans (remove one actor, who returns under a new account) > manual triage (resolves each item and prevents none)
   - compliance cost: rate limits == automatic filters == trust levels (platform-native, collecting nothing new) > entry gates (email or identity verification collects personal data and can need a privacy notice, more so where minors are plausibly present) > individual bans (a conduct decision, so a case record and an appeal path)

   - Rate limits and automatic filters tie on effort because each is a single settings change nobody has to maintain.
   - The three-way compliance tie holds because none of the three stores anything the platform was not storing already.
   - Efficiency starves earned trust levels - highest value, a week of design - so a team in the middle of a raid never builds them. Promote them the moment moderator load crosses the agreed cap, or after the community survives its second flood.
   - Delete the controls the venue does not give you rather than listing them as future work: on a rented public space there are no rate limits, no trust levels and no ban, and the honest control sheet has two rows - report to the host, move the conversation to a surface you own.

10. **Publish, announce, rehearse.** Ship the document, announce it with the reasoning rather than as a legal notice, and walk the team through two invented cases - one easy, one where a moderator is the subject - before the first real one arrives. Repeat the rehearsal whenever a new member joins the team.
11. **Set the review loop.**
    - Aggregate statistics on a fixed cadence.
    - An annual anonymized trends report.
    - A ladder review triggered by any case the team found hard to place.
12. **Persist the decisions.** If your environment has persistent memory, record these so later work in this community does not relitigate them:
    - the scope stance
    - the ladder
    - the escalation body
    - the response-time target

## The ladder is a gate, the outcomes are a menu

A serious code-of-conduct breach - harassment, threats, sustained targeting, anything where a person is being harmed right now - is a gate. The breach determines the rung, and no ratio gets a vote. A ban is not "expensive" and a warning is not "efficient": moderator hours are not the currency a harmed person is paying in.

Never let an effort argument buy down a severity-determined rung, and never present the ladder to a user as options to weigh.

Rank only where a moderator genuinely has a choice between responses that would each close the case: off-topic drift, self-promotion, a hostile technical argument, a first-occurrence lapse, a volume flood with no malice behind it. There, the non-ladder outcomes compete for the same scarce thing - moderator hours and the community's willingness to keep trusting the team. Rank them by recurrence prevented per unit of that:

- efficiency: systemic fix > content removal > role removal > public statement of the response that would have applied > mentoring
- effort: content removal == public statement (minutes, one moderator, no coordination) > systemic fix (a day to design one rule, template, or channel change) > role removal (a conversation plus a governance decision) > mentoring (a standing commitment across weeks, which can still fail)
- value: systemic fix (removes the class of incident, so every case it prevents afterwards is free) > role removal (removes the authority that made the behaviour harmful) > mentoring (keeps a genuinely well-meaning contributor - rare, and real) > content removal (resolves the visible instance and nothing structural) > public statement (tells the community the standard held)
- relationship cost: content removal == systemic fix (neither names a person, so neither spends any) > public statement (asserts a standard without naming anyone) > mentoring (spends a moderator's goodwill and hours, and the mentee's) > role removal (permanently changes someone's standing, and usually costs the community that person)
- compliance cost: systemic fix == content removal (no personal data, no decision about a person, no appeal) > public statement (a factual claim about an incident, so legal review once it names anything identifiable) > mentoring (a commitment the community can be held to) > role removal (a conduct decision: case record, right of appeal, and in a company-run community an HR and employment-law interface)

Two ties, both genuine:

- Content removal and a public statement cost the same effort because each is one person writing for a few minutes with nobody to consult.
- Content removal and a systemic fix cost the same relationship because neither one names anybody - that is exactly why they are the two a tired team should reach for first.

The order starves mentoring, which is highest on relationship investment and slowest to pay. It is never a substitute for a sanction when harm occurred. Promote mentoring anyway when three things hold together:

- the person is load-bearing for the project
- the behaviour is a skills gap rather than a values gap
- a specific moderator has volunteered the hours

This order is a default, not a law. Re-rank it against what the interview already told you:

- a volunteer project with no governance body cannot do role removal at all and should not list it
- a community whose frequent problem is submission floods gets almost everything from the systemic fix and nothing from the rest
- a company-run community with an HR interface can act on role removal in a week where a foundation takes a quarter

## Deliverables

- `CODE_OF_CONDUCT.md` - public, in the repository root or the platform's rules surface.
- **Conduct response runbook** - private, team-only, following the runbook template.
- **Public "what to expect when you report" page** - the reporter-facing summary of that runbook.
- **Moderator roster and agreement** - who holds which powers, coverage map, load cap, recusal and confidentiality duties.
- **Platform control sheet** - which control answers which situation, and who can apply it.
- **Announcement post** - what changed, why, where to report, what happens next.

Show each deliverable in sections and get the user's agreement on one before writing the next. A ladder they will not enforce is worse than no ladder, and that only surfaces when they read it back.

Write them in this order when the team cannot produce all six at once - reports protected per hour of writing, not shortest document first:

- efficiency: reporting channels (with named recipients and the alternate path) > enforcement ladder > `CODE_OF_CONDUCT.md` > platform control sheet > runbook > moderator roster and agreement > announcement post
- effort: reporting channels == announcement post (an hour each) > enforcement ladder (a session with the team over real past cases) > `CODE_OF_CONDUCT.md` (adapt a base document, then argue the standards) > platform control sheet (a day of clicking through settings and writing down what each one does) > moderator roster and agreement (weeks, because it needs people to say yes) > runbook (the longest document here, and the one nobody reads until a case arrives)
- value: reporting channels (nothing else in the list does anything until a report can reach someone) > enforcement ladder (turns each case from an argument into a lookup) > runbook (stops the delay that is the dominant enforcement error) > `CODE_OF_CONDUCT.md` (the public promise the rest makes true) > moderator roster (decides whether item 11 of the Publish gate can hold) > platform control sheet > announcement post

This is a write order, not a ship order: the Publish gate still requires all eleven items before anything goes out. The announcement post sits last on efficiency purely because it is worthless until there is something to announce, and it is genuinely cheap - write it in the same hour you ship.

## Invocation examples

Expect requests in roughly these shapes. Each one enters at a different point.

- _"We're 400 people on a chat server for our open-source project and it's getting nasty. Write us a code of conduct."_ → job 2, full workflow, chat-class platform controls.
- _"Someone just reported one of our maintainers to the maintainers' alias. What do we do?"_ → job 1, runbook first, then close the missing-alternate-channel gap that caused the awkwardness.
- _"We copied the Contributor Covenant two years ago and never used it. Is it any good?"_ → job 3, audit against the Publish gate, report pass/fail per item, fix only failures.
- _"Our issue tracker is drowning in AI-written bug reports."_ → job 4, but route to volume defenses rather than the behaviour ladder; there is usually no malice to escalate against.

Expected output shape for a full run - the last two sections are review output for the user, not shipped documents:

```
## Scope and jurisdiction
Surfaces · people covered · off-platform stance · which body handles what

## Enforcement ladder
Table: rung | trigger | consequence | who may apply it
Non-ladder outcomes available

## Reporting
Primary channel (named recipients) · alternate path · anonymous option
· acknowledgment target · no-retaliation clause

## Response team
Roster · powers per tier · coverage map · recusal rules · escalation body

## Runbook summary
Deadline clock · intake · investigation · decision rule · notification · records

## Platform controls
Control → situation → who applies it, per surface

## Publish gate
Each of the 11 items: pass / fail / how to fix

## Open questions for the user
```

## Community types that change the answer

Scope, ladder shape, reporting channels, records, and platform controls transfer unchanged across community types. Four things differ.

- **Company-run, professional audience.** Members are identifiable and often employed by customers or partners. Name the interface to HR and legal before an incident, decide who may speak publicly, and expect standing soft conflicts for every vendor employee on the response team. Sanctioning a paying customer's employee is a commercial decision as well as a conduct one - agree in advance who makes that call.
- **Company-run, individual developers.** Higher anonymity, more throwaway accounts, more raids. Weight entry gates and rate limits over identity-based measures, and check whether minors are plausibly present, which changes both moderation and data handling.
- **Volunteer open-source project.** There is no HR and no budget. Name the escalation body above the team anyway - a foundation, a fiscal host, or a written group of senior maintainers - because a team with nothing above it has no exit from a deadlocked case.
- **Rented public space.** On a platform you do not own, the host's rules outrank yours and you cannot ban anyone; your realistic tools are reporting to the host and moving the conversation to a surface you control.

## Responses that make things worse

First drafts reach for these because they sound kind. Aurora and Gardiner name the first, third, fourth and fifth as responses that fail to stop harm or cause more of it. Keep those four out of the ladder and out of the runbook.

- **Requiring an apology**, or asking the harmed person to accept one. A compelled apology destroys the only signal worth reading: whether the person would have apologised unprompted. Contributor Covenant 2.1's first rung says "a public apology may be requested" - a line carried into the most-adopted base document in open source (40,000+ projects, per opensource.guide) - and 3.0 drops it.
- **Mediating as a substitute for a decision, or without both parties' consent.** Framing "someone is harming people here" as "those two don't get along" quietly releases the team from acting, and mediation nobody agreed to is itself a harm. Following Django's manual: facilitated communication between the parties is permitted, but only as an add-on after the team has made and recorded its own decision, and only with everyone's informed consent - never in place of a decision, and never proposed to a harmed person as the response.
- **Letting the reported person stay on condition they avoid the person who reported them.** Either they are not a threat, in which case the condition is unnecessary, or they are, in which case the community is not safe either.
- **Asking the harmed person to choose the consequence.** Show them the proposed response before announcing it - that catches missed facts and retaliation risk. Letting them decide it exposes them to blame for the outcome.
- **Doing nothing because the account is gone or unidentified.** State publicly what the response would have been.

See [references/incident-response-runbook.md](./references/incident-response-runbook.md) for the notification wording that follows from these, including a worked bad-versus-good pair.

## Publish gate

Do not ship until all eleven hold. Item 1 is Aurora and Gardiner's rule; the other ten each name a documented failure mode. The eleven-item set is assembled here, not a published checklist.

1. The code applies to the community's most powerful people, in practice and not only on paper.
2. The scope clause names surfaces and people, and takes a stance on off-platform conduct.
3. Every rung of the ladder has both a trigger and a consequence.
4. Time-boxed sanctions state their duration.
5. A private reporting channel exists and reaches a named group.
6. A second channel exists for reports about the primary recipient.
7. The acknowledgment target is a number the team can hold at current volume.
8. A no-retaliation statement is published.
9. An escalation body above the moderation team is named.
10. The case-record location, access list, and retention rule exist in writing.
11. At least two people can execute every action the ladder promises.

Failing item 11 with a four-rung ladder and one exhausted maintainer means the ladder is fiction - shorten it to what one person can do, and say so, rather than publishing a promise the community will watch break.

## Operating metrics

Track five, review them on the same cadence as the statistics report. The set of five is a selection made here, not a published standard.

- **Acknowledgment within target** - share of reports acknowledged inside the published window.
- **Cases with a recorded outcome** - anything less than all of them means the ladder is being applied from memory.
- **Median time from report to resolution** - the number reporters feel, and the one that decides whether the next person bothers reporting.
- **Moderator load** - actions and cases per person per week, against the agreed cap. Rising load with a flat roster predicts the next resignation.
- **Repeat-violation rate** - sanctioned members who violate again. A rate near zero can mean the ladder works, or that nobody reports anymore; read it next to report volume, never alone.

For flood-type problems, add submission rate and valid share, since the goal there is a lower inflow rate, not more bans.

**Where the numbers come from.** Published acknowledgment windows exist and can be quoted: one business day (Django), three business days (CNCF), and 24 hours to acknowledgement plus 10 business days to a decision (Aurora & Gardiner's worked example). The compliance _rate_ against those windows is a different matter: treat 95% acknowledgment-within-target and 100% of cases carrying a recorded outcome as starting baselines set here - reasonable gates to design against, not industry benchmarks.

Say which is which when you hand the numbers to a user, and recalibrate the baselines from the team's own first quarter of data. [references/published-findings.md](./references/published-findings.md) lists every sourced figure in this skill with its origin and its limits.

## Failure modes

| Symptom                                                          | Fix                                                                                                                             |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Code of conduct exists, nobody has ever enforced it              | Build the team and runbook first, then republish with the real process                                                          |
| The rules are visibly not applied to a founder or top maintainer | Stop. Fix the exemption or drop the conduct framing; a selectively enforced code is worse than none                             |
| The only reporting address belongs to the person being reported  | Add the alternate path and publish it in the same paragraph as the primary                                                      |
| Sanction invented after the incident                             | Publish the ladder before the next case; retrofitting a rule turns an incident into a governance crisis                         |
| Everything handled in DMs, community sees nothing                | Keep the notification private, publish the fact of a response, and publish aggregate statistics on a cadence                    |
| Similar cases get different outcomes                             | Keep case records and check prior violations before deciding                                                                    |
| Every case stalls in deliberation                                | Fix a decision rule and a decision deadline in advance - the dominant enforcement error is delay, not haste (Aurora & Gardiner) |
| Team drowning in spam or low-quality submissions                 | Switch from individual bans to rate limits, entry gates and submission requirements                                             |
| One moderator handles everything                                 | Rotate duty, cap weekly load, recruit from observed helpers in the room                                                         |
| Chat evidence vanished when the message was deleted              | Archive before removing; the case record carries the evidence chat does not keep                                                |
| A suspension outlived its stated end date                        | Schedule the restoration the day the sanction is applied                                                                        |
| Every team member is conflicted on a case                        | Escalate to the named body; if none exists, close that gap first                                                                |
| Members argue the team broke its own published procedure         | Publish the reporter-facing summary; keep the detailed playbook internal and revisable                                          |

## References

- [references/code-of-conduct-outline.md](./references/code-of-conduct-outline.md) - document skeleton, the 2.1-versus-3.0 section map, scope wording, ladder table, and a weak/workable example pair
- [references/incident-response-runbook.md](./references/incident-response-runbook.md) - deadline clock, report-taking checklist, recusal grades, decision rules, notification templates and their negative example, case-record schema, and transparency reporting
- [references/platform-controls.md](./references/platform-controls.md) - venue-class controls, earned trust levels, rate limits, volume-attack defenses, and moderator roster design
- [references/published-findings.md](./references/published-findings.md) - every sourced figure and claim with its origin and limits

Cross-skill references:

- samber/developer-relations-skills@developer-community-health - measuring community health
- samber/developer-relations-skills@oss-issue-triage - technical issue workflow (labels, templates, stale policy)
- samber/developer-relations-skills@oss-governance - project decision rights and succession
- samber/developer-relations-skills@oss-contributor-onboarding - first-contribution path
- samber/dev-event-organizer-skills@event-code-of-conduct - for single-event conduct policy and on-site response; this skill covers the ongoing community, including events it runs as one surface among several
