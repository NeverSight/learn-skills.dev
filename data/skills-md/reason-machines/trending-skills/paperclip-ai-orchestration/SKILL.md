---
name: paperclip-ai-orchestration
description: Skill for using Paperclip — open-source orchestration platform for running autonomous AI-agent companies with org charts, budgets, governance, and heartbeats.
triggers:
  - set up paperclip for my ai company
  - orchestrate multiple ai agents with paperclip
  - configure agents and goals in paperclip
  - add a new agent to my paperclip company
  - monitor ai agent costs and budgets in paperclip
  - create a company with paperclip orchestration
  - heartbeat scheduling for ai agents
  - manage multi-agent workflows with paperclip
---

# Paperclip AI Orchestration

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Paperclip is an open-source Node.js + React platform that runs a **company made of AI agents**. It provides org charts, goal alignment, ticket-based task management, budget enforcement, heartbeat scheduling, governance, and a full audit log — so you manage business outcomes instead of individual agent sessions.

---

## Installation

### Quickstart (recommended)

```bash
npx paperclipai onboard --yes
```

This clones the repo, installs dependencies, seeds an embedded PostgreSQL database, and starts the server.

### Manual setup

```bash
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pnpm install
pnpm dev
```

**Requirements:**
- Node.js 20+
- pnpm 9.15+

The API server starts at `http://localhost:3100`. An embedded PostgreSQL database is created automatically — no manual DB setup needed for local development.

### Production setup

Point Paperclip at an external Postgres instance and object storage via environment variables:

```bash
# .env
DATABASE_URL=postgresql://user:password@host:5432/paperclip
STORAGE_BUCKET=your-s3-bucket
STORAGE_REGION=us-east-1
AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
PORT=3100
```

---

## Key CLI Commands

```bash
pnpm dev              # Start API + UI in development mode
pnpm build            # Build for production
pnpm start            # Start production server
pnpm db:migrate       # Run pending database migrations
pnpm db:seed          # Seed demo data
pnpm test             # Run test suite
npx paperclipai onboard --yes   # Full automated onboarding
```

---

## Core Concepts

| Concept | Description |
|---|---|
| **Company** | Top-level namespace. All agents, goals, tasks, and budgets are scoped to a company. |
| **Agent** | An AI worker (OpenClaw, Claude Code, Codex, Cursor, HTTP bot, Bash script). |
| **Goal** | Hierarchical business objective. Tasks inherit goal ancestry so agents know the "why". |
| **Task / Ticket** | A unit of work assigned to an agent. Conversations and tool calls are threaded to it. |
| **Heartbeat** | A cron-style schedule that wakes an agent to check for work or perform recurring tasks. |
| **Org Chart** | Hierarchical reporting structure. Agents have managers, direct reports, roles, and titles. |
| **Budget** | Monthly token/cost cap per agent. Atomic enforcement — agent stops when budget exhausted. |
| **Governance** | Approval gates for hires, strategy changes, and config rollbacks. You are the board. |

---

## REST API

The Paperclip API is served at `http://localhost:3100/api/v1`.

### Authentication

```typescript
// All requests require a bearer token
const headers = {
  'Authorization': `Bearer ${process.env.PAPERCLIP_API_KEY}`,
  'Content-Type': 'application/json',
};
```

### Create a Company

```typescript
const response = await fetch('http://localhost:3100/api/v1/companies', {
  method: 'POST',
  headers,
  body: JSON.stringify({
    name: 'NoteGenius Inc.',
    mission: 'Build the #1 AI note-taking app to $1M MRR.',
    slug: 'notegenius',
  }),
});

const { company } = await response.json();
console.log(company.id); // "cmp_abc123"
```

### Register an Agent

```typescript
const agent = await fetch(`http://localhost:3100/api/v1/companies/${companyId}/agents`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    name: 'Alice',
    role: 'CTO',
    runtime: 'claude-code',       // 'openclaw' | 'claude-code' | 'codex' | 'cursor' | 'bash' | 'http'
    endpoint: process.env.ALICE_AGENT_ENDPOINT,
    budget: {
      monthly_usd: 200,
    },
    heartbeat: {
      cron: '0 * * * *',          // every hour
      enabled: true,
    },
    reports_to: ceoAgentId,       // parent in org chart
  }),
}).then(r => r.json());
```

### Create a Goal

```typescript
const goal = await fetch(`http://localhost:3100/api/v1/companies/${companyId}/goals`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    title: 'Launch v1 to Product Hunt',
    description: 'Ship the MVP and generate 500 upvotes on launch day.',
    parent_goal_id: null,         // null = top-level goal
    owner_agent_id: ctoAgentId,
    due_date: '2026-06-01',
  }),
}).then(r => r.json());
```

### Create a Task

```typescript
const task = await fetch(`http://localhost:3100/api/v1/companies/${companyId}/tasks`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    title: 'Implement offline sync for notes',
    description: 'Use CRDTs to merge note edits made offline. See ADR-004.',
    assigned_to: engineerAgentId,
    goal_id: goal.id,              // links task to goal ancestry
    priority: 'high',
  }),
}).then(r => r.json());

