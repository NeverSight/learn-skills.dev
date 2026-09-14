---
name: keyid-agent-kit-mcp
description: Give AI agents (Claude, Cursor) a real email address with 27 MCP tools for inbox, send, reply, contacts, search, and more via KeyID.ai
triggers:
  - "give claude an email address"
  - "add email tools to my AI agent"
  - "set up MCP email for Claude Desktop"
  - "let my agent send and receive email"
  - "configure keyid agent kit"
  - "add email powers to cursor"
  - "MCP email server setup"
  - "AI agent email integration"
---

# KeyID Agent Kit — MCP Email Tools for AI Agents

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

KeyID Agent Kit gives AI agents (Claude, Cursor, or any MCP client) a real, working email address with 27 tools via the Model Context Protocol. No signup, no API keys to acquire manually, no cost. Powered by [KeyID.ai](https://keyid.ai).

## What It Does

- Provisions a real email address for your AI agent automatically
- Exposes 27 MCP tools: send, receive, reply, forward, search, contacts, drafts, webhooks, auto-reply, signatures, forwarding rules, metrics
- Runs as a stdio MCP server — compatible with Claude Desktop, Cursor, and any MCP client
- Uses Ed25519 keypairs for identity — auto-generated if not provided

## Installation

```bash
npm install @keyid/agent-kit
# or
yarn add @keyid/agent-kit
# or run directly without installing
npx @keyid/agent-kit
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `KEYID_PUBLIC_KEY` | Ed25519 public key (hex) | Auto-generated on first run |
| `KEYID_PRIVATE_KEY` | Ed25519 private key (hex) | Auto-generated on first run |
| `KEYID_BASE_URL` | API base URL | `https://keyid.ai` |

**Important:** Save the auto-generated keys after first run so your agent keeps the same email address across sessions. The keys are printed to stderr on first launch.

### Claude Desktop Setup

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "keyid": {
      "command": "npx",
      "args": ["@keyid/agent-kit"],
      "env": {
        "KEYID_PUBLIC_KEY": "$KEYID_PUBLIC_KEY",
        "KEYID_PRIVATE_KEY": "$KEYID_PRIVATE_KEY"
      }
    }
  }
}
```

### Cursor Setup

In `.cursor/mcp.json` at project root or global Cursor settings:

```json
{
  "mcpServers": {
    "keyid": {
      "command": "npx",
      "args": ["@keyid/agent-kit"],
      "env": {
        "KEYID_PUBLIC_KEY": "$KEYID_PUBLIC_KEY",
        "KEYID_PRIVATE_KEY": "$KEYID_PRIVATE_KEY"
      }
    }
  }
}
```

### First Run — Get Your Email Address

```bash
# Run once to generate keys and register the agent
npx @keyid/agent-kit
# Keys are printed to stderr — save them!
# Then set them in your environment or config
export KEYID_PUBLIC_KEY=<hex-from-output>
export KEYID_PRIVATE_KEY=<hex-from-output>
```

## All 27 Tools Reference

### Identity & Auth
```
keyid_provision     — Register agent, get assigned email address
keyid_get_email     — Get the current active email address
```

### Messages
```
keyid_get_inbox          — Fetch inbox; supports search query, filtering, pagination
keyid_send               — Send email (to, subject, body, HTML, scheduled time, display name)
keyid_reply              — Reply to a message by message_id
keyid_forward            — Forward a message to another address
keyid_update_message     — Mark read/unread, star/unstar
keyid_get_unread_count   — Get count of unread messages
```

### Threads & Drafts
```
keyid_list_threads   — List conversation threads
keyid_get_thread     — Get a thread with all its messages
keyid_create_draft   — Save a draft
keyid_send_draft     — Send a previously saved draft
```

### Settings
```
keyid_get_auto_reply   — Get current auto-reply/vacation responder config
keyid_set_auto_reply   — Enable/disable auto-reply with custom message
keyid_get_signature    — Get email signature
keyid_set_signature    — Set email signature text/HTML
keyid_get_forwarding   — Get forwarding rules
keyid_set_forwarding   — Add or update forwarding to another address
```

### Contacts
```
keyid_list_contacts    — List all saved contacts
keyid_create_contact   — Create a contact (name, email, notes)
keyid_delete_contact   — Delete a contact by ID
```

### Webhooks
```
keyid_list_webhooks           — List configured webhooks
keyid_create_webhook          — Register a webhook URL for inbound events
keyid_get_webhook_deliveries  — View delivery history and failures
```

### Lists & Metrics
```
keyid_manage_list   — Add/remove addresses from allow or blocklist
keyid_get_metrics   — Query usage metrics (sent, received, bounces)
```

## Real Code Examples

### Programmatic MCP Client (Node.js)

```javascript
import { spawn } from 'child_process';
import { createInterface } from 'readline';

