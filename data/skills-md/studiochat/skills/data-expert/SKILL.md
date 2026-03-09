---
name: data-expert
description: >
  Analyze customer conversation data, compute metrics, identify patterns, and generate reports
  using the Studio Chat Analytics API. Use when asked to analyze conversations, review performance,
  understand trends, examine deflection rates, sentiment distributions, handoff patterns, or any
  data analysis task involving platform activity.
---

# Data Expert

Fetch data from the Studio Chat API, process it with Python, and produce actionable analysis. All API calls are authenticated automatically via environment variables. The API base URL (`https://api.studiochat.io`) is hardcoded in the scripts.

## Setup

Set the following environment variables before using the scripts:

```bash
export STUDIO_API_TOKEN="sbs_your_api_key_here"
export STUDIO_PROJECT_ID="your-project-uuid"
```

API keys are available by request from the Studio Chat team at hey@studiochat.io.

## Tools

### fetch.py — Single API call

```bash
python3 scripts/fetch.py <path> [--params key=value ...] [-o file.json]
python3 scripts/fetch.py <path> --method POST [--body '{}'] [-o file.json]
```

### export_conversations.py — Batch export with enrichment

```bash
python3 scripts/export_conversations.py \
  --start YYYY-MM-DD --end YYYY-MM-DD [filters] [--enrich metrics|messages|all] \
  [--sentiment negative,neutral,positive] [--resources irrelevant,partial,relevant] \
  [--min-messages N] [--max-messages N] [--sort-by field] [--sort-order asc|desc] \
  [--format json|csv] -o output.json
```

## Workflow

1. **Fetch** — Pull data from the API
2. **Save** — Write raw JSON to a working directory for reference
3. **Process** — Use Python to parse, filter, aggregate, compute
4. **Report** — Write findings to markdown or CSV

Always save intermediate data to files. This enables re-processing without re-fetching.

## API Endpoints

Full specifications: [references/api-reference.md](references/api-reference.md)

### High-Level Metrics

| Endpoint | Returns |
|----------|---------|
| `GET /projects/{pid}/conversations/analytics` | Totals, deflection rate, time series, breakdowns by playbook/tag |
| `GET /account/conversations/analytics` | Account-wide totals across all projects |
| `GET /projects/{pid}/conversations/metrics/aggregate` | Sentiment + resource-quality distributions (filterable by tags, inbox_id, playbook_base_id) |

### Conversation Data

| Endpoint | Returns |
|----------|---------|
| `GET /projects/{pid}/conversations` | Paginated list with filters (playbook, date, handoff, tags, winback, inbox, search, sentiment, resources, message count, sorting) |
| `GET /projects/{pid}/conversations/summaries` | Lightweight summaries for batch scanning (slim: summary, sentiment, resources, tags, message_count) |
| `GET /projects/{pid}/conversations/{cid}/messages` | Full message history + citations |
| `GET /projects/{pid}/conversations/{cid}/metrics` | Sentiment, resource quality, summary for one conversation |
| `POST /projects/{pid}/conversations/{cid}/metrics/analyze` | Trigger scoring for an unscored conversation |

### AI Insights

| Endpoint | Returns |
|----------|---------|
| `GET /projects/{pid}/conversations/insights/trending-topics/status` | Cached topic analysis |
| `POST /projects/{pid}/conversations/insights/trending-topics/generate` | Start new topic analysis |
| `GET /projects/{pid}/conversations/insights/trending-topics/job/{jid}` | Poll job progress |
| `GET /projects/{pid}/conversations/insights/trending-topics/analysis/{aid}` | Completed topic analysis |

### Configuration Context

