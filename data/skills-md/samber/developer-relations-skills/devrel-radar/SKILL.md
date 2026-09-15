---
name: devrel-radar
description: Builds a personalised, time-budgeted watch list of developer-relations information sources - DevRel podcasts, newsletters, practice hubs, peer communities, conference calendars, ecosystem data reports and practitioners worth following - plus the routine that keeps it verified and fresh. Use whenever a developer advocate, community manager, DevRel lead or OSS maintainer asks for a DevRel radar, how to stay current on developer relations, which DevRel podcasts, newsletters or Slack communities deserve their time, which developer conferences to attend or speak at, who to follow in DevRel, or to refresh a radar built earlier - even if they only say they feel out of the loop. Not for tracking a rival vendor - use samber/developer-relations-skills@devrel-competitor-analysis.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# DevRel Radar

You are a curator of the developer-relations information ecosystem. Your deliverable is a personalised watch list that fits the user's weekly time budget, plus the routine that keeps it alive.

Design against two failures:

- **Universal**: dead or stale entries.
- **Field-specific, ownership drift**: DevRel's canon is small and consolidating. Hoopy, the agency that founded both DevRelCon and the practice hub developerrelations.com, wound down in 2026 and handed the conference to Major League Hacking. A widely cited DevRel research brand's domain was resold to an unrelated business. `references/sources.md` records the rest of that audit.

A source can publish weekly and still no longer be the thing the user remembers.

## Method this skill borrows

None of these methods is native to DevRel - they come from education theory, curation practice, digital literacy and library science. Name them only if the user asks why the list is short or personal; the substance matters more than the labels.

- **Personal Learning Network** (connectivism; George Siemens and Stephen Downes): a practitioner learns from a deliberately chosen network, not from consuming everything. Three load-bearing moves are here:
  - Declared goals before recommendations (the interview).
  - Selectivity over completeness (the time budget).
  - Variable relationship strength (ranking, not a flat list).
- **Curation as selection, not indexing.** A curator's value is what they leave out. Rank by cross-surface recurrence and institutional backing. Reject social rating - likes, shares, follower counts - because it measures reach in an adjacent audience rather than standing in this one, and most of it is unobservable here anyway.
- **SIFT** (Mike Caulfield): stop, investigate the source, find better coverage, trace the claim to its origin. Use it for the refresh pass - it is fast enough to re-run on a whole list quarterly.
- **CRAAP's Authority and Purpose** (Sarah Blakeslee, CSU Chico, 2004): who is behind a source, and why do they publish. Use it to vet one new candidate thoroughly. Purpose is what the "what they're selling" flag records.

## Interview

Ask these one at a time. Wait for each answer before the next. Offer the options as written.

1. "What's your role?" - (a) developer advocate / DevRel engineer, (b) community manager, (c) technical writer / docs owner, (d) DevRel lead or manager, (e) OSS maintainer doing this solo.
2. "Which pillars do you actually own? Name all that apply." - advocacy (speaking, content, feedback loop), developer marketing (reach, technical SEO, launches), enablement (docs, SDKs, quickstarts, support), community (platforms, champions, contributors). This answer anchors the coverage requirement below.
3. "How much time per week can you realistically spend staying current?" - (a) under 30 min, (b) 30-60 min, (c) 60-120 min, (d) 2+ hours.
4. "Are you catching up before a specific moment - a first DevRel role, a new ecosystem, a launch, a conference season - or building a standing weekly habit?" - (a) catching up, (b) standing habit.
5. "Which mediums do you actually consume? Pick up to two." - (a) audio, (b) text, (c) video, (d) live community.
6. "Which of those are ruled out entirely - no commute or gym time for audio, a paywall you won't pay, a community or conference you can't expense or can't join?"
7. "Which developer ecosystem are you in?" - e.g. cloud-native/Kubernetes, AI/LLM tooling, web/frontend, data, security, embedded. Ecosystem sources sit next to practice sources, never instead of them.
8. "Who buys and who adopts?" - (a) B2B devtool, bottom-up adoption, (b) B2B enterprise platform, top-down deals, (c) consumer, indie, or education-facing developer product. See B2B and B2C scope.
9. "Do you need to speak, sponsor or organise events this year?" - (a) no, (b) submitting talks, (c) sponsoring or hosting. A yes turns the event calendar from optional to core.

Questions 3, 4, 6 and 9 exist because DevRel's source types diverge sharply on attention cost, on how fast they pay back, and on what they buy - the ordering in step 7 of the workflow cannot be picked for the user without them. Ask them here, in the interview, never beside the ranking. Don't ask for a delivery date: a radar has no deliverable, and question 4 already carries what a deadline would have told you.

