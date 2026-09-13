---
name: openclaw-control-center
description: Local-first, security-first control center for OpenClaw agents — visibility dashboard with readonly defaults, token attribution, collaboration tracing, and safe write operations.
triggers:
  - openclaw control center
  - openclaw dashboard
  - openclaw agent monitoring
  - openclaw token usage
  - openclaw collaboration tracing
  - openclaw task approval
  - openclaw memory management
  - openclaw local control panel
---

# openclaw-control-center

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection

OpenClaw Control Center transforms OpenClaw from a black box into a local, auditable control center. It provides visibility into agent activity, token spend, task execution chains, cross-session collaboration, memory state, and document sources — with security-first defaults that keep all mutations off by default.

## What It Does

- **Overview**: System health, pending items, risk signals, and operational summary
- **Usage**: Daily/7d/30d token spend, quota, context pressure, subscription window
- **Staff**: Who is actively executing vs. queued — not just "has tasks"
- **Collaboration**: Parent-child session handoffs and verified cross-session messages (e.g. `Main ⇄ Pandas`)
- **Tasks**: Task board, approvals, execution chains, run evidence
- **Memory**: Per-agent memory health, searchability, and source file editing
- **Documents**: Shared and agent-core documents opened from actual source files
- **Settings**: Connector wiring status, security risk summary, update status

## Installation

```bash
git clone https://github.com/TianyiDataScience/openclaw-control-center.git
cd openclaw-control-center
npm install
cp .env.example .env
npm run build
npm test
npm run smoke:ui
npm run dev:ui
```

Open:
- `http://127.0.0.1:4310/?section=overview&lang=zh`
- `http://127.0.0.1:4310/?section=overview&lang=en`

> Use `npm run dev:ui` over `UI_MODE=true npm run dev` — more stable, especially on Windows shells.

## Project Structure

```
openclaw-control-center/
├── control-center/          # All modifications must stay within this directory
│   ├── src/
│   │   ├── runtime/         # Core runtime, connectors, monitors
│   │   └── ui/              # Frontend UI components
│   ├── .env.example
│   └── package.json
├── docs/
│   └── assets/              # Screenshots and documentation images
├── README.md
└── README.en.md
```

> **Critical constraint**: Only modify files inside `control-center/`. Never modify `~/.openclaw/openclaw.json`.

## Environment Configuration

Copy `.env.example` to `.env` and configure:

```env
# Security defaults — do NOT change without understanding implications
READONLY_MODE=true
LOCAL_TOKEN_AUTH_REQUIRED=true
IMPORT_MUTATION_ENABLED=false
IMPORT_MUTATION_DRY_RUN=false
APPROVAL_ACTIONS_ENABLED=false
APPROVAL_ACTIONS_DRY_RUN=true

# Connection
OPENCLAW_GATEWAY_URL=http://127.0.0.1:PORT
OPENCLAW_HOME=~/.openclaw

# UI
PORT=4310
DEFAULT_LANG=zh
```

### Security Flag Meanings

| Flag | Default | Effect |
|------|---------|--------|
| `READONLY_MODE` | `true` | All state-changing endpoints disabled |
| `LOCAL_TOKEN_AUTH_REQUIRED` | `true` | Import/export and write APIs require local token |
| `IMPORT_MUTATION_ENABLED` | `false` | Import mutations blocked entirely |
| `IMPORT_MUTATION_DRY_RUN` | `false` | Dry-run mode for imports when enabled |
| `APPROVAL_ACTIONS_ENABLED` | `false` | Approval actions hard-disabled |
| `APPROVAL_ACTIONS_DRY_RUN` | `true` | Approval actions run as dry-run when enabled |

## Key Commands

```bash
# Development
npm run dev:ui          # Start UI server (recommended)
npm run dev             # One-shot monitor run, no HTTP UI

# Build & Test
npm run build           # TypeScript compile
npm test                # Run test suite
npm run smoke:ui        # Smoke test the UI endpoints

# Lint
npm run lint            # ESLint check
npm run lint:fix        # Auto-fix lint issues
```

## TypeScript Code Examples

### Connecting to the Runtime Monitor

```typescript
import { createMonitor } from './src/runtime/monitor';

const monitor = createMonitor({
  gatewayUrl: process.env.OPENCLAW_GATEWAY_URL ?? 'http://127.0.0.1:4310',
  readonlyMode: process.env.READONLY_MODE !== 'false',
  localTokenAuthRequired: process.env.LOCAL_TOKEN_AUTH_REQUIRED !== 'false',
});

// Fetch current system overview
const overview = await monitor.getOverview();
console.log(overview.systemStatus);      // 'healthy' | 'degraded' | 'critical'
console.log(overview.pendingItems);      // number
console.log(overview.activeAgents);      // Agent[]
```

### Reading Agent Staff Status

