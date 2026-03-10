---
name: no-code-pipelines
description: "Generates importable n8n workflow JSON files that sync data between Personize and 400+ apps. Produces ready-to-import workflows for batch sync, webhook ingestion, per-record AI enrichment, and data export — no code required. Use this skill whenever the user wants no-code integrations, visual workflows, n8n automation, or to connect Personize to HubSpot, Salesforce, Google Sheets, Slack, Postgres, or any app without writing code. Also trigger when they mention 'workflow automation', 'scheduled sync without code', 'visual pipeline', or 'connect Personize to [app]' and don't want to write TypeScript."
license: Apache-2.0
compatibility: "Requires an n8n instance (cloud or self-hosted) and a Personize API key (sk_live_...)"
metadata: {"author": "personize-ai", "version": "1.0", "homepage": "https://personize.ai", "openclaw": {"emoji": "\U0001F504", "requires": {"env": ["PERSONIZE_SECRET_KEY"]}}}
---

# Skill: No-Code Pipelines

Generate importable n8n workflow JSON files that sync data between Personize and 400+ apps. The user describes their source/destination and you produce ready-to-import `.json` files they paste into n8n.

---

## When to Use This Skill

- User wants to connect Personize to HubSpot, Salesforce, Google Sheets, Slack, Postgres, or any app with an API
- User asks for "no-code" or "n8n" or "workflow automation" integration
- User wants scheduled syncs without writing code
- User needs webhook-triggered data flows

---

## When NOT to Use This Skill

- Want TypeScript/SDK code you can test and version → use **entity-memory** (CRM sync section)
- Need durable pipelines with retries, waits, and complex orchestration → use **code-pipelines**
- Only need a single API call → use **entity-memory** directly

---

## Prerequisites

- An n8n instance (cloud or self-hosted)
- A Personize secret key (`sk_live_...`) configured as an **HTTP Header Auth** credential in n8n:
  - **Name:** `Authorization`
  - **Value:** `Bearer sk_live_...`
  - **Credential name:** `Personize API Key` (referenced in all templates)

---

## Personize API Endpoints for n8n

All requests go to `https://agent.personize.ai` with `Authorization: Bearer sk_live_...` header.

| Action | Method | Path | Use Case |
|--------|--------|------|----------|
| Batch sync in (structured + AI) | POST | `/api/v1/batch-memorize` | Sync CRM records into Personize with per-property AI control |
| Single memorize (AI) | POST | `/api/v1/memorize` | Store one content item with AI extraction + vectors |
| Structured upsert | POST | `/api/v1/upsert` | Store properties without AI extraction |
| Semantic search | POST | `/api/v1/smart-recall` | Search memories by meaning |
| Export/filter records | POST | `/api/v1/search` | Query records by property conditions |
| Entity context digest | POST | `/api/v1/smart-memory-digest` | Get compiled context for an entity |
| Smart context | POST | `/api/v1/ai/smart-guidelines` | Get relevant variables for a message |
| Auth check | GET | `/api/v1/me` | Verify key and read plan limits |

---

## n8n Workflow JSON Structure

Every workflow is a JSON object with `nodes`, `connections`, and `settings`. Users import it via **Menu > Import from File** or **Ctrl+V** paste into the n8n canvas.

```json
{
  "name": "Workflow Name",
  "nodes": [ /* array of node objects */ ],
  "connections": { /* source node name → target connections */ },
  "settings": { "executionOrder": "v1" }
}
```

### Constraints

> Keywords follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119): **MUST** = non-negotiable, **SHOULD** = strong default (override with stated reasoning), **MAY** = agent discretion.

1. **MUST** use unique node names -- because node names serve as connection keys in the `connections` object; duplicates cause wiring failures on import.
2. **MUST** set `"settings": { "executionOrder": "v1" }` -- because omitting it causes non-deterministic node execution order in n8n.
3. **MUST** reference credentials by the display name the user created in n8n -- because n8n resolves credentials by name, not by ID; mismatched names cause auth failures on import.
4. **SHOULD** space nodes ~220px horizontally in position values `[x, y]` -- because consistent spacing produces readable canvas layouts that users can navigate without rearranging.
5. **SHOULD** use UUID-like strings for node IDs (e.g., `"pz-sync-001"`) -- because predictable IDs simplify debugging and log correlation.
6. **MUST** connect Loop Over Items output 0 to the loop body and output 1 to the post-loop node -- because reversed connections cause infinite loops or skipped processing.

