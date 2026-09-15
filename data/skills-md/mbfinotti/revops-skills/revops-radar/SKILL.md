---
name: revops-radar
description: Build a personalised, time-budgeted watch list of RevOps / Sales Ops information sources - revops podcasts, revops newsletters, revops communities, industry events, and revops people to follow - every source verified still active, with a periodic refresh routine that keeps the list fresh. Use whenever the user mentions a revops radar, staying current in revenue operations, which revops newsletters or podcasts to subscribe to, which revops communities or conferences deserve their time, or who to follow in the field - even if they never say "radar". Tool-agnostic; B2B-SaaS-centric with explicit B2C guidance. Do NOT use for sales-specific sources - use mbfinotti/sales-skills@sales-radar instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.1.4"
---

# RevOps Radar

You are a curator of the RevOps / Sales Ops information ecosystem. Lead with a short, ranked, verified-link watch list that fits the user's actual weekly time budget - never a bare name with no way to click through, and never a source you haven't checked is still alive.

## Start here

Roughly twenty verified sources, one line each, grouped by medium. Every entry below has a live, checked link at the snapshot date (2026-09-08). This is a representative top slice, not the deliverable itself - always run the Interview and Personalisation workflow below before handing anything to a user, and pull the rest of the inventory from the full snapshot.

**People to follow**

- **Justin Norris** - linkedin.com/in/justinnorris/ - host of RevOps FM, practitioner-level GTM/RevOps operating practice.
- **Kyle Poyar** - linkedin.com/in/kyle-poyar/ - Growth Unhinged; pricing, packaging, GTM benchmark data.
- **Rosalyn Santa Elena** - linkedin.com/in/rosalyn-santa-elena/ - founder, The RevOps Collective; the strongest cross-surface signal in this field.

**Podcasts**

- **RevOpsAF** - revopscoop.com/podcast - RevOps Co-op's flagship show, confirmed active with a Sept 2026 episode.
- **GTM Podcast** - gtmnow.com/podcast - Sam Jacobs; long-running GTM/RevOps operator interviews.
- **Salesforce Admins Podcast** - admin.salesforce.com/podcast - official Salesforce show, weekly, confirmed active.

**Newsletters & blogs**

- **Growth Unhinged** - growthunhinged.com - Kyle Poyar; pricing, PLG, GTM benchmark data.
- **GTMnow** - gtmnow.com - GTM operator tactics and career content.
- **RevOps Impact Newsletter** - substack.com/@revopsimpact - Jeff Ignacio (AWS); weekly RevOps + AI tactics from a named practitioner.

**Books**

- **Revenue Operations** - Stephen G. Diorio & Chris K. Hummel - the closest thing this field has to a foundational textbook.
- **From Impossible to Inevitable** - Aaron Ross & Jason Lemkin - foundational text on predictable pipeline generation.
- **Revenue Architecture** - Jacco van der Kooij - source for the Bowtie and SPICED frameworks.

**YouTube**

- **Salesforce Admins (official)** - youtube.com/@SalesforceAdmins - 135K subscribers, very active.
- **RevOps Co-op** - youtube.com/@revopscoop - video versions of RevOpsAF podcast episodes.
- **Winning by Design** - youtube.com/@WinningByDesign - revenue-architecture framework content.

**Communities**

- **RevOps Co-op** - revopscoop.com - the hub: Slack + podcast + conference, 19,000 members.
- **Pavilion** - joinpavilion.com - GTM-leader peer community with a dedicated RevOps-leader group, 5,000+ executives.
- **r/RevOps** - reddit.com/r/RevOps - confirmed active, free.

**Conferences**

- **GTM2026** (Pavilion) - attendgtm.com - Sept 28-Oct 1, 2026, NYC, ~1,000 VP+ operators.
- **Dreamforce** - salesforce.com/dreamforce/ - Sept 15-17, 2026, San Francisco.
- **MOPs-Apalooza** - mopsapalooza.com - Oct 21-22, 2026, virtual.

## Full source snapshot

The list above is a slice. Read [references/sources.md](references/sources.md) before building any watch list - the full dated inventory across podcasts, newsletters, communities, events, and certifications, with status labels and the corrections found in the 2026-09-08 pass (a rename, an ended show, a misattributed podcast, two URL fixes). [references/people-to-follow.md](references/people-to-follow.md), [references/books.md](references/books.md), and [references/video-channels.md](references/video-channels.md) hold the fuller roster per medium; [references/curation-method.md](references/curation-method.md) holds the ranking arithmetic this file compresses below.

## Interview

Ask these questions one at a time. Wait for each answer before asking the next. Offer the multiple-choice options as written.

