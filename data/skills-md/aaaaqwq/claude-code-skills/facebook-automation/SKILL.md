---
name: facebook-automation
description: "Automate Facebook tasks via Rube MCP (Composio): pages, posts, insights, comments, and ad accounts. Always search tools first for current schemas."
requires:
  mcp: [rube]
---

# Facebook Automation via Rube MCP

Automate Facebook operations through Composio's Facebook toolkit via Rube MCP.

## Prerequisites

- Rube MCP must be connected (RUBE_SEARCH_TOOLS available)
- Active Facebook connection via `RUBE_MANAGE_CONNECTIONS` with toolkit `facebook`
- Always call `RUBE_SEARCH_TOOLS` first to get current tool schemas

## Setup

**Get Rube MCP**: Add `https://rube.app/mcp` as an MCP server in your client configuration.

1. Verify Rube MCP is available by confirming `RUBE_SEARCH_TOOLS` responds
2. Call `RUBE_MANAGE_CONNECTIONS` with toolkit `facebook`
3. If connection is not ACTIVE, follow the returned auth link to complete Facebook OAuth
4. Confirm connection status shows ACTIVE before running any workflows

## Core Workflows

### 1. Page Management
- Search: `RUBE_SEARCH_TOOLS` with query "facebook page"
- List pages, get page details, update page info

### 2. Post Management
- Create posts (text, photo, video, link)
- Schedule posts for future publishing
- Edit and delete existing posts
- Get post insights and engagement metrics

### 3. Comments & Replies
- List comments on posts
- Reply to comments
- Hide/unhide comments
- Get comment insights

### 4. Page Insights
- Get page-level analytics (reach, engagement, followers)
- Post-level performance metrics
- Audience demographics

### 5. Ad Account (if available)
- List ad accounts
- Get campaign performance
- Manage ad sets and ads

## Tool Discovery Pattern

Always start with tool search:
```
RUBE_SEARCH_TOOLS query="facebook" toolkit="facebook"
```

Then use the exact tool names and schemas returned.

## Important Notes

- Facebook API has strict rate limits — batch operations when possible
- Page tokens expire; reconnect via RUBE_MANAGE_CONNECTIONS if auth fails
- Some features require Facebook Business verification
