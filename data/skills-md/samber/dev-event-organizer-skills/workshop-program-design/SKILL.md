---
name: workshop-program-design
description: Design how a hands-on technical workshop or training session actually runs, once the format decision has committed hours to it - facilitator coverage, participant prerequisites and environment setup, capacity ceilings, session length, materials, and what breaks when a room of laptops cannot reach the network. Use whenever the user mentions planning the sessions inside a workshop day, how many helpers a lab needs, writing prerequisites or setup instructions, capping workshop seats, bring-your-own-laptop versus a provisioned environment, or surviving bad venue WiFi - even if they never say "workshop". Do NOT use to place sessions in the grid - use samber/dev-event-organizer-skills@event-schedule-design instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Workshop Program Design

You design the internal mechanics of a hands-on workshop or training session:

- How many people can be in the room.
- Who helps them when they get stuck.
- What has to be true about their machine before they sit down.
- What they leave with.
- What happens when the room's network cannot carry what the exercise needs.

Your inputs arrive decided:

- Whether a workshop day or track exists at all, how it is bracketed against the talk days, and how it is ticketed - `samber/dev-event-organizer-skills@event-format-selection`. Do not re-argue any of it.
- Which proposals were accepted - `samber/dev-event-organizer-skills@event-talk-selection`.
- Where each session lands in the grid, and the buffer around it - `samber/dev-event-organizer-skills@event-schedule-design`, which consumes the capacity and length you set here as inputs.
- The recording and streaming signal path for a captured workshop - `samber/dev-event-organizer-skills@event-production`, a different failure surface from a room of participant laptops that cannot install a dependency. You stop at the attendee-side environment.

Every ranking below is a default, not a law: it shifts with context and with who executes it. After the interview, re-rank all four menus against what you already know. Any one of these overturns a default rung:

- An instructor who already runs this exact workshop commercially.
- A venue you have used four times and whose network you have measured.
- A sponsor providing the cloud environment.
- A cohort on employer-managed laptops.

## Interview

Ask one question at a time, multiple-choice where possible. Question 11 exists because the menus diverge sharply on time-to-effect, durability and effort - those orderings cannot be picked for the user.

1. Which part of the delivery is on the table: one session's mechanics, every session inside a workshop day, or a post-mortem on a workshop that went badly? Skip the menus already settled.
2. What must a participant be able to do at the end that they cannot do now - and can that be acquired by reading the material instead of doing it in the room?
3. Does the exercise need anything installed, downloaded or signed into on a participant's own machine: software, a toolchain, a vendor account?
4. Does any part of the exercise depend on a live network service while the session runs - a hosted console, an API, a package registry, a remote lab?
5. Can every participant be expected to bring a machine capable of running it, and be permitted to install on it? Would requiring one exclude anyone in the intended cohort?
6. Does the exercise run at distinct workstations or physical steps, or does everyone do the same thing at their own seat?
7. How many participants are expected, and what does the room actually give you: seats, movable furniture, power at the seats?
8. Who is in the room to help besides the person presenting, and are they competent in the material or only in the logistics?
9. What has the venue answered **in writing** about this room's network: sustained bandwidth, how many devices it holds, and whether it blocks unusual protocols or device types?
10. Will you, the organizer, be the party accepting a third-party platform's terms and issuing credentials on participants' behalf - and will any participant be a minor?
11. Three that re-rank everything:
    - By what date must this be ready.
    - Is this a one-off session or a curriculum you will run every edition.
    - What is the effort ceiling: organizer hours, people you can recruit into the room, and how reversible the choice has to be.
12. Did a prior edition's workshop network fail, and what specifically broke - bandwidth, a blocked protocol, a blocked device class, or the venue never answering?

## Hands-on commitment

The first decision, and the one most often skipped: does this session put hands on keyboards at all? Ranking (default, not a law - Q2 and Q9 re-rank it):

- effort (build, rehearsal, room support, day-of exposure): `full hands-on > demonstration only > no live hands-on`
- value, participants leave able to do the thing themselves: `full hands-on > demonstration only > no live hands-on`
- value, the content gets delivered whatever the room does: `no live hands-on > demonstration only > full hands-on`
- efficiency: `no live hands-on > demonstration only > full hands-on`