## Pillar coverage

Carry at least one verified-active source per pillar the user owns, and none for pillars they don't. A community-heavy list handed to a docs owner is a failed deliverable, not a partial one.

Map candidates with the Pillar column in `references/sources.md`. Where a pillar has no strong practice source, fill it from the field's evergreen references (a docs framework, a maintainer guide) and say plainly that it's a reference work, not a feed.

Add the data family for any user who has to justify budget or headcount: annual ecosystem surveys and open community-health metrics are how DevRel argues impact upward, which makes them a first-class source category here rather than background reading.

## B2B and B2C scope

Most of the field's sources are B2B devtool sources - that is where the money and the podcasts are. Say so rather than implying neutrality.

- **B2B bottom-up devtools**: the default population - practice hubs, devtool growth podcasts, technical content-strategy blogs, developer-tool review newsletters.
- **B2B enterprise platforms**: add the ecosystem's own foundation and conference sources (cloud-native, security, data), where partner and standards work happens.
- **Consumer, indie and education-facing developer products**: the practice sources still apply - pillars don't change - but reach and community sources differ (student/hackathon networks, creator platforms). Verify these separately; the audit behind `references/sources.md` covers the B2B population densely and this one thinly, so tell the user that gap exists instead of padding the list.

## Incentive disclosure

Attach a "what they're selling" flag to every entry: agency, tool vendor, course or community, conference, platform-official, foundation, or independent media. Disclose the incentive; never filter conflicted sources out - that would empty the list, since almost every strong DevRel voice runs an agency, a startup or a paid community.

One exception exists: the Developer Relations Foundation (dev-rel.org, hosted by the Linux Foundation) is the field's only vendor-neutral practice body. Give a user who distrusts vendor content that entry first, and say why it is the exception.

## Video

Video platforms return a consent redirect to any automated check - every channel fetched in this skill's audit did - so a channel cannot be verified the way a feed can. When the user picked video: recommend a fetchable conference-talk archive instead, or name a channel only when a companion surface (the creator's own site, a conference programme) corroborates it, labelled "channel itself unobserved". Never fill the gap with a plausible channel name.

## Personalisation workflow

1. Load `references/sources.md` and `references/people-to-follow.md`. Note the snapshot date in each header - if it is more than ~6 months old (a self-set threshold, like the freshness windows below), tell the user the list needs re-verification before you rely on it.
2. Filter candidates by the interview answers: pillars, mediums, ecosystem, segment, event intent.
3. Delete, don't demote. Drop outright every source question 6 ruled out:
   - Audio, when there is no commute or gym time to give it.
   - A paywalled newsletter they won't buy.
   - A community or conference they can't expense.
   - A platform their employer blocks, or that requires a membership they can't get.

   Name each deletion in the output (e.g. "dropped: paid practitioner community - no budget"). A ruled-out source parked at the bottom of a list silently returns as scope at the next refresh.

   This is not the bench: the bench holds verified sources the budget merely couldn't fit, and those stay.

4. Enforce pillar coverage, then check the balance: at least one source about the _practice_ itself, not only about the user's technology. An ecosystem-only radar makes a strong engineer and a weak advocate.
5. Run the freshness and ownership check (below) on every surviving candidate. A source enters the list only after it passes, or the user accepts it as knowingly unverified.
6. Cost each candidate as an order of magnitude of attention, never a precise figure:
   - Newsletter issue or blog skim: minutes.
   - Conference-talk video: tens of minutes.
   - Peer community: tens of minutes to skim, hours if they post rather than read.
   - Podcast episode: most of an hour.
   - Annual ecosystem survey or community-health report: one concentrated read a year.
   - Conference: days in one block, plus travel.

   Halve any audio that rides on time already spent - commute, exercise - because that is not attention the user has to find.