// Start the MCP server as a child process
const server = spawn('npx', ['@keyid/agent-kit'], {
  env: {
    ...process.env,
    KEYID_PUBLIC_KEY: process.env.KEYID_PUBLIC_KEY,
    KEYID_PRIVATE_KEY: process.env.KEYID_PRIVATE_KEY,
  },
  stdio: ['pipe', 'pipe', 'inherit'],
});

// Send a JSON-RPC request
function sendRequest(method, params = {}) {
  const request = {
    jsonrpc: '2.0',
    id: Date.now(),
    method,
    params,
  };
  server.stdin.write(JSON.stringify(request) + '\n');
}

// Read responses
const rl = createInterface({ input: server.stdout });
rl.on('line', (line) => {
  const response = JSON.parse(line);
  console.log('Response:', JSON.stringify(response, null, 2));
});

// Initialize MCP session
sendRequest('initialize', {
  protocolVersion: '2024-11-05',
  capabilities: {},
  clientInfo: { name: 'my-app', version: '1.0.0' },
});
```

### Call a Tool via MCP JSON-RPC

```javascript
// After initialization, call tools/call
function callTool(toolName, toolArgs) {
  const request = {
    jsonrpc: '2.0',
    id: Date.now(),
    method: 'tools/call',
    params: {
      name: toolName,
      arguments: toolArgs,
    },
  };
  server.stdin.write(JSON.stringify(request) + '\n');
}

// Get inbox
callTool('keyid_get_inbox', { limit: 10 });

// Send an email
callTool('keyid_send', {
  to: 'colleague@example.com',
  subject: 'Hello from my AI agent',
  body: 'This email was sent by an AI agent using KeyID.',
});

// Reply to a message
callTool('keyid_reply', {
  message_id: 'msg_abc123',
  body: 'Thanks, I will review this today.',
});

// Search inbox
callTool('keyid_get_inbox', {
  query: 'from:alice@company.com subject:report',
  unread_only: true,
});

// Set auto-reply
callTool('keyid_set_auto_reply', {
  enabled: true,
  subject: 'Out of Office',
  body: 'I am currently unavailable. My AI agent will respond shortly.',
});

// Create a contact
callTool('keyid_create_contact', {
  name: 'Alice Smith',
  email: 'alice@company.com',
  notes: 'Project lead for Q1 initiative',
});

// Schedule an email
callTool('keyid_send', {
  to: 'team@company.com',
  subject: 'Weekly Update',
  body: 'Here is the weekly status...',
  scheduled_at: '2026-03-25T09:00:00Z',
});

// Set email signature
callTool('keyid_set_signature', {
  signature: 'Best regards,\nAI Agent\npowered by KeyID.ai',
});

// Get metrics
callTool('keyid_get_metrics', {
  period: '7d',
});
```

### Using with the MCP SDK (if building a custom client)

```javascript
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const transport = new StdioClientTransport({
  command: 'npx',
  args: ['@keyid/agent-kit'],
  env: {
    KEYID_PUBLIC_KEY: process.env.KEYID_PUBLIC_KEY,
    KEYID_PRIVATE_KEY: process.env.KEYID_PRIVATE_KEY,
  },
});

const client = new Client(
  { name: 'my-email-agent', version: '1.0.0' },
  { capabilities: {} }
);

await client.connect(transport);

// List available tools
const tools = await client.listTools();
console.log('Available tools:', tools.tools.map(t => t.name));

// Get email address
const emailResult = await client.callTool({
  name: 'keyid_get_email',
  arguments: {},
});
console.log('Agent email:', emailResult.content[0].text);

// Check unread
const unread = await client.callTool({
  name: 'keyid_get_unread_count',
  arguments: {},
});
console.log('Unread count:', unread.content[0].text);

// Send email
await client.callTool({
  name: 'keyid_send',
  arguments: {
    to: 'recipient@example.com',
    subject: 'Automated report',
    body: 'Your daily report is attached.',
    html: '<p>Your <strong>daily report</strong> is attached.</p>',
  },
});

