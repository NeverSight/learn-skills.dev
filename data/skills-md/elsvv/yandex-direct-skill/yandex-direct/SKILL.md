---
name: yandex-direct
description: |
  Manage Yandex Direct campaigns, ads, keywords, bids, reports via API v5.
  Use when the user needs to work with Yandex Direct API — campaign management,
  ad groups, ads, keywords, bids, targeting, reports, statistics, dictionaries,
  or any other Yandex Direct API operation.
  Triggers: Yandex Direct, Direct API, campaigns API, ad management API,
  keyword bids, Yandex advertising API, Direct reports, Direct statistics.
---

# Yandex Direct API v5

## Essentials

### Base URLs

| Environment | JSON Endpoint | SOAP Endpoint |
|-------------|--------------|---------------|
| **Production** | `https://api.direct.yandex.com/json/v5/{service}` | `https://api.direct.yandex.com/v5/{service}` |
| **Sandbox** | `https://api-sandbox.direct.yandex.com/json/v5/{service}` | `https://api-sandbox.direct.yandex.com/v5/{service}` |
| **Reports** | `https://api.direct.yandex.com/json/v5/reports` | Same pattern |
| **Reports (sandbox)** | `https://api-sandbox.direct.yandex.com/json/v5/reports` | Same pattern |

### Authentication

All requests require an OAuth token in the `Authorization` header.

**Required Headers (every request):**

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer YOUR_OAUTH_TOKEN` | Always |
| `Content-Type` | `application/json; charset=utf-8` | Always |
| `Accept-Language` | `ru` or `en` | Recommended |
| `Client-Login` | `client_login` | Agency accounts only |

**Getting an OAuth Token:**

1. Register app at https://oauth.yandex.ru/client/new with `direct:api` permission
2. Get token: `https://oauth.yandex.ru/authorize?response_type=token&client_id=YOUR_CLIENT_ID`
3. Token appears in redirect URL: `#access_token=TOKEN&token_type=bearer&expires_in=31536000`
4. Token is valid for 1 year

**Quick token setup:**

```bash
bash scripts/get_token.sh --client-id YOUR_CLIENT_ID
```

### Request Format (JSON)

Every API request (except Reports) follows this JSON structure:

```json
{
  "method": "get|add|update|delete|suspend|resume|archive|unarchive|...",
  "params": {
    "SelectionCriteria": { ... },
    "FieldNames": ["Id", "Name", ...],
    "Page": { "Limit": 10000, "Offset": 0 }
  }
}
```

**Key patterns:**

- `SelectionCriteria` -- filter which objects to return (Ids, CampaignIds, States, Statuses, Types, etc.)
- `FieldNames` -- which fields to include in the response
- `Page` -- pagination: `Limit` (max 10000) and `Offset`
- `add` methods use an array of objects (e.g., `"Campaigns": [...]`)
- `update` methods use an array of objects with `Id` field
- `delete` methods use `SelectionCriteria` with `Ids` array

### Response Format

```json
{
  "result": {
    "Campaigns": [ ... ],
    "LimitedBy": 10000
  }
}
```

- `LimitedBy` appears when there are more objects than returned (need pagination)

**Error response:**

```json
{
  "error": {
    "error_code": 53,
    "error_string": "Authorization error",
    "error_detail": "Token not found or expired"
  }
}
```

### Units (API Points) System

Every response includes the `Units` HTTP header: `Units: spent/remaining/daily_limit`

Example: `Units: 10/20828/64000` means 10 points spent, 20828 remaining, 64000 daily limit.

| Rule | Detail |
|------|--------|
| Daily limit | Individual per advertiser, based on campaign activity |
| Refresh | Points awarded every 60 minutes (sliding 24h window) |
| Per period | 1/24 of daily limit per hour + unspent from previous 23 hours |
| Concurrent requests | Max **5** simultaneous requests per advertiser |
| Error cost | 20 points per error (except server errors) |
| Minimum daily limit | ~64,000 points for active accounts |
| Agency | Points deducted from advertiser by default; agency can opt to use own points |

