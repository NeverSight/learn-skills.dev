---
name: social-listening
description: "Monitor brand mentions, competitor activity, and industry conversations across web and social media. Use when asked to track what people say, monitor competitors on social, or find industry discussions. For structured competitive analysis, see competitor-research."
user-invocable: true
---

## [YOUR_PRODUCT] Context

Before helping, check `MEMORY.md` for: brand name, competitors, ICP pain phrases.
Follow output preferences from USER.md.
For chat platforms: bullet-point summary of key findings, not raw data.

# Social Listening

Track brand mentions, competitor activity, and industry conversations across the web and social media.

## Workflow

### Step 1: Web Mentions (Exa)

Search for mentions across blogs, forums, news:

```bash
orth run exa /search -d '{"query": "SEARCH_QUERY", "numResults": 20, "contents": {"text": true}}'
```

Query examples:
- Brand monitoring: `"[YOUR_PRODUCT] reviews feedback 2026"`
- Competitor tracking: `"[COMPETITOR_A] [PAIN_KEYWORDS]"`
- Pain signals: `"[PAIN_KEYWORDS your buyers complain about]"`
- Industry trends: `"[YOUR_CATEGORY] enterprise adoption 2026"`

### Step 2: Twitter/X Activity (Scrape Creators)

Monitor a company or person's tweets:

```bash
orth run scrapecreators /v1/twitter/user-tweets -q handle=TARGET_HANDLE
```

Search Twitter for mentions:

```bash
orth run scrapecreators /v1/twitter/search -q query=SEARCH_TERM
```

### Step 3: LinkedIn Activity (Scrape Creators)

Get company page data:

```bash
orth run scrapecreators /v1/linkedin/company -q url=https://linkedin.com/company/COMPANY
```

### Step 4: Extract Insights (ScrapeGraph)

For deep analysis of a specific page found in Steps 1-3:

```bash
orth run scrapegraph /v1/smartscraper -d '{"website_url": "URL_FROM_RESULTS", "user_prompt": "Extract sentiment, key complaints, praise, and feature requests about the product"}'
```

## Output Format

```
Monitoring: [what was searched]

Key findings:
- [finding 1 with source]
- [finding 2 with source]
- [finding 3 with source]

Sentiment: [positive/negative/mixed]

Action items:
- [what to do based on findings]
```

## Monitoring Playbooks

### Brand Monitoring
1. Exa search: `"BRAND_NAME reviews feedback"`
2. Twitter search: brand mentions
3. Summarize sentiment + key themes

### Competitor Watch
1. Exa search: `"COMPETITOR launch announcement funding"`
2. Twitter: competitor handle tweets
3. Analyze what they're shipping and saying

### Pain Signal Detection
1. Exa search: ICP pain phrases from MEMORY.md
2. Twitter search: problem-related keywords
3. Identify potential outbound targets

### Buyer Language Mining
1. Exa search: `"switched from X to Y" OR "looking for alternative to X"`
2. Extract exact phrases buyers use
3. Feed into positioning-messaging and cold-email skills

## Tips

- Include year in Exa queries for fresh results (e.g., "2026")
- Use Exa `contents.text: true` to get actual content, not just links
- Scrape Creators for social, Exa for web — use both for full picture
- Track consistently — set up periodic monitoring, not one-off searches

## Related Skills

- **signal-scanner** — automated buying signal detection (uses social-listening as data source)
- **competitor-research** — structured competitive analysis with pricing/team
- **content-strategy** — plan content based on listening findings
- **cold-email** — write outreach based on pain signals discovered
- **exa-company-research** — deeper web research on specific companies
- **exa-x-search** — X/Twitter search via Exa
