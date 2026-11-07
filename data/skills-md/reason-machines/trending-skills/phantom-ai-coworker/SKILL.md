---
name: phantom-ai-coworker
description: AI co-worker agent with its own computer, persistent memory, self-evolution, MCP server, and Slack/email identity built on Claude Agent SDK
triggers:
  - set up phantom ai agent
  - configure phantom co-worker
  - phantom self-evolving agent
  - phantom mcp server setup
  - phantom slack bot agent
  - build phantom ai coworker
  - phantom persistent memory agent
  - deploy phantom on docker
---

# Phantom AI Co-worker

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Phantom is an AI co-worker that runs on its own dedicated machine. Unlike chatbots, Phantom has persistent memory across sessions, creates and registers its own MCP tools at runtime, self-evolves based on observed patterns, communicates via Slack/email/Telegram/Webhook, and can build full infrastructure (databases, dashboards, APIs, pipelines) on its VM. Built on the Claude Agent SDK with TypeScript/Bun.

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   Phantom Agent                     │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────┐ │
│  │  Claude  │  │ Qdrant   │  │   MCP Server      │ │
│  │  Agent   │  │ (memory) │  │ (dynamic tools)   │ │
│  │   SDK    │  │          │  │                   │ │
│  └──────────┘  └──────────┘  └───────────────────┘ │
│  ┌──────────────────────────────────────────────┐   │
│  │         Channels                             │   │
│  │  Slack │ Email │ Telegram │ Webhook │ Discord │   │
│  └──────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────┐   │
│  │         Self-Evolution Engine                │   │
│  │  observe → reflect → propose → validate → evolve│
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## Installation

### Docker (Recommended)

```bash
# Download compose file and env template
curl -fsSL https://raw.githubusercontent.com/ghostwright/phantom/main/docker-compose.user.yaml -o docker-compose.yaml
curl -fsSL https://raw.githubusercontent.com/ghostwright/phantom/main/.env.example -o .env

# Edit .env with your credentials (see Configuration section)
nano .env

# Start Phantom (includes Qdrant + Ollama)
docker compose up -d

# Check health
curl http://localhost:3100/health

# View logs
docker compose logs -f phantom
```

### From Source (Bun)

```bash
git clone https://github.com/ghostwright/phantom.git
cd phantom

# Install dependencies
bun install

# Copy env
cp .env.example .env
# Edit .env

# Start Qdrant (required for memory)
docker run -d -p 6333:6333 qdrant/qdrant

# Start Phantom
bun run start

# Development mode with hot reload
bun run dev
```

## Configuration (.env)

```bash
# === Required ===
ANTHROPIC_API_KEY=                  # Your Anthropic API key

# === Slack (required for Slack channel) ===
SLACK_BOT_TOKEN=xoxb-              # Bot OAuth token
SLACK_APP_TOKEN=xapp-              # App-level token (socket mode)
SLACK_SIGNING_SECRET=              # Signing secret
OWNER_SLACK_USER_ID=U0XXXXXXXXX    # Your Slack user ID

# === Memory (Qdrant) ===
QDRANT_URL=http://localhost:6333    # Qdrant vector DB URL
QDRANT_API_KEY=                    # Optional, for cloud Qdrant
OLLAMA_URL=http://localhost:11434   # Ollama for embeddings

# === Email (optional) ===
RESEND_API_KEY=                    # For email sending via Resend
PHANTOM_EMAIL=phantom@yourdomain   # Phantom's email address

# === Telegram (optional) ===
TELEGRAM_BOT_TOKEN=                # BotFather token

# === Infrastructure ===
PHANTOM_VM_DOMAIN=                 # Public domain for served assets
PHANTOM_PORT=3100                  # HTTP port (default 3100)

# === Self-Evolution ===
EVOLUTION_VALIDATION_MODEL=claude-3-5-sonnet-20241022  # Separate model for validation
EVOLUTION_ENABLED=true

# === Credentials Vault ===
CREDENTIAL_ENCRYPTION_KEY=         # AES-256-GCM key (auto-generated if empty)
```