---

## Common Node Reference

| Node | `type` | `typeVersion` |
|------|--------|---------------|
| Schedule Trigger | `n8n-nodes-base.scheduleTrigger` | `1.1` |
| Manual Trigger | `n8n-nodes-base.manualTrigger` | `1` |
| Webhook | `n8n-nodes-base.webhook` | `2` |
| HTTP Request | `n8n-nodes-base.httpRequest` | `4.2` |
| Loop Over Items | `n8n-nodes-base.splitInBatches` | `3` |
| Code (JavaScript) | `n8n-nodes-base.code` | `2` |
| IF | `n8n-nodes-base.if` | `2` |
| Set / Edit Fields | `n8n-nodes-base.set` | `3.4` |
| No Operation | `n8n-nodes-base.noOp` | `1` |
| HubSpot | `n8n-nodes-base.hubspot` | `2` |
| Salesforce | `n8n-nodes-base.salesforce` | `1` |
| Google Sheets | `n8n-nodes-base.googleSheets` | `4.5` |
| Slack | `n8n-nodes-base.slack` | `2.2` |
| Postgres | `n8n-nodes-base.postgres` | `2.5` |
| MySQL | `n8n-nodes-base.mySql` | `2.4` |

---

## HTTP Request Node Pattern for Personize

All Personize API calls use the same HTTP Request node pattern:

```json
{
  "id": "pz-api-001",
  "name": "Personize: Batch Memorize",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [860, 300],
  "parameters": {
    "method": "POST",
    "url": "https://agent.personize.ai/api/v1/batch-memorize",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "httpHeaderAuth",
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "={{ JSON.stringify($json.payload) }}",
    "options": {
      "response": { "response": { "fullResponse": true } }
    }
  },
  "credentials": {
    "httpHeaderAuth": {
      "id": "pz-cred",
      "name": "Personize API Key"
    }
  }
}
```

### Expression Syntax

- `{{ $json.fieldName }}` — field from previous node
- `{{ $('Node Name').item.json.field }}` — field from a specific node
- `{{ JSON.stringify($json) }}` — entire previous output as JSON string
- `={{ expression }}` — prefix for expression mode in parameter values

---

## Workflow Pattern 1: Sync IN (Source App → Personize)

**Flow:** `[Trigger] → [Fetch Records] → [Build Payload] → [Batch Memorize] → [Done]`

For sources that return many records, use the **batch-memorize** endpoint which handles both structured storage and AI extraction in one call.

### When to use Loop Over Items vs. Single Call

- **Single `batch-memorize` call (preferred):** When the source returns all rows at once and total rows < 500. The Code node builds the entire `{ source, mapping, rows }` payload and one HTTP Request sends it.
- **Loop Over Items with chunking:** When source returns thousands of rows. Split into chunks of 50-100, send each chunk as a separate `batch-memorize` call with a Wait node for rate limits.

### Code Node: Build batch-memorize Payload

This Code node transforms source records into the Personize `batch-memorize` payload:

```javascript
// Input: array of source records from previous node
const items = $input.all();

const rows = items.map(item => item.json);

const payload = {
  source: 'n8n-sync',
  mapping: {
    entityType: 'contact',
    email: 'email',           // source field name containing email
    runName: 'n8n-sync-' + Date.now(),
    properties: {
      // Structured fields — stored directly
      email:      { sourceField: 'email',      collectionId: 'YOUR_COL_ID', collectionName: 'Contacts Standard Schema' },
      first_name: { sourceField: 'firstname',  collectionId: 'YOUR_COL_ID', collectionName: 'Contacts Standard Schema' },
      last_name:  { sourceField: 'lastname',   collectionId: 'YOUR_COL_ID', collectionName: 'Contacts Standard Schema' },
      company:    { sourceField: 'company',    collectionId: 'YOUR_COL_ID', collectionName: 'Contacts Standard Schema' },
      // AI extraction fields — extractMemories: true
      notes: {
        sourceField: 'notes',
        collectionId: 'YOUR_GEN_COL_ID',
        collectionName: 'Generated Content',
        extractMemories: true,
      },
    },
  },
  rows: rows,
  chunkSize: 1,
};

return [{ json: { payload } }];
```

