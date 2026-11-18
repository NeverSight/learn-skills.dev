---
name: pr-opportunity-scanner
description: "Daily scan for free PR opportunities: community threads (Reddit/HN/Dev.to) asking for tool recommendations, fresh roundup articles where your product can be featured, and a weekly local conference/meetup scan. Runs as cron or on-demand. For sales pipeline signals, see signal-scanner. For brand mentions, see social-listening."
user-invocable: true
---

## Context

Read `MEMORY.md` for: product description, wedge, competitors, repos, target community/region.
Read `memory/pr-opportunities.json` for already-surfaced URLs (dedup).
Follow output preferences from USER.md. For chat platforms: keep under ~15 lines.

**Repos / assets to promote** (pull from MEMORY.md → list of public repos and key links).

**Product angles** (pull from MEMORY.md → top differentiators and use cases).

# PR Opportunity Scanner

Find places where your product can get free visibility — community discussions and fresh articles where the product naturally fits.

## Query Categories (2 daily + 1 weekly)

### 1. Community Discussions (highest ROI)

People actively asking for recommendations — a relevant reply drives real signups.

```bash
exa-search__web_search_advanced_exa \
  query="recommend [YOUR_CATEGORY] tool OR best [YOUR_CATEGORY] for [JTBD] OR [YOUR_CATEGORY] tool for [USE_CASE] OR looking for alternative to [INCUMBENT]" \
  numResults=10 \
  startPublishedDate="YYYY-MM-DD" \
  type=keyword
```

Target sites: Reddit (subreddits where your ICP hangs out), Hacker News, Dev.to, Lobsters, GitHub Discussions, your community's preferred forums.

**What makes a good opportunity:**
- Thread is < 48h old (stale threads = wasted effort)
- Has engagement (>5 comments or >10 upvotes)
- Question matches your product's wedge from MEMORY.md
- No existing mention of your product (check first!)

### 2. Fresh Roundup Articles

Authors publishing tool lists/comparisons — contact them or leave a comment.

```bash
exa-search__web_search_advanced_exa \
  query="best [YOUR_CATEGORY] tools 2026 OR top tools for [JOB_TO_BE_DONE] OR [YOUR_CATEGORY] comparison OR [YOUR_CATEGORY] roundup" \
  numResults=10 \
  startPublishedDate="YYYY-MM-DD"
```

**What makes a good opportunity:**
- Published in last 7 days
- Lists competitors ([COMPETITOR_A], [COMPETITOR_B], [COMPETITOR_C], [COMPETITOR_D]) but NOT your product
- Author has contact info or comments section
- Site has meaningful traffic (not a spam blog)

### 3. Local Conferences & Meetups (weekly, Mondays only)

Upcoming tech events in your target region — speaking slots, booths, networking, CFPs.

```bash
exa-search__web_search_advanced_exa \
  query="[YOUR_REGION] tech conference 2026 OR [YOUR_CITY] meetup OR [YOUR_REGION] AI conference OR developer conference [YOUR_REGION] OR startup conference [YOUR_REGION]" \
  numResults=10 \
  startPublishedDate="YYYY-MM-DD"
```

Add a localized-language query if useful (e.g. local-language search terms).

**What makes a good opportunity:**
- Event is 2+ weeks away (enough time to apply as speaker / prepare)
- Relevant audience matching ICP from MEMORY.md
- Has CFP open, or free/cheap booth, or networking format
- Not purely corporate/government if low ICP density

**Track a curated list of recurring local events** (maintain in MEMORY.md → `pr.events`).

**Action types:**
- CFP open → draft talk proposal (topic: your wedge angle)
- Networking event → note date, register
- Booth/sponsor opportunity → evaluate cost vs reach
- Meetup → offer to give a lightning talk

## Scan Workflow

### Daily Cron Mode

1. **Load state** — read `memory/pr-opportunities.json`
2. **Set dates** — `startPublishedDate` = 2 days ago (catch things missed yesterday)
3. **Run Query 1** (community discussions) — 1 Exa call
4. **Run Query 2** (roundup articles) — 1 Exa call
5. **If Monday → Run Query 3** (local conferences, 1-2 Exa calls, `startPublishedDate` = 7 days ago)
6. **Deduplicate** — skip URLs already in pr-opportunities.json
7. **Score & filter** each result:
   - RELEVANCE: Does your product genuinely fit? (skip if forced)
   - FRESHNESS: < 24h = high, 24-48h = medium, > 48h = low
   - ACTIONABILITY: Can the founder act in < 5 min? (comment vs write article)
   - For conferences: TIME_TO_EVENT (> 2 weeks = actionable, < 2 weeks = info only)
8. **Pick top 3** — best opportunities only (conferences = separate section)
9. **For each opportunity, draft the action:**
   - Discussion → draft a short, helpful reply (not salesy — value first, mention product naturally)
   - Article → draft a short outreach message to the author, or a comment
   - Conference → draft CFP abstract / registration note / lightning talk pitch
10. **Update state** — add surfaced URLs to pr-opportunities.json
11. **Report to chat** — or `HEARTBEAT_OK` if nothing worth reporting

### On-Demand Mode

When the user asks "find PR opportunities" or "where can we get visibility":
1. Run both queries with wider date range (14 days)
2. Present top 5-10 ranked results
3. Offer to draft replies/outreach for selected ones

## State File: memory/pr-opportunities.json

```json
{
  "last_scan": "2026-03-29T10:30:00Z",
  "surfaced": [
    {
      "url": "https://reddit.com/r/...",
      "found": "2026-03-29",
      "type": "discussion",
      "status": "surfaced|acted|skipped",
      "title": "..."
    }
  ]
}
```

Keep last 90 days. Prune older entries on each scan.

## Output Format (Chat)

When opportunities found:
```
PR Scan [date]:

1. [discussion/article] Title
   link
   Action: [draft reply / contact author]
   [2-line draft of what to say]

2. ...

Reply "go 1" to post, "skip" to dismiss.
```

Monday conference section (appended when Query 3 runs):
```
Local conferences:
1. [Event name] — [city], [date]
   [CFP open / registration / networking]
   Action: [submit talk / register / skip]
```

Nothing found:
```
HEARTBEAT_OK
```

## Reply Drafting Rules

- **Value first, product second.** Answer the question helpfully. Mention your product only if it genuinely solves the problem.
- **No marketing speak.** Write as a peer sharing a tool, not a vendor pitching.
- **Short.** 3-5 sentences for Reddit/HN. 2-3 sentences for comments on articles.
- **Include proof.** Link to repo, demo, or specific feature — not the landing page.
- **Disclose.** "Disclosure: I'm the founder" — Reddit/HN expect this.
- Run through `humanizer` mentally — no AI-sounding patterns.

## Cost

- 2 Exa queries/day + 1-2 extra on Mondays: ~$0.02-0.10
- Monthly: ~$1-3
- Negligible compared to signal-scanner

## Cron Setup (example)

```
Job ID: pr-scan-001
Schedule: 0 10 * * * (daily 10:00 in your timezone)
Session: isolated
Deliver: announce → [your chat channel]
Prompt: "Run pr-opportunity-scanner skill in daily cron mode. Today is {date}."
```

## Related Skills

- **signal-scanner** — buying signals for sales pipeline (different purpose)
- **social-listening** — brand/competitor mention monitoring (on-demand)
- **social-writer** — craft LinkedIn/X posts based on found opportunities
- **copywriting** — write longer submissions or guest post pitches
- **content-strategy** — plan content calendar around discovered topics
- **humanizer** — polish any drafted replies before posting
