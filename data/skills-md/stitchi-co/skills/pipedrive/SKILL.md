---
name: pipedrive
description: Interact with Pipedrive CRM via REST API. Use when checking deal pipeline, sales activity, contacts, organizations, or revenue data. Covers deals, persons, organizations, activities, pipelines, and stages.
compatibility: Requires curl and PIPEDRIVE_API_TOKEN environment variable.
metadata:
  author: stitchi-co
  version: "1.0.0"
---

# Pipedrive

Query and manage Pipedrive CRM data via REST API v1.

## Auth

Requires `PIPEDRIVE_API_TOKEN` environment variable.

All requests append `?api_token=$PIPEDRIVE_API_TOKEN` as a query parameter.

Base URL: `https://api.pipedrive.com/v1`

## Setup

List your pipelines and stages to get IDs:
```bash
curl -s "https://api.pipedrive.com/v1/pipelines?api_token=$PIPEDRIVE_API_TOKEN"
curl -s "https://api.pipedrive.com/v1/stages?api_token=$PIPEDRIVE_API_TOKEN"
```

## Common Queries

**List open deals (with pagination):**
```bash
curl -s "https://api.pipedrive.com/v1/deals?api_token=$PIPEDRIVE_API_TOKEN&status=open&limit=100&sort=update_time%20DESC"
```

**Deals in a specific pipeline:**
```bash
curl -s "https://api.pipedrive.com/v1/deals?api_token=$PIPEDRIVE_API_TOKEN&status=open&pipeline_id=PIPELINE_ID"
```

**Deal summary (aggregate values):**
```bash
curl -s "https://api.pipedrive.com/v1/deals/summary?api_token=$PIPEDRIVE_API_TOKEN&status=open"
```

**Upcoming activities:**
```bash
curl -s "https://api.pipedrive.com/v1/activities?api_token=$PIPEDRIVE_API_TOKEN&done=0&limit=50&sort=due_date%20ASC"
```

**Recent activity (done in last 7 days):**
```bash
curl -s "https://api.pipedrive.com/v1/activities?api_token=$PIPEDRIVE_API_TOKEN&done=1&limit=50&sort=due_date%20DESC"
```

**Search persons/orgs:**
```bash
curl -s "https://api.pipedrive.com/v1/persons/search?api_token=$PIPEDRIVE_API_TOKEN&term=NAME"
curl -s "https://api.pipedrive.com/v1/organizations/search?api_token=$PIPEDRIVE_API_TOKEN&term=NAME"
```

**Get specific deal with details:**
```bash
curl -s "https://api.pipedrive.com/v1/deals/DEAL_ID?api_token=$PIPEDRIVE_API_TOKEN"
```

**Deals updated recently (stale deal detection):**
```bash
curl -s "https://api.pipedrive.com/v1/deals?api_token=$PIPEDRIVE_API_TOKEN&status=open&sort=update_time%20ASC&limit=100"
```

## Key Response Fields (Deals)

- `title` — deal name
- `value` / `currency` — monetary value
- `status` — open, won, lost, deleted
- `stage_id` — current stage
- `pipeline_id` — which pipeline
- `add_time` / `update_time` — timestamps
- `owner_name` — assigned to
- `org_name` / `person_name` — linked org/contact
- `expected_close_date` — forecasted close
- `weighted_value` — probability-adjusted value

## Pagination

Responses include `additional_data.pagination`:
- `more_items_in_collection` — boolean
- `next_start` — offset for next page
- `limit` — items per page (max 500)

Append `&start=N` for next page.

## Rate Limits

80 requests per 2 seconds per API token. For bulk queries, add small delays.
