---
name: event-code-of-conduct
description: Write a technical event's code of conduct and build the enforcement pipeline behind it - what the policy has to say, who and which spaces it binds (attendees, speakers, volunteers, sponsor and booth staff, satellite events), the reporting channels including an anonymous path, response-team composition and rehearsal, the on-site incident runbook and its response clock, the sanctions ladder, which rungs carry an appeal, and the transparency report. Use whenever asked to write or review an event or conference code of conduct, set up incident reporting, staff or train a CoC response team, decide a sanction for an attendee, or handle an on-site incident. Do NOT use for accessibility provisions - use samber/dev-event-organizer-skills@event-accessibility-inclusion. Not legal advice.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Code of Conduct

You design the policy and the machine that enforces it for a single, dated, physically located event. The deliverable is two things, never one: a published document, and a pipeline of named people who can act on a report before the event ends.

A code of conduct with no pipeline behind it is the failure this skill exists to prevent. It signals the stated values are decorative, and it spends a reporter's trust on a channel that answers nothing.

- `confcodeofconduct.com`, the template most tech conferences still link to, says so about itself: its text "should not be considered as enforceable" and events using it should write their own policy.
- `opensource.guide` states the rule directly: "a code of conduct that isn't (or can't be) enforced is worse than no code of conduct at all."

## This is not legal advice

The output is a policy, a staffing plan, and a runbook. Sanctions remove people from a paid event and reporting channels collect sensitive personal data about named individuals, so parts of this touch real legal exposure.

- Contract wording: the clause binding a sponsor's staff, the ticket terms carrying the ejection-without-refund right. This goes to counsel. Route it via `samber/dev-event-organizer-skills@event-sponsor-agreement`, which owns that clause.
- Data retention, access and deletion rules for incident records go to whoever holds the organization's privacy obligations.
- Anything involving a crime, a minor, or an imminent physical threat goes to emergency services and counsel first, and to this process second.

Say this before the interview. An organizer who mistakes a published policy for legal cover is worse off than one with no policy.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 5-7 exist because the menus below diverge sharply on time-to-effect, durability and effort - their default orderings cannot be picked for the user.

1. What is the event: format (meetup, hackathon, single-day or multi-day conference), headcount, dates, and how many physical locations or venues?
2. Who is bound by it beyond ticket-holders: speakers, volunteers, sponsor and booth staff, contractors, press, satellite or attendee-run fringe events, an online chat that runs before and after?
3. Is this event run by one organizing entity, or does it operate under an umbrella brand or franchise agreement that binds third-party organizers? (This changes more below than scale does - see the split after this interview.)
4. Who could plausibly be the subject of a report and also sits on the organizing team, holds the budget, or is the event's headline name? Answer honestly; the whole design turns on it.
5. What is the date the policy has to be published by, and is it fixed by ticket sales opening, a sponsor contract, or the team's own target? (A hard date promotes the fast-to-stand-up rungs and compresses the drafting posture.)
6. Is this a one-off edition or an annual event the team intends to keep running? (A compounding mandate promotes the durable rungs - a rehearsed standing team and a records regime over a policy page written once.)
7. What is the effort ceiling: organizer hours, whether anyone will staff a channel live during the event, budget for external help, and how much of this the team is willing to keep running between editions?
8. What already exists that the default ordering assumes away: a parent foundation or umbrella body with its own incidents team, a prior edition's policy and records, an in-house lawyer, a written cultural-identity or values document, a volunteer pool already trained.

## Single-organizer event vs. multi-organizer franchise

Harassment is the same conduct and needs the same enumerated list whoever bought the ticket. What genuinely changes every mechanic below is **who controls the people in the room**.

- **Single-organizer event** (PyCon US model). One entity runs the venue, the volunteers, the program, and the sanctions: everything here is yours to decide and execute. The constraint is capacity - a small named team, a compressed on-site clock, no one above you to escalate to when the report is about a member of that team. PyCon US answers this with three individually named leads (Incident Responder, PSF Director of Operations, Conference Chair), each publishing separate contact details, so a report about one of them still has somewhere to go.
- **Multi-organizer franchise or umbrella event** (MLH member-event model). A central body owns the policy; local organizers adopt it because the membership agreement obliges them to: "you are expected to adopt, make publicly available, and enforce the MLH Code of Conduct." Local organizers cannot run an ad hoc process: "organizers must immediately involve the onsite MLHers or MLH Incidents Team." Your policy work is mostly _not drafting_ - it is verifying which document actually binds you, learning the central runbook, and knowing that the central body decides whether anything is said publicly, with local wording and timing agreed centrally first.