console.log(task.id); // "tsk_xyz789"
```

### List Tasks for an Agent

```typescript
const { tasks } = await fetch(
  `http://localhost:3100/api/v1/agents/${agentId}/tasks?status=open`,
  { headers }
).then(r => r.json());
```

### Post a Message to a Task Thread

```typescript
await fetch(`http://localhost:3100/api/v1/tasks/${taskId}/messages`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    role: 'agent',
    content: 'Implemented CRDT merge logic. Tests passing. Ready for review.',
    tool_calls: [
      {
        tool: 'bash',
        input: 'pnpm test --filter=sync',
        output: '42 tests passed in 3.1s',
      },
    ],
  }),
});
```

### Report Agent Cost

Agents self-report token usage; Paperclip enforces budget atomically:

```typescript
await fetch(`http://localhost:3100/api/v1/agents/${agentId}/cost`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    tokens_in: 12400,
    tokens_out: 3800,
    model: 'claude-opus-4-5',
    task_id: taskId,
  }),
});
```

### Heartbeat Ping

Agents call this endpoint on each scheduled wake-up:

```typescript
const { instructions, tasks } = await fetch(
  `http://localhost:3100/api/v1/agents/${agentId}/heartbeat`,
  { method: 'POST', headers }
).then(r => r.json());

// instructions — what the org says to focus on now
// tasks        — open tasks assigned to this agent
```

---

## TypeScript SDK Pattern

Wrap the REST API for cleaner agent integration:

```typescript
// lib/paperclip-client.ts
export class PaperclipClient {
  private base: string;
  private headers: Record<string, string>;

  constructor(
    base = process.env.PAPERCLIP_BASE_URL ?? 'http://localhost:3100',
    apiKey = process.env.PAPERCLIP_API_KEY ?? '',
  ) {
    this.base = `${base}/api/v1`;
    this.headers = {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    };
  }

  private async req<T>(path: string, init?: RequestInit): Promise<T> {
    const res = await fetch(`${this.base}${path}`, {
      ...init,
      headers: { ...this.headers, ...init?.headers },
    });
    if (!res.ok) {
      const body = await res.text();
      throw new Error(`Paperclip API ${res.status}: ${body}`);
    }
    return res.json() as Promise<T>;
  }

  heartbeat(agentId: string) {
    return this.req<{ instructions: string; tasks: Task[] }>(
      `/agents/${agentId}/heartbeat`,
      { method: 'POST' },
    );
  }

  completeTask(taskId: string, summary: string) {
    return this.req(`/tasks/${taskId}`, {
      method: 'PATCH',
      body: JSON.stringify({ status: 'done', completion_summary: summary }),
    });
  }