- **No live hands-on** - the material ships as published resources, or the content runs as a talk. On a delivery view this is _no workshop at all_, and it wins the efficiency round outright: nothing in it can fail on the day. It is an established practice rather than a cop-out. MLH's hardware guide builds a whole async layer for exactly this: "Async resources allow students to familiarize themselves with tools and concepts on their own schedule before the hackathon begins". The same guide tells organizers to "Limit the number of workshops during an event as they consume valuable building time". Note the boundary: whether the _day_ exists is `samber/dev-event-organizer-skills@event-format-selection`'s call, already made; whether _this session_ is hands-on is yours.
- **Demonstration only** - the instructor drives, the room watches, nobody installs anything. One machine and one connection can fail, and both are yours.
- **Full hands-on** - the default only for what reading cannot teach. MLH's pre-event workshop covers the component the participants will actually use, stating "This covers basic wiring and the necessary initial code upload". Promotion condition, keyed to Q2: the answer to "can it be acquired by reading" is no.
- **Delete, do not demote:** strike **full hands-on** from this menu and from the axis lines above when Q4 says the exercise needs a live network service and Q9 says the venue has not answered the network question in writing. Run the demonstration and publish the material instead. A hands-on session nobody can connect to is the specific failure this skill exists to prevent. A deleted rung parked at the bottom reappears as scope on the day.

## Facilitator coverage

How a stuck participant gets unstuck. Ranking (default, not a law - Q6 and Q8 re-rank it):

- effort (recruiting, briefing, coordination on the day): `stationed helpers per work area > roaming troubleshooter > structured peer pairing > solo instructor`
- value, a stuck participant gets unstuck before giving up: `stationed helpers > roaming troubleshooter > structured peer pairing > solo instructor`
- value, coverage that holds as the room grows: `structured peer pairing > stationed helpers > roaming troubleshooter == solo instructor` - argued tie: both put a fixed number of answerers in front of a variable number of participants, so doubling the room halves what each participant can get either way; the difference between them is where that one extra person stands, which this axis does not measure.
- efficiency: `structured peer pairing > roaming troubleshooter > solo instructor > stationed helpers`

⚠️ **The first value axis is rank-identical to inverse effort.** Recovery latency is a real quantity, but ordering the rungs by it discriminates nothing effort has not already ordered, and an efficiency line resting on it alone collapses into cheapest-first. The growth axis is therefore the only one doing work, and it alone is why peer pairing leads rather than the solo rung.

- **Roaming troubleshooter** - the default: MLH tells the workshop host to "have a backup speaker walking around to help troubleshoot for those who start falling behind", and, for a remote room, to "ask them to share their screen to troubleshoot their issues". One recruited person who knows the material, not a logistics volunteer - Q8 asks which you have.
- **Structured peer pairing** - the efficiency leader. Its help capacity grows with the room by definition, which is what wins it the growth axis. CS-classroom pair-programming pedagogy gives that a mechanism rather than a headcount argument: assigned driver/navigator roles, swapped every 5-10 minutes, keep a navigator watching the driver's screen for the whole session. "Structured" is the load-bearing word. The same guidance calls plain, role-free pairing the version that "can often lead to one, or both, learners quickly losing focus" - this rung's own unmanaged failure under a different name. It can still pair two people who are both stuck and nobody notices; check in with pairs on the cadence the roaming rung already keeps.
- **Stationed helpers per work area** - the starved option: top of latency, top of effort, so efficiency never picks it. MLH's tool stations say to "ensure a mentor is stationed nearby" and to "Ensure these stations are staffed by experienced volunteers". Promotion condition, keyed to Q6: the exercise genuinely runs at distinct workstations or physically distinct steps, so a helper posted at one covers everyone who reaches it.
- **Delete, do not demote:** strike **solo instructor** from this menu and from the axis lines above as soon as the hands-on menu lands on full hands-on. Someone in a room doing the exercise will be stuck while the instructor is mid-sentence, and no rung below the roaming one addresses that.

Size coverage from Q6 and Q7 and mark the figure as yours - this number must come from your own judgment, not an external standard.

## Prerequisites and environment

What has to be true about a participant's machine and accounts before the session starts. Ranking (default, not a law - Q3, Q5 and Q10 re-rank it):