## Key Commands

```bash
# Docker operations
docker compose up -d               # Start all services
docker compose down                # Stop all services
docker compose logs -f phantom     # Stream logs
docker compose pull                # Update to latest image

# Bun development
bun run start                      # Production start
bun run dev                        # Dev mode with watch
bun run test                       # Run test suite
bun run build                      # Build TypeScript

# Health checks
curl http://localhost:3100/health
curl http://localhost:3100/status

# MCP server endpoint
curl http://localhost:3100/mcp
```

## Core Concepts & Code Examples

### 1. Memory System (Qdrant + Embeddings)

Phantom stores memories as vector embeddings for semantic recall across sessions.

```typescript
// src/memory/memory-manager.ts pattern
import { QdrantClient } from '@qdrant/js-client-rest';

const client = new QdrantClient({ url: process.env.QDRANT_URL });

// Storing a memory
async function storeMemory(content: string, metadata: Record<string, unknown>) {
  const embedding = await generateEmbedding(content); // via Ollama
  await client.upsert('phantom_memory', {
    points: [{
      id: crypto.randomUUID(),
      vector: embedding,
      payload: {
        content,
        timestamp: Date.now(),
        ...metadata,
      },
    }],
  });
}

// Recalling relevant memories
async function recallMemories(query: string, limit = 5) {
  const queryEmbedding = await generateEmbedding(query);
  const results = await client.search('phantom_memory', {
    vector: queryEmbedding,
    limit,
    with_payload: true,
  });
  return results.map(r => r.payload?.content);
}
```

### 2. Dynamic MCP Tool Registration

Phantom creates MCP tools at runtime that persist across restarts.

```typescript
// Pattern: registering a dynamically created tool
interface PhantomTool {
  name: string;
  description: string;
  inputSchema: Record<string, unknown>;
  handler: string; // serialized or endpoint URL
}

// Phantom internally registers tools like this
async function registerDynamicTool(tool: PhantomTool) {
  // Store tool definition in persistent storage
  await storeMemory(JSON.stringify(tool), {
    type: 'mcp_tool',
    toolName: tool.name,
  });

  // Register with MCP server at runtime
  mcpServer.tool(tool.name, tool.description, tool.inputSchema, async (args) => {
    return await executeToolHandler(tool.handler, args);
  });
}

// MCP server setup (how Phantom exposes tools to Claude Code)
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';

const mcpServer = new McpServer({
  name: 'phantom',
  version: '0.18.1',
});

// Connect Claude Code to Phantom's MCP server:
// In claude_desktop_config.json or .cursor/mcp.json:
// {
//   "mcpServers": {
//     "phantom": {
//       "url": "http://your-phantom-vm:3100/mcp"
//     }
//   }
// }
```

### 3. Slack Channel Integration

```typescript
// How Phantom handles Slack messages
import { App } from '@slack/bolt';

const slack = new App({
  token: process.env.SLACK_BOT_TOKEN,
  appToken: process.env.SLACK_APP_TOKEN,
  socketMode: true,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
});

// Phantom listens for direct messages and mentions
slack.event('message', async ({ event, say }) => {
  if (event.subtype) return; // Skip bot messages, edits

  const userMessage = (event as any).text;
  const userId = (event as any).user;

  // Recall relevant context from memory
  const memories = await recallMemories(userMessage);

  // Run Claude agent with memory context
  const response = await runPhantomAgent({
    message: userMessage,
    userId,
    memories,
    channel: (event as any).channel,
  });

  await say({ text: response, thread_ts: (event as any).ts });
});

// Phantom DMs you when ready
async function notifyOwnerReady() {
  await slack.client.chat.postMessage({
    channel: process.env.OWNER_SLACK_USER_ID!,
    text: "👻 Phantom is online and ready.",
  });
}
```

### 4. Claude Agent SDK Integration

