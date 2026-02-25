---
name: stackone-platform
description: Manage StackOne resources including API keys, linked accounts, logs, and webhooks. Use when user asks to "set up StackOne", "list my accounts", "debug API errors", "check integration status", or "configure webhooks". Covers authentication, account management, and troubleshooting. Do NOT use for building AI agents (use stackone-agents) or discovering connector capabilities (use stackone-connectors).
license: MIT
compatibility: Requires network access to fetch live documentation from docs.stackone.com
metadata:
  author: stackone
  version: "2.0"
---

# StackOne Platform

## Important

Before answering platform questions, fetch the latest documentation:
1. Fetch `https://docs.stackone.com/llms.txt` to discover all available doc pages
2. Fetch the specific page relevant to the user's question

Do not guess or rely on potentially outdated information in this skill. Always verify against live docs.

## Instructions

### Step 1: Identify what the user needs

StackOne is integration infrastructure for AI agents — 200+ connectors and 10,000+ production-ready actions across HR, ATS, CRM, LMS, and more. Agents reason, StackOne executes. Common tasks:

- **Setting up**: Creating API keys, understanding auth
- **Managing accounts**: Listing linked accounts, checking status, debugging connections
- **API calls**: Making requests to StackOne endpoints, understanding headers
- **Webhooks**: Subscribing to account lifecycle events
- **Debugging**: Investigating failed requests, auth errors, rate limits

### Step 2: Authentication

All API calls require Basic auth. The API key goes in the Authorization header:

```bash
curl https://api.stackone.com/accounts \
  -H "Authorization: Basic $(echo -n 'YOUR_API_KEY:' | base64)"
```

Key details:
- API keys are created at https://app.stackone.com
- Key format: `v1.{region}.xxxxx`
- The `x-account-id` header is required for data API calls — it identifies which linked account to query
- A **linked account** = a connection between your customer and a third-party provider (e.g., BambooHR)
- For how AI agents call StackOne actions (via SDK, MCP, or A2A), see the `stackone-agents` skill

### Step 3: Account management

Each linked account has:
- `id` — assigned by StackOne
- `provider` — the SaaS tool (e.g., `bamboohr`, `greenhouse`)
- `origin_owner_id` — your internal customer identifier
- `status` — `active`, `error`, `inactive`

To list accounts: `GET https://api.stackone.com/accounts`
To get one account: `GET https://api.stackone.com/accounts/{id}`

Fetch the accounts API reference for full details:
`https://docs.stackone.com/platform/api-reference/accounts/list-accounts`

### Step 4: Fetch API docs as needed

Consult `references/api-categories.md` for the StackOne API structure (Actions API, Platform API) and connector category documentation URLs.

## Examples

### Example 1: User wants to check their linked accounts

User says: "How do I see which accounts are connected in StackOne?"

Actions:
1. Confirm they have an API key (created at https://app.stackone.com)
2. Show the curl command: `GET https://api.stackone.com/accounts` with proper auth header
3. Explain the response fields: `id`, `provider`, `status`, `origin_owner_id`
4. Fetch `https://docs.stackone.com/platform/api-reference/accounts/list-accounts` for the full schema

Result: Working command with explanation of account statuses and how to use account IDs.

### Example 2: User wants to debug a failing integration

User says: "My StackOne API call is returning 401"

Actions:
1. Check if their API key is correctly base64-encoded (common mistake: forgetting the trailing colon)
2. Verify the key hasn't been revoked in the dashboard
3. If they get 200 on `/accounts` but fail on data endpoints, check that `x-account-id` is present and valid
4. Fetch `https://docs.stackone.com/overview/authentication` for the latest auth details

Result: Identified root cause with fix.

## Troubleshooting

### Error: 401 Unauthorized
**Cause**: Invalid or missing API key.
- Verify the key format is `v1.{region}.xxxxx`
- The Authorization header must be `Basic base64(api_key:)` — note the trailing colon before encoding
- Check the key is active at https://app.stackone.com

### Error: 400 Bad Request with "account not found"
**Cause**: The `x-account-id` header references a non-existent or disconnected account.
- List accounts with `GET /accounts` to find valid IDs
- Check the account status — it may be `error` or `inactive`

### Error: 429 Too Many Requests
**Cause**: Rate limit exceeded.
- StackOne applies rate limits per API key
- Implement exponential backoff
- Fetch `https://docs.stackone.com/overview/rate-limits` for current limits

### API calls return empty data
**Cause**: The linked account may have limited permissions on the provider side.
- Verify the provider credentials have the right scopes
- Check the account status in the dashboard
- Some providers require additional setup (API tokens, OAuth scopes)

## Key URLs

| Resource | URL |
|----------|-----|
| Dashboard | https://app.stackone.com |
| API base | https://api.stackone.com |
| Documentation | https://docs.stackone.com |
| Docs index | https://docs.stackone.com/llms.txt |