- effort (build, maintenance, two support surfaces or one): `both paths offered > provisioned environment only > published prerequisites > nothing published`
- value, share of the room that can actually start: `both paths offered > provisioned environment only > published prerequisites > nothing published`
- value, independence from the room's network while the session runs: `published prerequisites > both paths offered > provisioned environment only > nothing published`
- compliance cost (review triggered, and reversibility): `provisioned environment only == both paths offered > published prerequisites > nothing published` - argued tie: both rungs put you, not the participant, in the position of accepting a platform's terms for a room of people and issuing credentials on their behalf; offering a second path alongside changes nothing about who signed.
- efficiency: `published prerequisites > provisioned environment only > nothing published > both paths offered`

- **Published prerequisites** - the default: most workshop pages fill a prerequisites section. They sort into three classes the sheet in [references/prerequisite-and-environment-sheet.md](references/prerequisite-and-environment-sheet.md) writes out: prior knowledge, machine state, and accounts. Accounts are the class most often forgotten and the one that fails worst at minute zero.
- **Both paths offered** - local machine _or_ a pre-configured environment, participant's choice. As one workshop puts it: "You will have the option of either doing the workshop on the laptop or using GitHub Codespaces and a pre-configured environment". Top of readiness, top of effort, because you now maintain and support two environments.
- **Provisioned environment only** - the starved option: it removes the hardware and install-permission barrier entirely. One workshop puts it this way: "Everything is done in a web browser (Chrome, Firefox) - no local commands or installations are needed on your laptop", with per-participant logins and a versioned preinstalled toolchain. Promotion condition, keyed to Q5 and Q10: participants cannot be expected to own a capable machine, or are not permitted to install on the one they bring, or requiring one would exclude part of the intended cohort.
- **Delete, do not demote:** strike **nothing published** from this menu and from the axis lines above the moment Q3 says anything must be installed, downloaded or signed into. An empty prerequisites section is a promise that nothing is needed; publish it empty only when that promise is true.

**Compliance concerns.** Standing up an environment for a room means you accept a vendor's terms on behalf of people who never read them, and you issue and hold credentials. Where Q10 says minors are present, that acceptance is made for someone who cannot make it themselves. Name the review it triggers:

- The platform's terms for third-party use.
- Your own data posture for credentials.
- The same consent question `samber/dev-event-organizer-skills@event-accessibility-inclusion` sets for participant data.

On reversibility the rungs genuinely differ. The asymmetry is this skill's own argument rather than a published one: an environment you built is torn down on your schedule; an account a participant created because you told them to persists after you stop, and you cannot delete it for them.

## Capacity: three ceilings, take the lowest

**No ranking here, deliberately.** These are three ceilings on one number, not alternatives with different value. Which one binds is a fact about your exercise and your room, not a choice with an efficiency ratio, so ranking them would be false precision. Compute all three, take the lowest, and say which one bound.

- **Room ceiling** - seats with the furniture the exercise needs. The typical band for a technical event's breakout rooms is 10-20 or 20-40 with chairs movable into a circle (see `samber/dev-event-organizer-skills@event-venue-sourcing`'s space program), and power at the seats is a separate question from seats.
- **Coverage ceiling** - how many people the instructor plus whatever the facilitator menu bought can actually reach before someone gives up. This number is yours; say so when you state it.
- **Exercise-throughput ceiling** - how many can get real hands-on time given what is genuinely limited: kit, per-participant logins, licence seats, physical stations. This is the ceiling most often missed, because it is invisible until the twenty-first person needs the ninth board.

One low-cost mechanic worth trying, though it traces to a single 2017 event and no current conference in the record runs it - see [references/capacity-length-and-network-evidence.md](references/capacity-length-and-network-evidence.md) for what's confirmed running today instead: ask attendees before the day to "vote for your favorite workshops", explaining that "This will help us determine which rooms to place them in". Demand collected before the day beats a guess made at scheduling time, and it is a cheap request to add to whatever pre-event mail `samber/dev-event-organizer-skills@event-attendee-email-sequences` is already sending.

Session length is observed, never prescribed: published workshops cluster on 45-minute granularity and land at 150-180 minutes for real hands-on sessions. The full record, with each workshop's event and length, is in [references/capacity-length-and-network-evidence.md](references/capacity-length-and-network-evidence.md). Hand the chosen length to `samber/dev-event-organizer-skills@event-schedule-design` as an input; do not pick a slot length by averaging across events.

## Network and dependency posture