### Common Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 53 | Authorization error | Check token validity |
| 152 | Insufficient points | Wait for points refresh (hourly) |
| 1000 | Concurrent request limit | Reduce parallel requests |
| 1001 | Operation limit exceeded | Reduce batch size |
| 1002 | Invalid token | Reauthorize, get new token |
| 2000 | Unknown error | Retry after delay |
| 8800 | Object limit per request | Reduce batch size |
| 9000 | Insufficient units | Wait for daily limit refresh |

### Sandbox

- Completely isolated from production data
- No web interface -- API only
- Same restrictions as live API
- Reports limited to one campaign per request
- Data deleted after 1 month of inactivity
- Roles: Advertiser or Agency (with 3 test clients)
- Use `YANDEX_DIRECT_SANDBOX=true` in config or set base URL to `api-sandbox.direct.yandex.com`

### Configuration

The skill uses `config/.env` for credentials:

```bash
# Required
YANDEX_DIRECT_TOKEN=your_oauth_token

# Optional: sandbox mode
YANDEX_DIRECT_SANDBOX=true

# Optional: agency client login
YANDEX_DIRECT_CLIENT_LOGIN=client_login
```

## Scripts

**IMPORTANT:** Always run scripts with `bash` prefix and **absolute paths** from the skill directory. Scripts use bash-specific features and will not work if sourced from zsh. Do NOT `source scripts/common.sh` directly — use the wrapper scripts below.

### check_connection.sh
Verify API token and list available campaigns.
```bash
bash scripts/check_connection.sh
```

### campaigns.sh
Manage campaigns: list, get details, stats, suspend/resume/archive.
```bash
# List all campaigns
bash scripts/campaigns.sh --action list

# List only active campaigns
bash scripts/campaigns.sh --action list --states ON

# Get full campaign details
bash scripts/campaigns.sh --action get --ids 12345678

# Get campaign funds/spend info
bash scripts/campaigns.sh --action stats --ids 12345678

# Suspend a campaign
bash scripts/campaigns.sh --action suspend --ids 12345678

# Resume a campaign
bash scripts/campaigns.sh --action resume --ids 12345678
```

| Param | Description |
|-------|-------------|
| `--action, -a` | list, get, stats, suspend, resume, archive, unarchive |
| `--ids, -i` | Comma-separated campaign IDs |
| `--states, -s` | Filter: ON, OFF, SUSPENDED, ENDED, ARCHIVED |
| `--limit, -l` | Max results (default: 100) |

### ads.sh
Manage ads: list, get details, suspend/resume/moderate/archive.
```bash
# List ads by campaign
bash scripts/ads.sh --action list --campaign-ids 12345678

# List ads by ad group
bash scripts/ads.sh --action list --adgroup-ids 987654

# Get specific ad details
bash scripts/ads.sh --action get --ad-ids 111222333

# Suspend an ad
bash scripts/ads.sh --action suspend --ad-ids 111222333
```

| Param | Description |
|-------|-------------|
| `--action, -a` | list, get, suspend, resume, moderate, archive |
| `--campaign-ids` | Filter by campaign IDs |
| `--adgroup-ids` | Filter by ad group IDs |
| `--ad-ids` | Specific ad IDs |
| `--limit, -l` | Max results (default: 1000) |

### keywords.sh
Manage keywords and autotargeting.
```bash
# List keywords by campaign
bash scripts/keywords.sh --action list --campaign-ids 12345678

# List keywords by ad group
bash scripts/keywords.sh --action list --adgroup-ids 987654

# Suspend keywords
bash scripts/keywords.sh --action suspend --ids 111,222,333
```

