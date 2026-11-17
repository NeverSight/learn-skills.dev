---
name: lead-intelligence
description: AI-native lead intelligence and outreach pipeline. Replaces Apollo, Clay, and ZoomInfo with agent-powered signal scoring, mutual ranking, warm path discovery, source-derived voice modeling, and channel-specific outreach across email, LinkedIn, and X. Use when the user wants to find, qualify, and reach high-value contacts.
origin: ECC
---

# Lead Intelligence

Agent-powered lead intelligence pipeline that finds, scores, and reaches high-value contacts through social graph analysis and warm path discovery.

## When to Activate

- User wants to find leads or prospects in a specific industry
- Building an outreach list for partnerships, sales, or fundraising
- Researching who to reach out to and the best path to reach them
- User says "find leads", "outreach list", "who should I reach out to", "warm intros"
- Needs to score or rank a list of contacts by relevance
- Wants to map mutual connections to find warm introduction paths

## Tool Requirements

### Required
- **Exa MCP** — Deep web search for people, companies, and signals (`web_search_exa`)
- **X API** — Follower/following graph, mutual analysis, recent activity (`X_BEARER_TOKEN`, `X_ACCESS_TOKEN`)

### Optional (enhance results)
- **LinkedIn** — Direct API if available, otherwise browser control for search, profile inspection, and drafting
- **Apollo/Clay API** — For enrichment cross-reference if user has access
- **GitHub MCP** — For developer-centric lead qualification
- **Apple Mail / Mail.app** — Draft cold or warm email without sending automatically
- **Browser control** — For LinkedIn and X when API coverage is missing or constrained

> Required and optional environment variables: see [reference/configuration.md](reference/configuration.md).

## Pipeline Overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│ 1. Signal   │────>│ 2. Mutual    │────>│ 3. Warm Path    │────>│ 4. Enrich    │────>│ 5. Outreach     │
│    Scoring  │     │    Ranking   │     │    Discovery    │     │              │     │    Draft        │
└─────────────┘     └──────────────┘     └─────────────────┘     └──────────────┘     └─────────────────┘
```

## Voice Before Outreach

Do not draft outbound from generic sales copy.

Before writing a message, build a voice profile from real source material. Prefer:

- recent X posts and threads
- published articles, memos, or launch notes
- prior outreach emails that actually worked
- docs, changelogs, or product writing if those are the strongest signals

If live X access is available, pull recent original posts before drafting. If not, use supplied examples or the best repo/site material available.

Extract:

- sentence length and rhythm
- how compressed or explanatory the writing is
- how parentheses are used
- whether capitalization is conventional or situational
- how often questions are used
- phrases or transitions the author never uses

For Affaan / ECC style specifically:

- direct, compressed, concrete
- strong preference for specifics, mechanisms, and receipts
- parentheticals are for qualification or over-clarification, not jokes
- lowercase is optional, not mandatory
- no fake curiosity hooks
- no "not X, just Y"
- no "no fluff"
- no LinkedIn thought-leader cadence
- no bait question at the end

## Stage 1: Signal Scoring

Search for high-signal people in target verticals. Assign a weight to each based on:

| Signal | Weight | Source |
|--------|--------|--------|
| Role/title alignment | 30% | Exa, LinkedIn |
| Industry match | 25% | Exa company search |
| Recent activity on topic | 20% | X API search, Exa |
| Follower count / influence | 10% | X API |
| Location proximity | 10% | Exa, LinkedIn |
| Engagement with your content | 5% | X API interactions |

### Signal Search Approach

```python
# Step 1: Define target parameters
target_verticals = ["prediction markets", "AI tooling", "developer tools"]
target_roles = ["founder", "CEO", "CTO", "VP Engineering", "investor", "partner"]
target_locations = ["San Francisco", "New York", "London", "remote"]