| Endpoint | Returns |
|----------|---------|
| `GET /projects/{pid}/playbooks` | All playbooks (instructions, KB links, versions) |
| `GET /playbooks/{id}` | Full playbook content |
| `GET /playbooks/{id}/history` | Version history |
| `GET /playbooks/{id}/versions/{n}` | Specific historical version |
| `GET /playbooks/{base_id}/active` | Currently active version |
| `GET /playbooks/{base_id}/active/history` | Deployment timeline |
| `GET /playbooks/{id}/settings` | Kill switch, winback, URL shortener |
| `GET /projects/{pid}/knowledgebases` | All KBs with types and status |
| `GET /knowledgebases/{id}` | Full KB content |
| `GET /knowledgebases/{id}/items/{item_id}` | Individual item metadata |
| `GET /projects/{pid}/schedule` | Office hours, timezone, overrides |
| `GET /projects/{pid}/api-tools` | Custom HTTP integrations |
| `GET /projects/{pid}/settings` | Project personality tone |

### Quality Testing

| Endpoint | Returns |
|----------|---------|
| `GET /playbooks/{base_id}/eval-cases` | Test cases for a playbook |
| `GET /playbooks/{base_id}/eval-runs` | Test run history (paginated) |
| `GET /eval-runs/{run_id}` | Full run results with per-case scores |
| `GET /playbooks/{base_id}/eval-cases/export-yaml` | All cases in YAML format |

---

## Fetching Patterns

### 1. Aggregate Overview (fast, no pagination)

```bash
# High-level totals + breakdowns
python3 scripts/fetch.py \
  "/projects/$STUDIO_PROJECT_ID/conversations/analytics" \
  --params start_date=2025-01-01T00:00:00Z end_date=2025-02-01T00:00:00Z \
  -o analytics.json

# Sentiment + resource quality distributions
python3 scripts/fetch.py \
  "/projects/$STUDIO_PROJECT_ID/conversations/metrics/aggregate" \
  --params start_date=2025-01-01T00:00:00Z end_date=2025-02-01T00:00:00Z \
  -o metrics_agg.json
```

### 2. Filtered Analytics (by playbook, tag)

```bash
# Analytics for a specific playbook (use base_id for all versions)
python3 scripts/fetch.py \
  "/projects/$STUDIO_PROJECT_ID/conversations/analytics" \
  --params start_date=2025-01-01T00:00:00Z end_date=2025-02-01T00:00:00Z \
    playbook_base_ids=PLAYBOOK_BASE_UUID \
  -o playbook_analytics.json

# Analytics filtered by tags (AND logic)
python3 scripts/fetch.py \
  "/projects/$STUDIO_PROJECT_ID/conversations/analytics" \
  --params start_date=2025-01-01T00:00:00Z end_date=2025-02-01T00:00:00Z \
    tags=billing,refund \
  -o billing_refund_analytics.json
```

### 3. Conversation Listing with Filters

```bash
# Only handoff conversations
python3 scripts/fetch.py \
  "/projects/$STUDIO_PROJECT_ID/conversations" \
  --params start_date=2025-01-01T00:00:00Z end_date=2025-02-01T00:00:00Z \
    has_handoff=true limit=100 \
  -o handoffs.json

# Filter by sentiment (server-side, no enrichment needed)
python3 scripts/fetch.py \
  "/projects/$STUDIO_PROJECT_ID/conversations" \
  --params sentiment=negative limit=100 \
  -o negative_convos.json

# Filter by resource quality
python3 scripts/fetch.py \
  "/projects/$STUDIO_PROJECT_ID/conversations" \
  --params resources=irrelevant limit=100 \
  -o irrelevant_resources.json

# Short conversations sorted by message count
python3 scripts/fetch.py \
  "/projects/$STUDIO_PROJECT_ID/conversations" \
  --params max_messages=3 sort_by=message_count sort_order=asc limit=100 \
  -o short_convos.json

# Lightweight summaries for batch scanning
python3 scripts/fetch.py \
  "/projects/$STUDIO_PROJECT_ID/conversations/summaries" \
  --params sentiment=negative limit=50 \
  -o negative_summaries.json
```

### 4. Batch Export (all conversations + enrichment)