### reports.sh
Pull statistics reports (campaign, ad group, ad, keyword level).
```bash
# Campaign performance (last 30 days)
bash scripts/reports.sh

# Campaign performance for custom date range
bash scripts/reports.sh --date-range CUSTOM_DATE --date-from 2026-01-01 --date-to 2026-01-31

# Ad-level performance
bash scripts/reports.sh --type AD_PERFORMANCE_REPORT \
  --fields "AdId,AdGroupId,Impressions,Clicks,Ctr,AvgCpc,Cost"

# Keyword/criteria performance with filter
bash scripts/reports.sh --type CRITERIA_PERFORMANCE_REPORT \
  --fields "CriteriaType,Criteria,Impressions,Clicks,Ctr,AvgCpc,Cost" \
  --filter '{"Field":"CampaignId","Operator":"EQUALS","Values":["12345678"]}'

# Demographics (age/gender)
bash scripts/reports.sh --type CAMPAIGN_PERFORMANCE_REPORT \
  --fields "Age,Gender,Impressions,Clicks,Ctr,Cost"

# Search queries report
bash scripts/reports.sh --type SEARCH_QUERY_PERFORMANCE_REPORT \
  --fields "Query,Impressions,Clicks,Ctr,Cost"

# Save report to file
bash scripts/reports.sh --output report.tsv

# Predefined date ranges
bash scripts/reports.sh --date-range YESTERDAY
bash scripts/reports.sh --date-range LAST_7_DAYS
bash scripts/reports.sh --date-range THIS_MONTH
```

| Param | Default | Description |
|-------|---------|-------------|
| `--type, -t` | CAMPAIGN_PERFORMANCE_REPORT | Report type (see below) |
| `--date-range, -r` | LAST_30_DAYS | Date range preset |
| `--date-from` | — | Start date for CUSTOM_DATE |
| `--date-to` | — | End date for CUSTOM_DATE |
| `--fields, -f` | CampaignName,Impressions,Clicks,Ctr,AvgCpc,Cost | Fields |
| `--filter` | — | Filter JSON |
| `--output, -o` | stdout | Save to file |
| `--name, -n` | auto-generated | Report name |

Report types: ACCOUNT_PERFORMANCE_REPORT, CAMPAIGN_PERFORMANCE_REPORT, ADGROUP_PERFORMANCE_REPORT, AD_PERFORMANCE_REPORT, CRITERIA_PERFORMANCE_REPORT, SEARCH_QUERY_PERFORMANCE_REPORT, CUSTOM_REPORT

Date ranges: TODAY, YESTERDAY, LAST_3_DAYS, LAST_7_DAYS, LAST_14_DAYS, LAST_30_DAYS, LAST_90_DAYS, THIS_MONTH, LAST_MONTH, ALL_TIME, CUSTOM_DATE

### dictionaries.sh
Get reference data (regions, currencies, etc.).
```bash
bash scripts/dictionaries.sh --dict GeoRegions
bash scripts/dictionaries.sh --dict Currencies
```

### Advanced: common.sh functions

For custom API calls not covered by scripts above, use `common.sh` functions. **Must be run inside a bash script** (not sourced from zsh):

```bash
#!/bin/bash
source /path/to/scripts/common.sh
load_config
response=$(direct_request "campaigns" '{"method":"get","params":{...}}')
```

## All API v5 Services

