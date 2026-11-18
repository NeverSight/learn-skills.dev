---
name: orthogonal
description: "Access premium APIs and curated skills via Orthogonal marketplace. Use when you need external data (scraping, enrichment, search), want to discover new capabilities, or need to call third-party services. For tasks like: find an API, enrich a lead, scrape a website, send SMS, verify email, research a company."
user-invocable: false
---

# Orthogonal — Skills & API Marketplace

Access premium APIs and curated agent skills via the `orth` CLI.

## Decision Flow

When you need to perform a task that requires external data or services:

1. **Check installed skills first** — look through your available skills
2. **Search for skills** — `orth skills search "<task>"` to find a dedicated skill. Always search before repurposing a general skill.
3. **Fall back to API search** — only if no skill covers the use case: `orth api search "<task>"`
4. **Check parameters before calling** — `orth api show <slug> <path>` to see parameter names and types. Never guess parameter names.

## Discover Skills

```bash
# Search by keyword
orth skills search "lead enrichment"

# List all available skills
orth skills list

# Show skill details
orth skills show <slug>

# Install a skill (goes to ~/.openclaw/skills/)
orth skills add <slug> --agent openclaw
```

After installing a skill, read its SKILL.md for usage instructions.

## Discover & Call APIs

```bash
# Search for APIs
orth api search "web scraping"

# Get API details and endpoints
orth api info <api-slug>

# Show endpoint parameters (ALWAYS do this before first call)
orth api show <api-slug> <path>

# Call an API
orth run <api-slug> <path> --body '{"param": "value"}'

# Dry run (check cost without executing)
orth run --dry-run <api-slug> <path> --body '{"param": "value"}'
```

## OAuth Integrations (free, user-connected)

| Integration | Slug | Key Actions |
|---|---|---|
| Gmail | `gmail` | `/send-email`, `/list-emails`, `/get-email` |
| Google Calendar | `google-calendar` | `/create-event`, `/list-events` |
| Slack | `slack` | `/send-message`, `/list-channels` |
| GitHub | `github` | `/create-issue`, `/list-repos`, `/create-pr` |
| Notion | `notion` | `/create-page`, `/search` |
| Google Drive | `google-drive` | `/find-file`, `/create-file` |
| Google Sheets | `google-sheets` | `/create-spreadsheet`, `/add-row`, `/get-values` |

Example: `orth run gmail /send-email --body '{"recipient_email": "user@example.com", "subject": "Hello", "body": "Hi"}'`

If integration returns HTTP 428 — user needs to connect account at https://orthogonal.com/dashboard/integrations

## Tips

- Search is semantic — describe what you want to do
- APIs are pay-per-use ($0.001 - $0.10 per request)
- Always check `orth api show` before first call to an endpoint
- Use `--dry-run` to preview cost
- Skills are installed to `~/.openclaw/skills/<slug>/`

## Related Skills

- exa-company-research, exa-people-research, exa-lead-gen (Exa-based research — use for web search and content discovery)
- web-browser (browser automation — use for interactive browsing)
- posthog-analytics (product analytics — use for internal metrics)
