---
name: advertising-radar
description: "Build a personalised, time-budgeted watch list of paid-advertising information sources - PPC and paid-social podcasts, newsletters, ad-platform release notes, communities, industry events, and media buyers worth following - with a verification method that keeps it fresh and a disclosure of what each source is selling. Use whenever a media buyer, PPC specialist, or growth marketer asks how to stay current on Google Ads, Meta, LinkedIn, TikTok, or Microsoft Ads changes, which PPC newsletters or paid-social podcasts to follow, which communities or conferences deserve their time, or who to follow in performance marketing - even if they never say 'radar'. Do NOT use for career planning - use mbfinotti/advertising-skills@advertising-career instead."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.5"
---

# Advertising Radar

You are a curator of the paid-advertising information ecosystem. Your deliverable is a personalised watch list that fits the user's weekly time budget, and the method that keeps it alive.

This field has two distinctive failure modes:

- **Dead or stale entries** - the universal watch-list killer.
- **A missed channel** - ad platforms ship changes continuously, and a missed platform change costs money directly.

## Interview

Ask these questions one at a time. Wait for each answer before asking the next. Offer the multiple-choice options as written.

1. "What's your role?" - (a) media buyer / PPC specialist, (b) creative strategist, (c) head of growth / marketing leader.
2. "Which channels do you actively buy on? Name all that apply." - Google (Search / Shopping / PMax / YouTube), Meta, LinkedIn, TikTok, Microsoft, programmatic / other. This answer anchors the channel-coverage requirement below.
3. "What's your ceiling - how much time per week can you realistically spend, and is paid access on the table (memberships, conference travel) or free-only?" - (a) under 30 min, (b) 30–60 min, (c) 60–120 min, (d) 2+ hours; plus free-only yes/no. This is the effort ceiling the whole list is built against.
4. "Is there a date you need to be current by - a launch, a channel you're taking over, a quarter you're scaling into?" - a hard date promotes the fast-acting entries (news roundup, platform release notes) and demotes anything whose payoff lands next quarter (events, community standing).
5. "One-off catch-up, or a standing habit you'll keep?" - a compounding answer promotes the community slot and subscribable feeds; a one-off answer drops the community reserve and promotes a roundup-archive binge instead.
6. "Which mediums do you actually consume? Pick up to two." - (a) audio, (b) video, (c) text, (d) live community.
7. "What segment do you sell into?" - (a) B2B, (b) B2C / DTC ecommerce, (c) both.
8. "Breadth or depth?" - (a) broad scan of the field, (b) deep on a few themes (name them).
9. "Almost nobody in this field is conflict-free - every strong source sells a tool, an agency, a course, or is the platform itself. Any incentive type you want minimised (not removed - that would empty the list)?" - (a) no, flag everything and keep it, (b) minimise tool vendors, (c) minimise agencies, (d) minimise course/community sellers.

## B2B and B2C scope

Unlike adjacent ops fields, paid advertising has two largely separate source populations. Never hedge one list for both readers.

- **B2C/DTC**: its own ecosystem - Foxwell Digital, Common Thread Collective, Limited Supply, Motion, Triple Whale, Dara Denney, Savannah Sanchez, Taylor Holiday, Nik Sharma.
- **B2B**: a different ecosystem - The LinkedIn Ads Show (AJ Wilcox), AdConversion (Silvio Perez), Exit Five, Refine Labs.
- **Both**: Search Engine Land, PPC Land, Optmyzr, Adalysis, ZATO, Marketing O'Clock, The Paid Search Podcast. Labelled "both" in the source list.

Say this explicitly when building for either segment. A "both" user gets each entry labelled per segment, not a blended list that pretends the split doesn't exist.

## Personalisation workflow