```typescript
// Core agent loop using Anthropic Agent SDK
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function runPhantomAgent({
  message,
  userId,
  memories,
  channel,
}: PhantomAgentInput) {
  const systemPrompt = buildSystemPrompt(memories);

  // Agentic loop with tool use
  const response = await anthropic.messages.create({
    model: 'claude-opus-4-5',
    max_tokens: 8096,
    system: systemPrompt,
    messages: [{ role: 'user', content: message }],
    tools: await getAvailableTools(), // includes dynamic MCP tools
  });

  // Handle tool calls in loop
  if (response.stop_reason === 'tool_use') {
    return await handleToolCalls(response, message, userId);
  }

  // Store this interaction as memory
  await storeMemory(`User ${userId} asked: ${message}. I responded: ${response.content}`, {
    type: 'interaction',
    userId,
    channel,
  });

  return extractTextContent(response.content);
}

function buildSystemPrompt(memories: string[]): string {
  return `You are Phantom, an AI co-worker with your own computer.
You have persistent memory and can build infrastructure.

Relevant memories from past sessions:
${memories.map((m, i) => `${i + 1}. ${m}`).join('\n')}

You have access to your VM, can install software, build tools,
serve web pages on ${process.env.PHANTOM_VM_DOMAIN}, and register
new capabilities for yourself.`;
}
```

### 5. Secure Credential Collection

Phantom collects credentials via encrypted forms, never plain text.

```typescript
// Credential vault pattern
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

const ALGORITHM = 'aes-256-gcm';
const KEY = Buffer.from(process.env.CREDENTIAL_ENCRYPTION_KEY!, 'hex');

function encryptCredential(plaintext: string): string {
  const iv = randomBytes(16);
  const cipher = createCipheriv(ALGORITHM, KEY, iv);
  const encrypted = Buffer.concat([
    cipher.update(plaintext, 'utf8'),
    cipher.final(),
  ]);
  const authTag = cipher.getAuthTag();
  return `${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted.toString('hex')}`;
}

function decryptCredential(ciphertext: string): string {
  const [ivHex, authTagHex, encryptedHex] = ciphertext.split(':');
  const iv = Buffer.from(ivHex, 'hex');
  const authTag = Buffer.from(authTagHex, 'hex');
  const encrypted = Buffer.from(encryptedHex, 'hex');
  const decipher = createDecipheriv(ALGORITHM, KEY, iv);
  decipher.setAuthTag(authTag);
  return decipher.update(encrypted) + decipher.final('utf8');
}

// Phantom generates a one-time secure form URL for credential collection
async function generateCredentialForm(service: string, fields: string[]) {
  const token = randomBytes(32).toString('hex');
  // Store token with expiry
  await storeCredentialRequest(token, { service, fields, expires: Date.now() + 3600000 });
  return `${process.env.PHANTOM_VM_DOMAIN}/credentials/${token}`;
}
```

### 6. Self-Evolution Engine

Phantom observes its own behavior, proposes improvements, validates with a separate model, and evolves.

```typescript
// Evolution cycle pattern
interface EvolutionProposal {
  observation: string;
  currentBehavior: string;
  proposedChange: string;
  rationale: string;
  version: string;
}

async function runEvolutionCycle() {
  if (process.env.EVOLUTION_ENABLED !== 'true') return;

  // 1. Observe recent interactions
  const recentMemories = await recallMemories('recent interactions', 50);

  // 2. Generate proposals with primary model
  const proposals = await generateEvolutionProposals(recentMemories);

  for (const proposal of proposals) {
    // 3. Validate with DIFFERENT model to avoid self-enhancement bias
    const isValid = await validateProposal(proposal);

    if (isValid) {
      // 4. Apply evolution and version it
      await applyEvolution(proposal);
      await versionEvolution(proposal);

      // Notify owner of evolution
      await notifySlack(
        `🧬 I've evolved: ${proposal.observation}\n→ ${proposal.proposedChange}`
      );
    }
  }
}

