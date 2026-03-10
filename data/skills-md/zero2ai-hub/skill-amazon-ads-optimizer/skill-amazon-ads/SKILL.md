---
name: skill-amazon-ads
description: "Amazon Ads API v3 skill for OpenClaw agents. List profiles, manage Sponsored Products campaigns, view budgets and performance. Works with any advertiser account."
metadata:
  openclaw:
    requires: { bins: ["node"] }
---

# Amazon Ads API Skill

Manage Amazon Sponsored Products campaigns from your OpenClaw agent — list profiles, view campaigns, check budgets, and pull performance data.

---

## Setup

### 1. Create credentials file
```json
{
  "lwaClientId": "amzn1.application-oa2-client.YOUR_CLIENT_ID",
  "lwaClientSecret": "YOUR_CLIENT_SECRET",
  "refreshToken": "Atzr|YOUR_REFRESH_TOKEN",
  "profileId": "YOUR_ADS_PROFILE_ID",
  "region": "eu"
}
```
Save as `amazon-ads-api.json`. Set `AMAZON_ADS_PATH` env var to point to it (default: `./amazon-ads-api.json`).

> **Regions & endpoints:**
> - `na` → `advertising-api.amazon.com`
> - `eu` → `advertising-api-eu.amazon.com`
> - `fe` → `advertising-api-fe.amazon.com`

### 2. Get your Profile ID
```bash
node scripts/ads.js --profiles
```
Copy the `profileId` for your brand/marketplace and add it to the credentials file.

---

## Scripts

### `ads.js` — Campaigns & Summary
```bash
node scripts/ads.js --profiles                # list all advertiser profiles
node scripts/ads.js --campaigns               # list all SP campaigns
node scripts/ads.js --summary                 # active campaigns + budgets summary
node scripts/ads.js --campaigns --out c.json  # save to file
```

---

## Credentials Schema

| Field | Description |
|-------|-------------|
| `lwaClientId` | Ads app client ID (separate from SP-API) |
| `lwaClientSecret` | Ads app client secret |
| `refreshToken` | LWA refresh token |
| `profileId` | Advertising profile ID (from `--profiles`) |
| `region` | `na`, `eu`, or `fe` |

---

## Notes
- Ads API uses a **separate LWA app** from SP-API — different client ID/secret
- Profile ID is required for all campaign operations
- Tokens are fetched fresh per request (no caching overhead for CLI use)
- For production/high-frequency use, add token caching

## Related
- [skill-amazon-spapi](https://github.com/Zero2Ai-hub/skill-amazon-spapi) — Orders, inventory & listings