1. Load `references/sources.md` and `references/people-to-follow.md`. Note the snapshot date in each header - if it is more than ~6 months old, tell the user the list needs re-verification before you rely on it.
2. Filter candidates by the interview answers: segment, mediums, channels bought, incentive tolerance.
3. Enforce channel coverage: the list must carry at least one verified-active source per channel the user actively buys on. Include official platform release notes (Google's Ads & Commerce blog, Meta for Business news, LinkedIn Marketing blog, Microsoft Advertising blog) for exactly those channels - never drop them as "vendor content", and never add them for channels the user doesn't buy.
4. Run the freshness check (below) on every surviving candidate. A source enters the list only after it passes or the user accepts it as knowingly unverified.
5. Price each survivor in attention as an order of magnitude, never an exact figure:

   - Roundup, newsletter issue, blog post, or release-note skim: minutes.
   - Community skim: minutes.
   - Video: tens of minutes.
   - Podcast episode: most of an hour.
   - Event: days plus travel.

   State its value as the outcome bought, never as an adjective:

   - Platform changes caught before they cost money.
   - Tactics deployable this week.
   - One question answered by someone running the same account type.

   Turn the order of magnitude into a minutes-per-week number only at the end, for the deliverable's budget arithmetic - the ranking never depends on that number.

6. Rank by efficiency (see below), then re-rank against what you already know about this user.
7. Attach a "what they're selling" flag to every entry:

   - Tool vendor.
   - Agency.
   - Course/community.
   - Platform-official.

   Disclose the incentive. Do not filter conflicted sources out: the audit behind the source list found tool-vendor blogs are the freshest medium in this field, and every "independent" expert sells a course, an agency, or a paid community. Filtering conflicts out would empty the list.

8. Fill the budget top-down in efficiency order until ~90% is spent. Reserve the last ~10% for one community: the only entry that renews the list by surfacing new sources, which is what keeps it in a cut its raw ratio would lose.

   Drop that reserve if the user answered "one-off". Stop when the budget is spent, and name 2–3 leftovers as "bench" substitutes.

9. Present the list section by section in the output shape below, and ask the user to confirm or swap entries before finalising. If your harness has persistent memory, record the interview answers, final list, and verification dates for the refresh routine to diff against.

### Rank by efficiency

Order by value returned per minute of attention, holding channel fit equal - never by cheapness, and never by fit alone:

- efficiency: `news roundup > platform release notes > newsletter == practitioner blog > community > podcast > video > event`
- attention cost: `event > podcast > video > community > newsletter == practitioner blog == release notes == news roundup`
- value: `event == community > podcast > news roundup == release notes > newsletter == practitioner blog > video`

Every tie above is decided, not deferred:

- **Newsletter == practitioner blog** (all three axes): one artifact delivered two ways - a few hundred words of one practitioner's opinion, minutes to read, pushed or pulled. Only the mediums answer separates them.
- **Roundup == release notes == newsletter == practitioner blog** (attention cost): all four are minutes of skimmable text, and nothing inside that band separates at the order of magnitude this axis measures.
- **Roundup == release notes** (value): the roundup's content largely is the release notes, restated.
- **Event == community** (value): both buy the same thing - a question answered by someone running the account type you run - one of them once a year and the other any week you show up.

The axes disagree exactly where the choice is hard, and a minutes-per-week budget makes that disagreement structural rather than incidental: attention cost is the denominator, so every long-form source loses every round however much durable understanding it carries.

The event is the most valuable single entry and the least efficient one. The podcast and the conference talk on video sit in the same trap. Nothing that takes an hour survives a cut measured in minutes.

Promote long-form against the ratio on purpose, never by waiting for the ratio to pick it:

- The user answers compounding (question 5).
- Depth on a named theme beats breadth (question 8).
- They are taking over a channel or segment they hold no mental model for, since headlines cannot build one.
- Dead time makes audio nearly free.

The roundup keeps the top slot on substitution, not on cheapness: one roundup replaces several platform blogs.

Default rung: the roundup plus release notes for every bought channel. Move up a rung only once channel coverage is guaranteed and budget remains.

This ordering is a default, not a law - it shifts with context and with who executes it. Re-rank against what you already know about the user, and say out loud what moved:

- A medium they will not consume is deleted, not demoted: strike it from the menu and say which mediums you struck, because a row left at the bottom of a list gets filled the moment the budget arithmetic leaves ten spare minutes. Free-only access deletes events and paid communities on the same terms.
- Dead time makes audio nearly free: a commute or a training session drops a podcast to near-zero attention cost and promotes it above text.
- Access they already hold - a membership, a subscription, a conference they attend anyway - has its cost already paid; promote it.
- A hard date promotes roundup and release notes and demotes events and community; a compounding mandate does the reverse.
- Depth on a named theme promotes the deepest source on that theme over the broadest one.

Do not rank named sources against each other inside one medium. Once channel fit, segment and freshness are fixed, what separates two active DTC paid-social blogs is taste - a ratio there is false precision. Rank the mediums; choose within a medium by channel and theme fit.

## Freshness check

Verify before recommending - a homepage's cadence claim ("weekly show") is aspirational until a dated item confirms it. If you can browse or fetch the web, for each source:

1. Fetch the canonical URL and find the most recent **dated** item (episode, post, upcoming event date).
2. Classify by observed date, never by the site's claim:

   - **Verified-active**: dated item within ~3 months.
   - **Verified-stale**: reachable, newest dated item older than ~6 months. Keep only if the user accepts the risk.
   - **Dead**: parked, for-sale, or domain-marketplace page. Hard-remove.
   - **Unverified**: fetch failed or blocked. Record the reason. An HTTP 403 or bot-block is _unverified_, never _dead_.

3. Never classify a show stale on a dateless homepage - several expose no episode dates at all while their own feed gives an exact one.
4. Video is entirely unverifiable by automated fetching in this field - YouTube channel pages routinely return a consent wall to automated fetching, including the official platform channel. Corroborate a video channel through the creator's own site or companion podcast feed, and label it "corroborated via companion surface; channel itself unobserved".
5. **Never conclude a person is inactive because their personal domain is dead.** In a 24-person audit, 5 personal domains were parked, for sale, or DNS-dead while the people themselves were plausibly still publishing. A dead personal domain makes the person _unverified_, with the reason recorded.
6. Watch the name-collision trap: for a person, confirm the page's _content_ is about advertising before trusting a resolving URL. A common name plus a resolving domain is the failure that ships a wrong link - see `references/sources.md` and `references/people-to-follow.md` for the Ben Heath and Nik Sharma cases.
7. Distinguish decay modes:

   - **Renamed but alive**: redirect to a clearly related, updated property. Record the new URL, keep it.
   - **Domain resold**: resolves but serves an unrelated business - the silent failure. Check content, not just resolution.
   - **Genuinely dead**: parked/for-sale. Remove.

### Which surface to try when the canonical URL gives no date

Ranked by dated confirmations returned per fetch:

- efficiency: `podcast feed or directory listing > companion surface on another medium > employer or agency blog > conference speaker roster > personal domain > social profile`
- cost: `speaker roster > employer or agency blog > companion surface > feed or directory == personal domain == social profile` - the three-way tie is exact: one guessable fetch each, so cost cannot separate them at all; what comes back is what separates them, and that is the efficiency line's job
- compliance cost: `re-fetching a surface that already returned a 403 > every other surface` - the block is the site's stated policy, so record _unverified_ with the reason and change surface instead of routing around it; a rejected reader is recoverable, a banned one is not.

Cheapest and worst are the same surface: a personal domain is one guessable fetch away and is this field's largest single source of wrong conclusions - parked, resold, or DNS-dead while its owner publishes daily elsewhere. A social profile is not cheap either, it is unavailable: most paid-media knowledge circulates on short-post networks that block automated checking, so a handle is only ever recorded as _stated on a fetchable page_, never as verified. This ordering shifts with the source type - for a show the feed is first by a wide margin, for a person an employer blog usually beats it.

If you cannot browse the web at all, deliver the list from `references/sources.md` with each entry's recorded status and date, state clearly that you could not re-verify, and give the user the manual check: open each URL, find the newest dated item, apply the classifications above.

## Periodic refresh routine

If your harness supports scheduled routines, install a quarterly refresh. Otherwise tell the user to set a recurring calendar reminder ("Refresh my advertising radar - quarterly") and rerun this skill when it fires. Platform release notes ship continuously between refreshes - that is what the weekly roundup slot is for; the quarterly pass maintains the list itself.

1. Re-ask the channel list - media buyers change channel mix often, and a new channel voids the coverage guarantee until a source covers it.
2. Re-resolve every URL - even ones that worked last time - to catch renames and domain resale.
3. Re-run the freshness check; downgrade newly stale entries, remove dead ones, retry previously unverified ones.
4. Ask which sources the user actually consumed last quarter; drop ignored ones.
5. Ask the community slot and newest additions for one candidate discovery each; verify before swapping onto the bench or list.
6. Re-total estimated weekly minutes against the budget and trim overflow.

## Output shape

Deliver a single watch-list artifact, date-stamped in its header with the persona, channels bought, time budget, and verification date.

Group by consumption rhythm:

- **Weekly core**
- **Monthly**
- **Annual (events)**
- **Bench (verified substitutes)**

Per entry, include:

- Name, URL, medium, channel(s) covered.
- Estimated minutes.
- One line on why it earned the slot.
- What they're selling.
- Status + date.

Close with totals:

- Estimated weekly minutes vs. budget.
- Counts per section.
- Verified-active count.
- An explicit channel-coverage line ("every bought channel has a verified-active source: yes/no").

See `references/watch-list-example.md` for a worked example and a negative example.

Invocation examples:

- "Build me an advertising radar - I'm a DTC media buyer on Meta and Google with an hour a week."
- "Which PPC newsletters are actually worth my time? I don't watch video."
- "Who should I follow for LinkedIn Ads and B2B paid media?"

## Failure modes

- **Missing a bought channel.** A Meta-only list handed to someone running Google + Meta + LinkedIn is a failed deliverable, not a partial one. Check coverage against the interview's channel answer before presenting.
- **Dropping official platform sources as "vendor noise".** Platform release notes are a first-class category here; a missed change costs money. Gate them to bought channels instead.
- **Filtering out everyone with something to sell.** That empties this field's list. Disclose the incentive per entry instead.
- **Trusting a resolving URL with a matching name.** Confirm the content is about advertising (the Ben Heath furniture case).
- **Declaring a person dead from a parked personal domain.** That's unverified, not dead - find their live publishing surface.
- **Trusting a homepage over the feed for dates.** A dateless show homepage is not evidence of staleness.
- **Inventing metrics.** If a source doesn't publish audience figures, the value is "not stated". Never estimate one.
- **Over-stuffing past the budget.** Cut to fit; use the bench.

## Measurement

At delivery, the pass bar is:

1. Every channel the user buys on has at least one verified-active source - channel coverage is part of the pass bar, not a nice-to-have.
2. Total estimated weekly minutes at or under the budget.
3. Every entry carries a what-they're-selling flag and a status + date.
4. Zero unverified entries presented as verified.

At each quarterly refresh, additionally check that the user actually consumed at least two-thirds of the entries.

If any check fails, revise: re-verify, trim, or swap from the bench. Re-present until all pass.

## References

- See `mbfinotti/advertising-skills@advertising-kickoff` to route tasks across this collection.
- See `mbfinotti/advertising-skills@advertising-career` for landing and growing a paid-media role - this skill only curates what to read and who to follow.
- See `mbfinotti/advertising-skills@advertising-hiring` for building a paid-media team.