# Step 2: Exa deep search for people
for vertical in target_verticals:
    results = web_search_exa(
        query=f"{vertical} {role} founder CEO",
        category="company",
        numResults=20
    )
    # Score each result

# Step 3: X API search for active voices
x_search = search_recent_tweets(
    query="prediction markets OR AI tooling OR developer tools",
    max_results=100
)
# Extract and score unique authors
```

## Stage 2: Mutual Ranking (Summary)

For each scored target, analyze the user's social graph to find the warmest path. Rank mutuals primarily by number of connections to targets (40%), then role/company, location, industry alignment, and identifiability.

A weighted bridge-ranking model (`B(m)` → `B_ext(m)` → response-adjusted `R(m)`) produces three tiers: Tier 1 (direct bridge → warm intro asks), Tier 2 (one-hop bridge → conditional asks), Tier 3 (no bridge → cold outreach).

> Full weighting table, bridge-score formulas, tier interpretation, and the mutual-ranking report output format: see [reference/ranking-algorithm.md](reference/ranking-algorithm.md).

## Stage 3: Warm Path Discovery

For each target, find the shortest introduction chain:

```
You ──[follows]──> Mutual A ──[invested in]──> Target Company
You ──[follows]──> Mutual B ──[co-founded with]──> Target Person
You ──[met at]──> Event ──[also attended]──> Target Person
```

### Path Types (ordered by warmth)
1. **Direct mutual** — You both follow/know the same person
2. **Portfolio connection** — Mutual invested in or advises target's company
3. **Co-worker/alumni** — Mutual worked at same company or attended same school
4. **Event overlap** — Both attended same conference/program
5. **Content engagement** — Target engaged with mutual's content or vice versa

## Stage 4: Enrichment

For each qualified lead, pull:

- Full name, current title, company
- Company size, funding stage, recent news
- Recent X posts (last 30 days) — topics, tone, interests
- Mutual interests with user (shared follows, similar content)
- Recent company events (product launch, funding round, hiring)

### Enrichment Sources
- Exa: company data, news, blog posts
- X API: recent tweets, bio, followers
- GitHub: open source contributions (for developer-centric leads)
- LinkedIn (via browser-use): full profile, experience, education

## Stage 5: Outreach Draft (Summary)

Generate personalized outreach for each lead, matching the source-derived voice profile and the target channel. Channel priority: warm intro by email → direct email → LinkedIn DM → X DM/reply. Create drafts only; never send without explicit user approval.

> Full per-channel rules (email/LinkedIn/X), warm-intro vs cold-outreach templates, the execution pattern, and anti-patterns: see [reference/outreach-templates.md](reference/outreach-templates.md).

## Agents

This skill includes specialized agents in the `agents/` subdirectory:

- **signal-scorer** — Searches and ranks prospects by relevance signals
- **mutual-mapper** — Maps social graph connections and finds warm paths
- **enrichment-agent** — Pulls detailed profile and company data
- **outreach-drafter** — Generates personalized messages

## Example Usage

```
User: find me the top 20 people in prediction markets I should reach out to

Agent workflow:
1. signal-scorer searches Exa and X for prediction market leaders
2. mutual-mapper checks user's X graph for shared connections
3. enrichment-agent pulls company data and recent activity
4. outreach-drafter generates personalized messages for top ranked leads

Output: Ranked list with warm paths, voice profile summary, and channel-specific outreach drafts or drafts-in-app
```

## Reference Files

- [reference/ranking-algorithm.md](reference/ranking-algorithm.md) — Stage 2 full mutual-ranking: weighting table, weighted bridge-score formulas (`B`, `B_ext`, `R`), tier interpretation, and report output format.
- [reference/outreach-templates.md](reference/outreach-templates.md) — Stage 5 channel rules (email/LinkedIn/X), channel-selection heuristic, warm-intro and cold-outreach templates, execution pattern, and anti-patterns.
- [reference/configuration.md](reference/configuration.md) — required and optional environment variables.