| Service | Endpoint Suffix | Methods | Purpose |
|---------|----------------|---------|---------|
| **Campaigns** | `/campaigns` | add, update, delete, get, suspend, resume, archive, unarchive | Campaign management |
| **AdGroups** | `/adgroups` | add, update, delete, get | Ad group management |
| **Ads** | `/ads` | add, update, delete, get, moderate, suspend, resume, archive, unarchive | Ad management |
| **Keywords** | `/keywords` | add, update, delete, get, suspend, resume | Keyword/autotargeting management |
| **BidModifiers** | `/bidmodifiers` | add, set, delete, get | Bid adjustment management |
| **KeywordBids** | `/keywordbids` | set, setAuto, get | Keyword bid management |
| **AudienceTargets** | `/audiencetargets` | add, delete, suspend, resume, get, setBids | Audience target management |
| **RetargetingLists** | `/retargetinglists` | add, update, delete, get | Retargeting list management |
| **Sitelinks** | `/sitelinks` | add, delete, get | Sitelink set management |
| **AdExtensions** | `/adextensions` | add, delete, get | Callout extension management |
| **VCards** | `/vcards` | add, delete, get | Virtual business card management |
| **AdImages** | `/adimages` | add, delete, get | Image management |
| **AdVideos** | `/advideos` | add, get | Video management |
| **Creatives** | `/creatives` | add, get | Creative management |
| **Reports** | `/reports` | POST (custom) | Statistics and reporting |
| **Dictionaries** | `/dictionaries` | get | Reference data (regions, currencies, etc.) |
| **Clients** | `/clients` | get, update | Advertiser account management |
| **AgencyClients** | `/agencyclients` | add, update, get | Agency client management |
| **Changes** | `/changes` | check, checkCampaigns, checkDictionaries | Change tracking |
| **Feeds** | `/feeds` | add, update, delete, get | Product feed management |
| **DynamicTextAdTargets** | `/dynamictextadtargets` | add, delete, get, resume, setBids, suspend | Dynamic ad targeting |
| **SmartAdTargets** | `/smartadtargets` | add, update, delete, get, resume, setBids, suspend | Smart banner targeting |
| **TurboPages** | `/turbopages` | get | Turbo page parameters |
| **Businesses** | `/businesses` | get | Business profile data |
| **Strategies** | `/strategies` | add, update, get, archive, unarchive | Portfolio strategy management |
| **NegativeKeywordSharedSets** | `/negativekeywordsharedsets` | add, update, delete, get | Shared negative keyword sets |
| **KeywordsResearch** | `/keywordsresearch` | hasSearchVolume, deduplicate | Keyword preprocessing |
| **Leads** | `/leads` | get | Turbo page form submissions |
| **Bids** | `/bids` | set, setAuto, get | Bid management (legacy) |

## Detailed References

Read the reference file matching the area you need:

- **Campaign Management** (Campaigns, AdGroups, Ads, Keywords, BidModifiers, KeywordBids) -- [references/campaigns.md](references/campaigns.md)
- **Targeting** (AudienceTargets, RetargetingLists, DynamicTextAdTargets, SmartAdTargets) -- [references/targeting.md](references/targeting.md)
- **Extensions** (Sitelinks, AdExtensions, VCards, AdImages, AdVideos, Creatives) -- [references/extensions.md](references/extensions.md)
- **Reports** (Report service, report types, field names, date ranges, filters, headers) -- [references/reports.md](references/reports.md)
- **Other Services** (Dictionaries, Changes, Clients, AgencyClients, Feeds, Strategies, NegativeKeywordSharedSets, TurboPages, Businesses, Leads, KeywordsResearch) -- [references/other-services.md](references/other-services.md)
- **Common Use Cases** (bash script examples for frequent tasks) -- [references/use-cases.md](references/use-cases.md)

## Guidelines

- Always verify the token is valid before batch operations: `bash scripts/check_connection.sh`
- Use `Page.Limit` and `Page.Offset` for paginating through large result sets (max 10000 per request)
- Request only the `FieldNames` you actually need to save API points
- Use the `Changes` service to detect modifications before re-downloading all data
- For reports, use `processingMode: auto` and handle both 200 (ready) and 201/202 (pending) HTTP status codes
- Set `returnMoneyInMicros: false` in report headers to get human-readable monetary values
- For agency accounts, always include the `Client-Login` header
- Max 5 concurrent requests per advertiser -- queue or throttle your requests
- Use sandbox (`api-sandbox.direct.yandex.com`) for development and testing
- Store tokens securely in `config/.env` (file is gitignored)
- For monetary values in standard API requests/responses: amounts are in micros (multiplied by 1,000,000)
- For monetary values in reports: use `returnMoneyInMicros: false` header to get human-readable values, or divide by 1,000,000