```typescript
import { StaffConnector } from './src/runtime/connectors/staff';

const staff = new StaffConnector({ gatewayUrl: process.env.OPENCLAW_GATEWAY_URL });

// Get agents actively executing (not just queued)
const activeAgents = await staff.getActiveAgents();
activeAgents.forEach(agent => {
  console.log(`${agent.name}: ${agent.status}`);
  // 'executing' | 'queued' | 'idle' | 'blocked'
  console.log(`Current task: ${agent.currentTask?.title ?? 'none'}`);
  console.log(`Last output: ${agent.lastOutput}`);
});

// Get the full staff roster including queue depth
const roster = await staff.getRoster();
```

### Tracing Cross-Session Collaboration

```typescript
import { CollaborationTracer } from './src/runtime/connectors/collaboration';

const tracer = new CollaborationTracer({ gatewayUrl: process.env.OPENCLAW_GATEWAY_URL });

// Get parent-child session handoffs
const handoffs = await tracer.getSessionHandoffs();
handoffs.forEach(handoff => {
  console.log(`${handoff.parentSession} → ${handoff.childSession}`);
  console.log(`Delegated task: ${handoff.taskTitle}`);
  console.log(`Status: ${handoff.status}`);
});

// Get verified cross-session messages (e.g. Main ⇄ Pandas)
const crossSessionMessages = await tracer.getCrossSessionMessages();
crossSessionMessages.forEach(msg => {
  console.log(`${msg.fromAgent} ⇄ ${msg.toAgent}: ${msg.messageType}`);
  // messageType: 'sessions_send' | 'inter-session message'
});
```

### Fetching Token Usage and Spend

```typescript
import { UsageConnector } from './src/runtime/connectors/usage';

const usage = new UsageConnector({ gatewayUrl: process.env.OPENCLAW_GATEWAY_URL });

// Today's usage
const today = await usage.getUsageSummary('today');
console.log(`Tokens used: ${today.tokensUsed}`);
console.log(`Cost: $${today.costUsd.toFixed(4)}`);
console.log(`Context pressure: ${today.contextPressure}`);
// contextPressure: 'low' | 'medium' | 'high' | 'critical'

// Usage trend over 7 days
const trend = await usage.getUsageTrend(7);
trend.forEach(day => {
  console.log(`${day.date}: ${day.tokensUsed} tokens, $${day.costUsd.toFixed(4)}`);
});

// Token attribution by task (who ate the scheduled task tokens)
const attribution = await usage.getTokenAttribution();
attribution.tasks.forEach(task => {
  console.log(`${task.title}: ${task.tokensUsed} (${task.percentOfTotal}%)`);
});
```

### Reading Memory State

```typescript
import { MemoryConnector } from './src/runtime/connectors/memory';

const memory = new MemoryConnector({
  openclawHome: process.env.OPENCLAW_HOME ?? '~/.openclaw',
});

// Get memory health per active agent (scoped to openclaw.json)
const memoryState = await memory.getMemoryState();
memoryState.agents.forEach(agent => {
  console.log(`${agent.name}:`);
  console.log(`  Available: ${agent.memoryAvailable}`);
  console.log(`  Searchable: ${agent.memorySearchable}`);
  console.log(`  Needs review: ${agent.needsReview}`);
});

// Read daily memory for an agent
const dailyMemory = await memory.readDailyMemory('main-agent');
console.log(dailyMemory.content);

// Edit memory (requires READONLY_MODE=false and valid local token)
await memory.writeDailyMemory('main-agent', updatedContent, { token: localToken });
```

### Checking Wiring Status

```typescript
import { WiringChecker } from './src/runtime/connectors/wiring';

const wiring = new WiringChecker({ gatewayUrl: process.env.OPENCLAW_GATEWAY_URL });

const status = await wiring.getWiringStatus();
status.connectors.forEach(connector => {
  console.log(`${connector.name}: ${connector.status}`);
  // status: 'connected' | 'partial' | 'disconnected'
  if (connector.status !== 'connected') {
    console.log(`  Fix: ${connector.nextStep}`);
  }
});
```

### Approving Tasks (Gated Endpoint)

```typescript
import { TaskConnector } from './src/runtime/connectors/tasks';

const tasks = new TaskConnector({
  gatewayUrl: process.env.OPENCLAW_GATEWAY_URL,
  approvalActionsEnabled: process.env.APPROVAL_ACTIONS_ENABLED === 'true',
  approvalActionsDryRun: process.env.APPROVAL_ACTIONS_DRY_RUN !== 'false',
});

// This throws if APPROVAL_ACTIONS_ENABLED=false (default)
try {
  const result = await tasks.approveTask('task-id-123', { token: localToken });
  if (result.dryRun) {
    console.log('Dry run — no actual state change');
  }
} catch (err) {
  if (err.code === 'APPROVAL_ACTIONS_DISABLED') {
    console.log('Set APPROVAL_ACTIONS_ENABLED=true to enable approvals');
  }
}
```

