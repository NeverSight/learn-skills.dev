---
name: signal-scanner
description: "Scan for buying signals across ICP companies using Exa and social listening. Detects 7 signal types (hiring, funding, pain language, competitor mentions, tech stack changes, content, news), scores them, and routes to pipeline-manager. Run as daily cron or on-demand. For manual prospect research, see exa-company-research."
user-invocable: true
---

## Context

Before scanning, read `MEMORY.md` for: current ICP, wedge, competitors.
Read `memory/pipeline.json` to avoid re-detecting known prospects.
Follow output preferences from USER.md.
For chat platforms: compact signal list, max 15 lines.

# Signal Scanner

Automated buying signal detection for your ICP. Scans multiple sources, scores signals, and feeds qualified prospects into the pipeline.

## Signal Types (7)

### Tier 1: High-Value (7-9 pts, respond in 24-48h)

**1. Leadership Changes / Job Moves (9 pts)**
```bash
exa-search__web_search_advanced_exa \
  query="new CTO OR new VP Engineering OR Head of Engineering hired" \
  category=company \
  numResults=20 \
  startPublishedDate="YYYY-MM-DD"
```
Window: 2-4 weeks after announcement.

**2. Funding Rounds (9 pts)**
```bash
exa-search__web_search_advanced_exa \
  query="series A OR series B OR funding round developer tools OR engineering platform" \
  category=news \
  numResults=20 \
  startPublishedDate="YYYY-MM-DD"
```
Window: 2-6 weeks post-announcement.

**3. Hiring Surge — Target Roles (8 pts)**
```bash
exa-search__web_search_advanced_exa \
  query="hiring [TARGET_ROLE] OR [TARGET_TEAM] expansion [YOUR_DOMAIN_KEYWORDS]" \
  category=company \
  numResults=20
```
Window: Active while postings live.

### Tier 2: Medium-Value (6-7 pts, respond in 1-2 weeks)

**4. Competitor Mentions (7 pts)**
```bash
exa-search__web_search_advanced_exa \
  query="[COMPETITOR_A] OR [COMPETITOR_B] OR [COMPETITOR_C] OR [COMPETITOR_D] review evaluation" \
  category=tweet \
  numResults=20 \
  startPublishedDate="YYYY-MM-DD"
```

**5. Tech Stack Changes (7 pts)**
```bash
exa-search__web_search_advanced_exa \
  query="[TECH_MIGRATION_KEYWORDS related to your wedge — e.g. migrating to X, modernizing Y, adopting Z]" \
  numResults=20 \
  startPublishedDate="YYYY-MM-DD"
```

**6. Published Content on Pain (6 pts)**
```bash
exa-search__web_search_advanced_exa \
  query="[PAIN_KEYWORDS your buyers complain about publicly]" \
  numResults=20 \
  startPublishedDate="YYYY-MM-DD"
```

**7. Company News / Expansion (6 pts)**
```bash
exa-search__web_search_advanced_exa \
  query="[TARGET_TEAM] expansion OR new [TARGET_LOCATION] office OR [JTBD_KEYWORDS]" \
  category=news \
  numResults=20 \
  startPublishedDate="YYYY-MM-DD"
```

## Scan Workflow

### Daily Cron Mode

1. **Set date range** — `startPublishedDate` = yesterday's date (YYYY-MM-DD)
2. **Run Tier 1 scans** (3 queries) — highest value signals first
3. **Run Tier 2 scans** (4 queries) — if Tier 1 yields <3 results
4. **Deduplicate** — Match against existing pipeline.json prospects by domain
5. **Score each signal** — Assign points based on signal type
6. **ICP filter** — Quick check against ICP criteria from MEMORY.md
7. **Route to pipeline-manager**:
   - New prospects: Add with stage `signal_detected`
   - Existing prospects: Update signals array, re-score
8. **Report to chat** — Summary of new signals detected

### On-Demand Mode

When CEO asks "scan for signals" or "find new prospects":
1. Ask for focus (or use default ICP from MEMORY.md)
2. Run all 7 signal scans with wider date range (7-14 days)
3. Present top 10 signals ranked by score
4. Ask which to add to pipeline

## ICP Quick Filter

Before adding to pipeline, verify against ICP criteria from MEMORY.md. Typical filter slots:
- **Must have**: [must-have buyer attributes]
- **Must have**: [must-have company attributes]
- **Nice to have**: [intent signals]
- **Disqualify**: [auto-reject patterns]

## Output Format (Chat)

```
Signal Scan [date]:
[N] new signals detected

Tier 1 (respond today):
1. [Company] — [signal type] — [detail snippet]
   Score: [N] | Size: [N] [headcount metric]

Tier 2 (respond this week):
2. [Company] — [signal type] — [detail snippet]
   ...

Already in pipeline: [N] updated
Next scan: [tomorrow date]
```

## Cost Management

- Each Exa search: ~$0.01-0.05
- Daily scan (7 queries): ~$0.15-0.35
- Monthly: ~$3-7
- Use `startPublishedDate` to avoid re-scanning old content
- Skip Tier 2 if Tier 1 yields enough (>5 new signals)

## Related Skills

- **pipeline-manager** — receives and stores detected signals
- **exa-company-research** — deeper research on a specific company
- **exa-people-research** — find contacts at detected companies
- **social-listening** — deeper social media monitoring
- **competitor-research** — competitor-specific intelligence
- **lead-enrichment** — enrich detected prospects
- **company-intel** — full company dossier