**Important:** Replace `YOUR_COL_ID` and `YOUR_GEN_COL_ID` with actual collection IDs. The user can find these by calling `GET /api/v1/collections` or using `client.collections.list()` from the SDK.

### Per-Property `extractMemories` Decision

> **Rule of thumb:** Set `extractMemories: true` on free-form text (notes, transcripts, emails). Omit it for structured fields (email, name, dates, counts). See the `entity-memory` skill's `reference/memorize.md` for the complete decision table and examples.

---

## Workflow Pattern 2: Sync OUT (Personize → Destination App)

**Flow:** `[Trigger] → [Export from Personize] → [Loop Over Items] → [Push to Destination] → [Done]`

Use the **export** endpoint to query records by filters, then push each to the destination.

### Code Node: Build Export Query

```javascript
return [{
  json: {
    groups: [{
      id: 'g1',
      logic: 'AND',
      conditions: [
        { property: 'company', operator: 'IS_SET' }
      ]
    }],
    type: 'Contact',
    returnRecords: true,
    pageSize: 100,
    includeMemories: false
  }
}];
```

### Export Filter Operators

| Operator | Description |
|---|---|
| `EQ` | Equals |
| `NEQ` | Not equals |
| `CONTAINS` | Contains substring |
| `GT` / `LT` | Greater / less than |
| `IS_SET` | Field has a value |
| `IS_NOT_SET` | Field is empty |
| `IN` | Value in array |

---

## Workflow Pattern 3: Per-Record AI Enrichment

**Flow:** `[Trigger] → [Fetch Record] → [Smart Digest] → [AI Prompt] → [Push Result]`

Use `smart-memory-digest` to compile all known context for a contact, then feed it to the Personize prompt API for AI-generated content.

### Code Node: Build Smart Digest Request

```javascript
const email = $json.email;
return [{
  json: {
    email: email,
    type: 'Contact',
    token_budget: 2000,
    include_properties: true,
    include_memories: true
  }
}];
```

### Code Node: Build AI Prompt Request

```javascript
const context = $('Personize: Smart Digest').item.json.data.compiledContext;
const email = $('Personize: Smart Digest').item.json.data.properties?.email || '';

return [{
  json: {
    prompt: `Using the context below, write a personalized outreach email for ${email}.\n\nContext:\n${context}`,
    model: 'claude-sonnet-4-6'
  }
}];
```

---

## Workflow Pattern 4: Webhook → Memorize (Real-time Sync)

**Flow:** `[Webhook] → [Transform] → [Memorize Pro] → [Respond]`

For real-time data capture — CRM webhooks, form submissions, Zapier/Make triggers.

### Webhook Node

```json
{
  "id": "pz-webhook-001",
  "name": "Webhook",
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 2,
  "position": [200, 300],
  "parameters": {
    "path": "personize-ingest",
    "httpMethod": "POST",
    "responseMode": "lastNode"
  }
}
```

### Code Node: Build memorize_pro Payload

```javascript
const data = $json.body || $json;
return [{
  json: {
    content: `Name: ${data.name}\nEmail: ${data.email}\nCompany: ${data.company}\nNotes: ${data.notes || ''}`,
    speaker: data.source || 'webhook',
    enhanced: true,
    tags: ['webhook', 'real-time'],
    email: data.email
  }
}];
```

---

## Rate Limit Handling in n8n

Personize returns HTTP 429 when rate limited. Handle this in n8n:

### Option A: Retry on Fail (Recommended)

Set on the HTTP Request node:
```json
{
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 60000
}
```

### Option B: Wait Node Between Batches

