---
name: event-social-media
description: Run a technical event's own social presence inside the weight, phase and dates the marketing plan already fixed - platform selection, the campaign versus community hashtag, posts mapped onto campaign phases (announcement, CFP, speaker reveal, final push, live), speaker and sponsor amplification asks, and day-of coverage. Use whenever the user mentions event social media, a conference or hackathon content calendar, speaker-announcement posts, which platforms an event should post on, an event hashtag, or briefing a volunteer on live posting - even if they never say "social media". Do NOT use for channel weight and budget - use samber/dev-event-organizer-skills@event-marketing-plan; mining talk recordings afterwards is samber/dev-event-organizer-skills@event-content-repurposing.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Social Media

You run the social channel of a technical event's acquisition campaign: which platforms the event posts on, which hashtag carries which purpose, what gets posted at each campaign phase, who else is asked to amplify, and what happens on the day.

Three things arrive already decided. Do not re-derive them, and do not argue against them:

- **The weight, the phase and the dates** - `samber/dev-event-organizer-skills@event-marketing-plan` owns the channel mix, the campaign calendar spine and the per-phase targets. It hands you a weight, a set of dates and a target. Your job starts there.
- **The message** - `samber/dev-event-organizer-skills@event-positioning` supplies the promise, the audience definition and the anti-positioning sentence ("There are many [archetype] events. This is not one of them."). Social copy carries that sentence; it never invents a new angle or names a rival.
- **The voice** - `samber/dev-event-organizer-skills@event-cultural-identity` treats social as one touchpoint column in its tone-modulation matrix, alongside the MC script, signage and swag. Read the register off that matrix. A social voice invented separately is the single most common identity failure that skill exists to catch.

**Own social is deliberately weighted low by the umbrella, and that is not an oversight to correct.** The marketing plan ranks own social presence below the mailing list, local engagement and partner channels on value. DevOpsDays' own organizing guide notes that "with the dispersal of tech communities from Twitter, a lot of community events are struggling to reach people".

Your job is to run that discounted baseline well, not to relitigate its weight. If the interview surfaces a genuinely social-native audience, say so and route the reweighting back to the plan rather than absorbing the decision here.

One boundary to state out loud at the start of any engagement: **turning talk recordings into clips, threads and articles after the event is `samber/dev-event-organizer-skills@event-content-repurposing`'s job**, not yours. You own pre-event and live-during posting. The post-event archive-mining pipeline sits directly on your border and is the easiest scope to absorb by accident.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 5-7 exist because the menus below diverge sharply on time-to-effect, durability and effort - the default ordering cannot be picked for the user without them.

1. What did the marketing plan hand down for social: its weight in the mix, the fixed dates, the per-phase targets? If nothing was handed down, stop and route to `samber/dev-event-organizer-skills@event-marketing-plan` first - a content calendar with no campaign spine under it has nothing to hit.
2. Does this event deliberately opt out of promotion? Some do, and it is a real strategy, not a gap (see the opt-out below).
3. Where does this audience actually gather - name real properties, not the platforms you would name by default. A dispersed enterprise-infrastructure crowd, a single-campus student crowd and a design crowd share almost no platform.
4. What does the event already own: accounts and their real reach, a prior edition's photo archive, an existing house hashtag, a decentralized brand's shared tag?
5. What is the doors date, and how much runway is there before it? A short runway promotes the asks that use someone else's existing audience over anything that has to build one.
6. One edition's push, or an account meant to compound across editions? Be honest with the user here: an event account starts nearly cold each cycle unless the event persists, which is why creator-economy follower-growth advice does not transfer. A one-off push demotes every rung whose payback lands in a later edition - a second natively adapted account, an archive-building live rung; a compounding mandate promotes both.
7. Who actually writes and posts, for how many hours a week - and is that same person running the event on the day? This one answer decides the live-coverage rung more than any other.
8. Which governance pole does the event sit on: community-run, foundation-run, or company/vendor-run? It decides whether a neutrality policy constrains what the account may share.
9. What photo opt-out do the badges carry, and what do the speaker agreements say about recording and quoting? Collect this before planning any live coverage, not on the morning of.
10. Does any sponsor agreement contract live coverage, and is there a remote audience the live posts serve?
11. Does sponsor onboarding already collect a social handle to thank?

## Community-run, foundation-run, vendor-run

The axis that genuinely changes this skill's output is who owns the event, because it decides what the account is _allowed_ to post:

