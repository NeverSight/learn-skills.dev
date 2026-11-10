---
name: benchmarking-instagram-influencer-engagement
description: >
  Benchmarks and compares Instagram influencer engagement rates using apidojo's Instagram scraper on Apify.
  Triggers when the user asks to: compare engagement rates of Instagram accounts, check if an influencer
  has real or fake followers, analyze Instagram account performance metrics, benchmark a creator against
  competitors on Instagram, find Instagram accounts with unusually high or low engagement, verify
  influencer stats before a paid partnership, or audit an Instagram account's post performance.
  Returns follower count, average likes, average comments, engagement rate, and recent post performance.
  Ideal for influencer agencies, brand marketing teams, and campaign performance analysts.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/instagram-scraper
---

# Benchmarking Instagram Influencer Engagement

Pulls recent post data for one or multiple Instagram accounts and calculates engagement rate, consistency, and performance benchmarks. Used to vet influencers before partnerships or compare accounts against each other.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed


## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | Instagram URLs — profiles, hashtags, locations, audio pages, reels |
| `until` | string | Optional | — | Scrape posts until this date (YYYY-MM-DD) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |
## Workflow

```
Progress:
- [ ] Step 1: Get account list and analysis goal
- [ ] Step 2: Run instagram-scraper for each account
- [ ] Step 3: Calculate engagement rate per account
- [ ] Step 4: Apply benchmark standards
- [ ] Step 5: Deliver comparison report
```

### Step 1: Clarify Parameters

Ask the user for:
- **Instagram handles** to analyze (up to 10 accounts; each handle without @)
- **Number of recent posts to analyze** (default: 30 — enough for statistical reliability)
- **Analysis goal** — vetting for partnership, competitive benchmarking, or general audit

### Step 2: Run the Actor

Run separately for each account or pass as a list.


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~instagram-scraper"
Input:
{
  "usernames": ["[handle1]", "[handle2]", "[handle3]"],
  "maxItems": 30
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "usernames": ["[handle1]", "[handle2]"],
    "maxItems": 30
  }'
```

Wait for `SUCCEEDED`. Fetch dataset.

### Step 3: Calculate Engagement Metrics

For each account, from its posts array:

```
avg_likes = sum(post.likesCount) / num_posts
avg_comments = sum(post.commentsCount) / num_posts
engagement_rate = (avg_likes + avg_comments) / follower_count * 100
posting_frequency = num_posts / date_range_days
```

**Benchmark standards by follower tier:**
| Tier | Followers | Good ER | Great ER |
|------|-----------|---------|----------|
| Nano | 1K–10K | 5–8% | >8% |
| Micro | 10K–100K | 3–5% | >5% |
| Mid | 100K–500K | 1.5–3% | >3% |
| Macro | 500K–1M | 1–2% | >2% |
| Mega | 1M+ | 0.5–1% | >1% |

### Step 4: Flag Anomalies

Flag accounts with suspicious engagement patterns:
- **Low ER relative to tier:** ER below 0.5% suggests inflated followers
- **Like/Comment imbalance:** Very high likes but near-zero comments suggests like-buying
- **Engagement spikes:** One post with 10x normal engagement followed by dead content suggests bought promotion
- **Sudden follower jump:** Cross-reference last follower count change (if visible)

### Step 5: Format Report

## Output Format

```
# Instagram Engagement Benchmark Report
Accounts analyzed: [N] | Posts per account: [30] | Date: [DATE]

## Summary Comparison
| Account | Followers | Avg Likes | Avg Comments | Eng. Rate | Tier Benchmark | Status |
|---------|-----------|-----------|--------------|-----------|----------------|--------|
| @[name] | [N]       | [N]       | [N]          | [X.X%]    | [good/great/low] | ✅/⚠️/❌ |

## Detailed Analysis

### @[handle1]
- Followers: [N] | Tier: [Nano/Micro/Mid/Macro/Mega]
- Avg Likes: [N] | Avg Comments: [N]
- **Engagement Rate: [X.X%]** — [above/at/below] benchmark for this tier
- Posting frequency: [X] posts/week
- Best-performing post: [url] ([N] likes, [N] comments)
- ⚠️ Anomalies: [none / describe if any]
- **Verdict:** [Recommended / Proceed with caution / Do not recommend]

### @[handle2]
[same structure]

## Benchmark Verdict Key
- ✅ Healthy engagement — safe to partner with
- ⚠️ Below benchmark — investigate further before committing budget
- ❌ Suspicious patterns — likely inflated audience, do not recommend
```

## Troubleshooting

**Private accounts:** Instagram scraper cannot access private profiles. Skip these.
**Low post count:** Accounts with <10 recent posts have unreliable ER stats — flag this.
**Reels vs. posts:** Reels typically get 2-3x more engagement than static posts. If the account posts mostly Reels, adjust expectations.