  reportCost(agentId: string, payload: CostPayload) {
    return this.req(`/agents/${agentId}/cost`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }
}
```

---

## Building an Agent That Works With Paperclip

A minimal agent loop that integrates with Paperclip:

```typescript
// agent.ts
import { PaperclipClient } from './lib/paperclip-client';

const client = new PaperclipClient();
const AGENT_ID = process.env.PAPERCLIP_AGENT_ID!;

async function runHeartbeat() {
  console.log('[agent] heartbeat ping');

  const { instructions, tasks } = await client.heartbeat(AGENT_ID);

  for (const task of tasks) {
    console.log(`[agent] working on task: ${task.title}`);

    try {
      // --- your agent logic here ---
      const result = await doWork(task, instructions);

      await client.completeTask(task.id, result.summary);
      await client.reportCost(AGENT_ID, {
        tokens_in: result.tokensIn,
        tokens_out: result.tokensOut,
        model: result.model,
        task_id: task.id,
      });

      console.log(`[agent] task ${task.id} done`);
    } catch (err) {
      console.error(`[agent] task ${task.id} failed`, err);
      // Paperclip will reassign or escalate based on governance rules
    }
  }
}

// Heartbeat is usually driven by Paperclip's cron, but you can also self-poll:
setInterval(runHeartbeat, 60_000);
runHeartbeat();
```

---

## Registering an HTTP Agent (any language)

Any process reachable over HTTP can be an agent. Paperclip sends a POST to your endpoint:

```typescript
// Paperclip calls POST /work on your agent with this shape:
interface PaperclipWorkPayload {
  agent_id: string;
  task: {
    id: string;
    title: string;
    description: string;
    goal_ancestry: string[];   // full chain: company mission → goal → sub-goal
  };
  instructions: string;        // current org-level directives
  context: Record<string, unknown>;
}
```

Respond with:

```typescript
interface PaperclipWorkResponse {
  status: 'done' | 'blocked' | 'delegated';
  summary: string;
  tokens_in?: number;
  tokens_out?: number;
  model?: string;
  delegate_to?: string;        // agent_id if status === 'delegated'
}
```

---

## Multi-Company Setup

```typescript
// Create isolated companies in one deployment
const companies = await Promise.all([
  createCompany({ name: 'NoteGenius', mission: 'Best note app' }),
  createCompany({ name: 'ShipFast', mission: 'Fastest deploy tool' }),
]);

// Each company has its own agents, goals, tasks, budgets, and audit log
// No data leaks between companies
```

---

## Governance & Approvals

```typescript
// Fetch pending approval requests (you are the board)
const { approvals } = await fetch(
  `http://localhost:3100/api/v1/companies/${companyId}/approvals?status=pending`,
  { headers }
).then(r => r.json());

// Approve a hire
await fetch(`http://localhost:3100/api/v1/approvals/${approvals[0].id}`, {
  method: 'PATCH',
  headers,
  body: JSON.stringify({ decision: 'approved', note: 'Looks good.' }),
});

// Roll back a bad config change
await fetch(`http://localhost:3100/api/v1/agents/${agentId}/config/rollback`, {
  method: 'POST',
  headers,
  body: JSON.stringify({ revision: 3 }),
});
```

---

## Environment Variables Reference

```bash
# Required
PAPERCLIP_API_KEY=                  # Your API key for the Paperclip server

# Database (defaults to embedded Postgres in dev)
DATABASE_URL=                        # postgresql://user:pass@host:5432/db

# Storage (defaults to local filesystem in dev)
STORAGE_DRIVER=local                 # 'local' | 's3'
STORAGE_BUCKET=                      # S3 bucket name
STORAGE_REGION=                      # AWS region
AWS_ACCESS_KEY_ID=                   # From your environment
AWS_SECRET_ACCESS_KEY=               # From your environment

# Server
PORT=3100
BASE_URL=http://localhost:3100

# Agent-side (used inside agent processes)
PAPERCLIP_BASE_URL=http://localhost:3100
PAPERCLIP_AGENT_ID=                  # The agent's UUID from Paperclip
```

---

## Common Patterns

### Pattern: Manager delegates to reports

```typescript
// In your manager agent's heartbeat handler:
const { tasks } = await client.heartbeat(MANAGER_AGENT_ID);

for (const task of tasks) {
  if (task.complexity === 'high') {
    // Delegate down the org chart
    await fetch(`http://localhost:3100/api/v1/tasks/${task.id}/delegate`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ to_agent_id: engineerAgentId }),
    });
  }
}
```

### Pattern: @-mention an agent in a task thread

```typescript
await fetch(`http://localhost:3100/api/v1/tasks/${taskId}/messages`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    role: 'human',
    content: `@${designerAgentId} Can you review the UI for this feature?`,
  }),
});
// Paperclip delivers the mention as a trigger to the designer agent's next heartbeat
```

### Pattern: Export a company template (Clipmart)

```typescript
const blob = await fetch(
  `http://localhost:3100/api/v1/companies/${companyId}/export`,
  { headers }
).then(r => r.blob());

// Saves a .paperclip bundle with secrets scrubbed
fs.writeFileSync('my-saas-company.paperclip', Buffer.from(await blob.arrayBuffer()));
```

### Pattern: Import a company template

```typescript
const form = new FormData();
form.append('file', fs.createReadStream('my-saas-company.paperclip'));

await fetch('http://localhost:3100/api/v1/companies/import', {
  method: 'POST',
  headers: { Authorization: `Bearer ${process.env.PAPERCLIP_API_KEY}` },
  body: form,
});
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ECONNREFUSED localhost:3100` | Server not running. Run `pnpm dev` first. |
| `401 Unauthorized` | Check `PAPERCLIP_API_KEY` is set and matches server config. |
| Agent never wakes up | Verify `heartbeat.enabled: true` and cron expression is valid. Check server logs for scheduler errors. |
| Budget exhausted immediately | `monthly_usd` budget too low or tokens_in/tokens_out are being over-reported. Check `POST /agents/:id/cost` payloads. |
| Task stuck in `open` | Agent may be offline or heartbeat misconfigured. Check `/api/v1/agents/:id/status`. |
| Database migration errors | Run `pnpm db:migrate` after pulling new commits. |
| Embedded Postgres won't start | Port 5433 may be in use. Set `EMBEDDED_PG_PORT=5434` in `.env`. |
| Org chart not resolving | `reports_to` agent ID must exist before creating the subordinate. Create top-down. |

---

## Resources

- **Docs:** https://paperclip.ing/docs
- **GitHub:** https://github.com/paperclipai/paperclip
- **Discord:** https://discord.gg/m4HZY7xNG3
- **Clipmart (company templates):** https://paperclip.ing/clipmart *(coming soon)*