State which model a recommendation assumes whenever they differ. Most of the policy anatomy transfers to both; the response-team staffing menu, the appeals route and the public-statement authority do not.

Sponsor and booth staff sit on this seam either way. They are in scope of your policy - MLH, PyCon US and `confcodeofconduct.com` all name sponsors in their own scope clauses - but they are bound by a contract their employer signed, not by a ticket they bought. Say plainly in the policy that they are covered; the clause wording lives in `samber/dev-event-organizer-skills@event-sponsor-agreement`.

## Workflow

1. **State the disclaimer**, then run the interview.
2. **Pick the base-text posture** with the first menu below. If the event runs under a franchise or umbrella agreement, skip drafting: find the binding document and confirm which version applies.
3. **Write the scope clause**: which people, which spaces, which dates, and what happens off-site. Use [references/policy-anatomy-and-scope.md](references/policy-anatomy-and-scope.md); the scope clause is the section most events get wrong, and the one that decides whether a sanction is enforceable against the person who violated the policy.
4. **Choose the reporting channels** with the second menu. Write the two-part confidentiality promise into the policy: reports are confidential, and the reporter's identity stays confidential unless they instruct otherwise.
5. **Staff the response team** with the third menu, then publish its members' names in the reporting instructions. People report more when they know who receives it.
6. **Write the incident runbook** from [references/incident-runbook-and-response-team.md](references/incident-runbook-and-response-team.md): intake script, capture fields, escalation, decision method fixed in advance, the four-part notification, closure. Set the response clock in hours and days, and publish it.
7. **Publish the sanctions ladder before the first incident**, using [references/sanctions-ladder-appeals-and-transparency.md](references/sanctions-ladder-appeals-and-transparency.md). Inventing a sanction after the fact is what turns an incident into a governance crisis.
8. **Decide the appeal route and say which rungs carry one.** A uniform appeal right is rarely what an event means; MLH makes only suspensions and permanent bans appealable. State the asymmetry rather than implying it.
9. **Rehearse before doors open.** Walk the team through two or three practice cases. An unrehearsed team discovers its decision rule during the incident.
10. **Commit to a transparency report** for the edition, and to what it will and won't contain.

If your harness has persistent memory, store the scope decisions, the response team roster with their conflict declarations, the published response clock, and every sanction with its rung and reason. The next edition starts from a ladder that already exists and a record that makes a repeat offence visible - which is the only thing that lets rung 2 mean anything.

## Ranked menus

Every ordering below is a default, not a law; it shifts with context and with who executes it. Before presenting any of the three menus, re-rank it against the interview and say which answer moved which option:

- A hard publication date (Q5) promotes the rungs that stand up in an afternoon.
- A compounding annual mandate (Q6) promotes the durable ones.
- An asset the default assumes away (Q8) can beat the recommended rung outright - an umbrella body with its own incidents team makes most of the third menu moot, and an existing values document turns the starved option in the first menu into a copy-edit.

Where the user's constraints rule an option out, delete it from their plan rather than parking it at the bottom. A ruled-out option left on the list reappears as scope at T-2 weeks.

### Base-text posture

Efficiency (recommended order): **adapt an established text > adopt one verbatim > adapt plus a culture preamble**.

- value: adapt plus culture preamble > adapt > adopt verbatim
- effort: adapt plus culture preamble > adapt > adopt verbatim
- compliance cost: adapt plus culture preamble == adapt > adopt verbatim

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.**

- Value and effort are the same list, so one mechanism blocks every pair: the posture that buys a more usable document costs strictly more drafting.
- Compliance cost never separates a pair either - it restates the same order with the two adapting rungs tied.
- The check catches no misordering here; the ordering rests on the argument below.

Adopting verbatim is near-free and still loses, because the template names roles and contacts that do not exist at your event - which makes its reporting sentence unusable - and `confcodeofconduct.com` disclaims its own enforceability. Adapting costs an afternoon and fixes exactly that. The `==` on compliance cost is real rather than a dodge: both adapting postures keep the same Creative Commons attribution obligation and trigger the same single read by whoever holds legal authority; a culture preamble adds words, not legal surface.

**Default: adapt an established text.** Promote to the culture preamble whenever a stated identity or values document already exists.

A narrower variant of adopting verbatim: for a small volunteer-run event, linking directly to a peer event's own live, maintained code-of-conduct and values pages - rather than a generic template - inherits that peer's local legitimacy and enforcement record along with its text, at the same near-zero drafting cost. It is sound only when a suitable peer document exists in the same region or community and its scope (in-person versus online, jurisdiction) genuinely matches this event, and it still needs the same fix the generic template needs: confirm the linked policy is current and its host organization still exists before pointing to it, and replace any contact or role it names with this event's own.