await client.close();
```

### Webhook Integration

```javascript
import express from 'express';

const app = express();
app.use(express.json());

// Endpoint to receive KeyID webhook events
app.post('/keyid-webhook', (req, res) => {
  const event = req.body;

  if (event.type === 'message.received') {
    const { from, subject, body, message_id } = event.data;
    console.log(`New email from ${from}: ${subject}`);
    
    // Trigger your agent logic here
    handleIncomingEmail({ from, subject, body, message_id });
  }

  res.json({ ok: true });
});

app.listen(3000);

// Register the webhook via the MCP tool
// (call this once via your agent)
// callTool('keyid_create_webhook', {
//   url: 'https://your-server.com/keyid-webhook',
//   events: ['message.received'],
// });
```

## Common Patterns

### Pattern: Agent with Persistent Identity

```javascript
// Generate and store keys once, reuse forever
import { writeFileSync, readFileSync, existsSync } from 'fs';
import { generateKeyPairSync } from 'crypto'; // or use @noble/ed25519

const KEY_FILE = '.keyid-keys.json';

function loadOrCreateKeys() {
  if (existsSync(KEY_FILE)) {
    return JSON.parse(readFileSync(KEY_FILE, 'utf8'));
  }
  // Let @keyid/agent-kit auto-generate on first run,
  // then save what it prints to stderr
  // Or pre-generate using @noble/ed25519:
  // const privKey = randomBytes(32);
  // const pubKey = await ed.getPublicKeyAsync(privKey);
  return null; // will auto-generate
}
```

### Pattern: Email-Triggered Agent Loop

```javascript
// Poll inbox and process new messages
async function agentEmailLoop(client) {
  while (true) {
    const result = await client.callTool({
      name: 'keyid_get_inbox',
      arguments: { unread_only: true, limit: 5 },
    });

    const messages = JSON.parse(result.content[0].text);

    for (const msg of messages) {
      // Process with your LLM/agent logic
      const agentResponse = await processWithAgent(msg);

      // Reply
      await client.callTool({
        name: 'keyid_reply',
        arguments: {
          message_id: msg.id,
          body: agentResponse,
        },
      });

      // Mark as read
      await client.callTool({
        name: 'keyid_update_message',
        arguments: { message_id: msg.id, read: true },
      });
    }

    // Wait 60 seconds before next poll
    await new Promise(r => setTimeout(r, 60_000));
  }
}
```

### Pattern: Draft-Review-Send Workflow

```javascript
// Create draft, review, then send
const draft = await client.callTool({
  name: 'keyid_create_draft',
  arguments: {
    to: 'client@example.com',
    subject: 'Proposal',
    body: draftBody,
  },
});

const draftId = JSON.parse(draft.content[0].text).id;

// Human or agent reviews...
// Then send:
await client.callTool({
  name: 'keyid_send_draft',
  arguments: { draft_id: draftId },
});
```

## Troubleshooting

### Agent gets a new email address every run
**Cause:** Keys not persisted between runs.  
**Fix:** Save `KEYID_PUBLIC_KEY` and `KEYID_PRIVATE_KEY` from first run output and set them in your config or environment.

### MCP server not appearing in Claude Desktop
**Fix:** Restart Claude Desktop after editing config. Verify JSON is valid (no trailing commas). Check that `npx` is in your PATH.

### Tool calls return errors
**Fix:** Ensure the agent is provisioned first — call `keyid_provision` before other tools, or call `keyid_get_email` to confirm the agent has an address.

### Emails not being received
**Fix:** Check `keyid_manage_list` to ensure the sender isn't blocklisted. Check `keyid_get_metrics` for bounce data.

### Connection drops / server crashes
**Fix:** The server uses stdio — make sure nothing else is writing to stdout in the same process. Restart the MCP server process.

### Keys auto-generated but not shown
**Cause:** stderr may be suppressed by your MCP client.  
**Fix:** Run `npx @keyid/agent-kit` directly in a terminal first to capture the key output before adding to your MCP config.

## Protocol Details

- **Transport:** stdio (JSON-RPC over stdin/stdout)
- **MCP Protocol Version:** `2024-11-05`
- **Auth:** Ed25519 keypair — public key becomes agent identity, private key signs requests
- **Compatibility:** Claude Desktop, Cursor, any MCP-compatible client