- **Community-run** - no neutrality policy to enforce, no brand review, whoever holds the password posts. The constraint is volunteer hours, not permission.
- **Foundation-run** - a written neutrality policy is likely, and it is restrictive. CNCF's own guidelines:
  - Allow only "vendor-neutral, community-sourced" content.
  - Forbid sharing anything promoting a vendor product or pointing at a company website.
  - Replace case-by-case judgment with an explicit retweet allow-list.

  **This exists to enforce foundation neutrality and does not transpose downward**: a vendor-run event has no symmetric reason to avoid promoting its own product, and a small community event has no sponsor-neutrality policy to enforce at all. Import it only at this pole.

- **Company/vendor-run** - expect brand review, a marketer who owns the account, and paid amplification the other two poles cannot reach. Community and foundation guidance does not speak to this pole, so treat any rule borrowed from it as untested here.

## The opt-out: some events should not run a content calendar

Strange Loop's published guiding principles began, literally, with **"No marketing"** (thestrangeloop.com/about) - a long-running, heavily oversubscribed community-pole conference that deliberately declined active promotion as part of its identity. That is a real counter-example, not an execution gap.

Check three conditions before building any calendar. When they hold, recommend the minimal presence - a single announcement, the practical details, and nothing else - and say plainly that this is the identity-consistent choice rather than a shortfall:

- Positioning is built on scarcity, curation or word-of-mouth (`samber/dev-event-organizer-skills@event-positioning`'s category strategy will say so).
- Demand already exceeds capacity without promotion, or a prior edition sold out on announcement alone.
- The organizers experience promotion as off-brand, and the cultural identity's register supports them.

An event that opts out still needs the practical posts - dates, location, link, CFP close, doors - because the people already looking for it have to find them. "No marketing" is not "no information".

## Workflow

1. Run the interview. Fix the weight, dates and targets from Q1 before anything else.
2. Test the opt-out conditions (Q2 with the positioning read). If they hold, ship the minimal presence and stop here.
3. Restate the message and the anti-positioning sentence from `samber/dev-event-organizer-skills@event-positioning`, and read the social column of the tone matrix from `samber/dev-event-organizer-skills@event-cultural-identity`. Every post below inherits both.
4. Pick the platform set with the breadth menu. Platform names are examples throughout - the mix shifts every couple of years, and the audience answer from Q3 outranks any list.
5. Decide the hashtags by purpose, not by habit. Full taxonomy and the community-signalling contrast: [references/platform-fit-and-hashtags.md](references/platform-fit-and-hashtags.md).
6. Map posts onto the plan's phases - announcement, CFP open and close, speaker reveals, agenda release, early-bird close, final push, live, wrap. Post types per phase, plus a worked calendar and its negative counterpart: [references/phase-post-plan-and-amplification-kit.md](references/phase-post-plan-and-amplification-kit.md).
7. Build the amplification asks with the posture menu, and produce the shareable kit once rather than per request.
8. Choose the live-coverage rung, then write the named volunteer and the photo rules into the run of show - not into a document nobody opens on the day. Route the operational slot to `samber/dev-event-organizer-skills@event-run-of-show`.
9. Hand the recordings, the photo archive and the quotable moments to `samber/dev-event-organizer-skills@event-content-repurposing`. Say what you are handing over; do not start cutting clips.
10. Feed the per-platform tracked links back to the marketing plan's referral-signal measurement. That measurement layer is the plan's, not yours - you supply the links, it reads them.

If your harness has persistent memory, record the platform set with the audience answer that justified it, the hashtag decisions and their purposes, which asks were made of whom, and what actually got posted with what response. Next edition starts from a real archive and a real list of people who amplified, instead of a blank calendar.

Every ranking below is a default, not a law - it shifts with context and with who executes it. Re-rank all three menus against what you already know about this organizer: an organizer with a large personal following, a volunteer who edits video for a living, a decentralized brand with a shared community tag, a photo-hostile code of conduct, an audience concentrated on one campus. Each of those overturns a default rung, and each menu below says which.

## Platform set breadth

Ranked menu: reach bought per unit of organizer effort. The orderings below are judged, not measured.

- effort (writing, adaptation, account upkeep): `full presence > two natively adapted > home plus mirror > single home platform`
- value (people reached who were not already coming, judged): `two natively adapted > full presence > home plus mirror > single home platform`
- efficiency: `home plus mirror > single home platform > two natively adapted > full presence`

Value puts a well-run two-platform presence above a full spread on purpose. Marginal platforms reach heavily overlapping audiences, and at a volunteer effort budget they degrade into visibly unattended accounts - an account whose last post is four months old subtracts credibility from the event rather than adding reach.

- **Single home platform** - one account, where Q3 says the audience actually is. Everything else is a link on the comms hub the marketing plan already builds.
- **Home plus mirror** - the same posts cross-posted to a second platform with light adaptation. Cheap because nothing is rewritten.
- **Two natively adapted** - each post rewritten to its platform's format and audience. This is where the hours go.
- **Full presence** - four or more accounts, each maintained. MLH's campus-scale strategy names six platforms plus community groups: a real list, for an audience genuinely dispersed across them.

- **Default rung:** home plus mirror.
- **Promotion condition:** move to two natively adapted when Q3 names two platforms holding _different_ audiences with different reasons to attend - for example a professional network reaching the managers who approve travel budgets, and a community platform reaching the practitioners who actually want the talks. Adapting for two flavors of the same audience buys nothing.

**The starved option is full presence** - second on value, first on effort, so efficiency never picks it. Promote it in two cases: a company-run event where maintaining the accounts is already somebody's job, and a campus-scale hackathon whose audience genuinely lives across the platform spread MLH documents, where no single home platform reaches even half of them.

When Q3 names one platform and one only, **delete the other rungs rather than demoting them**. A second account created "just in case" and then abandoned is worse than never opening it, and a rung parked at the bottom of a menu reappears as scope in week three.

## Amplification-ask posture

Ranked menu - borrowed reach per unit of coordination effort. The ordering is judgment.

- effort (coordination, other people's calendars, per-item production): `coordinated partner push > per-speaker ask > sponsor thank-you == ready-made kit`
- value (reach through an audience that already trusts the poster, judged): `per-speaker ask > coordinated partner push > ready-made kit > sponsor thank-you`
- efficiency: `per-speaker ask > ready-made kit > sponsor thank-you > coordinated partner push`
- compliance cost (review triggered, reversibility spent): `sponsor thank-you == coordinated partner push > per-speaker ask`; the ready-made kit carries none.

- **Effort tie** (sponsor thank-you == ready-made kit): both are one-off content production with nobody else's calendar in the loop. The kit is built once; the thank-you is minutes per sponsor against a handle already sitting in the onboarding checklist.
- **Compliance-cost tie** (sponsor thank-you == coordinated partner push): both are governed by an already-signed agreement whose brand-usage and deliverable clauses decide what may be published. Both cost a check with the sibling that owns that agreement _before_ posting - a public post cannot be un-published after the fact.
- **Per-speaker ask position:** below both ties and above the kit's zero, because it does need one permission - the speaker's consent to being named and pictured. The speaker agreement normally grants it already, and the ask carries an explicit opt-out on top.

- **Ready-made kit** - speaker cards, a copy block, the hashtag, the link, image sizes. Built once, used by every other ask. Give the templates going to speakers, jurors and coaches a personal discount-code slot their own post can carry - it turns "please share this" into something their own network gets value from, distinct from the plain sponsor template, which carries no such incentive.
- **Per-speaker ask** - at confirmation, send the speaker their card plus one line asking them to post it and telling them the date the event's own post goes out. It rides on an email already being sent, which is why it is this cheap. At scale, decentralize delivery rather than routing every kit through one social owner: whoever internally manages a given speaker, sponsor or coach relationship hands that person their own kit, so amplification scales with the number of internal stakeholder-owners rather than bottlenecking on one person's queue.
- **Sponsor thank-you** - DevOpsDays' organizing guide collects, alongside logo and invoice details, "a Twitter handle for you to thank (very optional)". Its own framing is the point: goodwill, not a deliverable. Present it that way.
- **Coordinated partner push** - partner communities, media partners and ambassador programs posting on a dated moment. The deal itself belongs to `samber/dev-event-organizer-skills@event-media-partnerships` and `samber/dev-event-organizer-skills@cross-event-promotion`; you supply the date and the assets.

- **Default rung:** the ready-made kit plus the per-speaker ask.
- **Promotion condition, keyed to Q11:** add the sponsor thank-you the moment sponsor onboarding already collects a handle - it costs minutes. Add the coordinated push only once the marketing plan has weighted partner channels for that phase and the deal already exists.

**The starved option is the coordinated partner push** - second on value, first on effort. Promote it when the partnership deal is already signed (the marginal effort is then only date coordination, not negotiation), and for a first edition with no audience of its own, where borrowed audiences are the only audiences available.

For an event with no sponsors, **delete the sponsor rung** rather than leaving it as an aspiration on the menu. Same for the partner push when no partnership exists and none is being pursued this cycle.

A note on posting _before_ asking: check whether the sponsor agreement already contracts a social mention. If it does, the post is a fulfilment item owned by `samber/dev-event-organizer-skills@event-sponsor-fulfillment` and missing it is a breach, not a missed courtesy.

## Live-coverage depth

Ranked menu - evidence and in-room amplification bought per unit of effort on a day when everyone is already busy.

- effort (people, attention, on-the-day capacity): `full live desk > roving poster > scheduled skeleton > single recap`
- value (reach plus the archive next edition and next year's sponsors need, judged): `full live desk > roving poster > single recap > scheduled skeleton`
- efficiency: `single recap > roving poster > full live desk > scheduled skeleton`
- compliance cost (consent obtained, reversibility spent): `full live desk > roving poster == single recap`; the scheduled skeleton carries none.

The compliance tie is argued: the roving poster and the recap both publish images of identifiable attendees, so both need the same consent mechanism in place beforehand - the badge-carried photo opt-out owned by `samber/dev-event-organizer-skills@event-accessibility-inclusion`. They differ in volume, not in the permission required. The full desk adds live-quoting speakers and often streaming, which needs recording consent the speaker agreement may or may not already grant.

The skeleton ranks last on efficiency despite costing little, and that is deliberate: pre-written "doors are open" posts produce no artifact and reach mostly people already standing in the room. Its work goes into looking active rather than into anything reusable.

- **Single recap** - one post after doors close, carrying the day's real photos and a thank-you. Half an hour, and it produces something next edition can reuse. A deliberately minimal post-event plan stops at this plus one longer recap video across the archive's channels - resist growing it into a sprawling multi-week recap campaign the team cannot sustain against next edition's own workload.
- **Scheduled skeleton** - three to five posts written and scheduled in advance. Ships reliably with nobody's attention on the day, which is its whole and only merit.
- **Roving poster** - one named volunteer posting photos and quotes through the day. The archive this produces is what feeds the sponsor report, next edition's promotion, and `samber/dev-event-organizer-skills@event-content-repurposing`.
- **Full live desk** - several people, per-talk posts, a live thread, a photo pipeline, replies in real time.

- **Default rung:** the single recap.
- **Promotion condition:** move to the roving poster as soon as a volunteer can be _named in the run of show_ - not hoped for on the morning. An unnamed live-posting duty is the one that silently does not happen.

**The starved option is the full live desk** - first on value, first on effort, so efficiency never picks it. **Promotion condition, keyed to Q10**: a sponsor agreement actually contracts live coverage, or the event has a remote audience for whom the live posts _are_ the event.

For an event whose code of conduct or cultural identity restricts photography - a strict photo policy, an off-the-record norm, a badge-based opt-out that most attendees use - **delete the photo-based rungs** instead of demoting them. Plan text-only coverage or none, and say why, so nobody quietly reintroduces a camera on the day.

## Failure modes

- **Arguing against the umbrella's channel weight.** Opening a social plan by making the case that social should lead contradicts a decision `samber/dev-event-organizer-skills@event-marketing-plan` already made, and wastes the engagement on a fight the plan already settled. Run the discounted baseline well; route a genuine reweighting case back to the plan.
- **Importing a creator-economy benchmark.** "Post 3-5 times a week on a professional network, 3-10 times a day on a microblog" is continuous personal-brand cadence, measured on accounts that compound followers over years. An event campaign is short, dated and checkpoint-driven, starts near-cold each edition, and the mismatch is structural, not a matter of tone.
- **Treating a community hashtag as a campaign tag.** DevOpsDays tells prospective organizers to post "(Use the #devopsdays hashtag.)" - that is a standing community-identity tag letting a decentralized network find each other, not a per-edition measurement tag. Riding a community tag without also having your own campaign tag loses the measurement purpose entirely.
- **Redefining positioning in a post.** A new angle invented for a caption creates a second, competing story about what the event is. Carry the positioning sentence; do not improve it.
- **Doing the repurposing sibling's job.** Cutting talk clips, writing recap articles and building an evergreen distribution plan after the event belongs to `samber/dev-event-organizer-skills@event-content-repurposing`. Hand over the archive and stop.
- **Presenting the sponsor thank-you as obligatory.** Its own source calls it "very optional". Sold as a duty, it turns a goodwill gesture into an unfunded deliverable - and if the agreement genuinely contracts a mention, that is a fulfilment item, not this.
- **Importing a foundation's neutrality policy into a community or vendor event.** CNCF's rules exist to enforce foundation neutrality:
  - Applied to a small community event, they forbid perfectly normal posts for no reason.
  - Applied to a vendor-run event, they forbid the thing the event exists to do.
- **Letting the same person post live and run the day.** The organizer on duty cannot answer a venue problem and cover a keynote at once. Name a different person or drop to the recap rung.
- **Inventing a cadence number to sound precise.** Anchor posts to campaign dates that actually exist instead - a date is defensible, a frequency is not.

## Measurement

This skill sets **no numeric pass threshold**, and that refusal is deliberate. A target like "4% engagement" would be false precision imported from an unrelated domain; the reader would optimize against a number that means nothing here. Judge the channel on whether the dated posts shipped and whether the tracked links moved, not on a rate.

One real event-account figure exists and is worth naming precisely so it is not mistaken for a target: a 2025 academic study of 22 named computer-science conference accounts on X (arXiv:2503.01038) measured a median of 9 likes and 3 reposts per post, with follower counts from 206 to 74,115 and a strong correlation (Pearson 0.95) between follower count and likes. Those accounts are established conference brands that accumulated followers across up to 14 recurring editions - a continuously compounding audience, not a campaign starting near-cold each edition - so the figures describe that audience, not a threshold to import here.

- **Every dated post in the plan shipped on its date** (self-set, binary): the only measure fully inside your control, and the one that fails most often on volunteer teams.
- **Per-platform tracked link** (self-set): a distinct link per platform, decided before launch because it cannot be added retroactively. The marketing plan owns reading these; you own creating them.
- **Amplification take-up** (self-set): how many speakers and partners actually posted, out of those asked. A low rate diagnoses the ask, not the audience - usually an ask that arrived without a ready-made asset attached.
- **The archive produced** (self-set, and the one that pays next edition): photos, quotes and recordings usable by `samber/dev-event-organizer-skills@event-content-repurposing` and by next edition's promotion. A day covered by nobody produces nothing to promote with next year.

## Invocation examples

- "We're four months out from our 300-person infra conference. What should we be posting, and where?"
- "Our first speakers just confirmed - how do we announce them and get them to share it?"
- "Should our hackathon be on TikTok, or is that a waste of time for a student audience?"
- "What do we post during the event itself? Nobody has a spare pair of hands that day."
- "Our conference has always run on word of mouth and the organizers hate marketing. Do we even need a social plan?"

Expected output, with every judged or self-set element labeled as such:

- The platform set, with the audience answer that justified it.
- The hashtag decisions, with each one's purpose.
- A phase-mapped post plan pinned to the marketing plan's actual dates.
- The amplification asks, with who gets asked when and the kit they receive.
- A live-coverage rung, with a named person and the photo rules.
- The handover list for `samber/dev-event-organizer-skills@event-content-repurposing`.

## References

- [references/platform-fit-and-hashtags.md](references/platform-fit-and-hashtags.md) - the platform-fit table by campaign phase, the three-purpose hashtag taxonomy against the community-signalling contrast, the neutrality-policy scope flag, and the who-posts-versus-who-requests workflow for a team account.
- [references/phase-post-plan-and-amplification-kit.md](references/phase-post-plan-and-amplification-kit.md) - a worked phase-mapped post plan with its negative counterpart, the speaker and sponsor ask templates, the shareable kit contents, and the live-coverage briefing checklist.

See also, same collection:

- `samber/dev-event-organizer-skills@event-marketing-plan` - the umbrella: owns the channel weight, campaign spine, budget and per-phase targets this skill executes within.
- `samber/dev-event-organizer-skills@event-positioning` - supplies the message and the contrast-not-attack sentence every post carries.
- `samber/dev-event-organizer-skills@event-cultural-identity` - supplies the register; social is one touchpoint column in its tone-modulation matrix.
- `samber/dev-event-organizer-skills@event-run-of-show` - where the live-posting slot and its named volunteer belong on the day.
- `samber/dev-event-organizer-skills@event-content-repurposing` - takes the recordings and photo archive after the event; owns clips, articles and evergreen distribution.
- `samber/dev-event-organizer-skills@event-accessibility-inclusion` - owns the badge-carried photo and recording opt-out every live-coverage rung depends on.
