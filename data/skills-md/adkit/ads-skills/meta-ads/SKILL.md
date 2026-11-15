---
name: meta-ads
displayName: "AdKit for Meta Ads: Facebook and Instagram Campaigns, Ad Sets, Ads and Reporting"
description: >
  Create, edit, and report on Meta (Facebook and Instagram) ads from an AI agent through the
  AdKit MCP connector: campaigns, ad sets, ads, carousels, media upload, interest search, and
  results. Every change is saved as a draft that the user approves before it goes live. Use
  when the user wants to run, change, or check Facebook or Instagram ads. Not for Meta ad
  strategy: use meta-ads-strategy for that.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://adkit.so/features/ads-mcp/meta
triggers:
  - meta ads
  - meta ads mcp
  - facebook ads
  - facebook ads mcp
  - instagram ads
  - meta ads manager
  - facebook ad set
  - meta ads report
  - meta ads api
---

# Meta Ads with AdKit

This skill tells you how to create, edit, and report on Facebook and Instagram ads through AdKit. It covers the steps. For what to build (objective, audience, creative, budget), read the `meta-ads-strategy` skill.

## Connect AdKit

AdKit is one MCP connector for Meta, Google, TikTok, LinkedIn, Microsoft, Reddit, X, and Pinterest ads.

- **Claude, ChatGPT, and most AI apps:** add a custom connector with the address `https://mcp.adkit.so`, then sign in.
- **Claude Code:** `claude mcp add --transport http adkit https://mcp.adkit.so`

For other AI apps, see how to set up the [AdKit MCP server for Meta Ads](https://adkit.so/features/ads-mcp/meta). If the AdKit tools are not available, tell the user how to connect. Then stop.

## What AdKit can do on Meta

| Entity        | Actions                                                        |
| ------------- | -------------------------------------------------------------- |
| `campaigns`   | list, get, create, update, delete                              |
| `adsets`      | list, get, create, update, delete                              |
| `ads`         | list, get, create, update, delete                              |
| `media`       | list, upload, delete (images and videos)                       |
| `research`    | interests (find interest IDs for targeting)                    |
| `lead-forms`  | list (existing Instant Forms of a Facebook Page)               |
| `conversions` | list (custom conversions and recent pixel events)              |
| `results`     | list (spend, impressions, clicks, conversions, ROAS)           |
| `accounts`    | list, available, connect, disconnect, update, pages, pixels    |
| `drafts`      | get, publish (review your changes, then send them)             |
| `creatives`   | create, update, delete (advanced; normal ads do not need this) |

## Steps

All calls go through `adkit_manage` with `platform: "meta"`. Before a call you have not made in this session, read its fields with `adkit_help({ path: "manage meta <entity> <action>" })`. Do not guess field names. In this skill, `campaigns` `create` means `entity: "campaigns"`, `action: "create"`.

1. **Project:** call `adkit_projects` and get the `projectId`. Every call needs it.
2. **Account:** call `adkit_status`. If no Meta account is connected, call `adkit_setup` with `platform: "meta"` and give the user the link. After they sign in, use `accounts` `available`, then `accounts` `connect`.
3. **Account defaults:** find the Facebook Page with `accounts` `pages` and the pixel with `accounts` `pixels`. Save them with `accounts` `update` (`defaultPageId`, `defaultPixelId`). To also run ads under an Instagram account, ask the user for its ID and save it as `defaultInstagramUserId`. This change applies immediately, with no draft.
4. **Build from the top down.** Each create saves a draft. For each level, do these steps before you start the next level:
   - Show the draft to the user (`drafts` `get`, or the link `https://app.adkit.so/manage/drafts?open=<draftId>`).
   - Wait for a yes. Then publish it with `drafts` `publish`.
   - Use the Meta ID that the publish result returns as the parent of the next level. A draft ID never works as a parent ID.

   The levels, in order:
   1. **Campaign:** `campaigns` `create` with a name, an objective, and `status: "paused"`. A paused campaign spends nothing.
   2. **Ad set:** `adsets` `create` with the `campaignId`, budget, optimization, and targeting. Use `research` `interests` to get interest IDs.
   3. **Media:** `media` `upload` from a public URL. It returns an `imageHash` or a `videoId`. For a local file: call `adkit_manage` with `entity: "media"` and `action: "request_upload_url"` (no platform). It returns an upload URL. Send the file to that URL with `PUT`. Then call `media` `upload` with `source: "temporary_upload"`.
   4. **Ad:** `ads` `create` with the `adsetId`, the copy, the URL, and the creative.

5. **Go live:** `campaigns` `update` with `status: "active"`. Publish that draft only after the user says yes. Then check with `adsets` `list` and `ads` `list` that the ad sets and ads are active too.
6. **Results:** `results` `list` with a `level` and a `period` or a date range (`from` and `to`).

## Meta rules

- The campaign objective limits which optimization goals the ad set can use.
- An ad takes one creative source: `media` (one image or video), `carouselCards`, `existingPostId` (promote an existing post), or `creativeId`. Use `ads`, not `creatives`, for normal ads. AdKit builds the creative.
- `campaigns`, `adsets`, and `ads` list actions return settings only. Spend and conversions come from `results`.
- `conversions` shows what is tracked, not how many conversions happened.
- Ads shown in the EU need beneficiary and payer details. Save them once with `accounts` `update` (`dsaDefaults`).
- Use AdKit field names (camelCase). The entities in the table above ignore raw Meta API field names.

## Anything else in the Meta API

For a Meta feature that AdKit does not cover, use `entity: "platform-api-request"` with `action: "mutate"`. The action is always `mutate`, also for reads. AdKit sends the request to the Meta Marketing API as it is. The user must turn on Advanced Platform Access in AdKit's Agent Permissions.

- Check every path and field in the [Meta Marketing API reference](https://developers.facebook.com/docs/marketing-api/reference).
- Read requests run immediately, with no draft. Writes save a draft, like any other change.
- After you use it, report the missing feature with `adkit_feedback`.

```json
{
  "projectId": "<projectId>",
  "entity": "platform-api-request",
  "action": "mutate",
  "data": {
    "platform": "meta",
    "accountId": "act_<accountId>",
    "endpoint": "act_<accountId>/campaigns",
    "method": "POST",
    "payload": {
      "name": "Test campaign",
      "objective": "OUTCOME_TRAFFIC",
      "status": "PAUSED",
      "special_ad_categories": []
    },
    "description": "Create a paused traffic campaign"
  }
}
```

## Other platforms

The same AdKit connector runs [Google Ads](https://adkit.so/features/ads-mcp/google), [TikTok Ads](https://adkit.so/features/ads-mcp/tiktok), [LinkedIn Ads](https://adkit.so/features/ads-mcp/linkedin), [Microsoft Ads](https://adkit.so/features/ads-mcp/microsoft), [Reddit Ads](https://adkit.so/features/ads-mcp/reddit), [X Ads](https://adkit.so/features/ads-mcp/x), and [Pinterest Ads](https://adkit.so/features/ads-mcp/pinterest) ads. Each platform has its own skill in this repo, for example `google-ads` and `tiktok-ads`.