## UI Section Navigation

Navigate via query params:

```
http://127.0.0.1:4310/?section=overview&lang=zh
http://127.0.0.1:4310/?section=usage&lang=en
http://127.0.0.1:4310/?section=staff&lang=zh
http://127.0.0.1:4310/?section=collaboration&lang=en
http://127.0.0.1:4310/?section=tasks&lang=zh
http://127.0.0.1:4310/?section=memory&lang=en
http://127.0.0.1:4310/?section=documents&lang=zh
http://127.0.0.1:4310/?section=settings&lang=en
```

Sections: `overview` | `usage` | `staff` | `collaboration` | `tasks` | `memory` | `documents` | `settings`

Languages: `zh` (Chinese, default) | `en` (English)

## Integration Patterns

### Embedding in an Existing OpenClaw Workflow

If your OpenClaw agent needs to hand off instructions to the control center for setup, use the documented install block:

```typescript
// In your OpenClaw agent task
const installInstructions = `
cd openclaw-control-center
npm install
cp .env.example .env
# Edit .env: set OPENCLAW_GATEWAY_URL and OPENCLAW_HOME
npm run build && npm test && npm run dev:ui
`;
```

### Adding a Custom Connector

All connectors live in `control-center/src/runtime/connectors/`. Follow this pattern:

```typescript
// control-center/src/runtime/connectors/my-connector.ts
import { BaseConnector, ConnectorOptions } from './base';

export interface MyData {
  id: string;
  value: string;
}

export class MyConnector extends BaseConnector {
  constructor(options: ConnectorOptions) {
    super(options);
  }

  async getData(): Promise<MyData[]> {
    // Always check readonly mode for any write operation
    this.assertNotReadonly('getData is readonly-safe');

    const response = await this.fetch('/api/my-endpoint');
    return response.json() as Promise<MyData[]>;
  }
}
```

### Custom UI Section

```typescript
// control-center/src/ui/sections/MySection.tsx
import React from 'react';
import { useConnector } from '../hooks/useConnector';
import { MyConnector } from '../../runtime/connectors/my-connector';

export const MySection: React.FC = () => {
  const { data, loading, error } = useConnector(MyConnector, 'getData');

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {data?.map(item => (
        <li key={item.id}>{item.value}</li>
      ))}
    </ul>
  );
};
```

## Troubleshooting

### "Missing src/runtime" or "Missing core source"

This almost always means the working directory is wrong:

```bash
# Ensure you're in the repo root
pwd  # should end in /openclaw-control-center
ls control-center/src/runtime  # should exist
```

If cloned correctly but still missing: the clone was incomplete. Re-clone:

```bash
git clone https://github.com/TianyiDataScience/openclaw-control-center.git
```

### UI Doesn't Start / Port Conflicts

```bash
# Check if port 4310 is in use
lsof -i :4310
# or on Windows
netstat -ano | findstr :4310

# Change port in .env
PORT=4311
```

### Data Not Showing (Partial or Empty Sections)

1. Open `Settings` → **接线状态** (Wiring Status) — it lists exactly which connectors are connected, partial, or missing.
2. Common causes:
   - `OPENCLAW_GATEWAY_URL` not set or wrong port
   - `OPENCLAW_HOME` doesn't point to actual `~/.openclaw`
   - OpenClaw subscription snapshot not at default path

### Token Auth Failures

```bash
# Generate a local token (see openclaw docs for token location)
cat ~/.openclaw/local-token

# Pass via header in API calls
curl -H "X-Local-Token: <token>" http://127.0.0.1:4310/api/tasks/approve
```

### Approval Actions Silently Do Nothing

Check your `.env`:

```env
APPROVAL_ACTIONS_ENABLED=true   # Must be true
APPROVAL_ACTIONS_DRY_RUN=false  # Must be false for real execution
```

Both must be explicitly set. Default is disabled + dry-run.

### Memory Section Shows Inactive Agents

The memory section is scoped to agents listed in `openclaw.json`. If deleted agents still appear:

```bash
# Check active agents
cat ~/.openclaw/openclaw.json | grep -A5 '"agents"'
```

Remove stale entries from `openclaw.json` — the memory section will update on next load.

### Windows Shell Issues

Prefer `npm run dev:ui` over `UI_MODE=true npm run dev`. Cross-env variable setting behaves differently in PowerShell/CMD. The `dev:ui` script handles this internally.

## Prerequisites

- Node.js + npm
- A running OpenClaw installation with accessible Gateway
- Read access to `~/.openclaw` on the local machine
- (Optional) `~/.codex` and OpenClaw subscription snapshot for full usage data
