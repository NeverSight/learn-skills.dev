---
name: extracting-tiktok-comments-for-research
description: >
  Extracts and analyzes TikTok comments from any video or creator using apidojo's TikTok Comments scraper on Apify.
  Triggers when the user asks to: scrape TikTok comments from a video, analyze what viewers say about a
  TikTok post, extract comment data for sentiment analysis, find top comments on a viral TikTok video,
  collect TikTok user feedback from comments, build a dataset of TikTok community reactions, study
  audience sentiment on TikTok content, or research what a target audience cares about from TikTok comments.
  Returns commenter username, comment text, likes on comment, reply count, and timestamp.
  Ideal for market researchers, brand managers, content creators, and academic researchers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tiktok-comments-scraper
---

# Extracting TikTok Comments for Research

Pulls all public comments from TikTok videos for audience sentiment analysis, product research, or competitive intelligence. Comments are the rawest form of consumer voice — unfiltered reactions at scale.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed


## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | TikTok video URLs to scrape comments from |
| `includeReplies` | boolean | Optional | `false` | Include reply comments (nested) |
| `maxItems` | number | Optional | Unlimited | Maximum comments to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |
## Workflow

```
Progress:
- [ ] Step 1: Identify target video(s) and research goal
- [ ] Step 2: Run tiktok-comments-scraper
- [ ] Step 3: Fetch and clean comment dataset
- [ ] Step 4: Analyze themes, sentiment, and top comments
- [ ] Step 5: Deliver research output
```

### Step 1: Clarify Parameters

Ask the user for:
- **TikTok video URL(s)** — direct links to specific videos (e.g., `https://www.tiktok.com/@creator/video/[ID]`)
  OR
- **Creator handle** — pull comments from their most recent/viral videos
- **Max comments per video** (default: 500; max: ~3,000)
- **Research goal** — sentiment analysis, product feedback, audience profiling, or competitive intel
- **Date filter** (optional — focus on recent comments only)

**Tip for best research:** Use 3-5 videos from the same creator or about the same topic for a reliable dataset.

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~tiktok-comments-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~tiktok-comments-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~tiktok-comments-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tiktok-comments-scraper"
Input:
{
  "postURLs": [
    "https://www.tiktok.com/@[handle]/video/[VIDEO_ID_1]",
    "https://www.tiktok.com/@[handle]/video/[VIDEO_ID_2]"
  ],
  "maxCommentsPerPost": 500,
  "includeReplies": false
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tiktok-comments-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "postURLs": [
      "https://www.tiktok.com/@[handle]/video/[VIDEO_ID]"
    ],
    "maxCommentsPerPost": 500,
    "includeReplies": false
  }'
```

Wait for `SUCCEEDED`. Fetch dataset.

### Step 3: Clean Comment Dataset

From raw dataset, extract per comment:
- `text` — the comment text
- `author.uniqueId` — commenter username
- `diggCount` — likes on the comment
- `replyCommentTotal` — how many replies this comment received
- `createTime` — timestamp

Clean:
- Remove empty or emoji-only comments (if doing text analysis)
- Remove spam patterns (repeated text, links, self-promotions)
- Remove the creator's own replies (identified by matching `author.uniqueId`)

### Step 4: Analyze by Goal

**Goal: Sentiment analysis**
Classify each comment as Positive / Negative / Neutral (use the same lexical method as the Twitter sentiment skill). Weight by `diggCount` — a liked comment reflects community agreement.

**Goal: Product feedback**
Look for:
- Feature requests: "I wish", "you should", "would be better if", "needs"
- Pain points: "why doesn't it", "can't believe", "problem with", "doesn't work"
- Specific product mentions: nouns that repeat across multiple comments

**Goal: Audience profiling**
From commenter bios (if available) and comment language:
- Identify audience demographics signals (age signals, geographic signals, interest signals)
- Find what questions the audience asks most

**Goal: Top comments**
Simply sort by `diggCount` descending. Top-liked comments represent the community's most agreed-upon reactions.

### Step 5: Format Output

## Output Format

```
# TikTok Comment Analysis
Video(s): [N] | Total comments analyzed: [N] | Date: [DATE]

## Source Videos
| Video | Creator | Views | Comments Extracted |
|-------|---------|-------|-------------------|
| [url] | @[handle] | [N] | [N] |

## Sentiment Distribution (if goal = sentiment)
Positive: [X%] ([N] comments) | Negative: [X%] | Neutral: [X%]
Weighted by likes — Positive: [X%] | Negative: [X%]

## Top 10 Most-Liked Comments
| # | Comment | Likes | Replies |
|---|---------|-------|---------|
| 1 | "[comment text]" | [N] | [N] |

## Key Themes in Comments
| Theme | Frequency | Avg Likes per Comment |
|-------|-----------|----------------------|
| [Theme 1] | [N] | [N] |
| [Theme 2] | [N] | [N] |

## Most Asked Questions
1. "[question text]" — asked by [N] commenters
2. "[question text]" — [N] commenters

## Common Complaints / Pain Points
1. "[pain point]" — [N] comments, [N] total likes

## Audience Signals
- Age/demographic indicators: [summary]
- Geographic signals: [summary]
- Interest signals: [summary]
```

## Troubleshooting

**Few comments returned:** Video may have comments disabled or be relatively new. Try a different video.
**All comments in non-English:** Add a language filter post-processing, or adjust the search to English-language TikTok creators.
**Spam dominates results:** Apply a filter: remove comments shorter than 5 words AND with 0 likes, which tend to be bots.