1. "What's your role in the revenue org?" - (a) IC / analyst, (b) manager, (c) leader (director+).
2. "How much time per week can you realistically spend staying current?" - (a) under 30 min, (b) 30-60 min, (c) 60-120 min, (d) 2+ hours.
3. "Are you catching up before a specific moment - a new role, a planning cycle, a stack migration - or building a standing weekly habit?" - (a) catching up, (b) standing habit.
4. "Which mediums do you actually consume? Pick up to two." - (a) audio (podcasts), (b) video, (c) text (newsletters, blogs), (d) live community (chat, events).
5. "Which of those are ruled out entirely - no commute or gym time for audio, a paywall you won't pay, a paid community or conference you can't expense?"
6. "Breadth or depth?" - (a) broad scan of the whole field, (b) deep on a few themes (name them).
7. "What segment do you operate in?" - (a) B2B SaaS, (b) B2C / ecommerce, (c) both.
8. "Include vendor-run sources (tool-company blogs, research reports)?" - (a) yes, clearly flagged, (b) no, independent voices only.
9. "Is your revenue stack anchored on one dominant CRM platform with its own admin community and certification track - and should those platform-ecosystem sources be included?" - (a) yes, include them, (b) no.

Questions 2, 3, and 5 exist because the source types diverge sharply on effort, on how fast they pay back, and on what they buy - the ordering in step 6 cannot be picked for the user without them. Don't ask for a delivery date: a radar has no deliverable, and question 3 already carries what a deadline would have told you.

## B2B and B2C scope

The RevOps information ecosystem is overwhelmingly B2B-SaaS-centric; no dedicated B2C/DTC "RevOps" branch exists. Say this explicitly to a B2C or ecommerce user - do not imply parity.

For segment (b) or (c): keep the medium-agnostic frameworks (funnel math, forecasting, data hygiene) from B2B sources, but route community and benchmark needs to ecommerce operator communities instead (one verified analogue is in the source list). Warn that most named benchmarks and playbooks assume B2B sales cycles.

## Personalisation workflow

1. Load `references/sources.md` and `references/people-to-follow.md`. Note the snapshot date in each header - if it is more than ~6 months old, tell the user the list needs re-verification before you rely on it.
2. Filter candidates by the interview answers:
   - segment
   - mediums
   - seniority fit
   - vendor-run preference
   - platform-ecosystem preference
3. Delete, don't demote. Drop outright every source the user's constraints rule out:
   - audio, when they have no commute or exercise time to give it
   - a paid community or conference they can't expense
   - a paywall they won't buy
   - a platform they can't join

   Name each deletion in the output ("dropped: Pavilion - paid, no budget"). A ruled-out source parked at the bottom of a list silently returns as scope at the next refresh. This is not the bench: the bench holds verified sources the budget merely couldn't fit, and those stay.

4. Run the freshness check (below) on every surviving candidate. A source enters the list only after it passes or the user accepts it as knowingly unverified.
5. Cost each candidate as an order of magnitude of attention, never a precise figure - text in minutes, video in tens of minutes, a podcast episode most of an hour, a community tens of minutes to skim, an event days in one block. Halve any audio that rides on time already spent (commute, exercise).
6. Rank by efficiency - value per attention-minute, never by cheapness or audience size: `newsletters == blogs > community skim > podcasts > video` by efficiency, `community == events > podcasts > newsletters == blogs > video` by value. Within a medium, rank by role fit first, then durability (a named accountable author, institutional backing, cross-surface recurrence) - never by subscriber count. Full axis reasoning and why the ties are real: [references/curation-method.md](references/curation-method.md).
7. Name what this order starves: long-form (podcasts, talks, events, communities) tops value but sits at or off the bottom of the efficiency line, so a budget filled strictly top-down never buys it. Promote it anyway for a user new to the field, choosing depth on named themes, catching up before a specific moment, or riding commute/gym time that already paid the attention cost.
8. Fill the budget to ~90%, reserving the last ~10% for one community since communities are how the list renews itself; name 2-3 strong leftovers as "bench" rather than dropping them. Full numeric arithmetic: [references/curation-method.md](references/curation-method.md).
9. Re-rank against what you already know about this user - an already-paid source or membership costs nothing extra, an employer conference budget turns an event free, a colleague inside a community can be asked instead of joined. This ordering is a default, not a law.
10. Concentrate versus spread, by the interview's breadth answer:
    - **depth** users: concentrate the budget on 3–5 sources plus the people who publish on their named themes
    - **breadth** users: spread across mediums with one anchor hub community
11. Present the list in the output shape below, section by section, and ask the user to confirm or swap entries before finalising.
12. If your harness has persistent memory, record the interview answers, final list, and verification dates so the refresh routine can diff against them.

## Freshness check

Verify before recommending - a homepage's own cadence claim ("weekly show") is aspirational until a dated item confirms it. Well-regarded sources advertising "weekly" have gone 7+ months silent while the tagline stayed up (RevOps FM and The Revenue Formula are both confirmed examples in sources.md).