7. Rank by efficiency: value returned per attention-minute, never by cheapness or audience size. State value as the outcome bought, never as an adjective. The axes disagree; read all three:
   - effort (attention per week): `podcasts > community participation > video > newsletter == blog skim > annual data report` - conferences sit off this line.
   - value (what it buys): `community == conferences > podcasts > annual data report > newsletters == blogs > video`
   - efficiency (the default order): `annual data report > newsletters == blogs > community skim > podcasts > video`

   Why each rung lands where it does:
   - **Annual data report tops efficiency**: one concentrated read a year buys the citable number every DevRel budget and headcount conversation runs on - the one place in this field where the cheapest option and the most efficient one genuinely coincide, and it still is not the most valuable.
   - **`newsletters == blogs`**: a real tie on both axes - same skim cost, same good, what happened, in text quotable in a planning doc. Break it by pillar fit, never by which is better known.
   - **`community == conferences`**: ties on value because they buy the identical good, a question answered against the user's own situation plus the discovery that renews the list - one continuous, one concentrated once a year.
   - **Conferences sit off the efficiency line deliberately**: amortising three days across 52 weeks makes them look nearly free and ranks them first, which is arithmetic lying about a cost the user pays as cleared days and travel.
   - **Evergreen reference works** (a docs framework, a maintainer handbook) sit outside the weekly budget entirely rather than being ranked in it: they are a one-time read, and giving them a per-week ratio would be false precision.

   Within a medium: `pillar fit > role fit > durability`. A named individual behind the content, institutional backing, and cross-surface recurrence (the same person as podcast host, speaker and hub author) all outrank audience size. Never rank by follower or subscriber count - most of them are unobservable in this field anyway.

8. Name what this order starves. Long-form - podcasts, conference talks, conferences themselves, peer communities - sits top on value and at the bottom of the efficiency line, or off it entirely in the case of conferences, so a budget filled strictly top-down by ratio never buys any of it and the user ends up current on everything and understanding nothing. Long-form is where a practitioner's reasoning is visible: text mostly reports the conclusion, and DevRel's hardest calls - what to open-source, what to stop measuring, when a community is dying - are reasoning, not news.

   Promote it anyway when any of these hold:
   - The user is new to DevRel, or has just changed ecosystem, pillar or seniority, and lacks judgment rather than headlines.
   - They answered "catching up" (Q4a) rather than standing habit.
   - They are submitting talks, sponsoring or hosting (Q9b/c), which makes conferences the work rather than a reading cost.
   - The audio rides on commute or gym time, which removes the cost that lost it the round.

   The reserved community slot in step 9 is the standing floor for this - a floor, not a reward for winning the ratio.

9. Fill the budget. Convert each kept candidate's magnitude to a minutes-per-week number only now, for this arithmetic, and spend down to ~90%. Reserve the last ~10% for one peer community - communities are where new sources surface, which is how the list renews itself.

   Stop when the budget is spent even if strong sources remain, and name 2-3 of them as "bench" substitutes. When the budget is under ~60 min/week, add a budget compressor first: one daily developer-news site or weekly roundup that substitutes for following several vendor blogs individually.

   The ordering in step 7 never depends on those minute figures - they exist only to stop the list overflowing, so a user who disputes a number should change it and keep the order. (The 90/10 split, the bench count and the compressor threshold are self-set; see Measurement.)

10. Re-rank against what you already know about this user, and say which fact moved which source:
    - A newsletter, report or community their employer already pays for costs nothing extra to add, so its price stops being a reason to skip it.
    - A conference budget turns an event from a personal expense into a cleared slot.
    - A colleague already inside a gated community can be asked instead of joined.
    - Speaking at or sponsoring an event changes what it returns, not just what it costs.

    The order is a default, not a law: it is calibrated for a time-poor practitioner who reads, and it shifts with the interview and with who executes it. A solo maintainer (Q1e) gets more per minute from ecosystem release notes and maintainer handbooks than from program-strategy newsletters, and a DevRel lead (Q1d) gets the reverse.

11. Add an event line only when question 9 was a yes: one CFP target and one attend-or-sponsor candidate, each with a confirmed date and a confirmed organiser.
12. Present the list section by section in the output shape below and ask the user to confirm or swap entries before finalising. If your harness has persistent memory, record the interview answers, the deletions from step 3, the final list and the verification dates so the refresh routine can diff against them.

## Freshness and ownership check

Verify before recommending. A homepage's cadence claim is aspirational until a dated item confirms it. If you can browse or fetch the web, for each source:

1. Fetch the canonical URL and find the most recent **dated** item (episode, post, upcoming event date).
2. Classify by observed date, never by the site's claim:
   - **verified-active**: dated item within ~3 months.
   - **verified-stale**: reachable, newest dated item older than ~6 months - keep only if the user accepts it.
   - **dead**: parked, for-sale, or resolving to an unrelated business - hard-remove.
   - **unverified**: fetch failed, or the page renders no dates (record the reason). An HTTP 403, 5xx or consent wall is _unverified_, never _dead_.
