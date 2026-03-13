---
name: 30x-seo-ai-visibility
description: >
  Monitor brand visibility across AI platforms (Google AI Overview, ChatGPT, Claude, Gemini, Perplexity).
  Track LLM mentions, analyze AI-generated citations, identify AI search opportunities.
  Use when user says "AI visibility", "LLM mentions", "AI Overview", "ChatGPT visibility",
  "AI search", "generative search", "AI citations", or "brand in AI".
allowed-tools:
  - Bash
  - Read
---

# SEO AI Visibility Monitor

Monitor and analyze brand visibility across AI-powered search and LLM platforms using DataForSEO AI Optimization API.

## API Configuration

Credentials stored in `~/.config/dataforseo/auth` (Base64 encoded).

```bash
AUTH=$(cat ~/.config/dataforseo/auth)
```

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo ai-visibility domain <domain>` | Check domain mentions across AI platforms |
| `/seo ai-visibility keyword <keyword>` | See which domains AI cites for a topic |
| `/seo ai-visibility top-domains <keyword>` | Top cited domains for a keyword |
| `/seo ai-visibility top-pages <domain>` | Most cited pages from a domain |
| `/seo ai-visibility compare <domain1> <domain2>` | Compare AI visibility between domains |
| `/seo ai-visibility chatgpt <query>` | Get ChatGPT response for query |
| `/seo ai-visibility claude <query>` | Get Claude response for query |
| `/seo ai-visibility perplexity <query>` | Get Perplexity response for query |

## API Endpoints

### LLM Mentions Search (Domain/Keyword Monitoring)
```bash
curl -s -X POST "https://api.dataforseo.com/v3/ai_optimization/llm_mentions/search/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{
    "target": [{"domain": "example.com"}],
    "platform": "google",
    "location_code": 2840,
    "language_code": "en",
    "limit": 100
  }]'
```

### Top Domains for Keyword
```bash
curl -s -X POST "https://api.dataforseo.com/v3/ai_optimization/llm_mentions/top_domains/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{
    "target": [{"keyword": "TARGET_KEYWORD"}],
    "platform": "google",
    "limit": 20
  }]'
```

### Top Pages for Domain
```bash
curl -s -X POST "https://api.dataforseo.com/v3/ai_optimization/llm_mentions/top_pages/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{
    "target": [{"domain": "example.com"}],
    "platform": "google",
    "limit": 50
  }]'
```

### Aggregated Metrics
```bash
curl -s -X POST "https://api.dataforseo.com/v3/ai_optimization/llm_mentions/aggregated_metrics/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{
    "target": [{"domain": "example.com"}],
    "platform": "google"
  }]'
```

### Cross-Platform Aggregated Metrics
```bash
curl -s -X POST "https://api.dataforseo.com/v3/ai_optimization/llm_mentions/cross_aggregated_metrics/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{
    "target": [{"domain": "example.com"}]
  }]'
```

### ChatGPT Response
```bash
curl -s -X POST "https://api.dataforseo.com/v3/ai_optimization/chat_gpt/llm_responses/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{
    "prompt": "YOUR_QUERY_HERE"
  }]'
```

### Claude Response
```bash
curl -s -X POST "https://api.dataforseo.com/v3/ai_optimization/claude/llm_responses/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{
    "prompt": "YOUR_QUERY_HERE"
  }]'
```

### Gemini Response
```bash
curl -s -X POST "https://api.dataforseo.com/v3/ai_optimization/gemini/llm_responses/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{
    "prompt": "YOUR_QUERY_HERE"
  }]'
```

### Perplexity Response
```bash
curl -s -X POST "https://api.dataforseo.com/v3/ai_optimization/perplexity/llm_responses/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{
    "prompt": "YOUR_QUERY_HERE"
  }]'