**Starved: adapt plus a culture preamble** - highest value and highest effort, so efficiency starves it every round.

- It is the posture that makes a CoC a document people read rather than skim. !!Con's own policy states that "where many Codes of Conduct start and stop at preventing harassment, ours is part of an intentional effort to define the culture of !!Con events," and titles its expectations section "How to be !!Con".
- Promote it when the event has already done cultural-identity work (see `samber/dev-event-organizer-skills@event-cultural-identity`), which turns a week of drafting into an editing pass.

**Deleted, not demoted: writing your own from scratch.** Delete it unless the event has in-house counsel and a specific reason no template fits.

- MLH, PyCon US and `confcodeofconduct.com` all publish substantially the same enumerated prohibited-behavior list, a shared descent from the JSConf US 2012 and Ada Initiative template family rather than three independent arrivals. That lineage is exactly what makes it the list attendees and reporters have learned to look for.
- A from-scratch draft spends a week arriving at that same list minus whatever it forgets. What it forgets is exactly what a reporter needs to see named before they believe their case counts.

### Reporting channels

Efficiency: **published email alias > physically identifiable on-site responders > named conflict-of-interest alternates > anonymous intake path > staffed phone or SMS hotline**.

- value: physically identifiable responders > anonymous path > named alternates > published alias > staffed hotline
- effort: staffed hotline > physically identifiable responders > anonymous path > named alternates > published alias
- compliance cost: anonymous path > staffed hotline > published alias > physically identifiable responders == named alternates

The alias leads on efficiency because it costs minutes, works before and after the event, and is the address the printed policy has to carry. Visible responders lead on value because a distressed person reaches for someone they can see: PyCon US puts its trained responders in "brightly colored shirts", a channel with no online equivalent. The `==` on compliance cost holds because both visible responders and named alternates trigger the same single review - publishing an individual's name and contact, which is a consent conversation with that person, not a data-processing regime.

Compliance cost is a real axis here, unlike in most menus. Each channel carries a different exposure:

- **Anonymous path**: tops the axis because a report you cannot attribute is a record you cannot correct or delete on request, and a sanction built on it cannot be tested against the reporter. The retention, access and decision rules have to exist before the first report, since a wrong outcome is not reversible afterwards.
- **Staffed hotline**: puts call logs and possibly recordings of sensitive personal data in a third-party telco's hands.
- **Published alias**: creates an inbox of the same data that someone must own, restrict and retain under a written rule.

**Default: published alias plus named conflict-of-interest alternates plus physically identifiable on-site responders**, for any event with a physical day. Drop to alias plus alternates only for an online-only or pre-event-only scope.

