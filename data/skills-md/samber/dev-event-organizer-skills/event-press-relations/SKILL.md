---
name: event-press-relations
description: Run earned press coverage for a technical event - a one-way ask, not a barter deal. Covers whether to pursue press at all (most community events correctly do not), a two-lane accreditation policy for editorial journalists and independent bloggers or creators, the ungated media page, announcements pegged to the CFP, lineup, programme, on-sale and wrap-up beats, the embargo posture, the on-site press operation and interview logistics, and the single spokesperson designated before an incident needs one. Use whenever asked about press accreditation, a press kit or media page, pitching journalists about an event, embargoed announcements, a press room, or who speaks to reporters. Do NOT use for barter media partnerships - use samber/dev-event-organizer-skills@event-media-partnerships.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event Press Relations

You pursue coverage the event does not control and cannot trade for. Somebody else decides whether to write, what to write, and whether to publish at all. That asymmetry is the whole skill.

Make a "yes" cheap for a journalist or a creator to give. Make two irreversible failures less likely:

- A refusal that becomes a public dispute.
- A statement that cannot be unsaid.

Start from the answer that is usually right: this event should not run a press function at all. Two major developer-community events have no press accreditation policy.

- **PyCon US** has no current published press page, only a defunct 2013 one.
- **FOSDEM** requires no registration at all - "You don't need to register. Just turn up and join in!" - so "press access" there has no mechanism to grant or deny.

Read that as precedent, not as a gap they forgot to fill.

## What this skill owns, and what siblings own instead

- **Barter is not earned coverage.** A two-way visibility exchange with a newsletter, podcast or community - logo for blurb, no cash - belongs to `samber/dev-event-organizer-skills@event-media-partnerships`, which draws the same line from its side: earned coverage is "a one-way ask the event neither controls nor reciprocates". The moment something is promised back in return for words, hand the task over.
- **On-site press handling belongs here.** `samber/dev-event-organizer-skills@event-vip-management` routes it to this skill, which "claims accreditation, embargoes and on-site press handling", while that one keeps only "a _guest's own exposure_ to press". Claim the press room, the interview logistics and the shooting rules; hand back any question about one named guest's own photograph.
- **The event's own channels are not press.** Posting the lineup on the event's accounts is `samber/dev-event-organizer-skills@event-social-media`. Buying reach for it is `samber/dev-event-organizer-skills@event-marketing-plan`, whose channel menu carries a deliberately lightweight "pre-event press" rung and defers a real campaign here.
- **Attendee photo and recording consent is an access mechanism, not a press rule.** The colour-coded interaction-consent stickers (red: not interested in talking, or in being photographed) belong to `samber/dev-event-organizer-skills@event-accessibility-inclusion`, which owns whether they exist and how many. `samber/dev-event-organizer-skills@event-code-of-conduct` owns one adjacent line - "Harassing photography or recording." - and nothing else about consent. This skill owns only what press are told about the mechanism, and how it is enforced against a credential.

Policies change yearly and by edition, and staleness carries across every edition you copy from. Web Summit's accreditation page itself reads "Last updated: October 2020". Re-check any policy before adopting its wording.

Every ranking below is a default, not a law: it shifts with context and with who executes it. Re-rank all four menus after the interview, against what you already know about this organizer. Each of the following overturns a default rung:

- A team member who is a working journalist.
- An outlet that already covered a past edition.
- A keynote speaker whose name is itself the news.
- A venue with a spare room.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6-8 exist because the menus diverge sharply on time-to-effect, durability and effort. Nobody can pick those three defaults for the organizer.