```

## Analysis Modes

### 1. Domain AI Visibility Audit

Check how often a domain is cited by AI:

```
Input: domain (e.g., "example.com")
Output:
- Total AI mentions across platforms
- Questions/queries where cited
- Citation position (first source, etc.)
- Trend over time
- Competitor comparison
```

### 2. Keyword AI Landscape

See which domains AI cites for a topic:

```
Input: keyword (e.g., "best project management tools")
Output:
- Top cited domains
- Citation frequency per domain
- Content types that get cited
- Gap analysis (competitors cited, you're not)
```

### 3. AI Response Analysis

Get actual AI responses to understand context:

```
Input: query
Output:
- Raw AI response
- Sources cited
- How your brand is mentioned (if at all)
- Sentiment/positioning
```

### 4. Cross-Platform Comparison

Compare visibility across AI platforms:

```
Input: domain
Output:
- Google AI Overview visibility
- ChatGPT citation rate
- Claude citation rate
- Perplexity citation rate
- Platform-specific insights
```

## Key Metrics

### AI Visibility Score
- **Mentions Count**: Total times cited by AI
- **Query Coverage**: % of relevant queries where cited
- **Citation Position**: Average position in AI responses
- **Source Diversity**: Variety of pages being cited

### Platform Breakdown
| Platform | Data Available |
|----------|---------------|
| Google AI Overview | Mentions, queries, citations |
| ChatGPT | Response content, brand mentions |
| Claude | Response content, brand mentions |
| Gemini | Response content, brand mentions |
| Perplexity | Response content, sources |

## Output Format

### AI Visibility Report
```markdown
# AI Visibility: [domain]
Generated: [Date]

## Overview
- Total AI Mentions: X
- Platforms Present: Google AIO, ChatGPT, Claude
- Top Cited Pages: X pages

## Google AI Overview
- Mentions: X
- Top Queries:
  1. "[query]" - cited in position 1
  2. "[query]" - cited in position 3

## Platform Comparison
| Platform | Mentions | Trend |
|----------|----------|-------|
| Google AIO | X | +15% |
| ChatGPT | X | +8% |
| Claude | X | New |

## Top Cited Content
| Page | Mentions | Queries |
|------|----------|---------|
| /guide | 45 | 23 |
| /blog/post | 32 | 18 |

## Recommendations
1. [Gap identified] - Create content for [topic]
2. [Opportunity] - Optimize [page] for AI citation
```

### Keyword AI Landscape Report
```markdown
# AI Landscape: "[keyword]"

## Top Cited Domains
| Rank | Domain | Mentions | Authority |
|------|--------|----------|-----------|
| 1 | competitor1.com | 89 | High |
| 2 | competitor2.com | 67 | High |
| 3 | your-domain.com | 23 | Medium |

## Citation Analysis
- Average sources per response: 5
- Content types cited:
  - Guides/tutorials: 45%
  - Product pages: 30%
  - Blog posts: 25%

## Gap Opportunities
Keywords where competitors are cited but you're not:
1. [keyword] - competitor1 cited
2. [keyword] - competitor2 cited
```

## Strategic Implications

### Why AI Visibility Matters
- **Zero-click answers**: AI provides direct answers, reducing clicks
- **Authority signal**: Being cited = AI trusts your content
- **Future of search**: AI search growing rapidly
- **Brand presence**: Mentioned = remembered

### Optimization Strategies

1. **Structured content**: Clear headings, lists, definitions
2. **E-E-A-T signals**: Expertise, authoritativeness, trustworthiness
3. **Comprehensive coverage**: Answer related questions
4. **Fresh content**: Regular updates signal relevance
5. **Citation-worthy**: Stats, research, unique insights

### Red Flags
- Zero AI mentions (invisible to AI search)
- Competitors heavily cited, you're not
- Only cited for branded queries
- Decreasing trend in mentions

## Integration with Other Skills

- Use `seo-content` to optimize pages for AI citation
- Use `seo-keywords` to find queries where AI provides answers
- Use `seo-serp` to see AI Overview presence in SERPs
- Use `seo-backlinks` to build authority (correlates with AI trust)

## Best Practices

### Monitoring Cadence
| Check | Frequency |
|-------|-----------|
| Domain mentions | Weekly |
| Competitor comparison | Bi-weekly |
| Top keywords landscape | Monthly |
| Cross-platform audit | Monthly |

### Action Triggers
| Signal | Action |
|--------|--------|
| Competitor cited, you're not | Create/optimize content |
| Mention dropped | Investigate content issues |
| New query emerging | Create content opportunity |
| Wrong page cited | Optimize correct page |

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
