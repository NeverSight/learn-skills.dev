---
name: data-scraper-agent
description: Build an automated, scheduled AI data-collection agent for any public source — scrapes on a schedule, enriches with a free LLM (Gemini Flash), stores to Notion/Sheets/Supabase, learns from feedback. Use when the user wants to monitor, collect, or track public data automatically.
origin: community
---

# Data Scraper Agent

Build a production-ready, AI-powered data collection agent for any public data source.
Runs on a schedule, enriches results with a free LLM, stores to a database, and improves over time.

**Stack: Python · Gemini Flash (free) · GitHub Actions (free) · Notion / Sheets / Supabase**

## When to Activate

- User wants to scrape or monitor any public website or API
- User says "build a bot that checks...", "monitor X for me", "collect data from..."
- User wants to track jobs, prices, news, repos, sports scores, events, listings
- User asks how to automate data collection without paying for hosting
- User wants an agent that gets smarter over time based on their decisions

## Core Concepts

### The Three Layers

Every data scraper agent has three layers:

```
COLLECT → ENRICH → STORE
  │           │        │
Scraper    AI (LLM)  Database
runs on    scores/   Notion /
schedule   summarises Sheets /
           & classifies Supabase
```

### Free Stack

| Layer | Tool | Why |
|---|---|---|
| **Scraping** | `requests` + `BeautifulSoup` | No cost, covers 80% of public sites |
| **JS-rendered sites** | `playwright` (free) | When HTML scraping fails |
| **AI enrichment** | Gemini Flash via REST API | 500 req/day, 1M tokens/day — free |
| **Storage** | Notion API | Free tier, great UI for review |
| **Schedule** | GitHub Actions cron | Free for public repos |
| **Learning** | JSON feedback file in repo | Zero infra, persists in git |

### AI Model Fallback Chain

Build agents to auto-fallback across Gemini models on quota exhaustion:

```
gemini-2.0-flash-lite (30 RPM) →
gemini-2.0-flash (15 RPM) →
gemini-2.5-flash (10 RPM) →
gemini-flash-lite-latest (fallback)
```

### Batch API Calls for Efficiency

Never call the LLM once per item. Always batch:

```python
# BAD: 33 API calls for 33 items
for item in items:
    result = call_ai(item)  # 33 calls → hits rate limit

# GOOD: 7 API calls for 33 items (batch size 5)
for batch in chunks(items, size=5):
    results = call_ai(batch)  # 7 calls → stays within free tier
```

---

## Workflow

### Step 1: Understand the Goal

Ask the user:

1. **What to collect:** "What data source? URL / API / RSS / public endpoint?"
2. **What to extract:** "What fields matter? Title, price, URL, date, score?"
3. **How to store:** "Where should results go? Notion, Google Sheets, Supabase, or local file?"
4. **How to enrich:** "Do you want AI to score, summarise, classify, or match each item?"
5. **Frequency:** "How often should it run? Every hour, daily, weekly?"

Common examples to prompt:
- Job boards → score relevance to resume
- Product prices → alert on drops
- GitHub repos → summarise new releases
- News feeds → classify by topic + sentiment
- Sports results → extract stats to tracker
- Events calendar → filter by interest

### Step 2: Design the Agent Architecture

Generate this directory structure for the user:

```
my-agent/
├── config.yaml              # User customises this (keywords, filters, preferences)
├── profile/
│   └── context.md           # User context the AI uses (resume, interests, criteria)
├── scraper/
│   ├── __init__.py
│   ├── main.py              # Orchestrator: scrape → enrich → store
│   ├── filters.py           # Rule-based pre-filter (fast, before AI)
│   └── sources/
│       ├── __init__.py
│       └── source_name.py   # One file per data source
├── ai/
│   ├── __init__.py
│   ├── client.py            # Gemini REST client with model fallback
│   ├── pipeline.py          # Batch AI analysis
│   ├── jd_fetcher.py        # Fetch full content from URLs (optional)
│   └── memory.py            # Learn from user feedback
├── storage/
│   ├── __init__.py
│   └── notion_sync.py       # Or sheets_sync.py / supabase_sync.py
├── data/
│   └── feedback.json        # User decision history (auto-updated)
├── .env.example
├── setup.py                 # One-time DB/schema creation
├── enrich_existing.py       # Backfill AI scores on old rows
├── requirements.txt
└── .github/
    └── workflows/
        └── scraper.yml      # GitHub Actions schedule
```

### Steps 3-8: Build the Code

Implement each module from the full templates in **reference/implementation.md**:

- **Step 3 — Scraper source** (`scraper/sources/my_source.py`): `fetch()` returns items with standard schema `{name, url, source, date_found}`; includes HTML and RSS variants.
- **Step 4 — Gemini client** (`ai/client.py`): `generate()` with the 4-model fallback chain, rate limiting, and JSON parsing.
- **Step 5 — AI pipeline** (`ai/pipeline.py`): `analyse_batch()` chunks items (batch size 5), builds prompt with context + priorities + feedback bias, enriches with `ai_score`/`ai_summary`/`ai_notes`.
- **Step 6 — Feedback learning** (`ai/memory.py`): `load_feedback()`, `save_feedback()`, `build_preference_prompt()` to bias future scoring.
- **Step 7 — Storage** (`storage/notion_sync.py`): `get_existing_urls()` for dedup, `push_item()`, `sync()`.
- **Step 8 — Orchestrator** (`scraper/main.py`): wires sources → dedup by URL → AI enrich (if `GEMINI_API_KEY` set) → storage sync.

### Steps 9-10: Schedule & Configure

From **reference/github-actions.md**:

- **Step 9 — GitHub Actions** (`.github/workflows/scraper.yml`): cron schedule + `workflow_dispatch`, runs the agent, commits `feedback.json` after each run.
- **Step 10 — config.yaml**: single user-facing config — filters, priorities, storage provider, feedback statuses, AI settings. Also includes `requirements.txt`.

---

## Common Scraping Patterns

Five reusable fetch patterns (REST API, HTML, RSS, paginated API, JS-rendered via Playwright) are in **reference/scraping-patterns.md**.

---

## Anti-Patterns to Avoid

| Anti-pattern | Problem | Fix |
|---|---|---|
| One LLM call per item | Hits rate limits instantly | Batch 5 items per call |
| Hardcoded keywords in code | Not reusable | Move all config to `config.yaml` |
| Scraping without rate limit | IP ban | Add `time.sleep(1)` between requests |
| Storing secrets in code | Security risk | Always use `.env` + GitHub Secrets |
| No deduplication | Duplicate rows pile up | Always check URL before pushing |
| Ignoring `robots.txt` | Legal/ethical risk | Respect crawl rules; use public APIs when available |
| JS-rendered sites with `requests` | Empty response | Use Playwright or look for the underlying API |
| `maxOutputTokens` too low | Truncated JSON, parse error | Use 2048+ for batch responses |

---

## Free Tier Limits Reference

| Service | Free Limit | Typical Usage |
|---|---|---|
| Gemini Flash Lite | 30 RPM, 1500 RPD | ~56 req/day at 3-hr intervals |
| Gemini 2.0 Flash | 15 RPM, 1500 RPD | Good fallback |
| Gemini 2.5 Flash | 10 RPM, 500 RPD | Use sparingly |
| GitHub Actions | Unlimited (public repos) | ~20 min/day |
| Notion API | Unlimited | ~200 writes/day |
| Supabase | 500MB DB, 2GB transfer | Fine for most agents |
| Google Sheets API | 300 req/min | Works for small agents |

---

## Quality Checklist

Before marking the agent complete:

- [ ] `config.yaml` controls all user-facing settings — no hardcoded values
- [ ] `profile/context.md` holds user-specific context for AI matching
- [ ] Deduplication by URL before every storage push
- [ ] Gemini client has model fallback chain (4 models)
- [ ] Batch size ≤ 5 items per API call
- [ ] `maxOutputTokens` ≥ 2048
- [ ] `.env` is in `.gitignore`
- [ ] `.env.example` provided for onboarding
- [ ] `setup.py` creates DB schema on first run
- [ ] `enrich_existing.py` backfills AI scores on old rows
- [ ] GitHub Actions workflow commits `feedback.json` after each run
- [ ] README covers: setup in < 5 minutes, required secrets, customisation

---

## Real-World Examples

```
"Build me an agent that monitors Hacker News for AI startup funding news"
"Scrape product prices from 3 e-commerce sites and alert when they drop"
"Track new GitHub repos tagged with 'llm' or 'agents' — summarise each one"
"Collect Chief of Staff job listings from LinkedIn and Cutshort into Notion"
"Monitor a subreddit for posts mentioning my company — classify sentiment"
"Scrape new academic papers from arXiv on a topic I care about daily"
"Track sports fixture results and keep a running table in Google Sheets"
"Build a real estate listing watcher — alert on new properties under ₹1 Cr"
```

A complete working agent built with this exact architecture would scrape 4+ sources,
batch Gemini calls, learn from Applied/Rejected decisions stored in Notion, and run
100% free on GitHub Actions. Follow Steps 1–10 above to build your own.

---

## Reference Files

- **reference/implementation.md** — read when building the agent code (Steps 3-8): scraper source, Gemini client, AI pipeline, feedback memory, Notion storage, orchestrator.
- **reference/github-actions.md** — read when wiring scheduling/config (Steps 9-10): GitHub Actions YAML, `config.yaml` template, `requirements.txt`.
- **reference/scraping-patterns.md** — read when implementing a specific source type: REST API, HTML, RSS, paginated, or JS-rendered (Playwright) fetch patterns.
