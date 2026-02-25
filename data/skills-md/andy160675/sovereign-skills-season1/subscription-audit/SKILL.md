---
name: subscription-audit
description: Audit IT, AI, and SaaS subscription fees by searching Gmail and Slack for receipts, invoices, and billing notifications. Use when asked to find subscriptions, audit recurring charges, identify software costs, review SaaS spending, or compile a subscription fee report.
---

# Subscription Audit

Search Gmail and Slack via MCP to discover, extract, and report on all IT/AI/SaaS subscription fees.

## Workflow

The audit involves these steps:

1. Search Gmail with tiered queries (high-yield first, then broader)
2. Search Slack for subscription references
3. Read thread details to extract exact amounts
4. Consolidate and deduplicate results
5. Generate the final audit report

## Step 1: Search Gmail

Use `gmail_search_messages` via MCP. Run queries from `references/search-queries.md`, starting with Tier 1 (highest yield). Set `max_results` to 50–100 per query.

```bash
manus-mcp-cli tool call gmail_search_messages --server gmail --input '{"q": "<QUERY>", "max_results": 100}'
```

For each result file, extract thread IDs and subjects with Python:

```python
import json
with open('<result_file>') as f:
    data = json.load(f)
for t in data.get('result', {}).get('threads', []):
    for msg in t.get('messages', []):
        h = msg.get('pickedHeaders', {})
        print(f"{t['id']} | {h.get('subject','')} | {h.get('from','')}")
```

**Key Tier 1 queries** (always run these):
- `from:stripe.com receipt`
- `from:github.com receipt payment`
- `from:googleplay-noreply@google.com subscription`
- `from:anthropic.com OR from:mail.anthropic.com receipt invoice`
- `from:openai.com receipt invoice billing`
- `from:ionos OR from:godaddy OR from:namecheap OR from:cloudflare invoice domain`

For the full query list with rationale, read `references/search-queries.md`.

## Step 2: Search Slack

Use `slack_search_public_and_private` via MCP:

```bash
manus-mcp-cli tool call slack_search_public_and_private --server slack --input '{"query": "subscription invoice payment billing receipt", "limit": 20}'
```

Run 2–3 query variants. Slack rarely contains billing data but may reference costs in discussion.

## Step 3: Read Thread Details

For threads identified as IT/AI subscriptions, read full content to extract amounts:

```bash
manus-mcp-cli tool call gmail_read_threads --server gmail --input '{"thread_ids": ["<id1>","<id2>"], "include_full_messages": true}'
```

Batch up to 10 thread IDs per call. From the plain text content, extract:
- **Amount** — look for `£`, `$`, `€` followed by digits
- **Plan name** — e.g. "Claude Pro", "Starter", "Team Plan"
- **Billing period** — e.g. "Jan 18 – Feb 18, 2026"
- **Payment method** — e.g. "Visa ending 8149"
- **VAT** — typically 20% for UK-based users

## Step 4: Consolidate

Optionally run the consolidation script on saved MCP result files:

```bash
python3 /home/ubuntu/skills/subscription-audit/scripts/consolidate_results.py <output_dir> <json1> [json2 ...]
```

Group results by service provider. Deduplicate by thread ID. For each service, record:

| Field | Source |
|-------|--------|
| Service name | Sender name or subject line |
| Category | AI Assistant, Developer Tools, Cloud/Hosting, AI Voice, etc. |
| Current plan | From receipt body |
| Monthly cost | From receipt body (convert USD→GBP if needed) |
| Payment method | From receipt body |
| Billing cycle | Monthly or Annual |
| First seen / last seen | Earliest and latest receipt dates |

## Step 5: Generate Report

Use `templates/report_template.md` as the structural guide. The report must include:

1. **Executive Summary** — service count, total monthly/annual cost, summary table
2. **Detailed Analysis** — one section per service with billing history
3. **Conclusion** — recommendations on cost optimisation

Look up the current USD→GBP exchange rate when converting amounts. Deliver the report as a Markdown file with the raw JSON data as a secondary attachment.

## IT/AI Service Categories

When classifying subscriptions, use these categories:

| Category | Examples |
|----------|----------|
| AI Assistant | Anthropic Claude, OpenAI ChatGPT, Perplexity |
| AI Developer Tools | GitHub Copilot, Cursor, Replit |
| AI Voice / Media | ElevenLabs, Midjourney, Runway |
| Developer Tools | GitHub Plans, JetBrains, VS Code |
| Cloud / Hosting | AWS, Azure, Hetzner, DigitalOcean, Vercel |
| Web Hosting / Domain | IONOS, GoDaddy, Namecheap, Cloudflare |
| AI / Cloud Storage | Google AI Pro, iCloud+ |
| Productivity | Notion, Figma, Slack Pro |
| Security / Network | Tailscale, VPN services |
