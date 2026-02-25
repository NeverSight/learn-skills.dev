---
name: stackone-connectors
description: Discover StackOne's 200+ connectors and 9,000+ actions across HRIS, ATS, CRM, LMS, ticketing, messaging, documents, IAM, and accounting. Use when user asks "which providers does StackOne support", "what can I do with BambooHR", "recommend an integration for HR", "what actions are available", "how do I call a provider-specific action", or "does StackOne support Workday". Helps choose the right connector and actions for any use case. Do NOT use for building agents (use stackone-agents) or connecting accounts (use stackone-connect).
license: MIT
compatibility: Requires network access to fetch live documentation from docs.stackone.com
metadata:
  author: stackone
  version: "2.0"
---

# StackOne Connectors — Integration Discovery

## Important

Connector availability changes frequently as StackOne adds new providers. Before answering:
1. Fetch `https://docs.stackone.com/connectors/introduction` for the current connector list
2. For specific provider capabilities, fetch the relevant category API reference

Never assume a connector exists or doesn't exist without checking live docs.

## Instructions

### Step 1: Identify the user's integration need

Common patterns:
- **"What providers do you support for X?"** → Check the category (HRIS, ATS, CRM, etc.) in the connectors page
- **"Can I do Y with provider Z?"** → Check the provider's supported actions in the API reference
- **"Recommend an integration for my use case"** → Match the use case to a category, then list available providers

### Step 2: Look up connector availability

Fetch `https://docs.stackone.com/connectors/introduction` for the full, current list.

Consult `references/category-overview.md` for a snapshot of categories and example providers. But always verify against live docs since new connectors are added regularly.

### Step 3: Check available actions for a provider

Each connector exposes its own set of provider-specific actions. Action counts vary significantly — Salesforce has 370+ actions, HubSpot has 100+, while smaller providers may have a handful.

To find what's available for a specific provider:
1. Fetch `https://docs.stackone.com/connectors/introduction`
2. Find the provider and check its listed actions
3. For action details, fetch `https://docs.stackone.com/platform/api-reference/actions/make-an-rpc-call-to-an-action`

Actions are named `{provider}_{operation}_{entity}` (e.g., `bamboohr_list_employees`, `salesforce_get_contact`).

### Step 4: Execute actions via the Actions API

All actions are executed through StackOne's Actions API:

```bash
curl -X POST https://api.stackone.com/actions/rpc \
  -H "Authorization: Basic $(echo -n 'YOUR_API_KEY:' | base64)" \
  -H "x-account-id: ACCOUNT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "bamboohr_list_employees"
  }'
```

AI agents typically call actions via the SDK or MCP rather than raw API calls — see the `stackone-agents` skill for SDK/MCP integration.

Fetch `https://docs.stackone.com/platform/api-reference/actions/make-an-rpc-call-to-an-action` for the full RPC reference.

### Step 5: Test before building

- **AI Playground**: https://app.stackone.com/playground — test API calls interactively
- **MCP Inspector**: `npx @modelcontextprotocol/inspector https://api.stackone.com/mcp` — test via MCP
- **Postman**: importable collection available from the docs

## Release stages

| Stage | Meaning | Recommendation |
|-------|---------|----------------|
| **GA** | Production-ready, fully supported | Safe for production |
| **Beta** | Stable for testing, minor changes possible | OK for non-critical flows |
| **Preview** | Early-stage, expect breaking changes | Development/testing only |

## Examples

### Example 1: User wants to know what HR integrations are available

User says: "Which HRIS tools does StackOne support?"

Actions:
1. Fetch `https://docs.stackone.com/connectors/introduction`
2. Filter for the HRIS category
3. List available providers with their release stages and action counts
4. For specific providers the user is interested in, list their available actions

Result: Current list of HRIS connectors with per-provider action counts.

### Example 2: User wants to know what they can do with a specific provider

User says: "What can I do with BambooHR through StackOne?"

Actions:
1. Fetch `https://docs.stackone.com/connectors/introduction` and find BambooHR
2. List the available actions (e.g., `bamboohr_list_employees`, `bamboohr_get_employee`, etc.)
3. Explain the Actions API for executing them, or recommend using the SDK/MCP for agent integration
4. Fetch the Actions RPC reference for payload details if they need the raw API

Result: Full list of BambooHR actions with how to call them.

### Example 3: User needs a connector that doesn't exist

User says: "Does StackOne support our custom HR tool?"

Actions:
1. Check the connectors page — it may exist under a different name
2. If not found, explain two options:
   a. Request it: `https://docs.stackone.com/connectors/add-new`
   b. Build it: use the Connector Engine (see `stackone-cli` skill)
3. If they have budget/urgency, recommend the AI Builder for faster custom connector development

Result: Clear path forward — either request or build.

## Troubleshooting

### Can't find a specific provider
**Cause**: Provider may be listed under a different name, or may not be supported yet.
- Search the connectors page by the provider's official name
- Check if it's under a parent company name (e.g., "Microsoft Entra ID" not "Azure AD")
- If not found, suggest requesting it or building a custom connector

### Action returns "not supported" for a provider
**Cause**: The requested action doesn't exist for this provider.
- Each provider has its own set of actions — check the connectors page for what's available
- Action names include the provider prefix (e.g., `bamboohr_list_employees` not `list_employees`)
- Some actions require specific OAuth scopes on the provider side

### Connector logos not loading
**Cause**: Incorrect slug format.
- Logo URL format: `https://stackone-logos.com/api/{connector-slug}/filled/png`
- Slugs are lowercase, hyphenated (e.g., `bamboo-hr`, `google-drive`)
- Fetch the connectors page to verify the exact slug