1. Does any outlet, newsletter, podcast or independent creator cover this event's subject at this scale - name them. If nothing can be named, that answer alone decides Menu A.
2. Is registration meeting its curve without earned coverage? _(Together with Q1 this is the promotion condition for pursuing no press at all.)_
3. Community-run or vendor/company-run, and does any sponsor plan to make its own product news at this event? _(Sponsor product news is what forces an embargo posture the organizer does not control.)_
4. In-person, online-only or hybrid, how many days, and is a spare room or a quiet corner available? _(Online-only deletes both physical rungs on Menu C.)_
5. Expected attendance this edition, and last edition's figure if there was one.
6. What is the next calendar beat you would actually announce - CFP, lineup, programme, on-sale, day-of, wrap-up - and its date? Which of them is genuinely news rather than a page going live?
7. Is this one edition's push, or a relationship you want to compound across editions? _(A compounding mandate promotes the slow rungs: a warm outlet list, a pre-brief relationship.)_
8. What is the effort ceiling - organizer hours, how many comped seats you can spare, and who is willing to be the single voice on the record?
9. Has anyone ever been refused a press pass here, and how was it handled? _(A refusal already in the past changes Menu B's default immediately.)_
10. Is the event free and uncapped, or ticketed with a capacity?

## Community-run vs vendor-run

Ownership is the axis that moves rungs.

- **Community-run.** PyCon US and FOSDEM publish no accreditation policy at all, and DEF CON runs the lightest interview model there is: "If you are interested in connecting with a speaker for an interview the best process is to reach out to them directly". Lighter rungs are precedent here, not budget constraint.
- **Vendor/company-run.** Sponsors and the organizer both make product news, which forces an embargo posture and a brokered-interview expectation. CNCF-scale events "actively work with media and analyst partners to schedule briefings ahead of and during the conference".

Name which pole a recommendation assumes whenever the two differ.

## Workflow

1. Run the interview. Q1 and Q2 come first: a "nobody" plus a healthy registration curve ends this skill at Menu A's opt-out rung, and every step after it is wasted.
2. Set the press posture (Menu A). If it is _no press function_, say so, name where the residual exposure lives - the incident path itself is `samber/dev-event-organizer-skills@event-code-of-conduct`'s - and stop.
3. Build the media page before writing any policy, because the policy links to it. Keep it ungated: on large conferences' media pages every element downloads with no registration. Contents checklist, boilerplate rules, brand-asset rules and the past-edition stats that carry an event's credibility: [references/press-kit-and-calendar.md](references/press-kit-and-calendar.md).
4. Write the accreditation policy (Menu B) in plain language, and publish the refusal path with it. Eligibility wording, the proof stack, comp policy, caps and how to refuse without creating a dispute: [references/accreditation-policy.md](references/accreditation-policy.md).
5. Peg announcements to the calendar beats (same reference as step 3). Treat the lineup/schedule reveal as the single highest-leverage earned-media moment of the year, and plan it as a dedicated press moment rather than a page update. Once the contact list is long enough to repay the effort, add two refinements:
   - Note against each outlet what it actually publishes: a desk that reprints a plain numbers release, versus one that needs a market or economy angle with data attached. The pitch is then tailored once rather than re-guessed per send.
   - Offer one outlet or creator an early, exclusive angle ahead of the blanket release, instead of treating every recipient identically.
6. Set the embargo posture (Menu D) against Q3 and Q6 - sponsor product news is the usual reason a posture is forced on you.
7. Set the on-site depth (Menu C) and write the shooting rule before doors, naming what press may film, where, and what the attendee opt-out mechanism is. Press-room specifics, both interview models and the recording rules: [references/onsite-and-crisis.md](references/onsite-and-crisis.md).
8. Designate one spokesperson and one backup, and brief everyone else that they do not speak to press. Same reference: the four crisis cases and the five principles synthesized from them.
9. After the edition, harvest the stats into next year's fact sheet, and read each outlet and creator for whether they published at all.
10. Present section by section - posture, media page, accreditation policy, calendar, embargo posture, on-site, spokesperson - and get explicit approval per section before finalizing.

If your harness has persistent memory, record per edition:

- The posture and why.
- Who was accredited and who was refused, with the reason.
- Which beats were pitched and to whom.
- Who actually published.
- Every policy quoted, with the date it was checked.

Next edition starts from that instead of re-deriving a policy from other events' pages.

## Menu A - press posture

How much press function exists at all, before any specific journalist appears.

- effort (organizer hours, standing ownership, published policy, briefing): `dedicated press function > staged build > reactive contact only > no press function`
- value (earned coverage that reaches the audience this event needs): `dedicated press function > staged build > reactive contact only > no press function`
- compliance cost (review triggered, reversibility spent): `dedicated press function > staged build > reactive contact only == no press function`
- efficiency: `reactive contact only > staged build > dedicated press function > no press function`

**Value and effort run in the same order here, so no pair of rungs can put higher value against lower effort. None of the six pairs yields a strict-dominance relation, and the check finds nothing because it cannot: this menu is clean by construction, not by care, and that is not a pass.**

With value rank-identical to effort rank, the efficiency line collapses into cheapest-first among the rungs that buy anything, which is the one ordering a ranking exists to improve on. It therefore rests entirely on each rung's own argument below. A reader who disagrees with one of those arguments has nothing mechanical to appeal to.

The compliance `==` is argued, and it is the one axis carrying information. A reactive contact publishes no criterion anyone can be refused against, and puts one briefed person on the record. No press function publishes nothing either, but the statement still gets made by whichever volunteer is standing nearest the reporter, and it is exactly as unretractable: equal exposure, one assigned and one not.

- **Reactive contact only** - the default. A named press contact and a boilerplate paragraph on the site: answer what comes in, initiate nothing, and name the single voice that speaks while everyone else is briefed to say nothing. That designation costs one sentence and covers the one failure that cannot be reversed, which is why the rung leads on efficiency while buying almost no proactive coverage. **Promotion condition**: move up one rung when Q6 names a beat that is genuinely news - a keynote whose name is itself the story, a first edition, a venue or format change - _and_ Q1 named at least one outlet or creator who has covered this subject before.
- **Staged build** - an ungated media page, a two-lane eligibility policy, and announcements mapped onto the annual calendar. A growing community event lands here, and most of the material in this skill gets used at this rung.
- **Dedicated press function** - the starved rung: top of value, top of effort, top of compliance cost, so efficiency never picks it. **Promotion condition**: the event exceeds roughly 500–1,000 attendees - a self-set graduation band, not a measured threshold - _or_ Q3 says vendor sponsors are making their own product news at it. The second trigger fires far more often than the first at a small vendor event.
- **No press function** - nothing published, nobody designated, press treated as ordinary attendees. Last on efficiency, because near-zero effort buying nothing on the axis being measured is a ratio of zero. **Promoted to first outright when Q1 names nobody who covers this subject at this scale and Q2 says registration meets its curve without earned coverage** - the most common right answer for a community technical event, with direct precedent in both PyCon US and FOSDEM.
  - Every rung above it then manufactures a press function for an audience of nobody. The residual incident exposure does not vanish: the reporting and response path is `samber/dev-event-organizer-skills@event-code-of-conduct`'s, and what is absent is only a press-facing voice nobody is asking for.
- **Deleted when Q8 says nobody is willing to be the single voice on the record: the dedicated press function.** Delete it from this menu and from the axis lines above. A press operation whose spokesperson slot is empty produces a press conference answered by whoever is nearest, which is the failure the whole rung was bought to prevent.

## Menu B - accreditation breadth

Who gets a credential, and against what published bar.

- effort (policy drafting, per-application screening, refusal handling): `outlets plus creators with a stated bar > traditional outlets only > open > none`
- value (coverage reaching the developer audience, from people who will actually publish): `outlets plus creators with a stated bar > open > traditional outlets only > none`
- compliance cost (review triggered, reversibility spent): `traditional outlets only == outlets plus creators with a stated bar > open > none`
- efficiency: `open > outlets plus creators with a stated bar > traditional outlets only > none`

**Dominance check - clean by care.** Value and effort disagree on exactly one of the six pairs, which yields one strict-dominance relation: _open_ beats _traditional outlets only_ on value while costing less effort. The efficiency line has to place open above it, and it does. The other five pairs have value and effort rising together, so a ratio decides them rather than dominance.

State that one relation out loud, because it runs against instinct. A proof-heavy journalists-only policy at a developer event loses on both halves at once:

- **On value**, it excludes by definition the constituency that most reliably reaches developers.
- **On effort**, it costs more to administer than letting everyone in, because every application must be screened against a proof stack.

The compliance `==` is argued. Both lettered rungs publish a criterion that a refused applicant can quote back publicly, and neither refusal can be un-made once they post about it. Adding a creator lane doubles the paperwork, not the class of exposure.

**This menu starves nothing, and that is a finding rather than an omission.** The usual casualty of an efficiency order is the rung that tops both value and effort, since it loses every round. Here the value leader (_outlets plus creators with a stated bar_) also leads on effort, yet still finishes second on efficiency, close enough to the default that the promotion condition below reaches it in one step.

Nothing on this menu is both worth having and permanently unreachable, so there is no starved option to name and no rescue condition to write.

- **Open** - the default: anyone who says they are covering the event and names where it will run gets a comped seat. No proof stack, no second form, near-zero effort - and at a small community event where three people ask, it is what already happens. **Promotion condition**: move up one rung the first time applications exceed the comped seats Q8 says are available, or at the first refusal (Q9) - a refusal with no published criterion is the dispute this menu exists to avoid.
- **Outlets plus creators with a stated bar** - two lanes in plain language, reviewed separately: a Press lane for editorial journalists and freelancers on assignment, and a Creator lane for bloggers, podcasters and video creators. SXSW runs exactly this split with two different intake forms - "Submit the Press Application if your primary work is editorial journalism... Submit the Content Creator Application". Set the creator bar yourself and publish it, and read the warning below before borrowing anyone else's number.
- **Traditional outlets only** - the editorial-journalist lane with the commercial exclusions and the proof stack. RSA Conference's published line is "Those with sales, social media, marketing or account management roles will not be considered for press [accreditation]", and MWC/GSMA requires 4–5 relevant bylined articles published within the last three months plus, for freelancers, a valid assignment letter - "A press card alone will not be accepted as press credentials". It costs the most administration of the two mid rungs and buys the least developer reach, which is why the dominance relation lands on it.
- **None** - no accreditation, no comped press seats, reporters attend on whatever ticket exists. Last on efficiency at a ticketed event, where it means a reporter pays or does not come. **Promoted to first outright when Q10 says the event is free and uncapped**: a reporter simply walks in, exactly as at FOSDEM, and an accreditation process would be a form standing in front of an open door.
- **Deleted when Q8 says there are no comped seats to spare at all: open.** Delete it from this menu and from the axis lines above. Open accreditation whose comp promise cannot be honoured produces an accepted applicant turned away at the desk, which is a worse refusal than a policy-based one and lands on the day rather than in advance.

⚠️ **On borrowing a creator threshold.** MWC Barcelona (GSMA) publishes a quantitative creator bar - 100,000 or more subscribers or followers, and videos averaging 2,500 views. That is **one event's bar for its own creator lane at MWC's scale**. Never present it as a standard, and never transfer it to a community event's policy. Set a bar proportionate to your own audience, and say it is yours.

**Never set the creator bar below the press lane's.** MWC/GSMA, IBIE Baking Expo, IFEBP and ALA all hold the creator lane to the stricter bar: every published policy with a separate creator lane asks for an equal or higher level of verification than editorial press. The creator lane asks for a follower or view threshold, a minimum traffic count, or a year of on-topic publishing history, where the press lane asks only for a byline or an assignment letter.

"Anyone with a blog" is not how any of them read this lane. Full detail: [references/accreditation-policy.md](references/accreditation-policy.md).

## Menu C - on-site handling depth

What exists for press on the day.

- effort (day-of ownership, floor space, staffing, scheduling): `staffed press room with brokered interviews > working corner > named contact plus a written recording rule > no on-site provision`
- value (a reporter can actually file, and no attendee is recorded who opted out): `staffed press room with brokered interviews > named contact plus a written recording rule > working corner > no on-site provision`
- compliance cost (review triggered, reversibility spent): `staffed press room with brokered interviews > working corner > named contact plus a written recording rule`
- efficiency: `named contact plus a written recording rule > working corner > staffed press room with brokered interviews > no on-site provision`

**Dominance check - clean by care.** One strict-dominance relation exists across the six pairs: the _named contact plus a written recording rule_ beats the _working corner_ on value while costing less effort, because a table with power does not stop a camera and a written rule does. The efficiency line honours it. The other five pairs have value and effort rising together and are unconstrained.

The compliance axis is printed because recording consent is the one genuinely irreversible exposure in this skill. _No on-site provision_ is deliberately left off the ordering rather than scored zero: it triggers no review of its own, and that is exactly the problem. Press are on the floor anyway, recording, against a rule nobody wrote and nobody agreed to, and a published photograph cannot be unpublished afterwards.

An unmanaged exposure is not a low one.

- **Named contact plus a written recording rule** - the default: one person reachable on the day, plus a short published rule stating what press may film, where, and how the attendee opt-out is respected. Real events write this tightly. SXSW limits session video to the first 4 minutes of any speaker session, and bans tripods, lights and cabling in venue hallways. DEF CON forbids external production crews from filming inside the DEF CON area, and requires reporters to disclose press status when interviewing: "Violating this policy will forfeit your press [credentials]". **Promotion condition**: move up one rung when Q4 says multiple days - a reporter filing across two days needs somewhere to sit and power - or when accredited numbers exceed what one person can walk around with.
- **Working corner** - a quiet-ish table, power and wifi, plus the contact. Cheap and useful at community scale. It carries no rule on its own, which is why it loses the dominance round.
- **Staffed press room with brokered interviews** - the starved rung: top of value, top of effort, and efficiency never picks it. The constraints are real even at commercial scale. DEF CON's press room runs 6am to 6pm PST Friday–Sunday but explicitly "do[es] not have space for private interview rooms like you'll see at Black Hat", while CES reserves interview rooms bookable for up to 90 minutes. **Promotion condition**: the same graduation trigger as Menu A - past roughly 500–1,000 attendees, or vendor sponsors briefing media on their own news at your event.
- **No on-site provision** - press are attendees, nothing is staffed, nothing is written. Last on efficiency, and the only rung that leaves the consent question entirely unanswered.
- **Deleted when Q4 says online-only: the working corner and the staffed press room.** Delete both from this menu and from the axis lines above. What survives is the named contact and the recording rule, rewritten for the stream - who may clip it, how long a clip may be, and how a speaker or attendee opts out.

## Menu D - embargo posture

How unpublished material reaches a journalist before it is public.

- effort (list upkeep, scheduling, platform setup, chasing lift times): `credential-gated distribution > pre-brief under embargo > honour-system embargo on request > no embargoes`
- value (coverage landing at the moment the calendar needs it): `pre-brief under embargo > credential-gated distribution > honour-system embargo on request > no embargoes`
- compliance cost (review triggered, reversibility spent): `credential-gated distribution > pre-brief under embargo == honour-system embargo on request`; no embargoes carries none.
- efficiency: `honour-system embargo on request > pre-brief under embargo > credential-gated distribution > no embargoes`

**Dominance check - clean by care.** One strict-dominance relation across the six pairs: the _pre-brief_ beats _credential-gated distribution_ on value at lower effort, because a reporter who has talked to a human writes a fuller piece than one who downloaded a file, while the gated system mostly reduces leak risk rather than producing coverage. The efficiency line honours it. The remaining five pairs are unconstrained.

The compliance `==` is argued: both the pre-brief and the honour-system send put unpublished material in a reporter's hands under nothing but a stated lift time, and a break cannot be undone in either case. The pre-brief adds a conversation, not a different class of exposure. **Neither rung tells you how often an embargo actually holds** - a gate controls who sees the material at all, which is a different question from whether the people who see it wait.

- **Honour-system embargo on request** - the default: material goes to a named short list with a stated lift date and time including timezone, and nothing enforces it but the relationship. **Promotion condition**: move up one rung when Q6's beat is the lineup or schedule reveal - the single highest-leverage earned-media moment in the annual cycle - _and_ Q1 named an outlet that has covered a past edition, so there is a warm path to brief.
- **Pre-brief under embargo** - offer a small number of outlets or creators an early conversation ahead of the lift, with the material. It costs scheduling and a rehearsed spokesperson, and buys the fullest coverage available at this scale.
- **Credential-gated distribution** - a login-gated area holding embargoed releases that open as the lift times pass, run on a commercial wire-service distribution platform. Large conferences' media centres do exactly this: credentialed reporters log in to view embargoed releases, and the content is released as the embargoes lift. The starved rung on effort, and the only one with a vendor and a data review attached. **Promotion condition**: Q3 says sponsors are making product news at your event under their own embargoes - at that point the lift schedule is not yours to leak, and the gate is protecting somebody else's announcement rather than yours.
- **No embargoes** - nothing is held back; each item publishes on the public page when it is ready. Last on efficiency for the ratio-zero reason. **Promoted to first outright when Q6 finds nothing on the calendar that is genuinely news held back** - a schedule page going live on a planned date is a publication date, not an embargo, and dressing it as one teaches a journalist that your embargoes do not mean anything.
- **Deleted when Q3 says community-run with no sponsor product news: credential-gated distribution.** Delete it from this menu and from the axis lines above. A gated release platform standing between three friendly reporters and a speaker list is infrastructure guarding nothing, and parked at the bottom it returns next cycle as a budget line.

## Failure modes

- **Buying coverage.** Offering a sponsorship discount, a speaking slot or an exclusive in exchange for an article converts earned coverage into paid editorial, and both sides lose what made it worth having. If something is promised in return, it is `samber/dev-event-organizer-skills@event-media-partnerships`, priced honestly.
- **Refusing without a published criterion.** The refusal, not the policy, is what becomes public. Publish the bar before the first application, and refuse against it in writing with the criterion quoted back.
- **Generalising one event's creator threshold.** See the warning under Menu B. The 100,000-follower / 2,500-view bar is MWC's, for MWC.
- **Treating a schedule page as news.** Pitching a beat nobody would cover burns the one thing this skill accumulates, which is a journalist's willingness to open the next email.
- **Letting the recording rule live only in someone's head.** Write it, publish it with the accreditation policy, and make sure the on-site contact can point at the attendee opt-out mechanism `samber/dev-event-organizer-skills@event-accessibility-inclusion` owns.
- **Improvising the voice during an incident.** DEF CON's Goon guidance is blunt with staff and volunteers: "DO NOT SHARE photos or videos... DO NOT make any comments to reporters, and do not post about the incident [publicly]". Designate before, not during.
- **Merging the holding statement with the remedy.** Acknowledging fast and announcing a structural change are two messages days apart, and collapsing them either delays the acknowledgement or ships a half-considered remedy.
- **Assuming a quoted policy still holds.** Web Summit's accreditation page reads "Last updated: October 2020". Check the date on any page you copy from.

## Measurement

**No published figure quantifies what coverage volume does to registrations, and this skill states none rather than substituting a proxy that would read as one.** Every signal below is self-set. Fix each target before the edition, never after the data arrives.

- **Published-vs-accredited (self-set).** Of everyone credentialed, how many published anything at all. This is the only honest read on whether an accreditation bar is working, and it is the input to next edition's comp allocation.
- **Beat coverage (self-set).** Per calendar beat, who was pitched and who published. The lineup/schedule beat is the one to judge the year on.
- **Embargo integrity (binary).** Zero breaks before the stated lift time. Checkable, and the only measurement here with a correct answer rather than a target.
- **Consent breaches (binary).** Zero published images or recordings of anyone who used the opt-out mechanism. Also checkable, also with no acceptable non-zero value.
- **Voice discipline (binary).** During any incident, zero on-record statements from anyone but the designated spokesperson and their backup.

## Invocation examples

- "We're a 300-person community Go conference. Do we even need a press page, or is that a waste of time?"
- "A YouTuber with 40k subscribers asked for a free pass to cover our hackathon. What's our policy, and how do we say no to the next one without it blowing up?"
- "Our keynote is a name people will care about. How do we handle the announcement - embargo, pre-brief, or just post it?"
- "Two reporters are coming to our conference next month. What do we owe them on the day, and what are we allowed to tell them they can film?"

Expected output: a press brief, presented section by section for approval, with every figure labelled published or self-set.

1. The posture, with the interview answers that chose it - including the finding when the answer is no press function at all.
2. The media-page contents.
3. The accreditation policy, with its published criteria and refusal path.
4. The beat calendar with dates.
5. The embargo posture.
6. The on-site provision and the written recording rule.
7. The named spokesperson and backup.

## References

- [references/accreditation-policy.md](references/accreditation-policy.md) - eligibility wording with the published exclusions, the escalating proof stack, comp-vs-paid policy with DEF CON's exception, published caps, and how to write and deliver a refusal.
- [references/press-kit-and-calendar.md](references/press-kit-and-calendar.md) - the eight-element media-page checklist with real examples, boilerplate and brand-asset rules, past-edition stats that carry credibility, and the six announcement beats with lead times and who covers each.
- [references/onsite-and-crisis.md](references/onsite-and-crisis.md) - press-room specifics, the two interview models, photo/video and attendee-consent rules, embargo mechanics, spokesperson preparation, and the four crisis cases with the five principles drawn from them.

See also, same collection:

- `samber/dev-event-organizer-skills@event-media-partnerships` - the two-way barter deal this skill's one-way ask is not; it draws the same line from its side.
- `samber/dev-event-organizer-skills@event-social-media` - the event's own channels, which carry every announcement this skill also pitches.
- `samber/dev-event-organizer-skills@event-marketing-plan` - the acquisition plan whose lightweight pre-event press rung defers a real campaign here.
- `samber/dev-event-organizer-skills@event-vip-management` - a named guest's own exposure to press; it routes accreditation, embargoes and on-site handling to this skill.
- `samber/dev-event-organizer-skills@event-accessibility-inclusion` - owns the attendee photo/recording opt-out mechanism this skill's shooting rule enforces against.
- `samber/dev-event-organizer-skills@event-code-of-conduct` - owns incident reporting and response, and the one adjacent line on harassing photography.
