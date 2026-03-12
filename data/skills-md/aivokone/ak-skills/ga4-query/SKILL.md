---
name: ga4-query
description: "Query Google Analytics 4 via the Data API. Use when the user asks about GA4, Google Analytics, website traffic, page views, sessions, users, realtime data, or analytics reports. Triggered by: GA4, Google Analytics, analytics, sessions, pageviews, activeUsers, traffic, realtime, bounce rate, engagement."
---

# GA4 Query

## Setup

Check prerequisites before querying:

**Script path resolution:** Before running any script, determine the correct base path. Check in this order:
1. `.claude/skills/ga4-query/scripts/` — project-local install (run from repository root)
2. `~/.claude/skills/ga4-query/scripts/` — global install

Use whichever path exists. All script paths below use the project-local form; substitute the global path if that's where scripts are found.

1. **Virtual environment**: `.claude/skills/ga4-query/scripts/.venv/` must exist
2. **Config file**: `ga4-config.yaml` must be findable (see Config section)
3. **APIs enabled** in GCP project: Google Analytics Data API + Google Analytics Admin API

### First-time setup

```bash
# 1. Install dependencies
bash .claude/skills/ga4-query/scripts/setup.sh

# 2. Create ga4-config.yaml in project root or ~/.config/ga4-query/
#    (see Config section for template)

# 3. Enable APIs in GCP Console:
#    - Google Analytics Data API (analyticsdata.googleapis.com)
#    - Google Analytics Admin API (analyticsadmin.googleapis.com)

# 4. Test
ga4 accounts
```

### Claude Code sandbox

When running inside the Claude Code sandbox, network access is restricted. Add the following domains to `~/.claude/settings.json` under `sandbox.network.allowedDomains`:

**Setup (pip install):**
- `pypi.org`
- `files.pythonhosted.org`

**Runtime (GA4 API):**
- `analyticsdata.googleapis.com`
- `analyticsadmin.googleapis.com`
- `oauth2.googleapis.com`

## Config

The script searches for `ga4-config.yaml` in this order:

1. `--config` CLI parameter (explicit path)
2. `./ga4-config.yaml` (project root)
3. `~/.config/ga4-query/ga4-config.yaml` (user-level)

Template (`ga4-config.yaml`):
```yaml
property_id: "YOUR_PROPERTY_ID"
credentials_json: "/path/to/service-account.json"
```

The service account must have **Viewer** role on the GA4 property. Auth uses `service_account.Credentials.from_service_account_file()` with scope `analytics.readonly`.

## Usage

Use the `ga4` alias:

```bash
alias ga4='.claude/skills/ga4-query/scripts/.venv/bin/python3 .claude/skills/ga4-query/scripts/query.py'
```

### Subcommands

#### report — Standard reports (main command)

```bash
# Sessions and users by date (last 7 days)
ga4 report -d date -m sessions,activeUsers --start 7daysAgo --end yesterday

# Top pages by views
ga4 report -d pagePath -m screenPageViews --start 30daysAgo --end yesterday --order-by screenPageViews --desc --limit 20

# Traffic sources
ga4 report -d sessionSource,sessionMedium -m sessions --start 30daysAgo --end yesterday

# With filter
ga4 report -d pagePath -m screenPageViews --start 7daysAgo --end yesterday --filter "pagePath=~/palvelut"

# Multiple filters (ANDed)
ga4 report -d date -m sessions --start 7daysAgo --end yesterday --filter "country==Finland" --filter "sessionSource==google"

# JSON via stdin (recommended — avoids shell escaping issues)
echo '{"dimensions":["pagePath"],"metrics":["screenPageViews"],"dateRanges":[{"startDate":"7daysAgo","endDate":"yesterday"}]}' | ga4 report --json -

# JSON as direct argument (only for simple JSON with no nested quotes)
ga4 report --json '{"dimensions":["pagePath"],"metrics":["screenPageViews"],"dateRanges":[{"startDate":"7daysAgo","endDate":"yesterday"}]}'
```

