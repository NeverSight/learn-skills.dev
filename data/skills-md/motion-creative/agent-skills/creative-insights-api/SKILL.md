---
name: creative-insights-api
description: Calls the Motion creative insights api
---

# Creative Insights API

When asked for Motion analytics or creative insights, construct a curl request to the Creative Insights API.

## Environment Variables

The following environment variables must be set:

| Variable | Description |
|----------|-------------|
| `MOTION_API_TOKEN` | Bearer token for API authentication |

## Base URL

```
https://builder-be.staging.motionapp.com/api/creative-insights
```

## Available Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `format` | `'image'` \| `'video'` | Filter by creative format |
| `grouping` | `string` | How to group the results |
| `sortKey` | `string` | Field to sort by (e.g., `thumbstop`, `retention`, `spend`) |
| `sortDirection` | `'asc'` \| `'desc'` | Sort order |
| `dateRange` | `string` | Preset date range (e.g., `last_7d`, `last_30d`, `last_90d`) |
| `startDate` | `string` | Custom start date (ISO format) |
| `endDate` | `string` | Custom end date (ISO format) |
| `limit` | `number` | Maximum number of results to return |
| `creativeAssetIds` | `string` \| Filter by specific creative asset IDs (can pass multiple) |

## Instructions

1. Parse the user's request to determine which parameters to include
2. Only include parameters that are explicitly requested or contextually relevant
3. Build the query string with only the needed parameters
4. Execute the curl command
5. Display the results in a formatted table

## Example Request

```bash
curl -H "Authorization: Bearer $MOTION_API_TOKEN" "https://builder-be.staging.motionapp.com/api/creative-insights?format=video&sortKey=thumbstop&sortDirection=desc&dateRange=last_30d&limit=10"
```

## Default Behavior

If the user doesn't specify parameters, use these sensible defaults:
- `sortDirection=desc`
- `dateRange=last_30d`
- `limit=10`