async function validateProposal(proposal: EvolutionProposal): Promise<boolean> {
  // Uses a separate model instance to validate
  const validationResponse = await anthropic.messages.create({
    model: process.env.EVOLUTION_VALIDATION_MODEL!,
    max_tokens: 1024,
    messages: [{
      role: 'user',
      content: `Evaluate this AI self-improvement proposal for safety and benefit:
${JSON.stringify(proposal, null, 2)}

Respond with JSON: { "approved": boolean, "reason": string }`,
    }],
  });
  // Parse and return approval
  const result = JSON.parse(extractTextContent(validationResponse.content));
  return result.approved;
}
```

### 7. Infrastructure Building (VM Operations)

```typescript
// Phantom can run shell commands and Docker on its VM
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// Example: Phantom spinning up a Postgres container
async function provisionDatabase(projectName: string) {
  const port = await findAvailablePort(5432);
  const password = randomBytes(16).toString('hex');

  const { stdout } = await execAsync(`
    docker run -d \
      --name phantom-pg-${projectName} \
      -e POSTGRES_PASSWORD=${password} \
      -e POSTGRES_DB=${projectName} \
      -p ${port}:5432 \
      postgres:16-alpine
  `);

  const connectionString = `postgresql://postgres:${password}@localhost:${port}/${projectName}`;

  // Store connection string securely
  await storeCredential(`${projectName}_postgres`, encryptCredential(connectionString));

  // Register as MCP tool for future use
  await registerDynamicTool({
    name: `query_${projectName}_db`,
    description: `Query the ${projectName} PostgreSQL database`,
    inputSchema: { sql: { type: 'string' } },
    handler: `postgres:${connectionString}`,
  });

  return { connectionString, port };
}

// Serving a web page on Phantom's domain
async function serveWebPage(slug: string, htmlContent: string) {
  const filePath = `/var/phantom/public/${slug}/index.html`;
  await Bun.write(filePath, htmlContent);
  return `${process.env.PHANTOM_VM_DOMAIN}/${slug}`;
}
```

### 8. Webhook Channel

```typescript
// Send messages to Phantom via webhook
const response = await fetch('http://your-phantom:3100/webhook/message', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.PHANTOM_WEBHOOK_SECRET}`,
  },
  body: JSON.stringify({
    message: 'Analyze our GitHub issues and create a priority matrix',
    userId: 'automation-system',
    context: { source: 'ci-pipeline', repo: 'myorg/myrepo' },
  }),
});

const { response: agentResponse, taskId } = await response.json();
```

## Connecting Claude Code to Phantom's MCP Server

Once Phantom is running, connect Claude Code to use all of Phantom's registered tools:

```json
// ~/.claude/claude_desktop_config.json  or  .cursor/mcp.json
{
  "mcpServers": {
    "phantom": {
      "url": "http://your-phantom-vm:3100/mcp"
    }
  }
}
```

Or via CLI:
```bash
# Claude Code CLI
claude mcp add phantom --url http://your-phantom-vm:3100/mcp

# Verify connection
claude mcp list
```

## Docker Compose Structure

```yaml
# docker-compose.yaml (production user config)
services:
  phantom:
    image: ghostwright/phantom:latest
    ports:
      - "3100:3100"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN}
      - SLACK_APP_TOKEN=${SLACK_APP_TOKEN}
      - SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET}
      - OWNER_SLACK_USER_ID=${OWNER_SLACK_USER_ID}
      - QDRANT_URL=http://qdrant:6333
      - OLLAMA_URL=http://ollama:11434
      - PHANTOM_VM_DOMAIN=${PHANTOM_VM_DOMAIN}
      - RESEND_API_KEY=${RESEND_API_KEY}
    volumes:
      - phantom_data:/var/phantom
      - /var/run/docker.sock:/var/run/docker.sock  # For Docker-in-Docker
    depends_on:
      - qdrant
      - ollama
    restart: unless-stopped

  qdrant:
    image: qdrant/qdrant:latest
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

volumes:
  phantom_data:
  qdrant_data:
  ollama_data:
```

## Slack App Setup

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → Create New App → From manifest
2. Use this manifest:

```yaml
display_information:
  name: Phantom
features:
  bot_user:
    display_name: Phantom
    always_online: true
  app_home:
    messages_tab_enabled: true
oauth_config:
  scopes:
    bot:
      - channels:history
      - channels:read
      - chat:write
      - chat:write.customize
      - files:write
      - groups:history
      - im:history
      - im:read
      - im:write
      - mpim:history
      - users:read
settings:
  event_subscriptions:
    bot_events:
      - message.channels
      - message.groups
      - message.im
      - message.mpim
  interactivity:
    is_enabled: true
  socket_mode_enabled: true
```

3. Install to workspace → copy Bot Token (`xoxb-`) to `SLACK_BOT_TOKEN`
4. Generate App-Level Token with `connections:write` → copy to `SLACK_APP_TOKEN`
5. Copy Signing Secret → `SLACK_SIGNING_SECRET`
6. Get your user ID: In Slack, click your profile → copy Member ID → `OWNER_SLACK_USER_ID`

## Common Patterns

### Asking Phantom to Build a Tool

In Slack:
```
@phantom Create an MCP tool that queries our internal metrics API at 
https://metrics.internal/api/v2. It should accept a metric_name and 
time_range parameter and return JSON.
```

Phantom will build the tool, register it with its MCP server, and confirm it's available.

### Scheduling Recurring Tasks

```
@phantom Every weekday at 9am, check our GitHub repo myorg/myrepo for 
open PRs older than 3 days and post a summary to #engineering
```

### Requesting a Dashboard

```
@phantom Build a dashboard showing our deployment frequency over the 
last 30 days. Make it shareable with the team.
```

Phantom builds it, serves it at `https://your-phantom-domain/dashboards/deploy-freq`, and sends you the link.

### Memory Queries

```
@phantom What did I tell you about our database architecture last week?
@phantom What tools have you built for me so far?
@phantom Summarize everything you know about Project X
```

## Troubleshooting

### Phantom not starting
```bash
# Check all services are healthy
docker compose ps

# Qdrant must be ready before Phantom
docker compose logs qdrant
curl http://localhost:6333/health

# Ollama must pull embedding model
docker compose logs ollama
```

### Memory not persisting
```bash
# Verify Qdrant collections exist
curl http://localhost:6333/collections

# Check Phantom can reach Qdrant
docker compose exec phantom curl http://qdrant:6333/health
```

### Slack not receiving messages
- Verify `SLACK_APP_TOKEN` starts with `xapp-` (not `xoxb-`)
- Socket mode must be enabled in Slack App settings
- Check bot is invited to channels: `/invite @Phantom`
- Verify `OWNER_SLACK_USER_ID` is correct (not display name, actual ID)

### MCP tools not appearing in Claude Code
```bash
# Verify MCP server is running
curl http://localhost:3100/mcp

# Check tool registration
curl http://localhost:3100/mcp/tools

# Restart Claude Code after adding MCP config
```

### Evolution not triggering
```bash
# Check env var
echo $EVOLUTION_ENABLED  # should be "true"

# Verify validation model is set
echo $EVOLUTION_VALIDATION_MODEL

# Check logs for evolution cycle
docker compose logs phantom | grep -i evolv
```

### Docker socket permission denied
```bash
# Add phantom user to docker group, or run with:
sudo docker compose up -d

# Or add to docker-compose.yaml:
# user: root
```

## API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Health check |
| `/status` | GET | Agent status + uptime |
| `/mcp` | GET/POST | MCP server endpoint |
| `/mcp/tools` | GET | List registered tools |
| `/webhook/message` | POST | Send message to agent |
| `/credentials/:token` | GET/POST | Secure credential form |
| `/public/:slug` | GET | Served static assets |

## Version History & Rollback

```bash
# Phantom versions its own evolution
# View evolution history in logs
docker compose logs phantom | grep -i "evolved"

# Pin to specific version
# Edit docker-compose.yaml:
# image: ghostwright/phantom:0.18.1

# Roll back
docker compose down
# Change image tag in compose file
docker compose up -d
```
