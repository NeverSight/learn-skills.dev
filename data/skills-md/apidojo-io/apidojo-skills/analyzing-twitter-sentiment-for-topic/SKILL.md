---
name: analyzing-twitter-sentiment-for-topic
description: >
  Analyzes public sentiment on Twitter/X for any topic, brand, or event using apidojo's Tweet scrapers on Apify.
  Triggers when the user asks to: analyze Twitter sentiment about a topic, measure public opinion on Twitter,
  see if sentiment is positive or negative about a brand or issue on X, analyze the emotional tone of tweets
  about an event, research how Twitter reacts to a news story, measure brand or product sentiment from tweets,
  or compare sentiment between two competing topics or brands on Twitter.
  Returns sentiment classification, top positive and negative tweets, volume over time, and key themes.
  Ideal for PR teams, market researchers, political analysts, and social listening platforms.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/tweet-scraper, apidojo/tweet-scraper
---

# Analyzing Twitter Sentiment for a Topic

Collects a sample of tweets about any topic or keyword and performs sentiment analysis across the dataset. Identifies dominant emotional tone, key themes driving positive/negative sentiment, and volume patterns over time.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed


## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `searchTerms` | array | ✅ | `[]` | Twitter advanced search queries (e.g. `["#AI lang:en", "from:NASA"]`) |
| `sort` | string | Optional | `Top` | Sort order: `Latest`, `Top`, or `Latest+Top` |
| `tweetLanguage` | string | Optional | — | ISO 639-1 language code (e.g. `en`) |
| `maxItems` | number | Optional | Unlimited | Maximum tweets to return |
| `onlyVerifiedUsers` | boolean | Optional | `false` | Only tweets from verified users |
| `onlyTwitterBlue` | boolean | Optional | `false` | Only Twitter Blue subscribers |
| `onlyImage` | boolean | Optional | `false` | Only tweets with images |
| `onlyVideo` | boolean | Optional | `false` | Only tweets with videos |
| `onlyQuote` | boolean | Optional | `false` | Only quote tweets |
| `author` | string | Optional | — | Filter to a specific author handle |
| `inReplyTo` | string | Optional | — | Tweets replying to a specific handle |
| `mentioning` | string | Optional | — | Tweets mentioning a specific handle |
| `geotaggedNear` | string | Optional | — | Tweets near a location |
| `withinRadius` | string | Optional | — | Radius around geotaggedNear |
| `geocode` | string | Optional | — | Lat/lng + radius string |
| `placeObjectId` | string | Optional | — | Tweets tagged with a place |
| `minimumRetweets` | number | Optional | — | Minimum retweet count |
| `minimumFavorites` | number | Optional | — | Minimum like count |
| `minimumReplies` | number | Optional | — | Minimum reply count |
| `start` | string | Optional | — | Tweets after this date (YYYY-MM-DD) |
| `end` | string | Optional | — | Tweets before this date (YYYY-MM-DD) |
| `includeSearchTerms` | boolean | Optional | `false` | Add the matched search term to each tweet |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |
## Workflow

```
Progress:
- [ ] Step 1: Define topic and sentiment scope
- [ ] Step 2: Collect tweets via search
- [ ] Step 3: Classify sentiment per tweet
- [ ] Step 4: Identify themes per sentiment bucket
- [ ] Step 5: Deliver sentiment report
```

### Step 1: Clarify Parameters

Ask the user for:
- **Topic, keyword, or brand** to analyze
- **Date range** (default: last 7 days — Twitter sentiment data decays fast)
- **Language** (default: English)
- **Sample size** (default: 500 tweets — sufficient for reliable distribution)
- **Exclude retweets?** (default: yes — reduces duplicated opinion signals)
- **Comparison topic** (optional — for side-by-side sentiment comparison)

### Step 2: Collect Tweets


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tweet-scraper"
Input:
{
  "searchTerms": ["[TOPIC_KEYWORD]"],
  "maxItems": 500,
  "tweetLanguage": "en",
  "since": "[YYYY-MM-DD]",
  "until": "[YYYY-MM-DD]"
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "searchTerms": ["[TOPIC_KEYWORD]"],
    "maxItems": 500,
    "tweetLanguage": "en",
    "since": "[YYYY-MM-DD]"
  }'
```

### Step 3: Classify Sentiment

For each tweet's `text`, classify as Positive, Negative, or Neutral using lexical signals:

**Positive indicators:** love, great, amazing, perfect, best, win, excited, congrats, excellent, recommend, beautiful, proud, happy, thank, awesome, incredible
**Negative indicators:** hate, awful, worst, terrible, broken, scam, disappointed, angry, frustrated, disgusted, avoid, never again, shame, sad, fail, wrong, bad
**Strong negative amplifiers:** "can't believe", "what a joke", "are you serious", "wtf", "this is ridiculous"
**Neutral default:** Everything else

For ambiguous cases, use emoji signals:
- 😍🥰❤️🙌👏✨🔥 → lean Positive
- 😡🤬😤💀🗑️🤢👎 → lean Negative
- 🤔😐🤷 → lean Neutral

Weight tweets by engagement: a tweet with 1,000 likes carries more signal than one with 0.

### Step 4: Theme Extraction

For Negative tweets: identify the top 3-5 recurring nouns/themes. What are people upset about specifically?
For Positive tweets: identify the top 3-5 recurring praise themes.

Look for proper nouns (people, places, products), specific events, or feature names that appear repeatedly.

### Step 5: Format Report

## Output Format

```
# Twitter Sentiment Analysis: "[TOPIC]"
Period: [DATE_RANGE] | Tweets analyzed: [N] | Date: [DATE]

## Overall Sentiment
```
████████████░░░░░░░░  Positive: [X%] ([N] tweets)
████░░░░░░░░░░░░░░░░  Negative: [X%] ([N] tweets)
██████████░░░░░░░░░░  Neutral:  [X%] ([N] tweets)
```

Weighted by engagement:
- Positive sentiment accounts for [X%] of total likes/RTs
- Negative sentiment accounts for [X%] of total likes/RTs

**Overall verdict:** [Mostly Positive / Mixed / Mostly Negative / Polarized]

## Top Negative Themes
1. "[Theme]" — [N] tweets, [N] total likes
   Example: "@[handle]: [tweet excerpt]"
2. "[Theme]" — [N] tweets
3. "[Theme]" — [N] tweets

## Top Positive Themes
1. "[Theme]" — [N] tweets, [N] total likes
   Example: "@[handle]: [tweet excerpt]"
2. "[Theme]" — [N] tweets

## Most Engaged Tweets
🔴 Most-liked negative: @[handle] ([N] likes): "[excerpt]"
🟢 Most-liked positive: @[handle] ([N] likes): "[excerpt]"

## Volume Over Time
[Day 1]: [N] tweets | [Day 2]: [N] tweets | [Day 3]: [N] tweets

## Notable Spikes
[Date with highest volume] — [N] tweets | Likely cause: [describe if detectable from tweet context]
```

## Troubleshooting

**Sentiment feels inaccurate:** Lexical analysis misses sarcasm. For high-stakes decisions, manually review the top 20 tweets per bucket.
**Topic too broad:** Narrow the search term. "Apple" returns tech and food — use "Apple iPhone" instead.
**Very low tweet volume:** Topic may not be actively discussed on Twitter right now. Expand date range.