**Starved: the anonymous intake path** - highest value against exactly the reports the other channels never receive, and high effort because it forces a decision convention that works with no reporter to go back to. Promote it whenever there is a power gradient inside the reporting population: paid staff, sponsor booth staff who answer to a sponsor, students at a university-hosted hackathon, or a response team that includes the event's most senior organizer. PyCon US publishes no anonymous _channel_ while accepting anonymous reports at intake; CNCF runs a documented relay where any committee member forwards a report without the reporter's name (project practice, not an event's).

### Response-team staffing

Efficiency: **a named published team of 3-6 > routing into an umbrella body's incidents team > an external trust-and-safety contractor**.

- value: named published team > umbrella body's team > external contractor
- effort: external contractor > named published team > umbrella body's team
- compliance cost: external contractor > umbrella body's team > named published team

Sizing 3-6 is deliberate: it has to still function with a third of it unavailable, which at a three-day event is a certainty. Fix the decision method in advance including tie and absence rules, and let it err toward taking action - the dominant observed failure is inaction and delay on valid reports, not haste.

The umbrella route is near-zero effort where it exists and unavailable everywhere else, so treat it as conditional rather than as a rung anyone can pick. Its compliance cost is that the affiliation agreement makes someone else's procedure binding on you and removes your discretion to reverse the outcome.

**Default: a named published team of 3-6**, with every member's name in the reporting instructions and a recusal rule that starts the moment a member realizes it applies.

**Starved: the external trust-and-safety contractor** - highest value in the one case nothing else answers, highest effort (procurement, briefing, a retainer, and handing an outside party attendee personal data). Promote it when the event's most powerful person sits on the organizing team and no independent body exists above them. A code of conduct that will not apply to the most powerful people in the community should not be adopted at all; a contractor is the only rung that answers that precondition when there is no board to escalate to.

**Deleted, not demoted: a single named organizer as sole responder.** Delete it for any event where that organizer is also the most senior person on the team, because the channel then cannot receive the one report most likely to need it, and one person deciding alone at 2am is not a process. Left at the bottom of a list it reappears as "we'll just have someone handle it" two weeks out.

## Failure modes

- **A published policy with no pipeline.** The headline failure, and the template's own maintainers name it. Fix: do not publish the policy until a named team, a working channel and a ladder exist.
- **Responders nobody can find.** An alias in a PDF is useless to someone in distress in a hallway. Fix: put trained responders in visually distinctive clothing and say so in the opening announcement.
- **No path for a report about the response team.** Fix: publish individual contacts for at least two more people, at least one of whom is outside the organizing team's chain.
- **A uniform appeal right that the team did not mean.** Fix: state which rungs are appealable, to whom, in what form, and by when. MLH restricts appeals to suspensions and bans, by written email with evidence attached.
- **Sponsors and booth staff treated as outside the policy.** Fix: name them in the scope clause, and confirm the sponsor contract carries the compliance clause and the ejection-without-refund right.
- **Handling a case entirely in private.** A case resolved with nobody told reads, correctly, as no enforcement - the documented failure is a target concluding nothing happened and leaving. Fix: everyone who knew about the violation learns that a response occurred; the notification is private, the fact of enforcement is not.
- **A local organizer free-lancing a public statement.** Fix: name in advance who holds public-statement authority, and agree wording and timing centrally before anyone speaks.
- **Adopting a ladder the team cannot execute.** A published rung nobody has the standing to apply is worse than a shorter honest ladder. Fix: cut the ladder to what the team can actually do with leadership backing.

## Measurement

Measure the pipeline, not the policy - a policy has no observable output until a report arrives.

- **Reports received per edition, per 100 attendees.** A rise after improving channels is a trust signal, not a deterioration. Treat any target for this rate as self-set, and never manage it downward.
- **Time from report to acknowledgment, and from report to stated outcome.** Measure against the clock you published. Two bands to choose between:
  - PyCon US: the three leads meet within 24 hours for non-urgent reports, and follow up with the reporter within one week.
  - Aurora and Gardiner's handbook (written for online communities): 24 hours to acknowledgment, 10 business days to a decision.

  An event's clock has to fit inside the event, which is why it runs tighter than a project's.

- **Share of reporters who received a closing message.** The target is 100%; anything less means reports are going into a hole.
- **Rehearsal completed before doors open.** Binary, per edition.
- **Transparency report published.** Binary, per edition.

Pass threshold, and iterate until it is met: every report acknowledged inside the published window, and every reporter told the outcome before the published follow-up deadline. That threshold is self-set, and the two published bands above are what make it realistic rather than invented.

## Invocation examples

- "We're running our first 300-person conference in four months and we need a code of conduct." → run the interview, adapt an established text, and staff a three-person named team before publishing.
- "Someone reported a speaker to us an hour ago and we don't know what to do." → skip to the runbook's intake and escalation steps in [references/incident-runbook-and-response-team.md](references/incident-runbook-and-response-team.md); safety assessment first, decision method second.
- "Our CoC has been up for two years but we've never had a report - is that good?" → audit the channels against the second menu; a silent channel is more often an unreachable one than a clean event.
- "A sponsor's booth staff was rude to attendees. Can we throw them out?" → scope clause first, then the sanctions ladder; the contractual ejection right lives in `samber/dev-event-organizer-skills@event-sponsor-agreement`.

Expected output:

- A policy document.
- A one-page reporting card for the printed program and the website.
- A response-team roster with contacts and recusal declarations.
- A runbook the team can follow at 2am.
- A published ladder.

## Reference

- samber/dev-event-organizer-skills@event-volunteers for recruiting and shift-scheduling people into the responder role this skill specifies.
- samber/developer-relations-skills@developer-community-moderation for the standing, cross-event community and its ongoing moderation - this skill's own policy and response team govern a single dated event only, and hand back to that skill for a report, a pattern, or a person that outlasts the event.
- samber/dev-event-organizer-skills@event-attendee-experience for the quiet room this runbook borrows as an intake space.
- samber/dev-event-organizer-skills@event-accessibility-inclusion for designing the event so violations against the groups this policy protects are less likely in the first place, and for the interaction-consent stickers whose photography boundary [references/policy-anatomy-and-scope.md](references/policy-anatomy-and-scope.md) enforces. Do NOT use this skill for your code of conduct; use the skill in the description instead.
- samber/dev-event-organizer-skills@event-comms-channels for the attendee-facing chat spaces and event app this policy has to cover - every channel it stands up is a space the scope clause must name, and its roster decides who is bound and who moderates.
- samber/dev-event-organizer-skills@event-cultural-identity for the values-in-the-room content a policy's preamble can carry - that skill defines the culture, this one writes the policy and the enforcement.