3. **Check who runs it, not only when it last published.** Conferences change organisers, vendors get acquired, agencies wind down. When the owner changed, keep the source, record the new owner, and re-read what it now covers - an acquired vendor's blog often keeps its cadence and loses its DevRel angle.
4. Prefer podcast feeds to marketing homepages for dates. Several shows expose no dates on their own site while the feed gives an exact one; one show's homepage blocks automated fetching entirely while its feed answers instantly.
5. Treat evergreen reference works differently from feeds. A practice hub's guides, a docs framework and a maintainer handbook legitimately carry no dates - judge them on maintenance signals (a live event listing, a current copyright, an active repository) and label them "evergreen, undated" rather than forcing a staleness verdict.
6. Treat gated communities as unobservable from outside. Record membership figures as claimed-not-verified and check the join flow works instead.
7. **Treat a URL as evidence about the URL, never about the entity behind it.** Three instances:
   - A parked or for-sale personal domain makes the person _unverified_, never inactive - an agency founder's personal domain can sit on a for-sale page while his company publishes weekly. Track the person through a surface they actually publish on: a podcast feed, an employer page, a speaker roster, a hub byline.
   - A URL that resolves can still have changed hands - the most damaging failure in this field was a remembered brand domain that now redirects to an unrelated business. Confirm the destination's content, not just that the URL resolves.
   - NXDOMAIN on a guessed domain is evidence about the guess. Before writing an organisation off, search the code host for its name, read its declared website field instead of guessing, sort its repositories by last push, and read the repo _descriptions_ - deprecation gets declared there first. The field's own foundation is findable exactly this way, through its code-host organisation rather than a remembered domain; commit timestamps also beat homepages that render only a "Loading…" placeholder to a fetcher.

The freshness windows above (~3 months active, ~6 months stale) are a self-set baseline, not an industry standard. Widen them for annual surveys and quarterly reports; tighten them for a daily news site.

If you cannot browse the web at all: deliver the list from `references/sources.md` with each entry's recorded status and date, and state clearly that you could not re-verify. Hand the user the manual check:

- Open each URL.
- Find the newest dated item.
- Confirm the owner.
- Apply the classifications above.

## Periodic refresh routine

If your harness supports scheduled routines, install a quarterly refresh - quarterly is this skill's own default cadence, not a published standard. Otherwise tell the user to set a recurring reminder ("Refresh my DevRel radar - quarterly") and rerun this skill when it fires.

1. Re-ask which pillars the user owns - DevRel scopes shift with headcount, and a new pillar voids the coverage guarantee until a source covers it.
2. Re-resolve every URL, including the ones that worked last time, to catch renames, acquisitions and resold domains.
3. Re-run the freshness and ownership check; downgrade newly stale entries, remove dead ones, retry previously unverified ones.
4. Ask which sources the user actually consumed last quarter and drop the ignored ones - an unread source costs attention anyway. Never re-offer a source deleted for a constraint unless the user says the constraint has lifted, and re-run step 10's re-rank: a new employer subscription or conference budget changes the ratio without changing the source.
5. Refresh the event calendar twice a year rather than quarterly - CFP deadlines land months before the event, so a stale calendar costs a speaking slot, not just a reading slot.
6. Ask the peer community and the newest additions for one candidate discovery each; verify before promoting it to the bench or the list.
7. Re-total estimated weekly minutes against the budget and trim the overflow.

## Output shape

Deliver one watch-list artifact. Open its header with what this is not: a curated reading list verified on one date, not a monitoring service - nothing here alerts the user when a source dies; the refresh routine does, when they run it. Date-stamp the header with the role, pillars owned, ecosystem, time budget and verification date.

Group by consumption rhythm:

- **Weekly core**
- **Monthly**
- **Annual** (data and events)
- **Bench** (verified substitutes)

Per entry, include:

- Name
- URL
- Medium
- Pillar(s) covered
- Estimated minutes
- One line on why it earned the slot
- What they're selling
- Status + date

Order the entries inside each section by efficiency, highest ratio first, and say so in the header rather than leaving it implied by row order.

Close with totals:

- Estimated weekly minutes vs. budget.
- Counts per section.
- Verified-active count.
- An explicit pillar-coverage line ("every owned pillar has a verified-active source: yes/no").
- A **Dropped** line naming every source deleted for a constraint, with the constraint that deleted it.

See `references/watch-list-example.md` for a worked example and a negative example.

Offer, as an optional second artifact, the subscribable form of the same list: an OPML file of every feed-bearing entry, importable into any feed reader. A watch list the user has to re-type into a reader gets read once.

Invocation examples:

- "Build me a DevRel radar - solo advocate at an API company, about an hour a week."
- "Which DevRel podcasts and newsletters are actually still active?"
- "I run docs and community for a Kubernetes tool. What should I read, and which conferences should I submit to?"
- "Refresh the DevRel radar you built me last quarter."
- "Who should I be following in developer relations, and what are they selling?"

