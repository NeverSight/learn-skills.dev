---
name: desearch-ai-search
description: AI-powered search that aggregates and summarizes results from multiple sources including web, X/Twitter, Reddit, Hacker News, YouTube, ArXiv, and Wikipedia. Use this when you need a synthesized answer or curated links from across the internet and social platforms.
metadata: {"clawdbot":{"emoji":"🔎","homepage":"https://desearch.ai","requires":{"env":["DESEARCH_API_KEY"]}}}
---

# AI Search By Desearch

AI-powered multi-source search that aggregates results from web, Reddit, Hacker News, YouTube, ArXiv, Wikipedia, and X/Twitter — returning either 
summarized answers or curated links.

## Quick Start

1. Get an API key from https://console.desearch.ai
2. Set environment variable: `export DESEARCH_API_KEY='your-key-here'`

## Usage

```bash
# AI contextual search (summarized results from multiple sources)
desearch.py ai_search "What is Bittensor?" --tools web,reddit,youtube

# AI web link search (curated links from specific sources)
desearch.py ai_web "machine learning papers" --tools arxiv,web,wikipedia

# AI X/Twitter link search (curated post links)
desearch.py ai_x "crypto market trends" --count 20
```

## Commands

| Command | Description |
|---------|-------------|
| `ai_search` | AI-summarized search across multiple sources. Returns aggregated results with context. |
| `ai_web` | AI-curated link search. Returns the most relevant links from chosen sources. |
| `ai_x` | AI-powered X/Twitter search. Returns the most relevant post links for a topic. |

## Options

| Option | Description | Applies to |
|--------|-------------|------------|
| `--tools`, `-t` | Sources to search: `web`, `hackernews`, `reddit`, `wikipedia`, `youtube`, `arxiv`, `twitter` (comma-separated) | Both |
| `--count`, `-n` | Number of results (default: 10, max: 200) | All |
| `--date-filter` | Time filter: `PAST_24_HOURS`, `PAST_2_DAYS`, `PAST_WEEK`, `PAST_2_WEEKS`, `PAST_MONTH`, `PAST_2_MONTHS`, `PAST_YEAR`, `PAST_2_YEARS` | `ai_search` |

## Examples

### Research a topic with AI summary
```bash
desearch.py ai_search "What are the latest developments in quantum computing?" --tools web,arxiv,reddit
```

### Find academic papers
```bash
desearch.py ai_web "transformer architecture improvements 2026" --tools arxiv,web
```

### Get recent news from multiple sources
```bash
desearch.py ai_search "AI regulation news" --tools web,hackernews,reddit --date-filter PAST_WEEK
```

### Find YouTube tutorials
```bash
desearch.py ai_web "learn rust programming" --tools youtube,web
```

### AI-curated X/Twitter links on a topic
```bash
desearch.py ai_x "latest AI breakthroughs" --count 20
```

## Response

### Example (truncated)
```json
{
  "tweets": [
    {
      "id": "2023465890369728573",
      "text": "Superposition allows qubits to encode multiple possibilities...",
      "url": "https://x.com/rukky_003/status/2023465890369728573",
      "created_at": "2026-02-16T18:33:57.000Z",
      "like_count": 5,
      "retweet_count": 0,
      "view_count": 155,
      "reply_count": 0,
      "quote_count": 2,
      "lang": "en",
      "is_retweet": false,
      "is_quote_tweet": true,
      "media": [],
      "user": {
        "id": "1316260427190472704",
        "username": "rukky_003",
        "name": "RuqoCrypto 🧠",
        "url": "https://x.com/rukky_003",
        "followers_count": 2424,
        "verified": false,
        "is_blue_verified": true
      }
    }
  ],
  "search": [
    {
      "title": "What Is Quantum Computing? | IBM",
      "link": "https://www.ibm.com/think/topics/quantum-computing",
      "snippet": "Quantum computers take advantage of quantum mechanics..."
    }
  ],
  "miner_link_scores": {
    "2023465890369728573": "HIGH",
    "https://www.ibm.com/think/topics/quantum-computing": "MEDIUM"
  },
  "completion": "Quantum computing uses qubits that leverage superposition and entanglement to compute in fundamentally different ways than classical computers..."
}
```

### Notes
- `miner_link_scores` keys are tweet IDs for Twitter results and full URLs for web results. Values are `"HIGH"`, `"MEDIUM"`, or `"LOW"`.
- `media` is always an array; empty `[]` when no media is attached.
- `completion` is always a string; empty string `""` if summarization fails.

### Errors
Status 401, Unauthorized (e.g., missing/invalid API key)
```json
{
  "detail": "Invalid or missing API key"
}
```

Status 402, Payment Required (e.g., balance depleted)
```json
{
  "detail": "Insufficient balance, please add funds to your account to continue using the service."
}
```


## Resources
- [API Reference](https://desearch.ai/docs/api-reference/post-desearch-ai-search)
- [Desearch Console](https://console.desearch.ai)