```bash
# Export all conversations as JSON
python3 scripts/export_conversations.py \
  --start 2025-01-01 --end 2025-02-01 -o all_conversations.json

# Export with sentiment scores and summaries
python3 scripts/export_conversations.py \
  --start 2025-01-01 --end 2025-02-01 --enrich metrics -o convos_with_metrics.json

# Export EVERYTHING (metrics + messages)
python3 scripts/export_conversations.py \
  --start 2025-01-01 --end 2025-02-01 --enrich all -o full_export.json

# Export only negative sentiment as CSV
python3 scripts/export_conversations.py \
  --start 2025-01-01 --end 2025-02-01 --sentiment negative --format csv -o negative.csv
```

### 5. Single Conversation Deep Dive

```bash
# Get full message history
python3 scripts/fetch.py "/projects/$STUDIO_PROJECT_ID/conversations/CONV_ID/messages" -o messages.json

# Get quality metrics
python3 scripts/fetch.py "/projects/$STUDIO_PROJECT_ID/conversations/CONV_ID/metrics" -o metrics.json

# Trigger scoring for an unscored conversation
python3 scripts/fetch.py "/projects/$STUDIO_PROJECT_ID/conversations/CONV_ID/metrics/analyze" --method POST
```

### 6. Trending Topics Analysis

```bash
# Check if analysis exists
python3 scripts/fetch.py "/projects/$STUDIO_PROJECT_ID/conversations/insights/trending-topics/status"

# Start new analysis
python3 scripts/fetch.py \
  "/projects/$STUDIO_PROJECT_ID/conversations/insights/trending-topics/generate" \
  --method POST --body '{"tags": ["billing"]}'

# Poll job until complete
python3 scripts/fetch.py "/projects/$STUDIO_PROJECT_ID/conversations/insights/trending-topics/job/JOB_ID"
```

---

## Analysis Recipes

### Deflection Rate Analysis

```python
import json

with open("analytics.json") as f:
    data = json.load(f)

print(f"Total conversations: {data['total_conversations']}")
print(f"Deflection rate: {data['deflection_rate']:.1f}%")
print(f"Handoffs: {data['conversations_with_handoff']}")
print(f"AI-resolved: {data['conversations_without_handoff']}")

print("\nBy Playbook:")
for pb in data.get("by_playbook", []):
    print(f"  {pb['playbook_name']}: {pb['deflection_rate']:.1f}% deflection "
          f"({pb['total_conversations']} convs)")
```

### Sentiment Deep Dive

```python
import json

with open("metrics_agg.json") as f:
    agg = json.load(f)

total_scored = agg["total_scored_conversations"]
sent = agg["sentiment_distribution"]

print(f"Scored: {total_scored}/{agg['total_conversations']} ({agg['coverage_percentage']:.1f}% coverage)")
print(f"\nSentiment:")
for label in ["positive", "neutral", "negative"]:
    count = sent.get(label, 0)
    pct = (count / total_scored * 100) if total_scored else 0
    print(f"  {label}: {count} ({pct:.1f}%)")
```

---

## Reference

### Date Ranges

Always scope queries with `start_date` and `end_date` in ISO 8601 format:
- Full: `2025-01-01T00:00:00Z`
- The `export_conversations.py` script accepts short form: `2025-01-01`

### Metric Labels

| Type | Values | Meaning |
|------|--------|---------|
| Sentiment | `negative`, `neutral`, `positive` | Customer satisfaction (LLM-scored) |
| Resources | `irrelevant`, `partial`, `relevant` | How well KBs served the conversation |

### Deflection Rate

`deflection_rate = conversations_without_handoff / total_conversations x 100`

Higher = better (more conversations resolved by AI without human escalation).

### Filter Operators

- `tags` — AND logic: conversation must have ALL specified tags
- `playbook_base_id` — Matches all versions of a playbook
- `sentiment` — Comma-separated OR: `negative`, `neutral`, `positive`
- `resources` — Comma-separated OR: `irrelevant`, `partial`, `relevant`
- `min_messages` / `max_messages` — Integer range filter on message count
- `sort_by` — `last_message_at` (default), `first_message_at`, `message_count`
- `sort_order` — `desc` (default), `asc`