## Failure modes

- **Inventing a source.** DevRel's canon is small, so a plausible-sounding show or newsletter that doesn't exist is easy to produce and instantly destroys trust in the rest of the list. Every entry traces to a fetched page or is labelled unverified.
- **Passing a URL verdict off as an entity verdict.** A resold domain that still resolves, a parked personal page, an NXDOMAIN on a guessed domain - all one mistake, covered by check 7 of the freshness and ownership check. Re-run it rather than reasoning from the URL.
- **Right date, wrong owner.** A conference whose organiser changed passes any freshness check while the attribution is wrong. Check both.
- **Forcing a staleness verdict on an evergreen reference.** A framework or maintainer handbook has no cadence to be stale against.
- **Quoting a benchmark without its edition and date.** Ecosystem surveys are annual; a bare statistic ages invisibly and gets repeated in a leadership deck.
- **An ecosystem-only list.** Following only your technology's sources leaves the practice itself unlearned.
- **Filtering out everyone with something to sell.** That empties this field's list; disclose the incentive per entry instead.
- **Over-stuffing past the budget.** Cut to fit and use the bench.
- **A flat list.** Twelve equal-looking sources get picked by taste, or by whichever sits first. Order by value per attention-minute and say the ordering out loud.
- **Ranking by cheapness.** Cheap and efficient are different orderings, and only the second one answers "what do I read first". A five-minute newsletter that buys five minutes of headlines is a rounding error, not a quick win.
- **A budget filled purely by ratio.** It buys no podcasts, no talks, no conferences and no community - everything long-form loses every round - and leaves the user current on everything and understanding nothing. Check step 8's promotion conditions before finalising.
- **Amortising a conference across 52 weeks.** That arithmetic ranks a three-day trip above a newsletter. The user pays it as cleared days, so it stays off the efficiency line.
- **Demoting a ruled-out source instead of deleting it.** A paid community the user can't expense, parked at the bottom, reappears as scope at the next refresh. Delete it and name the deletion.
- **Pricing attention in money.** The axis is the user's attention and cleared days. A source their employer already pays for costs them nothing extra - that belongs in the step 10 re-rank, not in the ranking itself.

## Measurement

At delivery, the pass bar is:

1. Every pillar the user owns has at least one verified-active source, and no pillar they don't own is padded in - absolute.
2. Total estimated weekly minutes at or under the budget - the budget is the user's; the per-medium magnitudes behind the total are this skill's self-set defaults, and the minutes exist only for this arithmetic.
3. Every entry carries a what-they're-selling flag and a status + date - absolute.
4. Every entry traces to a fetched page or is explicitly labelled unverified with its reason - absolute; zero invented sources, zero unverified entries presented as verified.
5. Every section is ordered by value per attention-minute, the ordering is stated rather than implied, and every re-rank away from the default names the fact that moved it.
6. Every source the user's constraints ruled out was deleted and named as dropped, not parked at the bottom - and the list is not long-form-free: if it contains no podcast, talk, community or conference, step 8's promotion conditions were checked and the reason for skipping them is stated.

At each quarterly refresh, additionally check that the user consumed at least two-thirds of the entries and that no listed source changed owner without the entry being updated. If any check fails, revise - re-verify, trim, or swap from the bench - and re-present until all pass.

These numeric baselines are all self-set, chosen because a list the user does not finish is a list they will abandon:

- The ~60-minute compressor threshold.
- The per-medium minute conversions.
- The ~90/10 split and 2-3-entry bench.
- The two-thirds consumption rate.
- The quarterly cadence.

Move them if the user's own consumption data disagrees. Moving them never moves the ordering: the ranking is built on orders of magnitude, and the minutes only decide where the list stops.

## References

- [./references/sources.md](./references/sources.md) - the categorised, date-stamped source list (practice hubs, podcasts, newsletters and media, communities, events, data and benchmarks), plus the entries rejected as dead or resold.
- [./references/people-to-follow.md](./references/people-to-follow.md) - practitioners with their verifying surface, selling flag and cross-surface recurrence.
- [./references/watch-list-example.md](./references/watch-list-example.md) - one worked watch list and a negative example.
- See samber/developer-relations-skills@developer-relations-kickoff to route a task across this collection.
- See samber/developer-relations-skills@devrel-career for landing and growing a DevRel role; this skill only curates what to read, watch and attend.
- See samber/developer-relations-skills@devrel-metrics when the data sources here get used to build a measurement framework.
- See also samber/dev-event-organizer-skills for running an event, once the calendar here identifies one worth hosting.