What you do about the room's connection before you find out the hard way. Ranking (default, not a law - Q4 and Q9 re-rank it):

- effort (coordination, venue pressure, design constraint accepted): `remove the live dependency > clear the room's network in writing > declare the dependency with a fallback > assume the network holds`
- value, the session still runs when the room's network is bad: `remove the live dependency > clear the room's network in writing > declare the dependency with a fallback > assume the network holds`
- value, the exercise can still teach the topic: `assume the network holds == declare the dependency with a fallback == clear the room's network in writing > remove the live dependency` - argued tie across the three: none of them changes a single thing about what the exercise may contain; they differ only in what you know and what you said beforehand. Only the fourth deletes topics from what can be taught.
- efficiency: `declare the dependency with a fallback > clear the room's network in writing > assume the network holds > remove the live dependency`

- **Declare the dependency with a fallback** - the default, near-free: one workshop states "Internet is required as we would be using the cloud-based ClickHouse instance", another asks for internet access to a remote lab and names the participant-side fallback outright, "(Use Wi-Fi or your own data)". Policy breaks these sessions more often than bandwidth does: a VPN, an ad-blocker, a blocked protocol. The named causes are listed in [references/capacity-length-and-network-evidence.md](references/capacity-length-and-network-evidence.md).
- **Clear the room's network in writing** - promotion condition, keyed to Q9 and Q4: the exercise needs an unusual protocol, port or device class, or the venue has not answered. Policy, not capacity, is what breaks: MLH tells organizers to work with venue infrastructure and "ensure the network allows IoT and other devices, as these are often blocked by standard university networks", and a published workshop's own prerequisites hinge on "(RDP protocol allowed)". Ask the venue the written question `samber/dev-event-organizer-skills@event-venue-sourcing` already puts to them, plus the device count and the protocol list.
- **Remove the live dependency** - the starved option: top of resilience, top of effort, and the only rung that costs content. Promotion conditions: a venue that will not answer Q9, a prior edition where the room's network failed (**keyed to Q12**), or a topic that genuinely does not need the network. A cheap companion step: ask participants to pre-download, with MLH's own reason attached - "Encourage hackers to pre-download software drivers and IDEs ahead of time to reduce network load during the event".
- **Delete, do not demote:** strike **assume the network holds** from this menu and from the axis lines above whenever Q3 or Q4 says a participant must download, install or authenticate during the session. A whole room installing at once is a load case, not an assumption - and asking for pre-downloads exists to remove exactly this case.

## In the room, and after it

Workshop mechanics for day-of execution - see [references/coverage-and-room-mechanics.md](references/coverage-and-room-mechanics.md) for detail and negative examples:

- Build the recovery time into the plan rather than hoping it fits: "build time into your schedule to do breakout sessions, troubleshooting, and questions".
- Size the opening to the room: "For workshops with fewer attendees, we recommend starting with an icebreaker".
- Lower the cost of admitting you are stuck. MLH puts this squarely on the instructor: "be extremely aware of how intimidating code reviews and questions will be for participants".
- Give the material somewhere to live afterwards: "Have a channel in slack/Discord so hackers can ask follow-up questions about the workshop topic after it ends." Publish the window that access lasts (common examples are 72 hours or a month after the conference).

## Failure modes

- **Inventing a facilitator ratio.** Say "one instructor plus a roaming troubleshooter, sized from the room and the exercise" and mark the sizing as yours.
- **Prerequisites that list software and forget accounts.** Published workshops ask for a GitHub account, a vendor registration or a free product account as often as they ask for an install. An account needs a signup, an email confirmation, and sometimes an employer's SSO - all at minute zero, on the room's network, for everyone at once.
- **Treating a provisioned environment as the safe option.** It removes the local-install failure and replaces it with total dependence on the room's connection for the whole session, plus the compliance exposure above. It is safer only against the failures you named.
- **Copying a session length off another event's page.** Each event's length reflects its rooms, cohort and exercise. Take the granularity if it helps; do not take the number.
- **Letting the venue's WiFi answer be "it's fine".** Real network breakages are often policy - blocked device classes, blocked protocols, a VPN, an ad-blocker - none of which a bandwidth figure would have caught.
- **Reopening the format decision.** If the conversation drifts to whether the workshop day should exist or how to price it, that is `samber/dev-event-organizer-skills@event-format-selection` and it is already decided.
- **Confusing attendee-side failure with production failure.** A room of laptops that cannot install a dependency is yours; a dropped camera feed on the recording is `samber/dev-event-organizer-skills@event-production`.