Flags:
- `-d` / `--dimensions` — Comma-separated dimension names
- `-m` / `--metrics` — Comma-separated metric names (required unless `--json`)
- `--start` — Start date (default: `7daysAgo`)
- `--end` — End date (default: `yesterday`)
- `--filter` — Dimension filter (repeatable, ANDed together)
- `--order-by` — Sort field name
- `--desc` — Descending order (use with `--order-by`)
- `--limit` — Max rows
- `--json` — Raw JSON request body (overrides all other flags)

#### realtime — Live data

```bash
ga4 realtime -m activeUsers
ga4 realtime -d country -m activeUsers
```

No date range — realtime always returns last ~30 minutes.

#### Admin commands

```bash
ga4 accounts         # List accounts + properties
ga4 property         # Current property details
ga4 custom-dims      # Custom dimensions
ga4 custom-metrics   # Custom metrics
```

### Global flags

```bash
--config /path/to/ga4-config.yaml    # Override config search
--property 123456789                  # Override property_id from config
```

## Filter Syntax

| Syntax | Match type | Example |
|--------|-----------|---------|
| `field==value` | EXACT | `country==Finland` |
| `field!=value` | NOT EXACT | `pagePath!=/` |
| `field=~value` | CONTAINS | `pagePath=~/palvelut` |
| `field=^value` | BEGINS_WITH | `pagePath=^/blog` |
| `field=$value` | ENDS_WITH | `pagePath=$.html` |
| `field=*v1,v2` | IN_LIST | `country=*Finland,Sweden` |
| `field>N` | GREATER_THAN | `sessions>100` |
| `field>=N` | GREATER_THAN_OR_EQUAL | `sessions>=50` |
| `field<N` | LESS_THAN | `sessions<10` |
| `field<=N` | LESS_THAN_OR_EQUAL | `sessions<=5` |

Multiple `--filter` flags are ANDed. For OR logic or nested NOT, use `--json` passthrough via stdin (`echo '...' | ga4 report --json -`).

## Date Formats

- `YYYY-MM-DD` — Specific date (`2024-01-15`)
- `NdaysAgo` — Relative (`7daysAgo`, `30daysAgo`)
- `yesterday` — Yesterday
- `today` — Today (partial data)

## Common Dimensions & Metrics

See [references/dimensions.md](references/dimensions.md) and [references/metrics.md](references/metrics.md) for curated lists.

### Quick reference — Dimensions

| Dimension | Description |
|-----------|-------------|
| `date` | Date (YYYYMMDD format) |
| `pagePath` | Page URL path |
| `pageTitle` | Page title |
| `sessionSource` | Traffic source |
| `sessionMedium` | Traffic medium |
| `sessionCampaignName` | Campaign name |
| `country` | User country |
| `city` | User city |
| `deviceCategory` | desktop/mobile/tablet |

### Quick reference — Metrics

| Metric | Description |
|--------|-------------|
| `sessions` | Total sessions |
| `activeUsers` | Active users |
| `screenPageViews` | Page views |
| `engagementRate` | Engaged sessions / total |
| `averageSessionDuration` | Avg session length (seconds) |
| `bounceRate` | Non-engaged sessions / total |
| `conversions` | Key event conversions |
| `totalRevenue` | Total revenue |

## Output Format

Success — JSON to stdout:
```json
{
  "row_count": 7,
  "rows": [
    {"date": "20240101", "sessions": "142", "activeUsers": "98"}
  ],
  "metadata": {
    "dimensions": ["date"],
    "metrics": ["sessions", "activeUsers"]
  }
}
```

Errors — JSON to stderr + exit code 1:
```json
{"error": "..."}
```

## Notes

- GA4 returns **all values as strings** (unlike Google Ads micros). Numeric aggregation must be done after parsing.
- Realtime data covers approximately the **last 30 minutes**. Not all dimensions/metrics are available in realtime.
- GA4 has **quota limits**: 25,000 tokens/property/day for standard properties. Avoid excessive polling.
- `date` dimension returns format `YYYYMMDD` (no dashes).
- `row_count` in response reflects total matching rows (may exceed `--limit`).
- Admin commands (`accounts`, `property`, `custom-dims`, `custom-metrics`) require the Admin API to be enabled separately from the Data API.
