---
name: build-product-integrations
description: Build apps that integrate with external services via Membrane. Use when the user wants to add integrations to their product — let their customers connect to Slack, HubSpot, Salesforce, GitHub, Google Sheets, Jira, or any other app, execute actions, sync data, or handle webhooks. Covers backend token generation, frontend connection UI, running actions, data collections, and AI agent tooling.
license: MIT
metadata:
  author: Membrane Inc
  version: '1.0.0'
  homepage: https://getmembrane.com
---

# App Integration

Build apps that integrate with external services via [Membrane](https://getmembrane.com). Uses the [Membrane](https://getmembrane.com) CLI.

Use this skill when you need to add third-party integrations to a product — connecting customers to external apps, running actions on their behalf, syncing data, or providing AI agent tools.

## How Membrane Works

Membrane is an integration engine. You define **what** your app needs (which external apps, what operations, what data) and Membrane handles authentication, API calls, and data transformation.

### Core Concepts

**Workspace** — your project in Membrane. Contains all integrations, connectors, and configuration for your product.

**Customer** — a user or organization in your product. Each customer gets their own set of connections and integration state. Identified by a unique ID you choose (e.g. your user/org ID).

**Connector** — a pre-built adapter for an external app (e.g. Slack, HubSpot). Handles authentication (OAuth, API keys), API client setup, and connection testing. Membrane has connectors for thousands of apps — if one doesn't exist, Membrane Agent can build it.

**Integration** — the relationship between your product and an external app. Defined in your workspace, it groups connectors, actions, data collections, and flows for a specific app.

**Connection** — an authenticated link between a customer and an external app. Created when a customer goes through the OAuth/auth flow. Contains credentials managed by Membrane.

**Action** — a single operation on a connected app (e.g. "Send message", "Create task", "List contacts"). Has typed `inputSchema` and `outputSchema`. Can be run via API or used as AI agent tools.

**Data Collection** — a consistent API for working with external app data like a database table. Supports list, find, search, create, update, delete operations.

**Flow** — multi-step async logic triggered by events, schedules, or API calls. Composed of trigger, function, and control nodes.

### Element Layers

Membrane elements exist at three layers:

1. **Universal** — work across multiple external apps (no specific integration). Example: a "Create Task" action that works with any task management app.
2. **Integration** — specific to one external app (has `integrationId`). Example: a "Create Jira Issue" action.
3. **Connection** — specific to a customer's connection (has `connectionId`). Can customize integration-level elements per customer.

Integration-level elements need implementations per integration. Connection-level elements can override/customize integration-level defaults.

### Authentication Architecture

Membrane uses JWT tokens for API access:

- **Workspace Key** — identifies your workspace (set as JWT `iss` claim)
- **Workspace Secret** — used to sign tokens (never expose to frontend)
- **Customer Token** — JWT containing workspace key + customer ID, generated on your backend, used by frontend SDKs and API calls

External app credentials (OAuth tokens, API keys) are managed by Membrane — your app never handles them directly.

## Standard Workflow: Search → Use → Delegate

Always follow this pattern when working with Membrane:

1. **Search for what you need** — use intent search to find actions, connectors, or integrations
2. **Use it if it exists** — run the action, connect with the connector, etc.
3. **Delegate to Membrane Agent if it doesn't exist** — create an agent session to build the missing element

Example: User wants to list Slack channels

```bash
# Step 1: Search for a "list channels" action
npx @membranehq/cli action list --connectionId <slack-conn-id> --intent "list channels" --limit 5 --json

# Step 2: If found, run it
npx @membranehq/cli action run <actionId> --connectionId <slack-conn-id> --json

# Step 3: If NOT found, delegate to Membrane Agent
npx @membranehq/cli agent-session create --agent action-building --message "Create an action to list Slack channels for connection <slack-conn-id>" --json
npx @membranehq/cli agent-session get <sessionId> --wait --json
# Then search again and run the newly created action
```

Example: User wants to add a new app (e.g. Notion)

```bash
# Step 1: Search for existing Notion connector
npx @membranehq/cli search notion --elementType connector --json

# Step 2: If found, create a connection
npx @membranehq/cli connect --connectorId <connectorId>

# Step 3: If NOT found, delegate to Membrane Agent
npx @membranehq/cli agent-session create --agent connection-building --message "Build a connector for Notion (https://notion.so)" --json
npx @membranehq/cli agent-session get <sessionId> --wait --json
# Then create a connection with the new connector
```

**This pattern applies to everything in Membrane.** When an element (action, connector, data collection, flow) doesn't exist, always delegate to Membrane Agent to build it — never try to build it yourself.

## Authentication

### For Development / CLI

Authenticate with the Membrane CLI for development and testing:

```bash
npx @membranehq/cli login --tenant
```

Alternatively, install globally (`npm i -g @membranehq/cli@latest`) and use `membrane login --tenant`.

Always use `--tenant` to get a tenant-scoped token — this authenticates on behalf of a specific tenant (workspace + customer), so you don't need to pass `--workspaceKey` and `--tenantKey` on every subsequent command.

This opens a browser or prints an authorization URL. The user authenticates in Membrane, then selects a workspace and tenant.

Credentials are stored in `~/.membrane/credentials.json`.

#### Non-interactive Authentication

If browser login is not available (remote/headless), the CLI prints an authorization URL. Ask the user to open it and enter the code they see:

```bash
npx @membranehq/cli login complete <code>
```

### For Production (Backend Token Generation)

In production, your backend generates JWT tokens per customer per request:

```javascript
import jwt from 'jsonwebtoken'

function generateMembraneToken(customerId, customerName) {
  return jwt.sign(
    {
      id: customerId,
      name: customerName,
    },
    process.env.MEMBRANE_WORKSPACE_SECRET,
    {
      issuer: process.env.MEMBRANE_WORKSPACE_KEY,
      expiresIn: '2h',
    },
  )
}
```

Create an endpoint on your backend (e.g. `/api/membrane-token`) that returns this token. The frontend SDK calls this to authenticate.

## Adding Integrations to Your App

There are three main ways to use Membrane in your app:

### Option A: JavaScript SDK (Frontend)

```bash
npm install @membranehq/sdk
```

```javascript
import { MembraneClient } from '@membranehq/sdk'

const membrane = new MembraneClient({
  fetchToken: async () => {
    const response = await fetch('/api/membrane-token')
    const { token } = await response.json()
    return token
  },
})

// List available integrations
const integrations = await membrane.integrations.find()

// Open connection UI (popup)
await membrane.ui.connect({ integrationKey: 'hubspot' })

// List customer's connections
const connections = await membrane.connections.find()

// Reconnect a disconnected connection
await membrane.ui.connect({ connectionId: 'conn_123' })

// Delete a connection
await membrane.connection('conn_123').archive()
```

### Option B: React SDK (Frontend)

```bash
npm install @membranehq/react
```

```jsx
import { MembraneProvider, useIntegrations, useConnections, useMembrane } from '@membranehq/react'

function App() {
  return (
    <MembraneProvider
      fetchToken={async () => {
        const res = await fetch('/api/membrane-token')
        const { token } = await res.json()
        return token
      }}
    >
      <IntegrationsPage />
    </MembraneProvider>
  )
}

function IntegrationsPage() {
  const { items: integrations, loading } = useIntegrations()
  const { items: connections } = useConnections()
  const membrane = useMembrane()

  const handleConnect = (integrationKey) => {
    membrane.ui.connect({ integrationKey })
  }

  // ... render integrations list with connect buttons
}
```

### Option C: REST API (Backend)

Use the Membrane API directly from your backend.

Base URL: `https://api.getmembrane.com` (or `https://api.integration.app`)
Auth: `Authorization: Bearer <token>`

```bash
# List integrations
GET /integrations

# List connections
GET /connections

# Create connection request (returns auth URL)
POST /connection-requests
{"connectorId": "<id>"}

# Check connection request status
GET /connection-requests/<id>

# List actions for a connection
GET /actions?connectionId=<id>

# Run an action
POST /actions/<id>/run?connectionId=<cid>
{"input": {"channel": "#general", "text": "Hello!"}}
```

### Connection UI

Membrane provides a pre-built connection UI that handles OAuth flows and credential collection:

```
https://ui.integration.app/embed/integrations/{INTEGRATION_KEY}/connect?token={TOKEN}
```

Use in an iframe or redirect. Optional query params:

- `redirectUri` — redirect back after connection
- `allowMultipleConnections=1` — allow multiple connections per integration
- `name` — pre-set connection name

For reconnecting disconnected connections:

```
https://ui.integration.app/embed/connections/{CONNECTION_ID}/refresh?token={TOKEN}
```

## Running Actions

Actions are operations on connected apps. Find and run them:

### Using CLI

```bash
# Search actions by intent
npx @membranehq/cli action list --connectionId abc123 --intent "send a message" --limit 10 --json

# Run an action
npx @membranehq/cli action run <actionId> --connectionId abc123 --input '{"channel": "#general", "text": "Hello!"}' --json
```

### Using API

```bash
# Search actions
GET /actions?connectionId=abc123&intent=send+a+message&limit=10

# Run action
POST /actions/<actionId>/run?connectionId=abc123
{"input": {"channel": "#general", "text": "Hello!"}}
```

Each action has:

- `id` — unique identifier
- `name`, `description` — what it does
- `inputSchema` — JSON Schema of accepted parameters
- `outputSchema` — JSON Schema of the return value

The result is in the `output` field of the response.

## AI Agent Tools

Membrane actions can serve as tools for AI agents. Two approaches:

### Static Tools (known toolset)

Use when you know which tools the agent needs before the session starts.

1. List connections: `GET /connections`
2. Get actions for connection: `GET /actions?connectionId=<id>`
3. Map to your agent's tool format:
   ```javascript
   const tools = actions.items.map((action) => ({
     id: action.id,
     name: action.name,
     description: action.description,
     inputSchema: action.inputSchema,
   }))
   ```
4. When agent calls a tool: `POST /actions/<id>/run?connectionId=<cid>` with `{"input": {...}}`

### Dynamic Tools (runtime discovery)

Use when tools depend on user intent or conversation context.

Search actions by natural language intent:

```bash
GET /actions?connectionId=abc123&intent=send+a+message
```

This uses semantic search to find the best matching actions.

### MCP Server

Membrane provides an official MCP server for AI agents:

```
https://mcp.integration.app/sse?token={TOKEN}&productKey={PRODUCT_KEY}
```

Works with Claude, Cursor, and any MCP-compatible agent.

## Working with Membrane Agent

Membrane Agent is an AI agent that builds integration elements (connectors, actions, data collections, flows) for you. **You should not build these yourself** — delegate to Membrane Agent instead.

### When to Use Membrane Agent

- A connector for an external app doesn't exist yet
- An action you need isn't available
- You need a data collection, flow, or other integration element
- You need to customize how an integration works

### Creating Agent Sessions

Use the CLI to create agent sessions:

```bash
npx @membranehq/cli agent-session create --agent <agentName> --message "<description>" --json
```

Available agent types:

- `connection-building` — builds connectors for external apps
- `action-building` — builds actions for connected apps
- `membrane` — general-purpose Membrane agent (can build any element)

### Agent Session Workflow

1. **Create a session** with a clear description of what you need:

   ```bash
   npx @membranehq/cli agent-session create --agent action-building --message "Create an action to send a message in a Slack channel for connection abc123" --json
   ```

2. **Poll until complete** — the agent works asynchronously:

   ```bash
   npx @membranehq/cli agent-session get <sessionId> --wait --json
   ```

   - `state: "busy"` — still working, poll again
   - `state: "idle"` — done with current request
   - `status: "completed"` — session finished
   - `summary` — description of what was done (available when idle)

3. **Send follow-ups** if needed:

   ```bash
   npx @membranehq/cli agent-session send <sessionId> --message "Also add support for thread replies" --json
   ```

4. **Abort** if something goes wrong:
   ```bash
   npx @membranehq/cli agent-session abort <sessionId> --json
   ```

### What to Delegate vs. What to Build

**Delegate to Membrane Agent:**

- Connectors (authentication, API clients, connection testing)
- Actions (API mappings, input/output schemas, implementation logic)
- Data Collections (field schemas, CRUD operations, pagination)
- Flows (multi-step automation, event handling, scheduling)
- External Events (webhook subscriptions, event parsing)
- Field Mappings (data transformation between apps)

**Build yourself:**

- Backend token generation endpoint
- Frontend UI for displaying integrations and connections
- Agent tool mapping (converting Membrane actions to your LLM's tool format)
- Business logic that uses Membrane actions/data
- Custom UI components for your integration experience

### Tips for Effective Agent Prompts

When creating agent sessions, provide:

- **Connection ID** — always include when building actions (`for connection abc123`)
- **App name and URL** — when building connectors (`Build a connector for Notion (https://notion.so)`)
- **Specific operation** — describe exactly what the action should do (`Create an action to list all tasks assigned to the current user`)
- **Input/output expectations** — what parameters should be accepted and what should be returned

### Building a Connector via Agent

If no connector exists for an app:

```bash
# Search first
npx @membranehq/cli search notion --elementType connector --json

# If not found, build one
npx @membranehq/cli agent-session create --agent connection-building --message "Build a connector for Notion (https://notion.so)" --json

# Poll for completion
npx @membranehq/cli agent-session get <sessionId> --wait --json

# After built, create a connection
npx @membranehq/cli connect --connectorId <connectorId>
```

### Building an Action via Agent

If the action you need doesn't exist:

```bash
# Search first
npx @membranehq/cli action list --connectionId abc123 --intent "create a task" --limit 10 --json

# If not found, build one
npx @membranehq/cli agent-session create --agent action-building --message "Create an action to create a task with title, description, and assignee for connection abc123" --json

# Poll for completion
npx @membranehq/cli agent-session get <sessionId> --wait --json

# Search again to get the action ID
npx @membranehq/cli action list --connectionId abc123 --intent "create a task" --limit 10 --json
```

## Troubleshooting

### Connection Issues

Check connection status:

```bash
npx @membranehq/cli connection get <connectionId> --json
```

Key fields:

- `disconnected: true` — credentials expired or revoked, needs reconnection
- `error` — details about what went wrong

Reconnect:

```bash
npx @membranehq/cli connect --connectionId <connectionId>
```

### Action Errors

When an action fails, the response includes error details. Common issues:

- **Missing required input** — check `inputSchema` for required fields
- **Connection disconnected** — reconnect before retrying
- **Rate limiting** — the external app is rate-limiting requests, retry after delay
- **Permission denied** — the connection's OAuth scope doesn't cover this operation

### Finding the Right Action

If `action list --intent` doesn't return what you need:

1. Try different phrasings of your intent
2. List all actions without intent filter: `npx @membranehq/cli action list --connectionId abc123 --json`
3. If the action doesn't exist, build it via Membrane Agent (see above)

## CLI Reference

All commands support `--json` for structured JSON output. Add `--workspaceKey <key>` and `--tenantKey <key>` to override defaults.

### connection

```bash
npx @membranehq/cli connection list [--json]                # List all connections
npx @membranehq/cli connection get <id> [--json]           # Get a connection by ID
```

### connect (interactive)

```bash
npx @membranehq/cli connect --connectorId <id>                    # Create connection via browser OAuth
npx @membranehq/cli connect --connectionId <id>                   # Reconnect existing connection
```

Opens a browser for authentication. Use `--non-interactive` to print the URL instead.

### connection-request

```bash
npx @membranehq/cli connection-request create [options] [--json]   # Create connection request
npx @membranehq/cli connection-request get <requestId> [--json]    # Check request status
```

Options: `--connectorId <id>`, `--integrationId <id>`, `--integrationKey <key>`, `--connectionId <id>` (reconnect), `--name <name>`

Status values: `pending`, `success`, `error`, `cancelled`

### action

```bash
npx @membranehq/cli action list [--connectionId <id>] [--intent <text>] [--limit <n>] [--json]   # List/search actions
npx @membranehq/cli action run <actionId> --connectionId <id> [--input <json>] [--json]           # Run an action
```

### search

```bash
npx @membranehq/cli search <query> [--elementType <type>] [--limit <n>] [--json]   # Search connectors, integrations, etc.
```

### agent-session

```bash
npx @membranehq/cli agent-session create --agent <agentName> --message <text> [--json]   # Create session
npx @membranehq/cli agent-session list [--json]                                          # List sessions
npx @membranehq/cli agent-session get <id> [--wait] [--timeout <seconds>] [--json]       # Get status
npx @membranehq/cli agent-session send <id> --message <text> [--json]                    # Send follow-up
npx @membranehq/cli agent-session abort <id> [--json]                                    # Abort session
npx @membranehq/cli agent-session messages <id> [--json]                                 # Get messages
```

## Fallback: Raw API

If the CLI is not available, make direct API requests.

Base URL: `https://api.getmembrane.com`
Auth header: `Authorization: Bearer $MEMBRANE_TOKEN`

| CLI Command                                                  | API Equivalent                                                      |
| ------------------------------------------------------------ | ------------------------------------------------------------------- |
| `connection list --json`                                     | `GET /connections`                                                  |
| `connection get <id> --json`                                 | `GET /connections/:id`                                              |
| `search <q> --json`                                          | `GET /search?q=<q>`                                                 |
| `connection-request create --connectorId <id> --json`        | `POST /connection-requests` with `{"connectorId": "<id>"}`          |
| `connection-request get <id> --json`                         | `GET /connection-requests/:id`                                      |
| `action list --connectionId <id> --intent <text> --json`     | `GET /actions?connectionId=<id>&intent=<text>`                      |
| `action run <id> --connectionId <cid> --input <json> --json` | `POST /actions/:id/run?connectionId=<cid>` with `{"input": <json>}` |
| `agent-session create --message <text> --json`               | `POST /agent/sessions` with `{"prompt": "<text>"}`                  |
| `agent-session get <id> --wait --json`                       | `GET /agent/sessions/:id?wait=true`                                 |
| `agent-session send <id> --message <text> --json`            | `POST /agent/sessions/:id/message` with `{"input": "<text>"}`       |
| `agent-session abort <id> --json`                            | `POST /agent/sessions/:id/interrupt`                                |

## External Endpoints

All requests go to the Membrane API. No other external services are contacted directly by this skill.

| Endpoint                        | Data Sent                                                             |
| ------------------------------- | --------------------------------------------------------------------- |
| `https://api.getmembrane.com/*` | Auth credentials, connection parameters, action inputs, agent prompts |

## Security & Privacy

- All data is sent to the Membrane API over HTTPS.
- CLI credentials are stored locally in `~/.membrane/` with restricted file permissions.
- Connection authentication (OAuth, API keys) is handled by Membrane — credentials for external apps are stored by the Membrane service, not locally.
- Action inputs and outputs pass through the Membrane API to the connected external app.
- Never expose your Workspace Secret to the frontend. Token generation must happen on your backend.

By using this skill, data is sent to [Membrane](https://getmembrane.com). Only install if you trust Membrane with access to your connected apps.