## Measurement

Pick two or three. Decide in advance what result would change next edition, and write the metric and that trigger down before the session.

- **Ready at minute zero** (self-set): the share of the room that completed the prerequisites before arriving. This is the number that tells you whether to move up the prerequisite menu, and the only way to get it is to ask at the door.
- **Confidence, before and after** (sourced convention): a short "I am confident in my ability to..." rating for the specific skill taught, asked before the session starts and again at the end. This is the one metric here with a named precedent. The Carpentries run exactly this pair of surveys across thousands of hands-on technical-skill workshops and have reported swings from roughly a third to roughly two-thirds of respondents confident on the same task, pre-to-post. The precedent is life-sciences and data-science training rather than a developer conference, and it measures self-reported confidence, not observed task completion. Borrow the convention, not the figure.
- **Started-versus-finished** (self-set): how many participants reached the last exercise. A wide gap with a full room points at coverage; a wide gap with a small room points at prerequisites.
- **Help latency** (self-set): how long a raised hand waits. Set your own target, and note that it is the axis the facilitator menu's efficiency line deliberately does not rest on.
- **Post-session material use** (self-set): traffic to the published material inside the window you announced. It is also the honest test of the _no live hands-on_ rung - if the material carries the learning on its own, the room was optional.
- Sell-through of a separately ticketed workshop day belongs to `samber/dev-event-organizer-skills@event-format-selection`, not here.

## Invocation examples

- "We have a three-hour Kubernetes workshop for 40 people. How many helpers, and what do we ask attendees to install?"
- "Last year's workshop day fell apart because the venue WiFi died during the setup step. Fix it for this year."
- "Should we run this as hands-on, or just record the demo and publish the repo?"
- "Write the prerequisites section for our LLM workshop - the exercise needs a cloud console and a vendor account."

Expected output: a per-session delivery sheet carrying:

- the hands-on commitment, with the reason;
- the capacity number, and which of the three ceilings bound it;
- the facilitator coverage, with the basis of its sizing stated;
- the prerequisites, split into knowledge, machine state and accounts;
- the network posture, with what the venue answered;
- the materials, and the window they stay available;
- the trigger that would revise each choice next edition.

Present it section by section for validation, not as one block.

If your harness has persistent memory, record the capacity that bound and which ceiling bound it, the prerequisite sheet as shipped, what actually broke on the day, and the venue's written network answer. Next edition starts from that instead of re-deriving it.

## References

- [references/coverage-and-room-mechanics.md](references/coverage-and-room-mechanics.md) - the four coverage rungs written out, in-room and after-the-workshop mechanics with a negative example, the mentor-model contrast.
- [references/prerequisite-and-environment-sheet.md](references/prerequisite-and-environment-sheet.md) - the prerequisite artifact: three content classes, the provisioned-environment and both-paths rungs, materials and their access windows, the compliance review triggers, plus a filled example and a negative one.
- [references/capacity-length-and-network-evidence.md](references/capacity-length-and-network-evidence.md) - the three ceilings, the demand-vote room-assignment mechanic, published session lengths with their events, the density ratios with their caveats, and the named live-failure causes.

See also, same collection:

- `samber/dev-event-organizer-skills@event-format-selection` - decides whether a workshop day or track exists, its bracketing model and its ticketing; this skill takes all of that as given.
- `samber/dev-event-organizer-skills@event-schedule-design` - places the session in the grid and sizes the buffer around it; it consumes the capacity and length set here.
- `samber/dev-event-organizer-skills@event-talk-selection` - selects proposals across formats; a hands-on proposal should be judged on whether the instructor can run it at the capacity offered and whether the exercise scales, which are this skill's questions.
- `samber/dev-event-organizer-skills@event-venue-sourcing` - receives the workshop-specific room, power and network requirements produced here as a sourcing input.
- `samber/dev-event-organizer-skills@event-accessibility-inclusion` - sets the bar for accommodation and for participant data, including credentials issued to a room.
- `samber/dev-event-organizer-skills@event-volunteers` - recruits and briefs the people the facilitator menu asks for, and owns the logistics-versus-content line this skill depends on.