If you can browse or fetch the web, fetch each source's canonical URL, find the most recent dated item, and classify by that observed date, never the site's own claim: `verified-active` (within ~3 months), `verified-stale` (reachable but older, keep only if the user accepts the risk), `dead` (redirects to a parking/marketplace page - hard-remove), or `unverified` (fetch failed or blocked - record the reason; a 403 or bot-block is unverified, never dead). Distinguish renamed-but-alive, domain-resold, and genuinely-dead rather than collapsing them into one verdict, and catch not-yet-alive sources (a live "coming soon" page with nothing published) separately. Full decay-mode taxonomy and named examples: [references/curation-method.md](references/curation-method.md).

Video platforms, discussion forums, and short-post social networks systematically resist automated checking - mark them unverified with the reason and fall back to manual verification, or verify a person via a fetchable surface instead (a podcast guest list, speaker roster, team page) and label any handle as stated-there, not independently confirmed.

If you cannot browse the web at all: deliver the list from `references/sources.md` with each entry's recorded status, state clearly that you could not re-verify, and give the user the manual check.

## Periodic refresh routine

If your harness supports scheduled routines, install a quarterly refresh. Otherwise tell the user to set a recurring calendar reminder ("Refresh my revops radar - quarterly") and rerun this skill when it fires.

Each refresh:

1. Re-resolve every URL - even ones that worked last time - to catch renames and domain resale.
2. Re-run the freshness check; downgrade newly stale entries, remove dead ones, retry previously unverified and not-yet-alive ones.
3. Ask which sources the user actually consumed last quarter; drop ignored ones - an unread source costs attention anyway. Never re-offer a source deleted for a constraint unless the user says the constraint has lifted.
4. Ask the anchor community / newest additions for one candidate discovery each; verify and consider swapping onto the bench or list.
5. Re-total estimated weekly minutes against the budget and trim overflow.

## Output shape

Deliver a single watch-list artifact, date-stamped in its header with the persona, time budget, and verification date.

Group entries by consumption rhythm, not medium:

- **Weekly core**
- **Monthly**
- **Annual (events)**
- **Bench (verified substitutes)**
- **Dropped (ruled out, with the reason)**

Per entry, include:

- name
- URL
- medium
- estimated minutes
- one line on why it earned its slot
- verification status and date
- a vendor-run flag where it applies

Close with totals:

- estimated weekly minutes vs. budget
- counts per section
- how many entries are verified-active

See `references/watch-list-example.md` for a full worked example and a negative example.

Invocation examples:

- "Build me a revops radar - I'm a sales ops manager with about an hour a week."
- "Which revops newsletters are worth my time? I don't do podcasts."
- "Who should I follow in revenue operations - independent voices only?"

## Failure modes

- **Recommending a dead or dormant source.** Always verify before recommending; never serve the reference list unchecked as if it were live.
- **Trusting a remembered URL.** Domains get resold; a resolving link can now point at an unrelated business. Re-resolve and confirm content matches.
- **Inventing metrics.** If a source doesn't publish subscriber/download/member counts, the value is "not stated". Never estimate one.
- **Over-stuffing past the budget.** Forty great sources for a 60-minute budget is a failed deliverable. Cut to fit; use the bench.
- **Mistaking audience size for authority.** A big subscriber count measures marketing reach. Cross-surface recurrence and a named accountable author predict quality and durability better.
- **Collapsing decay modes.** Marking a renamed-but-alive source dead loses a good source; marking a 403 dead loses a good source; keeping a resold domain is worse than either.
- **Constructing a plausible-looking URL from memory** instead of pulling one from the snapshot or stating the source lacks a verified link.

## Measurement

The watch list is working when, at each quarterly refresh, all of these hold:

- every listed source was verified-active within the last 90 days, or explicitly user-accepted as stale/unverified
- total estimated weekly minutes are at or under the stated budget
- the user reports actually consuming at least two-thirds of the entries

If any check fails, revise - re-verify, trim, or swap from the bench - and re-present until all three pass. At delivery time the pass bar is stricter: zero unverified entries presented as verified, and the budget respected exactly.

## References

- `references/sources.md` - the categorised, date-stamped source list (podcasts, newsletters and blogs, communities, events, certifications).
- `references/people-to-follow.md` - practitioners worth following, with confirmed LinkedIn URLs, independence flags, and the cross-surface-recurrence signal.
- `references/books.md` - the foundational and practitioner book list.
- `references/video-channels.md` - every verified YouTube channel with subscriber counts.
- `references/curation-method.md` - the full ranking arithmetic and freshness-check decay-mode taxonomy.
- `references/watch-list-example.md` - one worked watch list plus a negative example.
- See `mbfinotti/revops-skills@revops-kickoff` to route tasks across this collection.
- See `mbfinotti/revops-skills@revops-career` for landing and growing a RevOps role - this skill only curates what to read and who to follow; career strategy lives there.
- See `mbfinotti/revops-skills@revops-hiring` for building a RevOps team.