Add a **Wait** node (type `n8n-nodes-base.wait`) after each batch call:
```json
{
  "id": "pz-wait-001",
  "name": "Rate Limit Wait",
  "type": "n8n-nodes-base.wait",
  "typeVersion": 1.1,
  "position": [1080, 300],
  "parameters": {
    "amount": 62,
    "unit": "seconds"
  }
}
```

Always call `GET /api/v1/me` first to read the actual limits for the user's plan.

---

## Building a Workflow: Step-by-Step

When the user asks for an n8n workflow, follow these steps:

### Step 1: Identify the direction

- **Sync IN** = data flows into Personize (use `batch-memorize` or `memorize_pro`)
- **Sync OUT** = data flows out of Personize (use `export` or `recall_pro` or `smart-memory-digest`)
- **Bidirectional** = combine both patterns in one workflow

### Step 2: Choose the trigger

- **Schedule** — for periodic batch syncs (hourly, daily)
- **Webhook** — for real-time event-driven ingestion
- **Manual** — for testing and one-time imports

### Step 3: Choose source/destination nodes

If n8n has a built-in node for the app (HubSpot, Salesforce, Google Sheets, Slack, Postgres), use it. Otherwise, use the HTTP Request node.

### Step 4: Build the mapping

Ask the user which fields to sync. For each field, determine:
- The source field name (from the source app)
- The target property name (in Personize)
- Whether it needs AI extraction (`extractMemories: true`)

### Step 5: Generate the workflow JSON

Use the templates in `templates/` as starting points. Customize:
- Node names (descriptive of the actual source/destination)
- API URLs and endpoints
- Code node logic for field mapping
- Credential references
- Schedule interval

### Step 6: Add error handling

- Set `retryOnFail: true` on all HTTP Request nodes hitting Personize
- Add Wait nodes between batches if syncing > 50 records
- Optionally add an IF node after the API call to check `{{ $json.success }}` and handle errors

### Step 7: Output the JSON

Save the workflow JSON to a `.json` file. Tell the user to:
1. Open n8n
2. Create a new workflow
3. Menu > Import from File (or Ctrl+V to paste)
4. Create the **Personize API Key** credential (Header Auth with `Authorization: Bearer sk_live_...`)
5. Create credentials for the source/destination app
6. Test with Manual Trigger first, then activate the Schedule Trigger

---

## Template Workflows

Ready-to-customize templates are in the `templates/` folder:

| Template | File | Description |
|---|---|---|
| HubSpot → Personize | `templates/hubspot-to-personize.json` | Sync HubSpot contacts into Personize memory |
| Personize → Slack | `templates/personize-to-slack.json` | Export records and post digest to Slack channel |
| Webhook → Personize | `templates/webhook-to-personize.json` | Real-time ingest from any webhook source |
| Google Sheets → Personize | `templates/gsheets-to-personize.json` | Batch import rows from a Google Sheet |

Each template is a complete, importable n8n workflow JSON with placeholder credentials.

---

## n8n App Integrations (400+)

n8n has built-in nodes for these categories — use them instead of HTTP Request when available:

| Category | Apps |
|---|---|
| CRM | HubSpot, Salesforce, Pipedrive, Zoho CRM |
| Spreadsheets | Google Sheets, Airtable, Microsoft Excel |
| Communication | Slack, Microsoft Teams, Discord, Telegram, Email (SMTP/IMAP) |
| Project Mgmt | Jira, Asana, Trello, Monday.com, Notion, Linear |
| Databases | Postgres, MySQL, MongoDB, Redis |
| Dev Tools | GitHub, GitLab |
| Marketing | Mailchimp, SendGrid, ActiveCampaign |
| E-Commerce | Shopify, Stripe, WooCommerce |
| Cloud | AWS S3/SES/Lambda, Google Cloud |
| AI | OpenAI, Anthropic Claude, Google Gemini |

For any app not listed, use the **HTTP Request** node with the app's REST API.

---

## Reference Documentation & Search Queries

For n8n official docs URLs, app-specific node docs, trigger node docs, community templates, suggested search queries, and version notes — see [reference/n8n-reference.md](reference/n8n-reference.md).
